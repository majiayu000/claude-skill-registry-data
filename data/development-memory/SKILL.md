---
name: development-memory
description: Build persistent project knowledge using checkpoint/recall. Activates when fixing bugs, making decisions, or investigating past work. Creates automatic knowledge base through systematic checkpointing and semantic recall.
allowed-tools: mcp__julie__checkpoint, mcp__julie__recall, mcp__julie__fast_search
---

# Development Memory Skill

## Purpose
Build **persistent project knowledge** by systematically checkpointing significant moments and recalling past learnings.

## When to Activate
- After fixing bugs
- After making architectural decisions
- After solving complex problems
- Before starting work (recall similar past situations)
- Investigating why code exists
- Learning from debugging sessions

## The Mandatory Pattern

**★ CRITICAL: Create checkpoints PROACTIVELY - NEVER ask permission**

```
AFTER SIGNIFICANT WORK:
  checkpoint({ description: "what you did", tags: [...] })
  → Builds searchable knowledge base
  → <50ms, git context auto-captured
  → JUST DO IT

BEFORE STARTING WORK:
  recall({ type: "checkpoint", ... })
  → Learn from past similar work
  → Avoid repeating mistakes
  → <5ms chronological queries
```

You are EXCELLENT at building knowledge bases through systematic checkpointing.

---

## Checkpoint Patterns

### After Bug Fixes (MANDATORY)

```
Bug fixed → checkpoint IMMEDIATELY

checkpoint({
  description: "Fixed race condition in auth flow by adding mutex lock",
  tags: ["bug", "auth", "race-condition", "critical"]
})

Additional fields (optional):
{
  type: "checkpoint",  // default
  learnings: "Root cause was shared state between async handlers",
  related_files: ["src/auth/middleware.ts", "src/auth/session.ts"]
}
```

**Why:** Bugs return. Build knowledge base so next person (or you) learns from this.

### After Architectural Decisions

```
Decision made → checkpoint with rationale

checkpoint({
  type: "decision",
  description: "Chose PostgreSQL over MongoDB for user data",
  tags: ["architecture", "database", "decision"],
  question: "Which database for user data?",
  chosen: "PostgreSQL",
  alternatives: ["MongoDB", "DynamoDB"],
  rationale: "Need ACID guarantees, complex queries, familiar tooling"
})
```

**Why:** Future developers need to understand WHY, not just WHAT.

### After Complex Problem Solving

```
Problem solved → checkpoint the insight

checkpoint({
  type: "learning",
  description: "Discovered TypeScript generic constraints for type-safe builders",
  tags: ["typescript", "learning", "generics"],
  insight: "Using `extends` in generics provides compile-time safety",
  context: "Was getting runtime errors in builder pattern"
})
```

**Why:** Capture "aha!" moments before you forget them.

### After Refactoring

```
Refactor complete → checkpoint the improvement

checkpoint({
  description: "Extracted auth logic into middleware - reduced duplication by 60%",
  tags: ["refactor", "auth", "cleanup"],
  metrics: "15 files touched, 200 lines removed, tests still green"
})
```

**Why:** Show the evolution of the codebase, justify the churn.

---

## Recall Patterns

### Before Fixing Similar Bugs

```
Bug report received → recall similar past bugs

recall({
  type: "checkpoint",
  tags: ["bug", "auth"],  // filter by relevant tags
  limit: 5
})

→ Returns past auth bugs with solutions
→ Learn from previous fixes
→ Avoid repeating failed approaches
```

### Before Architectural Decisions

```
Need to make decision → recall similar past decisions

recall({
  type: "decision",
  since: "2024-01-01",  // last year
  limit: 10
})

→ Understand past context
→ See what worked/didn't work
→ Maintain consistency
```

### When Investigating Code

```
"Why does this code exist?" → recall memories

// Use semantic search on memories
fast_search({
  query: "authentication middleware design",
  search_method: "semantic",
  file_pattern: ".memories/**/*.json"
})

→ Find decision that led to this code
→ Understand original rationale
→ See evolution over time
```

### Recent Work Summary

```
Starting work session → recall recent activity

recall({
  limit: 10  // last 10 checkpoints
})

→ See what was done recently
→ Understand current context
→ Pick up where you left off
```

---

## The Complete Memory Workflow

