---
name: spotify-player
description: "Terminal playback and search via spogo or spotify_player."
version: 1.0.0
author: External Agent contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [spotify, music, playback, spogo, spotify-player, premium]
    category: media
    related_skills: [youtube-content]
---

# Spotify Player Skill

Control Spotify playback and search from the terminal. Use `spogo` (preferred) for Spotify playback/search. Fall back to `spotify_player` if needed. Ported from External Agent `skills/spotify-player/SKILL.md`; `spotify_player` commands checked against the real 0.25.2 binary, `spogo` commands against upstream docs.

## When to Use

- Searching for a song, album, or artist on Spotify.
- Playing, pausing, skipping, or going back in what is playing.
- Moving playback to a different device, checking what is playing, liking the current track.
- Do not use for downloading music or for non-Spotify playback.

## Prerequisites

- A Spotify Premium account (playback control is Premium-only).
- Either `spogo` or `spotify_player` installed on the host. Neither is bundled with Hermes; the host owner installs one:
  - `spogo`: `brew install spogo` (tap `steipete/tap`)
  - `spotify_player`: `brew install spotify_player`, `cargo install spotify_player`, or a prebuilt binary from the project's releases page
- Auth is per-CLI, done once by the host owner:
  - `spogo`: import cookies with `spogo auth import --browser chrome`
  - `spotify_player`: run `spotify_player authenticate` first; for Spotify Connect, set a user `client_id` in its config
- Run commands through `terminal`.

## How to Run

Prefer `spogo`. When driving it non-interactively (scripts, agents), pass `--json` and `--no-input`: with no TTY on stdin, `spogo` refuses to prompt, so `--no-input` makes that explicit and `--json` keeps output machine-readable.

## Quick Reference

| Need | spogo (preferred) | spotify_player (fallback) |
|---|---|---|
| Search | `spogo search track "query"` | `spotify_player search "query"` |
| Play / pause / next / previous | `spogo play`, `spogo pause`, `spogo next`, `spogo prev` | `spotify_player playback play`, `... pause`, `... next`, `... previous` |
| Toggle play/pause | — | `spotify_player playback play-pause` |
| Start a track | `spogo play <id\|url>` | `spotify_player playback start track --name "<phrase>"` |
| Devices | `spogo device list`, `spogo device set "<name\|id>"` | `spotify_player connect` |
| Status | `spogo status` | `spotify_player get` |
| Like current track | — | `spotify_player like` |

## Procedure

### spogo

```
terminal(command="spogo search track \"query\" --json --no-input")
terminal(command="spogo play --no-input")
terminal(command="spogo pause --no-input")
terminal(command="spogo next --no-input")
terminal(command="spogo prev --no-input")
terminal(command="spogo device list --no-input")
terminal(command="spogo device set \"<name|id>\" --no-input")
terminal(command="spogo status --json --no-input")
```

### spotify_player (fallback)

```
terminal(command="spotify_player search \"query\"")
terminal(command="spotify_player playback play")
terminal(command="spotify_player playback pause")
terminal(command="spotify_player playback next")
terminal(command="spotify_player playback previous")
terminal(command="spotify_player playback play-pause")
terminal(command="spotify_player playback start track --name \"<phrase>\"")
terminal(command="spotify_player connect")
terminal(command="spotify_player like")
```

## Pitfalls

- Playback commands need an active Spotify session on a device; if nothing played recently, start playback in a Spotify app first, then control it from the CLI.
- `spotify_player` CLI commands talk to a client socket (default port `8080`); if no instance is running, a new client starts, which adds latency to the first call.
- Config folder: `~/.config/spotify-player` (for example `app.toml`).
- TUI shortcuts are available via `?` inside the `spotify_player` app — that is the interactive TUI, not the CLI surface above.
- Auth failures mean the CLI's own login/cookies expired: re-run the CLI's auth step (see Prerequisites) rather than working around it.

## Verification

- `spogo status` or `spotify_player get` returns the current playback state; a search returns JSON results for the query.
- Live check on the host: one of the CLIs is installed and authenticated, and a search plus a play/pause round-trip work on a real device. The CLI and Spotify auth are host-side prerequisites; without them the skill reports the missing setup instead of working around it.
