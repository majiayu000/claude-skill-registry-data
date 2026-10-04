---
name: autopilot
description: >-
  The whole coding loop on one deliberate yes: map, spec, critic-hardened
  plan, GitHub issues, parallel worktree implementers, fresh-context review
  loops, one PR with the evidence. Acts only on its itemized charter; parks
  what it can't settle honestly. Commands: /autopilot <task> [--merge],
  resume, status. It signs a charter and pushes branches, so it never
  auto-triggers — explicit invocation only.
disable-model-invocation: true
---

# autopilot — the whole loop, one yes

`/autopilot <task>` — run the full pipeline, stop at an open PR
`/autopilot <task> --merge` — also merge, once every gate is green
`/autopilot resume <change>` — pick up a crashed, aborted, or parked run
`/autopilot status` — report runs in flight under `out/dev/`

Answer one question: **what would come back if this task were handed to a
careful team and nobody watched over their shoulder?** The other coding
skills put a human at every gate; this one replaces those gates with the
things that made them work — fresh-context review, diverse critique, and a
test suite as the arbiter — and reserves the human for exceptions. Human
*on* the loop, not *in* it: you sign once, you get a PR, and anything the
pipeline couldn't settle honestly comes back **parked**, not guessed.

## The charter — one yes, spelled out

The invocation is the consent. Echo this before running, then don't ask again:

- **WILL:** read anything in the repo; write state under `out/dev/<slug>/`;
  create GitHub issues labeled `autopilot`; create and push branches
  `autopilot/<slug>/*`; open **one** PR; comment on and close its own
  issues; with `--merge`, merge that PR once every gate is green.
- **NEVER:** push to the default branch directly, force-push, rewrite
  history, delete branches or issues it didn't create, weaken a test to get
  green, or touch anything outside this repo.

## Auto mode — how the other skills run here

Autopilot drives **map**, **feature**, and **done** in *auto mode*, a shared
convention: every approval gate becomes a self-approval **on the record** —
the decision and its reason are appended to `log.md` instead of asked — and
every verdict that would need a human becomes a **PARK**. The skills' own
rules (task sizing, TDD, tripwires, never-weaken-tests) are unchanged; only
the waiting is removed. In auto mode the run **never calls a tool that
stops to wait on a human — `AskUserQuestion` first among them** (waiting on
sub-agents or commands is fine): with nobody watching, such a call isn't a
question, it's a deadlock. A decision only a human can settle is parked
with the decision spelled out — never waited on, never guessed.

## Step 0 — Preflight

- Confirm: a git repo, a clean tree, `gh` authenticated. Without `gh`,
  degrade honestly — local task files instead of issues, stop at the branch
  instead of a PR — and say so in the run header.
- Find the test command (`AGENTS.md`, `package.json`, `Makefile`,
  `pyproject.toml`, CI config). **No test suite?** Don't refuse — schedule a
  **testing-bootstrap phase** as the plan's first wave: stand up the
  runner, then write characterization tests around exactly the code the
  plan will touch. Without an objective test to pass, every review loop
  below is just one model agreeing with another; the bootstrap fixes that.
- Open `out/dev/<slug>/log.md` with the run header: charter, stop point
  (PR / merge), test command, start commit.

## Step 1 — Orient

Run **map** in auto mode: no `AGENTS.md` → generate one; one exists → refresh
only if stale. Every downstream agent starts oriented instead of cold.

## Step 2 — Spec: interview the codebase, not the user

**feature** Step 1 with the questions turned inward — the facts-vs-decisions
split holds with no user present. Every *fact* is answered by reading code,
docs, tests, and `git log`; whatever evidence can't settle — an open
decision or an unverifiable fact — is never resolved silently: it becomes a
numbered assumption (**A1…**) in `spec.md`, visible and revisable at the
PR, where wrong assumptions are cheap to catch. The
spec remains the contract every review below is judged against.

## Step 3 — Plan, hardened by critique instead of approval

Write `plan.md` per **feature** Step 2 — 2–5-minute tasks, exact files, own
verification step, dependency order. Then replace the human approval with a
**bounded critique loop**: parallel critic sub-agents, each with a different
lens — feasibility, hidden dependencies & ordering, test coverage, scope
creep — each returning *blocking findings or an approval*. If another
model's agent CLI is installed (detect per **done** Step 2), give one critic
seat to it: fresh context varies the perspective, a different model varies
the blind spots. Fix the blocking
findings, re-run the critics once. **Two rounds maximum**: past that,
critique stops finding real problems and starts agreeing with itself. Surviving blocking
findings park the run at the plan stage — a plan the critics can't pass is
the user's call, not a coin flip.

## Step 4 — Tasks become GitHub issues

