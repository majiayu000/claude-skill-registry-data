---
name: game-trailer
description:
  "Produce promo trailers from real gameplay of a Godot 4 game: a beat-synced 16:9 1080p60 trailer, a native 9:16
  vertical cut, a looping GIF and posters, rendered with Movie Maker from bot playthroughs in the game's own fonts and
  art, cut on the bar grid of a procedural cue, and reproducible from a marketing/ directory the game never depends on.
  Use for any trailer, teaser, gameplay or promo video, marketing or social media video, devlog clip or gameplay GIF of
  a Godot game, in GameGen projects or standalone."
---

# Gameplay trailers from real gameplay

The game's own bots play it under Godot's Movie Maker, a director script outside the project picks each shot's in-point
and draws captions and cards, and ffmpeg cuts the shots onto the bar grid of a trailer cue composed for the edit. Every
output is rebuilt from code in `marketing/`: re-editing means changing `timeline.json` and re-rendering the changed
shots. Nothing is faked: no keyframed players, no screen recordings, no stock music.

Deliverables: `<name>_trailer_16x9.mp4` (1920x1080, 60 fps, H.264 High yuv420p CRF 17, AAC 192k, -14 LUFS, faststart),
`<name>_trailer_9x16.mp4` (native 1080x1920 render), `<name>_loop.gif` (about 6 s, under 15 MB), and posters.

## Requirements

