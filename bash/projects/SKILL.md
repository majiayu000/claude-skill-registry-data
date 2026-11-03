---
name: projects
description: List known projects and their instinct statistics
category: memory
sources:
- repository: ecc
  original_path: commands/projects.md
  sha256: dc939242028d24119b985e6ad4fee3d6c8185f6bd19c716535384149bc9876f3
principles: []
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Projects Command

List project registry entries and per-project instinct/observation counts for continuous-learning-v2.

## Implementation

Run the instinct CLI using the plugin root path:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" projects
```

Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation):

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py projects
```

## Usage

```bash
/projects
```

## What to Do

1. Read `~/.claude/homunculus/projects.json`
2. For each project, display:
   - Project name, id, root, remote
   - Personal and inherited instinct counts
   - Observation event count
   - Last seen timestamp
3. Also display global instinct totals

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Source provenance

- `ecc/commands/projects.md`
