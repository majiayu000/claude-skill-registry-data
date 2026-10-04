---
name: resource-creation
description: >
    How to create new data tables and custom objects using the Frontline CLI.
    Use this when you need to bootstrap a new entity from scratch.
allowed-tools: Bash(frontline:*)
---

# Resource Creation Guide

This skill covers the creation of top-level entities: **Tables** and **Objects**.

> **Working with People, Companies, Deals, or Tickets?**
> These four objects are pre-provisioned and have a rich set of built-in behaviors
> (auto-creation, enrichment, deduplication, AI profiles). Read the **`crm-objects`** skill
> before extending or creating records on them to avoid duplicating what the platform
> already handles automatically.

## Tables vs Objects: Which to Create?

| Entity Type | Use Case                                                                   | Command            |
| ----------- | -------------------------------------------------------------------------- | ------------------ |
| **Table**   | Simple data structures, spreadsheet-like, no record types.                 | `frontline table`  |
| **Object**  | Business entities with record types (e.g. Leads, Tickets), advanced views. | `frontline object` |

## Creating a Table

To create a new data table, use `frontline table create`. You MUST provide at least one column in the `--data` payload.
Tables (`DATA_TABLE` type) use **one literal Unicode emoji** for their icon — not icon key strings.
Use any standard Unicode emoji (e.g. `📁`, `🚚`, `🌟`, `💬`). Do **not** use icon key strings like `"truck"`, `"package"`, or `"briefcase"` — those only work for objects and record types.

```bash
frontline table create <name> --data '{
  "displayName": "Display Name",
  "emoji": "📁",
  "icon_color": "blue",
  "columns": [
    { "name": "Name", "type": "string", "metadata": { "format": "text" } }
  ]
}'
```

### Example: Creating a "Shipments" Table

```bash
frontline table create shipments --data '{
  "displayName": "Shipments",
  "emoji": "🚚",
  "icon_color": "orange",
  "columns": [
    { "name": "Cargo", "type": "string", "metadata": { "format": "text" } },
    { "name": "Weight", "type": "number", "metadata": { "format": "decimal", "decimals": 2 } }
  ]
}'
```

## Creating a Custom Object

To create a new custom object, use `frontline object create`. This creates a more robust entity that supports multiple record types.
Objects use **icon keys** (not emoji characters) for their icon — the value must be one of the validated keys from the allowlist below (see **Available Icons**).
Do **not** use literal emoji like `"📦"` for objects — use a key string like `"ticket"` or `"briefcase"` instead.

**Important:** `object create` does NOT accept a positional name argument. The `name` slug must go inside `--data`. (Tables use a positional argument; objects do not.)

```bash
frontline object create --data '{
  "name": "my_object",
  "displayName": "Display Name",
  "singularNoun": "Item",
  "emoji": "ticket",
  "icon_color": "amber",
  "columns": [
    { "name": "Subject", "type": "string", "metadata": { "format": "text" } }
  ]
}'
```

- `name`: URL-safe slug (lowercase, alphanumeric, underscores). Used in CLI commands.
- `displayName`: Human-readable label shown in the UI.
- `singularNoun`: Singular form of the display name (e.g. `"Ticket"` for `"Support Tickets"`). Shown in record detail views and empty states.

### Example: Creating a "Support Tickets" Object

```bash
frontline object create --data '{
  "name": "tickets",
  "displayName": "Support Tickets",
  "singularNoun": "Ticket",
  "emoji": "life-buoy",
  "icon_color": "amber",
  "columns": [
    { "name": "Title", "type": "string", "metadata": { "format": "text" } },
    { "name": "Priority", "type": "select", "metadata": { "mode": "singleSelect" } }
  ]
}'
```

## Naming Rules

1.  **Name (slug)**: Lowercase, alphanumeric, and underscores only. E.g., `sales_leads`, `shipments_v2`.
2.  **Display Name**: Readable text with spaces. E.g., `Sales Leads`, `Shipments V2`.

## Emoji Field: Tables vs Objects

| Resource type            | `emoji` value             | Validation                              | Example                   |
| ------------------------ | ------------------------- | --------------------------------------- | ------------------------- |
| **Table** (`DATA_TABLE`) | One literal Unicode emoji | Single emoji grapheme (not an icon key) | `"📁"`, `"🚀"`, `"🌟"`    |
| **Object** (`OBJECT`)    | An icon key string        | Must be in the allowlist below          | `"briefcase"`, `"ticket"` |
| **Record Type**          | An icon key string        | Same allowlist as objects               | `"repeat"`, `"star"`      |

