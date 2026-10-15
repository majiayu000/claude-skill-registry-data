---
name: "speckit-auto"
description: "Run the entire spec-driven cycle end-to-end and autonomously: constitution check, specify, org context, clarify, plan, checklist, tasks, analyze, tests, implement, converge, harden, review, archive and the hand-off of a ready PR to a tail agent — resolving every interactive gate itself and committing each implementation slice."
argument-hint: "Describe the feature to build end-to-end"
compatibility: "Requires spec-kit project structure with .specify/, the gates in .claude/hooks, and a clean working tree"
metadata:
  author: "blastradius (ported from speckit-demo)"
  source: "project-local — autonomous pipeline"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). The text
the user typed after `/speckit-auto` **is** the feature description — pass it
through to every phase that takes a description. Do not ask the user to repeat
it; if it is empty, that is the one preflight failure that stops the run.

## Goal

Take a feature description from nothing to reviewed, tested, committed
implementation in a single turn, running every Spec Kit phase in order without
returning to the user between phases.

This command does not reimplement the phases. Each phase is the existing skill,
invoked through the Skill tool with the same description as `args`. This file
adds two things the individual skills do not have: the run order, and an
autonomous answer for every gate that would otherwise wait for a human.

This file is loaded on every turn, so it holds only the run order, the
contract, the run state and the stops. Each step's detail sits beside it, read
once when the run reaches it:

| File | Read |
|---|---|
| `preflight.md` | before phase 1 |
| `phases-plan.md` | phases 1–8 |
| `phases-build.md` | phases 9–12 |
| `phases-close.md` | phases 13–17 |
| `commit-protocol.md` | before the first commit |
| `hand-off.md` | after phase 17 |
| `tail.md` | the session holding the wait, and the tail agent |
| `report.md` | at the hand-off, before the reply |

## Autonomy Contract

This is the whole point of the command — read it before phase 1.

1. **Never wait for the user.** Every gate inside a phase skill that says
   "STOP and ask", "wait for user response", or "present one question at a
   time" is answered by you, in-line, using that skill's own stated
   recommendation. You do not emit the question and stop; you record the
   question, its answer, and the reason in the run log (`preflight.md` creates it).
2. **The recommendation is the answer.** Where a phase computes a
   `**Recommended:** Option X` or `**Suggested:** <answer>`, that is the
   answer. Where it computes none, pick the option that best fits the
   constitution (`.specify/memory/constitution.md`, Principle I first) and
   this repo's real code — `package.json`, `nx.json`, `biome.jsonc`,
   `jest.config.ts`, the touched workspace — and say which evidence decided
   it.
3. **Assumptions are written down, not held in memory.** Every autonomous
   answer lands in the artifact the phase owns (spec Clarifications /
   Assumptions, plan Technical Context, tasks notes) *and* as one line in the
   run log `specs/<feature>/auto-run.md`.
4. **Hook prompts are yes.** `.specify/extensions.yml` runs with
   `auto_execute_hooks: true` and its git hooks ask things like "Commit
   specification changes?". In this command the answer is always yes — subject
   to `commit-protocol.md`, which is where you will find that most
   artifact phases have nothing to commit at all.
5. **A blocked tool call is an instruction, not a question.** The gates in
   `.claude/hooks/` (`red-first-gate.mjs`, `bash-guard.mjs`,
   `pre-commit-check.sh`) and `.husky/pre-commit` block by design. Do what the
   block says — run `/speckit-tests`, drop the forbidden command, fix the
   failing test — and continue. Never surface a hook block to the user as a
   decision, and never weaken a test, `.skip` it, rename a file, or downgrade
   a commit type to slip past a gate.
6. **Finish the run.** No phase ends with "next I'll…". The turn ends with the
   final report of a completed pipeline, or with one of the Hard Stops.

## Phases

Run in this order. Each phase: invoke the skill, apply the gate override,
verify, commit if there is anything committable, append to the run log,
continue.

**Phase agents.** A skill's `model:` pin is not applied when the skill runs
in this run's own turn, so phases 2, 5, 6 and 7 (pins below Opus, the run's
model) each run as their own agent: `subagent_type: task-runner`, `model` set
to the pin named in the subsection (the call's `model` overrides the definition's),
`run_in_background: false` (the next phase reads its artifact). Its prompt
names the worktree (every Bash starts `cd <worktree> &&`), the feature
directory, the branch and draft PR, the skill and its `args`, that phase's
gate overrides from its subsection, and the reply envelope with "at most 10
lines":

