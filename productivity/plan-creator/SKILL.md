---
name: mk:plan-creator
version: 1.6.3
preamble-tier: 3
description: 'Creates structured multi-file implementation plans before build. Scope-aware: trivial tasks exit early, simple tasks get fast plans, complex tasks get full research + phase files + validation. Enforces Gate 1. Activated by /mk:plan or /mk:cook. NOT for ticket complexity analysis against an existing codebase (see mk:planning-engine); NOT for CEO-level scope review of existing plans (see mk:plan-ceo-review).'
argument-hint: '[task description] [--fast | --hard | --deep | --parallel | --two | --product-level [--no-design] [--no-scout] | --spike --timebox <duration>] [--tdd] [--html] [--advice] OR [archive | red-team {path} | validate {path}]'
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
source: local
keywords:
  - plan-creator
  - implementation-plan
  - phase-files
  - gate-1
  - scope-adaptive
  - design-evidence
when_to_use: Use when creating a structured multi-file implementation plan before build, including plans that consume a design evidence packet (e.g. from mk:figma) without re-analyzing the design source. NOT for ticket analysis (see mk:planning-engine) or scope review (see mk:plan-ceo-review).
user-invocable: true
meowkit:
  portability: provider-only
  providers:
    include:
      - claude-code
  requires:
    surfaces:
      - skills
    commands:
      - Agent
      - AskUserQuestion
      - Bash
  context_cost: high
owner: lifecycle
criticality: critical
status: active
runtime: claude-code
context_cost: high
dependency_edges:
  - id: mk:agent-detector
    type: peer
  - id: mk:autobuild
    type: peer
  - id: mk:brainstorming
    type: peer
  - id: mk:cook
    type: peer
  - id: mk:figma
    type: peer
  - id: mk:fix
    type: peer
  - id: mk:scale-routing
    type: peer
  - id: mk:scout
    type: peer
  - id: mk:validate-plan
    type: peer
  - id: mk:visual-plan
    type: peer
---

# Plan Creator

Public surface: classify → inspect → capture missing decisions → draft → validate → Gate 1. Produces plan.md overview + phase-XX detail files; execution, existing-plan audits, visual rendering, archive, and durable-memory capture stay with their existing owners.

## When to Use

Activate when:

- User runs `/mk:plan [task]` or `/mk:cook [task]`
- Non-trivial task (> 2 files OR > 1h OR architectural decisions)
- User supplies ≥2 upstream reports/specs (office-hours, brainstorming, planning-engine, confluence-spec, intake output…) → step-00.5 consolidates them into a Plan Intake Packet before planning (see `references/plan-intake-packet.md`)
- User supplies a design evidence packet (e.g. from `mk:figma`) → plan consumes it (viewport/state ACs, critical-action validation matrix, phase `blocked_on:` for high-risk flow ambiguity), never re-analyzes the design source (see `references/design-evidence-consumption.md`)
- Gate 1 requires a plan before Phase 3
- Green-field product build ("build a kanban app", "create a SaaS dashboard", "make a retro game maker") → step-00 auto-detects and offers `--product-level`
- Existing-plan audit → `mk:validate-plan`; archive → lifecycle CLI; visual rendering → `mk:visual-plan`.
- Hard/deep plan creation still runs its built-in red-team and validation interview before Gate 1. These are design-quality gates, not standalone subcommands, and must never be routed away.
- Compatibility aliases: `/mk:plan archive` → [archive workflow](references/archive-workflow.md); `/mk:plan red-team {path}` → [standalone red-team workflow](references/red-team-standalone.md); `/mk:plan validate {path}` → [standalone validation workflow](references/validate-standalone.md).

Standalone aliases route to their compatibility references; they do not replace hard/deep red-team or validation. `--html` routes to `mk:visual-plan`.

Skip when:

- `/mk:fix` with complexity=simple (Gate 1 exception)
- `mk:scale-routing` returns workflow=one-shot + zero blast radius

## Arguments

