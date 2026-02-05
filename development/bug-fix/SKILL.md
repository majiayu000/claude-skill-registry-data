---
name: bug-fix
description: Bug 修復流程。當用戶提到「bug」「錯誤」「問題」「修復」「fix」「壞掉」等關鍵字時自動使用。
---

# Bug 修復流程

## 觸發條件

當用戶提問包含以下關鍵字時自動啟用：
- 「bug」「錯誤」「問題」「修復」「fix」「壞掉」

## Bug 類型判斷

在開始修復前，**必須先判斷 Bug 類型**：

### 類型 A：純後端 Bug
**特徵**：
- 商業邏輯錯誤、資料處理問題
- Service、Repository、Model 層的錯誤
- 例如：資料計算錯誤、驗證規則失效、資料庫查詢問題

**執行流程**：
```
Sequential Thinking → /impact-analysis → /tdd → coder → reviewer
```

### 類型 B：純前端 Bug
**特徵**：
- 頁面顯示問題、樣式錯誤
- Blade 視圖、組件的問題
- 例如：排版錯亂、按鈕失效、表單顯示異常

**執行流程**：
```
Sequential Thinking → /impact-analysis → /components → ui-designer → coder → reviewer
```

### 類型 C：全端 Bug
**特徵**：
- 同時涉及後端邏輯和前端顯示
- 資料傳遞或渲染的問題
- 例如：資料未正確顯示、表單提交失敗

**執行流程**：
```
Sequential Thinking → /impact-analysis → /tdd → ui-designer → coder → reviewer
```

## 快速判斷清單

在開始前，回答以下問題：

```
□ Bug 發生在資料處理層？ → 後端 Bug
□ Bug 發生在商業邏輯？ → 後端 Bug
□ Bug 發生在頁面顯示？ → 前端 Bug
□ Bug 發生在樣式/排版？ → 前端 Bug
□ 資料正確但顯示錯誤？ → 前端 Bug
□ 顯示正確但資料錯誤？ → 後端 Bug
□ 兩者都有問題？ → 全端 Bug
```

## 執行流程

### 1. Sequential Thinking - 分析問題

分析問題根因：
- **現象**：Bug 的具體表現？
- **預期行為**：正確行為應該是什麼？
- **重現步驟**：如何重現？
- **Bug 類型**：後端 / 前端 / 全端？
- **根因假設**：可能的原因？

### 2. 影響範圍分析

執行 `/impact-analysis` 評估修改影響範圍。

### 3. 測試重現（後端 Bug 適用）

若涉及後端 Bug，執行 `/tdd` 撰寫失敗測試來重現 Bug。

### 4. 組件確認（前端 Bug 適用）

若涉及前端 Bug，執行 `/components` 確認可用的共用組件。

### 5. 修復

根據 Bug 類型使用對應的 agent：

| Bug 類型 | 使用 Agent |
|---------|-----------|
| 純後端 | coder |
| 純前端 | ui-designer → coder |
| 全端 | ui-designer → coder |

### 6. 審查

使用 `reviewer agent` 審查修復品質。

## 修復原則

- **最小修改**：只改必要的程式碼
- **避免副作用**：不引入新問題
- **測試驗證**：確保修復有效且無回歸

## 品質要求

- **NEVER** 不寫測試就修復後端 Bug
- **ALWAYS** 執行完整測試確認無回歸
- 前端修復必須確認共用組件的正確使用
- 必須經過 reviewer 審查
