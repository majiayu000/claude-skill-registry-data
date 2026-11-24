---
name: design-sound
description: "Make, find, choose and mix SFX and music for a video, game or reel: search the sound library, fetch real sounds from the web, make sounds by code (learn a recording into a model with knobs, or write a designed gesture), fit music to the cut, mix to platform loudness and check every cue. ElevenLabs and picture foley only when named. Licences are warned, never blocking. Use automatically for sound design, SFX, foley, soundtrack, mixing."
license: MIT
---

# Design Sound

One library, two ears, two hands. `search.py` finds a sound from a description (CLAP text-to-audio plus tag keywords)
and draws a sheet so you can look before choosing. `make.py` makes sounds by code: it learns a recording into a model
and renders new takes with controls, and `designs.py` writes gestures no recording holds. `fetch_web.py` brings in
recordings to learn from; `generate_elevenlabs.py` and `video_foley.py` run only when the owner names them. `foley.py` builds the effects stem from an event
list, `fit_music.py` edits a real track to the cut, `score.py` sketches music (placeholder only), `mix.py` carves,
ducks, masters and checks, `listen.py` checks any WAV. The library is data: `SOUND_LIBRARY_DIR` (default
`Documents/sound-library` in the home folder; `index.json`, `embeddings.npz`, `sources.json`), indexed in place.
Read `local.md` next to this file when it exists: the owner, machine paths and project rules, which win.

## When to use

Any video, reel, episode, game or demo that needs a sound made, chosen, placed, or a mix built or checked; pipelines
that cut and place sounds (Remotion reels, `watch-video` remakes, 2D and 3D films) call these scripts. A trailer,
action film or re-score of an existing cut also reads `references/cinematic-trailer.md`.

## The loop

1. Read every frame and list each element on its first frame (`references/make.md`, "Every element has a sound"), then
   describe each in plain words ("a heavy wooden door shut hard"), plus its kind.
2. `search.py "<description>" --sheet sheet.png` (add `--kind oneshot|bed|music`, `--max-seconds`).
3. Open the sheet and look: a hit has a sharp rise and the energy where you expect; a swell, a hiss or a long tail
   where you wanted a snap means a wrong pick. Read the rows: attack ms, centroid, band shares, licence.
4. Make it by code (`references/make.md`): `make.py learn` a full-quality WAV (`fetch_bigsoundbank.py`; MP3 previews
   and meme files sound cheap and the learn gate refuses them) into a model, then `make.py render` takes with
   controls; every take is audited and reseeded. Hits: `hit.py` (transient, body, tail, sub from separate models,
   lifted for punch). Gestures: `designs.py`. Passes and distance: `physics.py`. ElevenLabs/foley only when named.
5. Design: few moments, each with room (`density.py cues.json` flags BUSY, CROWDED, PILED); a cue may be a `make`
   model, a `hit` or a `design` instead of a file (`references/foley.md` for layering and sizes). Music: a real track,
   `fit_music.py` to the cut (`references/music.md`), or a composition plan on the cuts when the owner asks for one.
6. `mix.py mix.json --out final.wav --sheet sheet.png` (`references/mix.md`, which holds the mixing practice and its
   sources): voice high-passed and de-essed, music ducked (auto-lowered to keep the voice 11 LU over it) and carved
   at 1-4 kHz, beds band-limited, mono bass, -14 LUFS, ceiling lowered until AAC and Opus decodes stay under -0.3 dBTP.
   It listens to each stem alone and reads sync, masking and phone audibility on the final.
7. Fix every flag and rerun the stage that made it: wrong sound, sync over one frame, MASKED, `QUIET UNDER MUSIC`
   (cue under +6 dB(A) over the ducked music), `WEAK ON PHONE`, voice under 10 LU over the music, short-term over
   integrated + 5 LU, mono loss over 3 dB, a `reused` recording. Look at the final sheet: every event shows a front.
8. Report licence warnings once, one line per file, and the CC BY credits. Say plainly that nobody has listened to the
   mix unless someone has: these checks are measurements. For a film, send the owner a fast preview first.

## Commands

`PY` = `uv run --no-project --python 3.12 --with numpy --with scipy --with librosa --with soundfile --with pyloudnorm
--with psutil --with torch --with transformers --with matplotlib python` (CPU torch is enough once indexed).
`NET` = `uv run --no-project --python 3.12 --with numpy --with psutil --with requests python`.
Scripts live in `scripts/` next to this file; run them with absolute paths and never from a source sound folder.

