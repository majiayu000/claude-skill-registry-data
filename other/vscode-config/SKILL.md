---
name: vscode-config
description: Manage VSCode/Cursor configuration in this dotfiles repository. Use when working with settings.json, keybindings.json, or tasks.json files, or when asked about VSCode/Cursor configuration structure.
---

# VSCode Config Management

## Repository Structure

```
vscode/
├── user/           # Client-side, synced via Settings Sync
├── profiles/OPS/   # Profile-specific (vim bindings, editor prefs)
├── machines/ops/   # Server-side, symlinked via setup.sh
└── setup.sh        # Symlinks machine configs only
```

## Configuration Layers

| Layer | Location | Sync Method |
|-------|----------|-------------|
| Machine | `machines/<hostname>/` | `setup.sh` symlink |
| User | `user/` | Settings Sync |
| Profile | `profiles/<name>/` | Settings Sync |

## Common Tasks

**Add machine config**: Create `machines/<hostname>/settings.json`

**Update vim bindings**: Edit `user/settings.json` (keybindings sync to all machines)

**Run setup on server**: `./vscode/setup.sh` (uses hostname, or `--machine <name>`)

Machine settings override user/profile. Put machine-specific paths and extensions in machine config.
