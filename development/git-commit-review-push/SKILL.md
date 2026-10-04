---
name: git-commit-review-push
description: Commit current changes with conventional commits format, append the /ai-review trigger to the final commit, and push to remote repository. Use when committing and pushing changes so the pushed PR gets a full AI review.
allowed-tools:
  - Bash(git add:*)
  - Bash(git branch:*)
  - Bash(git commit:*)
  - Bash(git log:*)
  - Bash(git push:*)
  - Bash(git status:*)
models:
  claude: sonnet      # medium-complexity; branch rename logic and upstream tracking require broader reasoning
  copilot: auto
  codex: gpt-5.4
---

# Git Commit, Review-Trigger, and Push

Commit current changes using conventional commits format, embed the `/ai-review` full-review trigger in the last commit, and push to the remote repository.

## Workflow Steps

1. Check if there are any changes to commit using `git status --porcelain`
2. If there are changes, analyze the diff and group it into **logical units of work** (chunks). Commit each chunk separately with a [Conventional Commits](https://www.conventionalcommits.org) message — `<type>[optional scope]: <description>` with type one of `feat`/`fix`/`chore`/`docs`/`refactor`/`test`/`ci`/`perf`/`build`; subject lowercase, imperative, no trailing period, ≤ 72 chars:
   - If a commit message was provided as an argument, use it (single-chunk commit)
   - Otherwise generate an appropriate conventional commit message per chunk from the staged diff
   - Initialize `commit_made_in_step_2=false` before chunking, and set it to `true` once Step 2 creates at least one chunk commit so Step 4's code block can guard the trigger check explicitly
3. **Review trigger (mandatory)**: the **last** chunk commit — or the only commit when there is a single chunk — MUST end with `/ai-review` as the final line of the commit message body. The review gate (`pipeline-code-review-report.yml`) greps PR commit messages for `/ai-review` and forces a full PR review when found. Keep the subject line clean; the trigger goes in the body:

   ```
   feat(auth): add user authentication system

   /ai-review
   ```

   Earlier chunk commits must NOT carry the trigger — only the final one.
4. If a commit was made in step 2, verify the trigger is the final non-empty line of the
   commit body before pushing. Skip this check for merge commits — detect them via
   `git log -1 --format=%P | wc -w` > 1 (more than one parent) or by a `Merge` subject
   prefix — because `git log -1 --format=%b` returns the merged-branches list, not a
   usable commit body. The outer "If a commit was made in step 2" guard already excludes
   the no-commit path. The regex tolerates trailing whitespace / CRLF, unlike a strict string compare:

   ```bash
   if [ "${commit_made_in_step_2+x}" != "x" ]; then
      echo "Set commit_made_in_step_2=true when Step 2 created commit(s), false otherwise, before running Step 4." >&2
      exit 1
   fi
   if [ "$commit_made_in_step_2" = "true" ]; then
      # Merge commits (>1 parent, or a "Merge…" subject) have no usable %b body — skip the check entirely.
      subject="$(git log -1 --format=%s)"
      if [ "$(git log -1 --format=%P | wc -w)" -gt 1 ] || [[ "$subject" == Merge* ]]; then
         echo "Merge commit detected — skipping /ai-review trigger check."
      else
         git log -1 --format='%b' | awk 'NF { last=$0 } END { exit (last ~ "^[[:space:]]*/ai-review[[:space:]]*$") ? 0 : 1 }'
      fi
   fi
   ```

   If the check fails, echo the full commit message (helps diagnose missing-vs-misplaced trigger — the check passes only when `/ai-review` is the last non-empty line, optionally followed by trailing whitespace):

   ```bash
   git log -1 --format='%B'
   ```

   then amend the final commit to add the trigger. Reuse the **full** existing message (`%B` — subject, body, and any `Co-authored-by:` / `Signed-off-by:` / `Refs:` trailers) and append the trigger as a new paragraph; do **not** rebuild from `%s`, which would drop the body and every trailer. The check above only fails when `/ai-review` is absent from the final line, so appending is safe:

   ```bash
   git commit --amend -m "$(git log -1 --format='%B')" -m "/ai-review"
   ```
5. If there are no changes to commit, skip to step 6
6. **If `--issue <number>` was passed** — rename the local branch before pushing (see Branch Rename below)
7. Push to remote repository using `git push` (use `git push --set-upstream origin <new-branch>` if the branch was renamed)
8. If there's nothing to commit or push, report this to the user and continue gracefully (this is not an error)

**Note**: This command ONLY commits and pushes. It does not create or update PRs.

## Branch Rename (when `--issue <number>` is passed)

This step enforces the branch naming convention (same type vocabulary as Conventional Commits):

```
<type>/<issue>-short-description
```

**How to derive the new branch name:**

1. **`<type>`** — take the type from the conventional commit just made (e.g. `feat`, `fix`, `chore`). If the branch already has a conforming name with the correct type, use that type.
2. **`<issue>`** — the number passed via `--issue`.
3. **`short-description`** — generate a concise, lowercase, hyphen-separated description (3–6 words) that summarises what was changed. Derive it from the commit message subject or the staged diff — do not reuse the current branch name verbatim.

**Execution:**
```bash
git branch -m <new-branch-name>     # rename local branch
```
Then push with upstream tracking:
```bash
git push --set-upstream origin <new-branch-name>
```

**Constraints:**
- Only rename if the current branch name does NOT already conform to `<type>/<issue>-*` for the given issue number.
- If the current branch already matches (e.g. `feat/42-add-auth`), skip the rename and push normally.
- Tell the user the old and new branch names when a rename happens.

## Arguments

- Optional: pre-defined commit message (if not provided, will analyze changes and generate appropriate conventional commit message). The `/ai-review` trigger line is appended to the final commit regardless of whether the message was provided or generated.
- `--issue <number>` — renames the local branch to `<type>/<number>-short-description` before pushing, ensuring branch naming consistency

## Usage Examples

```
/git-commit-review-push
/git-commit-review-push feat: add user authentication system
/git-commit-review-push --issue 42
/git-commit-review-push --issue 42 feat: add user authentication system
```
