---
name: qissue
description: Draft, review, and create one GitHub issue through the optional Qissue adapter and an existing gh CLI login. Use when the user asks to file or report a bug, feature request, or question, including "create an issue", "file a bug", "이슈 올려줘", or "버그 리포트".
---

# Qissue

Create one reviewed GitHub issue without handling GitHub tokens inside QE. Keep QE responsible for deciding and explaining the work; delegate the external mutation to the bundled adapter script.

## Workflow

1. Run `command -v gh` and `gh auth status`.
   - If `gh` is missing, stop and show the platform-appropriate installation command.
   - If authentication is missing, stop and ask the user to run `gh auth login`. Never request, receive, echo, or store a PAT.
2. Determine the issue type: `bug`, `feature`, or `question`. Ask only when intent is ambiguous.
3. Draft a title of at most 80 characters and a focused body:
   - `bug`: reproduction, expected behavior, actual behavior, relevant bounded logs.
   - `feature`: problem, proposed outcome, alternatives or constraints.
   - `question`: context, attempts, and the unresolved question.
4. Remove secrets, credentials, private URLs, and unrelated raw logs. Do not attach files unless explicitly authorized.
5. Show the exact repository, label, title, and body. Obtain explicit confirmation before creating the issue.
6. Invoke `scripts/create-issue.mjs` only after confirmation. Prefer sending this JSON request through the tool's stdin channel:

```json
{
  "repo": "inho-team/qe-framework",
  "type": "bug",
  "title": "short issue title",
  "body": "focused issue body"
}
```

Resolve the script relative to this `SKILL.md`. In Claude, run `node "${CLAUDE_PLUGIN_ROOT}/skills/qissue/scripts/create-issue.mjs"`; in other clients, use the installed skill's absolute path. If the client cannot supply stdin directly, create one exact temporary JSON file through its filesystem-writing tool, pass `--request-file=/absolute/path`, and delete only that verified temporary file after the command finishes. Never interpolate user content into `bash -c`, `sh -c`, `eval`, or a shell command string.

7. Return the created issue URL. On adapter failure, report the fixed error code and safe diagnostic; do not retry an external write without user approval.

## Adapter contract

- Default repository: `inho-team/qe-framework`; override only with a repository matching `owner/name`.
- GitHub host: `github.com` only. Authentication and creation are pinned to that host.
- Accepted types and labels: `bug`, `feature`, `question`.
- The script appends bounded QE, OS, and Node environment metadata.
- The script calls `gh` with direct argv and `--body-file=-`; it never launches a shell.
- Use `--dry-run` before confirmation when a machine-readable preview is useful. Dry-run never calls `gh`.
- Issue creation is the only authorized external mutation. Do not close, edit, comment on, or bulk-create issues.

## Failure handling

- `QISSUE_GH_MISSING`: install GitHub CLI, then retry.
- `QISSUE_GH_AUTH`: run `gh auth login`, verify with `gh auth status`, then retry.
- `QISSUE_INVALID_REQUEST`: correct the bounded request fields and preview again.
- `QISSUE_CREATE_FAILED`: show the adapter's bounded diagnostic and ask before retrying.
- `QISSUE_INVALID_RESPONSE`: creation returned no canonical GitHub issue URL; do not claim success.

## Safety boundary

- Never collect GitHub tokens or ask the user to paste credentials into chat.
- Never build the `gh` call with shell interpolation.
- Never create an issue before the explicit preview confirmation.
- Never include completion evidence, logs, or environment values that may contain secrets without redaction.
