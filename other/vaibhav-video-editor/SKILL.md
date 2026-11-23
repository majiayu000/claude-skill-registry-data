---
name: vaibhav-video-editor
description: Full start-to-finish video editing that runs every installed video skill as one pipeline. Cuts silences and retakes, plans the edit from the transcript, then adds captions, motion graphics, face-tracked effects, transitions, camera moves, b-roll, sound effects and music, checks its own work and exports the final MP4. Routes each beat to the right tool (awa-video-reel, the 45-effect engine, Brand Nat codes, HyperFrames, Remotion, the Video Editor plugin, MultiCam shot) and follows the saved style (my-video-style). Also makes fully animated videos from a script with an AI voiceover (ElevenLabs, Google Gemini, HeyGen or free Kokoro). Use when someone types /vaibhav-video-editor, says "edit this video start to finish", "do the full edit", "make this a finished reel", "edit it in Nick style", "make an animated video with a voiceover", or asks for an edit combining cuts, motion graphics, effects, transitions and sound. For a single effect only, use /effects instead.
---

# Vaibhav AI Video Editor

You are the director and the editor. The user hands over raw footage and a goal; you deliver a finished, checked video. You decide which tool does each job, show one plan, wait for a yes, then do every technical step yourself.

Most users are not technical. Keep messages short and visual, never ask them to run commands, and never install anything without asking first.

This skill does not replace the other video skills. It runs them in the right order and gives them one shared plan. Read the parts of their `SKILL.md` files that you need before you call their scripts, and follow their rules (flags, file formats, gotchas). Paths that start with `references/` or `scripts/` are inside this skill's folder, unless the sentence names another skill ("its `scripts/render.sh`" means that skill's folder). `scripts/preflight.sh` prints where every other skill lives. Use absolute paths in commands.

## The pipeline at a glance

| # | Stage | Tools | Output |
|---|---|---|---|
| 0 | Preflight | `scripts/preflight.sh` | what's installed, what's missing |
| 1 | Brief and style | `my-video-style` or `references/house-style.md` | the edit brief |
| 2 | Prepare | transcribe, `scripts/check_words.py`, fix names, find faces | `work/NAME-words.json`, beat stills |
| 3 | Clean cut | silences, fillers, retakes | `work/NAME-cut.mp4` |
| 4 | Website b-roll question | awa-video-reel step 2 | yes + link, or none |
| 5 | Storyboard (approval gate) | `references/beat-map.md`, Brand Nat codes | plan table + style card |
| 6 | Build | engine A, B or C (below) | picture with graphics |
| 7 | Sound | awa mixer or `scripts/sound_mix.py` | final mix at -14 LUFS |
| 8 | Quality check | `references/quality-check.md` | fixes, then a final render |
| 9 | Deliver | | final MP4, no-music copy, credits, caption |

Never skip stage 5's approval, and never skip stage 8. No camera footage? Use **Voiceover mode** (near the end): script, AI voice, then a fully animated video.

## Stage 0: Preflight

Run `bash scripts/preflight.sh`. It prints one line per tool and component (`OK`, `MISSING` or `OPTIONAL`) and the paths it found. Keep the paths for later stages.

- **Required:** ffmpeg + ffprobe, Python 3, and at least one engine (awa-video-reel, the Video Editor plugin, or HyperFrames).
- **Missing a required tool:** say what it is for in one line and offer to install it. Follow the installing skill's own setup (`awa-video-reel/scripts/setup.sh`, `effects/scripts/setup.sh`, `/video-editor:start`, or brand-nat-styles' one-time setup, which avoids Homebrew for non-technical users).
- **Missing an optional component:** carry on without it and use the fallback in `references/toolkit.md`. Mention it once at the end ("Install X to get Y next time").
- Skip preflight if it already passed in this session.

## Stage 1: Brief and style

**Load the style first.** If `~/.claude/skills/my-video-style/SKILL.md` exists, read it in full: it is the user's own taste and it wins over every default here. If it names a skill that isn't installed, use the nearest tool from this toolkit and say so once. If there is no saved style, use `references/house-style.md` and offer `/video-editor:style` at the end.

**Who wins when rules disagree:** what the user says in this chat > a style preset they picked for this video > `my-video-style` > the Brand Nat codes they picked > the engine skill's defaults > `references/house-style.md`. A preset sets the look; their saved style still decides anything the preset doesn't cover (spellings, handle, export settings).

