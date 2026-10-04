---
name: feedback-pipeline
description: |
  Autonomous customer feedback intake pipeline: reads new submissions from a Google Sheet,
  routes each to the correct project owner via a routing table, sends a Slack/chat handoff,
  tracks response status, monitors SLA, escalates breaches, and emails the customer when
  resolved. Runs on a 4-hour cron cycle with a 2-hour escalation check. Use when feedback
  submissions need to reach the right person without manual triage, when SLA compliance is
  important, or when customer response loops are slow. Also for onboarding new projects into
  the feedback routing system, auditing open feedback, or rebuilding the pipeline state.
triggers:
  - /feedback-pipeline
  - feedback pipeline
  - process feedback
  - new feedback submissions
aliases: []
scope: agency-rooms
dept: [ops]
team: ["team-lead"]
priority: ops
author: agency-rooms
provenance: agency-rooms
last_updated: "2026-04-10"
trust_level: agent-authored
---

# Feedback Pipeline — Skill

## What this does

Autonomous customer feedback intake pipeline:

```
Customer fills Google Form → Sheet row (G=pending)
    │
    │ [Every 4h via cron, or anytime via /feedback-pipeline]
    │
    ├─ 1. Read new "pending" rows from Feedback sheet
    ├─ 2. Route project name → PD slug (routing.json)
    ├─ 3. Assign row (G=assigned, H={slug}-pd)
    ├─ 4. SendMessage to PD + write NEXUS handoff
    │
    │   PD handles work normally
    │
    │   PD signals completion — DUAL MECHANISM:
    │   ├─ SendMessage: "DONE feedback:{row}:{name} Response: {x}"
    │   └─ Sheet col K: set to "DONE"
    │
    ├─ 5. Detect DONE → sheet G=resolved, close row
    ├─ 6. gws gmail send to customer
    ├─ 7. Escalation check every 2h (SLA breach → G=escalated)
    └─ 8. State written to state.json

    Cron: 0 */4 * * *  (main loop)
    Cron: 0 */2 * * *  (escalation only)
```

---

## Files

```
~/.claude/skills/feedback-pipeline/
├── SKILL.md              ← this file
├── routing.json          ← project → PD slug mapping
├── feedback-sheet.ts     ← Google Sheets read/write (11-col schema)
├── feedback-pipeline.ts  ← main orchestrator
└── scripts/
    └── run.sh            ← bash entry for cron

~/.claude/agency-rooms/feedback/feedback-pipeline/
└── state.json            ← pipeline state (checkpoints, per-row state)
```

---

## Sheet Schema

Tab: `Feedback`

| Col | Header | Filled by |
|-----|--------|-----------|
| A | customer_name | Form |
| B | contact_email | Form |
| C | project_product | Form |
| D | feedback_type | Form |
| E | description | Form |
| F | submitted_at | Form |
| G | status | Pipeline (pending→assigned→resolved→closed/escalated) |
| H | assigned_to | Pipeline (PD slug) |
| I | pd_response | Pipeline or manual |
| J | resolved_at | Pipeline |
| K | pd_status | Pipeline/manual ("DONE" triggers completion) |

---

## Setup

### 1. Create Google Sheet + Form

1. Go to Google Sheets → New spreadsheet
2. Rename first tab to `Feedback`
3. Row 1 headers: `customer_name | contact_email | project_product | feedback_type | description | submitted_at | status | assigned_to | pd_response | resolved_at | pd_status`
4. Insert → Form (creates linked Google Form)
5. Configure form fields: Name, Email, Project (dropdown or text), Type (bug/improvement/question/request/complaint), Description
6. Copy the **Sheet ID** from the URL: `docs.google.com/spreadsheets/d/{THIS_PART}/edit`

### 2. Configure

```bash
# Edit state.json — set your sheet ID
cat ~/.claude/agency-rooms/feedback/feedback-pipeline/state.json
# Set "sheet_id" to the ID from step 1.5

# Verify routing.json has your PDs
cat ~/.claude/skills/feedback-pipeline/routing.json
```

### 3. Add routing

Edit `routing.json` to add new projects:
```json
{
  "project_to_pd": {
    "your-project": "your-pd-slug"
  },
  "aliases": {
    "shortcut": "your-project"
  }
}
```

### 4. Test manually

```bash
cd ~/.claude/skills/feedback-pipeline
tsx feedback-pipeline.ts

# Test escalation only
tsx feedback-pipeline.ts escalation
```

### 5. Start cron

```
/loop 4h /feedback-pipeline
/loop 2h "tsx ~/.claude/skills/feedback-pipeline/feedback-pipeline.ts escalation"
```

Or use CronCreate with:
- `0 */4 * * *` — main loop
- `0 */2 * * *` — escalation check

---

## PD Workflow

When a PD receives a feedback task (via SendMessage + NEXUS handoff):

1. Handle the work via normal PD workflow
2. When done, **both** of these:
   - Send team-lead: `DONE feedback:{row}:{customer_name} Response: {what was done}`
   - In the Feedback sheet, set column K (pd_status) to `DONE`

Either mechanism triggers resolution. Both together is fine too.

---

## Routing Resolution Order

1. Exact match in `project_to_pd` keys
2. Alias match → `project_to_pd`
3. Bidirectional partial contains (either direction)
4. Fallback: `fallback_pd` ("team-lead")

---

## State File

`~/.claude/agency-rooms/feedback/feedback-pipeline/state.json`

```json
{
  "last_processed_row": 1,
  "sheet_id": "...",
  "rows": {
    "2": { "status": "assigned", "assigned_to": "examplecrm-pd",
            "email": "...", "escalation_due": "2026-04-14T09:00:00Z",
            "notified_customer": false }
  },
  "sla": { "target_hours": 48, "warning_hours": 36 },
  "stats": { "total_processed": 0, "total_escalated": 0, "last_cycle": null }
}
```

---

## Manual Commands

| Command | What it does |
|---------|-------------|
| `tsx feedback-pipeline.ts` | Full cycle: detect new, route, DONE check, escalate |
| `tsx feedback-pipeline.ts escalation` | Escalation check only |
| `gws sheets +read --spreadsheet SHEET_ID` | Quick peek at sheet |
| `gws gmail send --to "x@y.com" ...` | Send test email |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `sheet_id not set` | Edit `state.json`, set `sheet_id` |
| `state.json not found` | Create at path above, see template in plan |
| PD not getting messages | Verify PD slug in `routing.json` matches actual agent name |
| Email not sending | Run `gws auth status` to check Gmail auth |
| Double-processing | `notified_customer: true` in state prevents re-trigger |
