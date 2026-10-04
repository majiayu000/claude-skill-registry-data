---
name: schema-design
description: >
    Complete guide for designing table and object schemas with the Frontline CLI.
    Covers choosing the right field type, metadata configuration, when to use
    select vs relation, naming conventions, and common schema patterns.
    Use as a reference before creating or extending any table or object.
allowed-tools: Bash(frontline:*)
---

# Schema Design Guide

This skill covers how to think about and build effective schemas using the
Frontline CLI. Read this before creating or modifying fields on any table or object.

> **Working with People, Companies, Deals, or Tickets?**
> These objects ship with pre-defined fields and run background automations
> (enrichment, deduplication, AI profiles, auto-linking). Many fields you might
> think to add already exist or are computed automatically. Always check the
> **`crm-objects`** skill first to avoid duplicates.

## Resource Selection: Table vs Object

| Type       | Goal                                    | Command         |
| ---------- | --------------------------------------- | --------------- |
| **Table**  | Simple spreadsheets, flat data          | `table create`  |
| **Object** | Business entities, record types, pipeln | `object create` |

### Who can change a schema

Schema changes are gated differently per resource type. **Permission denials** return `403`; missing USER API key is typically `401`; invalid payloads or business rules return `400`:

| Resource   | Required access to add/edit/delete fields, options, record types                               |
| ---------- | ---------------------------------------------------------------------------------------------- |
| **Object** | **ADMIN** or **OWNER** role. Not delegable — an object's schema is the shared CRM model.       |
| **Table**  | Edit access: admins/owners, the table's creator, or `FULL_ACCESS` via `frontline sharing set`. |

Reading a schema (`object get`, `object field list`, and their table equivalents) only needs
view access. If a field command fails with `403`, check the caller's role or the table's sharing
level before assuming the payload is wrong.

```bash
# Example: Create a new custom object (with icon and color)
# NOTE: object create does NOT take a positional name argument — put "name" inside --data
frontline object create --data '{
  "name": "my_object",
  "displayName": "My Object",
  "singularNoun": "Item",
  "emoji": "briefcase",
  "icon_color": "blue",
  "columns": [
    { "name": "Title", "type": "string", "metadata": { "format": "text" } }
  ]
}'
```

> **Note on the `emoji` field:**
>
> - **Tables** (`DATA_TABLE` — `frontline table create`): use **one Unicode emoji** character (e.g. `"📁"`, `"🚀"`). Not icon keys like `"truck"` or `"package"`.
> - **Objects** (`frontline object create`) and **Record Types**: must use an **icon key string** from a fixed allowlist (e.g. `"briefcase"`, `"rocket"`, `"chart"`). Literal emoji are rejected.
> - **Do not mix formats:** no icon keys on tables, no emojis on objects/record types.
> - Both support `icon_color` with a color name or hex.
>   See the `resource-creation` skill for the full icon key list and color reference.

## Field Type Decision Tree

```
What kind of data?
│
├─ Free text → string
│   ├─ Email address    → metadata: { "format": "email" }
│   ├─ URL / website    → metadata: { "format": "url" }
│   ├─ Phone number     → metadata: { "format": "phone" }
│   └─ General text     → metadata: { "format": "text" }
│
├─ Number → number
│   ├─ Money            → metadata: { "format": "currency", "currency": "USD", "decimals": 2 }
│   ├─ Percentage       → metadata: { "format": "percent" }
│   ├─ Integer count    → metadata: { "format": "integer" }
│   └─ Decimal          → metadata: { "format": "decimal", "decimals": 2 }
│
├─ Yes/No → boolean
│   └─ metadata: {}
│
├─ Date or time → date / dateOnly
│   ├─ With time + timezone → date, metadata: { "timezone": "America/New_York" }
│   └─ Date only (no time)  → dateOnly, metadata: {}
│
├─ Pick from a fixed list → select
│   ├─ Pick one    → metadata: { "mode": "singleSelect" }  (pass explicitly — omitting mode defaults to multiSelect)
│   └─ Pick many   → metadata: { "mode": "multiSelect" }
│
├─ Link to another entity → relation / prismaRelation
│   ├─ relation (object-to-object): metadata: { "relatedTableId": <id>, "displayColumn": <field-id>, "mode": "single"|"multi" }
│   └─ prismaRelation (object-to-platform-user): metadata: { "prismaModel": "User", "displayField": "fullName", "mode": "single"|"multi" }
│
└─ File attachment → file
    └─ metadata: { "showPreview": true }
```

