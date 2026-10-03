---
name: china-holidays
description: Query Chinese statutory holidays (法定节假日), makeup work days (调休上班日), and holiday schedules. Use when the user asks about Chinese holidays, whether a specific date is a workday or holiday, Spring Festival dates, National Day dates, or any Chinese holiday-related questions.
---

# China Holidays

Query Chinese statutory holidays, makeup work days, and schedules.

## Quick Start

Run the script without arguments to see upcoming holidays:

```bash
python3 scripts/query.py
```

Query a specific date:

```bash
python3 scripts/query.py 2026-02-08
```

## Output Examples

**Upcoming holidays:**
```
📅 未来 60 天节假日安排
🎉 放假安排:
【春节】
  2026-02-15 (周日)
  ...
💼 调休上班日:
  2026-02-14 (周六) - 春节调休
```

**Specific date:**
```
🎉 2026-02-17 是【春节】放假
💼 2026-02-14 是【春节】调休上班日
😴 2026-02-08 是普通周末休息日
💼 2026-02-09 是普通工作日
```

## Data Source

Uses [holiday-cn](https://github.com/NateScarlet/holiday-cn) for official Chinese holiday data from the State Council.