- `PY index.py [--add <folder>]...` index new or changed files; re-derives licence classes every run.
- `PY search.py "<description>" [--n 8] [--kind ...] [--licence any|public|cc0] [--max-seconds X] [--sheet out.png]`
- `NET fetch_web.py "<query>" --source openverse|archive|myinstants|youtube [--n 6] [--max-seconds 30] [--start S]`
- `PY make.py learn <recording> --name family/id [--from S --to S] | render <family/id> --out x.wav [--seed N] [--n N]
  [--size --pitch --length --bright --hard --ring --weight --energy --vary] | design <riser|subdrop|whoosh|blip|tick> | list`
- Only when named: `generate_elevenlabs.py` (`references/sources.md`), `video_foley.py` (`references/video-foley.md`).
- `PY listen.py <wav> [--expect "label@seconds"]...`; `eval.py` search benchmark; `reference_gap.py ours.wav ref.wav
  --hits t1,t2` band shares, peaks, jumps and pre-hit dips against a reference mix.
- `PY foley.py events.json --out foley.wav` effects stem; `fit_music.py <track> --duration S --out m.wav` music fit.
- `PY ui_kit.py build --style faithful|soft|crisp|warm|toy --out kit/ | check kit/` UI sounds + web player (foley.md).
- `PY mix.py mix.json --out final.wav [--sheet sheet.png] [--no-listen | --quick]` the mix and every check.
- `PY ab_test.py make mix.json --param hold|cue|unmask --out-dir DIR` blind A/B; `ab_test.py pick DIR <A|B|same>
  --note "<the owner's words>"` writes the pick into `house-defaults.json`.
- `PY memes.py build <folders> | detect words.json [--events e.json] --out cues.json` memes stay originals (pitch
  and speed only); detect finds the moment each fits and places it in a pause (`references/foley.md`, "Memes").

## House rules

- Sounds are made by code from learned recordings or designs, never by a generation model unless the owner names it:
  models sound good but come out different every call. Any licence is allowed:
  warn about `restricted`, `other` and `unknown` files, never drop them. Credit CC BY authors in the
  post or description (`sources.json`, field `credit`). A project's own sound rule wins.
- Every visible event gets its own sound at its own frame, placed from the event time, within one frame.
- No recording shared between two cues in a scene, and no one merged sound covering several actions; no filler
  sounds that no action makes. Only room tone and ambience run under everything. No reverb unless asked.
- Voice is mixed first, at least 10 LU over the music while it speaks; beds 15 LU under it, in their own band and 6 dB
  or more under the cues in their dominant band.
- Keep the top of the mix soft: cut shrill 2 to 6 kHz build-up. UI sounds: ask the owner's taste once (make.md, "UI").
- Water and other wet recordings sit about 10 dB under the music and only start when their shot does.
- Short impacts are CLAP's weak spot: always read the sheet for hits, slams and bursts instead of trusting rank 1.
- Values only ears can set (`house-defaults.json`: duck hold, cue margin, voice unmask) are the owner's call, never
  an agent's. Do not edit them or argue them from measurements. When the owner says the music pumps or an effect is
  buried or too loud, run `ab_test.py make` on that mix, send A and B with the printed question, keep the key hidden,
  and on the owner's letter run `pick` with their words. A new ear-only value goes in that file the same way.
- Generated sound costs credits or GPU time: library and web first, plans are free, never buy credits unasked.

## References

- `references/make.md` sounds by code: the learned model, controls, designs, checks, what the ear test found.
- `references/sources.md` web fetching, ElevenLabs commands and measured costs, prompt writing, the licence policy.
- `references/library.md` index fields, adding a folder, licence classes, search scoring and its limits.
- `references/foley.md` event format, layering rules, query words, size and distance maths, what the owner rejected.
- `references/music.md` the music library, mood search, `fit_music.py`, credits, the `score.json` sketch.
- `references/mix.md` mix.json, carving, ducking, phone bass, the whole-mix checks, mixing practice and Evidence.
- `references/video-foley.md` foley generated from a silent film: install, resources, when it hears nothing, licence.
- `references/cinematic-trailer.md` trailers and re-scores: heavy explosions, tails through cuts, punch,
  reference match, trailer music.
