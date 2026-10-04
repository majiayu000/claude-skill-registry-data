---
name: crud-operations
description: >
    How to create, update, and delete fields, options, rows, record types, and views
    using the Frontline CLI. Use when managing the schema or data of tables and objects.
allowed-tools: Bash(frontline:*)
---

# CRUD Operations

The Frontline CLI provides full CRUD for every entity on tables and objects.
The surface is symmetric: anything you can do on a table, you can do on an object
(objects additionally support record types, views, and relations).

## Discovering the Schema

Before modifying anything, always inspect the schema first:

```bash
# List all tables / objects
frontline table list
frontline object list

# Get detailed schema (fields, relations, record types)
frontline table schema <name>
frontline object schema <name>

# List fields (includes field IDs, types, options for select fields)
frontline table field list <name>
frontline object field list <name>
```

## Fields

Fields are the columns of a table/object. Each field has an `id`, `name`, `type`,
and optional metadata depending on the field type.

### Field Types & Metadata Reference

| Type             | Allowed `metadata` keys                                                                                                   | Notes                                                                                                                                                                           | Example                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `string`         | `format`: `text`, `email`, `url`, `phone_number`; `extendedField` (bool)                                                  | `format` is **required** when `metadata` is provided. `extendedField:true` = long/multi-line text (e.g. Description). Invalid format → 400.                                     | `{"type":"string","metadata":{"format":"text","extendedField":true}}`                                                  |
| `number`         | `format`: `decimal`, `integer`, `percent`, `currency`; `decimals`; `currency`; `min` (number); `max` (number)             | `currency` (e.g. `"USD"`) only meaningful with `format:"currency"`. `min` and `max` enforce optional range boundaries. Invalid format → 400.                                    | `{"type":"number","metadata":{"format":"currency","currency":"USD","decimals":2,"min":0,"max":100}}`                   |
| `boolean`        | _(none)_                                                                                                                  | Any metadata is ignored.                                                                                                                                                        | `{"type":"boolean","metadata":{}}`                                                                                     |
| `date`           | `timezone` (IANA, e.g. `America/New_York`); `format`; `timeFormat`                                                        | Date **and** time.                                                                                                                                                              | `{"type":"date","metadata":{"timezone":"UTC"}}`                                                                        |
| `dateOnly`       | `format`                                                                                                                  | Date only, no time component.                                                                                                                                                   | `{"type":"dateOnly","metadata":{}}`                                                                                    |
| `select`         | `mode`: `singleSelect`, `multiSelect`                                                                                     | **Options are NOT created here** — see warning below. If `mode` is omitted, the backend defaults to `multiSelect`. Pass `metadata.mode` explicitly for single-select.           | `{"type":"select","metadata":{"mode":"singleSelect"}}`                                                                 |
| `relation`       | `mode`: `single`, `multi`; `relatedTableId` (number); `displayColumn` (number); `relatedRecordTypeIds` (array of numbers) | All first three are **required**. `relatedTableId` = target object's id; `displayColumn` = field id shown for links. `relatedRecordTypeIds` limits allowed linked record types. | `{"type":"relation","metadata":{"mode":"multi","relatedTableId":123,"displayColumn":45,"relatedRecordTypeIds":[1,2]}}` |
| `prismaRelation` | `prismaModel`: `User`/`Conversation` (req); `displayField` (req); `mode`: `single`/`multi`                                | Objects only. Links to platform users (assignees). Assign values as an array of user IDs.                                                                                       | `{"type":"prismaRelation","metadata":{"prismaModel":"User","displayField":"fullName","mode":"multi"}}`                 |
| `file`           | `showPreview` (bool); `allowedFileTypes` (string[]); `maxFileSize` (number)                                               | `maxFileSize` in bytes.                                                                                                                                                         | `{"type":"file","metadata":{"showPreview":true}}`                                                                      |

