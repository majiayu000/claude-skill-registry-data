---
name: nex-deliverables
description: "Client deliverable tracking and project management system for web agencies, design studios, marketing firms, and freelancers managing multiple simultaneous projects and client relationships. Use when the user says \"track deliverables\", \"what's overdue\", \"send a status update to client\", \"add a new project deliverable\", \"I need to see what's in review\", or when managing multiple client projects with deadlines and status tracking."
version: 1.0.0
metadata:
  clawdbot:
    emoji: "📋"
    requires:
      bins:
        - python3
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-deliverables.py"
      - "lib/*"
      - "setup.sh"
scope: instance
invocation: workflow
---

<!-- provenance: ABSORBED FROM: /Users/marcelspatz/YURI-OS-MUSUBI/RESEARCH/ORACLE-CORPUS/openclaw-skills/skills/nexaiguy/nex-deliverables | scanned: 2026-05-17 | score: 10 -->

# Nex Deliverables

Client Deliverable Tracker for agency operators and freelancers. Monitor project status, track deadlines, manage client workload, and generate professional status updates. All data is stored locally on your machine—no external services required.

## When to Use

Use this skill when you need to:

- Add a new deliverable for a client project
- Update the status of a deliverable (planned, in progress, review, delivered, approved)
- Check which deliverables are overdue
- List all open deliverables for a specific client
- See the current workload across all clients
- Generate a status update email for a client
- Find a specific deliverable by searching
- Export deliverables to CSV or JSON
- View delivery statistics (delivery rate, average time to deliver, overdue percentage)

Trigger phrases: "what's open for", "what's still pending", "mark as delivered", "is this overdue", "deliverable status", "what was promised", "client status", "what's due", "deadline", "oplevering", "has this been approved", "show overdue", "client deliverables"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, installs any dependencies, and initializes the database.

## Available Commands

The CLI tool is `nex-deliverables`. All commands output plain text.

### Add Deliverable

Add a new deliverable for a client:

```bash
nex-deliverables add --client "Ribbens Airco" --title "Homepage redesign" --type website --deadline 2026-05-01
nex-deliverables add --client "ECHO Management" --title "Brand guidelines" --type branding --priority high
nex-deliverables add --client "Bakkerij Peeters" --title "Landing page" --type landing_page --deadline "next friday" --priority urgent
```

Deadline shortcuts: "today", "tomorrow", "next week", "next friday", or YYYY-MM-DD format.

### Manage Clients

Add, view, or list clients:

```bash
nex-deliverables client add --name "Ribbens Airco" --contact-name "John Ribbens" --email "john@ribbens.be" --phone "+32-123-456"
nex-deliverables client show --name "Ribbens Airco"
nex-deliverables client list
nex-deliverables client list --status active
```

### List Deliverables

List all deliverables with optional filters:

```bash
nex-deliverables list
nex-deliverables list --client "Ribbens Airco"
nex-deliverables list --status in_progress
nex-deliverables list --type website
nex-deliverables list --priority urgent
nex-deliverables list --overdue
nex-deliverables list --client "Ribbens Airco" --status in_progress
```

Statuses: planned, in_progress, review, delivered, approved, rejected
Types: website, landing_page, design, logo, branding, copy, email_campaign, automation, funnel, seo, maintenance, custom
Priorities: urgent, high, normal, low

### Show Deliverable Details

View full details of a specific deliverable:

```bash
nex-deliverables show 42
nex-deliverables show "Homepage redesign"
```

Shows full details including timeline, milestones, status history, and notes.

### Update Status

Update a deliverable's status by ID:

```bash
nex-deliverables status 42 delivered
nex-deliverables status 42 approved --message "Client signed off"
nex-deliverables status 15 in_progress
```

### Mark by Title

Quick status update by title (searches for best match):

```bash
nex-deliverables mark "Ribbens Airco homepage" delivered
nex-deliverables mark "ECHO brand guidelines" approved
```

### Show Overdue

Display all overdue deliverables across all clients:

```bash
nex-deliverables overdue
```

### Search

Full-text search across titles, descriptions, and notes:

```bash
nex-deliverables search "website"
nex-deliverables search "logo"
nex-deliverables search "Ribbens"
```

### Workload Summary

View overall workload and project distribution:

```bash
nex-deliverables workload
```

Shows counts by status, priority, and type. Displays total deliverables and active clients.

### Generate Status Email

Create a professional status update email for a client:

```bash
nex-deliverables email "Ribbens Airco"
nex-deliverables email "ECHO Management"
```

Outputs a formatted email listing open, delivered, and overdue items.

### Export

Export deliverables to CSV or JSON:

