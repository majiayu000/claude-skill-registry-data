---
name: pair-process-implement
description: "Implements a refined user story task-by-task, via a 5-step cycle per task (context, branch, implementation, quality, commit). At the closing phase it writes a checkpoint and publishes the PR through a handoff-only subagent (clean context), resuming from the checkpoint when re-invoked on an interrupted story. Composes /pair-capability-verify-quality, /pair-capability-record-decision, /pair-capability-checkpoint, /pair-capability-publish-pr."
version: 0.6.0
author: Foomakers
---

# /pair-process-implement — Task Implementation

Implement a user story by processing its tasks sequentially. Each task follows a 5-step cycle: context → branch → implementation → quality → commit. The story-level process has 5 phases (0–4): analysis, setup, implementation, **closing (checkpoint + PR)**, and post-review merge. When all tasks are done the closing phase writes a checkpoint (the handoff artifact) and composes `/pair-capability-publish-pr` — inside a **handoff-only subagent** so the PR is always built on a guaranteed-clean context — to produce a single ready-for-review PR.

**Two AI macro-phases (R4.2):** refinement → implementation. The boundary artifact between them is a **checkpoint**: it is written at the closing phase and re-read at the opening phase so an interrupted story resumes exactly where it stopped, never repeating completed tasks.

**implement composes, it never re-does gate/PR logic.** The gate → PR → board sequence lives entirely in `/pair-capability-publish-pr`; this skill composes it (never re-implements PR creation). Task iteration and the checkpoint boundary are what `/pair-process-implement` owns.

**One PR per story:** the story lands on ONE branch with ONE PR; subsequent work on the story (further tasks/features) updates that same PR, never a new one unless a human explicitly requests it.

## Process Profile

<!-- process-step: id=implement -->

Executable form of the **`implement`** step. A **direct** invocation while a step is disabled by the project's profile warns and asks for confirmation; a **composed** one never prompts — it degrades exactly as a step that is not installed. No section ⇒ no-op. See [process-profile gate](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/process-profile-gate.md).

## Composed Skills

| Skill              | Type       | Required                                                                                            |
| ------------------ | ---------- | --------------------------------------------------------------------------------------------------- |
| `/pair-capability-verify-quality`  | Capability | Yes — invoked at quality validation phase                                                           |
| `/pair-capability-record-decision` | Capability | Yes — invoked when a decision needs recording                                                       |
| `/pair-capability-checkpoint`      | Capability | Yes — `$mode=resume` at the opening phase (resume probe), `$mode=write` at the closing phase (handoff artifact). If not installed, degrade to git+PM-tool resume (see Graceful Degradation). |
| `/pair-capability-publish-pr`      | Capability | Yes — the closing phase composes it (gate → PR → board) inside a handoff-only subagent. If not installed → **HALT** (implement never re-implements PR creation). |
| `/pair-capability-assess-stack`    | Capability | Optional — invoked when a new dependency is detected. If not installed, warn and continue.          |
| `/pair-capability-verify-adoption` | Capability | Optional — invoked before commit to check adoption compliance. If not installed, warn and continue. |

## Arguments

| Argument | Required | Description                                                                                                                                                                                                                             |
| -------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$story` | No       | Story ID to implement, supplied by the invocation (e.g. `/pair-process-implement #256`). If omitted, detected from session context or the current branch (`feature/#<id>-*`). This is the id the resume probe (Step 0.0) uses and the closing phase forwards to `/pair-capability-checkpoint` and `/pair-capability-publish-pr`. If it cannot be resolved when a checkpoint operation needs it → **HALT**. |

## Phase 0: Story & Task Analysis (BLOCKING)

#### No implementation without complete understanding.

### Step 0.0: Resume Probe (checkpoint) — NEVER SKIP

The opening phase re-reads the checkpoint so an interrupted story resumes exactly where it stopped (AC2). This runs first, before loading the story, so completed tasks are never re-done.

