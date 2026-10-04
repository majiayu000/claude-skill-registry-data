---
name: harness-setup
version: 1.2.1
description: '[Quality] Use when a workflow step or the user asks for an agent quality harness: feedforward guides and feedback sensors.'
---

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Wire every feedforward guide and feedback sensor into the greenfield project so all later AI coding agents operate with maximum guidance and self-correct against quality gates BEFORE human review — raising first-attempt quality and catching defects at the earliest, cheapest stage.

**Summary:**
- **Purpose:** complete the outer harness—feedforward guidance plus computational and inferential feedback—so later agents self-correct before human review.
- **Testability contract:** resolve Unit/Integration/System/E2E and warranted Performance/Scale applicability from runner/config evidence; record owner/root/data, copy-ready full/focused commands, zero-match behavior, CI/simple Windows/macOS/Linux entry, unique run/data identity, and repeat proof. Block unresolved applicable fields; record evidence-backed `N/A` for non-applicable tiers.
- **Ordered path:** 1 Guards → 2 Phase A Stack Detection → 3 Phase B Feedforward Guides → 4 Phase C Computational Sensors → 5 Phase D Inferential Sensors → 6 Phase E Behaviour Harness → 7 Phase F Inventory Report → 8 Next Steps. Each phase blocks the next; feedforward and sensor choices require `AskUserQuestion`.
- **Quality boundary:** `/linter-setup` supplies computational sensors; this skill never installs them. Require intent-protecting evidence selected by profile, risk, tooling and budget; mutation/property sensors are optional, line coverage diagnostic; append inventory after every phase and keep it living.

**Main steps (run in order — each BLOCKS the next):**

1. **Guards** — verify `/linter-setup` (linter config + pre-commit hook + CI gate); detect existing inventory and enhance it, never skip it.
2. **Phase A — Stack Detection** — read plan / `architecture --mode=design` / tech-stack reports; write `stack-profile.md`; use `AskUserQuestion` for undetectable fields.
3. **Phase B — Feedforward Guides** — author/enhance CLAUDE.md/AGENTS.md (architecture patterns, anti-patterns, naming, boundaries), skill-activation rules, `docs/architecture/*` notes, and pattern catalog; confirm via `AskUserQuestion`.
4. **Phase C — Computational Sensors** — confirm `/linter-setup` outputs and list config paths; invoke it if any are missing.
5. **Phase D — Inferential Sensors** — wire review skills to lifecycle gates (`/why-review` pre-impl · `/code-quality-review` pre-commit · `/domain-analysis --mode=review` post-impl · `/production-readiness-review` + `/security-audit` pre-release · `/scan-codebase-health` recurring · `/integration-test --mode=review` feature-area TC audit BOTH pre-release AND recurring, catching orphaned Section-8 TCs and uncovered behavior); record under `## Review Gates`.
6. **Phase E — Behaviour Harness** — choose spec format, profile-fit test tiers, fixtures and intent-protecting evidence, and `test-strategy.md`; NEVER gate on line `%`.
7. **Phase F — Inventory Report** — append `harness-inventory.md` with all sensors and gaps; present it via `AskUserQuestion`.
8. **Next Steps** — use `AskUserQuestion` to choose `/feature-implement` (recommended), `/why-review`, or skip.

**Produces:**

- Feedforward guides: CLAUDE.md/AGENTS.md conventions, architecture docs, pattern catalogs, skill-activation rules
- Computational feedback sensors: `/linter-setup` linters, formatters, pre-commit hooks, and CI gates
- Inferential feedback sensors: AI review skills wired to lifecycle stages
- Harness inventory: `tmp/harness/harness-inventory.md`

**When invoked:** After `/scaffold` + `/linter-setup` in greenfield workflow; scaffolding must be complete.

**Does NOT do:** Install linters or configure formatters; `/linter-setup` owns that work.

---

## Activation Guards

**Check 1 — `/linter-setup` prerequisite (BLOCK if missing):** Before phases, verify it completed by checking for a root linter config (e.g., `.eslintrc`, `pyproject.toml`, `.editorconfig`), pre-commit hook config (e.g., `.husky/`, `.pre-commit-config.yaml`), and CI quality gate definition. If any is missing → `AskUserQuestion`: "/linter-setup appears incomplete. Computational feedback sensors must be in place before harness setup. Run /linter-setup first, then return here?" **BLOCK** Phases A–E until verification passes.

