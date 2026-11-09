---
name: shenghua
description: "Turn a voice note, a talking-head or green-screen video, or a written topic into a fully animated, brand-styled video — local word-level transcription, a timed shot list, kinetic typography, camera moves, licensed photos and clips of the people and products it mentions, synthesized sound design and a voice-ducked music bed, rendered as a 1080x1920 Short (or 1920x1080, 1080x1080, 1080x1350), with long-form YouTube videos built chapter by chapter. A to-camera take keeps the opening line and sign-off on camera; a green-screen talk keeps the keyed presenter on screen throughout; a bare topic gets an explainer script voiced with one offline voice per cartoon character, acted out by animated hosts. Use when asked to make a video from audio or a voice note, animate a narration, edit a to-camera or green-screen talk, make a Short or reel, explain a topic with cartoon characters, or build a YouTube video from chapters."
license: MIT
compatibility: "Requires bash, Python 3.10+, Node 18+ and ffmpeg on macOS or Linux (WSL on Windows). First run downloads Chromium, GSAP and fonts; transcription, rendering and encoding then run fully local and offline."
---

# Shenghua 声画

Takes an audio file and builds a complete edit around it: every shot is an HTML/GSAP scene timed to the exact spoken word, rendered frame by frame in headless Chromium, then muxed with a mixed soundtrack (voice + synthesized SFX + ducked music). The judgement — what each line should *look* like — is yours. The scripts handle transcription, rendering, audio, and encoding.

Four ways in, one workflow:

- **Audio** (voice note, narration): the whole video is animated.
- **A to-camera video** (`bookends`, the default for a video): the opening line and sign-off stay on camera as face shots; the rest is animated. Mode detail: `references/face-bookends.md`.
- **A green-screen video** (`presenter`): the keyed speaker stays on screen throughout, moving between layouts while graphics build beside them. Mode detail: `references/presenter.md`.
- **A topic or script** (script mode): you write the script, Step 1b voices it with one offline voice per character, and original cartoon hosts act it out. Mode detail: `references/explainers.md`. Everything after Step 1b runs on the generated `<work>/voice.wav` as if it were a recording.

Any of these can be **long form** (`length: long`): a YouTube video over about five minutes, recorded and built chapter by chapter, each chapter its own project, joined at the end by Step 10b. **Load `references/long-form.md` before Step 2**: the project layout, pacing, captions and assembly all change.

`SKILL_DIR` = the directory containing this SKILL.md. **Always load `SKILL_DIR/references/scene-blocks.md` before writing the shot list** (block catalogue, pacing rules, safe zones, sound-cue vocabulary). Load each mode's reference at the step that needs it.

---

## Step 0 — Gather inputs

| Field | Required | Example |
|-------|----------|---------|
| `audio`, `video` or `topic` | Yes | `~/Downloads/voice-note.m4a` · a to-camera `~/Movies/take-1.mp4` · `"explain Kafka consumer groups"` (script mode) |
| `script` | No | the script, plain or with `[FACE]` / `[VOICE]` sections (each starts on its own line); the spelling reference for captions. In script mode, `Name: line` lines, and it *is* the input |
| `cast` | No | script mode: who's in it and which voice, e.g. `teacher Mama Log, sidekick Pip (squeaky)` |
| `length` | No | `short` (default) · `long`: a YouTube video in chapters, usually `landscape` (`references/long-form.md`) |
| `format` | No | `vertical` 1080x1920 (default) · `landscape` 1920x1080 · `square` 1080x1080 · `portrait` 1080x1350 |
| `style` | No | for a `video`: `bookends` (default: face shots open and close) · `presenter` (green screen) |
| `position` | No | presenter mode: where the speaker stands — `auto` (default: you vary layouts under the pacing rules) · `bottom-right` · `bottom-left` · `left` · `right` · `full` |
| `kit` | No | brand kit folder **or kit name** for this video, e.g. `acme` or `~/clients/acme-kit` |
| `template` | No | visual theme id from `templates/templates.json` (default `kinetic`) |
| `music` | No | `synth` (default) · path to a royalty-free track · `none` |
| `model` | No | transcription model: `small` (default) · `base` for clean audio, ~2x faster · any faster-whisper name or local folder |
| `vocab` | No | names and terms the speaker uses: `"Kubernetes, Kafka, Jane Doe"` |
| `slug` | No | inferred from the topic, e.g. `java-origin` |

**Brand kit.** Resolved as: `kit` if given, then `./brand.json`, then the configured default, then `~/.config/shenghua/brand.json`, then the bundled `SKILL_DIR/brand.example.json`. **When the user has more than one kit (`brand_kit.py list` shows several) and the request names none, list them and ask which to use before anything renders.** Naming one — "in the Acme kit" — skips the question. To create, convert or manage kits, **load `references/brand-kits.md`**. A version-1 brand file converts once with `init_kit.py --from <file>`.

