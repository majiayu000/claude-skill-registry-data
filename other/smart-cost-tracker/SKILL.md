---
name: smart-cost-tracker
description: >
  Track AI agent spending in real time. Shows cost per message, per conversation,
  per day. Budget alerts, daily/weekly reports, cost-per-task breakdown.
  Use when the user asks about spending, costs, tokens, budget, or billing.
  Triggers on: "how much did that cost", "show my spending", "token usage",
  "budget", "cost report", "am I over budget", "daily spending".
tags:
  - cost
  - tokens
  - budget
  - spending
  - billing
  - usage
  - money
  - api-cost
---

# Smart Cost Tracker

You track AI spending so the user never gets surprised by their API bill.

## Core Behavior

When the user enables cost tracking, calculate the estimated cost after each response and append it to the cost log. The user controls when tracking is active. When the user asks about spending, present the data clearly.

## Data Storage Disclosure

This skill writes to `~/.openclaw/cost-log.json` on your local machine to track spending history. No data is sent to external services. You can delete this file at any time to clear all history. Tracking only runs when you explicitly enable it.

## How to Calculate Cost

### Token Pricing (as of March 2026)
```
Claude Opus 4.6:    $15.00 / 1M input,  $75.00 / 1M output
Claude Sonnet 4.6:   $3.00 / 1M input,  $15.00 / 1M output
Claude Haiku 4.5:    $0.80 / 1M input,   $4.00 / 1M output
GPT-5.4:             $2.50 / 1M input,  $10.00 / 1M output
GPT-5.2:             $1.50 / 1M input,   $6.00 / 1M output
GPT-5.1:             $0.60 / 1M input,   $2.40 / 1M output
DeepSeek V3:         $0.27 / 1M input,   $1.10 / 1M output
```

### Estimation Method
If exact token counts aren't available:
- Average English word = ~1.3 tokens
- Count words in the prompt + response, multiply by 1.3
- Apply the pricing for the current model
- Round to 4 decimal places

## Cost Log

Maintain a file `~/.openclaw/cost-log.json` with this structure:
```json
{
  "entries": [
    {
      "timestamp": "2026-03-27T14:30:00Z",
      "model": "openai-codex/gpt-5.4",
      "tokens_in": 1200,
      "tokens_out": 800,
      "cost_usd": 0.0110,
      "task": "summarized a paper",
      "session": "main"
    }
  ],
  "daily_totals": {
    "2026-03-27": { "cost": 0.43, "messages": 12, "tokens": 45000 }
  },
  "budget": {
    "daily_limit": 5.00,
    "monthly_limit": 50.00,
    "alert_threshold": 0.80
  }
}
```

## Commands

### "Start tracking" / "Enable cost tracking"
Begin logging costs after each message. Show confirmation: "Cost tracking enabled. I'll log token usage after each interaction."

### "Stop tracking" / "Disable cost tracking"
Stop logging. Show confirmation: "Cost tracking paused."

### "How much did that cost?"
Show the cost of the last message:
```
Last message: ~$0.0110 (1,200 in / 800 out tokens, gpt-5.4)
```

### "Show my spending" / "cost report"
Show a summary:
```
# Cost Report — March 27, 2026

## Today
Messages: 12 | Tokens: 45,000 | Cost: $0.43

## This Week
Messages: 67 | Tokens: 312,000 | Cost: $2.87

## This Month
Messages: 234 | Tokens: 1.2M | Cost: $11.43

## By Model
gpt-5.4:     $8.20 (72% of spend)
gpt-5.1:     $2.15 (19%)
haiku:        $1.08 (9%)

## Budget
Daily limit: $5.00 — used $0.43 (8.6%)
Monthly limit: $50.00 — used $11.43 (22.9%)
```

### "Set budget $X/day" or "Set budget $X/month"
Update the budget limits in cost-log.json.

### "Most expensive task"
Find the highest-cost entry and show it:
```
Most expensive: "Generated architecture diagram" — $0.89 (42K tokens, gpt-5.4)
```

### "Cost trend"
Show daily costs for the last 7 days:
```
Mar 21: $1.20 ████████
Mar 22: $0.85 █████
Mar 23: $2.10 █████████████
Mar 24: $0.43 ██
Mar 25: $1.67 ██████████
Mar 26: $0.92 █████
Mar 27: $0.43 ██  (so far)
```

### "Always show cost on/off"
Toggle whether cost is printed after every message:
```
[gpt-5.4 | 1.2K in / 800 out | $0.011]
```

## Budget Alerts

When spending exceeds the alert threshold (default 80%):
- Daily: "Budget alert: You've spent $4.20 of your $5.00 daily limit (84%)"
- Monthly: "Budget alert: You've spent $42.50 of your $50.00 monthly limit (85%)"

When over budget:
- "OVER BUDGET: You've spent $5.43 today, $0.43 over your $5.00 daily limit"

## Rules
- Never block the user from working even if over budget — just warn
- Costs are ESTIMATES unless exact token counts are available
- Always say "estimated" when using word-count approximation
- Store all data locally in ~/.openclaw/cost-log.json — never send to external services
- If the cost log doesn't exist, create it on first use
