---
name: executing-plans
description: Executes a written implementation plan task-by-task by dispatching a fresh implementer subagent per task, a reviewer subagent after each, and a progress ledger that survives context compaction. Use when a plan exists in docs/plans/ and the user wants it implemented, resumed after interruption, or finished with verification and a PR.
---

# Executing Plans

## Overview

Load the plan, review it critically, execute every task through a fresh implementer plus a reviewer gate, verify, then hand off. You are the controller: you coordinate, rule, and record. You do not write the code yourself.

**Announce at start:** "Using opm:executing-plans to implement `<plan path>`."

**Core principle:** fresh subagent per task + task review (spec + quality) + ledger = high quality, fast iteration, nothing lost to compaction.

**Why subagents:** an implementer with isolated context stays focused and succeeds because you construct exactly what it needs. It never inherits your session's history. This also keeps your own context clean for coordination.

## Choose the Mode

- **Subagent mode** (default): 4 or more tasks, or any task that needs its own judgment, tests, or review surface. Described in "The Task Loop".
- **Inline mode**: the plan has 3 or fewer tasks. You execute the steps yourself in this session, still following `opm:tdd-workflow`, still keeping the ledger, and still dispatching a `code-reviewer` subagent once at the end. See "Inline Mode".

Say which mode you are using and why.

## Setup

1. **Branch check.** Never start implementation on `main`/`master` without the user's explicit consent. Create or verify a feature branch (or worktree) first.
2. **Ledger check.** The ledger lives at `docs/plans/<plan-basename>.progress.md` (plan `docs/plans/2026-09-12-auth.md` -> `docs/plans/2026-09-12-auth.progress.md`). If it exists and its first line names your plan file, tasks with a `Task <N>: complete` line are DONE: do not re-dispatch them; resume at the first task without one. A task whose last line is a fix round is mid-loop: resume at the next round. Otherwise create it with `# OPM ledger - plan: <plan file path>` as line 1.
3. **Read the plan once.** Note Goal, Global Constraints, and the Interfaces blocks. If the plan names a Spec, read that too: the spec is the authority the plan argues from, and conflicts inside the plan resolve against it. A plan with no reachable spec gets a ledger note saying so; rulings made without one are provisional.
4. **Pre-flight conflict scan.** One row per pair of tasks that share a file or interface (what one produces vs. what the other consumes), and one row per task (do its tests agree with its code, do the files it creates match the files it later touches). Write the table to the ledger. Rule on each conflict before Task 1, spec as binding authority. "The scan is clean" without rows is not a scan you ran.
5. **Create a todo per task.**

Conversation memory does not survive compaction. Controllers that lost their place have re-dispatched entire completed task sequences, the single most expensive failure observed. After compaction, trust the ledger and `git log` over your own recollection.

## Continuous Execution and Rulings

Do not pause to check in between tasks. "Should I continue?" prompts and progress summaries waste the user's time; they asked you to execute the plan, so execute it. Between tool calls, narrate at most one short line.

**Rulings, not stalls.** Conflicts, ambiguities, plan defects, a cap you would have asked to exceed: decide them. Record every decision in the ledger as `Ruling: <what you decided> - <why> - <what it costs if wrong>` and keep going. A wrong ruling costs rework the user can see and undo; a session parked on a question costs their whole day.

**Only four things stop the run:**
1. An irreversible or destructive operation (data deletion, history rewrite, force push).
2. A security-sensitive action (secrets, auth changes, permission grants).
3. A side effect outside this branch that norms say you ask about first (merge, push to a shared branch, publish, deploy).
4. A plan so broken that every path forward is a guess.

For those, stop and ask. For everything else, rule and ledger.

## Model Selection

Always specify the model when dispatching; an omitted model inherits your session's (usually the most expensive).

- Task text contains the complete code to write (transcription plus testing), or a single-file mechanical fix: cheapest tier (`haiku`).
- Implementation from prose, multi-file integration, reviewers: mid tier (`sonnet`).
- Design judgment, broad codebase understanding, the final whole-branch review, fix round 3 escalation: most capable tier (`opus`).

Turn count beats token price: the cheapest models take 2-3x the turns on multi-step work. Use mid tier as the floor for anything that is not transcription.

## The Task Loop (Subagent Mode)

**Batch small same-shape work.** If several tasks are each a tiny independent edit of the same kind (the same constant change across files), compose ONE brief listing every file and its change, dispatch one implementer, and review the diff as one unit.

**Never dispatch two implementers in parallel** on the same branch; they conflict.

### 1. Compose the brief and dispatch the implementer

