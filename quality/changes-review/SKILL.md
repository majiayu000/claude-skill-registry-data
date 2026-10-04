---
name: changes-review
description: '[Code Quality] Use when a workflow step or the user asks for a review of current changes (staged/unstaged or branch diffs, focused scope). --fix-loop reviews, fixes, re-reviews. Cross-module or risky: workflow-review-changes.'
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

> **[BLOCKING]** Run the required gates in declared order; a triage-conditional phase completes with a recorded NOT-APPLICABLE reason, and how you orchestrate the work inside a phase is your choice.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

> **[TOP REMINDER — WHY-REVIEW FINDINGS-VALIDATION GATE IS NON-NEGOTIABLE]**
>
> If this review produces **ANY** finding (Critical / High / Medium / Low) in standalone mode, you **MUST invoke the `$why-review` skill** through the skill invocation with `--validate-findings <report-path>` **before** any fix, docs-manager --mode=update, commit, or handoff. A batch reviewer's or report-only specialist's own validation call covers its findings outside the independent check set (Phase 6). An actual skill call is the ONLY way to pass this gate — re-reading the cited `file:line`s yourself, "self-validating," or any inline/manual substitute does **NOT** count. In `--report-only` mode (including step 1 of `$workflow-review-changes`) stop after the report — the caller owns validation and fixing.

## Quick Summary

**Goal:** Review any change — one line or thousands of files, code or docs/config/infra — find real defects, missing updates, stale docs and drift with `file:line` evidence, validate every finding, fix the validated blocking ones at their owning layer, and re-review until the round bar clears. Spend depth where the risk is, not where the file count is.

**Summary:**

- **Triage first (Phase 0):** size band, change kinds, risk and blast radius decide which dimensions run, how deep, and how you orchestrate them. Write the **Review Plan** into the report before reviewing.
- **You orchestrate:** inline vs sub-agents, one wave vs batches, which specialist skills to escalate to (`--report-only`) — optimize for speed and cost at equal quality. The required gates below never flex.
- **Memory:** one task per selected dimension/batch and per required gate; ONE living report at `tmp/reports/changes-review-{date}-{slug}.md`, written first and appended per file/batch/phase — re-read it and the current task list after any compaction.
- **Loop (standalone):** Phase 6 validate (`$why-review --validate-findings`, an actual skill call) → Phase 7 SELF-FIX each validated finding that blocks the current round → full re-review (not for a round-1 LOW-only fix set closed by scoped check with no simplification applied) → Phase 7.5 holistic full-mode `$why-review` when fixes landed → Phase 8 `$docs-manager --mode=update`. Round 1 needs zero open findings; from round 2 only CRITICAL/HIGH/MEDIUM block, LOWs are deferred.
- **Modes:** standalone (default) · `--report-only` (Phases 0–5 only; the caller validates and fixes; this skill orchestrates, so its own review waves and gates still run — the flag removes fixing, asking and restarts, not its own fan-out — a caller always passes the flag explicitly, and step 1 of `$workflow-review-changes` passes it from the workflow registry; a nested call without it runs standalone and validates and fixes its own findings) · `--defer=<list>` (duties the caller runs instead — `whole-target`, `specialists`, `tests`, `entities`, `simplify`; when `$ARGUMENTS` carries it, read `.claude/skills/workflow-review-changes/references/caller-mode.md` FIRST; step 1 of `$workflow-review-changes` passes the first four explicitly) · `--fix-loop` (below).
- **Optional `--fix-loop` mode (standalone-only) DECOUPLES find from fix.** Each round runs the default review pass INLINE report-only (Phase 0 → Phase 5, fresh task list, stop before Phase 6), then `$why-review --validate-findings` → `$fix` on validated blocking findings → a FRESH full re-review of the changed diff, under a Goal Contract and bound convergence loop (optional `/goal`). Exit bar, round cap 3 (hard maximum 3), uncapped failing tests, no-shrink/increasing-blocker escalation, and a terminal Phase 8 `$docs-manager --mode=update` all apply. No flag → default behavior unchanged. Full protocol in `references/fix-loop.md` — read it FIRST when the flag is present (BLOCKING).

**Workflow:**

Phase -1 bind loop (standalone) → Phase 0 triage + Review Plan → Phase 0.7 dimension review (inline or parallel sub-agents) ∥ Phase 0.8 whole-target rationale pass → Phase 3.5–3.9 conditional gates (simplification opportunities, test coverage, entities, E2E) → Phase 4 consolidate + Dual-Feedback Ledger → Phase 5 docs triage → Phase 6 validate → Phase 7 fix + full re-review → Phase 7.5 holistic re-review → Phase 8 `$docs-manager --mode=update`.

**Key Rules:**

- MUST ATTENTION read the run's deviation log (`tmp/workflow-runs/<runId>/skips.md`) when present and treat each skipped, merged, simplified or reordered step as a review input.
- Every finding cites `file:line`, consequence, severity (`SYNC:severity-rubric`) and confidence; speculation is not a finding. Grep 3+ existing examples before flagging a convention violation — codebase convention wins over textbook rules.
- A triage-conditional phase that does not apply completes with a one-line `NOT-APPLICABLE — <evidence>` record; the required gates never do.

## Review Scope

Target: current working-tree changes by default (`git status`, `git diff`, `git diff --cached`); an explicit branch diff (`git diff <base>...<head>`) or commit range (`git diff <base>..<head>`) when the user asks for one. A pull-request or branch review ALWAYS uses the branch diff from the merge-base with the target (`git diff <target>...HEAD` ∪ uncommitted changes) — never only the latest commit or the working tree, so every commit of the branch is in scope.

## First Principle — Easy to Change · Easy to Scale · Easy to Maintain

> The full gate is `SYNC:core-engineering-principles`, inlined with this skill's protocol blocks below; its closing digest ends this file.

Pure docs-only changes skip this gate except for executable examples.

---

## Core Principles (ENFORCE ALL)

**YAGNI · KISS · DRY** (3+ similar patterns → flag extraction) · **Clean Code** (names reveal intent, one job per function) · **Follow Convention** (grep 3+ examples first) · **No Flaws** (trace happy + error paths, boundaries, null/empty) · **Proof Required** (`file:line` or it is not a finding) · **Doc Staleness** (cross-check changed files against their docs, specs and tests).

## Phase -1: Bind the Review Loop (FIRST ACTION — standalone-only)

- **Run** in standalone invocation: bind the review loop as a standing protocol obligation you self-drive, plus the `/goal` command as an accelerator WHEN available — review the full diff → run `$why-review --validate-findings` on every finding → SELF-FIX each validated finding that blocks the current round → re-review the WHOLE updated diff → loop until one complete pass clears that round's bar (round 1: zero open findings; round 2: zero CRITICAL/HIGH/MEDIUM, a LOW-only round ENDS the loop with the LOWs recorded as deferred) → Phase 7.5 when fixes landed, fixing only findings that block the current round and re-running until that bar is clear → Phase 8 `$docs-manager --mode=update`. If `/goal` is unavailable, record one line and continue under the protocol loop; never fake a gate.
- **SKIP** in `--report-only` mode (step 1 of `$workflow-review-changes` passes it; the caller owns the loop). Record: `Phase -1 deferred to the caller's review loop.`
- **SKIP** when `--fix-loop` is set — Fix-Loop Step 0b owns the single convergence binding and every round's review pass is report-only. Record: `Phase -1 deferred to --fix-loop Step 0b.`

## Phase 0: Triage + Review Plan (FIRST REVIEW ACTION)

1. **Collect the diff and its intent** from the review scope; list changed files with added/removed line counts, and read the stated intent (task, PBI, plan, Goal Contract, commit messages). When a plan or goal governs the change, check plan compliance — missing or extra scope versus the plan is a finding.
2. **Blast radius** — assess it by grep/read of callers and dependents: record impacted files, untested dependents and risk order, and prioritize file review order, highest-impact files first. Optional: for a high-risk change (shared contract, many callers, cross-module flow, public API) and when `.code-graph/graph.db` exists, `$graph-code --mode=blast-radius` or `trace <file> --direction downstream` can add hints — the graph can be stale or incomplete, so verify by reading; an absent graph is never a finding. When the diff crosses a boundary (frontend↔backend, service↔service, event producer↔consumer, shared contract), trace it end to end per `SYNC:cross-stack-impact-trace` and `SYNC:cross-service-check` — every consumer of a changed contract is in scope.
3. **Classify** the target:

| Axis | Values | Decides |
| --- | --- | --- |
| **Size band** | XS 1–3 files / ≤100 changed lines · S ≤15 · M ≤60 · L ≤300 · XL >300 | orchestration (see Scale Strategy) |
| **Change kinds** | docs-only · tooling/config · test-only · behavior · public contract/API · data/schema/migration · dependency upgrade · bus/event · security-sensitive · UI · infra/CI · cross-module | which dimensions and risk lenses run |
| **Risk** | irreversible · data integrity · security/authority · money/PII · wide blast radius · ambiguous intent | depth — escalate a dimension to its specialist skill whenever risk is present, whatever the size |
| **Mechanical churn** | generated files, lockfiles, pure renames/moves, formatting | verified by pattern (spot-check + grep for residue), recorded in the coverage ledger, not reviewed line by line |

4. **Write the Review Plan** as the report skeleton: triage result, selected dimensions (with the evidence that triggered each), dimensions ruled out (with evidence), orchestration and batches, and a **coverage ledger** listing every changed file → the dimension/batch that owns it. Create one task per selected dimension/batch and one per required gate (Phases 6–8, standalone).

## Phase 0.7: Dimension Review — What to Review

**Always-on core (every diff, cheap):** logic matches stated intent (`SYNC:logic-and-intention-review`) · bug detection (`SYNC:bug-detection`) · readability and change cost · convention fit · secrets/debug artifacts/sensitive files never staged · doc staleness · test pairing (`SYNC:integration-test-sync-check`) · architecture boundaries (read `architectureRules.layerBoundaries` from `docs/project-config.json`; an import that breaches `cannotImportFrom` is a BLOCKING Critical).

