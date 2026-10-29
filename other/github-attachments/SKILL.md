---
name: github-attachments
description: Attach a screenshot, image, mockup, diagram, log file, JSON/trace dump, or any binary artifact to a GitHub PR or issue, or share one inline instead of as a gist. Use whenever a PR/issue comment, description, or body would benefit from an embedded image or file — UI changes, repro screenshots, before/after shots, design mockups, captured logs or traces. Wraps the `gh attach` extension. Select this when planning to upload, embed, or inline a file on a GitHub PR/issue rather than reaching for a gist or external host.
---

# Attach files to GitHub PRs and issues

Use [`gh attach`](https://github.com/enthus-appdev/gh-attach), the GitHub CLI extension installed by this dotfiles repo, when a PR or issue needs an image or file such as a screenshot, mockup, log, or trace. PR and issue uploads live on auth-protected refs under `refs/uploads/issues/<N>`; ad-hoc uploads use `refs/uploads/misc/<key>`.

## Choose an upload

- Use a PR or issue upload when an image belongs in a PR/issue description or comment: for example, a UI change, repro screenshot, before/after view, or design mockup.
- Use an ad-hoc upload for a small artifact you want to share inline, such as a log snippet, JSON dump, or captured trace.
- Prefer an inline attachment over a gist or external host when the artifact belongs with the GitHub discussion.

## Upload and share

By default, `gh attach` prints Markdown to stdout; it does not post a comment unless `--comment` is set.

```sh
gh attach <pr-or-issue> path/to/file.png
gh attach path/to/file.png
gh attach --comment <pr> screenshot.png
gh attach --title "<label>" <pr> file.png
gh attach --key <slug> banner.png
```

The first command prints a Markdown image tag for you to paste. The second detects the PR from the current branch. Put flags before the PR/issue number when using `--title`. `--key` creates an ad-hoc upload that is not tied to a PR or issue.

For scripts, request JSON and extract the uploaded file URL:

```sh
gh attach --json <pr> file.png | jq -r '.files[0].url'
```

On success, `--json` suppresses stderr; failures still print a plain-text error to stderr.

You can pipe a screenshot from macOS or insert the generated Markdown into a longer PR comment:

```sh
screencapture -i -t png - | gh attach --name shot.png <pr> -
gh attach <pr> file.png | gh pr comment <pr> --body-file -
```

When reading from stdin, `--name` is required.

## Inspect or restore uploads

```sh
gh attach list
gh attach list --issues
gh attach list --misc
gh attach get <pr> --output ./restored
```

`list` shows every upload ref in the current repository; `--issues` and `--misc` filter the results. `get` restores the PR's uploaded files to the given output directory.

## Clean up

To purge PR and issue upload refs automatically when a PR or issue closes, copy `.github/workflows/cleanup-gh-attach.yml` from the upstream repository into the target repository's `.github/workflows/`. The workflow handles only `refs/uploads/issues/*`.

Ad-hoc uploads under `refs/uploads/misc/*` are not garbage-collected. Delete one manually with confirmation disabled:

```sh
gh attach delete --key <slug> --yes
```

`--yes` is required for non-interactive use, including agent-driven invocations.

## Agent-specific checks

- To verify an upload in a private repository, use `gh api repos/<owner>/<name>/contents/<file>?ref=<sha>`. The embed URL `blob/<sha>/<file>?raw=true` requires a browser session cookie; a PAT does not authenticate it.
- Before deleting an ad-hoc upload, include `--yes`. Without it, the command waits for confirmation and can hang an agent run.
