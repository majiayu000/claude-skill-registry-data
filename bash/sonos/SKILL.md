---
name: sonos
description: "Sonos control: search, queue, playlists, rooms/groups, volume, YouTube."
metadata:
  short-description: Sonos music and YouTube playback
---

# Sonos

Use for Sonos music, playback, queue, room/group, and YouTube workflows.

## Rules

- Prefer existing local Sonos tooling in the current repo before inventing shell/API calls.
- Do not change speaker groups, queues, or playback unless the user asks for it.
- Confirm target room/group when ambiguous.
- For YouTube, prefer a playable audio URL or local extraction workflow already present in the repo; avoid downloading unless requested.
- Keep network/debug work out of scope unless the user explicitly asks for diagnostics.
- Secrets, service tokens, and account auth: check env/profile first; use `op` only via the repo/AGENTS rules.

## Workflow

1. Discover repo commands:
   - `rg --files`
   - package scripts or CLI help
2. Identify target:
   - room/group
   - service/source
   - query, URL, playlist, album, artist, or track
3. Dry-read current state when useful:
   - rooms/groups
   - now playing
   - queue
4. Execute the requested playback action.
5. Verify by reading current state again.

## Common Tasks

- Search and play music by track, album, artist, playlist, or station.
- Add or replace the queue.
- Pause, resume, skip, seek, shuffle, repeat.
- Set volume or mute for a room/group.
- Move/group playback between rooms.
- Play YouTube audio/music through Sonos when supported by local tooling.

## YouTube Notes

- Treat YouTube URLs as media sources first, not as download requests.
- If conversion/extraction is needed, prefer the local toolchain already used by the repo.
- State constraints clearly when Sonos/service support blocks direct playback.
