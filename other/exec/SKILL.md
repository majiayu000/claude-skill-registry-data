---
name: exec
description: "Execute the next incomplete step (or full phase with --phase), ship the result, and prepare the next step"
type: execution
version: v0.8
argument-hint: "[--phase] [--execute-approved]"
invocation: orchestrator
---

# Exec

Invoke as `$exec`.

Identify the next incomplete unit of work from the phased plan, build an execution plan, implement it, ship the result, and prepare the next step. By default, executes only the next single incomplete step. If `$ARGUMENTS` contains `--phase`, execute the next full phase and ship once at the end.

## Process

1. **Migration check:** If `tasks/roadmap.md` does not exist but `tasks/todo.md` contains multiple `## Phase` headers, migrate: copy `tasks/todo.md` → `tasks/roadmap.md`, then trim `tasks/todo.md` to just the current phase (first phase with unchecked steps). Commit with `chore: migrate to roadmap.md + todo.md split`.
2. Read `tasks/todo.md` — this contains the current phase's steps. Reference `tasks/roadmap.md` only if cross-phase context is needed.
3. Read `CLAUDE.md` for project conventions.
3a. Read `docs/codex-accountable-agent-workflow.md` and act as Sol for every non-trivial mutation.
3b. If `tasks/record-todo.md` or `tasks/recurring-todo.md` exists, count unchecked advisory items for status only. Do not select them as next work.
4. Find the next incomplete item:
   - Look for the next phase with an unchecked milestone.
   - If `$ARGUMENTS` contains `--phase`, scope the full next incomplete phase.
   - Otherwise, find the next unchecked `- [ ]` step within that phase.
   - **If the phase has acceptance criteria but no implementation steps** (no `### Tests First` or `### Implementation` section): invoke `$plan-phase` for this phase to generate implementation steps and file-level detail before proceeding.
5. **Check `tasks/manual-todo.md`** (if it exists) for unchecked items with `_(blocks: Step N.X)_` matching the current step. If a blocking external human-only manual task is found, stop and tell the user: "**Manual task blocking this step:** [task]. Complete it before proceeding, or run `$guide` for step-by-step instructions." Do NOT execute the step unless the manual task is completed or the user explicitly overrides the blocker. If the unchecked item is task-doc bookkeeping, reconciliation, or agent-executable work (repo edits, SDK wiring, local commands, tests, audits, generated assets, or authenticated CLI/API work), do not route it to `$guide`; route it to `$reconcile-dev-docs fix tasks`, promote it to `tasks/todo.md`, or handle it as a direct dev-doc audit.
6. Research what is needed — read only the files relevant to the step.
6a. For user-facing product, SaaS, marketplace, dashboard, internal tool, product-experience work, or substantial new feature work, check whether the selected step would introduce durable database/storage, auth, payments, analytics, deployment, admin tooling, multi-tenancy, or production observability before clickable prototype experiments have calibrated one journey. If the current plan or user instruction does not explicitly authorize that infrastructure, stop and re-plan the step around a separate prototype/experiment phase using fake, fixture, local, or in-memory data. When multiple workflows, layouts, densities, copy approaches, navigation models, or interaction patterns remain plausible, prefer multiple small experiment routes such as `/experiments/<variant>` over one merged implementation. Record the deferred infrastructure and the evidence needed to promote it later.
6b. Read the current phase's `### Execution Profile` from `tasks/todo.md` if present:
   - If missing, treat the phase as `serial`.
   - Use the profile only for the current step or scoped phase; do not plan ahead.
   - If the profile's `Parallel mode` is `agent-team`, stop before implementation unless the active workflow can run branch-backed isolated worktrees or a dedicated agent team. Each write lane must have a non-primary GitHub `Branch:` value and the phase must include a consolidation/PR review step before final validation or shipping.
   - Read `Accountability topology` independently. Default non-trivial mutations to `sol-terra`; use `sol-luna-terra` only for one to three decision-complete, disjoint Luna write lanes; reserve `sol-only-trivial` for the convention's trivial exemption.
