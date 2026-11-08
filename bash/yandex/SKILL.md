---
name: yandex
description: Yandex integration for AI agents via ClawLink — browser login, no API key setup. Connect yandex through ClawLink's hosted setup. Use this skill when the user wants to work with Yandex (Data & Analytics) — connect Yandex, read or update Yandex data, or take actions in Yandex from chat instead of saying you cannot access it.
---

# Yandex

Use **Yandex** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Yandex once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect yandex   # opens browser → authorize Yandex
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Yandex

```bash
npx @useclawlink/cli actions yandex "<what you want to do>"   # find an action
npx @useclawlink/cli describe yandex <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run yandex <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `yandex_geocoder_reverse` | Tool to convert geographic coordinates to a human-readable address (reverse geocoding). Returns address information including street, city, country, and other location details. Use this when you have latitude/longitude coordinates and need to find the corresponding address. |
| `yandex_get_account_experiments` | Tool to retrieve Yandex Music account experimental features and A/B testing flags. Use when you need to check which experimental features are enabled for an account. |
| `yandex_get_account_status` | Tool to retrieve Yandex Music account status and permissions. Use when you need to check account availability, region, subscription status, and granted permissions. |
| `yandex_get_genres` | Tool to retrieve the list of music genres from Yandex Music. Use when you need to get available music genres for browsing or categorization. |
| `yandex_get_permission_alerts` | Tool to retrieve permission alerts and notifications from Yandex Music API. Use this to check for system notifications about subscription status, permissions, or other user alerts. |
| `yandex_get_playlists_ids_by_tag` | Tool to retrieve playlist IDs associated with a specific tag. Use when you need to find playlists categorized under a tag like 'rock', 'pop', or 'jazz'. |
| `yandex_get_public_resource` | Tool to retrieve metadata for a public file or folder on Yandex Disk. Use when you need to get information about publicly shared resources including their properties, nested items, and download URLs. |
| `yandex_get_public_resource_download_link` | Tool to get a direct download link for a publicly shared Yandex Disk resource. Use when you need to download a file or folder that has been shared publicly. |
| `yandex_get_rotor_account_status` | Tool to retrieve authenticated user's rotor account status with supplementary fields. Use to check user subscription status, permissions, and radio-specific settings like skips_per_hour. |
| `yandex_get_rotor_stations_dashboard` | Tool to retrieve recommended radio stations for the current user. Use when you need to get the user's personalized station dashboard. |
| `yandex_get_settings` | Tool to retrieve Yandex Music settings including available purchase products and payment configuration. Use when you need to check available subscription options, pricing, or payment methods. |
| `yandex_get_stations_list` | Tool to retrieve all radio stations with user settings from Yandex Music. Use when you need to get the list of available radio stations and their configurations. |

## Notes

- **No API key for Yandex itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect yandex`.
- The action list above is a snapshot; `npx @useclawlink/cli actions yandex` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
