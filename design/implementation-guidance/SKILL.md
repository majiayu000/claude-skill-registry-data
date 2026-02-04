---
name: implementation-guidance
description: 'Provides detailed guidance on how to implement a single plan step while adhering to architecture and quality standards.'
metadata:
  id: ce.skill.implementation-guidance
  tags: [execution, testing, validation]
  inputs:
    files: [PLAN.md, ARCHITECTURE.md, CONTRIBUTING.md]
    concepts: [small-diffs]
    tools: [toolset:write]
  outputs:
    artifacts: [ce.task.validate]
    files: []
    actions: [apply-changes]
  dependsOn:
    artifacts: [ce.task.validate]
    files: [.vscode/tasks.json]
  related:
    artifacts: [ce.prompt.implement-step]
    files: []
---

# Implementation Guidance Skill

This skill helps you turn a single plan step into code changes while following TDD and
maintaining architectural integrity.

## Steps

1. **Select a plan slice.** Identify the next unimplemented milestone or task from `PLAN.md`.
   Summarise its objective, inputs, outputs and acceptance criteria.

2. **Review constraints.** Load `ARCHITECTURE.md` and `CONTRIBUTING.md` to understand any
   constraints (e.g. design patterns, layer boundaries, security policies). Ensure your
   implementation will not violate them.

3. **Write tests first.** Before writing production code, design unit and integration tests
   that express the desired behaviour. Use the testing strategy guidelines and harness
   appropriate frameworks.

4. **Implement incrementally.** Write small, focused commits that satisfy one test at a time.
   Avoid large diffs. Document significant decisions or deviations in an ADR if necessary.

5. **Run validation and linting.** After coding, execute the validation task (`Context Kit: Validate`)
   and any language-specific linters or static analysis tools. Fix issues immediately.

6. **Summarise changes.** Prepare a concise summary of what was changed, which files were
   touched and how the acceptance criteria were met. Provide links to relevant docs or ADRs.

7. **Handoff for review.** Once the step is complete and validated, hand off to the reviewer
   agent or trigger the `review-changes` prompt for quality assurance.

By following this process you produce maintainable code that is easy to review and less likely to
introduce regressions or technical debt.