6c. **`--execute-approved` branch** (if `$ARGUMENTS` contains `--execute-approved`):
   - Reject `--execute-approved --phase` — approved packets target one step, not a full phase.
   - Exec `scripts/approved-plan.sh check`.
   - On `ok`: run `scripts/approved-plan.sh consume`, log `Approved packet consumed: Phase X / Step Y (approved_at=…).`, then skip steps 7 and 8 and jump to step 9 (execute).
   - On non-zero exit: relay the single-line reason to the user, run `scripts/approved-plan.sh mark-stale`, then fall through to steps 7–8 (standard plan + implicit approval). Never auto-retry.
   - Requires `jq` for the write path. If `jq` is absent, `scripts/approved-plan.sh consume` dies with `ERROR: jq required for write operations. Install with: brew install jq (macOS) or apt install jq (Debian/Ubuntu).` (see `require_jq_write` at `scripts/approved-plan.sh:21`); `check` may surface the same message via its write-path preflight. Relay the message verbatim and stop — no `jq`-free fallback exists. If the check prints a `mode-mismatch` reason (resolved mode is `claude-only`), treat it as a user error and stop.
7. Present the execution plan to the user:
   - What the step requires
   - Which files will be created or modified
   - The approach and any trade-offs
   - Whether the execution profile will run serially, use read-only research lanes, use review lanes, or use disjoint write lanes
   - For `agent-team`: the planned lane branches and the consolidation/PR review gate
8. Use `update_plan` to track the proposed work, then execute by default. Do not ask for routine approval after presenting a `$exec` plan; the user's `$exec` invocation is implicit approval for the next planned step or scoped phase. Ask a concise confirmation question only when the work requires a separate safety decision: destructive commands, production deploys, paid/external account actions, credential or secret handling beyond the project contract, accepting an execution-profile downgrade, proceeding despite a blocker, or materially changing the planned scope.
9. Execute the plan:
   - Apply the execution profile:
     - `serial`: execute normally.
     - `research-only`: launch read-only subagent lanes first when the active environment permits subagents, synthesize their findings, then implement in the main agent.
     - `review-only`: implement in the main agent, then launch review subagent lanes before final validation.
     - `implementation-safe`: launch write subagent lanes only when every write lane has disjoint `Owns` paths and explicit `Must not edit` boundaries; otherwise downgrade to `research-only` or `serial` and report the downgrade.
     - `agent-team`: do not execute in one shared local tree. Use separate GitHub branches for every write lane, require branch + commit SHA + PR URL deliverables, and run the planned consolidation/PR review step before integration. If branch push or PR review cannot be performed, stop and report the blocker.
   - If it is a tests-first step: write the failing tests, run them to confirm they fail.
   - If it is an implementation step: implement it, run existing tests for regressions.
   - If it is a verification step: run all tests, fix any failures. If validation is clean and a following cleanup/refactor step is explicitly conditional on validation findings or says no source changes are expected, complete that no-op cleanup in the same execution by recording the no-op result instead of preserving it as a separate next-step plan.
   - The main agent owns integration, conflict resolution, task doc updates, history updates, shipping, and deployment.
   - If a subagent touches files outside its owned paths or returns conflicting changes, stop and reconcile before validation.
   - For every Luna lane, record the complete assignment and return contract. Reject overlapping ownership. Sol must inspect the actual diff and surrounding code, enforce allowed/forbidden paths, and personally integrate or reject the work.
9b. **Accountability lifecycle:** After integration, run integrated verification. For every non-trivial mutation, launch a fresh Terra context with `$expert-review --adversarial-diff --read-only`. Record every structured finding and give it exactly one Sol disposition: `accepted`, `rejected`, or `deferred`. Remediate accepted findings, rerun relevant checks, and run a fresh focused Terra re-audit when remediation affects security, authentication, billing, persistence, migrations, concurrency, privacy, data loss, or broad cross-package contracts. Finish with final Sol acceptance.
10. Mark the completed work in `tasks/todo.md`:
   - Default mode: check off the completed step.
   - `--phase` mode: check off the completed steps and any acceptance criteria satisfied by the phase work.
