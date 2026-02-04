---
name: document-node
description: Generate comprehensive {node_name}.example.json files that showcase real-world usage of Workscript workflow nodes. Use when asked to document a node, create node documentation, generate node examples, or produce usage examples for workflow nodes. Also use when a subagent needs to create node documentation as part of node development or review.
---

# Document Node Skill

Generate production-quality `{node_name}.example.json` workflow files demonstrating correct usage of Workscript nodes.

## Required Context

Before generating documentation, you MUST:

1. **Read the node source file** (`.ts` file) to understand:
   - `metadata.id` - The node type identifier
   - `metadata.inputs` - Expected configuration parameters
   - `metadata.outputs` - Output data structure
   - `metadata.ai_hints` - Purpose, when_to_use, expected_edges, post_to_state
   - `execute()` method - All conditional logic and edge returns

2. **Locate the node** in `/packages/nodes/src/` or subdirectories:
   - Core nodes: `/packages/nodes/src/{NodeName}.ts`
   - Data nodes: `/packages/nodes/src/data/{NodeName}.ts`
   - Custom nodes: `/packages/nodes/src/custom/{integration}/{NodeName}.ts`

## Output Format

Create file: `{node_name}.example.json` in same directory as the node source.

```json
{
  "id": "{node-id}-examples",
  "name": "{NodeName} Examples",
  "version": "1.0.0",
  "description": "Comprehensive examples demonstrating all {NodeName} capabilities",
  "initialState": { /* Realistic test data */ },
  "workflow": [ /* Inline nested configuration examples */ ]
}
```

## Critical Rules

### Rule 1: Sequential Feature Showcase (NOT Deep Nesting)

**For documentation examples**, use a **flat sequential array** where each step demonstrates a different feature of the node being documented. This makes examples clear and easy to understand.

**DO NOT** create deeply nested workflows - even if they are technically correct, they obscure the features being demonstrated.

```json
// WRONG - Deeply nested (hard to read, obscures individual features)
{
  "workflow": [
    {
      "extractText": {
        "method": "extractAll",
        "extractType": "email",
        "success?": {
          "extractText": {
            "method": "extractAll",
            "extractType": "url",
            "success?": {
              "extractText": {
                "method": "regex",
                "pattern": "...",
                "success?": {
                  "log": { "message": "Done" }
                }
              }
            }
          }
        }
      }
    }
  ]
}

// CORRECT - Sequential steps showcasing each feature clearly
{
  "workflow": [
    {
      "extractText": {
        "method": "extractAll",
        "field": "emailText",
        "extractType": "email",
        "outputField": "allEmails",
        "success?": "log"
      }
    },
    {
      "extractText": {
        "method": "extractSpecific",
        "field": "emailText",
        "extractType": "email",
        "occurrence": 0,
        "outputField": "primaryEmail",
        "success?": "log"
      }
    },
    {
      "extractText": {
        "method": "regex",
        "field": "productData",
        "pattern": "Product: ([A-Z0-9]+)",
        "flags": "g",
        "outputField": "productIds",
        "success?": "log"
      }
    },
    {
      "log": {
        "message": "All examples completed!",
        "results": "$.allEmails"
      }
    }
  ]
}
```

**Key principles for documentation examples:**
- Each workflow step = one feature/operation demonstration
- Use simple edge terminations (`"success?": "log"`) not deep nesting
- Group related examples by operation type in sequence
- End with a summary log showing all collected results
- Edges CAN use string references like `"log"` in documentation examples

### Rule 2: Realistic Initial State

Create domain-appropriate test data:

```json
{
  "initialState": {
    "products": [
      { "id": 1, "name": "Laptop", "price": 999.99, "inStock": true, "category": "Electronics" },
      { "id": 2, "name": "Mouse", "price": 29.99, "inStock": false, "category": "Electronics" }
    ],
    "users": [
      { "id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin" }
    ]
  }
}
```

### Rule 3: Demonstrate ALL Edges

For each node, show workflows that trigger each possible edge:

```json
// Node with success/error/found/not_found edges
{
  "database": {
    "operation": "find",
    "table": "users",
    "query": { "id": "$.userId" },
    "found?": { /* next node inline */ },
    "not_found?": { /* handle missing */ },
    "error?": { /* handle error */ }
  }
}
```

### Rule 4: Show All Operations

If the node supports multiple operations, demonstrate each:

```json
// Math node - show add, subtract, multiply, divide
// Filter node - show equals, contains, gt, lt, between, regex
// Transform node - show stringify, parse, uppercase, lowercase
```

### Rule 5: Edge Naming with `?` Suffix

