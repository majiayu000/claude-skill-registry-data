---
name: formulas
description: >
    Formula columns enable dynamic, spreadsheet-like calculated values for both standard CRM objects and custom tables. They automatically recalculate when dependent fields, relations, or back-relations are modified.
allowed-tools: Bash(frontline:*)
---

# Formulas: Dynamic Calculated Fields

Formula columns enable dynamic, spreadsheet-like calculated values for both standard CRM **objects** and custom **tables**. They automatically recalculate when dependent fields, relations, or back-relations are modified.

---

## Formula Field Definition

A formula field is defined by setting the field's `type` to `"formula"` and providing a `metadata` object:

```json
{
  "name": "Total Cost",
  "type": "formula",
  "metadata": {
    "expression": { ... },
    "applyIf": { ... }
  }
}
```

### Metadata Fields

- **`expression`** (Object, Required): The Abstract Syntax Tree (AST) representing the calculation.
- **`applyIf`** (Object, Optional): A filter query (JSON matching filter). The formula will only evaluate if the record matches this query. If it does not, the field evaluates to a fallback/default value.
- **`numberConfig`** (Object, Optional): Cumulative formatting settings (e.g. format, decimals, currency) used if the inferred formula output is numeric.
- **`dateConfig`** (Object, Optional): Cumulative formatting settings (e.g. format, timezone) used if the inferred formula output is a date. The `timezone` field is strictly validated and must be a valid IANA timezone name from the supported list (e.g. `UTC`, `America/New_York`, `America/Chicago`, etc.).
- **`stringConfig`** (Object, Optional): Formatting when the inferred output is string. Supports `format`: `text`, `email`, `url`, or `phone_number`. Use `extendedField: true` with `format: "text"` for long (multi-line) display, same as standard string columns.
  _Note: The `outputType` of the formula column is automatically calculated by the backend based on the expression tree._

---

## Abstract Syntax Tree (AST) Nodes

Every formula is built recursively using six node types:

### 1. Constant Node (`constant`)

Represents a static literal value.

- **`value`**: string or number.

```json
{
    "type": "constant",
    "value": 0.15
}
```

### 2. Field Node (`field`)

References a field on the current record or on a related record.

- **`field`**: The bracketed path format:
    - Direct field: `"[Field Name]"`
    - Relational field (direct relation): `"[Relation Name].[Field Name]"`
- **`fallbackValue`** (Optional): Value used if the field is empty or null. Can be a string or number.
- **Percent Formatted Scaling**: If the referenced column is a standard `number` field with `format: "percent"`, its resolved value (or fallback value, if used) will automatically be divided by `100` during evaluation. This ensures that a stored integer like `10` (representing 10%) correctly behaves as `0.1` inside formula calculations (e.g. `[Price] * [Tax Rate]`).

```json
{
    "type": "field",
    "field": "[Quantity]",
    "fallbackValue": 0
}
```

### 3. Operator Node (`operator`)

Performs mathematical or string operations.

- **`operator`**: One of:
    - `"add"` (+): Sums all arguments (requires numeric inputs).
    - `"subtract"` (-): Subtracts arguments sequentially (requires numeric inputs).
    - `"multiply"` (\*): Multiplies all arguments (requires numeric inputs).
    - `"divide"` (/): Divides arguments sequentially (requires numeric inputs).
    - `"concat"`: String concatenation of all arguments (coerces non-string arguments to string).
- **`arguments`**: Array of formula nodes (minimum 1 argument).

```json
{
    "type": "operator",
    "operator": "multiply",
    "arguments": [
        { "type": "field", "field": "[Quantity]" },
        { "type": "field", "field": "[Unit Price]" }
    ]
}
```

### 4. Aggregate Node (`aggregate`)

Aggregates fields across related records.

- **`operation`**: One of `"count"`, `"sum"`, `"avg"`, `"min"`, `"max"`, `"sumProduct"`.
- **`field`** (Required): Target column name in the related table to aggregate. **Note:** In the Zod schema, `field` is strictly required even for `"count"`. For count operations, provide any valid field name (e.g. `"id"` or `"Hours"`).
- **`relation`** (Optional if `isBackRelation` is true, otherwise Required): Name of the relation column on the root table.
- **`isBackRelation`** (Optional): Set to `true` if aggregating via a back-relation.
- **`backRelationColumnId`** (Optional): The relation column ID on the target table pointing back to this table.
- **`arguments`** (Optional): Additional weight fields (required for `"sumProduct"` to multiply the field by).