11. **Pre-ship validation:**
   - First check conversation context for lint/typecheck/test/build output already produced this session. Do NOT re-run commands whose results are already available.
   - For any validation category not already run, find commands from: `CLAUDE.md`, `Makefile`/`Justfile` (check/lint/typecheck/test/build targets), `package.json` (lint/typecheck/check/test/build scripts), `pyproject.toml`/`setup.cfg`, `Cargo.toml`. If none found and no prior output exists, skip.
   - Inspect validation output even when commands exit zero. If warnings are emitted, either fix them, record them as explicitly accepted with rationale, or report them clearly as unresolved.
   - If errors are found (from prior output or fresh runs), fix them and rerun only the failing commands to confirm. Include fixes in the shipping commit, or a separate commit if unrelated.
   - If errors cannot be auto-fixed, **STOP. Do not ship.** Report the errors to the user and ask how to proceed. Never commit or push code with known build/lint/type/test failures.
11b. **Quality gate for non-trivial mutations:**
   - Apply `docs/quality-gate-contract.md` when the completed step changes source code, scripts, configuration, schemas, generated runtime assets, deploy behavior, workflow policy, validation rules, command surfaces, or multiple files.
   - If the completed step creates, deletes, renames, or changes behavior/metadata in any tracked `SKILL.md` or `PACK.md`, refresh the public skills catalog export before shipping: run `node scripts/generate-skills-catalog-export.mjs` and `scripts/validate-skills-catalog-export.sh`; include changed `exports/skills-catalog/v1/**` artifacts in the shipping boundary.
   - The Skills Showcase lives in the separate `agentic-skills-showcase` repository and imports the public catalog export. Do not run Showcase app generators, Next.js builds, or website asset refreshes during normal `agentic-skills` shipping. If a skill change needs curated website copy, record the follow-up for the Showcase repo instead of editing app files here.
   - Before commit/push, produce a diff-aware ship manifest for the exact shipping boundary. It must include: User goal, Changed files, Per-file purpose, User-goal mapping, Tests run, Skipped tests, Adversarial review, Residual risk, Rollback note, and Next command.
   - Add topology; Luna assignments/results; requested/resolved models and fallbacks; Sol inspection/integration evidence; grouped changed files; integrated verification and unavailable checks; Terra findings and dispositions; remediation; focused re-review; deferred risks; and final Sol acceptance.
   - Refuse shipping while an accepted Critical/High Terra finding is unresolved, integrated verification failed, or a required focused Terra re-audit is missing.
   - For non-trivial source changes, run a targeted `quality-sweep audit`, `$expert-review`, configured review lane, or explicitly justified equivalent adversarial review before commit/push. Fix findings or record accepted residual concerns in the manifest.
   - Final output must distinguish executable verification from documentation-only or task-only checks. Documentation/task checks can support source changes, but cannot be the only proof for non-trivial source mutations.
   - If no executable check is relevant, state why in `Skipped tests` and explain the residual risk. Do not write "not run" without a rationale.
   - If the user corrected the agent during the step, the pre-commit ship manifest must prove the exact shipping boundary includes a `tasks/lessons.md` update for the current correction. Treat the correction as repeatable unless the manifest proves otherwise. If it exposes a workflow failure, also include the relevant skill contract, validation script, fixture, or test enforcement update in the same shipping boundary, or include `Correction enforcement:` with the blocker or not-applicable rationale and the concrete follow-up file/command when needed.
