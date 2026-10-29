---
name: msb-setup
description: "Machine-level setup and first run: msbctl setup's SETUP_SECTIONS (git identities, Claude login, your network, new-sandbox defaults) plus the raw file, writing ~/.config/msb/config.toml through set_toml_key()/remove_toml_table(), secrets/global.env at 0600 through set_env_file_value() keeping its documenting comments, needs_welcome()/maybe_welcome() and the welcome-done marker, named Claude tokens with [defaults] claude_token and the registry entry overriding it, and a LAN group needing defaults.private_dns_groups. Use when adding a machine-level setting or changing first-run behaviour."
---

# Setup

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

`msbctl setup` is the machine-level twin of `edit`: `SETUP_SECTIONS` (git identities, Claude login, your network, new-sandbox defaults) plus "edit the file", each writing to `~/.config/msb/config.toml` via `set_toml_key()` / `remove_toml_table()` or to `secrets/global.env` via `set_env_file_value()` (0600, keeps the documenting comments). The main menu's "setup" item opens it. `maybe_welcome()` (bare `msbctl` and `add`, interactive only) offers the same sections as a guided walk-through the first time: `needs_welcome()` is true only if there is no `welcome-done` marker AND nothing configured yet, so an already-set-up machine is marked done silently. A group you define under "your network" that names LAN hosts goes in `defaults.private_dns_groups`, which `msbctl add` and `edit` read to set `allow_private_dns`. Claude tokens are named (`claude_tokens()`: `CLAUDE_CODE_OAUTH_TOKEN` is `main`, `CLAUDE_CODE_OAUTH_TOKEN_<NAME>` the rest); `[defaults] claude_token` picks the default and a registry entry's `claude_token` overrides it, and whichever is chosen is handed to msb as `CLAUDE_CODE_OAUTH_TOKEN`, so the guest never knows. A new machine-level setting should get a section here. When testing, `claude` may be on PATH and adds a "run claude setup-token" row to the login menu — patch `shutil.which` so numbering is deterministic.
