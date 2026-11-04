---
name: ship-branch
description: >-
  Commit, push and open a PR the way this repo does it: feat/fix/docs/chore branch from main, explicit paths,
  Conventional Commits with the commitlint scopes, PR into main with an honest body, never merge. Use for
  "commit", "push", "open a PR", "ship it", "cut a branch".
---

# Ship a branch

The `.claude/hooks/pre-bash.mjs` guard denies the worst mistakes: pushing to `main`, force-push, skipping
hooks with the no-verify flag, npm/npx/yarn. It asks before `gh pr merge` and production deploys. This skill
is the path that never trips it.

## 0. Where am I?

```bash
git branch --show-current
git status --porcelain
git remote -v
```

- **No remote?** Stop and ask the user to create the GitHub repository (or to give you its URL, or confirm
  `gh repo create <name> --private --source . --push`). Don't create a public repo on your own.
- On `main` with changes → step 1. On a work branch → step 2.

## 1. Cut a branch from main

```bash
git switch -c feat/<area>         # or fix/<area>, docs/<topic>, chore/<topic>
```

`<area>` matches a scope: `pwa`, `ui`, `brand`, `core`, `assistant`, `services`, `a11y`, `i18n`, `e2e`,
`claude`, `tooling`, `docs`, `release` (from `commitlint.config.mjs`). Uncommitted changes come along. If they
are the user's unrelated work, ask before moving them.

## 2. Commit

- Gate first: `pnpm run ci:quality` and the `verify-change` skill for what tests can't prove.
- Stage **explicit paths** (`git add <paths>`), never `git add -A` over someone's work in progress. Check with
  `git diff --staged --stat`.
- One logical change per commit. Conventional Commit, scope = area:

```bash
git commit -m "feat(services): meldunek in three steps" -m "Why, in one or two lines." -m "Co-Authored-By: …"
```

- End the message with the attribution line from the system reminder when one is given.
- If a hook fails (lint-staged, commitlint), fix the cause and commit again. Never skip hooks.

## 3. Push and open the PR

```bash
git push -u origin HEAD
gh pr create --base main --title "<type>(<scope>): <summary>" --body-file <scratchpad>/pr.md
```

PR body, filled in honestly:

```markdown
## Summary

What and why; the user-visible effect; which angle it serves (simpler / convenient / accessible / more
matters).

## Test plan

- [x] only commands you actually ran, with results (`pnpm run ci:quality`, flows, Lighthouse numbers)
- [ ] what was not verified (real device, VoiceOver…)

## Screenshots

390×844 and senior mode for UI changes.

## Guardrails

No official marks; fictional data; disclaimer visible (`pnpm run audit:guardrails`).

## Risk

What could break for the jury (offline, install, links), and how to roll back.
```

End the body with the PR attribution line from the system reminder when one is given.

## 4. After

- Report the PR URL and the CI state (`gh pr checks <n>`).
- **Never merge.** The user merges, and `gh pr merge` asks them anyway. Never force-push. Add a new commit
  instead.
- Deploying the merged `main` to the submission URL is the `competition-submission` skill.
