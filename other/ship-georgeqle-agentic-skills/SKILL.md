---
name: ship
description: Ship current work (update docs, commit, push, deploy) and optionally plan the next step
type: shipping
version: v0.12
argument-hint: "[--no-plan] [--no-deploy] [--save-conversation] [--save-all-conversations]"
invocation: orchestrator
---

# Ship

Ship current work, commit, push, deploy, and plan the next step. If `$ARGUMENTS` contains `--no-plan`, skip planning. If `$ARGUMENTS` contains `--no-deploy`, skip deployment. If `$ARGUMENTS` contains `--save-conversation`, save the current conversation to `conversations/`. If `$ARGUMENTS` contains `--save-all-conversations`, export all past conversations to `conversations/`.

## Process

### 1. Check if there's anything to ship
Run `git status` and `git diff --stat`.
- If the working tree is clean AND there are no unpushed commits: skip to step 3 (or stop if `--no-plan`).
- If there are changes: continue to step 2.

### 1b. Pre-ship error check
Before shipping, check for pre-existing errors so they get fixed and included in this step's commit.

a) **Check conversation context first.** If lint, typecheck, or test output already exists in the current session (e.g., from a TDD run step or plan-mode execution), use that output. Do NOT re-run commands whose results are already available.

b) **Run only what's missing.** For any validation category (lint, typecheck, tests) that was NOT already run this session, find and run the project's commands. Check these sources:
   - `CLAUDE.md` — look for lint, typecheck, or test commands
   - `Makefile` / `Justfile` — look for `check`, `lint`, `typecheck`, `test` targets
   - `package.json` — look for `lint`, `typecheck`, `check`, `test` scripts
   - `pyproject.toml` / `setup.cfg` — look for tool configs (ruff, mypy, pytest)
   - `Cargo.toml` — `cargo check`, `cargo clippy`
   - If no validation commands are found and no prior output exists, skip this step.

c) **Fix errors.** If any pre-existing errors are found (from prior session output or fresh runs):
   - Fix them.
   - Re-run only the previously-failing commands to confirm the fixes.
   - These fixes will be committed alongside the current work in step 2d (or as a separate commit if the fixes are unrelated to the current feature).

d) **If errors can't be auto-fixed** (e.g., requires user decision, third-party dependency issue), **STOP. Do not ship.** Report the errors clearly to the user and ask how they want to proceed. Never commit or push code with known build/lint/type/test failures.

### 1c. Quality gate for non-trivial mutations
   - Apply `docs/quality-gate-contract.md` when the work to ship changes source code, scripts, configuration, schemas, generated runtime assets, deploy behavior, workflow policy, validation rules, command surfaces, or multiple files.
   - Build a ship manifest from the exact diff and unpushed commits that will be included in the shipping boundary. The manifest must include: User goal, Changed files, Per-file purpose, User-goal mapping, Tests run, Skipped tests, Adversarial review, Residual risk, Rollback note, and Next command. The `Next command` field must use Claude slash-command syntax; for a completed `/ship` run, default to `/exec` unless project state names a more specific next route. Do not leave `Next command` blank unless all planned work is genuinely complete, in which case use `none`.
   - For non-trivial source changes, run a targeted `quality-sweep audit`, `/code-review`, configured review lane, or explicitly justified equivalent adversarial review before commit/push. Fix findings or record accepted residual concerns in the manifest.
   - Final output must distinguish executable verification from documentation-only or task-only checks. Documentation/task checks can support source changes, but cannot be the only proof for non-trivial source mutations.
   - If the tree contains unrelated pre-existing changes, the manifest must separate included files from untouched files and explain why the ship boundary is safe. If that cannot be proven, stop instead of shipping.
   - **Pack install artifact boundary:** Treat `.agents/project.json` as the committed project designation. When pack configuration changed, include `.agents/project.json` in the shipping boundary. Treat `.claude/skills/**` and `.codex/skills/**` as generated local skill roots recreated by `scripts/pack.sh refresh`; generated skill roots must not be staged or committed. If those roots are untracked, leave them uncommitted and report them as generated local artifacts. If any path under those roots is already tracked or modified as a tracked file, stop unless the current task explicitly includes repository hygiene to untrack or ignore generated skill roots.
   - If the user corrected the agent during the work being shipped, the pre-commit ship manifest must prove the exact shipping boundary includes a `tasks/lessons.md` update for the current correction. Treat the correction as repeatable unless the manifest proves otherwise.

