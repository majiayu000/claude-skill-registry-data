---
name: story-driven-ci
description: Design or replace lean CI around tester.army e2e, isolated Neon branches, and native TesterArmy Linear issue export. Use for legacy Playwright CI retirement, user-story acceptance coverage, replay cost controls, or sequencing pilot adoption before other repositories. Produces a scoped standard, story/evidence ledger, deletion plan, and executable rollout gates rather than a parallel legacy lane.
---

# Story-driven CI

## Outcome

Replace inherited CI architecture with the smallest pipeline that proves important user outcomes. Use the `e2e` runner for deterministic and agentic acceptance together, disposable Neon databases for state isolation, and TesterArmy's native Linear integration for confirmed product defects. Do not optimize for old test counts, YAML shape, or selector-by-selector parity.

Read [the verified framework contracts](references/framework-contracts.md) before writing config or workflows. Load `/e2e` for test syntax and `/neon` plus `/neon-postgres-branches` for approved database operations. Use the repository's native rollout plan for project-specific stories and adoption sequence. Repository instructions and explicit authorization govern execution.

## Non-negotiable decisions

- Legacy browser tests are a behavior inventory, not architectural requirements. Classify requirements as keep, consolidate, or intentionally drop with a reason. Never silently lose critical business behavior.
- Deprecate the old pattern now. Replace it in one bounded cutover after the new standard proves selected acceptance criteria. A temporary validation baseline is not permission to build permanent dual runners, a compatibility layer, or a full case-parity project.
- Preserve useful typechecks, unit tests, security boundaries, and deploy admission. Delete duplicate execution, not independent safety checks. A real browser story belongs here only when an outcome depends on integrated UI behavior.
- Never run acceptance against shared Neon `dev`, production, or an unverified database URL. Unresolved credential exposure blocks database, branch, and credential operations, not design work.
- Do not weaken an internal Docker network to accommodate model calls. Use an approved hosted acceptance runner with a deliberately separate test/model path. Do not bypass CI ownership with fabricated flags.
- Do not push, dispatch hosted runs, deploy, grant access, create/export Linear tickets, or mutate cloud resources just because a plan describes it. Execute only within explicit authorization. Ask once for remaining consequential decisions.

## 1. Inspect and define the contract

Read handoffs, repository instructions, native change artifacts, graph context, working-tree status, workflow triggers, release admission, and current auth/data boundaries. Preserve pre-existing files and secret-bearing changes. If graph context has no relevant node, inspect only the needed workflow/config/artifact paths.

Create a **story ledger** with these columns:

| Story ID / requirement source | Persona + initial state | User action + observable result | Exact business oracle | Layer / suite | Evidence / status |
| --- | --- | --- | --- | --- | --- |
| Required stable ID, not an invented Linear ticket | Seeded isolated user/data | One complete outcome | Persisted state, permissions, totals, or other concrete assertion | Unit/API or required browser story | Test ID, commit, report and run link, or explicitly planned |

An oracle is the assertion that decides correctness. Use exact `expect` assertions for prices, authorization, persisted records, and destructive actions. Agent interpretation is appropriate for navigation and visual/semantic checks, not a replacement for accounting or permission assertions. Keep goals narrow. Require a bounded cleanup/reset contract and distinct records per mutating test.

Select required stories by product risk and changed behavior. Consolidate redundant journeys, but avoid a giant chained test where an early failure hides unrelated outcomes. Record excluded stories and why. Do not infer "covered" from filenames or a green job.

## 2. Start with the minimal pipeline

Use one admission workflow with fast independent checks and one Chromium acceptance execution on the same candidate revision. Prefer one app build/start, one installation, bounded workers, and explicit retries `0` as the initial policy. Change worker/retry policy only with measured evidence and a documented flake budget. Do not add browser matrices, mobile lanes, shards, production-like seed copies, or separate agent/deterministic jobs without a requirement.

Sequence the expensive path after fast checks: validate trust and target inputs, provision isolated database, migrate/seed, start candidate app, run selected stories, retain evidence, clean up. PR runs cancel superseded work. Ensure cancellation does not strand branches: explicit cleanup plus expiration and reconciliation are required.

A stable required admission check must not disappear or pass vacuously through path filtering, skipped jobs, `--pass-with-no-tests`, or fork restrictions. Compute affected stories where reliable, then fall back to the full required suite for shared code/config/schema changes or an unknown dependency. Cheap static checks can run on every relevant revision. Only add post-merge verification when release admission or different integration behavior needs it, not a redundant replay of the same contract.

Measure wall time, runner minutes, model usage/cost when observable, cold/warm cache behavior, flakes, unique required stories proven, and orphan branches. Capture a baseline before choosing numeric performance targets. More green tests is not the objective.

## 3. Own the Neon lifecycle

Pin the Neon project and approved non-production parent IDs. Default to schema-only branches with synthetic fixtures, or an explicitly approved sanitized parent. Verify the actual pinned CLI/API supports the chosen creation mode. Documentation and installed CLI can disagree. Never copy production data by default.

Branches are PR-scoped in identity but **attempt-scoped in mutable state**. A name/ownership record includes repository, PR, candidate SHA, run ID, and attempt. Different concurrent attempts must not reset, seed, or delete one another's branch. Reusing one persistent PR branch is allowed only with serialized ownership and a proven reset contract.

Before migration or seeding, verify provider-returned project, parent, branch ID, connection endpoint, database/role, and ownership against pinned allowlists. Reject shared/production targets and missing identity. Obtain the connection string only for the created branch, mask it, and keep control-plane credentials out of app/test/model environments. Never print raw connection strings or secret values.

