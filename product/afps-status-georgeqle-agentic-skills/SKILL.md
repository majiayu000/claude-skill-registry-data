---
name: afps-status
description: Summarize AFPS product-workflow progress from existing artifacts and recommend the next concrete skill command
type: analysis
version: v0.10
required_conventions: [alignment-page]
argument-hint: "[optional project path, product path, or focus]"
---

# AFPS Status

Invoke as `/afps-status`.

Use this skill when the user asks where a product project is in the AFPS workflow, what research/planning/implementation artifact is missing next, whether task docs match product evidence, or which AFPS command should run next.

AFPS here means the product workflow from raw idea through concept scoping, customer discovery/research, lifecycle/growth planning, specs, roadmap/phase work, implementation, validation, and shipping. This is read-mostly reconciliation. It summarizes existing artifacts and recommends a route; it does not create a competing workflow state system.

## Process

1. Resolve target project:
   - Default to the current working directory.
   - If `$ARGUMENTS` names a path, inspect that project.
   - If `$ARGUMENTS` names a product path, app, customer, audience, or focus, prioritize matching artifacts under `research/`, `specs/`, `tasks/`, and `alignment/`.
   - Confirm whether the target is a git worktree when possible. Continue with filesystem evidence if git is unavailable.
2. Read project orientation:
   - `.agents/project.json`
   - `README.md`, `AGENTS.md`, `CLAUDE.md`
   - package/workspace manifests and obvious app entrypoints when needed to understand whether implementation exists.
   - Use `scripts/pack.sh list-packs` when available to determine enabled packs; do not grep `.agents/project.json` directly when choosing installed-pack routes.