### 1d. Public Skills Catalog Freshness
If the shipping boundary creates, deletes, renames, or changes behavior/metadata in any tracked `SKILL.md` or `PACK.md`, refresh the public skills catalog export before commit:

- `node scripts/generate-skills-catalog-export.mjs`
- `scripts/validate-skills-catalog-export.sh`

Include changed `exports/skills-catalog/v1/**` artifacts in the same shipping boundary. The Skills Showcase lives in the separate `agentic-skills-showcase` repository and imports this public export; do not run Showcase app generators, Next.js builds, or website asset refreshes during normal `agentic-skills` shipping. If a skill change needs curated website copy, record the follow-up for the Showcase repo instead of editing app files here.

### 1e. Ship manifest route convention
When writing a ship manifest, summary, task review note, or final response with a `Next command` field, use Claude slash-command syntax. For a completed `/ship` run, the default executable handoff is `/exec` unless project state names a more specific next route. Do not leave `Next command` blank unless all planned work is genuinely complete, in which case use `none`.

### 2. Ship the work
a) Read the project's CLAUDE.md to understand current progress.
b) Update `tasks/todo.md` — mark completed items as done (check off steps and milestone criteria).
c) Update `tasks/history.md` — append a brief record of what was accomplished this session (phase/step completed, key changes). Create it if it doesn't exist.
d) If `tasks/todo.md`, `tasks/roadmap.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, or `tasks/recurring-todo.md` changed and `scripts/audit-task-docs.mjs` exists, run `node scripts/audit-task-docs.mjs` and fix any failures before final next-work routing.
e) **Save conversation (skip if `--save-conversation` and `--save-all-conversations` both absent):**
   Run `scripts/save-conversation.sh` to export the current Claude Code conversation as a markdown file in `conversations/`. If the script is not found or fails (e.g., not running in Claude Code, no local conversation history), warn and continue — do not block shipping. Include the generated file in the shipping boundary.
   - If `$ARGUMENTS` contains `--save-all-conversations`, run `scripts/save-conversation.sh --all` instead.

f) Ship the changes using the `/commit-and-push-by-feature` compatibility workflow and `docs/github-delivery-contract.md`:
   - Group changes into logical feature/function buckets.
   - Use conventional commit messages.
   - Ensure or reuse the linked issue and issue-backed non-primary branch before committing.
   - Publish the branch and create or update one ready pull request; do not merge it.

### 3. Deploy (skip if `--no-deploy`)

If the ready pull request is not merged into the current primary branch, defer deployment and route to explicit review/`github-pr merge`. Never deploy development state from the work branch.
After shipping, deploy only when the project has an explicit manual deploy contract.

a) **Check for deploy contract.** Look for `deploy.md` or `tasks/deploy.md`.
   - If neither file exists, skip deploy and report `Deploy skipped: no explicit manual deploy contract (deploy.md or tasks/deploy.md)`.
   - If a deploy contract exists, continue.

b) **Invoke `/deploy`** (release-ops pack) targeting the default environment (staging).
   - Pass the deploy contract context to `/deploy` (release-ops pack).
   - Skip ledger recording and staleness reporting — those are for standalone `/deploy` (release-ops pack) invocations only.
   - If `/deploy` (release-ops pack) reports failure, report the error. Do not retry.

### 4. Plan the next step (skip if `--no-plan`)

**Prerequisite:** If neither `tasks/todo.md` nor `tasks/roadmap.md` exists, or if no uncompleted steps remain, there is no plan to continue. Run `/roadmap` to scan task pipeline health and recommend the next context-aware action (stale todo, missing steps, etc.). Then stop (do not enter plan mode).

a) **Migration check:** If `tasks/roadmap.md` does not exist but `tasks/todo.md` contains multiple `## Phase` headers, migrate: copy `tasks/todo.md` → `tasks/roadmap.md`, then trim `tasks/todo.md` to just the current phase (first phase with unchecked steps). Commit with `chore: migrate to roadmap.md + todo.md split`.
b) Read only the current active task/phase in `tasks/todo.md` to identify the next uncompleted step. Do not select unchecked boxes from completed sections, historical roadmap notes, reconciliation reports, manual/record/recurring advisory files, or any roadmap section not explicitly promoted into the current todo surface.
b2) If `tasks/record-todo.md` or `tasks/recurring-todo.md` exists, count unchecked advisory items for status only. Do not select them as next work.
c) **Check if the current phase is complete** (all steps checked, milestone criteria met):
   - If **YES — Phase transition:**
     1. Archive the completed phase: copy `tasks/todo.md` → `tasks/phases/phase-N.md` (create `tasks/phases/` if needed). Fill in the "On Completion" section.
     1b. If `tasks/manual-todo.md` exists, inspect unchecked items before advancing phases:
         - If any unchecked `_(blocks: Step N.X)_` items still apply to the completed phase, stop. Do NOT archive the manual task file, mark the phase complete, or advance to the next phase unless the user explicitly overrides the blocker.
         - Unchecked `_(after: Step N.X)_` items are non-blocking follow-up tasks. Archive them with the phase and warn the user that they remain incomplete.
     2. Check off the phase milestone in `tasks/roadmap.md`.
     3. Copy the next phase from `tasks/roadmap.md` → overwrite `tasks/todo.md`.
     3b. Extract the next phase's manual tasks (from `**Manual Tasks:**` in `tasks/roadmap.md`) into a fresh `tasks/manual-todo.md`. If the next phase has no manual tasks, delete `tasks/manual-todo.md` if it exists.
     4. If no more phases remain, run `/roadmap` to recommend the next action based on project state. Then stop (do not enter plan mode).
     5. **Just-in-time planning:** **You MUST invoke `/plan-phase` for the new phase** — do NOT tell the user the phase is "deferred" or ask them to run `/plan-phase` manually. A phase without implementation steps is NOT deferred; it simply hasn't been decomposed yet (only items under the `## Deferred / Future Work` heading in the roadmap are actually deferred). This auto-invocation generates implementation steps, the phase `### Execution Profile`, and file-level detail using the full context of what was learned during prior phases. The roadmap only stores strategic outlines — implementation detail is generated when a phase is started, not upfront.
   - If **NO:** find the next uncompleted step within the current phase.