> ⚠️ **`select` options are a separate step.** The field-create body only sets
> `mode` — it never creates the option values. Passing options inline
> (`metadata.options`, `metadata.tags`, or a top-level `options`/`tags` array)
> is rejected with `400`. Create the `select` field first, then add each value
> with `frontline <table|object> option create <name> <field-id> --data
'{"name":"...","color":"..."}'` (see the `crud-operations` skill → Options).
> On **update**, replace options via the top-level `tags` array, not `metadata`.

## Column Type Cannot Be Changed After Create

Once a field exists, its `type` is fixed. `field update` supports renaming, constraints, metadata tweaks, and (for `select`) replacing options — but **not** changing `string` to `select`, `number` to `date`, etc.

To migrate to a different field type:

1. Create a new field with the target type (and `metadata.mode` for `select`).
2. Add options if it is a `select` field.
3. Copy or transform values on existing records (`record update` / bulk operations).
4. Update views or record types that referenced the old column.
5. Delete the old field when no longer needed.

## Field Constraints

You can set constraints on fields during creation or update:

| Constraint | Description                                   | Example            |
| ---------- | --------------------------------------------- | ------------------ |
| `required` | Field must have a value in every record       | `"required": true` |
| `unique`   | Field value must be unique across all records | `"unique": true`   |

```bash
# Make a field required and unique
frontline object field update <object> <field-id> --data '{"required": true, "unique": true}'

# Remove the required constraint
frontline object field update <object> <field-id> --data '{"required": false}'
```

## Attaching Fields to Specific Record Types (Objects Only)

By default, when you create a new field/column via the CLI or Public API, the field is automatically added to **all** record types of the object.

If you want a field to only belong to a specific record type (and not be visible in others), pass `record_type_id` (or `recordTypeId`) in the `--data` JSON payload to scope the new field to that single record type.

```bash
# Example: Create a field that only belongs to record type ID 42
frontline object field create my_object --data '{
  "name": "Special Code",
  "type": "string",
  "record_type_id": 42
}'
```

### Ask before creating a field on a multi-record-type object

Adding a field to every record type is rarely what the user wants, so **do not silently fall back to the "all record types" default**. Before creating a field on an object:

1. Check how many record types the object has: `frontline object record-type list <object>`.
2. **If the object has more than one record type and the user did not say which one(s) the field is for, stop and ask them.** Show the list of record types (name + id) and let them choose:
    - **"All record types"** → omit `record_type_id` (this is the legacy default behavior — leave it as-is).
    - **A single specific record type** → pass that record type's id as `record_type_id`.
3. If the object has only one record type, just create the field — there is nothing to disambiguate.

> [!NOTE]
> The field-create endpoint scopes to **one** record type at a time (`record_type_id` is singular). To put a brand-new field on **several but not all** record types, create it on one of them (or on none and then detach), and add it to each additional record type by updating that record type's `columnIds` — see the `record-type-management` skill. Multi-record-type selection in a single create call is not supported yet.

> [!IMPORTANT]
>
> - `record_type_id` **only** applies to **Objects** (`frontline object field create`).
> - **Tables** (`frontline table field create`) do not support record types, and trying to specify a record type id will return a `BadRequestError`.

## Select vs Relation: When to Use Which

| Use **select** when...                       | Use **relation** when...                     |
| -------------------------------------------- | -------------------------------------------- |
| Options are simple labels (Status, Priority) | Values are full records in another table     |
| List is short and rarely changes             | List grows organically (contacts, companies) |
| No extra data attached to each option        | Each value has its own fields and metadata   |
| You want colored badges in the UI            | You need to navigate to the linked record    |
| Example: Stage, Priority, Category           | Example: Company, Assigned User, Contact     |

## Complete Field Type Reference

### string

