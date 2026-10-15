---
name: Spotify
description: Control Spotify playback via Web API — now playing, search, play/pause/next/previous.
requires:
  bins: []
  env: [SPOTIFY_ACCESS_TOKEN]
---

# Spotify

Use this skill to inspect what is playing, search music, and control
playback on any Spotify Connect device.
It calls Spotify Web API directly (no CLI/TUI wrapper).

## Use when

- "what is playing right now?"
- "play playlist X"
- "next track"
- "lower the volume" (with `play/device_id` to target a specific device)

## Do not use when

- No device is connected to Spotify Connect → API returns
  `NO_ACTIVE_DEVICE` (-32070). Open Spotify on a device first.
- You need local audio synthesis (TTS, non-Spotify playback) → use a different skill.
- You need library edits/playlist creation → possible via API but out of v0.1 scope.

## Auth

Requires `SPOTIFY_ACCESS_TOKEN` (user scope). The refresh-token flow is
managed by the operator (Spotify OAuth 2.0 PKCE or Authorization Code).
This extension **does not** auto-refresh tokens. If a token expires,
rotate it externally and update env.

## Tools

### `status`
Token presence and endpoint status. Use before issuing playback commands.

### `now_playing`
Returns `{is_playing, progress_ms, track, artists, album, uri, device}`.
204/"no active device" → `{is_playing:false, reason:"no active device"}`.

### `search { query, types?, limit? }`
- `types` default `track`; accepts `track,artist,album,playlist,show,episode,audiobook`
- `limit` 1..50 (default 10)

Returns raw `/v1/search` JSON. Useful as input for a follow-up `play`.

### `play { uri?, device_id? }`
- Without `uri`: resume playback.
- `spotify:track:...` plays that track.
- `spotify:album:...` / `spotify:playlist:...` / `spotify:artist:...` sets `context_uri`.
- `device_id` optional: targets a specific device.

### `pause { device_id? }` · `next { device_id? }` · `previous { device_id? }`
Direct playback controls.

## Execution guidance

- If `-32070 NO_ACTIVE_DEVICE`: tell the user to open Spotify on a
  speaker/phone and retry.
- If `-32011 unauthorized`: token expired; operator must rotate it.
- If `-32013 rate limited`: respect `retry_after` from the response.
- Save `device.id` from `now_playing` for later calls to avoid
  additional discovery steps.
