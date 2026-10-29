---
name: pull-request
description: Create or update a Pull Request with a short bullet-point description tailored to its conventional-commit type (feat, fix, refactor, chore, perf, or trivial). Auto-detects whether to create or update based on branch state, detects type from branch/commits/issues, and fills the matching bundled template. Use when invoking /pull-request, when the user asks to open or update a PR, or after pushing work that needs a PR.
argument-hint: '[create|update] [type|#number] [draft]'
model: sonnet
effort: high
---

# Pull Request

Be extremely concise and sacrifice grammar for the sake of concision. Write the description to be easy to understand and read (3rd grader level language). Clear and concise.

This is a solo personal project, not an enterprise repo. PR bodies are flat bullet lists — no headings, no checklists, no ceremony. Reference shape:

```
- Added the `category` database table to support structured expense management.
- Included snapshot metadata files for database schema versioning.
- Implemented category-based sorting functionality within the expenses view component.
```

## Quick start

```
/pull-request                       # auto-detect: update if PR exists for branch, else create
/pull-request create                # force create (errors if PR exists for branch)
/pull-request update                # force update (errors if no PR for branch)
/pull-request 158                   # update specific PR (number → implies update)
/pull-request feat                  # auto-detect action, force type
/pull-request create feat           # create + force type
/pull-request update 158 fix        # update PR 158 + force type
/pull-request create draft          # create as draft
```

## Workflow

1. **Determine action.**
   - `gh pr view --json number,url` for current branch.
   - PR exists → `update`. No PR → `create`. Bare number arg → `update <n>`. Explicit `create`/`update` overrides.
   - If `gh repo set-default` is unset, surface the error — do not guess the repo.

2. **Identify PR / branch context.**
   - `update`: confirm PR number and base branch (`gh pr view --json baseRefName`).
   - `create`: confirm current branch (`git branch --show-current`); base branch defaults to repo default (`gh repo view --json defaultBranchRef`); check push state via `git rev-parse --abbrev-ref --symbolic-full-name @{u}` (errors when no upstream).

3. **Gather detection signals + propose type.** Skip when the user passed an explicit type override.
   - `git branch --show-current` — check for a conventional-commit prefix (`feat/…`, `fix/…`, `chore/…`, `refactor/…`, `docs/…`, `ci/…`, `build/…`, `style/…`, `test/…`, `perf/…`; `/` or `-` separator).
   - `git log <base>..HEAD --pretty=%s%n%b` — extract conventional-commit prefix and `!` marker from each subject; scan bodies for `BREAKING CHANGE:` footers.
   - For each linked issue (branch regex `^(feat|fix|refactor|chore|docs|ci|build|style|test|perf)[/-](\d+)[-_]` + `Closes #N`/`Fixes #N` references in commits): `gh issue view <n> --json state,labels,title`.
   - **Propose type:**
     - Strong agreement → propose with reasoning, confirm.
     - Conflicting signals → propose best-guess with signal table, confirm.
     - **Zero signal** → "No conventional-commit signals detected" + override list, user picks.
   - Map detected type to template: `docs|ci|build|style|test` → `trivial`.
   - Wait for confirmation before continuing.

4. **Load the matching template.** Read `templates/<type>.md` from this skill's directory. Templates are bundled here for portability — do not read `.github/PULL_REQUEST_TEMPLATE/` or `docs/pr_template.md`.

5. **Gather PR content.**
   - `gh pr diff <n>` (update) or `git diff <base>..HEAD` (create).
   - `gh pr view <n> --json commits` (update) or `git log <base>..HEAD` (create).
   - Read referenced files for context where needed.

6. **Fill the template.**

   **Universal fill rules:**
   - Strip guidance HTML comments (`<!-- ... -->`) before saving the body.
   - No headings. Flat bullets only, max 5, one line each.
   - Plain English, past tense. Say what changed, not how the diff did it.
   - Skip anything obvious from the diff. A 2-bullet PR is fine.
   - When an issue is linked, only note deltas from the issue.
   - Needs a hand-check before merge? Say it in a bullet. No checkboxes.

   **Auto-injections:**
   - **Linked issue.** If branch encodes an issue and `gh issue view <n>` returns `state: OPEN`, put `Closes #<n>` on its own first line, blank line, then bullets. If `CLOSED` or missing, skip and surface in the HITL gate. Update mode: only inject when the existing body has no `Closes #` line.
   - **Multi-issue.** When ≥2 issue references found across commits/branch, inject `Closes #129, #130` (comma-separated).
   - **Breaking changes.** When commits contain `!` after type or `BREAKING CHANGE:` footer, add one bullet: `**Breaking:** <what breaks, what to do>`. No bullet when nothing breaks.

   **Update mode: preserve trailing links.** Read existing body via `gh pr view <n> --json body`. Keep any trailing link line (e.g. `[v0 Session](…)`) — v0 writes it and a rewrite would drop it. Re-append it after the bullets.

   **Create mode: generate title.** Format `<type>: <subject>` or `<type>(<scope>): <subject>` — prefix matches body type. Subject source priority: linked-issue title (strip leading type prefix) → top commit subject (strip prefix) → synthesized from diff (ask user if fallback hit). Scope lifted from commits when consistent across history; omitted when mixed. Length ≤72 chars; truncate subject, never prefix.

7. **Save artifact.**
   - `update`: `thoughts/prs/{number}_description.md` (overwrite if exists).
   - `create`: `thoughts/prs/{branch-slug}_description.md` (slug = branch name with `/` → `-`); rename to `{number}_description.md` after `gh pr create` returns the number.

8. **HITL gate.** Single `y/edit/n`.

   **Update mode:**
   ```
   Filled body saved to thoughts/prs/{number}_description.md.
   Apply to PR #{number}? (y/edit/n)
   ```

   **Create mode:**
   ```
   About to create PR:
     Title:  feat: relay inbound Twilio SMS to action queue
     Base:   main
     Mode:   ready
     Push:   feat/129-twilio-sms-relay → origin (will run git push -u origin)
     Body:   thoughts/prs/feat-129-twilio-sms-relay_description.md

   Confirm? (y/edit/n)
   ```

   `edit` opens the body file (or surfaces the path); title/base/draft are re-prompted inline if the user wants to alter them after editing, then the gate is shown again. Default ready in create mode; opt into draft via `draft` positional arg or `wip/`/`draft/` branch prefix. `n` aborts cleanly; the saved artifact remains for the next run.

9. **Execute.**
   - Create: `git push -u origin <branch>` (if unpushed) → `gh pr create --base <base> --title <title> --body-file <file>` (add `--draft` if draft mode). Rename the artifact to `{number}_description.md`.
   - Update: `gh pr edit {number} --body-file thoughts/prs/{number}_description.md`.
   - Surface the URL, plus any hand-check bullets the user still needs to run.

## Notes

- **Portable:** templates live in `templates/` next to this file. Drop the skill into any repo and it works — no `.github/` or `docs/` setup required.
- Be extremely concise and sacrifice grammar for the sake of concision.
- Short beats complete. Nobody but the author reads these.
- Never append `🤖 Generated with [Claude Code](https://claude.com/claude-code)` to PR bodies.
