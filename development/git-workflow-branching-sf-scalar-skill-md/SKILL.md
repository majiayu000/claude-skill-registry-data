---
name: git-workflow-branching
description: When creating, updating, and merging code in a collaborative version control environment.
version: 2.0.0
category: dev-tools
tags: [dev-tools, git, collaboration, version-control]
skill_type: workflow
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 1500
dangerous: false
requires_review: false
security_level: safe
dependencies: []
triggers: [git, branch, merge, commit, pull request]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: true }
  shell: { execute: true }
input_requirements: [git repository, remote configured]
output_contract: [linear git history, conventional commits, no WIP commits on main]
failure_conditions: [direct push to main, merge conflicts unresolved, broken CI on main]
last_updated: 2026-05-15
---

# Git Workflow & Branching

## Purpose
Clean git history is essential for debugging (`git bisect`), code review, and team collaboration. This skill standardizes branch naming, commit formatting, and merging to maintain a readable, revertible, and bisect-able history.

## When to use
- Starting a new feature or bugfix ticket
- Reviewing PRs and merging code into mainline
- Hotfixing production environments
- Onboarding new team members

## When NOT to use
- Dealing with complex merge conflicts (use git documentation)
- Repository history rewrites (different concern)
- CI/CD trigger configuration (separate skill)

## Inputs required
- Git repository with `main` branch
- Remote repository (GitHub, GitLab, Gitea)
- Team agreement on branch naming and commit conventions

## Workflow
1. **Sync Main**: ALWAYS fetch and pull latest from `main` before creating branch
2. **Create Branch**: Use convention `type/ticket-id-short-description` (e.g., `feat/PROJ-123-add-login`)
3. **Commit Atomically**: Commit in small logical chunks. MUST use Conventional Commits format
4. **Keep Branch Synced**: Rebase against `main` frequently to avoid merge conflicts
5. **Push Regularly**: Push to remote regularly (enables collaboration, backup)
6. **Rebase Before PR**: Interactive rebase to clean up WIP commits before opening PR
7. **Squash Merge**: Merge PR using squash-merge to keep main history clean
8. **Delete Branch**: Delete feature branch after merging (cleanup)

## Rules
- MUST NEVER push directly to `main` (always use PRs)
- MUST use Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`
- MUST rebase before opening PR (no merge commits from main)
- MUST delete feature branches after merging
- MUST NOT commit with messages like "wip", "fixed typo", "trying again"
- MUST resolve conflicts locally before pushing
- MUST NOT force-push to shared branches
- MUST keep feature branches <5 days old before merging

## Anti-patterns
- **WIP Commits**: Pushing commits like "wip", "fixed typo", "let me try again" to main
- **Long-lived Branches**: Keeping branches active for weeks without syncing with main
- **Merge Commits**: Allowing merge commits from main to pollute history (use rebase)
- **Squashing Too Early**: Squashing before PR review (makes feedback hard to track)
- **Force Pushing to Shared**: `git push -f` on branches other developers are using
- **Vague Messages**: "Update stuff", "fix bug" (impossible to bisect later)

## Failure conditions
- Direct push to `main` detected
- Merge conflicts exist when opening PR
- Broken tests or CI failures on main
- WIP commits in main history
- Feature branches never deleted after merge

## Validation checklist
- [ ] Branch created from latest main
- [ ] Branch name follows `type/ticket-id-description` format
- [ ] All commits use Conventional Commits format
- [ ] No "wip", "fixed typo", or vague commit messages
- [ ] Commits are atomic (each solves one thing)
- [ ] Rebase completed, no merge commits from main
- [ ] All conflicts resolved locally
- [ ] CI passes before PR merge
- [ ] PR description links ticket
- [ ] Branch deleted after merging

## Output format
- **Branch naming**: `type/ticket-id-short-desc` (e.g., `feat/AUTH-42-oauth-integration`)
- **Commit format**: `type(scope): description\n\nbody\n\nfooter`
- **History**: Linear commits on main (no merge commits)
- **Merge strategy**: Squash-merge to single conventional commit

## Security considerations
- NEVER commit secrets (use `.gitignore`, environment variables)
- Code review MUST happen before main (enforce via PR requirements)
- Force-push MUST be disabled on main branch
- Branch protection rules MUST require passing CI

## Agent execution notes
- Agent MAY: Create branches, make commits, rebase branches, resolve conflicts, open PRs
- Agent MUST NEVER: Push directly to main, create WIP commits, force-push shared branches
- Agent MUST ASK: Before force-pushing, before deleting branches, before modifying main history
- Agent MUST VALIDATE: Branch follows naming convention, commits are conventional, CI passes

## Example

**❌ Anti-pattern (WIP commits, vague messages, no rebasing):**
```bash
git checkout main
# Forgot to pull - out of sync
git checkout -b feature-branch
git commit -m "wip"
git commit -m "fixed typo"
git commit -m "let me try again"
git commit -m "update stuff"
git push origin feature-branch
# Merge directly to main without PR
```

**✅ Correct pattern (Atomic commits, conventional, rebased, squashed):**
```bash
git fetch origin
git checkout -b feat/PROJ-123-add-oauth

# Make atomic commits with conventional format
git commit -m "feat(auth): add oauth service initialization"
git commit -m "feat(auth): implement oauth callback handler"
git commit -m "test(auth): add oauth flow tests"

git push origin feat/PROJ-123-add-oauth

# Before PR: rebase and squash if needed
git fetch origin
git rebase origin/main

# Squash merge via PR (git will handle this)
# After merge:
git checkout main
git pull origin main
git branch -d feat/PROJ-123-add-oauth
git push origin --delete feat/PROJ-123-add-oauth
```
