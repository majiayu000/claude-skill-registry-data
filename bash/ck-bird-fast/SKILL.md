---
license: MIT
name: bird-fast
description: Post tweets, read threads, search X/Twitter from the terminal using the bird CLI. Use when automating Twitter/X, posting from scripts, analyzing tweet threads, monitoring mentions, or working with the Twitter API without OAuth setup.
---

# bird CLI

A command-line interface for X/Twitter that authenticates via your existing browser session — no API keys or OAuth setup required.

## Overview

bird is a TypeScript-based CLI that uses Twitter's internal GraphQL API with automatic query ID management. It extracts authentication cookies from Safari, Chrome, or Firefox.

**Key Features:**
- Zero-config authentication via browser cookies
- Full tweet lifecycle: post, reply, read, search
- Media uploads (images, GIFs, videos) with alt text
- Multiple output formats (human-readable, JSON, plain)
- Automatic GraphQL query ID refresh and REST API fallback

## When to Use

- Posting tweets or replies from scripts or automation
- Reading and analyzing tweet threads programmatically
- Searching for mentions or specific content
- Monitoring Twitter activity from the CLI

## Prerequisites

- **Node.js >= 22** OR Homebrew (for standalone binary)
- **Browser login**: Must be logged into x.com in Safari, Chrome, or Firefox

## Installation

```bash
# npm
npm install -g @steipete/bird

# pnpm
pnpm add -g @steipete/bird

# bun
bun add -g @steipete/bird

# Homebrew (macOS — standalone binary, no Node.js required)
brew install steipete/tap/bird

# One-shot execution (no install)
bunx @steipete/bird whoami
npx @steipete/bird whoami
```

## Authentication

bird uses a three-tier priority chain:

| Priority | Source | How to Set |
|----------|--------|-----------|
| 1 (highest) | CLI flags | `--auth-token`, `--ct0` |
| 2 | Environment variables | `AUTH_TOKEN`, `CT0` (or `TWITTER_AUTH_TOKEN`, `TWITTER_CT0`) |
| 3 (default) | Browser cookies | Auto-extracted from Safari → Chrome → Firefox |

**Verify authentication:**
```bash
bird whoami    # Shows authenticated user
bird check     # Shows credential source
```

## Quick Start

```bash
# Post a tweet
bird tweet "Hello from the terminal!"

# Read a tweet
bird read https://x.com/user/status/1234567890123456789

# Reply to a tweet
bird reply 1234567890123456789 "Great point!"

# Search tweets
bird search "from:elonmusk" -n 20

# View your mentions
bird mentions
```

## Command Reference

### Writing Commands

#### tweet
Post a new tweet with optional media.

```bash
bird tweet "<text>" [options]

# Options
--media <path>    Attach media file (repeatable, up to 4 images/GIFs or 1 video)
--alt <text>      Alt text for corresponding --media (repeatable)

# Examples
bird tweet "Check this out!"
bird tweet "Photo gallery" --media img1.jpg --alt "First photo" --media img2.jpg --alt "Second"
bird tweet "Demo video" --media demo.mp4
```

#### reply
Reply to an existing tweet.

```bash
bird reply <tweet-id-or-url> "<text>" [options]

# Examples
bird reply 1234567890123456789 "I agree!"
bird reply https://x.com/user/status/1234567890123456789 "Great thread!"
bird reply 1234567890123456789 "Here's a screenshot" --media shot.png --alt "Screenshot"
```

### Reading Commands

#### read
Fetch a single tweet. Handles standard tweets, Notes (long-form), and Articles.

```bash
bird read <tweet-id-or-url>

# Shorthand: just provide the ID or URL
bird 1234567890123456789
bird https://x.com/user/status/1234567890123456789
```

#### replies / thread

```bash
bird replies <tweet-id-or-url>    # All replies to a tweet
bird thread <tweet-id-or-url>     # Full conversation thread
```

### Search Commands

#### search

```bash
bird search "<query>" [-n <count>]

# Examples
bird search "claude ai" -n 20
bird search "from:anthropic"
bird search "@username"
```

