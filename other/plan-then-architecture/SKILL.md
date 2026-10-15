---
name: plan-then-architecture
description: How to plan non-trivial work in this repo — write a plan, get it torn apart by the opposite provider through Orca until you converge, then write an ASCII architecture doc a human can read in one pass. Use before writing implementation code for any change that touches more than one file or has a concurrency, contract, or data-integrity angle.
license: MIT
---

# Plan, then architecture

Two artifacts, in this order, before any implementation code:

```
   plan.md          ──► adversarial review ──► converge ──► architecture.md
   (the reasoning)      (opposite provider)     (rev N)      (the shape)
```

`plan.md` is for the decision — options, rejections, verification, risk.
`architecture.md` is for the reader — diagrams, anchors, build order.
They are not the same document and neither replaces the other.

Both go in the agent folder that `CLAUDE.md` already mandates:

```
docs/plans/<topic-in-kebab-case>/<claude|codex|cursor|human>/plan.md
docs/plans/<topic-in-kebab-case>/<claude|codex|cursor|human>/architecture.md
```

**Scope.** This skill covers the *pre-implementation* phase. The post-commit
opposite-provider code review is a different process —
[`docs/development/agent-workflow.md`](../../../docs/development/agent-workflow.md).
Run this one first; nothing here commits code.

---

## Phase 1 — write the plan

Read the code before you write a word of it. `karpathy-guidelines` applies: the
ladder shortens the solution, never the reading.

A plan is done when it has all of these:

1. **What is actually broken**, split into numbered defects, each anchored to real
   `file.py:line`. Grep the anchors fresh immediately before writing — anchors drift,
   and a wrong line number is worse than no line number because it looks verified.
2. **The fix**, as one sentence of intent plus one named change per defect.
3. **Deliberately not building** — every item with the reason AND *what would change
   my mind*. A plan without this section will get rejected for scope.
4. **Steps and verification** — every step carries the check that fails if the step
   is wrong. Name the actual test file. Name the existing tests your change breaks;
   there are almost always some.
5. **Risk register** — one row per way this goes wrong, each with its mitigation and
   the step that proves it.
6. **Review rounds** — empty at first; Phase 3 fills it.

Mark the status at the top: `PLAN` / `IN PROGRESS` / `BUILT`, plus `rev N`.

### Claims that will get you rejected

- "No code path can do X" — check every path first, including the `-y` flag on the
  ffmpeg call and the fallback branch nobody uses.
- "No skill/pipeline depends on this" — grep `skills/pipelines/**`, not just
  `.agents/skills/*/SKILL.md`. Pipeline directors pass tool arguments you are about
  to delete.
- "This is atomic" — say which lock, held from where to where, and in what order
  relative to every other lock.
- "Duration == sum of parts" — not once a transition, xfade, or speed change exists.

---

## Phase 2 — adversarial review by the opposite provider

Claude-authored plan → Codex reviews. Codex-authored → Claude reviews. Never review
your own plan.

This is **supervised orchestration**, not a handoff: you wait for findings and you
iterate. Load the current command surface first — never guess flags:

```bash
orca skills get orchestration
```

Then the loop. Substitute your resolved Orca executable for `orca`:

```bash
orca orchestration run-create --objective "<topic>: converge plan with reviewer" --json
orca orchestration task-create --spec "<the review brief, see below>" --json

# Custom model/effort needs the low-level path: worker-start cannot pass -m/-c.
orca terminal create --worktree current --title "PLAN REVIEW" \
  --command "codex --model gpt-5.6-sol -c model_reasoning_effort=high \
             -s workspace-write -c sandbox_workspace_write.network_access=true -a never" --json
orca terminal wait --terminal <handle> --for tui-idle --timeout-ms 120000 --json
orca orchestration dispatch --task <task_id> --to <handle> --inject --json

orca orchestration check --wait --types worker_done,escalation,question,status \
  --timeout-ms 540000 --json
orca orchestration check --ack <delivery_id> --json
```

### Three gotchas that cost real time

**1. Never launch the reviewer with `-s read-only`.** Its sandbox blocks the local
socket the Orca CLI needs, so `worker_done` fails with "Could not connect to the
running Orca app" *after* the review is finished and the findings are stranded in a
session you then have to resume. Use `workspace-write` + `network_access=true` and
enforce read-only **by instruction** ("change no repo file"). Verify afterwards:

```bash
git -c core.bare=false --work-tree=. --git-dir=.git status --porcelain
```

Plain `git status` fails in these worktrees (`core.bare = true` in the shared config).

**2. Tell the reviewer to pass the body as a literal.** Codex will otherwise write
`--body "$ORCA_BODY"`, the variable is unset, and you receive a `worker_done` with a
subject and an empty body. Put this in the brief verbatim:

> Pass the worker_done body as a LITERAL single-quoted string, never a shell
> variable. If it is too long for one command, send the findings as two or three
> `--type status` messages first, then a final `worker_done` with the verdict.

