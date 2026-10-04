---
name: safe-test-runner
description: Prepare and classify local test commands before asking approval to execute them.
risk: medium
required_tools:
  - file.read
  - git.status
  - shell.dry_run
suggested_subagent: project-inspector
business_domain: software-development
cadence: task
approval_required_for:
  - shell.execute_approved
---

# Safe Test Runner

Use this skill when the user wants tests, lint, or checks run safely.

Rules:
- Read package scripts or project docs before suggesting a command.
- Always dry-run/classify before execution.
- Do not execute shell commands without approval.