1. **Check**: Is `/pair-capability-checkpoint` installed AND does a checkpoint exist for this story (`.pair/working/checkpoints/<story-id>.md`)?
2. **Skip**: If no checkpoint exists → this is a fresh start. Proceed to Step 0.1 (normal one-shot flow — no regression, AC4).
3. **Act**: Compose `/pair-capability-checkpoint $mode=resume` (pass `$story` — the story id from the invocation, see [Arguments](#arguments); if absent it is detected from the branch). Use the parsed state — branch, tasks done, key decisions, remaining todos — to skip re-analysis and jump straight to the **first pending task** in Phase 2, **without repeating** completed tasks.
4. **Act — edge cases** (resolve before continuing):
   - **Checkpoint exists but its branch is missing** (checkpoint says branch X, repo has none): **HALT** and report the divergence. Do not guess a branch.
   - **Stale checkpoint (story already Done)**: warn that the story is already Done and **require explicit developer confirmation** before reusing the checkpoint. Never silently resume a finished story.
   - **Corrupted/incomplete checkpoint**: `/pair-capability-checkpoint` reports what parsed and what is missing — confirm the gaps with the developer before proceeding (never guess).
5. **Verify**: Either a fresh start is confirmed, or a valid checkpoint is resumed with the first pending task identified. If `/pair-capability-checkpoint` is not installed, fall back to the git+PM-tool resume (Idempotent Re-invocation) and continue.

### Step 0.1: Load Story

1. **Check**: Is the user story already loaded in this session?
2. **Skip**: If yes, confirm story ID and move to Step 0.1b.
3. **Act**: Read the story from the PM tool — resolution: see [way-of-working / PM-tool + code-host resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md).
   - Understand business value and acceptance criteria.
   - Confirm epic context.
4. **Verify**: Story is fully loaded. If not → **HALT**.

### Step 0.1b: Activate Story in PM Tool (NEVER SKIP)

1. **Check**: Is the story already assigned to the current developer AND status is "In Progress"?
2. **Skip**: If BOTH conditions met, move to Step 0.2.
3. **Act**: Update the PM tool:
   - **Assign** the story to the current developer (if not already assigned).
   - **Set status to "In Progress"** in the PM tool board/project.
4. **Verify**: Story is assigned and In Progress. If PM tool is inaccessible → warn developer and continue.

### Step 0.2: Analyze Tasks

1. **Check**: Are all tasks in the story readable and complete?
2. **Act**: Read ALL tasks. For each task, validate it has:
   - Complete task information (ID, parent story, priority, status)
   - Implementation approach (technical design, files, dependencies)
   - Acceptance criteria (deliverable, quality standards, verification)
   - Development workflow (TDD approach if development task, implementation steps)
3. **Verify**: All tasks are complete and follow the task template. If any task is incomplete → **HALT** and propose specific task updates.

### Step 0.3: Confirm with Developer

Present analysis:

```text
IMPLEMENTATION STATE:
├── Story: [#ID: Title]
├── PM Status: [In Progress ✓ | ⚠️ Not updated — reason]
├── Tasks: [N total — list each with type and status]
├── Task Types: [Development: N, Documentation: N, Configuration: N]
├── Dependencies: [prerequisite stories and their status]
└── Ready: [Yes | No — reason]
```

Ask: _"Ready to proceed with implementation?"_

## Phase 1: Setup

### Step 1.1: Load Technical Context

1. **Check**: Are adoption files already loaded in this session?
2. **Skip**: If yes, move to Step 1.2.
3. **Act**: Read:
   - [architecture.md](../../../.pair/adoption/tech/architecture.md) — architectural patterns
   - [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — approved libraries and versions
   - [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) — development process
   - [Design Rules](../../../.pair/knowledge/guidelines/code-design/design-principles/design-rules.md) — evidence-based do/don't patterns to avoid generating (constraints, not suggestions)
4. **Verify**: Technical context loaded. If adoption files missing, warn and proceed with guideline defaults.

### Step 1.2: Create or Switch to Feature Branch

1. **Check**: Does a branch for this story already exist? (`git branch --list 'feature/#<story-id>-*'`)
2. **Skip**: If branch exists, switch to it (`git checkout <branch>`) and move to Step 1.3.
3. **Act**: Create the branch from the adopted base branch — resolved by the convention's **`base-branch` resolution** order (`## Git Workflow` → legacy `## Merge Strategy` → default `main`), never re-derived here, so this skill and `/pair-capability-publish-pr` (the other reader of the key) cannot disagree on the branch — on the **code host**: branches and PRs are code-host operations, story/state writes (Step 0.1b, Step 2.8) are PM-tool operations; see the [routing table + `base-branch` resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md). Absent `code-host` ⇒ the same tool as the PM tool, so nothing changes for a single-tool project:

   ```bash
   # <base-branch> is the resolved adopted value, NOT a literal
   git checkout <base-branch> && git pull origin <base-branch>
   git checkout -b feature/#<story-id>-<brief-description>
   ```

4. **Verify**: On the correct feature branch.

### Step 1.3: Choose Commit Strategy

1. **Check**: Is this a single-task story?
2. **Skip**: If single task, set strategy to `commit-per-story` (one task = one commit). Move to Phase 2.
3. **Act**: Ask the developer:

   > **Commit strategy for this story:**
   > 1. **Commit per task** (recommended) — develop one task, ask dev, commit, update checkbox, next task. Single PR at end.
   > 2. **Commit per story** — develop all tasks continuously, then ask dev, commit all, update all checkboxes, single PR.

4. **Verify**: Strategy is set. Apply consistently for the entire story.

## Phase 2: Task-by-Task Implementation

Process tasks **sequentially**, one at a time. For each task:

### Step 2.1: Select Next Task

1. **Check**: Scan all tasks in dependency order. Find the first task that is not yet completed.
   - A task is "completed" if its checklist item is marked ✅ in the story AND (if commit-per-task) the commit exists on the branch.
2. **Skip**: If all tasks are completed, move to Phase 3.
3. **Act**: Set the active task. Update session state:

   ```text
   ACTIVE TASK:
   ├── Task: [T-N: Title]
   ├── Type: [Development | Documentation | Configuration | Research]
   ├── Mode: [TDD | Direct Implementation]
   └── Phase: [Starting]
   ```

### Step 2.2: Validate Task Completeness

1. **Check**: Does the active task have all required fields per the task template?
2. **Skip**: If complete, proceed to Step 2.3.
3. **Act**: If incomplete → **HALT**. Report missing fields and propose specific updates.

### Step 2.3: Execute Implementation

#### For Development Tasks (TDD Required):

Follow the TDD discipline rules strictly, and the [Design Rules](../../../.pair/knowledge/guidelines/code-design/design-principles/design-rules.md) loaded in Step 1.1 — do not generate a new instance of a known do/don't pattern (e.g. god module, static-only namespace class, optional-bag dispatch instead of a discriminated union).

#### TDD Discipline Rules:

1. **New features → add tests autonomously.** Write unit tests without asking.
2. **Modifying existing tests → ask developer with evidence.** Show what changes and why, get approval before modifying any existing test.
3. **No code+test changes in the same session.** When changing production code, do NOT modify tests until all existing tests pass. Separate RED, GREEN, and REFACTOR into distinct sessions:
   - **RED session**: Write or modify ONLY test code. Tests MUST fail. No implementation code changes.
   - **GREEN session**: Write or modify ONLY implementation code. Write minimal code to make tests pass. No test code changes.
   - **REFACTOR session**: Improve structure without changing behavior. Both test and production code may be cleaned up. All tests must remain green.
4. **Every module file must have a corresponding unit test file.** 1:1 mapping between source modules and test files.
5. **Avoid mocks — prefer in-memory test doubles.** Use dependency injection with in-memory implementations (e.g., `InMemoryFileSystemService` instead of mocking `fs`).

#### For Non-Development Tasks (Direct Implementation):

- **Documentation**: Implement directly following documentation standards.
- **Configuration**: Apply infrastructure guidelines.
- **Research**: Document findings and recommendations.

### Step 2.4: Check for New Dependencies

1. **Check**: Did the implementation introduce any new dependency not listed in [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md)?
2. **Skip**: If no new dependencies, move to Step 2.5.
3. **Act**: Is `/pair-capability-assess-stack` installed?
   - **Yes**: Compose `/pair-capability-assess-stack` to validate and register the dependency. If `/pair-capability-assess-stack` rejects (incompatible) → **HALT**.
   - **No**: Warn the developer:

     > New dependency detected: `[package@version]`. `/pair-capability-assess-stack` is not installed — please manually verify against the tech stack and update [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md).

4. **Verify**: Dependency is either validated by `/pair-capability-assess-stack` or acknowledged by developer.

### Step 2.5: Check for Decisions

1. **Check**: Did the implementation introduce any decision not covered by existing ADRs or ADLs?
2. **Skip**: If no new decisions needed, move to Step 2.6.
3. **Act**: Ask the developer if a decision record is needed. If yes, compose `/pair-capability-record-decision` with the appropriate `$type` (`architectural` or `non-architectural`) and `$topic`.
4. **Verify**: Decision recorded and adoption files updated.

### Step 2.6: Verify Adoption Compliance

1. **Check**: Is `/pair-capability-verify-adoption` installed?
2. **Skip**: If not installed, warn:

   > `/pair-capability-verify-adoption` is not installed — skipping adoption compliance check. Please manually verify code against adoption files.
   Move to Step 2.7.

3. **Act**: Compose `/pair-capability-verify-adoption` with `$scope` appropriate to the task.
   - Non-conformities reported → resolve via `/pair-capability-assess-stack` (tech-stack issues) or `/pair-capability-record-decision` (architectural gaps).
4. **Verify**: Adoption compliance confirmed or all non-conformities resolved.

### Step 2.7: Verify Quality

1. **Act**: Compose `/pair-capability-verify-quality` with `$scope = all`.
2. **Verify**: All quality gates pass. If any gate fails → **HALT**. Developer must fix before proceeding.

### Step 2.8: Task Completion

1. **Check**: Is the commit strategy `commit-per-task`?
2. **Skip**: If `commit-per-story`, continue to next task — return to Step 2.1. No inter-task confirmation.
3. **Act** (BLOCKING): Present task summary and **ask developer for confirmation BEFORE committing**:

   ```text
   TASK DONE:
   ├── Task:   T-N — [title]
   ├── Files:  [N added, N modified]
   └── Next:   T-N+1 — [title] (or "PR" if last task)
   ```

   Ask: _"Task T-N done. OK to commit or changes needed?"_

   **This confirmation is required for EVERY task** — commit-per-task exists precisely to give the developer a checkpoint between tasks.

4. **Verify**: Developer confirms. If changes needed → apply changes, re-run quality (Step 2.7), ask again.
5. **Act**: Stage and commit following the [commit template](../../../.pair/knowledge/guidelines/collaboration/templates/commit-template.md) (resolve override-first — [template resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/template-resolution.md)):

   ```text
   [#<story-id>] <type>: <task-description>

   - <specific changes>
   - Task: T-N — <task title>

   Refs: #<story-id>
   ```

6. **Verify**: Commit created.
7. **Act**: Update the PM tool story issue body:
   - Mark the completed task checkbox (`- [x] **T-N**`) in the **Task Breakdown** section.
   - Mark any **Definition of Done** checkboxes that are now factually satisfied by this task's work (e.g., "SKILL.md created", "template validated"). Leave unchecked items that require reviewer confirmation (e.g., "Code reviewed and merged").
8. **Act — persist progress**: If `/pair-capability-checkpoint` is installed, compose `/pair-capability-checkpoint $mode=write` to update `.pair/working/checkpoints/<story-id>.md` with the tasks now done. This keeps the checkpoint current so an interruption after this task resumes from the next pending one (Step 0.0). If `/pair-capability-checkpoint` is not installed, skip — git+PM state still supports the git-based resume.
9. **Check**: Is this the last task?
   - **Yes**: Move to Phase 3 (Closing: checkpoint + PR).
   - **No**: Return to Step 2.1.

## Phase 3: Closing — Checkpoint + Publish PR

The task cycle is done. The closing phase writes the checkpoint (handoff artifact) and composes `/pair-capability-publish-pr` inside a handoff-only subagent, so the PR is built on a guaranteed-clean context. implement never re-does the gate/PR/board logic here — it composes `/pair-capability-publish-pr` only.

### Step 3.1: Final Commit (if commit-per-story)

1. **Check**: Is the commit strategy `commit-per-story`?
2. **Skip**: If `commit-per-task`, all commits already exist. Move to Step 3.2.
3. **Act** (BLOCKING): Present summary and **ask developer for confirmation BEFORE committing**:

   ```text
   ALL TASKS DONE:
   ├── Tasks:  [list all T-N with titles]
   ├── Files:  [N added, N modified]
   └── Action: Commit all changes
   ```

   Ask: _"All tasks done. Ready to commit or changes needed?"_

4. **Verify**: Developer confirms. If changes needed → apply changes, re-run quality, ask again.
5. **Act**: Stage all changes and commit:

   ```text
   [#<story-id>] feat: <story-description>

   - <summary of all completed tasks>
   - Tasks: T-1, T-2, ..., T-N

   Refs: #<story-id>
   ```

6. **Verify**: Commit created with all changes.
7. **Act**: Update the PM tool story issue body:
   - Mark ALL task checkboxes (`- [x] **T-N**`) in the **Task Breakdown** section.
   - Mark all **Definition of Done** checkboxes that are factually satisfied by the implementation. Leave unchecked items that require reviewer confirmation (e.g., "Code reviewed and merged").

### Step 3.2: Write the Checkpoint (handoff artifact)

The checkpoint is the boundary artifact (R4.2) and the **input contract for `/pair-capability-publish-pr`** — the handoff document the subagent runs on.

1. **Act**: Compose `/pair-capability-checkpoint $mode=write` (pass `$story`). This creates/updates `.pair/working/checkpoints/<story-id>.md` with the five sections: story, branch, tasks done, key decisions, remaining todos.
2. **Verify**: The checkpoint file exists and captures the completed story state (all tasks done, branch, decisions). This file — not this session's memory — is what the PR is built from.
3. **Act — if `/pair-capability-checkpoint` is not installed**: synthesize the handoff inline (branch, tasks done, decisions, ACs) and pass it directly to `/pair-capability-publish-pr` as `$handoff`; note the absence in the output.

### Step 3.3: Publish the PR via a Handoff-Only Subagent (AC1)

The PR is produced on a **guaranteed-clean context**: a fresh subagent whose entire prompt is the handoff, nothing from this session. This is mechanical isolation (D23) — an **anonymous** subagent, **no named role**. A skill cannot `/clear` its own context (D7), so the reset is achieved by delegating to a subagent.

1. **Check**: Is subagent spawning available in this tool/environment?
2. **Act — primary path (subagent)**: Spawn an **anonymous subagent** whose prompt is the **handoff document only** — the checkpoint contents (or the path `.pair/working/checkpoints/<story-id>.md`) plus a single instruction: run `/pair-capability-publish-pr $story=<story-id> $handoff=.pair/working/checkpoints/<story-id>.md`. Pass **no other session context** — the subagent's context is the handoff and nothing else (clean context / fresh context reset within one execution, R4.1). The subagent runs `/pair-capability-publish-pr` (gate → PR → tags → ready-for-review → board) and returns the PR number/URL and board result.
3. **Act — degraded inline path (AC3)**: If subagent spawning is **unavailable** (tool/environment cannot spawn one — subagent spawning unavailable), do NOT skip the split: the checkpoint is already written (Step 3.2), then compose `/pair-capability-publish-pr` **inline** in the current session (`$story`, `$handoff` = the checkpoint). **Note the degradation in the output** (`Context: degraded — inline publish, no subagent reset`). Behavior is otherwise equivalent to the primary path.
4. **Act — dispatch the review (AC1 of #234; this session is the actor)**: `/pair-capability-publish-pr` Phase 5 registers the `pair-review` check as **pending** (merge blocked from t0) but cannot spawn the review subagent from inside the handoff subagent — nested dispatch is commonly forbidden — so it returns **`Review: review-dispatch-required — /pair-process-review $pr=<n>`**. When that signal comes back, **this top-level session** spawns the anonymous review subagent (a sibling of the publish subagent, not a nested one), prompt = the PR reference plus the bounded instruction:

   ```text
   Run /pair-process-review $pr=<number> $dispatched=true.
   Phases 1–5 only: verdict, `pair-review` check, PR-state synthesis.
   NEVER run Phase 6 and NEVER merge, whatever the verdict — the merge is a human act.
   ```

   Pass no authoring context (D23 isolation: the reviewer must not inherit the author's assumptions). If `/pair-capability-publish-pr` returns `Review: dispatched` instead (it ran at top level), there is nothing to do here. If this session cannot spawn the reviewer either, record `Review: pending — dispatch unavailable, run /pair-process-review <pr> in a fresh session`: the merge stays blocked, so the review is deferred, never skipped.
5. **Act — edge case (subagent fails mid-PR)**: The checkpoint remains valid. Re-invoking `/pair-process-implement` re-runs this closing phase; `/pair-capability-publish-pr` is **idempotent** — it detects an existing PR and updates it in place rather than opening a second one. Never open a second PR for the story.
6. **Verify**: A single ready-for-review PR exists (created or updated), its number/URL is captured for the output, and the review is either dispatched or explicitly recorded as deferred. A red quality gate inside `/pair-capability-publish-pr` propagates here as a **HALT** (no PR side effects) — implement does not create the PR itself.

Note: the checkpoint is **not** removed here — it must survive the review/fix loop so a re-review or fix round can resume from it. Cleanup happens at merge (Phase 4).

## Phase 4: Post-Review Merge

After code review approval (typically via `/pair-process-review`), re-invoke `/pair-process-implement` to merge and close — see [post-review-merge.md](./post-review-merge.md) for the merge-precondition, merge-commit, merge, parent-cascade, and checkpoint-cleanup steps (Steps 4.1–4.5) plus the completion output.

This is one of the flow's **two** merge paths (the other is `/pair-process-review` Phase 6), and both carry the **same** blocking precondition: the PR-state synthesis must be `ready-to-merge` (`merge_allowed` from [`pr-state.sh`](../../../.pair/knowledge/assets/pr-state.sh)), re-evaluated on the current head — an approving review alone is not the condition. See [pr-states.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/pr-states.md).

On story completion (Done, at merge), the checkpoint is no longer needed — `post-review-merge.md` Step 4.5 removes `.pair/working/checkpoints/<story-id>.md` so finished-story state never lingers (checkpoint lifecycle: written at the closing phase, cleaned up at merge).

## Output Format

At the closing phase (Phase 3):

```text
IMPLEMENTATION COMPLETE:
├── Story:      [#ID: Title]
├── Branch:     [feature/#ID-description]
├── Strategy:   [commit-per-task | commit-per-story]
├── Tasks:      [N/N completed]
├── Commits:    [N commits on branch]
├── Checkpoint: [.pair/working/checkpoints/<id>.md — written]
├── Context:    [clean — subagent handoff-only | degraded — inline publish, no subagent reset]
├── PR:         [#PR-number — URL — Created | Updated (from /pair-capability-publish-pr)]
├── Review:     [dispatched — subagent (clean context) | pending — dispatch unavailable, run /pair-process-review <pr>]
└── Quality:    [All gates passing]
```

At merge (Phase 4): see [post-review-merge.md](./post-review-merge.md).

## HALT Conditions

Implementation stops immediately when:

- **Checkpoint/branch divergence** (Step 0.0) — checkpoint names a branch the repo does not have; report and stop, do not guess a branch
- **Story not loaded or incomplete** (Phase 0)
- **Task specifications incomplete** (Step 2.2)
- **Quality gate failure** (Step 2.7) — developer must fix
- **New dependency rejected by /capability-assess-stack** (Step 2.4)
- **Commit template not found** (Step 2.8 / Step 3.1) — cannot commit without template
- **`/pair-capability-publish-pr` not installed** (Step 3.3) — implement composes the PR sequence, never re-implements it
- **Quality gate red inside `/pair-capability-publish-pr`** (Step 3.3) — propagates as implement's HALT; no PR side effects (the PR-template-not-found and gate HALTs live in `/pair-capability-publish-pr`)
- **PR state is not `ready-to-merge`** (Step 4.1) — `merge_allowed` fails: red gate, review not approved/still pending, or 🔴 without an explicit non-author human approval on the current head. Never bypass a required check to merge

On HALT: report the blocker clearly, propose resolution, wait for developer.

## Idempotent Re-invocation

See [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md). Re-invoking `/pair-process-implement` on a partially completed story is safe and expected — per-step:

1. **Checkpoint**: the opening-phase resume probe (Step 0.0) reads the checkpoint and jumps to the first pending task — never repeating completed tasks. When `/pair-capability-checkpoint` is absent, the git+PM resume below applies.
2. **Branch**: detects existing branch, switches to it.
3. **Commit strategy**: if commits already exist on branch, infer strategy from history.
4. **Tasks**: scans task checklist and git log to identify completed tasks. Skips them.
5. **PR**: the closing phase re-composes `/pair-capability-publish-pr`, which detects an existing PR and updates it in place — never a duplicate. A subagent that failed mid-PR is recovered this way (the checkpoint stays valid, the rerun is idempotent).
6. **Quality gates**: re-runs all gates (fast if already passing).
7. **Merge**: if a PR exists and its state synthesizes to `ready-to-merge`, proceeds directly to Phase 4 (merge); otherwise Phase 4's Step 4.1 HALTs with the unmet condition.

The skill resumes from the first incomplete step — never re-does completed work.

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (PM tool not accessible → ask the developer directly; adoption file missing → proceed with guideline defaults) for the standard scenarios. Additional cases:

- **Subagent spawning unavailable**: take the degraded inline path (Step 3.3) — checkpoint still written, `/pair-capability-publish-pr` composed inline, degradation noted in the output. Never skip the checkpoint/PR split. The review dispatch degrades the same way: `pair-review` stays pending (merge blocked) and the re-run instruction is recorded, never an inline self-review.
- **`/pair-capability-checkpoint` not installed**: skip the resume probe and the write step; resume from git+PM state (Idempotent Re-invocation) and synthesize the handoff inline for `/pair-capability-publish-pr`.
- **`/pair-capability-publish-pr` not installed**: **HALT** — implement composes the gate/PR/board sequence, it never re-implements it. Report the missing dependency.
- **`/pair-capability-assess-stack` not installed**: Warn on new dependency, continue without validation.
- **`/pair-capability-verify-adoption` not installed**: Warn, skip adoption compliance check.
- **No quality gate command**: Fall back to individual checks (lint, test, type check).

## Notes

- This skill **modifies files and creates git artifacts** (branches, commits) and **writes the checkpoint**. The PR itself is created/updated by the composed `/pair-capability-publish-pr` (in the subagent, or inline when degraded) — implement never re-implements PR creation.
- The **subagent's prompt is the handoff only** — the checkpoint, nothing from this session. Anonymous, no named role (mechanical isolation, D23); a skill cannot `/clear` its own context (D7), so the subagent provides the clean-context reset.
- Task iteration is sequential — each task completes its full cycle before the next begins.
- The developer can stop between tasks; re-invoke to resume — the opening-phase resume probe (Step 0.0) reads the checkpoint (see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md)).
- Single PR per story regardless of commit strategy.
- **Squash happens at merge** (Phase 4), not before PR creation. Individual commits are preserved on the branch during review.