d0) **Skip no-op verification handoffs:** If the next uncompleted step is verification-only/no-op-only (for example, "refactor if validation exposes drift", "verify", "run validation", or `Files: no source changes expected`) and the current session already has passing validation evidence for the same scope, do not write a clear-context plan for it. Mark the step complete in `tasks/todo.md`, record the no-op result in the review/history, ship those task-doc updates, then continue selecting the next substantive step. If verification found failures, drift, warnings needing judgment, or source edits are required, treat that remediation as substantive work and plan it normally.
d) Write a **self-contained** implementation plan for the next step into `tasks/todo.md`. This plan must be complete enough that a fresh context can execute it by reading only CLAUDE.md and `tasks/todo.md`. Include:
   - What needs to be built/changed
   - Which files will be affected (full paths)
   - Key technical decisions or risks
   - Relevant context from the current session (gotchas, patterns established, conventions used)
   - If test strategy is `tdd`: which tests to write first and what they should assert
   - If test strategy is `tests-after`: note that tests will be written in the Green step
   - The current phase's `### Execution Profile`, including whether the next execution is serial, research-only, review-only, implementation-safe, or agent-team
   - Acceptance criteria: how to verify the step is done
   - **Ship-one-step handoff contract:** the next clear-context implementation session must implement only this step, validate it, then run `/ship` when done.
e) Include task-document changes in the same issue-backed branch and ready pull-request boundary via `/commit-and-push-by-feature`.

### 5. Enter plan mode (skip if `--no-plan`)
**YOU MUST run the full plan-mode approval sequence.** This is not optional. A next-step plan being written or already present is not a completed `/ship` unless `--no-plan` is set or the approval UI is presented successfully.

1. Call `EnterPlanMode`. This enters plan mode.
2. In plan mode, write the plan file to the path specified by the plan-mode system prompt. Keep it brief: name the next step, state that the full implementation plan is in `tasks/todo.md`, and include the ship-one-step handoff: "implement only this step, validate it, then run `/ship` when done." Do not explore the codebase or perform multi-phase planning; this is a pass-through to present the approval UI.
3. Call `ExitPlanMode`. This presents the approval UI where the user can choose "clear context and implement" to start a fresh context that reads `tasks/todo.md` and implements the plan.