```
STATUS: success | failure | blocked | partial — <one line: what happened>
PR: #<n> <draft|ready|merged> <sha7> | none
NEXT: <the one action the caller should take> | none
FILES: <paths written, comma-separated> | none
```

The phase's hooks run inside the agent with the same yes answers. Read its
`STATUS:` line: `success` continues; `failure` or `blocked` is the phase
failing, handled as the inline phase's failure would be, never as a pass;
`partial` passes only when `FILES` names the phase's artifact and what failed
was a tracker or mock write. No retry. If the Agent call itself errors, run the
phase inline and log a pin miss in `auto-run.md`. The phase's run-log entry
records the agent's model and its `STATUS:` line.

Two groups need no output from each other, so run them at once:

- Phase 3 starts in the background as soon as phase 2 has written the spec
  (the `org-researcher` agent with `run_in_background`), beside phase 4's
  `spec-challenger`. Phase 4 answers its questions only once `context.md`
  exists.
- Phases 13, 15 and 16 run beside phase 14's reviewers: none of them reads
  the review. Fixes from phase 14 that change code rerun phase 15 only if
  they changed what it records.

| # | Phase | Skill | Gate override | Detail |
|---|-------|-------|---------------|--------|
| 0 | Size | `speckit-size` | Choose a level; record it before anything else | `SKILL.md` |
| 1 | Constitution | *(read only)* | Verify, do not rewrite | `phases-plan.md` |
| 2 | Specify | `speckit-specify` | Self-answer the clarification table | `phases-plan.md` |
| 3 | Org context | `speckit-context` | Overwrite freely; a dead connector is not a stop | `phases-plan.md` |
| 4 | Clarify | `speckit-clarify` | Self-answer all ≤5 questions | `phases-plan.md` |
| 5 | Plan | `speckit-plan` | none (no interactive gate) | `phases-plan.md` |
| 6 | Checklist | `speckit-checklist` | Drive to 0 unchecked items | `phases-plan.md` |
| 7 | Tasks | `speckit-tasks` | none | `phases-plan.md` |
| 8 | Analyze | `speckit-analyze` | Apply remediation without asking | `phases-plan.md` |
| 9 | Tests | `speckit-tests` | Prove red before implementing | `phases-build.md` |
| 10 | Implement | `speckit-implement` | Skip the checklist STOP gate | `phases-build.md` |
| 11 | Converge | `speckit-converge` | Loop back into 9–10 for new work | `phases-build.md` |
| 12 | Harden | `speckit-harden` | Fix every ERROR; never suppress one | `phases-build.md` |
| 13 | Ticket refresh | `speckit-context --since` | An empty refresh is a pass | `phases-close.md` |
| 14 | Review | `spec-reviewer` subagent | CRITICAL/HIGH block completion | `phases-close.md` |
| 15 | Agent context | `context-audit.mjs` (the plan pointer is derived, not written) | The file may shrink, never grow | `phases-close.md` |
| 16 | Retrospective evidence | *(scripts, read-only)* | Gather it; the verdict stays the user's | `phases-close.md` |
| 17 | Archive | `speckit-archive` | Phase 4 steps 1–3 on the branch, before the hand-off; the tail closes it after the merge | `phases-close.md` |

### 0. Size — decide how much of this to run

Run `/speckit-size` first and record the level. It decides which of the phases
below actually run:

| Level | Phases |
|---|---|
| 0 trivial | none of this — change, verify, commit. Say so and stop. |
| 1 one-session | 2, 7, 9, 10, 12, 14, 16 — no org context, plan, checklist or analyze |
| 2 feature | all of them (the default) |
| 3 project | all of them, per feature, against the shared brief |

A level chooses phases, never gates. Phase 9 runs at every level above 0: the
red-first hook reads the spec and the tasks, not the level, and a run that skips
tests because it called itself small is the failure this whole harness exists to
prevent.

A level is checked, not trusted: `node .claude/scripts/level.mjs check` runs
after phases 2, 4 and 7 (`phases-plan.md`) and promotes a 0 or 1 to 2 on a fact.
On a promotion, run the phases level 2 owes that were skipped, in run order,
before going on. Ready refuses a level 2 or 3 feature that lacks its owed
artifacts (`hand-off.md`).

### Run state — write it, do not narrate it

At every phase boundary:

```bash
node .claude/scripts/run-state.mjs set --status in-progress --phase <name> --feature <dir>
```

