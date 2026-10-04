---
name: vault-sync-setup
description: Use when the user wants to install Vault Sync, connect an existing Vault Git repository to a local folder, refresh it, configure a recurring pull schedule, or make a local Vault available to an AI agent through filesystem files.
---

# Vault Sync Setup

Vault Sync mirrors an existing Vault Git repository to local files. It does not create Vaults, manage replicas, call app APIs, search, query, summarize, rank, index, or push changes.

## Workflow

1. Confirm the environment is macOS, Linux, or WSL2. For Windows users, recommend WSL2 and keep the Vault under the WSL filesystem.
2. Check for `bash` and `git`. `rg` is optional but useful for later consumption.
3. Install `vault-sync` if it is not already on `PATH`. Prefer the bundled script:

```bash
bash skills/vault-sync-setup/scripts/install-vault-sync.sh
```

If the bundled script is unavailable, install from GitHub:

```bash
mkdir -p ~/.local/bin
curl -fsSL https://raw.githubusercontent.com/graphlit/vault-sync/main/bin/vault-sync -o ~/.local/bin/vault-sync
chmod +x ~/.local/bin/vault-sync
```

4. Ask for the Vault Git repository URL and preferred local folder if missing. Use `~/vaults/<repo-name>` as the default.
5. Do not infer the local Vault path from the current working directory, app name, or repository owner. Do not invent hidden app folders such as `~/.zine/vault`, `~/.dossium/vault`, or `~/.graphlit/vault`.
6. Initialize and verify:

```bash
vault-sync init <vault-repo-url> <path>
vault-sync pull <path>
vault-sync doctor <path>
```

7. Ask before installing a recurring schedule. If approved:

```bash
vault-sync schedule install <path> --every 5m
```

## Agent Behavior

- Treat the Vault as generated, read-only context.
- Do not edit Vault files unless the user explicitly asks to modify local copies.
- Do not use `vault-sync` as a search or read API. After setup, use normal filesystem tools.
- If Git authentication fails, let the user complete their normal Git or GitHub CLI authentication flow.
