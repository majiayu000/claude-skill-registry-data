---
name: linear-change-status
description: Change Linear issue statuses through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use when the user asks to move a Linear task or issue to Done, In Progress, Backlog, Todo, or another workflow state and the normal Linear MCP connector is unavailable, blocked, or insufficient.
metadata:
  category: productivity
  capability_taxonomy_ids:
    - cap.productivity.issue_tracking
    - cap.tools.api_automation
  compatibility:
    runtimes:
      - codex
      - claude_code
      - cursor
      - antigravity
      - windsurf
  distribution_scope: public
  invocation_strategy: explicit
  version: v0.2
  source_of_truth: https://github.com/nicshik/linear-skills
---

# Linear Change Status

Use this skill when the user explicitly asks to change a Linear issue status through the Linear API, or when the normal Linear connector cannot perform a narrow status transition.

Prefer the official Linear MCP connector for read-only discovery. This skill is a fallback status changer, not a general Linear client.

## Preconditions

- `LINEAR_API_KEY` is available in the shell, `LINEAR_ENV_FILE`, `--env-file`, or a local `.env.local`.
- The key belongs to a Linear user with permission to edit the target issue.
- Network access to `https://api.linear.app/graphql` is allowed.

## Non-Negotiable Rules

- Use `scripts/change_status.py`.
- Use the shared GraphQL client from this repository; it resolves `LINEAR_API_KEY`, uses `certifi` for TLS when available, and redacts the token from API errors.
- Never print the API key.
- Do not store the API key in the skill directory.
- Read the issue first, find the target workflow state inside the issue team, update, then verify.
- If the issue is already in the target state, report a no-op instead of sending an update.
- For bulk changes, use `--batch-file`; it is dry-run by default and processes issues one at a time. Use `--apply-batch` only when the user explicitly asked for the batch mutation.
- Do not use this skill to discover issue requirements, comments, relations, or queue priority.
- Do not use this skill to decide whether a task is ready for `Done`; make that delivery or readiness decision in the calling workflow before invoking the script.
- If a final comment is needed, create it through `linear:linear` first; then run this status-change script.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request a persistent command prefix:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-change-status/scripts/change_status.py"]`

Tell the user to choose the option like "Yes, and don't ask again for commands that start with this prefix". After that, the same status-change script can run without repeated prompts.

Keep the command prefix stable by running from the `linear-skills` repository root. Pass the API key only through the environment or `--env-file`; never pass the key as a command argument.

For full setup details and a ready-to-copy rules snippet, see `docs/codex-approvals.md` in the repository root.

## Default Flow

1. Identify the issue key or ID and target status from the user request.
2. If the key is only in a project `.env.local`, pass it via `--env-file`.
3. Run the script, preferably with `--json` when another agent will consume the result.
4. Report the previous status, target status, update result, verified status, and `error_category` when present.

## Recommended Commands

```bash
python3 scripts/change_status.py LIN-123 Done --env-file /path/to/.env.local
python3 scripts/change_status.py LIN-124 "In Progress" --json
python3 scripts/change_status.py LIN-125 Done --dry-run
python3 scripts/change_status.py --batch-file status_changes.tsv --json
python3 scripts/change_status.py --batch-file status_changes.tsv --apply-batch --json
```

## Output Shape

- Text output: `before`, `target`, `updated` or `noop`, and `verify`.
- `--json` output: structured fields for issue, before state, target state, action, changed flag, verified state, `completed_at`, and `error_category`.
- Failure categories are `missing_api_key`, `not_found`, `ambiguous_status`, `permission_denied`, and `network`.
- A no-op uses `action=noop` and `error_category=already_in_target`; this is a successful outcome, not a failed update.
- On failure, show the API or validation error directly without guessing.

## Batch File Shape

Use one issue per line:

```text
LIN-123	Done
{"issue":"LIN-124","status":"In Progress"}
```

Without `--apply-batch`, batch mode is always a dry-run preview even if `--dry-run` is omitted.

## Workflow Boundary

Use this skill only after read-only discovery and any required comments or checks are complete:

1. The caller identifies the issue and target status.
2. The caller confirms the transition is appropriate for its workflow.
3. `linear-change-status` changes the workflow state and verifies the result.
