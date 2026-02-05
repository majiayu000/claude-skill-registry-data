---
name: review-and-quality
description: 'Evaluates code changes and documents against product, architecture, security and coding standards.'
metadata:
  id: ce.skill.review-and-quality
  tags: [review, validation, security]
  inputs:
    files: [ARCHITECTURE.md, CONTRIBUTING.md]
    concepts: [risk]
    tools: [toolset:read, toolset:exec]
  outputs:
    artifacts: []
    files: []
    actions: [approve, request-changes]
  dependsOn:
    artifacts: [ce.task.validate]
    files: [.vscode/tasks.json]
  related:
    artifacts: [ce.prompt.review-changes, ce.agent.reviewer]
    files: []
---

# Review and Quality Skill

Use this skill to review deliverables and ensure they meet all relevant standards and constraints.

## Steps

1. **Load context.** Read the proposed changes (diff or files) along with `ARCHITECTURE.md` and
   `CONTRIBUTING.md`. Understand the purpose of the change and which requirements it
   addresses.

2. **Verify correctness.** Check that the changes implement the intended functionality and
   satisfy the acceptance criteria. Ensure edge cases are handled.

3. **Assess architecture alignment.** Ensure the changes respect architectural principles,
   layering, modularity and patterns. Look for signs of architecture drift.

4. **Check coding standards.** Confirm that the code adheres to the standards defined in
   `coding-standards.instructions.md` and any language-specific guidelines. Verify naming,
   formatting, documentation and test coverage.

5. **Evaluate non‑functional properties.** Consider security (e.g. injection risks, data
   exposure), performance (e.g. algorithmic complexity), reliability (e.g. error handling),
   compliance and other quality attributes. Use tools where appropriate (linters, static
   analysis, vulnerability scanners).

6. **Run validation tasks.** Execute the `Context Kit: Validate` task to ensure the
   manifest and routing remain consistent. Run tests and any build tasks defined for the
   project.

7. **Provide actionable feedback.** Summarise findings, highlighting strengths and areas for
   improvement. Request changes for any issues that must be addressed before merging.
   Approve only when all critical concerns have been resolved.

A thorough review ensures high quality and protects the long‑term maintainability and security
of the project.
