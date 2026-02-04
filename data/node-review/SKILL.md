---
name: node-review
description: Review workscript node implementations for alignment with NODE_DEVELOPMENT_BLUEPRINT.md and consistency with the new-node skill. Use when reviewing node code, auditing node implementations, checking for compliance with single-edge return pattern, validating ai_hints metadata consistency, or ensuring thorough documentation of state interactions. Triggers on requests like "review this node", "check node compliance", "audit node implementation", or "validate node metadata".
---

# Workscript Node Review Skill

Review workflow node implementations for compliance with the NODE_DEVELOPMENT_BLUEPRINT.md and consistency with the new-node skill patterns.

## Review Process

### Step 1: Read the Node Implementation

Read the complete node file to understand:
- Class name and file location
- Metadata structure (id, name, version, description, inputs, outputs, ai_hints)
- Execute method logic and return patterns
- State mutations and edge data

### Step 2: Run the Checklist

See [references/checklist.md](references/checklist.md) for the complete review checklist covering:
- Structure compliance
- Single-edge return pattern
- Metadata completeness
- ai_hints consistency
- State management
- Error handling
- Documentation quality

### Step 3: Check for Common Issues

See [references/common-issues.md](references/common-issues.md) for frequent problems and fixes.

**Critical consistency issues to verify:**

1. **ai_hints.example_usage must use exact node id**
   ```typescript
   // If metadata.id = 'calculateField'

   // WRONG - suffixed with '-1'
   example_usage: '{"calculateField-1": {...}}'

   // CORRECT - exact id
   example_usage: '{"calculateField": {...}}'
   ```

2. **All edge names in example_usage must match expected_edges**
   ```typescript
   // If expected_edges: ['success', 'error', 'empty']

   // WRONG - uses 'done' which isn't in expected_edges
   example_usage: '{"myNode": {"done?": "next"}}'

   // CORRECT - uses 'success' which is in expected_edges
   example_usage: '{"myNode": {"success?": "next"}}'
   ```

3. **State key names must be consistent**
   - Document in `post_to_state` exactly what keys are written
   - Verify the code actually writes those exact keys
   - Use namespaced keys (e.g., `filterResult` not `result`)

### Step 4: Document State Interactions

For each node, produce a **State Interaction Documentation** section:

```markdown
## State Interactions

### Reads from State (get_from_state)
- `$.inputArray` - Array of items to process (resolved by engine before execution)
- `$.config.threshold` - Optional threshold value from nested state

### Writes to State (post_to_state)
- `filterResult` - Array of items matching the filter criteria
- `filterCount` - Number of items that matched
- `filterApplied` - Boolean indicating filter was executed

### Edge Data Returns
- **success**: `{ filtered: [...], count: number, originalCount: number }`
- **empty**: `{ count: 0, criteria: {...} }`
- **error**: `{ error: string, nodeId: string }`
```

### Step 5: Verify Workflow Usage Example

Ensure the node's documentation includes a clear workflow usage example:

```json
{
  "filter-data": {
    "data": "$.items",
    "field": "status",
    "operator": "equals",
    "value": "active",
    "success?": "process-results",
    "empty?": "handle-empty",
    "error?": "log-error"
  }
}
```

The example must:
- Use the exact node id (no `-1` suffix)
- Show all required config parameters
- Show relevant edge routing for all expected_edges
- Include state references where applicable

### Step 6: Generate Review Report

Produce a structured review report:

```markdown
## Node Review: [NodeName]

### Compliance Status: [PASS/NEEDS FIXES]

### Issues Found
1. [Issue description]
   - Location: [line/section]
   - Fix: [recommended fix]

### Checklist Summary
- [ ] Single-edge return pattern: PASS/FAIL
- [ ] Metadata complete: PASS/FAIL
- [ ] ai_hints consistent: PASS/FAIL
- [ ] State documented: PASS/FAIL
- [ ] Error handling: PASS/FAIL

### State Interaction Documentation
[Include full state documentation]

### Recommended Fixes
[List specific code changes if needed]
```

## Quick Validation Commands

After reviewing, verify the node builds and tests pass:

```bash
bun run build:nodes
bun run test:nodes
```
