---
name: nsforge-formula-management
description: 公式庫管理。觸發詞：找公式, 列出, 更新公式, 刪除公式, 公式庫。
---

# 公式庫管理 Skill

> **⚠️ 操作後必須向用戶展示結果！**
> - `derivation_get_saved` 後顯示公式內容（LaTeX 格式）
> - `derivation_search_saved` 後顯示搜尋結果摘要
> - 刪除前務必用 `derivation_get_saved` 顯示內容讓用戶確認

## 工具速查

| 操作 | 工具 | 參數 |
|------|------|------|
| 列出 | `derivation_list_saved(category?)` | 可選分類篩選 |
| 搜尋 | `derivation_search_saved(query)` | 關鍵字 |
| 取得 | `derivation_get_saved(result_id)` | ID |
| 更新 | `derivation_update_saved(result_id, ...)` | ID + 要更新的欄位 |
| 刪除 | `derivation_delete_saved(result_id, confirm=True)` | ⚠️ 需確認 |
| 統計 | `derivation_repository_stats()` | 無 |

## 調用範例

```python
# 列出所有
derivation_list_saved()

# 按分類
derivation_list_saved(category="pharmacokinetics")

# 搜尋
derivation_search_saved(query="temperature")

# 取得詳情
derivation_get_saved(result_id="temp_corrected_elimination_20260102")

# 更新（可更新欄位：description, clinical_context, assumptions, limitations, references, tags, verified, verification_notes）
derivation_update_saved(
    result_id="...",
    verified=True,
    tags=["pk", "temperature"]
)

# 刪除（⚠️ 先 get 顯示內容，獲得用戶確認後才執行）
derivation_delete_saved(result_id="...", confirm=True)
```

## 刪除流程

1. `derivation_get_saved` 顯示要刪除的內容
2. 詢問用戶確認
3. 用戶同意後才執行 `derivation_delete_saved(..., confirm=True)`