12. Ship the completed work:
   - Update `tasks/history.md` with a brief record of what was accomplished. Create it if needed.
   - Commit and publish using `$commit-and-push-by-feature` with `docs/github-delivery-contract.md`; ensure the issue-backed non-primary branch and create or update one ready pull request without merging it.
13. Deploy:
   - If the ready pull request is not merged into the current primary branch, defer deployment and route to explicit review/`$github-pr merge`. Never deploy development state from the work branch.
   - Check for an explicit manual deploy contract in `deploy.md` or `tasks/deploy.md`.
   - If neither file exists, skip deploy and report `Deploy skipped: no explicit manual deploy contract (deploy.md or tasks/deploy.md)`.
   - If a deploy contract exists, read it first and use it to determine the deploy method.
   - Supplement the contract by checking: `spec.md`, `CLAUDE.md`, `tasks/roadmap.md`, `tasks/todo.md`, `Makefile`/`Justfile`, `package.json`, `deploy/`/`infra/`/`scripts/`, `docker-compose*.yml`.
   - Do NOT look in `.github/workflows/` — this project does not use GitHub Actions.
   - If a deploy contract exists but no deploy method is found, ask the user how deployment works. Do not guess.
   - Exec the deploy and verify the output for errors.
   - Do not run `aws sso login` preemptively from stale context, old logs, or assumptions. If the deploy method uses an AWS profile and auth status is uncertain, first run `aws sts get-caller-identity --profile <profile>` using the profile from the deploy contract or deploy command.
   - If the AWS identity check succeeds, proceed directly with the deploy and do not run `aws sso login`.
   - If the AWS identity check or the deploy command fails because AWS SSO credentials are missing or expired, do not skip deployment. Exec the matching `aws sso login --profile <profile>` command, using the profile from the deploy contract, deploy command, or error output.
   - When `aws sso login` prints a browser URL, device code, or verification instructions, relay them to the user and tell them to navigate to the provided URL and complete the login in their browser. Keep the login command running until it succeeds, fails, or times out.
   - After a successful SSO login, rerun the original deploy command once. This auth recovery is part of the same deploy attempt, not an automatic retry of a failed deploy.
   - If the user cannot complete SSO login or the login command fails, report the deploy as blocked by authentication. Do not report it as skipped.
   - If a health check URL or status command exists, run it.
   - If the deploy fails, report the error. Do not retry automatically.
14. Plan the next step:
   - Read `tasks/todo.md` to identify the next uncompleted step in the current phase.
   - **Check if the current phase is complete** (all steps checked, milestone criteria met):
     - If **YES — Phase transition:**
       1. Archive the completed phase: copy `tasks/todo.md` → `tasks/phases/phase-N.md` (create `tasks/phases/` if needed). Fill in the "On Completion" section.
       1b. If `tasks/manual-todo.md` exists, inspect unchecked items before advancing phases:
           - If any unchecked `_(blocks: Step N.X)_` items still apply to the completed phase, stop. Do NOT archive the manual task file, mark the phase complete, or advance to the next phase unless the user explicitly overrides the blocker.
           - Unchecked `_(after: Step N.X)_` items are non-blocking follow-up tasks. Archive them with the phase and warn the user that they remain incomplete.
       2. Check off the phase milestone in `tasks/roadmap.md`.
       3. Copy the next phase from `tasks/roadmap.md` → overwrite `tasks/todo.md`.
       3b. Extract the next phase's manual tasks (from `**Manual Tasks:**` in roadmap) into a fresh `tasks/manual-todo.md`. If the next phase has no manual tasks, delete the file.
       4. If no more phases remain, publish the planning/task updates in the same ready pull-request boundary via `$commit-and-push-by-feature`, then run `$research-roadmap` to recommend the next action based on project state. Then stop.
       5. **Just-in-time planning:** Invoke `$plan-phase` for the new phase. This generates implementation steps and file-level detail using the full context of what was learned during prior phases.
     - If **NO:** find the next uncompleted step within the current phase.
   - If the next uncompleted step is verification-only/no-op-only (for example, "refactor if validation exposes drift", "verify", "run validation", or `Files: no source changes expected`) and the current session already has passing validation evidence for the same scope, mark it complete with a review note and continue to the next substantive item. Do not write a fresh execution plan for a step whose expected result is "no source changes".