| Flag              | Mode                     | Research                | Phase Files                                                                                   | Validation                                                                   |
| ----------------- | ------------------------ | ----------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| (default)         | Auto-detect from scope   | Follows mode            | Follows mode                                                                                  | Follows mode                                                                 |
| `--fast`          | Fast                     | Skip                    | plan.md only                                                                                  | Semantic checks only                                                         |
| `--hard`          | Hard                     | 2 researchers           | plan.md + phases                                                                              | Full interview                                                               |
| `--deep`          | Deep                     | 2-3 researchers         | plan.md + phases + bounded phase map: file inventory, test gaps, interfaces, dependencies     | Full interview                                                               |
| `--parallel`      | Parallel                 | 2 researchers           | plan.md + phases + ownership matrix                                                           | Full interview                                                               |
| `--two`           | Two approaches           | 2 researchers           | 2 approach files + trade-off matrix                                                           | After selection                                                              |
| `--product-level` | Product spec             | 2 researchers (broader) | plan.md only (user stories + features + design language; NO phase files)                      | Semantic + check-product-spec.sh (no red-team, no validation interview — v1) |
| `--spike`         | Time-boxed investigation | Skip                    | spike plan from `assets/spike-plan-template.md` (investigate + findings phases; NO test/ship) | Semantic only                                                                |

**`--spike` constraints (Agile context only — gated by `agile-feedback-cycle.md` 2 when loaded):**

- Requires `--timebox <duration>` (e.g., `--timebox 2d`, `--timebox 4h`); reject with "spike requires --timebox" if absent
- Sets plan frontmatter `spike: true`, `timebox:`, and `findings_doc:` (default `tasks/plans/{slug}/findings.md`)
- INCOMPATIBLE with `--product-level` and `mk:autobuild` FULL density (autobuild gate breaks). Reject combination "spike incompatible with autobuild FULL — use --fast or mk:cook"
- Advisory cap: warn if `story_points > 5` — likely two spikes, or spike + story

**Composable flags:**

- `--tdd` — add tests-first phase sections and preserve strict TDD in the cook handoff. See `references/tdd-mode.md`.
- `--advice` — opt-in strategic supervision for one planning run, capped at 4 calls: GUIDE after the scope challenge, RESCUE on an unresolved red-team contradiction, REVIEW before Gate 1, RECHECK after a correction. Athena reads the plan and can return it to the planner; it never writes the plan and never approves Gate 1. Without the flag there are zero calls and no state. See `references/advice-checkpoints.md`.
- Visual work belongs to `mk:visual-plan`. Plan-creator emits only the handoff metadata needed for that skill; Markdown plan files remain source of truth.

## Requirements Capture Contract

