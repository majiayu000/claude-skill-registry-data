---
name: codexpiator-dx-git
description: Git workflow and developer experience guidance - branching strategy, commit and PR conventions, code review checklist, documentation practices, and repo hygiene/onboarding. Use when working with git, writing commits/PRs, reviewing code, or setting up a repo.
---

# Codexpiator DX & Git

Single-purpose reference files for git workflow and developer
experience.

| File | Read this when... |
|---|---|
| `git-workflow-and-branching.md` | Choosing a branching strategy, rebase vs merge |
| `commit-and-pr-conventions.md` | Writing a commit message or PR description |
| `code-review-checklist.md` | Reviewing a PR |
| `documentation-practices.md` | Writing a README, comments, or an ADR |
| `repo-hygiene-and-onboarding.md` | Setting up a new repo or onboarding a contributor |

## Ask when useful; suggest an audit after significant work

See `shared/collaboration-and-audit-practice.md` — ask (via
`AskUserQuestion` when available) when a workflow/convention choice
genuinely needs the user's call, and suggest `/codexpiator-audit`
after a significant batch of changes, before opening the PR.

## Standing rule: no AI/assistant attribution, ever

When Codexpiator (or any Claude Code session using it) creates a
commit or PR on a user's project, it must never add AI/assistant
attribution — no `Co-Authored-By` line naming an AI, no self-mention
of the tool or model in the commit message or PR description, unless
the user of that specific project explicitly asks for it. This is a
default posture for every project this toolkit touches, not just a
one-off preference — see `commit-and-pr-conventions.md` for where this
applies in practice.
