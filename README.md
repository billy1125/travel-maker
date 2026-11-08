# travel-maker

一套用於自助旅行規劃的 Claude Code skill suite，以 Markdown 建立個人旅遊規劃資料庫。每趟行程是 `travels/` 底下一個獨立的行程專案，涵蓋行程總覽、每日行程、交通節點（機場、車站、市內交通）、旅宿指南與聯絡信件、攝影景點與行李清單。行程討論、更新與查證都透過 Claude Code 技能進行，每次異動前自動備份。以繁體中文為主，AI 負責整理與查證，行程決定與資料確認由使用者負責。

## ⚠ 使用須知

> 使用前請先閱讀以下事項。

- **範圍**：本專案只提供資料夾架構、格式規範與 Claude Code 技能，不提供任何實際行程內容。
- **資訊需自行查證**：營業時間、票價、班次、公休日都會變動。技能會用網路查證，但查證結果不保證正確或即時，出發前請以官方公告為準。
- **訂房事實以確認單為準**：確認碼、日期、房價、取消政策一律以 `assets/` 的訂房確認單 PDF 為準，網路查到的資料不覆蓋它。
- **確認狀態由使用者決定**：每日行程的「已確認」橫幅只由使用者加上，Claude 不代填。
- **Use at your own risk**：本專案為個人用途，不保證內容正確與完整。

## 技能一覽

技能放在 [.claude/skills/](.claude/skills/)，所有行程專案共用。

| 技能 | 做什麼 | 產物 |
|---|---|---|
| `discuss-itinerary` | 討論前讀完全部行程、交通指南與參考資源 | （只讀，不寫檔） |
| `update-itinerary` | 歸檔舊版後，同步更新行程總覽與每日行程；只能由使用者呼叫 | `itinerary.md`、`days/`、`archive/` |
| `build-transportation` | 盤點機場、車站、港口、巴士站等交通節點，查證後建立或補充指南 | `transportations/` |
| `build-hotel` | 盤點旅宿，建立旅宿指南、英文與當地語言聯絡信件，並整理館方回信 | `hotel/` |
| `save-website-abstract` | 把討論中抓取過的網站整理成摘要 | `assets/website_abstract.md` |
| `tw-opendata-transportation` | 查詢台灣交通部 OpenData（台鐵、高鐵、捷運、客運、民航）；預設不呼叫 | （查詢結果） |

各技能的執行細節見各自的 `SKILL.md`，共用規範見 [CLAUDE.md](CLAUDE.md)。

## 快速開始

```
討論 Japan-2026 的行程          → /discuss-itinerary
把剛剛討論的異動寫進行程        → /update-itinerary
補齊這趟行程的車站與機場指南    → /build-transportation
建立旅館指南與聯絡信件          → /build-hotel
整理這次查過的網站              → /save-website-abstract
```

呼叫技能時要指明行程專案（例：`Japan-2026`），沒指明時 Claude 會先問。

## 基本使用流程

1. 把 [travels/_template/](travels/_template/) 整個複製成 `travels/{行程名稱}/`，名稱用英文，例：`travels/Japan-2026/`
2. 填寫新專案的 `CLAUDE.md`（日期、目的地、當地語言、幣別、國碼、名稱寫法）、`README.md`、`itinerary.md`
3. 執行 `/discuss-itinerary` 讀取資料後開始討論；需要即時資訊時由 Claude 用網路查證
4. 有行程異動時執行 `/update-itinerary`；有新交通節點或旅宿時接著執行 `/build-transportation`、`/build-hotel`
5. 本次討論抓取過網站，就執行 `/save-website-abstract`

## 前置需求

1. **Claude Code**：所有技能都在 Claude Code 內執行。
2. **PyMuPDF**（選用）：只有讀 `assets/` 的 PDF（訂房確認單、電子機票、車站構造圖）時需要，`pip install pymupdf`。本環境沒有 `pdftoppm`，Claude Code 的 Read 工具也讀不了 PDF，只能先抽成文字再讀。
3. **Twinkle Hub MCP**（選用）：只有使用 `tw-opendata-transportation` 時需要。

