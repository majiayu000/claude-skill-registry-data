---
name: fix
description: '[Implementation] Use when you need to analyze and fix issues [INTELLIGENT ROUTING]. Flag: --target={ci|issue|logs|test|types|ui} scopes the fix; --target=types resolves TypeScript errors inline.'
disable-model-invocation: false
---

> Codex compatibility note:
>
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - User-question prompts mean to ask the user directly in Codex.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, execute each listed child-skill step explicitly and report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.

<!-- CODEX:PROJECT-REFERENCE-LOADING:START -->

## Codex Project-Reference Loading (No Hooks)

Codex uses static project-reference loading instead of runtime-injected project docs.
When coding, planning, debugging, testing, or reviewing, open project docs explicitly using this routing.

**Always read:**

- `docs/project-config.json` (project-specific paths, commands, modules, and workflow/test settings)
- `docs/project-reference/docs-index-reference.md` (routes to the full `docs/project-reference/*` catalog)
- `docs/project-reference/lessons.md` (always-on guardrails and anti-patterns)

**Missing/stale context route:** If `docs/project-config.json`, the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any task-required reference doc is missing or stale, auto-run `$project-init` or the narrow setup route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) before ordinary project-specific work. If Codex mirrors or `AGENTS.md` are missing/stale, ask the user to run `$sync-codex`; do not auto-run it.

**Situation-based docs:**

