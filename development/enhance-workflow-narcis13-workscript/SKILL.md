---
name: enhance-workflow
description: Analyze, refactor, and enhance existing Workscript workflow JSON files based on user feedback. Use when asked to improve, optimize, refactor, fix, or enhance an existing workflow. Triggers on requests like "improve this workflow", "optimize the X workflow", "add error handling to", "make this workflow more robust", "refactor for flat structure", or when users provide critique, suggestions, or requirements for workflow improvements. Complements the new-workflow skill by handling post-creation refinements.
---

# Workscript Workflow Enhancer

Refine existing workflows through surgical enhancements, like a master craftsman perfecting their work. Every enhancement removes what doesn't belong and reveals the workflow's true potential.

## Core Philosophy

**Surgical precision over wholesale rewriting.** Enhancing a workflow means understanding its purpose and making focused changes that improve without disrupting. Changes should be:

- **Targeted**: Address specific issues without side effects
- **Preserving**: Maintain what already works well
- **Additive when needed**: Add guards, error handling, or new branches
- **Subtractive when possible**: Remove unnecessary nesting, redundancy, or complexity

## Enhancement Workflow

Workflow enhancement follows these steps:

1. Identify the target workflow
2. Analyze the workflow thoroughly
3. Understand the enhancement request
4. Plan targeted changes
5. Implement enhancements
6. Validate improvements

### Step 1: Identify the Target Workflow

The user must specify which workflow to enhance. Accept:

- Direct path: `/apps/sandbox/resources/shared/prompts/my-workflow.json`
- Workflow name: `my-workflow` (resolve to standard locations)
- Contextual reference: "the email processing workflow", "data-pipeline.json"

**Default locations to search:**
```
/apps/sandbox/resources/shared/prompts/
/apps/api/prompts/
```

If the target is ambiguous, ask for clarification before proceeding.

### Step 2: Analyze the Workflow Thoroughly

Before making any changes, perform comprehensive analysis using `scripts/analyze-workflow.ts`:

```bash
bun /Users/narcisbrindusescu/teste/workscript/.claude/skills/enhance-workflow/scripts/analyze-workflow.ts <workflow.json>
```

The analysis examines:

- **Structure**: Flat vs nested ratio, nesting depth, node count
- **Guards**: Input validation, AI response validation, array guards
- **Error Handling**: Presence of `error?` edges on nodes that can fail
- **State Management**: State keys read and written, potential conflicts
- **Pattern Usage**: Identified patterns (loops, conditionals, pipelines)
- **Opportunities**: Specific improvement suggestions

Read the full workflow contents and understand:

1. What the workflow does (purpose)
2. How data flows through nodes
3. Where branching occurs and why
4. What guards are present or missing
5. What works well vs. what could improve

### Step 3: Understand the Enhancement Request

User feedback comes in several forms. See `references/enhancement-patterns.md` for detailed patterns.

**Direct requests**: "Add error handling to all nodes", "Flatten the nested structure"
**Observations**: "The workflow fails when AI returns invalid JSON", "It crashes on empty arrays"
**Advice**: "It should validate input first", "The loop needs a guard"
**Critique**: "Too deeply nested", "Missing defensive guards", "Hard to read"

For each piece of feedback, identify:

1. **What** specifically needs to change
2. **Why** the change improves the workflow
3. **Where** in the workflow the change applies
4. **How** to implement without breaking existing functionality

### Step 4: Plan Targeted Changes

Map feedback to specific workflow components:

| Feedback Type | Target | Enhancement Approach |
|---------------|--------|----------------------|
| Missing guards | Entry point | Add `validateData` for input validation |
| AI response fails | After `ask-ai` | Add JSON validation chain |
| Empty array crashes | Before loops | Add `logic` array length guard |
| Too nested | Workflow structure | Flatten sequential operations |
| Missing error handling | All fallible nodes | Add `error?` edges |
| Hard to maintain | Deeply nested branches | Extract to flat workflow array |
| Performance issues | Loops, API calls | Add timeouts, batch processing |