> **Rule of thumb:** if you're calling `frontline table create`, paste **one** Unicode emoji. If you're calling `frontline object create` or `frontline object record-type create`, pick a key from the list below. **Never** use icon keys on tables or literal emojis on objects.

## Available Icons (Objects and Record Types only)

Objects and record types use the `emoji` field with a **validated icon key**. Tables use any literal emoji instead.

Use the `emoji` field to set an object's icon. The value must be one of the valid icon keys:

`home`, `user`, `users`, `contact-book`, `building`, `building-2`, `briefcase`, `agreement`,
`handshake`, `legal-doc`, `legal-hammer`, `shopping`, `cart`, `store`, `invoice`, `credit-card`,
`coins`, `wallet`, `money-bag`, `ticket`, `life-buoy`, `support`, `headset`, `task`, `clipboard`,
`file`, `folder`, `book`, `book-open`, `bookmark`, `mail`, `call`, `chat`, `calendar`, `clock`,
`timer`, `hourglass`, `location`, `maps`, `globe`, `earth`, `link`, `tag`, `flag`, `chart`,
`pie-chart`, `target`, `megaphone`, `rocket`, `idea`, `magnet`, `star`, `award`, `medal`,
`badge`, `certificate`, `crown`, `diamond`, `gift`, `percent`, `heart`, `hospital`, `stethoscope`,
`shield`, `lock`, `key`, `fingerprint`, `umbrella`, `settings`, `edit`, `wrench`, `code`, `puzzle`,
`database`, `layers`, `hierarchy`, `pipeline`, `package`, `truck`, `car`, `bicycle`, `bus`,
`property`, `school`, `graduate`, `plant`, `leaf`, `fire`, `sun`, `moon`, `image`, `video`,
`music`, `mic`, `camera`, `paint`, `compass`, `anchor`, `zap`, `flash`, `notification`, `user-add`,
`repeat`, `cloud`, `wifi`, `printer`, `airplane`, `restaurant`, `coffee`, `phone`, `analytics`,
`pulse`, `contracts`, `delivery`, `receipt`, `qr-code`, `barcode`, `calculator`, `download`, `upload`,
`filter`, `search`, `view`, `share`, `archive`, `dumbbell`, `brain`, `atom`, `chip`, `robot`,
`satellite`, `factory`, `warehouse`, `mountain`, `tree`, `flower`, `drone`, `gamepad`, `safe`,
`label`, `stamp`, `thumbs-up`, `smile`, `recycle`, `laptop`, `tv`, `headphones`, `speaker`,
`alarm`, `glasses`, `flashlight`, `feather`, `id-card`, `loyalty`, `coupon`, `presentation`,
`ruler`, `highlighter`, `passport`, `bitcoin`, `fuel`, `luggage`, `bone`, `whistle`, `sofa`

> The list above is a convenience snapshot. For the **authoritative, always-current** list, run
> `frontline guidance icons` (field `iconKeys`) — it comes straight from the backend. See the `guidance` skill.

## Available Icon Colors

Use the `icon_color` field to set the icon color. You can use a **color name** (case-insensitive) or a **hex code**:

| Name    | Hex       |
| ------- | --------- |
| red     | `#f87171` |
| orange  | `#fb923c` |
| amber   | `#fbbf24` |
| yellow  | `#facc15` |
| lime    | `#a3e635` |
| green   | `#4ade80` |
| emerald | `#34d399` |
| teal    | `#2dd4bf` |
| cyan    | `#22d3ee` |
| sky     | `#38bdf8` |
| blue    | `#60a5fa` |
| indigo  | `#818cf8` |
| violet  | `#a78bfa` |
| purple  | `#c084fc` |
| pink    | `#f472b6` |
| rose    | `#fb7185` |

> Snapshot — run `frontline guidance icons` (field `iconColors`) for the authoritative name→hex list.

## Record Type Icons and Nouns

Record types on objects also support `emoji`, `icon_color`, and `singularNoun`. If omitted, they inherit from the parent object.

```bash
frontline object record-type create deals --data '{
  "name": "renewal",
  "displayName": "Renewals",
  "singularNoun": "Renewal",
  "emoji": "repeat",
  "icon_color": "teal"
}'
```

## Adding More Fields

Once the entity is created, you can add more fields using the `field create` subcommand:

```bash
frontline table field create <table-name> --data '{...}'
frontline object field create <object-name> --data '{...}'
```

For a full reference on field types and metadata, see the `schema-design` skill.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
