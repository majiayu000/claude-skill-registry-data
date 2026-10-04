---
name: pr
description: Commit pending changes, push, and create a pull request with proper description
argument-hint: "[title]"
---

# Create Pull Request

Commit any pending changes in logical groups, push the branch, then create a GitHub pull request with comprehensive description.

## Step 1: Commit All Pending Changes

Delegate to the `skills:commit-all` command to turn any uncommitted work into logically grouped commits:

```
Skill(skill="skills:commit-all")
```

If the working tree is already clean, this is a no-op - proceed directly to Step 2.

## Step 2: Gather PR Context (Parallel)

Launch FOUR parallel agents simultaneously to collect all information at once:

**Agent 1 — Git Status**:
```bash
git status
```
Confirm the working tree is clean after Step 1.

**Agent 2 — Commit History**:
```bash
git log main..HEAD --oneline
git log main..HEAD --format='%h %s%n%b'
```
Capture all commits that will be in the PR with their full messages.

**Agent 3 — Diff Summary**:
```bash
git diff main...HEAD --stat
git diff main...HEAD
```
Capture the full diff and file-level summary of all changes.

**Agent 4 — Fetch Remote**:
```bash
git fetch origin
```
Ensure remote refs are up to date for comparison.

## Step 3: Analyze and Sync (Parallel)

Once Step 2 completes, launch TWO parallel agents:

**Agent 1 — Check Remote Sync**:
```bash
git rev-list --left-right --count origin/main...HEAD
```
Determine whether the branch has diverged from origin/main.

**Agent 2 — Analyze Changes for PR Description**:
Using the commit history and diff from Step 2, produce:
- A concise summary (2-4 bullet points) of what changed and why
- A detailed changes list grouped by area (backend, frontend, tests, config)
- A PR title in the PR Title Format below if `$ARGUMENTS` was not provided
- Test plan based on what was modified

## Step 4: Push and Create PR

Push the branch to remote:

```bash
git push -u origin $(git branch --show-current)
```

Then create the PR:

```bash
gh pr create --title '<title>' --body-file - <<'EOF'
## Summary
- Bullet point summary of changes

## Changes
- Detailed list of what changed

## Test plan
- [ ] Tests pass locally
- [ ] Manual testing completed
- [ ] No regressions

## Screenshots (if UI changes)
N/A
EOF
```

## PR Title Format

Use the commit subject format from `skills:commit-all`, `type(scope): subject`, with the type and scope of the PR's main change:
- `feat(preferences): add user preferences endpoint`
- `fix(auth): handle expired sessions`
- `refactor(billing): extract invoice totals`
- `feat(api)!: remove v1 routes` (`!` marks a breaking change)
- `chore: update dependencies` (repo-wide, so no scope)

## If `$ARGUMENTS` Provided

Use as PR title. Otherwise, generate from commits.

## Output

Return the PR URL when complete.

## Checklist Before PR

- [ ] All tests pass
- [ ] Code is formatted and linted (PHP: `composer lint`, Kotlin: ktlint, Rust: `cargo fmt` + `cargo clippy -- -D warnings`, JS/TS: Prettier)
- [ ] No secrets in code
- [ ] SDK regenerated if API changed