> **Notes**
>
> - **Timezone Validation:** For `date` columns, the `timezone` metadata property is strictly validated and must be a valid IANA timezone name from the supported list (e.g., `UTC`, `America/New_York`, `America/Chicago`, etc.). Invalid zones will result in a 400 Bad Request error.
> - Field `type` in create is `select` (mapped internally to `tags`). The API response also returns `"type": "select"`.
> - **`field update` cannot change a column's `type`.** To convert e.g. `string` → `select`, create a new `select` field, add its options, migrate record values if needed, then delete the old field when safe.
> - The create/update body is **strict**: unknown top-level keys (e.g. `options`, `tags`, `label`) are rejected with `400`, and only the keys listed above are meaningful inside `metadata` for each type. Other `metadata` keys are stored but ignored by the UI.

> ⚠️ **Select/multi-select options cannot be created inline.**
>
> Passing options inside the field-create body — whether as `metadata.options`, `metadata.tags`, or a top-level `options`/`tags` array — returns `400`. **The field-create endpoint only sets `mode`; it never creates options.**
>
> Create the field first, then add each option with `option create` (see [Options](#options-select-field-values) below). On **update**, the supported way to replace a select field's options is the top-level `tags` array (`field update <id> --data '{"tags":[...]}'`), not `metadata`.

### Create

```bash
# String field with email format
frontline table field create <table> --data '{
  "name": "Email",
  "type": "string",
  "metadata": { "format": "email" }
}'

# Number field with currency
frontline table field create <table> --data '{
  "name": "Amount",
  "type": "number",
  "metadata": { "format": "currency", "currency": "USD", "decimals": 2 }
}'

# Single-select field
frontline object field create <object> --data '{
  "name": "Priority",
  "type": "select",
  "metadata": { "mode": "singleSelect" }
}'

# Date field with timezone
frontline table field create <table> --data '{
  "name": "Due Date",
  "type": "date",
  "metadata": { "timezone": "America/New_York" }
}'
```

> **Objects with multiple record types:** a new field is added to **all** record types unless you scope it. Before creating a field on a multi-record-type object, if the user did not say which record type(s) it belongs to, list them (`frontline object record-type list <object>`) and ask. Choose "all" → omit `record_type_id`; one specific type → pass `record_type_id`. See the `schema-design` skill for details.

### Update

```bash
# Rename a field
frontline table field update <table> <field-id> --data '{"name": "Renamed Field"}'

# Mark a field as required
frontline object field update <object> <field-id> --data '{"required": true}'

# Add a unique constraint
frontline table field update <table> <field-id> --data '{"unique": true}'

# Combine multiple changes
frontline object field update <object> <field-id> --data '{"name": "Email", "required": true, "unique": true}'
```

Supported update keys: `name`, `metadata`, `required`, `unique`, `tags`, `defaultValue`.

> **Column type is immutable after create.** Do not pass `"type"` in `field update` expecting to convert an existing column (e.g. `string` → `select`). That is not supported. Create a new field with the desired type instead.

### Delete

```bash
frontline table field delete <table> <field-id>
```

## Options (Select Field Values)

Options are the selectable values for `singleSelect` and `multiSelect` fields.
You need the **field ID** first (use `field list`).

> Options are **always a separate step** from field creation — they can't be
> passed inline in the field-create body (that returns `400`). Create the
> `select` field, grab its id, then run one `option create` per value.

### Available Colors

Use color **names** (case-insensitive) or hex codes:

`Terracotta`, `Amber`, `Lime`, `Emerald`, `Lavender`, `Sky`, `Magenta`,
`Bright Red`, `Teal`, `Gray`, `Brown`, `Orange`, `Yellow`, `Green`,
`Blue`, `Purple`, `Pink`, `Red`

> Snapshot — run `frontline guidance icons` (field `optionColors`) for the authoritative list. See the `guidance` skill.

### List

```bash
frontline table option list <table> <field-id>
frontline object option list <object> <field-id>
```

### Create

```bash
frontline object option create <object> <field-id> --data '{
  "name": "Hot",
  "color": "Magenta"
}'
```

### Update / Delete

```bash
frontline object option update <object> <option-id> --data '{"name": "Warm", "color": "Amber"}'
frontline object option delete <object> <option-id>
```

> **Note**: `option-id` is the option's own ID (not the field ID).

## Rows (Records)

### Create

> ⚠️ **Creating a Person with an email auto-links a Company.**
>
> If you're calling `record create` on the built-in `people` object with an `Email` field and a **non-generic domain** (e.g. `john@acme.com`, not `john@gmail.com`), the platform automatically creates and/or links the matching `companies` record by domain. After `record create people` succeeds, the Company is already linked.
>
> - **Do NOT** also create the Company manually.
> - **Do NOT** call `relation link people <id> Companies <company-id>` to assign it.
>
> See `crm-objects` skill → People → top-of-section warning for the full rules and the edge cases (generic domains, overriding the auto-linked Company, etc.).

```bash
# Body is a flat key-value map: { "Field Name": value }
frontline table row create <table> --data '{
  "Name": "Acme Corp",
  "Amount": 50000,
  "Status": [1]
}'

# For People: the Company link happens automatically from the email domain.
# Do not create or link a Company manually after this.
frontline object record create people --data '{
  "First Name": "John",
  "Last Name": "Doe",
  "Email": "john@acme.com"
}'
```

> Select fields expect an array of option IDs: `[1, 3]`

**Assigning a record type at creation time:** pass `_type` with the numeric record type ID. Records default to the object's default record type if omitted. Get record type IDs from `frontline object record-type list <object>`.

```bash
frontline object record create people --data '{
  "First Name": "John",
  "Last Name": "Doe",
  "Email": "john@example.com",
  "_type": 8
}'
```

### Bulk Create

You can create multiple rows or records at once by passing a JSON array to `--data`.

```bash
# Create multiple table rows
frontline table row bulk-create <table> --data '[
  { "Name": "Acme Corp", "Amount": 50000 },
  { "Name": "Globex Inc", "Amount": 120000 }
]'

# Create multiple object records
frontline object record bulk-create <object> --data '[
  { "First Name": "John", "Last Name": "Doe" },
  { "First Name": "Jane", "Last Name": "Smith" }
]'
```

### Update

```bash
# Only send the fields you want to change
frontline table row update <table> <row-id> --data '{"Amount": 75000}'
frontline object record update <object> <row-id> --data '{"Status": [2]}'
```

### Delete

```bash
frontline table row delete <table> <row-id>
frontline object record delete <object> <row-id>
```

### Get by ID

```bash
frontline table row get <table> <row-id>
frontline object record get <object> <row-id>
```

## Record Types (objects only)

Record types group records into categories (e.g., "Lead", "Customer" in a People object).

Create, update, and delete require an **ADMIN** or **OWNER** key (`403` otherwise). Passing a table name returns `404`: tables keep the single implicit record type they are created with.

### List

```bash
frontline object record-type list <object>
```

### Create

```bash
frontline object record-type create <object> --data '{
  "name": "lead",
  "displayName": "Lead",
  "columnIds": [1, 2, 3]
}'
```

> Passing `columnIds` auto-creates default Table + Record views with those columns.

### Update / Delete

```bash
frontline object record-type update <object> <record-type-id> --data '{"displayName": "Qualified Lead"}'
frontline object record-type delete <object> <record-type-id>
```

## Views (objects only)

Views control how records are displayed in the UI (table grid, kanban board, single record).

### List

```bash
frontline object view list <object>
```

### Create

```bash
# View types: table, kanban, record
# First argument is the object; --record-type defaults to the object's default record type
frontline object view create <object> --record-type <record-type-id> --data '{
  "name": "Kanban Board",
  "type": "kanban",
  "metadata": { "groupingColumnId": 42 }
}'
```

### Update / Delete

```bash
frontline object view update <object> <view-id> --data '{"name": "Updated Board"}'
frontline object view delete <object> <view-id>
```

## Workflow: Full Object Setup

Create a new record type with a kanban view for a deals pipeline:

```bash
# 1. Check current fields
frontline object field list deals

# 2. Create a record type (returns record_type_id)
frontline object record-type create deals --data '{
  "name": "enterprise",
  "displayName": "Enterprise Deals",
  "columnIds": [1, 2, 5, 8]
}'

# 3. Add a kanban view to the record type
frontline object view create deals --record-type <record-type-id> --data '{
  "name": "Pipeline Board",
  "type": "kanban",
  "metadata": { "groupingColumnId": 5 }
}'
```

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
