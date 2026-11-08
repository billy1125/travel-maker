---
name: source-document-extraction
description: 把旅遊相關 PDF（電子機票、訂房確認單、車站構造圖等）擷取成 Markdown，存在原 PDF 旁邊供 Read 讀取。Read 工具讀不了 PDF 時使用。
---

# PDF 文字擷取

本環境沒有 `pdftoppm`，Read 工具無法直接讀 PDF。這個技能用 `scripts/extract_pdf.py` 把 PDF 轉成 Markdown，再用 Read 讀。

## 輸出位置

預設輸出到原 PDF 的同一個資料夾，檔名與 PDF 相同，副檔名改成 `.md`（例：`assets/ticket.pdf` → `assets/ticket.md`）。`--raw` 輸出 `.txt`，`--figures` 輸出 `<檔名>-p<頁碼>.png`。

- 原 PDF 只讀，不改、不搬移
- 同名 `.md` 已存在時，先問使用者要不要覆寫

## 步驟

1. **找可用的 Python**：環境名稱不限，只要能 `import pymupdf, pymupdf4llm` 就可以用。依序試下面的路徑，用第一個通過的：

   ```bash
   for py in "${SDE_PYTHON:-}" ~/miniconda3/envs/*/python.exe ~/anaconda3/envs/*/python.exe ~/miniforge3/envs/*/python.exe \
             ~/miniconda3/envs/*/bin/python ~/anaconda3/envs/*/bin/python ~/miniforge3/envs/*/bin/python; do
     [ -x "$py" ] && "$py" -c "import pymupdf, pymupdf4llm" 2>/dev/null && { echo "$py"; break; }
   done
   ```

   都不通過時，請使用者依 repo 根目錄 `README.md` 的「建議的 conda 環境」建立環境，不自行安裝套件。

2. **執行腳本**（`PY` 是步驟 1 找到的路徑，`SCRIPTS` 是本技能的 `scripts/`）：

   ```bash
   "$PY" SCRIPTS/extract_pdf.py "assets/xxx.pdf"
   ```

3. **用 Read 讀產出的 `.md`**，回報輸出路徑後接續原本的工作。

## 旗標

| 旗標 | 作用 |
|------|------|
| `--pages 1-3,5` | 只擷取指定頁（從 1 起算） |
| `--margins N` | 每頁上下各裁掉 N 點，去掉頁首頁尾 |
| `--no-clean` | 不清理，保留 pymupdf4llm 原始輸出 |
| `--raw` | 輸出純文字 `.txt`，每頁前加 PAGE 標記；表格或版面錯亂時用來對照 |
| `--figures` | 把指定頁轉成 PNG，用 Read 看圖（車站構造圖、文字擷取讀不到的版面）；要搭配 `--pages` |
| `--figure-dpi N` | `--figures` 的解析度，預設 150 |
| `-o path` | 指定輸出路徑 |

預設清理會移除反引號、粗體、HTML 標籤、頁分隔、單獨的頁碼行與跨頁重複的頁首頁尾，標題最多保留 5 層。清理只動標記，不刪內文。

## 注意

- 擷取結果中的確認碼、訂位代號、日期、金額，引用前要和 `--raw` 或 `--figures` 對照一次，避免版面解析錯位
- Windows 終端是 cp950，腳本只把結果寫進 UTF-8 檔案，不要改成 print 到終端