Output goes to `<kit output.dir>/<slug>/` (default `~/shenghuas`); work files go to `<output dir>/<slug>/work/`. Create it now:

```bash
mkdir -p <output dir>/<slug>/work
work="<output dir>/<slug>/work"
```

Pick the defaults and proceed. Don't interrogate — the kit question above is the one exception. In script mode there is no file to check; go to Step 1b after setup. If the audio or video path is missing or not a file, say so and stop. With a `video`, pass it wherever a step takes `<audio>`; ffmpeg reads the voice from its audio track.

## Step 1 — Setup (first run, and whenever the kit changes)

```bash
bash SKILL_DIR/scripts/setup.sh [--voices] [--vision] [<kit>]
```

Checks `ffmpeg`, `node`, `faster_whisper` and `numpy`; installs `playwright-core` and its Chromium build; downloads GSAP and the themes' fonts into `SKILL_DIR/assets/` and the kit's fonts and logos into `SKILL_DIR/assets/kits/<id>/` (the kit argument is a path or a kit name), so several clients' kits live side by side. Prints `ready` or names the missing piece; re-running is a no-op for an unchanged kit. `--voices` fetches the script-mode voice models (~500 MB, online once); `--vision` installs the optional face detector (keying frames an off-centre speaker, sourced photos keep the face in frame) — everything works without it.

## Step 1a — Approve the look (first run, and every new kit)

Render the brand board, show it, and wait for a yes; `brand_kit.py check <kit>` prints the contrast report. Commands and what to look for: `references/brand-kits.md` → *The brand board*. Pick the theme in Step 4 first if the user hasn't — the board renders one theme.

## Step 1b — Script mode: write and voice the script

Only when there is no recording. **Load `SKILL_DIR/references/explainers.md` first** — the explainer shape, the analogy, the cast roles, the script format.

1. Write the analogy mapping, then the script as `Name: line` lines, to `<work>/script.txt`. Show both to the user and wait for a yes; the script is the cheapest thing to change.
2. Voice it (first run: `setup.sh --voices`):

```bash
python3 SKILL_DIR/scripts/speak.py "$work"/script.txt "$work" [--cast "$work"/cast.json]
```

Writes `voice.wav`, `speech.json`/`speech.js` (who speaks when; the hosts read it), and `words.json` + `transcript.txt`, each line's words timed by recognition. A line recognition can't read keeps estimated times; the result line names it (`… 14/15 lines aligned (1 estimated: pip line 7)`) — tell the user. `--no-align` estimates every line, for a fast draft only. Model, device and compute type follow the same flags and `config.json` as `transcribe.py` (Step 2). Tell the user which voice each character got and ask them to listen to `voice.wav`; you cannot. From here, `<audio>` in every later step is `"$work"/voice.wav`. Skip Step 2: `words.json` is already timed and spelled as the script. In Step 3, `script.txt` is the reference and fixes are rarely needed.

## Step 2 — Transcribe

Tell the user the estimate first: roughly **2–3x realtime on CPU** for `small`.

```bash
python3 SKILL_DIR/scripts/transcribe.py <audio> --outdir "$work" --model small --vocab "<vocab>"
```

Writes `words.json` (every word with start/end) and `transcript.txt` — one phrase per line as `[start] word@time word@time …`. Read `transcript.txt`; the per-word times are what you cut to.

`--model` takes any faster-whisper name (`tiny` … `large-v3-turbo`) or a local CTranslate2 folder; `--device auto|cpu|cuda` and `--compute-type int8|float16|float32` control where it runs (a GPU is several times faster than CPU; larger models trade speed and disk for accuracy). Defaults come from `~/.config/shenghua/config.json` (`{"whisper": {"model": …, "device": …, "compute_type": …}}`; `VV_CONFIG` points at another file), then the built-ins.

Run it in the background for anything over two minutes; never wait silently — the first run downloads the model and may sit at low CPU for a few minutes. **Long steps outlast shell time limits:** transcribing, keying, rendering and encoding can each outrun an agent's command timeout. Start them detached and poll the log: `nohup <command> > "$work"/<step>.log 2>&1 &`, then read the log until it prints its `Next:` line. `key_greenscreen.py` and `render-frames.sh` both resume where they stopped: re-run the same command.

## Step 2a — Trim the take (every mode with a recording)

```bash
python3 SKILL_DIR/scripts/trim_take.py <audio-or-video> "$work" [--in auto] [--out auto]
```

