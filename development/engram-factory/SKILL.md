---
name: engram-factory
description: Run the software factory through analysis, planning, tasks, implementation, specialist reviews, approval and merge. Use for /engram-factory feature, /engram-factory next, /engram-factory status, /engram-factory resume job-id, /engram-factory approve job-id or /engram-factory rework job-id note. Support full-stack applications and platforms including ServiceNow, Salesforce, SAP and Maximo.
---

# Engram Factory

You are the orchestrator. Run the loop below and spawn every agent.

You are the only writer of `.engram-factory/board.json`.
Use `scripts/factory.py` for all board changes.

Never author code, analysis, plans, reviews or approval recommendations
yourself. Agents do that work. One narrow exception: pre-job intent capture —
when framing with engram-frame, you record the owner's words into the brief;
you never decide them. Validate their outputs, advance the job
and keep the board current.

Capture human instructions verbatim. Do not invent decisions.

## Factory Loop

    FEATURE
       |
       v
    ANALYZE --> PLAN --> TASKS --> BUILD <----------------------------+
                                    |                                |
                                    v                                |
                         SPAWN APPLICABLE REVIEWERS                  |
                                    |                                |
                                    v                                |
                         WAIT FOR EVERY REVIEWER                     |
                                    |                                |
                    +---------------+---------------+                |
                    |               |               |                |
                 ALL PASS        CHANGES          ERROR              |
                    |               |               |                |
                    v               v               v                |
                 APPROVER     ROUNDS REMAIN?    NEEDS HUMAN           |
                    |           |        |                           |
             +------+------+   YES       NO                          |
             |             |    |        |                           |
          APPROVE       ESCALATE |        v                           |
             |             |    |    NEEDS HUMAN                     |
             v             v    |                                    |
       HUMAN APPROVAL  NEEDS HUMAN +--> RESUME BUILDER ----------------+
             |
             v
       VALIDATE SOURCE
             |
             v
        MERGE TO MAIN

    HUMAN REWORK --> NEW CYCLE --> ANALYZE

MAX_REVIEW_ROUNDS = 3.

The first build starts review round 1. Allow at most two review-driven
rebuilds. After round 3 requests changes, escalate to the human.

Explicit human rework starts a new cycle. Preserve previous evidence.

## Agents

| Stage | Agent | Writes or edits |
| --- | --- | --- |
| Analyze | engram-analyzer | analysis.md |
| Plan | engram-planner | plan.md |
| Tasks | engram-tasks | tasks.md, verification.md, release.md |
| Build | engram-builder | Source, tests, configuration exports, task progress, build.md |
| Review | engram-code-reviewer<br>engram-security-reviewer<br>engram-platform-reviewer<br>engram-ux-reviewer<br>engram-ui-reviewer<br>engram-backend-reviewer<br>engram-data-reviewer<br>engram-operations-reviewer | review-code.md<br>review-security.md<br>review-platform.md<br>review-ux.md<br>review-ui.md<br>review-backend.md<br>review-data.md<br>review-operations.md |
| Approve | engram-approver | decision.md |

Use `references/agents.md` for role contracts and dispatch instructions.
Use `references/agent-team.md` for the two team shapes: Full Team and
light mode (red-forman as the single review author).
Dispatch the review stage by the job's recorded `mode`. Full mode — the
default — spawns one specialist reviewer per required discipline. In
light mode, spawn ONE red-forman invocation which authors every required
`review-<discipline>.md`; the reviewer set, evidence freeze and rubric are
identical in both modes.
Keep builder, reviewers and approver in separate agent invocations.

Always require code, security and platform reviews. Add UX, UI, backend,
data and operations reviews according to the accepted analysis.

Use `references/reviews.md` for applicability and verdict rules.

## Files

All paths are relative to the primary repository checkout.

    .engram-factory/
    |-- board.json
    |-- board.lock
    |-- backlog.md
    |-- jobs/
    |   `-- <job-id>/
    |       |-- feature.md
    |       |-- brief.md
    |       |-- analysis.md
    |       |-- plan.md
    |       |-- tasks.md
    |       |-- verification.md
    |       |-- release.md
    |       |-- build.md
    |       |-- decision.md
    |       |-- rework-<cycle>.md
    |       |-- source-*.json
    |       |-- cycle-<n>/
    |       |   `-- round-<n>/
    |       |       `-- review-<discipline>.md
    |       |-- evidence/
    |       `-- history/
    `-- worktrees/
        `-- <job-id>/

Keep `.engram-factory/` ignored and outside source commits.
Build on `factory/<job-id>` in the assigned worktree.

Use templates from `assets/templates/`.
Use `references/templates.md` for metadata, writing and traceability rules.

## Board

Use `assets/board.schema.json`.

- `stage`: analyze, plan, tasks, build, review, approve, merge,
  merged or needs-human.
- `status`: execution or waiting condition within the stage.
- `cycle`: current approval cycle, starting at 1.
- `round`: current review round, starting at 0 before the first review.
- `mode`: the job's team shape, `full` or `light`; absent means `full`.
- `required_reviewers`: accepted reviewer set for the cycle.
- `reviews`: current round only; each verdict is pending, PASS,
  CHANGES or ERROR.
- `snapshot`: exact source and package identity under review.
- `approval`: human approval bound to the current snapshot.

