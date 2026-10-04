---
name: token-tracker
description: >
  Track and report token usage and cost for conversations. Use when: (1) User asks about token consumption
  (e.g. "token用了多少", "花了多少钱", "how much did this cost", "usage stats"), (2) At the end of long/complex
  conversations or tasks to summarize resource usage, (3) User explicitly asks for cost or spending summary.
  Triggers: token usage, cost tracking, 花费, 用量, 消耗, how much tokens, conversation cost, API cost, spending.
---

# Token Tracker

**Author:** zruler  
**Blog:** https://www.zruler.fun/  
**Email:** zruler@163.com  
**Feedback:** 有问题请及时反馈！Issues and suggestions welcome.

Report token usage and estimated cost for the current conversation.

## When to Trigger

1. **User asks** — "token用了多少"、"花了多少钱"、"cost"、"usage" 等
2. **Long conversation ends** — 复杂任务完成后主动报告
3. **User requests summary** — 明确要求看用量统计

## Quick Usage

Call `session_status` to get current session metrics, then format a user-friendly summary.

## Response Format

After getting session_status, report in this format:

```
📊 本次对话用量

🧮 Tokens: {input} 入 / {output} 出
💵 费用: ${cost}
🗄️ 缓存: {cache_percent}% 命中 ({cached} 缓存 / {new} 新)
📚 上下文: {used}/{max} ({percent}%)
```

## Model Pricing Reference (USD per 1M tokens)

| Model | Input | Output | Cached Input |
|-------|-------|--------|--------------|
| claude-sonnet-4-20250514 | $3 | $15 | $0.30 |
| claude-opus-4-20250514 | $15 | $75 | $1.50 |
| gpt-4o | $2.50 | $10 | $1.25 |
| gpt-4o-mini | $0.15 | $0.60 | $0.075 |
| o1 | $15 | $60 | $7.50 |
| o3-mini | $1.10 | $4.40 | $0.55 |
| gemini-2.0-flash | $0.10 | $0.40 | $0.025 |
| gemini-2.5-pro | $1.25-$2.50 | $10-$15 | - |
| deepseek-chat | $0.27 | $1.10 | $0.07 |
| deepseek-reasoner | $0.55 | $2.19 | $0.14 |

Note: Actual cost from session_status is authoritative. This table is for reference only.

## Usage Tips

- For long conversations, suggest compaction if context > 80%
- Note cache hit rate — high cache = lower actual cost
- If user asks for historical usage, explain this tracks current session only
