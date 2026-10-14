---
name: plan
description: '[Planning] Use when you need intelligent plan creation with prompt enhancement. Flag: --mode={ci|cro} (default none — standard planning); --mode=ci plans a fix from a GitHub Actions CI run/log, --mode=cro plans conversion-rate optimization (25-item CRO framework).'
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

**Goal:** Research the codebase and collaborate with the user to deliver a validated, implementation-ready phased plan — every phase startable immediately (exact file paths, zero open decisions, mapped TC IDs) — so coding proceeds without rework at minimum future change cost.

**Summary:**

- PLANNING ONLY — NEVER implement/execute code; produce `plan.md` + per-phase `phase-XX` files + a `goal.md` Goal Contract, then hand off.
- **Main pipeline (the steps AI keeps forgetting):** pre-check active/suggested plan → bootstrap Goal Contract (`goal.md`) → ONE research wave (`researcher` + `scout` subagents, spawned together, barrier before synthesis) → codebase + project-reference analysis (scout if docs absent) → `planner` subagent writes `plan.md` + `phase-XX` files (Alternatives, Rationale, UI Layout, Test Specs) → parallelism pass (tag every phase PAR/SEQ + write set + `## Execution Waves`) → post-plan granularity self-check → mandatory final tasks.
- **The plan output itself carries parallelism metadata** — every phase tagged `PAR`/`SEQ` with the write set it owns, every `SEQ` naming its forcing dependency (see [Plan Parallelism Metadata](#plan-parallelism-metadata-mandatory--every-plan-output)). Omitting it is a defect of THIS skill: `$plan-execute` fans out only on what the plan declares.
- **`--mode={ci|cro}` routing:** `ci` plans a fix from a GitHub Actions run/log (loads `references/mode-ci.md`); `cro` plans conversion-rate optimization (25-item framework, `references/mode-cro.md`); default (no flag) = standard flow. Mode only ADDS a reference payload — SAME engine, SAME `$plan-review` gate, SAME `planner` agent.
- Default mode HARD (parallel subagents, project-reference docs, the `$plan-review` convergence loop under its 3-round ceiling); fast mode ONLY when EVERY trivial-task condition holds. Every phase passes the 5-point granularity check ("Can I start coding RIGHT NOW?"), carries `## Test Specifications` with TC IDs, uses bottom-up estimation (phase-hours drive man-days; SP DERIVED).
- **Mandatory final tasks + gates:** write Test Specs per phase → `$plan-validate` → `$plan-review` (convergence loop, 3-round ceiling) → `$why-review` (standalone) → re-estimate vs finalized phases; New Tech/Lib gate before approval; **Domain Entity Gate (MANDATORY when the plan touches an entity/VO/aggregate)** — apply `SYNC:domain-entity-change-gate` so the plan DECIDES classification, invariant ownership, aggregate boundary, concurrency, construction, events, and the test obligation (each naming its owning file) instead of deferring them to implementation; ask the user directly confirm before any next step.

**Workflow:**

1. **Pre-Check** — Detect active/suggested plan or create new directory
2. **Research wave** — All independent research threads spawned in ONE message (researcher + scout subagents, max 5 tool calls each), then a barrier before synthesis
3. **Codebase Analysis** — Search for project reference docs (patterns-reference, project-structure, architecture, adr); scout if not found
4. **Plan Creation** — Planner subagent creates plan.md + phase-XX files with full sections
5. **Parallelism pass** — Tag every phase PAR/SEQ with its write set; declare `## Execution Waves` in plan.md
6. **Post-Validation** — Optionally interview user to confirm decisions via $plan-validate

**Key Rules:**

- PLANNING ONLY: do NOT implement or execute code changes
- Always run $plan-review after plan creation
- Ask user to confirm before any next step
- **MANDATORY IMPORTANT MUST ATTENTION** detect new tech/lib in plan and create validation task (see New Tech/Lib Gate below)
- **MANDATORY IMPORTANT MUST ATTENTION** when the plan touches an entity, value object, or aggregate, run the **Domain Entity Gate** below — state paradigm + subdomain fit BEFORE any entity task, and answer every triggered decision row with its OWNING FILE; "discover during implementation" is not an answer. Record `No domain-entity surface — gate N/A` when it does not fire

## First Principle — Easy to Change

> **Success metric of every coding decision: _future change cost_.**
> DRY, SRP, abstraction, design patterns, naming, layering, tests — every
> technique serves one goal: **making next change cheaper**.

Evaluating code, refactor, test, abstraction, ask:
**does this make next change cheaper or more expensive?**

- Reject "best practices" raising change cost (premature abstraction,
  speculative generality, leaky indirection, ceremony without payoff).
- Name real enemies in findings: **coupling, hidden state, duplicated
  knowledge, unclear intent, irreversible decisions exposed too early**.
- Simpler design easy to change beats sophisticated design that isn't.

Apply this lens **before** invoking any rule, pattern, or checklist
below — if a downstream rule raises change cost, this principle wins.

---

## Default Mode Policy

> **Default mode HARD (full rigor).** Every section below — parallel researcher subagents, the full `$plan-review` convergence loop (3-round ceiling), base-class greps, microservices/event-driven analysis, mandatory user approval — applies by default.
>
> **Opt out to fast mode ONLY when ALL true** (task genuinely trivial):
>
> - Single-file edit, ≤30 lines changed
> - No design choice (only one reasonable approach)
> - No cross-service impact, no contract change, no new dependency
> - No new pattern — follows existing codebase pattern
> - User explicitly asked for a quick change
>
> **Any condition fails → use full protocol below.** When in doubt, default hard — skipping rigor on a non-trivial task wastes more rework than rigor saves.
>
> **Fast mode skips (and only skips):** parallel researcher subagents (direct grep instead), the `$plan-review` re-review loop (single round, no fresh re-review even when findings remain), `$plan-validate` interview (inline confirm only), New Tech/Lib Gate (only if truly no new deps).

## New Tech/Lib Gate (MANDATORY for all plans)

**MANDATORY IMPORTANT MUST ATTENTION** after plan creation, detect new tech/packages/libraries not in project. If found: task tracking per lib → WebSearch top 3 alternatives → compare (fit, size, community, learning curve, license) → recommend with confidence % → ask the user directly to confirm. **Skip if** plan uses only existing dependencies.

## Domain Entity Gate (MANDATORY when the plan touches an entity, VO, or aggregate)

> Apply `SYNC:domain-entity-change-gate` (inlined below) — the SAME protocol `$plan-review` and `$changes-review` read, and whose A–P checklist `$domain-entities-review` owns. — why: a plan that leaves aggregate boundary, invariant ownership, or concurrency to "discover during implementation" ships a design review will reject, and the rework is paid twice.

**Fires when** the plan introduces or changes a domain entity / value object / aggregate root, its fields, invariants, relationships, or state transitions; an aggregate boundary, repository, or cross-aggregate reference; a domain event; or a concurrency/reconstitution concern. Otherwise record `No domain-entity surface — gate N/A`.

**The plan MUST name the decision AND the owning file for every triggered row** — an unanswered row is a plan that is not executable:

1. **Classification** — entity vs value object vs aggregate root (swap test applied).
2. **Invariant ownership** — which rules the entity enforces vs which the boundary validates; failure signalling (throw vs `Result`) consistent with the project convention.
3. **Aggregate boundary + concurrency** — what shares a transaction and why; cross-aggregate refs by ID; concurrency token on the ROOT; enforcing mechanism for any set-based invariant.
4. **Construction vs reconstitution** — separate creation and load paths; load raises no events.
5. **Events** — what is raised, when it dispatches (after commit / outbox), domain vs integration contract.
6. **Test obligation** — each invariant gets a property TC + boundary counter-case as a planned task, NEVER left implicit.

MUST ATTENTION state **paradigm** (OO-mutable / type-driven-immutable / event-sourced) and **subdomain fit** (core / supporting / generic / CRUD) BEFORE planning entity tasks — NEVER plan a rich domain model for a CRUD subdomain, and NEVER plan setter/mutability tasks against an immutable or event-sourced model.

---

## Greenfield Mode

> **Auto-detected:** No existing codebase found (no discovered source directories, no manifest files, no populated `project-config.json`) → skill auto-switches to greenfield mode. Planning artifacts (docs/, plans/, .claude/) don't count — repository must have actual code directories with content.

**When greenfield detected:**

1. Skip codebase analysis phase (researcher subagents grepping code)
2. **Replace with:** market research + business evaluation via WebSearch + WebFetch
3. Delegate architecture decisions to `solution-architect` agent
4. Output: `plans/{id}/plan.md` with greenfield-specific phases (domain model, tech stack, project structure)
5. Skip reading project reference docs (won't exist in greenfield)
6. Enable broad web research: tech landscape, best practices, framework comparisons
7. Every decision point requires ask the user directly with 2-4 options + confidence %
8. **[CRITICAL] Business-First Protocol:** Tech stack decisions come AFTER full business analysis. Do NOT ask user to pick tech stack upfront. Instead: complete business evaluation → derive technical requirements → research current market options → produce comparison report → present to user. See `solution-architect` agent for full tech stack research methodology.

- Research reports <=150 lines; plan.md <=80 lines
- **External Memory:** Write all research/analysis to `.ai/workspace/analysis/{task-name}.analysis.md`. Re-read ENTIRE analysis file before generating plan.

Run the planning methodology engine. Load the relevant `references/engine-*.md` for each phase (skip a phase per its own skip rule):

- `references/engine-research.md` — Research & Analysis (skip if given researcher reports)
- `references/engine-figma.md` — Design Context Extraction (skip if no Figma URLs / backend-only)
- `references/engine-codebase-understanding.md` — Codebase Understanding (skip if given scout reports)
- `references/engine-solution-design.md` — Solution Design (trade-offs, security, performance, edge cases, architecture)
- `references/engine-plan-organization.md` — Plan Creation, Organization & Output Standards

## Mode Dispatch (`--mode={ci|cro}`)

> **Default (no `--mode` flag): IGNORE this section — run the standard plan flow below, byte-for-byte unchanged.** `--mode` only adds a domain-specific reference load + intake convention on top of the SAME engine, the SAME mandatory `$plan-review` gate, and the SAME `planner` agent. It never replaces the engine.

| Flag         | Positional `$ARGUMENTS`                               | Load before planning                                                             | Plan frontmatter overrides                |
| ------------ | ----------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------- |
| `--mode=ci`  | a GitHub Actions run/log URL                          | `references/mode-ci.md` (CI failure classes: build/test/env/Docker/dependencies) | `priority: P1`, `tags: [ci, bugfix]`      |
| `--mode=cro` | content/issues to optimize (optional screenshots/URL) | `references/mode-cro.md` (25-item CRO framework + multimodal intake)             | `priority: P2`, `tags: [cro, conversion]` |

When a `--mode` is present: (1) read the matching `references/mode-*.md`; (2) apply its intake + domain focus to `$ARGUMENTS`; (3) run the standard plan workflow below — same `planner` subagent, same phase-file structure, same mandatory `$plan-review`. The mode adds a reference payload only.

## Scaffolding-First Protocol (Conditional)

**Activation conditions (ALL must be true):**

1. Active workflow is `workflow-greenfield-init` OR `workflow-big-feature`
2. AI MUST ATTENTION self-investigate for existing base/foundational abstractions using these patterns:
    - Abstract/base classes: `abstract class.*Base|Base[A-Z]\w+|Abstract[A-Z]\w+`
    - Generic interfaces: `interface I\w+<|IGeneric|IBase`
    - Infrastructure abstractions: `IRepository|IUnitOfWork|IService|IHandler`
    - Utility/extension layers: `Extensions|Helpers|Utils|Common` (directories or classes)
    - Frontend foundations: `base.*component|base.*service|base.*store|abstract.*component` (if frontend present)
    - DI/IoC registration: search for DI registration patterns idiomatic to project's framework
3. If existing scaffolding found → **SKIP.** Log: "Existing scaffolding detected at {file:line}. Skipping Phase 1 scaffolding."
4. If NO foundational abstractions found → **PROCEED** with scaffolding phase.

**When activated:**

Phase 1 of plan MUST ATTENTION be **Architecture Scaffolding** — all base abstract classes, generic interfaces, infrastructure abstractions, DI registration with OOP/SOLID principles. Runs BEFORE feature stories. AI self-investigates what base classes the tech stack needs. All infrastructure behind interfaces with ≥1 concrete implementation (Dependency Inversion). Phase 1's deliverable MUST ATTENTION also include the **golden-path example set** `$scaffold` emits — one worked, compile-checked `*.example.*` per applicable pattern (backend: command · query · handler · entity-with-invariants · value-object · repository · domain event + event handler; frontend-if-UI: form · list · store · API service; tests: one integration test on happy + failure path) in an isolated, production-excluded `examples/` tree using the scaffolded base abstractions, so post-scaffold `$architecture-review-full` gate has real, gradeable code before any feature work.

**When skipped:** Plan proceeds normally — feature stories build on existing base classes.

## PLANNING-ONLY — Collaboration Required

> **DO NOT** use the manual plan-mode switching tool — already in a planning workflow.
> **DO NOT** implement or execute any code changes.
> **COLLABORATE** with user: ask decision questions, present options with recommendations.
> After plan creation, ALWAYS run `$plan-review` to validate plan.
> ASK user to confirm plan before any next step.

## Your mission

<task>
$ARGUMENTS
</task>

## Pre-Creation Check (Active vs Suggested Plan)

Check `## Plan Context` section in injected context:

- If "Plan:" shows a path → Active plan exists. Ask user: "Continue with this? [Y/n]"
- If "Suggested:" shows a path → Branch-matched hint only. Ask if user wants to activate or create new.
- If "Plan: none" → Create new plan using naming from `## Naming` section.

## Workflow

1. If creating new: create directory using `Plan dir:` from `## Naming` section, then run `node .claude/scripts/set-active-plan.cjs {plan-dir}`. If reusing: use active plan path from Plan Context. Pass directory path to every subagent.
2. **Goal Contract bootstrap (BEFORE investigation and phase writing):** resolve active goal per `SYNC:goal-contract-satisfaction-loop` — create/update `{plan-dir}/goal.md` from `.claude/templates/goal-contract-template.md`, recording original request, purpose, success criteria, constraints, required evidence. Every phase's success criteria maps to a saved goal criterion. Redact secrets.
3. Follow strictly the "Plan Creation & Organization" rules in `references/engine-plan-organization.md`.
4. **Project-reference preflight — BEFORE dispatch.** Resolve and read the required project-reference documents first. Record missing or stale references as scoped research inputs; never discover the governing conventions only after workers have already started.
5. **Research wave — ONE message, ONE barrier.** Enumerate the independent research threads this task needs — per-module code investigation, pattern discovery, dependency mapping, prior-art/library search — then tag each `PAR`/`SEQ` and declare `Parallel plan: wave 1 = [...] · SEQ = [...] (reason)` before dispatch. Research is read-only, so a thread is `PAR` unless it consumes another thread's output (name that output). Spawn the whole wave in ONE message: `researcher` agents (max 2) for external/prior-art threads, max 5 tool calls per agent; `scout` agents for codebase threads, one per module/area with a disjoint read scope. Give each agent its own report path under `{plan-dir}/research/` or `{plan-dir}/scout/` so no two agents write the same file.
6. Analyze codebase against the preflight references. **ONLY IF a required reference is missing or older than 3 days:** include a scoped `$scout <instructions>` member in the research wave to gather the missing evidence; do not launch an unplanned later round trip.
7. **Barrier, then synthesize.** Advance only after EVERY wave member returns (a skipped thread counts as returned). Read the report FILES (not memory), reconcile conflicting findings, and record unresolved gaps — a second wave is dispatched only for gaps the first wave exposed.
8. Main agent gathers research/scout report filepaths; pass to `planner` subagent with prompt to create implementation plan.
9. **Parallelism pass (MANDATORY before handoff).** Validate each phase's **Mode, Wave, write set, and SEQ dependency**, then write the `## Execution Waves` line — see [Plan Parallelism Metadata](#plan-parallelism-metadata-mandatory--every-plan-output). This is what lets `$plan-execute` fan out; an untagged plan executes strictly sequentially.
10. Main agent receives implementation plan from `planner`; ask user to review.

## Post-Plan Validation (Optional)

After plan creation, offer validation interview to confirm decisions before implementation.

**Check `## Plan Context` → `Validation: mode=X, questions=MIN-MAX`:**

| Mode     | Behavior                                                                        |
| -------- | ------------------------------------------------------------------------------- |
| `prompt` | Ask user: "Validate this plan with a brief interview?" → Yes (Recommended) / No |
| `auto`   | Automatically execute `$plan-validate {plan-path}`                              |
| `off`    | Skip validation step entirely                                                   |

**If mode is `prompt`:** Use ask the user directly tool with options above.
**If user chooses validation or mode is `auto`:** Execute `$plan-validate {plan-path}` SlashCommand.

## Output Requirements

**Plan Directory Structure** (use `Plan dir:` from `## Naming` section)

```
{plan-dir}/
├── research/
│   ├── researcher-XX-report.md
│   └── ...
├── reports/
│   ├── XX-report.md
│   └── ...
├── scout/
│   ├── scout-XX-report.md
│   └── ...
├── plan.md
├── phase-XX-phase-name-here.md
└── ...
```

**Research Output Requirements**

- Research markdown reports concise (<=150 lines); cover all topics + citations.

**Plan File Specification**

- Every `plan.md` MUST ATTENTION start with YAML frontmatter:

    ```yaml
    ---
    title: '{Brief title}'
    description: '{One sentence for card preview}'
    status: pending
    priority: P2
    effort: { sum of phases, e.g., 4h }
    story_points: { sum of phase SPs, e.g., 8 }
    man_days_traditional: '{ total e.g., 6d (4d code + 2d test) }'
    man_days_ai: '{ total with AI e.g., 3d (2d code + 1d test) }'
    branch: { current git branch }
    tags: [relevant, tags]
    created: { YYYY-MM-DD }
    ---
    ```

- Save overview at `{plan-dir}/plan.md` (<80 lines): list each phase with status, progress, **Mode (`PAR`/`SEQ`)**, links to phase files; add the `## Execution Waves` line below the phases table.
- For each phase, create `{plan-dir}/phase-XX-phase-name-here.md` with sections: Context links, Overview, Key Insights, Requirements, **Alternatives Considered** (minimum 2 approaches with pros/cons), **Design Rationale** (WHY chosen approach), Architecture, **UI Layout** (see below), Related code files, **Parallel Execution** (Mode `PAR`/`SEQ` · Write set · SEQ dependency — see below), Implementation Steps, Todo list, Success Criteria, Risk Assessment, Security Considerations, Next steps.
- **UI Layout:** For frontend-facing phases, include ASCII wireframe. Classify components by tier (common/domain-shared/page-app). For backend-only phases: `## UI Layout` → `N/A — Backend-only change.`

## Plan Parallelism Metadata (MANDATORY — every plan output)

`$plan-execute` fans out ONLY on what the plan declares. An untagged plan forces sequential execution, so omitting this metadata is a defect of THIS skill, not of the executor.

1. **Tag every phase `PAR` or `SEQ`** — in the `plan.md` phases table (`Mode` column) and in each phase file's `## Parallel Execution` section. `PAR` = its inputs contain no pending phase's output AND its write set is disjoint from every other `PAR` phase.
2. **Declare the write set per phase** — the exact file paths the phase creates / modifies / deletes (globs only when their members are enumerable from the plan). Two `PAR` phases MUST have disjoint write sets; any overlap → merge the phases, or demote the later one to `SEQ` and name the shared file.
3. **Every `SEQ` names its forcing dependency** — `SEQ — needs phase-02's {migration | generated type | contract | file}`. "Feels sequential", "safer in order", or an unnamed dependency is not a reason: retag it `PAR`.
4. **Group `PAR` phases into waves** in a `## Execution Waves` line in `plan.md`:
   `Execution waves: wave 1 = [phase-01, phase-03] · wave 2 = [phase-04] · SEQ = [phase-02 (needs phase-01 schema), phase-06 (approval gate)]`.
5. **Gates and reviews are SEQ boundaries** — a user-approval, review, verification, or migration phase never shares a wave with the phases it gates; it runs after that wave's barrier.
6. **Phase-file block format** (copy verbatim into each phase file):

    ```markdown
    ## Parallel Execution

    - Mode: PAR | SEQ
    - Write set: `src/a/x.ts`, `src/a/x.spec.ts`
    - Wave: 1
    - SEQ dependency: {name the phase + the exact artifact it produces — omit when Mode: PAR}
    ```

**Behavior/Sync Planning Checks**

- For behavior-changing work, every phase should name changed behavior, unchanged behavior to preserve, TC/test proof, and docs/spec sync action.
- For AI-extracted specs/TCs, plan must mark them reference-only until canonical acceptance.
- For `.claude` skills/hooks/workflows/sync tooling, plan must include generated mirror sync or explicit no-sync evidence.

## **IMPORTANT Task Planning Notes (MUST ATTENTION FOLLOW)**

- Always break work into many small todo tasks via task tracking
- Always add a final review todo task to verify work quality and identify fixes/enhancements
- **MANDATORY FINAL TASKS:** After all planning todos, ALWAYS add these final tasks:
    1. **Task: "Write test specifications for each phase"** — Add `## Test Specifications` with TC-{FEATURE}-{NNN} IDs to every phase file. Use `$spec [mode=tests]` if feature docs exist; `Evidence: TBD` for TDD-first mode.
    2. **Task: "Run $plan-validate"** — `$plan-validate` skill interviews user with critical questions, validates plan assumptions.
    3. **Task: "Run $plan-review"** — `$plan-review` skill, convergence loop (review → validate findings → fix → fresh full re-review) bounded by a **3-round ceiling, NEVER a target**: a clean pass ENDS the loop at ANY round, round 1 included; round 3 completing with CRITICAL/HIGH/MEDIUM still open escalates by asking the user directly, never a silent PASS. SP raises the RIGOR of each round, never a round floor: ≤3 → checklist + code-proof trace; 4-8 → + adversarial simulation; >8 → code-proof trace mandatory in every round.
    4. **Task: "Run $why-review (standalone only)"** — If NOT inside a workflow, `$why-review` validates design rationale, alternatives considered, risk assessment. Skip if a workflow already includes `$why-review`.
    5. **Task: "Re-evaluate estimation against finalized plan"** — Pre-completion estimates anchor on scope guesses; finalized phases reveal true cost. After phases/TCs/decisions locked: (a) re-derive `bottom_up_hours = Σ phase_hours` from finalized phase files; (b) recompute `likely_days`, `risk_margin_pct`, `min-max range` per `SYNC:estimation-framework`; (c) compare to current frontmatter `man_days_traditional` / `story_points`. If `|delta| > 20%` → UPDATE frontmatter, add `reestimate_delta_pct: <signed>` + 1-line `reestimate_reason`. If `|delta| > 50%` → flag `SHOULD-RESCOPE` and surface to user by asking the user directly before implementation.

## Important Notes

- Activate needed skills from catalog during process.
- Token efficiency without sacrificing quality. Sacrifice grammar for concision in reports.
- Unresolved questions → list at end of report.

---

## Standalone Review Gate (Non-Workflow Only)

> **MANDATORY IMPORTANT MUST ATTENTION:** If skill is called **outside a workflow** (standalone `$plan`), generated plan MUST ATTENTION include `$changes-review` as a **final phase/task** in plan. Ensures all implementation changes get reviewed before commit even without a workflow enforcing it.
>
> If already running inside a workflow (e.g., `workflow-feature`, `workflow-bugfix`), skip this — workflow sequence handles `$changes-review` at appropriate step.

## Next Steps (Standalone: MUST ATTENTION ask user by asking the user directly. Skip if inside workflow.)

**MANDATORY IMPORTANT MUST ATTENTION — NO EXCEPTIONS** after completing this skill, MUST ATTENTION use ask the user directly to present these options. Do NOT skip because task seems "simple" or "obvious" — user decides:

- **"Proceed with full workflow (Recommended)"** — Detect best workflow to continue (plan created). Ensures review, validation, implementation, testing not skipped.
- **"$why-review"** — Validate design rationale before implementation (standalone only — skipped when workflow includes it)
- **"$plan-review"** — Validate plan before implementation
- **"$plan-validate"** — Interview user to confirm plan decisions
- **"$plan-execute"** — Start coding & testing the finalized plan. Recommended implementation route after plan validated.
- **"Skip, continue manually"** — user decides

## Post-Plan Granularity Self-Check (MANDATORY)

After creating all phase files, run **recursive decomposition loop**:

1. Score each phase against 5-point criteria (file paths, no planning verbs, ≤30min steps, ≤5 files, no open decisions)
2. Each FAILING phase → create task to decompose into sub-plan (with own $plan → $plan-review → $plan-validate → fix cycle)
3. Re-score new phases. Repeat until ALL leaf phases pass (max depth: 3)
4. **Self-question:** "For each phase, can I start coding RIGHT NOW? If any needs 'figuring out' → sub-plan it."

## Preservation Inventory (MANDATORY for bugfixes)

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks for each file read. Prevents context loss from long files. For simple tasks, MUST ATTENTION ask user whether to skip.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
- `docs/specs/` — Test specifications by module (read existing TCs to include test strategy in plan)

> Each phase file MUST ATTENTION satisfy: <=5 files per phase, <=3h effort, clear success criteria, mapped test cases.

> **Evidence Gate:** MANDATORY IMPORTANT MUST ATTENTION — every claim, finding, recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

<!-- SYNC:plan-granularity -->

> **Plan Granularity** — Every phase must pass 5-point check before implementation:
>
> 1. Lists exact file paths to modify (not generic "implement X")
> 2. No planning verbs (research, investigate, analyze, determine, figure out)
> 3. Steps ≤30min each, phase total ≤3h
> 4. ≤5 files per phase
> 5. No open decisions or TBDs in approach
>
> **Failing phases →** create sub-plan. Repeat until ALL leaf phases pass (max depth: 3).
> **Self-question:** "Can I start coding RIGHT NOW? If any step needs 'figuring out' → sub-plan it."

<!-- /SYNC:plan-granularity -->

<!-- SYNC:preservation-inventory -->

> **Preservation Inventory** — MANDATORY for bugfix plans. Trigger keywords in plan title/frontmatter: `fix`, `bug`, `regression`, `broken`, `defect`. Author MUST produce this table BEFORE writing implementation steps.
>
> **Columns:** `Invariant | file:line | Why (data consequence if broken) | Verification (TC-ID or grep)`
>
> **BLOCKED until:** ≥3 rows · every File cell has `file:line` · every Verification cell has TC-ID or grep (not "manually verify")

<!-- /SYNC:preservation-inventory -->

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
> **Stop conditions:** confidence <80% on any critical decision → escalate by asking the user directly · ≥3 revisions on same thought → re-frame the problem · branch count >3 → split into sub-task.
>
> **Implicit mode:** apply methodology internally without visible markers when adding markers would clutter the response (routine work where reasoning aids accuracy).
>
> **Deep-dive:** see `$sequential-thinking` skill (`.claude/skills/sequential-thinking/SKILL.md`) for worked examples (API design, debugging, architecture), advanced techniques (spiral refinement, hypothesis testing, convergence), and meta-strategies (uncertainty handling, revision cascades).

<!-- /SYNC:sequential-thinking-protocol -->

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

<!-- SYNC:estimation-framework -->

> **Estimation Framework** — Bottom-up first; SP DERIVED; output min-max range when likely ≥3d. Stack-agnostic. Baseline: 3-5yr dev, 6 productive hrs/day. AI estimate assumes Claude Code + project context.
>
> **Method:**
>
> 1. **Blast Radius pass** (below) — drives code AND test cost
> 2. Decompose phases → hours/phase → `bottom_up_hours = Σ phase_hours`
> 3. `likely_days = ceil(bottom_up_hours / 6) × productivity_factor`
> 4. Sum **Risk Margin** (base + add-ons) → `max_days = likely_days × (1 + margin)`
> 5. `min_days = likely_days × 0.9`
> 6. Output as range when `likely_days ≥3`; single point allowed `<3` (still record margin)
> 7. `man_days_ai` = same range × AI speedup
> 8. `story_points` DERIVED from `likely_days` via SP-Days — NEVER driver. Disagreement >50% → trust bottom-up
>
> **Productivity factor:** 0.8 strong scaffolding+codegen+AI hooks · 1.0 mature default · 1.2 weak patterns · 1.5 greenfield
>
> **Cost Driver Heuristic (apply BEFORE work-type row):**
>
> - **UI dominates** in CRUD/business apps — 1.5-3x backend (states, validation, responsive, a11y, polish)
> - **Backend dominates ONLY:** multi-aggregate invariants, cross-service contracts, schema migrations, heavy query/perf, new event flows
>
> **Reuse-vs-Create axis (PRIMARY lever, per layer):**
>
> | UI tier                                      | Cost     |
> | -------------------------------------------- | -------- |
> | Reuse component on existing screen           | 0.1-0.3d |
> | Add control/column to existing screen        | 0.3-0.8d |
> | Compose components into NEW screen           | 1-2d     |
> | NEW screen, custom layout/states/validation  | 2-4d     |
> | NEW shared/common component (themed, tested) | 3-6d+    |
>
> | Backend tier                                         | Cost      |
> | ---------------------------------------------------- | --------- |
> | Reuse query/handler from new place                   | 0.1-0.3d  |
> | Small update existing handler/entity                 | 0.3-0.8d  |
> | NEW query on existing repo/model                     | 0.5-1d    |
> | NEW command/handler on existing aggregate (additive) | 1-2d      |
> | NEW aggregate/entity (repo, validation, events)      | 2-4d      |
> | NEW cross-service contract OR schema migration       | 2-4d each |
> | Multi-aggregate invariant / heavy domain rule        | 3-5d      |
>
> **Rule:** Sum tiers across UI+backend+tests, apply productivity factor. Reuse short-circuits tiers — call out.
>
> **Test-Scope drivers (compute test_count EXPLICITLY — "+tests" hand-wave is #1 failure):**
>
> | Driver                            | Count                                                  |
> | --------------------------------- | ------------------------------------------------------ |
> | Happy-path journeys               | 1 per story / AC main flow                             |
> | State-machine transitions         | reachable transitions × allowed actors                 |
> | Multi-entity state combos         | state(A) × state(B) — REACHABLE only, not Cartesian    |
> | Authorization matrix              | (owner, non-owner, elevated, unauth) × each mutation   |
> | Validation rules                  | 1 per required field / boundary / format / cross-field |
> | UI states (per new screen/dialog) | happy, loading, empty, error, partial — present only   |
> | Negative paths / invariants       | 1 per violatable business rule                         |
>
> | Test tier (Trad, incl. setup+assert+flake) | Cost     |
> | ------------------------------------------ | -------- |
> | 1-5 cases, fixtures reused                 | 0.3-0.5d |
> | 6-12 cases, 1 new fixture                  | 0.5-1d   |
> | 13-25 cases, multi-entity setup            | 1-2d     |
> | 26-50 cases OR new state-machine coverage  | 2-3d     |
> | >50 cases OR full E2E journey              | 3-5d     |
>
> **Test multipliers:** new fixture/seed harness +0.5d · cross-service/bus assertion +0.3d each · UI E2E ×1.5 · each new role +1-2 cases
>
> **Blast Radius (mandatory pre-pass — affects code AND test):**
>
> 1. Files/components directly modified — count
> 2. Of those, "complex" (>500 LOC, multi-handler, central, frequently-modified) — count
> 3. Downstream consumers (callers, event subscribers, cross-service) — list
> 4. Shared/common code touched (multi-app blast) — yes/no
> 5. Regression scope — areas needing re-test
>
> **Rule:** Complex touch → add `risk_factors`. Each downstream consumer → +1-3 regression cases. Blast >5 areas OR >2 complex → re-evaluate SPLIT before estimating.
>
> **Risk Margin (drives max bound):**
>
> | likely_days         | Base margin                     |
> | ------------------- | ------------------------------- |
> | <1d trivial         | +10%                            |
> | 1-2d small additive | +20%                            |
> | 3-4d real feature   | +35%                            |
> | 5-7d large          | +50%                            |
> | 8-10d very large    | +75%                            |
> | >10d                | +100% AND **flag SHOULD SPLIT** |
>
> **Risk-factor add-ons (additive — enumerate in `risk_factors`):**
>
> | Factor                                                                | +margin |
> | --------------------------------------------------------------------- | ------- |
> | `touches-complex-existing-feature` (>500 LOC, multi-handler, central) | +20%    |
> | `cross-service-contract` change                                       | +25%    |
> | `schema-migration-on-populated-data`                                  | +25%    |
> | `new-tech-or-unfamiliar-pattern`                                      | +30%    |
> | `regression-fan-out` (≥3 downstream areas re-test)                    | +20%    |
> | `performance-or-latency-critical`                                     | +20%    |
> | `concurrency-race-event-ordering`                                     | +25%    |
> | `shared-common-code` (multi-consumer/multi-app)                       | +25%    |
> | `unclear-requirements-or-design`                                      | +30%    |
>
> **Collapse rule:** total margin >100% → STOP, split (padding past 2x is dishonesty). Margin <15% on `likely_days ≥5` → under-estimated, widen.
>
> **Work-Type Caps (hard ceilings on `likely_days`):**
> | Work type | Max SP | Max likely |
> | --- | --- | --- |
> | Single field / config flag / style fix | 1 | 0.5d |
> | Add property to existing model + bind to existing UI | 2 | 1d |
> | **Additive endpoint + minor UI control** (button/menu/column), reuses fixtures | **3** | **2-3d** |
> | Additive endpoint + **NEW UI surface** OR additive multi-layer + new domain rule + 2+ test files | 5 | 3-5d |
> | NEW model/aggregate OR migration OR cross-module contract OR heavy test (>1.5d) OR NEW UI + non-trivial backend | 8 | 5-7d |
> | NEW UI surface + (NEW aggregate OR migration OR cross-service contract) | 13 | SHOULD split |
> | Cross-service contract + migration combined | 13 | SHOULD split |
> | Beyond | 21 | MUST split |
>
> **SP→Days (validation only):** 1=0.5d/0.25d · 2=1d/0.35d · 3=2d/0.65d · 5=4d/1.0d · 8=6d/1.5d · 13=10d/2.0d (Trad/AI likely)
> **AI speedup:** SP 1≈2x · 2-3≈3x · 5-8≈4x · 13+≈5x. AI cost = `(code_gen × 1.3) + (test_gen × 1.3)` (30% review overhead).
>
> **MANDATORY frontmatter:**
>
> ```yaml
> story_points: <n>
> complexity: low | medium | high | critical
> man_days_traditional: '<min>-<max>d' # range when likely ≥3d; '<N>d' when <3d
> man_days_ai: '<min>-<max>d'
> risk_margin_pct: <n> # base + add-ons
> risk_factors: [touches-complex-existing-feature, regression-fan-out] # closed-list from add-ons; [] if none
> blast_radius:
>     touched_areas: <n>
>     complex_touched: <n>
>     downstream_consumers: [list or count]
>     shared_common_code: yes | no
> estimate_scope_included: [code, integration-tests, frontend, i18n, docs]
> estimate_scope_excluded: [unit-tests, e2e, perf, deployment, code-review-rounds]
> estimate_reasoning: |
>     5-7 lines covering:
>     (a) UI tier — row applied
>     (b) Backend tier — row applied
>     (c) Test scope — case breakdown by driver, file count, fixtures, tier row
>     (d) Cost driver — dominant tier + why
>     (e) Blast radius — touched, complex, regression scope
>     (f) Risk factors — list driving margin; why not larger/smaller
>     Example: "UI: compose Form/Table/Dialog → NEW screen (~1.5d). Backend: NEW command on existing aggregate,
>     reuses validation+repo (~1d). Tests: 4 transitions × 2 actors + 3 validation + 2 UI states = 13 cases,
>     1 new fixture → tier 13-25 ~1.5d. Driver: UI composition + new states. Blast: 4 areas, 1 complex.
>     Risk: base 35% + touches-complex +20% = 55% → max 3.9d → range 2.5-4d."
> ```
>
> **Sanity self-check:**
>
> - `likely_days ≥3d` and single-point? → reject, must be range
> - Margin <15% on `likely_days ≥5d`? → under-estimated, widen
> - Margin >100%? → STOP, split instead of buffer
> - Complex existing feature touched, no regression budget in `(c)`? → reject
> - Blast `>5` areas OR `>2` complex, no split discussion? → reject
> - Purely additive on existing model AND existing UI? → cap SP 3 unless tests >1.5d
> - NEW UI surface (page/complex form/dashboard)? → SP 5+ even if backend one endpoint
> - Backend cross-service / migration / multi-aggregate? → SP 8+ regardless of UI
> - `bottom_up_hours / 6` vs SP-Days disagreement >50%? → trust bottom-up, downgrade SP
> - Without tests, SP drops ≥1 bucket? → tests dominate; state explicitly
> - Reasoning called out UI vs backend vs blast vs risk factors? → if missing, add

<!-- /SYNC:estimation-framework -->

<!-- SYNC:plan-quality -->

> **Plan Quality** — Every plan phase MUST ATTENTION include test specifications.
>
> 1. Add `## Test Specifications` section with TC-{FEATURE}-{NNN} IDs to every phase file
> 2. Map every functional requirement to ≥1 TC (or explicit `TBD` with rationale)
> 3. TC IDs follow `TC-{FEATURE}-{NNN}` format — reference by ID, never embed full content
> 4. Before any new workflow step: call the current task list and re-read the phase file
> 5. On context compaction: call the current task list FIRST — never create duplicate tasks
> 6. Verify TC satisfaction per phase before marking complete (evidence must be `file:line`, not TBD)
>
> **Mode:** TDD-first → reference existing TCs with `Evidence: TBD`. Implement-first → use TBD → `$spec [mode=tests]` fills after.

<!-- /SYNC:plan-quality -->

<!-- SYNC:iterative-phase-quality -->

> **Iterative Phase Quality** — Score complexity BEFORE planning.
>
> **Complexity signals:** >5 files +2, cross-service +3, new pattern +2, DB migration +2
> **Score >=6 →** MUST ATTENTION decompose into phases. Each phase:
>
> - ≤5 files modified
> - ≤3h effort
> - Follows cycle: plan → implement → review → fix → verify
> - Start Phase N+1 only after Phase N passes VERIFY — why: building on an unverified phase compounds errors downstream
>
> **Phase success = all TCs pass + code-reviewer agent approves + no CRITICAL findings.**

<!-- /SYNC:iterative-phase-quality -->

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

<!-- SYNC:domain-entity-change-gate -->

> **Domain Entity Change Gate** — ONE protocol binding every skill or agent that PLANS, IMPLEMENTS, or REVIEWS a change touching a domain entity, value object, or aggregate, so a planner, an implementer, and a reviewer apply the SAME rules to the SAME change. `$domain-entities-review` is the canonical owner of the full A–P checklist; this gate is the shared trigger plus the decision set that must be answered. NEVER re-derive a weaker local copy — why: when planning and review disagree on entity rules, the plan ships a design that review then rejects, and the rework is paid twice.
>
> **Trigger — fires when ANY holds:** a new entity / value object / aggregate root is introduced · an existing one gains or loses a field, invariant, relationship, or state transition · an aggregate boundary, repository, or cross-aggregate reference changes · a domain event is added, renamed, or re-payloaded · a concurrency or reconstitution concern on a root changes. State `No domain-entity surface — gate N/A` when none holds.
>
> **Step 1 — Detect BEFORE deciding.** Both answers change which rules even apply:
>
> - **Paradigm** (per aggregate, from the code — NEVER assumed): OO-mutable · type-driven/immutable · event-sourced. Setter, mutability, and reconstitution rules are written for OO-mutable; applying them to the other two manufactures false findings and false plan tasks.
> - **Subdomain fit:** core (rich model owed) · supporting (Active Record or light model) · generic (buy, do not model) · CRUD (Transaction Script — a rich entity here is ceremony). NEVER plan or flag a rich model where the subdomain has no invariant beyond required-field.
>
> **Step 2 — Answer all 6 decision points.** Each is a decision the change MUST make explicitly:
>
> | #   | Decision point                                                                                               | Answered when                                                                                                                                                                                                                                                                                |
> | --- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | 1   | **Classification** — entity vs value object vs aggregate root                                                | The swap test is applied ("would an identical copy be interchangeable?"); a VO is immutable with structural equality and has no repository                                                                                                                                                   |
> | 2   | **Invariant ownership** — entity owns "can this state exist?", the boundary owns "is this input acceptable?" | Each rule is placed on one side and named; failure signalling (throw vs `Result`) matches the project convention consistently; a DB constraint is a backstop, NEVER the rule                                                                                                                 |
> | 3   | **Aggregate boundary + concurrency**                                                                         | Only true always-consistent invariants share an aggregate; cross-aggregate references are by ID; one aggregate mutates per transaction; the ROOT carries the concurrency token; set-based invariants (uniqueness across instances) name a real enforcing mechanism, never an in-memory check |
> | 4   | **Construction vs reconstitution**                                                                           | Creation and load are separate paths; the load path raises NO domain events and re-runs NO creation rules; required data sits in the constructor/factory                                                                                                                                     |
> | 5   | **Events**                                                                                                   | Raised inside the aggregate; dispatched AFTER commit (outbox when crossing a process); internal domain events kept distinct from published integration contracts; handlers idempotent                                                                                                        |
> | 6   | **Test obligation**                                                                                          | Every invariant maps to a universally-quantified property TC PLUS a boundary counter-case — the spec NAMES it and a test GUARDS it (Dual-Feedback); a single happy-path example is NOT coverage                                                                                              |
>
> **Step 3 — Apply by context.** Same decisions, different obligation:
>
> | Calling context                                                                                     | Obligation                                                                                                                                                                                                                                                                                                                                                                                                                |
> | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | **Planning** (`$plan`)                                                                              | The plan MUST name the decision and the owning file for every triggered row. An unanswered row is a plan that is not executable — surface it, do NOT let implementation discover it.                                                                                                                                                                                                                                      |
> | **Plan review** (`$plan-review`)                                                                    | An unanswered, hand-waved, or deferred-to-implementation row is a FINDING with `file:line` into the plan. Presence of the word "entity" is NEVER an answer.                                                                                                                                                                                                                                                               |
> | **Implementation** (`$plan-execute`, `$fix`, and any implementing agent — e.g. `backend-developer`) | The decisions are INPUTS, not questions to reopen: implement each triggered row as the plan/spec decided it, at the owning file it named. A row that arrives UNANSWERED is a blocker — surface it and get it decided; NEVER settle it silently at the keyboard, and NEVER pick an aggregate boundary from a DB table or UI screen because the plan left it open. Paradigm and subdomain fit still gate which rules apply. |
> | **Change review** (`$changes-review`)                                                               | Route to the owner — **Mode A (default):** read `$domain-entities-review`'s Phase 2 A–P checklist and apply it as review lenses. **Mode B (escalation):** delegate to `$domain-entities-review` when standalone AND the diff carries 3+ entity files. Findings enter the normal finding set with `file:line` + severity.                                                                                                  |
>
> **Duplication guard — SKIP the gate entirely when ANY row holds.** Record the deferral line, then proceed:
>
> | Suppressing context                                                                                                              | Deferral line                                                   |
> | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
> | The running skill IS `$domain-entities-review`                                                                                   | `Gate is this skill's own body — A–P checklist owns it.`        |
> | Invoked inside `$workflow-review-changes` (its step 5 runs `$domain-entities-review` as a dedicated conditional parallel member) | `Gate deferred to workflow step 5 $domain-entities-review.`     |
> | `$why-review` running in `--validate-findings` terminal mode                                                                     | `Gate N/A — validate-findings is terminal, no sub-skill calls.` |
>
> — why: unguarded, this edge duplicates a review the parent workflow already runs and closes a `changes-review → domain-entities-review → why-review → changes-review` cycle.
>
> **BLOCKED until:** trigger evaluated (or `gate N/A` recorded) · paradigm + subdomain fit stated · all 6 triggered decision points answered or raised as findings · guard row checked before any delegation.

<!-- /SYNC:domain-entity-change-gate -->

<!-- SYNC:domain-entity-change-gate:reminder -->

**MUST ATTENTION** when the change PLANS or REVIEWS a new/updated domain entity, value object, or aggregate, apply the **Domain Entity Change Gate** — `$domain-entities-review` owns the full A–P checklist; detect paradigm + subdomain fit FIRST, then answer all 6 decision points (classification · invariant ownership + failure signalling · aggregate boundary + concurrency · construction vs reconstitution · events · property-TC test obligation). Planning must NAME each decision; plan review treats an unanswered row as a FINDING; change review routes to the owner (Mode A read / Mode B delegate). SKIP under the 3-row duplication guard and record the deferral line. — why: one protocol shared by planner and reviewer is what stops a plan shipping an entity design that review then rejects.

<!-- /SYNC:domain-entity-change-gate:reminder -->

<!-- SYNC:estimation-framework:reminder -->

- **MANDATORY MUST ATTENTION** estimation: bottom-up phase hours drive `man_days_traditional` (`Σh/6 × productivity_factor`); SP DERIVED. UI cost usually dominates — bump SP one bucket if NEW UI surface (page/complex form/dashboard). Frontmatter MUST include `story_points`, `complexity`, `man_days_traditional`, `man_days_ai`, `estimate_scope_included`, `estimate_scope_excluded`, `estimate_reasoning` (UI vs backend cost driver). Cap SP 3 for additive-on-existing-model+existing-UI unless test scope >1.5d. SP 13 SHOULD split, SP 21 MUST split.
  <!-- /SYNC:estimation-framework:reminder -->

<!-- SYNC:plan-quality:reminder -->

**IMPORTANT MUST ATTENTION** include `## Test Specifications` with TC IDs per phase. Call the current task list before creating new tasks.

<!-- /SYNC:plan-quality:reminder -->

<!-- SYNC:plan-granularity:reminder -->

**IMPORTANT MUST ATTENTION** verify all phases pass 5-point granularity check. Failing phases → sub-plan. "Can I start coding RIGHT NOW?"

<!-- /SYNC:plan-granularity:reminder -->

<!-- SYNC:understand-code-first:reminder -->

**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read code BEFORE any modification. Run graph trace when graph.db exists.

<!-- /SYNC:understand-code-first:reminder -->

<!-- SYNC:evidence-based-reasoning:reminder -->

- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim. Confidence >80% to act, <60% = do NOT recommend.
  <!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:iterative-phase-quality:reminder -->

**IMPORTANT MUST ATTENTION** score complexity first. Score >=6 → decompose. Each phase: plan → implement → review → fix → verify. No skipping.

<!-- /SYNC:iterative-phase-quality:reminder -->

<!-- SYNC:fix-layer-accountability:reminder -->

**IMPORTANT MUST ATTENTION** trace full data flow and fix at the owning layer, not the crash site. Audit all access sites before adding `?.`.

<!-- /SYNC:fix-layer-accountability:reminder -->

<!-- SYNC:cross-service-check:reminder -->

**IMPORTANT MUST ATTENTION** microservices/event-driven: scan producers, consumers, sagas, contracts in task scope. Per touchpoint: owner · message · consumers · risk (NONE/ADDITIVE/BREAKING). Missing consumer = silent regression.

<!-- /SYNC:cross-service-check:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:sequential-thinking-protocol:reminder -->

**MUST ATTENTION** apply sequential-thinking — multi-step Thought N/M, REVISION/BRANCH/HYPOTHESIS markers, confidence % closer; see `$sequential-thinking` skill.

<!-- /SYNC:sequential-thinking-protocol:reminder -->

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

<!-- SYNC:nested-task-creation:reminder -->

- **MANDATORY** Parent workflow rows do not replace child phase tracking; expand phases and link the parent when nested.
- **MANDATORY** Orchestrators pre-expand child skill phases before invocation; use `[N.M] $skill-name — phase` prefixes and one-`in_progress` discipline.

<!-- /SYNC:nested-task-creation:reminder -->

<!-- SYNC:goal-contract-satisfaction-loop:reminder -->

- **MANDATORY** Resolve the active Goal Contract BEFORE work (active plan `goal.md` → `plans/goals/{YYMMDD-HHmm}-{slug}/goal.md` → create from current request) and read saved success criteria before editing.
- **MANDATORY** Append iteration evidence after execution; emit a Goal Satisfaction matrix (PASS/FAIL/BLOCKED) before reporting PASS; loop on validated FAIL; escalate repeated no-progress or blockers. NEVER store secrets in goal files.

<!-- /SYNC:goal-contract-satisfaction-loop:reminder -->

<!-- SYNC:parallel-subagent-dispatch -->

> **Parallel Sub-Agent Dispatch** — Plan parallelism the moment a task breakdown exists, BEFORE executing it — running provably independent tasks sequentially wastes wall-clock. Applies to every multi-step job: workflow steps, planning, batch updates, investigation, research, scans, reviews, doc sync. **Plan execution is metadata-gated, NEVER default-parallel** — fan-out follows ONLY what the plan declares (`PAR`/`SEQ` tags + per-phase write set); an untagged plan runs sequentially — why: a derived write set cannot see cascade or generated writes.
>
> 1. **Tag every task `PAR` or `SEQ`.** `PAR` = inputs exclude every pending task's output AND write set disjoint from every other `PAR`. Else `SEQ` — MUST ATTENTION name the dependency forcing it.
> 2. **Group `PAR` into waves.** No edge between members. Two writers of one file NEVER share a wave. Read-only work (search, investigation, review, research) parallelizes freely.
> 3. **Declare before dispatch:** `Parallel plan: wave 1 = [...] · wave 2 = [...] · SEQ = [...] (reason)`.
> 4. **Spawn each wave in ONE message** — every `spawn_agent` call in one response, NEVER dripped per turn. Route each task to its specialist (`.claude/skills/shared/sub-agent-selection-guide.md`); NEVER `code-reviewer` as catch-all.
> 5. **Brief each sub-agent self-contained:** goal · scope + owned files · reference docs · return contract (summary + `Full report:` path, per SYNC:subagent-return-contract) · incremental persistence to `plans/reports/` (per SYNC:incremental-persistence).
> 6. **Barrier per wave.** Advance ONLY after EVERY member returns (a skipped conditional counts as returned). Merge, mark each task completed/skipped, THEN dispatch the next wave. Mutating steps wait for the barrier.
> 7. **One level deep.** A dispatched sub-agent executes its own brief; further fan-out stays the orchestrator's job unless that agent's `.claude/agents/*.md` definition authorizes it.
>
> **NEVER parallelize:** tasks sharing a write target · a task consuming a pending task's output · trivial single-file work (dispatch overhead > gain) · an order a skill or workflow explicitly fixes · gates awaiting user approval.
>
> **Blocked until:** MUST ATTENTION every task tagged PAR/SEQ with a named reason per SEQ · waves declared + write-set disjointness checked · each wave spawned in ONE message · barrier honored before the next wave.

<!-- /SYNC:parallel-subagent-dispatch -->

<!-- SYNC:parallel-subagent-dispatch:reminder -->

- **MANDATORY** After planning tasks, tag each PAR/SEQ and spawn every PAR wave as parallel sub-agents in ONE message — default parallel for workflows, batch updates, investigation, research, reviews; plan execution fans out ONLY on what the plan declares.
- **MANDATORY** Disjoint write sets per wave · all-return barrier before the next wave · specialist routing · sub-agents NEVER fan out further unless their own agent definition authorizes it.

<!-- /SYNC:parallel-subagent-dispatch:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** deliver a validated, implementation-ready plan — every phase startable immediately (exact file paths, zero open decisions, mapped TC IDs) — so coding runs without rework at minimum future change cost.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Plan Granularity:** every phase passes the 5-point check or sub-plans.
- **Preservation Inventory:** bugfix plans tabulate invariants with `file:line` + verification.
- **Nested Task Creation:** child skills expand visible phase tasks; link parent when nested.
- **Project Reference Docs Guide:** ALWAYS read required project docs before target work.
- **Task Tracking & External Report:** bootstrap tasks; persist findings to `plans/reports/`.
- **Critical Thinking:** every claim needs traced proof; confidence >80% to act.
- **Sequential Thinking:** multi-step Thought N/M with REVISION/BRANCH/HYPOTHESIS markers.
- **Understand Code First:** read code + grep 3+ patterns before planning.
- **Cross-Service Check:** scan producers, consumers, sagas, contracts for breaking risk.
- **Estimation Framework:** bottom-up phase hours drive man-days; SP DERIVED.
- **Plan Quality:** every phase carries `## Test Specifications` with TC IDs.
- **Iterative Phase Quality:** score complexity first; decompose at score ≥6.
- **Fix-Layer Accountability:** NEVER fix at the crash site; fix the invariant owner.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**IMPORTANT MUST ATTENTION** PLANNING ONLY — NEVER implement or execute code; produce `plan.md` + per-phase files + `goal.md` Goal Contract, then hand off — why: this skill's contract is a plan, not a change.
**IMPORTANT MUST ATTENTION** default mode HARD — opt out to fast mode ONLY when ALL trivial-task conditions hold — why: skipping rigor on a non-trivial task costs more rework than rigor saves.
**MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks via task tracking BEFORE starting; add a final review todo; on context loss call the current task list first — never duplicate tasks.
**MANDATORY IMPORTANT MUST ATTENTION** bootstrap the Goal Contract (`goal.md` from `goal-contract-template.md`) BEFORE investigation; every phase success criterion maps to a saved goal criterion. Redact secrets.
**MANDATORY IMPORTANT MUST ATTENTION** validate decisions with user by asking the user directly — NEVER auto-decide because a task seems "obvious"; the user decides the next step.
**MANDATORY IMPORTANT MUST ATTENTION** every phase passes the 5-point granularity check ("Can I start coding RIGHT NOW?") — failing phases → sub-plan (max depth 3).
**MANDATORY IMPORTANT MUST ATTENTION** detect new tech/lib not in project → task tracking per lib → WebSearch top 3 → compare → recommend with confidence % → ask the user directly — why: an unvetted dependency is an irreversible decision exposed too early.
**MANDATORY IMPORTANT MUST ATTENTION** estimation is bottom-up — phase hours drive `man_days_traditional` (`Σh/6 × productivity_factor`); SP DERIVED, never the driver; UI cost usually dominates; emit full `estimate_reasoning` frontmatter.
**MANDATORY IMPORTANT MUST ATTENTION** every phase carries `## Test Specifications` with `TC-{FEATURE}-{NNN}` IDs; map every functional requirement to ≥1 TC (or explicit `Evidence: TBD` for TDD-first).
**MANDATORY IMPORTANT MUST ATTENTION** for `.claude` skills/hooks/workflows/sync work, plans MUST include generated-mirror sync action or explicit no-sync evidence — why: a silently stale mirror diverges from source.
**MANDATORY IMPORTANT MUST ATTENTION** NEVER skip `$plan-review` after plan creation — run it standalone or as the workflow step; standalone `$plan` also appends `$changes-review` as a final task.
**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read target code BEFORE planning; cite `file:line`; run graph trace when `.code-graph/graph.db` exists — why: local conventions override generic framework defaults.
**MANDATORY IMPORTANT MUST ATTENTION** run the full main pipeline in order — pre-check plan → bootstrap `goal.md` → ONE research wave (`researcher` + `scout` in one message) → barrier → codebase + project-reference analysis (scout if docs absent) → `planner` writes `plan.md` + `phase-XX` → parallelism pass (PAR/SEQ + write sets + `## Execution Waves`) → granularity self-check → mandatory final tasks; NEVER skip a step because it seems obvious — why: the skipped step (Goal Contract, granularity, test specs) is the one AI silently drops.
**MANDATORY IMPORTANT MUST ATTENTION** dispatch the research threads as ONE wave in ONE message (declare `Parallel plan:` first, one report path per agent) and synthesize only after EVERY member returns — why: dripping researchers one per turn serializes the cheapest-to-parallelize half of planning.
**MANDATORY IMPORTANT MUST ATTENTION** the emitted plan MUST carry parallelism metadata — every phase tagged `PAR`/`SEQ`, its write set declared, every `SEQ` naming the exact artifact it waits on, and `## Execution Waves` in `plan.md` — why: `$plan-execute` fans out only on what the plan declares, so an untagged plan silently forces sequential execution.
**MANDATORY IMPORTANT MUST ATTENTION** queue the final-task block on EVERY plan — Test Specs per phase → `$plan-validate` → `$plan-review` (convergence loop, 3-round ceiling — a clean pass ends it at any round) → `$why-review` (standalone only) → re-estimate vs finalized phases (flag `SHOULD-RESCOPE` when delta >50%).
**IMPORTANT MUST ATTENTION** `--mode={ci|cro}` only ADDS a domain reference load (`references/mode-ci.md` / `mode-cro.md`) + intake on top of the SAME engine, gate, and `planner` agent — default (no flag) runs the standard flow byte-for-byte; NEVER let a mode replace the engine or skip `$plan-review`.

**Anti-Rationalization:**

| Evasion                                 | Rebuttal                                                                                                                |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| "Task too simple to plan"               | Default mode HARD. Opt out ONLY when ALL trivial conditions hold.                                                       |
| "I already know the codebase"           | Show `file:line` from 3+ patterns + graph trace. No proof = not read.                                                   |
| "Phase is clear enough"                 | Run the 5-point granularity check: "Can I start coding RIGHT NOW?" — else sub-plan.                                     |
| "Plan looks good, skip review"          | NEVER skip `$plan-review` — fresh eyes catch author blind spots.                                                        |
| "Only existing libs, skip the gate"     | Prove it — grep manifests. Any new tech/lib → WebSearch + ask the user directly before approval.                        |
| "I'll just estimate SP directly"        | SP is DERIVED from bottom-up phase hours, never the driver. Σh/6 × productivity first.                                  |
| "It's a `.claude` change, no sync"      | State the mirror action or explicit no-sync evidence — stale mirrors fail the oracle.                                   |
| "`--mode=ci`, so skip the normal flow"  | Mode only ADDS a reference payload — same engine, same `$plan-review`, same `planner` agent.                            |
| "Plan's done, skip the final tasks"     | Test Specs → `$plan-validate` → `$plan-review` → `$why-review` → re-estimate are MANDATORY, not optional.               |
| "Phases feel sequential, skip the tags" | "Feels sequential" is not a dependency. Tag `PAR`/`SEQ`, declare write sets, and name the artifact each `SEQ` waits on. |
| "The executor can work the order out"   | It can't — `$plan-execute` fans out only on declared write sets. No tags = sequential execution you caused.             |

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break into small todo tasks and sub-tasks via task tracking.

**IMPORTANT MUST ATTENTION** PLANNING ONLY — never implement; cite `file:line` evidence (confidence >80% to act); NEVER skip `$plan-review` and the New Tech/Lib + Goal-Contract gates.

---

> **Closing reminder — Easy to Change is the success metric.** Every finding,
> test, refactor, and abstraction must answer one question: _does this make
> the next change cheaper or more expensive?_ If it doesn't reduce future
> change cost, reject it. Coupling, hidden state, duplicated knowledge, and
> unclear intent are the real enemies — call them out by name.

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
