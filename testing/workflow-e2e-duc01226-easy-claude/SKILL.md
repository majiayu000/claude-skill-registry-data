---
name: workflow-e2e
description: '[Workflow] Use when writing, updating and verifying E2E tests through a bounded green fix/retest loop. --source={changes|recording|update-ui|prompt|context|whole}, --visual-review={true|false}.'
disable-model-invocation: false
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Workflow steps follow the guided contract in `$start-workflow` → Step Execution Protocol: `gate` steps are fixed; other steps may flex with a logged reason.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** One E2E lifecycle for every request — resolve the source and scope, author or update tests only when needed, then converge the fixed scope to an honest green through the configured runner. E2E quality/visual review is capped at one pass per verification attempt; execution/fix/retest rounds remain a separate bounded convergence mechanism.

**Use this** to write, update, run, verify or fix E2E/browser/user-flow coverage. Use `workflow-integration-test` (`--mode=green` / `--mode=write`) for integration tiers, `$e2e-test --mode=verify` alone for a one-shot report-only check, and `workflow-bugfix` when the task is a product bug whose E2E test is only the proof.

**IMPORTANT MANDATORY Steps:** $investigate -> $e2e-test -> $e2e-test --mode=verify --fix-loop -> $docs-manager --mode=update -> $workflow-end -> $watzup

**Step contract:** steps follow `$start-workflow` → Step Execution Protocol — `gate` steps always run, a step that runs invokes its skill invocation, and every other deviation is logged. NEVER batch-complete validation gates.

## Size & Kind Triage (FIRST action)

Before choosing steps, classify the target and record the result in the run report:

- **Source** — resolve `--source` (below) and `--visual-review` (below). State both before any step.
- **Size** — XS: one known test or journey · S: one feature's cases (≤15 test files) · M: several features or ≤60 files · L/XL: a module-wide or `whole` run (hundreds of cases). Size sets batching and delegation, never whether the green gate runs.
- **Kind** — test-only authoring · baseline/visual update · verification-only (`prompt|context|whole` with no expected edits) · product fix expected (a failing journey on changed behavior) · data/auth/environment-sensitive (seed, accounts, external services).
- **Risk** — escalate depth on shared persistent state, auth/secrets, irreversible data, cross-service journeys, or an ambiguous scope; not on file count alone.

The triage picks which recommended skills run and how deep. An unresolvable source or scope stops with an ambiguity record — never a silently chosen maintenance mode.

## Required Quality Gates (non-negotiable)

