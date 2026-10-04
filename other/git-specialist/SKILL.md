---
name: git-specialist
description: Git workflows, branching strategies, repository management, and conflict
  resolution. Use when asked to set up a branching strategy, resolve a merge conflict,
  clean up git history (rebase, squash), configure git hooks, set up a monorepo structure,
  recover from a bad commit or accidental push, or write a .gitignore file.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: operations
  tags:
  - git
  - version-control
  - branching
  - merge-conflicts
  - gitflow
  - trunk-based
---

# Git Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `resolve this merge conflict`, `git branching strategy`, `rebase`.
- The requested work fits this skill's lane: Branching strategies, merge conflicts, git history cleanup, git hooks, monorepo git config.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: CI/CD pipeline configuration (use cicd-specialist).

## First actions
1. `Bash('git log --oneline -20')` and `Bash('git branch -a')` — understand current repo state
2. `Glob('**/.gitignore', '**/.gitattributes', '**/.githooks/**')` — find git config files
3. For conflict resolution: `Bash('git status')` and `Bash('git diff')` to understand the full conflict scope

## Decision rules
- For new projects: recommend trunk-based development unless the team has specific reasons for gitflow
- For history cleanup: never rebase commits that have been pushed and shared — only local commits
- For `git push --force`: always recommend `--force-with-lease` instead

## Output contract
- For branching strategy: document the chosen workflow, branch naming conventions, and merge rules
- For conflict resolution: show the resolved file content; explain what each side changed and why the resolution is correct

## Constraints
- NEVER suggest `git push --force` on main/master branches
- NEVER suggest force-pushing shared branches without warning about team impact

## Reference
- `references/legacy-agent.md`: branching strategies, git hooks, monorepo patterns, history rewriting, recovery procedures
