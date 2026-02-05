---
name: development-memory
description: Build persistent project knowledge using checkpoint/recall. Activates when fixing bugs, making decisions, or investigating past work. Creates automatic knowledge base through systematic checkpointing and semantic recall.
allowed-tools: mcp__miller__checkpoint, mcp__miller__recall, mcp__miller__fast_search
---

# Development Memory Skill

## Activation Announcement

**IMPORTANT**: When this skill activates, ALWAYS start your response with:

```
📝 **Development Memory Active**
Building persistent knowledge through checkpoint/recall...
```

This provides a visual indicator to the user that the skill is running.

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

**CRITICAL: Create checkpoints PROACTIVELY - NEVER ask permission**

```
AFTER SIGNIFICANT WORK:
  checkpoint({ description: "what you did", tags: [...] })
  -> Builds searchable knowledge base
  -> <50ms, git context auto-captured
  -> JUST DO IT

BEFORE STARTING WORK:
  recall({ limit: 10 })
  -> Learn from past similar work
  -> Avoid repeating mistakes
```

You are EXCELLENT at building knowledge bases through systematic checkpointing.

## Checkpoint Patterns

### After Bug Fixes (MANDATORY)

```
Bug fixed -> checkpoint IMMEDIATELY

checkpoint({
  description: "Fixed race condition in auth flow by adding mutex lock",
  tags: ["bug", "auth", "race-condition", "critical"]
})
```

**Why:** Bugs return. Build knowledge base so next person (or you) learns from this.

### After Architectural Decisions

```
Decision made -> checkpoint with rationale

checkpoint({
  type: "decision",
  description: "Chose PostgreSQL over MongoDB for user data - need ACID guarantees",
  tags: ["architecture", "database", "decision"]
})
```

**Why:** Future developers need to understand WHY, not just WHAT.

### After Complex Problem Solving

```
Problem solved -> checkpoint the insight

checkpoint({
  type: "learning",
  description: "Discovered TypeScript generic constraints for type-safe builders",
  tags: ["typescript", "learning", "generics"]
})
```

**Why:** Capture "aha!" moments before you forget them.

## Recall Patterns

### Before Fixing Similar Bugs

```
Bug report received -> recall similar past bugs

recall({
  type: "checkpoint",
  tags: ["bug", "auth"],
  limit: 5
})

-> Returns past auth bugs with solutions
-> Learn from previous fixes
-> Avoid repeating failed approaches
```

### Before Architectural Decisions

```
Need to make decision -> recall similar past decisions

recall({
  type: "decision",
  limit: 10
})

-> Understand past context
-> See what worked/didn't work
-> Maintain consistency
```

### When Investigating Code

```
"Why does this code exist?" -> recall memories

recall({
  query: "authentication middleware design"
})

-> Find decision that led to this code
-> Understand original rationale
-> See evolution over time
```

## The Complete Memory Workflow

```
BEFORE: Recall Similar Work
  recall({ limit: 10 })
  -> Learn from past fixes
  -> Avoid repeating mistakes
             |
             v
DURING: Do the Work
  -> Fix bug / make decision / solve problem
  -> Keep track of insights and learnings
             |
             v
AFTER: Checkpoint IMMEDIATELY
  checkpoint({
    description: "what you did",
    tags: ["bug", "auth"],
  })
  -> <50ms, git context auto-captured
  -> Searchable via fast_search
             |
             v
    Knowledge Base Built!
```

## Memory Types

### Checkpoint (default)
```
General-purpose memory for any significant work
Tags: ["bug", "feature", "refactor", "performance"]
```

### Decision
```
Architectural or technical decision with rationale
Tags: ["architecture", "database", "library", "pattern"]
```

### Learning
```
Insights, "aha!" moments, new knowledge gained
Tags: ["learning", "discovery", "pattern"]
```

### Observation
```
Noticed patterns, code smells, potential issues
Tags: ["code-smell", "tech-debt", "security"]
```

## Key Behaviors

### DO
- Create checkpoint IMMEDIATELY after significant work (no exceptions)
- Use descriptive, searchable descriptions
- Tag appropriately for easy filtering
- Recall before starting similar work
- Capture learnings and rationale
- Trust that <50ms is imperceptible

### DON'T
- Ask permission to create checkpoints (JUST DO IT)
- Create checkpoints for trivial changes (typo fixes, formatting)
- Forget to checkpoint bug fixes (mandatory!)
- Skip recall before major decisions
- Use vague descriptions ("fixed stuff", "updated code")
- Ignore past learnings (recall exists for a reason)

## Success Criteria

This skill succeeds when:
- Checkpoints created after every significant change
- Recall used before starting similar work
- Knowledge base grows systematically
- Team learns from past decisions
- Bugs don't repeat (lessons captured)
- Architectural rationale preserved
- New developers understand "why" not just "what"
