---
name: spec-interview
description: 大型功能開發前，讓 Claude 用 AskUserQuestionTool 深度訪問你（技術、UI/UX、風險、取捨），產出完整 spec，再開新 session 執行。適合在複雜功能實作前、需求模糊時、或開始新專案架構設計時使用。
disable-model-invocation: true
context: fork
---

# Spec Interview — 訪談式 Spec 建立

> 來源：Thariq Shihipar (@trq212, Anthropic Claude Code 核心團隊)
> 「my favorite way to use Claude Code to build large features is spec based」
> 原始 gist：[claude-code-interview-command](https://gist.github.com/robzolkos/40b70ed2dd045603149c6b3eed4649ad)（71 ★）

## 核心理念

大多數人開發大型功能的問題不是技術能力不足，而是**需求不夠清楚就開始實作**。
Spec Interview 強迫你在動手前先被訪問一遍，把模糊的需求變成 Claude 可以 1-shot 執行的精確 spec。

```
模糊 prompt → 直接實作    ❌ Claude 邊猜邊做，來回修改多次
模糊 prompt → 訪談 → spec → 新 session 執行   ✅ Claude 1-shot 完成
```

### Unhobbling the Model（Thariq 核心工程哲學）

> "The goal is to constantly remove constraints to give Claude more agency."

模型本身已有很強的能力，但環境中充滿**不必要的限制**（hobbles）：
- 過度細碎的步驟指令（讓 Claude 無法自主判斷）
- 僵化的工具 schema（限制 Claude 組合工具的方式）
- 過多的 safety guardrails（在不必要的地方阻斷代理行為）

**Spec Interview 是 Unhobbling 的體現**：把模糊需求轉成清晰 spec，讓 Claude 在執行 session 中擁有充足資訊，不需要不斷回頭確認 → 更多自主性、更少中斷。

**Delete-and-Rebuild Cycle（隨模型能力升級主動刪除）**：
- 模型能力每隔幾個月大幅提升
- 過去需要 10 行 spec 才能描述清楚的需求，現在 3 行就夠
- **積極刪除舊的 scaffolding**（詳細步驟、重複限制、過度 handholding）
- 衡量標準：「移除這段說明後，Claude 還能做對嗎？」→ 能就刪

---

## 執行流程（3 步驟）

### Step 1：寫最小 Spec（或直接描述目標）

不需要完整，1-2 句話描述你想做什麼：

```
我想在 dashboard 加一個 real-time 通知系統
```

或先建立 plan 檔案：

```bash
echo "實作 real-time 通知系統，支援 WebSocket，UI 右上角 bell icon" > plan.md
```

### Step 2：啟動 Spec Interview

```
請用 AskUserQuestionTool 深度訪問我關於這個功能的所有細節：
技術實作、UI/UX、邊界案例、風險、取捨。
不要問顯而易見的問題。訪談完成後，產出完整的 spec 文件。

功能：[你的功能描述]
```

或用 `/spec-interview` 搭配 plan 檔案：

```
/spec-interview plan.md
```

Claude 會用 AskUserQuestionTool 逐一訪問（modal UI 阻塞 agent loop，確保你充分回答）：
- 技術實作細節與限制
- UI/UX 期望行為
- 邊界案例與例外處理
- 與現有系統的相容性
- 接受標準（何謂「完成」）

### Step 3：開新 Session 執行 Spec

訪談完成後，Claude 產出 spec 文件。**開新 session**，把 spec 貼進去：

```
請依照以下 spec 實作，不要問問題，直接執行：

[貼上 spec 內容]
```

新 session 有乾淨的 context，Claude 專注在執行而非釐清需求。

---

## 為什麼要開新 Session 執行？

訪談 session 的 context 已經充滿探索性的對話和中間產物。
執行 session 需要的是乾淨的 context — 只有 spec 和程式碼。

```
訪談 session：問題、反問、釐清、模糊探索  ← 留在 child context
執行 session：精確 spec → 直接執行          ← 乾淨開始
```

---

## Interview Command（Thariq 原版）

可以把以下內容存成 `.claude/skills/spec-interview/scripts/interview.sh` 供 Claude 呼叫：

```bash
#!/usr/bin/env bash
# 讀取 plan 檔案，啟動訪談模式
# 用法：claude --model claude-opus-4-8 "$(cat interview-prompt.txt)" < "$1"
PLAN_FILE="${1:-plan.md}"
cat <<EOF
Read this plan file and interview me in detail using the AskUserQuestionTool
about literally anything: technical implementation, UI & UX, concerns, tradeoffs, etc.
Ask non-obvious questions that I might not have thought of.
Continue interviewing until you have enough information, then generate a specification document.

Plan file content:
$(cat "$PLAN_FILE" 2>/dev/null || echo "No plan file found at: $PLAN_FILE")
EOF
```

---

## 架構哲學（Thariq — Seeing like an Agent）

設計功能時，採用「從模型視角出發」的方法：

### 工具設計原則（Claude Code 內部採用）

| 原則 | 說明 |
|------|------|
| **Progressive Disclosure 優於加工具** | 不要把所有資訊塞進 system prompt；讓 Claude 在需要時透過子 agent 探索 |
| **~20 個工具上限** | 每個工具都增加模型認知負荷；加新工具需高門檻 |
| **工具需讓模型理解如何呼叫** | AskUserQuestion 成功關鍵：不是格式指令，而是獨立工具 + modal UI |
| **Tasks > Todos** | 隨模型能力提升，舊工具可能變成限制；Tasks 支援跨 session 協作 |

### 3 次失敗 → 1 次成功：AskUserQuestion 的設計過程

1. **第 1 次（失敗）**：把問題加為 ExitPlanTool 的參數 → 模型被衝突資訊搞混
2. **第 2 次（失敗）**：用 markdown 格式指令 → 模型不穩定遵守
3. **第 3 次（成功）**：獨立工具 + modal UI → 阻塞 agent loop 直到使用者回應 ✅

**洞察**：工具設計失敗通常不是因為模型能力不足，而是**工具設計沒讓模型清楚理解呼叫時機**。

---

## Gotcha

- **不要跳過訪談直接執行**：模糊 spec 讓 Claude 邊猜邊做，最終需要多次來回修改。
- **訪談結束後一定開新 session**：帶著訪談對話執行 = context rot 從一開始就發生。
- **spec 要包含接受標準**：「功能完成」的定義必須可驗證（測試、截圖、端到端流程）。
- **不要問顯而易見的問題**：Claude 已經知道很多，訪談要專注在你的特定限制和邊界。
- **Spec 完成後搭配 `/go` 驗證模式**：讓 Claude 端到端測試 → `/simplify` → 開 PR（Boris Cherny 建議）。