Godot 4.2 or later (the templates were verified end to end on 4.7), `ffmpeg` and `ffprobe`, `uv` (scripts declare their
Python deps inline: pillow, numpy, scipy, soundfile, matplotlib), and a game that can be played by a bot (see
[the adapter contract](references/game-adapter.md#what-the-game-must-provide)). Movie Maker opens a game window per
render; it needs a desktop session, not a headless one.

## GameGen projects and standalone use

In a GameGen project, read [shared context](../../references/shared-context.md), the ready preferences and
[repository contracts](../../references/repository.md):

- Take title, description, genre and target platforms from preferences; ask for what they do not hold (studio, handle,
  destination, status line, length) with the question tool, once.
- `GAME` in `render.py` is `paths.game`; the cue imports the toolkit from `<paths.tools>/audio`; copy final deliverables
  and review sheets to `<paths.artifacts>/trailer/` when they are accepted.
- Bots and playthroughs belong to [game-qa](../game-qa/SKILL.md) and [godot-gameplay](../godot-gameplay/SKILL.md); the
  cue is composed with [game-audio-procedural](../game-audio-procedural/SKILL.md) under the audio conventions of
  [game-audio-vfx](../game-audio-vfx/SKILL.md), including its flash and reduced-motion limits.
- Record the trailer as one scoped task in the existing tracker, with the review evidence.

For a Godot game outside GameGen, do not start `game-bootstrap` or create preferences: resolve paths, brand and
destination from the repository and the request. Without a vendored audio toolkit, vendor game-audio-procedural's
`scripts/` to `tools/audio` first, or use a licensed or user-supplied cue whose bars you map by hand into the same
bar-map JSON.

The game never depends on `marketing/`: no autoload, scene or script in the project references it, and exports stay
unchanged. Gitignore `marketing/out/` and `<game>/override.cfg`.

## Workflow

### 1. Concept and beat sheet

Copy [assets/marketing/](assets/marketing/) into the repository root as `marketing/` and fill `trailer/concept.md` from
its template. Decide destination and length first (30-45 s for X and Bluesky), then the beat sheet in bars: a gameplay
hook in the first 2 seconds, readable muted (short captions in the game's fonts), the core verbs, a tour, a climax with
a hit-stop, and an end card with title, tagline, studio, "in development" and handle. See
[concept-and-music.md](references/concept-and-music.md) for platform targets and a proven structure. Get the user's
approval of the beat sheet before composing or rendering: it is the cheapest place to change the trailer.

### 2. Trailer cue and bar map

Pick a BPM where one bar is a whole number of 60 fps frames (`14400 / BPM`: 150 gives 96, 120 gives 120, 100 gives 144,
75 gives 192; see the table in [concept-and-music.md](references/concept-and-music.md#choosing-the-bpm)). Set `bpm` and
`bars` in `timeline.json`; `trailer_cue.py` reads them. Replace the cue skeleton's `compose()` with an arrangement built
with game-audio-procedural that follows the beat sheet bar for bar, uses the game's sonic identity and main hook, and
lists every edit hit in `HITS`. Render and verify:

```bash
uv run marketing/audio/trailer_cue.py     # out/audio/trailer.wav + trailer.json (bar map)
uv run marketing/audio/trailer_check.py   # hits within 10 ms, -16 LUFS, peaks, gap, tail, review PNG
```

Ask the user to listen; the checks are objective, the music is their call.

### 3. Adapter and scouting

Bind `godot/shot_director.gd` to the game through its `ADAPTER` section: bot scene, player lookup, progress value, state
columns worth mining, target hp, HUD/card nodes to hide, camera overrides, input assists. Set `GAME`, `NAME`,
`SCOUT_RUNS` and `bot_args()` in `render.py`. [game-adapter.md](references/game-adapter.md) has the contract and the
hook table.

```bash
uv run marketing/render.py scout          # every level/boss at 960x540: CSV, events, labelled contact sheets
uv run marketing/render.py highlights     # segments, peaks, hp drops and events with frames and progress
```

Look at the contact sheets: they show what the bot actually does, the only footage available. Mine loops, top speed,
grinds, combos and boss hp drops, and note candidates in the concept's shot table.

### 4. Edit decision list

Write `trailer/timeline.json` ([schema](references/timeline-schema.md)): shots tiling the bar grid exactly (fractional
bars allowed when they land on whole frames), each with a `start` for the bot, an in-point trigger (`x` crossing,
`frame`, n-th `hit`, n-th `event`, plus `delay`), optional `lead` frames, and `fx` in beats (caption, label card, flash,
fades, slow motion). Cards (`studio`, `logo`) need no gameplay. Point the overlay's BRAND constants at the game's own
fonts, palette, logo, key art and studio mark.

### 5. Render shots

```bash
uv run marketing/render.py shots [ids...]            # 16:9, three Movie Maker runs in parallel
uv run marketing/render.py probe <shot>              # once: director frame == movie frame (needs fade_in at 0)
uv run marketing/render.py shots --portrait          # after the 16:9 phase, never at the same time
```

Fix failures at the source: an in-point that never triggers, a bot that is too slow (pre-roll), a frame that blinks or
shows HUD. Read [gotchas.md](references/gotchas.md) before the first render and whenever a render looks wrong.

### 6. Assemble and deliver

```bash
uv run marketing/render.py assemble [--portrait]     # trim by in_frame, concat, cue + ducked SFX, loudnorm, encode
uv run marketing/render.py gif                       # palettegen/paletteuse, cross-faded seam, < 15 MB
uv run marketing/render.py poster
uv run marketing/render.py all                       # everything above, both formats, plus review
```

Details and encoder settings: [assembly-and-review.md](references/assembly-and-review.md).

### 7. Review

```bash
uv run marketing/render.py review [--portrait]       # format, half-bar contact sheet, cut-to-beat, loudness
```

Inspect the half-bar sheets yourself (HUD leaks, blinking, cropped text in 9:16, washed-out frames, wrong order), fix,
and re-render only changed shots. Then send the user the sheets, the report and the output paths: the final watch, with
sound on and off, is theirs. Do not call the trailer good on numbers alone.

## Conventions

- Bars are 1-based for humans (concept, timeline, bar map); fx timing is in beats from the in-point.
- Overlays are pure functions of the shot frame: deterministic renders, slow motion never slows graphics.
- Respect the game's flash-safety limits in overlays (template: peak 0.35, soft fades).
- Real gameplay only: engine time scale for slow motion is the only manipulation; gameplay changes needed for a shot are
  game tasks, not trailer code.
- Keep shot renders and intermediates in `marketing/out/` (gitignored); commit the code, concept and timeline.
- Report what was rendered and checked, the output paths, and what remains for the user to judge.
