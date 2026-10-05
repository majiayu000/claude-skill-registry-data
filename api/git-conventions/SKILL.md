---
name: git-conventions
description: Apply when committing, branching, or opening a pull request. Conventional commit format, branch naming, PR scope.
license: MIT
version: 1.0.0
tokens_target: 650
triggers:
  - git commit
  - branch
  - pull request
loads_after: []
supersedes: []
---

# Sub-Skill: Git & Workflow Conventions
<!-- target: ~650 tokens (real tiktoken count) | 15 rules -->

**Purpose:** Consistent commit history, clean branches, no merge conflicts through discipline.
Rules that work in teams of 2–20 developers.

---

## Rules

### Commit Messages (Conventional Commits)

1. **Format:** `<type>(<scope>): <description>` — always lowercase, no period at the end.
   - Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `ci`
   - Example: `feat(auth): add JWT refresh token rotation`
2. **Description in imperative mood.** `add feature` not `added feature` or `adds feature`.
3. **Scope is the affected module name.** `fix(user-service): handle null email` — not `fix(backend)`.
4. **Mark breaking changes with `!`.** `feat(api)!: remove deprecated v1 endpoints`
5. **Body for non-obvious changes.** Explains the *why*, not the *what*.

### Branching

6. **Branch names:** `<type>/<ticket-id>-<short-description>` — e.g. `feat/PROJ-123-user-export`.
7. **Feature branches live max. 2 days.** Longer → rebase daily onto `main`.
8. **No direct push to `main` or `develop`.** Always through a pull request.
9. **Delete branch before PR merge.** Clean up merged branches from remote.

### Pull Requests

10. **PR title = commit message of the squash commit.** Consistency between PR and git log.
11. **Max. 400 lines diff per PR.** Larger → split. Reviewers cannot meaningfully review more than 400 lines.
12. **Self-review before opening a PR.** Read through once yourself, fix obvious mistakes.

### Merge Strategy

13. **Squash-merge for feature branches.** Clean linear history on `main`.
14. **Merge commit for release branches.** So release points remain visible.
15. **`git rebase -i` before PR for clean commits.** Squash WIP commits together.

---

## Why This Sub-Skill Earns Stars

The agent automatically creates correct commit messages and branch names.
No manual corrections, no discussions in review about formatting.
