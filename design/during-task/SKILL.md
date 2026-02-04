---
name: during-task
description: Lightweight tactical guidance during implementation. Just MCP suggestions and quick lookups, no heavy Graphiti searches.
---

# @during-task - Lightweight Tactical Guidance

**Use DURING:**
- Implementing tasks from `tasks.md`
- Before coding each subtask
- When switching implementation areas
- When unsure which MCP for specific subtask

**CAN be called MULTIPLE times** (designed for this!)

---

## What It Does (Lightweight!)

```
1. Get MCP suggestions for subtask (no full Graphiti search)
2. Quick gotcha lookup (optional, only if stuck)
3. Brief workflow guidance
```

**Token cost**: ~300 tokens  
**Frequency**: 5-10 times per spec  
**ROI**: Stays aligned = prevents rework

---

## Execution

### Default: Just MCP Suggestions

```typescript
suggest_mcps({
  task: "[specific subtask]",
  include_examples: false
});
```

**Returns:**
- Vibe (might change if switching domains)
- Top 3 MCPs for this subtask
- Brief purpose

### When Stuck: Quick Gotcha Lookup

```typescript
search_memory_facts({
  query: "[specific tech/component] [specific issue]",
  group_ids: ["screengraph"],
  max_facts: 3  // Just top 3, not 10!
});
```

**Returns:**
- Known workarounds
- Quick fixes
- Past solutions

---

## Output Format (Brief!)

```markdown
**Task**: [subtask]
**MCPs**: [mcp1], [mcp2], [mcp3]

Do this:
1. [action 1]
2. [action 2]
```

**~5 lines. That's it.**

---

## Integration

### With Spec-Kit Implementation

```bash
# Already ran @before-task during discovery
# Now implementing tasks.md

# Task 1: Create database schema
@during-task Create user table schema
→ MCPs: encore-mcp, context7
# Code it

# Task 2: Add API endpoint  
@during-task Add user registration endpoint
→ MCPs: encore-mcp, sequential-thinking
# Code it

# Task 3: Build UI component
@during-task Build registration form
→ MCPs: svelte, browser
# Code it

# All tasks done → Run @after-task
```

### Domain Switching

```bash
# Working on backend
@during-task Add database migration
→ Vibe: backend_vibe, MCPs: encore-mcp

# Now switching to frontend
@during-task Update UI to show new field
→ Vibe: frontend_vibe, MCPs: svelte, browser
# ✅ Vibe changed automatically!
```

---

## Token Efficiency

### Good Usage (Specific)
```
@during-task Add password validation logic      → 300 tokens ✅
@during-task Create login form component        → 300 tokens ✅
@during-task Write unit test for auth endpoint  → 300 tokens ✅
```

### Bad Usage (Too Broad)
```
@during-task Implement entire authentication feature → 2000 tokens ❌
# This should be @before-task, not @during-task!
```

---

## Rules

✅ **Call for each subtask** - Designed for frequent use  
✅ **Be specific** - "Add validation" not "implement feature"  
✅ **Skip Graphiti re-search** - Already have context from @before-task  
❌ **Don't use for discovery** - That's @before-task  
❌ **Don't call for trivial changes** - Changing a variable name doesn't need context

---

## When NOT to Call

Skip @during-task for:
- Trivial changes (typo fixes, variable renames)
- Copy-paste work (adapting existing code)
- Following exact instructions from plan.md

Use @during-task for:
- New implementation work
- Switching between domains
- Unsure which MCP to use
- Implementing complex logic

---

## Comparison

```
Without @during-task:
  → Implement blindly
  → Use wrong MCP
  → Waste time

With @during-task:
  → Quick guidance (300 tokens)
  → Right MCP immediately
  → Stay on track
```

**300 tokens to avoid 30 minutes of wrong direction = 100x ROI.**

---

**Purpose**: Provide lightweight, frequent check-ins during implementation without burning tokens on redundant searches.
