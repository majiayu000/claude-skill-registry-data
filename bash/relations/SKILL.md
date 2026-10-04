---
name: relations
description: >
    How to manage relations between object records using the Frontline CLI.
    Use when you need to link or unlink records between objects (e.g., assign
    a Person to a Company), query related records, or perform reverse lookups.
allowed-tools: Bash(frontline:*)
---

# Managing Relations

## Creating Relation Fields

There are two relation field types:

### `relation` — object to object

Links records in one object to records in another. Before creating, run `frontline object get <target>` to get:

- `data.id` → use as `relatedTableId`
- the field you want displayed (e.g. Name) → its `id` → use as `displayColumn`

```bash
frontline object field create <source-obj> --data '{
  "name": "Company",
  "type": "relation",
  "metadata": {
    "relatedTableId": 1,
    "displayColumn": 1,
    "mode": "single",
    "relatedRecordTypeIds": [2, 3]
  }
}'
```

- `relatedTableId`: numeric ID of the target object/table.
- `displayColumn`: numeric field ID from the target to use as the display label.
- `mode`: `"single"` (many-to-one) or `"multi"` (one-to-many).
- `relatedRecordTypeIds` (optional, array of numbers): restrict linked records to specific record types on the target object.
- `includeActivity` (optional, boolean, default `false`): **custom objects only.** When `true`, a record's timeline also shows the activity of the records linked through this relation, merged automatically into the same activity endpoint (the response shape is unchanged). Editable on update.

### Merge related activity into the timeline (`includeActivity`)

For relations on **custom objects**, set `includeActivity: true` so the parent record's activity feed also includes the activity of its related records:

```bash
# On create
frontline object field create <source-obj> --data '{
  "name": "Company",
  "type": "relation",
  "metadata": { "relatedTableId": 1, "displayColumn": 1, "mode": "single", "includeActivity": true }
}'

# Toggle on update
frontline object field update <source-obj> <field-id> --data '{
  "metadata": { "includeActivity": true }
}'
```

The flag is returned on the field as `include_activity`. It only applies to custom objects — standard objects manage their timeline separately and ignore it.

### `prismaRelation` — object to platform user

Links records to Frontline platform users (e.g. for "Assignee" or "Owner" fields):

```bash
frontline object field create <source-obj> --data '{
  "name": "Assignee",
  "type": "prismaRelation",
  "metadata": {
    "prismaModel": "User",
    "displayField": "fullName",
    "mode": "single"
  }
}'
```

- `prismaModel`: `"User"` for platform users (required).
- `displayField`: `"fullName"` for `User` (required — this is the resolver's display property).
- `mode`: `"single"` or `"multi"`.

## Discovering Relations

Before working with relations, inspect the object schema to find relation names:

```bash
frontline object schema people
```

The output includes a `relations` array:

```json
{
    "relations": [
        {
            "name": "company",
            "target": "companies",
            "mode": "multi",
            "display_field": "Name"
        },
        { "name": "deals", "target": "deals", "mode": "multi", "display_field": "Name" }
    ]
}
```

The `name` field is what you use as the `<relation>` argument.

## Link a Record

Connect a source record to a target record through a named relation:

```bash
frontline object relation link <object> <source-id> <relation> <target-id>
```

> ⚠️ **People → Company is auto-linked by email domain. Don't do it manually unless one of the exceptions applies.**
>
> When a Person was created/updated with an email on a non-generic domain (anything other than gmail, outlook, etc.), the platform already linked them to the Company matching that domain (creating the Company if needed). Calling `relation link people <id> Companies <company-id>` right after `record create people` is almost always wrong — it either duplicates the auto-link or pisses on a Company the platform was about to enrich for you.
>
> **Only call `relation link` for People → Companies when:**
>
> - The Person has no email, or the email domain is generic (gmail/outlook/yahoo/icloud/etc.).
> - You want to **override** the auto-linked Company with a different one. In that case: read the current link, `relation unlink` it, then `relation link` the intended Company.
> - The user gave you an explicit company name that differs from what the domain implies and you've verified it's the right target.
>
> See `crm-objects` skill → People → top-of-section warning for the full ruleset and `companyAutoLinkEnabled` gate.

```bash
# Link a person to a company — only for the exceptions listed above.
# Verify auto-link did NOT already handle this before running.
frontline object relation link people 6625abc123def456 Companies 6625def789abc012
```

- **Idempotent**: linking the same target twice won't create duplicates.
- Returns the updated source record.

## Unlink a Record

Remove a link between two records:

```bash
frontline object relation unlink <object> <source-id> <relation> <target-id>
```

```bash
# Remove person from company
frontline object relation unlink people 6625abc123def456 Companies 6625def789abc012
```

## Get Related Records (Forward Lookup)

"What records does this person point to through `Companies`?"

```bash
frontline object relation get <object> <source-id> <relation>
```

```bash
# Get all companies linked to this person
frontline object relation get people 6625abc123def456 Companies
```

Returns an array of related records with their full data.

## Find by Relation (Reverse Lookup)

"Which people point to this company?"

```bash
frontline object relation find-by <object> <relation> <target-id> [--page N] [--page-size N]
```

```bash
# Find all people linked to a specific company
frontline object relation find-by people Companies 6625def789abc012

# With pagination
frontline object relation find-by people Companies 6625def789abc012 --page 1 --page-size 20
```

Returns a paginated result: `{ rows, total_count, total_pages, current_page }`.

## Workflow: Transfer a Person Between Companies

```bash
# 1. Show current company links
frontline object relation get people <person-id> Companies

# 2. Unlink from old company
frontline object relation unlink people <person-id> Companies <old-company-id>

# 3. Link to new company
frontline object relation link people <person-id> Companies <new-company-id>

# 4. Verify
frontline object relation get people <person-id> Companies
```

## Workflow: Find All Deals for a Company

```bash
# Find deals linked to a company (reverse: deals that point to this company)
frontline object relation find-by deals Company <company-id>
```

## Filtering by Relation

You can also filter records by relations using the query system
(see `filter-and-query` skill):

```bash
# Find people with no company
frontline object record list people --query '{"path": "[Company]", "operator": "isNull"}'

# Find people linked to specific companies
frontline object record list people --query '{
  "path": "[Company]",
  "operator": "containsAny",
  "value": ["6625def789abc012", "6625def789abc999"]
}'
```

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
