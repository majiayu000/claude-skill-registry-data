---
name: playlistable-mcp
description: Create AI-powered Spotify playlists and discover music via Playlistable MCP. Use when the user wants to generate playlists from a mood/prompt, search songs or artists, get personalized playlist suggestions, or manage their playlists. Requires OAuth authentication via https://mcp.playlistable.io/authorize. Supports PLAYLISTABLE_API_KEY env var or config/auth.json.
metadata: {"clawdbot":{"emoji":"🎵","requires":{"bins":["node"],"env":["PLAYLISTABLE_API_KEY"]},"primaryEnv":"PLAYLISTABLE_API_KEY"}}
---

# Playlistable MCP

Create AI-powered Spotify playlists and discover music using the Playlistable MCP server.

## Authentication

Needs a Playlistable API key (`PLAYLISTABLE_API_KEY` env var or `config/auth.json`).

To get one:

```bash
node {baseDir}/scripts/auth.mjs
```

Fully automatic — starts a local HTTP server, opens browser for Spotify OAuth, catches the redirect, exchanges the code for an API key via PKCE, and saves it to `{baseDir}/config/auth.json`. No manual copy-paste needed.

If the key is already saved, scripts read it automatically from `config/auth.json`.

## How it works

The MCP server at `https://mcp.playlistable.io` exposes tools via Streamable HTTP transport. The `mcp-call.mjs` script sends JSON-RPC requests directly — no MCP SDK needed.

### Common workflows

**Generate a playlist:** User describes a mood → `generate_playlist` creates an async Spotify playlist → returns playlist URL immediately. Tracks appear in the background.

**Browse playlists:** `get_playlists` lists all user playlists. `get_playlist` gets details + tracks for a specific one.

**Edit a playlist:** `edit_playlist` adds or removes songs by Spotify track ID.

**Search music:** `search_songs` and `search_artists` search Spotify directly.

**Get suggestions:** `playlist_suggestions` returns 6 AI-generated mood suggestions based on the user's listening history and time of day.

## Scripts

### Authenticate

```bash
node {baseDir}/scripts/auth.mjs
```

### Call MCP tools

```bash
node {baseDir}/scripts/mcp-call.mjs <tool> [json-params]
node {baseDir}/scripts/mcp-call.mjs --list-tools
```

**Examples:**

```bash
# Generate a playlist
node {baseDir}/scripts/mcp-call.mjs generate_playlist '{"mood": "chill lo-fi for studying"}'

# Get personalized suggestions
node {baseDir}/scripts/mcp-call.mjs playlist_suggestions '{"userHour": 22}'

# List playlists
node {baseDir}/scripts/mcp-call.mjs get_playlists

# Get playlist details
node {baseDir}/scripts/mcp-call.mjs get_playlist '{"id": "PLAYLIST_ID"}'

# Edit playlist songs
node {baseDir}/scripts/mcp-call.mjs edit_playlist '{"id": "PLAYLIST_ID", "addedSongs": ["4iV5W9uYEdYUVa79Axb7Rh"], "removedSongs": []}'

# Delete playlist
node {baseDir}/scripts/mcp-call.mjs delete_playlist '{"id": "PLAYLIST_ID"}'

# Search songs
node {baseDir}/scripts/mcp-call.mjs search_songs '{"query": "Blinding Lights", "limit": 5}'

# Search artists
node {baseDir}/scripts/mcp-call.mjs search_artists '{"query": "The Weeknd", "limit": 5}'

# List all available tools
node {baseDir}/scripts/mcp-call.mjs --list-tools
```

## Available MCP Tools

| Tool | Description | Key params |
|------|-------------|------------|
| `generate_playlist` | Create a playlist from a mood/prompt | `mood` (string, required) |
| `get_playlist` | Get playlist details + tracks | `id` (string, required) |
| `get_playlists` | List user's playlists (paginated) | `lastDocId` (string, optional) |
| `edit_playlist` | Add/remove songs by Spotify track ID | `id`, `addedSongs`, `removedSongs` |
| `delete_playlist` | Delete a playlist | `id` (string, required) |
| `playlist_suggestions` | Get 6 AI mood suggestions | `userHour` (0-23, optional) |
| `search_songs` | Search Spotify tracks | `query`, `limit` (1-10) |
| `search_artists` | Search Spotify artists | `query`, `limit` (1-10) |

See [references/api_reference.md](references/api_reference.md) for full parameter details, response formats, and error handling.

## Playlist Generation Flow (important)

Playlist generation takes ~30 seconds. Always follow this flow:

1. Call `generate_playlist` → returns immediately with `id` and Spotify URL
2. **Share the Spotify URL with the user right away** so they have it
3. Wait ~15s, then poll `get_playlist` every 10 seconds until `status === "ready"`
4. Once ready, display the track list to the user

Use the `--wait` flag to handle this automatically:

```bash
node {baseDir}/scripts/mcp-call.mjs generate_playlist '{"mood": "..."}' --wait
```

This generates, polls until ready (~30s), then prints the full playlist with tracks.

## Notes

- Free users get a limited "teaser" playlist. Paid users get full playlists.
- `playlist_suggestions` is time-aware — pass `userHour` for better results (morning workout vs late-night chill).
- Songs are identified by **Spotify track IDs** (e.g., `4iV5W9uYEdYUVa79Axb7Rh`). Use `search_songs` to find IDs.
