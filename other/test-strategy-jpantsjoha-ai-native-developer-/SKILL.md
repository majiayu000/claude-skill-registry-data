---
name: test-strategy
description: Map requirement acceptance to proportionate executable checks and real user journeys before implementation and completion.
---

# Test Strategy

Read the accepted requirement, relevant business journey, risks and project check
commands. Maintain the existing test strategy with criterion → check → environment →
owner mappings; identify uncovered criteria before dispatch.

Choose unit checks for logic, integration checks for seams, and journey checks for the
actual user entrypoint. Include relevant negative, persistence, permission, recovery and
regression cases. A direct API call cannot substitute for a changed browser interaction;
a health response cannot establish user acceptance. Use owned manual checks when
appropriate and report their result separately from automated coverage.

For planning-only assignments, return the coverage map and commands to the assigned
worker; do not execute or create fixtures. When execution is authorised within your lane,
run candidate checks and record command, revision, environment, outcome and limits. For new regression guards verify a representative defect makes the check fail
in an isolated fixture; do not damage a shared working tree. Avoid tests that merely
repeat wording or implementation. Return uncovered acceptance to product-owner and
delivery-orchestrator; never weaken a requirement to make a suite pass.
