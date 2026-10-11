---
name: git-workflow
description: Git — branching, commits, PR workflow, merge, release tagging.
---

## Detect First

Before applying any convention, run:

```bash
git log --oneline -10
```

Look for the existing pattern in the project history:
- **Conventional Commits**: `feat:`, `fix:`, `chore:`, `docs:` prefixes
- **GitHub Flow**: plain imperative sentences, no prefix
- **GitFlow**: `feature/`, `release/`, `hotfix/` branch names in merge commits
- **Trunk-based**: short-lived branches, frequent merges to main, feature flags

Always follow the project's established pattern. Only fall back to Conventional Commits if no pattern is detectable.

---

## Branch Naming

| Prefix | Purpose | Lifetime | Merge target |
|---|---|---|---|
| `feature/*` | New functionality | Days to 1 sprint | `main` / `develop` |
| `fix/*` | Non-urgent bug fix | Hours to days | `main` / `develop` |
| `hotfix/*` | Urgent production fix | Hours | Release tag + `main` |
| `release/*` | Release stabilization | Days | `main` + tag |
| `chore/*` | Tooling, deps, config | Hours to days | `main` / `develop` |

- Branch names: lowercase, hyphens only, no spaces (e.g., `feature/user-auth-refresh`).
- Keep names short but descriptive; include a ticket ID when the project uses one (e.g., `fix/PROJ-123-null-pointer`).

---

## Commit Messages

Follow `skills/shared/conventional-commits/SKILL.md` for format details. Key rules:

- One logical change per commit — never mix a feature and a bug fix in the same commit.
- Subject line: ≤ 72 characters; imperative mood ("add", not "added" or "adds").
- Body (optional): explain *why*, not *what* — the diff already shows what changed.
- No AI attribution lines (`Co-Authored-By: Claude`, `Generated with …`).

---

## Pull Request Rules

- **Title**: `<type>: <what changed> (<why, if not obvious>)` — mirrors the squash commit that will land on main.
- **Description**: include a short summary, test plan (checklist), and a link to the ticket or issue.
- **No WIP PRs merged to main**: use Draft PRs for work in progress; convert to ready only when CI is green.
- **Self-review first**: read your own diff before requesting review.
- **Keep PRs small**: prefer multiple focused PRs over one large one; large PRs get shallow reviews.

---

## Merge Strategy

| Scenario | Strategy | Reason |
|---|---|---|
| Feature / fix branch → main | **Squash merge** | Clean, linear history; one commit per feature |
| Release branch → main | **Merge commit** | Preserves full release history |
| Hotfix → main | **Merge commit** | Traceability for post-incident review |
| Sync main → long-lived branch | **Rebase** | Avoids noisy merge commits mid-branch |

- Never force-push to `main` or `master`.
- Delete the source branch after merge.

---

## Release Tagging

- Format: `vMAJOR.MINOR.PATCH` (semantic versioning).
- Tag only from `main` after CI passes.
- Annotated tags preferred: `git tag -a v1.2.0 -m "Release v1.2.0"`.
- Push tag explicitly: `git push origin v1.2.0`.

| Change type | Bump |
|---|---|
| Breaking change | MAJOR |
| New feature, backward-compatible | MINOR |
| Bug fix, patch, docs | PATCH |

---

## Hotfix Flow

1. `git checkout -b hotfix/v1.2.1 v1.2.0` — branch from the affected release tag, not from main.
2. Apply the minimal fix; commit.
3. Tag: `v1.2.1`.
4. Merge back to `main` with a merge commit.
5. Delete the hotfix branch.

---

## Protected Branch Requirements

`main` and `master` must enforce:
- Pull request required (no direct push).
- At least 1 approval from a reviewer who did not author the PR.
- All CI checks must pass before merge.
- No force-push.
- No deletion.