Before producing a plan, plan-creator MUST be able to answer all 5 dimensions in concrete sentences (cook's exact-requirements contract — see `.claude/skills/cook/SKILL.md` "Exact-Requirements Contract (Phase 1)"):

1. **Expected output** — concrete artifact(s) the user will see at the end (file paths, feature behavior, UI screen, API endpoint + payload, CLI command + flags).
2. **Acceptance criteria** — specific behaviors / inputs → outputs / edge cases that MUST work to call it "done".
3. **Scope boundary** — what is explicitly OUT of scope this round.
4. **Non-negotiable constraints** — stack, file locations, naming, backward compatibility, deadlines, performance.
5. **Touchpoints** — which existing files/modules (from scout) will be modified or extended; which contracts must stay stable.

Every clarifying question MUST cite scout findings (file paths) in its options. Abstract options like "Add the feature" without a file path are a failure mode — replace with options of the form "Add to `src/api/users.ts` (matches existing pattern)" or "Create new `src/api/profile.ts`".

Skip when input is an existing plan path (`plan.md` / `phase-*.md`) — the plan already encodes scout output and the 5 dimensions.

## Workflow

Before starting, read `references/failure-catalog.md` for common planning failure modes to avoid.

Execute via `workflow.md`. Step-file architecture — load one step at a time.
Fast mode (`--fast`) uses `workflow-fast.md` (steps 00→03→04→07→08).

**Agile DoR advisory (Phase 1 entry, conditional):** if the parsed plan frontmatter contains a non-empty `jira_tickets:` list AND `agile-story-gates.md` is loaded (Agile context active per `mk:agent-detector` Step 0b), run 1 of `agile-story-gates.md` for each ticket BEFORE generating phase files. Render the advisory checklist; never block — let the user decide. Skip silently when `jira_tickets:` is absent or the rule is not loaded.

```
Step 0: Scope Challenge → trivial (exit) | simple (fast) | complex (hard/deep)
Step 0.5: Intake Packet (conditional: ≥2 external artifacts) → consolidate upstream artifacts, else clean skip
Step 1: Research (hard/deep/parallel/two only) → 2-3 researchers, max 5 calls each
Step 2: Codebase Analysis (hard/deep/parallel/two only) → scout + docs (deep: bounded scope map)
Step 3: Draft Plan → plan.md (≤80 lines) + phase-XX files (12-section template; deep: + phase map; tdd: + regression sections)
Step 4: Semantic Checks → goal/ACs/constraints + structural validation
Step 5: Red Team (hard/deep/parallel/two only) → 4-persona scaling, red-team-findings.md, adjudication
Step 6: Validation Interview (hard/deep/parallel/two only) → 3-5 critical questions with detection keywords, propagate answers
Step 7: Gate 1 → self-check + AskUserQuestion (Approve | Modify | Reject)
Step 8: Hydrate Tasks → phase checkboxes → session tasks
Step 9: Post-Plan Handoff → mode-pruned AskUserQuestion (cook|validate|red-team|end) → write `handoff.next` to plan.md → STOP
```

## Output Structure

**Fast mode:** Single `plan.md` (goal, context, scope, approach, ACs)
**Hard mode:** Directory with plan.md + phase files:

```
tasks/plans/YYMMDD-name/
├── plan.md              ← overview (≤80 lines)
├── research/            ← researcher reports (hard mode)
├── phase-01-name.md     ← 12-section detail (≤150 lines)
├── phase-02-name.md
└── ...
```

## Gotchas

- **Wrong workflow model**: feature-model on a bug fix skips investigation → confirm type at Step 0
- **Goal describes activity**: "Implement OAuth" vs "Users can log in with OAuth" → rewrite as outcome
- **ACs can't be verified**: "code is clean" blocks Gate 2 → every AC must reference a command/file check
- **Monolithic plan**: plan.md over 80 lines → move detail to phase files or research reports
- **Research disconnected**: findings archived but not cited in plan → Step 3 MUST integrate research into Key Insights
- **Over-planning trivial tasks**: 2-file config change gets full research → Step 0 scope gate exits early
- **Skipping scout on unfamiliar codebases**: → always run mk:scout if codebase is new
- **Using `--deep` to decide architecture**: deep maps a chosen approach; if the approach is unclear, route to `mk:brainstorming` first.
- **Dropping TDD at handoff**: when `tdd_mode=true`, step-09 MUST print cook with `--tdd`; sentinel/env state alone is not a cross-session contract.
- **Post-Plan Handoff is deterministic**: step-09 fires `AskUserQuestion`; do NOT auto-invoke the chosen command. User must type it in a fresh session for clean context.
- **`handoff.next` enum is validated**: values outside `{cook, validate, red-team, autobuild, end}` fail `validate-plan.py`.
- **Whole-Plan Consistency Gates W1 / W2 fire after red-team and validation interview**: stage-then-apply algorithm — no edits land until the user resolves any unresolved contradictions. See `references/whole-plan-sweep.md`.
- **`consistency_sweeps` frontmatter is optional**: legacy plans without it still validate as `PLAN_COMPLETE`.
- **Sweep recursion is bounded**: "resolve now" caps at 2 attempts per gate; further unresolved items convert to Risk rows.
- **`.plan-state.json` v1.2 schema is additive**: consumers MUST treat unknown keys (`verification_tier`, `consistency_sweeps_passed`) as optional and default-empty. v1.1 readers ignore them silently.
- **Post-hydration integrity-check failure is a hard stop**: cycle / count-mismatch / missing-metadata failures print an explicit diff and STOP — do NOT auto-recover or silently continue. Human resolution required before step-09. See `references/task-management.md` "Post-Hydration Integrity Checks".
- **Re-analyzing a design source that already has a packet duplicates interpretation**: when a design evidence packet path is present, cite the packet — do NOT call the design source's tools or re-parse its raw JSON. See `references/design-evidence-consumption.md`.

## References

| File                                               | Purpose                                                                                                                                                                                                              |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workflow.md`                                      | Step sequence, variable table, flow diagram (hard mode)                                                                                                                                                              |
| `workflow-fast.md`                                 | Compact step sequence for `--fast` mode (00→03→04→07→08)                                                                                                                                                             |
| `step-03a-product-spec.md`                         | Product-level spec drafter: user stories, features, design language. Replaces step-03 when `planning_mode = product-level`.                                                                                          |
| `assets/product-spec-template.md`                  | Product spec template (Vision, Features, Design Language, AI Integration, Out-of-Scope)                                                                                                                              |
| `assets/spike-plan-template.md`                    | Spike plan template (used when `planning_mode = spike`). Two phases: investigate + findings. Required frontmatter: `spike: true`, `timebox:`, `findings_doc:`. NOT compatible with `mk:autobuild` FULL.                |
| `references/anthropic-example-plan.md`             | RetroForge few-shot calibration example for product-level mode (ambition + feature density reference)                                                                                                                |
| `step-00-5-intake-packet.md`                       | Conditional intake packet builder: consolidates ≥2 pre-existing external artifacts before research/drafting                                                                                                          |
| `references/plan-intake-packet.md`                 | Plan Intake Packet contract: purpose, activation, 6-block schema, quality rules, boundaries                                                                                                                          |
| `references/design-evidence-consumption.md`        | Consuming a design evidence packet (e.g. Figma): do/don't, adjudication precedence, decision-ledger, flow→validation-matrix, `blocked_on:` phase blocking. Never re-analyzes the design source.                        |
| `step-05-red-team.md`                              | Red team review: persona scaling, subagent dispatch, adjudication                                                                                                                                                    |
| `step-06-validation-interview.md`                  | Critical question generation and answer propagation                                                                                                                                                                  |
| `step-07-gate.md`                                  | Self-check and Gate 1 AskUserQuestion presentation                                                                                                                                                                   |
| `step-09-post-plan-handoff.md`                     | Deterministic post-Gate-1 handoff: mode-pruned `AskUserQuestion` (cook \| validate \| red-team \| autobuild \| end), live risk re-scan, writes `handoff.next` to plan.md frontmatter, prints command + STOPs.        |
| `references/whole-plan-sweep.md`                   | Whole-Plan Consistency Sweep algorithm (Gates W1 + W2). Stage-then-apply: read-only Pass 1 stages Pending Sweep Edits; decision check blocks on unresolved contradictions; write Pass 2 applies edits and logs.   |
| `references/deep-mode.md`                          | Deep mode contract: when to use/avoid, scout budgets, phase-map appendix, context rules.                                                                                                                             |
| `references/tdd-mode.md`                           | TDD flag contract: phase sections, optional frontmatter, cook handoff propagation, RED-task hydration.                                                                                                                |
| `references/verification-roles.md`                 | Verification Roles for step-04 sub-step 4d (Fact Checker / Flow Tracer / Scope Auditor / Contract Verifier) with tier selection by phase count. Subagents are READ-ONLY; orchestrator writes the `## Verification Log`. |
| `prompts/personas/plan-assumption-destroyer.md`    | Plan-specific assumption skeptic persona                                                                                                                                                                             |
| `prompts/personas/plan-scope-complexity-critic.md` | Plan-specific YAGNI/scope minimalist persona                                                                                                                                                                         |
| `prompts/personas/plan-security-adversary.md`      | Plan-specific security adversary (auth bypass, injection, data exposure). Used at 4+ phases.                                                                                                                         |
| `prompts/personas/plan-failure-mode-analyst.md`    | Plan-specific failure mode analyst (race conditions, cascading failures, recovery). Used at 6+ phases.                                                                                                               |
| `references/phase-template.md`                     | 12-section phase file template                                                                                                                                                                                       |
| `references/ops-metrics-design.md`                 | If task involves metrics/KPIs/dashboards, load for metric philosophy, templates, and domain fallbacks                                                                                                                |
| `references/cold-start-context-brief.md`           | When writing phase files, follow this template for self-contained, cold-start-safe phase files                                                                                                                       |
| `references/plan-mutation-protocol.md`             | When modifying an existing plan (split/insert/skip/reorder/abandon), follow this protocol                                                                                                                            |
| `references/worked-example-stripe-billing.md`      | For plan detail level reference, see this complete worked example (the 7-phase model)                                                                                                                                |
| `references/scope-challenge.md`                    | Scope modes (HOLD/EXPANSION/REDUCTION)                                                                                                                                                                               |
| `references/research-phase.md`                     | Researcher spawning protocol                                                                                                                                                                                         |
| `references/plan-organization.md`                  | Directory structure, naming, size rules                                                                                                                                                                              |
| `references/output-standards.md`                   | YAML frontmatter, required sections                                                                                                                                                                                  |
| `references/validation-questions.md`               | Critical question categories for interview                                                                                                                                                                           |
| `references/gate-1-approval.md`                    | AskUserQuestion gate + Context Reminder                                                                                                                                                                              |
| `references/task-management.md`                    | Hydration, cross-session resume, sync-back                                                                                                                                                                           |
| `references/solution-evaluation.md`                | Trade-off scoring criteria                                                                                                                                                                                           |
| `references/gotchas.md`                            | Full gotchas list                                                                                                                                                                                                    |
| `references/solution-design-checklist.md`          | Trade-off analysis checklist for Architecture/Risk/Security sections (5 dimensions)                                                                                                                                  |
| `references/adr-generation.md`                     | Architecture Decision Record generation                                                                                                                                                                              |
| `references/parallel-mode.md`                      | Ownership matrix template, parallel group rules                                                                                                                                                                      |
| `references/two-approach-mode.md`                  | Approach file template, trade-off matrix, selection flow                                                                                                                                                             |
| `scripts/validate-plan.py`                         | Plan completeness validator. **Depends on PyYAML** (installed via `.claude/scripts/bin/setup-workflow` into `.claude/skills/.venv/`). Run via `.claude/skills/.venv/bin/python3 scripts/validate-plan.py <plan.md>`. |
| `scripts/check-product-spec.sh`                    | Product-spec structural validator (POSIX bash). Enforces feature count, user stories, forbidden patterns. Used by step-03a and step-04 for `--product-level` mode.                                                   |
| `references/workflow-models/feature-model.md`      | Workflow template for feature tasks (loaded JIT by step-00)                                                                                                                                                          |
| `references/workflow-models/bugfix-model.md`       | Workflow template for bug fix tasks (loaded JIT by step-00)                                                                                                                                                          |
| `references/workflow-models/refactor-model.md`     | Workflow template for refactor tasks (loaded JIT by step-00)                                                                                                                                                         |
| `references/workflow-models/security-model.md`     | Workflow template for security tasks (loaded JIT by step-00)                                                                                                                                                         |

## Known Exceptions

- `references/anthropic-example-plan.md` — filename retained as the source-provenance attribution for the few-shot calibration example. The file content is the appendix of a published harness-design article (Prithvi Rajasekaran, Labs); renaming would obscure the research origin. Future brand-prose audits skip this filename per this documented exception.

## Related Rules

- `.claude/rules/gate-rules.md` — Gate 1 hard-stop conditions this skill enforces (plan approval before Phase 3)
- `.claude/rules/orchestration-rules.md` — boundary contract; verification subagents stay READ-ONLY; sweep stays in planner context (never delegated)
- `.claude/rules/task-state-emission.md` — when an active durable task record exists, emit status/step via `mewkit task-state update` (advisory; active durable tasks only)

## Start

Read and follow `workflow.md`.
