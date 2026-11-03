---
name: prune
description: Delete pending instincts older than 30 days that were never promoted
category: memory
sources:
- repository: ecc
  original_path: commands/prune.md
  sha256: b2ff4b7ff2eef3893975736b899f84043665c765972609c0ff816be18cf42b82
principles: []
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Prune Pending Instincts

Remove expired pending instincts that were auto-generated but never reviewed or promoted.

## Implementation

Run the instinct CLI using the plugin root path:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" prune
```

Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation):

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py prune
```

## Usage

```
/prune                    # Delete instincts older than 30 days
/prune --max-age 60      # Custom age threshold (days)
/prune --dry-run         # Preview without deleting
```

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Source provenance

- `ecc/commands/prune.md`
