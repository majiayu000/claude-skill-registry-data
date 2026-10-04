---
name: to-pr
description: Use when the user types `/to-pr`, asks to prepare or open a PR, or wants Claude to standardize branch checks, validation, a suggested commit message, and draft PR creation for this repo. Follows the repo PR template, `develop` base branch, and the repo-root Python quality gate (ruff, black, pytest).
version: "1.0.0"
---

# To PR

Prepares and opens a GitHub pull request for this repository using the documented workflow,
without creating commits or pushing branches.

## When to use

- When the user types `/to-pr`
- When the user asks Claude to prepare, publish, or open a PR
- After the implementation is complete and ready for review handoff

## Preconditions

- Run git and `gh` commands from the repo root.
- Run validation from the repo root (Python project, no subfolder build step).
- Do not create commits in this skill.
- Do not push branches in this skill. If the branch is not already on `origin`, stop and ask
  the user to push it manually.
- A linked GitHub issue is **not required** — this is a solo, course-scale project (see
  `docs/INDEX.md`). If an issue exists, link it; if not, proceed without one.

## Workflow

1. Inspect scope first with `git status -sb` and `git diff --stat`. If the worktree includes
   unrelated changes, do not stage everything; ask which files belong in scope.
2. Check the branch. Never open a PR from `develop` or `main`. Branch names should follow
   `feature/...`, `fix/...`, `chore/...`, `docs/...`, `refactor/...`, or `test/...`, optionally
   with an issue number (see `CONTRIBUTING.md`).
3. If a related issue exists and its context is unclear, fetch it with
   `gh issue view <number> --comments` before drafting the PR summary.
4. Verify GitHub CLI readiness with `gh --version` and `gh auth status`. If auth is missing,
   stop and ask the user to authenticate.
5. Run the required local quality gate from the repo root:

```bash
ruff check .
black --check .
pytest
```

6. Generate a suggested commit message using this repo's convention (see
   `CONTRIBUTING.md`): a single line, `type(scope): description`, no body unless the user
   asks for one, and never a `Co-Authored-By: Claude` trailer.
7. Confirm the branch is already ready for review. If there are uncommitted changes or
   unpushed commits that should be part of the PR, stop and ask the user to handle
   commit/push manually before continuing.
8. Open a draft PR targeting `develop` with `gh pr create --draft --base develop`.
9. Use `.github/PULL_REQUEST_TEMPLATE.md` for the PR body and fill every section that
   applies. If there's no linked issue, write `Not applicable` under Related Issue instead of
   leaving it blank or fabricating one.
10. Keep the PR text high-signal. Prefer short factual statements tied to the actual diff.
    Avoid filler, vague benefits, generic AI phrasing, and claims like "improves
    maintainability" unless the PR body explains exactly how.
11. After creation, report the suggested commit message, branch name, validation status, and
    PR URL.

## Safety rules

- Never stage unrelated user changes silently.
- Default to a draft PR unless the user explicitly asks for ready-for-review.
- Never create a commit or push a branch from this skill.
- If `ruff`, `black --check`, or `pytest` fail, stop and fix or report the failures before
  opening the PR.
- Never pad the PR description with low-information text just to make sections look fuller.
