---
name: pr-publish
description: >
  Create or edit a GitHub pull request with `gh` from the reviewed draft at
  `.github/drafts/pr-draft.md`. Use only when that draft exists and the user
  asks to publish, open, or push it live — typically handed off from
  `pr-draft`. Opens the PR in draft state assigned to the user; never merges
  or pushes commits.
---

# PR Publish

Publish the PR draft by running the steps below in order.

## Hard limits

- GitHub PR writes only, and only `gh pr create` / `gh pr edit`. Never merge, comment, close, reopen, or mark a PR ready.
- Never push, pull, commit, or change branches.
- Never edit the draft or any tracked file. The only file you may write is the temporary body file in step 9.
- Read-only git and read-only `gh` for every precondition.

## Read the draft

1. Read `.github/drafts/pr-draft.md`. If it is missing, stop and tell the user to run `pr-draft` first.
2. Parse the front-matter: `title`, `base`, `labels`. Everything after the closing `---` is the body. Use these values verbatim — never rewrite them.
3. Record the head branch: `git rev-parse --abbrev-ref HEAD`. If it equals `base`, stop — a branch cannot open a PR against itself.

## Preconditions

Any failure here stops the skill with no PR written.

4. **Branch is on the remote.** `git ls-remote --heads origin <branch>` must return a line. If it is empty, stop and tell the user to push the branch first — never push it yourself.
5. **Nothing local is unpushed.** Take the remote SHA from step 4's output and confirm the remote branch contains local `HEAD`: `git merge-base --is-ancestor HEAD <remote-sha>`. Exit 0 means the remote holds everything local. Any other result (including an unknown object) means local is ahead or unconfirmed — stop and tell the user to push first.

## Create vs edit

6. Look up the open PR for this pair: `gh pr list --head <branch> --base <base> --state open --json number`. GitHub allows at most one.
   - A result — edit that PR number with `gh pr edit`.
   - Empty — create with `gh pr create`.

## Labels

7. Fetch the repo's labels once: `gh label list --json name --limit 500`.
8. Every label the draft names must already exist. If any is missing, stop, list the missing names, and tell the user to run `/label-setup` — never create labels.

## Assemble, confirm, run

9. Write the body to a temporary file outside the repo with `mktemp`. Pass it as `--body-file`.
10. Assemble the exact command. Apply the constants the draft does not carry: `--draft` and `--assignee @me` on create.
    - Create:
      ```
      gh pr create --title "<title>" --body-file <tmpfile> \
        --base <base> --head <branch> --draft --assignee @me \
        --label "<label>"   # repeat --label per label
      ```
    - Edit (`--draft` and assignee are not re-applied; add labels without removing any):
      ```
      gh pr edit <number> --title "<title>" --body-file <tmpfile> \
        --base <base> --add-label "<label>"   # repeat --add-label per label
      ```
11. Show the assembled command(s) in full and ask once for approval. Run nothing until the user approves.
12. On approval, run the command, then delete the temporary body file. Report the PR URL `gh` prints, and note it opened in draft state — the user marks it ready for review on GitHub.
