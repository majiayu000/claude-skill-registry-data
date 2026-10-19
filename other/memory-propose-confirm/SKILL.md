---
name: memory-propose-confirm
description: This skill should be used by the maigo orchestrator whenever a Soyo or Anon output contains a ## Memory propose section. Handles the confirm flow, fence-tracking rules for detecting the section, no-answer handling, and parallel-mode timing adjustments. Applies to /maigo:go, /maigo:quick, /maigo:team, /maigo:review.
---

<!-- mkdocs-include-start -->

# Memory Propose Confirm Flow

**Owner**: orchestrator
**Consumers**: [`/maigo:go`](https://github.com/Lee-W/maigo/blob/main/commands/go.md)、[`/maigo:quick`](https://github.com/Lee-W/maigo/blob/main/commands/quick.md)、[`/maigo:team`](https://github.com/Lee-W/maigo/blob/main/commands/team.md)、[`/maigo:review`](https://github.com/Lee-W/maigo/blob/main/commands/review.md)

## 觸發條件

當 🟡 Soyo 或 🎀 Anon 的輸出末尾含 `## Memory propose` 段時，orchestrator 在該 agent 完成後、繼續下一步前，立刻執行 confirm flow。

## Confirm Flow

1. **格式檢查**：檢查 propose 段的 6 個必填欄位（`name` / `slug` / `description` / `body` / `type` / `rationale`）是否齊全。
   缺任一欄位 → 不 confirm，印一行提示「偵測到 propose 段但格式不完整，已跳過」，繼續正常流程。
2. **顯示 index**：顯示目前兩個 memory 來源的 index：
   - `~/.config/maigo/memory/MEMORY.md`（cross-project）
   - `~/.claude/projects/<current-project>/memory/MEMORY.md`（per-project，若存在）
3. **印出摘要**：印出 propose 摘要（type / name / description / rationale）。
4. **AskUserQuestion**，選項：`存` / `修改` / `跳過`。
5. 選「存」或「修改」→ reuse [`/maigo:remember`](https://github.com/Lee-W/maigo/blob/main/commands/remember.md) 步驟 5+6
   （以 propose 的欄位為預填值；「修改」時步驟 5 讓使用者改各欄位）。
6. 選「跳過」→ 繼續正常流程，不寫任何檔。

Confirm flow 完成後繼續主線流程——不改變命令的步驟結構。

## 三態：存 / 跳過 / 未決（重要）

confirm flow 的結果有**三**種，不是兩種。orchestrator 不可把後兩者混為一談：

| 結果 | 觸發 | 處置 |
|---|---|---|
| **存** | 使用者選「存」/「修改」 | 寫檔（step 5） |
| **跳過** | 使用者**明確選**「跳過」 | 不寫檔，丟棄 propose，繼續 |
| **未決** | 使用者**沒選任何項**（關掉問題 / dismiss / AskUserQuestion 回 "did not answer"） | 不寫檔，但**不丟棄** propose |

**「沒回答」≠「跳過」。** dismiss 一個問題不是 decline——它只代表「現在不決定」。把 no-answer 當成跳過會把使用者還想留著的 memory 默默吃掉。

未決時 orchestrator 必須：

- 不寫任何檔（跟跳過一樣）
- **保留** propose 段——在回覆末尾原樣附上那個 `## Memory propose`（fenced，可複製），讓使用者之後說一聲就能存
- 印一行中性提示，例如：「memory propose 未決——你沒選，我先保留著，要存再跟我說。」
- **不要**自行推論成跳過或存，也不要追問逼使用者立刻決定；保留著、繼續主線即可

使用者之後任何時點說「存那個 memory」/「剛剛那條記起來」→ 直接 reuse step 5 寫檔，不必重跑整個 confirm flow。

## Fence-Tracking 規則

偵測 `## Memory propose` 標頭時，**只掃描 code fence 外的行**；code block 內（triple-backtick fence 之間）的同名標頭不觸發 confirm flow。

追蹤法：從輸出文字開頭往下追蹤 triple-backtick 計數（奇數 → in-fence），遇到 `^## Memory propose` 且 in-fence 為 true 時跳過。

## 並行模式追加

在 `/maigo:team` 的並行場景（🟡 Soyo 和 🟣 Taki 並行）下：若 Soyo 輸出含 `## Memory propose`，等**兩邊都回來後**再跑 confirm flow，不要插在 Taki 還在執行中間。