Cuts the dead air before the first word (keeps 0.5s) and after the last (keeps 2.5s for the outro), writes a lossless `voice.wav`, shifts `words.json` and `transcript.txt` so the first kept moment is 0, and records the cut in `take.json` — `key_greenscreen.py` and `extract_face.sh` apply it, so after trimming every time you handle is an edit time. With a video input it also probes the source into `take.json`'s `probe` block (resolution, fps, codec, bitrate, HDR): an HDR take prints a warning (re-record in SDR — HDR face shots wash out), a non-30fps take an advisory that the edit renders at 30 fps, and Step 6's `--resolution source` reads the block. Pass `--in`/`--out` in seconds to cut by hand; cut points inside the speech make an excerpt, such as a Short from a long talk, and drop the words outside them. Re-running trims from the raw transcript again. From here on, `<audio>` is `"$work"/voice.wav` and `<duration>` is the length it prints.

## Step 2b — Key the speaker (presenter mode)

**Load `references/presenter.md` first** — the keying detail and the layout rules. Then:

```bash
python3 SKILL_DIR/scripts/key_greenscreen.py "$work" --preview 30 [--mask x,y,w,h …]
python3 SKILL_DIR/scripts/key_greenscreen.py "$work" [--mask x,y,w,h …] [--quality master]   # detached for long takes
```

It measures the screen itself (a take with no usable screen fails with the reason — fall back to `bookends`), scales anything taller than `--max-height` (default 3840) before keying so a 4K take needs no manual downscale, and converts any frame rate to 30 fps edit frames. **Look at `presenter-preview.png` and wait for a yes** before the full run. The full run writes `presenter/fNNNNN.webp` (~4 frames/s on 6 cores, so a 6-minute take is about 45 minutes): tell the user, run it detached, and re-run the same command if it stops; it keys only what is missing.

## Step 2c — Clean the voice (optional)

For a noisy phone or room recording (first run: `setup.sh --enhance`):

```bash
python3 SKILL_DIR/scripts/enhance_voice.py "$work"
```

Runs DeepFilterNet on `voice.wav` and writes `voice-clean.wav` (the raw take is kept). You cannot hear the difference — ask the user to listen to both, and if they prefer it, use `voice-clean.wav` as `<audio>` from here on. Skip this step for studio-quiet recordings.

## Step 3 — Proofread the captions

Captions are burned in. Scan `transcript.txt` for misheard words — proper nouns and technical terms break first (observed: `San Micro Systems` → Sun Microsystems, `Ok` → Oak, `CNC++` → C/C++, `Right once` → Write once). Write `<work>/fixes.json` mapping the raw token to its fix; an empty string drops the token:

```json
{ "San": "Sun", "Ok.": "Oak.", "CNC++,": "C/C++,", "alias,": "", "that@50.22": "data" }
```

A plain key fixes the token everywhere. For a common word misheard once, key it as `token@time` (the start time printed in `transcript.txt`) and only that word changes. Optionally write `<work>/keywords.json`, words that stay in the accent colour once spoken: `["Kafka", "Java@3.00"]` — names and the few nouns the video is about, one per phrase at most.

```bash
python3 SKILL_DIR/scripts/build_captions.py "$work"
```

Writes `<work>/words.js`, plus `captions.srt` and `captions.vtt` from the same phrases — subtitle files for platforms that index uploaded captions, muxed or copied by the later steps. Never change timestamps. Tell the user about any token you could not resolve instead of guessing. With a `script`, it is the reference for spelling: a token that differs from it goes in `fixes.json`; an ad-libbed line stays — tell the user where the take left the script.

## Step 4 — Shot list (confirm before building)

Load `references/scene-blocks.md`. Write a shot table — one row per shot, cut on word times:

```
#   in-out        line (spoken)                      block              sound
01  0.00-2.70     Did you know Java wasn't…          slam + strike      hit@0.44 hit@2.12
02  2.70-6.10     a completely different problem     highlight-box      whoosh, hit@4.60
03  6.10-8.30     Back in the early 1990s            vhs + counter      tick, hit@7.20
```

Rules (short form; long form holds evolving diagrams instead, `references/long-form.md` → *Pacing*): a new shot every 1–4 seconds; a hit only on a word that deserves it; captions hidden whenever the spoken word *is* the visual. Read the script once for a reaction beat — a fail, a dry aside, a payoff the viewer would react to out loud — and if one stands out, give it a *Reaction gif* row (`scene-blocks.md` says which lines qualify); none is fine, more than one is rarely right. Find photos and clips before the table is final (Step 5). See `SKILL_DIR/examples/kafka-vs-rabbitmq/` for a complete worked shot list.

**Pick the template (theme) now.** Read `templates/templates.json` and choose the `id` whose mood matches the topic — each theme changes type, colour, captions *and* motion (default shot entry, shake, flash), so it is a real choice, not a palette swap. `kinetic` fast dark explainers (default) · `documentary` founder stories · `newsroom` announcements · `blueprint` architecture · `brutalist` hot takes · `aurora` AI/SaaS launches · `minimal` editorial deep dives · `retro` history of tech. If the user asked for a specific look, use that.

