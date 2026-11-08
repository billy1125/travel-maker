---
name: save-website-abstract
description: 將討論中抓取的新網站內容整理成摘要，寫入 assets/website_abstract.md
allowed-tools: Read Write Edit Glob WebFetch mcp__twinkle-hub__twtools-fetch_url_as_markdown
---

討論結束後，針對本次討論中實際閱讀過、且在 `assets/reference_website.md` 中**沒有出現過**的網站，整理摘要並歸入 `assets/website_abstract.md`。

> **作用範圍**：本技能中的 `assets/` 路徑相對於本次操作的行程專案 `travels/{行程名稱}/`；`reference/` 仍相對於此 SKILL.md 所在目錄。執行前先確認是哪個行程專案，使用者沒指明就先問；不對 `travels/_template/` 執行。

## 執行步驟

### 1. 確認本次討論抓取的新網站

回顧本次對話，列出所有使用 WebFetch 讀取過的網址，並與 `assets/reference_website.md` 比對：

- 讀取 `assets/reference_website.md` 取得已知 URL 清單
- 列出**未曾出現在 reference_website.md** 的新 URL
- 若所有 URL 都已在 reference_website.md 中，**仍繼續執行**——已知 URL 若尚未有摘要，同樣需要整理

### 2. 讀取格式規範

讀取 `reference/website_abstract_format.md`（相對於此 SKILL.md 所在目錄），了解摘要格式。

### 3. 確認或建立 assets/website_abstract.md

- 讀取 `assets/website_abstract.md`（若存在）
- 若檔案不存在，依 `reference/website_abstract_format.md` 的範本建立初始結構（含六個空白分類區塊）

### 4. 為每個新網站撰寫摘要

針對每個需要整理的 URL：

1. **判斷分類**（交通 / 美食 / 購物 / 景點 / 住宿 / 行李準備）  
   若網站涵蓋多類，選最主要的分類；在「適用範圍」欄位說明其他面向。
   旅館官網與訂房頁歸「住宿」，但**細節寫進 `hotel/` 的旅宿指南，這裡只留摘要**。

2. **撰寫摘要條目**，格式如下：

   ```
   ### [標題](URL)

   **整理日：** YYYY/MM/DD（今日日期）
   **適用範圍：** {此資料適用的路段、城市或行程日}

   - {重點 1}
   - {重點 2}
   - {重點 3}
   ```

   摘要重點要求：
   - 3–5 條，每條寫對旅程有用的**具體事實**（數字、名稱、注意事項）
   - 不寫廣告語或空泛的讚美
   - 若內容已在本次對話中讀取，直接從記憶中整理；若需補充細節，優先使用 `mcp__twinkle-hub__twtools-fetch_url_as_markdown` 重新讀取，失敗再改用 WebFetch

   **⚠️ 抓取失敗的處理（403 / 逾時 / 無內容）：**
   - 若兩種工具均無法取得內容，**跳過該 URL，不寫入摘要**
   - 在步驟 6 的回報中，將該 URL 列為「無法取得」並說明原因
   - 不以空白或錯誤內容建立條目

3. **防止重複**：若該 URL 已存在於 `website_abstract.md`，跳過，不重複寫入。

### 5. 寫入 assets/website_abstract.md

將各條目寫入對應的分類區塊（交通 / 美食 / 購物 / 景點 / 住宿 / 行李準備）：

- 用 Edit 工具將新條目插入對應分類區塊的末尾
- 更新檔案頂部的「更新日」為今日日期
- 若某分類區塊原本只有「（待整理）」，移除該佔位文字後再插入條目

### 6. 回報結果

完成後條列：
- 新增了哪幾個條目（標題、分類、URL）
- 哪些 URL 因已存在於摘要而跳過
- 哪些 URL 因無法取得內容（403 / 逾時）而跳過，供使用者知悉
- 提醒使用者：若這些網站還沒加入 `assets/reference_website.md`，可自行補充（該檔案由使用者維護）

## 限制

- **不修改** `assets/reference_website.md`（由使用者維護）
- **不修改** `reference/website_abstract_format.md`
- 所有文字使用繁體中文