15. Write a self-contained implementation plan for the next step into `tasks/todo.md`, complete enough for a fresh session to execute from `tasks/todo.md` alone.
16. Include task-document changes in the same issue-backed branch and ready pull-request boundary via `$commit-and-push-by-feature`.

## Output

- Step or phase completed
- Files modified
- Deploy status (if deployed)
- Validation results (if lint/typecheck/test/build commands were run) — explicitly state whether failures are expected (red phase: tests before implementation) or unexpected (regressions/bugs), and call out any warnings as fixed, accepted, or unresolved
- Manual tasks — pending count from `tasks/manual-todo.md` (if it exists)
- Advisory tasks — pending record/recurring counts from `tasks/record-todo.md` and `tasks/recurring-todo.md` if they exist
- **Next work:** the next concrete project task, blocker, smoke test, or follow-up
- **Recommended next command:** one command or route for that work

## Next-Step Routing

Before handing back, identify the next concrete work item from project state, then recommend the executor and invocation.

Output exactly two lines beyond the normal report:

- **Next work:** <specific task name, manual blocker, verification gap, discovery task, or explicit parked state>
- **Recommended next command:** <one command or route>

Rules:

- Make the next work item primary. Derive it from `tasks/todo.md`, `tasks/manual-todo.md`, deploy status, validation gaps, smoke-test gaps, phase-transition output, or completion of the current queues. Do not use agent mode itself as the next work item.
- Do not emit `Recommended next command: none` unless the latest user request explicitly asks to pause, park, archive, or wait. If implementation phases, documentation work, and promotable advisory items are all exhausted, route to new-phase discovery: `**Next work:** discover candidate next phase or explicitly park the project`. `$brainstorm` is owned by the `product-design` pack — check `.agents/project.json.enabled_packs` for `product-design` (or `enabled_skills.brainstorm`); if absent, recommend `npx skillpacks install product-design` from the project shell first, then `**Recommended next command:** $brainstorm` (tell the user to start a fresh Codex CLI session if `$brainstorm` is still unavailable after install); if present, recommend `**Recommended next command:** $brainstorm` directly.
- If a post-roadmap `$research-roadmap` scan reports documentation current with no missing or stale work, do not stop at documentation completeness; recommend `$brainstorm` as the next route for candidate phase discovery, applying the same `product-design` pack-availability check above.
- Use `./scripts/agent-mode.sh` only to choose command text. If it is missing, unset, or non-zero, infer routing from the current invocation and task type instead of asking the user to select a mode by default.
- Normalize copied task routes to Codex syntax before final output. If `tasks/todo.md`, `tasks/roadmap.md`, benchmark reports, or prior handoffs contain Claude slash commands for base skills (for example `/exec`, `/ship`, `/roadmap`, `/guide`, `/reconcile-dev-docs`), treat them as task identifiers, not final command text. Convert the final `Recommended next command` to the equivalent Codex `$...` command unless the next action is explicitly a Claude-only handoff, `/delegate`, or a human-guided Claude workflow.
- Inference defaults:
  - Codex skill invocation (`$exec`, `$ship`, `$ship-end`, or `$exec --execute-approved`) → recommend the matching `$...` command.
  - Imported Claude slash routes or orchestration-heavy work → normalize to the matching Codex `$...` command unless the next action is explicitly a cross-agent handoff or human-guided Claude workflow.
  - External human-only manual work (browser/auth/DNS/service dashboard work with no reliable authenticated CLI/API path, paid account setup, real-device checks, or production smoke-test work needing human sign-off) → recommend `$guide` or a Claude-guided manual step rather than `$exec`.
  - Agent-executable work misfiled in `tasks/manual-todo.md`, task-doc bookkeeping, stale `tasks/manual-todo.md` cleanup, or reconciliation against repo/history reality → recommend `$reconcile-dev-docs fix tasks`, promotion to `tasks/todo.md`, or a direct dev-doc audit, not `$guide`.
  - Approved packet present → recommend `$exec --execute-approved` unless the resolved mode is explicitly `claude-only`.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, include `npx skillpacks install <pack-name>` from the project shell as the prerequisite.
