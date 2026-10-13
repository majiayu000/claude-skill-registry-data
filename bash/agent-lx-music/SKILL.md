---
name: agent-lx-music
description: "Control agent-lx-music (alx) CLI to search, play, download music, fetch lyrics/covers, and manage playlists."
version: 2.0.0
author: agent-lx-music project
license: MIT
metadata:
  hermes:
    tags: [music, cli, playback, download, playlist, lyric, cover]
    related_skills: [mpv-media-player]
---

# agent-lx-music (alx) — Music CLI Agent Usage Guide

## Overview

`alx` is a terminal-native music CLI that replaces lx-music-desktop. It uses mpv as a detached daemon for playback, supports JS source scripts for URL resolution, and has native search for multiple music platforms.

All commands support `--json` output and `--quiet` to suppress non-data output.

## Quick Command Reference

### Search

```bash
alx search "keyword"                   # Search all platforms
alx search "keyword" --source kw       # Search specific platform (kw/wy/kg)
alx search "keyword" --limit 10        # Limit results
alx search "keyword" --id-only         # Output only CLI IDs (for piping)
alx search "keyword" --json            # JSON output
```

### Playback

```bash
alx play <cli_id>                      # Play by search result ID
alx play <cli_id> --quality flac24bit  # Play with specific quality
alx play <url>                         # Play direct URL
alx play /path/to/file.mp3            # Play local file
alx play --from-playlist "name"       # Play entire playlist
alx play --from-playlist "name" --shuffle  # Shuffle playlist
alx next / alx prev                   # Skip tracks
alx pause / alx resume / alx stop     # Playback control
alx seek +30 / alx seek 2:30 / alx seek 50%  # Seek
alx volume 80 / alx volume +10        # Volume (0-100)
alx repeat off|one|all                # Repeat mode
alx shuffle on|off                    # Shuffle mode
alx now                               # Current playback status
alx state                             # Full player state (JSON-friendly)
alx quit                              # Kill mpv daemon
```

### Download

```bash
alx download add <id>                          # Download single song
alx download add <id1> <id2> <id3>             # Download multiple songs
alx download add <id> --quality flac24bit      # Specific quality
alx download add --file playlist.m3u           # Batch from M3U/CSV/JSON
alx download status                            # Active downloads
alx download list                              # Download history
alx download retry <task_id>                   # Retry failed download
```

### Playlists

```bash
alx playlist list                      # List all playlists
alx playlist create "name"            # Create playlist
alx playlist delete "name"            # Delete playlist
alx playlist rename "old" "new"       # Rename playlist
alx playlist add "name" <id>          # Add song(s)
alx playlist remove "name" <id>       # Remove song
alx playlist show "name"              # Show playlist contents
alx playlist play "name"              # Play playlist
alx playlist play "name" --shuffle    # Shuffle play
alx playlist export "name" --format m3u   # Export (m3u/json/csv)
alx playlist import file.m3u --name "name"  # Import
```

### Favorites

```bash
alx fav list                          # List favorites
alx fav add                           # Add current song
alx fav add <id>                      # Add specific song
alx fav remove <id>                   # Remove from favorites
alx fav play                          # Play all favorites
```

### Lyrics & Cover

```bash
alx lyric                             # Lyrics for current song
alx lyric <id>                        # Lyrics for specific song
alx lyric <id> --translated           # Translated lyrics
alx lyric <id> --romanized            # Romanized lyrics
alx lyric <id> --save                 # Save as .lrc file
alx pic <id>                          # Cover art URL
alx pic <id> --save                   # Download cover art
```

### Source Management

```bash
alx source list                       # List installed sources
alx source add <path_or_url>          # Add source script
alx source remove <id>                # Remove source
alx source update <id>                # Update from remote URL
alx source test <id>                  # Health check (init/search/url)
alx source info <id>                  # Detailed source info
alx source health                     # Show source health & circuit breaker metrics
```

### Board & Discover

```bash
alx board                             # List available charts
alx board --source wy --id wy-hot    # Songs in a chart
alx board --source wy --id wy-hot --play  # Play chart
alx discover                          # Recommended playlists
alx discover --source kw --tag 华语   # Filter by tag
alx discover show <playlist-id>       # List songs
alx discover play <playlist-id>       # Play recommended playlist
```

### Queue

```bash
alx queue show                        # Show current queue
alx queue add <id>                    # Add to queue
alx queue insert <id>                 # Insert after current
alx queue remove <position>           # Remove by position
alx queue move <from> <to>            # Reorder
alx queue clear                       # Clear queue
```

### Local Library

```bash
alx local scan                        # Scan download dir (or beets)
alx local list                        # List indexed files
alx local play <index>                # Play local file
```

### Config

```bash
alx config                            # Show all config
alx config get <key>                  # Get value
alx config set <key> <value>          # Set value
alx config path                       # Config file path
```

## JSON Output

All commands support `--json` for structured output. Example search result:

```json
[
  {
    "cli_id": "04164d6d",
    "song_id": "228908",
    "name": "Sunny Day",
    "singer": "Jay Chou",
    "source": "kw",
    "interval": "04:29",
    "album_name": "Ye Hui Mei",
    "pic_url": "https://img3.kuwo.cn/..."
  }
]
```

## Aliases

- `sch` = `search`
- `dl` = `download`
- `pl` = `playlist`
- `q` = `queue`
- `lrc` / `lyr` / `lyrics` = `lyric`
- `cover` = `pic`
- `hot` = `board`
- `explore` = `discover`

## Verbose Mode

Use `--verbose` or `-v` for debug output showing which sources are queried, HTTP requests, and JS sandbox execution details.