- Project structure/architecture/tech-stack/deployment/setup (any layer — backend, frontend, or infra): `project-structure-reference.md`
- Backend/CQRS/API/domain/entity changes: `backend-patterns-reference.md`, `domain-entities-reference.md`
- Frontend/UI/styling/design-system: `frontend-patterns-reference.md`, `scss-styling-guide.md`, `design-system/README.md`
- Spec authoring, `docs/specs/` pathing, or TC format: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`
- Behavior/public-contract changes or spec-test-code sync: `workflow-spec-test-code-cycle-reference.md` plus the spec docs above
- Derived spec indexes/ERDs/reimplementation guides: `spec-system-reference.md` and source Feature Specs under `docs/specs/`
- Integration test implementation/review: `integration-test-reference.md`
- E2E test implementation/review: `e2e-test-reference.md`
- Code review/audit work: `code-review-rules.md` plus domain docs above based on changed files

Do not read all docs blindly. Start from `docs-index-reference.md`, then open only relevant files for the task.

<!-- CODEX:PROJECT-REFERENCE-LOADING:END -->

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: `in_progress` on start, `completed` on end.
> **[BLOCKING]** Every completed/skipped step MUST include evidence or explicit skip reason.
> **[BLOCKING]** If Task tools unavailable, maintain equivalent step-by-step plan tracker with same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Eliminate the root cause of an issue using parallel subagent investigation — traced end-to-start with `file:line` evidence and fixed at the lowest invariant-owning layer (never the crash site) — then prove the fix with `$prove-fix` so the disease is cured, not just the symptom.

**Summary:**

- **Purpose:** an intelligent fix router that cures the disease, not the symptom — diagnose root cause with evidence, fix at the lowest invariant-owning layer, prove it with `$prove-fix`, then keep spec + tests + code in sync.
- **Router first (`--target=`):** with `--target={ci|issue|logs|test|types|ui}` clear the Root-Cause Prerequisite Gate, then jump to that self-contained inline branch (each runs its own diagnosis + `$prove-fix`); no flag = run the full diagnose→fix spine. — why: branches must not re-run §1/§2 of the standalone spine, but no branch is exempt from having a traced root cause.
- **Main steps (no-flag spine):** Root-Cause Prerequisite Gate → scout (parallel subagents) → diagnose root cause end-to-start (`debug-investigate`, `file:line` evidence, hypothesis matrix, forward convergence proof) → Confidence & Evidence Gate → plan with impact analysis → 🛑 Validate-Before-Fix approval → implement at the owning layer → `$prove-fix` → conditional `$spec` correctness check → `$changes-review` (production code) → `$why-review` terminal sign-off.
- **Root-Cause Prerequisite Gate (BLOCKING, runs FIRST):** a direct `$fix` call — no-flag spine **and** every `--target=` branch — MUST NOT edit code until `$debug-investigate` produced a root cause for THIS problem in THIS session, proven by a the current task list row or a written investigation report (memory is not evidence; a parent workflow row alone is not proof). Not run → run `$debug-investigate` first, then resume from the planning step. — why: otherwise the first edit lands with zero traced cause and patches the symptom site.
- **Three hard gates that cannot be skipped:** the Root-Cause Prerequisite Gate (above), the Confidence & Evidence Gate (declare `Confidence: X%` + `file:line`, STOP if <60%) and the 🛑 Validate-Before-Fix approval (present root cause + plan by asking the user directly before any code change — skip approval only inside a workflow).
- **Diagnose before patching:** trace the symptom end-to-start to the invariant-owning layer, and NEVER fix at the crash site — the crash site is a symptom, the cause enters at a lower layer.
- **Mode + skip rules:** default mode HARD (full rigor) unless ALL 5 trivial-bug opt-out conditions hold; standalone (no parent workflow) self-assembles the minimum spine `debug-investigate → fix + prove-fix → $spec correctness check → $changes-review (production code) → $why-review`; inside a workflow this whole contract is SKIPPED — **except the Root-Cause Prerequisite Gate, which never skips**: it still demands proof the sequence actually ran `debug-investigate` for this problem. — why: standalone has no sequence supplying diagnosis, spec sync, or review; and a workflow row is not proof its diagnosis step ran.

**Workflow:**

1. **Scout** — Use scout/researcher subagents to explore issue in parallel
2. **Diagnose** — Trace root cause through code paths with evidence
3. **Plan** — Create fix plan with impact analysis
4. **Fix** — Implement and verify the fix

**Key Rules:**

- **Root-Cause Prerequisite Gate (BLOCKING):** no code edit until `$debug-investigate` traced THIS problem in THIS session — evidence, not recall
- Debug Mindset: every claim needs `file:line` evidence
- Use subagents for parallel investigation of multiple hypotheses
- Always create a plan before implementing complex fixes
- **Target flag** (see [Target Routing](#target-routing---target)): `--target={ci|issue|logs|test|types|ui}` selects a self-contained inline branch that scopes the fix to that domain. No flag = full diagnose→fix spine below.

## Default Mode Policy

> **Default mode HARD (full rigor).** Every section below — parallel scout/researcher subagents, root-cause tracing with `file:line` evidence, Confidence & Evidence Gate, fix plan with impact analysis, preservation tests for the bug — applies by default.
>
> **Opt out to fast mode ONLY when ALL true** (bug genuinely trivial):
>
> - Root cause obvious from error message AND already located (no diagnosis needed)
> - Single-file fix, ≤10 lines changed
> - No cross-service impact, no contract change
> - Test for bug already exists OR bug non-functional (typo, log message)
> - Confidence in fix ≥95% without further investigation
>
> **Any condition fails → use full protocol below.** When in doubt, default hard. Skipping diagnosis on non-trivial bug fixes symptom and leaves disease.
>
> **Fast mode skips (and only skips):** parallel subagent investigation (direct read/grep instead), separate fix plan (inline change), regression-test authoring (only if covering test exists). Does NOT skip Confidence & Evidence Gate, Behavioral Delta Matrix, or running existing test suite.

## 🛑 Root-Cause Prerequisite Gate (Direct `$fix` Invocation) — BLOCKING

> **[BLOCKING] `$fix` MUST NOT edit code until `$debug-investigate` has produced a root cause for THIS problem in THIS session.** This gate runs BEFORE the Standalone Mode Minimum Contract below, BEFORE any `--target=` branch body, and BEFORE the 🛑 Validate-Before-Fix approval. — why: `$fix` invoked directly can otherwise reach its first edit with zero traced root cause, which patches the symptom site and ships the disease.
>
> **1. Trigger — ALL direct `$fix` invocations.** User-typed slash command or model-selected skill; every `--target={ci|issue|logs|test|types|ui}` branch **and** the no-flag spine alike. The `--target=` branches do NOT re-run §1/§2 of the contract below, but they DO pass through this gate. — why: a branch's own `debugger`/`tester` subagent step is not an end-to-start root-cause trace, so scoping the run does not remove the need for one.
>
> **2. Check — evidence, never memory.** Before the first code edit, determine whether `$debug-investigate` already ran **in this session, for this same problem**. Accept ONLY:
>
> - a the current task list row for `debug-investigate` (or its phase tasks) covering this symptom, **or**
> - a written investigation report naming this symptom (e.g. `.ai/workspace/analysis/{issue-name}.analysis.md`, `plans/reports/debug-investigate-*.md`) containing the end-to-start trace.
>
> **No such evidence → treat as NOT run.** Recalling that the cause "is known" is not evidence. — why: after context compaction the model's belief that it already investigated survives while the actual findings do not.
>
> **3. Act.** Not run → run `$debug-investigate` on the problem FIRST, then resume the `$fix` spine **from its planning step** using that root-cause report. This subsumes the spine's internal step-1 `debugger` subagent (identical to the contract's §1 rule below). — why: re-running diagnosis after the skill already traced it double-runs the spine.
>
> **4. Same-problem test.** A prior `$debug-investigate` for a **different** symptom does NOT satisfy this gate. Satisfaction binds to the problem, not to the skill name. When the current `<issues>` names a symptom the existing report does not cover, the gate FIRES. — why: one investigation per session would otherwise license unlimited untraced fixes.
>
> **5. Skip conditions — explicit, narrow, and recorded.** Record which one applies with its proof; never skip silently:
>
> | Condition                                                                                                                                                                             | Skip?   |
> | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
> | Same-problem evidence per §2 exists → cite the `file:line` / task-row proof and proceed                                                                                               | YES     |
> | Fast-mode-trivial bug (**ALL 5** `Default Mode Policy` opt-out conditions hold) → MAY inline the end-to-start trace instead of spawning the skill; the trace itself is still REQUIRED | PARTIAL |
> | Active parent workflow row whose sequence **already executed** `debug-investigate` for this problem → cite the completed step                                                         | YES     |
> | Active parent workflow row **alone**, with no completed `debug-investigate` step for this problem                                                                                     | **NO**  |
>
> **The last row is the hole this gate closes.** The contract below detects standalone mode by the mere _presence_ of a parent workflow row (`Detect mode`, §"Standalone Mode Minimum Contract"); a row can exist while the sequence's `debug-investigate` step never ran, ran for a different symptom, or was skipped. This gate ADDS the stricter requirement — proof of execution for THIS problem — on top of that detection; it never relaxes it. — why: presence of a container task is not evidence that the work inside it happened.
>
> **BLOCKED until:** the §2 check is stated with its evidence (or its explicit skip row + proof) AND a root-cause trace for this problem exists. **NEVER** proceed to plan or edit on "the cause is obvious" alone.

## Standalone Mode Minimum Contract (Non-Workflow Only)

> **`$fix` is normally a step inside `workflow-bugfix`** — there the sequence (`scout → investigate → debug-investigate → spec [mode=amend] → plan → … → fix → prove-fix → … → spec [mode=sync] → workflow-review-changes`) supplies the diagnosis, spec sync, and review around the fix. **Called STANDALONE, no sequence supplies them.** `$fix` alone diagnoses and patches code; it does NOT by itself guarantee the root cause was traced to its owning layer, that the Feature Spec under `docs/specs/` still matches behavior, or that the change was reviewed. Standalone, that gap is symptom-patching + spec/doc drift.
>
> **Scope:** this contract governs the **no-flag `$fix` spine** (the full diagnose→fix path). The `--target={ci|issue|logs|test|types|ui}` branches are self-contained — each runs its own diagnosis + `$prove-fix` — so they do NOT re-run §1/§2 here; standalone, they inherit only **§3 (spec-correctness check)** and **§4 (why-review)** as their trailing gates (and `--target=issue` already owns its own `$changes-review` gate — see that branch).
>
> **Detect mode:** call the current task list first (per the Nested Task Expansion Contract below). **Active parent workflow row present → this whole section is SKIPPED** (the workflow owns these steps; duplicating them double-runs the spine) — **but the Root-Cause Prerequisite Gate above still applies**: skipping this section requires the parent sequence's `debug-investigate` step to be _completed for this problem_, not merely present. Row present + that step not run → the gate fires and `$debug-investigate` runs first. **No parent row → standalone:** before the first code edit, MUST ATTENTION self-assemble this minimum bugfix spine as task tracking todos, in order:
>
> 1. **`$debug-investigate`** — _root cause, FIRST; mandated by the Root-Cause Prerequisite Gate above, whose §2 evidence check decides whether it already ran for this problem._ Trace the symptom end-to-start to the invariant-owning layer with `file:line` evidence (hypothesis matrix + forward convergence proof). This **is** the standalone diagnosis — it subsumes the spine's internal step-1 `debugger` subagent; resume the spine from its planning step using this report. _Fast-mode-trivial bugs (ALL Default Mode Policy opt-out conditions met) MAY inline the trace instead of spawning the skill, but the end-to-start trace is still required._
> 2. **Fix spine** — _this skill's_ `plan → 🛑 approve → implement → `$prove-fix`` body below. The Validate-Before-Fix approval gate and `$prove-fix` are unchanged.
> 3. **`$spec` spec-correctness check** — _CONDITIONAL, ensures spec docs aren't left stale._ From the proven root cause, decide which case holds:
>     - **Spec was WRONG / stale** — it described behavior that was never true, or intended behavior changed and the spec wasn't updated. The spec is (part of) the defect → run `$spec [mode=amend]` to correct the §1-§7 spec, then `$spec [mode=sync]` to reconcile §8 `TC-{FEATURE}-{NNN}` ↔ integration tests.
>     - **Spec was CORRECT, the code just failed to meet it** — pure code defect; §1-§7 behavior now matches the spec again. **No §1-§7 amendment.** But still check the §8 test cases: if the bug reproduced a scenario/edge case that **no existing `TC-{FEATURE}-{NNN}` covered** (the spec was _correct but lacked the bug case_), add a regression test case via `$spec [mode=tests]` so the spec captures it, then `$spec [mode=sync]` to reconcile §8 ↔ the new regression test. Only if an existing TC already covered the case do you record `Spec verified correct, bug case already in §8 — no spec change (code-only defect)` with `file:line` evidence and move on. Never leave a fixed bug whose case is absent from the spec's §8.
>     - **No governing spec exists** — the buggy area has no Feature Spec under `docs/specs/`. Record `No governing spec — nothing to amend` with `file:line` evidence; if the area now warrants one, run `$spec [mode=init]` (then `[mode=tests]` to seed §8 with the bug case as a regression TC) rather than only suggesting it. _Decide the case explicitly — skip only the amendment, never the decision; never leave the bug case undocumented when a spec governs the area._
> 4. **`$why-review`** — _rationale review, the FINAL todo (after the fix AND after any `$changes-review`)._ Terminal sign-off on the converged change: root cause correctly owned, fix at the lowest invariant-owning layer (not the crash site), no symptom-patching, regression covered, and the §3 spec decision justified. Reporting "done" is blocked until this passes. _Non-functional-trivial fixes (typo, log/comment text; fast-mode) MAY satisfy this inline/briefly rather than spawning the full skill — symmetric with §1._
>
> **Production-code fixes** also get a `$changes-review` todo **before** §4 (the broad code review whose validated fixes may change the diff; §4 then signs off on the result). `$changes-review` placement and the inside-workflow skip are owned by the shared Standalone Review Gate below — reference it; do not restate the mandate. **Final standalone todo order:** `debug-investigate → [fix spine + prove-fix] → spec-check → changes-review (if production code) → why-review`.

## Debug Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.**

- Verify each hypothesis against an actual code trace before acting — do NOT assume first hypothesis correct — why: the first guess is usually the nearest-attention trap, not the cause
- Every root cause claim must include `file:line` evidence
- If you cannot prove root cause with code trace, state "hypothesis, not confirmed"
- Question assumptions: "Is this really the cause?" → trace actual execution path
- Challenge completeness: "Are there other contributing factors?" → check related code paths
- No "should fix it" without proof — verify fix addresses traced root cause

## ⚠️ MANDATORY: Confidence & Evidence Gate

**MANDATORY IMPORTANT MUST ATTENTION** declare `Confidence: X%` with evidence list + `file:line` proof for EVERY claim.
**95%+** recommend freely | **80-94%** with caveats | **60-79%** list unknowns | **<60% STOP — gather more evidence.**

**Ultrathink** plan and start fixing these issues; follow Orchestration Protocol, Core Responsibilities, Subagents Team, Development Rules:
<issues>$ARGUMENTS</issues>

## Target Routing (`--target=`)

`$fix` is an intelligent router. With no flag it runs the full diagnose→fix spine below. Pass `--target=` to scope the run to a self-contained inline branch:

| `--target` | Behavior                                                        |
| ---------- | --------------------------------------------------------------- |
| `types`    | **Inline branch (below)** — TypeScript / type-error resolution. |
| `ci`       | **Inline branch (below)** — CI / pipeline failure triage.       |
| `issue`    | **Inline branch (below)** — tracked issue / ticket resolution.  |
| `logs`     | **Inline branch (below)** — log / stack-trace-driven debugging. |
| `test`     | **Inline branch (below)** — failing-test repair.                |
| `ui`       | **Inline branch (below)** — UI / visual-defect fixes.           |

No `--target` (or an unrecognized value) → run the full Workflow spine below; infer the right specialization from `<issues>`.

> **Formerly standalone skills.** `--target=ci|issue|logs|test|ui` were previously the separate skills `/fix-ci`, `/fix-issue`, `/fix-logs`, `/fix-test`, `/fix-ui`; they are now inline branches of `$fix` (folded — the standalone names no longer exist).

### `--target=types` — TypeScript / type-error branch

Run `tsc --noEmit` (or `nx build` / `bun run typecheck` / `npx tsc`) to gather all type errors, then:

1. **Collect** — Capture every type error with `file:line`.
2. **Classify** — Group by cause: missing types, wrong signatures, import/export issues.
3. **Fix at root** — Give each value its real, specific type (or `unknown` + a narrowing guard). Do NOT use `any` to silence the checker — `any` ships the underlying type defect. Fix the root cause (wrong interface, missing export), not the symptom site. — why: `any` silences the checker and lets the type defect ship.
4. **Repeat** until `tsc --noEmit` is clean — zero type errors.
5. **🛑 Validate Before Fix:** present errors + root cause by asking the user directly, get approval before code changes (skip if inside a workflow).
6. **After fixing, run `$prove-fix`** — build code proof traces per change with confidence scores. Never skip.

The Debug Mindset, Confidence & Evidence Gate, and all SYNC gates below apply to this branch unchanged.

### `--target=ci` — CI / pipeline-failure branch

**Goal:** Analyze CI/CD pipeline logs to identify and fix build/test failures in the configured CI provider/tooling.

**Key Rules:**

- **Infrastructure context:** read `docs/project-config.json` → `infrastructure.cicd.tool` to identify the CI provider/tooling (e.g. `azure-devops`, `github-actions`, `gitlab-ci`); target that provider's pipeline config files.
- Focus on CI-specific issues (env vars, Docker, dependencies, build order).
- Verify the fix does not break local development.

**Workflow:**

1. Use the `debugger` subagent to read the CI logs via the configured CI tool/API (from `docs/project-config.json`), analyze the final failing log/error **backward** to the root cause, and report back. Write findings to `.ai/workspace/analysis/{ci-issue}.analysis.md`; re-read before implementing.
2. **🛑 Present root cause + proposed fix → ask the user directly → wait for approval.**
3. Implement the fix from the report.
4. Use the `tester` subagent to verify; report back.
5. If tests fail, repeat from step 2.
6. Report a summary of changes; suggest next steps. Then run `$prove-fix`.

**Notes:** Use the CLI/API for the configured CI provider. If it is GitHub Actions and `gh` is unavailable, instruct the user to install and authorize GitHub CLI first.

The Debug Mindset, Confidence & Evidence Gate, and all SYNC gates below apply to this branch unchanged.

### `--target=issue` — tracked-issue / ticket branch

**Goal:** Investigate and fix bugs reported as tracked issues (e.g. GitHub issues) with full traceability.

**Active-goal read (BEFORE root-cause work):** resolve the active Goal Contract per `SYNC:goal-contract-satisfaction-loop` (active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md` → create from the issue). Map the ticket's acceptance criteria to the saved success criteria; after the fix, append proof evidence and remaining gaps to the Iteration Log. Closure is blocked while any required criterion remains FAIL.