Migration errors, partial setup, failed tests, cancellation, and PR closure all need cleanup behavior. Delete only the recorded owned branch ID after identity checks, not everything matching a prefix. Set expiration as a backstop and reconcile abandoned ownership records. Test lifecycle failure paths with mocks first, then require authorized provider evidence. Generic documentation about inherited roles cannot resolve a specific credential incident.

## 4. Use replay without promising free execution

CI defaults to read-only cache. Persist vetted replay entries, scoped by runner/engine/config/test compatibility and trust, not a database endpoint or secret. Do not import writable cache from untrusted PR code into a trusted run. Prove both warm and cold execution.

Only validated replayed `agent.act` actions avoid a model call. Cache misses, fallback, `cache: false`, `agent.assert`, `agent.waitFor`, and `agent.extract` may call the model. Read-only cache does not mean replay-only. Replays check recorded end state but still need a valid isolated environment and exact assertions.

Budget each required agent story with `maxSteps`, `maxModelCalls`, `maxInputTokens`, `maxObservationBytes`, and judgment/test timeouts from the installed config types. These bound work, not dollar spend. Reports expose `modelCalls` and limits, not guaranteed token/dollar totals. Do not copy obsolete `maxTokens` or `consume` step-repair settings from older guidance. Restrict model context to synthetic non-sensitive data.

Use targeted `--last-failed` for diagnosis, not to replace full-suite admission evidence. Archive the first report/artifacts before a rerun because output is overwritten. Seed replay only on authorized trusted runs. Do not broadly disable judgment to make CI appear cheap.

## 5. Separate trust, evidence, and reporting

Never expose Neon management, model, or application credentials to unreviewed fork code or privileged `pull_request_target` checkout. Keep untrusted checks read-only and credential-free on an appropriate isolated runner. A protected hosted acceptance path tests an explicitly approved immutable revision with short-lived test credentials. If that path is unavailable, report the required acceptance as blocked, not green. Restrict cloud control-plane tokens to provisioning/cleanup steps and audit downstream secret scope separately.

The required admission result uses process exit status plus the required-story ledger. `e2e` exit `0` means selected tests passed; exit `1` means failure; exit `2` means no tests selected unless explicitly overridden. Distinguish startup/config/auth/model/engine/no-test infrastructure failures from product assertion failures.

Retain `.e2e/report.json`, JUnit when useful, necessary screenshots/traces, run URL, tested SHA, branch lifecycle evidence, and per-story status. Choose bounded retention and scrub artifacts/logs of secrets and personal data. Never delete original failure evidence before rerun. Preserve real failures through cleanup and artifact-upload steps.

PR comments are optional evidence delivery, not admission. The current `github` reporter writes job summaries but cannot comment from a fork's read-only token. Prefer summaries/artifacts initially. If a separate privileged publisher is later justified, it must treat artifacts as untrusted and validate repository, revision, schema, and size without executing content. That is a security design choice, not a documented built-in publisher. Use least permissions and no model/Neon secrets there.

## 6. Integrate Linear the native way

**Two surfaces:** open-source `e2e` CLI reports are local/CI artifacts; TesterArmy's hosted project Issues tab owns the documented native Linear export. The supplied docs do not establish automatic CLI report ingestion, automatic ticket creation on CI failure, or bidirectional Linear sync. Do not invent these features or build a custom ticket bot to bridge that uncertainty.

After the human approves the intended workspace/team and access scope, connect Linear under each hosted project's **Integrations → Linear**, authorize the TesterArmy app, and save the default team. The connection is project-shared; members can export without separate sign-in. Workspace admin approval may be required.

Triage confirmed product defects with expected/actual behavior, reproducible steps, screenshot/report evidence, and the TesterArmy issue link. Native export creates tickets as the TesterArmy app and names the exporting teammate. Severity maps `5 → Urgent`, `4 → High`, `3 → Medium`, lower → Low. One TesterArmy issue links to at most one ticket; this does not deduplicate different issues or guarantee updates to existing tickets.

Do not export transient infrastructure failures or flakes as product defects by default. Verify the issue source and export route before claiming the CI-to-Linear workflow works. Preserve approval for ticket creation until explicitly authorized. For required stories, add existing Linear requirement keys to the story ledger when supplied, without claiming native export performs requirement synchronization.

## 7. Prove, cut over, then generalize

First prove one pilot, then adapt the policy to a second pilot with its own data/auth requirements. For each pilot require:

1. Correct candidate revision and supported hosted trigger.
2. Required stories and exact oracles proven with fresh reports.
3. Warm and cold replay behavior, bounded model work, failure diagnostics.
4. Neon identity guards and cleanup after success/failure/partial provisioning/cancellation, with no shared-DB contact.
5. Trust/secret isolation, non-vacuous admission, preserved release integration.
6. One authorized native Linear export and repeat-export behavior, or a precisely documented blocker with no claim of integration completion.
7. Replacement gates pass before deleting the classified legacy configs, scripts, workflows, dependencies, and docs. Keep framework-required browser engine dependencies.

Update native proposal/design/spec/tasks coherently. Remove superseded parity work and duplicate task IDs. Do not check off, synchronize/archive, or announce completion with unresolved acceptance gates. Keep separate statuses for implemented, locally checked, hosted proven, and externally blocked.

Expand to other repositories only after both pilots have evidence, a deletion manifest, measured cost/reliability, and remaining project-specific requirements. Reuse the policy and tiny existing helpers, not a pilot's deployment topology or a new central framework. Finish with paths, verification evidence, explicit blockers, and one next step.
