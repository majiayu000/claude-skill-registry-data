---
name: engineering-standards
description: "Use only when the request concerns standards, responsibility, complexity, smells, naming, refactoring catalogs, or task-plan rules; not routine work."
---

# Skill: engineering-standards

## Purpose

Apply the shared engineering standards library: manifesto, constitution, design principles, responsibility model, complexity budget, smells, naming, testing, errors, observability, API/domain/state/config/data/dependency philosophy, and evolution rules.

Use this skill when the task is broad, architectural, quality-focused, standards-focused, or when a change risks growing into a dumping ground.

## Required references

Read only the references needed for the task:


- `../../engineering/README.md` — index and selection rules for the standards library.
- `../../engineering/00_manifesto.md` — stable engineering intent.
- `../../engineering/01_constitution.md` — non-negotiable engineering law.
- `../../engineering/05_design_principles.md` — SOLID, KISS, DRY, YAGNI, Clean Architecture, DDD, TDD as behavior.
- `../../engineering/06_responsibility_model.md` — single responsibility at function/class/file/package/service/layer/context levels.
- `../../engineering/07_complexity_budget.md` — size and complexity thresholds.
- `../../engineering/08_engineering_smells.md` — code-level smells.
- `../../engineering/09_architectural_smells.md` — boundary and architecture smells.
- `../../engineering/10_antipattern_catalog.md` — recurring bad design patterns.
- `../../engineering/11_refactoring_catalog.md` — safe refactoring tools.
- `../../engineering/12_naming_bible.md` — naming rules.
- `../../engineering/24_task_todo_style.md` — structured TODO/task plans.
- `../../engineering/25_api_philosophy.md` — API and CLI contract design.
- `../../engineering/26_domain_modeling.md` — domain boundaries, invariants, commands, events, and policies.
- `../../engineering/27_state_machine_philosophy.md` — explicit states and valid transitions.
- `../../engineering/28_concurrency_philosophy.md` — async, workers, locks, queues, retries, timeouts, and backpressure.
- `../../engineering/29_configuration_philosophy.md` — configuration, secrets, flags, defaults, and lifecycle.
- `../../engineering/30_dependency_philosophy.md` — dependency admission, wrapping, risk, and removal.
- `../../engineering/31_data_philosophy.md` — source of truth, schema changes, migrations, retention, caching, and consistency.
- `../../engineering/32_ui_architecture_philosophy.md` — UI state, component boundaries, accessibility, and frontend architecture.
- `../../engineering/33_ai_engineering_philosophy.md` — evidence-bound AI engineering and agent patch quality.
- `../../engineering/34_evolution_decision_tree.md` — decision trees for adding structure.
- `../../engineering/35_evidence_contract.md` — evidence requirements and uncertainty reporting.
- `../../engineering/36_task_lifecycle_gates.md` — proportional task gates.
- `../../engineering/37_review_regression_gates.md` — review and regression gates.
- `../../engineering/38_library_drift_audit.md` — library drift audit contract.

## Operating rules

- Do not apply principles as slogans.
- Translate principles into concrete design choices.
- Do not force Clean Architecture, DDD, CQRS, event sourcing, or similar styles unless the repository already uses them or the user asks.
- Prefer the smallest design that preserves correctness and future maintainability.
- Treat large files and mixed responsibilities as risks, not style issues.
- A human-authored 10k-line file is unacceptable except generated/vendor/lock/migration-like exceptions or explicit legacy containment.

## Output

When this skill materially affects the answer, name the principle or smell and the concrete action taken.
