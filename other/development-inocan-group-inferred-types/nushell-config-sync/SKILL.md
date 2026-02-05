---
name: nushell-config-sync
description: Sync Nushell configuration files between the repo (os-config/nushell) and the system config path ($nu.config-path). Use when the user wants to push, pull, or diff nushell config files.
---

# Nushell Config Sync

Synchronizes Nushell configuration files between this repository and the system.

## Paths

- **Repo path**: `os-config/nushell/` in this repository
- **System path**: The directory containing `$nu.config-path` (typically `~/.config/nushell/` on Linux/macOS or `%APPDATA%\nushell\` on Windows)

## Commands

### Push (repo -> system)

Copies config files FROM `os-config/nushell/` TO the system Nushell config directory.

```bash
python .claude/skills/nushell-config-sync/sync.py push
```

### Pull (system -> repo)

Copies config files FROM the system Nushell config directory TO `os-config/nushell/`.

```bash
python .claude/skills/nushell-config-sync/sync.py pull
```

### Diff (compare repo vs system)

Shows unified diff between repo and system config files.

```bash
python .claude/skills/nushell-config-sync/sync.py diff
python .claude/skills/nushell-config-sync/sync.py diff -f config.nu  # specific file
```

## Files Synced

- `config.nu` - Main Nushell configuration
- `env.nu` - Environment configuration

## Usage

When user says:
- "push nushell config" or "sync config to system" -> run push command
- "pull nushell config" or "sync config from system" -> run pull command
- "diff nushell config" or "compare nushell config" -> run diff command

Always run diff before push/pull to show the user what will change.
