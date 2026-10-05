---
name: doppler-secrets
description: Use when setting up Doppler as secrets source of truth, syncing Doppler to fnox/Keychain, bulk importing/exporting secrets, validating Doppler vs fnox parity, or troubleshooting Doppler CLI issues in this mise+chezmoi dev environment.
---

# Doppler Secrets Management

Doppler is the cloud source of truth. fnox/Keychain is the local runtime cache.

## Architecture

```
Doppler (project: dotfiles, config: dev)
  -> uv run mde-py secrets sync
    -> fnox/Keychain (local cache)
      -> mise (_.fnox-env = { tools = true })
        -> env vars -> .mcp.json / tools
```

New secrets go to Doppler first. `secrets sync` pulls them to fnox/Keychain.

## Setup

```bash
# Install (via mise or brew)
doppler login
doppler projects create dotfiles
doppler setup --project dotfiles --config dev
```

## Adding a New Secret

```bash
# CORRECT: Add to Doppler first (source of truth)
doppler secrets set NEW_KEY --project dotfiles --config dev
# Then sync to local cache
uv run mde-py secrets sync

# WRONG: Adding to fnox directly (bypasses source of truth)
fnox set NEW_KEY --provider keychain --global
```

## Bulk Import (fnox -> Doppler, one-time migration)

```bash
uv run mde-py secrets export-to-doppler
# Reads fnox list, pushes each to Doppler
# Validates parity after export
```

## Sync (Doppler -> fnox/Keychain)

```bash
uv run mde-py secrets sync
# Downloads from Doppler, updates fnox/Keychain entries
# Existing _.fnox-env chain then loads them into mise
```

## Validation

```bash
uv run mde-py secrets validate
# Compares Doppler vs fnox, reports mismatches
```

## Critical Gotcha: --command Flag

```bash
# CORRECT: variables expand AFTER Doppler injects
doppler run --command='echo $SECRET_KEY'

# WRONG: shell expands $SECRET_KEY BEFORE Doppler -> empty
doppler run -- echo $SECRET_KEY
```

## chezmoi Integration

In `~/.config/chezmoi/chezmoi.toml`:
```toml
[doppler]
project = "dotfiles"
config = "dev"
```

Then in chezmoi templates:
```
{{ doppler "SECRET_NAME" }}
{{ dopplerProjectJson.SECRET_NAME }}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adding secret to fnox instead of Doppler | Add to Doppler first, then sync |
| Using `doppler run -- echo $VAR` | Use `doppler run --command='echo $VAR'` |
| Forgetting --project/--config flags | Run `doppler setup` in project dir first |
| Not running sync after adding to Doppler | Run `uv run mde-py secrets sync` |
| Storing Doppler token in plaintext | Use `fnox set DOPPLER_TOKEN --provider keychain --global` |

## Offline Mode

Doppler creates an encrypted fallback at `~/.config/doppler/fallback.json`.
fnox/Keychain also retains synced values. Both work offline.