In script mode, the hosts carry the video: cut shots on `line(who, n)` times from `speech.json`, give the sidekick a bubble for their lines (`say()`), name each term with a `.pill` the first time it's spoken, and use lanes and tokens for anything that queues, flows or is numbered.

**Presenter mode:** **load `references/presenter.md` now.** Every row names a layout — `full`, `split-left` (`split`), `split-right`, `close`, the corner bubbles `pip-br`/`pip-bl`/`pip-tr`/`pip-tl`, `cut`, plus chapter cards for long talks. A chosen `position` becomes the default layout for every shot; with `auto`, follow the pacing rules (never the same layout twice in a row, varied holds, a pip bubble over most cutaways).

**Bookends:** **load `references/face-bookends.md` now.** The first and last rows are face shots (*Face hook*, *Face sign-off*), timed from the script's `[FACE]` sections; a series badge goes on shot 02.

Show the table and the media list (every photo and clip, with its source and licence) to the user. Wait for a yes — this is the expensive part to change later.

## Step 5 — Source photos and clips

Whenever the audio names a person, company, product or event, show it: the founder on stage, the product launch, the person saying the line. `find_media.py` searches licensed sources (Wikimedia Commons, Openverse, Internet Archive, and Pexels with `PEXELS_API_KEY`) alongside the open web (Bing images) and YouTube:

```bash
python3 SKILL_DIR/scripts/find_media.py search "$work" "Yang Zhilin portrait"                       # photos
python3 SKILL_DIR/scripts/find_media.py search "$work" "Yang Zhilin keynote" --kind video           # talks
python3 SKILL_DIR/scripts/find_media.py fetch "$work" m6 --name yang-launch
python3 SKILL_DIR/scripts/find_media.py fetch "$work" m8 --name yang-gtc --section 120-150
python3 SKILL_DIR/scripts/find_media.py fetch "$work" --url "https://youtu.be/…" --name demo --section 30-45
python3 SKILL_DIR/scripts/find_media.py search "$work" "facepalm" --kind gif                        # reactions
python3 SKILL_DIR/scripts/find_media.py fetch "$work" m11 --name facepalm
```

Gifs come from Commons, and from GIPHY when `GIPHY_API_KEY` is set (GIPHY results are marked ⚠). A fetched gif becomes an mp4 in `clips/src/`; cut it like any clip with `--loop` so it fills a longer shot. Never put a `.gif` in an `<img>`: the browser plays it on its own clock, so every render would differ. One or two reaction beats per video, on a punchline, never on the point itself.

Results without a licence are marked ⚠. When a licensed result is as good a shot, take it; otherwise use the best shot, preferring the subject's own channel over re-uploads. Queries that work: the name plus the company, then name + event ("keynote", "launch", "interview"). A YouTube or page fetch downloads the video once into `clips/src/.cache/` (720p over 15 minutes), then cuts `--section` (≤120s) from it, so later sections are instant — tell the user the first fetch of a long talk takes a few minutes. To find a quote inside a section, run `transcribe.py` on the fetched clip and use the word times as `--from` in Step 6. With the vision setup (`setup.sh --vision`), a fetched photo's face position is recorded in `faces.js`, so `.photo`/`.pip` boxes keep the face in frame automatically.

**Look at every photo and every preview sheet before using it.** Search results lie: the wrong person with the same name, a news site's logo or banner burned into the image, a thumbnail with text on it. Crop around a banner with `object-position` or pick another result. If you cannot view images, list each file with its source and what you expect it to show, and ask the user to confirm.

Logos: `https://cdn.jsdelivr.net/npm/simple-icons@13/icons/<slug>.svg`. Every fetch is recorded in `<work>/credits.json`; log hand-sourced files yourself. The report lists every ⚠ file so the user knows which footage belongs to someone else before posting.

Quoting a paper or an article? Capture the passage itself so it can appear on screen with the quoted lines highlighted:

```bash
node SKILL_DIR/scripts/excerpt.js "$work" <url> --text "the quoted passage" --name <slug>
node SKILL_DIR/scripts/excerpt.js "$work" --pdf paper.pdf --page 3 --rect x,y,w,h --name <slug>
```

Writes `excerpts/<slug>.png` plus the highlight's position into `excerpts.js`, and credits the source in `credits.json` (marked ⚠ unlicensed — a quotation, so name it in the description). Place it with the *Document card* block (`docCard()`) in Step 6.

## Step 6 — Author the composition

```bash
python3 SKILL_DIR/scripts/fill_template.py "$work" <duration> --format vertical --template <template-id> [--brand <kit>]
# --format vertical|landscape|square|portrait · omit --template for the default kinetic theme
# --resolution 4k records a 2x master in render.json; render-frames.sh then renders 4k by default
# --resolution source matches the probed take (Step 2a): a 4K recording gets a 4K master without you computing anything
```