這個專案本身不需要建置或安裝，內容全是 Markdown。`.claude/settings.json` 禁止直接執行 `python`／`pip`，Claude 遇到需要讀 PDF 時會先詢問，由使用者手動執行。

## 設計要點

- **三層結構**：`itinerary.md`（總覽與行程原則）→ `days/`（每日細節）→ `transportations/`、`hotel/`（由每日檔案連結），改動時同層與跨層一起維持一致。
- **行程原則優先**：硬性限制（出發時間、住宿不換點、班機緩衝等）寫在 `itinerary.md` 的「行程原則」，任何調整先對照這一節。
- **異動前自動備份**：`/update-itinerary` 在每次改動前把舊版留在 `archive/{YYYYMMDD-HHMM}/`，備份唯讀。
- **框架與行程分離**：共用規範與技能放在 repo 根目錄；行程專屬資訊寫在各行程專案的 `CLAUDE.md`。`travels/` 不進 git，只追蹤 `_template/`。

## 目錄結構

```
travel-maker/
├── CLAUDE.md                     # 所有行程專案共用的規範
├── README.md
├── LICENSE                       # CC BY-NC 4.0
├── NOTICE                        # 第三方元件與授權
├── .claude/
│   ├── settings.json             # 權限設定
│   └── skills/                   # 共用技能
│       ├── discuss-itinerary/
│       ├── update-itinerary/
│       │   └── reference/        # 行程、每日、交通、旅宿格式規範
│       ├── build-transportation/
│       ├── build-hotel/
│       ├── save-website-abstract/
│       │   └── reference/        # 網站摘要格式規範
│       └── tw-opendata-transportation/   # 第三方元件，Apache-2.0
└── travels/                      # 行程專案（git 不追蹤）
    ├── _template/                # 新行程專案的範本（git 追蹤）
    └── {行程名稱}/
        ├── CLAUDE.md             # 該行程專屬的資訊與規則
        ├── README.md             # 該行程的索引
        ├── itinerary.md          # 航班、住宿分段、每日摘要與行程原則
        ├── days/                 # 每日行程，檔名 yyyyMMDD.md
        ├── transportations/      # 路段、單一車站、市內交通系統
        ├── hotel/                # 旅宿指南、聯絡信件、館方回信
        ├── photospots/           # 攝影景點，一個城市一個檔案
        ├── assets/               # 電子機票、訂房確認單、網址索引、網站摘要
        ├── luggage_items.md      # 行李清單
        └── archive/              # 異動前的自動備份（唯讀）
```

## 交接鏈

```
/discuss-itinerary ─→ 討論與查證 ─→ /update-itinerary ─→ /build-transportation
                          │                                （有新交通節點時接續）
                          ├─→ /build-hotel（有新旅宿或訂房變動時）
                          └─→ /save-website-abstract（抓取過網站時）
```

## 已知限制

- Claude Code 無法直接讀 PDF，訂房確認單等資料需要使用者先用 PyMuPDF 抽出文字。
- `tw-opendata-transportation` 只有批次資料，不含即時到站、誤點資訊。

## 📄 授權 / License

本專案以 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)（姓名標示－非商業性 4.0 國際）授權，全文見 [LICENSE](LICENSE)。可以複製、修改與再散布，但須標示出處，且不得用於商業目的。

Copyright (c) 2026 Cho-Hsun Lu (billy1125)

**例外：第三方元件不適用本授權**，各自保留原授權，詳見 [NOTICE](NOTICE)：

| 元件 | 來源 | 授權 |
|---|---|---|
| [`tw-opendata-transportation`](.claude/skills/tw-opendata-transportation/) | 外部取得 | Apache License 2.0（[全文](.claude/skills/tw-opendata-transportation/LICENSE)）；查詢的資料適用政府資料開放授權條款第 1 版 |
