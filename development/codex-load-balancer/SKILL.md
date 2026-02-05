---
name: codex-load-balancer
description: Pick a CODEX_HOME source and/or an auth.json credential file per tmux-workflow worker so many Codex workers can balance across multiple logins. Use with tmux-workflow when you need multi-account scaling.
---

# codex-load-balancer

This skill exposes a tiny CLI (`scripts/clb`) that:
- chooses a `CODEX_HOME` **source** directory for a worker (`clb pick`)
- chooses an auth credential file from an **AUTH_TEAM** directory (`clb pick-auth`)

It is designed to be called by `tmux-workflow/scripts/twf` when `twf_use_load_balancer: true`.

## Configure

Edit `scripts/clb_config.yaml`:
- `sources`: comma-separated list of `CODEX_HOME` template directories (optional; default fallback is `~/.codex`)
- `auth_team_dir`: **required** when using `pick-auth` (should contain multiple auth JSON files; names unrestricted)

`pick-auth` selection algorithm:
- pick the **least-used** auth file (usage counts persisted in `state_file`)
- if tied, pick randomly among the least-used

## Commands

- Pick a source directory (used by `twf`):
  - `bash .codex/skills/codex-load-balancer/scripts/clb pick --worker <full> --base <base>`
- Pick an auth file (used by `twf`):
  - `bash .codex/skills/codex-load-balancer/scripts/clb pick-auth --worker <full> --base <base>`
- Inspect a whole team’s usage by driving Codex `/status` in tmux (requires `tmux` + `codex`):
  - `bash .codex/skills/codex-load-balancer/scripts/clb status /abs/path/to/AUTH_TEAM`
- List configured sources:
  - `bash .codex/skills/codex-load-balancer/scripts/clb list`
- Inspect resolved config:
  - `bash .codex/skills/codex-load-balancer/scripts/clb where`

## tmux-workflow integration

Enable in `tmux-workflow/scripts/twf_config.yaml`:
- `twf_use_load_balancer: true`

Optional:
- `twf_load_balancer_cmd: "/abs/path/to/.codex/skills/codex-load-balancer/scripts/clb"`
- or `TWF_LOAD_BALANCER_CMD=/abs/path/to/clb`

When enabled, `twf` will:
- call `clb pick` to choose `TWF_CODEX_HOME_SRC` (if you didn’t set `TWF_CODEX_HOME_SRC` explicitly)
- call `clb pick-auth` and copy the chosen file into each worker home as `auth.json` (overriding the synced `auth.json`)