| Gate                                                                                       | Evidence that proves it                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tests-pass` — the fixed scope is green in THIS run                                        | `$e2e-test --mode=verify --fix-loop` report: exact runner output (counts, failing names, exit status), the configured consecutive fresh green runs, Round Integrity Check pass, no scope shrink, no skipped/weakened/deleted test                    |
| Case traceability                                                                          | Each selected owner-qualified case/variant (or strict-default TC/§8 when no native `specArtifacts` profile applies) maps to an actual test, assertion and observed result; ID presence alone is not proof; unresolved links stay `UNVERIFIED` |
| Honest verdicts                                                                            | Every failure is classified `SOURCE-WRONG` / `TEST-WRONG` / `TEST-NOT-OPTIMAL` / `ENVIRONMENT-BLOCKED` / `AMBIGUOUS` before any edit; a fix lands at the owning layer and is reviewed                                                         |
| Explicit acceptance                                                                        | No snapshot, baseline, fixture or expectation changes without a named acceptance record; otherwise `ACCEPTANCE-PENDING`                                                                                                                       |
| Visual (when it applies)                                                                   | One review pass per verification attempt: every required capture opened/read case by case via `$experience-review --rounds=0`; blocking findings return to the execution/fix/retest loop. A false value cannot waive a required gate            |
| Docs synced (when the run changed tests, baselines, product source or documented behavior) | `$docs-manager --mode=update` triage result with terminal evidence                                                                                                                                                                                           |
| `run-closed`                                                                               | `$workflow-end` (top-level only) verifies every gate above                                                                                                                                                                                    |

`N/A` needs evidence: E2E is `APPLICABLE` only with a configured framework, runner and command; a relevant but unavailable capability is `ENVIRONMENT-BLOCKED`, never green.

## Recommended Skills

| Skill                                   | Earns its cost when                                                                                | Proves / feeds                                             |
| --------------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `$investigate`                          | Scope, runner, case profile or test organization is not already evidenced in this session; M+ size | Applicability, case map, commands, data strategy           |
| `$e2e-test` (`e2e-author`, conditional) | `--source` is `changes`, `recording` or `update-ui`                                                | Authored/updated artifact + exact scope handed to the loop |
| `$e2e-test --mode=verify --fix-loop` (gate)    | Always                                                                                             | `tests-pass`, verdicts, visual gate, fresh reruns          |
| `$experience-review --rounds=0`         | Called by the loop when visual review applies                                                      | Per-capture records, blocking vs advisory findings         |
| `$docs-manager --mode=update` (conditional)            | The run changed tests, baselines, product source, specs or documented behavior                     | Docs synced                                                |
| `$workflow-end` (gate)                  | Always                                                                                             | `run-closed`                                               |
| `$watzup` (`e2e-watzup`, conditional)   | Top-level run only; a nested run leaves the recap to its parent                                    | Handoff summary                                            |

`$test` is not a second top-level run and no separate visual-fix loop exists — `$e2e-test --mode=verify --fix-loop` is the single convergence and remediation owner after preparation. Skipping a recommended skill is fine when triage shows it does no real work; log it as a deviation (`intent-skip` / `when-false`) with evidence.

**Conditional step notes (registry `skipReason`, verbatim):**

- `$e2e-test` — skip when: Resolved --source is prompt, context, or whole; e2e-test --mode=verify --fix-loop owns scenario selection or generation for that source.
- `$docs-manager --mode=update` — skip when: Verification-only run: no test, baseline, product source, spec, or documented behavior changed, so docs-manager --mode=update has nothing to record; cite the unchanged diff and the terminal verify report.
- `$watzup` — skip when: Nested inside a parent workflow (workflow-feature, workflow-bugfix, workflow-big-feature, workflow-greenfield-init); the parent's tail (workflow-end then watzup) owns the whole run's recap, so this nested run's workflow-end skips its recap as `covered by the parent workflow's watzup` instead of printing a second one.

## Source Dispatch (`--source`)

An explicit value wins. When omitted, infer in order: recording JSON present → `recording`; explicit whole-project request → `whole`; run/verify/QC a feature, bugfix, journey or current context → `prompt` or `context`; UI/style/template diff with baseline intent → `update-ui`; confirmed code/spec/API change → `changes`. No evidenced signal → stop with an ambiguity record.

| `--source`           | Use when                                                                    | `$e2e-test` mode it drives                                                                                                                                        |
| -------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `changes`            | Test specs, source or API changed and E2E coverage must follow              | `from-changes` / `from-spec`: update only cases the changed intent requires                                                                                       |
| `recording`          | A browser recording JSON exists and a runner test is wanted                 | `from-recording`: convert with the project's configured recorder/converter (else author by hand), add outcome assertions, follow the configured test organization |
| `update-ui`          | UI changed and screenshot baselines need review                             | `update-ui`: collect candidate evidence; keep accepted expectations until an explicit acceptance record                                                           |
| `prompt` / `context` | A feature, bugfix, journey, QC request or current context defines the scope | none — the loop selects or generates cases                                                                                                                        |
| `whole`              | Project-wide E2E/QC verification                                            | none — the loop runs the configured full suite                                                                                                                    |

Authoring sources run only a focused authoring check at most; the final full green run belongs to the loop. Every source hands the loop one exact scope plus its case map.

## Visual Review (`--visual-review`)

Resolve independently from an explicit value, the task request and the project contract. `true` (explicit or project-required) on an applicable surface: capture the project-declared state × viewport matrix per the resolved `uiStateCapture.mode`, index captures, and have `$experience-review --rounds=0` read every required capture in exactly one review pass for that verification attempt. Validated `BLOCKING` findings join the execution failure set and return to owning-layer repair; a fresh rerun may collect fresh evidence but never starts a second review pass for the prior attempt. `ADVISORY` findings are recorded, never looped on. A false value cannot waive a project-required gate. A non-visual scope records `N/A`.