Colours in shots come from the kit: write `var(--brand-primary)`, `var(--brand-primary-ink)` (the brand colour as readable text), `var(--brand-text)`, `var(--brand-muted)`, `var(--brand-surface2)`, `var(--brand-success)`, `var(--brand-error)`, never a hex value, so the same shots render in any client's colours. Logos are in `BRAND.logos` (`mark`, `wordmark.onDark`, `wordmark.onLight`); see *Logo end card* and *Corner mark* in `scene-blocks.md`.

`<duration>` = last word end + ~2.5s for the outro; with a `video`, last word end + 0.5s, and never past the recording's length (`ffprobe -v error -show_entries format=duration -of csv=p=0 <video>`). `fill_template.py` rounds it up to a whole frame and prints it; use that number from here on.

Writes `<work>/index.html` from the template with brand, geometry and duration filled, and installs the vendored assets and the kit as `<work>/vendor` and `<work>/kit` — **copies**, so the project survives skill updates and being moved to another machine. **Re-running keeps your authored shots** (BEGIN/END SHOTS and TIMELINE carry over), so re-fill freely to change the kit, theme, format or duration; `--force` starts over with the stock demo. `--relink` re-installs `vendor/` and `kit/` without touching the composition — the fix when an old project's symlinks dangle after a skill update. Mode specifics: presenter mode sets `presenterPosition()` and the speaker's look once, then every shot's layout (`references/presenter.md`); bookends extracts the face frames with `extract_face.sh` and plays them with `faceCam()` (`references/face-bookends.md`).

For every clip shot, cut the fetched clip to the shot's in/out. The size is the box it fills — `vertical` or `landscape` for full-bleed, or the `.pip` box size like `900x620`. `--from` is the second inside the clip to start at. Add `--audio` when the clip's own sound should play — a founder's line, a crowd:

```bash
bash SKILL_DIR/scripts/extract_clip.sh "$work"/clips/src/torvalds-talk.mp4 "$work" 900x620 torvalds 8.9 12.6 --from 20 --audio
bash SKILL_DIR/scripts/extract_clip.sh "$work"/clips/src/facepalm.mp4 "$work" 900x620 facepalm 31.2 33.4 --loop
```

Clip audio ducks under the narration automatically, so it only really plays over a pause in the voice. For the speaker's line to land, place the clip over a gap in the recording (a scripted `[CLIP]` beat) or leave it silent and put the quote on screen with a *Portrait quote*. **B-roll is the same mechanism** — a `clip()` (or the alias `broll()`) under narration; the *B-roll under narration* block in `scene-blocks.md` has the full-bleed + lower-third pattern.

Replace the demo shots between `BEGIN SHOTS` / `END SHOTS` (markup) and `BEGIN TIMELINE` / `END TIMELINE` (GSAP) with your shot list, using the helpers the template already defines. Keep the outer `#world` and `#cam` containers intact: `shot()`, `slam()`, `hit()`, `rise()`, `pop()`, `stagger()`, `drift()`, `kenBurns()`, `lowerThird()`, `ticker()`, `typer()`, `counter()`, `swap()`, `terminal()`, `moveTo()`, `centerOf()`, `gantt()`, `faceCam()`, `clip()`, `broll()`, `punchIn()`, `punchPulse()`, `docCard()`, the `NOCAP` ranges, and the `CAP_STYLE` constant. Every helper that makes noise pushes its own sound cue. `slam()`/`pop()`/`rise()` take `"spring"` as a final argument for a spring-physics entry; `punchIn()` slow-pushes a face shot or photo, `punchPulse()` snap-zooms an emphasis beat — see *Punch-in* in `scene-blocks.md`. `CAP_STYLE` overrides the theme's caption motion (`pop` word-by-word, `rise`, `fade`, `phrase`, `off`); left `null`, each theme's own caption motion applies.

The display style (`.xl`) is uppercase and width-expanded; captions are condensed. Size headlines for the expanded width — a vertical frame fits ~6 characters at 250px.

## Step 7 — QA stills (loop until clean)

Pick one timestamp per shot, at the moment of densest content. Pass them as a comma-separated list with **no spaces**; spaces parse as `NaN`:

```bash
node SKILL_DIR/scripts/render.js stills "$work"/index.html "$work"/stills 0.6,2.4,4.9,…
bash SKILL_DIR/scripts/contact-sheet.sh "$work"/stills "$work"/contact.jpg
```

Measure first — this needs no eyes and runs in seconds:

```bash
node SKILL_DIR/scripts/render.js check "$work"/index.html ["$work"/check.json]
```

