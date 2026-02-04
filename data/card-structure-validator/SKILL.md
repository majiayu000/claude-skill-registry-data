---
name: card-structure-validator
description: |
  檢驗日文學習卡片的結構完整性和格式正確性。
  使用時機：
  - 當需要檢查卡片的 YAML frontmatter 格式
  - 當需要驗證卡片區塊（解釋、例句、相關連結）是否完整
  - 當卡片顯示異常需要診斷
  - 當批次建立完成後想抽查品質
  關鍵字：檢查卡片、驗證結構、卡片格式、YAML 錯誤、卡片診斷
---

# 卡片結構驗證

檢驗日文學習卡片的結構完整性，提供診斷報告和修復建議。

## 使用方式

讀取指定卡片，執行結構檢查，輸出診斷報告。

```
請檢查 zettelkasten/verb-u/030_manabu.md 的卡片結構
```

## 檢查項目

### YAML Frontmatter

| 欄位 | 必要性 | 驗證規則 |
|------|--------|----------|
| card_id | 必要 | 格式：`{category}_{number}` |
| title | 必要 | 格式：`"日文 (讀音)"` 或 `"日文A vs 日文B"` |
| category | 必要 | 須為有效分類（noun, verb-u, grammar 等） |
| jlpt_level | 必要 | n5, n4, n3, n2, n1 之一 |
| tags | 建議 | 陣列格式 |
| dictionary | 建議 | 包含 reading, pos, definition_ja |

### 必要區塊

| 區塊 | 驗證規則 |
|------|----------|
| 日文解釋 | `### 日文` 或 `### 日文解釋` 標題存在 |
| 中文解釋 | `### 中文` 或 `### 中文解釋` 標題存在 |
| 英文解釋 | `### English` 標題存在 |
| 例句 | `## 例句` 區塊存在，且有編號例句 |

### 連結格式

| 檢查項 | 正確格式 |
|--------|----------|
| Markdown 連結 | `[text](path.md)` |
| 相對路徑 | `../category/file.md` |
| 禁止格式 | `[[wikilink]]` |

## 輸出格式

```markdown
## 卡片結構診斷報告

**檔案**：{path}
**card_id**：{id}

### ✅ 通過的檢查
- YAML frontmatter 格式正確
- 必要區塊完整
- 連結格式正確

### ⚠️ 警告
- 缺少 dictionary.definition_en（可選欄位）
- tags 數量較少（建議 3-5 個）

### ❌ 錯誤
- 缺少 English 解釋區塊
- card_id 格式不符（應為 verb-u_030）

### 修復建議
1. 新增 `### English` 區塊
2. 修正 card_id 為 `verb-u_030`
```

## 與 Agent 的關係

| 角色 | 職責 |
|------|------|
| **card-structure-handler**（Agent） | 批次建立卡片結構，並發執行 |
| **card-structure-validator**（Skill） | 人工抽查驗證，互動式報告 |

**互補而非替代**：Agent 負責建立，Skill 負責驗證。

## 注意事項

- 此 Skill 只讀取和分析，不修改任何檔案
- 若需修復，請根據報告手動編輯或使用相關腳本
- 批次驗證請使用 `verify-meta.py` 腳本
