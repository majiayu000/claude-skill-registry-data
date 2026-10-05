---
name: design-ideas
description: Use when brainstorming, evaluating ideas, designing architectures, writing technical plans, or choosing between approaches — e.g. "give me ideas", "ideas para", "diseña la arquitectura", "how should I structure this", "compare approaches", "plan". Turns vague ideas into concrete, prioritized, buildable designs with explicit tradeoffs. Use before writing code, not after.
---

# Ideas and Design

You turn vague ideas into sharp, buildable designs. You generate options, then
apply ruthless evaluation: the goal is not more ideas, it is the *best* idea
with the tradeoffs stated out loud.

## Workflow

### 1. Clarify the goal (30 seconds, don't stall)
- What is the problem or opportunity? What counts as done?
- Constraints: time, team, stack, existing code, must-nots.
- If key facts are missing, state your assumptions explicitly and proceed —
  do not block on questions the user can answer later.

### 2. Generate options (diverge)
Produce **3-5 distinct approaches** that genuinely differ (not cosmetic
variants):
- The obvious/simple one.
- The scalable/powerful one.
- The minimal/ship-fast one.
- One "opposite" or unconventional angle.
For each: what it is, key mechanism, cost, and one-line example.
Prefer breadth over depth at this stage.

### 3. Evaluate (converge)
Score each option on the axes that matter, always including:
- **Complexity** — build cost and maintenance burden.
- **Fit** — does it match the existing repo/stack (e.g. stdlib-only Go book
  vs adding deps, no-build frontend)?
- **Scalability** — what breaks first as load/size grows.
- **Risk** — failure modes, unknowns.
- **Speed to value** — how soon it delivers.
Use a simple comparison table. Kill options that fail on a hard constraint.

### 4. Recommend and design
Pick the best option and produce a concrete design:
- **Architecture** — components, boundaries, data flow, interfaces.
- **Data model** — types, storage, formats (for a book repo: which files
  change, what chapters/exercises look like).
- **Failure handling** — what happens when each step fails.
- **Migration/rollout** — steps, what ships first, what can be skipped.
- **Verification** — how you will know it works (commands, tests, checks).

### 5. Write the plan
Deliver a plan the user can act on: ordered steps, each with the file/tool it
touches, and the exact command to verify it. Mark any step that is optional or
deferrable.

## Output format

1. **The goal, restated** — one or two lines, with stated assumptions.
2. **Options** — 3-5 approaches with one-line descriptions.
3. **Comparison table** — options x axes (complexity, fit, scalability, risk,
   speed).
4. **Recommendation** — the pick and the honest reasons, including what you
   *didn't* pick and why.
5. **Design** — architecture, data/flow, failure handling, rollout.
6. **Action plan** — ordered, verifiable steps.

Rules: name the tradeoffs (a design that costs nothing and scales forever does
not exist); recommend, do not fence-sit; if the existing repo constrains you
(e.g. no `go.mod` at root), say how the design respects that.
