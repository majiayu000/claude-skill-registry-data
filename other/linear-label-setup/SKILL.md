---
name: linear-label-setup
description: Ensure Linear issue labels exist through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use only as a narrow fallback when the normal Linear connector cannot create missing labels.
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

# Linear Label Setup

Use this skill when the normal Linear connector cannot create required issue labels and a narrow, audited GraphQL fallback is needed.

## Rules

- Use `scripts/label_setup.py`.
- Never print the API key.
- Do not store the API key in the skill directory.
- Resolve the target team and current labels before creating anything.
- Use `--dry-run` before live setup when checking missing labels.
- Existing labels are a no-op.
- Create only the labels explicitly passed with `--label`.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-label-setup/scripts/label_setup.py"]`

## Recommended Commands

```bash
python3 scripts/label_setup.py --team LIN --label Product --dry-run --json
python3 scripts/label_setup.py --team LIN --label Product --description "Product work" --color "#5E6AD2" --json
```

## Output Shape

- Text output: team and one action per label.
- `--json` output: target team, label actions, verified labels, and `error_category`.
- Failure categories are `missing_api_key`, `not_found`, `ambiguous_lookup`, `permission_denied`, and `network`.
