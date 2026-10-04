---
name: release-manager
description: Prepare release readiness notes, version checks, test checklist, and local issue drafts.
risk: medium
required_tools:
  - git.status
  - git.diff
  - git.log
  - file.read
  - shell.dry_run
  - github.issue_draft
suggested_subagent: release-manager
business_domain: software-release
cadence: task, weekly
approval_required_for:
  - file.write_safe
  - shell.execute_approved
  - github.issue_create_approved
---

# Release Manager

Use this skill when the user asks to prepare a release plan or release notes.

Rules:
- Inspect git status, diff, recent commits, package metadata, and memory first.
- Draft release notes or GitHub issues locally before any external write.
- Never publish packages or releases from this skill.