```json
{
    "type": "aggregate",
    "relation": "line_items",
    "field": "subtotal",
    "operation": "sum"
}
```

### 5. Pad Left Node (`padLeft`)

Pads the left side of a string calculation to achieve a specific length.

- **`value`**: Formula node returning the base value.
- **`length`**: Number (final string length).
- **`char`**: Single character to pad with.

```json
{
    "type": "padLeft",
    "value": { "type": "field", "field": "[Sequential ID]" },
    "length": 6,
    "char": "0"
}
```

### 6. Time Operator Node (`timeOperator`)

Performs date/time addition, subtraction, or difference operations.

- **`operator`**: One of:
    - `"add"` (+): Adds a numeric amount to a date (requires one Date argument and one Number argument).
    - `"subtract"` (-): Subtracts a numeric amount from a date (requires the first argument to be Date and the second to be Number).
    - `"diff"`: Calculates the difference between two dates (requires both arguments to be Date; returns an integer count of the selected unit: `endDate - startDate`).
- **`arguments`**: Array containing exactly two formula nodes.
- **`unit`**: The time granularity unit, one of: `"second"`, `"minute"`, `"hour"`, `"day"`, `"month"`, `"year"`.

```json
{
    "type": "timeOperator",
    "operator": "add",
    "arguments": [
        { "type": "field", "field": "[Fecha Creacion]" },
        { "type": "constant", "value": 5 }
    ],
    "unit": "day"
}
```

---

## Forbidden Patterns & Limitations (What is NOT Allowed)

To ensure validation consistency and prevent runtime crashes or performance bottlenecks, the following configurations are strictly forbidden and will fail semantic validation:

1. **Referencing Formula Columns (Flat Model Constraint)**:
    - A formula column **cannot** reference another formula column (neither in local fields nor during relation/back-relation aggregation). Chaining formulas is not allowed.
2. **Direct Relational References**:
    - You **cannot** reference a relation column itself as a standalone field in a formula (e.g., `[contratista]` as a standalone field is forbidden).
    - However, for direct (single) relations, you **can** traverse them to reference specific fields on the related record (e.g., `[contratista].[Tarifa Hora]`). For back-relations or multi-relations, you must use an `aggregate` node.
3. **Non-Numeric Arguments in Math Operators**:
    - Math operators (`add`, `subtract`, `multiply`, `divide`) require all arguments to resolve to `number` or `autoIncrement` types. Passing strings, booleans, dates, or tags is not allowed.
4. **Non-Numeric Aggregations**:
    - Mathematical aggregation operations (`sum`, `avg`, `sumProduct`) can **only** target numeric fields in the related table. Trying to sum or average strings or dates is not allowed.
5. **Empty or Non-Numeric arguments in `sumProduct`**:
    - The `sumProduct` aggregate requires at least one argument in the `arguments` array, and all arguments must evaluate to numbers.
6. **Kanban View Order References**:
    - Kanban view order fields cannot be referenced in any formula.
7. **Self-Referential Formulas**:
    - A formula column cannot reference itself, either directly or indirectly.
8. **Manual Writes / API Updates**:
    - Formula columns are read-only (`readOnly: true`). You cannot manually write or update a formula column's value through the record update API.
9. **Maximum Nesting Depth (AST Depth Limit)**:
    - A formula AST **cannot** exceed a maximum depth of **5** (root-to-leaf node count; the root node is depth 1). This limit applies to the entire expression tree (operators, conditionals, aggregates, `padLeft`, etc.). Formulas deeper than 5 are rejected at validation.
    - **How depth is counted:** `depth(node) = 1 + max(depth(children))`. Children are: `arguments` on `operator` / `timeOperator` / `aggregate` (including `sumProduct` weights), `then` and `else` on `ifElse`, and `value` on `padLeft`. QueryDSL filters (`applyIf`, `ifElse.filter`, `aggregate.filter`) are **not** part of AST depth.
10. **Fields with Brackets in Name**:
    - Columns/fields **cannot** be created or renamed to contain `[` or `]` in their name. This is to ensure that paths can be unambiguously parsed in formula expressions.

---

## Edge Cases & Safety Behaviors

1. **Division by Zero Safety**:
    - If the denominator in a `"divide"` operation resolves to `0` or `null`, the operation fails gracefully. The cell will be saved with `value: null`, `isValid: false`, and `error: "Division by zero"`.
