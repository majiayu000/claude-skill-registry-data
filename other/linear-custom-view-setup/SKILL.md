---
name: linear-custom-view-setup
description: Ensure one Linear Custom View exists through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use only as a narrow fallback when the normal Linear connector cannot set up a required view.
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

# Linear Custom View Setup

Use this skill when the normal Linear connector cannot create a required Custom View and a narrow, audited GraphQL fallback is needed.

## Rules

- Use `scripts/custom_view_setup.py`.
- Never print the API key.
- Resolve the team, project, and labels before creating a view.
- Use `--dry-run` before live setup.
- Existing views with the same name in the same team are a no-op.
- Do not use this helper for queue reading; use `linear-custom-view` for that.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-custom-view-setup/scripts/custom_view_setup.py"]`

## Recommended Commands

```bash
python3 scripts/custom_view_setup.py --team LIN --project "Example Project" --name "Product MVP" --label Product --open-only --dry-run --json
python3 scripts/custom_view_setup.py --team LIN --name "Product MVP" --label Product --open-only --json
```

## Output Shape

- Text output: view name, team, project, labels, and action.
- `--json` output: target metadata, created view, verified view, and `error_category`.
- Failure categories are `missing_api_key`, `not_found`, `ambiguous_lookup`, `permission_denied`, and `network`.