**Style presets** live in `references/styles/`. Read the whole file when the user names one:
- `kinetic-promo.md`: a clean, quick faceless reel from an AI voice: big kinetic type with a yellow key word, motion graphics that act out each line, zoom-through transitions, punch-ins, a drifting dot grid, a comment CTA card. The default look for voiceover mode when the user gives no other style. Worked example: `examples/kinetic-promo/`.
- `nick-saraev.md`: Nick Saraev's fast AI-tool list reels (split card, full face and full-screen stat layouts, glowing browser cards, blue keyword captions, pause-free pace, comment-keyword CTA). Triggers: "Nick style", "Nick Saraev style", "edit like Nick". Has a classic 2025 variant.

Then ask only what you don't already know, in one short message:
- Which video? (a path, or drag it in; several clips are joined in name order). No footage, or they want an animated video with an AI voice: switch to **Voiceover mode** below.
- Where is it going and what shape? (default from the style: usually 9:16 for Reels, TikTok and Shorts)
- In one line, what is it about, and what should the viewer do at the end?
- Style: their saved style, a style preset (`references/styles/`, for example Nick style), Brand Nat codes (offer to open the guide: `brand-nat-styles/guide/index.html`), a vibe in words, or "you pick".
- Look: clean or cinematic. Music: a mood or none. Handle for an end card, if any.
- Anything to feature (logo, screenshots, their own screen recording) and names that must be spelled exactly.

If they're in a hurry, use the style and defaults and go.

**Project folders.** Work inside a project folder: originals in `raw/` (never modified), assets in `assets/`, working files in `work/`, finished videos in `exports/`. Name every working file after the video (`raw/beach-day.mov` → NAME `beach-day`, `work/beach-day-words.json`). Create the folders if they're missing.

## Stage 2: Prepare

