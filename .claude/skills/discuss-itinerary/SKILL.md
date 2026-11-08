---
name: discuss-itinerary
description: 行程討論前的準備步驟：讀取全部行程與參考資源，再進行有根據的討論
allowed-tools: Read Glob WebFetch WebSearch
---

每次討論行程前執行此技能，確保討論有完整的現有行程資料、交通指南與參考資源作為基礎，不憑空推測。

> **作用範圍**：本技能中行程檔案的路徑（`itinerary.md`、`days/`、`assets/` 等）都相對於本次操作的行程專案 `travels/{行程名稱}/`。執行前先確認是哪個行程專案，使用者沒指明就先問；不對 `travels/_template/` 執行。

## 執行步驟

### 1. 讀取總行程與資源索引

讀取以下檔案：

- `itinerary.md` — 總行程概覽（各日住宿、主題、行程原則）
- `assets/reference_website.md` — 可用參考網站清單（交通、美食、購物、景點）
- `assets/website_abstract.md` — 已整理的網站摘要（若檔案存在則讀取）

### 2. 讀取交通指南

用 Glob 列出 `transportations/` 內的所有 `.md` 檔案，並逐一讀取。

### 3. 讀取每日行程

讀取 `days/` 內所有 `.md` 檔案（含同一日拆成多案的 `yyyyMMDD-{slug}.md`）。

### 4. 向使用者報告已就緒，摘要現況

完成讀取後，向使用者簡報：

- **行程架構**：各日住宿城市、主題、確認景點、雨天備案
- **已整備的交通資料**：列出 `transportations/` 已有哪些路段的指南
- **可用參考資源**：列出 `assets/reference_website.md` 中與本次討論主題相關的連結

格式簡潔，一目了然即可，不需逐字重述每日細節。

### 5. 進入討論

詢問使用者想討論或調整的主題，並根據步驟 1–3 讀取的資料進行有根據的回應。

若使用者提供外部網址補充資料，使用 WebFetch 抓取後再納入討論。
若需要查詢即時資訊（如票價、時刻表），使用 WebSearch。

## 討論中的原則

- 未完成步驟 1–3 的讀取前，不進行任何行程建議或修改
- 行程建議需對應到具體的 `days/yyyyMMDD.md` 或 `itinerary.md` 的現有內容
- 每次討論結束，若有任何行程變動，提醒使用者執行 `/update-itinerary` 同步檔案
- 若本次討論中有抓取新網站內容，提醒使用者執行 `/save-website-abstract`（整理至 `assets/website_abstract.md`）
- 所有討論使用繁體中文
