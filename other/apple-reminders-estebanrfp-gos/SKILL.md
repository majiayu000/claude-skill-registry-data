---
name: apple-reminders
description: Manage Apple Reminders (macOS). Use when the user wants to see pending reminders, create new ones, or mark them as done.
---

# Apple Reminders (GenosOS)

Manage reminders via the dedicated `reminders` tool. Secure — no exec or osascript exposed.

## Actions

```
reminders({ action: 'list' })                                          → pending reminders
reminders({ action: 'create', title: 'Buy milk', dueDate: '2026-03-25' })
reminders({ action: 'complete', index: 1 })                            → mark first as done
```

## When to Use

- User mentions "reminder" or "Reminders app"
- Creating personal to-dos with due dates that sync to iOS
- Managing Apple Reminders lists

## When NOT to Use

- Scheduling GenosOS tasks or alerts → use `cron` tool
- Calendar events → use `calendar` tool
- One-time notifications → use `cron` tool

## Notes

- macOS only — reads from Apple Reminders app
- Default list: "Reminders" (use listName parameter to change)
- dueDate is optional (format: YYYY-MM-DD)
- First run may trigger macOS permission prompt
