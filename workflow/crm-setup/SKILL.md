---
name: crm-setup
description: >
    End-to-end guide for building a CRM using the Frontline CLI.
    Covers creating custom objects/tables with fields, setting up relations
    between entities, adding pipeline stages, populating data, and querying
    across related objects. Use as a reference when building any multi-entity
    business workflow from scratch.
    IMPORTANT: Before designing new entities or fields, always read the
    `frontline-internals` skill to understand what the system already handles
    automatically (activity sync, consolidation, built-in objects).
allowed-tools: Bash(frontline:*)
---

# Building a CRM with the Frontline CLI

> [!IMPORTANT]
> **Read the [`crm-objects`](../crm-objects/SKILL.md) skill first.**
> It has the complete field catalog, background automations, auto-creation rules,
> AI profile/summary behavior, and deduplication logic for each built-in object.
> Also read [`frontline-internals`](../frontline-internals/SKILL.md) for the broader
> platform mechanics (activity sync, memories, consolidation).
> Designing entities that duplicate built-in behaviour leads to split history and inconsistent data.

This skill walks through building a complete CRM system: Companies, Contacts,
and Deals — with relations, pipeline stages, record types, and views.

> The built-in `companies`, `people`, and `deals` objects already
> exist. This guide uses **custom objects** to show how to build everything from
> scratch, but the same patterns apply when extending existing objects.

## Available Field Types

| Type            | Usage                                    | Value format             |
| --------------- | ---------------------------------------- | ------------------------ |
| `string`        | Text fields (name, email, url)           | `"text"`                 |
| `number`        | Numeric fields (amounts, counts)         | `42`                     |
| `date`          | Timestamps                               | `"2026-04-17T00:00:00Z"` |
| `dateOnly`      | Date without time                        | `"2026-04-17"`           |
| `boolean`       | True/false toggles                       | `true` / `false`         |
| `select`        | Single/multi-select (options with color) | `[1, 3]` (option IDs)    |
| `relation`      | Link to records in another table         | `["record_id_1"]`        |
| `autoIncrement` | Auto-generated sequential ID             | _(auto)_                 |
| `file`          | File attachment                          | _(upload only)_          |

## Available Option Colors

When creating options for select fields, use these color **names** (case-insensitive).
Note this is a **different palette** from icon colors.

| Name       | Hex       |
| ---------- | --------- |
| Terracotta | `#D08F6D` |
| Amber      | `#FFCA41` |
| Lime       | `#D4F997` |
| Emerald    | `#00DC71` |
| Lavender   | `#B76FFF` |
| Sky        | `#339AFF` |
| Magenta    | `#FE55AA` |
| Bright Red | `#E90012` |
| Teal       | `#00D1B7` |
| Gray       | `#727272` |
| Brown      | `#775B49` |
| Orange     | `#8D4818` |
| Yellow     | `#846826` |
| Green      | `#237045` |
| Blue       | `#215B9D` |
| Purple     | `#7132A2` |
| Pink       | `#A32662` |
| Red        | `#A0362E` |

> Snapshot — run `frontline guidance icons` (field `optionColors`) for the authoritative list. See the `guidance` skill.

## Step 1 — Create the Objects or Tables

Use `object create` for business entities and `table create` for simple data.

**Icons:** tables (`table create` / `table update`) use a **Unicode emoji** in `emoji` (e.g. `"🚚"`). Objects use an **icon key** string (e.g. `"handshake"`). Do not mix the two formats.

```bash
# Create a new "Embarques" table
frontline table create embarques --data '{
  "displayName": "Embarques",
  "emoji": "🚚",
  "icon_color": "orange",
  "columns": [
    { "name": "Nombre", "type": "string", "metadata": { "format": "text" } }
  ]
}'

# Create a new "Pedidos" table
frontline table create pedidos --data '{
  "displayName": "Pedidos",
  "emoji": "📦",
  "icon_color": "blue",
  "columns": [
    { "name": "Nombre", "type": "string", "metadata": { "format": "text" } }
  ]
}'
```

The system also ships with these core objects:

```
companies  — Companies
people     — People (contacts)
deals      — Deals (sales pipeline)
```

