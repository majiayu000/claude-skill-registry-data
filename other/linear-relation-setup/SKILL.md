---
name: linear-relation-setup
description: Ensure one Linear issue relation exists through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use only as a narrow fallback when the normal Linear connector cannot create related or blocking links between issues.
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

# Linear Relation Setup

Use this skill when the normal Linear connector cannot create one relation between two Linear issues and a narrow, audited GraphQL fallback is needed.

## Rules

- Use `scripts/relation_setup.py`.
- Never print the API key.
- Read both issues and existing relations before mutation.
- Use `--dry-run` before live relation creation.
- Supported relation types are `related`, `blocks`, and `blocked-by`.
- `blocked-by` is stored as a `blocks` relation in the reverse direction.
- If the relation already exists, report a no-op.
- Do not delete, rewrite, or bulk-create relations.
- Read the issues again after mutation and report the verified relation.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-relation-setup/scripts/relation_setup.py"]`

## Recommended Commands

```bash
python3 scripts/relation_setup.py LIN-123 LIN-100 --type related --dry-run --json
python3 scripts/relation_setup.py LIN-123 LIN-100 --type blocked-by --json
```

## Output Shape

- Text output: issue, related issue, requested relation type, normalized type, action, source, and target.
- `--json` output: target issues, before relations, create input, created relation, verified relation, and `error_category`.
- Failure categories are `missing_api_key`, `not_found`, `validation`, `permission_denied`, and `network`.
