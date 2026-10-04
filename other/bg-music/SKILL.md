---
name: bg-music
description: Mix a trendy looped background track under a finished short, attenuated well below the speaker (~-18dB). Picks a random song from ./songs/<category>/, or recurses across every mood folder when category is "ALL SONGS" (the default). Avoids repeating the last 5 picks via ./songs/.recent. Runs after loudnorm so the bed never overpowers the broadcast-leveled speech. Pair with pick-mood to route by clip vibe instead of pure random.
allowed-tools: Bash
user-invocable: true
---

# bg-music

Background music makes a podcast clip feel like a TikTok, not a recording.
This skill picks a random mp3 from the local `./songs/` library, loops it to
match the clip's length, and mixes it under the speaker with a hard volume
attenuation. No ducking sidechain — the bed is just quiet enough to live
underneath broadcast-leveled speech.

## Invoke

```
.claude/skills/bg-music/bg-music.sh <input> <out> [category=ALL SONGS] [volume=0.17] [fade=0.6]
```

- `input` — finished, loudnorm'd mp4
- `out` — output mp4 with music mixed in
- `category` — subfolder of `./songs/` to pick from (e.g. `Energetic`, `Story`, `Inspiring`). Defaults to `ALL SONGS`, which recurses across every mood folder under `./songs/`.
- `volume` — linear gain for the bg track, default `0.17`. Lower for more speech-forward clips.
- `fade` — seconds of fade-in so the bed ramps up instead of blasting at `t=0` (it would otherwise be exposed under the speech-free title card). Default `0.6`.

## How

- Picks a random `.mp3`/`.MP3`/`.wav` from `$SHORTS_ROOT/songs/<category>/`.
- Loops it with `-stream_loop -1` so any track length covers the clip.
- `amix` with `duration=first` so output matches the video duration exactly.
- Bg volume hard-set; output limited with `alimiter=limit=0.97` to avoid clip.
- Video is stream-copied.

## Caveats

- Re-encodes audio only.
- Idempotent via `<out>.bgmeta` (input mtime + category + volume + fade + chosen track basename).
- The chosen track is logged to stderr so you can reproduce / blacklist.
