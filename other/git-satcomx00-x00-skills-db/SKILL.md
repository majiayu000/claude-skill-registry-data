---
name: git
description: Git workflow best practices — conventional commits, branching strategy, rebase/merge patterns, and commit hygiene for clean project history.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
---

# git

Git workflow best practices — conventional commits, branching strategy, rebase/merge patterns, and commit hygiene for clean project history.

## Instructions

Follow these Git workflow practices when working in this repository:

### Conventional Commits

Always write commit messages using the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat` – new feature
- `fix` – bug fix
- `docs` – documentation only
- `style` – formatting, missing semicolons, etc. (no logic change)
- `refactor` – code change that is neither a fix nor a feature
- `perf` – performance improvement
- `test` – adding or fixing tests
- `chore` – build process, tooling, dependency updates
- `ci` – CI/CD configuration changes
- `revert` – revert a previous commit

**Examples:**
```
feat(auth): add OAuth2 login with GitHub
fix(api): handle null pointer when user profile is missing
chore(deps): bump axios from 1.4.0 to 1.6.0
```

### Branching Strategy

Use **trunk-based development** with short-lived feature branches:

- `main` – production-ready code, always deployable
- `feat/<ticket-id>-<short-description>` – new features
- `fix/<ticket-id>-<short-description>` – bug fixes
- `chore/<short-description>` – maintenance tasks
- `release/<version>` – release preparation (if needed)

Keep branches small and short-lived (< 2 days ideally). Merge via pull request with at least one review.

### Commit Hygiene

- **Atomic commits** – each commit should represent a single logical change
- **No WIP commits** – squash work-in-progress commits before merging
- **No secrets** – never commit tokens, passwords, or private keys
- **Sign commits** – use `git commit -S` when GPG signing is required
- **Rebase, don't merge** for feature branches to keep history linear:
  ```bash
  git fetch origin
  git rebase origin/main
  ```

### Useful Aliases

Suggest these aliases for productivity:
```bash
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.st "status -sb"
git config --global alias.undo "reset HEAD~1 --mixed"
```

### Pull Request Rules

- PR title must follow Conventional Commits format
- PR body must describe *what* changed and *why*
- Link to the relevant issue with `Closes #<issue>`
- Keep PRs focused — one concern per PR

## Examples

```bash
# Good commit
git commit -m "feat(cart): add quantity selector to product card"

# Fix with scope and body
git commit -m "fix(checkout): prevent double-submit on payment form

Debounce the submit handler to avoid duplicate charges when the user
clicks the button multiple times before the API responds.

Closes #142"

# Create a feature branch
git checkout -b feat/123-add-dark-mode

# Rebase before opening PR
git fetch origin && git rebase origin/main

# Squash last 3 commits before merge
git rebase -i HEAD~3
```

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [Pro Git Book](https://git-scm.com/book/en/v2)
