---
name: chill-putio
description: Automate chill.institute torrent/magnet ingestion into put.io. Use when asked to search, scan, or fetch torrent/magnet links from chill.institute and add them to put.io, or when troubleshooting the chill/put.io ingestion pipeline (cookies, profiles, put.io token).
---

# Chill → put.io

## Quick start

1) Ensure Chrome is logged in to `https://chill.institute` on **mb-server**.
2) Confirm cookies can be read:

```bash
sweetcookie --browser chrome --profile "Default" --domain "chill.institute" --format cookie-header
```

3) Scan a page for magnet/torrent links (dry run):

```bash
chillput --url "https://chill.institute" --dry-run
```

4) Add new links to put.io:

```bash
chillput --url "https://chill.institute"
```

## How it works

- `chillput` uses `sweetcookie` (SweetCookieKit CLI) to read Chrome cookies on mb-server.
- It fetches the provided chill.institute page, extracts magnet/torrent links, and POSTs them to put.io.
- Dedupe state is stored at `~/.cache/chillput/state.json`.

## Config

Env file:
- `PUTIO_OAUTH_TOKEN` (required)
- `CHILL_COOKIE_DOMAIN` (default: `chill.institute`)
- `CHILL_COOKIE_PROFILE` (default: `Default`)

Location:
- `/Users/mariano/Coding/infra/chillinstitute/.env`

Override via CLI:
- `--profile "Default"`
- `--domain "chill.institute"`
- `--env /path/to/.env`

## Notes / gotchas

- Chrome profiles are usually named `Default`, `Profile 1`, etc. The displayed Chrome account name is **not** the profile id.
- First cookie read may require a macOS Keychain prompt for “Chrome Safe Storage”. Approve once on mb-server.
- If `sweetcookie` fails with a profile name, retry without `--profile` (the CLI already does this fallback).

## Useful commands

List available Chrome stores:
```bash
sweetcookie --list-stores --browser chrome
```

Show help:
```bash
chillput --help
```

## References
- See `references/usage.md` for CLI paths and troubleshooting.
