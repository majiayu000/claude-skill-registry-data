---
name: linear-delete-issue
description: Soft-delete one Linear issue through the direct Linear GraphQL API after read-before-delete and explicit guard checks. Use only as a narrow fallback when the normal Linear connector cannot delete an issue.
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

# Linear Delete Issue

Use this skill when the normal Linear connector cannot delete one issue and a narrow, audited GraphQL fallback is needed.

Prefer the official Linear connector for normal issue deletion. This skill is a fallback soft-delete helper, not a general Linear client.

## Preconditions

- `LINEAR_API_KEY` is available in the shell, `LINEAR_ENV_FILE`, `--env-file`, or a local `.env.local`.
- The key belongs to a Linear user with permission to delete the target issue.
- Network access to `https://api.linear.app/graphql` is allowed.
- The target issue was backed up or otherwise verified according to the caller's own project rules.

## Non-Negotiable Rules

- Use `scripts/delete_issue.py`.
- Never print the API key.
- Do not store the API key in the skill directory.
- Delete exactly one issue per invocation.
- Only soft-delete through Linear's normal issue trash flow.
- Do not permanently delete issues.
- Read and verify the target issue before sending the mutation.
- Use `--dry-run` first for every issue unless the caller has already produced an equivalent checked dry-run.
- For live deletion, pass `--confirm <ISSUE-KEY>`; the value must match the resolved issue identifier.
- Prefer a stable issue key such as `LIN-123` when available. A URL or UUID that points to a comment, project, relation, or another workspace is not a valid delete target.
- Use guard options such as `--expect-status`, `--forbid-label`, `--require-no-children`, `--require-no-relations`, and `--require-no-comments` when the caller has deletion rules.
- `--require-no-relations` covers both directions: outgoing `relations` and incoming `inverseRelations`. An issue that other issues point at is blocked even when it declares no relations of its own. The guard check reports `outgoing_visible_count` and `incoming_visible_count` separately.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request a persistent command prefix:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-delete-issue/scripts/delete_issue.py"]`

Keep the command prefix stable by running from the `linear-skills` repository root. Pass the API key only through the environment or `--env-file`; never pass the key as a command argument.

## Recommended Commands

```bash
python3 scripts/delete_issue.py LIN-123 --env-file /path/to/.env.local --dry-run --json
python3 scripts/delete_issue.py LIN-123 --env-file /path/to/.env.local --expect-status Done --forbid-label Idea --require-no-children --require-no-relations --require-no-comments --confirm LIN-123 --json
```

## Output Shape

- Text output: target issue, action, status, labels, and verification status.
- `--json` output: structured fields for `before`, `guard_checks`, `deleted`, `verified`, `action`, `verification_status`, and `error_category`.
- Failure categories are `missing_api_key`, `not_found`, `validation`, `permission_denied`, and `network`.
- Issue lookup failures use `error_category=not_found` and `error_code=issue_not_found`, with safe `lookup`, `input_kind`, and `hint` fields. No delete mutation is sent in this case.