2. **Precondition (`applyIf`) Evaluation & Fallbacks**:
    - If a record does not match the query specified in `applyIf`, the evaluation engine skips calculating the main expression.
    - The cell value will evaluate to `value: null` with `isValid: true` and `error: null` (top-level fallbacks on the column metadata are not schema-supported).
3. **Circular Dependencies & Self-References**:
    - Creating or updating a formula column that references itself will fail schema validation with a `Column "<name>" not found` or `flat model constraint` error.
    - The flat model constraint (no formula referencing another formula) fully prevents circular reference loops.
4. **Schema Changes (Missing / Renamed Columns)**:
    - If a column referenced by a formula is deleted or renamed, the path cannot be resolved at runtime.
    - The cell state will be set to `value: null`, `isValid: false`, and `error: "Column <name> not found..."` to alert the user.
5. **Floating-Point Arithmetic**:
    - Mathematical calculations use IEEE-754 double-precision floating-point arithmetic. Minor precision differences (e.g. `423.50000000000006` instead of `423.5`) can occur.
6. **Querying Formula Validity**:
    - You can query records based on whether their formula calculated successfully using the `isValid` and `isInvalid` operators (which require no value). For example, to find rows where a division-by-zero or other calculation error occurred: `{"path": "[My Formula Field]", "operator": "isInvalid"}`.
7. **Percent-Formatted Column Scaling**:
    - When a formula references a standard `number` column configured with `"format": "percent"`, the value is automatically divided by `100` (e.g. `10` becomes `0.1`). This allows intuitive multiplication (e.g., `[Subtotal] * [Tax Rate]`) without manually dividing by 100 in the formula. Note that this auto-division does not apply when referencing other formula columns.

---

## CLI Command: Formula Preview

Before creating a formula column, you can preview its output on existing data using the CLI.

### Objects Preview

```bash
frontline object formula preview <object-name> --data '<preview-json>'
```

### Tables Preview

```bash
frontline table formula preview <table-name> --data '<preview-json>'
```

### Preview JSON Payload

```json
{
    "formulaMetadata": {
        "expression": {
            "type": "operator",
            "operator": "concat",
            "arguments": [
                { "type": "field", "field": "[First Name]" },
                { "type": "constant", "value": " " },
                { "type": "field", "field": "[Last Name]" }
            ]
        }
    },
    "previewFilter": {
        "path": "[Status]",
        "operator": "eq",
        "value": "Active"
    },
    "limit": 5
}
```

---

## Comprehensive Real-World Examples

### 1. Margin & Discount Calculations (Math Operators)

Calculate the final price of an item after applying a discount percentage:

```json
{
    "type": "operator",
    "operator": "multiply",
    "arguments": [
        {
            "type": "field",
            "field": "[Price]",
            "fallbackValue": 0
        },
        {
            "type": "operator",
            "operator": "subtract",
            "arguments": [
                { "type": "constant", "value": 1 },
                { "type": "field", "field": "[Discount Rate]", "fallbackValue": 0 }
            ]
        }
    ]
}
```

### 2. Formatted ID Generation (String Concatenation & Padding)

Generate an ticket ID formatted as `TKT-000142`:

```json
{
    "type": "operator",
    "operator": "concat",
    "arguments": [
        { "type": "constant", "value": "TKT-" },
        {
            "type": "padLeft",
            "value": { "type": "field", "field": "[Auto ID]" },
            "length": 6,
            "char": "0"
        }
    ]
}
```

### 3. Total Invoice Amount (SUM_PRODUCT Aggregate)

Calculate the total invoice price by summing `(Quantity * Unit Price)` across all related Line Items:

```json
{
    "type": "aggregate",
    "relation": "Line Items",
    "field": "Quantity",
    "operation": "sumProduct",
    "arguments": [
        {
            "type": "field",
            "field": "[Line Items].[Unit Price]"
        }
    ]
}
```

### 4. Dynamic Commission (ApplyIf Filter Conditions)

Apply a 10% commission only if the deal `[Amount]` is greater than or equal to $10,000 (otherwise, commission is 5%):

**Commission Field definition:**

- `applyIf`: `{"path": "[Amount]", "operator": "gte", "value": 10000}`
- `expression`:
    ```json
    {
        "type": "operator",
        "operator": "multiply",
        "arguments": [
            { "type": "field", "field": "[Amount]" },
            { "type": "constant", "value": 0.1 }
        ]
    }
    ```
