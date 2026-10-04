---
name: aggregations
description: >
    How to create, update, delete, and compute aggregations on views
    using the Frontline CLI. Aggregations are summary statistics 
    (SUM, AVERAGE, COUNT_FILLED, etc.) attached to view columns.
allowed-tools: Bash(frontline:*)
---

# Aggregations

Aggregations are summary statistics attached to a view's columns. They compute
values like SUM, AVERAGE, COUNT_FILLED, MIN, MAX across all rows matching the
current view's filters.

## Available Operations

| Operation        | Applies To     | Description               |
| ---------------- | -------------- | ------------------------- |
| `COUNT_EMPTY`    | Any column     | Count of empty/null cells |
| `COUNT_FILLED`   | Any column     | Count of non-empty cells  |
| `PERCENT_EMPTY`  | Any column     | % of empty cells          |
| `PERCENT_FILLED` | Any column     | % of non-empty cells      |
| `SUM`            | Number columns | Sum of all values         |
| `AVERAGE`        | Number columns | Average of all values     |
| `MIN`            | Number/Date    | Minimum value             |
| `MAX`            | Number/Date    | Maximum value             |

## Prerequisites

You need a **view ID** and a **column ID**. Get both from:

```bash
# Get object/table detail (includes views with their IDs)
frontline object get <object>

# Get fields (includes column IDs)
frontline object field list <object>
```

## List Aggregations

```bash
frontline object aggregation list <object> <view-id>
frontline table aggregation list <table> <view-id>
```

## Create an Aggregation

```bash
# SUM on a number column
frontline object aggregation create <object> <view-id> \
  --data '{"columnId": 5, "operation": "SUM"}'

# COUNT_FILLED on any column
frontline object aggregation create <object> <view-id> \
  --data '{"columnId": 3, "operation": "COUNT_FILLED"}'

# COUNT_FILLED scoped to a specific tag (option) ID — useful in kanban views
frontline object aggregation create <object> <view-id> \
  --data '{"columnId": 8, "operation": "COUNT_FILLED", "tagId": 12}'
```

## Update an Aggregation

Change the operation of an existing aggregation:

```bash
frontline object aggregation update <object> <view-id> <agg-id> \
  --data '{"operation": "AVERAGE"}'
```

## Delete an Aggregation

```bash
frontline object aggregation delete <object> <view-id> <agg-id>
```

## Compute Aggregation Values

Compute the actual numeric results for all aggregations on a view.
Optionally filter with a query or search:

```bash
# Compute all aggregations
frontline object aggregation compute <object> <view-id>

# Compute with a filter
frontline object aggregation compute <object> <view-id> \
  --query '{"path":"[Status]","operator":"containsAny","value":[3]}'

# Compute for a specific column only
frontline object aggregation compute <object> <view-id> --column-id 5
```

---

## Typical Workflow

```bash
# 1. Identify the view and columns
frontline object get deals
# → view ID = 1
frontline object field list deals
# → Amount column ID = 5, Status column ID = 8

# 2. Add aggregations
frontline object aggregation create deals 1 \
  --data '{"columnId": 5, "operation": "SUM"}'
frontline object aggregation create deals 1 \
  --data '{"columnId": 5, "operation": "AVERAGE"}'
frontline object aggregation create deals 1 \
  --data '{"columnId": 8, "operation": "COUNT_FILLED"}'

# 3. Compute results
frontline object aggregation compute deals 1
# → { aggregations: [{ columnId: 5, operation: "SUM", value: 1250000 }, ...] }

# 4. Compute only for "Won" deals
frontline object aggregation compute deals 1 \
  --query '{"path":"[Status]","operator":"containsAny","value":[3]}'
```

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
