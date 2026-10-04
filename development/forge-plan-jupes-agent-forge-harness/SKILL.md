---
name: forge-plan
description: Phase 2 of the Forge pipeline. Turn a research document into an implementation plan that is built around Beads issues and TDD. Reads plans/research/<slug>.md, designs the build, sets up red-green-refactor test strategy using the tdd skill, materializes a Beads epic/feature/tasks with dependencies and priorities, and defines demo/test checkpoints. Use when starting /forge-plan or the plan step of /forgemaster.
---

# forge-plan

Phase 2 of 4 in the Forge pipeline (research → **plan** → implement → ship). Input is the research
document from [[forge-research]]; output is `plans/drafts/<slug>.md` plus a Beads issue graph.

The plan is **not** just a file — it is a Beads-tracked, TDD-shaped build sequence with explicit
points where the user can see the work running.

## When to Use

- The user runs `/forge-plan <slug>` or `/forgemaster` enters its plan phase.
- A `plans/research/<slug>.md` exists (or the user wants to plan a researched feature).

## Prerequisites

```bash
bun run forge:phase-gate plan --slug <slug>     # verifies research artifact exists
cat plans/research/<slug>.md                    # the source of truth for this plan
```

If no research document exists, stop and tell the user to run `/forge-research <slug>` first.
Do not invent research.

## Process

### 1. Absorb the research

Read `plans/research/<slug>.md` end to end. The plan must be consistent with its decisions,
constraints, and non-goals. If you find a contradiction, surface it instead of silently diverging.

### 2. Set up TDD for the feature

Read and follow the TDD skill at `.claude/skills/tdd/SKILL.md` (see also its `tests.md`,
`interface-design.md`, `deep-modules.md`). Apply its discipline to **this** feature:

- **List behaviors to test**, not implementation steps — phrase each as a specification
  ("user can save settings and they survive a refresh").
- Design the **public interface** for testability (small interface, deep implementation).
- Plan **vertical slices**: one failing test → minimal code → repeat. Reject horizontal slicing
  (all tests first, then all code).
- Mark the **tracer-bullet** behavior: the first end-to-end test that proves the path works.
- Name the test files that will hold these behaviors, adjacent to source (`*.test.ts`).

Capture this as the plan's Test Strategy section (below).

### 3. Design the build sequence with demo checkpoints

Break the work into ordered steps. Group steps into **checkpoints** — points where something is
runnable and observable. Each checkpoint must name a concrete command or action the user can run to
*see* progress (a test, a dev server route, a CLI invocation). Mark a checkpoint
`(no live demo)` only when the work genuinely has no observable surface yet.

### 4. Write the plan document

Write to `plans/drafts/<slug>.md` (matches the existing `/plan` convention):

```markdown
# Plan: <slug> — <feature title>
Generated: <date>
Repo: <repo>
Phase: plan (2/4) — from plans/research/<slug>.md

## Summary
<~100 tokens: what is being built, why, the approach>

## Existing Code to Reuse
- `path` — <how it is reused> (from research)

## TDD Strategy (red-green-refactor)
Following .claude/skills/tdd. Behaviors are tested through public interfaces, vertically.

| # | Behavior (as a spec) | Test file | Tracer? |
|---|----------------------|-----------|---------|
| 1 | <observable behavior> | `x.test.ts` | yes |
| 2 | <observable behavior> | `x.test.ts` | no |

Refactor watch-list (after green): <duplication / deep-module opportunities>.

## Build Sequence & Checkpoints
### Checkpoint A — <name>
Steps:
1. <step> — `path` — <change>
2. <step> — `path` — <change>
Demo: `bun test path/x.test.ts` (or `bun run dev` → /route) — user sees <observable result>.

### Checkpoint B — <name>
...
Demo: `(no live demo)` — internal refactor, verified by tests only.

## Files to Create / Modify
| File | Create/Modify | Purpose |
|------|---------------|---------|

## Validation Commands
\`\`\`bash
bun run typecheck
bun test <paths>
\`\`\`

## Beads Issue Map
| Beads ID | Type | Title | Depends on | Priority |
|----------|------|-------|-----------|----------|

## Estimated Scope
- Files: <n new / n modified>; Complexity: Low|Medium|High; Checkpoints: <n>
```

### 5. Plan review loop

Before creating Beads issues, run a review-plan feedback loop to catch false premises early.
Spawn a `review-plan` sub-agent (Agent tool, `subagent_type: "Explore"`, prompt:
`"Review plans/drafts/<slug>.md using the review-plan skill"`). Loop up to **2 turns**; stop
early when the verdict is **SOUND** (zero Blocker + High + Medium findings).

```
turn = 0
loop:
  1. Spawn Agent (review-plan skill) → returns verdict + findings by severity
  2. Log: bd comments add <feature-id> "review: plan <VERDICT> — <#B>/<#H>/<#M>/<#L>"
  3. If SOUND (no Blocker/High/Medium):  break — plan is clean
  4. turn += 1
  5. If turn >= 2:  break — maximum turns reached
  6. Address every Blocker, High, and Medium finding by editing plans/drafts/<slug>.md
     Log: bd comments add <feature-id> "worklog: plan revised after review turn <turn> — <summary>"
  7. Continue loop
```

After the loop, tell the user the final verdict and turn count (e.g. "SOUND after 1 review" or
"NEEDS REVISION — 2 review turns exhausted"). If Medium+ findings remain after 2 turns, surface
them explicitly so the user can decide whether to address them before implementing.

### 6. Materialize Beads

Create the issue graph that the implement phase will execute. Set **`--priority` on every issue**
using `.claude/skills/beads-priority-assignment/SKILL.md` (see [[beads-priority-assignment]]).

```bash
# One feature (or epic) to group the work
bd create --json --repo <repo> --type feature --title "<feature title>" --priority <p> \
  --description "<summary>" --acceptance "<top-level acceptance criteria>"

# One task per checkpoint (or per behavior for fine-grained TDD)
bd create --json --repo <repo> --type task --title "<checkpoint/behavior>" --priority <p> \
  --acceptance "<the test(s) that prove this done>"

# Sequential dependencies between checkpoints
bd dep add <later-id> --requires <earlier-id>
```

Prefer **one task per checkpoint** so each closed task maps to something the user saw run.
Record every created id back into the plan's Beads Issue Map and the forge state.

If Beads/Dolt is unavailable (`bd` errors), note it in the plan under a `## Beads` heading,
list the issues that *should* exist, and continue — do not block planning.

### 7. Approve & hand off

Present the plan summary (scope, checkpoints, Beads created) and ask the user to approve.
On approval, advance the forge state:

```bash
bun run forge:phase-gate plan --slug <slug> --write
```

Then point to the next phase: `/forge-implement <slug>` (or `/forgemaster` continues).

## Exit Criteria

- [ ] `plans/drafts/<slug>.md` exists with TDD Strategy and Checkpoints filled.
- [ ] Each checkpoint names a demo command or is explicitly `(no live demo)`.
- [ ] Plan review loop ran: SOUND verdict reached, or 2 turns completed; outcome logged to Beads.
- [ ] Any remaining Medium+ findings (after 2 turns) surfaced to user before proceeding.
- [ ] Beads issues created (or their absence noted with reason) and mapped in the plan.
- [ ] User approved the plan; forge state advanced to `plan` complete.
