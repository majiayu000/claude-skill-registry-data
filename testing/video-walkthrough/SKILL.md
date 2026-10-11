---
name: video-walkthrough
description: >-
  Record a video walkthrough of a user scenario via Playwright: a Gherkin
  test scenario is replayed in a browser, every step is captioned as a
  subtitle, and the output is an mp4 (+ .srt) plus optional clean before/after
  screenshots of every step. One artifact serves both as proof the feature is
  tested and as video documentation. Use when asked to "record a walkthrough
  video", "make a video guide for a feature", "add a walkthrough to US-XX",
  "capture a demo of the scenario" — или по-русски: «записать видео
  прохождения», «сделать видео-инструкцию по фиче», «добавить walkthrough к
  US-XX», «снять демо сценария», «сделать скрины прохода».
---

# Video walkthroughs via Playwright

Turns one Gherkin scenario into a **test + video walkthrough**. The same
scenario that verifies the feature is recorded in a browser with slowMo and
per-step subtitles.

Communicate with the user in their language. The language of the artifacts
(subtitles, narration, screenshot names) follows the language of the scenario
steps, not the language of this document.

## When to apply
- A feature is done → the client needs a "how it works" video.
- Proof is needed that the user path is tested.
- You want living UI documentation that cannot silently rot (if the test
  breaks, the video does not build).

## Principles (do not violate)
1. **The video is a by-product of the test, not a separate procedure.** The
   scenario is written anyway; recording is attached via a flag.
2. **Verification is assertions only (`expect`).** Never "watch" recorded
   video frames multimodally — token-expensive and pointless. Video is for
   humans, assertions are for machines. The exception is not about
   verification: viewing PNGs from `screens/` as a separate, explicitly
   requested UX/UI-analysis task (see "Walkthrough screenshots").
3. **Stable selectors (`data-testid`)**, not fragile paths — otherwise
   debugging eats tokens.
4. **Isolated data (seed)** via a dedicated backend/fixture — real data is
   never touched, `id`s/state are deterministic.
5. **Test stand on dedicated ports** — never conflict with the developer's
   working server.

## One-time project setup
1. Create a `qa/` directory, copy into it **only the `.ts` files from `lib/`**
   (caption, click-marker, record, fixtures, steps, screens — specs import
   them by relative path, so they must live in the project), plus
   `playwright.config.ts` and `package.json`. The Python narration
   (`narrate.py`, `accents.json`, `add-accent.py`) is **not vendored** — the
   `video:voice*` scripts call it from the global install
   (`~/.claude/skills/video-walkthrough/`); the dictionary is global too, and
   project-specific vocabulary goes into `qa/lib/accents.json` (overrides the
   global one, see "Narration").
2. `cd qa && npm install && npx playwright install chromium`. For narration —
   once: `npm run setup` (voice stack into the global venv).
3. Configure `webServer` in the config: start the app (front+back) on
   **dedicated ports** with seed data; `reuseExistingServer: false` for
   determinism.
4. Add ~5 `data-testid`s to the key nodes of the scenario (buttons, cards,
   inputs, list rows). Text/role selectors where they are stable.
5. Create a seed fixture (minimal deterministic data) and a `globalSetup`
   that resets the mutable layer before each run.

## Authoring a scenario (per feature)
1. Create a file pair named `US-XX-<slug>` in `qa/scenarios/`:
   - `.feature` — human-readable Gherkin (source of truth);
   - `.spec.ts` — executable scenario, steps mirror the `.feature` verbatim.
   **File name = video name** (`qa/videos/US-XX-<slug>.mp4`).
2. Write steps through the wrapper `step(cap, 'step text', async () => { … })`:
   text = Gherkin line = report heading = video subtitle.
3. Actions — via helpers (`openApp`, `dragSelect`, clicks by `getByTestId`).
   Checks — `expect(...)`.
4. Rules learned in practice (follow them):
   - **Navigate (`page.goto`) in the first step** — so the screen is never
     blank; the subtitle bar survives navigation (restored on `load`).
   - **Never "watch" the video to verify** — assertions only.
   - **≥2 meaningful elements** where the UI needs a range (e.g. word
     selection).
