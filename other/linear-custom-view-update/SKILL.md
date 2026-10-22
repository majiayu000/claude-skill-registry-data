---
name: linear-custom-view-update
description: Update one existing Linear Custom View through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use only as a narrow fallback when the normal Linear connector cannot update Custom View metadata or filters.
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

# Linear Custom View Update

Use this skill when the normal Linear connector cannot update one existing Custom View and a narrow, audited GraphQL fallback is needed.

## Rules

- Use `scripts/custom_view_update.py`.
- Never print the API key.
- Read the Custom View before mutation.
- Use `--dry-run` before live updates.
- Update only the fields explicitly passed on the command line.
- Use `--name` for a narrow Custom View rename without changing filters or manual order.
- Do not use this helper to read queue order; use `linear-custom-view` for that.
- Do not use this helper to change manual issue ordering.
- Read the Custom View again after mutation and report the verified result.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-custom-view-update/scripts/custom_view_update.py"]`

## Recommended Commands

```bash
python3 scripts/custom_view_update.py "Product MVP" --team LIN --label Product --status Backlog --open-only --dry-run --json
python3 scripts/custom_view_update.py https://linear.app/example/view/product-mvp-123abc --name "[Archive] Product MVP" --dry-run --json
python3 scripts/custom_view_update.py https://linear.app/example/view/product-mvp-123abc --team LIN --shared --json
```

## Output Shape

- Text output: view name, action, labels, statuses, and whether the filter changes.
- `--json` output: target metadata, before view, update input, updated view, verified view, and `error_category`.
- Failure categories are `missing_api_key`, `not_found`, `ambiguous_lookup`, `validation`, `permission_denied`, and `network`.
