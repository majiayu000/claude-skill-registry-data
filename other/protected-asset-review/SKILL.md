---
name: protected-asset-review
description: Review protected asset policy and risky local data surfaces.
risk: high
required_tools:
  - file.list
  - file.read
  - git.diff
  - shell.dry_run
suggested_subagent: security-reviewer
business_domain: safety-governance
cadence: task, audit
approval_required_for:
  - file.write_safe
  - shell.execute_approved
---

# Protected Asset Review

Use this skill when the user wants to check databases, backups, secrets, customer data, or system paths are protected.

Rules:
- Verify policy before tool actions.
- Treat database deletion, backup movement, secret reads, and customer-data access as high-risk.
- Never weaken protected asset policy.