**Key Rules:**

- Link the fix back to the issue for traceability.
- Verify the fix addresses the specific reproduction steps from the issue.

**Workflow:**

1. Activate the `debug-investigate` skill and follow its workflow — this step **satisfies** the Root-Cause Prerequisite Gate for this problem; record its report path as the gate's §2 evidence. See `.claude/docs/AI-DEBUGGING-PROTOCOL.md` for comprehensive guidelines.
2. Use external memory at `.ai/workspace/analysis/issue-[number].analysis.md` for structured analysis. **Re-read the ENTIRE analysis file before proposing any fix.**
3. **🛑 Present root cause + proposed fix → ask the user directly → wait for approval before implementing.**
4. Implement, then run `$prove-fix`.

> **Standalone Review Gate (non-workflow only):** any standalone production-code fix — the no-flag spine (Standalone Mode Minimum Contract above) **or** `$fix --target=issue` — adds a `$changes-review` task tracking todo as the **final changes-review gate**, placed immediately before the contract's §4 `$why-review` terminal sign-off (spec-check → changes-review → why-review). Inside a workflow, skip — the sequence handles `$changes-review`.

The Debug Mindset, Confidence & Evidence Gate, and all SYNC gates below apply to this branch unchanged.

### `--target=logs` — log / stack-trace branch

**Goal:** Analyze application logs to diagnose and fix runtime errors or unexpected behavior.

**Key Rules:**

- Focus on log patterns: stack traces, error codes, timing anomalies.
- Cross-reference logs with source code to find the actual root cause.

**Workflow:**

1. Check whether `./logs.txt` exists. If missing, set up permanent log piping in the project's script config (`package.json`, `Makefile`, `pyproject.toml`, …): **Bash/Unix** append `2>&1 | tee logs.txt`; **PowerShell** append `*>&1 | Tee-Object logs.txt`. Run the command to generate logs.
2. Use the `debugger` subagent to analyze `./logs.txt`: read with `Grep` `head_limit: 30` (last 30 lines; increase if needed — avoid loading the whole file). Write analysis to `.ai/workspace/analysis/{issue-name}.analysis.md`; re-read before fixing.
3. Use the `scout` subagent to locate the exact source of the issue; report back.
4. Use the `planner` subagent to create an implementation plan; report back.
5. **🛑 Present root cause + fix plan → ask the user directly → wait for approval.**
6. Implement the fix.
7. Use the `tester` subagent to verify; report back.
8. Use the `code-reviewer` subagent to review the changes; report back.
9. If tests fail, repeat from step 3.
10. Report a summary; suggest next steps. Then run `$prove-fix`.

The Debug Mindset, Confidence & Evidence Gate, and all SYNC gates below apply to this branch unchanged.

### `--target=test` — failing-test branch

**Goal:** Run test suites, analyze failures, and fix the underlying code or test issues.

