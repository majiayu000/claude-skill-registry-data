---
name: pipeline-setup
description: >
    How to set up a pipeline workflow using the Frontline CLI: create stage
    fields, configure options, create record types, and add kanban views.
    Use when building any staged workflow like sales pipelines, support
    ticket flows, or project tracking boards.
allowed-tools: Bash(frontline:*)
---

# Pipeline Setup Guide

A pipeline is a visual workflow where records move through stages (e.g.,
Lead → Qualified → Proposal → Won/Lost). This skill walks through building
one from scratch using the Frontline CLI.

## Anatomy of a Pipeline

A pipeline requires three things:

1. **A select field** — holds the current stage of each record
2. **A record type** — groups fields relevant to this pipeline
3. **A kanban view** — visualizes records as cards grouped by stage

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│   Lead   │   │ Qualified│   │ Proposal │   │   Won    │
│          │   │          │   │          │   │          │
│ ┌──────┐ │   │ ┌──────┐ │   │ ┌──────┐ │   │ ┌──────┐ │
│ │Deal A│ │   │ │Deal C│ │   │ │Deal E│ │   │ │Deal F│ │
│ └──────┘ │   │ └──────┘ │   │ └──────┘ │   │ └──────┘ │
│ ┌──────┐ │   │          │   │          │   │          │
│ │Deal B│ │   │          │   │          │   │          │
│ └──────┘ │   │          │   │          │   │          │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
     ← Kanban view grouped by "Stage" field →
```

## Step 1 — Create the Stage Field

If the object doesn't already have a stage/status field, create one:

```bash
# Check existing fields first
frontline object field list <object>

# Create a single-select field for stages
frontline object field create <object> --data '{
  "name": "Stage",
  "type": "select",
  "metadata": { "mode": "singleSelect" }
}'
```

Note the **field ID** from the response — you'll need it for the kanban view.

## Step 2 — Add Stage Options

Add stages in the order they should appear on the board.
Use colors to visually distinguish stages:

```bash
# Sales pipeline example
frontline object option create <object> <field-id> --data '{"name": "Lead", "color": "Gray"}'
frontline object option create <object> <field-id> --data '{"name": "Qualified", "color": "Sky"}'
frontline object option create <object> <field-id> --data '{"name": "Proposal Sent", "color": "Amber"}'
frontline object option create <object> <field-id> --data '{"name": "Negotiation", "color": "Lavender"}'
frontline object option create <object> <field-id> --data '{"name": "Won", "color": "Emerald"}'
frontline object option create <object> <field-id> --data '{"name": "Lost", "color": "Red"}'
```

### Color Suggestions by Stage Semantics

| Stage type           | Suggested color  |
| -------------------- | ---------------- |
| New / Unqualified    | Gray             |
| Active / In Progress | Sky, Blue        |
| Waiting / Pending    | Amber, Yellow    |
| Positive outcome     | Emerald, Green   |
| Negative outcome     | Red, Bright Red  |
| Special / VIP        | Lavender, Purple |

These are suggestions; for the full set of valid option colors run `frontline guidance icons`
(field `optionColors`).

## Step 3 — Create a Record Type

Record types let you define which fields are visible for this pipeline view.
Pick only the fields that are relevant to the workflow:

```bash
# First, find the field IDs you want to include
frontline object field list <object>
# Note the IDs for: Name, Stage, Value, Company, Owner, etc.

# Create the record type with those field IDs
frontline object record-type create <object> --data '{
  "name": "sales_pipeline",
  "displayName": "Sales Pipeline",
  "columnIds": [1, 2, 5, 8, 12]
}'
```

Note the **record type ID** from the response.

## Step 4 — Create a Kanban View

The kanban view groups records by the stage field. You can create it directly on
the object (uses the default record type) or on a specific record type:

```bash
# Directly on the object (recommended for simple pipelines)
frontline object view create <object> --data '{
  "name": "Pipeline Board",
  "type": "KANBAN",
  "metadata": { "groupingColumnId": <stage-field-id> }
}'

