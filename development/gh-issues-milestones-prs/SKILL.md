---
name: gh-issues-milestones-prs
description: Write GitHub Issues/PRs and manage milestones for this repo. Use for issue/PR content conventions and gh CLI workflow (including milestones).
---

# GitHub Issues and PRs

## Workflow

- Use templates in `.github/ISSUE_TEMPLATE/task.md` and `.github/PULL_REQUEST_TEMPLATE.md`.
- Use `gh` with `--body-file` to avoid shell quoting problems.
- For milestones, use `gh milestone --help` and follow the standard GitHub milestone workflow.

## Content conventions

- Be literal, unambiguous, and clear.
- Include required readings so future agents pick them up.
- Use numbered/lettered lists for stable references.
- Calibrated confidence: distinguish must‑haves vs speculative ideas.
- Add skimmable extra commentary for the owner.

## Identity note

- All agents share the project owner’s GitHub identity; clarify authorship/assignee in body text or footers.
