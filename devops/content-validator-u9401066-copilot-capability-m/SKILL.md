---
name: content-validator
description: |
  Validate that written content accurately reflects source materials.
  LOAD THIS SKILL WHEN: User says "驗證", "validate", "檢查準確性", "核對" | after writing notes/reports | ensuring content accuracy.
  CAPABILITIES: Source-target comparison, citation verification, fact checking, consistency check.
---

# 內容驗證技能 (Content Validator)

## 描述

驗證撰寫內容是否忠實反映來源材料，確保引用準確、事實正確。

## 觸發條件

- 「驗證內容」「檢查準確性」「核對引用」
- "validate", "verify", "fact check", "check accuracy"
- 完成筆記或報告後需要品質檢查

## Agent 驗證能力

### 1. 來源比對

Agent 會將撰寫內容與原始來源逐項比對：

```python
# 驗證流程偽代碼
def validate_content(note: str, source: str) -> ValidationResult:
    results = []
    
    # 1. 提取筆記中的所有事實陳述
    claims = extract_claims(note)
    
    # 2. 對每個陳述在來源中尋找支持
    for claim in claims:
        support = find_support_in_source(claim, source)
        if support.found:
            results.append({"claim": claim, "status": "✅ 已驗證", "source": support.location})
        elif support.partial:
            results.append({"claim": claim, "status": "⚠️ 部分支持", "note": support.note})
        else:
            results.append({"claim": claim, "status": "❌ 未找到支持", "action": "需要修正或補充引用"})
    
    return results
```

### 2. 數據準確性檢查

| 檢查項目 | 驗證方式 |
|----------|----------|
| 數字引用 | 比對來源中的數值 |
| 統計結果 | 確認 p 值、CI、OR 等 |
| 百分比 | 重新計算驗證 |
| 日期/年份 | 與來源交叉核對 |

### 3. 引用格式檢查

```python
def check_citations(note: str, references: list) -> list:
    issues = []
    
    # 找出所有引用標記
    citations = find_citation_markers(note)
    
    for cite in citations:
        # 檢查引用是否存在於參考文獻
        if cite not in references:
            issues.append(f"引用 {cite} 不在參考文獻中")
        
        # 檢查引用格式是否正確
        if not is_valid_format(cite):
            issues.append(f"引用 {cite} 格式不正確")
    
    return issues
```

## 執行流程

### 完整驗證流程

```
輸入：筆記/報告 + 原始來源
    ↓
Step 1: 事實陳述提取
    - 識別所有可驗證的陳述
    ↓
Step 2: 來源比對
    - 逐一比對來源支持度
    ↓
Step 3: 數據驗證
    - 檢查所有數字和統計
    ↓
Step 4: 引用檢查
    - 驗證引用格式和存在性
    ↓
Step 5: 一致性檢查
    - 檢查內部邏輯一致性
    ↓
輸出：驗證報告 + 修正建議
```

## 輸出格式

```markdown
## 內容驗證報告

**驗證時間**: 2024-12-22 10:30
**來源文件**: smith-2024-remimazolam.pdf
**驗證對象**: notes/smith-2024-summary.md

---

### 📊 驗證摘要

| 類別 | 通過 | 警告 | 錯誤 |
|------|------|------|------|
| 事實陳述 | 12 | 2 | 1 |
| 數據引用 | 8 | 1 | 0 |
| 引用格式 | 5 | 0 | 0 |
| **總計** | **25** | **3** | **1** |

**驗證結果**: ⚠️ 需要修正

---

### ✅ 已驗證項目

| 陳述 | 來源位置 |
|------|----------|
| "Remimazolam 起效時間 1-2 分鐘" | p.3, Methods |
| "納入 15 篇 RCT" | p.2, Abstract |
| ... | ... |

### ⚠️ 需要確認

| 陳述 | 問題 | 建議 |
|------|------|------|
| "低血壓發生率降低 22%" | 來源寫 "relative risk 0.78" | 修正為 RR 或計算正確百分比 |
| "2,340 位病患" | 來源寫 "2,334 participants" | 更正數字 |

### ❌ 錯誤項目

| 陳述 | 問題 | 修正建議 |
|------|------|----------|
| "研究結論推薦首選使用" | 來源未有此結論 | 刪除或改為 "作者建議可考慮使用" |

---

### 📝 修正清單

1. [ ] 第 23 行：將 "22%" 改為 "RR 0.78 (22% 相對風險降低)"
2. [ ] 第 31 行：將 "2,340" 改為 "2,334"
3. [ ] 第 45 行：刪除 "首選使用" 改為 "可考慮使用"

---

### ✏️ 自動修正 (可選)

如需自動修正已標記的錯誤，請確認後執行。
```

## 使用範例

**範例 1：快速驗證**
```
用戶：「驗證這份筆記的準確性」
執行：
1. 讀取筆記和原始來源
2. 提取可驗證陳述
3. 比對驗證
4. 產出驗證報告
```

**範例 2：數據驗證**
```
用戶：「檢查報告中的所有統計數據」
執行：
1. 找出所有數字和統計值
2. 與來源比對
3. 標記不一致項目
```

**範例 3：引用檢查**
```
用戶：「確認所有引用都正確」
執行：
1. 提取所有引用標記
2. 比對參考文獻清單
3. 檢查引用格式
```

## 驗證嚴格度

| 等級 | 說明 | 適用場景 |
|------|------|----------|
| **Strict** | 每個數字都必須完全一致 | 發表論文、正式報告 |
| **Normal** | 允許四捨五入差異 | 一般筆記、內部文件 |
| **Lenient** | 只檢查重大錯誤 | 快速瀏覽、初稿 |

## 相關技能

- `note-writer` - 撰寫筆記
- `report-formatter` - 格式化報告
- `report-writing` - 組合技能：完整報告撰寫
