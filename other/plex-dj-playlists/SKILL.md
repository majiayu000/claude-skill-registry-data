---
name: plex-dj-playlists
description: Export Plex music and movie libraries and create curated Plex playlists using server credentials loaded from .env. Uses TMP workspace outputs and never embeds tokens in skill files.
version: 1.1.0
author: local
license: MIT
metadata:
  hermes:
    tags: [Plex, Playlists, Music, Movies, Curation, API]
---

# plex-dj-playlists

Use this skill to export Plex libraries and create/replace playlists through the Plex API.

Path aliases (portable install)
- `HERMES_AGENT_ROOT` = repository root where this skill is installed
- `HERMES_ENV` = `HERMES_AGENT_ROOT/.env`
- `HERMES_TMP` = `HERMES_AGENT_ROOT/TMP/plex-dj-playlists`

Credential contract
- Credentials are loaded from `HERMES_ENV` (not hardcoded absolute paths).
- Required env vars:
  - `PLEX_BASE_URL`
  - `PLEX_SERVER_TOKEN`
  - `PLEX_MACHINE_ID`
- Do not hardcode or print tokens in output.

Output location
- All generated exports go to `HERMES_TMP`.

Music workflow

A) Static multi-playlist builder (artist list based)
1. Export tracks:
   - `python skills/media/plex-dj-playlists/scripts/plex_export_library.py`
2. Build predefined playlists from that export:
   - `python skills/media/plex-dj-playlists/scripts/plex_make_playlists.py --tracks TMP/plex-dj-playlists/<export-file>.json`
3. Existing playlists with matching names are deleted and recreated for deterministic results.

B) Dynamic style-cue playlist builder (preferred for Plexamp voice requests)
1. Create or replace one music playlist from free-form cues:
   - `python skills/media/plex-dj-playlists/scripts/plex_music_playlist.py --name "Chill Coding" --cues "chill coding focus instrumental lofi ambient"`
2. Useful options:
   - `--limit 45` (playlist length)
   - `--max-per-artist 3` (artist diversity)
   - `--section-id <id>` (override music library)
   - `--dry-run` (score/preview without writing playlist)

Movie workflow
- Create/refresh a curated movie playlist and export full movie library metadata:
  - `python skills/media/plex-dj-playlists/scripts/plex_movie_playlist.py`
- Script output includes:
  - detected movie section
  - total movie count
  - export path
  - playlist name
  - playlist item count
  - sample selected titles

Selection guidance
- If the user asks for music or Plexamp listening, use `plex_music_playlist.py`.
- If the user asks for fixed batch playlists by favorite artists, use `plex_make_playlists.py`.
- If the user asks for films/movie night lists, use `plex_movie_playlist.py`.

Notes
- Movie workflow currently uses the first Plex library section where `type=movie`.
- Music workflow auto-detects first section where `type=artist` unless `--section-id` is provided.
- Scoring profiles are intentionally editable to match user taste.