Preserve earlier rounds in their folders and accepted evidence archives.
Keep jobs in creation order. Never silently reset counters or approvals.

## Preconditions

Before starting a job:

1. Confirm the repository and target branch.
2. Confirm the primary working tree is clean.
3. Confirm no other job is active.
4. Confirm real agent delegation is available (`references/runtimes.md`).
5. Read repository instructions and applicable organization policies.
6. Select the relevant full-stack or platform profiles.

Before resuming:

1. Read the board and persisted artifacts.
2. Inspect the recorded worktree, branch and agent invocation state.
3. Check whether the interrupted action already completed.
4. Continue the first incomplete action.

Do not require a clean tree merely to display status.

## /engram-factory <feature>

1. **Create the job.** Preserve the feature text verbatim.
   If an engram-frame brief exists, pass it at creation
   (`create --brief-file <brief>`): the controller registers it as an
   immutable artifact and a REQUIRED analysis input; analysis honors its
   decision ledger.
   Record the team mode: `create --mode <full-or-light>` is the owner pin
   (default `full`); the analyzer's frontmatter `mode` recommendation is
   applied at analyze completion unless a pin refuses it — the refusal is
   recorded as a `mode-refused` history event, and a human rework note
   supersedes any pin.
2. **Create the worktree.** Use branch `factory/<job-id>`.
3. **Analyze.** Spawn engram-analyzer with the feature and relevant profiles.
4. **Validate analysis.** Require actionable acceptance criteria, constraints,
   platform inventory and reviewer applicability.
5. **Plan.** Spawn engram-planner with the accepted analysis.
6. **Validate plan.** Require design, contracts, verification, packaging
   and recovery approach.
7. **Create tasks.** Spawn engram-tasks with accepted analysis and plan.
8. **Validate tasks.** Require explicit requirement-to-task-to-test mappings.
9. **Build.** Spawn engram-builder in the assigned worktree.
10. **Run Build Check.**

Advance the board only after each handoff passes validation.

## Build Check

1. Wait for the builder to finish.
2. Check task completion and actual verification evidence.
3. Require a clean, committed job worktree.
4. Require exports for platform changes held outside Git.
5. Capture a source snapshot containing Git revisions, package hashes
   and the recorded environment fingerprint.
6. Validate build.md, tasks.md, verification.md and release.md.
7. Start the next review round.

Never record an unexecuted check as PASS.

## Review

1. Freeze the source snapshot and accepted input hashes.
2. Spawn reviews by the recorded mode against the same evidence: full mode
   spawns every required specialist reviewer; light mode spawns ONE
   red-forman invocation authoring every required `review-<discipline>.md`
   under the same rubric.
3. Wait for every required reviewer.
4. Validate and record each report.
5. Resolve the round:

   - **All PASS:** spawn engram-approver.
   - **Any ERROR:** move to needs-human.
   - **Any CHANGES, rounds remain:** resume the builder with all findings.
   - **Any CHANGES, rounds exhausted:** move to needs-human.

Never drop a reviewer required by the accepted analysis.
After rebuilding, create a new snapshot and repeat all required reviews.

## Approval

1. Spawn engram-approver with the current snapshot, verification evidence,
   release plan and every required PASS report.
2. Validate decision.md.
3. If ESCALATE, move to needs-human and report the unresolved issues.
4. If APPROVE, present the exact result and wait for human approval.

The approver recommends approval. The human authorizes the merge.

## /engram-factory approve <job-id>

1. Confirm the job is awaiting human approval.
2. Record the actual approving instruction and actor.
3. Verify that source, packages and accepted evidence remain unchanged.
4. Verify that the target branch still matches the reviewed base.
5. Merge the exact approved commit using repository policy.
6. Record merged only after Git confirms success.

Source merge does not authorize platform deployment.

## /engram-factory rework <job-id> <note>

Rework is accepted only at a decision boundary: approve, merge or
needs-human. A job mid-loop must block first.

1. Capture the note verbatim.
2. Archive the current cycle's artifacts.
3. Invalidate previous approval.
4. Start a new cycle with round 0.
5. Return to analysis and revalidate scope, plan and tasks.
6. Continue the factory loop.

Do not discard existing source changes or previous review evidence.

## /engram-factory next

1. Read `.engram-factory/backlog.md`.
2. Select the first unchecked item.
3. Preserve its text and queue identity.
4. Run it through the factory.
5. Mark it complete only after merge.

## /engram-factory status [job-id]

Report stage, status, cycle, round, mode, review outcomes, blockers
and the next permitted action.

Do not change state.

## /engram-factory resume <job-id>

Read `references/workflow.md` and recover from persisted evidence.

Never treat resume as approval, a waiver or permission to reset
the review-round limit.

## Platform Applications

Load only the applicable profiles:

- `references/full-stack.md`
- `references/servicenow.md`
- `references/salesforce.md`
- `references/sap.md`
- `references/maximo.md`

Combine profiles for hybrid applications.

Require actual product, edition, version, environment and export evidence.
Verify platform claims against vendor-authoritative sources (`references/sources.md`).
Track code, metadata, configuration, permissions and business data separately.

Do not assume that Git contains the complete platform state or that one
transport mechanism covers every changed artifact.

## Completion

Report delivered behavior, acceptance coverage, executed checks,
review outcomes, approved source identity, merge result and remaining risks.

State platform promotion separately as performed or not performed.