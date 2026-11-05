---
name: pr
description: Create a pull request with proper branch, description, and labels
argument-hint: "[base-branch]"
allowed-tools: "Bash(git *), Bash(gh *), Bash(npm *), Read, Grep"
---

# Create Pull Request

## Branch naming

If not already on a feature branch, create one from the commit history:
- Features: `feature/<short-description>`
- Fixes: `fix/<short-description>`
- Docs: `docs/<short-description>`
- Refactors: `refactor/<short-description>`

## Pre-flight checks

1. Run `npm test` — unit tests must pass
2. Run `npx wp-scripts lint-js` on changed JS files
3. Run `composer lint` if PHP files changed
4. Check `git diff main...HEAD` to understand full scope of changes

## Create the PR

Base branch: `$ARGUMENTS` (default: `main`)

Use `gh pr create` with:

- **Title**: under 70 chars, imperative mood (e.g., "Add cron-list ability" not "Added cron-list ability")
- **Body** format:

```
## Summary
<2-4 bullet points describing what changed and why>

## Changes
<list of files/areas affected>

## Testing
- [ ] Unit tests pass (`npm test`)
- [ ] Ability tests pass (`npm run test:abilities -- --file tests/abilities/core-abilities.test.js`)
- [ ] JS lint clean (`npm run lint:js`)
- [ ] PHP lint clean (`composer lint`)
- [ ] Manually tested in browser (if UI changes)

## Notes
<any migration steps, breaking changes, or reviewer guidance>
```

- **Labels**: add if available — `enhancement`, `bug`, `documentation`, `breaking-change`
- Push branch with `-u` flag before creating PR

## After creating

Print the PR URL so the user can review it.
