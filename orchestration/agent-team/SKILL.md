---
name: agent-team
description: 啟動 Agent Team 模式，多個 worker 平行處理任務並共享發現。適用於大型重構、codebase 遷移、全面審查。
disable-model-invocation: true
---

# Agent Team — 多 Worker 平行協作

> 依據 [Multi-Agent Coordination Patterns](https://claude.com/blog/multi-agent-coordination-patterns) 的 Agent Teams 模式
> 📦 離線歸檔：[`archive/articles/multi-agent-coordination-patterns.md`](https://github.com/zeuikli/claude-code-workspace/blob/blog-archive/archive/articles/multi-agent-coordination-patterns.md)

啟動針對 $ARGUMENTS 的 Agent Team 協作。

## 架構

```
Coordinator（主對話）
├── Worker A — 負責領域 1
├── Worker B — 負責領域 2
└── Worker C — 負責領域 3
```

## 工作流程

1. **分析任務範圍**：理解 $ARGUMENTS 描述的任務
2. **劃分工作區域**：按目錄 / 模組 / 功能拆分，確保無重疊
3. **啟動 Workers**：每個 Worker 使用獨立 Sub Agent，指定：
   - 負責的檔案範圍
   - 具體目標
   - 完成標準
4. **平行執行**：所有 Worker 同時啟動
5. **收集結果**：等待所有 Worker 完成，彙整摘要
6. **衝突解決**：如有跨 Worker 的衝突變更，由 Coordinator 決策
7. **產出報告**：統一的變更摘要 + 修改檔案清單

## Worker 規範

- 每個 Worker 只修改自己負責的檔案
- 不跨區域修改（避免 merge 衝突）
- 完成後回傳：變更摘要 + 修改清單 + 待確認事項

## 終止條件

- 所有 Worker 回報完成
- 或達到時間上限（由使用者指定）
- 或 Coordinator 判斷已收斂（無新發現）

## Data Contract Pattern（平行前先對齊 I/O 格式）

> 來源：[shanraisshan/claude-code-best-practice — orchestration-workflow](https://github.com/shanraisshan/claude-code-best-practice/tree/main/orchestration-workflow)

在 fan-out Workers **之前**，Coordinator 必須明確定義每個 Worker 的輸入格式與輸出格式，讓所有 Worker 的結果可以直接合併，無需二次轉換。

**範例**：三個 Worker 各自查詢不同時區的現在時間，輸出格式事先統一：

```json
{ "time": "14:30", "tz": "UTC+8", "formatted": "2026-04-18 14:30 (UTC+8)" }
```

Coordinator 在 prompt 中明確寫出此 schema，Worker A/B/C 直接輸出符合格式的 JSON，Coordinator 只需 `JSON.parse` 後合併陣列，無需猜測欄位名稱或手動對齊格式。

**沒有 Data Contract 的後果**：Worker A 回傳 `time: "2:30pm"`、Worker B 回傳 `timestamp: 1713420600`，Coordinator 需要額外解析邏輯，增加錯誤風險。

## Gotcha

- **Workers 無法直接溝通**：所有發現必須回傳給 Coordinator，不能 Worker A 把結果傳給 Worker B。
- **各 Worker context 完全隔離**：Worker A 讀到的檔案，Worker B 看不到；如需共享，由 Coordinator 明確傳入。
- **Worker 失敗不會自動重試**：Coordinator 必須處理單一 Worker 失敗的情況，並決定是否重啟或降級。
- **任務分割要互相獨立**：若子任務有依賴關係（A 需要 B 的結果），不適合平行，改用序列委派。