**Whole-diff correctness (every behavior-changing diff):** one reader takes the complete change as one behavior per `SYNC:whole-diff-correctness` — you, when it fits your context; otherwise the reviewer that already reads the whole target (Phase 0.8, or the caller's whole-target pass inside `$workflow-review-changes`), with the lane protocol in its brief; a dedicated lane only when neither has room. Batches add depth but never replace it.

**Triggered dimensions** — run when the triage evidences the trigger; escalate to the specialist skill (always with `--report-only`, so it validates its own findings and never edits) when the risk is material or the dimension spans many files:

| Trigger (evidence) | Inline lens | Escalate to |
| --- | --- | --- |
| Behavior-bearing code | spec drift adjudication, test coverage | `$integration-test --mode=review` (Phase 3.7) |
| Auth, permissions, secrets, input handling, external data, dependencies, PII/money | enforcement on every path, negative tests, no secrets in diff | `$security-audit --report-only` |
| Data access, loops over data, hot paths, caching, concurrency, render-heavy UI | N+1, unbounded queries, paging, allocation | `$performance-review --report-only` |
| Cross-module change, new module/layer, public contract or dependency-direction change | layering, coupling, ADRs, backward compatibility of every caller | `$architecture --mode=review --report-only` |
| Domain entity / value-object / aggregate files | invariants, encapsulation (`SYNC:domain-entity-change-gate`) | `$domain-analysis --mode=review --report-only` (Phase 3.8) |
| Deployable service, API, job, migration, config, operational surface | rollback, idempotency, config in every environment, fail-fast | `$production-readiness-review --report-only` |
| Frontend/UI files (project frontend patterns) | this skill owns the UI dimension | `$ui-design --mode=review --report-only` |
| AI surface? Only if `node .claude/scripts/ai-signal-scan.cjs --json` (`--base <review base>` for a branch/PR) has `status: surface` (`clean` → record `No AI-feature surface`, stop; `unknown` → §0.1 grep once) | small diff: read `.claude/skills/shared/protocols/ai-engineering-gate.md` and apply it | `$ai-engineering-review --report-only`, spawned only when the scan lists a surface |
| DB migration · dependency upgrade · bus/event · API contract · config/env · infra | rollback + volume · semver + advisories · idempotency + retry + poison message · additive vs breaking · all environments · env parity | the matching specialist when material |
| Specs, feature docs, PBIs, test specs in the diff | M1–M7 code-to-spec drift gate (`shared/sdd-artifact-contract.md`), M7 demo test on every added business case | `$spec` audit when broad |
| Bugfix / regression / stale output | End→Start debugger trace gate (`SYNC:end-to-start-debugger-trace`) | `$investigate --mode=debug` when untraced |
| Change implements a documented spec/PBI | spec-compliance pre-pass (`spec-compliance-reviewer`) BEFORE code-quality review | — |
| Multilingual UI text | translation sync (`SYNC:translation-sync-check`) — missing locale updates surface using ask user tool | — |

Derive categories from the repository's actual structure (`SYNC:category-review-thinking`), not a fixed grid; the table is a floor, not a ceiling. Inside `$workflow-review-changes` or under `--defer=specialists`, do not escalate to a specialist the parent already runs — record the dimension as owned by the parent's specialist wave and keep only the inline lens.

**Conditional E2E/browser/user-flow trigger** — apply `.claude/skills/shared/e2e-quality-protocol.md` only for changed executable E2E specs, browser config, fixtures, page/component objects, recordings, or source that alters an exercised user journey (a doc that merely mentions E2E is not a trigger). On positive evidence, Phase 3.9 records the trigger paths and must Invoke `$e2e-test --mode=verify` report-only over the fixed E2E scope (never `--fix-loop`); with no trigger record `E2E quality gate: NOT-APPLICABLE — no executable E2E/browser/user-flow surface in the diff`; a positive trigger that cannot run stays `ENVIRONMENT-BLOCKED`.

## Scale Strategy — How to Orchestrate (your choice)

| Band | Recommended shape |
| --- | --- |
| **XS / S** | Review inline in one pass; escalate only a risk-flagged dimension to its specialist. No batching. |
| **M** | One parallel wave (spawned in ONE message): lenses that must read the same files share one agent, which carries each lens's full protocol, unless their combined skills and files would not fit one context with room to reason; plus the Phase 0.8 pass; you consolidate. |
| **L** | Systematic batching (`SYNC:systematic-review-batching`): risk-weighted batches per module/category (high-risk ≤8 files or ≤2000 diff lines; low-risk styling/tests/docs/config text may pool to ≤20 files or ≤4000 lines; mechanical churn verified by pattern), each batch validating its own findings, one report section per batch, then a cross-batch synthesis pass for interactions the batches cannot see. |
| **XL** | As L, plus: review in risk order from the blast radius; batch mechanical churn by pattern; checkpoint the coverage ledger after every wave; re-read the report and the current task list before each new wave. Never sample silently — any file not reviewed line by line is listed with the reason. |

Sub-agent briefs carry the triage, their slice of the coverage ledger, any finding in their scope labelled as an UNVALIDATED hint, the instruction to write their report section FIRST and append per file, for a batch the instruction to validate its own findings (`SYNC:systematic-review-batching` Step 2b), and the protocols per `SYNC:review-protocol-injection`. Integrate sub-agent findings RAW — never filter, soften or override them. Parallelize only independent read-only work; a spec-compliance pre-pass returns before the wave it precedes.

## Phase 0.8: Whole-Target Rationale Pass (standalone)

Run `$why-review` in FULL mode over the whole review target combined with the current changes, in parallel with the Phase 0.7 wave (a sub-agent for M and larger; inline for XS/S). It catches whole-package issues scoped reviewers miss — foreclosed alternatives, assumptions that only break when files are read together. Brief it read-only: never `--fix-loop`, and its `$integration-test --mode=review` linkage is deferred to Phase 3.7, which owns the coverage gate (record `Linkage deferred to changes-review Phase 3.7 / parent workflow step.`). Its findings merge into Phase 4. Skip in `--report-only` mode when the caller runs its own whole-target pass (step 2 of `$workflow-review-changes`, or `--defer=whole-target`), recording `Phase 0.8 deferred to the caller's whole-target review.`

## Phases 3.5–3.9: Conditional Gates

- **Phase 3.5 — simplification opportunities** (code changed): `$code-simplifier --report-only` over the changed code; its proposals are findings for the same validation/fix loop, never applied here. Under `--defer=simplify` the caller runs a mutating `$code-simplifier` later over the same code: skip and record `Phase 3.5 deferred to the caller's $code-simplifier step.` The flag is explicit — a bare `--report-only` still runs this phase.
- **Phase 3.7 — test coverage** (behavior-bearing code changed): `$integration-test --mode=review --report-only` over the full diff; Gate 7 maps every behavior change to its profile-declared canonical scenario/case and a covering executing test and assertion/result (integration-first; unit fallback needs justification). GAP / SPEC-GAP results are findings. Inside `$workflow-review-changes` (or under `--defer=tests`) the parent's dedicated step owns it — record `Phase 3.7 deferred to parent workflow $integration-test --mode=review step.`
- **Phase 3.8 — domain entities** (entity files changed): apply the `SYNC:domain-entity-change-gate` lenses inline, or delegate to `$domain-analysis --mode=review --report-only` when 3+ entity files or aggregate invariants change. Inside `$workflow-review-changes` (or under `--defer=entities`) its dedicated step owns it.
- **Phase 3.9 — E2E quality** (positive E2E trigger only): report-only `$e2e-test --mode=verify`, per the trigger rule above.
- **Fresh-context gate** (M and larger, zero findings so far): one zero-memory sub-agent re-reads the diff to catch what an anchored reviewer misses; it may only ADD findings.

## Phase 4: Consolidate + Spec Drift + Dual-Feedback Ledger

1. Merge every dimension, batch, specialist and Phase 0.8 finding into the report by severity, **deduplicating by root cause first** (same owning `file:line` range and same violated rule — one entry listing every source, the highest justified severity); note reviewer conflicts; confirm the coverage ledger has no unreviewed file.
2. **Spec Drift Adjudication** (every behavior-changing file, `SYNC:spec-drift-adjudication`): compare the change with its configured canonical owner and classify **CODE-WRONG** (BLOCKING — fix code/test), **SPEC-STALE** (intended change; reconcile the owner, its profile-declared scenario/case and mapped tests), **SPEC-SILENT** (code enforces an unstated invariant; enrich the owner and prove a guarding test), or **AMBIGUOUS** (ask user tool before editing either side). Green tests never normalize drift.
3. **Dual-Feedback Ledger** — one row per behavior-changing finding with a Spec-feedback cell and a Test-feedback cell; a blank or bare `N/A` on either axis is a FAIL (every N/A carries its reason). The strict default profile expresses these as §3/§4 requirements and §8 TCs.
4. **Goal Satisfaction** — when an active Goal Contract exists (`SYNC:goal-contract-satisfaction-loop`), emit the Goal Satisfaction matrix; a required criterion at FAIL is a finding.

## Phase 5: Docs Triage

Flag every doc, spec or test artifact the change makes stale (section + what changed) as a finding. Do not edit docs here — Phase 7 fixes validated doc findings and Phase 8 sweeps the rest.

**`--report-only` ends here:** return the report path, findings by severity, the coverage ledger summary, spec-drift verdicts and any unconfirmed trade-off. Inside `$workflow-review-changes` hand the report to the parent's validation and fix steps.

## Phase 6: Why-Review Findings Validation (standalone; REQUIRED before any fix)

**Trigger:** ANY finding of any severity — the only skips are a literally empty finding set, or every finding already validated by its batch reviewer or report-only specialist with none in the independent check set of `SYNC:systematic-review-batching` Step 3 (record which). Invoke `$why-review --validate-findings <report-path>` through the skill invocation (terminal mode, same session). CLEAN → record `## Why-Review Validation` and continue. HAS ISSUES → reconcile the report (revise severities, remove false positives, add surfaced findings, record `## Why-Review Validation Notes`) and re-validate the updated report — at most 2 re-do rounds; still not clean → record `## Why-Review Validation — Unresolved` and escalate using ask user tool. Findings a `--report-only` specialist or a batch reviewer already validated are carried as validated, except the independent check set of `SYNC:systematic-review-batching` Step 3 (every CRITICAL/HIGH finding, reviewer conflicts, a sampled share of each batch's MEDIUM findings), which this pass re-validates; `$code-simplifier --report-only` proposals are not self-validated and go through this gate.

## Phase 7: Recursive Auto-Fix + Full Re-Review Loop

**Trigger:** validated findings that block the current round (round 1: any severity; round 2+: CRITICAL/HIGH/MEDIUM). Round-2 LOW-only findings are recorded and deferred, not fixed — list them under `## Deferred LOW Findings (severity floor, round ≥2)`. In round 1 a LOW with a local fix is fixed and closed by a scoped check, and a LOW needing new code or tests is deferred (Round-1 LOW closure).

1. SELF-FIX each validated finding that blocks the current round at its owning layer — inline for a handful of local fixes, `$fix --target=review <report>` for many or cross-module ones (called from this phase it is a reviewer-owned fix: no approval prompt and no nested `$changes-review` — this loop re-reviews); a defect whose owning cause the report does not trace gets `$investigate --mode=debug` first; a finding the fixer believes is wrong is logged `REJECTED` with its new evidence and re-validated via `$why-review --validate-findings` before it counts as closed. Behavior-changing fixes add or update the guarding test; validated stale docs are fixed at the canonical artifact.
2. Verify the fix set (affected tests, lint, spec/doc sync, config checks) and append `## Fix Cycle {N}` to the report: findings fixed, files changed, verification commands and results. When a later verify step runs the tests once, last (`SYNC:verify-last-order` — the caller says so or its sequence has one), this verification is static: lint, spec/doc sync and config checks only, and a fix may write or amend tests but does not run them.
3. **Re-review the WHOLE current diff** (original changes + fixes) from Phase 0 with a fresh task list (a round-1 LOW-only fix set closed by scoped check or deferral, with no simplification proposal applied, is the one exception — Round-1 LOW closure) — re-read every changed file; the prior report is history, never truth. Re-triage: the fix may change the size band or add a change kind.
4. Repeat until one complete pass clears the round bar.

**Stop conditions:** the same validated finding repeats for 2 full review invocations with no progress → ask the user; a fix needs product/owner input → record the blocker and ask; a required tool or sub-skill is unavailable → ask before adapting. NEVER hand validated blocking findings back as "recommendations" in standalone mode, and never mark the review clean after a fix without the full re-review (a round-1 LOW-only fix set closed by scoped check or deferral, with no simplification proposal applied, is the one exception — Round-1 LOW closure). Inside `$workflow-review-changes` or `--report-only`, the caller owns fixing and re-review.

## Phase 7.5: Holistic Full-Mode Why-Review (standalone; when fixes landed)

Once the Phase 7 loop converges and any fix landed — other than a round-1 LOW-only fix set closed by scoped check with no simplification applied — invoke `$why-review` in FULL mode (never `--validate-findings`) over the WHOLE review target combined with every fix as one artifact — the post-fix state Phase 0.8 never saw. Keep fixing only findings that block the current round and re-running until that bar is clear; round-2 LOW-only findings are recorded and deferred, not fixed. When no fix landed, record `Phase 7.5: not needed — no fix landed; Phase 0.8 reviewed this exact state.` Inside `$workflow-review-changes` its post-fix `why-review` step owns this.

## Phase 8: Final Docs-Update (standalone; ALWAYS once the loop converges)

Invoke `$docs-manager --mode=update` over the full changeset (diff + fixes). Before it, apply SPEC-STALE and SPEC-SILENT verdicts to the configured canonical owner and its profile-declared scenario/case with the mapped executing test (the strict default profile uses `$spec [update]` + `$spec [mode=tests]`). Record the result under `## Phase 8 Docs-Update`. A spec-content edit here (a new rule or scenario/case) triggers exactly one bounded re-review of the affected package; prose-only edits do not. Inside `$workflow-review-changes` the parent's `$docs-manager --mode=update` step owns this.

## Output Format

The report (`tmp/reports/changes-review-{date}-{slug}.md`) holds, in order: Review Plan (triage, selected/ruled-out dimensions, orchestration) · coverage ledger · findings by severity (`file:line`, consequence, confidence, dimension) · Spec Drift verdicts · Dual-Feedback Ledger · Goal Satisfaction matrix (when a Goal Contract exists) · `## Why-Review Validation` · `## Fix Cycle {N}` blocks · `## Deferred LOW Findings (severity floor, round ≥2)` · Phase 7.5 / Phase 8 records · verdict: **PASS at the current round bar** or **ISSUES FOUND**.

## Recommended Skills

| Skill | When | Why |
| --- | --- | --- |
| `$graph-code --mode=blast-radius`, `$graph-code --mode=trace` | optional: high-risk change and `.code-graph/graph.db` exists | stale-able hint for impact and risk order |
| `$security-audit`, `$performance-review`, `$architecture --mode=review`, `$domain-analysis --mode=review`, `$production-readiness-review`, `$ui-design --mode=review`, `$ai-engineering-review` — all `--report-only` | triggered dimension with material risk | specialist depth without a second fixer |
| `$integration-test --mode=review --report-only` | behavior-bearing code | coverage map + assertion quality |
| `$code-simplifier --report-only` | code changed | clarity/maintainability opportunities |
| `$e2e-test --mode=verify` (report-only) | positive E2E trigger | E2E quality gate |
| `$why-review` (FULL / `--validate-findings`) | Phase 0.8 / 6 / 7.5 | rationale pass, validation, post-fix holistic pass |
| `$fix --target=review`, `$investigate --mode=debug` | Phase 7 | owning-layer fixes, untraced defects |
| `$docs-manager --mode=update`, `$spec` | Phase 8 | docs and canonical specs in sync |
| `$workflow-review-changes` | risky, large or pre-merge work that needs guaranteed specialist depth and a runtime experience check | the orchestrated version of this loop |

## AI Agent Integrity Gate

Before reporting done: grep every removed or renamed name across ALL file types (zero dangling references); ask WHY before changing an existing value; verify ALL affected outputs (one green run ≠ all green); re-read files after any compaction.

## `--fix-loop` Mode — Read `references/fix-loop.md` First (BLOCKING)

**Trigger:** `$changes-review --fix-loop [scope]`. Optional; standalone-only. When the flag is present, read `references/fix-loop.md` in full FIRST (BLOCKING) — before Phase -1 and before any review work. It holds the whole mode: Fix-Loop Steps 0–3, the ordered convergence and escalation gate, the terminal docs-manager --mode=update and the review receipt. Without the flag, skip it: every phase above runs exactly as documented. In `--report-only` mode or as step 1 of `$workflow-review-changes`, the caller wins — ignore the flag, do not read the reference, and record `--fix-loop ignored — the caller owns the loop`.

---

<!-- SYNC:core-engineering-principles -->

> **Core Engineering Principles — Easy to Change · Easy to Scale · Easy to Maintain** — The success metric of every plan, implementation and review is _future change cost_: the next change must be cheap, safe and provable. DRY, reuse, abstraction, interfaces, wrappers, patterns, layering, tests and the harness exist only to serve that goal. Apply this gate BEFORE any narrower design rule or checklist; when a narrower design rule would raise change cost, this principle wins — it never waives a required gate (tests, review, security, user confirmation). It is evidence-gated: judge fit against the project's config, accepted decisions and local patterns, and never impose a technique the project does not use.
>
> 1. **Easy to change.** Keep one owner per piece of knowledge — DRY the rule, not look-alike text. Reuse an existing helper, component or module before writing a new one (search 3+ siblings and cite them). Put purpose-named interfaces or ports at volatile boundaries: wrap a third-party SDK or infrastructure dependency in an adapter when it is volatile, likely to be swapped, or needs a test seam, so a swap touches one place — a stable dependency used directly is fine, and a pass-through wrapper that lowers no change cost is a defect. Keep units small and cohesive with explicit dependencies; no hidden state, boolean traps or leaked implementation detail. Extract an abstraction for a real second consumer or an evidenced change axis, never for speculation; prefer the reversible decision and defer an irreversible one until evidence forces it. Depth → `SYNC:design-patterns-quality`, `SYNC:complexity-prevention`.
> 2. **Easy to scale.** Growth in features, modules, team, data or load must not multiply edit sites or cost. Add a variant by extension (a new handler, registration or config entry), not by editing every switch over the same discriminator. Keep module boundaries and dependency direction explicit. Bound every loop, query, result set, queue and concurrency on the paths that matter, so work grows with the request, not with total data. Scale only what the project's profile warrants — no speculative distribution or infrastructure. Depth → `SYNC:scale-technique-gate`, `SYNC:engineering-foundation-gate` (F5, F6).
> 3. **Easy to maintain.** Protect every changed behavior with tests that name the business intent or invariant and FAIL when it breaks — happy, error, edge, boundary and regression paths, not only the changed line. Tests are repeatable and isolated. The mechanical harness (format, lint, types, build, test — the same command locally and in CI) runs and passes. Names and structure state intent, and docs or specs that embed the behavior stay in sync. Depth → `SYNC:engineering-foundation-gate` (F3, F4, F7), `SYNC:harness-setup`.
>
> **By phase:**
>
> - **Plan** — each phase names what it reuses (`file:line`), the seam or abstraction it adds or why none is needed, the next plausible change and its edit-site count, the growth bound, and the test that proves each invariant — or `N/A` with a reason where an item cannot apply (a docs-only phase has no growth bound).
> - **Implement** — search for reuse before writing; after writing, recount the edit sites of the next plausible change, confirm each new test fails when its intent breaks, and run the harness.
> - **Review** — judge each pillar `PASS` / `FAIL` / `N/A` with `file:line` evidence and name the real enemy: coupling, duplicated knowledge, hidden state, unbounded growth, untested intent, unclear intent or an irreversible decision exposed too early. A finding names its consequence for the next change; absence of a pattern is not a defect.
>
> **Self-check before claiming done:** (1) What is the next plausible change, and how many files would it touch? (2) What breaks at 10× features, data or load? (3) Which named test goes red if this behavior breaks, and does the harness run it?

<!-- /SYNC:core-engineering-principles -->

<!-- SYNC:whole-diff-correctness -->

> **Whole-Diff Correctness Lane** — Purpose: catch the defects that only appear when a change is read as one behavior rather than as files — a flow that breaks across layers, a boundary the change mishandles, a caller it silently breaks. One reviewer reads the complete behavior-changing diff, plus whatever surrounding code it needs, as a single change. Split only when the diff cannot fit one context with room to reason, and then along the change's own flows, never by file type. It is one assignment: the orchestrator runs it inline when the change fits its context, otherwise gives it to a reviewer that already reads the whole target, and to a dedicated reviewer only when none has room; a batch or specialist reviewer reviews only its own scope. Batches and specialists add depth; they never replace this pass.
>
> **Hunt:** walk each changed behavior through the situations real users and data create — empty, first and last, limits, time crossing a day or time zone, alternate clients, roles, channels and states, retries and partial failure, concurrent use. The history of the changed lines (blame, recent commits) and the comments beside them record intent the change can break; the project's own instructions and conventions are part of the contract.
>
> **Report:** rate how sure you are each candidate is real and reachable — 0 not a defect, or not introduced or newly exposed by this change; 25 plausible, unverified; 50 likely, not confirmed; 85 confirmed by tracing the code path; 100 confirmed with a concrete failing input — and keep what reaches 85, each with its reachable trigger path and consequence. Rarity and impact set severity, never confidence: a confirmed rare defect is still reported. A candidate whose reality or reachability cannot be settled (below 85, not ruled out) is never silently dropped when its consequence would be MEDIUM or higher: report it as `NOT VERIFIABLE`, naming what would settle it; a lower-consequence unsettled candidate is an observation. What is never a finding is defined once in `SYNC:severity-rubric`.

<!-- /SYNC:whole-diff-correctness -->

<!-- SYNC:review-policy -->

> **Executable review policy** — Review skills/tooling MUST use `.claude/scripts/lib/review-policy.cjs` (policy version 6) for round eligibility. Assign severity first; never change it to obtain PASS.
>
> **Blocking predicate:** `blockingFindings(round, findings, hardGates)` returns all validated round-1 findings except LOWs closed with `resolution: 'scoped-fix-verified' | 'deferred'` (valid only for LOW). From round 2, only CRITICAL/HIGH/MEDIUM findings block. `NOT VERIFIABLE` remains a separate blocking unresolved-evidence state every round. Failed binary gates are synthetic CRITICAL every round; test-green gates use `kind: 'test'`, others `kind: 'binary'` (default). No severity floor waives test-green, security-must-fix, required-artifact, or other binary gates.
>
> **Evaluation:** `evaluateRound` retains floor-round/deferred LOWs in `deferredLow`, scoped-fixed LOWs in `scopedClosedLow`, never both. LOW-only rounds do not block after the floor. It reports `extensionGranted: false`, `ESCALATE` for exhausted review budgets with review blockers, and `failingTestGates` / `testLoopContinues` for open test gates.
>
> **Budget/minimum:** `MAX_ROUNDS=3`, `HARD_MAX_ROUNDS=3`: ceilings, never targets. Every review blocker may use round 3; unresolved blockers at the cap escalate. No conditional extension. Clean review ends at `round >= minRounds`; default minimum 1, explicit maximum 3. Persist the declaration; never infer it from the round counter.
>
> **Test exception:** failing `kind: 'test'` gates are outside the review budget: they neither earn extensions nor escalate. While they are the ONLY blockers, status stays `CONTINUE`, accepting subsequent rounds beyond 3 until tests pass. Review blockers past budget still escalate; without a failing test gate, a run never reopens past budget.
>
> **Durable record:** MUST retain `runId`, target fingerprint/revision, policy version, minimum/maximum/completed rounds, full findings/gate evidence, interruption/resume metadata, and acceptance. Use atomic, lock-serialized `start`, `record`, `accept`, `interrupt`, `resume`, `invalidate`, `check` transitions. Identical completed rounds are idempotent and consume budget once. Changed target fingerprints invalidate evidence/acceptance while preserving bounded budget; stale evidence cannot be accepted. Record round 1 once after LOW closure: `targetFingerprint` is post-fix; `reviewedFingerprint` identifies the full-pass target and is required for `scoped-fix-verified`. Never claim the full pass reviewed later fixes. Policy-version changes (including LOW floor/closure or round budget) invalidate old records: start a new run. Interrupt/resume preserves completed rounds/findings. Records are bookkeeping, not consent, native permission, or proof of host review.
>
> **CLI boundary:** JSON stdin; real clock, supplied `now` rejected. State directories must be absolute non-root real directories; records size-bounded; malformed/locked state fails closed. Keep full reports on disk; inline envelopes summarize transport only. Each new consumer needs a semantic fixture, boundary counter-cases, seeded mutant, and report with target fingerprint/command exit status.

<!-- /SYNC:review-policy -->

<!-- SYNC:cross-stack-impact-trace -->

> **Cross-Stack Impact Trace** — FIRST review action: comprehend change holistically, THEN judge files. Every reviewed diff: note change context, trace full pipeline of main affected area end-to-end across client↔server seam, so a change on one tier can never silently break the other. (Distinct from `SYNC:cross-service-check`, which owns service-to-service / event boundary — this owns client↔server tier seam inside one app; pair both for full-pipeline coverage.)
>
> 1. **Comprehend context FIRST** — before file-by-file review, write short **Change Context** note: what changed, intent (why), originating tier (frontend / backend / shared / infra), main affected feature/flow. Do before flagging anything.
> 2. **Identify cross-stack seam(s)** — for main affected area, locate contract seam(s) between client and server: API route/endpoint + verb, request/response DTO or payload shape, shared type/schema, event/message contract, query/route params. Infer tier layout from `docs/project-config.json` and project conventions.
> 3. **Trace full pipeline end-to-end, in change's direction:**
>     - **Backend change → trace FORWARD to every frontend consumer:** handler/controller → response DTO/serializer → API client/service → store/state → component/template rendering or submitting it.
>     - **Frontend change → trace BACKWARD to backend contract:** component/form → API client call → route/endpoint → request DTO/validation → handler/domain.
>     - Grep route path, DTO/type name, each field name across BOTH tiers. Optional: when `.code-graph/graph.db` exists, `$graph-code --mode=connect-api` or `python .claude/scripts/code_graph trace <file> --direction both --json` can add hints about the connection (may be stale — verify by reading).
> 4. **Verify BOTH sides still agree** — for every changed seam confirm other tier matches: route path & verb, field names & types, nullability/optionality, required vs optional params, enum values, auth/permission, error/status shape. Any mismatch = **BREAKING** finding (backend change breaks a frontend consumer, or frontend now sends what backend rejects).
> 5. **Classify each seam:** NONE (no contract change) / ADDITIVE (backward-compatible) / BREAKING (consumer on other tier must change too). BREAKING seam whose other-tier consumer NOT updated in same diff = HIGH severity minimum (CRITICAL for auth/money/data-integrity paths).
>
> **Skip ONLY** when change has no cross-tier seam — pure docs, pure styling with no data contract, or single-tier tooling. State explicitly: `Single-tier change — no cross-stack seam`. Backend-only or single-tier repo still traces internal consumers (`SYNC:cross-service-check` for service/event boundaries).
>
> **BLOCKED until:** Change Context noted · seam(s) identified or explicit N/A · full pipeline traced in change direction · every changed seam classified NONE / ADDITIVE / BREAKING.

<!-- /SYNC:cross-stack-impact-trace -->

<!-- SYNC:cross-service-check -->

> **Cross-Service Check** — Microservices/event-driven: MANDATORY before concluding investigation, plan, spec, or feature doc. Missing downstream consumer = silent regression.
>
> | Boundary            | Grep terms                                                                      |
> | ------------------- | ------------------------------------------------------------------------------- |
> | Event producers     | `Publish`, `Dispatch`, `Send`, `emit`, `EventBus`, `outbox`, `IntegrationEvent` |
> | Event consumers     | `Consumer`, `EventHandler`, `Subscribe`, `@EventListener`, `inbox`              |
> | Sagas/orchestration | `Saga`, `ProcessManager`, `Choreography`, `Workflow`, `Orchestrator`            |
> | Sync service calls  | HTTP/gRPC calls to/from other services                                          |
> | Shared contracts    | OpenAPI spec, proto, shared DTO — flag breaking changes                         |
> | Data ownership      | Other service reads/writes same table/collection → Shared-DB anti-pattern       |
>
> **Per touchpoint:** owner service · message name · consumers · risk (NONE / ADDITIVE / BREAKING).
>
> **BLOCKED until:** Producers scanned · Consumers scanned · Sagas checked · Contracts reviewed · Breaking-change risk flagged

<!-- /SYNC:cross-service-check -->

<!-- SYNC:systematic-review-batching -->

> **Systematic Review Batching (map-reduce)** — When a changeset is large, do NOT review files one-by-one. Partition into size-capped batches, fire one specialized sub-agent per batch in parallel, then reduce. This bounds EVERY context — each batch agent AND the orchestrator — so coverage stays complete as file count grows.
>
> **Trigger ladder (one ordered escalation — not competing thresholds):**
>
> 1. **< 10 changed files** → sequential per-file review (default; no batching).
> 2. **≥ 10 changed files** → switch to systematic parallel mode. Announce: `"Detected {N} changed files. Switching to systematic parallel review protocol."` Then: categorize → size-capped batches → flat consolidation.
> 3. **categories > 6 OR files > 40** → additionally insert the hierarchical synthesis tier (below). Everything from rung 2 still applies.
>
> **Step 1 — Categorize.** Group changed files into logical categories derived from the project's actual structure (not forced). Category is the *concern axis*; orient with these examples, derive what fits the repository:
>
> | Category Type | Example Groupings |
> | --- | --- |
> | Agent/Tooling | AI scripts, hooks, skill definitions, workflow configs, linting rules |
> | Root config/docs | Root README, project config, CI/CD pipeline configs |
> | Reference docs | Architecture docs, patterns references, setup guides |
> | Feature/domain docs | Business feature documentation, spec files, ADRs |
> | Backend logic | Service/handler/controller source (infer from project structure) |
> | Frontend logic | UI component/state/API source (infer from project structure) |
> | Data/Schema | Migrations, schema files, seed data |
> | Tests | Unit, integration, E2E test files |
> | Infrastructure | Docker, k8s, CI/CD, cloud manifests |
>
> **Step 2 — Risk-weighted batches.** Size caps bound each agent's context; the risk tier decides how tight the cap is. Classify each category's tier FIRST — a file whose tier is unclear takes the high-risk tier:
>
> | Risk tier | Examples | Batch cap (whichever hits first) |
> | --- | --- | --- |
> | **High** | domain/business logic, commands/handlers/jobs, schema/migrations/data access, auth/permissions/secrets/money/PII, concurrency, public contracts, UI with state or requests | ≤8 files OR ≤2000 diff-lines — one category per batch |
> | **Low** | UI styling/markup with no logic, tests, docs and specs, configuration text | ≤20 files OR ≤4000 diff-lines — low-risk categories may share a batch |
> | **Mechanical churn** | generated files, lockfiles, pure renames/moves, bulk formatting | no batch agent — the orchestrator verifies by pattern (rule check plus a sample) and records it in the coverage ledger |
>
> Any category exceeding its cap splits into more batches (30 high-risk backend files → 4 batches). Size caps — not category caps — make "many files" safe: a category cap alone lets one giant category blow a single agent's context. Risk weighting spends line-by-line depth where a defect costs most; the whole-target reviewer and specialist escalation still cover low-risk files.
>
> **Step 2a — Sub-agent type per batch** (match the batch's dominant concern):
>
> - Code logic (any stack) → `code-reviewer`
> - Security-sensitive changes → `security-auditor`
> - Performance-critical paths → `performance-optimizer`
> - Docs, plans, specs, configs, infra → `general-purpose`
>
> Each batch sub-agent receives: its full file list; the Step 2b instruction to validate its own findings; `SYNC:category-review-thinking` as its primary thinking model — derive each category's concerns from first principles, NOT a fixed checklist (if the consuming skill does not carry that block, apply category-first thinking directly); project reference docs relevant to its concern (discover via `*patterns*`, `*conventions*`, `*style-guide*`); cross-reference verification instructions (counts, tables, links). All batch agents run in parallel and write findings to `tmp/reports/` (per `SYNC:task-tracking-external-report`); reducers read from disk, never from memory.
>
> **Step 2b — Each batch validates its own findings before returning.** The batch agent runs `$why-review --validate-findings <its batch report>` — a real terminal skill call in its own session, where the batch's code and protocols are already loaded — keeps the findings that survive, marks each `validated: in-batch`, lists every finding it rejected or re-tiered with its original severity, and never fixes. This matches report-only specialists and avoids re-loading the same context in a separate validator.
>
> **Step 3 — Reduce.**
>
> - **Deduplicate FIRST — before any validation or fix.** Merge findings that share one root cause (same owning `file:line` range and same violated rule or invariant) into one entry that lists every source batch/reviewer, keeps the highest justified severity plus each source's own severity, and records the merge — a severity disagreement between sources is a reviewer conflict. A cross-batch duplicate is never validated or fixed twice.
> - **Independent check set (after dedup).** In-batch validation trades independence for cost, so the orchestrator re-validates with `$why-review --validate-findings` in the main session: every finding raised or kept at CRITICAL/HIGH, including one its batch rejected or demoted; every finding two reviewers disagree on (severity, owner or fix); every finding its batch did not mark `validated: in-batch`; and at least one in three of each batch's MEDIUM findings (minimum one), picked by position in the batch report, never by content. When a batch's sample shows unreliable validation — more than one in four sampled findings rejected or re-tiered — validate all of that batch's MEDIUM findings. The remaining LOW and unsampled MEDIUM findings ride on their in-batch validation. Keep each validation pass small enough that every finding in it gets full attention.
> - **Flat reduction (rung 2, ≤6 categories AND ≤40 files):** the orchestrator collects each batch report, cross-references counts/tables/contracts ACROSS batches, detects gaps visible only across categories (feature in code but missing from docs; new API endpoint with no client call), and consolidates into one categorized holistic report.
> - **Hierarchical reduction (rung 3, > 6 categories OR > 40 files):** insert a mid-tier — each concern with two or more batches gets ONE synthesizer agent that reads only its own batch reports and emits a single concern-synthesis (a single-batch concern needs no synthesizer: its batch report is its synthesis). The orchestrator reads the **concern-syntheses (~5)**, never the raw batch reports — keeping the reducer's context O(#concerns), not O(#files).
>   - **Cross-concern interaction pass (mandatory at rung 3 — closes the synthesis-tier blind spot):** concern-siloed synthesis can drop an interaction spanning two concerns AND two batches (tainted source in data-layer/batch 7 → sink in api/batch 3). So: (a) each concern-synthesizer MUST emit an explicit **"cross-concern interaction candidates"** list — entities/symbols/contracts it touched that plausibly bind to another concern (shared DTOs, event names, table/collection names, exported symbols); (b) the orchestrator MUST run the Step-3 cross-reference/gap step **over those candidate lists across all concern-syntheses**, not only within a batch, before concluding. Without this pass the tier trades completeness for context-bounding on exactly the large diffs it targets.
>
> **Step 4 — Holistic assessment.** With all findings combined, judge: overall coherence as a unified intent; cross-category sync (docs match code? contracts match callers?); risk areas where categories interact; missing doc/spec updates for changed artifacts.
>
> **No silent truncation.** If any cap forces sampling or a batch is dropped for budget, ANNOUNCE the dropped/sampled scope explicitly — bounded coverage must never read as complete coverage.

<!-- /SYNC:systematic-review-batching -->

<!-- SYNC:end-to-start-debugger-trace -->

> **End-to-Start Debugger Trace** — For non-trivial bugs, failed verification, regression fixes, behavior-changing code, or unclear code flow, start from the observed final state and walk backward before proposing a fix.
>
> 1. **Frame 0: observed end state** — Name the exact user-visible output, failing assertion, log line, persisted value, API response, rendered UI, or aggregate bucket. Record the reader/query/renderer that produced it with `file:line` evidence.
> 2. **Walk backward one hop at a time** — Trace final reader -> projection/cache/storage -> writer -> consumer/handler/job -> producer/caller -> original trigger. At every hop record: input, transformation, output, owner, and evidence.
> 3. **Enumerate all feeder paths** — Find every upstream producer/caller/event/job that can write into the final path, including retry, async, cache, background, and alternate UI/API paths. Mark each path verified, ruled out, or still unknown.
> 4. **Build the hypothesis matrix** — For each plausible cause, list evidence for, evidence against, how to reproduce/verify, blast radius, and status (`primary`, `contributing`, `ruled out`, `latent`). Do not fix until competing causes are explicitly resolved or bounded.
> 5. **Choose the owning fix layer** — Identify the invariant owner and select the authoritative correction and enforcement points from traced contracts and the project's architecture. Keep validation at untrusted boundaries. Choose a shared point only when evidence shows it owns the invariant for those consumers. A fix at the symptom site is rejected unless the symptom site owns the invariant.
> 6. **Prove convergence forward** — After choosing the fix, walk start -> end again and show how the corrected state reaches the observed final output. Map each root cause to a fix part and each fix part to a test/proof.
>
> **BLOCKED until:** final state named · backward trace written · all feeder paths enumerated · hypothesis matrix completed · owning fix layer justified · forward convergence proof mapped to tests.
>
> **NEVER:** Start at the first suspicious code path. Collapse multiple producers into one "flow". Treat duplicate symptoms as duplicate records without proving the read model. Skip ruled-out hypotheses.

<!-- /SYNC:end-to-start-debugger-trace -->

<!-- SYNC:sequential-thinking-protocol -->

> **Sequential Thinking Protocol** — Structured multi-step reasoning for complex/ambiguous work. Use when planning, reviewing, debugging, or refining ideas where one-shot reasoning is unsafe.
>
> **Trigger when:** complex problem decomposition · adaptive plans needing revision · analysis with course correction · unclear/emerging scope · multi-step solutions · hypothesis-driven debugging · cross-cutting trade-off evaluation.
>
> **Format (explicit mode — visible thought trail):**
>
> 1. `Thought N/M: [aspect]` — one aspect per thought, state assumptions/uncertainty
> 2. `Thought N/M [REVISION of Thought K]: ...` — when prior reasoning invalidated; state Original / Why revised / Impact
> 3. `Thought N/M [BRANCH A from Thought K]: ...` — explore alternative; converge with decision rationale
> 4. `Thought N/M [HYPOTHESIS]: ...` then `[VERIFICATION]: ...` — test before acting
> 5. `Thought N/N [FINAL]` — only when verified, all critical aspects addressed, confidence >80%
>
> **Mandatory closers:** Confidence % stated · Assumptions listed · Open questions surfaced · Next action concrete.
>
> **Stop conditions:** confidence <60% on any critical decision → stop and escalate using ask user tool (60-80% → verify first) · ≥3 revisions on same thought → re-frame the problem · branch count >3 → split into sub-task.
>
> **Implicit mode:** apply methodology internally without visible markers when adding markers would clutter the response (routine work where reasoning aids accuracy).

<!-- /SYNC:sequential-thinking-protocol -->

<!-- SYNC:understand-code-first -->

> **Understand Existing Code First** — For code changes, read and trace the target before planning or editing; do not apply a code workflow to work with no code surface.
>
> 1. Search for relevant existing implementations and cite `file:line`; aim for 3+ comparable examples when they exist, and record when the project has fewer or none.
> 2. Read the target area and its configured project references; identify actual structure, owners, and conventions without assuming a framework, layer model, or base class.
> 3. Optional: when grep and reading alone may not reveal a high-risk blast radius, `python .claude/scripts/code_graph trace <file> --direction both --json` (when `.code-graph/graph.db` exists) can add callers and dependents — a hint that may be stale, verified by reading the files.
> 4. Map affected dependencies and callers with available repository tools (grep, reading); an absent, stale or unsupported graph never blocks or fails the task.
> 5. Write investigation to `tmp/analysis/` for non-trivial tasks (3+ files).
> 6. Re-read the analysis before implementing; update it when evidence changes.
> 7. Follow a fitting local pattern, or state why no suitable pattern exists and justify a project-appropriate choice.
>
> **BLOCKED until:** target and relevant existing patterns are inspected, applicable dependencies are traced, and material assumptions have evidence. If an item does not apply or the repository has no comparable implementation, record that fact rather than fabricating a gate result.

<!-- /SYNC:understand-code-first -->

<!-- SYNC:design-patterns-quality -->

> **Design Quality** — Be opinionated about changeability, and choose techniques by their preconditions. For brownfield work, project config, references, accepted decisions, and current code define the local architecture; do not silently replace a settled pattern. For a new non-trivial system, treat the options below as hypotheses; use the domain, change, and deployment boundaries to select a fit, not a universal target architecture.
>
> 1. **DRY the knowledge, not merely the text.** Keep one owner for a business rule or policy that must change together. Similar-looking code with different reasons to change may stay separate; extract shared functions, modules, types, or components when a real consumer and lower change cost justify them.
> 2. **Give modules explicit responsibilities and dependency direction.** A modular monolith can fit a new application with one release boundary and no evidenced need for independent deployment, scaling, compliance, availability, or runtime; choose another topology when measured ownership or operating boundaries require it. Use Clean/Hexagonal/Ports-and-Adapters ideas to keep policy independent of volatile infrastructure when that boundary buys testability or change isolation. Add layers only when each owns a real contract; split deployment/services only for a demonstrated scaling, ownership, availability, compliance, or release need.
> 3. **Model the domain to its actual complexity.** Use DDD language, aggregates, value objects, and explicit invariants where domain rules and lifecycle matter. Keep straightforward CRUD workflows simple; do not add tactical DDD ceremony without domain complexity.
> 4. **Use events for real decoupling.** Domain/integration events and messaging fit asynchronous reactions or independently owned modules/services. Define idempotency, ordering, retry/recovery, and an outbox/CDC strategy when delivery crosses a durable boundary. Use a direct call inside one consistency boundary when asynchronous delivery adds no value.
> 5. **Use Repository and Unit of Work at meaningful persistence boundaries.** They fit when they protect aggregate/query contracts, isolate a changing persistence technology, or coordinate a real transaction. Do not wrap every ORM call in a generic repository or add a Unit of Work that duplicates the platform's transaction behavior.
> 6. **Apply OOP/SOLID where the language and model use objects.** Prefer cohesive responsibilities, dependency inversion at volatile boundaries, and composition before inheritance; avoid interface-per-class and abstractions with no second implementation or test seam. In functional or data-oriented code, preserve the same cohesion, explicit dependencies, and small contracts without forcing classes.
> 7. **Build UI from cohesive components.** Keep state at the narrowest useful owner; use a store for state genuinely shared across components/routes or for coordinated async data. Add caching only with a freshness/invalidation policy and evidence of a repeated or expensive read. Use the framework's reactive model for composable asynchronous changes and dispose subscriptions/resources by its lifecycle. Apply BEM when the project uses SCSS/BEM; otherwise follow the selected CSS modules, utility, or naming method.
> 8. **Place behavior with its invariant/data owner.** Trace callers and dependencies; use the owner selected by the project's architecture. Do not assume Entity > Service > Controller, or any other fixed layer order.
> 9. **After extraction/move/rename:** grep the full affected scope for dangling references. Preserve project naming/style and verify caller contracts before changing an abstraction.
>
> **Selection gate:** read project config, references, accepted decisions, and comparable implementations. Name the problem/precondition a chosen pattern solves, the simpler alternative, and the trade-off. Configuration may select a stack-specific pattern; it does not make an unjustified abstraction free.
>
> **Review dimensions:** use focused passes over applicable concerns, then group repeated, evidenced violations when they share one cause. A repeated smell is not automatically a defect; name the damaged quality attribute and project-specific consequence.

<!-- /SYNC:design-patterns-quality -->

<!-- SYNC:complexity-prevention -->

> **Complexity Prevention (Ousterhout)** — Use change cost as a review lens, not as a technology checklist. Apply each concern only when its code path and project architecture make it relevant; absence of a pattern is not a defect.
>
> 1. **Change amplification** — estimate edit sites for a plausible change in this area. Several coordinated edits may indicate duplication or a missing owner, but assess cohesion and trade-offs before calling it structural.
> 2. **Cognitive load** — look for unnecessary dependencies, implicit ordering, boolean traps, hidden state, or nesting that makes a local change hard to reason about.
> 3. **Repeated cross-cutting behavior** — where logging, validation, authorization, error handling, or transactions recur, consider an existing shared mechanism that fits the project's runtime; do not prescribe middleware/interceptors/aspects where none exist.
> 4. **Leaked implementation detail** — when an abstraction boundary exists, check whether callers depend on provider/query/storage details unnecessarily. ORM queries, cursors, repositories, and query sets are examples only.
> 5. **Scattered variant logic** — repeated switches or conditionals over the same discriminator may signal a useful owner or dispatch point; retain simple local branches when they fit better.
> 6. **Invariant ownership** — verify that rules are protected by the owner chosen in this architecture. Rich entities, value objects, functional modules, and service-owned rules are all valid when consistent with project evidence.
> 7. **Primitive/domain types** — introduce a richer type only when it reduces repeated validation or protects an evidenced invariant; do not wrap every primitive by default.
> 8. **Cross-cutting policy** — centralize recurring policy when the project has a suitable extension point; one-off behavior may remain local.
> 9. **Module depth** — assess whether an abstraction hides meaningful work or adds more concepts than it removes; class/interface counts are examples, not requirements.
> 10. **Repeated lifecycle behavior** — repeated component, handler, job, or resource lifecycle may justify the project's idiomatic abstraction (function, hook, composable, trait, class, or helper), but only after fit and consumer evidence.
> 11. **Abstraction timing** — repetition triggers evaluation, not automatic extraction. Compare the cost of duplication with the indirection and future variation an abstraction creates.
> 12. **Reusable algorithms** — when a non-trivial stack-generic algorithm repeats, prefer a coherent existing helper or an evidenced shared owner; do not create utility layers for hypothetical reuse.
> 13. **Place computation with its data and invariant owner** — trace callers and use the architecture's documented responsibility model. There is no universal controller/service/entity/model order.
> 14. **Extraction decision** — move or share a rule when doing so gives it one clear owner or serves real consumers. A single use is not sufficient evidence by itself; keep code local when extraction would add ceremony.
>
> **Illustrative shapes only:** entity method, DTO mapper, domain service, application service, pure function, module, middleware, repository, store, or component can be appropriate depending on project evidence. Never use this list as a required target architecture.
>
> **Operating heuristics:** read callers and sibling implementations, count affected edit sites, prefer removing unnecessary code, surface assumptions at boundaries, and ask what changes when the requirement shifts. Measure good code by safe change cost in its actual context, not by a universal layer diagram.

<!-- /SYNC:complexity-prevention -->


<!-- SYNC:review-protocol-injection -->

> **Review Protocol Injection** — Fresh reviewer prompts MUST embed 11 protocol blocks VERBATIM, copied WHOLESALE; these are review-tier renderings. When canonical `SYNC:` protocols change, update their renderings here in the same edit. Copy this template into the Agent `prompt`; replace only `{placeholders}` in Task / Round / Reference Docs / Target Files / Output. Never alter embedded sections at dispatch.
>
> **Why inline expansion:** Fresh reviewers need every rule immediately; file pointers/placeholders depend on reads or hooks that may not fire. The hybrid policy (`SYNC:shared-protocol-duplication-policy`) therefore retains all 11 full bodies in this template, copied wholesale.

### Subagent Type Selection

- `code-reviewer` — for code reviews (reviewing source files, git diffs, implementation)
- `general-purpose` — for plan / doc / artifact reviews (reviewing markdown plans, docs, specs)

### Canonical Agent Call Template (Copy Verbatim)

```
spawn_agent({
  description: "Fresh Round {N} review",
  agent_type: "code-reviewer",
  prompt: `
## Task
{review-specific task — e.g., "Review all uncommitted changes for code quality" | "Review plan files under {plan-dir}" | "Review integration tests in {path}"}

## Round
Round {N}; ZERO prior-round memory. Re-read every target with your own tools. Trust no main-agent information beyond this prompt.

## Protocols (follow VERBATIM — these are non-negotiable)

### Spec ↔ Tests ↔ Code Triangulation
FIRST review the WHOLE PACKAGE. Read `docs/project-config.json`: valid `specArtifacts` profiles select configured `intent/contracts/evidence` roles, identifiers, ownership and test-carrier dialects; only absent profiles use strict-default §3 ACs / §4 BRs / §5 invariants / §8 TCs. Malformed/unsupported declarations are `BLOCKED`, never absent/fallback. Load governing artifact, tests, and changed code TOGETHER; judge mutual consistency before isolated checks.
1. Locate canonical owner sections, guarding tests, and implementing code. Native profiles: preserve owner path + case/scenario ID + optional variant; resolve configured carriers to actual tests. Missing faces are findings (SPEC-GAP / TEST-GAP / DEAD-SPEC).
2. Triangulate pairwise; log every disagreement and classify its wrong face:
   - code vs spec: behavior absent from configured `intent/contracts` (or strict-default §3/§4/§5/§8) → CODE-EXTRA or SPEC-STALE; a hard contract/invariant with no enforcing path → CODE-WRONG.
   - tests vs spec: native case without executing assertions, or assertions absent from native rules/cases → TEST-GAP or SPEC-SILENT. Without `specArtifacts`, check strict-default §8 TCs.
   - tests vs code: uncovered changed path → TEST-GAP; test passing a deliberately broken invariant → WEAK-TEST (apply the mutation thinking in Bug Detection).
3. Hidden-rule capture: enforced but unstated invariants (SPEC-SILENT) MUST become findings, additions to configured `intent`/`contracts`, and `evidence` links to native cases with inspected executing assertions. Without profiles, use strict-default §3/§4/§5/§8 and TC. Enrich; never silently pass.
4. Proceed only after agreement or all disagreements are logged; re-review enriched spec/test packages.
NEVER PASS unlogged spec/test/code disagreements. Diff = entry point; package = judgment unit.

### Evidence-Based Reasoning
Speculation FORBIDDEN; prove every claim.
1. Every claim: cite file:line, grep results, or framework docs
2. Confidence: >80% act freely; 60-80% verify first; <60% DO NOT recommend
3. Cross-service validation required for architectural changes
4. Insufficient evidence is valid/expected output
BLOCKED until: Evidence file path (file:line) provided; Grep search performed; 3+ similar patterns found; Confidence level stated.
Forbidden without proof: "obviously", "I think", "should be", "probably", "this is because".
If incomplete → output: "Insufficient evidence. Verified: [...]. Not verified: [...]."

### Bug Detection
MUST check categories 1-4 for EVERY review. Never skip.
1. Null Safety: Can params/returns be null? Are they guarded? Optional chaining gaps? .find() returns checked?
2. Boundary Conditions: Off-by-one (< vs <=)? Empty collections handled? Zero/negative values? Max limits?
3. Error Handling: Try-catch scope correct? Silent swallowed exceptions? Error types specific? Cleanup in finally?
4. Resource Management: Connections/streams closed? Subscriptions unsubscribed on destroy? Timers cleared? Memory bounded?
5. Concurrency (if async): Missing await? Race conditions on shared state? Stale closures? Retry storms?
6. Stack-Specific: Check the configured language/runtime pitfalls and framework-specific failure modes discovered from local code.
Admit a finding only with a reachable trigger path (the caller, input or state that reaches the defect) and a consequence; a concern no supported path reaches is an observation, and unsettled reachability is `NOT VERIFIABLE` only when the concern would be MEDIUM or higher.
Classify every finding by consequence (never by effort): CRITICAL = immediate material security/safety/data-loss risk or failed binary gate → block; HIGH = material correctness, contract, privacy, or authority risk → must fix; MEDIUM = bounded consequential edge/resilience/maintainability gap → must clear the current round, or escalate with an explicit residual-risk follow-up that does not create a clean pass; LOW = non-blocking polish with no credible present impact → record/defer from round 2; `NOT VERIFIABLE` is unresolved evidence, not LOW.

### Design Patterns Quality
Every code change:
1. Consistency/reuse: follow documented patterns; justify extraction cost by repetition or real consumer need. Similar names alone never require shared bases.
2. Responsibility: follow config/references/accepted decisions/code; place behavior with its owner. Assume no entity/service/controller hierarchy or forbidden layer without evidence.
3. Apply cohesion/coupling/dependency principles where paradigm assumptions fit; SOLID suits OO boundaries, not every language/codebase.
4. After extraction/move/rename: Grep ENTIRE scope for dangling references. Zero tolerance.
5. YAGNI: repetition prompts evaluation, never numeric extraction thresholds. Extract when shared change reasons, real consumers, or evidenced ownership/substitution lower total change cost; no hypothetical-use patterns.
6. Purpose naming: public/cross-layer abstractions name consumer capability/domain/contract, not provider/SDK/framework/database/transport. `IStorage`/`Storage` → `AzureBlobStorage`; use `IAzureStorage` only when Azure-specific semantics are intentionally part of the contract.
7. Contract-fit: read callers/all implementations; narrow over-broad abstractions (`IObjectStore`, `DocumentStore`), never reward misleading generic names.
8. Naming signals: `Manager`, `Helper`, `Utils`, `Data`, `Thing`, `Service`, `Interface`, type decorations/unexplained abbreviations are defects only when hiding purpose/scope/responsibility.
9. Concrete names: provider/strategy/transport/test-double names may distinguish real behavior (`AzureBlobStorage`, `InMemoryStorage`, `RetryingStorage`); exclude from caller contracts unless promised.
10. Preserve local interface syntax/naming: `.NET` `I` prefixes and Google TypeScript unmarked interfaces are both valid.
Anti-patterns to flag: God Object, Copy-Paste inheritance, Circular Dependency, Leaky Abstraction.

### Logic & Intention Review
Verify behavior matches change intent.
1. Every changed file MUST serve stated purpose; flag unrelated scope creep.
2. Trace one complete success scenario through changed code.
3. Trace one failure/edge scenario through changed code.
4. With plan context, map every acceptance criterion to code.
5. Test/spec changes: tests name protected business rule/invariant and fail when it breaks.
6. Migration exclusion: no migration-code tests; schema/data migrations are one-time paths, not core application logic.
NEVER PASS without both happy/error traces.

### Test Spec Verification
Map changed code to test specs.
1. Discover test/spec format in docs, test cases, BDD features, or spec folders.
2. Every changed path MUST map to a test case/spec or be flagged "needs test case".
3. New functions/endpoints/handlers → test-spec creation flag.
4. Exclude migrations from test/spec creation: one-time execution, not core application logic.
5. Verify existing spec evidence resolves actual code (file:line); flag stale references.
6. Meaningful cases name business intent/invariants; flag implementation-mirroring behavior-only cases.
7. Auth/data changes → verify corresponding authorization and data-state test cases exist.
8. Missing changed-path specs → log gap, recommend project test-spec workflow.
NEVER skip test mapping; uncovered paths risk production bugs.

### Behavioral Delta Matrix
MANDATORY for any bugfix review. Produce input-state × pre-fix × post-fix × delta table BEFORE writing verdict.
- Minimum 3 rows; include at least one row OUTSIDE the original bug report.
- Any "REGRESSION" delta → review returns FAIL until a preservation test is added.
- Narrative descriptions do NOT substitute for the matrix.
Example rows (external-record sync fix):
| Input                 | Pre-fix | Post-fix                  | Delta      |
| --------------------- | ------- | ------------------------- | ---------- |
| Record exists (valid) | Reused  | Always recreated → orphan | REGRESSION |
| Record missing (404)  | Error   | Recreated                 | Fixed      |

### Fix-Layer Accountability
Trace execution/data flow; fix the violated contract's owner, never assume the crash site.
MANDATORY before ANY fix:
1. Trace actual origin, transformations, boundaries, failure; invent no absent layers.
2. Identify invalid-state/behavior contract owner from architecture/code evidence.
3. Fix authoritative owner; retain untrusted-boundary validation. Justify multi-file fixes by owned contracts, not file-count thresholds.
4. Inspect relevant existing bypass entries: constructors/adapters/parsers/caches/persistence.
BLOCKED until: The affected path is traced; the owner is supported by file:line evidence; relevant consumers and bypass paths are checked; and the correction point fits the project's architecture.
Anti-patterns (REJECT): assuming the symptom site is the owner; scattering workarounds without tracing the contract; assuming the lowest technical layer is always authoritative; removing validation from a real trust boundary to force a single correction point.

### Rationalization Prevention
AI skips steps via these evasions. Recognize and reject:
- "Too simple for a plan" → Simple + wrong assumptions = wasted time. Plan anyway.
- "I'll test after" → RED before GREEN. Write/verify test first.
- "Already searched" → Show grep evidence with file:line. No proof = no search.
- "Just do it" → Still need task tracking. Skip depth, never skip tracking.
- "Just a small fix" → Small fix in wrong location cascades. Verify file:line first.
- "Code is self-explanatory" → Future readers need evidence trail. Document anyway.
- "Combine steps to save time" → Combined steps dilute focus. Each step has distinct purpose.

### Graph-Assisted Investigation (optional advice)
Optional: for high-risk blast radius (shared contract/many callers/cross-module/cross-service/public API), .code-graph/graph.db suggests callers/dependents/impacted tests. Treat it as a hint, NOT proof: stale/incomplete graphs lag uncommitted edits/unindexed paths. Verify important results by files/grep; skip low-risk/local changes. An absent or stale graph is never a finding.
Pattern: grep/read → optional graph suggestions → grep/read verification.
- High-risk investigation: trace --direction both on 2-3 entry files
- Fix/debug with wide reach: callers_of on buggy function + tests_for
- Feature touching a shared contract: connections on files to be modified
- Review of a high-risk change: tests_for on changed functions
- Blast radius: trace --direction downstream
CLI: python .claude/scripts/code_graph {command} --json. Use --node-mode file first (10-30x less noise), then --node-mode function for detail.

### Understand Code First
HARD-GATE: Do NOT write, plan, or fix until you READ existing code.
1. Search 3+ similar patterns (grep/glob) — cite file:line evidence.
2. Read existing files in target area — understand structure, base classes, conventions.
3. Optional high-risk hints: python .claude/scripts/code_graph trace <file> --direction both --json if .code-graph/graph.db exists; verify stale-capable caller/dependent hints by files.
4. Map dependents by grep/read callers; optional graph connections/callers_of adds hints.
5. Write investigation to tmp/analysis/ for non-trivial tasks (3+ files).
6. Re-read analysis file before implementing — never work from memory alone.
7. NEVER invent new patterns when existing ones work — match exactly or document deviation.
BLOCKED until: Read target files; Grep 3+ patterns; Assumptions verified with evidence. (The code graph is optional advice, never a gate.)

## Reference Docs (READ before reviewing)
Read only lane-resolved docs; do not re-resolve the whole set.
- `code-review-rules.md`, inside the reference-docs root (default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path)
- {lane-specific docs the orchestrator resolved — e.g., the pattern doc for the files under review, integration-test-reference.md for a test lane, the governing spec for a spec-compliance lane}

## Target Files
{explicit file list OR "run git diff to see uncommitted changes" OR "read all files under {plan-dir}"}

## Output
Write a structured report to tmp/reports/{review-type}-round{N}-{date}.md with sections:
- Status: PASS | FAIL
- Issue Count: {number}
- Critical Issues (with file:line evidence)
- High Priority Issues (with file:line evidence)
- Medium / Low Issues
- Cross-cutting findings

Return the report path and status to the main agent.
Every finding MUST have file:line evidence. Speculation is forbidden.
`
})
```

### Rules

- DO copy the template wholesale — including all 11 embedded protocol sections
- DO replace only the `{placeholders}` in Task / Round / Reference Docs / Target Files / Output sections with context-specific content
- DO choose `code-reviewer` agent_type for code reviews and `general-purpose` for plan / doc / artifact reviews
- DO NOT paraphrase, summarize, or skip any protocol section
- DO NOT pass file contents inline — the sub-agent reads via its own tool calls so it has a fresh context
- DO NOT reference protocols by file path or tag name — the bodies are already embedded above
- DO NOT introduce placeholder markers for the protocols — they must stay literally expanded

<!-- /SYNC:review-protocol-injection -->

<!-- SYNC:logic-and-intention-review -->

> **Logic & Intention Review** — Verify WHAT code does matches WHY it was changed.
>
> 1. **Change Intention Check:** Every changed file MUST serve the stated purpose. Flag unrelated changes as scope creep.
> 2. **Happy Path Trace:** Walk through one complete success scenario through changed code
> 3. **Error Path Trace:** Walk through one failure/edge case scenario through changed code
> 4. **Acceptance Mapping:** If plan context available, map every acceptance criterion to a code change
> 5. **Tests Verify Intent:** For test/spec changes, verify tests name the protected business rule or invariant and would fail if that intent breaks.
> 6. **Migration Test Exclusion:** Do not write tests for migration code. Schema/data migrations are one-time execution paths, not core application logic.
>
> **NEVER mark review PASS without completing both traces (happy + error path).**

<!-- /SYNC:logic-and-intention-review -->

<!-- SYNC:bug-detection -->

> **Bug Detection** — MUST ATTENTION check categories 1-4 for EVERY review. Never skip.
>
> 1. **Null Safety:** Can params/returns be null? Are they guarded? Optional chaining gaps? `.find()` returns checked?
> 2. **Boundary Conditions:** Off-by-one (`<` vs `<=`)? Empty collections handled? Zero/negative values? Max limits?
> 3. **Error Handling:** Try-catch scope correct? Silent swallowed exceptions? Error types specific? Cleanup in finally?
> 4. **Resource Management:** Connections/streams closed? Subscriptions unsubscribed on destroy? Timers cleared? Memory bounded?
> 5. **Concurrency (if async):** Missing `await`? Race conditions on shared state? Stale closures? Retry storms?
> 6. **Stack-Specific:** Check the configured language/runtime pitfalls and framework-specific failure modes discovered from local code.
>
> **Admit a finding only with a reachable trigger path** (the caller, input or state that reaches the defect) and a consequence; an unreachable concern is an observation, and unsettled reachability is `NOT VERIFIABLE` only when the concern would be MEDIUM or higher (`SYNC:severity-rubric`).
>
> **Classify every finding by consequence, not by fix effort; `SYNC:severity-rubric` is authoritative and this is only a quick reminder:**
> - **CRITICAL → block immediately:** an immediate material security/authorization or safety bypass, secret/PII exposure, destructive action, data loss/corruption, or silent failure on a critical path. A failed binary gate is a separate hard blocker (represented as synthetic CRITICAL by the executable policy), not an ordinary tier judgment.
> - **HIGH → must fix before PASS/merge:** wrong behavior on a supported path, violated business/data invariant, meaningful privacy/authority gap, breaking contract/compatibility change, likely material harm, or missing proof for a behavior-changing fix.
> - **MEDIUM → clear before the current round can pass:** a bounded but consequential edge case, resilience/observability/testability/maintainability gap, credible future defect, or local architectural drift with real impact but no immediate material loss. If the fix needs an owner/product decision, stop and escalate with an explicit follow-up and residual-risk record; that record is not a clean-pass waiver.
> - **LOW → record/defer from round 2 onward:** wording/formatting, minor documentation or convention drift, optional defensive cleanup, or cosmetic refinement with no credible present correctness, security, privacy, authority, availability, or data-integrity impact.
> Assign the highest tier supported by evidence. An observation is not a finding until it names the affected asset/user/data/contract, consequence, evidence, and tier. Effort, annoyance, implementation cost, and proximity to the round cap are never severity inputs. `NOT VERIFIABLE` is an evidence state, not a tier; if the unresolved claim could affect a required behavior or binary gate, keep it blocking until proved or explicitly owner-accepted with residual risk. Failed tests, parity, required artifacts, and security-must-fix checks are binary gates and block independently of severity. For the full decision tree, boundary examples, score mappings, and domain-vocabulary normalization, follow `SYNC:severity-rubric`.

<!-- /SYNC:bug-detection -->

<!-- SYNC:test-spec-verification -->

> **Test Spec Verification** — Map changed code to test specifications.
>
> 1. Identify the project's test/spec format from existing docs, test-case files, BDD feature files, or spec folders.
> 2. Every changed code path MUST ATTENTION map to a corresponding test case/spec (or flag as "needs test case")
> 3. New functions/endpoints/handlers → flag for test spec creation
> 4. Migration files are excluded from TC/test creation; schema/data migrations are one-time execution paths, not core application logic.
> 5. If spec evidence fields exist, verify they point to actual code (`file:line`, not stale references)
> 6. Verify each meaningful test case names the business intent/invariant; flag behavior-only cases that only mirror implementation details.
> 7. Auth/data changes → verify corresponding authorization and data-state test cases exist.
> 8. If no specs exist for a changed path → log the gap and recommend the project's test-spec workflow.
>
> **NEVER skip test mapping.** Untested code paths are the #1 source of production bugs.

<!-- /SYNC:test-spec-verification -->

<!-- SYNC:integration-test-sync-check -->

> **Integration Test Sync Check** — Verify changed business logic files have corresponding tests.
>
> 1. From changed files → identify **business logic files**: handlers, commands, queries, services, controllers, resolvers, event processors. Naming varies by stack — infer from project conventions (e.g., `*Service.*`, `*Handler.*`, `*Controller.*`, `*Command.*`, `*Query.*`, `*Resolver.*`). Exclude migration files: schema/data migrations are one-time execution paths, not core application logic.
> 2. For each identified file → search for a corresponding test file. Infer test naming from existing tests in the project (e.g., `*.test.ts`, `*Tests.java`, `*_test.py`, `*.spec.js`, `*Tests.cs`). Check standard test directories (`tests/`, `spec/`, `__tests__/`, or adjacent test projects/packages).
> 3. If test EXISTS → check if test methods cover changed behavior (new methods/parameters/logic paths)
> 4. If test MISSING → **MANDATORY**: use ask user tool: "Business logic file `{file}` has no integration tests — run `$integration-test` before proceeding, or confirm tests already written?" Options: "Run `$integration-test` first" (Recommended) | "Tests already written/updated — proceed"
> 5. Severity: **HIGH** — missing tests for changed business logic MUST be surfaced to the user; do NOT silently flag and continue
>
> **Surface every business-logic change that lacks test coverage for an explicit user decision using ask user tool — never silently skip. — why: a silent skip ships untested business logic to production.**

<!-- /SYNC:integration-test-sync-check -->

<!-- SYNC:translation-sync-check -->

> **Translation Sync Check** — Verify multilingual UI changes include translation updates.
>
> 1. Determine multilingual mode from project config: `localization.enabled === true` and `supportedLocales.length > 1`
> 2. Detect UI-facing file changes via extensions/path patterns (`.ts`, `.tsx`, `.html`, `.css`, `.scss` plus `localization.uiPathPatterns` when configured)
> 3. For multilingual UI changes, verify translation resource diffs exist (`localization.translationFilePatterns` when configured)
> 4. If translation updates are missing → **MANDATORY**: use ask user tool: "UI text changed in a multilingual project, but translation updates were not detected. Run translation sync now or proceed with explicit risk acceptance?" Options: "Run translation sync first" (Recommended) | "Proceed with explicit risk acceptance"
> 5. Severity: **HIGH** — no silent pass for multilingual UI text changes without explicit translation-sync decision
>
> **Do NOT silently skip. Multilingual UI text changes require explicit translation-sync confirmation.**

<!-- /SYNC:translation-sync-check -->

<!-- SYNC:category-review-thinking -->

> **Category Review Thinking** — A thinking framework for reviewing any category of changed files. NOT a fixed checklist — derive concerns from domain knowledge; the examples are starting points only. Your knowledge of the category exceeds any list here — trust it.
>
> **Step 1 — Understand the category's role.** What is this category responsible for in the overall system? What invariants must it uphold? What are its consumer contracts (who depends on it, what do they expect)?
>
> **Step 2 — Read project conventions for this category.** Search for reference docs, style guides, ADRs, or READMEs specific to this area. Grep 3+ existing similar files — extract naming conventions, structural patterns, shared base classes. If no docs exist, derive conventions empirically from existing code.
>
> **Step 3 — Derive concerns from first principles.** Apply all that are relevant; expand beyond this list based on the actual category:
>
> - **Correctness:** Does the logic match the intent? Trace happy path AND error path.
> - **Boundary contracts:** Are interfaces/APIs/events/protocols honored? No implicit coupling introduced?
> - **Project conventions:** Does new code follow the patterns found in Step 2? Evidence-confirmed, not assumed.
> - **Security:** Auth enforced at every entry point? Input validated at boundaries? No secrets in the diff?
> - **Performance:** Unbounded operations? N+1 patterns? Blocking calls in async context? Unindexed queries?
> - **Maintainability:** DRY? Single responsibility? Complexity within reason? Names reveal intent?
> - **Boundary naming:** When the category exposes public or cross-layer types, APIs, events, or modules, verify that names describe the capability, domain purpose, or contract rather than the current provider/framework/transport; concrete adapters may carry those details. Check callers and implementations before flagging a name, and treat generic names (`Manager`, `Helper`, `Utils`, `Data`) as signals rather than automatic violations.
> - **Test coverage:** Are the changed paths covered by tests? Are existing tests still valid after the change?
> - **Documentation:** Do related docs, specs, or READMEs reflect the changes?
>
> **Step 4 — Create sub-tasks and execute.** For each identified concern: create a task tracking sub-task, work through it with `file:line` evidence, mark done. No findings without proof.
>
> **Illustrative concern examples by category type** (not exhaustive — trust your knowledge beyond this):
>
> - _Server-side logic:_ handler/service structure conventions, validation layer placement, side-effect isolation, cross-service boundary enforcement, data-access layer separation, error propagation strategy
> - _Client-side logic:_ component lifecycle management, resource cleanup (subscriptions, listeners, timers), state management patterns, API integration layer separation, reactive stream composition
> - _Data/Schema:_ migration reversibility (rollback script), lock impact on table volume, backfill idempotency, index coverage for query patterns, deployment ordering
> - _Configuration:_ present in ALL environments? No secrets in diff? App fails fast if config missing (not silently null)? Documented in setup guide?
> - _Infrastructure:_ dev/prod parity? No hardcoded dev values (localhost, debug flags)? Pinned image/dependency versions? CI/CD secret requirements documented?
> - _Styles/Assets:_ follows project naming conventions? Uses design variables/tokens (no hardcoded magic values)? Correct scope (no global side effects from component styles)?
> - _Documentation:_ accurate? Links valid? Examples still match current code/behavior? Covers new scenarios?
> - _Tests:_ assertions verify specific outcomes (not just "no exception")? Idempotent (repeatable N times)? Covers edge cases, not just happy path?
> - _Security artifacts:_ all code paths reach the gate? Negative tests exist (unauthorized denied)? Both enforcement AND display control updated?
> - _Build/Tooling:_ rule changes apply consistently? No exceptions that silently swallow violations? Impact on CI runtime documented?

<!-- /SYNC:category-review-thinking -->

<!-- SYNC:graph-assisted-investigation -->

> **Graph-Assisted Investigation (optional advice)** — Optional: for high-risk blast radius (shared contract, many callers, cross-module/cross-service flow, public API), `.code-graph/graph.db` may add callers, dependents and impacted tests beyond grep/read. Treat it as a hint, NOT proof: stale or incomplete graphs lag uncommitted edits and unindexed paths. verify anything that matters by reading files/grep. Skip it for low-risk or local changes.
>
> An absent or stale graph is never a finding and never blocks, fails or gates work.
>
> **Pattern:** grep/read → optional graph suggestions → grep/read verification.
>
> | Situation                          | Optional graph query                         |
> | ---------------------------------- | -------------------------------------------- |
> | High-risk investigation            | `trace --direction both` on 2-3 entry files  |
> | Fix/debug with wide reach          | `callers_of` on buggy function + `tests_for` |
> | Feature touching a shared contract | `connections` on files to be modified        |
> | Review of a high-risk change       | `tests_for` on changed functions             |
> | Blast radius                       | `trace --direction downstream`               |
>
> **CLI:** `python .claude/scripts/code_graph {command} --json`. Start `--node-mode file` (10-30x less noise), then `--node-mode function` for detail.

<!-- /SYNC:graph-assisted-investigation -->


<!-- SYNC:task-tracking-external-report -->

> **Task Tracking & External Report Persistence** — Bootstrap this before execution; then run project-reference doc prefetch before target/source work.
>
> 1. Create a small task breakdown before target file reads, grep, edits, or analysis. On context loss, inspect the current task list first.
> 2. Mark one task `in_progress` before work and `completed` immediately after evidence; never batch transitions.
> 3. For plan/review work, create `tmp/reports/{skill}-{YYMMDD}-{HHmm}-{slug}.md` before first finding.
> 4. Append findings after each file/section/decision and synthesize from the report file at the end.
> 5. Final output cites `Full report: tmp/reports/{filename}`.
>
> **Blocked until:** task breakdown exists, report path declared for plan/review work, first finding persisted before the next finding.

<!-- /SYNC:task-tracking-external-report -->

<!-- SYNC:source-test-drift-check -->

> **Source/test drift check.** For coding, fix, debug, investigation, test, or review work: when source behavior changes, inspect affected unit/integration/E2E tests and decide from evidence whether tests should change to match intended behavior or the source change is an unintended bug to fix. Do not write tests for migration code; schema/data migrations are one-time execution paths, not core application logic.

<!-- /SYNC:source-test-drift-check -->

<!-- SYNC:spec-drift-adjudication -->

> **Spec drift adjudication (code-wrong vs spec-stale).** Whenever behavior diverges from a canonical owner artifact under the configured business root (`specRoots.business.path`, default `docs/specs`), you MUST NOT silently pick a side. Resolve and validate `specArtifacts` from `docs/project-config.json`: when valid, use its `intent/contracts/evidence` section roles and native case carriers; only when absent, use the strict-default Feature Spec sections (§3 AC, §4 BR, §5 invariant, §8 TC). A malformed or unsupported declaration blocks; never fall back. Adjudicate per `shared/sdd-artifact-contract.md` → **Drift Gates**:
>
> 1. **Detect** — compare the change against the owner's documented intent/contracts and linked evidence. No divergence → record `Spec in sync` and move on.
> 2. **Classify** the divergence:
>    - **CODE-WRONG** — the owner artifact correctly states intended behavior and the change violates it → BLOCKING finding; fix the code/test against intended behavior, creating or updating a regression case in the configured native carrier (strict-default TC when no profile exists).
>    - **SPEC-STALE** — the change is the new intended behavior and the owner now documents the old/wrong behavior → update the canonical owner FIRST through the configured spec workflow, then synchronize its evidence/test carriers. Without a profile, use `$spec [mode=update]`, `$spec [mode=tests]`, then `$spec [mode=sync]`.
>    - **AMBIGUOUS** — intended behavior is unclear → ask the user or canonical spec owner before editing either side.
>    - **SPEC-SILENT** — code correctly enforces an invariant/behavior absent from the owner artifact → not drift but an UNWRITTEN rule. Prove it is always-true (≥2 enforcement points or a rejecting guard), express it as a universally-quantified property, add it to the configured `intent` or `contracts` section, and link it from `evidence` to a native case with an inspected assertion. Without a profile, use the invariant-harvest workflow to add the rule to strict-default §4 (or §3/§5) and a guarding §8 TC. A discovered invariant left only in code or tests is INCOMPLETE.
> 3. **Never normalize drift just because code/tests are green** — green can encode the drift itself. Reconcile to canonical intent, never to whichever side currently passes.
>
> A behavior-changing review/implementation that leaves a spec divergence unadjudicated is INCOMPLETE; an unwritten-but-enforced invariant left uncaptured in the configured owner and case evidence (strict-default §4/§8) is equally INCOMPLETE.

<!-- /SYNC:spec-drift-adjudication -->

<!-- SYNC:severity-rubric -->

> **Severity Rubric** — Classify every finding by consequence, not by effort, reviewer preference, or how annoying the fix is. One scale applies to every review, skill, agent, workflow, and host so a tier means the same everywhere. Choose the highest credible consequence supported by evidence; do not lower a tier to make a round pass.
>
> **Finding vs observation (required):** An observation becomes a finding only when it names the affected user/system/data/contract, the shipped consequence, the evidence location, and the normalized tier. `INFO`, advice, preference, duplicate wording, or an unsubstantiated concern is not a finding and must not reopen a loop. If the concern might affect a required behavior or gate but evidence is incomplete, emit `NOT VERIFIABLE` with the missing evidence and keep it unresolved; never silently convert uncertainty into LOW.
>
> **Reachable trigger path (required):** a finding also names HOW a supported configuration reaches the defect — the caller, input, state or event sequence that drives execution or data there. A concern on a path nothing reaches (dead code, a branch its guard excludes, an impossible state) is an observation: record it as advice, never as a LOW to fix. Also never a finding: what a compiler, type checker, linter or test run for this change already reports in the review evidence; a behavior change the stated intent asks for; an issue silenced by a suppression that predates this change and states its reason (a suppression the change adds is itself reviewed); a pre-existing issue on a line the change neither touched nor made reachable. When reachability cannot be settled and the concern would be MEDIUM or higher, emit `NOT VERIFIABLE` naming what would settle it; a polish-level concern with unsettled reachability is an observation. — why: a speculative LOW admitted as a finding becomes build work in round 1.
>
> | Severity | Action | Definition and examples |
> | --- | --- | --- |
> | CRITICAL | Block immediately; escalate | Immediate material risk if shipped: authentication/authorization or safety bypass; secrets/PII exposure; irreversible destructive action; data loss/corruption; a silent failure on a critical path. A failed binary gate is carried by the executable policy as a separate synthetic blocker, not an ordinary severity judgment. |
> | HIGH | Must fix before PASS/merge | Material correctness or contract risk: wrong behavior on a supported path; violated business/data invariant; meaningful privacy or authority gap; breaking API/schema/compatibility change; likely harm to users/downstream systems; a missing proof for a behavior-changing fix. |
> | MEDIUM | Must clear the current round; escalate if the fix needs an owner decision | Bounded but consequential risk: an edge case, resilience/observability/testability/maintainability gap, credible future defect, or local architectural drift — real impact, not immediate material loss. A recorded follow-up does not make an open MEDIUM a clean pass. |
> | LOW | Record and defer; never opens another fix/re-review round from round 2 onward, never raises the round budget | Non-blocking polish with no credible present correctness, security, privacy, authority, availability, or data-integrity impact: wording/formatting, minor documentation or convention drift, optional defensive cleanup, cosmetic refinement. |
>
> **Consequence decision tree (apply in order):** (1) A failed binary gate stays a separate hard blocker (synthetic CRITICAL in the executable helper) — never hide it behind an ordinary label. Otherwise, would shipping permit immediate material security/safety/authority harm, irreversible destruction, data loss/corruption, or a critical-path silent failure? → **CRITICAL**. (2) Does a supported path, invariant, public contract, privacy/authority boundary, compatibility promise, or behavior-changing proof fail with material impact? → **HIGH**. (3) A bounded but consequential edge, resilience, observability, testability, maintainability, or architectural gap with credible impact? → **MEDIUM**. (4) Evidence shows only non-blocking polish? → **LOW**. (5) Evidence to choose among 1–4 missing → **NOT VERIFIABLE**, not LOW. When several tiers fit, select the highest credible consequence; effort, cost, reviewer discomfort, frequency alone, proximity to the round cap, and obtaining another round never decide the tier.
>
> **Boundary examples:** auth bypass, exposed secret/PII, destructive command without an authority gate, or failed required test/generation/parity gate → **CRITICAL**; wrong supported response, broken invariant/API/schema, meaningful privacy/authority defect, or unproven behavior-changing fix → **HIGH**; bounded retry/timeout/alert/testability gap or credible maintainability drift → **MEDIUM**; typo, formatting, optional cleanup, or cosmetic suggestion proven not to affect behavior → **LOW**. A missing fact about any boundary is **NOT VERIFIABLE** until evidence or a documented residual-risk decision exists.
>
> **Classification procedure (every finding):** (1) state the affected user, system, data, contract, or gate; (2) assess consequence if it ships; (3) assess exposure/likelihood and reversibility/detectability; (4) select the highest justified tier; (5) cite `file:line` or equivalent evidence and a confidence percentage. `NOT VERIFIABLE` is a pending evidence state, not a fifth tier and never a LOW escape hatch: if the claim could affect required behavior, security, privacy, authority, availability, data integrity, or a binary gate, it stays an open evidence blocker until resolved or explicitly owner-accepted with documented residual risk. Classify LOW only when evidence supports the absence of credible present material impact.
>
> **Hard-gate rule:** Binary gates (tests, required artifacts, security must-fix checks, generated parity, policy compliance) are not severity-rated findings. The executable helper records a failed gate as a synthetic CRITICAL blocker so one predicate can carry it; the report still names the gate and failure evidence. A failed gate blocks at every round, even when all ordinary findings are LOW. A failed non-test gate is bounded by the three-round review cap; a failing test gate is outside the round budget and loops until the tests pass.
>
> **Score-based skills** map their numeric scale onto these tiers — no parallel vocabulary:
>
> - **0-2 criterion scoring** (e.g. production-readiness-review): `0` = CRITICAL/HIGH (unmet, blocks readiness), `1` = MEDIUM (partial, consequential gap), `2` = pass. A polish-only criterion is LOW, not a forced `0`.
> - **Two-axis scoring** (e.g. performance-review, impact × likelihood): high impact + high exposure → CRITICAL/HIGH; material impact, bounded exposure → HIGH/MEDIUM; low impact and exposure → LOW. Record the axes and why the tier is the highest credible consequence.
> - **Scorecards / `/20` grades** (e.g. `architecture --mode=scalability`): the aggregate score and verdict band are separate from finding severity. A sub-80 area is evidence to investigate, not an automatic tier; classify each underlying gap by the decision tree and keep advisory score deductions apart from blocking findings.
>
> **Domain-vocabulary normalization (mandatory):** a skill may keep a local reporting vocabulary, but it MUST feed this same four-tier round predicate — never a second severity system:
>
> - `BLOCKED`, `HARD FAIL`, or `FAIL` is a blocking local verdict, not an automatic CRITICAL: CRITICAL for an immediate material risk or failed binary gate, otherwise HIGH or MEDIUM with evidence, while the local block holds until the owning gate is satisfied.
> - `WARN` is not permission to ignore: MEDIUM when consequential, LOW only when evidence shows no credible present material impact, HIGH/CRITICAL when the consequence warrants. `PASS`/compliant is not a finding.
> - UI `P0`/`P1`/`P2`/`P3`/`P4` start as CRITICAL/HIGH/MEDIUM/LOW/LOW; override upward only on evidence of a higher shipped consequence. A P0/P1 accessibility or task-completion floor stays a blocking gate even when called a priority.
> - Numeric SRE/readiness or impact/likelihood scores are evidence inputs, not tiers: emit the score, the consequence, and the normalized tier together. `INFO`/advisory observations are not findings unless evidence shows a material consequence.
>
> A tier drives the gate: CRITICAL/HIGH/MEDIUM stay actionable and blocking under the round policy; all review blockers may use up to three rounds, then escalate; LOW may be tracked as a follow-up and, from round 2, never justifies another fix/re-review by itself. An owner decision may explain or schedule an open MEDIUM but never makes it a clean pass; owner acceptance never makes a failed binary gate pass and must record scope, rationale, and residual risk.

<!-- /SYNC:severity-rubric -->


<!-- SYNC:goal-contract-satisfaction-loop -->

> **Goal Contract Satisfaction Loop** — Persist the user goal in an external file, execute against it, and loop review/fix until every saved required criterion passes or a blocker escalates. Bounded closed loop — NEVER open-ended autonomous exploration.
>
> 1. **Resolve the active goal** (in order): active plan `goal.md` → `<plans root>/goals/{YYMMDD-HHmm}-{slug}/goal.md` (plans root default `plans`; a `docsRoots.plans.path` entry in `docs/project-config.json` overrides the path) → create a new Goal Contract from the current user request (template: `.claude/templates/goal-contract-template.md`).
> 2. **Required sections:** Original Request, Purpose, Success Criteria (checkboxes; mark required vs optional), Constraints, Evidence Required, Iteration Log, Goal Satisfaction matrix.
> 3. **Before work:** read the active goal and map planned work to saved success criteria — execution serves the saved criteria, never chat memory alone.
> 4. **After execution/verification:** append an Iteration Log entry — result, evidence references (`file:line`, command output, report path), remaining gaps.
> 5. **Review gate:** emit a Goal Satisfaction matrix — `| Success Criterion | Evidence | Status |` with PASS/FAIL/BLOCKED. Overall PASS requires every required criterion PASS.
> 6. **Loop rule (retry):** required criterion FAIL → validate the gap is real → fix → re-review only the affected criteria. Stop cleanly when all required criteria PASS.
> 7. **Escalation rule (stop):** two consecutive iterations with no criterion progressing, or a blocker needing user input → mark the criterion BLOCKED with a user-facing reason and escalate. NEVER loop indefinitely.
> 8. **Skip rule:** tiny conversational tasks may skip the goal file ONLY with a recorded one-line reason. User-accepted gate skips are recorded in the goal file with reason and scope.
> 9. **Security:** NEVER store secrets, tokens, credentials, or private customer data in goal files — store evidence references and redact sensitive values.
>
> **Blocked until:** active goal resolved (or skip reason recorded) · saved success criteria read before edits · iteration evidence appended after execution · Goal Satisfaction matrix emitted before any PASS verdict.

<!-- /SYNC:goal-contract-satisfaction-loop -->

<!-- SYNC:trade-off-interrogation-gate -->

> **Trade-Off Interrogation Gate** — ALWAYS ask these THREE questions before ANY verdict, score, finding, or recommendation — about the thing under review AND about every recommendation YOU make. — why: naming a benefit without its price is an endorsement, not a review; the costliest trade-offs are the ones nobody wrote down.
>
> 1. **Is there any trade-off?** Name what it SACRIFICES. "None" / "pure win" is an unfinished analysis, NOT an answer — to claim none, state which dimensions you checked and why each is unaffected: future change cost · complexity · performance/latency · memory/cost · coupling · reversibility · migration burden · operational load · blast radius · security posture · testability · team skill/ramp · delivery time · UX.
> 2. **Is it worth it?** Weigh gain against sacrifice EXPLICITLY — what is gained (with a metric) · what it costs · WHO pays · WHEN it comes due — then emit **WORTH IT / NOT WORTH IT / UNCLEAR**. "Better" with no metric and no cost FAILS this question. NOT WORTH IT → withdraw or replace the recommendation, never keep it as-is.
> 3. **Is the trade-off material enough to CONFIRM WITH THE USER?** A material trade-off is the user's call, never yours. **MATERIAL** when ANY holds: irreversible / one-way door (data migration, public contract, storage format, vendor lock-in) · cost shifted onto someone else (another team, ops/on-call, future maintainer, end user) · one quality attribute traded for another (correctness↔speed, security↔convenience, latency↔cost, simplicity↔flexibility) · a boundary crossed (client↔server tier, service contract, event contract, shared library) · a high-consequence path (auth, money, data integrity, breaking change, High/Medium residual risk) · the worth-it verdict is UNCLEAR.
>
> **MATERIAL → STOP and confirm using ask user tool BEFORE the verdict stands** — state the trade-off, both options, what each sacrifices, and your recommendation. **NOT material →** record it inline with a one-line justification and proceed.
>
> **Non-asking execution contexts — ESCALATE BY HANDOFF, never by silence.** ask user tool reaches only the main interactive agent: a sub-agent cannot ask the user, and a terminal/verdict-only mode asks nothing by design. When you are running in such a context, the obligation is **redirected, never waived** — do ALL of: (a) complete questions 1 and 2 normally; (b) decide materiality and record it in the Trade-Off Assessment row with `confirmed? = NO — cannot ask from this context`; (c) **name the unconfirmed MATERIAL trade-off explicitly in your returned summary/verdict so the CALLER (or parent orchestrator) escalates it using ask user tool on your behalf** — a material trade-off mentioned only inside a report file on disk is NOT a handoff; (d) do not emit an unqualified PASS — mark the verdict as carrying an unconfirmed material trade-off, so the caller's gate stays closed until the user answers. The caller inherits the escalation duty the moment it reads your return.
>
> This carve-out is about **reachability, not convenience**: it applies ONLY where the tool genuinely cannot reach the user (spawned sub-agent, terminal validate/verdict-only mode, non-interactive/headless run). It is NEVER a licence to skip the question, to self-approve a one-way door, or to downgrade materiality because asking is inconvenient — if you CAN ask, you MUST ask.
>
> **Emit a Trade-Off Assessment row** per reviewed decision and per recommendation: `| decision | sacrifices | gain (metric) | who pays, when | WORTH IT/NOT/UNCLEAR | material? | confirmed? |`.
>
> **BLOCKED until:** trade-off named (or dimensions-checked justification given) · worth-it verdict emitted · materiality decided · every MATERIAL trade-off either confirmed with the user OR — in a non-asking context — handed off in the returned verdict for the caller to confirm. A MATERIAL trade-off that is neither confirmed nor handed off can NEVER be PASS, and NEVER gets buried as a Low-severity note.
>
> **NEVER** answer "no trade-off" without checking · decide a material trade-off silently on the user's behalf · let convergence/delivery pressure authorize walking through a one-way door · bundle several material trade-offs into one vague "proceed?".

<!-- /SYNC:trade-off-interrogation-gate -->

<!-- SYNC:domain-entity-change-gate -->

> **Domain Entity Change Gate** — ONE DDD-specific protocol binding every skill or agent that PLANS, IMPLEMENTS, or REVIEWS a change to a domain entity, value object, or aggregate in a model that uses DDD tactical patterns or an evidenced equivalent. First inspect the project's domain model and accepted architecture. If neither uses that model, record `DDD-specific gate N/A — project model: <evidence>`; still apply the project's normal ownership, invariant, assertion-backed test, and evidence rules. `$domain-analysis --mode=review` is the canonical owner of the full A–P checklist; this gate is the shared trigger plus the decisions that must be answered when applicable. NEVER re-derive a weaker local copy — why: when planning and review disagree on entity rules, the plan ships a design that review then rejects, and the rework is paid twice.
>
> **Trigger — after DDD applicability is established, fires when ANY holds:** a new entity / value object / aggregate root is introduced · an existing one gains or loses a field, invariant, relationship, or state transition · an aggregate boundary, repository, or cross-aggregate reference changes · a domain event is added, renamed, or re-payloaded · a concurrency or reconstitution concern on a root changes. State `No domain-entity surface — gate N/A` when none holds.
>
> **Step 1 — Detect BEFORE deciding.** Both answers change which rules even apply:
>
> - **Paradigm** (per aggregate, from the code — NEVER assumed): OO-mutable · type-driven/immutable · event-sourced. Setter, mutability, and reconstitution rules are written for OO-mutable; applying them to the other two manufactures false findings and false plan tasks.
> - **Subdomain fit:** core (rich model owed) · supporting (Active Record or light model) · generic (buy, do not model) · CRUD (Transaction Script — a rich entity here is ceremony). NEVER plan or flag a rich model where the subdomain has no invariant beyond required-field.
>
> **Step 2 — Answer all 6 decision points.** Each is a decision the change MUST make explicitly:
>
> | # | Decision point | Answered when |
> | - | -------------- | ------------- |
> | 1 | **Classification** — entity vs value object vs aggregate root | The swap test is applied ("would an identical copy be interchangeable?"); a VO is immutable with structural equality and has no repository |
> | 2 | **Invariant ownership** — entity owns "can this state exist?", the boundary owns "is this input acceptable?" | Each rule is placed on one side and named; failure signalling (throw vs `Result`) matches the project convention consistently; a DB constraint is a backstop, NEVER the rule |
> | 3 | **Aggregate boundary + concurrency** | Only true always-consistent invariants share an aggregate; cross-aggregate references are by ID; one aggregate mutates per transaction; the ROOT carries the concurrency token; set-based invariants (uniqueness across instances) name a real enforcing mechanism, never an in-memory check |
> | 4 | **Construction vs reconstitution** | Creation and load are separate paths; the load path raises NO domain events and re-runs NO creation rules; required data sits in the constructor/factory |
> | 5 | **Events** | Raised inside the aggregate; dispatched AFTER commit (outbox when crossing a process); internal domain events kept distinct from published integration contracts; handlers idempotent |
> | 6 | **Test obligation** | Every applicable invariant is named and protected by an executing assertion in the project's native test format, with property and boundary-countercase coverage where applicable; GWT is optional. A valid `specArtifacts` profile supplies case identity/carriers; use property TCs only when the profile is absent. A malformed declared profile blocks; a happy-path example alone is NOT coverage |
>
> **Step 3 — Apply by context.** Same decisions, different obligation:
>
> | Calling context | Obligation |
> | --------------- | ---------- |
> | **Planning** (`$plan`) | The plan MUST name the decision and the owning file for every triggered row. An unanswered row is a plan that is not executable — surface it, do NOT let implementation discover it. |
> | **Plan review** (`$plan --mode=review`) | An unanswered, hand-waved, or deferred-to-implementation row is a FINDING with `file:line` into the plan. Presence of the word "entity" is NEVER an answer. |
> | **Implementation** (`$plan --mode=execute`, `$fix`, and any implementing agent — e.g. `backend-developer`) | The decisions are INPUTS, not questions to reopen: implement each triggered row as the plan/spec decided it, at the owning file it named. A row that arrives UNANSWERED is a blocker — surface it and get it decided; NEVER settle it silently at the keyboard, and NEVER pick an aggregate boundary from a DB table or UI screen because the plan left it open. Paradigm and subdomain fit still gate which rules apply. |
> | **Change review** (`$changes-review`) | Route to the owner — **Mode A (default):** read `$domain-analysis --mode=review`'s Phase 2 A–P checklist and apply it as review lenses. **Mode B (escalation):** delegate to `$domain-analysis --mode=review` when standalone AND the diff carries 3+ entity files. Findings enter the normal finding set with `file:line` + severity. |
>
> **Duplication guard — SKIP the gate entirely when ANY row holds.** Record the deferral line, then proceed:
>
> | Suppressing context | Deferral line |
> | ------------------- | ------------- |
> | The running skill IS `$domain-analysis --mode=review` | `Gate is this skill's own body — A–P checklist owns it.` |
> | Invoked inside `$workflow-review-changes` (its step 4 runs `$domain-analysis --mode=review` as a dedicated conditional parallel member) | `Gate deferred to workflow step 4 $domain-analysis --mode=review.` |
> | `$why-review` running in `--validate-findings` terminal mode | `Gate N/A — validate-findings is terminal, no sub-skill calls.` |
>
> — why: unguarded, this edge duplicates a review the parent workflow already runs and closes a `changes-review → domain-analysis --mode=review → why-review → changes-review` cycle.
>
> **BLOCKED until:** DDD applicability evaluated with project evidence (or the DDD-specific gate is recorded N/A) · if applicable, trigger evaluated (or `gate N/A` recorded), paradigm + subdomain fit stated, all 6 triggered decision points answered or raised as findings, and guard row checked before any delegation.

<!-- /SYNC:domain-entity-change-gate -->

<!-- SYNC:design-review-checklist -->

> **Front-End Design Review Checklist** — the EXECUTABLE review protocol for any artifact carrying a user-facing front-end surface. Full catalog (`A1`…`Q` plus §R, ~155 checks with failure signals and default severities; worked calibration cases in `.claude/docs/design-review-calibration.md`): **`.claude/docs/design-review-checklist.md`**. This gate carries the protocol and the triage pass; the file carries the checks.
>
> **Applies when — and ONLY when — the change, plan, or artifact carries a user-facing front-end surface.** A back-end-only diff, a doc edit, or a config change is `N/A`: state that once and move on. NEVER run a UI review on a non-UI change to manufacture coverage. When it DOES apply, **MUST ATTENTION READ `.claude/docs/design-review-checklist.md` and work its sections** — a review that cites a check ID without opening the catalog is asserting, not checking.
>
> **`CL-1` Context before checks (§0.1).** Establish platform · primary user & expertise · primary task · success metric · constraints · review scope · available artifacts. Fewer than four known → state the gap at the top of the report and mark affected findings **low confidence** — why: a check judged against an unknown task is a guess wearing an ID.
>
> **`CL-2` Evidence or nothing (§0.2).** Every finding cites a specific location (screen · element · `file:line`). NEVER invent a measurement — contrast, tap-target size, and load time that cannot be measured from the given artifact are `NOT VERIFIABLE`, never a guessed number. Tag every finding `MEASURED` · `OBSERVED` · `HEURISTIC`. Status values: `PASS` · `FAIL` · `PARTIAL` · `N/A` · `NOT VERIFIABLE`.
>
> **`CL-3` Severity, then a cap (§0.3).** `P0` blocks task completion / loses data / excludes a protected group (ship blocker) · `P1` significant friction or a legal accessibility floor (fix before release) · `P2` measurable inefficiency (next iteration) · `P3` polish (backlog) · `P4` note. Translate to other dialects (BLOCKED/WARN, Critical–Low, BLOCKING/ADVISORY) ONLY through the §0.3 severity map. Cap the report at the top 10 by severity unless a full audit was requested. A clean section reports "no issues found" — NEVER pad. Every `P0`/`P1` carries a concrete fix.
>
> **`CL-4` Section sweep, in order — over whole SURFACES, not files (§0.5).** Map changed files to the pages/views/dialogs they render into, reconstruct each surface's composition (component tree + style origins; render when it can run, else `ENVIRONMENT-BLOCKED`), then sweep: §A core usability heuristics · §B cognitive load & surface complexity (B12–B15: surface load, progressive disclosure, one job per view, the project's complexity budget) · §C visual design & hierarchy · §D interaction and relevant product states · §E information architecture & container fit (E9–E11: dialog vs full view vs stepped flow vs side panel vs inline) · **§F web / §G mobile — conditional on platform; §H expert & data-heavy use — conditional on usage, not platform** · §I accessibility: use WCAG 2.2 AA as the web baseline and meet any stricter applicable legal or project requirement; for other platforms, use the documented platform standard. Record the selected standard and its source; severity follows the governing release contract · §J content & UX writing · §K trust, ethics & privacy · **§L AI & agentic patterns — conditional on the product having AI features** · §M cross-cutting consistency · **§R forms & data entry — conditional on input: fill the Field Necessity Matrix first** · §N edge-case probes. Make one focused pass per applicable section and record N/A with evidence for sections the surface does not support. Cluster a defect repeated across surfaces into ONE finding; calibrate against `.claude/docs/design-review-calibration.md`.
>
> **`CL-5` Quick Triage Pass (§P)** when a full sweep is not possible — use these prompts for applicable surfaces: (1) can a new user complete the primary task unaided · (2) is feedback timely against the project/platform expectation · (3) do relevant empty/loading/error states offer a forward path · (4) is the primary action obvious and reachable for supported inputs · (5) do contrast and focus meet the selected accessibility standard (WCAG 2.2 AA baseline for web) · (6) can users operate the surface with its supported input modes · (7) do interactive targets meet the platform's size/spacing guidance · (8) are destructive actions recoverable where appropriate · (9) does the surface work at its smallest supported size and required zoom/reflow · (10) are there deceptive or coercive patterns.
>
> **`CL-6` Report shape (§O).** Context (+ known gaps) → Verdict (Ship / Ship with fixes / Do not ship) → What works (2–4 specific strengths, cited) → Findings grouped `P0`→`P3`, each with Location · Evidence + tag · Impact · Principle (checklist ID) · Fix → Open questions → Coverage table. Any `P0` caps the grade at Fail regardless of score; report a score only ALONGSIDE findings, never instead of them.
>
> **Component architecture pass (§M6–§M9) when source code is in scope.** Verify the ownership model documented or demonstrated by the project, reuse/composition decisions, and whether shared behavior is duplicated without a reason. Do not require tiers, a base abstraction, or a particular test hierarchy unless the project uses one. Report applicable checklist IDs with `file:line` evidence; do not infer source architecture from a screenshot alone.
>
> **Precedence and no-double-counting.** The project's design-system / SCSS / frontend-pattern docs and accepted ADRs OUTRANK this checklist; the brief's stated direction outranks aesthetic judgment. A deliberate, documented convention is NEVER a defect — check intent before flagging, and surface a genuine conflict to the user with both sides, NEVER resolve it silently. This checklist is the review PROCEDURE, not a third set of taste rules: `UI-1.1`–`UI-9.4` ask "does it meet the usability floor?", `DD-1`–`DD-8` ask "is this THIS product's interface?", and these checks ask "did the review actually look, with evidence, and rank it?". Where a check restates a `UI-*` or `DD-*` clause, report the defect ONCE under whichever ID the consuming skill already uses.
>
> **For a PLAN or a PLAN REVIEW.** When the plan contains UI work, bind applicable acceptance criteria to the target platform/surface, relevant user states, and the selected accessibility standard. Each UI phase MUST name, per new or reshaped view: its primary task, its container (E9), its information priority (what is shown now / later / never here), and — for input — the inputs required at creation vs deferred (§R1–R2). A plan review treats a UI phase missing these as a finding against the checklist IDs it leaves unbound. Use WCAG 2.2 AA as the web baseline and meet any stricter applicable legal or project requirement; for other platforms, identify the documented platform standard. Identify conditional sections (§F/§G/§H, §L) that apply. Do not require every catalogued state; record the standard and its source, and keep unsupported checks N/A.

<!-- /SYNC:design-review-checklist -->


<!-- SYNC:whole-diff-correctness:reminder -->

**MUST ATTENTION** Whole-diff correctness lane: read the complete behavior-changing diff once as one change (split only by flow when it cannot fit); hunt defects through real situations — boundaries, time crossing a day or zone, alternate clients, roles and states, retries, concurrency — using blame/history and adjacent comments as recorded intent; keep only confirmed findings (85+: code path traced) with a reachable trigger path, and report an unsettled candidate that would be MEDIUM or higher as `NOT VERIFIABLE` naming what would settle it, never dropped — rarity sets severity, never confidence.

<!-- /SYNC:whole-diff-correctness:reminder -->

<!-- SYNC:domain-entity-change-gate:reminder -->

**MUST ATTENTION** when a changed model uses DDD tactical patterns or an evidenced equivalent, apply the **Domain Entity Change Gate** — `$domain-analysis --mode=review` owns the full A–P checklist; detect paradigm + subdomain fit FIRST, then answer all 6 applicable decisions (classification · invariant ownership + failure signalling · aggregate boundary + concurrency · construction vs reconstitution · events · assertion-backed native test obligation). Use property TCs only under the absent-profile default; a malformed declared `specArtifacts` profile blocks without fallback. When the project does not use this model, record the DDD-specific gate N/A and still protect actual invariants and outcomes through the configured owner. Planning must NAME each applicable decision; plan review treats an unanswered row as a FINDING; change review routes to the owner (Mode A read / Mode B delegate). SKIP under the 3-row duplication guard and record the deferral line. — why: one protocol shared by planner and reviewer is what stops a plan shipping an entity design that review then rejects.

<!-- /SYNC:domain-entity-change-gate:reminder -->

<!-- SYNC:understand-code-first:reminder -->

**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read code/conventions BEFORE any modification or explanation. The code graph is optional advice for high-risk blast radius (a hint that may be stale), never a requirement.

<!-- /SYNC:understand-code-first:reminder -->

<!-- SYNC:evidence-based-reasoning:reminder -->

**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim; never speculate. Confidence >80% to act, <60% = do NOT recommend; "not enough evidence" is valid output.

<!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:design-patterns-quality:reminder -->

**IMPORTANT MUST ATTENTION** select patterns from project evidence and real needs; keep one owner per rule, justify abstractions by change cost, and grep affected scope for dangling references after extraction, move, or rename.

<!-- /SYNC:design-patterns-quality:reminder -->

<!-- SYNC:complexity-prevention:reminder -->

**IMPORTANT MUST ATTENTION** assess change amplification, cognitive load, coupling, leaked detail and invariant ownership from project evidence. Extract only when a real owner or consumer lowers change cost; no universal layer order or numeric threshold.

<!-- /SYNC:complexity-prevention:reminder -->

<!-- SYNC:graph-assisted-investigation:reminder -->

**Optional advice:** the code graph (`.code-graph/graph.db`) can hint at a high-risk blast radius grep misses; it can be stale, so verify by reading files. Never required.

<!-- /SYNC:graph-assisted-investigation:reminder -->

<!-- SYNC:logic-and-intention-review:reminder -->

**IMPORTANT MUST ATTENTION** verify WHAT the code does matches WHY it changed, and every changed file serves the stated purpose. Trace happy + error paths. Flag scope creep.

<!-- /SYNC:logic-and-intention-review:reminder -->

<!-- SYNC:bug-detection:reminder -->

**IMPORTANT MUST ATTENTION** check null safety, boundary conditions, error handling, resource management for every review.

<!-- /SYNC:bug-detection:reminder -->

<!-- SYNC:test-spec-verification:reminder -->

**IMPORTANT MUST ATTENTION** map every changed function/endpoint/code path to a test case. Search for the project's test spec format near changed files. Flag untested paths and coverage gaps; recommend test creation.

<!-- /SYNC:test-spec-verification:reminder -->

<!-- SYNC:integration-test-sync-check:reminder -->

**IMPORTANT MUST ATTENTION** check changed logic files for matching tests. Surface missing tests using ask user tool — mandatory, not advisory.

<!-- /SYNC:integration-test-sync-check:reminder -->

<!-- SYNC:translation-sync-check:reminder -->

**IMPORTANT MUST ATTENTION** for multilingual UI text changes, verify translation updates are present or explicitly accepted by the user as risk (ask user tool when missing) before PASS.

<!-- /SYNC:translation-sync-check:reminder -->

<!-- SYNC:cross-stack-impact-trace:reminder -->

**MUST ATTENTION** FIRST review action — note change context + holistically trace full pipeline of main affected area across client↔server seam (BE→FE forward, FE→BE backward). Verify both tiers still agree on route/DTO/field/type/nullability/auth; any mismatch = BREAKING finding. Skip only for single-tier / docs-only changes (state so).

<!-- /SYNC:cross-stack-impact-trace:reminder -->

<!-- SYNC:cross-service-check:reminder -->

**IMPORTANT MUST ATTENTION** microservices/event-driven: scan producers, consumers, sagas, contracts in task scope. Per touchpoint: owner · message · consumers · risk (NONE/ADDITIVE/BREAKING). Missing consumer = silent regression.

<!-- /SYNC:cross-service-check:reminder -->

<!-- SYNC:sequential-thinking-protocol:reminder -->

**MUST ATTENTION** use structured reasoning for complex or ambiguous work, implicitly when visible markers would clutter. Verify hypotheses, revise assumptions, and close with confidence, assumptions, open questions and a concrete next action.

<!-- /SYNC:sequential-thinking-protocol:reminder -->

<!-- SYNC:task-tracking-external-report:reminder -->

- **MANDATORY** Bootstrap task tracking before target work; transition one task at a time.
- **MANDATORY** Persist plan/review findings to `tmp/reports/` incrementally and synthesize from disk.

<!-- /SYNC:task-tracking-external-report:reminder -->

<!-- SYNC:end-to-start-debugger-trace:reminder -->

**IMPORTANT MUST ATTENTION** debugger trace gate: for non-trivial bug/fix/investigation/review work, start at the observed final output and trace backward through reader -> storage/projection -> writer -> consumer/job -> producer/trigger. Enumerate all feeder paths and hypotheses before fixing; select the authoritative invariant owner from project architecture and retain validation at untrusted boundaries. **BLOCKED until** trace, hypothesis matrix, owning fix layer, and forward convergence proof exist.

<!-- /SYNC:end-to-start-debugger-trace:reminder -->


<!-- SYNC:goal-contract-satisfaction-loop:reminder -->

- **MANDATORY** Resolve the active Goal Contract BEFORE work (active plan `goal.md` → `<plans root>/goals/{YYMMDD-HHmm}-{slug}/goal.md`, plans root default `plans` and overridable via a `docsRoots.plans.path` entry in `docs/project-config.json` → create from current request) and read saved success criteria before editing.
- **MANDATORY** Append iteration evidence after execution; emit a Goal Satisfaction matrix (PASS/FAIL/BLOCKED) before reporting PASS; loop on validated FAIL; escalate repeated no-progress or blockers. NEVER store secrets in goal files.

<!-- /SYNC:goal-contract-satisfaction-loop:reminder -->

<!-- SYNC:systematic-review-batching:reminder -->

- **MANDATORY** Large changeset → risk-weighted batches, one parallel sub-agent per batch: high-risk ≤8 files OR ≤2000 diff-lines; low-risk (styling, tests, docs, config text) may pool to ≤20 files OR ≤4000 diff-lines; mechanical churn is verified by pattern, not batched. Never review many files one-by-one.
- **MANDATORY** Each batch agent validates its own findings (`$why-review --validate-findings` in its own session); the reducer deduplicates by root cause FIRST, then re-validates only CRITICAL/HIGH (including in-batch rejections and demotions), reviewer conflicts, unvalidated findings and a MEDIUM sample.
- **MANDATORY** > 6 categories OR > 40 files → add the hierarchical synthesis tier; each concern-synthesizer emits cross-concern interaction candidates and the orchestrator runs the cross-concern pass before concluding.

<!-- /SYNC:systematic-review-batching:reminder -->

<!-- SYNC:severity-rubric:reminder -->

- **MANDATORY** Classify every finding Critical/High/Medium/Low by consequence using the affected asset, shipped impact, exposure, reversibility, evidence location, and confidence; Critical/High/MEDIUM remain actionable under the round bar, while LOW is recorded/deferred from round 2 onward.
- **MANDATORY** A finding names a reachable trigger path (caller, input, state or event that reaches the defect) and a consequence; an unreachable concern is an observation, and unsettled reachability is `NOT VERIFIABLE` only when the concern would be MEDIUM or higher (an observation otherwise) — never a speculative LOW.
- **MANDATORY** Keep binary gates separate from severity: a failed test, security must-fix, required artifact, or parity check blocks at every round and is never relabeled LOW.
- **MANDATORY** Score-based skills (sre 0-2, perf two-axis) map onto the same four tiers — no parallel severity vocabulary.

<!-- /SYNC:severity-rubric:reminder -->

<!-- SYNC:category-review-thinking:reminder -->

- **MANDATORY** Derive review categories from file language + directory semantics + change nature; create a sub-task per category.
- **MANDATORY** Derive each category's concerns from first principles with `file:line` evidence — never a fixed checklist.

<!-- /SYNC:category-review-thinking:reminder -->


<!-- SYNC:trade-off-interrogation-gate:reminder -->

- **MANDATORY MUST ATTENTION ALWAYS ASK THE 3 TRADE-OFF QUESTIONS** — on the thing under review AND on every recommendation you make: (1) **what does it SACRIFICE?** name the dimensions checked (change cost · complexity · perf · coupling · reversibility · migration · ops load · blast radius · security · testability · delivery time · UX) — "none"/"pure win" is an unfinished analysis; (2) **is it worth it?** gain (with a metric) vs cost, WHO pays, WHEN → emit **WORTH IT / NOT WORTH IT / UNCLEAR**; NOT WORTH IT → withdraw or replace it; (3) **is it MATERIAL enough to confirm with the user?** irreversible/one-way door · cost shifted onto another team/ops/maintainer/user · one quality attribute traded for another · a tier/service/event/library boundary crossed · auth/money/data-integrity/breaking-change/High-or-Medium-risk path · verdict UNCLEAR → **STOP and confirm using ask user tool BEFORE the verdict**.
- **MANDATORY** A MATERIAL trade-off with no user confirmation can NEVER be PASS; never bury one as a Low-severity note, never decide it silently, and never let delivery or convergence pressure authorize a one-way door — an un-walked-back one-way door is the user's call, not the reviewer's.
- **MANDATORY — a context that cannot ask escalates BY HANDOFF, never by silence.** ask user tool reaches only the main interactive agent, so a sub-agent or a terminal/verdict-only mode cannot ask. There the duty is REDIRECTED, not waived: still name the trade-off, still decide materiality, record `confirmed? = NO — cannot ask from this context`, and **state the unconfirmed MATERIAL trade-off in your RETURNED verdict so the CALLER escalates it** (a note only in an on-disk report is not a handoff); never emit an unqualified PASS. If you CAN ask, you MUST ask.

<!-- /SYNC:trade-off-interrogation-gate:reminder -->


<!-- SYNC:design-review-checklist:reminder -->

- **MUST ATTENTION** when the change/plan/artifact has an applicable user-facing UI surface, READ `.claude/docs/design-review-checklist.md` and run it: `CL-1` establish context first (platform · user · task · metric · constraints · scope · artifacts — state missing context and its confidence impact) · `CL-2` evidence or nothing, cite a location per finding, NEVER invent a measurement (unmeasurable → `NOT VERIFIABLE`), tag `MEASURED`/`OBSERVED`/`HEURISTIC` · `CL-3` rank `P0`–`P4`, cap at top 10 by severity, NEVER pad, concrete fix on every `P0`/`P1` · `CL-4` sweep §A–§N plus §R over whole surfaces (changed files → affected views, composition reconstructed, render or `ENVIRONMENT-BLOCKED`), including surface load B12–B15, container fit E9–E11, §H by usage, Field Necessity Matrix for input, applying only relevant platform/product sections and the WCAG 2.2 AA web baseline plus any stricter applicable legal/project requirement, or the documented standard for other platforms · `CL-5` short on time → use the §P prompts · `CL-6` report in the §O shape · for source code, assess component ownership, base abstractions, reuse, and duplication using the project's documented taxonomy or observed boundaries. Project design-system docs and ADRs OUTRANK the checklist; report a defect ONCE across `UI-*`/`DD-*`/`CL-*`. For a plan, bind only applicable sections and states to acceptance criteria, and name each UI view's primary task, container, information priority, and creation-vs-deferred inputs; a plan review flags a UI phase that omits them. Skip when the work has no user-facing UI surface, and state why.

<!-- /SYNC:design-review-checklist:reminder -->

<!-- SYNC:review-principle-awareness -->

> **Review Applicability / Current-Principles Awareness** — Every review must first classify the change context (greenfield foundation, brownfield feature/refactor, test/docs/config/UI/infra, or actor-facing/machine surface) and take notice of the applicable current principles below. This is an evidence-gated applicability check, not a mandate to flag or build every item.
>
> **Detailed protocol routing — read/apply only when warranted:**
> - `SYNC:scale-ready-foundation` — greenfield foundation is blocking; big-feature brownfield fit/adapt/defer; architecture review is advisory when auditing. Detailed carriers: `workflow-greenfield-init`, `workflow-big-feature`.
> - `SYNC:test-architecture-execution-contract` — assertion-bearing tests use the project's configured/native format, name the guarded intent/technical contract, and assert an owned outcome; GWT is one valid format. Detailed carriers: `integration-test`, `workflow-greenfield-init`, and the test-architecture review path.
> - `SYNC:ai-agent-as-user-access` — when an AI/machine actor or future contract is evidenced, inspect identity/delegation, capability boundaries, selected API/CLI/MCP/WebMCP/event/SDK surface, safety/consent, audit/observability, and native-format contract tests. Detailed carriers: `workflow-greenfield-init`, `workflow-big-feature`, `architecture --mode=review`.
> - `SYNC:design-system-check` — when UI changes, inspect the design-system and component-contract obligations; route visual/UX depth to the owning UI review.
>
> **Review behavior:** Check only principles applicable to the reviewed scope; record `APPLY-NOW`, `ADAPT-IN-SLICE`, `DEFER-AS-OPPORTUNITY`, `NOT-APPLICABLE`, `BLOCKED`, or `UNVERIFIED` with `file:line`/config/CI evidence, status/severity, owner/route, and next step/revisit trigger. Do not invent findings from a generic checklist, flag unrelated pre-existing gaps as regressions, silently expand the requested scope, or mutate a parent gate merely because advice exists.
>
> **Ownership:** `changes-review` coordinates the applicability pass and routes depth to the owning specialist (`architecture --mode=review`, `integration-test --mode=review`, `security-audit`, `performance-review`, `ui-design --mode=review`, `production-readiness-review`, or another matching review). A specialist reports its own lens and does not duplicate or override another review's verdict; existing brownfield gaps stay advisory unless new, safety-relevant, or explicitly in scope.
>
> **Required review note:** `context/scope | principle/protocol checked | evidence | status/verdict | severity | owner/route | next step/revisit trigger`.
>
> **BLOCKED when:** an applicable principle is required for safety/correctness but missing, unowned, or untestable. Otherwise record an evidence-backed `NOT-APPLICABLE`, advisory, `DEFER-AS-OPPORTUNITY`, or `UNVERIFIED` result according to the lifecycle and change context; creating a greenfield foundation remains subject to its own blocking protocol.

<!-- /SYNC:review-principle-awareness -->

<!-- SYNC:review-principle-awareness:reminder -->

**IMPORTANT MUST ATTENTION** Every review first checks the change context and routes only applicable principles to their detailed protocols: scale-ready foundation, test intent in the project's native format (GWT is one option), AI-agent-as-user access, and UI/component design when relevant. Record evidence-backed apply/adapt/defer/N/A/block/unverified status with owner and next step; do not invent unrelated findings or expand scope.

<!-- /SYNC:review-principle-awareness:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** review any change — one line or thousands of files — with depth where the risk is: triage first, evidence for every finding, validate before fixing, SELF-FIX the validated blocking findings (standalone), re-review the whole updated diff, and finish with `$docs-manager --mode=update` (round 1: zero open findings; round 2: zero CRITICAL/HIGH/MEDIUM, LOWs deferred).

**IMPORTANT MUST ATTENTION** Phase 0 triage (size band · change kinds · risk · blast radius) and the Review Plan with its coverage ledger come BEFORE any review work; every changed file is owned by a dimension or batch, and every ruled-out dimension carries its evidence.
**IMPORTANT MUST ATTENTION** you choose the orchestration — XS/S inline, M one parallel wave, L/XL risk-weighted batches (each validating its own findings) plus a synthesis pass — but never sample silently and never skip a required gate.
**IMPORTANT MUST ATTENTION** ANY finding in standalone mode (Critical / High / Medium / OR Low) → invoke the `$why-review` skill via the skill invocation with `--validate-findings <report-path>` BEFORE any fix, docs-manager --mode=update, commit, or handoff — an actual skill call, never inline self-validation; findings a batch reviewer or report-only specialist already validated outside the independent check set (Phase 6) are covered by its call.
**IMPORTANT MUST ATTENTION** after a fix, re-review the WHOLE current diff from Phase 0 with a fresh task list — never only the fixed files; run Phase 7.5 when any fix landed (not for a round-1 LOW-only fix set closed by scoped check with no simplification applied) and Phase 8 `$docs-manager --mode=update` always (standalone).
**IMPORTANT MUST ATTENTION** every behavior-changing file gets a Spec Drift verdict and every behavior-changing finding a Dual-Feedback Ledger row (spec AND test); missing tests and missing translations surface using ask user tool.
**IMPORTANT MUST ATTENTION** specialists run `--report-only`; integrate their findings RAW — never filter, soften or override them.
**IMPORTANT MUST ATTENTION** one task per selected dimension/batch and per required gate; the living report is written first and appended per file/batch — re-read it and the current task list after any compaction.
**IMPORTANT MUST ATTENTION** every claim needs `file:line` proof and a confidence (>80% act, 60–80% verify first, <60% do not recommend); grep 3+ examples before flagging a convention.
**IMPORTANT MUST ATTENTION `--fix-loop` mode (optional, standalone-only; no flag → default unchanged):** (0) resolve the fixed diff scope + Goal Contract and plan the loop tasks → (0b) bind the convergence loop (protocol loop primary + optional `/goal` accelerator) → (1) round loop: report-only review pass INLINE (Phase 0 → Phase 5, fresh task list, stop before Phase 6) → `$why-review --validate-findings` → `$fix` on VALIDATED blocking findings at the owning layer → append Iteration Log → (2) converge when a FRESH full review pass over the post-fix diff clears the current round's bar (round 1: zero open validated findings; round 2: zero validated CRITICAL/HIGH/MEDIUM, LOW deferred) with the working-tree-unchanged backstop / escalate on non-progress → (3) terminal Phase 8 `$docs-manager --mode=update` + recap; never commit or push unless asked. **Mode scope:** this standalone mode pairs ONE review pass with `$fix` on the validated findings; it is DISTINCT from `$workflow-review-changes --fix-loop`, which re-runs the WHOLE default workflow until a round applies zero fixes. The mode's full text is `references/fix-loop.md` — read it FIRST (BLOCKING) whenever the flag is present.
**IMPORTANT MUST ATTENTION** in `--fix-loop`, run the review pass and `$why-review` INLINE — NEVER as a sub-agent, NEVER re-invoke this skill with `--fix-loop` — regenerate a fresh loop task plan every round, apply ONLY validated findings, and keep the diff base fixed (`{scope}` = branch-diff base ∪ current uncommitted changes, recomputed each round).
**IMPORTANT MUST ATTENTION** enforce the **round cap (default 3, hard maximum 3)** in `--fix-loop`; review blockers not shrinking across 2 rounds or increasing, or the budget spent with blocking findings still open → **STOP & escalate** using ask user tool. NEVER loop past round 3 on review blockers, or open-ended — only failing test gates continue, until green; round-2 LOW-only findings converge and are recorded as deferred.
**IMPORTANT MUST ATTENTION** when Phase 0.7 finds executable E2E/browser/user-flow artifacts, read `.claude/skills/shared/e2e-quality-protocol.md` and invoke `$e2e-test --mode=verify` report-only in Phase 3.9; when no trigger exists, record `NOT-APPLICABLE` and do not run an E2E lane — why: optional routing preserves review cost while preventing unverified user-flow changes from hiding inside a generic code review.

**Anti-Rationalization:**

| Evasion | Rebuttal |
| --- | --- |
| "Tiny diff, skip triage" | Triage on an XS diff takes a minute and is what licenses the lean path; a 2-file auth change still escalates to `$security-audit`. |
| "Big diff, run every specialist on everything" | Triage decides — spend specialist depth where the risk is, batch the rest, and verify mechanical churn by pattern. |
| "Too many files, sample a few" | Never sample silently — every changed file is in the coverage ledger, reviewed or classified with evidence. |
| "Finding is obvious, fix now" | Invoke `$why-review --validate-findings` first — unvalidated findings are not fixes. |
| "Only re-check the fixed files" | Fixes interact with earlier changes — re-review the whole current diff. |
| "Tests are green, the spec drift is fine" | Green can encode the drift — adjudicate every divergence. |
| "Clean review, docs surely fine" | Clean code ≠ current docs — Phase 8 `$docs-manager --mode=update` always runs (standalone). |
| "Sub-agent already reviewed it" | Integrate its findings raw; the main agent never overrides them. |

**[TASK-PLANNING]** Break scope into small todo tasks before acting; maintain one `in_progress`; add a final review todo.

<!-- SYNC:core-engineering-principles:reminder -->

**MUST ATTENTION** Core Engineering Principles — every plan, implementation and review must be **Easy to change** (reuse first, one owner per rule, interfaces/adapters at volatile boundaries, no speculative abstraction) · **Easy to scale** (extend by addition, bounded growth, explicit boundaries, sized to the project's real profile) · **Easy to maintain** (intent-named tests that fail when the rule breaks across happy/error/edge paths; harness green locally and in CI). Before done: next change → how many edit sites? 10× → what breaks? which test goes red?

<!-- /SYNC:core-engineering-principles:reminder -->
