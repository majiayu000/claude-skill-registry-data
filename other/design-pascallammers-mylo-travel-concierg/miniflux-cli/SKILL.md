---
name: miniflux-cli
description: Command-line interface for managing Miniflux feeds. Use for authentication, adding feeds, and searching entries.
---

# Miniflux-CLI

Miniflux-CLI is a command-line interface for managing Miniflux feeds. Use this to authenticate with Miniflux, add new feeds, and search entries.

## Getting Started

Before using any commands (except `login` and `logout`), you must authenticate with your Miniflux instance.

### Login

Authenticate with your Miniflux instance:

```bash
miniflux-cli login --endpoint <URL> --api-key <KEY>
```

- `--endpoint`: Your Miniflux instance URL (e.g., `https://miniflux.example.com`)
- `--api-key`: API key from Miniflux Settings

The configuration is saved to `~/.config/miniflux-cli/config.toml` and verified automatically.

### Logout

Remove stored credentials:

```bash
miniflux-cli logout
```

## Commands

### Add a New Feed

```bash
miniflux-cli add <feed_url>
```

Add a new RSS/Atom feed to your Miniflux instance.

**Important:** Before adding a feed, verify that the URL returns valid RSS/Atom XML. The Miniflux instance may be rate limited by the target server if it repeatedly attempts to fetch invalid or non-existent feed URLs. Use a tool like `curl` or a browser to validate the feed first.

Example:
```bash
miniflux-cli add https://example.com/feed.xml
```

### List Entries

```bash
miniflux-cli list [OPTIONS]
```

List feed entries (ordered by publication date, newest first). Default shows only unread entries.

**Options:**
- `--limit <n>`: Maximum number of results (default: 30)
- `--search <query>`: Search through entries with query text
- `--starred`: Filter by starred entries only
- `--all`: List all entries (default is unread only)
- `--json`: Output in JSON format

Examples:
```bash
# List latest 30 unread entries
miniflux-cli list

# List all entries
miniflux-cli list --all

# Search entries
miniflux-cli list --search "golang"

# List starred entries with limit
miniflux-cli list --starred --limit 50

# Combine multiple filters
miniflux-cli list --all --search "golang" --limit 20
miniflux-cli list --search "golang" --json
```

## Configuration

Authentication credentials are stored in `~/.config/miniflux-cli/config.toml` with the following format:

```toml
endpoint = "https://miniflux.example.com"
api_key = "your-api-key"
```

## Error Handling

If you see "failed to load config" errors, run `miniflux-cli login` to set up your credentials.

## Help

Display help for any command:

```bash
miniflux-cli --help
miniflux-cli login --help
miniflux-cli add --help
miniflux-cli search --help
```
