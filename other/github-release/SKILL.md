---
name: github-release
description: Prepare release notes, issue drafts, and GitHub release readiness checks.
risk: medium
required_tools:
  - git.status
  - git.diff
  - git.log
  - github.repo_read
  - github.issue_draft
approval_required_for:
  - github.issue_create_approved
---

# GitHub Release

Use this skill when the user wants a release review, release notes, or a GitHub issue related to release work.

Rules:
- Inspect git state and recent commits first.
- Draft external updates locally before proposing any GitHub write.
- Use approval-gated GitHub write tools only after the user approves.
- Never publish packages or releases directly.