**3. A `check --wait` timeout is a checkpoint, not a failure.** Reviews run 6–15
minutes at high effort. Keep rolling the wait. Read progress with
`orca terminal read --terminal <handle> --json` (the tail is spinner-polluted; strip
it) — but only to check liveness, never as a substitute for the reported findings.

### The review brief

Ask for findings you can act on, not an opinion:

- verify **every** `file:line` in the plan against the code; report drift
- take a position on each named design decision: ACCEPT or REJECT **with a concrete
  failure case** (inputs/state → wrong outcome), not a preference
- hunt what the plan missed — name the areas: other writers of the same artifact,
  other readers, concurrency between two entry points, cache keys, resume/retry
  paths, contracts in `skills/pipelines/**`, tests that break
- judge scope against `karpathy-guidelines`: what is over-built, and is anything in
  "Deliberately not building" actually required to close the ticket
- output: `SEVERITY (BLOCKER|MAJOR|MINOR|NIT) - claim - file:line - failure case -
  suggested change`, then a `VERDICT` line
- read-only; change no repo files; expect follow-up rounds

---

## Phase 3 — converge

**Verify every finding against the code before you accept it.** Reviewers are
sometimes right about the defect and wrong about the cause. Two rounds of this on
one plan produced: five confirmed blockers, one correct-but-misattributed diagnosis,
and one reversal of a change the same reviewer had asked for.

For each round:

1. Re-read the cited code. Confirm or refute.
2. Accept, partially accept, or push back **with a reason** — a judgement call is
   not a defect, and saying so is allowed. Reviewers will concede.
3. Apply the change to the plan, bump `rev N`.
4. Record it in `## Review rounds` — a table of finding → resolution. This is the
   audit trail a human reads to see the plan got harder, not just longer.
5. Send the revision back with an explicit map of *which change went where*, and
   name anything you did **not** do and why. New task, new `dispatch --inject` to
   the same terminal so the reviewer keeps its context.

Converged means the reviewer says APPROVE, or APPROVE WITH CHANGES where every
remaining item is a wording nit you then apply. Do not implement before that.

Expect 3–5 rounds on anything touching concurrency or a data contract. A plan
approved on round 1 usually means the brief was too soft.

---

## Phase 4 — architecture.md

Now write the doc a human reads in one pass. Load `explain-with-ascii` and follow it.
The rules that matter most here:

- **78 columns, hard cap**, inside fenced ` ```text ` blocks. Check it, don't eyeball
  it:

  ```bash
  python3 - <<'PY'
  p='docs/plans/<topic>/<agent>/architecture.md'
  inb=False
  for i,l in enumerate(open(p),1):
      if l.startswith('```'): inb = not inb; continue
      s=l.rstrip('\n')
      if inb and len(s)>78: print(f"{i}: {len(s)} cols")
  PY
  ```

  Box-drawing characters are multi-byte, so `awk 'length>78'` lies. Count characters.
  Also check that every line of a box shares one width.

- **Two diagrams carry the whole doc:** *today*, with `★ DIVERGENCE` callouts naming
  the exact lines where paths split, and *after*, with the entries funnelling into
  one component and an explicit convergence bar:

  ```
  ═════════ ALL THREE ROUTES CONVERGE HERE — one publisher ═════════
  ```

  The funnel *is* the claim. If your fix has no funnel, say what shape it does have.

- **Show resolved values, not just calls** — `→ true`, `→ renders/final.mp4`.
- **Failure edges inline** — `invalid → success=False, NO job`. A happy-path diagram
  hides what the implementer will actually hit.
- **A timeline diagram wherever ordering is the design** (crash windows, lock
  windows, commit markers). Ordering arguments are unreadable as prose.

Then, for the agent who implements it:

- a **surface table**: `file:line` → what changes, one row each, plus a short list of
  what is deliberately untouched
- a **build order**, dependency-first, ending in the end-to-end check
- **two or three observations** the diagrams make obvious and prose would bury. Name
  a consequence ("the whole bug is upstream of the renderer"), never a summary.

Link back to `plan.md` for reasoning; do not restate it.

---

## Done

- [ ] `plan.md` has all six sections; every anchor grepped fresh
- [ ] reviewer is the opposite provider and reported through Orca (`task-list` shows
      the tasks `completed`)
- [ ] every finding verified against code, then accepted or refuted in writing
- [ ] `## Review rounds` records each round and its resolutions
- [ ] reviewer's verdict is APPROVE
- [ ] `architecture.md` passes the 78-column and box-width checks
- [ ] reviewer terminal closed; `git status` (with the `core.bare` override) shows
      only `docs/plans/` touched
- [ ] no implementation code written

Implementation starts after this, and goes through
[`docs/development/agent-workflow.md`](../../../docs/development/agent-workflow.md)
for the commit-time review.

## Worked example

`docs/plans/opn-30-edit-decisions-render-desync/claude/` — five review rounds, three
REJECTs, one reversal, `plan.md` §6 has the full round table and `architecture.md`
has the before/after funnel.