It seeks to each shot at 25%, 50% and 85% of its window and reports text past the frame edge, text under the caption box, text over the speaker's face (presenter mode), characters the kit's fonts lack (naming the characters; a kit `fonts.fallback` marks deliberate coverage), shots that render nothing at all three moments, dangling `vendor/`/`kit/` links from before the copy layout (fix: `fill_template.py … --relink`), and `PAGE ERROR` lines. Exit 1 means findings. Fix and re-run until it is clean; it catches clipped headlines that a full render would waste minutes on.

Then, **if you can view images**, read `contact.jpg` for what measurement cannot judge: crops that cut off a face or subject, an image that does not match the line, and layouts that fit the frame but read badly. Fix, re-render only the affected stills, and look again. If you cannot view images, say so in the report and ask the user to look at `contact.jpg` before Step 9. Do not start Step 9 with a known defect — a full render costs minutes.

## Step 7a — Preview the edit in the browser (fast, optional)

Stills can't judge motion. Serve the work dir and review pacing, transitions, caption timing and word emphasis live:

```bash
python3 SKILL_DIR/scripts/preview.py "$work"             # prints http://localhost:8377/_preview.html
python3 SKILL_DIR/scripts/preview.py "$work" --check     # headless self-test, exit 0/1
```

Play, scrub a frame at a time, or click any word in the transcript to jump the playhead to it — the edit loop before committing to a render. The shell drives `window.renderAt(t)` from its own rAF loop; the render path is untouched. Serve detached with `nohup` and a log if your shell has a time limit. Run `--check` to verify the shell headlessly; ask the user to open the URL when pacing matters. Fix, re-check, then move to sound.

## Step 8 — Sound

```bash
node SKILL_DIR/scripts/render.js cues "$work"/index.html "$work"/cues.json
python3 SKILL_DIR/scripts/synth_audio.py "$work"/cues.json <duration> "$work" --template <template-id> --drop <time-of-final-slam>
```

Writes `sfx.wav` and `music.wav`. When `words.js` exists, it also writes a duck envelope into `mix.json`: pauses of 0.6s or more in the voice let the music swell back up between phrases instead of staying flat-ducked throughout — no flag needed. Pass the same `<template-id>` as Step 6: the music follows the theme's tempo, key and layers, and varies per video (the slug folder). Omit `--drop` if the video has no final slam; otherwise use the time of the last big hit. Optional pacing flags: `--drums-from <t>` brings the drums in at `<t>`; `--quiet <a>:<b>` ducks the music between `a` and `b` (repeatable). Story moments make the music act out a line: `--stop <a>:<b>` (tape stop, silence, back at `b`), `--muffle <a>:<b>` (behind a wall, opening into `b`), `--stutter <a>:<b>` (a stuck one-beat loop until `b`); when to use each is in `scene-blocks.md` → *Sound cues*. With `music` set to a file, pass `--no-music` and give that file to Step 10; with `none`, pass `--no-music` and nothing else.

The kit's `audio` block (`references/brand-kits.md` → *Sound*) applies here without flags: a sound pack or the kit's own files replace synth cues, any cue can be quieter, louder or muted, the kit can bring its own music track, and its mix levels go into `mix.json` for Step 9 or 10. When the user asks for a different whoosh, quieter hits or their own music, change the kit, not the scripts; for one video only, pass the track to Step 10 instead.

You cannot hear the result. Say so in the report and ask the user to listen.

## Step 9 — Render frames

**Anything over about a minute: render with `render-chunks.sh`** — it renders and encodes in ~30 s chunks, streaming each chunk's frames straight from Chromium into the encoder, so no frames directory ever exists and peak scratch is just the chunk mp4s no matter how long the video is (the old whole-frames path needs ~1.4 MB × frames: 18 GB for a 7-minute 1080p video, ~70 GB at 4K — pass `--png` only when you need PNG frames on disk for debugging, e.g. contact sheets or re-rendering a single frame by number). A killed run resumes at the first missing chunk:

```bash
bash SKILL_DIR/scripts/render-chunks.sh [--blur 4] [--resolution 4k] [--chunk 30] [--music file] \
  "$work"/index.html "$work" <duration> <audio> "$out"
```

`--resolution 4k` renders a 4K master; without it the fill's `render.json` decides. Pass `--blur 4` for the final render only: it adds motion blur and makes the render about 8× slower — `VV_BLUR_SAMPLES=2` gives a cheap approximation while you judge whether blur is worth the time. A chunked render produces the mp4 directly — **skip Step 10** and go to Step 10a.

**Short videos, drafts and single-shot fixes** use `render-frames.sh`:

```bash
bash SKILL_DIR/scripts/render-frames.sh [--blur 4] [--resolution 4k] [--force] "$work"/index.html "$work"/frames <duration> [workers] [from_frame to_frame]
```

