---
name: glab-gitlab-issue
description: Read and manage GitLab issues through the `glab` CLI. Use when a user provides an issue ID and repository and asks to view issue details, comments, or uploaded images, publish comments, update assignees or labels, or manage issue time tracking (estimate/spent time) without using the web UI.
---

# Glab Gitlab Issue

Manage GitLab issues from the terminal using `glab`.

## Required Inputs

Collect these inputs before running commands:

- `repo`: `OWNER/REPO` or `GROUP/NAMESPACE/REPO` (example: `example-org/example-app`)
  - Pass plain repo path (do not pre-encode `%2F`).
  - The helper script auto-encodes repo path only when calling `glab api` endpoints.
- `issue_id`: issue IID in that repository (example: `165`)
- `author` (for commit query): GitLab username (example: `octocat`)

## Workflow

1. Confirm authentication with `glab auth status` if access is uncertain.
2. Identify intent: view, comment, assignee update, label update, or time tracking.
3. For reading an issue, use `view`; it caches GitLab `/uploads/...` files from the description and notes by default under `${XDG_CACHE_HOME:-$HOME/.cache}/codex/glab-gitlab-issue/` and rewrites them to local links in the output.
4. Return key result, including any changed fields.

## Preferred Execution

Prefer the bundled helper script for consistency:

```bash
bash scripts/issue.sh <action> --repo <repo> --issue <issue_id> [...flags]
```

Supported actions:

- `commits`: query commit history by repo + author, return committed date/author/message
- `view`: view issue; optional comments/system logs/json output; caches upload files by default
- `images`: lower-level helper to refresh/list cached `/uploads/...` files from the issue description and notes
- `note`: post a comment from inline text
- `note-file`: post a comment from a file
- `assignee`: update assignees
- `labels`: add/remove labels
- `estimate`: set time estimate
- `add-spent`: add spent time and return created timelog ID
- `list-spent`: list timelog entries on the issue and return timelog IDs
- `delete-spent`: delete one spent-time entry by timelog ID, owner-safe by default
- `reset-estimate`: clear estimate
- `reset-spent`: clear spent time

Use `--dry-run` with any action to preview the underlying `glab` command.

## Command Reference

Load [references/commands.md](references/commands.md) when exact command syntax is needed.

## Practical Examples

View issue with comments:

```bash
bash scripts/issue.sh commits --repo example-org/example-api --author octocat --limit 20
bash scripts/issue.sh view --repo example-org/example-app --issue 165 --comments
```

Use a custom cache directory or bypass caching:

```bash
bash scripts/issue.sh view --repo example-org/example-app --issue 30 --comments --cache-dir /tmp/issue-30-cache
bash scripts/issue.sh view --repo example-org/example-app --issue 30 --no-cache
```

Publish a comment:

```bash
bash scripts/issue.sh note --repo example-org/example-app --issue 165 --message "Finished today's progress update."
```

Update assignee and labels:

```bash
bash scripts/issue.sh assignee --repo example-org/example-app --issue 165 --assignee alice
bash scripts/issue.sh labels --repo example-org/example-app --issue 165 --add backend,urgent --remove triage
```

Track time:

```bash
bash scripts/issue.sh estimate --repo example-org/example-app --issue 165 --duration 3h
bash scripts/issue.sh add-spent --repo example-org/example-app --issue 165 --duration 45m --summary "daily report"
bash scripts/issue.sh list-spent --repo example-org/example-app --issue 165 --limit 20
bash scripts/issue.sh delete-spent --repo example-org/example-app --issue 165 --timelog-id gid://gitlab/Timelog/12345
```

## Troubleshooting

- If `404` occurs, verify repo path and issue IID belong to the same project.
- If `403` occurs, verify token scope and project access.
- If comment text contains many special characters, use `note-file`.
