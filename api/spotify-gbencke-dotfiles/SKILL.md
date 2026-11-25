---
name: spotify
description: Query the Spotify Web API (search tracks/artists/albums, fetch artist, album, playlist, audio features, recommendations) using SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET env vars via client-credentials auth. Use when the user asks to search Spotify, look up an artist/album/track, fetch playlist contents, or invokes /spotify.
---

# Spotify Web API

Auth is handled by the helper using env vars `SPOTIFY_CLIENT_ID` and
`SPOTIFY_CLIENT_SECRET` (client-credentials flow — already verified working).
No OAuth redirect needed for public catalog data.

Run the helper next to this file:

```bash
python3 ~/.pi/agent/skills/spotify/spotify.py <command>
```

## Commands

| Command | Example |
|---|---|
| Search | `spotify.py search "bohemian rhapsody" track 10` |
| | `spotify.py search "radiohead" artist 3` |
| GET any endpoint | `spotify.py get /v1/artists/4Z8W4fKeB5YxbusRsdQVPb` |
| | `spotify.py get /v1/playlists/37i9dQZF1DXcBWIGoYBM5M` |
| | `spotify.py get /v1/albums/<id>/tracks limit=50` |
| POST | `spotify.py post /v1/playlists '{"name":"X","public":false}'` |

Useful endpoint paths (append IDs from search results):

- `/v1/artists/{id}`, `/v1/artists/{id}/top-tracks?market=US`, `/v1/artists/{id}/albums`
- `/v1/albums/{id}`, `/v1/albums/{id}/tracks`
- `/v1/tracks/{id}`, `/v1/audio-features/{id}`
- `/v1/playlists/{id}`, `/v1/playlists/{id}/tracks`
- `/v1/recommendations?seed_artists=...&seed_genres=...&limit=20`
- `/v1/browse/categories`, `/v1/browse/new-releases`

## Auth

`spotify_auth.py` was run once: a refresh token is stored at
`.spotify_token.json` (chmod 600, gitignored). `spotify.py` uses it
automatically (scopes: playlist-read-private, playlist-read-collaborative,
user-read-recently-played, user-top-read), so user endpoints like
`/v1/me/playlists`, `/v1/me/top/artists` and `/v1/me/player/recently-played`
work. Without the token file it
falls back to client-credentials (public catalog only). To re-authorize or
add scopes: edit `SCOPES` in `spotify_auth.py` and re-run it.

## Notes

- User endpoints available with current scopes: `/v1/me/playlists`, playlist contents, `/v1/me/top/artists`, `/v1/me/top/tracks`, `/v1/me/player/recently-played`.
- Note: `/v1/browse/new-releases` can return stale data; `tag:new` search only reaches ~2 weeks back. For a longer window, pull `/v1/artists/{id}/albums` for the user's top artists and filter by `release_date`.
- More scopes (saved tracks, playback, etc.) require re-running `spotify_auth.py`.
- Pipe through `jq` to trim noise: `... | jq '.tracks.items[] | {name, artists: [.artists[].name]}'`.
- Token is refreshed per invocation; fine for interactive use.
