---
name: npm-package-helper
description: Inspect package metadata, lockfiles, scripts, and npm release readiness.
risk: medium
required_tools:
  - file.read
  - git.status
  - shell.dry_run
approval_required_for:
  - shell.execute_approved
---

# npm Package Helper

Use this skill when the user asks to inspect, prepare, or verify an npm package.

Rules:
- Read `package.json` and lockfiles before suggesting commands.
- Use `shell.dry_run` before any execution.
- Never run `npm publish`; only suggest a checklist unless a future explicitly governed publish tool exists.
- Keep writes approval-gated.