**Check 2 — Existing harness inventory:** Check `tmp/harness/harness-inventory.md`. If found → `AskUserQuestion`: "Harness inventory already exists — re-run to enhance existing harness, or skip?" Existing `CLAUDE.md`/`AGENTS.md` are feedforward guides to enhance, NEVER skip signals.

---

## Phase A — Stack Detection

Read, in order: `plan.md` frontmatter → `architecture --mode=design` report → tech-stack-comparison report. Extract:

- Primary language(s) and framework(s)
- Test framework and test runner
- CI provider/tooling
- Package manager and monorepo structure (if any)
- Module system and build tooling

Write detection result to `tmp/harness/stack-profile.md`.

If any field is undetectable → `AskUserQuestion` before proceeding.

---

## Phase B — Feedforward Guide Setup (Inferential)

For each guide type, check existence; create it or enhance an existing guide:

1. **CLAUDE.md / AGENTS.md — Architecture conventions:** add "Architecture Patterns" (choices from `/architecture --mode=design`, e.g., Clean Architecture, CQRS, Repository), "Anti-Patterns" (stack-specific), "Naming Conventions" (language-idiomatic), and "Module Boundaries" (allowed imports and dependency direction).
2. **Skill activation rules:** document CLAUDE.md auto-activation for common stack tasks, e.g., domain-entity changes → `/domain-analysis --mode=review`; before commits → `/code-quality-review`.
3. **Architecture notes:** create `docs/architecture/` with `bounded-contexts.md` (boundaries/ownership), `dependency-rules.md` (allowed layer imports), and `naming-conventions.md` (project-specific file/class/function names).
4. **Pattern catalog:** create `docs/architecture/pattern-catalog.md`, document each `/architecture --mode=design` choice with DO/DON'T examples, and anchor examples to actual project files once scaffolding produces them.
5. **Discovery gate (`SYNC:ai-discovery-doc-quality`):** every created or enhanced guide leads with its purpose, when to read it and its critical rules, ends with closing reminders when long, and is routed from the root instruction file or docs index by a `read <path> when <situation>` trigger — a guide nothing routes to is never read. Put generated root-context changes through `/ai-context-refresh`, not a hand-edit of a generated section; run `/prompt-enhance` on each hand-owned guide that changed.

Present created/updated guides via `AskUserQuestion`: "Feedforward guides above will be created/enhanced. Confirm or adjust?"

---

## Phase C — Computational Feedback Sensors

Confirm `/linter-setup` outputs by checking the root linter config (e.g., `.eslintrc`, `pyproject.toml`, `.editorconfig`), pre-commit hook config (e.g., `.husky/`, `.pre-commit-config.yaml`), and CI quality gate. If any is missing, invoke `/linter-setup` before continuing. Output confirmation with file paths.

---

## Phase D — Inferential Feedback Sensors

Configure AI review skills by lifecycle stage. Present via `AskUserQuestion`: "Which inferential sensors should be mandatory vs optional for this repository?"

- **Pre-implementation:** `/why-review` validates design rationale before the implementation approach is committed.
- **Pre-commit:** document in CLAUDE.md that significant changes run `/code-quality-review`.
- **Post-implementation:** `/domain-analysis --mode=review` when domain entity files are in the changeset.
- **Pre-release (mandatory):** `/production-readiness-review` for reliability/operations and `/security-audit` for production security.
- **Recurring drift:** schedule `/scan-codebase-health` quarterly or on CI schedule. Also wire `/integration-test --mode=review`'s Missing Integration Test / Spec-Coverage Gate feature-area TC audit (Phase 3 addendum), which catches orphaned Section-8 TCs and uncovered behavior, both pre-release alongside the two mandatory gates and on the same recurring cadence; a diff-scoped run cannot catch a Section-8 TC whose test regressed outside the current changeset.

Add the agreed sensor configuration to CLAUDE.md under "## Review Gates".

---

## Phase E — Behaviour Harness (Spec + Test Strategy)