Frames render supersampled (2x) and are saved as lossless PNG: crisp edges and exact brand colours, about 1.2 MB a frame (~4 GB for 108s) and 2–3x slower than a draft. The script prints the frames' disk cost up front. Run it in the background; progress lines (`progress 812/3240 frames · 2.1 fps · 18m05s left`) go to stdout. For a quick preview cut, prefix `VV_QUALITY=draft` (1x JPEG); render the final with the default.

**A killed render resumes:** completed frames are skipped, so re-run the same command — no gap hunting. `--force` re-renders everything, which a composition change needs. The optional frame range re-renders a single shot after a fix; each bound is its own argument, so it is safe under zsh. Re-render a range with the same quality as the rest, or Step 10 refuses to mix them.

## Step 10 — Mix and encode

Skip this step when Step 9 used `render-chunks.sh` — it already encoded and mixed. Otherwise:

```bash
out="<brand.output.dir>/<slug>/<slug>.mp4"
bash SKILL_DIR/scripts/mix-encode.sh [--10bit] [--embed] "$work" <audio> <duration> "$out" [music-file]
```

Normalises the voice, ducks the music under it (letting it swell in the voice's pauses when `mix.json` has a duck envelope), lays the SFX on top, pads everything to the full duration, and targets −14 LUFS, with progress lines while it encodes. Video is H.264 at CRF 16 (slow preset, bitrate-capped so film grain can't balloon the file), converted and tagged as BT.709 so phones show the brand colours as designed. The cap scales with the canvas from `render.json`: 16 Mbps at 1080x1920, up to 68 Mbps for a 4K master. A 108s vertical lands around 200 MB: high enough to survive the platform's own re-encode.

- Draft JPEG frames encode `veryfast`/CRF 20 — a preview cut, fast. `VV_PRESET` overrides the preset (e.g. `medium` on a slow machine).
- `--10bit` encodes 10-bit H.264 against banding in dark gradients.
- `--embed` muxes `captions.srt` as a soft subtitle track. Either way, any `captions.srt`/`captions.vtt` are copied next to the mp4.

## Step 10a — Deliver (optional, recommended)

```bash
bash SKILL_DIR/scripts/deliver.sh [--cover <seconds>] "$work" "$out"
```

