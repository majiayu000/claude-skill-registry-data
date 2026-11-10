---
name: explainer-kit
description: Explainer Kit - the support layer the talking-explainer skill runs on - machine setup check, the user's brand + voice profile, voiceover transcription to word timings, audio mastering, the corner-logo overlay, sync check, seam diffs and the tools that turn a character image into a talking mascot. Use it through talking-explainer; use it directly only for its setup ("set up my explainer profile", "run the explainer setup check") or one of its tools by name.
---

# Explainer Kit

Shared tools for the talking-explainer skill. It is not a film recipe on its own - the film phases live in
talking-explainer's SKILL.md.

Paths used below:
- `<skill>` = this skill's folder. `<engine>` = `<skill>/../spatial-film`.
- `<home>` = `TALKING_EXPLAINER_HOME` or `~/.talking-explainer`. Profile = `<home>/profile/`.
- `<py>` = the `python` command saved in `<home>/config.json` by setup-check (e.g. `py -3.12` on Windows,
  `python3` on macOS).

Run every film script from the film project root. Scripts are proven code - run them, never regenerate them.

## Phase S - Setup (first run only, skip when `<home>/profile/brand.json` exists)

1. `node <skill>/scripts/setup-check.mjs` - fix every MISSING line with the install command it prints, rerun
   until it exits 0. Tell the user plainly what to install; do not install system tools without asking. Its
   YOUR INPUTS block lists what only the user can bring (TODO / ASK / OPTIONAL) - steps 2-5 fill those.
2. Brand interview, one message (include the voiceover question: ElevenLabs voice clone on a paid plan, or
   recording themselves with a decent mic in a quiet room - no route = stop and tell them they need one), then
   `node <skill>/scripts/profile.mjs init --name "<brand>" ...` (flags: `--wordmark "Part1,Part2" --logo <file>
   --logo-has-text --ink #hex --accent #hex --opener "explains" --cta "Follow for more" --presenter "<mascot name>"
   --language "<language>" --films-dir <dir>`). A PNG logo goes through
   `<py> <skill>/scripts/prep-logo.py <logo> <home>/profile` first. No logo = wordmark only.
3. Voice: fill `<home>/profile/voice.md` (the template explains both ways) - 5-question interview, or
   `<py> <skill>/scripts/speech-profile.py` on the transcript of a 5+ minute unscripted recording of them talking.
4. Presenter: the bundled talking demo, or their own talking character (talking-explainer's "Your own talking
   character" section).
5. Music (optional): their own licensed bed at `<home>/profile/music/bed.mp3`. Otherwise the HeyGen catalog
   (`npx hyperframes auth login` once, then `node <engine>/scripts/music-search.mjs "<mood>"`) or no bed.

`node <skill>/scripts/profile.mjs show` prints the merged profile at any time.

## Files

| Path | What |
|---|---|
| `scripts/setup-check.mjs` | Checks every tool, saves the Python command, prints install commands for what is missing. |
| `scripts/profile.mjs` | `init` / `show` / `path` for the user's brand profile. |
| `scripts/new-explainer.mjs` | Base scaffold (engine skeleton + kit + brand + SFX + audio). talking-explainer's scaffold calls it - do not run it on its own. |
| `scripts/prep-logo.py`, `scripts/build-brand.py` | Logo cleanup; the corner-logo overlay (`m-brand`) timed from film.json. |
| `scripts/prep-mascot.py` | Normalise a character's pose PNGs, write the manifest, fit blinks when faces exist. |
| `scripts/transcribe.py`, `scripts/words.py` | faster-whisper word timings; print every word with its start time (the storyboard's cue sheet). |
| `scripts/master-audio.py` | Voice loudnorm + sidechain-ducked bed + loudness report. |
| `scripts/sync-check.py`, `scripts/seam-diff-all.mjs` | Render audio vs source word timings; seam diffs with the presenter box masked. |
| `scripts/speech-profile.py` | Measure a speaker's style from a long unscripted recording's transcript. |
| `scripts/cut-sheet.py`, `scripts/mouth-fit.py`, `references/mascot-sheet-prompt.md` | A TALKING character from 3 image prompts: cut the sheets into sprites, fit 6 mouth shapes per pose. |
| `references/voice-script.md` | How to write a script in the speaker's voice (loaded in talking-explainer phase 1). |
| `assets/brand/` | Montserrat 700 + OFL (logo font). The user's logo is copied in per film; SFX come from HyperFrames' `media-use` skill. |
| `template/` | Base kit.css, frame.md, snippets, scene-starter, worker brief, presenter track - talking-explainer layers its Apple look on top. |
| `template/profile/` | Sample profile: brand.example.json, logo.svg, voice.example.md. |

## Hard rules

1. **The speaker's voice is untouchable** - only loudness mastering; the visuals move to the words, never the reverse.
2. **Music must be theirs to use** - their own licensed file, the HeyGen catalog, or none. Never pull a track off
   YouTube or a random site.
3. **Sync check** = transcribe the RENDERED mp4, then `sync-check.py` against the source timings. That is the proof
   the picture lands on the words - never claim it from reasoning.
4. renders/, .media/, .hyperframes/ and audio files stay out of git.

## When things go wrong

| Symptom | Cause | Fix |
|---|---|---|
| A script says "run setup-check first" | no `<home>/config.json` | `node <skill>/scripts/setup-check.mjs` |
| `prep-mascot.py` needed | custom mascot folder without manifest.json | `<py> <skill>/scripts/prep-mascot.py <home>/profile/mascot` |
| Voice clips after a gain lift | plain gain on a hot take | `master-audio.py` (loudnorm), never plain gain |
| `build-presenter.py` dies in ffmpeg on `vo-master.wav` | audio not mastered yet | run `master-audio.py` first |
| seam-check FAILs ~1% on every cut | the presenter moves across seams | `seam-diff-all.mjs`: 0.00% outside the box = pass |
| Render is ~15x slower than expected | no GPU / software path | render-final prints the gpu mode; close other GPU apps or accept the wait |
