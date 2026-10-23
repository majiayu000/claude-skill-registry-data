---
name: lyrion-api
description: >-
  Query the Lyrion Music Server over its JSON-RPC API from the Flask app. Use
  this whenever a task needs live data from Lyrion — the now-playing track,
  player list, transport state, album art, or any `slim.request` command — or
  when adding a feature that reads from the music server. Covers the request
  format, the tag system, the shared cache, and the self-signed-TLS rules, so
  new calls match how `services/lyrion.py` already talks to the server.
---

# Talking to Lyrion (JSON-RPC)

All server communication goes through `services/lyrion.py`. Add new server calls there and expose them as functions the routes import — routes never build JSON-RPC payloads themselves.

## Request shape

Lyrion speaks JSON-RPC over `POST {LYRION_HOST}/jsonrpc.js`. Every call goes through `lyrion_request(payload)`, which posts the payload, tolerates the empty non-JSON body Lyrion returns for unknown player ids, and returns `{}` instead of raising. Read results defensively: `data.get("result", {}).get(...)`.

The payload is always a `slim.request` with a player id (or `""` for server-wide commands) and a command array:

```python
payload = {
    "id": 1,
    "method": "slim.request",
    "params": [player_id, ["status", "-", 1, "tags:aAldcKy"]],
}
data = lyrion_request(payload)
```

- `params[0]` — player id (a MAC address), or `""` for server-wide queries like `players`.
- `params[1]` — the command and its arguments. `"-"` as the playlist index means "current track"; the trailing count (`1`) limits returned items.

**Examples already in the file** — read them before writing a new call:
- `get_players()` — `["", ["players", "0", "100"]]`, returns `players_loop`.
- `get_now_playing(player_id)` — `["status", "-", 1, "tags:aAldcKy"]`, returns the current track from `playlist_loop`.

## The tag system

`status` returns only the fields you ask for via a `tags:` string, one letter per field. The ones this app uses:

| tag | field | notes |
|-----|-------|-------|
| `a` | artist | |
| `A` | role-keyed artist lists | multiple artists joined by `", "` under a role key (`trackartist`, `artist`) |
| `l` | album | |
| `y` | year | `0` when unknown, normalized to `None` |
| `d` | duration | |
| `c` | coverid | absent for remote/streamed tracks |
| `K` | artwork_url | remote streams (Deezer/Spotify/radio); may be relative to the host |

Title and track id come back by default, and so do the player-level fields such as `mixer volume` (negated while the player is muted; `_volume` maps it to `volume`/`muted`). That track id is the key into the SQLite `tracks` table for lyrics (see `services/database.py`). When reading artists, prefer `trackartist` (full "feat." line) then fall back to `artist` then `albumartist`, matching `get_now_playing`.

Need a field the app doesn't fetch yet? Add its tag letter to the `tags:` string and map it in the returned dict — don't make a second call.

## Covers and same-origin proxying

Covers are proxied through this app rather than pointed straight at `LYRION_HOST`, so the page can read image pixels on a canvas to derive the accent tint (a cross-origin image would taint the canvas). `fetch_cover` gets local artwork by coverid (optionally an `NxN` thumbnail, falling back to full art on 404); `fetch_remote_cover` gets a stream's `artwork_url`. Both funnel through `_read_image`, which caps size at `COVER_MAX_BYTES` and aborts 502 on oversized or non-image payloads.

## Caching and shared state

`get_active_now_playing()` is the entry point routes should call for now-playing state. It caches the snapshot of all playing players for `NOW_PLAYING_TTL` (2s) behind `_now_lock`, so Lyrion sees one enumeration per TTL regardless of how many clients poll. It also ages the cached playback position by wall-clock time so the progress bar and karaoke highlight stay accurate across shared reads. If you add server calls that clients poll, follow this pattern rather than hitting Lyrion per request.

`_last_player` keeps the auto-selected player stable across polls; only mutate it under `_now_lock` (see `_auto_select`).

## TLS: verify=False only for the local host

The local Lyrion server is self-signed, so calls to `LYRION_HOST` pass `verify=False` — this is documented accepted risk "audit S1" (PR #15). Keep the inline comment referencing it whenever you add such a call, so bandit's `# nosec` justification trail stays intact. Calls to **public** CDN URLs (`fetch_remote_cover`) keep verification **on** — never blanket-disable it.

## Checklist for a new server call

1. Add the function to `services/lyrion.py`, building a `slim.request` payload.
2. Route it through `lyrion_request` and read `result` defensively.
3. Request exactly the tags you need; map them into a plain dict.
4. If clients will poll it, cache behind a lock with a short TTL.
5. Add a test that patches `lyrion_request` (see `tests/test_lyrion_request.py` and `tests/test_now_playing_cache.py`) — never hit a real server in tests.