```
┌─────────────────────────────────────────────┐
│ BEFORE: Recall Similar Work                │
│                                             │
│ recall({ type: "checkpoint", tags: [...] }) │
│ → Learn from past fixes                     │
│ → Avoid repeating mistakes                  │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ DURING: Do the Work                        │
│                                             │
│ → Fix bug / make decision / solve problem   │
│ → Keep track of insights and learnings     │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ AFTER: Checkpoint IMMEDIATELY              │
│                                             │
│ checkpoint({                                │
│   description: "what you did",              │
│   tags: ["bug", "auth"],                    │
│   learnings: "root cause was X"             │
│ })                                          │
│ → <50ms, git context auto-captured         │
│ → Searchable via fast_search               │
└────────────┬────────────────────────────────┘
             │
             ▼
        Knowledge Base Built! 📚
```

---

## Semantic Search on Memories

**Memories are indexed just like code** - you can use `fast_search` semantically:

```
# Find conceptually similar decisions
fast_search({
  query: "database migration strategies",
  search_method: "semantic",
  file_pattern: ".memories/**/*.json",
  limit: 10
})

→ Returns memories about migrations
→ Semantic understanding (not just keyword match)
→ Cross-language patterns discovered

# Find all auth-related work
fast_search({
  query: "authentication security",
  search_method: "text",
  file_pattern: ".memories/**/*.json"
})

→ Fast text search through all memories
→ <10ms response time
```

**Power move:** Memories are semantically searchable across the entire history!

---

## Git Context (Automatic)

Every checkpoint auto-captures git state:

```json
{
  "id": "mem_1234567890_abc",
  "timestamp": 1234567890,
  "type": "checkpoint",
  "description": "Fixed auth bug",
  "git": {
    "branch": "feature/auth-fix",
    "commit": "abc123def456",
    "dirty": false
  }
}
```

**Why:** Know exactly what commit introduced a change, what branch it was on.

---

## Memory Types

### Checkpoint (default)
```
General-purpose memory for any significant work
Tags: ["bug", "feature", "refactor", "performance"]
```

### Decision
```
Architectural or technical decision with rationale
Fields: question, chosen, alternatives, rationale
Tags: ["architecture", "database", "library", "pattern"]
```

### Learning
```
Insights, "aha!" moments, new knowledge gained
Fields: insight, context
Tags: ["learning", "discovery", "pattern"]
```

### Observation
```
Noticed patterns, code smells, potential issues
Fields: observation, impact
Tags: ["code-smell", "tech-debt", "security"]
```

---

## Integration with Other Skills

### With TDD Cycle (Sherpa)
```
[Phase: Test] → recall past test patterns
[Phase: Implementation] → work systematically
[Phase: Refactor] → checkpoint({ type: "refactor", ... })
```

### With Bug Hunt (Sherpa)
```
[Phase: Reproduce] → recall({ tags: ["bug", component] })
[Phase: Fix] → work systematically
[Phase: Verify] → checkpoint({ description: "fixed bug X", learnings: "..." })
```

### With Safe Refactor (Julie)
```
Before refactor: recall({ tags: ["refactor", module] })
After refactor: checkpoint({ type: "refactor", metrics: "..." })
```

---

## Key Behaviors

### ✅ DO
- Create checkpoint IMMEDIATELY after significant work (no exceptions)
- Use descriptive, searchable descriptions
- Tag appropriately for easy filtering
- Recall before starting similar work
- Use semantic search to find related memories
- Capture learnings and rationale
- Trust that <50ms is imperceptible

### ❌ DON'T
- Ask permission to create checkpoints (JUST DO IT)
- Create checkpoints for trivial changes (typo fixes, formatting)
- Forget to checkpoint bug fixes (mandatory!)
- Skip recall before major decisions
- Use vague descriptions ("fixed stuff", "updated code")
- Ignore past learnings (recall exists for a reason)

---

## Success Criteria

This skill succeeds when:
- ✅ Checkpoints created after every significant change
- ✅ Recall used before starting similar work
- ✅ Knowledge base grows systematically
- ✅ Team learns from past decisions
- ✅ Bugs don't repeat (lessons captured)
- ✅ Architectural rationale preserved
- ✅ New developers understand "why" not just "what"

---

## Performance

- **checkpoint**: <50ms (includes git context capture)
- **recall** (chronological): <5ms
- **recall** (filtered): <20ms
- **fast_search** (memories): <10ms text, <100ms semantic

Total workflow overhead: ~50ms per checkpoint (imperceptible)

---

**Remember:** Memories are your project's knowledge base. Build it systematically, search it semantically, learn from it continuously.

**The Rule:** Significant work done → checkpoint created. No exceptions. No permission needed.