Define the project behaviour harness:

- **Functional spec:** `AskUserQuestion`: "Feature documentation format?" Options: feature-spec (8-section tech-free), TDD specs only, lightweight ADRs. Establish the business spec root (default `docs/specs`; a `specRoots.business.path` entry in `docs/project-config.json` overrides the path) or an equivalent spec home.
- **Test tiers:** Select boundaries from the actual architecture and runner. Unit may cover pure rules; integration exercises applicable production boundaries (CQRS or persistence only where present); system/E2E cover warranted user/runtime paths. Record absent tiers as evidence-backed N/A, never impose a real database or CQRS layout on a stack that has neither.
- **Approved fixtures:** pre-seed reference/lookup data as approved snapshots; integration tests accumulate data and NEVER delete/reset it.

### Testability & Execution Matrix (write to `test-strategy.md`)

Copy the `architecture --mode=design` contract into `test-strategy.md`; resolve every tier from verified project/configuration evidence before choosing tools:

| Tier | Applicability + evidence | Owner | Runner/framework + config | Test root | Data/fixture policy | Full command | Focused/partial command | Zero-match behavior | CI gate | Simple Windows/macOS/Linux entry point | Repeat proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Unit | `APPLICABLE` / `N/A — {evidence}` | {owner} | {runner/config} | {root} | {fixtures/factories} | `{command}` | `{filter}` | `{non-zero behavior}` | {gate} | `{command, or .cmd + .sh pair}` | `{result or planned owner}` |
| Integration/System | `APPLICABLE` / `N/A — {evidence}` | {owner} | {runner/config} | {root} | {public-path + additive data} | `{command}` | `{filter}` | `{non-zero behavior}` | {gate} | `{command, or .cmd + .sh pair}` | `{two no-reset runs}` |
| E2E | `APPLICABLE` / `N/A — {evidence}` | {owner} | {configured browser/config} | {root} | {reachable journey data} | `{command}` | `{filter}` | `{non-zero behavior}` | {gate} | `{command, or .cmd + .sh pair}` | `{result or evidence-backed N/A}` |

`APPLICABLE` requires runner/framework/configuration/root/command evidence. If no E2E framework, configuration, and command are verified, record `N/A — {config/source evidence}`; do not infer a browser stack from generic examples. Full/focused commands must be copy-ready, report exact counts/exit status, and fail invalid or zero-match selection.

### Run, Data, Isolation & Repeat Policy (write beside the matrix)

For each applicable persistent-state tier, record run/test identity generation and unique business-data suffix, supported public paths, realistic valid data, count-before-create idempotent/restart-safe reference setup, keyed additive accumulation with integrity checks, mutable-root/parallel-worker isolation, immutable shared data, realistic actor pacing, observable arrange barriers, and exact results. Require two consecutive no-reset full runs; until executed, mark proof `planned — {owner}`, not PASS. Keep property/invariant, mutation, change, and behavior coverage meaningful; line coverage remains diagnostic only.

**Test-strength sensors (NOT a line-coverage gate):**

- **Line coverage is a diagnostic only — NEVER gate a build on it.** Low coverage is a useful NEGATIVE signal (an area is untested → investigate); high coverage is NOT evidence of quality (lines can execute with no meaningful assertion). Report it as a diagnostic; do not fail CI on a coverage %.
- **Test-strength evidence:** Follow the shared Harness Engineering owner and F4. Select assertion-intent review, contract checks, targeted mutation/fault injection, property/metamorphic checks or a focused defect probe according to invariant risk, stack and budget. Record the protected outcome and a concrete break the assertion catches. No mutation tool, property tool or score threshold is universally required. Ask before installing an optional sensor; when selected, document its meaningful maintained threshold and limits.
- **Property checks (optional sensor):** choose them for broad-input invariants when tooling and risk justify them; otherwise record the alternate assertion/contract evidence. Tool absence alone is not a gap.
- **Keep behavior/change-coverage (meaningful, not a %):** every behavior-changing file must have a test that asserts the changed outcome — see `/integration-test --mode=review` Gate 7. This is the right notion of "coverage"; the line-% is not.

Document the agreed strategy in `docs/architecture/test-strategy.md`.

---