Assembles `<work>/delivery/`: the master mp4, a web copy (~8 Mbps, under half the master's size), the `captions.srt`/`.vtt`, a cover frame (default 1.0s in, where the title card sits), `credits.txt` from `credits.json`, and a `README.txt` listing the folder. Hand the folder — or the web copy — to whoever posts the video.

## Step 10b — Assemble the chapters (long form)

Once every chapter has its `<dir>/<dir>.mp4`:

```bash
python3 SKILL_DIR/scripts/assemble.py <output dir>/<slug>
bash SKILL_DIR/scripts/deliver.sh --cover <seconds> <output dir>/<slug>/assembly <output dir>/<slug>/<slug>.mp4
```

Joins the chapters listed in `chapters.json` without re-encoding the video, normalises the joined audio once to −14 LUFS, and writes `assembly/captions.srt`/`.vtt` on the joined timeline, `assembly/chapters.txt` (YouTube timestamps) and `assembly/credits.json`. Details and its warnings: `references/long-form.md` → *Assemble*.

## Step 11 — Verify, then report

Before reporting, extract a frame from the **encoded file** at a shot you changed, read it, and check the duration and size — a still rendered from the HTML is not proof the video contains the fix:

```bash
ffmpeg -v error -y -ss <t> -i <out.mp4> -frames:v 1 -vf scale=360:-1 <work>/verify.jpg
ffprobe -v error -show_entries format=duration,size -of compact <out.mp4>
```

When the input was a video (bookends, presenter), also grade the output against the source:

```bash
python3 SKILL_DIR/scripts/check_quality.py <source-video> "$out"
```

Prints a VMAF score (95+ means the edit preserved the footage's quality; below, re-encode with a higher bitrate). Builds of ffmpeg without libvmaf skip cleanly — say so in the report rather than claiming a score.

```
<slug>.mp4 · 1080x1920 · 108.2s · 112 MB · -14.7 LUFS

  shots 30 · sound cues 117 · images 4 · clips 2 · captions fixed 6

  credits     James Gosling 2008 (Wikimedia, CC BY-SA) · Solitary oak (geograph, CC BY-SA)
  unverified  music taste — listen before posting · timeline years are stylistic

Next: preview it on a phone, then post it with the credits in the description
```

`mix-encode.sh` prints raw `ffprobe` output; reformat it into the line above for the report. Get the credits with `find_media.py credits "$work"` ready to paste into the description, and name any unlicensed clip on its own line. Point at the `delivery/` folder when Step 10a ran.

**A retake of the same script:** don't re-author. Transcribe and trim the new take, `fill_template.py` its work dir, then `python3 SKILL_DIR/scripts/retime.py <old work> <new work>` re-times the whole edit — timeline, NOCAP ranges, `@time` keys in fixes/keywords — onto the new take. Passages that differ between takes (ad-libs, cut sentences) are listed, never silently mis-timed; handle those by hand, then re-run `build_captions.py` in the new work.

---

## Non-negotiables

- **Shot list confirmed before authoring.** Rendering is cheap; redesigning thirty shots is not.
- **Every image and clip is looked at before it is used.** Never ship media you have not seen.
- **Every file is credited.** Licensed or not, each photo and clip goes in the description credits, and the report names every ⚠ file and every invented detail (dates, labels) that isn't in the audio.
- **Every fix is verified in the encoded file**, not just in a still.
- Transcription is local. Never upload the audio. Voices are synthesized locally too, and named in the report so the user can disclose them.
- Characters are original. Never draw, name or imitate an existing cartoon, film or game character.
- Colours come from the kit's `--brand-*` tokens, never hex values in shots. One brand accent; `--brand-success` only for success states, `--brand-error` only for errors.
- A client's logos and fonts come from the client. Never fetch a company's logo or font from the web, and never put a competitor's logo in a video unless the client asks for it.
- Timelines are deterministic: no `Math.random()`, no `Date.now()`. The grain uses a seeded PRNG.
- Captions never cover the element the viewer is meant to read; hide them via `NOCAP` instead.
- Never commit rendered files or `work/`.
- `faceCam()` in/out times match the `extract_face.sh` ranges exactly; never re-time a face shot alone. The same holds for `clip()` and `extract_clip.sh`.

## Failure states

| Symptom | Cause | Fix |
|---|---|---|
| `Executable doesn't exist at …ms-playwright…` | playwright-core updated, its Chromium build isn't installed | re-run `setup.sh` |
| Fix visible in stills but not in the video | frames never re-rendered — a range passed as one quoted string renders zero frames | re-run `render-frames.sh` with the range as two separate args; completed frames are skipped |
| `… is a dangling symlink` from `render.js` | an old project's `vendor/`/`kit/` links broke when the skill updated | `fill_template.py "$work" <duration> --relink` |
| Video shorter than the audio | an audio filter trimmed the stream | `mix-encode.sh` pads and trims to the duration; don't hand-roll the mix |
| Output file is hundreds of MB | film grain defeats compression at constant CRF | keep the `-maxrate` cap in `mix-encode.sh` |
| `frames/ mixes high-quality PNG and draft JPEG frames` | a range was re-rendered with a different `VV_QUALITY` | re-render the whole video with one setting |
| Accent colour looks orange or washed out on a phone | an encode without the BT.709 conversion and tags | use `mix-encode.sh`; don't hand-roll the encode |
| Frame render fills the disk | high-quality PNG frames are ~1.2 MB each | `render-chunks.sh` (the default for finals) streams frames into the encoder with no frames directory; the `--png` debug path needs real disk — free space, or preview with `VV_QUALITY=draft` |
| Wrong or fallback font in stills | fonts not downloaded for this brand | re-run `setup.sh` with the kit |
| `font X lacks glyphs for: …` from `render.js check` | characters the kit's fonts don't cover | swap them, or set `fonts.fallback` in brand.json (`references/brand-kits.md`) |
| `PAGE ERROR` in render output | a script error in the timeline | fix it; GSAP only warns on missing selectors, so also check each shot visually |
| `missing frame face/… ` or `clips/…` stops the render | a `faceCam()` / `clip()` range is wider than the extracted one | re-run `extract_face.sh` / `extract_clip.sh` with that shot's in/out |
| YouTube fetch crawls or fails with a challenge warning | no JS runtime, or yt-dlp is out of date | needs `node` or `deno` on PATH; `pipx upgrade yt-dlp` |
| `kokoro-onnx is not installed` / `Voice model missing` / `Cannot load the 'base' alignment model` | script mode set up without voices, or offline before the models were fetched | `setup.sh --voices` (online, once) |
| `deepfilternet not installed` from `enhance_voice.py` | Step 2c run without the optional install | `setup.sh --enhance` (online, once) |
| `pdftoppm not found` from `excerpt.js` | PDF excerpt without poppler | `apt install poppler-utils` / `brew install poppler` |
| `no probed source` from `fill_template.py --resolution source` | no `probe` block in `take.json` — audio-only input or trim never ran | run `trim_take.py` on the video first, or pass `--resolution 1080p`/`4k` |
| `PAGE ERROR … excerpts.js` | work dir filled before excerpts.js existed | `fill_template.py "$work" <duration> --relink` writes the placeholder |

Mode-specific failures are in each mode's reference: `references/presenter.md` (keying), `references/face-bookends.md` (face shots), `references/brand-kits.md` (kits and fonts).
