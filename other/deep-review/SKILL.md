---
name: deep-review
description: 對 staged changes 執行三維度平行審查（安全、效能、風格），合成優先排序的發現摘要。
disable-model-invocation: true
context: fork
---

# Deep Review — 三維度平行程式碼審查

對目前的 staged changes 執行以下三個平行審查：

## 1. 安全審查
使用 security-reviewer agent，檢查：
- 注入漏洞（SQL、XSS、command injection）
- 認證與授權缺陷
- 敏感資料暴露

## 2. 效能審查
檢查以下效能問題：
- N+1 查詢
- 記憶體洩漏風險
- 阻塞操作（blocking I/O in async context）
- 不必要的重複計算

## 3. 風格審查
檢查一致性：
- 是否遵循專案既有的程式碼風格
- 命名慣例是否統一
- 是否有多餘的程式碼或未使用的 import

## 輸出格式

將三個維度的發現合併為優先排序的清單：
1. 🔴 Critical — 必須修復才能合併
2. 🟡 Warning — 建議修復
3. 🔵 Info — 可選的改善建議

每項包含 `file:line` 引用與修復建議。

## `/ultrareview` — 雲端多 Agent Fleet 審查（Research Preview）

> v2.1.86+，適用 Pro / Max / Team / Enterprise

當 staged changes 規模大、或想要獨立於本地環境的深度審查時，使用 `/ultrareview`：

```bash
/ultrareview           # 審查當前 branch vs main
/ultrareview <PR-num>  # 審查指定 PR
```

**與本地 Deep Review 的差異**：

| | 本地 Deep Review | `/ultrareview` |
|---|---|---|
| 執行位置 | 本地 context | 雲端 agent fleet |
| 耗時 | 即時 | 5–10 分鐘 |
| 費用 | 計入訂閱額度 | 3 次免費（Pro/Max），之後 $5–20/run |
| 適用場景 | 快速 pre-commit 把關 | 複雜 PR / 安全敏感變更 |

**使用建議**：日常用本地三維度 Deep Review；高風險或大型 PR 才升級到 `/ultrareview`。

## Gotcha

- **只審查 staged 變更**：未 `git add` 的修改不在範圍內；請先確認 staging area 正確。
- **三個 agent 必須全部完成**才能合成報告；若其中一個逾時，其餘結果仍輸出但需標注「部分審查」。
- **安全 reviewer 需讀完整檔案**，不只看 diff；若 diff 範圍外有相關漏洞也應標注。
- **`.claude/` 目錄的變更**需特別標注 — 這些是系統指令，任何修改都有安全隱含。
- **不要提出風格修改以外的 rewrite 建議** — 這是審查而非重構，Critical 項必須是真正的阻擋問題。
