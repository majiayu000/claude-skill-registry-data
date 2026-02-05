---
name: new-node
description: Create new workflow nodes for the Workscript engine or refactor existing nodes. Generate complete, production-ready node implementations following the single-edge return pattern. Use when creating new nodes, developing custom integrations, building data manipulation nodes, refactoring existing nodes, or implementing workflow capabilities.
---

# Workscript Node Development Skill

## Overview

This skill helps you create and refactor workflow nodes for the Workscript Agentic Workflow Engine. All nodes follow a consistent pattern with the **critical single-edge return rule**: every node execution MUST return an EdgeMap with exactly ONE key.

## Instructions

When creating or refactoring a node, follow these steps:

### Step 1: Gather Requirements

Ask clarifying questions to understand:
1. **Node purpose** - What should this node do?
2. **Node category** - Core, data manipulation, server, or custom integration?
3. **Inputs** - What configuration parameters does it need?
4. **Outputs** - What data should it return via edges?
5. **Edge types** - What routing outcomes are possible? (success/error, found/not_found, true/false, etc.)
6. **State mutations** - What state keys should it write?

### Step 2: Determine File Location

Based on category, place the node file in:
- **Core nodes** → `/packages/nodes/src/MyNode.ts`
- **Data manipulation** → `/packages/nodes/src/data/MyNode.ts`
- **Custom integrations** → `/packages/nodes/src/custom/[provider]/MyNode.ts`

### Step 3: Create the Node File

Use the appropriate template from [templates/](templates/):
- [standard-node.ts](templates/standard-node.ts) - Basic success/error pattern
- [boolean-node.ts](templates/boolean-node.ts) - True/false branching
- [lookup-node.ts](templates/lookup-node.ts) - Found/not_found pattern
- [multi-outcome-node.ts](templates/multi-outcome-node.ts) - Multiple routing outcomes
- [external-api-node.ts](templates/external-api-node.ts) - HTTP/API calls
- [database-node.ts](templates/database-node.ts) - Database operations

### Step 4: Implement the Node Structure

Every node MUST have:

```typescript
import { WorkflowNode } from '@workscript/engine';
import type { ExecutionContext, EdgeMap } from '@workscript/engine';

export class MyNode extends WorkflowNode {
  // 1. Complete metadata with ai_hints
  metadata = {
    id: 'myNode',           // Unique identifier (camelCase or kebab-case)
    name: 'My Node',        // Human-readable name
    version: '1.0.0',       // Semantic version
    description: 'What this node does',
    inputs: ['param1', 'param2'],
    outputs: ['result'],
    ai_hints: {
      purpose: 'Brief purpose statement',
      when_to_use: 'When to use this node',
      expected_edges: ['success', 'error'],
      example_usage: '{"my-node": {"param1": "value", "success?": "next"}}',
      example_config: '{"param1": "string", "param2?": "number"}',
      get_from_state: [],
      post_to_state: ['myNodeResult']
    }
  };

  // 2. Execute method with single-edge return
  async execute(context: ExecutionContext, config?: any): Promise<EdgeMap> {
    // Implementation following the pattern
  }
}

export default MyNode;
```

### Step 5: Follow the Single-Edge Return Pattern

**CRITICAL**: The execute method must ALWAYS return exactly ONE edge key:

```typescript
async execute(context: ExecutionContext, config?: any): Promise<EdgeMap> {
  const { param } = config || {};

  // VALIDATION - Return error edge immediately
  if (!param) {
    return {
      error: () => ({ error: 'Missing required parameter: param' })
    };
  }

  // BUSINESS LOGIC in try-catch
  try {
    const result = await this.operation(param);
    context.state.myNodeResult = result;

    // Return SINGLE success edge
    return {
      success: () => ({ result })
    };

  } catch (error) {
    // Return SINGLE error edge from catch
    return {
      error: () => ({
        error: error instanceof Error ? error.message : 'Operation failed',
        nodeId: context.nodeId
      })
    };
  }
}
```

### Step 6: Export the Node

Add exports to `/packages/nodes/src/index.ts`:

```typescript
// Add import
import MyNewNode from './MyNewNode';

// Add to ALL_NODES array
export const ALL_NODES = [
  // ... existing nodes
  MyNewNode,
];

// Add individual export
export { MyNewNode };
```

### Step 7: Create Tests

Create a test file alongside the implementation:

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { MyNode } from './MyNode';
import type { ExecutionContext } from '@workscript/engine';

describe('MyNode', () => {
  let node: MyNode;
  let context: ExecutionContext;

  beforeEach(() => {
    node = new MyNode();
    context = {
      state: {},
      inputs: {},
      workflowId: 'test-workflow',
      nodeId: 'test-node',
      executionId: 'test-execution-123'
    };
  });

  // CRITICAL: Always test single-edge return
  it('should return only one edge key', async () => {
    const result = await node.execute(context, { param: 'value' });
    expect(Object.keys(result)).toHaveLength(1);
  });
});
```

### Step 8: Build and Verify

```bash
bun run build:nodes
bun run test:nodes
```

## Refactoring Existing Nodes

When refactoring:

1. **Read the existing node** to understand current behavior
2. **Identify issues** - Check for multiple edge returns, missing validation, unclear naming
3. **Apply fixes** following the single-edge pattern
4. **Update tests** to verify single-edge return
5. **Update exports** if node ID changes

## Common Edge Patterns

| Pattern | Edge Names | Use Case |
|---------|------------|----------|
| Success/Error | `success`, `error` | Basic operations |
| Boolean | `true`, `false`, `error` | Conditional logic |
| Lookup | `found`, `not_found`, `error` | Search operations |
| Exists | `exists`, `not_exists`, `error` | File/record checks |
| Multi-value | `high`, `medium`, `low`, `error` | Categorization |
| Empty/Results | `success`, `empty`, `error` | List operations |

## Best Practices

1. **Single Responsibility** - One node, one purpose
2. **Early Validation** - Return error edge immediately for invalid inputs
3. **Clear Naming** - Use semantic edge names (not "ok" or "done")
4. **State Namespacing** - Use prefixed keys like `myNodeResult`
5. **Meaningful Errors** - Include nodeId, operation, and suggestion in errors
6. **No Instance State** - Keep nodes stateless, use context.state
7. **Complete ai_hints** - Help AI workflows generate correct usage

## Reference

For comprehensive documentation, see:
- [reference.md](reference.md) - Quick reference and patterns
- [examples.md](examples.md) - Complete node examples
- [NODE_DEVELOPMENT_BLUEPRINT.md](/NODE_DEVELOPMENT_BLUEPRINT.md) - Full blueprint

## Workflow JSON Usage

After creating a node, use it in workflows:

```json
{
  "id": "my-workflow",
  "name": "My Workflow",
  "version": "1.0.0",
  "initialState": {},
  "workflow": [
    {
      "my-node-1": {
        "param1": "value",
        "param2": 42,
        "success?": "next-node",
        "error?": "error-handler"
      }
    }
  ]
}
```