Read `.claude/skills/shared/e2e-quality-protocol.md` before authoring or verification, and `.claude/skills/shared/ui-state-capture-protocol.md` when visual review applies; they own the scenario/invariant, isolation, auth, wait, evidence, cleanup and capture rows. This workflow owns only sequencing.

## Test Architecture Contract Handoff

Resolve one record before the first authoring or verification step and carry it to every step (the loop owns execution evidence; `$docs-manager --mode=update` receives the terminal result):

| Field                            | Required content                                                                                                                                                           |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `applicability`                  | `APPLICABLE` with evidence of a configured framework, runner and command; otherwise `N/A — <evidence>`. Skill-local browser helpers are not project evidence               |
| `caseMap`                        | Configured owner/case/scenario/variant + evidence fields, or strict-default TC/§8 when no native profile applies; a malformed declared profile blocks and never falls back |
| `fullCommand` / `focusedCommand` | Copy-ready configured commands; invalid or zero-match selections exit non-zero                                                                                             |
| `runIdentity` / `dataStrategy`   | Unique non-sensitive run identity, public-path setup, declared seed/accumulation mode, parallel-worker isolation                                                           |
| `testOrganization`               | The declared local pattern and its canonical locator/action/wait owners; never require a Page Object Model or abstract base the project does not select                    |
| `result`                         | Exact counts, failing names, exit status, repeat evidence; two consecutive no-reset full runs for each applicable persistent-state suite                                   |

Browser journeys follow observe → act → observe with the configured runner's native waits or an evidenced project helper; action pacing applies only when the project contract configures it and never substitutes for a real settle signal.

## Orchestration Freedom

You choose inline vs sub-agent, batching and wave layout, optimizing wall-clock and token cost at equal quality. Fixed constraints only: a test exists before it is verified; fixes are re-verified after they land; `$workflow-end` runs last; gates awaiting user approval never run in parallel; each loop round runs the default verify pass inline (never a nested `--fix-loop`). Recommended: XS/S inline without sub-agents; L/XL partition authoring and failure triage per module or feature batch (one report per batch), while the green gate still runs the full fixed scope; delegate authoring to the `e2e-runner` agent when the batch is large.

## Memory & Reporting

- One task per selected step (and per batch for L/XL) so nothing is lost after compaction.
- Write the run report under `tmp/reports/` FIRST, then append per step, round and batch; visual records are appended one capture at a time.
- After compaction, re-read the report and the current task list before continuing; sub-agent briefs make report writing their first deliverable and return only the summary envelope.

## Fix Path & Loop Bounds

Owned by `$e2e-test --mode=verify --fix-loop`; this workflow only enforces its bounds. Classify before editing, trace root cause with `$investigate --mode=debug`, fix at the owning layer with `$fix`, review the round's diff with `$changes-review`, run the Round Integrity Check, then rerun fresh over the same scope. Converge on the configured consecutive fresh green runs (default 2) within the round cap (default 3). A non-shrinking or rising failure count, a cap hit with failures open, scope shrink or test loss → `NOT-CONVERGED` and escalate using ask user tool with exact evidence. Never weaken, skip, narrow, delete, silence or auto-accept to obtain green.

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `e2e-visual-design-contract` — Evidence and baseline rules for visual review in E2E and human QC; handling visual-review evidence or visual baseline updates → .claude/skills/shared/protocols/e2e-visual-design-contract.md
- `incremental-persistence` — Persist results per file or section while the work proceeds; a sub-agent or heavy step processes more than three files → .claude/skills/shared/protocols/incremental-persistence.md
- `session-goal-ledger` — Keep the original goal and every user prompt of the session; running a long or multi-prompt session → .claude/skills/shared/protocols/session-goal-ledger.md
- `subagent-return-contract` — Sub-agents return a structured envelope and a report path, never an inline report; spawning a sub-agent → .claude/skills/shared/protocols/subagent-return-contract.md
- `test-architecture-execution-contract` — Testability as an architecture condition: required test types and execution modes; setting up or reviewing a test architecture → .claude/skills/shared/protocols/test-architecture-execution-contract.md
- `workflow-registry-binding` — Read the workflow registry entry and the workflow skill together, since they must agree; executing or editing a workflow → .claude/skills/shared/protocols/workflow-registry-binding.md

