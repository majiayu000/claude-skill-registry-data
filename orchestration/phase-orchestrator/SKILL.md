---
name: phase-orchestrator
description: >-
  Orchestrates phase-based implementation plans using the host's todo tracker
  and subagents for implementation, review, validation, default phase commits,
  plan finalization, and a final end-to-end review. Delegates work through the
  companion phase-implementer, phase-reviewer, and phase-final-reviewer skills
  and consumes plans in the write-phase-plan format. Use when the user provides
  a plan, checklist, PRD, or phase document and asks for delegated multi-agent
  execution across phases.
license: MIT
---

# Phase Orchestrator

## Goal

Run a phase-based plan through a repeatable delegated workflow. The plan is
the source of truth, any PRD/spec is supporting context, and each phase should
move through orientation, implementation, validation, review, plan updates, and
commits by default.

Use this skill only when the user explicitly asks for delegated phase
orchestration, invokes this skill, or asks to implement a plan/checklist using
subagents.

## Companion Skills

This skill is the parent of a five-skill workflow:

- `write-phase-plan` — authors plans in the format this skill consumes best.
- `phase-implementer` — the delegated worker contract for implementing exactly
  one phase (Phase Loop step 2).
- `phase-reviewer` — the delegated worker contract for the review-and-fix pass
  on a completed phase (Phase Loop step 4).
- `phase-final-reviewer` — the delegated worker contract for the end-to-end
  review of the whole feature after all phases (Final Whole-Feature Pass).

Each worker skill carries that role's standing rules: single-phase or
single-pass scope, no-revert discipline, no-commit default, and the required
final-response format. The parent's prompt only needs to supply the per-run
context from the templates below.

How to dispatch a worker role depends on the host:

1. **Named custom agents.** If the host supports named custom agents or
   subagent types (Cursor custom agents, for example), prefer a dedicated
   agent per role whose definition is the matching companion skill's body.
2. **General subagent + installed skill.** Otherwise, launch a general-purpose
   subagent and instruct it to load and follow the matching installed
   companion skill by name.
3. **Inline rules.** If the subagent cannot load skills, paste the companion
   skill's standing rules into the prompt along with the per-run context.

## Host Mapping

- Use the host's todo tracker (`TodoWrite` in Cursor) for the in-chat
  orchestration state. Keep exactly one phase or orchestration step
  `in_progress`.
- Use the host's subagent or task tool (`Subagent` in Cursor) for delegated
  implementation, broad read-only exploration, review/fix passes, validation,
  and shell/git work when delegation is useful.
- Use fast read-only subagents (Cursor's `explore` type, where available) for
  broad codebase discovery before implementation.
- Use shell-focused subagents only for command-heavy validation or git
  operations.
- Respect the user's or host's model choice for workers. Pass a model
  explicitly only when the user requests a specific model for the run or for
  a specific worker.
- Use background subagents when the host supports them and independent
  read-only investigations can run in parallel.
- Do not assume subagents can be "closed"; inspect their final response and
  continue from the parent agent.
- Record every spawned subagent's ID in the main thread (alongside its phase
  in the todo/phase notes) when the host exposes one. Some hosts can resume a
  completed subagent by ID with its full context preserved (Cursor's task
  tool `resume` parameter). The user may ask for flows that reuse the same
  agent across the run — the same reviewer re-checking its own earlier
  findings, or an implementer revisiting its phase after review — and
  resuming beats a fresh dispatch there because the agent keeps everything it
  already learned. Keeping the IDs in thread history is what makes that
  possible later.
- Treat worker responses as structured handoffs. Require the result fields
  defined below so the parent can compare and combine results without
  carrying an unstructured transcript in context.
- Follow the host's normal tool rules: read tool schemas before unfamiliar
  calls, avoid destructive git commands, and never revert user-owned work.

## Inputs

Accept any of these as the plan source:

