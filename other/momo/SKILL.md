---
name: momo
description: Momo namespace for Netsnek e.U. time tracking and invoicing tool for freelancers. Logs work hours, generates timesheets, creates invoices, and tracks payments.
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os: [linux]
    permissions: [exec]
  minis:
    originalSource: "https://clawskills.sh/skills/kleberbaum-momo"
    convertedAt: "2026-10-31T22:12:39.706Z"
    license: "Unknown"
---

# Momo

## Time is Money

Momo helps freelancers track hours and get paid. Log work as you go, generate timesheets for clients, and create invoices that match your logged time.

Invoke Momo when logging time, preparing reports, or generating client invoices.

## Tracking Workflow

1. **Log** — Record hours against projects and tasks
2. **Report** — Aggregate time by project, client, or date range
3. **Invoice** — Turn logged time into line items on an invoice

## Timesheet Commands

```bash
# Log new time entry
./scripts/timesheet.sh --log --project "Acme Corp" --hours 2.5 --task "API design"

# Generate report
./scripts/timesheet.sh --report --from 2026-02-01 --to 2026-02-18

# Create invoice from logged time
./scripts/timesheet.sh --invoice --client "Acme Corp" --period Feb-2026
```

### Arguments

| Argument   | Purpose                              |
|------------|--------------------------------------|
| `--log`    | Add a time entry (project, hours, task) |
| `--report` | Generate timesheet or summary report |
| `--invoice`| Create invoice from logged hours     |

## Freelancer Story

**Scenario**: You completed 12 hours for Acme Corp in February.

1. `timesheet.sh --log` — Add entries as you work (or batch at end of week).
2. `timesheet.sh --report --period Feb-2026` — Review and verify totals.
3. `timesheet.sh --invoice --client "Acme Corp"` — Generate PDF invoice and track sent/paid status.