3. Inspect AFPS evidence from existing artifacts:
   - Product-path state: `research/.progress.yaml`, including legacy `active_path` normalized mentally to `active_paths`.
   - Research-loop state: selected-set run manifests `research/_working/{orchestrator}-run.yaml` (or `research/{slug}/_working/{orchestrator}-run.yaml`) for the self-advancing research orchestrators (`customer-discovery`, `competitive-analysis`, `positioning`, `journey-map`). When a manifest exists, read its `selected_frameworks` and compare against existing canonical intermediates `research/{orchestrator}-{framework}.md` (or `research/{slug}/{orchestrator}-{framework}.md`) to derive how many frameworks are complete. A manifest with frameworks still pending — or all intermediates present but no synthesized canonical (`research/{orchestrator}.md`) yet — means that loop is **mid-run**.
   - Concept artifacts: `research/idea-brief*.md`, app-scoped `research/*/idea-brief*.md`, and concept/interview notes.
   - Discovery artifacts: customer-discovery docs such as `research/icp.md`, competitive analysis, customer feedback, journey/lifecycle maps, value-prop canvas, positioning, lean canvas, market evidence, and assumption/risk trackers.
   - Lifecycle/growth artifacts: onboarding, activation, retention, conversion, monetization, GTM, growth model, metrics, PMF, and experiment docs.
   - Product/spec artifacts: `specs/`, `spec.md`, app/feature specs, UX/UI/prototype/UAT/consolidation notes, Production Ready Approval records under `alignment/spec-interview-{topic}.html` or `alignment/production-ready-{topic}.html`, and other alignment pages under `alignment/`.
   - Execution artifacts: `tasks/roadmap.md`, `tasks/todo.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, `tasks/recurring-todo.md`, `tasks/history.md`, `tasks/phases/`, and recent validation notes.
   - Rapid pipeline artifacts: `research/vard-ship-log.md` (VARD experiments), `research/ord-ship-log.md` (ORD packages), and `alignment/vard-*.md` or `alignment/ord-*.md` alignment docs.
   - Git evidence: `git status --short`, current branch/upstream, last relevant commits, unpushed commits, and changed files.
4. Reconcile evidence instead of trusting one file:
   - Distinguish missing artifacts, stale artifacts, contradictory artifacts, completed work, active implementation tasks, manual blockers, unvalidated implementation, and unshipped local changes.
   - Treat `research/.progress.yaml` as a manifest of product/app/customer focus, not as the source of truth over concrete artifacts. Its `pipeline_stage` is a pointer to which orchestrator stage last ran, not per-framework status. Treat Production Ready Approval as a confirmed alignment-page artifact, not a new lifecycle database or registry.
   - For a self-advancing research orchestrator, derive framework progress from the run manifest + canonical-intermediate existence and report it as "k of N frameworks complete," not from `tasks/todo.md` checkboxes (the migrated orchestrators no longer queue framework work there).
   - If product-path manifest entries are missing or stale, report the exact proposed update in prose. Do not write `research/.progress.yaml` unless the user explicitly asks for mutation.
   - If task docs contradict research/spec/code/git evidence, call out the contradiction and route to reconciliation rather than choosing whichever artifact is newest.
5. Detect rapid pipeline activity:
   - If `research/vard-ship-log.md` exists, report VARD pipeline status: number of experiments shipped and the most recent entry. Under each concept, read the **latest traction entry's** persisted `Status:` (`iterating` | `graduating` | `archived`) and `Recommendation:` line, and report that status and recommendation rather than re-deriving graduation readiness from raw signals. A `graduating` status is the graduation-ready signal; keep raw traction signals as supporting evidence only.
   - If `research/ord-ship-log.md` exists, report ORD pipeline status: number of packages published and the most recent entry. Under each package, read the **latest traction entry's** persisted `Status:` (`iterating` | `graduating` | `archived`) and `Recommendation:` line, and report that status and recommendation rather than re-deriving readiness from raw signals. A `graduating` status is the graduation-ready signal.
   - If `vard` or `ord` packs are enabled, note the active rapid pipeline alongside deliberate pipeline status.
6. Classify AFPS stage:
   - `graduation-ready`: a rapid pipeline's latest ship-log traction entry shows `Status: graduating` — the experiment/package is ready to enter the full AFPS pipeline.
   - `unscoped`: no concept brief or the concept is too unclear for customer discovery.
   - `concept-ready`: concept exists but discovery pack/skills are not enabled.
   - `discovery-needed`: concept exists and discovery skills are enabled, but customer discovery is absent or not specific enough.
   - `research-incomplete`: customer discovery exists but market, competitive, value, positioning, journey, or lifecycle evidence is missing.
   - `lifecycle-gap`: discovery exists but onboarding, conversion, activation, retention, monetization, GTM, or metrics questions block spec quality.
   - `spec-needed`: research is sufficient but durable product/spec artifacts are absent or stale.
   - `roadmap-needed`: research/spec artifacts exist but `tasks/roadmap.md` or `tasks/todo.md` is missing, stale, contradictory, or not actionable.
   - `execution-ready`: a clear unchecked implementation task exists with no blocking manual task.
   - `ship-needed`: implementation changes are present, completed, or unpushed but validation, task review, commit, push, or deploy packaging is pending.
   - `reconcile-needed`: artifacts conflict enough that the next step should be reconciliation before new research or implementation.
7. Choose the next route with these rules:
   - VARD latest traction `Status: graduating`: `/idea-scope-brief` to enter the full Business AFPS pipeline, linking the vard-scan/align/ship-log entries as evidence. Recommend it directly only when base skills are visible in the active session or project-local install state; otherwise recommend `npx skillpacks init` from the project shell before `/idea-scope-brief`.
   - ORD latest traction `Status: graduating`: `/devtool-user-map` to enter Devtool AFPS (prefix `npx skillpacks install devtool` from the project shell if the `devtool` pack is not enabled, per the step-8 availability gate), or `/idea-scope-brief` for the rare cross-domain Business case.
   - No concept brief or unclear concept: `/idea-scope-brief`
   - Concept exists but business discovery is missing: `npx skillpacks install business-research` from the project shell.
   - Concept exists and discovery is enabled, but no customer-discovery evidence: `/customer-discovery`
   - A self-advancing research loop is mid-run (a run manifest exists with frameworks still pending, or all intermediates exist but no synthesized canonical yet): re-invoke that same orchestrator to advance one phase — `/customer-discovery`, `/competitive-analysis`, or `/positioning` when `business-research` is installed, or `/journey-map` when `customer-lifecycle` is installed — and tell the user to clear context and re-run it. This continuation takes precedence over starting a new orchestrator; do not imply a single pass and do not route framework work to `/exec`.
   - Customer discovery exists but market/value evidence is missing: the most specific installed discovery command, usually `/competitive-analysis`, `/value-prop-canvas`, or `/positioning`; if `business-research` is not installed, recommend `npx skillpacks install business-research` first.
   - Journey/lifecycle/growth questions are missing after discovery: route to the **`/journey-map` orchestrator first**, not directly to a child lifecycle skill. `journey-map` is the parent orchestrator that owns inline routing to `/onboarding-map`, `/conversion-map`, `/retention-map`, `/lifecycle-metrics`, and `/expansion-map` via its Optional Research Trigger Map. Recommend `/journey-map <product-path>` whenever the canonical journey map (`research/journey-map.md` or `research/{slug}/journey-map.md`) is missing, stale, or incomplete, or when any child lifecycle detour (onboarding/conversion/activation/retention/monetization/metrics/expansion) is being considered — let `journey-map` choose the child skill. Recommend a child lifecycle skill directly only when the canonical journey map already exists and is current and the user has explicitly scoped that single stage. If `customer-lifecycle` is not installed, recommend `npx skillpacks install customer-lifecycle` from the project shell; for habit/growth-loop questions specifically, `npx skillpacks install business-growth`.
   - Research/specs exist but task queue is stale or absent: `/roadmap`
   - Clear executable task exists: `/exec`
   - Implementation is done but unvalidated, dirty, uncommitted, unpushed, or otherwise unshipped: `/ship`
   - Contradictory research/spec/task evidence: `/reconcile-research` when business-ops is enabled, `/spec-drift` when agent-work-admin is enabled, otherwise `/codebase-status` with a focused prompt naming the contradiction.
8. Validate command availability before recommending pack-local routes:
   - Use `scripts/pack.sh list-packs` when present to detect enabled packs.
   - If the best command lives in an uninstalled pack, recommend the package install command instead of the unavailable command: `npx skillpacks install <pack>` from the project shell.
   - If `scripts/pack.sh` is missing or pack lookup fails, do not assume base or pack skills are available. Fall back to `npx skillpacks which <skill>` (which pack provides a skill) and `npx skillpacks status` (installed/enabled state) to confirm provenance. Recommend only commands visible in the active session; otherwise recommend `npx skillpacks init` for missing base skills or `npx skillpacks install <pack>` for missing pack skills, and mention the degraded lookup only if it changes confidence.
   - Installed-but-not-yet-visible guard: a pack being enabled (and `npx skillpacks which <skill>` resolving to it) does **not** prove the skill is invokable in the current session. If the target skill is not visible in the active session's skill list or local skill roots even though its pack is installed, do not recommend invoking it directly. Recommend `npx skillpacks refresh` and reloading the skill registry (Claude Code `/reload-skills`, then `/clear`; restart if the skill is still invisible) — or a fresh Codex session for Codex — before the skill invocation. This is the reload path, not a reinstall.

## Output

Produce a concise structured report with:

- **Overview:** repo path, product/app focus, git status, enabled packs, active rapid pipelines (VARD/ORD), and whether AFPS evidence is single-path or multi-path.
- **Rapid Pipeline Status** (if applicable): VARD and/or ORD experiment counts, latest shipment, and the latest persisted traction `Status:` and `Recommendation:` per concept/package (`graduating` = graduation-ready), with raw traction signals as supporting evidence.
- **Artifact Map:** concept, customer discovery/research, lifecycle/growth, specs/prototypes/UAT, tasks, alignment pages, and shipping evidence with present/missing/stale status. For a research stage whose run manifest exists, report loop progress as "k of N frameworks complete" and whether it is mid-run.
- **AFPS Stage:** one stage label from the workflow above, with confidence and evidence.
- **Contradictions And Gaps:** conflicting artifacts, missing product-path manifest updates, stale task queues, manual blockers, validation/shipping gaps, and uncertainty.
- **Recommended Route:** the next concrete work item and why it is the narrowest route.

End with exactly:

```md
**Next work:** <specific AFPS step or blocker>
**Recommended next command:** <one command or route>
```

## Constraints

- Read-only by default. Do not modify workflow state, task docs, research docs, specs, or git state unless the user explicitly asks for mutation.
- Do not create a new AFPS state file or schema. Use existing artifacts, especially `research/.progress.yaml`, `research/`, `specs/`, `tasks/`, `alignment/`, and git. Production Ready Approval is an alignment-page artifact convention, not a competing lifecycle registry.
- Propose missing `research/.progress.yaml` updates in the report instead of writing them by default.
- Do not run expensive tests, installs, web research, deploys, or external-account actions during status synthesis.
- Do not treat `tasks/record-todo.md` or `tasks/recurring-todo.md` as execution queues unless an item has clearly been promoted into `tasks/todo.md`.
- Do not route agent-executable repo work to `/guide`; reserve guided/manual routes for human-only blockers.
- Do not create or modify GitHub Actions workflows.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/afps-status-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Default Shipping Contract

- **Default next-step routing:** when reporting completion, include the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>` so the next caller has a concrete handoff.
- Normally read-only and should not create or modify tracked repository files.
- If the user explicitly asks this skill to create or modify tracked files, follow `docs/github-delivery-contract.md` and finish with an issue-backed non-primary branch plus ready pull request; do not merge it.
- This contract does not override stricter safety rules about secrets, destructive history changes, release publication/tag confirmation, production deploy confirmation, paid actions, or public visibility changes.
