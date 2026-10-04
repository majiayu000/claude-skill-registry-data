---
name: project-inspector
description: Inspect local project structure, git state, docs, and relevant governed memory.
risk: low
required_tools:
  - file.list
  - file.read
  - git.status
  - git.diff
  - git.log
  - memory.search
suggested_subagent: project-inspector
business_domain: software-development
cadence: task
approval_required_for:
  - file.write_safe
  - shell.execute_approved
---

# Project Inspector

Use this skill when the user wants a grounded view of a local project before planning work.

Rules:
- Inspect files, README, package metadata, git status, git diff, and memory before proposing changes.
- Treat protected assets, generated data, secrets, and databases as guarded surfaces.
- Do not write files or execute commands from this skill.