One issue per plan task, **created in dependency order** so every
`depends-on: #n` names a real number: the full briefing (a fresh agent must
be able to execute from the issue text alone), the files it touches, its
verification command, and the spec IDs it implements (`[D2, A1]`, where
one applies). Label
`autopilot`, title `[<slug>] <task name>`. Record issue numbers back into
`plan.md`. Issue prose describes **behavior, not code** — "the sync service
drops the patch", never `applyPatch()` at line 42, no file paths or line
numbers in prose; analysis artifacts cite
file:line because they're verified now, tracker artifacts must outlive the
refactor. (The files-touched list stays — it's the worker's briefing, not
durable prose.)

Local files stay canonical; the issues are the published mirror — and the
hand-off that actually reaches the workers, since the run's `out/` state is
uncommitted mid-run and invisible inside the worktrees below.

## Step 5 — Dispatch in dependency waves

- One sub-agent per task, in an **isolated git worktree**, on branch
  `autopilot/<slug>/task-<n>`, with the full task briefing in its prompt.
- Independent tasks run **concurrently**; a dependent wave starts only when
  the tasks it depends on have merged (Step 7).
- Each agent works by **feature** Step 3, verbatim: failing test first, then
  the minimal green, then a checkpoint commit — never weaken an existing
  test, no TODOs or skips as a path to green, **two failed attempts at the
  same task → stop and park**, don't grind the wall.

## Step 6 — Review loop, per task, until clean

- Fresh-context reviewers per **done** Step 2: they see only the diff, the
  task briefing, and the spec — never the implementer's conversation. A
  reviewer with no memory of writing the code has no loyalty to it.
  Spec-compliance first, correctness second, style never. That includes
  done's optional **cross-model second opinion** when a `codex`/`gemini`
  CLI is on the PATH — it earns the most here, where no human sits at any
  gate.
- Run **done**'s fake-green tripwires on every diff: tests modified or
  deleted in the diff that makes them pass, new skips, hardcoded
  expectations, TODO stand-ins.
- Findings go back to the implementer to fix, then re-review. Clean → the
  task is merge-ready. **Three rounds without clean → PARK** the task with
  the findings on the record; the rest of the run keeps flowing.
- The arbiter is the **test suite**: a reviewer's approval doesn't override
  a red suite, and a green suite doesn't excuse a spec violation.

## Step 7 — Integrate wave by wave

The orchestrator merges merge-ready task branches into
`autopilot/<slug>/main` in dependency order, running the **full suite after
every merge**. A red integration points at the merge that broke it — that
task returns to Step 6 with the failure attached; independent tasks keep
flowing. Only the orchestrator merges; workers never touch each other's
branches.

## Step 8 — Ship

1. Run **done** in auto mode on the integrated diff — the full evidence
   checklist, including *actually running the change*, with output quoted.
2. Push the integration branch; open **one PR**: the spec's summary, the
   evidence checklist, `Closes #n` for every completed issue — and parked
   tasks listed plainly, not swept.
3. Comment each issue with its outcome; parked issues stay open with the
   park reason.
4. `--merge` and every gate green → merge (never force, branch protection
   respected). Otherwise **the PR is the deliverable** — merging is yours.
5. Report in chat and `log.md`: per task — SHIPPED / AT PR / PARKED (why) —
   and where human attention is actually needed. Clean up worktrees; archive
   `out/dev/<slug>/` once merged.

## State and the escape hatch

`out/dev/<slug>/`: `spec.md`, `plan.md` (tasks + issue #s + status),
`log.md` (append-only; **the orchestrator is its only writer** — parallel
writers corrupt logs), `tasks/<n>.md`, `.work/`. Resume uses **feature**'s
ritual: log, then plan, then `git log`, then continue at the first
unfinished task — never trust residual conversation memory.

**Abort:** create `out/dev/<slug>/ABORT` (empty file) and the orchestrator
stops cleanly at the next wave boundary — worktrees intact, state saved,
`resume` picks it back up.

## Guardrails

- **The charter is the whole consent.** Nothing outside the WILL list, ever
  — scope discovered mid-run becomes a follow-up issue, not a silent
  expansion of the mandate.
- **Park, don't guess.** Ambiguity a critic loop can't settle, a task two
  attempts couldn't crack, a review three rounds couldn't clean — parked
  with the evidence, run continues. A guessed answer costs more than a
  parked task.
- **Tests are the arbiter.** No LLM verdict — critic, reviewer, or
  implementer, local model or cross — outranks the suite. No suite →
  bootstrap one before implementing.
- **Bounded loops everywhere.** Two critique rounds, two implementation
  attempts, three review rounds. Unbounded self-correction diverges or
  rubber-stamps; the bounds are what keep it honest.
- **Inherited hard rules hold.** Never weaken a test, no fake-green, scope
  contract, append-only honest logging — every rule from feature/done
  applies verbatim; autonomy removed the waiting, not the rules.
- **Honest report or no report.** Parked tasks appear in the PR body and
  the final report with reasons — a run that hides its failures has failed
  twice.
