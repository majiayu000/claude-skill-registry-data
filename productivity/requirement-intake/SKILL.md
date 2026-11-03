---
name: requirement-intake
description: Turns an untagged task on the board — a paragraph of intent — into an approved, executable plan before any code is written. Covers the workflow/ scratch folder, the questions protocol, sizing, and what must be exported before a task can finish. Use when a board task has no [tag], or when asked how requirements become plans.
---

# Requirement Intake

A tagged task (`[backend] Add /health endpoint with test`) means you already did
the requirement engineering — it goes straight to the task-workflow skill.

An **untagged** task is a requirement. It gets a requirement engineer first.

```
- [ ] TASK-31 Reply digest for operator — status: todo
      Operator gets a daily email digest of new replies grouped by niche.
      Link each reply to the business detail page.
```

Title on the line, description indented. That is the only thing a human writes.

## One pen

**The human writes in `tasks.md` and nowhere else.** They may read anything.

Everything an agent produces goes in `workflow/` — a gitignored scratch folder at
the repo root. Two surfaces, one owner each, no ambiguity about who wrote what.

```
<repo root>/
  tasks.md              human writes here. git-tracked. short. the index.
  workflow/             agents write here. gitignored. verbose. the working memory.
    .env                knobs (self-created on first run)
    TASK-31-reply-digest/
      state.md  plan.md  assumptions.md  questions.md
      review-1.md  review-2.md  backlog.md
```

### workflow/ is organised by slice, never by file type

One task = one folder = every artifact for that task, together.

```
✗ workflow/plans/   workflow/reviews/   workflow/state/     grouping by file type
✗ workflow/backend/ workflow/frontend/                      grouping by agent
✓ workflow/TASK-31-reply-digest/                            grouping by task
```

The second one matters: a requirement usually spans modules and agents, so it has
no home module. The task is the slice.

### Bootstrap (first run, idempotent)

1. `workflow/` missing → create it.
2. `/workflow/` missing from `.gitignore` → append it. Never rewrite the rest of
   the file.
3. `workflow/.env` missing → write it with these defaults and comments:

```ini
# task-agent workflow knobs. Per developer, gitignored.
PLAN_GATE=medium          # never | small | medium | always — sizes that need your approval
AUTO_MERGE=off            # off | gated  (gated conditions are in the task-workflow skill)
MERGE_TARGET=develop
MAX_REVIEW_ROUNDS=3       # reviewer FAIL -> fix -> re-review, this many times, then blocked
MAX_FIX_CYCLES=2          # gate failures fed back to the implementer per round
NOTIFY=osascript          # osascript | print | <shell command taking the message as $1>
```

Unreadable, missing, or unparseable `.env` → use these defaults with
**`AUTO_MERGE=off`**. The one irreversible action always fails closed.

## The intake phases

Intake is **one phase**: a run sets `status: planning`, runs the requirement
engineer, and does not stop until the task has landed on its next human gate or
gone straight to implementation. `planning` is a crash marker, never a resting
place — a task found sitting in `planning` had its run interrupted, and the next
run restarts the phase.

| board status | what runs | next |
|---|---|---|
| `todo` (untagged) | create `workflow/<TASK-id>-<slug>/` + `state.md`, set `planning`, run the **task-requirement-engineer** agent: understand → validate → feasibility → size → plan | `needs-answer`, `plan-review`, or `doing` |
| `needs-answer` | **the human** answers on the board, then writes `answered: yes` | re-run this phase with the answers |
| `plan-review` | **the human** writes `approved: yes` on the board | `doing` |
| `doing` and after | the **task-workflow** skill takes over unchanged | — |

Both human gates behave identically: the loop skips the task entirely until the
confirming line is present. Neither ever times out into a guess.

`PLAN_GATE` decides whether `plan-review` happens at all:

| `PLAN_GATE` | plans you approve |
|---|---|
| `always` | every plan |
| `medium` *(default)* | MEDIUM and LARGE. SMALL is auto-approved. |
| `small` | SMALL only (unusual; for trusting the RE on big work but not small) |
| `never` | none — fully hands off |

A skipped gate is not a skipped plan. `plan.md` is still written, still linked
from the board, still the implementer's contract, and still reviewed as part of
the PR.

A gate the knob skips is recorded as an approval, not as an absence of one:

