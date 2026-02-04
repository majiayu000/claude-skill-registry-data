---
name: defining-spikes
description: Create spike definitions with canonical names and numbered approaches for parallel exploratory implementation. Use when partner has an underdefined feature idea and wants to explore multiple implementation approaches in parallel, when uncertain which technical approach is best, or when comparing alternatives before committing to implementation
---

# Defining Spikes

## Overview

Transform underdefined feature requests into structured spike definitions that multiple agents can execute in parallel, each exploring a different approach.

**Core principle**: Define once, execute many times. The definition creates a contract for parallel exploration.

**Announce at start**: "I'm using the Defining Spikes skill to create a spike definition."

## What is a Spike Definition?

A spike definition is NOT implementation. It's a structured exploration plan containing:
- Clear goal and success criteria
- Canonical identifier for branches/files
- 2-3 genuinely different approaches to try
- Git infrastructure for parallel execution

**You are defining what to explore, not exploring it yourself.**

## The Process

Copy this checklist to track progress:

```
Defining Spikes Progress:
- [ ] Phase 1: Understanding Desired Outcome (goal and success criteria gathered)
- [ ] Phase 2: Implementation Constraints (must-haves/must-nots identified or skipped)
- [ ] Phase 3: Choose Canonical Name (kebab-case identifier confirmed with partner)
- [ ] Phase 4: Generate Approaches (2-3 genuinely different approaches listed)
- [ ] Phase 5: Create Spike Infrastructure (branch, notes file committed)
```

### Phase 1: Understanding Desired Outcome (Mandatory - ONE round)

Ask 1-4 questions focused on WHAT, not HOW:

**Ask about**:
- What problem are we solving?
- What does success look like?
- What constraints exist (backwards compatibility, performance, security)?
- How will we know we're done?

**Don NOT ask about**:
- Which library to use
- How to architect it
- Implementation details
- Specific technical approaches

**One round only.** Get enough to understand the goal, then move forward.

### Phase 2: Implementation Constraints (Optional - ONE round if needed)

Only ask if there are unclear must-haves or must-nots:
- "Must use existing auth system"
- "Can't add new dependencies"
- "Must support IE11"

**If partner didn't mention constraints, assume none.** Move to Phase 3.

### Phase 3: Choose Canonical Name

Create short kebab-case identifier. Examples:
- `replace-3d-vectors`
- `add-graphql-api`
- `improve-test-perf`
- `migrate-to-postgres`

Ask partner to confirm the name. This name will be used for all branches and files.

### Phase 4: Generate Approaches

List 2-3 numbered, high-level approaches that are genuinely different.

**Genuinely different means**:
- Different strategies, not just different libraries
- Different architectural patterns
- Different scope or migration paths

**Examples**:

✅ **Good - Genuinely Different**:
```
1. Incremental migration with parallel APIs
2. Gateway/facade pattern wrapping existing system
3. Full rewrite with shared business logic
```

❌ **Bad - Too Similar**:
```
1. Use date-fns library
2. Use Day.js library
3. Use Luxon library
```
(These are all "adopt a library" - same strategy)

**If no obvious different approaches exist, say so**:
```
Approaches:
- Only one obvious approach: [describe it]
```

### Phase 5: Create Spike Infrastructure

1. **Create branch**: `spike-[canonical-name]`
2. **Determine spike notes location** (use bash `test -d docs` to check):
   - If `docs/` directory exists: create `docs/spike-notes-[canonical-name].md`
   - If `docs/` does not exist: use AskUserQuestion tool to ask partner:
     - Option 1: Create `docs/` directory and use it
     - Option 2: Write `spike-notes-[canonical-name].md` to project root

   **DO NOT**:
   - Create alternative directories like `.spikes/`, `spikes/`, etc.
   - Create subdirectories like `docs/spikes/`
   - Invent custom organization structures
   - Use symlinks or other indirection

   **Use ONLY** `docs/` (if exists or created) OR project root.

3. **Create file**: `spike-notes-[canonical-name].md` (in determined location) with this structure:

```markdown
# Spike: [Canonical Name]

## Goal
[What we're trying to achieve]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Constraints
[Must-haves and must-nots, or "None"]

## Approaches

### Approach 1: [Name]
[High-level description]

### Approach 2: [Name]
[High-level description]

### Approach 3: [Name]
[High-level description - if applicable]

## Effort Limit
[e.g., "~2-3 hours of exploration per approach"]

## Notes
[Any additional context]
```

4. **Commit spike notes** to the spike branch
5. **Tell partner**: "Spike defined. Ready to execute with branches like `spike-[canonical-name]-1`, `spike-[canonical-name]-2`, etc."

## Red Flags - STOP and Reconsider

- **Planning implementation details** → You're executing, not defining
- **Creating WIP branch to start coding** → You're executing, not defining
- **Creating custom spike directories** (`.spikes/`, `spikes/`, etc.) → Use docs/ or project root only
- **Asking many rounds of questions** → Limit to 2 rounds max
- **"I need more information before I can start"** → Start with what you have
- **"20 minutes isn't enough time"** → Time pressure is not an excuse to skip steps
- **Accepting vague success criteria** → Pin down "what does done look like?"

**All of these mean: You're not following the defining-spikes process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too open-ended to define" | That's what spikes are for - reducing ambiguity |
| "I need to explore the codebase first" | That's execution, not definition |
| "This is too simple for multiple approaches" | Then say so explicitly - don't assume |
| "Time pressure - skip the git setup" | Git infrastructure is mandatory, even under pressure |
| "Let me just implement it" | You're defining, not executing |

## When NOT to Use This Skill

**Don't use for**:
- Well-defined features (use writing-plans instead)
- Questions that don't need exploration (just answer them)
- Single obvious approach (may not need a spike at all)

**Ask partner**: "This seems well-defined. Do you actually want a spike, or should we plan the implementation directly?"

## After Definition Complete

Your job is done. Partner will either:
- Execute spikes themselves
- Spawn multiple agents to execute approaches in parallel
- Decide a spike isn't needed after seeing the definition

**Do NOT start implementing.** Definition and execution are separate roles.

## Remember

- 2 rounds of questions maximum
- Focus on WHAT, not HOW
- Get canonical name approval
- Generate genuinely different approaches (or note if only one exists)
- Create git infrastructure (branch + committed notes file)
- Pin down success criteria
- Then STOP - don't implement
