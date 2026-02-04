---
name: scratchpad-fetch
description: Download and aggregate web pages/docs into timestamped scratchpad files. Use when user asks to "concatenate all these resources", "get all these links", "checkout all these resources", or wants to gather fresh context from documentation URLs. All URLs from one prompt go into single file at docs/scratchpad/<timestamp>.md.
allowed-tools: Bash
---

# Scratchpad Fetch

## Overview

Downloads web pages via curl and appends content to timestamped scratchpad file. All URLs from single user prompt → single file. Simple context gatherer for documentation.

## Usage

When user provides URLs and asks to:
- "concatenate all these resources"
- "get all these links"
- "checkout all these resources"
- "gather these docs"
- "download these pages"

**Execute:**

```bash
./skills/scratchpad-fetch/scripts/fetch_urls.sh <url1> <url2> <url3> ...
```

**Output:** `docs/scratchpad/YYYYMMDD_HHMMSS.md`

## Script Behavior

`fetch_urls.sh`:
- Creates `docs/scratchpad/` if missing
- Generates timestamp: `YYYYMMDD_HHMMSS`
- Downloads each URL with curl
- Appends all content to single file
- Adds headers/separators for readability
- Reports success/failure per URL

## Example

User: "checkout all these resources: https://example.com/api https://example.com/guide"

```bash
./skills/scratchpad-fetch/scripts/fetch_urls.sh \
  https://example.com/api \
  https://example.com/guide
```

Output: `docs/scratchpad/20250129_143052.md` containing both pages.

## Notes

- Dumb but effective for gathering fresh docs
- One prompt = one file
- curl follows redirects (`-L`)
- Failures logged but don't stop other URLs
