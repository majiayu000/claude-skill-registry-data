---
name: brainstorming
description: "Generate 2-4 distinct approaches with trade-off analysis across simplicity, flexibility, performance, effort, and risk, driving collaborative decision-making before implementation. Use when evaluating alternatives before committing to an implementation strategy. Proactively suggest when the team defaults to the first idea without exploring competitors."
allowed-tools: Read, Bash, Grep, Glob, AskUserQuestion, TaskCreate, TaskList, TaskUpdate
context: fork
agent: Explore
---

# Brainstorming

## Contract

Iron law: **explore before committing — choosing wrong costs ten times what exploring costs.** Invoked by `/flow:brainstorm` Phase 2 (GENERATE), Phase 3 (COMPARE), and Phase 4 (DECIDE), and whenever several valid approaches exist, requirements are ambiguous, or the team defaults to its first idea. Returns 2–4 genuinely distinct, implementable approaches (name, summary, pros, cons, effort, risk), a comparison table across the dimensions that matter for this decision, a recommendation with its key trade-off, and the user's choice via `AskUserQuestion`, logged to the decision journal. Permitted skips: none — the recommendation is never the decision; the user chooses.

## Process

Track five tasks — clarify goal, check existing patterns, generate approaches, compare and recommend, user decision — and confirm with `TaskList` at the end.

### 1. Clarify the goal

Confirm **what** must happen (outcome, not implementation), **why** (motivation, constraints), and **who** is affected. Ambiguous → `AskUserQuestion`; do not guess.

### 2. Check existing patterns

```bash
grep -r "relevant_pattern" --include="*.{ts,js,py,rb}" -l
git log --oneline --all --grep="related keyword" | head -10
```

Existing patterns get priority; consistency has value.

### 3. Generate 2–4 approaches

Per approach: **Name**, **Summary** (one line), **Pros**, **Cons**, **Effort** (Small/Medium/Large), **Risk** (Low/Medium/High).

Rules:
- Minimum 2, maximum 4. More than 4 is analysis paralysis — cap and decide with available information.
- Genuinely distinct, not minor variations; "we can only do A or B" usually hides a C.
- Include the "do nothing" or "simplest possible" option when applicable.
- Each must be implementable — no hand-waving.
- Present all options before discussing any, so the first does not anchor.

### 4. Compare

| Dimension | Approach A | Approach B | Approach C |
|-----------|-----------|-----------|-----------|
| Simplicity | | | |
| Flexibility | | | |
| Performance | | | |
| Consistency | | | |
| Effort | | | |
| Risk | | | |

Pick the dimensions relevant to THIS decision from these tensions: Simplicity vs Flexibility, Speed vs Correctness, Consistency vs Innovation, Build vs Buy, Coupling vs Convenience, Explicit vs Implicit.

### 5. Recommend and decide

State the recommendation with rationale and the single most important trade-off. Play devil's advocate on your own pick — what could go wrong? Then `AskUserQuestion` for the decision and log it.

## Not Reasons to Skip

"The obvious approach", "no time to brainstorm", "I've done this before" — documenting why takes minutes; rework from a wrong choice takes days. If all approaches are truly equivalent, pick the simplest and say so. If the decision is cheaply reversible (naming, formatting), pick one and move on rather than bikeshed.
