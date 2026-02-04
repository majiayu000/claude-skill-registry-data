---
name: costs
description: View cost dashboard and spending analytics (project)
---

# Cost Dashboard Skill

Display Devflow cost tracking and spending analytics by reading session data directly.

## Usage

```
/costs [options]
```

## Options

| Option | Description |
|--------|-------------|
| --period day | Show today's costs only |
| --period week | Show this week's costs |
| --period month | Show this month's costs (default) |
| --history N | Show last N sessions |
| --story KEY | Filter by story key |

## Prompt

You are displaying the Devflow cost dashboard.

**Arguments:** $ARGUMENTS

### Step 1: Read Configuration

Read the configuration file:
- Path: `tooling/.automation/costs/config.json`

This contains:
- `budget_dev`: Development budget (USD)
- `subscription_plan`: Current plan (free/pro)
- `subscription_token_limit`: Monthly token limit
- `subscription_billing_period_days`: Days in billing period
- `display_currencies`: Currencies to show
- `currency_rates`: Exchange rates

### Step 2: Find Session Files

Find all session files:
- Path pattern: `tooling/.automation/costs/sessions/*.json`

### Step 3: Read and Aggregate Session Data

For each session file, extract:
- `session_id`: Session identifier
- `start_time` / `end_time`: Timestamps
- `story_key`: Associated story (if any)
- `entries[]`: Array of cost entries with `model`, `input_tokens`, `output_tokens`, `cost_usd`
- `totals`: Aggregated totals for the session

Identify the most recent session as the "current session".

### Step 4: Calculate Metrics

Calculate:
1. **Current session tokens/cost**: From the most recent session
2. **Cumulative tokens**: Sum of all tokens across ALL sessions this billing period
3. **Cumulative cost**: Sum of all `cost_usd` across ALL sessions
4. **Cost by model**: Group costs by model (opus, sonnet, haiku)
5. **Cost by story**: Group costs by story_key
6. **Budget usage**: (cumulative_cost / budget_dev) * 100
7. **Subscription usage**: (cumulative_tokens / subscription_token_limit) * 100
8. **Average cost per session**: cumulative_cost / session_count
9. **Average tokens per session**: cumulative_tokens / session_count
10. **Input/output ratio**: total_input_tokens / total_output_tokens
11. **Days remaining**: Calculate from billing period start
12. **Projected monthly cost**: (cumulative_cost / days_elapsed) * 30
13. **Projected token usage**: (cumulative_tokens / days_elapsed) * 30

### Step 5: Apply Filters

Based on $ARGUMENTS:
- `--period day`: Filter sessions from today only
- `--period week`: Filter sessions from last 7 days
- `--period month`: Filter sessions from last 30 days (default)
- `--history N`: Show only last N sessions
- `--story KEY`: Filter sessions matching story_key

### Step 6: Format Output

Display the dashboard using this format:

```
=================================================================
                    DEVFLOW COST DASHBOARD
=================================================================
Plan: [plan] | Tokens: [cumulative]/[limit] ([%]%) | [days] days left
This Session: $[current_cost] | Cumulative: $[total_cost]
=================================================================

PERIOD: [period]                        SESSIONS: [count]

--- TOKEN USAGE ---------------------------------------------
                   This Session         Cumulative
Input:             [current_in]         [total_in]
Output:            [current_out]        [total_out]
Total:             [current_total]      [total_total]

I/O Ratio:         [ratio]:1 (higher = more input-heavy conversations)

--- COST BY MODEL -------------------------------------------
[model]            $[cost]  ([%]%)  [bar]

--- COST BY STORY -------------------------------------------
[story-key]        $[cost]  ([%]%)
(no story)         $[cost]  ([%]%)

--- BUDGET STATUS -------------------------------------------
Spent:     $[total]  /  $[budget]  ([%]%)
[================================--------------------] [%]%

[WARNING] if > 75%: "Approaching budget limit!"
[CRITICAL] if > 90%: "Near budget limit - consider pausing"

--- PROJECTIONS (based on current usage rate) ---------------
Monthly token projection:    [projected] / [limit] ([%]%)
Monthly cost projection:     $[projected_cost]
Avg cost per session:        $[avg_cost]
Avg tokens per session:      [avg_tokens]

--- RECENT SESSIONS -----------------------------------------
[session_id]  [date]  [tokens]  $[cost]  [story or "-"]
[session_id]  [date]  [tokens]  $[cost]  [story or "-"]
[session_id]  [date]  [tokens]  $[cost]  [story or "-"]
(show last 5 sessions)

--- CURRENCIES ----------------------------------------------
$[USD] | E[EUR] | L[GBP] | R$[BRL]
=================================================================
```

### Budget Warnings

Display warnings based on config thresholds:
- If budget usage > `warning_percent` (75%): Show [WARNING]
- If budget usage > `critical_percent` (90%): Show [CRITICAL]
- If subscription usage > 80%: Show token limit warning

### Notes

- Format large numbers with K/M suffixes (e.g., 1.5K, 2.3M)
- Round costs to 2 decimal places
- Show percentages to 1 decimal place
- Use text-based progress bars with = and - characters
- Current session = most recent session file by timestamp
- Cumulative = sum of ALL sessions in the billing period
- If no sessions found, display a message indicating no cost data available
- Calculate days remaining: billing_period_days - days since first session of period