- A path to a plan, checklist, task breakdown, issue list, or phase document.
- A pasted plan in the conversation.
- A PRD or spec plus a request to derive implementation phases.

Optional inputs:

- PRD, design doc, ticket, issue, or acceptance criteria.
- Branch, commit style, validation commands, release constraints, or PR target.
- A stopping point such as "phase 2 only", "implementation only", or "no commits".

If the plan does not name phases, derive a conservative dependency-ordered phase
list and record that grouping in the plan or in the in-chat todos before
starting implementation.

The companion `write-phase-plan` skill defines the plan format this skill
consumes best (phase sections with status, scope, acceptance criteria,
validation commands, and an implementation log). A plan in that shape needs no
derivation step; prefer it when authoring a plan ahead of an orchestration run.

## Orchestrator Duties

Before spawning implementation workers:

1. Read the plan, optional PRD/spec, repo instructions, relevant contributor
   docs, and current git status.
2. Identify phases, dependencies, validation requirements, ownership boundaries,
   and whether the user opted out of the default commit workflow.
3. Create or update the in-chat todo plan with one active phase or orchestration
   step.
4. Note existing dirty worktree changes and treat them as user-owned unless a
   subagent clearly made them for this workflow.

During the run:

- Execute phases sequentially unless the plan marks phases as independent and
  their write scopes are disjoint.
- Give every subagent enough context to act safely: plan path, PRD/spec path,
  phase scope, prior phase results, repo rules, validation commands, ownership
  scope, dirty-worktree notes, and commit policy.
- Tell coding subagents they are not alone in the worktree, must not revert work
  they did not make, and must adapt to existing or concurrent changes.
- If new information invalidates the plan, update the plan and downstream phase
  items instead of silently following stale instructions.
- Keep the user updated at phase boundaries, before edits, during long
  validation, and whenever a blocker or plan deviation appears.

## Phase Topologies

The default topology for a phase is one implementer, then validation, then one
reviewer. During orientation, pick a different topology when the phase's shape
calls for it:

- **Batch migration** — one worker discovers the target items, parallel
  implementers each own a disjoint batch, then aggregate validation and one
  reviewer over the combined diff. For mechanical changes across many files.
- **Audit / sweep** — parallel read-only workers each inspect a slice, a
  separate verifier confirms each finding against the code, and the parent
  deduplicates and ranks before acting. For phases whose output is findings
  rather than edits.
- **Fix-until-green** — run the failing check, dispatch a fix worker, re-run,
  repeat. Stop when the check passes or two consecutive rounds make no
  progress; then escalate to the user or update the plan instead of looping.
- **Competing drafts** — for a high-stakes design decision inside a phase, two
  or three workers draft independently; the parent compares and adopts or
  synthesizes one before implementation proceeds.

Rules for every topology: parallel workers must have disjoint write scopes;
every loop needs an explicit stop condition (success, an attempt ceiling, or
no-progress detection); and results come back in the Worker Result Contract
shape so the parent can combine them without carrying transcripts.

## Phase Loop

Run this loop for each phase in dependency order.

### 1. Orient The Phase

- Re-read the phase section, acceptance criteria, and prior logs.
- Inspect git status and recent relevant commits.
- Choose the phase's topology (see Phase Topologies): the default single
  implementer, or a fan-out/loop shape when the phase calls for one.
- Update the todo tracker before spawning workers.

### 2. Implementation Worker

Spawn a worker under the `phase-implementer` contract to implement only the
active phase. The worker edits files directly. The parent orchestrator owns
commits by default unless the user opted out or explicitly delegated commits
to a worker.

After the worker returns:

- Note its agent ID in the phase's todo/notes for possible resumption.
- Inspect its summary, changed paths, validation results, blockers, and risks.
- Inspect git status and a focused diff.
- If implementation is incomplete because assumptions changed, send a bounded
  follow-up (resume the same worker by ID so it keeps its context) or update
  the plan before continuing.

