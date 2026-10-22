---
name: linear-create-issue
description: Create one Linear issue through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use only as a narrow fallback when the normal Linear connector is unavailable or cannot create the issue.
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

# Linear Create Issue

Use this skill when the normal Linear connector cannot create an issue and a narrow, audited GraphQL fallback is needed.

Prefer the official Linear connector for normal issue creation. This skill is a fallback issue creator, not a general Linear client.

## Preconditions

- `LINEAR_API_KEY` is available in the shell, `LINEAR_ENV_FILE`, `--env-file`, or a local `.env.local`.
- The key belongs to a Linear user with permission to create issues in the target team.
- Network access to `https://api.linear.app/graphql` is allowed.

## Non-Negotiable Rules

- Use `scripts/create_issue.py`.
- Never print the API key.
- Do not store the API key in the skill directory.
- Create exactly one issue per invocation.
- Resolve the target team, status, project, and labels before sending the mutation.
- Use `--dry-run` first when a caller needs to verify labels or metadata without creating an issue.
- Do not create missing labels or workflow states. Stop and report the missing setup instead.
- Use `--optional-label` for labels that should be added only when they already exist.
- Read the created issue back through GraphQL and report the verified result.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request a persistent command prefix:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-create-issue/scripts/create_issue.py"]`

Keep the command prefix stable by running from the `linear-skills` repository root. Pass the API key only through the environment or `--env-file`; never pass the key as a command argument.

## Recommended Commands

```bash
python3 scripts/create_issue.py --team LIN --status Backlog --title "Example idea" --description-file /path/to/body.md --label Idea --dry-run
python3 scripts/create_issue.py --team LIN --project "Example Project" --status Backlog --title "Example idea" --description "Short body" --label Idea --optional-label Product --json
```

## Output Shape

- Text output: resolved target metadata, then `created` or `dry_run`.
- `--json` output: structured fields for target metadata, created issue, verified issue, action, and `error_category`.
- Failure categories are `missing_api_key`, `not_found`, `ambiguous_lookup`, `validation`, `permission_denied`, and `network`.
