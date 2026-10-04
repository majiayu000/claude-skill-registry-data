---
name: record-type-management
description: >
    How to manage record types and views for custom objects using the Frontline CLI.
    Record types allow you to group fields, and views (Table/Kanban) allow 
    you to visualize records for a specific record type.
allowed-tools: Bash(frontline:*)
---

# Record Type Management

Custom Objects support multiple **Record Types**. Each record type can have one or more **Views** (Table or Kanban).

> **Note:** Extra **record types** and `frontline object view ...` / `frontline object record-type ...` apply to **Objects** (`frontline object create`).
> **Tables** (`frontline table create`) keep a single implicit record type and return `404` if you pass a table name to those object commands — but Tables still have their own **views** via table APIs (`frontline table get`, table view endpoints), not via `object view`.

## Permissions

Creating, updating, and deleting record types (and views) requires an API key whose user is
**ADMIN** or **OWNER**; anything else returns `403`. Listing is available to any user who can
see the object. Record types define the account's shared CRM model, so unlike table schemas
they cannot be delegated with `frontline sharing set`.

## Record Types

A record type is a subset of fields (columns) from the object.

> **Record types share ONE underlying object — not separate storage.** Unique constraints and
> deduplication are enforced object-wide, across all record types. For People that means Email
> (primary) and Phone Number (secondary) can't repeat even across a "Lead" and a "Person" type.
> **Converting** a record (e.g. lead → customer) = changing its record type, NOT creating a new
> record. Search before creating to avoid duplicates.

### List Record Types

```bash
frontline object record-type list <object-name>
```

### Create a Record Type

Pass `columnIds` (numeric field IDs) to control which fields belong to this record type. Get field IDs from `frontline object get <object>`. Both create and update support `columnIds`:

```bash
frontline object record-type create <object-name> --data '{
  "name": "my_type",
  "displayName": "My Record Type",
  "columnIds": [1, 2, 5]
}'
```

> **Important:** Always use `columnIds` (array of numbers). `fieldNames` is accepted by the API but is not wired to field assignment and will be silently ignored.

#### Skipping enrichment (`disableSideEffects`)

Both create and update accept an optional `disableSideEffects` boolean (default `false`). When `true`, records of this type are saved **without running automatic enrichment**: AI-generated summaries/profiles, enrichment from external sources (logos, company info, social links), and auto-linking records to one another (e.g. matching a person to a company by email domain).

Everything else keeps running so the data stays usable:

- **RAG sync** — records remain searchable by Max and your agents.
- **Activity/audit-log mirroring** — the activity history is still recorded.
- **Automations** — triggers still fire.
- **Composed/computed fields (e.g. Full Name), defaults and validations** — always run (before-hooks).

Use it for bulk imports or whenever you want full manual control over a record's data.

```bash
# Create a record type that skips automatic enrichment
frontline object record-type create <object-name> --data '{
  "name": "import",
  "displayName": "Import",
  "disableSideEffects": true
}'

# Toggle it on an existing record type
frontline object record-type update <object-name> <record-type-id> --data '{
  "disableSideEffects": true
}'
```

The flag is returned on the record type as `disable_side_effects`.

### Update a Record Type

```bash
# Rename
frontline object record-type update <object-name> <record-type-id> --data '{
  "displayName": "Updated Name"
}'

# Update fields assigned to the record type
frontline object record-type update <object-name> <record-type-id> --data '{
  "columnIds": [1, 2, 5, 10]
}'
```

**The default record type is protected.** You cannot change its `name` or `displayName`, and you cannot delete it — both return `400`. Its `columnIds`, emoji, and color can still be updated while it is the default.

### Delete a Record Type

```bash
frontline object record-type delete <object-name> <record-type-id>
```

You cannot delete the default record type — promote another one to default first.

---

## Views

Views always belong to a specific record type. The view commands take the **object
name (slug)** as the positional argument; pass `--record-type <id>` on create to
target a specific record type (the default record type is used if omitted).

### Create a Kanban View

Requires a `groupingColumnId` (must be a single-select field). View types are
uppercase: `KANBAN`, `TABLE`, `RECORD`.

The first argument is the **object name**. Pass `--record-type <id>` to scope the view to a specific record type; the object's default record type is used when it is omitted.

```bash
frontline object view create <object-name> --record-type <record-type-id> --data '{
  "name": "Process Board",
  "type": "KANBAN",
  "metadata": { "groupingColumnId": 12 }
}'
```

### Create a Table View

```bash
frontline object view create <object-name> --record-type <record-type-id> --data '{
  "name": "Full List",
  "type": "TABLE",
  "metadata": {}
}'
```

### List Views

```bash
frontline object view list <object-name>
```

### Update a View

```bash
# Rename the view
frontline object view update <object-name> <view-id> --name "Renamed View"

# Refine view metadata (Table/Kanban)
frontline object view update <object-name> <view-id> --column-order "First Name, Last Name, Email"
frontline object view update <object-name> <view-id> --hidden-columns "ID, createdAt"
frontline object view update <object-name> <view-id> --sticky-columns "First Name" # TABLE views only
frontline object view update <object-name> <view-id> --dialog-field-order "Email, Phone"
```

### Delete a View

```bash
frontline object view delete <object-name> <view-id>
```

---

## See also

- `record-security` skill — configure FLS per record type
- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