Verify they exist:

```bash
frontline object list
```

### Setting Icons on Existing Objects/Tables

```bash
# Objects take an icon KEY for emoji; tables take a literal emoji.
frontline object update deals --data '{"emoji": "handshake", "icon_color": "emerald"}'
frontline table update embarques --data '{"emoji": "🚚", "icon_color": "teal"}'
```

### Available Icon Colors

Use the `icon_color` field with a **color name** (case-insensitive):

`red`, `orange`, `amber`, `yellow`, `lime`, `green`, `emerald`, `teal`,
`cyan`, `sky`, `blue`, `indigo`, `violet`, `purple`, `pink`, `rose`

> Snapshot — run `frontline guidance icons` (field `iconColors`) for the authoritative name→hex list.

## Step 2 — Inspect & Extend the Schema

### View current fields

```bash
frontline object field list companies
frontline object field list people
frontline object field list deals
```

### Add custom fields

```bash
# Add a "Probability %" number field to Deals
frontline object field create deals --data '{
  "name": "Probability",
  "type": "number",
  "metadata": { "format": "percent" }
}'

# Add a "Next Follow-up" date field to Deals
frontline object field create deals --data '{
  "name": "Next Follow-up",
  "type": "dateOnly",
  "metadata": {}
}'
```

## Step 3 — Understand Relations

The built-in objects already have relations defined:

```bash
frontline object schema people
# → relations: [{ name: "companies", target: "companies", mode: "multi" }]

frontline object schema deals
# → relations: [
#     { name: "people", target: "people", mode: "multi" },
#     { name: "company", target: "companies", mode: "single" }
#   ]
```

The `name` field is what you use in all relation commands.

## Step 4 — Populate Data

### Create companies

```bash
frontline object record create companies --data '{
  "Name": "Acme Corp",
  "Domain": "acme.com",
  "Primary Location": "New York, USA"
}'
# → { id: "6625aaa...", ... }

frontline object record create companies --data '{
  "Name": "TechStart Inc",
  "Domain": "techstart.io",
  "Primary Location": "San Francisco, USA"
}'
# → { id: "6625bbb...", ... }
```

### Create contacts

```bash
frontline object record create people --data '{
  "First Name": "Alice",
  "Last Name": "Johnson",
  "Email": "alice@acme.com",
  "Phone Number": "+1-555-0101",
  "Role": "VP Sales"
}'
# → { id: "6625ccc...", ... }

frontline object record create people --data '{
  "First Name": "Bob",
  "Last Name": "Smith",
  "Email": "bob@techstart.io",
  "Role": "CTO"
}'
# → { id: "6625ddd...", ... }
```

### Create deals

```bash
# Use option IDs from `frontline object field list deals`
# Stage options: 1=Lead, 2=In Progress, 3=Won, 4=Lost

frontline object record create deals --data '{
  "Name": "Acme Enterprise License",
  "Stage": [2],
  "Value": 150000
}'
# → { id: "6625eee...", ... }
```

## Step 5 — Link Records

### Link person → company

```bash
# Alice works at Acme
frontline object relation link people 6625ccc... Companies 6625aaa...

# Bob works at TechStart
frontline object relation link people 6625ddd... Companies 6625bbb...
```

### Link deal → company and deal → person

```bash
# The Acme deal belongs to Acme Corp
frontline object relation link deals 6625eee... Company 6625aaa...

# Alice is the contact for this deal
frontline object relation link deals 6625eee... People 6625ccc...
```

### Verify links

```bash
# What company does Alice belong to?
frontline object relation get people 6625ccc... Companies

# Who are the contacts for the Acme deal?
frontline object relation get deals 6625eee... People

# Which deals belong to Acme Corp? (reverse lookup)
frontline object relation find-by deals Company 6625aaa...

# Which people work at Acme Corp? (reverse lookup)
frontline object relation find-by people Companies 6625aaa...
```

## Step 6 — Set Up Pipeline Views

### Create record types for deal stages

