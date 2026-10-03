---
name: decommission
description: Systematically tear down and remove a service, package, or infrastructure component
type: execution
version: v0.1
required_conventions: [alignment-page]
---

# Decommission

Invoke as `$decommission`.

Use this skill when the user wants to remove a service, package, module, or infrastructure component from the project.

## Process

1. Identify the target to decommission.
2. Audit all references: imports, configs, infrastructure, documentation.
3. Categorize as active dependencies, dead references, or infrastructure.
4. Present the removal plan and wait for approval. Use `update_plan` to track the work; use `request_user_input` only if the session is already in Plan mode and a structured choice would help.
5. Execute removal: migrate consumers, delete target, clean up references.
6. Verify: tests, build, grep for remaining references.

## Output

- **Dependencies Resolved**: consumers migrated or updated
- **Infrastructure Cleanup**: automated vs. manual required
- **Verification**: tests, build, remaining references

## Constraints

- Always audit dependencies before removing anything.
- Never delete cloud resources automatically — only IaC definitions.
- Present the plan and get approval before making changes. Do not assume a Claude-style `EnterPlanMode` or clear-context accept flow exists.


## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/decommission-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
