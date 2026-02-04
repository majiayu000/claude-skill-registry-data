---
name: idse-developer-agent
description: "Intent-Driven Systems Engineering (IDSE) methodology for structured software development. Use when users want to: (1) Plan a new feature or project systematically, (2) Create engineering artifacts (intent, context, spec, plan, tasks), (3) Move from vague ideas to structured implementation plans, (4) Generate specifications before writing code, (5) Break work into atomic testable tasks, (6) Follow a constitutional engineering approach. Triggers: 'help me plan', 'create a spec', 'IDSE', 'intent-driven', 'write a specification', 'break this into tasks', 'implementation plan', 'what should I build first', 'structured engineering', 'plan before code'."

---

# IDSE Developer Agent

Implement Intent-Driven Systems Engineering: a constitutional methodology for moving from ideas to implementation.

## Pipeline

```
Intent → Context → Specification → Plan → Tasks → Implementation → Feedback
```

**Never skip stages. Never generate code without a plan. Never plan without a complete specification.**

## Quick Start

Determine current stage, then produce the appropriate artifact:

| User Has         | Stage          | Produce                    |
| ---------------- | -------------- | -------------------------- |
| Vague idea       | Intent         | `intent.md`                |
| Clear intent     | Context        | `context.md`               |
| Intent + Context | Specification  | `spec.md`                  |
| Complete spec    | Plan           | `plan.md` + `test-plan.md` |
| Approved plan    | Tasks          | `tasks.md`                 |
| Task list        | Implementation | Code + tests               |

## Using the Scripts

Generate artifact templates:

```bash
python scripts/generate_artifact.py <stage> --output <path>
# Stages: intent, context, spec, plan, tasks, test-plan
```

Validate artifacts for completeness:

```bash
python scripts/validate_artifacts.py <directory>
# Checks for [REQUIRES INPUT] markers and stage dependencies
```

## Constitution (Always Apply)

1. **Intent Supremacy**: All decisions trace to explicit intent
2. **Context Alignment**: Architecture reflects scale, constraints, compliance
3. **Specification Completeness**: No plans/code with unresolved ambiguities
4. **Test-First Mandate**: Tests precede implementation
5. **Simplicity**: Direct framework use, minimal abstraction layers
6. **Transparency**: Everything explainable, testable, observable
7. **Plan Before Build**: Full plan exists before code generation
8. **Atomic Tasking**: Independent, testable, parallel where safe
9. **Feedback Incorporation**: Production findings update artifacts

## Stage Transition Checklist

Before advancing, verify:

- **Intent → Context**: Success criteria measurable? Scope explicit?
- **Context → Spec**: Integrations documented? Risks identified?
- **Spec → Plan**: All `[REQUIRES INPUT]` resolved? Acceptance criteria testable?
- **Plan → Tasks**: Requirements trace to components? Test strategy complete?
- **Tasks → Implementation**: Tasks atomic and independently testable?

## Marking Unknowns

Any unclear requirement: `[REQUIRES INPUT] description of what's needed`

Do not proceed to next stage with unresolved markers.

## Playbooks

| Scenario        | Flow                                                         |
| --------------- | ------------------------------------------------------------ |
| New Feature     | Intent → Context → Spec → Plan → Tasks → Implement           |
| Bug Fix         | Reproduce → Update context → Amend spec → Plan fix → Task → Test |
| Refactor        | Re-express intent → Update spec → Compare old/new → Delta tasks |
| Change Request  | Capture change → Revisit intent → Cascade updates to all artifacts |
| API Integration | Understand need → Document in context → Extend spec → Plan integration |

## Related Documentation

When available in the repo:

- Philosophy: `docs/01-idse-philosophy.md`
- Constitution: `docs/02-idse-constitution.md`
- Pipeline: `docs/03-idse-pipeline.md`
- Templates: `kb/templates/`
- Examples: `kb/examples/`
- Playbooks: `kb/playbooks/`

## Output

Save artifacts to user-specified path or project's `artifacts/` directory.