5. **Scenario language = artifact language.** Write steps in the user's
   language: Russian steps produce Russian subtitles and narration, English
   steps produce English ones. References: `scenarios/example.spec.ts` (ru),
   `scenarios/example-en.spec.ts` (en).

## Running and delivering
1. First fast, without recording — verify the logic:
   `npm test`  (→ `playwright test --project=fast`)
2. Then with recording:
   `npm run video`  (→ `--project=video`: slowMo + subtitles + mp4)
   Option to burn subtitles into frames: `npm run video:burn` (`BURN_SUBS=1`).
3. Optionally narrate the subtitles (see "Narration"):
   `npm run video:voice` — Silero (offline); `npm run video:voice:hq` — edge
   Optionally collect the walkthrough screenshot bank: `npm run screens`
   (see "Walkthrough screenshots").
4. Deliver `qa/videos/US-XX-<slug>.mp4`. It goes into git as documentation:
   one feature = one stable file, a re-run overwrites it (git keeps history).
   Heavy/numerous videos → git-LFS (`*.mp4 filter=lfs`).

## Narration (optional)
`npm run video:voice` (→ `python3 lib/narrate.py videos`) synthesizes speech
from the `.srt` and mixes it into the mp4 with per-cue offsets (ffmpeg
`adelay`).
- Works **post-factum on a finished mp4+srt pair** — old videos can be
  narrated without re-running the test; the audio track is replaced entirely,
  re-running is idempotent.
- **Language** (`--lang auto|ru|en`, default auto): detected per video from
  its subtitles — more Cyrillic → Russian, otherwise English. For English the
  Russian pipeline (RUAccent, accents.json, runorm) is skipped entirely;
  voices: silero `en_0`, edge `en-US-AriaNeural`, say `Samantha`.
- Engines (`--engine auto|silero|edge|say`). Default is Silero (`xenia`):
  offline, deterministic. **"High-quality narration"** — `npm run
  video:voice:hq` (`--engine edge`, Microsoft neural voice `Svetlana`):
  lively intonation out of the box, reads Latin script and numbers by itself;
  needs internet, unofficial API. `say` — emergency fallback, zero install.
  `auto` picks Silero: torch is looked up in the current interpreter, then the
  script re-executes itself in the skill venv
  (`~/.claude/skills/video-walkthrough/.venv`); if absent — falls back to say.
  The venv is created once: `python3 -m venv
  ~/.claude/skills/video-walkthrough/.venv && …/.venv/bin/pip install torch
  omegaconf numpy ruaccent "transformers<5" num2words runorm` (models download
  to cache on first synthesis).
- **Stress marks and terms (Russian narration).** Subtitles stay clean;
  before synthesis the text passes a preprocessor (`speech_text`): RUAccent
  places stress marks (`+` before the vowel, homographs by context), numbers
  are spelled out, and the `lib/accents.json` dictionary defines Cyrillic
  pronunciation of terms (`"Whisper": "у+испер"`). Silero **silently drops
  Latin script and digits** — the script warns about terms without a
  pronunciation: add them to accents.json and re-run. Dictionary replacements
  are protected from RUAccent (it erases foreign `+` marks).
  The project-level `./lib/accents.json` (relative to the run directory,
  usually `qa/lib/`) overrides the global one — put project vocabulary there;
  `narrate.py` itself is still called from the global install.
  Unknown Latin script is backstopped by runorm (per-token transliteration,
  `ℹ` mark in the output) — the word will sound, but for exact pronunciation
  still add a dictionary entry; `⚠` remains for cases where even runorm
  failed.