## Phase F — Harness Inventory Report

Write `tmp/harness/harness-inventory.md`:

```markdown
# Harness Inventory

Generated: {date}
Stack: {detected stack from Phase A}

## Testability & Verification Contract

Copy the resolved `test-strategy.md` matrix into this inventory and keep the status current:

**Status:** `PASS | PARTIAL | BLOCKED`

| Tier | Applicability + evidence | Owner | Runner/config/root | Full | Focused/partial | Zero-match behavior | CI / simple Windows/macOS/Linux entry point | Identity/data/isolation/fidelity policy | Repeat proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Unit | `APPLICABLE` / `N/A — {evidence}` | {owner} | {runner/config/root} | `{command}` | `{filter}` | `{non-zero behavior}` | {gate / command} | {policy reference} | {result/status} |
| Integration/System | `APPLICABLE` / `N/A — {evidence}` | {owner} | {runner/config/root} | `{command}` | `{filter}` | `{non-zero behavior}` | {gate / command} | {policy reference} | `{two no-reset runs}` |
| E2E | `APPLICABLE` / `N/A — {evidence}` | {owner} | {runner/config/root} | `{command}` | `{filter}` | `{non-zero behavior}` | {gate / command} | {policy reference} | `{result or evidence-backed N/A}` |

Missing/placeholder evidence is an open gap, not a PASS. The inventory must preserve the strategy's unique identity, additive-data, isolation, realistic-fidelity, and two-run proof fields; E2E N/A remains evidence-backed.

## Feedforward Guides

| Type          | File/Skill                           | Purpose                         |
| ------------- | ------------------------------------ | ------------------------------- |
| Inferential   | CLAUDE.md §Architecture Patterns     | Shapes AI architectural choices |
| Inferential   | CLAUDE.md §Anti-Patterns             | Prevents known bad patterns     |
| Inferential   | docs/architecture/pattern-catalog.md | DO/DON'T examples per pattern   |
| Computational | .editorconfig                        | Cross-IDE consistency           |

## Feedback Sensors — Computational

| Stage      | Tool/Hook          | What it catches                                |
| ---------- | ------------------ | ---------------------------------------------- |
| Pre-commit | {linter}           | Style violations, common errors                |
| Pre-commit | {formatter}        | Code formatting drift                          |
| CI         | {type-checker}     | Type errors                                    |
| CI         | {static-analyzer}  | Security, complexity, dead code                |
| CI         | {selected strength sensor, or N/A with alternate evidence} | Protected intent; threshold only if justified |
| CI         | {coverage-tool}    | Untested areas (DIAGNOSTIC only — never gated) |

## Feedback Sensors — Inferential

| Stage               | Skill/Agent             | What it catches                |
| ------------------- | ----------------------- | ------------------------------ |
| Pre-implementation  | /why-review             | Design rationale gaps          |
| Pre-commit          | /code-quality-review            | Convention drift, logic errors |
| Post-implementation | /domain-analysis --mode=review | Domain model quality           |
| Pre-release         | /production-readiness-review             | Operational readiness          |
| Pre-release         | /security-audit               | Security vulnerabilities       |
| Pre-release + Recurring | /integration-test --mode=review (feature-area TC audit) | Orphaned Section-8 TCs, uncovered changed behavior |

## Open Gaps

| Area                     | Reason   | Risk           |
| ------------------------ | -------- | -------------- |
| {area not yet harnessed} | {reason} | {LOW/MED/HIGH} |
```

Present inventory to user for review via `AskUserQuestion`.

---

## Next Steps

`AskUserQuestion`:

- **"/feature-implement (Recommended)"** — Begin implementing the project plan with full harness in place
- **"/why-review"** — Review harness design rationale before proceeding
- **"Skip"** — Proceed manually without workflow guidance

---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `ai-discovery-doc-quality` — Agent-guide content value, authority, retention and verified discovery; writing a doc that an agent reads → .claude/skills/shared/protocols/ai-discovery-doc-quality.md
- `engineering-foundation-gate` — Seven engineering-foundation dimensions judged by project profile; creating or reviewing how a project is built, run, tested or checked → .claude/skills/shared/protocols/engineering-foundation-gate.md
- `harness-setup` — Agent quality harness: feedforward guides and feedback sensors; setting up an agent quality harness → .claude/skills/shared/protocols/harness-setup.md
- `test-architecture-execution-contract` — Testability as an architecture condition: required test types and execution modes; setting up or reviewing a test architecture → .claude/skills/shared/protocols/test-architecture-execution-contract.md

