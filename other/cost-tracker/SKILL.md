---
name: cost-tracker
description: 追蹤並計算當前 session 的 Token 使用量和花費（USD）。產出前後對比報告，幫助使用者了解 workspace 優化的實際效益。
disable-model-invocation: true
---

# Cost Tracker — Token 使用量與花費追蹤

> 依據 [Claude Agent SDK Cost Tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)

## 定價表（2026-05，官方 Opus 4.8 發布後）

| 模型 | Input ($/1M tokens) | Output ($/1M tokens) | Cache Read ($/1M) | Cache Write ($/1M) |
|------|---------------------|----------------------|--------------------|---------------------|
| **Opus 4.8** | $5.00 | $25.00 | $0.50 | $6.25 |
| **Sonnet 4.6** | $3.00 | $15.00 | $0.30 | $3.75 |
| **Haiku 4.5** | $1.00 | $5.00 | $0.10 | $1.25 |

> 來源：[Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)、[Pricing](https://platform.claude.com/docs/en/about-claude/pricing)。
> Cache Read = 0.1× input、Cache Write(5m) = 1.25× input。Opus 4.8 fast mode 為 premium 定價，不在此表。

## 使用方式

在 session 中執行 `/cost-tracker`，系統將：

1. **統計當前 session 的 Token 使用量**
   - 分別計算 input / output / cache tokens
   - 按模型分層統計（Haiku / Sonnet / Opus）

2. **計算花費（USD）**
   - 套用上方定價表
   - 區分主對話 vs Sub Agent 花費

3. **產出前後對比**
   - **優化前**（假設全部使用 Opus）的預估花費
   - **優化後**（Advisor 模式分層）的實際花費
   - 差異百分比

## 計算公式

```
花費 = (input_tokens × input_price / 1M)
     + (output_tokens × output_price / 1M)
     + (cache_read_tokens × cache_read_price / 1M)
     + (cache_write_tokens × cache_write_price / 1M)
```

## 分層估算模型

依據 CLAUDE.md 的 Advisor 模式，各角色的 Token 分配比例：

| 角色 | 模型 | 預估 Token 佔比 |
|------|------|-----------------|
| 搜尋探索 | Haiku | ~30% |
| 程式碼實作 + 測試 | Sonnet | ~55% |
| 架構審查 + 顧問 | Opus | ~15% |

## 輸出格式

```markdown
### Session Cost Report

| 指標 | 數值 |
|------|------|
| Total Input Tokens | xxx |
| Total Output Tokens | xxx |
| Cache Read Tokens | xxx |
| Cache Write Tokens | xxx |
| **Total Cost (USD)** | $x.xx |

#### 模型分層花費

| 模型 | Tokens | Cost (USD) | 佔比 |
|------|--------|-----------|------|
| Haiku | xxx | $x.xx | xx% |
| Sonnet | xxx | $x.xx | xx% |
| Opus | xxx | $x.xx | xx% |

#### 優化效益

| 指標 | 全 Opus | Advisor 分層 | 節省 |
|------|---------|-------------|------|
| 預估花費 | $x.xx | $x.xx | -xx% |
```

## Agent SDK 整合範例（TypeScript）

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

let sessionCost = 0;
const modelBreakdown: Record<string, { tokens: number; cost: number }> = {};

for await (const message of query({ prompt: "your task" })) {
  if (message.type === "result") {
    sessionCost += message.total_cost_usd;

    for (const [model, usage] of Object.entries(message.modelUsage)) {
      if (!modelBreakdown[model]) modelBreakdown[model] = { tokens: 0, cost: 0 };
      modelBreakdown[model].tokens += usage.inputTokens + usage.outputTokens;
      modelBreakdown[model].cost += usage.costUSD;
    }
  }
}

console.log(`Session total: $${sessionCost.toFixed(4)}`);
for (const [model, data] of Object.entries(modelBreakdown)) {
  console.log(`  ${model}: ${data.tokens} tokens, $${data.cost.toFixed(4)}`);
}
```

## Gotcha

- **Claude Code 的 `/usage` 是累積值**：它顯示從 session 開始到當下的總量，不是「本次操作」的增量。
- **Cache write tokens 比 input 貴**：cache write = 1.25× input price，計算時不要誤用 input 單價。
- **「優化前」是假設值**：以全 Opus 計算的對比數字是估算，實際上你可能原本也不是全 Opus。
- **Sub Agent 費用需個別計算**：子 agent 的 token 不一定計入主對話的 `/usage`，需確認 SDK 版本行為。
- **定價表可能已更新**：本 skill 的定價以 2026-04 為準，若超過 3 個月請重新確認官方定價。