```bash
# Get the field IDs to include in each record type
frontline object field list deals
# → Use the IDs for Name, Stage, Value, People, Company

frontline object record-type create deals --data '{
  "name": "active_pipeline",
  "displayName": "Active Pipeline",
  "columnIds": [1, 2, 3, 5, 8]
}'
# → { id: 7, ... }
```

### Create a kanban board for the pipeline

```bash
# Use the Stage field ID for grouping (e.g., field ID 2)
# Create directly on the object (no record type needed)
frontline object view create deals --data '{
  "name": "Pipeline Board",
  "type": "KANBAN",
  "metadata": { "groupingColumnId": 2 }
}'

# Or scoped to a specific record type with --record-type <id>
frontline object view create deals --record-type 7 --data '{
  "name": "Pipeline Board",
  "type": "KANBAN",
  "metadata": { "groupingColumnId": 2 }
}'
```

> View types must be uppercase: `KANBAN`, `TABLE`, `RECORD`.

## Step 7 — View Customization (Ordering and Visibility)

Refine your views to show only the most important information:

```bash
# Set order of columns/fields
frontline object view update deals <view-id> --column-order "Name, Stage, Value, Company"

# Hide less relevant fields
frontline object view update deals <view-id> --hidden-columns "createdAt, updatedAt"

# Order fields in the record creation dialog
frontline object view update deals <view-id> --dialog-field-order "Name, Stage, Value, Probability"
```

## Step 8 — Query Your CRM

### Find high-value deals

```bash
frontline object record list deals --query '{
  "operator": "and",
  "conditions": [
    { "path": "[Value]", "operator": "gte", "value": 50000 },
    { "path": "[Stage]", "operator": "containsAny", "value": [2] }
  ]
}' --sort '[{"path": "[Value]", "type": "desc"}]'
```

### Find contacts with no company

```bash
frontline object record list people --query '{
  "path": "[Companies]", "operator": "isNull"
}'
```

### Search across fields

```bash
frontline object record list people --search "alice"
frontline object record list companies --search "tech"
```

### Find all contacts at a specific company

```bash
frontline object relation find-by people Companies <company-id>
```

## Step 8 — Export & Backup

```bash
# Export all deals to spreadsheet
frontline object export xlsx deals --output deals_report.xlsx

# Export filtered data (only won deals)
frontline object export csv deals \
  --query '{"path": "[Stage]", "operator": "containsAny", "value": [3]}' \
  --output won_deals.csv

# Export all contacts
frontline object export xlsx people --output contacts_backup.xlsx
```

## Quick Command Reference

```
┌──────────────────────────────────────────────────────────────────┐
│ SCHEMA                                                           │
│  frontline object list                                           │
│  frontline object schema <obj>                                   │
│  frontline object field list <obj>                               │
│  frontline object field create <obj> --data '{...}'              │
│  frontline object option create <obj> <field-id> --data '{..}'   │
├──────────────────────────────────────────────────────────────────┤
│ RECORDS                                                          │
│  frontline object record create <obj> --data '{...}'             │
│  frontline object record list <obj> [--query] [--search]         │
│  frontline object record get <obj> <id>                          │
│  frontline object record update <obj> <id> --data '{...}'        │
│  frontline object record delete <obj> <id>                       │
├──────────────────────────────────────────────────────────────────┤
│ RELATIONS                                                        │
│  frontline object relation link <obj> <id> <rel> <target>        │
│  frontline object relation unlink <obj> <id> <rel> <target>      │
│  frontline object relation get <obj> <id> <rel>                  │
│  frontline object relation find-by <obj> <rel> <target-id>       │
├──────────────────────────────────────────────────────────────────┤
│ VIEWS & RECORD TYPES                                             │
│  frontline object record-type list <obj>                         │
│  frontline object record-type create <obj> --data '{...}'        │
│  frontline object view list <obj>                                │
│  frontline object view create <obj> [--record-type <id>] --data '{...}' │
├──────────────────────────────────────────────────────────────────┤
│ EXPORT                                                           │
│  frontline object export xlsx <obj> [--query] [--output]         │
│  frontline object export csv <obj> [--query] [--output]          │
└──────────────────────────────────────────────────────────────────┘
```

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