- Only present multiple commands when the ambiguity materially changes execution safety or there are equally valid next work items. Otherwise choose the best route and mention degraded mode lookup inline.

### Pack-Aware Command Text

PoketoWork kanban packs are hibernated while Poketo.work is being rebuilt. Do not substitute `$exec-kanban`, `$ship-kanban`, or `$ship-end-kanban` for base-default recommendations. If `.agents/project.json` still lists a hibernated kanban pack, keep recommending the base default command and mention `scripts/pack.sh remove <kanban-pack>` only when cleanup of stale pack designation is directly relevant.

- **No-match / no-pack:** emit the base-default recommendation exactly as today.
- **Degraded path:** missing or malformed `.agents/project.json` (or non-zero exit from `list-packs`) -> silent fallback to the base-default recommendation with a single inline comment `pack-lookup: skipped (no project.json)` appended to the recommendation line.
- **Scope:** recommendation-text routing only. `$exec --execute-approved` still consumes `.agents/approved-plan.json` verbatim regardless of pack routing — the approval-packet contract is unchanged.

## Constraints

- One step at a time by default, or one phase with `--phase`. Then stop and let the user decide what is next.
- `--execute-approved` consumes an `approved` packet at `.agents/approved-plan.json` (contract in `docs/operating-modes.md` § "Approval packet"). `--execute-approved --phase` is rejected — packets target one step. In `claude-only` mode the flag is a user error; Codex is not the executor. Requires `jq` on PATH.
- Always present the plan before executing, then proceed by default under implicit approval. Do not assume a Claude-style `EnterPlanMode` or clear-context accept flow exists.
- Ask for explicit confirmation only for separate safety decisions, and ask one concise question when that is needed. Avoid back-to-back variants like "Approve and I'll exec..." followed by a second restatement of the same action.
- Keep context footprint minimal — only read files relevant to the current step.
- If a blocker prevents completion, document it in `tasks/todo.md` and stop.
- Follow the test strategy annotated on each phase. Do not skip test steps for `tdd` phases.
- Follow the `### Execution Profile` annotated on each phase. If subagents are unavailable in the active environment, execute serially and report the downgrade.
- Do not let subagents update `tasks/todo.md`, `tasks/roadmap.md`, `tasks/history.md`, shipping commits, or deploy steps. Those remain main-agent responsibilities.
- Do not run parallel write lanes unless their `Owns` paths are disjoint. When in doubt, downgrade to `research-only` or `serial`.
- Do not commit on or push mutations directly to the primary branch. Use `$commit-and-push-by-feature` to ensure and publish the issue-backed work branch and ready pull request. Temporary `agent-team` lane branches remain isolated and must pass consolidation/PR review before integration.
- Do NOT execute external human-action items from `tasks/manual-todo.md`. Bookkeeping or agent-executable items that were misfiled there should be reconciled through `$reconcile-dev-docs` or promoted into `tasks/todo.md`, not routed to `$guide`.
- Do NOT execute items from `tasks/record-todo.md` or `tasks/recurring-todo.md` unless the item has first been promoted into `tasks/todo.md`.
- `exec` ships by default in Codex. Use `$ship` only when there is already finished work in the tree or unpushed commits that need packaging without running a new step.
- Never use GitHub Actions for deployment. Only use manual deploy scripts, Makefiles, or CLI commands.
- Never deploy to production without explicit user confirmation.
- Do not modify code as part of the deploy process.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
