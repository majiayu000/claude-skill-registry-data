---
name: linear-update-issue
description: Update one existing Linear issue through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use only as a narrow fallback when the normal Linear connector cannot add labels, assign a user, set a parent, update text, set issue priority, or set manual sort order.
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

# Linear Update Issue

Use this skill when the normal Linear connector cannot perform a narrow update on one existing issue.

## Rules

- Use `scripts/update_issue.py`.
- Never print the API key.
- Read the target issue before mutation.
- Use `--dry-run` before live updates when checking labels, assignee, parent, text, priority, or manual sort order.
- Update only the fields explicitly passed on the command line.
- Read the issue again after mutation and report the verified result.
- `--priority` accepts `none`, `no-priority`, `no_priority`, `urgent`, `high`, `medium`, `normal`, `low`, or numeric `0..4`.
- `--sort-order` updates Linear's workspace-wide manual issue order. Use it only after reading the relevant Custom View queue and preparing the full target order.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-update-issue/scripts/update_issue.py"]`

## Recommended Commands

```bash
python3 scripts/update_issue.py LIN-123 --add-label Product --assignee "Alice Example" --dry-run --json
python3 scripts/update_issue.py LIN-123 --parent LIN-100 --append-description-file /path/to/note.md --json
python3 scripts/update_issue.py LIN-123 --priority high --dry-run --json
python3 scripts/update_issue.py LIN-123 --sort-order -199000 --dry-run --json
```

## Output Shape

- Text output: issue, action, label changes, assignee, and parent.
- `--json` output: target issue, resolved update input, updated issue, verified issue, and `error_category`.
- Failure categories are `missing_api_key`, `not_found`, `ambiguous_lookup`, `validation`, `permission_denied`, and `network`.