Edges always end with `?`:
- `success?`, `error?`, `found?`, `not_found?`
- `true?`, `false?`, `valid?`, `invalid?`
- `exists?`, `not_exists?`, `passed?`, `filtered?`

## Generation Process

1. **Read node source file** - Extract metadata and execute logic
2. **Identify all operations** - List every operation/mode the node supports
3. **Identify all edges** - List every edge the node can return
4. **Design initial state** - Create realistic test data matching node inputs
5. **Create examples** - One workflow section per major use case
6. **Add documentation logs** - Include log nodes showing results

## Example Structure Template

```json
{
  "id": "{node-id}-examples",
  "name": "{NodeName} Examples",
  "version": "1.0.0",
  "description": "Comprehensive examples demonstrating all {NodeName} capabilities",
  "initialState": {
    "/* Realistic domain data matching node inputs - provide multiple data sources to showcase different features */"
  },
  "workflow": [
    {
      "{node-id}": {
        "/* Example 1: Basic usage - simplest configuration */",
        "outputField": "example1Result",
        "success?": "log"
      }
    },
    {
      "{node-id}": {
        "/* Example 2: Different operation/mode */",
        "outputField": "example2Result",
        "success?": "log"
      }
    },
    {
      "{node-id}": {
        "/* Example 3: Advanced usage with all options */",
        "outputField": "example3Result",
        "success?": "log"
      }
    },
    {
      "{node-id}": {
        "/* Example 4: Edge case or alternative configuration */",
        "outputField": "example4Result",
        "success?": "log"
      }
    },
    {
      "log": {
        "message": "All {NodeName} examples completed successfully!",
        "example1Result": "$.example1Result",
        "example2Result": "$.example2Result",
        "example3Result": "$.example3Result",
        "example4Result": "$.example4Result"
      }
    }
  ]
}
```

**Template guidelines:**
- Add one workflow step per feature/operation you want to demonstrate
- Each step should have a unique `outputField` to store results
- Use `"success?": "log"` as a simple edge terminator (not deep nesting!)
- Final log step summarizes all results using state references

## State References

Use `$.` syntax for state access:
- `$.products` - Access state.products
- `$.user.name` - Access nested state.user.name
- `$.filterPassed` - Access node output stored in state

## State Keys Written by Nodes

Common node state outputs (reference from node's `ai_hints.post_to_state`):
- math: `mathResult`
- logic: `logicResult`
- filter: `filterPassed`, `filterFiltered`, `filterStats`
- sort: `sortedItems`
- validateData: `validationResult`, `validationErrors`
- editFields: `editFieldsResult`, `fieldsModified`
- database: `dbInserted`, `dbRecord`, `dbUpdated`, `dbDeleted`, `dbRecords`
- filesystem: `fileContent`, `fileWritten`, `fileExists`

## Quality Checklist

Before finalizing, verify:

- [ ] Read the actual node source file
- [ ] Used **sequential flat array** pattern (NOT deeply nested workflows)
- [ ] Each workflow step showcases ONE feature/operation of the node
- [ ] Created realistic initialState with multiple data sources for different features
- [ ] Demonstrated all operations/modes the node supports
- [ ] Showed all edge paths (success, error, and conditional edges)
- [ ] Used correct edge naming with `?` suffix
- [ ] Used `"success?": "log"` as simple terminators (not deep nesting)
- [ ] Referenced correct state keys (from ai_hints.post_to_state)
- [ ] Each step writes to unique outputField for clear result tracking
- [ ] Final summary log shows all collected results
- [ ] File saved as `{node_id}.example.json` in node's directory

## Quick Reference: Workflow JSON Schema

```json
{
  "id": "string (required, pattern: ^[a-zA-Z0-9_-]+$)",
  "name": "string (required)",
  "version": "string (required, pattern: ^\\d+\\.\\d+\\.\\d+$)",
  "description": "string (optional)",
  "initialState": "object (optional)",
  "workflow": "array (required, min: 1 item)"
}
```

## Reference: Reading Node Source

When reading a node's `.ts` file, extract:

```typescript
metadata = {
  id: 'node-id',           // Use this in workflow
  name: 'Node Name',       // Use in description
  inputs: ['param1'],      // Config parameters
  outputs: ['result'],     // Edge data keys
  ai_hints: {
    purpose: '...',
    when_to_use: '...',
    expected_edges: ['success', 'error'],  // All possible edges
    example_config: '...',
    post_to_state: ['stateKey']            // State keys written
  }
};
```

Analyze the `execute()` method to understand:
- All `return { edgeName: () => ({...}) }` statements
- Conditional logic that determines which edge is returned
- Required vs optional configuration parameters
