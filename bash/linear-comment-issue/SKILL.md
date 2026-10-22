---
name: linear-comment-issue
description: Add one comment to a Linear issue through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use only as a narrow fallback when the normal Linear connector is unavailable or cannot create the comment.
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

# Linear Comment Issue

Use this skill when the normal Linear connector cannot create a comment and a narrow, audited GraphQL fallback is needed.

Prefer the official Linear connector for normal comments. This skill is a fallback comment creator, not a general Linear client.

## Preconditions

- `LINEAR_API_KEY` is available in the shell, `LINEAR_ENV_FILE`, `--env-file`, or a local `.env.local`.
- The key belongs to a Linear user with permission to comment on the target issue.
- Network access to `https://api.linear.app/graphql` is allowed.

## Non-Negotiable Rules

- Use `scripts/comment_issue.py`.
- Never print the API key.
- Do not store the API key in the skill directory.
- Create exactly one comment per invocation.
- Read and verify the target issue before sending the mutation.
- Prefer a stable issue key such as `LIN-123` when available. A URL or UUID that points to a comment, project, relation, or another workspace is not a valid comment target.
- Use `--dry-run` first when a caller needs to verify the issue without creating a comment.
- Read the issue again after commenting and report the verified result.
- If the helper returns `error_code=issue_not_found`, do not retry as a missing API key problem. Verify the target with `linear-read-issue` and the stable issue key.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request a persistent command prefix:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-comment-issue/scripts/comment_issue.py"]`

Keep the command prefix stable by running from the `linear-skills` repository root. Pass the API key only through the environment or `--env-file`; never pass the key as a command argument.

## Recommended Commands

```bash
python3 scripts/comment_issue.py LIN-123 --body-file /path/to/comment.md --env-file /path/to/.env.local --dry-run
python3 scripts/comment_issue.py LIN-123 --body "Short comment" --env-file /path/to/.env.local --json
```

## Output Shape

- Text output: target issue, then `commented` or `dry_run`.
- `--json` output: structured fields for target issue, comment, verified issue, action, and `error_category`.
- Failure categories are `missing_api_key`, `not_found`, `validation`, `permission_denied`, and `network`.
- Issue lookup failures use `error_category=not_found` and `error_code=issue_not_found`, with safe `lookup`, `input_kind`, and `hint` fields. No comment mutation is sent in this case.