`EnterPlanMode` alone does not present the approval UI. `ExitPlanMode` must only be called after `EnterPlanMode` has succeeded and the session is visibly in plan mode. If Claude Code reports "You are not in plan mode", do not retry `ExitPlanMode`; call `EnterPlanMode` first, then write the brief pass-through plan and call `ExitPlanMode`.

There is no normal final-answer checkpoint between writing/finding the next plan and presenting the approval UI. If the prior tool call was interrupted after the plan was written, resume by calling `EnterPlanMode` rather than summarizing and stopping, unless the session is already visibly in plan mode.

### 6. Plan-mode approval content (skip if `--no-plan`)
When writing the brief pass-through plan in step 5, include a short ship summary (2-3 lines max) and **present the execution plan** to the user. Summarize the plan that was written to `tasks/todo.md` in step 4d:
- What was shipped (if anything)
- Deploy status (if deployed or skipped)
- Test status — **explicitly state whether any failing tests are expected (red phase: tests written before implementation) or unexpected (regressions/bugs that need fixing)**
- Manual tasks — pending count from `tasks/manual-todo.md` (if it exists), note any that block upcoming steps
- Advisory tasks — pending record/recurring counts from `tasks/record-todo.md` and `tasks/recurring-todo.md` if they exist
- What needs to be built/changed
- Which files will be created or modified (full paths)
- The approach (e.g., test strategy, key technical decisions)
- **Ship-one-step handoff contract:** after approval, implement only this step, validate it, then run `/ship` when done.
- Any decisions or trade-offs the user should weigh in on

This gives the user something concrete to review before selecting "clear context and implement".

## Next-Step Routing

After writing the next-step plan and before entering plan mode (or before stopping when `--no-plan` is set), identify the next concrete work item from project state, then recommend the executor and invocation.

Output exactly two lines beyond the normal ship summary:

- **Next work:** <specific task name, manual blocker, verification gap, or "none">
- **Recommended next command:** <one command or route>

Rules:

- Make the next work item primary. Derive it from the next-step plan, `tasks/todo.md`, `tasks/manual-todo.md`, deploy status, validation gaps, smoke-test gaps, or the absence of remaining work. Do not use agent mode itself as the next work item.
- Treat `tasks/todo.md` as the only executable current-task surface. Historical roadmap entries and unchecked advisory/manual/record/recurring items are reconciliation candidates, not next executable work, unless the current active todo section explicitly promotes them.
- If no remaining work exists — no unchecked steps in `tasks/todo.md`, no phases remaining in `tasks/roadmap.md`, no pending manual blockers, no validation gaps, and no deploy failures — emit `**Next work:** none` and `**Recommended next command:** none — all planned work is complete`. Do not force a route to `/exec` when there is genuinely nothing to execute.
- Never recommend `/ship`, `/ship --no-deploy`, or `/ship --no-plan` as the routine next command from a completed `/ship` run. `/ship` packages current work; after it completes, hand off to the next executable route such as `/exec`, check `.agents/project.json.enabled_packs` for `agent-work-admin` — if `agent-work-admin` is not enabled, recommend `npx skillpacks install agent-work-admin` from the project shell first; if `agent-work-admin` is enabled, recommend `/roadmap`, check `.agents/project.json.enabled_packs` for `guided-walkthrough` — if `guided-walkthrough` is not enabled, recommend `npx skillpacks install guided-walkthrough` from the project shell first; if `guided-walkthrough` is enabled, recommend `/guide`, or check `.agents/project.json.enabled_packs` for `docs-health` — if `docs-health` is not enabled, recommend `npx skillpacks install docs-health` from the project shell first; if `docs-health` is enabled, recommend `/reconcile-dev-docs fix tasks` based on project state. Recommend `/ship` again only when shipping failed before commit/push or when the next concrete work is explicitly to retry an incomplete shipping operation.
- Use `./scripts/agent-mode.sh` only to choose command text. If it is missing, unset, or non-zero, infer routing from the current invocation and task type instead of asking the user to select a mode by default.
- Normalize copied task routes to Claude syntax before final output. If `tasks/todo.md`, `tasks/roadmap.md`, benchmark reports, or prior handoffs contain Codex dollar commands for base skills (for example `$exec`, `$ship`, `$roadmap`, `$guide`, `$reconcile-dev-docs`), treat them as task identifiers, not final command text. Convert the final `Recommended next command` to the equivalent Claude `/...` route unless the next action is explicitly a Codex handoff — check `.agents/project.json.enabled_packs` for `agent-bridge` — if `agent-bridge` is not enabled, recommend `npx skillpacks install agent-bridge` from the project shell first; if `agent-bridge` is enabled, recommend `/delegate $exec`.
- Inference defaults:
  - Hybrid execution handoff → check `.agents/project.json.enabled_packs` for `agent-bridge` — if `agent-bridge` is not enabled, recommend `npx skillpacks install agent-bridge` from the project shell first; if `agent-bridge` is enabled, recommend `/delegate $exec`.
  - Claude-only or orchestration-heavy work → recommend `/exec`.
  - Codex-only execution → recommend `$exec`.
  - External human-only manual work (browser/auth/DNS/service dashboard work with no reliable authenticated CLI/API path, paid account setup, real-device checks, or production smoke-test work needing human sign-off) → check `.agents/project.json.enabled_packs` for `guided-walkthrough` — if `guided-walkthrough` is not enabled, recommend `npx skillpacks install guided-walkthrough` from the project shell first; if `guided-walkthrough` is enabled, recommend `/guide` — or a Claude-guided manual step rather than `/exec`.
  - Agent-executable work misfiled in `tasks/manual-todo.md`, task-doc bookkeeping, stale `tasks/manual-todo.md` cleanup, or reconciliation against repo/history reality → check `.agents/project.json.enabled_packs` for `docs-health` — if `docs-health` is not enabled, recommend `npx skillpacks install docs-health` from the project shell first; if `docs-health` is enabled, recommend `/reconcile-dev-docs fix tasks` — promotion to `tasks/todo.md`, or a direct dev-doc audit, not `/guide`.
