---
name: nick-git-ops
description: Git workflow automation and guidance for Nick's multi-project workflow, especially repos in ~/Projects/. Use when doing git commits, status checks, branching, merges, rebases, reviewing dirty working trees, cleaning branch flow, or managing multiple repos. Enforce conventional commits and safer git habits.
---

# Nick Git Ops

Use this as the default Git workflow skill for Nick.

## Purpose
Make git work cleaner, safer, and faster across multiple projects.

## Core use cases
- check repo status quickly
- manage multiple repos in `~/Projects/`
- create clean branches
- write conventional commit messages
- decide merge vs rebase
- prepare changes before push
- reduce accidental messy git operations

## Hard rules
- Follow conventional commits
- Never commit secrets or `.env` files
- Check status before risky git operations
- Prefer readable branch names and history
- Be explicit about repo context when multiple projects exist

## Conventional commit defaults
Use formats like:
- `feat: add signup flow`
- `fix: resolve dashboard loading bug`
- `refactor: simplify auth guard`
- `chore: update dependencies`
- `docs: clarify setup notes`
- `test: add login flow coverage`

## Standard workflow
1. Confirm current repo and branch
2. Review working tree status
3. Review staged vs unstaged changes
4. Choose branch action if needed
5. Create a clear conventional commit message
6. Push cleanly
7. Note any merge/rebase risk before acting

## Multi-project rules
When working across projects:
- identify the exact repo first
- avoid assuming current directory is the intended repo
- prefer repo summary before batch work
- call out dirty repos clearly

## Merge vs rebase defaults
- use merge when preserving branch history matters
- use rebase when cleaning local feature history before merge
- avoid rewriting shared history casually

## References
- Read `references/commit-conventions.md` for commit style
- Read `references/branching.md` for naming and branch hygiene
- Read `references/merge-rebase-guide.md` when choosing history strategy
- Read `references/multi-repo-workflow.md` for ~/Projects/ habits
- Read `references/safety-checklist.md` before risky git operations

## Bundled scripts
- `scripts/repo_status_summary.sh` — summarize git status across repos
- `scripts/generate_commit_message.sh` — generate conventional commit stubs
- `scripts/create_branch_name.sh` — generate readable branch names
- `scripts/pre_push_checklist.sh` — create a pre-push sanity checklist