<!-- PROTOCOL-GUIDES:END -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

<!-- SYNC:test-architecture-execution-contract:reminder -->

**MUST ATTENTION** Each assertion-bearing test names the behavior or technical contract it protects and asserts an outcome it owns. Use the project's configured/native test format — Given/When/Then is one valid format, never a framework-wide requirement. When `specArtifacts` is valid, link configured owner/case/variant identity and `intent/contracts` evidence; when absent, name the guarded business intent or technical contract. A malformed declared profile BLOCKS without fallback. Broad test-format migration → assign an owner and next step, never rewrite cases outside scope.

**MUST ATTENTION** Before implementation record evidence-backed applicability for the test types and modes the task/project contract requires: copy-ready full and focused commands where available, zero-match behavior, a useful platform-appropriate entry point, supported execution modes and environments, state-isolation requirements, exact results, and repeat evidence where persistent state makes it relevant. Exercise claimed modes; report a missing required capability as `ENVIRONMENT-BLOCKED`. Never invent production targets or impose a test format. Browser/UI E2E uses the configured runner's waits or project helper for observable readiness and outcomes; apply action pacing only where the project contract specifies it. Reuse the project's evidenced test organization — require a POM, base class, or component taxonomy only when the project actually selects it.

<!-- /SYNC:test-architecture-execution-contract:reminder -->

<!-- SYNC:engineering-foundation-gate:reminder -->

**IMPORTANT MUST ATTENTION** evidence-backed lifecycle/scale/criticality/repo/runtime profile; unknowns take lower tiers. Judge all 7 outcomes: **F1** reproducible build/run/test · **F2** exercise supported/required modes; dual modes only when warranted · **F3** applicable local/CI/production-shaped test portability · **F4** test-strength proof; no universal mutation tool · **F5** measured performance at warranted scale/risk · **F6** build/change scalability at meaningful module boundaries · **F7** stack/profile-fit mechanical checks. Evidence-backed `N/A-by-profile` is valid; prevent over-engineering. Creation blocks warranted omissions; brownfield advises without score changes, with smallest next steps. Catalog: `.claude/docs/engineering-foundation-catalog.md`; update first, re-run `inject_engineering_foundation_gate.py`.

<!-- /SYNC:engineering-foundation-gate:reminder -->

<!-- SYNC:ai-discovery-doc-quality:reminder -->

**MUST ATTENTION** AI-read guides: purpose/read-when and priorities first; retain action-changing rules, exceptions and rationale; verify triggered discovery and parser contracts. Use the content-value and semantic-disposition gate after enhancement; keep evidence in temporary reports and fix generated output at its source.

<!-- /SYNC:ai-discovery-doc-quality:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Wire every feedforward guide and feedback sensor into the greenfield project so all later AI coding agents operate with maximum guidance and self-correct against quality gates BEFORE human review — raising first-attempt quality and catching defects at the earliest, cheapest stage.
**IMPORTANT MUST ATTENTION** Testability contract: resolve evidence-backed Unit/Integration/System/E2E and warranted Performance/Scale rows, copy-ready full/focused commands, zero-match failures, owner/root/data, CI/simple Windows/macOS/Linux entry, supported host/container modes and environment reach, unique run identity, isolation, and repeat proof before claiming setup, review, or test completion.

**IMPORTANT MUST ATTENTION Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Harness Engineering:** feedforward + feedback loops; require profile-fit intent evidence, never line-coverage %, keep quality left.

