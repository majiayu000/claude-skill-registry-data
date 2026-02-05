---
name: date-check
description: |
  Verify current date from system. Use when outputting dates, scheduling, or time-sensitive operations. Prevents knowledge cutoff errors.
---

# Date Check SKILL

## Purpose

Prevent date errors caused by knowledge cutoff.
Get accurate current date/time from the system.

## When to Use

### Automatic Triggers
- Before outputting dates or day of week
- Before using relative dates ("today", "tomorrow", "this week")
- Before mentioning schedules or deadlines
- Before outputting year-specific information

### Manual Check
- When user asks about dates
- When handling time-sensitive information

## Process

### Step 1: Get Current Date

```bash
date "+%Y-%m-%d %H:%M:%S %A"
```

Note: Output varies by system. Always trust the actual execution result.

### Step 2: Verify Against Environment

Cross-check with `Today's date` in environment info.

### Step 3: Use Correct Date

Use the verified date in your response.

## Important Reminders

1. **Never trust knowledge cutoff** - Always verify system date
2. **Pay special attention to year** - May default to wrong year
3. **Calculate relative dates** - Compute "last week", "next month" from current date

## Quick Reference

| Info | Command |
|------|---------|
| Today | `date "+%Y-%m-%d"` |
| Day of week | `date "+%A"` |
| Week number | `date "+%V"` |
| Day of year | `date "+%j"` |
