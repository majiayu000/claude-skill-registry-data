---
name: skill-quality-gate
description: >
  Audit Codex skills and plugins for trigger clarity, duplication, context
  bloat, missing references, unsafe instructions, and validation gaps. Use
  before installing, publishing, or relying on generated skills.
---

# Skill Quality Gate

Run this before considering a skill pack usable.

## Checks

1. Every skill has frontmatter `name` and `description`.
2. Description names the job, triggers, and required tools.
3. Skill body is short enough to load cheaply.
4. Long details live in references.
5. Skills do not overlap heavily.
6. No skill silently installs or runs untrusted software.
7. Output contracts are explicit.
8. Scripts are executable and scoped.

## Local Audit

```bash
SUPERCHARGE_PLUGIN="${SUPERCHARGE_PLUGIN:-plugins/codex-supercharge}"
scripts/skill_audit.sh skills
scripts/skill_audit.sh --strict skills
python3 "$SUPERCHARGE_PLUGIN/scripts/plugin_discovery_audit.py" --plugin-root "$SUPERCHARGE_PLUGIN" --strict
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/codex-supercharge/skills/<skill-name>
```

## Findings Format

Lead with issues:

```md
## Findings
- [P1] ...
- [P2] ...

## Duplicates

## Missing Tests

## Recommended Changes
```

Use `$low-token-context` if the audit output becomes large.

## Validation

- `skill_audit.sh` reports folded descriptions, missing skip/validation/provenance, and risky commands.
- `plugin_discovery_audit.py` reports index/defaultPrompt/router/boundary references with no stale skill or reference links.
- `quick_validate.py` passes for every changed skill folder.
- Findings distinguish blocking metadata failures from follow-up quality debt.
