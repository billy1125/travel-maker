# Travelmaker

個人旅遊規劃資料庫的通用框架。每趟行程是 `travels/` 底下一個獨立的行程專案，用 Claude Code 搭配專案內的技能來討論、更新行程。

## 資料夾結構

| 路徑 | 說明 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | 所有行程專案共用的規範 |
| `.claude/` | 所有行程專案共用的技能與權限設定 |
| `travels/` | 行程專案，git 不追蹤 |
| [travels/_template/](travels/_template/) | 新行程專案的範本（git 追蹤） |

每個行程專案的內容：

| 路徑 | 說明 |
|---|---|
| `CLAUDE.md` | 該行程專屬的資訊與規則（日期、目的地、當地語言名稱寫法等） |
| `README.md` | 該行程的索引：每日行程、交通、旅宿、攝影景點的連結表 |
| `itinerary.md` | 行程總覽：航班、住宿分段、每日摘要表格與**行程原則** |
| `days/` | 每日行程細節，檔名 `yyyyMMDD.md` |
| `transportations/` | 交通節點指南：路段、單一車站、市內交通系統 |
| `hotel/` | 旅宿指南：訂房事實、館內設施、聯絡信件與館方回信 |
| `photospots/` | 攝影景點，一個城市一個檔案 |
| `assets/` | 電子機票、訂房確認單等 PDF，以及網址索引 `reference_website.md`、網站摘要 `website_abstract.md` |
| `luggage_items.md` | 行李清單 |
| `archive/{YYYYMMDD-HHMM}/` | 每次行程異動前的自動備份（唯讀） |

## 新增行程

1. 把 `travels/_template/` 整個複製成 `travels/{行程名稱}/`（例：`travels/Japan-2026/`）
2. 填寫新專案的 `CLAUDE.md`、`README.md`、`itinerary.md`

## 使用方式

指明要操作的行程專案後，執行 `/discuss-itinerary` 開始行程討論；討論後執行 `/update-itinerary` 同步更新檔案。詳見 [CLAUDE.md](CLAUDE.md)。

## 環境需求

這個專案本身不需要建置或安裝任何東西——內容全是 Markdown。**唯一需要外部套件的情境是讀行程專案 `assets/` 裡的 PDF**（訂房確認單、電子機票、車站構造圖）：

| 用途 | 套件 | 說明 |
|---|---|---|
| 從 PDF 抽出文字 | **PyMuPDF**（`import fitz` 或 `import pymupdf`） | `pip install pymupdf`。本環境沒有 `pdftoppm`，Claude Code 的 Read 工具也讀不了 PDF，只能靠這個抽成 `.txt` 再讀 |

執行方式由**使用者手動處理**：`.claude/settings.json` 禁止直接執行 `python`／`pip`，也沒有預先允許的 conda 規則。Claude 遇到需要讀 PDF 時會先詢問，不自行選擇執行環境。