**Active-goal read (BEFORE fixing):** resolve the active Goal Contract per `SYNC:goal-contract-satisfaction-loop` (active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md` → create from the reported test failure). Map failing-test evidence (before) and passing-test evidence (after) to the saved success criteria in the Iteration Log — a passing suite that misses a saved required criterion does NOT close the loop.

**Key Rules:**

- Distinguish between code bugs and flawed test expectations.
- Re-run tests after the fix to confirm all pass.
- Read `docs/project-reference/integration-test-reference.md` before reviewing/writing integration tests; consult `docs/specs/` for expected-behavior context when diagnosing failures.

**Workflow:**

1. Use the `tester` subagent to compile the code and fix any syntax errors.
2. Use the `tester` subagent to run the tests; report back. Write failure analysis to `.ai/workspace/analysis/{test-issue}.analysis.md`; re-read before fixing.
3. If tests fail, use the `debugger` subagent to find the root cause; report back.
4. Use the `planner` subagent to create an implementation plan; report back.
5. **🛑 Present root cause + fix plan → ask the user directly → wait for approval.**
6. Implement the plan step by step.
7. Use the `tester` subagent to verify; report back.
8. Use the `code-reviewer` subagent to review the changes; report back.
9. If tests fail, repeat from step 2.
10. Report a summary; suggest next steps. Then run `$prove-fix`.

The Debug Mindset, Confidence & Evidence Gate, and all SYNC gates below apply to this branch unchanged.

### `--target=ui` — UI / visual-defect branch

**Goal:** Diagnose and fix UI/UX issues — layout, styling, responsiveness, and visual bugs.

**Key Rules:**

- Always use BEM classes on template elements.
- Check responsive breakpoints when fixing layout issues.
- **Pre-read (design system):** load `designSystem.canonicalDoc` + `tokenFiles` from `docs/project-config.json` so fixes use real token names (`--brand-*`, `$brand-*`) and canonical component classes — not invented values.

**Required skills (priority order):** `ui-ux-pro-max` (design-intelligence DB) → `web-design-guidelines` (principles) → `design --lane=marketing` (implementation patterns).

**Workflow:**

**FIRST** — run `ui-ux-pro-max` searches to understand context and common issues:

```bash
python $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "<product-type>" --domain product
python $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "<style-keywords>" --domain style
python $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "accessibility" --domain ux
python $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "z-index animation" --domain ux
```

If the user provides screenshots/videos, use the `visual analysis tooling` skill to describe the issue in detail so developers can predict the root causes.

> **🛑 After identifying the UI root cause, present findings + proposed fix → ask the user directly → wait for approval before any code change.**

1. Use the `ui-ux-designer` subagent to implement the fix step by step (against the design guideline — `designSystem.canonicalDoc`).
2. Capture screenshots (at the exact parent container, not the whole page) and analyze with the appropriate Gemini skill (`visual analysis tooling`, `video-analysis`, or `document-extraction`) so the result matches the design guideline and addresses all issues. Repeat until addressed.
3. Use the browser automation tooling to verify the fix matches the design guideline.
4. Use the `tester` subagent to compile and test; report back. Repeat until all tests pass.
5. **If the user approves:** run the `project-manager` and `docs-manager` subagents in parallel to update plan progress and `./docs`; have `project-manager` also create/update a project roadmap at `./docs/project-roadmap.md`.
6. Report a summary; suggest next steps. Then run `$prove-fix`.

The Debug Mindset, Confidence & Evidence Gate, and all SYNC gates below apply to this branch unchanged.

## Workflow:

If user provides screenshots or videos, use `visual analysis tooling` skill to describe issue in detail; ensure developers can predict root causes from description.

### Fulfill the request

**Question Everything:** Use ask the user directly tool to ask probing questions to fully understand user's request, constraints, true objectives. Don't assume — clarify until 100% certain.

- Use ask the user directly to clarify any open questions.
- Ask 1 question at a time; wait for answer before next question.
- No questions → start next step.

> **⚠️ Validate Before Fix (NON-NEGOTIABLE):** After root cause + plan creation, MUST ATTENTION present findings + proposed fix plan to user by asking the user directly and get explicit approval BEFORE any code changes. No silent fixes.
> **End-to-Start Trace Gate:** For non-trivial bugs, failed verification, stale/incorrect final outputs, or behavior-changing fixes, the root-cause plan MUST ATTENTION include `Debugger Trace: End -> Start`, feeder paths, hypothesis matrix, owning fix layer, and forward convergence proof. If missing, STOP and run `$debug-investigate` or `$investigate` before planning code changes. (The Root-Cause Prerequisite Gate already forces this at invocation time; this gate re-checks the _content_ of the resulting trace.)

### Fix the issue

**Active-goal read (BEFORE root-cause work):** resolve the active Goal Contract per `SYNC:goal-contract-satisfaction-loop` — active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md` → create from the reported issue via `.claude/templates/goal-contract-template.md`. The saved success criteria define what "fixed" means — a proven local fix that misses a saved required criterion is NOT complete. After proof, append root cause, proof evidence, and remaining goal gaps to the Iteration Log. Tiny fixes may skip deeper gates ONLY with user-accepted reason recorded in the goal file.

Use `sequential-thinking` skill to break complex problems into sequential thought steps.
Use `problem-solving` skills to tackle issues.
Analyze skills catalog and activate other needed skills during the process.

1. Use `debugger` subagent to find root cause and report back to main agent. **Skip this step when the Root-Cause Prerequisite Gate already ran `$debug-investigate` for this problem** — that report subsumes this step; resume at step 3 (planning) instead of re-tracing. — why: re-running diagnosis double-runs the spine.
   1.5. Write investigation results to `.ai/workspace/analysis/{issue-name}.analysis.md`. Re-read ENTIRE file before planning fix.
   1.6. Confirm the report contains final symptom -> reader -> storage/projection -> writer -> consumer/job -> producer/origin, all feeder paths, hypothesis matrix, owning fix layer, and forward convergence proof.
2. Use `researcher` subagent to research root causes on internet (if needed) and report back.
3. Use `planner` subagent to create implementation plan based on reports; report back.
4. **🛑 Present root cause + fix plan → ask the user directly → wait for user approval.**
5. Use `$plan-execute` SlashCommand to implement plan step by step.
6. Final Report:

- Report back to user with summary of changes; explain briefly; guide user to get started; suggest next steps.
- Ask user whether to commit and push to git; if yes, use `git-manager` subagent.

* **IMPORTANT:** Sacrifice grammar for concision when writing reports.
* **IMPORTANT:** List unresolved questions at end of reports, if any.

**REMEMBER:**

- Generate images with `visual analysis tooling` skills on the fly for visual assets.
- Read and analyze generated assets with `visual analysis tooling` skills to verify they meet requirements.
- For image editing (removing background, adjusting, cropping), use media processing tooling as needed.

- **After fixing, MUST ATTENTION run `$prove-fix`** — build code proof traces per change with confidence scores. Never skip.

> **Spec-Loop completion gate (canonical: `SYNC:spec-loop-discipline`).** The fix is NOT done until the touched invariants close the loop: (1) every §4 [HARD] rule / §5 invariant the bug violated has a **universally-quantified property TC** ("for ALL inputs in {domain}, {invariant} holds") + boundary counter-case — not just the single reproduction example (this is the property bar the §3 regression-TC must meet, not merely an example case); (2) the fixed core-logic line is **mutation-killed** — if a mutant survives on the changed line the killing test is missing, so the bug can silently return (MUTATION-SCORE bar, not line-coverage %); (3) the finding fed BOTH the spec and the tests per the §3 spec-correctness decision AND a guarding test (Dual-Feedback) — a code-only patch with neither leaves the disease undocumented. Re-verify spec + tests + code together before declaring the fix complete.

---

## Next Steps (Standalone: after the Minimum Contract completes. Skip if inside workflow.)

> **The Root-Cause Prerequisite Gate and the Standalone Mode Minimum Contract above are NOT optional and NOT a question** — standalone `$fix` has already auto-run `debug-investigate` (gate-enforced) → fix spine → `$prove-fix` → conditional `$spec` check → (`$changes-review` for production code) → `$why-review` as the terminal sign-off. Do not re-ask the user whether to do those; they are the guaranteed floor.
>
> **AFTER that floor is met,** MUST ATTENTION use ask the user directly to offer what lies BEYOND the minimum (user decides):

- **"Proceed with full workflow (Recommended)"** — Hand off to the best-fit workflow (e.g. `workflow-bugfix`) from here to add the remaining gates the minimum spine omits — `plan-validate`, `integration-test` authoring/review/verify, `production-readiness-review`, `security-review`, `changelog`, `docs-update`.
- **"$test"** — Run the full test suite to verify the fix in context.
- **"Commit & push"** — Hand the proven, reviewed change to the `git-manager` subagent.
- **"Stop here"** — Minimum contract satisfied; user takes it from here.

> If already inside a workflow, skip both the contract and this menu — the workflow sequence handles diagnosis, spec sync, review, and next steps.

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks for each file read. Prevents context loss from long files. For simple tasks, MUST ATTENTION ask user whether to skip.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

<!-- SYNC:end-to-start-debugger-trace -->

> **End-to-Start Debugger Trace** — For non-trivial bugs, failed verification, regression fixes, behavior-changing code, or unclear code flow, start from the observed final state and walk backward before proposing a fix.
>
> 1. **Frame 0: observed end state** — Name the exact user-visible output, failing assertion, log line, persisted value, API response, rendered UI, or aggregate bucket. Record the reader/query/renderer that produced it with `file:line` evidence.
> 2. **Walk backward one hop at a time** — Trace final reader -> projection/cache/storage -> writer -> consumer/handler/job -> producer/caller -> original trigger. At every hop record: input, transformation, output, owner, and evidence.
> 3. **Enumerate all feeder paths** — Find every upstream producer/caller/event/job that can write into the final path, including retry, async, cache, background, and alternate UI/API paths. Mark each path verified, ruled out, or still unknown.
> 4. **Build the hypothesis matrix** — For each plausible cause, list evidence for, evidence against, how to reproduce/verify, blast radius, and status (`primary`, `contributing`, `ruled out`, `latent`). Do not fix until competing causes are explicitly resolved or bounded.
> 5. **Choose the owning fix layer** — Identify the invariant owner and the lowest shared point that protects all downstream consumers. A fix at the symptom site is rejected unless the symptom site owns the invariant.
> 6. **Prove convergence forward** — After choosing the fix, walk start -> end again and show how the corrected state reaches the observed final output. Map each root cause to a fix part and each fix part to a test/proof.
>
> **BLOCKED until:** final state named · backward trace written · all feeder paths enumerated · hypothesis matrix completed · owning fix layer justified · forward convergence proof mapped to tests.
>
> **NEVER:** Start at the first suspicious code path. Collapse multiple producers into one "flow". Treat duplicate symptoms as duplicate records without proving the read model. Skip ruled-out hypotheses.

<!-- /SYNC:end-to-start-debugger-trace -->

<!-- SYNC:root-cause-debugging -->

> **Root Cause Debugging** — Systematic approach, never guess-and-check.
>
> 1. **Reproduce** — Confirm the issue exists with evidence (error message, stack trace, screenshot)
> 2. **Isolate** — Narrow to specific file/function/line using binary search + graph trace
> 3. **Trace** — Follow data flow from input to failure point. Read actual code, don't infer.
> 4. **Hypothesize** — Form theory with confidence %. State what evidence supports/contradicts it
> 5. **Verify** — Test hypothesis with targeted grep/read. One variable at a time.
> 6. **Fix** — Address root cause, not symptoms. Verify fix doesn't break callers via graph `connections`
>
> **NEVER:** Guess without evidence. Fix symptoms instead of cause. Skip reproduction step.

<!-- /SYNC:root-cause-debugging -->

<!-- SYNC:nested-task-creation -->

> **Nested Task Expansion Contract** — For workflow-step invocation, the `[Workflow] ...` row is only a parent container; the child skill still creates visible phase tasks.
>
> 1. Call the current task list first. If a matching active parent workflow row exists, set `nested=true` and record `parentTaskId`; otherwise run standalone.
> 2. Create one task per declared phase before phase work. When nested, prefix subjects `[N.M] $skill-name — phase`.
> 3. When nested, link the parent with `TaskUpdate(parentTaskId, addBlockedBy: [childIds])`.
> 4. Orchestrators must pre-expand a child skill's phase list and link the workflow row before invoking that child skill or sub-agent.
> 5. Mark exactly one child `in_progress` before work and `completed` immediately after evidence is written.
> 6. Complete the parent only after all child tasks are completed or explicitly cancelled with reason.
>
> **Blocked until:** the current task list done, child phases created, parent linked when nested, first child marked `in_progress`.

<!-- /SYNC:nested-task-creation -->

<!-- SYNC:project-reference-docs-guide -->

> **Project Reference Docs Gate** — Run after task-tracking bootstrap and before target/source file reads, grep, edits, or analysis. Project docs override generic framework assumptions.
>
> 1. Identify scope: file types, domain area, and operation.
> 2. **Read `docs/project-config.json` first — the project's machine-readable map.** It is the single source of truth for THIS repo (modules/paths, framework + search keywords, test/E2E/integration run-commands, design system, architecture rules, workflow patterns); ground exact paths, run-commands, and conventions on it **before investigating, planning, or coding** — never assume framework defaults (`CLAUDE.md` + reference docs are derived from it). If it — or the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any required reference doc — is missing or stale, auto-run `$project-init` or the narrow route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) first; if Codex mirrors or `AGENTS.md` are stale, ask the user to run `$sync-codex` (never auto-run it).
> 3. Required docs by trigger: always `docs/project-reference/lessons.md`; doc lookup `docs-index-reference.md`; review `code-review-rules.md`; backend/CQRS/API `backend-patterns-reference.md`; domain/entity `domain-entities-reference.md`; frontend/UI `frontend-patterns-reference.md`; styles/design `scss-styling-guide.md` + `design-system/design-system-canonical.md`; integration tests `integration-test-reference.md`; E2E `e2e-test-reference.md`; feature docs/specs `feature-spec-reference.md` + `spec-system-reference.md` + `spec-principles.md`; behavior/public-contract/spec-test-code sync `workflow-spec-test-code-cycle-reference.md`; derived spec index/ERD/reimplementation guides `spec-system-reference.md` + source Feature Specs under `docs/specs/`; architecture/new area `project-structure-reference.md`.
> 4. Read every required doc, then before target work state: `Reference docs read: ... | Not applicable: ...`.
>
> **Ready when:** scope evaluated, `docs/project-config.json` consulted, required docs checked/read or setup route completed, `lessons.md` confirmed, citation emitted.

<!-- /SYNC:project-reference-docs-guide -->

<!-- SYNC:task-tracking-external-report -->

> **Task Tracking & External Report Persistence** — Bootstrap this before execution; then run project-reference doc prefetch before target/source work.
>
> 1. Create a small task breakdown before target file reads, grep, edits, or analysis. On context loss, inspect the current task list first.
> 2. Mark one task `in_progress` before work and `completed` immediately after evidence; never batch transitions.
> 3. For plan/review work, create `plans/reports/{skill}-{YYMMDD}-{HHmm}-{slug}.md` before first finding.
> 4. Append findings after each file/section/decision and synthesize from the report file at the end.
> 5. Final output cites `Full report: plans/reports/{filename}`.
>
> **Blocked until:** task breakdown exists, report path declared for plan/review work, first finding persisted before the next finding.

<!-- /SYNC:task-tracking-external-report -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:understand-code-first -->

> **Understand Code First** — HARD-GATE: Do NOT write, plan, or fix until you READ existing code.
>
> 1. Search 3+ similar patterns (`grep`/`glob`) — cite `file:line` evidence
> 2. Read existing files in target area — understand structure, base classes, conventions
> 3. Run `python .claude/scripts/code_graph trace <file> --direction both --json` when `.code-graph/graph.db` exists
> 4. Map dependencies via `connections` or `callers_of` — know what depends on your target
> 5. Write investigation to `.ai/workspace/analysis/` for non-trivial tasks (3+ files)
> 6. Re-read analysis file before implementing — never work from memory alone. — why: long context drifts from the file; the file is ground truth
> 7. NEVER invent new patterns when existing ones work — match exactly or document deviation. — why: divergent patterns fragment the codebase and slow every future reader
>
> **BLOCKED until:** `- [ ]` Read target files `- [ ]` Grep 3+ patterns `- [ ]` Graph trace (if graph.db exists) `- [ ]` Assumptions verified with evidence

<!-- /SYNC:understand-code-first -->

<!-- SYNC:evidence-based-reasoning -->

> **Evidence-Based Reasoning** — Speculation is FORBIDDEN. Every claim needs proof.
>
> 1. Cite `file:line`, grep results, or framework docs for EVERY claim
> 2. Declare confidence: >80% act freely, 60-80% verify first, <60% DO NOT recommend
> 3. Cross-service validation required for architectural changes
> 4. "I don't have enough evidence" is valid and expected output
>
> **BLOCKED until:** `- [ ]` Evidence file path (`file:line`) `- [ ]` Grep search performed `- [ ]` 3+ similar patterns found `- [ ]` Confidence level stated
>
> **Forbidden without proof:** "obviously", "I think", "should be", "probably", "this is because"
> **If incomplete →** output: `"Insufficient evidence. Verified: [...]. Not verified: [...]."`

<!-- /SYNC:evidence-based-reasoning -->

<!-- SYNC:fix-layer-accountability -->

> **Fix-Layer Accountability** — NEVER fix at the crash site. Trace the full flow, fix at the owning layer.
>
> AI default behavior: see error at Place A → fix Place A. This is WRONG. The crash site is a SYMPTOM, not the cause.
>
> **MANDATORY before ANY fix:**
>
> 1. **Trace full data flow** — Map the complete path from data origin to crash site across ALL layers (storage → backend → API → frontend → UI). Identify where the bad state ENTERS, not where it CRASHES.
> 2. **Identify the invariant owner** — Which layer's contract guarantees this value is valid? That layer is responsible. Fix at the LOWEST layer that owns the invariant — not the highest layer that consumes it.
> 3. **One fix, maximum protection** — Ask: "If I fix here, does it protect ALL downstream consumers with ONE change?" If fix requires touching 3+ files with defensive checks, you are at the wrong layer — go lower.
> 4. **Verify no bypass paths** — Confirm all data flows through the fix point. Check for: direct construction skipping factories, clone/spread without re-validation, raw data not wrapped in domain models, mutations outside the model layer.
>
> **BLOCKED until:** `- [ ]` Full data flow traced (origin → crash) `- [ ]` Invariant owner identified with `file:line` evidence `- [ ]` All access sites audited (grep count) `- [ ]` Fix layer justified (lowest layer that protects most consumers)
>
> **Anti-patterns (REJECT these):**
>
> - "Fix it where it crashes" — Crash site ≠ cause site. Trace upstream.
> - "Add defensive checks at every consumer" — Scattered defense = wrong layer. One authoritative fix > many scattered guards.
> - "Both fix is safer" — Pick ONE authoritative layer. Redundant checks across layers send mixed signals about who owns the invariant.

<!-- /SYNC:fix-layer-accountability -->

<!-- SYNC:source-test-drift-check -->

> **Source/test drift check.** For coding, fix, debug, investigation, test, or review work: when source behavior changes, inspect affected unit/integration/E2E tests and decide from evidence whether tests should change to match intended behavior or the source change is an unintended bug to fix. Do not write tests for migration code; schema/data migrations are one-time execution paths, not core application logic.

<!-- /SYNC:source-test-drift-check -->

<!-- SYNC:test-failure-fault-adjudication -->

> **Test-Failure Fault Adjudication** — When a test fails (or you are debugging or fixing a failure), the job is to determine _who is at fault — the source code or the test code_. Getting that verdict right matters more than turning the suite green. Binds every debug / fix / test skill identically.
>
> 1. **Provisional verdict before touching either side.** Classify the observed evidence as SOURCE-WRONG, TEST-WRONG, TEST-NOT-OPTIMAL, ENVIRONMENT-BLOCKED, or AMBIGUOUS; then `$debug-investigate` and trace end-to-start before editing. A green-again suite is NOT the goal.
> 2. **Triangulate against the spec AND the source.** If a governing Feature Spec covers the behavior (e.g. `docs/specs/**` — §3 ACs / §4 BRs / §5 invariants / §8 TCs), it is the tiebreaker for _intended_ behavior — compare BOTH the production source and the failing test against it. With no spec, the documented intent / acceptance criteria / caller contract is the reference. Decide from this evidence whether the SOURCE is wrong or the TEST is wrong.
> 3. **Classify who is at fault, then fix the wrong side at its root:**
>     - **SOURCE-WRONG** — production code violates the spec's intended behavior or a clear invariant → fix the source at the owning layer; keep or strengthen the test that caught it.
>     - **TEST-WRONG** — the test encodes a stale or incorrect assertion, setup, or expectation that contradicts intended behavior → fix the test at its root. NEVER weaken an assertion, add a skip, or relax a timeout to force green.
>     - **TEST-NOT-OPTIMAL** — intended behavior is valid but the test seam, timing, or assertion signal is fragile → improve the test without weakening the invariant.
>     - **ENVIRONMENT-BLOCKED** — infrastructure or external state prevents a source/test verdict → preserve diagnostics and stop mutation until the environment is healthy.
>     - **AMBIGUOUS** — evidence or intended behavior does not safely select an owner → ask the user or canonical owner before editing.
>     - NEVER change a test to match broken source, and NEVER change source to satisfy a broken test. (Migration code excluded — schema/data migrations are one-time execution paths, not core application logic.)
> 4. **Ask the user when intended behavior is unclear.** If no spec covers the behavior, the spec is silent, or the spec is ambiguous about which side is correct, STOP and ask the user directly (or consult the canonical spec owner) before editing either side — never silently pick source or test just to make the suite pass.
>
> Reconcile to intended behavior, never to whichever side currently passes — green can encode the very bug.

<!-- /SYNC:test-failure-fault-adjudication -->

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:fix-layer-accountability:reminder -->

**IMPORTANT MUST ATTENTION** trace full data flow and fix at the owning layer, not the crash site. Audit all access sites before adding `?.`.

<!-- /SYNC:fix-layer-accountability:reminder -->

<!-- SYNC:understand-code-first:reminder -->

**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read code BEFORE any modification. Run graph trace when graph.db exists.

<!-- /SYNC:understand-code-first:reminder -->

<!-- SYNC:evidence-based-reasoning:reminder -->

**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim. Confidence >80% to act, <60% = do NOT recommend.

<!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:task-tracking-external-report:reminder -->

- **MANDATORY** Bootstrap task tracking before target work; transition one task at a time.
- **MANDATORY** Persist plan/review findings to `plans/reports/` incrementally and synthesize from disk.

<!-- /SYNC:task-tracking-external-report:reminder -->

<!-- SYNC:project-reference-docs-guide:reminder -->

- **MANDATORY** Before investigating, planning, or coding, read `docs/project-config.json` (the project map: modules/paths, run-commands, conventions, architecture/workflow rules) + the required project-reference docs, and cite `Reference docs read: ...`.
- **MANDATORY** Always include `lessons.md`; project config + conventions override generic framework defaults.
- **MANDATORY** If project config, root instruction files, or any required reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.

<!-- /SYNC:project-reference-docs-guide:reminder -->

<!-- SYNC:end-to-start-debugger-trace:reminder -->

**IMPORTANT MUST ATTENTION** debugger trace gate: for non-trivial bug/fix/investigation/review work, start at the observed final output and trace backward through reader -> storage/projection -> writer -> consumer/job -> producer/trigger. Enumerate all feeder paths and hypotheses before fixing. **BLOCKED until** trace, hypothesis matrix, owning fix layer, and forward convergence proof exist.

<!-- /SYNC:end-to-start-debugger-trace:reminder -->

<!-- SYNC:nested-task-creation:reminder -->

- **MANDATORY** Parent workflow rows do not replace child phase tracking; expand phases and link the parent when nested.
- **MANDATORY** Orchestrators pre-expand child skill phases before invocation; use `[N.M] $skill-name — phase` prefixes and one-`in_progress` discipline.

<!-- /SYNC:nested-task-creation:reminder -->

<!-- SYNC:goal-contract-satisfaction-loop:reminder -->

- **MANDATORY** Resolve the active Goal Contract BEFORE work (active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md` → create from current request) and read saved success criteria before editing.
- **MANDATORY** Append iteration evidence after execution; emit a Goal Satisfaction matrix (PASS/FAIL/BLOCKED) before reporting PASS; loop on validated FAIL; escalate repeated no-progress or blockers. NEVER store secrets in goal files.

<!-- /SYNC:goal-contract-satisfaction-loop:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Eliminate the root cause of an issue — traced end-to-start with `file:line` evidence and fixed at the lowest invariant-owning layer (never the crash site) — then prove the fix with `$prove-fix` so the disease is cured, not just the symptom.

**MUST ATTENTION — Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **End-To-Start Debugger Trace:** start at observed final output, trace backward through every feeder path before fixing.
- **Root Cause Debugging:** reproduce → isolate → trace → hypothesize → verify → fix the cause, never symptoms.
- **Nested Task Creation:** parent workflow rows don't replace child phase tracking; expand and link phases.
- **Project Reference Docs Guide:** read required project-reference docs (`lessons.md` always) before target work.
- **Task Tracking & External Report:** bootstrap task tracking; persist plan/review findings to `plans/reports/` incrementally.
- **Critical Thinking:** apply critical + sequential thinking; traced proof per claim, confidence >80% to act.
- **Understand Code First:** search 3+ patterns and read code before any modification.
- **Evidence-Based Reasoning:** cite `file:line` for every claim; <60% confidence = do NOT recommend.
- **Fix-Layer Accountability:** trace full data flow, fix at the owning layer, not the crash site.
- **Source/Test Drift Check:** when source behavior changes, decide from evidence whether affected tests change.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.

**IMPORTANT MUST ATTENTION** Root-Cause Prerequisite Gate (BLOCKING, FIRST) — a direct `$fix` call (no-flag spine AND every `--target=` branch) MUST NOT edit code until `$debug-investigate` traced THIS problem in THIS session, proven by a the current task list row or a written investigation report; recall is NOT evidence, a prior investigation of a DIFFERENT symptom does NOT count, and a parent workflow row alone is NOT proof its diagnosis step ran — not satisfied → run `$debug-investigate` first, then resume from the planning step — why: without it the first edit lands with zero traced cause and patches the symptom site
**IMPORTANT MUST ATTENTION** trace the symptom end-to-start to the invariant-owning layer and fix there — NEVER at the crash site — why: the crash site is a symptom; the bad state enters at a lower layer and one fix there protects all downstream consumers
**IMPORTANT MUST ATTENTION** declare `Confidence: X%` + `file:line` proof for EVERY claim — 95%+ recommend, 80-94% caveats, 60-79% list unknowns, STOP if <60% — why: speculation patches the wrong layer and ships the disease
**IMPORTANT MUST ATTENTION** 🛑 Validate-Before-Fix — present root cause + plan by asking the user directly and get approval BEFORE any code change (skip ONLY inside a workflow) — why: silent fixes bypass the human gate on irreversible code change
**IMPORTANT MUST ATTENTION** route on `--target=` FIRST — each `{ci|issue|logs|test|types|ui}` branch is self-contained (own diagnosis + `$prove-fix`); no flag = full diagnose→fix spine — why: branches must not re-run §1/§2 of the standalone spine
**IMPORTANT MUST ATTENTION** default mode HARD (full rigor) — opt out to fast mode ONLY when the bug is genuinely trivial (ALL 5 Default Mode Policy conditions met); when in doubt default hard — why: skipping diagnosis on a non-trivial bug fixes the symptom and leaves the disease
**IMPORTANT MUST ATTENTION** standalone (no parent workflow) self-assembles the spine `debug-investigate → fix + prove-fix → $spec correctness check → $changes-review (production code) → $why-review`; inside a workflow SKIP the contract — but NEVER the Root-Cause Prerequisite Gate, which still demands proof the sequence's `debug-investigate` step ran for this problem — why: standalone has no sequence supplying diagnosis, spec sync, or review; and a container row is not proof its diagnosis step ran
**IMPORTANT MUST ATTENTION** after fixing, run `$prove-fix` — build code proof traces per change with confidence scores; never skip — why: a "should fix it" without a forward convergence proof is unverified
**IMPORTANT MUST ATTENTION** spec-loop completion — the fix is NOT done until the violated §4/§5 invariant has a universally-quantified property TC + boundary case, the changed line is mutation-killed, and the finding fed BOTH spec and tests (Dual-Feedback) — why: a code-only patch leaves the bug case undocumented and able to silently return
**IMPORTANT MUST ATTENTION** break work into small task tracking todos BEFORE starting (one read = one task); call the current task list first on context loss to resume, never duplicate — why: long debug files exhaust context and silently lose findings
**IMPORTANT MUST ATTENTION** read required project-reference docs (`lessons.md` always; `integration-test-reference.md` for test branch; `docs/specs/` for behavior) before target work — why: project conventions override generic debugging assumptions
**IMPORTANT MUST ATTENTION** on a FAILED TEST (`--target=test` or any test failure), FIRST read the `$integration-test-review` skill protocol (assertion-quality, coverage & spec↔test↔code fault gates) to set fix direction — decide whether the fault is a source-code root cause or a test-code setup/assertion issue — why: fixing without that verdict patches the wrong side and can green a broken invariant.
**IMPORTANT MUST ATTENTION** search 3+ similar patterns and read existing code before any fix; evaluate fit before copying a nearby pattern — why: closest example ≠ matching preconditions
**IMPORTANT MUST ATTENTION** add a final review todo to verify work quality, then extract root-cause lessons (`$learn`) if the failure mode would recur without the reminder

**Anti-Rationalization:**

| Evasion                                       | Rebuttal                                                                                                                                                         |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Root cause is obvious, just patch it"        | Trace end-to-start to the invariant owner with `file:line` first — the obvious site is the symptom.                                                              |
| "I already investigated this"                 | Show the the current task list row or investigation report for THIS symptom. Recall is not evidence — after compaction the belief survives, the findings do not. |
| "A workflow is running, it handled diagnosis" | A parent row is a container, not proof. Cite the _completed_ `debug-investigate` step for this problem or the gate fires.                                        |
| "`--target=` scopes it, so no trace needed"   | Every branch passes through the Root-Cause Prerequisite Gate. A `debugger`/`tester` subagent step is not an end-to-start trace.                                  |
| "Fix it where it crashes"                     | Crash site ≠ cause site. Fix at the LOWEST layer that owns the invariant and protects all consumers.                                                             |
| "Add a `?.` / guard and move on"              | Scattered defensive checks = wrong layer. One authoritative fix beats many guards.                                                                               |
| "Confident enough, skip evidence"             | No `file:line` + Confidence % = no claim. STOP and gather evidence if <60%.                                                                                      |
| "Small fix, skip the approval gate"           | 🛑 Validate-Before-Fix is non-negotiable standalone — present root cause + plan, get approval.                                                                   |
| "Tests pass, the fix is done"                 | Not done until property TC + boundary case exist, the changed line is mutation-killed, and spec ↔ tests fed (Dual-Feedback).                                     |
| "Already searched the codebase"               | Show `file:line` evidence. No proof = no search.                                                                                                                 |

**IMPORTANT MUST ATTENTION** NEVER edit code until `$debug-investigate` traced THIS problem in THIS session — evidence (task row / report), not recall.
**IMPORTANT MUST ATTENTION** NEVER fix at the crash site — trace end-to-start to the invariant owner and fix there.
**IMPORTANT MUST ATTENTION** declare `Confidence: X%` + `file:line` for every claim; STOP if <60%.
**IMPORTANT MUST ATTENTION** 🛑 Validate-Before-Fix approval before any code change, then `$prove-fix` after — never skip either.

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break into small todo tasks and sub-tasks via task tracking.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:START -->

## Hookless Prompt Protocol Mirror (Auto-Synced)

Source: `.claude/.ck.json` + `.claude/skills/shared/sync-inline-versions.md` (`:full` blocks) + `.claude/scripts/lib/hookless-prompt-protocol.cjs`

## [WORKFLOW-EXECUTION-PROTOCOL] [BLOCKING] Workflow Execution Protocol — MANDATORY IMPORTANT MUST CRITICAL. Do not skip for any reason.

**Generic portability boundary:** Reusable skills and protocol text stay project-neutral; project-specific conventions are discovered from docs/project-config.json and docs/project-reference/. Apply shared AI-SDD from `shared/sdd-artifact-contract.md`. Read `docs/project-config.json` and `docs/project-reference/docs-index-reference.md`, then open the project reference docs named there. For spec, test-case, behavior-change, public-contract, or `docs/specs/` work, route through the local spec docs named by the docs index: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`, and `workflow-spec-test-code-cycle-reference.md` when specs/tests/code must stay synchronized. If either file or a required reference doc is missing or stale, auto-run `$project-init` (or the narrow lower-level route such as `$project-config`, `$docs-init`, `$scan-all`, or `$scan --target=<key>`) before ordinary project-specific work. Any supported AI tool may execute when this shared context and local docs are available.

1. **DETECT:** If the prompt starts with an explicit slash skill/workflow command, execute it directly. Otherwise match the prompt against the workflow catalog and skill list.
2. **ANALYZE:** Choose the best option: execute directly, invoke a skill, activate a standard workflow, or compose a custom step combination.
3. **AUTO-SELECT:** Pick the best option yourself. Do not ask the user to choose between direct execution, skill, standard workflow, or custom workflow.
4. **ACTIVATE:** For a selected workflow, call `$start-workflow <workflowId>`; for a selected skill, invoke that skill; for a custom workflow, sequence custom steps directly; for direct execution, proceed with the task.
5. **CREATE TASKS:** task tracking for ALL workflow/skill/custom steps before execution when the selected path has multiple steps.
6. **PARALLELIZE:** Before executing the task list, tag each task `PAR` (independent inputs + write set disjoint from every other `PAR` task) or `SEQ` (name the blocking dependency), group `PAR` tasks into waves, declare the wave plan, and spawn each wave's sub-agents in ONE message — all-return barrier per wave, fan-out one level deep unless a sub-agent's own definition authorizes further fan-out. Sequential-by-default is a defect when tasks are independent; do not parallelize shared write targets, output-consuming tasks, trivial single-file work, ordering a skill or workflow explicitly fixes, or user-approval gates.
7. **EXECUTE:** Advance per the **Workflow Step Advancement & Parallel Phases** rule in your context instructions — model-driven; a sub-agent completion advances a step identically to an inline call; a parallel-phase group is an all-return barrier (advance only after ALL members return, never serialize it)

## Shared AI-SDD Protocol Markers

Source: `.claude/skills/shared/sync-inline-versions.md`

## SYNC:ai-sdd-artifact-contract

> **AI-SDD Artifact Contract** — Shared spec-driven development rules stay portable and source-owned.
>
> 1. Keep reusable AI-SDD principles in `.claude`; put repository-specific paths, commands, owners, products, and formats in project config/reference docs.
> 2. Preserve cycle: `spec -> plan -> tasks -> implement -> verify -> update spec/docs`.
> 3. Trace every requirement or invariant through decision, task, TC/test, source evidence, and docs/spec update.
> 4. Treat code-to-spec extraction as reference-only until accepted by the canonical spec owner.
> 5. Any supported AI tool may plan, implement, review, or verify with synced context; using multiple tools is optional.
> 6. Update `.claude` source first, then sync generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`. — why: mirrors are generated artifacts; hand-edits are overwritten on the next sync
> 7. If `docs/project-config.json`, root instruction files, or a required project-reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.
>
> **Active reference:** `shared/sdd-artifact-contract.md` in the active skills root.

---

## SYNC:ai-sdd-artifact-contract:reminder

- **MANDATORY** Apply `shared/sdd-artifact-contract.md`; keep reusable AI-SDD in `.claude` and local rules in project docs.
- **MANDATORY** Code-to-spec extraction is reference-only until canonical acceptance; any supported AI tool may execute with synced context.
- **MANDATORY** Update `.claude` source before syncing generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`.
- **MANDATORY** Missing or stale project config, root instruction files, or required reference docs route project-specific work through `$project-init` or the narrow setup route automatically.
  **[TASK-PLANNING] [MANDATORY]** BEFORE executing any workflow or skill step, create/update task tracking for all planned steps, then keep it synchronized as each step starts/completes.

## [LESSON-LEARNED-REMINDER] [BLOCKING] Task Planning & Continuous Improvement — MANDATORY. Do not skip.

Break work into small tasks (task tracking) before starting. Add final task: "Analyze AI mistakes & lessons learned".

**Extract lessons — ROOT CAUSE ONLY, not symptom fixes:**

1. Name the FAILURE MODE (reasoning/assumption failure), not symptom — "assumed API existed without reading source" not "used wrong enum value".
2. Generality test: does this failure mode apply to ≥3 contexts/codebases? If not, abstract one level up.
3. Write as a universal rule — strip project-specific names/paths/classes. Useful on any codebase.
4. Consolidate: multiple mistakes sharing one failure mode → ONE lesson.
5. **Recurrence gate:** "Would this recur in future session WITHOUT this reminder?" — No → skip `$learn`.
6. **Auto-fix gate:** "Could `$code-review`/`$code-simplifier`/`$security-review`/`$lint` catch this?" — Yes → improve review skill instead.
7. BOTH gates pass → ask user to run `$learn`.
   **[CRITICAL-THINKING-MINDSET]** Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
   **Anti-hallucination principle:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.
   **AI Attention principle (Primacy-Recency):** Put the 3 most critical rules at both top and bottom of long prompts/protocols so instruction adherence survives long context windows.
   **Goal-driven execution:** Define success criteria first, loop until verified, and stop only when observable checks pass.
   **Tests verify intent:** Tests must protect business rules/invariants and fail when the protected intent breaks, not only mirror current behavior.

## Common AI Mistake Prevention (System Lessons)

- **Re-read files after context compaction.** Edit requires prior Read in same context; compaction wipes read state. Re-read before editing.
- **Grep for old terms after bulk replacements.** AI over-trusts find/replace completeness. Grep full repo after bulk edits for missed refs in docs/configs/catalogs.
- **Check downstream references before deleting.** Deletions cascade doc/code staleness. Map referencing files before removal.
- **After memory loss, check existing state before creating new.** Compaction wipes prior-work memory. Query current state to resume — never blindly duplicate.
- **Verify AI-generated content against actual code.** AI hallucinates APIs, class names, method signatures. Grep to confirm existence before documenting/referencing.
- **Trace full dependency chain after edits.** Changing a definition misses downstream consumers. Trace the full chain.
- **When renaming, grep ALL consumer file types.** Some file types silently ignore missing refs (no compile error). Search code, templates, configs, generated files.
- **Trace ALL code paths when verifying correctness.** Code existing ≠ code executing. Trace early exits, error branches, conditional skips — not just happy path.
- **Update docs that embed canonical data when source changes.** Docs inlining derived data (workflows, schemas, configs) go stale silently. Update all embedding docs alongside source.
- **Verify sub-agent results after context recovery.** Background agents may finish while parent compacted — grep-verify output, don't trust assumed completion.
- **Cross-check full target list against sub-agent assignments.** Parallel sub-agents by category miss boundary items. Reconcile union of assignments against target list before proceeding.
- **Sub-agents inherit knowledge only from their agent .md definition — use custom agent types, not built-in Explore.** Tool adoption = permission + knowledge + enforcement (numbered workflow step).
- **Persist sub-agent findings incrementally, not as a final batch.** Long sub-agents hit cutoffs before final write — findings lost. Instruct append-per-section to report file.
- **When debugging, ask "whose responsibility?" before fixing.** Trace caller (wrong data) vs callee (wrong handling). Fix at responsible layer — never patch symptom site.
- **Test failure → record a provisional verdict before trace/edit, then investigate.** Use the full five-way taxonomy: SOURCE-WRONG (production violates intent), TEST-WRONG (assertion/setup is stale), TEST-NOT-OPTIMAL (valid but fragile or low-signal test), ENVIRONMENT-BLOCKED (external state prevents a verdict), or AMBIGUOUS (intent/evidence cannot choose safely). Then trace root cause and triangulate against the governing spec (`docs/specs/**` if one exists) AND source. NEVER weaken an assertion, add a skip, relax a timeout, or change source merely to force green.
- **Grep ALL removed names after extraction/refactoring.** Primary file "done" ≠ secondary files clean. Grep entire scope for every removed symbol before declaring complete.
- **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Pattern-matching as "wrong" skips context. Before changing or reporting any constant/limit/flag/cutoff: read comments, git blame, the CALLER's ordering (the guarantee that makes the value correct usually lives in code running immediately BEFORE the cited line), and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard — and in a validation pass, an accurate `file:line` citation proves the transcription, never the defect.
- **Verify ALL affected outputs, not just the first.** One build green ≠ all green. Multi-stack changes (backend/frontend/tests/docs) require verifying EVERY output.
- **Evaluate fit before copying a nearby pattern.** Closest example ≠ matching preconditions — verify the new context shares the same constraints, base classes, scope, lifetime.
- **Holistic-first debugging — resist nearest-attention trap.** Don't dive into first plausible cause. List EVERY precondition (config, env vars, paths, DB, endpoints, creds, versions, DI, data). Verify each against evidence (grep/query — not reasoning). Ask "what would falsify this?" — if nothing, it's not a hypothesis. Most expensive failure: going deeper in "obvious" layer while bug sits in layer never questioned.
- **Surgical changes — apply the diff test (context-aware).** Two modes: (1) Bug fix → every line traces to the bug; no restyling; orphan cleanup only for imports YOUR changes made unused. (2) Review/enhancement → implement improvements AND announce as "Enhancement beyond main request: [what]". Never silently scope-creep. Diff test: "Would this line exist if I wasn't asked to do X?" — if no, delete or announce.
- **Surface ambiguity before coding — don't pick silently.** Multiple valid interpretations → present each with effort: "[Request] could mean (1) [N h], (2) [N h]. Which matters?" List scope/format/volume/constraints assumptions first. If simpler path exists, say so. Never silently pick.
- **[MANDATORY FIRST ACTION] ALWAYS activate a suitable skill or workflow BEFORE responding.** Match task against workflow catalog + skill list; invoke via skill invocation or `$start-workflow <workflowId>`. NEVER answer or write code before checking. Skip = protocol violation.
- **Why-Review adversarial mindset — apply when reviewing any plan, decision, or design.** Default SKEPTIC not VALIDATOR: steel-man a rejected alternative, invert each stated reason ("what does it sacrifice?"), stress-test top 2-3 assumptions, run pre-mortem ("ships, fails in 3 months — what breaks?"), surface 1-2 alternatives author missed. Section presence ≠ quality; quality = causal reasoning + concrete mitigations + evidence, not "it's better" or "monitor closely".
- **Front-load report-write in sub-agent prompts for large reviews.** Many-file sub-agents hit budget before final write — findings lost. Design prompts so: (1) report-write is first explicit deliverable, (2) append per-file/section (not batched), (3) scope bounded so reads don't exhaust budget. Truncated mid-sentence with no report file → spawn narrower scope, don't retry same prompt.
- **After context compaction, re-verify all prior phase outcomes before continuing.** Summaries describe intent, not environment state (git index, filesystem, processes). On resume, FIRST audit: git status, re-read modified files, verify filesystem. Every "completed" claim is an untested hypothesis until evidence confirms.
- **OOM/memory: check row count before row size.** Triage: (1) Unbounded query — no DB filter for trigger? Push filter to DB; eliminates OOM. (2) Large rows? Projection reduces proportionally. Row reduction > projection in ROI.
- **Assert the outcome your system OWNS, never the intermediate state your INFRASTRUCTURE owns.** When testing anything asynchronous (queue/broker delivery, retries, background jobs, caches, replication), assert the final business/entity state. NEVER assert the delivery bookkeeping — consume/send status, attempt counts, last-error, row existence or counts in a broker, scheduler, or outbox/inbox table. That bookkeeping lives in shared infrastructure that ANY co-running process (a peer worker, a second replica, a leftover local container) can write, usually under a deterministic shared key, so the assertion silently tests the developer's environment instead of the system: green when run alone, flaky the instant anything else shares that broker + database. Gate question for every assertion: "would this hold no matter WHICH process did the work?" — if no, assert the converged data state instead. Corollary: process-local fault injection and in-process telemetry cannot gate work any process may perform — use them as stress amplifiers (arm → bounded window → disarm → assert convergence), never as preconditions.
- **Keep domain concepts out of generic/shared/infrastructure layers.** Reusable layer (shared library, framework, infra module) must reference NO consumer-specific domain concept — tenant/customer/product IDs, business entities, feature rules. Leak compiles + runs → passes review silently while coupling the "reusable" layer to one consumer. Keep shared type domain-free; push domain fields/logic down into the consumer via subclass/composition. — why: a layer coupled to one consumer's domain is no longer reusable.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:END -->