<!-- PROTOCOL-GUIDES:END -->


<!-- SYNC:test-architecture-execution-contract:reminder -->

**MUST ATTENTION** Each assertion-bearing test names the behavior or technical contract it protects and asserts an outcome it owns. Use the project's configured/native test format — Given/When/Then is one valid format, never a framework-wide requirement. When `specArtifacts` is valid, link configured owner/case/variant identity and `intent/contracts` evidence; when absent, name the guarded business intent or technical contract. A malformed declared profile BLOCKS without fallback. Broad test-format migration → assign an owner and next step, never rewrite cases outside scope.

**MUST ATTENTION** Before implementation record evidence-backed applicability for the test types and modes the task/project contract requires: copy-ready full and focused commands where available, zero-match behavior, a useful platform-appropriate entry point, supported execution modes and environments, state-isolation requirements, exact results, and repeat evidence where persistent state makes it relevant. Exercise claimed modes; report a missing required capability as `ENVIRONMENT-BLOCKED`. Never invent production targets or impose a test format. Browser/UI E2E uses the configured runner's waits or project helper for observable readiness and outcomes; apply action pacing only where the project contract specifies it. Reuse the project's evidenced test organization — require a POM, base class, or component taxonomy only when the project actually selects it.

<!-- /SYNC:test-architecture-execution-contract:reminder -->

<!-- SYNC:e2e-visual-design-contract:reminder -->

**MUST ATTENTION** visual E2E/QC resolves the project design authority first, applies project design-system and frontend decisions plus applicable `UI-*`/`DD-*`/`CL-*` roles, records component ownership using the project's taxonomy or observed boundaries, sends static source findings to `$ui-design --mode=review` and runtime image evidence to `$experience-review`, captures states and transitions required by the configured evidence contract, reloads the convention docs then reads and records each required capture before synthesizing findings with coverage gaps, treats `UIX`/UI/accessibility-floor findings as blocking and `UIX-POLISH`/DD identity as advisory, never invents measurements, and never auto-promotes baselines; non-visual runs state `N/A`.

<!-- /SYNC:e2e-visual-design-contract:reminder -->


<!-- SYNC:session-goal-ledger:reminder -->

- **MANDATORY** Session goal ledger per the `Task Planning Rules`: pin `Original goal:`, keep `User prompts this session: P1…Pn`, and map the result to every prompt before claiming done; full text: `.claude/skills/shared/protocols/session-goal-ledger.md`.

<!-- /SYNC:session-goal-ledger:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** one E2E lifecycle — resolve `--source` and visual mode, author only when the source needs it, then converge the fixed scope to an honest green through `$e2e-test --mode=verify --fix-loop` or escalate with exact evidence.

- **MUST ATTENTION** triage first (source, size, kind, risk) and record it; size changes batching and depth, never whether the green gate runs.
- **MUST ATTENTION** `tests-pass` = exact runner output for the fixed scope, configured consecutive fresh green runs within the round cap, Round Integrity Check pass — never weaken, skip, narrow, delete or auto-accept a test or baseline to get there.
- **MUST ATTENTION** map every selected owner-qualified case (or strict-default TC/§8) to an actual test, assertion and result; classify each failure before editing and fix at the owning layer.
- **MUST ATTENTION** visual review only when requested or required by the project contract for an applicable surface; read and record every required capture case by case via `$experience-review --rounds=0`; a false value cannot waive a project-required gate.
- **MUST ATTENTION** cap E2E quality/visual review at one pass per verification attempt; do not confuse bounded execution/fix/retest convergence with review rounds.
- **MUST ATTENTION** write the report under `tmp/reports/` first, keep one task per selected step, re-read both after compaction; `$workflow-end` runs last.