Create a change plan before implementing:

```markdown
## Enhancement Plan

### Target: workflow-id.json

### Changes:
1. [Location] - [Change description] - [Rationale]
2. [Location] - [Change description] - [Rationale]

### Preserved:
- [What stays unchanged and why]

### Risk Assessment:
- [Potential issues and mitigations]
```

### Step 5: Implement Enhancements

Apply changes following these principles:

**For structure changes:**

- Preserve working sections verbatim unless they need changes
- Use surgical edits, not full rewrites
- Convert `success?` chains to flat workflow arrays when sequential
- Keep actual branching (`true?`/`false?`, `valid?`/`invalid?`) as edges

**For adding guards:**

- Add input validation at workflow entry
- Add JSON validation after `ask-ai` calls
- Add array length checks before loops
- Add `error?` edges to all nodes that can fail

**For flattening:**

- Move sequential operations to workflow array
- Keep only true conditional branches as nested edges
- Preserve edge handlers for errors and alternative paths

**For state management:**

- Track what each node writes to state
- Ensure no state key conflicts
- Add intermediate state keys when needed for clarity

### Step 6: Validate Improvements

After implementing changes, validate using the standard workflow validator:

```bash
bun /Users/narcisbrindusescu/teste/workscript/.claude/skills/new-workflow/scripts/validate-workflow.ts <workflow.json>
```

And compare before/after:

```bash
bun /Users/narcisbrindusescu/teste/workscript/.claude/skills/enhance-workflow/scripts/diff-workflows.ts <original.json> <enhanced.json>
```

Validation checks:

1. **Structural integrity**: Valid JSON, required fields present
2. **No regressions**: Original capabilities preserved
3. **Enhancement applied**: Requested changes implemented correctly
4. **Node validity**: All node types registered
5. **State paths valid**: All `$.path` references correct

## Enhancement Categories

### Category 1: Add Defensive Guards

The most common enhancement - making workflows robust against runtime errors.

**Pattern: Input Validation Guard**

Add at workflow entry:

```json
{
  "validateData": {
    "validationType": "required_fields",
    "data": "$.input",
    "requiredFields": ["userId", "action"],
    "invalid?": {
      "log": { "message": "Missing required input: {{$.validationErrors}}" }
    }
  }
}
```

**Pattern: AI Response JSON Guard**

Add after any `ask-ai` expecting structured output:

```json
{
  "validateData": {
    "validationType": "json",
    "data": "$.aiResponse",
    "valid?": {
      "validateData": {
        "validationType": "required_fields",
        "data": "$.parsedJson",
        "requiredFields": ["expectedField"],
        "valid?": { ... },
        "invalid?": {
          "log": { "message": "AI response missing fields: {{$.validationErrors}}" }
        }
      }
    },
    "invalid?": {
      "log": { "message": "AI did not return valid JSON" }
    }
  }
}
```

**Pattern: Array Length Guard**

Add before loops or array operations:

```json
{
  "logic": {
    "operation": "greater",
    "values": ["$.items.length", 0],
    "true?": { ... loop or array processing ... },
    "false?": {
      "log": { "message": "No items to process" }
    }
  }
}
```

### Category 2: Flatten Structure

Convert unnecessarily nested workflows to flat sequential structure.

**Before - Excessive Nesting:**

```json
{
  "workflow": [
    {
      "filter": {
        "success?": {
          "sort": {
            "success?": {
              "log": { "message": "Done" }
            }
          }
        }
      }
    }
  ]
}
```

**After - Flat Sequential:**

```json
{
  "workflow": [
    {
      "filter": {
        "items": "$.data",
        "error?": { "log": { "message": "Filter failed" } }
      }
    },
    {
      "sort": {
        "type": "simple",
        "error?": { "log": { "message": "Sort failed" } }
      }
    },
    {
      "log": { "message": "Done" }
    }
  ]
}
```

### Category 3: Add Error Handling

Ensure all fallible nodes have `error?` edges.

