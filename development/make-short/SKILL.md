---
name: make-short
description: Build a fully-synthetic vertical short (1080×1920, ~40s) end-to-end from a topic — script + beats.json, linked TSX beats over a persistent canvas, phone-scale QA, render, ElevenLabs voice with exact word-synced captions, SFX audition, optional music bed. Use when the user wants to "make a short", "create a shorts video", build a TSX short for a niche (chess, math, algorithms, dev tips, Excel…), add voice/captions to a short, or continue the short-N series in this repo. This is the 100%-TSX track — for video-model pixels use make-ai-short, for the paper-collage documentary look use make-vox. Defers raw TSX crash rules to vidtsx-2d-generator and SFX taste to suggest-sfx + brand §7.
---

# make-short — fully-TSX vertical shorts, end to end

Everything is code: no footage, no stock. One short = one Remotion composition fed by a
beats contract, with voice and SFX layered on after render. Proven across the 12 example
shorts in `shorts/`. The idea bank + niche ranking lives in **`IDEAS.md`** — read it when
picking a topic, and grow it when brainstorming.

Run everything from the **repo root**. Tools are stdlib-only Python 3.10+; `ffmpeg`/`node`
must be on PATH; API keys live in `.env` (see `.env.example`).

## Artifact contract

```
shorts/short-N-<niche>/
  script.md        — hook, beat sheet table (time | on screen | VO), production notes
  beats.json       — machine contract: format, vo[] (text+start/end+words), beats[], niche timeline
  voice/           — per-line TTS clips + voice.wav        (gen_voice.py)   [gitignored]
  sfx-plan.json    — cue sheet on the global timeline       (mix_sfx.py)
  output/          — short-N-sfx.mp4 (+ music auditions)                    [gitignored]
remotion/src/shots/short-N/
  ShortN<Name>.tsx — THE composition (registered by npm run gen)
  vo.gen.ts        — AUTO-GENERATED VO with exact word times (never hand-edit)
```

Shared kit: `remotion/src/lib/shorts.tsx` (Captions, Kicker, BigTitle, Stamp, PauseCard,
StatChip, ProgressBar, ShortsBackdrop, SAFE areas, prog helper). Niche libs so far: `lib/chess.tsx`,
`lib/math.tsx`, `lib/algo.tsx`, `lib/sheet.tsx`, `lib/piano.tsx`, `lib/prob.tsx`, `lib/map.tsx`,
`lib/orbit.tsx`, `lib/chart.tsx`, `lib/story.tsx`… **Add at most ONE new niche lib per short**,
generic enough for a series.

## Stage 1 — script + beats

Beat grammar (~38–42s): **HOOK** (0–3.4s, frame 0 FULLY composed — the payoff already visible,
no fade from black) → **SETUP** → optional **QUIZ** (PauseCard, ~2.5s — drives comments) →
**REVEAL** in 2–4 steps, each synced to a VO word → **TWIST** → **LOOP** (last frame == frame 0,
dissolving the payoff back into the intro so it replays seamlessly).

**Outros — no fluff.** NEVER end on an old-school engagement-CTA — no "what should I do next?",
no "comment below", no "which one should I break down". They read as dated. End on the PAYOFF
line, and let the visual LOOP blend back into the intro — the loop-into-intro *is* the ending.
Prefer a clean visual dissolve/reset that lands the last frame exactly on frame 0. If a seamless
loop genuinely isn't possible for a topic, just end on the payoff with no filler. Don't pad the
tail: trim the composition so it ends shortly after the payoff, not seconds of dead air.

VO rules: ~100 words total, estimate line windows at **~2.7 words/sec with slack to the next
line's start** (tighter forces audible atempo squeeze — 3.3wps needed a 1.3× squeeze; 2.7wps
peaked at 1.11×). Facts must be verified before scripting. Write `script.md` + `beats.json`
(vo lines with estimated start/end; niche timeline in global SECONDS).

## Stage 2 — the composition

- One `.tsx` under `remotion/src/shots/short-N/`, `compositionConfig` 1080×1920 @30, ~42s.
  Follow vidtsx-2d-generator's hard rules (frame-based only, monotonic ranges, Easing.bezier).
