---
name: n8n-support
description: Comprehensive n8n workflow engineering support for creating production-ready workflows. Use when users need to generate n8n workflows, debug loop execution issues, implement nested operations, design data table architectures, fix anti-patterns, create parallel processing patterns, handle webhook callbacks, or build complex multi-tier workflows. Provides battle-tested patterns that work around known n8n bugs and limitations.
---

# n8n Workflow Support

Production-ready patterns for n8n workflow automation that work around platform limitations.

## Quick Start Checklist

Before generating ANY n8n workflow:

1. **Nested loops?** → Use sub-workflows (ONLY reliable method)
2. **Need state?** → Use Data Tables (50MB limit per table)
3. **Parallel processing?** → Must have Merge node to converge
4. **Status updates?** → Keep HTTP callbacks inline, never parallel
5. **Google Sheets?** → Use Append in loops, not Update
6. **Complex data flow?** → Create multiple specialized Data Tables

## Critical Platform Knowledge

### ✅ What Actually Works
- **Sub-workflows**: Clean execution contexts for nested operations
- **Native Data Tables**: Primary state management solution
- **Conditional Loop-Back**: Using IF nodes to branch back
- **Webhook Callbacks**: For async coordination (inline only)
- **Pass-Through State**: State in item JSON data
- **Merge Nodes**: Left joins instead of nested loops
- **Google Sheets Append**: For data capture in loops

### ❌ Broken Features (DO NOT USE)
- Direct nested Loop Over Items → State corruption guaranteed
- $workflow.staticData in Code nodes → Does not exist
- Microsoft Excel in loops → Fails silently
- Loop state auto-reset → Doesn't happen
- Parallel callbacks → May never execute
- Memory-based state → Not persistent

## Core Workflow Patterns

### Pattern 1: Simple Loop with State
```
[Initialize Data] → [Data Table: Init] → [Process] → [IF: Continue?]
                            ↑                              ↓ false
                            └──────────── true ────────────┘
                                                           ↓
                                                      [Continue]
```

### Pattern 2: Nested Operations (Sub-workflows Required)
```
Main: [Loop Over Items] → [Execute Sub-workflow] → [Merge/Wait] → [Continue]
                                    ↓
                            [Clean Context]
                                    ↓
Sub: [Inner Loop] → [Process] → [Webhook Callback]
```

### Pattern 3: Parallel Processing with Convergence
```
[Split In Batches] → [Execute Workflow] → [Merge (Wait All)] → [Aggregate]
         ↓                                         ↑
    [Parallel Branches] ───────────────────────────┘
```

### Pattern 4: Data Enrichment Without Nesting
```
[Load Reference] → [Store in Table] → [Process Items] → [Merge by Key]
                                              ↓
                                    [Enrich Input 1 Mode]
```

## Data Table Architecture

### Essential Tables Structure

Create multiple tables for complex workflows:

```javascript
// execution_tracker - Core execution state
{
  execution_id: "string (PK)",
  entity_type: "string",
  entity_id: "string", 
  status: "processing|complete|error",
  parent_id: "string",
  metadata: "json",
  created_at: "datetime"
}

// content_storage - Generated content
{
  content_id: "string (PK)",
  entity_id: "string",
  content_type: "string",
  content: "json",
  version: "number",
  created_at: "datetime"
}

// workflow_state - Temporary state
{
  state_id: "string (PK)",
  execution_id: "string",
  state_key: "string",
  state_value: "json",
  expires_at: "datetime"
}
```

## Code Node Patterns

### Initialize Loop State
```javascript
// Always pass state through items
return [{
  json: {
    _execution_id: $execution.id,
    _iteration: 0,
    _max_iterations: 10,
    data: $json,
    _continue: true
  }
}];
```

### Increment Counter
```javascript
// State in item, not static variables
return [{
  json: {
    ...$json,
    _iteration: ($json._iteration || 0) + 1,
    _continue: ($json._iteration + 1) < $json._max_iterations
  }
}];
```

### Check Dependencies
```javascript
// For complex workflows with dependencies
const canProceed = $json.required_items?.every(
  item => $json.completed_items?.includes(item)
);
return [{
  json: {
    ...$json,
    can_proceed: canProceed,
    status: canProceed ? "ready" : "waiting"
  }
}];
```

## Error Handling

Every workflow needs:
1. Error Trigger workflow (separate)
2. Exponential backoff: `Wait = 2^retry_count` seconds
3. Max retries: 3
4. Error logging in Data Table
5. Dead letter pattern for failures

## Node Configurations

### Loop Over Items
```json
{
  "batchSize": 1,
  "options": {
    "pauseBetweenItems": 100
  }
}
```

### Execute Sub-workflow
```json
{
  "source": "database",
  "workflow": "{{ $json.workflow_id }}",
  "waitForSubWorkflow": false,
  "options": {
    "shareParentExecutionId": false
  }
}
```

### Merge Node (for parallel convergence)
```json
{
  "mode": "waitForAll",
  "outputKey": "combined",
  "keepOnlyProperties": false
}
```

### Data Table Upsert
```json
{
  "operation": "upsert",
  "tableId": "{{ $json.table_name }}",
  "fieldsToMatch": ["execution_id", "entity_id"],
  "options": {
    "returnData": true
  }
}
```

## Testing Checklist

Before deployment:
- [ ] All nested loops use sub-workflows
- [ ] Data Tables initialized properly
- [ ] No staticData in Code nodes
- [ ] Google Sheets uses Append in loops
- [ ] All parallel branches converge
- [ ] HTTP callbacks are inline
- [ ] Max iteration safeguards in place
- [ ] Error handling implemented
- [ ] Tested with 0, 1, and many items

## Advanced Patterns

For complex patterns, see references:
- **Multi-tier workflows**: See [references/hierarchical-workflows.md](references/hierarchical-workflows.md)
- **Table management**: See [references/table-manager.md](references/table-manager.md)  
- **Anti-patterns**: See [references/anti-patterns.md](references/anti-patterns.md)
- **GitHub issues**: See [references/known-issues.md](references/known-issues.md)

## Webhook Patterns

### Status Update (Inline)
```
[Process] → [HTTP: Update Status] → [Check Response] → [Continue]
                    ↓
            [Must wait for response]
```

### Async Callback
```
Main: [Execute Sub] → [Wait Node (Resume on Webhook)] → [Process Result]
                                    ↑
Sub: [Process] → [HTTP: Callback] ─┘
```

## Quick Fixes

### Loop Only Runs Once?
- Solution: Use sub-workflow for inner loop
- Why: Execution context pollution

### Parallel Tasks Not Completing?
- Solution: Add Merge node with waitForAll
- Why: n8n needs explicit convergence

### Callbacks Not Firing?
- Solution: Move HTTP callback inline
- Why: Parallel branches may not execute

### State Not Persisting?
- Solution: Use Data Tables, not variables
- Why: No static data in Code nodes

## When to Call Scripts

- **Table setup**: Run `scripts/table-manager.py` first
- **Workflow generation**: Use `scripts/generate-workflow.py`
- **Validation**: Run `scripts/validate-workflow.py`