### 3. Validation

Run or delegate affected validation for the phase. Use the repo's documented
commands when available, and include tests, lint, typecheck, migrations, or
browser checks when relevant.

If validation cannot run, record the exact command, blocker, and risk in the
phase notes or plan log.

### 4. Review And Fix Worker

Spawn a worker under the `phase-reviewer` contract after implementation and
initial validation. Note its agent ID alongside the phase.

Build the review prompt from primary evidence first: the plan and acceptance
criteria, the actual diff or commit range, repo rules, and validation results.
Do not lead with the implementer's summary. Include implementer notes only as
supplemental context for the reviewer to consult after independently inspecting
the change. This avoids anchoring the review to what the implementer believed it
changed.

The reviewer/fixer should:

- Review the phase against the plan, PRD/spec, repo rules, security, tenancy/data
  ownership, migrations, tests, and likely regressions.
- Patch concrete issues directly when bounded and low-risk.
- Leave review fixes uncommitted for the parent orchestrator to commit unless
  the user opted out or explicitly delegated commits to the reviewer/fixer.
- Report no-op clearly if no changes are needed.
- Report larger design issues with the exact plan changes needed.

### 5. Default Commit

Commit each completed phase by default unless the user requested "no commits",
"implementation only", or another no-commit constraint. Prefer the parent
agent's normal commit workflow unless a dedicated shell subagent is clearly
useful.

When committing:

- Follow the host's git safety rules.
- Inspect git status, full staged/unstaged diff, and recent log first.
- Stage only files that belong to the active phase.
- Run repo-required pre-commit validation and affected tests.
- Fix validation failures only when the fix is clearly in phase scope.
- Create a focused commit, or report an explicit no-op if there are no phase
  changes.

### 6. Plan Finalization

Update the plan or phase log for the active phase.

Record:

- Phase status: Done, Partial, or Blocked.
- Implementation summary and changed behavior.
- Validation commands and results.
- Review outcome.
- Commit SHAs, if commits were created.
- Deviations from the original plan.
- Downstream changes, remaining risks, and manual checks not performed.

Commit the plan/log update separately from implementation changes unless the
user opted out of commits.

## Final Whole-Feature Pass

After all requested phases are finalized:

1. Run aggregate validation appropriate for the whole feature.
2. Spawn a worker under the `phase-final-reviewer` contract to inspect the
   complete feature against the plan and PRD/spec.
3. If the final reviewer changed files, validate those fixes.
4. Commit final fixes or final plan/log updates unless the user opted out of
   commits.
5. Give the user a concise final summary with phase status, validation, commit
   SHAs if any, remaining manual gaps, and branch/worktree status.

Give the final reviewer the plan, acceptance criteria, complete diff or commit
range, and aggregate validation before phase summaries. Phase summaries are
supplemental and should be read only after an independent pass over the primary
evidence.

## Worktrees And Stacked PRs (Option For Complex Plans)

For a plan with sequenced phases plus parallel tracks — especially when the
user's checkout is on their own branch, is behind the default branch, or
carries dirty user-owned work — run the orchestration in dedicated git
worktrees and land each phase as a PR in a stack, instead of committing to the
user's checkout.

When to choose this mode:

- The plan names foundations that later phases build on, so phases must land
  as separate reviewable PRs in dependency order.
- Two or more tracks touch disjoint areas (for example API vs web) and can run
  as concurrent implementation workers without colliding.
- The current checkout is not a safe base: behind origin, on a personal
  branch, or dirty with user-owned edits.

Setup:

1. Choose worktree locations and branch names from the target repo's
   contributor docs and the user's rules — conventions differ (some require a
   specific in-repo directory, others forbid one). Only when no rule exists,
   default to a sibling directory such as `../<repo>-<feature>-work`.
2. Fetch and branch from `origin/<default-branch>`, not the local checkout:
   `git worktree add <worktree-path> origin/<default-branch> --detach`.
