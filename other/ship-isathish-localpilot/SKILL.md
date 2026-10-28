---
name: ship
description: Finish and hand off a change — final verification, tidy the diff, write a conventional commit message / PR title and description / changelog entry, and (only with explicit permission) commit, push or open the PR. USE WHEN the user says "commit", "write a commit message", "open a PR", "describe my changes", "prepare for merge", "wrap up", "ship", "release notes".
---

# Ship

Goal: a clean, reviewable change with an honest description — and no irreversible git action without the user saying so.

## 1. Know exactly what is changing
- `run_command`: `git status --short`, `git diff --stat`, then `git diff` (and `git diff --cached` if things are staged). Read the diff, not your memory of it.
- Spot leftovers: debug logging, commented-out code, TODOs you introduced, stray files (`.DS_Store`, editor configs, large binaries, `.env`), formatting-only churn in unrelated files. Fix or exclude them. Never commit secrets — if a key/token is in the diff, stop and tell the user.
- Unfamiliar modified files you didn't touch may be another person's or session's work in progress: leave them alone and don't stage them.

## 2. Final verification
- `get_diagnostics` on changed files; run lint/typecheck/tests/build using the project's commands; for UI, `browser_inspect` the affected screen once. Fix failures before describing the change as done.
- Update the changelog (`Unreleased` section) and docs if behaviour or usage changed.

## 3. Write the message
Conventional Commits, imperative mood, ≤ 72-char subject, body explains *why* and anything non-obvious:
```
feat(settings): patch model-install progress in place

A full re-render on every pull-progress tick restarted CSS animations and
reset scroll, which read as the page blinking. Progress bars and labels now
update via data-job attributes; a full render only happens when a job's
status changes.

Closes #123
```
Types: feat · fix · refactor · perf · test · docs · build · ci · chore. Scope = module/area. Breaking changes: `!` after type and a `BREAKING CHANGE:` footer.

PR description template:
```markdown
## What
One paragraph in user terms.
## Why
Problem / motivation, link to issue or spec.
## How
Key design points, notable trade-offs, anything reviewers should look at first.
## Testing
Commands run and results; manual steps; screenshots for UI.
## Checklist
- [ ] Tests added/updated · [ ] Docs/changelog · [ ] No secrets · [ ] Backward compatible (or migration noted)
```

## 4. Act only with permission
- Show the proposed commit message / PR text in chat. **Do not** run `git add -A`, `git commit`, `git push`, `gh pr create`, tag, or amend unless the user explicitly asked for that action in this conversation (`ask_user` if unsure). Never force-push, rewrite published history, or bypass hooks (`--no-verify`).
- When asked to commit: stage only the files that belong to this change (`git add <paths>`), commit with the message, and report the hash (`git log -1 --oneline`). When asked to open a PR and `gh` is available: push the branch and `gh pr create --title … --body …`; print the URL.

## 5. Report
- The commit/PR text, verification performed, and any follow-ups (e.g. "needs a screenshot", "docs page X should mention Y").
