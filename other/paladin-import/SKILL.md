---
name: paladin-import
description: "Bulk-import credentials into the Paladin vault from .env files, CSV/JSON exports, Bitwarden, or 1Password — or discover where credentials live. Returns names/kinds/counts only; secret values never enter the agent's context."
version: 1.0.0
author: argobox
license: MIT
platforms: [linux, windows, macos]
metadata:
  custodian:
    band: L2
    cost_usd: 0.0
    configured: true
  hermes:
    tags: [Security, Credentials, Paladin, Vault, Import]
---

# Paladin Import (bulk credential onboarding)

Move credentials out of plaintext and into the encrypted Paladin vault, in
bulk, from three kinds of sources — without the secret values ever passing
through your (the agent's) context. You see names, kinds, and counts; the
values flow directly from the source into AES-256-GCM inside the tool's
process.

## Quick Reference

| Action | Invocation |
|--------|------------|
| Find where credentials live (report-only) | `source=discover` |
| Import a .env file | `source=env, path=/path/to/.env` |
| Import every .env under a directory | `source=env, path=/dir, recursive=true` |
| Import a password-manager CSV export | `source=csv, path=/path/to/export.csv` |
| Import a JSON secrets dump | `source=json, path=/path/to/secrets.json` |
| Import from Bitwarden | `source=bitwarden, search="api key"` |
| Import from 1Password | `source=1password, from_vault="Main"` |
| Preview without writing | any of the above + `dry_run=true` |

CSV covers Chrome, Firefox, Bitwarden, LastPass, 1Password, and KeePass exports
offline (no CLI needed) — the value column is auto-detected from the header.
JSON accepts a flat `{"NAME": "value"}` object or an array of `{name, value}`.

## Arguments

- `source` (required): `discover` | `env` | `csv` | `json` | `bitwarden` | `1password`
- `path`: for `env` — a .env file or a directory to scan; for `csv`/`json` — the file
- `recursive`: for `env` — `true` to scan subdirectories
- `pattern`: for `env` — filename pattern (default `.env*`)
- `search`: for `bitwarden`/`1password` — only matching items
- `folder`: for `bitwarden` — only items in this folder
- `from_vault`: for `1password` — only items in this 1Password vault
- `profile`: paladin profile to import into (default `default`)
- `dry_run`: `true` to preview; nothing is written
- `overwrite`: `true` to replace already-vaulted names (default: skip them)

## The intended agent workflow

1. `source=discover` — see what exists (env files, shell-rc export NAMES,
   whether `bw`/`op` are installed and unlocked). Nothing is imported.
2. Relay the discovery to the human; let them choose sources.
3. Import each chosen source (use `dry_run=true` first if unsure).
4. Report the counts and any `git-tracked` / `git-unignored` flags — those
   credentials were exposed to git and should be rotated, not just vaulted.

## Requirements

- The vault must be unlockable non-interactively: `PALADIN_PASSPHRASE` or
  `PALADIN_KEYFILE` must be set (or run `paladin init` first). If not, the
  tool returns `locked: true` with instructions instead of prompting.
- Bitwarden: `bw` CLI installed and unlocked (`export BW_SESSION=$(bw unlock --raw)`).
- 1Password: `op` CLI installed and signed in (`op signin`).

## What this tool will never do

- Print, return, or log a secret value — reports carry names/kinds/sources.
- Import on `discover` — discovery is report-only; importing takes an
  explicit source invocation.
- Re-import silently over existing entries — duplicates are skipped unless
  `overwrite=true` is explicitly passed.