3. Make the worktree runnable before spawning workers: copy gitignored env
   files from the user's checkout, install dependencies, run the repo's
   build-before-measure steps (built packages, generated clients). Workers
   inherit a broken toolchain otherwise.
4. Create one additional worktree per concurrent track
   (`git worktree add <track-worktree-path> <base-branch> -b <track-branch>`)
   so parallel workers never share a checkout. Point each worker at its own
   worktree path in its prompt.
5. Remove temporary worktrees when done (`git worktree remove <worktree-path>`),
   and if the host can point its diff view at a worktree (Cursor's
   `SetActiveBranch`), do so, so the IDE diff follows the work.

Branching and stacking:

- One branch per phase, cut from the previous phase's branch when the phase
  depends on it: foundations first, then tracks stacked on the last foundation
  they need. Parallel tracks branch from the same base, not from each other.
- Commit each phase on its branch (orchestrator owns commits), push with
  `git push -u origin <branch>`, then open the PR with the `gh` CLI, setting
  `--base` to the parent branch for stacked phases and to the default branch
  for the stack root:
  `gh pr create --title "type(scope): subject" --body "$(cat <<'EOF' ... EOF)" --base <parent-branch>`.
- Record the PR number in the phase's todo item so the final summary can map
  phases to PRs.
- A schema/migration phase ships as its own PR based on the default branch;
  code that depends on it stacks on the migration branch (many repos require
  this — check the repo's contributor docs).

Keeping the stack healthy during the run:

- Check CI on every open PR after pushes (`gh pr checks <n>`); investigate
  failures with `gh api .../actions/jobs/<id>/logs` before assuming a worker's
  change caused them — a failure may predate the stack's base.
- If the default branch gains a fix the stack needs, merge it forward through
  the stack in order (base branch first, then each child), using a temporary
  worktree if the branches are checked out elsewhere. Never rebase or
  force-push pushed branches.
- When an inner PR merges early, GitHub retargets its children automatically;
  verify with `gh pr view <n> --json baseRefName`.
- Follow the repo's stack-collapse rules before final review if it has them
  (prove containment with `git merge-base --is-ancestor` before closing inner
  PRs; the survivor merges, never closes).

The final summary must report the stack shape: which PRs are open, their base
branches, merge order, CI state, and which worktrees were created or removed.

## Prompt Templates

Adapt these to the repo and phase. These templates are the per-invocation
context to hand each worker — the standing role rules (scope discipline,
no-commit default, response format) live in the companion skills, so the
prompt's job is the run-specific facts. If the worker runs as a named custom
agent built from the companion skill, the template alone is enough; if it runs
as a general subagent, prepend an instruction to load and follow the matching
companion skill, or paste that skill's standing rules above the template.
When resuming a prior worker by ID instead of dispatching fresh, send only
what changed since its last response; it retains the rest.

### Worker Result Contract

Every worker response must use these headings in this order:

1. `Outcome` — concise result or explicit no-op.
2. `Changed files` — files the worker changed, not every file it inspected.
3. `Behavior or findings` — implemented behavior or review findings and fixes.
4. `Validation` — exact commands or checks and their results.
5. `Downstream impact` — plan changes, follow-up work, or `None`.
6. `Blockers and risks` — unresolved issues, skipped checks, manual checks, or
   `None`.

Keep `Changed files` proportional. List paths individually when the list is
short. When it would become a long, low-signal inventory, group paths by
module/directory, give counts, and name only high-signal or exceptional files.
Label a grouped list as a summary rather than exhaustive; the parent inspects
git status and the diff for the authoritative file list.

### Implementation Worker (`phase-implementer`)

```text
You are implementing phase {phase_name} of this plan.

Context:
- Plan: {plan_path_or_summary}
- PRD/spec: {prd_path_or_summary_or_none}
- Prior phase commits and notes: {prior_phase_summary}
- Repo instructions and validation requirements: {repo_rules_summary}
- Current dirty-worktree notes: {dirty_worktree_summary}

Ownership:
- You own {owned_files_or_modules}.
- Other agents or the user may have changes in the worktree. Do not revert work
  you did not make. Adapt to existing changes.

Task:
- Implement only phase {phase_name}.
- It is acceptable to deviate from the plan when the codebase shows a better
  path, but document the reason and downstream impact.
- Commit policy: {commit_policy}. The parent orchestrator commits by default;
  do not commit from this worker unless this explicitly delegates commit
  authority to you.

Validation:
- Run {affected_tests_or_checks} where practical.
- If a required check is not practical, explain why.

Final response:
- Use the Worker Result Contract headings in order.
- In `Behavior or findings`, describe the behavior implemented.
```

### Review And Fix Worker (`phase-reviewer`)

```text
Review and fix phase {phase_name}.

Context:
- Plan: {plan_path_or_summary}
- PRD/spec: {prd_path_or_summary_or_none}
- Change under review: {commit_range_or_diff_scope}
- Validation evidence: {phase_validation_results}
- Repo rules: {repo_rules_summary}
- Commit policy: {commit_policy}
- Supplemental implementer notes: {phase_result}

Task:
- First inspect the plan, acceptance criteria, and actual change. Form an
  independent assessment before reading the supplemental implementer notes.
- Review the phase against acceptance criteria, repo conventions, security,
  tenancy/data ownership, migrations, and test coverage.
- Patch concrete issues directly when bounded and low-risk.
- Do not commit from this worker unless the commit policy explicitly delegates
  commit authority to you.
- If no changes are needed, say so clearly.
- If the plan should change, describe the exact plan and downstream updates.

Final response:
- Use the Worker Result Contract headings in order.
- In `Behavior or findings`, report findings fixed, the no-op result, and any
  findings not fixed.
```

### Final Reviewer (`phase-final-reviewer`)

```text
Review the entire feature after all requested phases.

Context:
- Plan: {plan_path}
- PRD/spec: {prd_path_or_none}
- Complete change: {commit_range_or_diff_scope}
- Final validation results so far: {validation_summary}
- Supplemental phase results: {all_phase_results}

Task:
- First inspect the plan, acceptance criteria, and complete change. Form an
  independent assessment before reading the supplemental phase results.
- Review end-to-end behavior against the plan and PRD/spec.
- Look for integration bugs, missing acceptance criteria, stale plan state,
  validation gaps, unsafe data ownership, and regressions across phase
  boundaries.
- Patch only concrete issues that are safe to fix now.
- Do not commit from this worker unless the commit policy explicitly delegates
  commit authority to you.

Final response:
- Use the Worker Result Contract headings in order.
- In `Behavior or findings`, report findings fixed, the no-op result, and any
  findings not fixed.
```

## Plan Conventions

Prefer a stable plan structure:

- Phase status: Not started, In progress, Done, Partial, or Blocked.
- Implementation log entries with date, phase, summary, validation, review
  result, commits if any, deviations, and remaining risks.
- Downstream changes called out where the original phase plan changed.
- Manual checks listed separately from automated checks.

Do not let the plan become ceremonial. If implementation or review shows that a
task is obsolete, split, merged, or better solved differently, update the plan
and explain why.

## Git And Validation Rules

- Follow repo contributor instructions before every commit.
- Use non-interactive git commands.
- Stage intentionally and avoid unrelated dirty files.
- Never use destructive git commands unless the user explicitly requested them.
- Keep implementation, review fixes, plan finalization, and final feature fixes
  distinct when committing.
- For multi-phase plans that should land as reviewable PRs rather than commits
  on the user's checkout, use the worktree + stacked-PR mode above.
- If required validation cannot run, record the command, blocker, and risk in
  both the subagent result and the plan log.