- Beats = `<Sequence>` scenes over ONE persistent canvas (the board/equation/array is the
  continuity — rewinds and evolutions happen in a single component's timeline, not cuts).
- `Captions lines={VO}` + `ProgressBar` mounted at the ROOT (global time), scenes beneath.
- **THE recurring bug: frames inside a `<Sequence>` are LOCAL.** Converting a global beat
  second to a scene cue is `local_f = global_s*fps − sequence_from`. Check every cue twice.
- Frame-0 rule: hook scene uses `warm` props (BigTitle/EqRow) and negative `at`s so highlights/
  stamps are already on at f0. Loop scene reverses the hook's punch-in (settle 1.06→1 vs grow
  1→1.06) so the video loops seamlessly.
- Safe areas: captions block centered ~y1500; nothing critical in bottom 340px / right 160px.

## Stage 3 — QA (do not skip, it catches real bugs every time)

```
cd remotion && npm run gen        # frames.mjs does NOT run gen-registry itself
node scripts/frames.mjs ShortNName 0,<beat-boundaries+hero-frames>,<last> --scale=0.5
```
READ every PNG (phone scale). Checklist: frame 0 composed & thumbnail-grade · every reveal
synced to its beat · nothing covering the payoff element · kickers swap with the narration ·
captions clear of UI zones · loop frame ≈ frame 0. Fix, re-render frames, only then:

```
node scripts/render-all.mjs ShortNName --scale=1     # -> remotion/out/ShortNName.mp4
```

## Stage 4 — voice (ElevenLabs, word-exact captions)

```
python tools/gen_voice.py --beats shorts/short-N-<niche>/beats.json \
    --voice TX3LPaxmHKxFdv7VOQHJ --emit-ts remotion/src/shots/short-N/vo.gen.ts
```
- Per-line TTS with `/with-timestamps` → REAL per-word times (tempo-scaled, global) written
  into beats.json AND `vo.gen.ts`. The shot imports `{ VO } from './vo.gen'` — captions then
  highlight on the exact spoken word. Never estimate when a voice track exists.
- Clips are cached by text-hash: rewriting one line only re-bills that line.
- Voice: the examples use ElevenLabs premade "Liam" (`TX3LPaxmHKxFdv7VOQHJ`); swap in any voice
  (including your own clone) with the `--voice` flag + regen.
- Then re-render the composition (captions retimed) and mux:
  `ffmpeg -i remotion/out/<Id>.mp4 -i shorts/.../voice/voice.wav -map 0:v -map 1:a -c:v copy
   -c:a aac -b:a 192k -t 42 remotion/out/<Id>-voiced.mp4`

## Stage 5 — SFX (the suggest-sfx machinery, shorts flavor)

Read `brand.md` §7 + `media/library/sfx/catalog.json`. Library-first; add generic recipes to
`palette.json` + `python tools/gen_sfx.py` only for genuine misses. Author
`shorts/short-N-<niche>/sfx-plan.json` (preview = the -voiced.mp4, out = output/short-N-sfx.mp4).

Shorts taste adaptations: **diegetic action sounds are the content** (piece thocks, digit
pops) and may exceed long-form density; decorative cues stay `optional: true`; layer the 2–3
hero moments (capture+stamp, carry flight+landing+chime). Cue times from EXACT landing frames:
`at_s = (move.at + move.dur + sequence_from) / fps`.

```
PYTHONIOENCODING=utf-8 python tools/mix_sfx.py shorts/short-N-<niche>/sfx-plan.json --print
PYTHONIOENCODING=utf-8 python tools/mix_sfx.py shorts/short-N-<niche>/sfx-plan.json
```
The mix is an AUDITION — the user's ear is the audit gate before anything is called final.
Update catalog `used_in` afterwards.

## Stage 6 — music (optional, per video)

Library beds in `media/library/music/` (gen_music.py to grow). Audition over the SFX mix:
`python tools/mix_music.py --all --base shorts/short-N-<niche>/output/short-N-sfx.mp4`
(or `--bed <id>`). Hard-ducked under voice.

## Done =

script.md + beats.json authored (facts verified) · composition QA'd frame-by-frame · rendered
at scale 1 · voice generated with word-exact captions and muxed · SFX plan authored + audition
mixed (~−15.5 LUFS, awaiting the user's ear) · library used_in updated · IDEAS.md queue updated.
