---
name: issue-publish
description: >
  Create or edit a GitHub issue with `gh` from the reviewed draft at
  `.github/drafts/issue-draft.md`. Use only when that draft exists and the
  user asks to publish, open, or file it — typically handed off from
  `github-issue-creator`. Assigns the issue to the user; never comments,
  closes, or reopens.
---

# Issue Publish

Publish the issue draft by running the steps below in order.

## Hard limits

- GitHub issue writes only, and only `gh issue create` / `gh issue edit`. Never comment, close, or reopen an issue.
- No git or codebase changes of any kind — the draft included. The only file you may write is the temporary body file in step 8.
- Read-only `gh` for every precondition.

## Read the draft

1. Read `.github/drafts/issue-draft.md`. If it is missing, stop and tell the user to run `github-issue-creator` first.
2. Parse the front-matter: `title`, `labels`. Everything after the closing `---` is the body. Use these values verbatim — never rewrite them.

## Precondition

3. Confirm the repo is reachable and `gh` is authenticated: `gh repo view`. If it fails, stop and tell the user to check the repo or run `gh auth login`.

## Create vs edit

4. **Create** unless the user named an existing issue number to update.
5. **Edit** only when the user gave an issue number. First confirm it exists with `gh issue view <number>`; if that fails, stop rather than create a new issue by mistake.

## Labels

6. Fetch the repo's labels once: `gh label list --json name --limit 500`.
7. Every label the draft names must already exist. If any is missing, stop, list the missing names, and tell the user to run `/label-setup` — never create labels.

## Assemble, confirm, run

8. Write the body to a temporary file outside the repo with `mktemp`. Pass it as `--body-file`.
9. Assemble the exact command. Apply the constant the draft does not carry: `--assignee @me` on create.
   - Create:
     ```
     gh issue create --title "<title>" --body-file <tmpfile> \
       --assignee @me --label "<label>"   # repeat --label per label
     ```
   - Edit (assignee is not re-applied; add labels without removing any):
     ```
     gh issue edit <number> --title "<title>" --body-file <tmpfile> \
       --add-label "<label>"   # repeat --add-label per label
     ```
10. Show the assembled command(s) in full and ask once for approval. Run nothing until the user approves.
11. On approval, run the command, then delete the temporary body file. Report the issue URL `gh` prints.
