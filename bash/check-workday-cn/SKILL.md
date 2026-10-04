---
name: check-workday-cn
description: Determine whether today (or a given date) is a working day in mainland China by querying holiday-cn yearly JSON from jsDelivr and applying holiday/makeup-workday rules. Use when users ask questions like "今天是不是工作日", "这天要不要上班", "是不是节假日/调休补班", or when a workflow needs a reliable workday boolean.
---

# Check Workday CN

Check whether today is a workday with official holiday override data from:
`https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json`

## Workflow

1. Run `python3 scripts/check_today_workday.py`.
2. Read `is_workday` from output.
3. Explain reason:
   - If date exists in `days[]`, use `isOffDay` directly (`false` => workday, `true` => off day).
   - If date does not exist in `days[]`, fall back to weekday rule (Mon-Fri workday, Sat-Sun off day).

## Commands

Use today in Asia/Shanghai:

```bash
python3 scripts/check_today_workday.py
```

Check specific date:

```bash
python3 scripts/check_today_workday.py --date 2026-02-15
```

Machine-readable output:

```bash
python3 scripts/check_today_workday.py --json
```

## Output Contract

Always return:
- Queried date (YYYY-MM-DD)
- `is_workday` boolean
- Reason (`holiday override` or `weekday fallback`)
- Data source URL
