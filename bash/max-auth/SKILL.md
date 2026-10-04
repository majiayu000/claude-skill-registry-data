---
name: max-auth
allowed-tools: Bash(max:*)
description: Manage Max CLI authentication — store per-user API key (synced with Frontline CLI), sign out, and inspect the active profile. Use when the user needs Max terminal auth, whoami, or clearing credentials.
---

## Prerequisites

- The `max` CLI must be installed (`npm i -g @getfrontline/cli` — provides both `frontline` and `max` binaries).
- A **per-user API key** from the Frontline web app. To get one: click your user name in the bottom-left of the sidebar → **Settings** → **My settings** → **Bring your own Agent** → **Create personal API key**. Up to 5 per user. The browser SSO (Firebase) flow is **paused** in the CLI; `MAX_CLI_AUTH_URL` is not required for the current flow.
- See the **[CLI authentication docs](https://docs.getfrontline.ai/cli/authentication)** for the full breakdown.

## How credentials work

- `max auth login <api-key>` saves the same key to the **Max** store (`max-cli`) and the **Frontline** store (`frontline-cli`) under the **same profile name**, so `max` and `frontline` stay aligned.
- `max` commands call the **Public API** (`…/public/v1/max/...`) with `Authorization: Bearer <apiKey>` (USER key, same as SoR).
- Public API base URL: same as `frontline` — `FRONTLINE_BASE_URL`, profile `baseUrl`, or `--base-url` on each command (`max auth login --base-url …` persists it on the Frontline profile).
- API key resolution: `--api-key` → `MAX_API_KEY` / `FRONTLINE_API_KEY` → Max profile `apiKey` → Frontline profile `apiKey` (same name).

## Commands

### Sign in (save API key)

```bash
max auth login <api-key> [--profile <name>] [--base-url <url>]
```

| Option             | Description                                                                                          |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| `<api-key>`        | Per-user API key (required argument)                                                                 |
| `--profile <name>` | Profile to save under (default: current; if set, also switches active profile for Max and Frontline) |
| `--base-url <url>` | Public API root for **both** `max` and `frontline` on that profile (must end with `/public/v1`)      |

**Examples:**

```bash
max auth login flk_abc123

max auth login flk_abc123 --profile staging \
  --base-url https://staging-api.example.com/public/v1
```

### Sign out

```bash
max auth logout [--profile <name>] [--keep-frontline]
```

| Option             | Description                                                    |
| ------------------ | -------------------------------------------------------------- |
| `--profile <name>` | Profile to clear (default: current)                            |
| `--keep-frontline` | Only clear the Max store; leave the matching Frontline profile |

By default, the matching Frontline profile is removed too.

### Check profile / credentials

```bash
max auth whoami [--json] [--profile <name>]
```

Shows API key preview, `maxApiBaseUrl`, whether a matching Frontline profile exists, and Max config path (no JWT decode; browser SSO is paused).

### Config path

```bash
max config-path
```

## Troubleshooting

- **"No API key saved for profile …"** — run `max auth login <api-key>` or `frontline auth login <api-key>` with the same `--profile`.
- **"No Max API key found"** — same as above, or set `MAX_API_KEY` / `FRONTLINE_API_KEY`.
- **401 on Max** — key revoked or wrong; create a new key in the app and run `max auth login` again.

## Browser SSO note

The legacy flow (`max auth login` with no argument, hosted page + localhost callback) is commented out in the package. To restore it later, see git history and `packages/cli/src/max/browserLogin.ts`.
