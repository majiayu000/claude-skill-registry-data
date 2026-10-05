---
name: park
description: Commit and push the session's work to a branch, then return to a clean main. Nothing merges and nothing deploys. Use when asked to park this, shelve this, or set an experiment aside for later.
icon: local_parking
displayDescription: "Shelves an experiment: commits the session's work, pushes it to a remote branch, then returns to a clean main. Nothing deploys and nothing merges; the report names the branch so the work is easy to resume later."
invoke: ["park this","shelve this","set this aside","park it"]
---

# park

Save the session's work to a remote branch, then step off it and return to a clean `main`. Same safety net as `checkpoint`, different end state: the session ends back on `main`, with the experiment shelved under a named branch.

## When invoked

Use this skill when asked to set the current work aside — phrases like "park this", "shelve this", "set this aside". To save and *keep* working on the branch, that's `checkpoint`; to make the work live, that's `ship`.

**If asked to "merge and push"**: that's the retired ambiguous skill name, and it now maps onto more than one verb. Confirm the intended end state before doing anything: `ship` (merge into `main`, push, deploy), `checkpoint` (push the branch, keep working), or `land` (combine several pieces of pending work into a local `main`, pushing nothing).

## Instructions

1. **Get the work onto a branch**: `git branch --show-current`.
   - **On `main`**: create a branch named for the work, not the date — `git checkout -b wip/<short-topic>` (uncommitted changes ride along). Never commit to `main` from this skill.
   - **On a work branch already**: stay on it.

2. **Survey the tree**: run `git status --short` and classify every entry as in scope (this session's work) or out of scope. **Never run `git add -A`, `git add .`, or `git add` on a directory** — always add explicit file paths. Note that out-of-scope untracked files are untouched by branch switches — they will still be sitting in the tree after the return to `main`; name them in the report.

3. **Quick check, not the full verify**: run `npm run lint`; if the session touched `website/`, also run `npm --prefix website run lint` (root ESLint ignores the website workspace). A failure does not block the park — a shelved experiment is allowed to be mid-mess — but it goes in the report so resuming starts with eyes open.

4. **Commit in the repo's conventional style** (`feat(scope):`, `fix(scope):`, with a short why) — a parked branch may later merge to `main` via `ship`, so its commits are real history.

5. **Push the branch**: `git push -u origin <branch>`. Pushing a branch publishes nothing.

6. **Return to main**: `git checkout main`, then confirm with `git status --short` that the tree is clean (out-of-scope untracked files excepted).

7. **Report**:
   - The branch name — this is the resume handle; say it plainly ("to pick this back up, ask to resume `wip/<topic>`")
   - Each commit (hash + subject), lint status, files left out and why
   - Confirmation the session is back on a clean `main` and nothing deployed

## Guardrails

- Never touch `main`: no commits to it, no merges into it, no pushes of it
- Never force-push, never rewrite pushed history
- Never commit `ga-analysis/output/`, `ga-analysis/service-account.json`, `.env*`, or anything credential-shaped — even if explicitly staged by mistake
- If there is nothing in scope to commit, say so and stop — don't invent a branch
- Never delete the parked branch — it is the only copy of the shelved work
