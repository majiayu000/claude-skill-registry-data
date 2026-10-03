---
name: spotify
description: MUST USE whenever the user asks to play, pause, skip, queue, or control music on Spotify. You CAN control playback via the Web API adapter — never answer from knowledge and never say you cannot play music.
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    requires:
      env: ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"]
---

# Spotify

HARD RULES: You CAN play music — the adapter below is a working playback remote.
NEVER say "I can't play music" or answer from knowledge. ALWAYS call the adapter.
There is NO `openclaw spotify` command and NO spotifyd/spotify_player/spogo binary — never try those; the adapter via exec is the ONLY playback path (a third-party plugin was removed).
NEVER use web_search/web_fetch for playback requests — search the Spotify catalog with the adapter's `search`, not the web.
For "play Radiohead", "queue X", "pause", "next", "volume 50%":

1. **Check first** — Always run `status` before acting. Note `is_playing`, current item, and active device. Known devices: `jarvis-server` (homelab speakers — prefer when asked "on the server/homelab"), user's MacBook/phone by name.
2. **Don't hijack** — If something is already playing and the user did NOT say "now", "interrupt", or "switch": `search` the request, then `queue --uri` it (adds to up-next, current music keeps playing) and say it's queued. Only `play` (replace) when idle or explicitly asked to switch.
3. **Resolve** — If track/artist ambiguous, `web_search` for disambiguation, then `exec`: `python3 /app/voice/spotify_adapter.py search --query "<query>"`. Use the real URI from search results — never invent one.
4. **Control** — Call adapter:
   - `python3 /app/voice/spotify_adapter.py devices` (list; `*` = active)
   - If `play` fails with NO_ACTIVE_DEVICE: `python3 /app/voice/spotify_adapter.py transfer --device "<name>"`, then retry play.
   - `python3 /app/voice/spotify_adapter.py play --query "<query>" [--device <name>]`
   - `python3 /app/voice/spotify_adapter.py queue --uri <spotify:track:...>`
   - `python3 /app/voice/spotify_adapter.py pause|next|prev|volume --value 50`
   - `python3 /app/voice/spotify_adapter.py status`
3. **Auth** — Adapter handles OAuth token refresh from `/home/node/.openclaw/spotify.json` (refresh token). If not authenticated, instruct user to run `python3 /app/voice/spotify_adapter.py auth` and follow URL.
4. **Verify (mandatory)** — After `play`, run `status` and check real state. Only say "playing X" if the player reports `is_playing:true` on that track. If NO_ACTIVE_DEVICE: `transfer --device "<name>"`, retry play, re-check status. If `play` returns ok but `status` still shows `is_playing:false` / `item:null` after one retry: stop, report honestly that the app accepted the command but isn't rendering audio — the desktop app is asleep and needs one manual play press in the Spotify app, then API control works.
5. **Confirm** — Report what started playing, device, and queue state. Do not build a music service; adapter is tiny wrapper over Web API.
