---
name: task-breakdown
description: "Decomposes a spec or architecture into buildable tasks with acceptance criteria, dependencies, and implementation order for AI agents or engineers. Produces `.agents/tasks.md`. Not for clarifying unclear requirements (use discover) or designing architecture (use system-architecture). For code quality checks after building, see review-chain. For packaging and PRs, see ship."
argument-hint: "[spec or architecture to decompose]"
allowed-tools: Read Grep Glob Bash
license: MIT
metadata:
  author: hungv47
  version: "2.0.0"
  budget: standard
  estimated-cost: "$0.15-0.50"
promptSignals:
  phrases:
    - "break this down"
    - "task list"
    - "acceptance criteria"
    - "sprint planning"
    - "work breakdown"
    - "decompose this"
  allOf:
    - [break, down, tasks]
  anyOf:
    - "tasks"
    - "breakdown"
    - "acceptance criteria"
    - "sprint"
    - "dependencies"
  noneOf:
    - "code review"
    - "documentation"
  minScore: 6
routing:
  intent-tags:
    - task-decomposition
    - dependency-mapping
    - acceptance-criteria
    - sprint-planning
    - work-breakdown
  position: pipeline
  produces:
    - tasks.md
  consumes:
    - system-architecture.md
    - spec.md
    - product/flow/*.md  # reads every flow file in the directory
  requires: []
  defers-to:
    - skill: discover
      when: "requirements are unclear, need to clarify first"
    - skill: system-architecture
      when: "architecture undefined, need technical design first"
  parallel-with: []
  interactive: false
  estimated-complexity: medium
---

# Task Breakdown — Orchestrator

*Productivity — Multi-agent orchestration. Break architecture into executable tasks and build them one at a time with AI agents.*

**Core Question:** "Can an engineer pick up any single task and ship it independently?"

## Inputs Required
- Architecture document, feature spec, or problem description to decompose
- Target scope (MVP, full feature, spike)

## Output
- `.agents/tasks.md`

## Chain Position
Previous: `system-architecture`, `discover`, or conversation context | Next: task execution (Phase 2)

**Re-run triggers:** When architecture changes after initial breakdown, when scope mode changes (e.g., full → minimal), or when tasks consistently fail acceptance criteria (indicates decomposition issues).

## Context Resolution

Task-breakdown works from whatever context is available. It does NOT require artifacts on disk — conversation context from the current session is equally valid.

**Resolution order:**
1. **Conversation context** — if discover or system-architecture ran in this session, their decisions are in context
2. **Artifacts on disk** — `architecture/system-architecture.md`, `.agents/spec.md`, every `.agents/product/flow/*.md`
3. **Defer to discover** — if neither exists, recommend running `/discover` first. Do not conduct your own interview — clarification is discover's job.

If artifacts exist but their `date` fields are older than 30 days, recommend re-running the source skill. Tip: `/navigate status` gives a single-pass freshness report across all upstream artifacts.

---

## Multi-Agent Architecture

### Agent Roster

| Agent | File | Focus |
|-------|------|-------|
| decomposer-agent | `agents/decomposer-agent.md` | Splits features into atomic, right-sized tasks |
| dependency-mapper-agent | `agents/dependency-mapper-agent.md` | Maps dependency graph, finds hidden dependencies |
| ordering-agent | `agents/ordering-agent.md` | Merges tasks + deps into risk-first ordered list |
| acceptance-agent | `agents/acceptance-agent.md` | Writes precise, verifiable acceptance criteria |
| critic-agent | `agents/critic-agent.md` | Quality gate review, sizing check, coverage trace |

### Execution Layers

```
Layer 1 (parallel):
  decomposer-agent ────────┐
  dependency-mapper-agent ──┘── run simultaneously

Layer 2 (sequential):
  ordering-agent ──────────── merges task list + dependency graph
    → acceptance-agent ────── writes criteria for ordered tasks
      → critic-agent ─────── final quality review
```

### Dispatch Protocol

1. **Confirm scope mode** — ask the user: "Are we decomposing everything (FULL), building exactly what's spec'd (LOCKED), or cutting to minimum (MINIMAL)?" Default to LOCKED if finished spec provided, MINIMAL if MVP mentioned.
2. **Extract durable decisions** — before decomposing, identify and list the architectural decisions that every task will reference: route structures, database schema shape, key data models, auth approach, third-party service boundaries, deployment target. Write these as a "Shared Context" header in the task artifact so every task can reference them without repeating or diverging. If system-architecture.md exists, extract from there. If not, extract from conversation context.
3. **Layer 1 dispatch** — send brief + scope mode + shared context to `decomposer-agent` and `dependency-mapper-agent` in parallel.
4. **Layer 2 sequential chain** — pass both outputs to `ordering-agent`, then ordered list to `acceptance-agent`, then complete breakdown to `critic-agent`.
5. **Revision loop** — if critic returns FAIL, re-dispatch affected agents with feedback. Maximum 2 rounds.
6. **Assembly** — merge into the task artifact format. Every task block gets a seeded `**History:**` entry (`{{today}} · task-breakdown · created`) so the audit trail has an origin. Save to `.agents/tasks.md`.

### Routing Rules

| Condition | Route |
|-----------|-------|
| Scope mode MINIMAL | decomposer-agent actively cuts features before decomposing |
| Scope mode FULL | decomposer-agent captures everything; defer cuts to after |
| Scope mode LOCKED | decomposer-agent follows spec exactly; flags gaps but doesn't add |
| Critic PASS | Assemble and deliver |
| Critic FAIL | Re-dispatch cited agents with feedback |
| Revision round > 2 | Deliver with critic's remaining issues noted |

---

## Critical Gates

Before delivering, the critic-agent verifies ALL of these pass:

- [ ] Every task has exactly ONE acceptance test
- [ ] No task depends on something not yet defined
- [ ] Risky/uncertain work is front-loaded
- [ ] All external config is in Prerequisites, not buried in tasks
- [ ] A junior dev could verify each acceptance criterion
- [ ] No task requires unstated knowledge to complete
- [ ] Tasks are vertical slices (each delivers a testable increment through all layers). Horizontal-only tasks require explicit justification.

**If any gate fails:** the critic identifies which agent must fix it and the orchestrator re-dispatches with specific feedback.

---

## Single-Agent Fallback

When context window is constrained or the decomposition is simple (fewer than 10 tasks expected):

1. Skip multi-agent dispatch
2. Confirm scope mode with the user
3. Decompose using the Task Format and Sizing Rules below
4. Map dependencies inline
5. Order risk-first
6. Write acceptance criteria for each task
7. Run the Critical Gates checklist as self-review
8. Save to `.agents/tasks.md`

---

## Scope Modes

| Mode | When | Behavior |
|------|------|----------|
| **FULL SCOPE** | Discovery, greenfield, "what would it take?" | Capture everything — defer cuts to after decomposition |
| **LOCKED SCOPE** | Spec is final, ready to build | Decompose exactly what's written — flag gaps but don't add |
| **MINIMAL SCOPE** | Too much on the plate, need an MVP | Actively cut before decomposing — ask "can we ship without this?" for each feature |

Default to LOCKED SCOPE if the user provides a finished spec. Default to MINIMAL SCOPE if the user mentions MVP, prototype, or time pressure.

---

## Task Format

Every task gets a **stable ID** (`T1`, `T2`, `T3`...) assigned at creation and **never renumbered**. Inserting a task later uses the next free number (e.g., `T8` even if it belongs between `T3` and `T4`). Removed tasks keep their ID with `Status: removed` — don't delete the block, so dependents fail loudly instead of silently mis-pointing.

**Index ordering:** Rows in the Status Index are ordered by **execution order**, not ID. When inserting `T8` logically between `T3` and `T4`, place the T8 row between them. IDs never move; rows do.

### File Layout

The artifact opens with a **status index table** — a single skim surface so a resuming agent finds the next task in one read, without scanning every block. The index is the source of truth for status; task blocks carry the detail. Both must stay in sync — whenever a task's `Status` flips, update its row in the index in the same edit.

```markdown
---
skill: task-breakdown
version: 1
date: {{today}}
status: draft
---

# Tasks

## Status Index

| ID | Title | Status | Depends on | Updated |
|----|-------|--------|------------|---------|
| T1 | Scaffold Next.js + Supabase | done | — | 2026-04-21 · agent-implementer |
| T2 | Auth: signup + login | in_progress | T1 | 2026-04-21 · agent-implementer |
| T3 | Tasks table + RLS | pending | T1 | 2026-04-21 · task-breakdown |
| T4 | Create-task form | pending | T2, T3 | 2026-04-21 · task-breakdown |
| T5 | Email notification | blocked | T4 | 2026-04-21 · agent-implementer |

## Shared Context

[Architectural decisions every task references — extracted in Dispatch Protocol step 2]

## Tasks

### Task T[N]: [Title]

**Status:** pending
**Updated:** {{today}} · task-breakdown
**Evidence:** —

**Depends on:** [Task IDs this requires, e.g. "T1, T3", or "None"]

**Outcome:** [What exists when done - one sentence]

**Why:** [What this unblocks]

**Acceptance:** [How to verify - specific test, expected result]

**Autonomy:** AFK | HITL
**Why HITL:** [only if HITL — what specific judgment is needed]

**Human action:** [External setup needed, if any]

**History:**
- {{today}} · task-breakdown · created
```

Each task is a `###` block under the `## Tasks` container. Siblings, not nested. Agents anchor on `### Task T[N]:` to jump from index row to task block.

Every task block carries a seeded `**History:**` entry at creation time (`{{today}} · task-breakdown · created`). This guarantees the audit trail has an origin — Update/Remove/Reopen entries append below it.

### Status field

| Value | Meaning |
|-------|---------|
| `pending` | Not started. Default at creation. |
| `in_progress` | An agent has picked it up. Set agent name in `Updated`. |
| `done` | Acceptance passed. `Evidence` must cite commit SHA or test result. |
| `blocked` | Can't proceed. `Evidence` states the blocker. |
| `removed` | No longer needed. Block stays so dependent tasks surface breakage. |

**Transition rules:**
- Only flip `pending → in_progress` if every task in `Depends on` is `done`.
- Flipping to `done` or `blocked` requires a non-empty `Evidence` line (commit SHA, test pass, artifact path, or blocker description). No evidence → not done and not blocked.
- `blocked` and `removed` are terminal until reopened — see Reopen Protocol.

**Who may make each transition:**

| Transition | Who | Notes |
|------------|-----|-------|
| `pending → in_progress` | Agent | Only if deps are all `done` |
| `in_progress → done` | Agent | Requires non-empty `Evidence` |
| `in_progress → blocked` | Agent | `Evidence` states the blocker |
| stale `in_progress → pending` | Agent | Per Resume Protocol step 3 only — with staleness check |
| `done → pending` | Human (via Reopen) | Never agent-initiated |
| `blocked → pending` | Human (via Reopen) | Never agent-initiated |
| `removed → pending` | Human (via Reopen) | Never agent-initiated |
| `* → removed` | Human | Via Remove Protocol |
| `done → in_progress` directly | **Never** | Always Reopen to `pending` first |

Always bump `Updated:` with the current date and `· {agent/user identity}` in the same format used in the Status Index (`YYYY-MM-DD · {actor}`).

### Sizing Rules

Right size:
- Changes ONE testable thing
- 5-30 min agent implementation time
- Failure cause is obvious and isolated

Split if:
- Multiple independent things to test
- Multiple files for different reasons
- Acceptance has multiple unrelated conditions

### Autonomy Classification

Every task gets an **Autonomy** label:

| Label | Meaning | When to use |
|-------|---------|-------------|
| **AFK** | Agent can execute end-to-end without human judgment | Deterministic tasks: scaffolding, CRUD, tests, migrations with clear schema |
| **HITL** | Needs human judgment during execution | Taste decisions, external approvals, ambiguous acceptance criteria, security-sensitive changes |

**Default to AFK.** Only mark HITL when the task genuinely requires a judgment call that the agent can't make from the spec alone. Every HITL task must state *what specific judgment* is needed — "needs review" is not sufficient.

**Why this matters:** Orchestrators (navigate, multi-agent systems) use this to batch-run AFK tasks autonomously and queue HITL tasks for user attention. Mislabeling AFK as HITL wastes the user's time. Mislabeling HITL as AFK risks wrong decisions.

### Content Rules

**Outcomes, not implementation.**

Bad: "Create users table with id, email, created_at using Prisma"
Good: "Database stores user records with unique emails and timestamps"

**Risk-first ordering.**
Put uncertain/complex tasks early. Fail fast on hard problems.

**Dependencies explicit.**
Every task lists what it needs. Enables parallel work and failure impact analysis.

---

## Phase 2: Task Execution

### Before Starting

1. Read architecture doc fully
2. Read task list fully — Status Index first, then Shared Context, then individual task blocks
3. Understand the end state before writing code
4. If anything is ambiguous, ask — assumptions cause rework.

### Resume Protocol (agent picking up an existing task list)

Any agent (including a fresh session with no prior context) uses this exact sequence to determine what to work on:

1. **Read the Status Index table** in execution order, top to bottom. Do not scan task blocks yet.
2. **Find the first row where:** `Status: pending` AND every ID in `Depends on` has `Status: done` in the index. This is the next task.
3. **If none exists**, check for `Status: in_progress` rows:
   - If the `Updated` attribution is *you* (same agent, same session) → continue it.
   - If the attribution is a different agent, apply the staleness check below. If stale → flip back to `pending` with a note in `Updated`, then restart step 2.
   - Otherwise → do not touch it. Stop and surface to the user ("T2 is claimed by agent-X, updated {date}").
4. **If all tasks are `done` or `removed`** → report completion and stop.
5. **If only `blocked` tasks remain** → surface the blockers to the user. Do not silently skip them.
6. **Claim the task:** flip `Status: pending → in_progress`, set `Updated:` to today + your agent identity, in both the index row and the task block. Commit this status change **before** starting work so concurrent agents see the claim (see Concurrency Model below).
7. Execute Per-Task Protocol below.
8. **On completion:** flip `Status: in_progress → done`, fill `Evidence:` with commit SHA or test output, update the index row. Then loop back to step 1 for the next task.

**Never flip a status without updating both the index and the task block in the same edit.** They are the same fact written twice — drift breaks resume.

#### Staleness check (for step 3 claim reclamation)

Do **not** reclaim a task just because its timestamp is old. A HITL task legitimately claimed by a human reviewer may sit for a day. Only reclaim if **both** of these are true:

- Time since `Updated` exceeds the task's expected window: **2 hours for AFK**, **24 hours for HITL**.
- **No commits by the claiming agent** appear in `git log --author` (or the relevant VCS history) within that window.

If either check fails, assume the agent is legitimately working — do not steal. When in doubt, stop and surface to the user.

#### Concurrency model

Markdown-as-coordination is **best-effort, not a lock**. Two agents reading the file simultaneously can both decide `T3` is next and both write `in_progress` — last write wins.

**Safe patterns:**
- **Serial execution** (default): only one agent works the list at a time. Simplest and covers 90% of real use.
- **Shared git remote**: before claiming, `git pull --rebase`. Write the claim. `git commit && git push`. If push fails due to conflict, pull and restart Resume Protocol from step 1.
- **Shared filesystem without git**: not safe without an external lock. Run agents serially.

If you discover mid-work that your claim was overwritten (your `Updated` attribution is gone from the task block), **abort current work** and restart Resume Protocol from step 1.

### Per-Task Protocol

1. State which task you're starting (by ID, e.g. "Starting T3"). Note the task's current `Revision:` number if present.
2. Write minimum code to pass acceptance.
3. **Before committing work**, re-read the task block. Abort current work and restart Resume Protocol if any of:
   (a) `Revision:` bumped since you claimed — spec changed mid-flight,
   (b) `Status` flipped back to `pending` — PM unclaimed the task,
   (c) your agent identity is no longer in `Updated:` — another agent overwrote your claim.
   On abort, re-read the new Acceptance before re-claiming.
4. State exactly what to test and expected result.
5. **AFK tasks:** Run the acceptance test. Pass → write `Evidence`, flip to `done`, commit, move to next task without waiting. Fail → fix and re-test (max 2 attempts, then flip to `blocked` with reason and flag to user).
6. **HITL tasks:** Stop and present the result. Wait for user confirmation. Pass → write `Evidence`, flip to `done`, commit, announce next task. Fail → fix the specific issue only, don't expand scope.

### Coding Rules

**Do:**
- Write absolute minimum code required
- Focus only on current task
- Keep code modular and testable
- Preserve existing functionality

**Avoid — these cause scope creep and breakage:**
- Sweeping changes across unrelated files
- Touching unrelated code
- Refactoring unless the task requires it
- Adding features not in the current task
- Premature optimization

**When human action is needed:**
- State exactly what to do and which file/value to update
- Wait for confirmation before continuing

### When Stuck

0. It is better to stop and say "I'm stuck — here's what I've tried" than to keep attempting fixes that aren't working. Bad work is worse than no work.
1. State what's blocking
2. Propose smallest modification to unblock
3. Wait for approval

### Scope Change Protocol

If you discover a missing requirement:

1. Stop current task
2. State what's missing and why it's needed
3. Propose where it fits in task order
4. Wait for PM to update task list
5. Resume only after task list is updated

### Update / Remove / Reopen Protocol

The task file is **append-only for history**. Never silently overwrite acceptance criteria or delete a task block — future agents need to see what changed. Every mutation lands as a new line in a `**History:**` block at the bottom of the task, with date + actor + one-line reason.

**Update** (acceptance, outcome, or dependencies changed while task is still open):

1. Bump `**Revision:**` counter on the task block (add the field if absent; start at `2` on first revision).
2. Rewrite the changed field in place (e.g., replace `Acceptance:` with the new test).
3. Append to `**History:**` below the task: `- 2026-04-21 · user · revision 2: tightened acceptance to require RLS test, not just row creation.`
4. If `Status` was `in_progress`, flip it back to `pending` — the in-flight work is now against a stale spec. Agent must re-claim.

**Remove** (task is no longer needed):

1. Flip `Status: removed` in both the index and the task block.
2. Keep the block — do not delete. Dependents (`T7 depends on T4`) must continue to resolve IDs.
3. Append to `**History:**`: `- 2026-04-21 · user · removed: superseded by T9 (unified auth flow).`
4. **Check downstream**: any task with this ID in `Depends on` needs review. Flag them in the response, don't auto-rewrite their deps. For any downstream task already `in_progress` or `done` at removal time, call it out explicitly — the in-flight or completed work may need reopening.

**Reopen** (a `done`, `blocked`, or `removed` task needs to run again):

1. Flip `Status` back to `pending` (or directly to `in_progress` if claiming immediately).
2. Clear `Evidence:` to `—` (the old evidence no longer proves the current spec).
3. Append to `**History:**`: `- 2026-04-21 · user · reopened: production bug in T5's email template, re-running task.`
4. Update the index row to match.

**Example task block after one revision + one reopen:**

```markdown
### Task T5: Email notification on task create

**Status:** pending
**Updated:** 2026-04-21 · user
**Evidence:** —
**Revision:** 2

**Depends on:** T4
**Outcome:** User receives email within 30s of creating a task
**Acceptance:** Create a task via UI → Resend webhook fires → email lands in inbox → template renders task title
**Autonomy:** AFK

**History:**
- 2026-04-19 · task-breakdown · created
- 2026-04-20 · agent-implementer · done (commit abc1234, test passed)
- 2026-04-21 · user · revision 2: added template rendering check; reopened due to prod bug
```

**Never do this:**
- Delete a task block (breaks dependency resolution)
- Edit `Evidence` on a `done` task without reopening first (destroys the audit trail)
- Renumber IDs to "tidy up" (invalidates every `Depends on` reference)

---

## Anti-Patterns

| Anti-Pattern | Problem | INSTEAD |
|--------------|---------|---------|
| "Build the auth system" | 5+ tasks disguised as one | decomposer-agent splits into registration, login, middleware, reset, verification |
| "Create the Button component" | Not independently testable | Combine with click handling and visual states |
| Hidden dependency | Task 8 needs API key not mentioned until Task 8 | dependency-mapper-agent surfaces it; goes in Prerequisites |
| "User flow works correctly" | Vague acceptance — means different things to everyone | acceptance-agent writes specific action + input + expected result |
| Implementation-as-outcome | "Use Redux for state management" dictates HOW | decomposer-agent writes WHAT: "User data fetches efficiently with caching" |
| Saving integrations for the end | Integration issues discovered late cause the most rework | ordering-agent front-loads risky integration work |

---

## Worked Example

**User:** "Break down a Todo app with Supabase auth and email notifications."

**Orchestrator confirms:** LOCKED SCOPE (spec is clear).

**Layer 1 dispatch (parallel):**
- `decomposer-agent` → produces 7 tasks assigned stable IDs T1–T7: scaffold (T1), signup (T2), login + protected routes (T3), tasks table + RLS (T4), create task (T5), email notification (T6), end-to-end test (T7)
- `dependency-mapper-agent` → fan-out from T1 (T2, T3, T4 parallel), fan-in at T5 (needs T2, T3, T4), hidden dep: Resend API key missing from prerequisites

**Layer 2 chain:**
- `ordering-agent` → merges: moves Resend API key to Prerequisites, orders risk-first (auth before CRUD), identifies parallelism (T2 and T4 can run simultaneously once T1 is done)
- `acceptance-agent` → writes T2 acceptance: "Submit signup form → user appears in Supabase Auth → confirmation email sent"
- `critic-agent` → PASS, all gates pass

**First-run artifact (all pending, saved to `.agents/tasks.md`):**

```markdown
## Status Index

| ID | Title | Status | Depends on | Updated |
|----|-------|--------|------------|---------|
| T1 | Scaffold Next.js + Supabase | pending | — | 2026-04-21 · task-breakdown |
| T2 | Auth: signup | pending | T1 | 2026-04-21 · task-breakdown |
| T3 | Auth: login + protected routes | pending | T1 | 2026-04-21 · task-breakdown |
| T4 | Tasks table + RLS | pending | T1 | 2026-04-21 · task-breakdown |
| T5 | Create task | pending | T2, T3, T4 | 2026-04-21 · task-breakdown |
| T6 | Email notification | pending | T5 | 2026-04-21 · task-breakdown |
| T7 | End-to-end test | pending | T5, T6 | 2026-04-21 · task-breakdown |
```

A fresh agent opening this file runs Resume Protocol: Status Index → first pending with all deps done → **T1**. Claims it, executes, flips to `done` with evidence, moves to T2 or T4 (both unblocked once T1 lands).

---

## PM Feedback Format

When reporting test results, always use the stable task ID:

```
Task T[N]: PASS | FAIL | BLOCKED

[If FAIL]: What broke, error message, steps to reproduce
[If BLOCKED]: What's preventing test
```

---

## Artifact Template

Save to `.agents/tasks.md` using the Task Format above.

**Re-run behavior** depends on what changed:

- **Additive refinement** (new tasks discovered, acceptance tightened, dependencies adjusted): **edit in place** using the Update / Remove / Reopen protocols. Stable IDs persist, `History:` blocks accumulate, the Status Index is updated row-by-row. This is the default — multi-agent resume depends on it.
- **Full re-decomposition** (architecture changed significantly, scope pivoted, the old breakdown no longer maps to current reality): **snapshot** the existing file as `tasks.v[N].md` (incremented), then write a fresh `tasks.md` from scratch. Confirm with the user before snapshotting — they lose live status and in-flight claims.

Default to additive refinement. Only snapshot when the user confirms the old plan is discarded.

---

## Next Step

Tasks are ready. Begin implementation of the first unblocked task. Run `review-chain` after each major task completion. Run `ship` when all tasks are done.

## References

- [references/sizing-examples.md](references/sizing-examples.md) — Right-sized vs wrong-sized tasks with split/combine guidance
- [references/dependency-patterns.md](references/dependency-patterns.md) — Common dependency patterns, visualization, and hidden dependency detection
- [references/acceptance-criteria.md](references/acceptance-criteria.md) — Acceptance criteria templates by task type
