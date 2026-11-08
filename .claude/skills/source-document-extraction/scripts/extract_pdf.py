# -*- coding: utf-8 -*-
"""Extract text from a PDF into clean Markdown (UTF-8 file).

Default: pymupdf4llm -> Markdown, then light cleanup (strip backticks, bold,
HTML tags, page separators, lone page numbers, repeated headers/footers;
cap heading depth at 5). Output goes next to the PDF as <stem>.md unless -o
is given.

Usage:
    PY scripts/extract_pdf.py input.pdf                 # -> input.md
    PY scripts/extract_pdf.py input.pdf --pages 1-2     # selected pages
    PY scripts/extract_pdf.py input.pdf --raw           # plain text -> input.txt
    PY scripts/extract_pdf.py input.pdf --figures --pages 3   # page PNGs
    PY scripts/extract_pdf.py input.pdf -o out/x.md

PY is any Python that can `import pymupdf, pymupdf4llm`.
Results are written to files, never printed, to avoid cp950 errors on
Windows terminals. Status lines on stderr are ASCII-only.
"""
import argparse
import os
import re
import sys
import unicodedata
from collections import Counter

import pymupdf as fitz  # PyMuPDF; `import fitz` is deprecated

_HTML_TAG = re.compile(r"<!--.*?-->|</?[a-zA-Z][^>]*>")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_USCORE = re.compile(r"__(.+?)__")
_PAGE_SEP = re.compile(r"^\s*-{3,}\s*end of page.*$", re.I)
_NUM_ONLY = re.compile(r"^\s*\d{1,4}\s*$")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_TRAIL_NUM = re.compile(r"\s*\d{1,4}\s*$")
_WS = re.compile(r"\s+")
_MAX_HEADING = 5


def normalize(s: str) -> str:
    """Collapse spaces and drop a trailing page number."""
    return _WS.sub(" ", _TRAIL_NUM.sub("", s.strip())).strip()


def detect_running(doc, indices: list[int], min_repeat: int,
                   band: int = 3) -> set[str]:
    """Find header/footer lines repeated across pages (first/last `band` lines)."""
    counts: Counter[str] = Counter()
    for i in indices:
        lines = [s.strip() for s in doc[i].get_text().splitlines() if s.strip()]
        for s in lines[:band] + lines[-band:]:
            n = normalize(s)
            if len(n) >= 4 and any(ch.isalnum() for ch in n):
                counts[n] += 1
    return {n for n, c in counts.items() if c >= min_repeat}


def _running_lines(lines: list[str], min_repeat: int) -> set[str]:
    """Find whole lines repeated in the Markdown (skip headings, tables, lists)."""
    counts: Counter[str] = Counter()
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith(("#", "|", "-")):
            continue
        n = normalize(s)
        if len(n) >= 6 and any(c.isalnum() for c in n):
            counts[n] += 1
    return {n for n, c in counts.items() if c >= min_repeat}


_KANGXI = re.compile(r"[⼀-⿟]")


def _strip_inline(s: str) -> str:
    # Kangxi radicals (e.g. U+2FB6) -> normal CJK chars (e.g. U+98DB)
    s = _KANGXI.sub(lambda m: unicodedata.normalize("NFKC", m.group()), s)
    s = _HTML_TAG.sub("", s)
    s = s.replace("`", "")
    s = _BOLD.sub(r"\1", s)
    s = _USCORE.sub(r"\1", s)
    return s.replace("**", "")


def clean_markdown(md: str, page_count: int, boilerplate: set[str]) -> str:
    """Light, text-preserving cleanup of pymupdf4llm output."""
    src = [_strip_inline(l).rstrip() for l in md.split("\n")]
    min_repeat = max(3, page_count // 2)
    boiler = boilerplate | _running_lines(src, min_repeat)
    # header text may be glued to the start of a paragraph: strip as prefix
    prefixes = [re.compile(r"^\s*" + re.escape(b) + r"\s*\d{0,4}\s*")
                for b in boiler if b]

    out: list[str] = []
    for line in src:
        if _PAGE_SEP.match(line):
            continue
        for _ in range(6):  # multi-part headers need repeated passes
            changed = False
            for pat in prefixes:
                new = pat.sub("", line, count=1)
                if new != line:
                    line, changed = new, True
            if not changed:
                break
        line = line.rstrip()
        h = _HEADING.match(line)
        if h:
            text = h.group(2).strip()
            out.append("#" * min(len(h.group(1)), _MAX_HEADING) + " " + text
                       if text else "")
            continue
        if _NUM_ONLY.match(line):
            continue
        if line == "" and out and out[-1] == "":
            continue
        out.append(line)
    return "\n".join(out).strip() + "\n"


def parse_pages(spec: str, page_count: int) -> list[int]:
    """'5-8,10' -> 0-based page indices."""
    pages: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages.extend(range(int(a) - 1, int(b)))
        else:
            pages.append(int(part) - 1)
    return [p for p in pages if 0 <= p < page_count]


def ascii_safe(s: str) -> str:
    return s.encode("ascii", "replace").decode("ascii")


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract PDF text to Markdown")
    ap.add_argument("pdf", help="PDF path")
    ap.add_argument("--pages", help="1-based pages, e.g. '1-3,5'; default all")
    ap.add_argument("--margins", type=float, default=0,
                    help="crop N points from top and bottom of each page")
    ap.add_argument("--no-clean", action="store_true",
                    help="keep raw pymupdf4llm Markdown")
    ap.add_argument("--raw", action="store_true",
                    help="plain text with PAGE markers (.txt)")
    ap.add_argument("--figures", action="store_true",
                    help="render selected pages to PNG instead of text")
    ap.add_argument("--figure-dpi", type=int, default=150,
                    help="DPI for --figures (default 150)")
    ap.add_argument("-o", "--out",
                    help="output path; default <pdf dir>/<stem>.md (or .txt)")
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    indices = (parse_pages(args.pages, doc.page_count)
               if args.pages else list(range(doc.page_count)))
    stem = os.path.splitext(os.path.basename(args.pdf))[0]
    ext = ".txt" if args.raw else ".md"
    out = args.out or os.path.join(os.path.dirname(args.pdf), stem + ext)
    out_dir = os.path.dirname(out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    if args.figures:
        for i in indices:
            doc[i].get_pixmap(dpi=args.figure_dpi).save(
                os.path.join(out_dir or ".", f"{stem}-p{i + 1}.png"))
        print(f"done -> {ascii_safe(out_dir or '.')} ({len(indices)} figures)",
              file=sys.stderr)
        return

    if args.raw:
        content = "".join(f"\n========== PAGE {i + 1} ==========\n"
                          + doc[i].get_text() for i in indices)
    else:
        try:
            import pymupdf4llm
        except ImportError:
            sys.stderr.write("error: pymupdf4llm not installed in this Python.\n")
            sys.exit(1)
        md = pymupdf4llm.to_markdown(doc, pages=indices, page_separators=False,
                                     margins=args.margins, ignore_code=True)
        if args.no_clean:
            content = md
        else:
            boiler = detect_running(doc, indices, max(3, len(indices) // 2))
            content = clean_markdown(md, len(indices), boiler)

    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"done -> {ascii_safe(out)} ({len(indices)} pages)", file=sys.stderr)


if __name__ == "__main__":
    main()
