---
name: implementation-planning
description: Plan a multi-step change before editing. Use for work with multiple files, dependencies, migration risk, or non-obvious verification; skip for trivial fixes.
---

# Implementation Planning

Inspect the repository before drafting the plan. The plan must describe this codebase, not an imagined one.

1. Translate the request/spec into outcomes and acceptance criteria.
2. Identify relevant modules, tests, contracts, migrations, and constraints using codebase reconnaissance.
3. Split work into ordered, independently verifiable steps. Each step names the likely files or components, intended change, and check.
4. Mark dependencies, decisions, data migrations, compatibility effects, and rollback considerations.
5. Prefer vertical slices that produce testable behavior. Avoid artificially tiny steps or task lists that merely restate the code.
6. Identify which parts can be delegated safely and which need a single owner.
7. Keep optional improvements separate from required scope.

Deliver a compact plan with sequence, acceptance checks, risks, and assumptions. A plan is not proof of completion. Revise it when inspection reveals different facts; do not force the implementation to fit a stale plan.