```
      plan: workflow/TASK-31-reply-digest/plan.md  (SMALL · 1 slice)
      approved: yes (auto — PLAN_GATE=medium, size SMALL)
```

The board still reads `status: plan-review`, so the next run picks it up through
the ordinary claim rule and nothing special-cases the bypass. You can also see, six
months later, that no human ever read that plan.

## The questions protocol

RE questions go **on the board**, short, with a stated default. The human answers
in place. Long-form context stays in `workflow/<folder>/questions.md`.

```
- [ ] TASK-31 Reply digest for operator — status: needs-answer
      Operator gets a daily email digest of new replies grouped by niche.
      workflow: TASK-31-reply-digest
      Q1: One email with niche sections, or one email per niche? (default: one email)
      A1:
      Q2: Include replies from suppressed businesses? (default: no)
      A2:
      answered:
```

- Max five questions. One line each. **Every question names its default**, so the
  human can accept the lot without typing an answer.
- `needs-answer` is human-gated. A driver skips the task until the human writes
  `answered: yes` — same shape as `approved: yes`, same meaning: your turn is
  over. A loop ticking every few minutes must never answer its own questions.
- On resume: `A<n>: <anything>` wins and goes into `plan.md` verbatim. An `A<n>`
  the human left empty means **use the stated default** — record it in
  `assumptions.md` and continue. Answer the two that matter, ignore the rest.

## Handing the plan back to the board

When RE finishes, the dispatcher writes to the board (RE never touches `tasks.md`):

1. **Add the tag** from `plan.md`'s `## Agent` section — the line stops being
   untagged, and every downstream rule works as it always has.
2. **Add the pointer**: `workflow: TASK-31-reply-digest`.
3. **Add the plan line**: `plan: workflow/TASK-31-reply-digest/plan.md  (MEDIUM · 2 slices · 1 migration)`.
4. **Set the status** per `PLAN_GATE`.

```
- [ ] TASK-31 [backend] Reply digest for operator — status: plan-review
      Operator gets a daily email digest of new replies grouped by niche.
      workflow: TASK-31-reply-digest
      plan: workflow/TASK-31-reply-digest/plan.md  (MEDIUM · 2 slices · 1 migration)
      approved:
```

### When the work is bigger than one sitting

RE writes proposed child lines to `workflow/<folder>/tasks.md`. The dispatcher
appends them to the board with real ids and `depends:` lines, then closes the
parent:

```
- [x] TASK-31 Reply digest for operator — status: done
      decomposed into TASK-32, TASK-33
- [ ] TASK-32 [backend] Build digest query + BuildDigestService with tests — status: todo
      plan: workflow/TASK-31-reply-digest/plan.md
- [ ] TASK-33 [backend] Schedule SendDigestJob daily 07:00 with tests — status: todo
      depends: TASK-32
      plan: workflow/TASK-31-reply-digest/plan.md
```

Children are tagged, so they skip intake entirely and share the parent's plan.

## The export rule

`workflow/` is gitignored. Anything that must outlive the task has to leave it
before the task can reach `done`:

| must land in | what |
|---|---|
| the PR body | the original requirement text, the plan, and the assumptions |
| `tasks/architecture.md` | `architecture-delta.md` applied — LARGE only, inside the worktree |
| `tasks/system_model.md` | `system-model-delta.md` applied — LARGE only, inside the worktree |
| the project's manual test cases | updated whenever operator-visible behavior changed |
| `docs/conventions.md` or `CLAUDE.md` | only if the task established a new project rule |

**A task must not be set to `done` while a durable artifact exists only inside
`workflow/`.** That single rule is what makes gitignoring the folder safe.

## Absolute paths in worktrees

`workflow/` is gitignored, so **it does not exist inside a task worktree**. An
implementation agent running in `../<repo>-worktrees/TASK-31` that reads
`workflow/TASK-31-reply-digest/plan.md` finds nothing — and will happily invent a
plan instead of failing.

Every prompt handed to an implementation or review agent passes the plan by
**absolute path**:

```
/Users/you/code/my-store/workflow/TASK-31-reply-digest/plan.md
```

Working directory is the worktree. Plan reads come from the main checkout.

## Cleanup

A task reaching `done` keeps its workflow folder until the PR is merged (the
review rounds need it). After that it is garbage. Deleting
`workflow/TASK-31-reply-digest/` costs nothing — the PR holds everything durable.
