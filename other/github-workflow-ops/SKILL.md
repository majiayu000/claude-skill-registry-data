---
name: github-workflow-ops
description: "Use when operating GitHub from Hermes: authentication, gh CLI setup, issue triage, pull-request review, inline comments, REST fallbacks, or local git/GitHub workflow verification."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# GitHub Workflow Operations

Class-level guide for GitHub work. Use `gh` when authenticated and fall back to git plus GitHub REST via curl when needed.

## Authentication
Set up or verify GitHub auth before repository operations. Cover both `gh auth` and git transport (HTTPS tokens or SSH keys). Keep tokens out of logs and use helper environment scripts only for scoped sessions.

## Issues
Create, search, triage, label, assign, and update issues. Use issue templates for feature requests and bug reports when creating structured issues. Always capture issue number/URL after creation.

## Code review and pull requests
Review local diffs or GitHub PRs by reading the diff, checking risk areas, leaving inline comments when requested, and running relevant verification. Do not approve or report success without inspecting the changed files and command output.

## Verification checklist
- `gh auth status` or equivalent before API calls.
- `git status` before modifying repository state.
- Capture PR/issue URLs or IDs for side effects.
- Run the smallest relevant test/lint/build before claiming review or fix completion.

## Support packages
Absorbed source skill packages are preserved under `references/absorbed-skills/` for detailed commands, templates, and scripts.