1. **Several clips:** join them first (Video Editor plugin `join.py`, or ffmpeg concat after matching size, fps and audio). Use the joined file from here on.
2. **Probe:** size, shape, fps, duration, audio, whether a person is on camera. awa-video-reel's `scripts/probe.py` also finds the median face box.
3. **Transcribe with word timings.** Use the best tool available, in this order: the user's style or memory (it may name a working whisper setup and flags, for example for mixed Hindi and English), the Video Editor plugin's `transcribe.py --vocab "NAMES"`, the effects engine's `words.py`, then `npx hyperframes transcribe audio.mp3 --json`.
   Never run a tool that writes next to its input (the effects engine's `words.py` writes `<video>.words.json` and may install its own transcriber) on a file in `raw/`: copy it to `work/` first, and ask before anything installs.
4. **Check the timings against the audio:** `python3 scripts/check_words.py <video> work/NAME-words.json`. Whisper word times drift after music, applause or a stretch with no talking (turbo models by a second or more), and whisper.cpp without alignment gives coarse word times. For each flagged stretch, re-transcribe just that stretch cut on its speech gaps, or snap the first word after each gap to where the speech starts. Every visual is timed to these words, so fix them before planning.
5. **Read the whole transcript.** Fix misheard names and brands (for example "cloud code" → "Claude Code") everywhere you'll use the words.
6. **Find the face in every shot.** Make a still per planned beat with a 10-row grid (`ffmpeg -ss <t> -i <video> -frames:v 1 -vf "scale=216:384,drawgrid=w=216:h=38.4:c=red@0.5"`, then tile them) and note where faces sit. In multi-scene or AI-generated videos the face moves between shots (top of frame in one, middle in the next, a row of faces on a stage), so each graphic is placed for its own shot, not for the whole video. Note bright or white areas too: white text over them needs a dark backing.
7. **No speech or no audio:** no captions and no silence cuts. Pick moments by looking at frames, and build the edit from music, titles and motion.

## Stage 3: Clean cut

The rough cut comes before any graphics, so every later time sits on the final timeline.

1. Find silences and fillers: the Video Editor plugin's `silences.py --words work/NAME-words.json --out work/NAME-keep.json`, with the style's settings (`--min-silence`, `--pad-before`, `--pad-after`, `--remove-fillers`). Without the plugin, use ffmpeg `silencedetect` (about -35 dB, 0.35 s) plus the transcript gaps.
2. **Retakes:** read the transcript for repeated or restarted lines. Keep the last complete take, drop the earlier ones and any "wait, let me redo that".
3. **Respect a rough cut.** If the user already cut the video (or their style says they send rough cuts timed to screen recordings), only trim silences where it won't break a transition, a scroll or a screen recording. Ask when unsure.
4. Render the cut: `python3 scripts/apply_keep.py <video> work/NAME-keep.json work/NAME-cut.mp4`. It cuts with short audio fades so the joins don't click. If nothing needs cutting, skip it and use the original: say so in the plan.
5. Transcribe `work/NAME-cut.mp4` again, or shift the word times with the `-timemap.json` that `apply_keep.py` writes next to the cut. **Every time from here on is on the cut's timeline.**
6. Over 60 s and meant for a short: offer the strongest 60 s from the transcript, or `/video-editor:clips` to make several shorts.

## Stage 4: Ask about websites

If the video names a website, app or online tool they show or tell people to use, ask before planning, exactly as awa-video-reel step 2 describes: offer recorded b-roll of using it start to finish, ask for the link, never guess a URL, and offer the Claude Code follow-through when the video says to paste a prompt somewhere. Their own screen recording is always an option. No website in the video: don't ask.

## Stage 5: Storyboard (approval gate)

Plan the whole edit before rendering anything. Read `references/beat-map.md` (which visual fits which moment, and how every Brand Nat code is built) and `references/transitions-sound.md`.

1. **Edit thesis:** one line on what this edit must do for the message.
2. **Sections:** hook (first 1 to 3 s), setup, each point or proof, payoff, call to action.
3. **Choose the engine** (more in `references/toolkit.md`):
   - **A. Reel engine** (awa-video-reel): clips up to 60 s, talking head or not. The default when it's installed. Effects, captions, cards, camera moves, website b-roll, Remotion intro and end cards, music and sound effects in one render. It renders at the source fps up to 30.
   - **B. Long-form engine** (Video Editor plugin `render.py`): over 60 s, many screen recordings, a style that needs 60 fps or Remotion, or no awa install. Effects come from the effects engine as a pre-pass, motion graphics from HyperFrames or Remotion as overlays, sound from `scripts/sound_mix.py`.
   - **C. Motion-graphics build** (HyperFrames, or Remotion when the style says so): graphics-led looks where the footage becomes one layer in a designed frame (Nat L3, L7, L8, L9, G3, G7, X3, X11, X19, explainers). Load `/hyperframes` first and follow its work loop.
   - You can combine them: for example engine A for the edit, plus a HyperFrames hook rendered separately and joined in front.
4. **Write the plan table in chat:**

   | # | Time | What's said | On screen | Built with | Transition in | Sound |
   |---|---|---|---|---|---|---|

   "Built with" names the tool and the exact primitive, for example `effects: orbit`, `awa card: list`, `HF: logo tiles (Nat V1)`, `camera: punch 1.1`.
5. **Style card under it** (max 6 lines): the style preset if one is used, the Brand Nat codes in play with their names (even when the user didn't pick codes, name the closest ones so they can swap them), look (clean or cinematic), accent colour, captions, music (mood and track), end card, b-roll.
6. **Budget and pacing rules:**
   - 5 to 6 styles for the whole video. Same job, same treatment every time.
   - A new beat every 3 to 6 s (or the style's pace, for example 2 to 3 s). Never two big things at once: an effect, a card and a b-roll never overlap. Max 2 layers stacked.
   - Leave talking-only breathers. Effects 1.5 to 4 s, cards 2 to 6 s, b-roll 3 to 6 s.
   - Open strong in the first 2 s. Close on the call to action, then the end card.
   - Numbers on screen are only numbers they said or gave. Never invent stats, views or prices.
7. **Optional extras** to offer in one line each when they fit: a MultiCam shot prompt (`/multicam-shot`) for an AI camera pass on a short hook (it makes a prompt for Seedance 2.0 Fast, not a render); a Remotion intro card when the video doesn't open with its own hook.
8. Ask: "Any changes? Point at a row number, or say go." Wait. Apply changes and re-show only what changed.

## Stage 6: Build

Make the first render a preview where the engine supports it (half size or `--preview`), and check stills before any long render.

**Engine A (awa-video-reel).** Run its `scripts/prepare.sh` on `work/NAME-cut.mp4`, then write `fx.json`, `edit.json` and `cards.json` in its job folder from the approved plan, using the exact formats, effect gotchas and caption-off list in its `SKILL.md`. Check effect stills with `fx.py --still`, then `bash scripts/render.sh <job>` in the background. Use `SKIP_FX=1` (and `SKIP_HF=1`) on re-renders when only cards, captions, music or sound changed. For Nat codes it can't express, build that moment in HyperFrames (engine C) and join or overlay it after.

**Engine B (Video Editor plugin).** Read its `skills/edit/reference/plan-format.md`. Run the effects pre-pass on the cut first when the plan has effects (`effects/scripts/fx.py --plan`), and use that file as the plan's `input`. Write `work/NAME-plan.json` (captions, titles, zooms, overlays, b-roll; `keep` covers the whole clip because the cut is done), render with `--preview`, check, then render full. Motion graphics it can't express: build them in HyperFrames with a transparent root (`hyperframes/references/overlays.md`), render, and place them with `overlays`.

**Engine C (HyperFrames).** Load `/hyperframes` and read `motion-doctrine` and `captions-overlay` before composing. Put the cut footage in as a video layer (with `data-has-audio="true"` so the voice comes through, then add sound in stage 7); use `npx hyperframes remove-background` for anything that goes behind the person (Nat H1, L1, X1, X3, X17). Writing the composition from a small generator script (word groups, cue list and timings as data) keeps re-builds fast. Run `npx hyperframes check --json` and fix every error and every contrast or readability warning, then `npx hyperframes snapshot --at <the middle of every beat> --no-end` and look at each still before the full render (`render . -o out.mp4 --fps <fps>`, in the background). In Remotion, follow `remotion-best-practices`.

**60 fps edits.** The effects engine and awa render at 30 fps at most. When the style or the footage is 60 fps, don't run them over the whole video: cut each effect's shot out (with a little handle on each side), run the effect on that segment, then splice it back frame-exact into a 60 fps base (`fps=60`, `trim=start_frame/end_frame`, original audio mapped untouched) and build everything else on that base. Check that the base has the same frame count as the original. Tell the user which seconds are 30 fps inside the 60 fps video.

**Reuse earlier work.** If the project already has a build for this video (an earlier HyperFrames or Remotion project, keyed screen recordings, cropped logos, measured box positions), reuse those assets and measurements instead of rebuilding them.

**Rules for every engine:**
- Never cover the face (eyes to chin). Graphics go above the head, below the chin, beside the face, or behind the cut-out person.
- Keep text inside the platform safe zone (`references/house-style.md`, or the style's own numbers).
- Captions off while an effect or card puts its own text or UI in the caption area.
- Real proof only: a recreated screen is never presented as a real one. Blur private names, emails and numbers.
- New filename for every version (`NAME-v001.mp4`, `v002`...). Never overwrite the original.

## Stage 7: Sound

- **Engine A:** awa's mixer already places sound effects on every effect, card, list item, b-roll and camera move, ducks music about 10 dB under the voice, and mixes to -14 LUFS. Add extra cues with `"sfx"` in `edit.json` and scale with `"sound": {"level": ...}` (Nat S1 = 1.0, S2 = about 0.6 with only big moments).
- **Engines B and C:** write `work/NAME-cues.json` from the plan (one cue per visual beat, rules in `references/transitions-sound.md`) and run `python3 scripts/sound_mix.py`. Named sounds come from awa-video-reel's library when installed, else HyperFrames' bundled 21 (the same names), so this works with HyperFrames alone; a missing sound is skipped with a warning. It places the sound effects, ducks music under the voice, high-passes at 80 Hz, mixes to -14 LUFS / -1 dBTP, and writes a no-music copy too.
- Sound never fights the voice. Music only when the style or the user wants it. Never add copyrighted trending songs: the no-music copy is for adding those inside Instagram or TikTok.

## Stage 8: Quality check

Follow `references/quality-check.md` on every render before you show it: a contact sheet, a still at the middle of every beat, the first and last frames, a loudness measure, and a spot check of caption timing. Fix what you find and re-render; tell the user in one line what you fixed.

Then show the preview and take changes in plain words ("captions bigger", "zoom when I say insane", "the cut at 0:14 is too sudden"). Times they point at are on the edited video. If they say "add that to my style", update `my-video-style` (see `/video-editor:style`).

## Stage 9: Deliver

Render the final at full quality and export to `exports/` (or where the engine puts it, for example Downloads for awa). Then tell them, briefly:
- where the files are, length, size and shape, and the version number
- the no-music copy and what it's for
- the music credit line if the track needs one (awa prints it)
- which tools and Brand Nat codes you used, and anything you were unsure about
- one line: watch it before posting

Offer in one line each: another shape (for example 16:9 with a blurred fill), shorts from it (`/video-editor:clips`), a MultiCam shot prompt, a post caption with a comment-keyword CTA, or saving new preferences to their style. Never post or upload anything.

## Voiceover mode: motion-graphics videos from a script

For explainers, tool round-ups, ads and faceless reels: no camera footage, an AI voice, and a fully animated HyperFrames video timed to every word. It also adds a voiceover to footage that has none (screen recordings, b-roll).

**1. Script.** Take their script, or write one from their topic in their voice (a style preset's script shape, for example Nick style's "top 5 … right now / the first is … / comment KEYWORD"). Length: about 150 words a minute for a calm read, 200 to 220 for a fast reel. Short sentences, numbers written the way they should be read. Show the script and wait for an OK.

**2. Voice.** Pick the provider with them (one line each). For reels, voice it line by line: put one spoken line per row in `work/NAME-lines.txt` (every list item on its own row) and run `python3 scripts/voice_lines.py work/NAME-lines.txt work --name NAME --pace brisk --provider <p> --voice <id>`. It voices each line, lays them out with natural breaths, keeps every line on screen long enough to read, and writes one voice track with word timings. Paces: `normal`, `brisk` (default, about 1.2x and readable), `fast` (packed). `--min-hold "2:2.3"` gives a line with an animated card more time. For one continuous read (an explainer), use `python3 scripts/voiceover.py work/NAME-script.txt work --name NAME --provider <p> --voice <id>` instead. The providers:

| Provider | Cost | Quality | Needs | Word timings |
|---|---|---|---|---|
| `elevenlabs` | paid plans; the free plan needs a credit line and isn't for commercial use | most natural, voice cloning, reads Hindi and Hinglish (`eleven_multilingual_v2`) | `ELEVENLABS_API_KEY` | exact, from the API |
| `gemini` (Google) | free key from Google AI Studio, with free-tier limits | very natural, directed delivery (`style`) | `GEMINI_API_KEY` | by transcription |
| `heygen` | free with a HyperFrames sign-in | natural | `npx hyperframes auth login` | exact |
| `kokoro` | free, offline, commercial use OK | good, clearly synthetic in places | one-time setup (ask first): `python3.12 -m venv ~/.local/share/hyperframes-venv && ~/.local/share/hyperframes-venv/bin/pip install kokoro-onnx soundfile` (`voiceover.py` uses that venv automatically; Python 3.15 isn't supported yet), then a ~340 MB model on first use | by transcription |

- API keys live only in the user's environment (`export ELEVENLABS_API_KEY=...` in `~/.zshrc`, added by them). Never ask for a key in the chat, never write one into a file, and never fall back to another voice silently when a key is missing: say what's missing and stop.
- `--list-voices` shows the voices for `elevenlabs` and `kokoro`. Let them pick by name; offer two or three that fit the video.
- Listen check: duration close to the plan, names and numbers read right, no clipped words. Regenerate the whole read after any script change (timings come from the read). Run `scripts/check_words.py` on transcribed timings.
- The output (`NAME-voice.*`, `NAME-voice-words.json`) replaces the transcript from stage 2: every visual is timed to these words.

**3. Storyboard.** As stage 5, one row per sentence or beat, at the same pace rules. With no face on screen the visuals carry everything: kinetic type on key words, real logos and screenshots of every product named, UI recreations labelled as such, charts for numbers, icons, and optional AI b-roll (generated only after they approve the list and its credits). Read `/hyperframes` and its `references/types/explainer.md` (or `vertical.md` for reels) before planning.

**4. Build (engine C).** Put the voice in the composition as an `<audio id="vo">` from 0, drive every entrance from the word times, and build captions from the same words (or, in kinetic-promo style, make the spoken words themselves the big on-screen type). Start from `examples/kinetic-promo/build.py` when the look fits: keep its helpers (word slams, labels, zoom-through, punch-ins, grid) and rewrite the scenes for the new script. Lint, snapshot every beat, render. A style preset applies here too (Nick style without the face card: the split card becomes full-height cards).

**5. Sound and delivery.** As stages 7 to 9: `scripts/sound_mix.py` on the render (the voice is the video's audio, so music ducks under it) with a cue per visual beat, -14 LUFS. Deliver the video, the no-music copy, and the voice file on its own. Name the voice provider in the delivery note, and the credit line when the plan needs one (ElevenLabs free plan).

## Honest limits

- Each engine has its own limits (awa: clips up to 60 s and 30 fps; effects: 30 fps, starter versions, need one clearly visible face, so not on crowd shots; recorded b-roll: logged-out pages only). Say so when it matters.
- Brand Nat codes marked ≈ in `references/beat-map.md` are close builds, not exact copies.
- If something fails twice, read the failing skill's troubleshooting notes, then tell the user plainly what broke and what you'll try next.
