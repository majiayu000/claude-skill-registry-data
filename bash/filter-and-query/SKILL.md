---
name: filter-and-query
description: >
    How to filter, search, and sort records using the Frontline CLI.
    Use when you need to find specific records in a table or object by
    building query conditions, combining them with AND/OR logic,
    searching by text, or sorting results.
allowed-tools: Bash(frontline:*)
---

# Filtering and Querying Records

The `frontline table row list` and `frontline object record list` commands accept
`--query`, `--search`, and `--sort` flags for filtering data.

## Quick Reference

```bash
# Simple text search across all fields
frontline object record list people --search "john"

# Filter by a single condition
# TIP: Use 'frontline object field list <name>' to find field names and tag IDs
frontline object record list deals --query '{
  "path": "[Amount]",
  "operator": "gte",
  "value": 10000
}'

# Multiple conditions (AND)
frontline object record list deals --query '{
  "operator": "and",
  "conditions": [
    { "path": "[Status]", "operator": "containsAny", "value": [1, 2] },
    { "path": "[Amount]", "operator": "gte", "value": 5000 }
  ]
}'

# Sort results
frontline object record list people --sort '[{"path": "[Last Name]", "type": "asc"}]'
```

## Path Format

Field paths use bracket notation: `[Field Name]`

For relation fields (querying through a linked record's field):
`[Relation Field].[Target Field]`

```jsonc
"path": "[Email]"              // Direct field
"path": "[Company].[Name]"     // Through a relation
```

## Operators by Field Type

### String Fields

| Operator     | Description     | Value        |
| ------------ | --------------- | ------------ |
| `equals`     | Exact match     | `"string"`   |
| `ne`         | Not equal       | `"string"`   |
| `contains`   | Substring match | `"string"`   |
| `startsWith` | Starts with     | `"string"`   |
| `endsWith`   | Ends with       | `"string"`   |
| `isNull`     | Field is empty  | _(no value)_ |
| `isNotNull`  | Field has value | _(no value)_ |

### Number Fields

| Operator               | Description           | Value        |
| ---------------------- | --------------------- | ------------ |
| `equals`               | Equal to              | `number`     |
| `ne`                   | Not equal             | `number`     |
| `lt`                   | Less than             | `number`     |
| `lte`                  | Less than or equal    | `number`     |
| `gt`                   | Greater than          | `number`     |
| `gte`                  | Greater than or equal | `number`     |
| `isNull` / `isNotNull` | Null checks           | _(no value)_ |

### Date / DateOnly Fields

| Operator               | Description  | Value                          |
| ---------------------- | ------------ | ------------------------------ |
| `equals`               | Exact date   | `"2026-04-17T00:00:00Z"`       |
| `before`               | Before date  | `"2026-04-17T00:00:00Z"`       |
| `after`                | After date   | `"2026-04-17T00:00:00Z"`       |
| `onOrBefore`           | On or before | `"2026-04-17T00:00:00Z"`       |
| `onOrAfter`            | On or after  | `"2026-04-17T00:00:00Z"`       |
| `between`              | Date range   | `["2026-01-01", "2026-12-31"]` |
| `isNull` / `isNotNull` | Null checks  | _(no value)_                   |

### Tags (Select/Multi-select) Fields

> **Important**: Tag values must be numeric **tag IDs**, not names.
> Use `frontline table field list <table>` or `frontline object field list <object>`
> to find tag IDs in the `options` array of each field.

| Operator               | Description           | Value              |
| ---------------------- | --------------------- | ------------------ |
| `containsAny`          | Has any of these tags | `[1, 2]` (tag IDs) |
| `containsAll`          | Has all of these tags | `[3, 5]` (tag IDs) |
| `notIn`                | Does not have any of  | `[4]` (tag IDs)    |
| `isNull` / `isNotNull` | Null checks           | _(no value)_       |

### Relation Fields

| Operator      | Description          | Value            |
| ------------- | -------------------- | ---------------- |
| `containsAny` | Linked to any of     | `["id1", "id2"]` |
| `notIn`       | Not linked to any of | `["id1"]`        |
| `isNull`      | No linked records    | _(no value)_     |
| `isNotNull`   | Has linked records   | _(no value)_     |

### Boolean Fields

| Operator               | Description    |
| ---------------------- | -------------- |
| `isTrue`               | Value is true  |
| `isFalse`              | Value is false |
| `isNull` / `isNotNull` | Null checks    |

### Formula Fields

Formula fields evaluate to one of the primitive types (number, string, boolean, date, tags) and support all of their respective operators. In addition, they support calculation status operators:

| Operator    | Description                             | Value        |
| ----------- | --------------------------------------- | ------------ |
| `isValid`   | Formula was evaluated successfully      | _(no value)_ |
| `isInvalid` | Formula evaluation failed with an error | _(no value)_ |

## Combining Conditions

Use `and` / `or` groups to combine conditions. Groups can be nested.

```jsonc
{
    "operator": "or",
    "conditions": [
        {
            "operator": "and",
            "conditions": [
                { "path": "[Status]", "operator": "containsAny", "value": [1] },
                { "path": "[Amount]", "operator": "gte", "value": 10000 },
            ],
        },
        {
            "path": "[Priority]",
            "operator": "containsAny",
            "value": [5],
        },
    ],
}
```

This matches: (Status is Open AND Amount >= 10000) OR Priority is Urgent.

## Sorting

Pass a JSON array of sort specs:

```bash
# Single sort
frontline table row list my_table --sort '[{"path": "[Name]", "type": "asc"}]'

# Multi-sort (primary + secondary)
frontline table row list my_table --sort '[
  {"path": "[Status]", "type": "desc"},
  {"path": "[createdAt]", "type": "asc"}
]'
```

## Pagination

```bash
frontline table row list my_table --page 1 --page-size 50
```

- `--page`: Page number (default: 1)
- `--page-size`: Items per page (default: 50, max: 200)

## Filter by Record Type (objects only)

`--record-type` accepts either the numeric record type ID or the special string `"all"`.
Use `frontline object record-type list <object>` to find the numeric ID.

```bash
# By numeric ID (preferred — name-based lookup is not supported)
frontline object record list people --record-type 8
frontline object record list deals --record-type 3

# "all" returns records of every record type
frontline object record list deals --record-type "all"
```

## Full Example

Find all open deals worth over $10k, owned by a specific company, sorted by amount:

```bash
frontline object record list deals \
  --query '{
    "operator": "and",
    "conditions": [
      { "path": "[Status]", "operator": "containsAny", "value": [1] },
      { "path": "[Amount]", "operator": "gte", "value": 10000 },
      { "path": "[Company]", "operator": "isNotNull" }
    ]
  }' \
  --sort '[{"path": "[Amount]", "type": "desc"}]' \
  --page-size 20
```

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