**Nodes that need error? edges:**

| Node Type | Common Errors |
|-----------|---------------|
| `database` | Connection, query syntax, not found |
| `filesystem` | File not found, permissions |
| `fetchApi` | Network, timeout, HTTP errors |
| `ask-ai` | API errors, rate limits |
| `auth` | Invalid credentials |
| `validateData` | Validation failures |

**Enhancement pattern:**

```json
{
  "database": {
    "operation": "find",
    "table": "users",
    "query": { "id": "$.userId" },
    "found?": { ... },
    "not_found?": {
      "log": { "message": "User {{$.userId}} not found" }
    },
    "error?": {
      "log": { "message": "Database error: {{$.error}}" }
    }
  }
}
```

### Category 4: Optimize Loops

Make loops safer and more efficient.

**Add loop guard:**

```json
{
  "logic": {
    "operation": "and",
    "values": [
      { "operation": "greater", "values": ["$.items.length", 0] }
    ],
    "true?": {
      "logic...": {
        "operation": "less",
        "values": ["$.index", "$.items.length"],
        "true?": [ ... loop body ... ],
        "false?": null
      }
    },
    "false?": {
      "log": { "message": "No items to process" }
    }
  }
}
```

### Category 5: Improve State Management

Make state usage clearer and prevent conflicts.

**Pattern: Explicit intermediate state:**

```json
{
  "workflow": [
    {
      "filter": { "items": "$.rawData" }
    },
    {
      "editFields": {
        "mode": "manual_mapping",
        "fieldsToSet": [
          { "name": "filteredData", "value": "$.filterPassed", "type": "array" }
        ]
      }
    },
    {
      "sort": { "type": "simple" }
    },
    {
      "editFields": {
        "mode": "manual_mapping",
        "fieldsToSet": [
          { "name": "processedData", "value": "$.sortedItems", "type": "array" }
        ]
      }
    }
  ]
}
```

## Enhancement Checklist

Before finalizing any enhancement:

- [ ] **Validation passes**: `validate-workflow.ts` returns success
- [ ] **Guards added**: Entry validation, AI validation, array guards
- [ ] **Error edges present**: All fallible nodes have `error?` edges
- [ ] **Structure optimized**: Sequential operations are flat
- [ ] **State is clear**: No ambiguous or conflicting state keys
- [ ] **Version bumped**: Increment version number for changes
- [ ] **Diff reviewed**: Changes match enhancement request

## Anti-Patterns to Avoid

See `references/anti-patterns.md` for detailed examples.

**Over-enhancement**: Adding more than requested, scope creep
**Breaking changes**: Removing functionality without replacement
**Over-flattening**: Flattening actual conditional branches
**Guard overload**: Adding redundant validations
**State pollution**: Adding unnecessary intermediate state keys

## Quick Reference

### Command Reference

```bash
# Analyze workflow
bun .claude/skills/enhance-workflow/scripts/analyze-workflow.ts <workflow.json>

# Validate enhanced workflow
bun .claude/skills/new-workflow/scripts/validate-workflow.ts <workflow.json>

# Compare before/after
bun .claude/skills/enhance-workflow/scripts/diff-workflows.ts <original> <enhanced>
```

### Common Enhancements

| Request | Enhancement |
|---------|-------------|
| "Add guards" | Input validation + AI validation + array guards |
| "Flatten structure" | Convert success? chains to workflow array |
| "Add error handling" | Add error? edges to all fallible nodes |
| "Make robust" | All guards + all error edges |
| "Optimize loop" | Add length guard + exit condition |

### Reference Documentation

- **Enhancement Patterns**: [references/enhancement-patterns.md](references/enhancement-patterns.md)
- **Anti-Patterns**: [references/anti-patterns.md](references/anti-patterns.md)
- **Workflow Syntax**: `/new-workflow/references/workflow-syntax.md`
- **Node Reference**: `/new-workflow/references/node-quick-reference.md`
- **Flat vs Nested**: `/new-workflow/references/flat-vs-nested.md`