- **Dictionary maintenance — the working loop (Russian).**
  1. Run narration → the output shows `⚠ латиница без произношения` → add
     entries and re-run; stop only when there are zero warnings.
  2. The user heard a mispronounced word (typical case — Anglicisms in
     Cyrillic where «е» is read soft: тег→т+эг, флеш→фл+эш) → add an entry
     and re-narrate **only the affected videos**:
     `grep -l слово qa/videos/*.srt`.
  3. Replacement matches whole words, so a Russian key needs all word forms.
     Do not list them by hand — generate from the word-form base
     (danakt/russian-words, 1.5M words, at `lib/russian-words.txt` of the
     global skill): `python3 lib/add-accent.py плеер пл+эер --apply` — finds
     cases and compounds («видеоплеером», «медиаплееры»). **First run without
     `--apply` and review the candidates**: short roots give false matches
     («тег» → «стегать», «стратег») — use `--no-compounds` and/or
     `--exclude`. If the base is missing (another machine) — the script
     prints the download command.
  4. Common terms (Enter, PDF, тег…) go into the global dictionary
     `~/.claude/skills/video-walkthrough/lib/accents.json`, project vocabulary
     (product and file names) — into the local `qa/lib/accents.json`.
  Check pronunciation without recording: `speech_text('фраза')` from
  narrate.py.
- **Expressiveness (silero).** Punctuation pauses (dash, colon) are inserted
  by SSML automatically. Semantic emphasis — a `<video>.speech.json` sidecar
  next to the srt: `{"subtitle text": {"emphasis": ["keyword"]}}` — the
  keyword is read slightly slower with micro-pauses (emulating emphasis,
  which Silero lacks). Fill in while authoring: one emphasis per phrase — the
  object of the action or the result of the step; the key equals the subtitle
  text verbatim.
- A phrase that does not fit its 5-second slot is sped up (`atempo`, up to
  x2); if it still does not fit — the script warns: raise `STEP_HOLD_MS` and
  re-record the video.
- Spends no tokens — pure code execution.

## Walkthrough screenshots (optional)
`npm run screens` (→ `SCREENS=1 playwright test --project=fast`) replays the
same scenarios and saves **clean** frames of every step into
`qa/screens/<scenario>/`: `NN-before-…png` / `NN-after-…png` pairs — the UI
state before and after the action, names derived from step texts. This is a
screenshot bank for UX/UI analysis of the product.
- **Frames are clean**: in fast mode the subtitle bar and click marker are not
  drawn — the screenshots show the honest UI without recording overlays. The
  "before" frame of the first step is skipped (the page is blank before
  navigation).
- **Rewrite semantics as for videos**: a run wipes the scenario folder and
  writes a fresh set; names are deterministic (no timestamps), git keeps
  history.
- **The skill only collects frames; analysis is a separate task.** The run
  itself spends no tokens (pure code execution). View the PNGs multimodally
  only when the user explicitly asked for a UX/UI review; the bank works as
  input for the `feature-ux-analyze` skill (the "competitor" = your own
  product).
- No spec changes needed: the same `step()` wrapper does the capturing.

## Readability settings
- A subtitle stays on screen at least **5 s** per step (`STEP_HOLD_MS`,
  default 5000). Fast steps are stretched to the minimum. Change:
  `STEP_HOLD_MS=7000 npm run video`.
- `slowMo` (in the config, ~300 ms) makes individual actions visible.
- Clicks are highlighted with an expanding ring at the pointer
  (`click-marker.ts`, `video` mode only) — the viewer sees where the scenario
  clicked. Works by itself, baked into the frame like the subtitles.

## Token cost
- One-time infrastructure setup: noticeable, but once.
- New feature: +little on top of the usual test (the scenario is written
  anyway).
- Recording/conversion — code execution, ~0 tokens.
- ❌ Multimodal analysis of recorded video frames — **never** (200k+ tokens
  per video, pointless: assertions verify). Viewing PNGs from `screens/` —
  only on an explicit UX/UI-analysis request, not for verification.

## Reference
See `scenarios/example.spec.ts` + `.feature` (Russian) and
`scenarios/example-en.spec.ts` + `.feature` (English) in this repository as
templates to copy. The library lives in `lib/` (`caption.ts`, `record.ts`,
`fixtures.ts`, `steps.ts`, `screens.ts`).