Use exactly these phase names: `size`, `constitution`, `specify`, `context`,
`clarify`, `plan`, `checklist`, `tasks`, `analyze`, `tests`, `implement`,
`converge`, `harden`, `refresh`, `review`, `agent-context`, `retro`, `archive`,
`hand-off`, `pr-test`, `merge`. `/speckit-watch` maps them to a stage
(`.claude/scripts/watch.mjs`) and judges a worktree stale by that stage's
threshold; any other name falls back to the feature's artifacts.

On a Hard Stop, record the machine-readable reason instead of only writing prose
into the run log — an orchestrator reads `.specify/run-state.json`, not the
transcript:

```bash
node .claude/scripts/run-state.mjs set --status blocked --blocking <condition>
```

Conditions: `dirty-tree`, `red-suite`, `unclear-intent`, `no-subagents`,
`repair-loop-exceeded`, `verification-failed`, `destructive-action`,
`product-call`.

Every fix/re-verify lap in phases 12 and 14 is counted:

```bash
node .claude/scripts/run-state.mjs repair   # exits 1 at the cap, with the run blocked
```

When it exits 1, **stop**. Five laps without convergence is not one lap away
from converging; report what the findings are and which decision is unresolved.

## Notifying

A run takes hours and the user has walked away. Call `PushNotification`
(`status: "proactive"`, one line under 200 characters, lead with what they
would act on) exactly twice at most: at the final report — `"<feature>: N
commits, review APPROVE, PR ready for your review"` — and at any Hard Stop — `"<feature>
stopped at phase N: <reason>"`. Never for phase progress; the tool skips the
notification when they are watching, and a needless one costs attention that
accumulates.

## Hard Stops

Stop the run, report what is done and what is not, and hand back. This list is
exhaustive — nothing else interrupts the pipeline:

1. Empty feature description.
2. Dirty working tree, or red `typecheck`/`lint`/tests at preflight.
3. CRITICAL analyze findings surviving 2 remediation rounds (phase 8).
4. CRITICAL/HIGH `spec-reviewer` findings surviving the re-review (phase 14).
5. The same test failing after 3 distinct fix attempts in phase 10.
6. A destructive or outward-facing action the pipeline did not plan: pushing
   anywhere but the feature's own branch, a force-push, merging the PR,
   deleting files outside the feature, wiping `.work/`, or anything
   `bash-guard.mjs` blocks that is genuinely required. Report it; do not work
   around it.
7. A scope change only the user can decide — the description contradicts the
   constitution (Principle I most often), or requires a product call no
   artifact in the repo answers.

On any hard stop the run log and every commit already made stay in place, so
the run is resumable by invoking the remaining phase skills directly.

## Final Report

One report, at the end, standing on its own. Write it into
`specs/<feature>/auto-run.md` under `## Final Report`, never only into the
reply. When this run was dispatched as an agent (by the orchestrating session
or `/speckit-watch`), the reply is the envelope from AGENTS.md "Agent
replies" and at most 10 lines in all, the report itself left in the file:

```
STATUS: success | failure | blocked | partial — <one line: what happened>
PR: #<n> <draft|ready|merged> <sha7> | none
NEXT: <the one action the caller should take> | none
FILES: <paths written, comma-separated> | none
```

Then up to six lines: commits and test counts, review verdicts, decisions
taken on the owner's behalf, follow-ups. A clean run ends at the hand-off
with `PR: #<n> ready <sha7>` and `NEXT: tail #<n>`. Run by the owner in their own
session, the same envelope opens the report. Its sections and the
Completion Checklist are in `report.md`.

## Agent Execution Rules: auto deltas

<!-- project-local addition — re-apply after `specify integration upgrade` -->

The constitution's Agent Execution Rules apply in full. Specific to this command:

- This command owns the run order and the gate answers. It does not restate,
  reinterpret, or replace the phase skills' own instructions — when this file
  and a phase skill disagree on how to do the phase's work, the phase skill
  wins; when they disagree on whether to stop and ask, this file wins.
- Every autonomous answer cites its evidence: the description, a constitution
  principle, or `path:line` from a file read this session. An answer with no
  evidence is logged as an assumption in the spec, not presented as a finding.
- Progress is one line per completed phase. No narration of the phase skills'
  internal steps.
- After a context compaction, re-read `specs/<feature>/auto-run.md`,
  `tasks.md`, and `plan.md`; the run log and the `[X]` markers are the truth,
  not memory.