```bash
# Plain text — single-line input (default)
--data '{ "name": "Notes", "type": "string", "metadata": { "format": "text" } }'

# Long text — multi-line text area (use for Descriptions, summaries, notes)
--data '{ "name": "Description", "type": "string", "metadata": { "format": "text", "extendedField": true } }'

# Email — enables validation and mailto links
--data '{ "name": "Email", "type": "string", "metadata": { "format": "email" } }'

# URL — renders as clickable link
--data '{ "name": "Website", "type": "string", "metadata": { "format": "url" } }'

# Phone — formats and enables click-to-call
--data '{ "name": "Phone", "type": "string", "metadata": { "format": "phone_number" } }'
```

> **Normal text vs long text:** both use `"format": "text"`. Add `"extendedField": true` for a multi-line text area (e.g. a Description). Omit it for a single-line input.

### number

```bash
# Currency — shows $ symbol, 2 decimal places
--data '{ "name": "Revenue", "type": "number", "metadata": { "format": "currency", "currency": "USD", "decimals": 2 } }'

# Percentage — shows % symbol
--data '{ "name": "Win Rate", "type": "number", "metadata": { "format": "percent" } }'

# Integer — no decimals
--data '{ "name": "Headcount", "type": "number", "metadata": { "format": "integer" } }'

# Decimal — custom precision
--data '{ "name": "Weight", "type": "number", "metadata": { "format": "decimal", "decimals": 3 } }'
```

### relation (object → object)

Links a record to records in another object. Requires the target object's table ID and the field ID to display as the link label. Get both from `frontline object get <target>`.

```bash
# Single link (many-to-one)
--data '{ "name": "Company", "type": "relation", "metadata": { "relatedTableId": 1, "displayColumn": 1, "mode": "single" } }'

# Multi link (one-to-many)
--data '{ "name": "Contacts", "type": "relation", "metadata": { "relatedTableId": 2, "displayColumn": 24, "mode": "multi" } }'
```

- `relatedTableId`: numeric `id` of the target object (from `frontline object get <target>` → `data.id`)
- `displayColumn`: numeric field `id` to show as the label (e.g. the Name field id)
- `mode`: `"single"` or `"multi"`
- `includeActivity` (optional, default `false`): **custom objects only.** When `true`, the record's timeline also merges in the activity of the linked records. See the `relations` skill.

### prismaRelation (object → platform user)

Links a record to a platform entity — most commonly a Frontline account **User**. Use this for fields like "Assignee" or "Owner". The built-in `Users` field on People, Deals, and Tickets is exactly this type.

```bash
--data '{ "name": "Owner", "type": "prismaRelation", "metadata": { "prismaModel": "User", "displayField": "fullName", "mode": "single" } }'
```

- `prismaModel` (required): `"User"` (account users) or `"Conversation"`
- `displayField` (required): the property to show as the label — `"fullName"` for `User`
- `mode`: `"single"` or `"multi"`

Both `prismaModel` and `displayField` are **required** — omitting either returns a 400.

**Assigning values on a record:** pass an array of numeric user IDs as the field value.

```bash
frontline object record update deals <record-id> --data '{ "Owner": [42] }'
```

### boolean

```bash
--data '{ "name": "Is Active", "type": "boolean", "metadata": {} }'
```

### date / dateOnly

```bash
# Datetime with timezone and display format (not "datetime" — that is a legacy value)
--data '{ "name": "Meeting Time", "type": "date", "metadata": { "timezone": "America/New_York", "format": "MM/dd/yyyy", "timeFormat": "12h" } }'

# With display format + 24-hour time
--data '{ "name": "Met At", "type": "date", "metadata": { "timezone": "UTC", "format": "MM/dd/yyyy", "timeFormat": "24" } }'

# Date only (no time component)
--data '{ "name": "Start Date", "type": "dateOnly", "metadata": {} }'
```

Optional display metadata: `format` is a date-fns pattern — `MMMM d, yyyy`, `MMM d, yyyy`,
`d MMM yyyy`, `M/d/yyyy`, `MM/dd/yyyy`, `d/M/yyyy`, `dd/MM/yyyy`, `yyyy-MM-dd` (or `timeDelta`
for relative display like "3 days ago"). `timeFormat` is `"12"` or `"24"`. If you pass `metadata`
on a `date` field, `timezone` is required. Run `frontline guidance fields` for the full reference.

