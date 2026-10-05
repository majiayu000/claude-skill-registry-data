---
name: kiro-usage-day-report
description: >-
  Use when checking `llm_gateway_usage_events` for one China-time calendar day,
  especially to total Kiro credits and break down accounts matched by name
  substring plus user-specified exact account names.
---

# Kiro Usage Day Report

Use this skill to answer questions like:
- "昨天中国时间 Kiro 用了多少积分？"
- "账号名包含 `laohan` 的号当天用了多少积分？"
- "再把 `KitWilliam` 也算进去。"

This is a read-only reporting skill. It does not modify LanceDB tables.

## When To Use
1. One-day Kiro credit totals from `llm_gateway_usage_events`.
2. China-time daily usage reports (`Asia/Shanghai`).
3. Account subsets defined by:
   - one or more name substrings
   - one or more exact account names supplied by the user
4. Cases where the user wants both the global total and the subset total for the same day.

## Why This Skill Exists
- The authoritative data lives in `llm_gateway_usage_events` inside the content DB.
- LanceDB's Python query layer is fine for filtering rows, but aggregate expressions like `sum(credit_usage)` are not supported reliably enough for this workflow.
- For final numbers, use the bundled Python script to fetch the candidate rows and aggregate locally.

## Default Data Source
- DB path: `/mnt/wsl/data4tb/static-flow-data/lancedb`
- Table: `llm_gateway_usage_events`
- Provider filter: `provider_type = 'kiro'`

Schema source of truth in this repo:
- `shared/src/llm_gateway_store/schema.rs`
- `shared/src/llm_gateway_store/types.rs`

## Execution Policy
1. Interpret the requested date in `Asia/Shanghai`.
2. Use the half-open China-time window `[YYYY-MM-DD 00:00:00, next day 00:00:00)`.
3. Filter LanceDB by provider and time window first.
4. Aggregate `credit_usage` locally in Python.
5. Treat rows with `credit_usage_missing = true` or null `credit_usage` as missing-metering rows.
6. If missing-metering rows exist, report the total as a lower bound.
7. For account subsets:
   - substring matching is case-insensitive
   - exact account additions are also matched case-insensitively
   - exact accounts with zero usage should still be reported explicitly

## Script
Bundled script:
- `skills/kiro-usage-day-report/scripts/kiro_usage_day_report.py`

Preferred command:

```bash
python skills/kiro-usage-day-report/scripts/kiro_usage_day_report.py \
  --date 2026-04-11
```

With substring plus exact account additions:

```bash
python skills/kiro-usage-day-report/scripts/kiro_usage_day_report.py \
  --date 2026-04-11 \
  --contains laohan \
  --account KitWilliam
```

Multiple match inputs are allowed:

```bash
python skills/kiro-usage-day-report/scripts/kiro_usage_day_report.py \
  --date 2026-04-11 \
  --contains laohan \
  --contains spare \
  --account KitWilliam \
  --account some-other-name
```

JSON output:

```bash
python skills/kiro-usage-day-report/scripts/kiro_usage_day_report.py \
  --date 2026-04-11 \
  --contains laohan \
  --account KitWilliam \
  --format json
```

## Output Contract
Always report:
1. China-time day and UTC window.
2. Global Kiro total for that day.
3. Global row count and missing-metering row count.
4. If subset filters were provided:
   - subset total
   - subset row count
   - subset missing-metering row count
   - per-account breakdown
   - exact accounts with zero usage, if any

## Interpretation Rules
- `credit_usage` is the exact Kiro credit usage only when upstream metering was present.
- `missing_credit_rows > 0` means the reported total is incomplete and should be described as `>= value`.
- Do not silently turn missing credit rows into zero-cost rows in prose.

## Recommended Handoff Shape
1. State the exact China-time window.
2. Give the global Kiro total.
3. Give the subset total if requested.
4. List per-account totals.
5. Mention whether the totals are exact or lower bounds.

## Common Mistakes
- Using local machine time without naming the timezone.
- Using `count_rows` plus SQL `LIKE` as the final source of truth for the subset total.
- Forgetting user-specified exact accounts that do not contain the substring.
- Hiding missing-metering rows.
