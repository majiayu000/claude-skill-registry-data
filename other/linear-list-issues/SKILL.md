---
name: linear-list-issues
description: Read and filter Linear issues through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use as a read-only fallback when the normal Linear connector cannot list issues for migration, label cleanup, or metadata preflight.
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

# Linear List Issues

Use this skill when the normal Linear connector cannot provide a checked issue list and a narrow, audited read-only GraphQL fallback is needed.

## Rules

- Use `scripts/list_issues.py`.
- Never print the API key.
- This helper is read-only and must not contain GraphQL mutation operations.
- Prefer scoped queries with `--team` and/or `--project`.
- Use `--without-labels` to find issues with no labels.
- Use `--missing-label` to find issues that do not have a required label.
- Use `--json` when another tool or agent should consume the output.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-list-issues/scripts/list_issues.py"]`

## Recommended Commands

```bash
python3 scripts/list_issues.py --team LIN --project "Example Project" --open-only --without-labels --json
python3 scripts/list_issues.py --team LIN --missing-label Product --limit 25 --json
```

## Output Shape

- Text output: counts and one line per matched issue.
- `--json` output: target metadata, filters, issues, counts, `has_more`, and `error_category`.
- Failure categories are `missing_api_key`, `not_found`, `ambiguous_lookup`, `permission_denied`, and `network`.