> ⚠️ **Timezone Validation:**
> The `timezone` field in `date` metadata is strictly validated. It must be one of the following valid timezones:
> `UTC`, `America/New_York`, `America/Chicago`, `America/Denver`, `America/Los_Angeles`, `America/Toronto`, `America/Vancouver`, `America/Mexico_City`, `America/Guatemala`, `America/Bogota`, `America/Lima`, `America/Sao_Paulo`, `America/Argentina/Buenos_Aires`, `America/Santiago`, `America/Caracas`, `America/Montevideo`, `America/La_Paz`, `America/Asuncion`, `America/Managua`, `America/Costa_Rica`, `America/Panama`, `America/Jamaica`, `America/Havana`, `America/Puerto_Rico`, `America/Barbados`, `Pacific/Honolulu`, `Pacific/Auckland`, `Pacific/Fiji`, `Pacific/Guam`, `Pacific/Tahiti`, `Pacific/Samoa`, `Pacific/Tongatapu`, `Europe/London`, `Europe/Paris`, `Europe/Berlin`, `Europe/Rome`, `Europe/Madrid`, `Europe/Amsterdam`, `Europe/Brussels`, `Europe/Vienna`, `Europe/Zurich`, `Europe/Moscow`, `Europe/Istanbul`, `Europe/Athens`, `Europe/Stockholm`, `Europe/Oslo`, `Europe/Helsinki`, `Europe/Copenhagen`, `Europe/Warsaw`, `Europe/Prague`, `Europe/Budapest`, `Europe/Bucharest`, `Europe/Sofia`, `Europe/Kiev`, `Europe/Minsk`, `Europe/Vilnius`, `Europe/Riga`, `Europe/Tallinn`, `Europe/Dublin`, `Europe/Lisbon`, `Africa/Cairo`, `Africa/Johannesburg`, `Africa/Lagos`, `Africa/Casablanca`, `Africa/Nairobi`, `Africa/Addis_Ababa`, `Africa/Algiers`, `Africa/Tunis`, `Africa/Khartoum`, `Africa/Accra`, `Africa/Dakar`, `Africa/Bamako`, `Asia/Dubai`, `Asia/Jerusalem`, `Asia/Kolkata`, `Asia/Singapore`, `Asia/Hong_Kong`, `Asia/Shanghai`, `Asia/Seoul`, `Asia/Tokyo`, `Asia/Bangkok`, `Asia/Jakarta`, `Asia/Manila`, `Asia/Kuala_Lumpur`, `Asia/Ho_Chi_Minh`, `Asia/Phnom_Penh`, `Asia/Vientiane`, `Asia/Yangon`, `Asia/Dhaka`, `Asia/Kathmandu`, `Asia/Colombo`, `Asia/Karachi`, `Asia/Kabul`, `Asia/Tashkent`, `Asia/Almaty`, `Asia/Yekaterinburg`, `Asia/Novosibirsk`, `Asia/Krasnoyarsk`, `Asia/Irkutsk`, `Asia/Yakutsk`, `Asia/Vladivostok`, `Asia/Magadan`, `Asia/Kamchatka`, `Asia/Riyadh`, `Asia/Qatar`, `Asia/Kuwait`, `Asia/Bahrain`, `Asia/Muscat`, `Asia/Tehran`, `Asia/Baghdad`, `Asia/Damascus`, `Asia/Beirut`, `Asia/Amman`, `Asia/Nicosia`, `Australia/Sydney`, `Australia/Melbourne`, `Australia/Brisbane`, `Australia/Perth`, `Australia/Adelaide`, `Australia/Darwin`, `Australia/Hobart`.
> Invalid values will result in a validation error (`400 Bad Request`).

### select (single / multi)

```bash
# Single-select (pick one)
--data '{ "name": "Priority", "type": "select", "metadata": { "mode": "singleSelect" } }'

# Multi-select (pick many)
--data '{ "name": "Tags", "type": "select", "metadata": { "mode": "multiSelect" } }'
```

After creating, add options:

```bash
frontline object option create <obj> <field-id> --data '{ "name": "High", "color": "Magenta" }'
frontline object option create <obj> <field-id> --data '{ "name": "Medium", "color": "Amber" }'
frontline object option create <obj> <field-id> --data '{ "name": "Low", "color": "Gray" }'
```