**IMPORTANT MUST ATTENTION Main steps (in order — each BLOCKS the next):** Guards (verify `/linter-setup`) → A Stack Detection (`stack-profile.md`) → B Feedforward Guides (CLAUDE.md patterns/anti-patterns/naming/boundaries + skill-activation rules + pattern catalog) → C Computational Sensors (confirm linter/hook/CI) → D Inferential Sensors (wire `/why-review`, `/code-quality-review`, `/domain-analysis --mode=review`, `/production-readiness-review`, `/security-audit`, `/scan-codebase-health`, `/integration-test --mode=review` missing-test/spec-coverage gate to gates) → E Behaviour Harness (spec format + profile-fit test tiers + intent evidence + `test-strategy.md`) → F Inventory Report (`harness-inventory.md`) → Next Steps. NEVER skip or reorder — why: each phase consumes the prior phase's verified output.

**IMPORTANT MUST ATTENTION** BLOCK on the `/linter-setup` prerequisite first — ALWAYS verify computational sensors (linter config, pre-commit hook, CI gate) exist before any phase runs — why: keep quality left; cheapest gates must precede inferential ones, and this skill never installs them itself
**IMPORTANT MUST ATTENTION** NEVER auto-decide feedforward-guide or sensor content — present the draft and confirm via `AskUserQuestion` — why: harness conventions bind every future agent; silent choices propagate to all later sessions
**IMPORTANT MUST ATTENTION** write `tmp/harness/harness-inventory.md` incrementally (append after each phase) — NEVER hold findings in memory — why: long context drifts and silently drops findings
**IMPORTANT MUST ATTENTION** walk phases A→F as a hard barrier sequence — NEVER skip or reorder; each phase BLOCKS the next until its guard passes — why: a later phase consumes the prior phase's verified output
**IMPORTANT MUST ATTENTION** require profile-fit intent-protecting evidence for the behaviour harness — NEVER fail a build on a line-coverage % — why: lines execute without asserting intent, so coverage % is a diagnostic only, never a quality gate
**IMPORTANT MUST ATTENTION** wire `/integration-test --mode=review`'s feature-area-wide TC audit as a Phase D sensor BOTH pre-release AND on the SAME recurring cadence as `/scan-codebase-health` — never pre-release only — why: a diff-scoped-only run cannot see a §8 TC whose covering test regressed outside the current change set; only a periodic feature-area sweep catches it
**IMPORTANT MUST ATTENTION** research tool choices per detected stack — NEVER hardcode a linter/formatter/mutation tool — present top 2-3 options, enforce strictest defaults, loosen only with explicit approval — why: harnessability depends on the actual stack, not a default
**IMPORTANT MUST ATTENTION** harness inventory is a LIVING document — update it when new sensors are added later — why: a stale inventory misrepresents the active feedback loop
**IMPORTANT MUST ATTENTION** grep 3+ existing guides/sensors before authoring a new one; verify fit (same stack, gate stage, lifecycle) before copying a nearby pattern — why: closest example ≠ matching preconditions
**IMPORTANT MUST ATTENTION** cite `file:line` / config-path evidence for every detected sensor and stack fact (confidence >80% to act, <60% DO NOT recommend) — NEVER speculate a tool exists; grep the config to confirm — why: a hallucinated sensor leaves a real gap unguarded
**IMPORTANT MUST ATTENTION** bootstrap task tracking before phases — `TaskCreate` one todo per phase, mark `in_progress`/`completed` as you go; on context loss `TaskList` first — why: resume work, never duplicate phases

**Anti-Rationalization:**

| Evasion                                         | Rebuttal                                                                                  |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------- |
| "Linter probably set up — skip the prereq check" | Grep for the config files. No `file:line` proof = BLOCK Phase A/B/C/D/E until verified.   |
| "I'll pick the obvious linter myself"            | NEVER auto-decide — present top 2-3 via `AskUserQuestion`; the user owns binding conventions. |
| "High line coverage means tests are strong"      | Coverage is a diagnostic, not a gate. Choose profile-fit intent evidence; lines run without asserting. |
| "Inventory's small, I'll hold it in memory"      | Append per phase to the inventory file — context loss silently drops findings.            |
| "CLAUDE.md exists, harness already done"         | CLAUDE.md is a feedforward guide to ENHANCE, never a signal to skip phases.               |

**IMPORTANT MUST ATTENTION** BLOCK on `/linter-setup` before any phase · NEVER auto-decide harness content (`AskUserQuestion`-gate) · require profile-fit intent evidence, NEVER a universal mutation tool or line-coverage % gate.
