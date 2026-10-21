---
name: using-skills
description: Choose the smallest applicable workflow when task routing is uncertain. Triggers on "which skill should I use", "用哪个技能".
---

# Using Skills

## When to use

- Choose the smallest applicable workflow when task routing is uncertain.

**Not for:** clear tasks with a selected skill; skill-authoring for maintenance.

## Steps

1. Identify intent, scope and uncertainty; use a clear skill directly and avoid ritual routing for simple questions.

2. Choose by output and problem; clarify only if alternative interpretations change the work.

3. Sequence only necessary prerequisites and reuse confirmed artifacts instead of forcing every lifecycle stage.

4. Load the skill and only needed references; use ordinary engineering judgment if none fits and identify recurring gaps.

## Verify

- Selected workflow fits intent; unnecessary skills, artifacts and repeated approval requests are avoided.

## Phase catalog

- **01-product** — brainstorm, oss-strategy, spec
- **02-research** — research
- **03-design** — api-design, architecture, codebase-design, design-research, domain-modeling, frontend-design, image-to-code, imagegen, prompt-engineering, prototype, schema-design
- **04-develop** — auth-implementation, breakdown, context-engineering, error-handling, i18n, implement, multi-agent-orchestration
- **05-tune** — cost-optimization, performance, refactoring, simplify
- **06-test** — api-testing, e2e-testing, load-testing, tdd, test-generation
- **07-verify** — a11y-review, code-review, debugging, linting, security-review
- **08-ship** — ci-cd, deprecation-migration, git-workflow, oss-polish, shipping
- **09-operate** — documentation-audit, handoff, incident-response, observability, purity-audit
- **meta** — skill-authoring, using-skills

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/phase-tree.md](references/phase-tree.md) — full ASCII decision tree by phase and task shape.

External skill discovery (`npx skills find/add`) is out of scope — this router maps tasks to this collection's internal skills only.
