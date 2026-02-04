---
name: simple-task
description: Format and validate JSON data structures. Use when you need to pretty-print JSON, validate syntax, or convert between compact and formatted JSON.
license: MIT
---

# Simple Task - JSON Formatter

Format and validate JSON data structures with consistent styling.

## When to Use This Skill

Use this skill when you need to:

- Pretty-print JSON for readability
- Validate JSON syntax
- Convert compact JSON to formatted JSON
- Ensure consistent JSON formatting
- Debug JSON structure issues

## Process

### Step 1: Receive JSON Input

Accept JSON data in one of these forms:

- Raw JSON string
- JSON file path
- Inline JSON object

### Step 2: Validate Syntax

Check if the JSON is valid:

1. Attempt to parse the JSON
2. Identify syntax errors if present
3. Report specific error location and type

### Step 3: Format JSON

Apply consistent formatting:

1. Use 2-space indentation
2. Sort keys alphabetically (optional)
3. Ensure trailing newline

### Step 4: Output Result

Provide the formatted JSON:

- Display formatted output
- Save to file if requested
- Report any validation errors

## Examples

### Example 1: Basic Formatting

**Input**:

```json
{ "name": "John", "age": 30, "city": "New York" }
```

**Process**:

1. Parse JSON (valid)
2. Apply 2-space indentation
3. Format output

**Expected Output**:

```json
{
  "name": "John",
  "age": 30,
  "city": "New York"
}
```

### Example 2: Validation Error

**Input**:

```json
{ "name": "John", "age": 30 }
```

**Process**:

1. Attempt to parse
2. Detect syntax error (trailing comma)
3. Report error location

**Expected Output**:

```text
Error: Invalid JSON syntax
Line 1, position 25: Unexpected token }
Trailing comma not allowed in JSON
```

### Example 3: Nested Structure

**Input**:

```json
{
  "user": {
    "name": "Alice",
    "contact": { "email": "alice@example.com", "phone": "555-0123" }
  },
  "active": true
}
```

**Process**:

1. Parse complex nested structure
2. Apply formatting recursively
3. Maintain key order

**Expected Output**:

```json
{
  "user": {
    "name": "Alice",
    "contact": {
      "email": "alice@example.com",
      "phone": "555-0123"
    }
  },
  "active": true
}
```

## Best Practices

- Always validate before formatting
- Use consistent indentation (2 spaces recommended)
- Preserve data types (numbers, booleans, null)
- Handle edge cases (empty objects, arrays)
- Provide clear error messages for invalid JSON

## Common Pitfalls

- **Trailing commas**: Not valid in standard JSON
- **Single quotes**: JSON requires double quotes
- **Unquoted keys**: Keys must be quoted strings
- **Comments**: Not supported in standard JSON
- **Special characters**: Must be properly escaped

## Dependencies

No external dependencies required. Uses standard JSON parsing capabilities.

## Error Handling

**Invalid JSON**:

- Report syntax error with location
- Suggest common fixes
- Do not attempt to format

**Empty Input**:

- Return empty object `{}` or array `[]`
- Do not error on empty input

**File Not Found**:

- Report file path error
- Suggest checking path
- Do not continue processing