### Available Option Colors

`Terracotta`, `Amber`, `Lime`, `Emerald`, `Lavender`, `Sky`, `Magenta`,
`Bright Red`, `Teal`, `Gray`, `Brown`, `Orange`, `Yellow`, `Green`,
`Blue`, `Purple`, `Pink`, `Red`

> Snapshot (a different palette from icon colors) — run `frontline guidance icons` (field
> `optionColors`) for the authoritative list. See the `guidance` skill.

## Common Schema Patterns

### 1. Status Pipeline

A single-select field with ordered stages:

```bash
frontline object field create deals --data '{
  "name": "Stage",
  "type": "select",
  "metadata": { "mode": "singleSelect" }
}'
# Then add stages in order:
frontline object option create deals <field-id> --data '{"name": "Lead", "color": "Gray"}'
frontline object option create deals <field-id> --data '{"name": "Qualified", "color": "Sky"}'
frontline object option create deals <field-id> --data '{"name": "Proposal", "color": "Amber"}'
frontline object option create deals <field-id> --data '{"name": "Won", "color": "Emerald"}'
frontline object option create deals <field-id> --data '{"name": "Lost", "color": "Red"}'
```

### 2. Contact Info Set

Standard contact fields for a People-like object:

```bash
frontline object field create <obj> --data '{"name":"Email","type":"string","metadata":{"format":"email"}}'
frontline object field create <obj> --data '{"name":"Phone","type":"string","metadata":{"format":"phone_number"}}'
frontline object field create <obj> --data '{"name":"Website","type":"string","metadata":{"format":"url"}}'
frontline object field create <obj> --data '{"name":"Address","type":"string","metadata":{"format":"text"}}'
```

### 3. Financial Tracking

```bash
frontline object field create <obj> --data '{"name":"Amount","type":"number","metadata":{"format":"currency","currency":"USD","decimals":2}}'
frontline object field create <obj> --data '{"name":"Probability","type":"number","metadata":{"format":"percent"}}'
frontline object field create <obj> --data '{"name":"Close Date","type":"dateOnly","metadata":{}}'
```

### 4. Categorization with Multi-Select

```bash
frontline object field create <obj> --data '{
  "name": "Industries",
  "type": "select",
  "metadata": { "mode": "multiSelect" }
}'
frontline object option create <obj> <field-id> --data '{"name":"SaaS","color":"Sky"}'
frontline object option create <obj> <field-id> --data '{"name":"E-commerce","color":"Purple"}'
frontline object option create <obj> <field-id> --data '{"name":"Healthcare","color":"Emerald"}'
frontline object option create <obj> <field-id> --data '{"name":"Fintech","color":"Amber"}'
```

## Naming Conventions

| Do ✅                       | Don't ❌                  |
| --------------------------- | ------------------------- |
| `First Name`                | `firstName`, `first_name` |
| `Email`                     | `email_address`           |
| `Primary Location`          | `primary-location`        |
| `Deal Value`                | `dealValue`               |
| Title Case, space-separated | camelCase or snake_case   |

Field names are **display names** shown in the UI. Use natural, readable names.

> [!IMPORTANT]
> **Forbidden Characters:** Field names **cannot** contain brackets `[` or `]`. These characters are reserved for referencing paths in formulas. Using them in field names will result in validation errors (`400 Bad Request`).

## Workflow: Extending an Existing Object

```bash
# 1. Check what fields already exist
frontline object field list companies

# 2. Check schema for relations
frontline object schema companies

# 3. Add new fields — only add what's missing
frontline object field create companies --data '{
  "name": "Annual Revenue",
  "type": "number",
  "metadata": { "format": "currency", "currency": "USD", "decimals": 0 }
}'

# 4. Add a categorization field
frontline object field create companies --data '{
  "name": "Industry",
  "type": "select",
  "metadata": { "mode": "singleSelect" }
}'
# Add options
frontline object option create companies <field-id> --data '{"name":"Technology","color":"Sky"}'
frontline object option create companies <field-id> --data '{"name":"Finance","color":"Amber"}'

# 5. Verify the final schema
frontline object field list companies
```

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
