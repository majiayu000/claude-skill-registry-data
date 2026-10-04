---
name: gitops-engineer
description: >
  Enterprise GitOps — branching strategies, release management, semantic
  versioning, conventional commits, and git automation.
  Trigger: When designing branching strategy, automating releases, configuring hooks, or managing versioning.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: gitops-engineer

Enterprise GitOps. Git is the single source of truth.

## Trigger

- Designing a branching strategy for a project
- Automating releases and changelogs
- Configuring git hooks (pre-commit, pre-push)
- Defining semantic versioning and conventional commits
- Resolving merge conflicts or history issues

## Workflow LEND

1. ANALYZE
   ├── Stack: GitHub, GitLab, Gitea
   ├── Team: solo, 2-5, 5+ people?
   ├── Current strategy: trunk-based, GitHub Flow, Git Flow?
   └── Releases: manual, automatic, semver?

2. OFFER (Senior Menu)
   ├── A) GitHub Flow — branches per feature, PRs to main, simple and effective
   ├── B) Trunk-based — direct commits to main with feature flags, ideal for CI/CD
   └── C) Git Flow — develop/main, release branches, hotfixes, for long cycles

3. CHOOSE → user confirms

4. EXECUTE
   ├── Branch protection: require PRs, approvals, status checks, linear history
   ├── Hooks: pre-commit (lint + format + secrets), commit-msg (conventional)
   ├── Release: semver tags, automatic changelog (git-cliff or semantic-release)
   ├── Conventional commits: feat, fix, chore, docs, refactor, test, style
   ├── Merge strategies: squash (trunk-based), merge commit (Git Flow), rebase (clean history)
   ├── CI: GitHub Actions to validate commits and PRs
   └── Documentation: CONTRIBUTING.md with workflow explained

5. VERIFY
   ├── Branch protection rules are active
   ├── Hooks run without errors
   └── A test release generates the changelog correctly

- [ ] Save decisions and changes to Engram (mem_save)
- [ ] Check if README, AGENTS.md, or ARCHITECTURE.md need updating
- [ ] If docs changed → update them in the same PR/commit