Supports [Twitter's advanced search syntax](https://twitter.com/search-advanced): `from:`, `to:`, `since:`, `until:`, `filter:links`, etc.

#### mentions / bookmarks

```bash
bird mentions [-u <handle>] [-n <count>]    # Mentions of a user (defaults to you)
bird bookmarks [-n <count>]                  # Your bookmarked tweets
```

### Utility Commands

```bash
bird whoami                        # Show authenticated user
bird check                         # Verify credentials and show source
bird query-ids [--fresh] [--json]  # Inspect/refresh GraphQL query ID cache
bird help [command]                # Show help
```

## Global Options

| Option | Description |
|--------|-------------|
| `--auth-token <token>` | Twitter auth_token cookie |
| `--ct0 <token>` | Twitter ct0 cookie |
| `--cookie-source <source>` | Browser priority: `safari`, `chrome`, `firefox` (repeatable) |
| `--chrome-profile <name>` | Chrome profile name |
| `--firefox-profile <name>` | Firefox profile name |
| `--timeout <ms>` | Request timeout in milliseconds |
| `--plain` | Stable output: disable emoji and color (good for scripts) |
| `--no-emoji` | Disable emoji in output |
| `--no-color` | Disable ANSI colors |
| `--json` | Output as JSON (command-specific) |

## Media Attachments

| Type | Extensions | Limit |
|------|------------|-------|
| Images | `.jpg`, `.jpeg`, `.png`, `.webp` | Up to 4 |
| GIFs | `.gif` | Up to 4 |
| Videos | `.mp4`, `.m4v`, `.mov` | 1 only |

Cannot mix videos with images/GIFs.

```bash
# Alt text for accessibility
bird tweet "Three photos" \
  --media photo1.jpg --alt "Beach sunset" \
  --media photo2.jpg --alt "Mountain view" \
  --media photo3.jpg --alt "City skyline"
```

## Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| Human-readable | (default) | Interactive terminal |
| Plain | `--plain` | Scripting (no emoji/color) |
| JSON | `--json` | Programmatic parsing |

```bash
# Parse tweet data in a script
bird read 1234567890123456789 --json | jq '.text'

# Mention monitoring
bird mentions -n 50 --json | jq '.[] | {user: .user.screen_name, text: .text}'
```

## Configuration

Optional JSON5 config files:

| Location | Scope |
|----------|-------|
| `~/.config/bird/config.json5` | Global |
| `./.birdrc.json5` | Project-specific |

```json5
// Example config
{
  cookieSource: ["firefox", "safari"],
  firefoxProfile: "default-release",
  timeoutMs: 20000
}
```

## Examples

### Daily Automation Script

```bash
#!/bin/bash
DATE=$(date +"%B %d, %Y")
bird tweet "Daily status for $DATE: All systems operational. #status"
```

### Thread Analysis

```bash
# Get all replies to a viral tweet as JSON
bird replies https://x.com/user/status/1234567890123456789 --json | \
  jq '.[] | {user: .user.screen_name, text: .text, likes: .favorite_count}'
```

### Multi-Image Product Post

```bash
bird tweet "Product launch gallery 🚀" \
  --media hero.png --alt "Product hero shot" \
  --media feature1.png --alt "Feature overview" \
  --media feature2.png --alt "Technical specs" \
  --media pricing.png --alt "Pricing table"
```

### Monitor Mentions and Reply

```bash
#!/bin/bash
bird mentions -n 20 --json | jq -r '.[] | "\(.id) \(.user.screen_name): \(.text)"'
```

## Best Practices

- **Use `--json` for scripting** — always when parsing output programmatically
- **Use `--plain` in CI/CD** — avoids emoji/color issues in logs
- **Add alt text** — always include `--alt` when attaching images
- **Refresh query IDs proactively** — run `bird query-ids --fresh` if bird hasn't been used in a few days
- **Set env vars for automation** — use `AUTH_TOKEN` / `CT0` instead of browser cookies in scripts
- **Handle rate limits** — Twitter throttles; add delays (`sleep`) in bulk automation scripts

## Troubleshooting

### "No auth token found"

```bash
# Verify you're logged into x.com in your browser
# Try specifying the browser explicitly
bird whoami --cookie-source safari

# Or set credentials via environment
export AUTH_TOKEN="your-auth-token"
export CT0="your-ct0-token"
bird whoami
```

### GraphQL 404 errors

Query IDs may be stale. Refresh the cache:
```bash
bird query-ids --fresh
```

### Error 226 (automation detected)

bird automatically falls back to the REST API. If it persists, wait a few minutes and retry.

### Wrong account detected

```bash
# Multiple browser profiles may have different sessions
bird whoami --cookie-source chrome --chrome-profile "Profile 1"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Runtime error (network, auth, API) |
| 2 | Invalid usage (unknown command, bad arguments) |

## Technical Notes

- Uses Twitter's private GraphQL API endpoints
- Query IDs cached at `~/.config/bird/query-ids-cache.json` (24-hour TTL)
- Automatic query ID refresh on 404 errors
- REST API fallback (`statuses/update.json`) for error 226
- Subject to breakage if Twitter changes internal APIs

## Resources

- [GitHub Repository](https://github.com/steipete/bird) — Source code and issues
- [Changelog](https://github.com/steipete/bird/blob/main/CHANGELOG.md) — Version history
