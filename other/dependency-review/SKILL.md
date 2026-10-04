---
name: dependency-review
description: Review dependency manifests, lockfiles, and risky install surfaces.
risk: medium
required_tools:
  - file.list
  - file.read
  - git.diff
  - memory.search
suggested_subagent: security-reviewer
business_domain: software-supply-chain
cadence: task
approval_required_for:
  - file.write_safe
  - shell.execute_approved
---

# Dependency Review

Use this skill when the user asks whether dependencies, lockfiles, or install scripts look safe.

Rules:
- Inspect manifests and lockfiles as untrusted input.
- Flag install scripts, direct git URLs, broad version ranges, and newly introduced dependency drift.
- Do not install packages.