- Only present multiple commands when the ambiguity materially changes execution safety or there are equally valid next work items. Otherwise choose the best route and mention degraded mode lookup inline.
- Final route contract: completed `/ship` runs must not self-route back to `/ship`; route to `/exec` or a more specific next actionable skill unless shipping itself failed before commit/push, or emit `none` when all planned work is genuinely complete.

## Constraints
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, include `npx skillpacks install <pack-name>` from the project shell as the prerequisite.
- **Fix unrelated issues:** If any step surfaces errors, warnings, or lint issues — even ones unrelated to the current work — investigate and fix them before continuing. Commit these fixes separately with a descriptive message (e.g., `fix: resolve unused import warning in auth.ts`).
- Do NOT write plans into CLAUDE.md. CLAUDE.md is for project conventions and config only.
- `tasks/roadmap.md` is the source of truth for the full phased plan. `tasks/todo.md` holds only the current phase.
- Do NOT create `tasks/todo.md` from scratch — if it doesn't exist and there's no roadmap, suggest discovery skills instead.
- Do NOT re-read files you've already read this session. Use what's in context.
- Do NOT explore the codebase extensively for planning. Keep context footprint minimal.
- If the tree is clean and the next step plan already exists in `tasks/todo.md`, skip straight to step 5.
- Do not enter plan mode solely for verification-only/no-op-only work whose commands already passed in the current session and whose expected source changes are none. Record the completed verification/no-op result and advance to the next substantive item.
- Unless `--no-plan` is set or a documented blocker stops planning, do not end the turn after writing, finding, or shipping the next-step plan; run the full `EnterPlanMode` -> pass-through plan -> `ExitPlanMode` approval sequence.
- The plan shown to the clear-context implementation session must include the ship-one-step handoff: "implement only this step, validate it, then run `/ship` when done." The plan-mode prompt is the human approval boundary that prevents a runaway loop.
- The plan must be actionable, not vague. Include specific file paths, technical details, and the current phase's `### Execution Profile`.
- Do not execute or plan from `tasks/record-todo.md` or `tasks/recurring-todo.md`; report their counts only unless an item has been promoted into `tasks/todo.md`.
- When task docs changed, do not finish with a next-work recommendation until `node scripts/audit-task-docs.mjs` passes, if that script exists.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