```bash
nex-deliverables export --format csv --output deliverables.csv
nex-deliverables export --format json
nex-deliverables export --format csv --client "Ribbens Airco"
```

### Statistics

View delivery metrics and performance:

```bash
nex-deliverables stats
```

Shows total deliverables, delivery rate, average time to deliver, and overdue percentage.

## Example Interactions

**User:** "What's still open for Ribbens Airco?"
**Agent runs:** `nex-deliverables list --client "Ribbens Airco" --status in_progress`
**Agent:** Shows all in-progress deliverables with deadlines.

**User:** "Mark the ECHO Management homepage as delivered"
**Agent runs:** `nex-deliverables mark "ECHO Management homepage" delivered`
**Agent:** Confirms the status update.

**User:** "What deliverables are overdue?"
**Agent runs:** `nex-deliverables overdue`
**Agent:** Lists all overdue items with how many days late.

**User:** "Generate a status email for Bakkerij Peeters"
**Agent runs:** `nex-deliverables email "Bakkerij Peeters"`
**Agent:** Outputs a professional email with open, delivered, and overdue items.

**User:** "Add a new deliverable: landing page for Bakkerij Peeters, deadline next Friday"
**Agent runs:** `nex-deliverables add --client "Bakkerij Peeters" --title "Landing page" --type landing_page --deadline "next friday"`
**Agent:** Confirms the deliverable was added with the calculated deadline.

**User:** "Show me the workload summary"
**Agent runs:** `nex-deliverables workload`
**Agent:** Displays counts by status, priority, and type across all clients.

**User:** "What's overdue?"
**Agent runs:** `nex-deliverables overdue`
**Agent:** Lists all overdue items with urgency indicators.

**User:** "Show me statistics on delivery performance"
**Agent runs:** `nex-deliverables stats`
**Agent:** Displays delivery rate, average time to deliver, and overdue rate.

**User:** "Export all deliverables to a CSV file"
**Agent runs:** `nex-deliverables export --format csv --output deliverables.csv`
**Agent:** Confirms the file was created.

## Output Parsing

All CLI output is plain text, structured for easy parsing:

- Deliverable IDs in brackets: `[42]`
- Status indicators: ⚪ planned, 🟡 in_progress, 🟠 review, 🟢 delivered, ✅ approved, ❌ rejected
- Overdue items marked with ⚠️
- Section headers separated with dashes
- Every command output ends with `[Nex Deliverables by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally. Do not show raw database paths or internal details.

## Important Notes

- All deliverable data is stored locally at `~/.nex-deliverables/`. No telemetry, no analytics.
- No external API calls are made—fully offline.
- Database is initialized automatically on first use.
- Deliverable types have default SLAs (Service Level Agreements) for automatic deadline calculation. For example, a website defaults to 30 days, a logo to 7 days.
- Deadlines support natural language shortcuts: "today", "tomorrow", "next week", "next Friday" for convenience.
- The system tracks full status history for each deliverable, showing when and how status changed.
- Search is case-insensitive and matches any part of title, description, or notes.
- Export formats: CSV (spreadsheet-friendly) and JSON (programmatic use).

## Troubleshooting

- **"Database not found"**: Run `bash setup.sh` to initialize the database.
- **"Deliverable not found"**: Check the spelling or use `nex-deliverables search` to find it.
- **"Client not found"**: Add the client first with `nex-deliverables client add --name "..."`.
- **No output**: Check that Python 3 is installed and accessible.

## Database Schema

The system uses SQLite with the following main tables:

- **clients**: Client information (name, contact, email, phone, retainer details, status)
- **deliverables**: Deliverable tracking (title, type, status, priority, deadline, dates, hours)
- **milestones**: Sub-tasks within deliverables
- **status_updates**: Historical record of all status changes

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
Author: Kevin Blancaflor

## Session Notes

### 2026-06-16
- session: 178m | peak ctx: 0% | compacts: 0
- tools: Bash×205, Read×121, WebFetch×114, Edit×87, WebSearch×72, Write×33, TodoWrite×13, Agent×10, ToolSearch×9, Skill×4, AskUserQuestion×1, mcp×1, TaskStop×1
- corrections: go over it again, full red team and grounding in more fresh online research together with local, then check the compatibility across other organs, run phase 1. all agentic nano swarm | 'The legal one is the wall: an Austria-resident running automated Polymarket ' rick we are not doing full automated trading on polymarket, also polymarket is allowed in austria, you mustve fact checke | go over it again, full red team and grounding in more fresh online research together with local, then check the compatibility across other organs, run phase 1. all agentic nano swarm
- errors: none
