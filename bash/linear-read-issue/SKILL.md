---
name: linear-read-issue
description: Read a Linear issue through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use only as a read-only fallback when the normal Linear connector is unavailable or cannot return required issue comments or relations.
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

# Linear Read Issue

Use this skill when the normal Linear connector cannot read a target issue, comments, or relations and a narrow read-only GraphQL fallback is needed.

Prefer the official Linear connector for normal issue reads. This skill is not a general Linear client and must not be used for updates.

## Preconditions

- `LINEAR_API_KEY` is available in the shell, `LINEAR_ENV_FILE`, `--env-file`, or a local `.env.local`.
- The key belongs to a Linear user with access to the target issue.
- Network access to `https://api.linear.app/graphql` is allowed.

## Non-Negotiable Rules

- Use `scripts/read_issue.py`.
- Never print the API key.
- Do not store the API key in the skill directory.
- Keep this helper read-only. It must not send GraphQL mutations.
- Prefer a stable issue key such as `LIN-123` when available. A UUID or URL without an issue key may refer to another Linear entity.
- Use `--include-comments` only when comments are required.
- Use `--include-relations` only when blocker or related-issue context is required.
- Do not use this skill to decide queue priority; use `linear-custom-view` for Custom View order.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request a persistent command prefix:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-read-issue/scripts/read_issue.py"]`

Keep the command prefix stable by running from the `linear-skills` repository root. Pass the API key only through the environment or `--env-file`; never pass the key as a command argument.

## Recommended Commands

```bash
python3 scripts/read_issue.py LIN-123 --env-file /path/to/.env.local
python3 scripts/read_issue.py "https://linear.app/example/issue/LIN-123/example-title" --json
python3 scripts/read_issue.py LIN-123 --json --include-comments --include-relations
```

## Output Shape

- Text output: issue identifier, status, team, project, labels, and optional comment/relation counts.
- `--json` output: `schema_version`, `fetched_at`, lookup input, and issue payload.
- Failure categories are `missing_api_key`, `not_found`, `permission_denied`, and `network`.
- Issue lookup failures use `error_category=not_found` and `error_code=issue_not_found`, with safe `lookup`, `input_kind`, and `hint` fields.
- `issue_not_found` means Linear was reached but the target Issue was not found by the provided reference. Do not report it as a missing API key unless the error category is `missing_api_key`.
