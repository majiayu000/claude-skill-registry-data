---
name: spatial-film
description: Spatial Film - the film engine behind talking-explainer. Make a 45-90 s unnarrated spatial 3D product motion graphic (one CSS-3D camera, push-throughs, no hard cuts, last frame loops into the first) with real product UI, platform-faithful third-party canvases (GHL, n8n, Zapier), a native-tempo music bed and SFX, rendered at 1080p60 via HyperFrames. Built by 5 parallel scene workers against one contract (frame.md + seam table + per-scene harness). Use when the user says "spatial film" or "3D motion graphic", hands over a MOTION-PROMPT.md, or asks for a 6+ scene / 3D-camera product video with NO voiceover. A narrated explainer (the user's voice and/or a mascot presenting) is explainer-kit, which runs on this skill's machinery.
---

# Spatial Film

Proven end to end on a 60s product film (7 scenes, 5 workers in one wave, every seam frame-exact, check clean,
1080p60 in 4m19s). The template's `film.json` holds that film's real scene bars and cue sheet as the worked example.

`<skill>` = this skill's folder (the directory this SKILL.md is in). Run every script from the film project root.
`python` below = the Python command saved by explainer-kit's setup-check in `~/.talking-explainer/config.json`
(`py -3.12` on Windows, `python3` on macOS).

## What you need

- Node 20+, `ffmpeg` + `ffprobe` on PATH, Python 3.10+ with `numpy` and `Pillow`.
- The HyperFrames skills: `npx hyperframes skills update general-video hyperframes-animation media-use` (packet
  builder, blueprints + animation map, music helper). The CLI itself is pinned per project and runs through `npx`.
- Playwright for pre-rendering surfaces: `npm i -D playwright` in the film folder (or set `PLAYWRIGHT_PATH`).
- Optional, for sourced music: a HeyGen account - run `npx hyperframes auth login` once in your own terminal.
  Without it, bring your own track and start phase 4 at `music-analyze.py`.
- A GPU-capable machine for the final render (it still renders on the software path, about 15x slower).

## How to use this skill without wasting context

- Load ONE phase reference at a time, when its phase starts. Never preload them all.
- Scripts are the proven code. Run them; never regenerate their logic inline.
- The main session never reads a whole scene file (20-60KB). Judge scenes by contact sheets; fix with `grep -n`
  plus an exact patch.
- Workers get file PATHS, not pasted content. `storyboard.html` (60KB+) is grepped by cell id, never read whole.
- Read a contact sheet first; open single snapshot PNGs only to check a detail.

## Phases (each ends on a gate - do not move on until it passes)

| # | Phase | Load | Gate |
|---|---|---|---|
| 0 | Scaffold: `node <skill>/scripts/new-film.mjs <dir> --name <slug>` | - | folder has film.json, frame.md, kit, template docs |
| 1 | Intake, BRIEF, STORYBOARD, sketch sheet | `references/storyboard.md` | user's explicit "go" recorded under `## Locked` |
| 2 | frame.md, kit, pre-rendered surfaces | `references/surfaces.md` (+ `platform-canvases.md` only if GHL/n8n/Zapier appear) | no `{{` in frame.md; every capture PNG looked at |
| 3 | Harness smoke test, packets, parallel workers | `references/workers.md` | every scene: lint 0 errors, contact sheet matches its block |
| 4 | Music + SFX (run while workers build) | `references/audio.md` | bed at native BPM, bar 0 on a downbeat; cues in film.json |
| 5 | Assemble, check, seams, render, ship | `references/verify-ship.md` | check passes, seam-check all PASS, hardware-gpu render verified |

Route through `/hyperframes` -> `/general-video` for the intent and sketch-review steps (this skill supplies
the project shape, contract, scripts and gates; general-video supplies the packet builder and worker role).

## Files

| Path | What |
|---|---|
| `template/` | Project skeleton: `film.json` (scene bars, BPM, bgm, SFX, cues - the ONE source of timing), `frame.md` (design-truth contract with fill-ins), `BRIEF.md`, `STORYBOARD.md`, `assets/kit.css` (base film kit), `assets/fonts/` (Poppins 500/700 + OFL), `references/worker-brief.md`, `references/scene-starter.html` (lint-clean scene skeleton), `references/snippets.html`, `package.json` (pinned hyperframes 0.8.117). |
| `surfaces/` | Ready HTML rebuilds of the GHL, n8n and Zapier canvases + a long marketing page (fictional Northwind Dental data), `platform.css`, `sprite.svg`, `jobs.json`. |
| `scripts/new-film.mjs` | Scaffold a project from the template. |
| `scripts/capture-surfaces.cjs` | Render `src/captures/*.html` -> `assets/captures/*.png` at 2x (jobs.json). |
| `scripts/measure-surface.cjs` | 1x boxes of elements on a surface, for exact annotation/crop targets. |
| `scripts/make-harness.py`, `scripts/test-scene.mjs` | Per-scene isolated test projects; lint + snapshot one scene. |
| `scripts/music-search.mjs`, `sfx-search.mjs` | HeyGen catalog via media-use's REST helper (Windows-safe). |
| `scripts/music-analyze.py`, `music-bars.py` | numpy-only tempo + per-bar energy (no librosa needed). |
| `scripts/bgm-cut.py` | Cut the bed on bar lines, splice the track's own outro, fades; `--b` repeats to loop a bed under a longer film. |
| `scripts/assemble.py` | `film.json` -> `index.html` (scene slots on the bar grid, bgm, SFX with durations + lanes). |
| `scripts/seam-check.py` | Pixel-proves every seam (before / at / after the cut) and the loop (frame 0 vs last). |
| `scripts/render-final.mjs` | CLI render with `--browser-gpu`, logged to a file, gpu mode + ffprobe verified, then `flash-scan.py`. |
| `scripts/flash-scan.py` | Every frame of a render: a frame unlike both neighbours (an element shown for 1/60s) = a bug. |
| `scripts/encode-web.mjs` | Web encode (H.264 CRF 21, faststart, AAC or `--silent`) + poster frame. |
| `scripts/blink-fit.py`, `scripts/build-presenter.py` | Narrated films: blink overlays for sheet poses (`--band` = eye band); the presenter overlay from its track, with lip sync when the mascot has `mouth-fit.json`. |
| `scripts/el-tts.py`, `el-words.py`, `el-music.py` | Narrated films via ElevenLabs (key in env `EL`, never on disk): voice candidates from SCRIPT.md, Scribe word timings, a generated bed. |
| `scripts/seam-diff.py` | Seam diff with the presenter box masked (narrated films). |
| `scripts/fromto-scan.py` | Pre-render: flags `fromTo` FROM-only props that render workers (mid-scene seeks) never apply. 0 hits before every render. |
| `scripts/patch_exact.py` | Exact, CRLF-safe find/replace for scripted scene fixes (asserts one match each). |
| `scripts/selftest.mjs` | End-to-end proof the skill works on this machine. Must print PASS. |

## Narrated films (a voiceover + an on-screen presenter)

Proven on a narrated "API vs Webhook" explainer (83s, vertical and landscape, cloned voice, mascot presenter,
10 scenes by 5 workers). The music-film rules above still hold except where these replace them:

- **Voice candidates first.** `EL=<key> python <skill>/scripts/el-tts.py . eric=<voice_id> michelle=<voice_id>`
  reads the indented lines of `SCRIPT.md` and writes one MP3 per voice to `src/audio/voice-candidates/` (key from
  env only, never on disk). Let the user pick by ear, then transcribe only the pick.
- **Narration is the clock.** Word times: `EL=<key> python <skill>/scripts/el-words.py <voice.mp3>
  src/timing/voice-words.json` (ElevenLabs Scribe - no local model, needs a key), or
  faster-whisper with `word_timestamps` (language set, VAD on; explainer-kit's `transcribe.py`, free and local). Keep the word JSON in `src/timing/`. In `film.json` set `"bpm": 60, "beats_per_bar": 1` so a "bar" is 1s and scene
  lengths are plain seconds cut in the sentence pauses. Storyboard blocks give scene-local word times; arrivals
  start ~0.1s early and land on the word. Give a title at least ~1s on screen before the next cut (check the cut
  against the LAST word of the line it shows).
- **`film.json` extras** (assemble.py + make-harness.py read them): `"audio": [{id, src, dur, volume}]` for the
  voice, `"overlays": [{id, track, z}]` for a full-film layer (the presenter) that sits above every scene, so it
  never pops at a seam and the scenes stay presenter-free.
- **Presenter from pose PNGs:** one transparent PNG per pose (explainer-kit's `prep-mascot.py` trims,
  scales and writes the manifest), then `scripts/blink-fit.py <mascot_dir>` (optional, needs torch; fits the BLINK eye band onto each pose by NCC; poses under 0.70 get
  no blink) and `scripts/build-presenter.py` (writes the overlay from `src/presenter-track.json`: poses on cue
  words, head-anchored so swaps never jump, voice-envelope bob, breath, blinks, fx). Never hand-edit its output.
- **Audio:** loudnorm the voice to -16 LUFS / -1.5 dBTP (a plain gain clipped at +4.6 dBTP), sidechain-duck the
  bed under it offline (~17 dB below the voice), SFX quiet (0.1-0.45). Pad the voice key or the duck truncates
  the bed to the voice length (check warned "bgm 110.25s vs slot 113s"):
  `[1:a]apad=whole_dur=<TOTAL>[k];[0:a][k]sidechaincompress=threshold=0.03:ratio=6:attack=25:release=450,atrim=end=<TOTAL>`.
  No catalog bed (HeyGen search 500s or no login): `EL=<key> python <skill>/scripts/el-music.py .media/candidates/bed.mp3
  <ms> "<prompt: instrumental, BPM, sits under a narrator, no drops, ends on a resolved chord>"` - a track that
  winds down on its own at the film's length needs no splice.
- **Seam check noise:** the presenter moves across every seam, so `seam-check.py` FAILs on it alone. Judge each
  flagged pair with `scripts/seam-diff.py a.png b.png out.png x0,y0,x1,y1` (masks the presenter box) - 0.00%
  outside it is a pass.
- **Vertical (1080x1920) size law:** every scene's top band carries a real headline (60-84px), body text >= 40px,
  objects use the full width and the height above the presenter. The first wave shipped ~33px text in the top
  45% of the frame - put these numbers in frame.md before dispatch, not after.
- **Not a loop:** a narrated film ends on a held lockup; ignore the loop line of seam-check.

## Hard rules (the ones that make it premium and smooth)

1. **Truth from source.** Product UI is ported from the product's own HTML/CSS; third-party canvases are rebuilt
   from the user's real captures, never memory. Fictional data only. Only features the product really has.
2. **One camera.** Perspective 1866px (35mm) in every scene; a drift layer under the cam layer so nothing is ever
   still; parallax + DOF blur on far leaves. No opacity/filter/overflow/clip-path on a 3D parent (it flattens).
3. **Crisp at 1080p+.** Scale UI with CSS `zoom` (`.kit-zoom`), never `transform: scale(>1)`; author each piece at
   its closest on-screen size; captures are 2x PNGs shown at or below native.
4. **60fps smoothness law.** Transform/opacity only; springs for landings, expo/power3 for arrivals, inOut for
   camera legs; no linear, steps, snap or rounding; camera legs overlap 0.15-0.3s and last 0.6s+.
5. **Deterministic.** One paused timeline per scene registered last on `window.__timelines[id]`, `fromTo` with
   explicit starts, no random/clock/CSS transitions.
6. **Seams are shared frames.** Each seam is one exact picture both neighbours hold ~0.1s, locked by a 2D plate
   outside the rig. No hard cut, no empty frame, no fade-to-nothing. Last frame = first frame.
7. **On the grid.** Scenes are whole/half bars; clicks, ticks, stamps and swaps land on beats; music at its native
   tempo cut on bar lines.
8. **Contract fixes, not scene fixes.** Root-relative `assets/...` paths, ids never starting with a digit, ids and
   classes prefixed with the scene id. A rule every scene would break is fixed once in frame.md / worker-brief.
9. **Bans.** No emoji, neon glow, purple-to-blue gradient, colored left-border cards, circular spinners (shimmer),
   stock people, "John Doe", slideshow pacing or motion that says nothing.
10. **Finals from the CLI with the hardware GPU.** Never Studio's Export (software path, ~15x slower).

## When things go wrong

| Symptom | Cause | Fix |
|---|---|---|
| Lint: asset path error | `../assets/` in a sub-composition | root-relative `assets/...` (fix in the contract) |
| Lint: invalid composition id | id starts with a digit | `s01-click`, never `01-click` (film.py refuses it) |
| Packet builder throws / packet > 48KB | two blueprint ids, or too many `rules:` | one `id (Adapt)`; 2-3 rules per block |
| UI looks soft | transform-scaled or pushed toward camera past authored size | `.kit-zoom`, author at closest size |
| 3D suddenly flat | opacity/filter/overflow on a 3D ancestor | move it to the leaf |
| Seam pops | one side not holding the shared frame | `seam-check.py`, fix the drifting side's plate/pose |
| Seam FAILs a few % but the frames look identical | a rig copy under the plate doubles its shadow | only the plate shows while it holds (frame.md seams) |
| Product UI drifts from the real app | rebuilt from memory or partial CSS | capture the real app at 2x (`surfaces.md` first section) |
| 800+ `duplicate_audio_track` warnings | SFX without `data-duration` | re-run `assemble.py` |
| `music-search` says no credential | not logged in | user runs `npx hyperframes auth login` in their terminal |
| Render crawls ~1 frame/s | software GPU (Studio export) | `render-final.mjs` (CLI, `--browser-gpu --workers 6`) |
| Render keeps running after stop | stopping the shell does not stop node | kill the process tree (verify-ship.md) |
| No render progress visible | output piped through `| tail` | log to a file (render-final.mjs does) |

## Self-test

```bash
node <skill>/scripts/selftest.mjs
```

Scaffolds a 2-scene film in a temp folder, then runs the harness, assemble, `check`, seam-check, a hardware-GPU
render (1920x1080 at 60 fps) and the web encode. It must print `PASS` - run it on a new machine and after any edit.
