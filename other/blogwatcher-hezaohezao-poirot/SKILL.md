---
name: blogwatcher
description: "Monitor blogs and RSS/Atom feeds via blogwatcher-cli."
allowed-tools:
  - bash
  - read_file
enabled: true
related-skills: []
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT); JulienTant/blogwatcher-cli
---

# Blogwatcher

Track blog and RSS/Atom feed updates with the `blogwatcher-cli` tool. Supports
automatic feed discovery, HTML scraping fallback, OPML import, and read/unread
article management.

## Prerequisites

`blogwatcher-cli` must be installed. Pick one method:

```bash
# Go install
go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest

# Binary (Linux amd64)
curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli

# Docker
docker run --rm -v blogwatcher-cli:/data ghcr.io/julientant/blogwatcher-cli scan
```

All releases: https://github.com/JulienTant/blogwatcher-cli/releases

Verify installation:
```bash
blogwatcher-cli --version
```

## When to Use

- User wants to monitor blog updates
- User wants to track RSS/Atom feeds
- User wants to import OPML subscriptions
- User wants a digest of new articles from tracked blogs

## Common Commands

```bash
# Add a blog to track
blogwatcher-cli add https://example.com/blog

# Add with explicit feed URL
blogwatcher-cli add https://example.com/blog --feed https://example.com/feed.xml

# Scan for new articles
blogwatcher-cli scan

# List tracked blogs
blogwatcher-cli list

# List unread articles
blogwatcher-cli articles --unread

# Mark article as read
blogwatcher-cli read <article-id>

# Import OPML
blogwatcher-cli import subscriptions.opml

# Export OPML
blogwatcher-cli export > subscriptions.opml
```

## Workflow

### Setup (first time)

```bash
# Install blogwatcher-cli (see Prerequisites)
# Add blogs to track
blogwatcher-cli add https://blog1.com
blogwatcher-cli add https://blog2.com

# Or import existing OPML
blogwatcher-cli import my-subscriptions.opml
```

### Daily check

```bash
# Scan for new articles
blogwatcher-cli scan

# Show unread
blogwatcher-cli articles --unread

# Read an article (marks as read)
blogwatcher-cli read <article-id>
```

### Automated monitoring

Set up a cron job to scan periodically:

```bash
# Scan every morning at 8am
echo "0 8 * * * blogwatcher-cli scan" | crontab -
```

## Docker with persistent storage

The database lives at `~/.blogwatcher-cli/blogwatcher-cli.db` by default. In
Docker, use a volume to persist:

```bash
# Named volume
docker run --rm -v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan

# Host bind mount
docker run --rm -v /path/on/host:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan
```

## Pitfalls

- **blogwatcher-cli not installed**: this skill requires the external tool.
  Install first (see Prerequisites).
- **Feed discovery fails**: some sites don't expose `<link rel="alternate">`
  tags. Use `--feed` to specify the feed URL explicitly.
- **Rate limiting**: scanning many feeds rapidly may get you blocked. The tool
  handles this, but don't run `scan` too frequently.
- **Database location**: if using Docker, always set `BLOGWATCHER_DB` to a
  volume-mounted path, or data is lost on container exit.
- **OPML encoding**: ensure OPML files are UTF-8 encoded for proper import.