Record `BASE=$(git rev-parse HEAD)` before dispatching.

The brief is the single source of requirements. It contains, and only contains:
1. One line on where this task fits in the project.
2. The task's full text from the plan, copied verbatim (Files, Interfaces, every step with its code blocks).
3. The plan's Global Constraints block, verbatim.
4. The Produces entries of earlier tasks this task Consumes, with any deviation the implementer of those tasks reported.
5. Relevant file paths to read (the files this task touches, plus one or two exemplars of the codebase's patterns).
6. Your resolution of any ambiguity you noticed in the task, and any parked finding in the area this task touches.

**Never** paste the whole plan, the spec, prior-task summaries, or chat history. A real session's dispatch hit 42k chars of which 99% was pasted history. Exact values (numbers, magic strings, signatures, test cases) live in the task text; do not paraphrase them.

Record the implementer's agent identity from the dispatch result; fix rounds 1-2 resume it.

#### Implementer prompt template

```
Agent (subagent_type: general-purpose, model: <per Model Selection>)
description: "Implement Task N: <task name>"
prompt: |
  You are implementing Task N: <task name>, one task of a larger plan.
  Work from: <repo root>. Branch: <branch>.

  ## Where this fits
  <one line>

  ## Your task (requirements, exact values are binding)
  <task text verbatim from the plan>

  ## Global constraints
  <verbatim block>

  ## Interfaces from earlier tasks
  <Produces entries this task consumes>

  ## Files to read first
  <paths>

  ## Rules
  - Follow the steps in order. TDD is mandatory (opm:tdd-workflow): write
    the failing test, run it and see it fail, implement minimally, run it
    and see it pass, commit. Do not skip the red step.
  - Run the focused test while iterating; run the full suite once before
    the final commit.
  - Do NOT dispatch subagents of your own, and never spawn a reviewer.
    A reviewer is already scheduled by the controller after you report.
  - Follow the file structure in the task. If a file you are creating grows
    beyond the task's intent, stop and report DONE_WITH_CONCERNS rather
    than splitting it on your own.
  - Do not restructure code outside your task. Follow existing patterns.
  - It is always OK to stop and say this is too hard. Bad work is worse
    than no work. Escalate with BLOCKED or NEEDS_CONTEXT when: the task
    needs an architectural decision with several valid answers; you need
    code context you cannot find; you are reading file after file without
    progress.

  ## Self-review before reporting
  Completeness: every requirement implemented? Edge cases? Quality: clear
  names, clean code? Discipline: nothing beyond what was asked (YAGNI),
  existing patterns followed? Tests: verify real behavior, not mocks;
  output pristine (no stray warnings)? Fix what you find before reporting.

  ## Report (under 15 lines)
  - Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
  - Commits: short SHA + subject, each
  - Tests: command run, RED output summary, GREEN output summary
    (e.g. "14/14 passing, output pristine")
  - Deviations from the task text or Interfaces block, if any
  - Concerns, if any
  If BLOCKED or NEEDS_CONTEXT: what you are stuck on, what you tried,
  what you need.
```

### 2. Handle the report

- **DONE:** proceed to review.
- **DONE_WITH_CONCERNS:** read the concerns. Correctness or scope concerns get addressed before review; observations ("this file is getting large") are noted in the ledger and review proceeds.
- **NEEDS_CONTEXT:** provide the missing context and re-dispatch.
- **BLOCKED:** change something. Context problem: add context, same model. Reasoning problem: more capable model. Too large: split it. Plan is wrong: rule on the correction, ledger it, re-dispatch with the ruling in the brief. Never re-run the same dispatch unchanged.

Before review, confirm independently that commits exist: `git log --oneline BASE..HEAD`. An implementer report is a claim (see `opm:verification-before-completion`).

### 3. Dispatch the reviewer

Every task gets a review: spec compliance AND code quality, both verdicts required. Implementer self-review never replaces it. Never fix findings yourself in the controller session; controller fixes pollute your context and skip review.

Hand the reviewer the task text and the diff. Prefer to have the reviewer run the git commands itself (keeps the diff out of your context); paste the output only when the diff is tiny.

Do not pre-judge for the reviewer. If the prompt you are writing contains "do not flag", "at most Minor", or "the plan chose", stop: you are sparing yourself a review loop. Let the reviewer raise it and rule on it afterwards.

#### Reviewer prompt template

```
Agent (subagent_type: general-purpose, model: <per Model Selection>)
description: "Review Task N (spec + quality)"
prompt: |
  You are reviewing one task's implementation: first whether it matches
  its requirements, then whether it is well-built. This is a task-scoped
  gate, not a merge review. Your review is read-only: do not modify the
  working tree, index, or branches. Do not dispatch subagents.

  ## What was requested
  <task text verbatim>

  ## Global constraints
  <verbatim block>

  ## What the implementer claims
  <implementer's short report>

  ## Diff under review
  Base: <BASE>  Head: <HEAD>
  Run: `git log --oneline <BASE>..<HEAD>`, `git diff --stat <BASE>..<HEAD>`,
  `git diff -U10 <BASE>..<HEAD>`. The diff is your view of the change. Read
  a changed file separately only when a hunk you must judge is cut off,
  and inspect code outside the diff only to check a concrete risk you can
  name (a changed contract's call sites, shared mutable state, lock order).
  Say what you checked.

  ## Do not trust the report
  It is unverified claims about the code, including its rationales ("left
  it per YAGNI"). Judge the code. Do not re-run the suite to confirm the
  report; run a focused test only when reading raises a specific doubt.
  Warnings or noise in the reported test output are findings.

  ## Part 1: Spec compliance
  Missing (skipped or claimed but not implemented), Extra (unrequested,
  over-engineered), Misunderstood (right feature, wrong way). A batched
  brief: every listed file must have its hunk. Requirements you cannot
  verify from this diff alone: report as "Cannot verify", do not go hunting.

  ## Part 2: Code quality
  Separation of concerns; explicit error handling (no swallowed errors);
  DRY without premature abstraction; edge cases; tests verify behavior,
  not mocks; each file has one responsibility; new files not already
  large. Cite file:line for every finding.

  ## Calibration
  Critical: broken, insecure, or data-losing. Important: cannot be trusted
  until fixed (missed requirement, fragile behavior, swallowed errors,
  tests that assert nothing, verbatim duplicated logic). Minor: polish and
  "coverage could be broader". If the task text mandates something this
  rubric calls a defect, report it as Important, labeled plan-mandated.
  Name what was done well before listing issues.

  ## Output (the report is your whole final message, no preamble)
  ### Spec compliance: COMPLIANT | ISSUES (list) | CANNOT VERIFY (list)
  ### Strengths
  ### Issues: Critical / Important / Minor, each with file:line, what,
      why, how to fix
  ### Verdict: Approved | Needs fixes, with 1-2 sentences of reasoning
```

Resolve every "Cannot verify" item yourself; you hold the cross-task context. A confirmed gap enters the fix loop as a finding.

### 4. The fix loop (up to 3 rounds)

The loop triggers on spec ISSUES, any Critical or Important finding, or a "Cannot verify" you confirmed as a gap. Two routes leave it immediately:

- **Minor findings** go to the ledger (`Task <N>: minor (deferred): <one-liner>`) for the final review to triage. They never enter the loop.
- **Plan-mandated findings**, or any finding that conflicts with the plan text: rule on it with the spec as authority, ledger the ruling, then either dispatch the fix or park it. Never dismiss a finding because the plan mandates it.

A fix round is one fix dispatch plus one scoped re-review.

- **Rounds 1-2:** resume the original implementer (SendMessage to its agent ID) with the open findings verbatim and the covering test files to re-run. If it cannot be resumed, dispatch a fresh implementer with the brief plus the findings.
- **Round 3:** dispatch a fresh implementer on a more capable model with the brief, the findings, and: "A prior implementer attempted this task twice; you own it now."
- **Every round:** the implementer fixes, re-runs the covering tests, and reports commits plus test output. Then dispatch a scoped re-review (mid tier or cheaper) with the findings list and `git diff <FIX_BASE>..<HEAD>` where FIX_BASE is the head the previous review saw. The re-reviewer verdicts each finding ADDRESSED or NOT ADDRESSED ("attempted" is not addressed), flags new Critical/Important breakage in the fix diff only, and lists out-of-scope observations, which go to the ledger as deferred minors.
- **After each round**, ledger: `Task <N>: fix round <R>/3 (<X> addressed, <Y> open - <one-liners>; commits <a7>..<b7>)`.

**The breaker.** If round 3 still leaves findings open, stop dispatching and adjudicate each open finding yourself:
- Reviewer wrong or contestable: `Task <N>: parked - <finding> - Ruling: <why the code stands>`.
- Real but nothing downstream builds on it: park it with a ruling that says real and deferred.
- Real and load-bearing (a later task builds on it, or it reveals a plan defect): rule on the smallest change that unblocks dependent work, ledger it, carry it into the next task's brief. Stop only if every path forward is a guess.

Adjudicate only at the cap. Every adjudication is a ledger entry; silent discards are forbidden.

### 5. Complete the task

When the review is clean, or every open finding is parked with a ruling at the cap, append:
- `Task <N>: complete (commits <base7>..<head7>, review clean)`, or
- `Task <N>: complete (commits <base7>..<head7>, <K> parked)`

Mark the todo complete and move to the next task. Never move on while Critical/Important findings are neither fixed nor parked-with-ruling.

## Inline Mode (3 or fewer tasks)

1. Setup as above (branch, ledger, read plan and spec, todos).
2. For each task: follow each step exactly as written, red then green then commit (`opm:tdd-workflow`). Run every verification the step names and read the output. Ledger `Task <N>: complete (commits ...)` after each.
3. After the last task, dispatch one `code-reviewer` subagent with the plan path and `git diff <branch-base>..HEAD`, fix Critical/Important findings yourself in this mode (there is no implementer to resume), and re-run the covering tests.
4. Continue to "Finishing".

If a task turns out to need judgment the plan did not anticipate, or the count grows past 3, switch to subagent mode for the remaining tasks and say so.

## Ledger Format

```
# OPM ledger - plan: docs/plans/2026-09-12-auth.md
Branch: feat/auth  Base: 3f2a1c9
Preflight: <table rows or "clean: N pairs checked, M tasks self-consistent">
Ruling: <decision> - <why> - <cost if wrong>
Task 1: complete (commits 3f2a1c9..8b77d10, review clean)
Task 2: minor (deferred): duplicated fixture setup in test_session.py:12
Task 2: fix round 1/3 (2 addressed, 1 open - missing 401 path; commits 8b77d10..c01e4aa)
Task 2: complete (commits 8b77d10..d9e02f1, review clean)
```

Append-only. One line per event. The commits it names exist in git even when your context no longer remembers creating them.

## Finishing

1. **Final whole-branch review.** Dispatch a `code-reviewer` subagent (most capable tier) with the plan path, the spec path, `git diff <branch-base>..HEAD`, and the ledger's deferred-minor and parked lines to triage. For security-relevant diffs, also dispatch `security-reviewer`; for diffs heavy in error handling, `silent-failure-hunter`. If findings come back, dispatch ONE fix subagent with the complete list (never one fixer per finding), then one scoped re-review. Residual findings get adjudicated and ledgered; there is no second fix wave.
2. **Verify.** Invoke `opm:verification-before-completion`: run the full test suite, linter, type check, and build fresh; walk the spec requirement by requirement. No claims without output.
3. **Report rulings.** Collect every ledger line containing `Ruling:` or `parked` into your final message under "Rulings I made", in order, each with what it costs if wrong. This list is the only place decisions you took on the user's behalf reach them.
4. **Offer the PR.** Present a summary of the branch and ask whether to open a pull request (`gh pr create`) or leave the branch for them. Do not push or open the PR without a yes; that is stop condition 3.
5. **Compound learnings.** If anything non-obvious was learned (a gotcha in the toolchain, a plan defect pattern, a reviewer finding that recurred), invoke `opm:compound-learnings` to capture it. Skip it if nothing surprised you, and say so.

Leave the ledger in place; it is the record of how the branch was built.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Close enough on spec compliance" | Reviewer found spec gaps = not done. Fix, or hit the cap and adjudicate. Those are the only exits. |
| "I'll fix it myself, dispatching is overhead" | Controller fixes pollute your context and skip review. Resume the implementer. |
| "One more round will converge" | Past 3 rounds, failure is structural. Adjudicate and route. |
| "This finding is obviously wrong, I'll drop it" | You adjudicate only at the cap, and every ruling is a ledger entry. Silent discards are forbidden. |
| "The fix was small, skip the re-review" | Unreviewed fixes are how regressions land. Every round ends with a scoped re-review. |
| "Reviews slow the loop down" | The loop without reviews is unverified churn. Reviews are its brakes and steering. |
| "Ledger bookkeeping is overhead" | The ledger is what survives compaction. Without one, controllers have redone whole task sequences. |
| "I'll paste the plan so the implementer has full context" | Full context is the failure mode. Task text plus interfaces plus constraints, nothing else. |
| "The implementer spawned its own reviewer, free assurance" | A duplicate seat reviewing the same diff. Flag it as a defect; the task review is the gate. |
| "Let me check in with the user before Task 4" | They asked you to execute the plan. Only the four stop conditions stop you. |
| "The implementer said DONE, so it's done" | A report is a claim. `git log` and the reviewer decide. |

<!-- Adapted from obra/superpowers (MIT) -->