# On a specific record type (optional — use when you have multiple subtypes)
frontline object view create <object> --record-type <record-type-id> --data '{
  "name": "Pipeline Board",
  "type": "KANBAN",
  "metadata": { "groupingColumnId": <stage-field-id> }
}'
```

> `groupingColumnId` must be the ID of a single-select field.
> View type must be uppercase: `KANBAN`, `TABLE`, `RECORD`.

## Step 5 — Polish the View (Ordering and Visibility)

After creating a view, you can refine which columns are visible and in what order
without manually editing JSON. This is useful for keeping boards clean:

```bash
# Set a specific column order for the cards/table
frontline object view update <object> <view-id> --column-order "Subject, Priority, Status"

# Hide technical or system columns
frontline object view update <object> <view-id> --hidden-columns "Created At, Updated At"

# Freeze columns on the left (e.g., Name) for easier horizontal scrolling (TABLE views only)
frontline object view update <object> <view-id> --sticky-columns "Name, Stage"

# Configure the order of fields in the record creation/edit dialog
frontline object view update <object> <view-id> --dialog-field-order "Subject, Priority, Description"

# Set the order of columns (groups) in a Kanban board
frontline object view update <object> <view-id> --option-order "New, In Progress, Closed"
```

> [!TIP]
> **Prioritize Ergonomics**: Only show fields that help users make decisions at a
> glance. For a Kanban board, 3-4 fields is usually the sweet spot. For tables,
> hide system fields (`autoId`, `updatedAt`) unless they are strictly necessary.

## Step 6 — Populate and Verify

```bash
# Create some records with stages
frontline object record create <object> --data '{
  "Name": "Acme Enterprise Deal",
  "Stage": [1],
  "Value": 150000
}'

frontline object record create <object> --data '{
  "Name": "TechCorp License",
  "Stage": [2],
  "Value": 75000
}'

# Verify by listing records filtered by stage
frontline object record list <object> --query '{
  "path": "[Stage]", "operator": "containsAny", "value": [1]
}'
```

## Complete Example: Support Ticket Pipeline

```bash
# 1. The Status field already exists on tickets as a predefined field.
#    Check its field ID and existing options:
frontline object field list tickets
# → Status field ID = 64, existing options: New, On You, On Customer, On Hold, Closed

# 2. Add more stages to the existing Status field (optionsEditable: true)
frontline object option create tickets 64 --data '{"name": "Escalated", "color": "Bright Red"}'
frontline object option create tickets 64 --data '{"name": "Waiting on Vendor", "color": "Amber"}'

# 3. Also add a priority field
frontline object field create tickets --data '{
  "name": "Priority",
  "type": "select",
  "metadata": { "mode": "singleSelect" }
}'
# → { id: 11, ... }

frontline object option create tickets 11 --data '{"name": "Critical", "color": "Bright Red"}'
frontline object option create tickets 11 --data '{"name": "High", "color": "Magenta"}'
frontline object option create tickets 11 --data '{"name": "Medium", "color": "Amber"}'
frontline object option create tickets 11 --data '{"name": "Low", "color": "Gray"}'

# 4. Create record type with relevant fields
frontline object field list tickets
# → Suppose: 1=Subject, 10=Status, 11=Priority, 5=Assignee, 3=Description

frontline object record-type create tickets --data '{
  "name": "support_board",
  "displayName": "Support Board",
  "columnIds": [1, 10, 11, 5, 3]
}'
# → { id: 4, ... }

# 5. Create kanban view grouped by Status — directly on the object
frontline object view create tickets --data '{
  "name": "Ticket Board",
  "type": "KANBAN",
  "metadata": { "groupingColumnId": 10 }
}'

# 6. Create a table view too (for list browsing)
frontline object view create tickets --data '{
  "name": "All Tickets",
  "type": "TABLE",
  "metadata": {}
}'
```

## Tips

- **Stage order can be customized** — use `--option-order` to control the Kanban board grouping order independently of the global select field settings.
- **One select field per board** — each kanban view groups by exactly one select field
- **Multiple pipelines** — create different record types for different workflows on the same object (e.g., "Sales Pipeline" and "Partner Pipeline" on Deals)
- **Add a table view too** — kanban is great for workflow, but a table view is useful for filtering and bulk operations
- **Use relations** — link pipeline records to people/companies for context (`frontline object relation link`)

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
