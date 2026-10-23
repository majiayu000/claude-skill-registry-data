---
name: execute-plan
description: "Use only when the operator has explicitly asked, for this run, to carry out a written plan through delegated workers: a fresh implementer per task, a conformity-then-quality review of each task, scoped re-review of fixes, a decision register. Opt-in, never started on its own."
disable-model-invocation: true
---

# execute-plan

Opt-in support for steps 5 to 7 of `WORKFLOW.md`, for the case where the operator chooses to hand a finished `plan` to
delegated workers instead of building it task by task in the conversation. It is not the default way to build
(`code` is), and it never starts because a plan exists.

## When
Only after the operator has said, in this run and about this plan, that it should be executed this way (step 0).
Typical fit: a plan of mostly independent tasks, each testable on its own, where context per task would otherwise
pile up. Poor fit: tightly coupled tasks, a plan still being reshaped, work that needs the operator's eyes on each step.

## Steps
0. **Get the operator's decision, every time.** Name the plan file, the scope (the whole plan or the first N
   tasks) and the mode (delegated workers, or inline with a final fresh review). Wait for an explicit yes. A yes
   given for another plan, another day or a previous run does not carry over, and `skills/plan` keeps its rule
   that nothing runs the whole plan on its own: this block executes only what the operator just granted. No
   answer is a no.
1. **Set up.** Work in an isolated worktree (`skills/start-feature`), never on the base branch without consent.
   Open a **ledger** file outside version control, named for the plan, whose first line identifies the plan
   file. Every finished task gets one completion line with its commit. After a context loss, trust the ledger
   and the commit log over memory: a controller that forgot where it was has re-dispatched finished tasks before.
2. **Read the plan and its spec once**, note the plan's global constraints, create one tracked item per task.
   The spec is the authority the plan argues from; conflicts inside the plan resolve against it.
3. **Scan the plan for conflicts before dispatching anything.** Write a table into the ledger: one row per
   pair of tasks that share a file or an interface (what one produces, what the other consumes, what you found),
   and one row per task (does its own text agree with itself: tests against code, files created against files
   touched later). "The scan is clean" with no rows is a scan not run. Settle each conflict against the spec and
   record the ruling.
4. **Run the task loop**, in dependency order:
   1. Write the task brief to a file; record BASE (the commit before the task).
   2. Dispatch a fresh implementer from `references/01-implementer-brief.md`, with the model chosen on purpose
      (`skills/choose-model`). It asks its questions before starting, implements with tests, commits, reviews
      its own diff and writes a report file.
   3. Verify the claim, not the report: read the diff for the task yourself or through the reviewer, never
      accept "done" on the worker's word (`skills/gate` §8).
   4. Write the task diff to a file and dispatch the task review from `references/02-task-review.md`: conformity
      to the brief first, quality second, read-only.
   5. Findings go back to the implementer; each fix round ends in a scoped re-review from
      `references/03-scoped-re-review.md`, which judges the previous findings and the fix diff only.
   6. Cap the rounds (three by default, written in the ledger). Past the cap the remaining findings are listed and
      brought to the operator; the loop does not run a fourth time on hope.
   7. Append the completion line, tick the item.
5. **Decisions that are not stops go in the register** (`references/04-decision-register.md`): a naming
   tie-break, an ordering the spec leaves open, which of two spec-valid options. One line each, with the reason
   and what it costs if wrong. A decision that changes behaviour the spec states, a public contract or data is
   not a register entry; it is a stop.
6. **Stop and ask, always, for**: an irreversible or destructive operation; a security-sensitive action; an
   effect outside the worktree (a merge, a push to a shared branch, a publish); a plan so inconsistent that every
   continuation is a guess; the round cap; anything the operator reserved. These override any grant from step 0.
7. **After the last task, review the whole branch once** with a fresh reviewer on the most capable model
   available (`skills/review`). One fix dispatch for what it finds, one scoped re-review, then the residuals go
   to the operator.
8. **Hand back to the pipeline.** The task reviews are an aid, not the gate: run `gate` on the result, then
   `review`, exactly as for built-inline work. Delete the ledger only when the branch is merged.

## Output / checkpoint
`build_done` after the last task, with the ledger (completion lines, conflict table, register) kept as the trail;
`verified` still comes only from `gate`. If the run stopped, the ledger names the first unfinished task.

## Guardrails
- **No execution without a fresh, explicit operator decision for this run.** A plan on disk, a green earlier
  run or an operator's general enthusiasm is not one.
- **A worker never dispatches workers**, and a reviewer never spawns a second opinion: the review seats are
  already in the loop, and a review you ask a worker to run on its own work counts for nothing.
- **Each worker gets exactly what it needs, as files**: the brief, the constraints, the diff. Never the
  controller's conversation, and never a paste of a large artefact into a prompt that stays resident for the rest of the run.
- A worker's report is an unverified claim. The reviewer reads the diff; it re-runs a test only to settle a
  named doubt, and the implementer's own test evidence is read, not regenerated.
- Never weaken a test, a gate or a threshold to end a fix round (`skills/tdd`, `skills/gate`).
- Set the model explicitly on every dispatch; an omitted one inherits the most expensive.
- Mixed up with `dispatch-parallel`? That block fans out independent work at once; this one runs a chain
  (implement, review, fix, re-review) per task.

| Thought | What to do instead |
|---|---|
| "The operator wanted the plan done, so I will not ask again" | Step 0 is per run. Ask. |
| "The worker said all tests pass" | Claims are checked against the diff and the output (`skills/gate` §8). |
| "One more fix round will settle it" | The cap exists for the loop that is not converging. Stop and list. |
| "This conflict is small, I will just choose" | Register it if the spec does not state it; stop if it does. |

Predicted, not recorded: replace with verbatim sentences from a `skills/testing-blocks` run when one exists.

## Origin
The `subagent-driven-development` skill of `superpowers` (MIT, read 2026-10-02): fresh implementer per task,
conformity-before-quality task review, scoped re-review, ledger against context loss, the pre-flight conflict
table, model chosen per role. Its `do` counterpart in `claude-mem` (Apache-2.0, same date) contributed the
rule that nothing is committed before its verification passes. Rewritten in our words. Two deliberate
differences: the source runs without pausing between tasks and settles every conflict itself; this block is
opt-in per run, has a round cap that returns to the operator and treats behaviour or contract changes as stops.
