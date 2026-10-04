---
name: pr
description: Open a pull request with a strict minimal body — Summary (2-4 sentences) plus an ASCII Flow diagram plus `Closes #<issue>`. No changes list, no tests section, no breaking-changes section. Works in dirty repos by committing only PR-relevant changes, creates a branch from trunk without asking, pushes the branch, watches GitHub Actions until they terminate, then hands off to /code-review.
---

# /pr

Before rendering user-facing output, read `../_shared/plain-output.md` and `../_shared/ascii-diagrams.md`.

Open a pull request with a minimal, opinionated body.

## Preconditions

1. **Remote exists.** `git remote get-url origin` must succeed.
2. **`gh` authenticated.** `gh auth status` must succeed.
3. **No unresolved conflicts.** If `git diff --name-only --diff-filter=U` prints anything, stop and tell the user to resolve conflicts first.
4. **Dirty repos are allowed.** Do not require a clean working tree. Preserve unrelated changes by staging and committing only files that belong to this PR.

## Process

1. Capture the starting branch and working tree state:

```bash
START_BRANCH="$(git branch --show-current)"
git status --short
```

2. If `START_BRANCH` is `main`, `master`, or `trunk`, create a PR branch without asking. Derive the name from the issue number when known, otherwise from the task title or timestamp:

```bash
git switch -c "<type>/<short-kebab-task>"
```

Do not stash first; the working tree moves with the new branch. This keeps unrelated dirty files present but uncommitted.

3. Find the linked issue number. Options, in order:
   - If the user passed an explicit `--issue <n>` or `<n>` argument, use it.
   - Otherwise, scan recent commit bodies (`git log -20 --format=%B`) for `Refs #<n>`, `Fixes #<n>`, or `Closes #<n>`. Use the most common match.
   - Otherwise, scan the current branch name for an issue number.
   - If still not found, ask the user for the issue number.

4. Fetch the issue title and labels: `gh issue view <n> --json title,labels`. Use them as input, not as the PR title directly.

5. Build a PR title that satisfies the repository's `pr-title` / `commitlint` rules:
   - Format: `type(scope): subject` or `type: subject`.
   - Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
   - Subject must be lowercase.
   - Subject must be at most 72 characters.
   - Prefer the issue title's existing Conventional Commit title if it already passes.
   - Otherwise infer the type from the issue labels, issue title, or shipped change; default to `fix` only for bug repairs and `feat` only for user-visible behavior, otherwise use `chore`.
   - Do not include `#<issue>` in the title; the body owns `Closes #<n>`.

6. Validate the title before creating the PR. If the repository has commitlint installed, run it against the title from the repo root:

```bash
printf '%s\n' "$PR_TITLE" | bunx commitlint
```

If validation fails, fix the title and rerun validation. Do not open a PR with a title that fails `commitlint`.

7. Commit only the PR-relevant changes if needed:
   - Inspect `git status --short` and `git diff --stat`.
   - Decide which paths belong to this PR from the user request, issue, and changes you made.
   - Stage only those paths with explicit pathspecs: `git add -- <path>...`.
   - Never use `git add -A`, `git add .`, or `git commit -a` in a dirty repo.
   - Leave unrelated modified/untracked files unstaged.
   - If there are staged PR-relevant changes, commit them with a Conventional Commit message that references the issue when available, e.g. `fix(pr): handle dirty worktrees\n\nRefs #<n>`.
   - If there are no staged changes but the branch already has commits to push, continue.
   - If there are no staged changes and no branch commits, stop: there is nothing to open.

8. Build the PR body using the template in `REFERENCE.md`:
   - `## Summary` — 2-4 sentences. What and why. Written against the issue's problem statement.
   - `## Flow` — an ASCII diagram showing the runtime or user flow introduced by this PR (see `../_shared/ascii-diagrams.md`). Required.
   - Final line: `Closes #<n>`.
   - **Nothing else.** No changes section, no test plan, no screenshots block, no rollout plan.

9. Write the body to a temp file (the heredoc keeps the ASCII diagram intact).

10. Push the branch:

```bash
git push -u origin "$(git branch --show-current)"
```

11. Open the PR, or update the existing PR for this branch if one already exists:

```bash
if gh pr view --json number,url >/tmp/current-pr.json 2>/dev/null; then
  gh pr edit --title "$PR_TITLE" --body-file "<tmpfile>"
else
  gh pr create --title "$PR_TITLE" --body-file "<tmpfile>"
fi
```

Do not create duplicate PRs for the same branch.

Fallback create command:

```bash
gh pr create --title "$PR_TITLE" --body-file "<tmpfile>"
```

12. Capture the PR URL. Delete the temp file.

13. **Wait for GitHub Actions.** Do not hand off until checks terminate. The PR is not complete until all checks pass.

```bash
gh pr checks "<pr-number>" --watch --fail-fast
```

- `--watch` blocks until every check finishes (success, failure, cancelled, or skipped).
- `--fail-fast` returns non-zero the moment any check fails, so you surface failures promptly instead of waiting for the rest.
- If `gh pr checks` returns "no checks reported on the <branch> branch", there are no workflows — treat this as a pass and continue.
- If any check fails, stop and surface:
  1. The failing check name(s).
  2. The last ~30 lines of the failing job log via `gh run view <run-id> --log-failed` (find `run-id` with `gh pr checks <n> --json link -q '.[]|select(.state=="FAILURE")|.link'`).
  3. Tell the user: *"CI failed. Address the failure before running `/code-review` — either fix the underlying bug in this branch, or if the failure is unrelated infra, explicitly say so and I will proceed."*
- Do not retry failing checks automatically. Do not approve, dismiss, or close the PR.

## Forbidden sections (do not add these even if the user asks offhand)

- "Changes" / "Files changed" — the diff is visible; do not enumerate it.
- "Tests" / "Test plan" — verification lives in the issue.
- "How to verify" / "Screenshots" — out of this body's scope.
- "Breaking changes" — if there are any, mention them in the Summary prose.
- "Checklist" — no ceremony.
- Emoji headers.

## Output

Use Plain Senior output with the PR URL and final CI status (`all-pass`, `none-configured`, or `failed`).

````markdown
## Decision
PR opened or updated: <url>.

## Why
CI status: <all-pass | none-configured | failed>.

## Example
```bash
gh pr checks "<pr-number>" --watch --fail-fast
```

## Risk
<failed check summary, no checks configured, or "None known">

## Next
<handoff line below>
````

Only proceed to the handoff when CI has terminated cleanly (all-pass or no-checks). If CI failed, do NOT print the handoff — print the failure summary and stop.

On success, end with exactly this line and stop:

> PR opened: <url>. CI green. Run `/code-review` to fan out reviewers and post findings to the PR.
