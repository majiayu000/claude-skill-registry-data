---
name: bilibili-cli
description: Interact with Bilibili (B站/哔哩哔哩) via CLI — fetch video info, subtitles, comments, download audio, search users/videos, browse trending rankings, manage favorites, and perform interactions like likes and triple-clicks
---

# bilibili-cli Skill

A CLI tool for interacting with Bilibili (哔哩哔哩). Use it to fetch video info, search content, browse user profiles, download audio, and perform interactions like liking or triple-clicking.

## Prerequisites

```bash
# Install (requires Python 3.10+)
pip install bilibili-cli
# Or: uv tool install bilibili-cli
```

## Authentication

Most read commands work without login. Subtitles, favorites/following/watch-later/history, feed, and interactions require login.

```bash
bili status                    # Check if logged in
bili login                     # QR code login (if not authenticated)
```

Authentication auto-detects local browser cookies (Chrome/Firefox/Edge/Brave). If cookies are found and valid, no manual login needed.

## Command Reference

### Video

```bash
# Get video details (accepts BV ID or full URL)
bili video BV1ABcsztEcY
bili video https://www.bilibili.com/video/BV1ABcsztEcY

# Options
bili video BV1ABcsztEcY --subtitle      # Show subtitles (AI or uploaded)
bili video BV1ABcsztEcY --ai            # Show B站 AI summary
bili video BV1ABcsztEcY --comments      # Show top comments
bili video BV1ABcsztEcY --related       # Show related videos
bili video BV1ABcsztEcY --json          # Raw JSON output
```

### User

```bash
# Look up user profile (by UID or username)
bili user 946974
bili user "影视飓风"

# List user's videos
bili user-videos 946974 --max 20
bili user-videos "影视飓风" --json
```

### Search

```bash
# Search users (default)
bili search "关键词"

# Search videos
bili search "关键词" --type video
```

### Discovery

```bash
bili hot                       # Trending/popular videos
bili hot --max 10               # Limit results
bili rank                      # Site-wide ranking
bili feed                      # Dynamic timeline (requires login)
```

### Collections (require login)

```bash
bili favorites                 # List favorite folders
bili favorites <ID> --page 2   # Videos in a folder
bili following                 # Following list
bili watch-later               # Watch later list
bili history                   # Watch history
```

### Audio Extraction

```bash
# Download audio and split into ASR-ready WAV segments (25s each, 16kHz mono)
bili audio BV1ABcsztEcY                 # Split to /tmp/bilibili-cli/{title}/
bili audio BV1ABcsztEcY --segment 60    # 60s per segment
bili audio BV1ABcsztEcY --no-split      # Full m4a file, no splitting
bili audio BV1ABcsztEcY -o ~/data/      # Custom output directory
```

### Interactions (require login)

```bash
bili like BV1ABcsztEcY         # Like a video
bili like BV1ABcsztEcY --undo  # Unlike
bili coin BV1ABcsztEcY         # Give 1 coin
bili coin BV1ABcsztEcY -n 2    # Give 2 coins
bili triple BV1ABcsztEcY       # 一键三连 (like + coin + favorite)
```

### Account

```bash
bili status                    # Quick login check
bili whoami                    # Detailed profile info
bili whoami --json              # Profile as JSON
bili login                     # QR code login
bili logout                    # Clear credentials
```

## JSON Output

Major query commands support `--json` for machine-readable output:

```bash
bili video BV1ABcsztEcY --json | python3 -c "import sys,json; print(json.load(sys.stdin)['stat']['view'])"    # Get view count
bili hot --json | python3 -c "import sys,json; print(json.load(sys.stdin)['list'][0]['title'])"                # First trending title
bili user 946974 --json | python3 -c "import sys,json; print(json.load(sys.stdin)['user_info']['name'])"       # Username
```

## Common Patterns for AI Agents

```bash
# Get a video's subtitle text for summarization
bili video BV1ABcsztEcY --subtitle

# Extract audio for speech-to-text (ASR)
# Segments are saved to /tmp/bilibili-cli/{title}/seg_000.wav, seg_001.wav, ...
bili audio BV1ABcsztEcY --segment 25

# Find a user's latest video BV ID
bili user-videos 946974 --max 1 --json | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['bvid'])"

# Check if logged in before performing actions
bili status && bili like BV1ABcsztEcY

# Search and get first result
bili search "topic" --type video --json | python3 -c "import sys,json; r=json.load(sys.stdin); print(r[0]['bvid'] if r else 'not found')"
```

## Error Handling

- Commands exit with code 0 on success, non-zero on failure
- Error messages are prefixed with ❌
- Login-required commands show ⚠️ with instruction to run `bili login`
- Invalid BV IDs show a clear error message
