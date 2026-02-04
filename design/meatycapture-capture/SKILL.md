---
name: meatycapture-capture
description: Capture bugs/enhancements/ideas to request-logs. For quick operations use /mc command instead.
---

# MeatyCapture Skill

Request-log markdown files for development tracking.

## Quick Commands (use `/mc` for simple operations)

| Command | Example |
|---------|---------|
| List | `meatycapture log list PROJECT --json` |
| View | `meatycapture log view PATH --json` |
| Search | `meatycapture log search "query" PROJECT --json` |
| Capture | `meatycapture log create --json < input.json` |

## Workflows (load only when needed)

| Action | When to Load |
|--------|--------------|
| [Capture](./workflows/capturing.md) | Batch capture, validation, templates |
| [View/Search](./workflows/viewing.md) | Advanced filters, output formats |
| [Status Update](./workflows/updating.md) | Change item status |
| [Projects](./workflows/managing.md) | Configure projects, defaults |

## Field Reference

See [./references/field-options.md](./references/field-options.md) for valid values.
