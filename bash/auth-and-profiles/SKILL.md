---
name: auth-and-profiles
description: How to authenticate the Frontline CLI and manage named profiles for working with multiple environments. Covers getting an API key from the Frontline app, login/logout, switching profiles, per-call overrides, and config storage location.
allowed-tools: Bash(frontline:*)
---

# Authentication & Profiles

The `frontline` CLI authenticates against the **Frontline Public API** with a Bearer API key. The `max` binary shares the same key store — logging in with either keeps both in sync.

## Getting an API key from the app

Open the Frontline app, click your **user name in the bottom-left of the sidebar**, and choose **Settings**.

- **Personal (USER) key** — recommended for CLI use. Under **My settings** → **Bring your own Agent** → **Create personal API key**. Each user can hold up to **5 personal keys**. This is the key type the CLI is most useful with: writes are attributed to the user.
- **Account (GENERAL) key** — under **Account settings** → **Developer** → **Create API key**. Read-only integrations and dashboards. Does **not** work on endpoints that require `USER` scope (they return `401`).

Copy the key the moment it's shown — Frontline stores only the SHA-256 hash, so it can never be displayed again. If you lose a key, delete it from that same screen and create a new one.

## Quick start

```bash
frontline auth login <api-key>
```

This stores the key in the **current profile** (default name: `default`) and points it at the production Public API at `https://prod-api.getfrontline.ai/public/v1`. It also writes the same key to the matching Max profile.

## Managing profiles

### Create a profile for each environment

```bash
# Production (uses the default base URL)
frontline auth login <prod-key> --profile prod

# A custom environment / on-prem
frontline auth login <key> --profile staging --base-url https://staging-api.example.com/public/v1
```

Passing `--profile` to `login` switches the active profile to the new one automatically.

### Switch the active profile

```bash
frontline auth profiles use prod
```

After this, every command without an explicit `--profile` uses the `prod` key and base URL.

### List profiles

```bash
frontline auth profiles list             # JSON output (default)
frontline auth profiles list --pretty    # human-readable
```

Shows each profile's redacted key preview, base URL, which one is active, and the on-disk config path.

### Check identity

```bash
frontline auth whoami
```

Calls `GET /public/v1/me` and prints the account (and user, for `USER` keys) the active key represents.

### Remove a profile

```bash
frontline auth logout                    # removes the active profile
frontline auth logout --profile staging  # removes a named profile
```

`max auth logout` also removes the matching Frontline profile by default. Pass `--keep-frontline` on the Max side to clear only Max.

## Per-call overrides

Any command accepts these one-off flags:

```bash
frontline agents list --api-key <other-key>
frontline agents list --profile staging
frontline agents list --base-url https://staging-api.example.com/public/v1
```

Useful for scripts and CI where you don't want to persist credentials.

Pass `--profile`, `--api-key`, and `--base-url` on the **leaf command** (the subcommand you run), not immediately after the `frontline` binary:

```bash
frontline auth whoami --profile staging          # correct
frontline sharing get --profile user-a ...       # correct
frontline --profile staging auth whoami          # wrong — Commander rejects this
```

## Resolution priority

When a command needs credentials, the CLI resolves them in this order:

1. `--api-key` / `--base-url` flags on the command.
2. `FRONTLINE_API_KEY` / `FRONTLINE_BASE_URL` environment variables.
3. The active profile's stored values.
4. Built-in default base URL: `https://prod-api.getfrontline.ai/public/v1`.

## Config location

Config is stored by the OS using the standard `conf` package paths:

- **macOS**: `~/Library/Preferences/frontline-cli-nodejs/`
- **Linux**: `~/.config/frontline-cli-nodejs/`
- **Windows**: `%APPDATA%\frontline-cli-nodejs\Config\`

Run `frontline auth profiles list --pretty` to print the exact path the CLI is using.

## Typical workflow

```bash
# 1. Set up profiles once
frontline auth login <dev-key>  --profile dev
frontline auth login <prod-key> --profile prod

# 2. Work in dev
frontline auth profiles use dev
frontline object list
frontline agents list

# 3. Switch to prod when needed
frontline auth profiles use prod
frontline workflows list

# 4. Quick one-off against a third profile without switching
frontline object list --profile staging
```

## Troubleshooting

| Symptom                        | Likely cause                                                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| `"No API key found"`           | No profile is configured. Run `frontline auth login <key>`.                                                   |
| `"Missing or invalid API key"` | Key was revoked or expired. Generate a new one and `frontline auth login` again.                              |
| `401 Unauthorized` on writes   | You're using a `GENERAL` key on a `USER`-only endpoint. Create a personal key under **Bring your own Agent**. |
| `429 Too Many Requests`        | Rate limit is 1000 req/min per account. Back off and retry.                                                   |

## See also

- **API authentication reference**: <https://docs.getfrontline.ai/docs/authentication>
- **CLI auth page**: <https://docs.getfrontline.ai/cli/authentication>
- For UI walkthroughs (channels, billing, etc.): <https://help.getfrontline.ai>
