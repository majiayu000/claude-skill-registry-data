---
name: tgsearch
description: Search Telegram from the CLI — discover public channels by keyword or search messages within a channel. Use when the user wants to find Telegram channels, look up posts/messages in a channel, or do Telegram OSINT from the terminal.
---

# tgsearch

CLI for Telegram search, built on Telethon (MTProto user API — not the Bot API).

## Setup

1. `pip install telethon`
2. Set `TG_API_ID` and `TG_API_HASH` in the environment — get them at https://my.telegram.org (API Development Tools).
3. First run prompts for phone number + login code; the session is cached in `tgsearch.session` afterwards.

## Usage

Run the script in this skill's directory (`tgsearch.py`):

```bash
python3 tgsearch.py find "osint"              # discover public channels by keyword
python3 tgsearch.py find "osint" -n 50        # more results
python3 tgsearch.py grep @channelname "cve"   # search messages within a channel
python3 tgsearch.py grep @channelname "cve" -n 100
```

Output of `find`: `@username  members  title` per line. Output of `grep`: `date  first-100-chars-of-message` per line.

## Notes

- `find` uses Telegram's contacts search — the same discovery the apps use. There is no API for a true global search of all public channels; results are what Telegram returns for the account.
- `grep` searches message text server-side in a single channel the account can see (public channels work without joining).
- Rate limits apply: keep `-n` modest and avoid rapid repeated calls.
