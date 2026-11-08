# {行程名稱}

{YYYY} {目的地}旅遊規劃（{N} 天 {N} 晚，{MM/DD}–{MM/DD}）

## 行程概要

- **去程：** {航班號}｜{MM/DD} {HH:MM} {出發機場} → {HH:MM} {抵達機場}
- **回程：** {航班號}｜{MM/DD} {HH:MM} {出發機場} → {HH:MM} {抵達機場}
- **訂位代號：** {訂位代號}
- **住宿：** {城市} {N} 晚（{旅宿}）→ {城市} {N} 晚（{旅宿}）

## 總行程

- **[itinerary.md](itinerary.md)** — 主行程總覽：航班、住宿分段、每日摘要表格與**行程原則**

## 每日行程

| 日期 | 住宿 | 主題 |
|---|---|---|
| [{MM/DD}（Day 1）](days/{yyyyMMDD}.md) | {城市} | {主題} |

各日檔案開頭的橫幅代表查證進度，分兩級：`> ✅ **YYYY.MM.DD 資訊已初步確認**` 是營業時間、票價與班次已逐項查過一輪；`> ✅ **YYYY.MM.DD 資訊已確認**` 是完整確認、內容不會再改。沒有橫幅的日子尚未查證。

## 交通資訊

| 檔案 | 內容 |
|---|---|

完整清單見 [transportations/README.md](transportations/README.md)。

## 旅宿資訊

| 檔案 | 內容 |
|---|---|

旅宿指南的訂房事實（確認碼、日期、房型、房價、取消政策）一律以 `assets/` 的訂房確認單 PDF 為準。總覽見 [hotel/README.md](hotel/README.md)。

## 攝影景點

| 檔案 | 內容 |
|---|---|

總覽見 [photospots/README.md](photospots/README.md)。

## 其他資料

| 路徑 | 說明 |
|---|---|
| [luggage_items.md](luggage_items.md) | 行李清單 |
| [shopping.md](shopping.md) | 購物指南：平日採買據點與紀念品 |
| [assets/reference_website.md](assets/reference_website.md) | 參考網站索引（由使用者維護） |
| [assets/website_abstract.md](assets/website_abstract.md) | 參考網站摘要，依交通／美食／購物／景點／住宿／行李準備分類 |
| `assets/*.pdf` | 電子機票、訂房確認單等 |
| `archive/{YYYYMMDD-HHMM}/` | 每次行程異動前的自動備份（唯讀） |

## 使用方式

在 Claude Code 中執行 `/discuss-itinerary` 開始行程討論；討論後執行 `/update-itinerary` 同步更新檔案。詳見 [CLAUDE.md](CLAUDE.md) 與 repo 根目錄的 [CLAUDE.md](../../CLAUDE.md)；讀 PDF 的環境需求見根目錄 [README.md](../../README.md)。