- `fallbackValue` on the column definition handles the alternative case (5% commission) when the query filter is not matched.

### 5. Inline Conditionals (ifElse Node)

Evaluate conditional branches directly inside the formula expression using standard query filters:

```json
{
    "type": "ifElse",
    "filter": {
        "path": "[Es Feriado]",
        "operator": "isTrue"
    },
    "then": {
        "type": "operator",
        "operator": "multiply",
        "arguments": [
            { "type": "field", "field": "[Hours]" },
            { "type": "constant", "value": 200 }
        ]
    },
    "else": {
        "type": "operator",
        "operator": "multiply",
        "arguments": [
            { "type": "field", "field": "[Hours]" },
            { "type": "constant", "value": 100 }
        ]
    }
}
```

### 6. Filtered Aggregations (aggregate Node Filter)

Filter child rows dynamic tables when aggregating records (reuses standard query condition filters):

```json
{
    "type": "aggregate",
    "relation": "log_horas",
    "field": "Hours",
    "operation": "sum",
    "filter": {
        "path": "[Es Feriado]",
        "operator": "isTrue"
    }
}
```

---

## 7. QueryDSL Filter Operator Reference

When writing filters for `ifElse` nodes, aggregate `filter` objects, or preconditions (`applyIf`), you MUST use the exact operator strings defined in the system. Verbose natural-language names (like `greaterThan` or `lessThanOrEqual`) are invalid and will trigger schema validation errors.

For the complete list of allowed operator strings by field type, refer to the [Filter & Query Skill (QueryDSL)](../filter-and-query/SKILL.md).

---

## 8. Recalculation Engine: Execution Paths

The formula engine operates under two distinct paths depending on whether you are editing schema columns or mutating records:

### A. Bulk Recalculation Path

- **Trigger**: When a formula column is created, updated (metadata or expression change), or restored.
- **Mechanism**: Runs a high-performance database-level aggregation pipeline. First, it performs `updateMany` to nullify values not matching `applyIf`, and then executes `$merge` directly inside MongoDB.
- **Workflow / Automation Side-Effects**: **Bypassed.** Runs directly in the database without firing events or triggers (`runsCount` stays at `0` for automation workflows).

### B. Incremental Recalculation Path

- **Trigger**: When a row/record value is mutated via the update API, or when a related record referenced by a formula changes.
- **Mechanism**: Calculates the formulas in-memory using Node.js, updates the specific row(s), and triggers updates on dependent rows/columns in cascade.
- **Workflow / Automation Side-Effects**: **Active.** Dispatches update events, fires WebSockets, creates audit logs, and triggers automation workflows.

---

## Advanced Nested Conditional Example (AST depth 4 of 5)

Below is a nested conditional formula (AST depth **4**) evaluating holiday status, contractor tag types, and variable math:

```json
{
    "type": "ifElse",
    "filter": {
        "path": "[Es Feriado]",
        "operator": "isTrue"
    },
    "then": {
        "type": "ifElse",
        "filter": {
            "path": "[Etiquetas]",
            "operator": "containsAny",
            "value": [70]
        },
        "then": {
            "type": "operator",
            "operator": "multiply",
            "arguments": [
                { "type": "field", "field": "[Hours]" },
                { "type": "field", "field": "[contratista].[Tarifa Hora]" },
                { "type": "constant", "value": 4 }
            ]
        },
        "else": {
            "type": "operator",
            "operator": "multiply",
            "arguments": [
                { "type": "field", "field": "[Hours]" },
                { "type": "field", "field": "[contratista].[Tarifa Hora]" },
                { "type": "constant", "value": 2 }
            ]
        }
    },
    "else": {
        "type": "ifElse",
        "filter": {
            "path": "[Etiquetas]",
            "operator": "containsAny",
            "value": [71]
        },
        "then": {
            "type": "operator",
            "operator": "multiply",
            "arguments": [
                { "type": "field", "field": "[Hours]" },
                { "type": "field", "field": "[contratista].[Tarifa Hora]" },
                { "type": "constant", "value": 1.5 }
            ]
        },
        "else": {
            "type": "operator",
            "operator": "multiply",
            "arguments": [
                { "type": "field", "field": "[Hours]" },
                { "type": "field", "field": "[contratista].[Tarifa Hora]" }
            ]
        }
    }
}
```
