---
name: localize
description: Run the ad-localization job on the ads in input/ (or on the sample with "/localize example"). Drafts every ad for each market in config/, checks lengths, names and numbers, runs a blind back-translation, re-sets the text in image ads, dubs video ads with a stock voice after asking, and builds a review kit. Use when the user types /localize.
argument-hint: "[example] [language codes, e.g. fr,es]"
disable-model-invocation: true
allowed-tools: Edit(./output/**) Edit(./config/markets.json) Bash(python3 scripts/job.py *) Bash(python3 scripts/blind.py *) Bash(python3 scripts/kit.py *) Bash(python3 scripts/video.py *) Bash(python3 scripts/reset_image_text.py *) Bash(python3 scripts/phone_check.py *) Bash(python3 scripts/voice.py account) Bash(python3 scripts/voice.py voices *)
---

# /localize: from English ads to a review kit

Arguments: `$ARGUMENTS`. If they include `example`, add `--example` to the config and prepare commands (sample
company and ads from `examples/`). Language codes (for example `fr,es`) go to `--languages`.

Follow `CLAUDE.md` throughout: the AI-draft label everywhere, nothing uploaded, ask before every paid step, stock
voices only, the key never in the chat, blind back-translation stays blind, a fresh computer (only the kit's own
tools), dashboards left in their language. Run every command exactly as written here, from this folder, without
`cd`. Tell the person what you are doing in one short line per step.

## 0. Getting the ads in (when the person pastes ad-library links)

Ad libraries make poor sources. LinkedIn's Ad Library blocks simple downloads, and the file it plays is LinkedIn's own
re-saved copy, often bigger than the advertiser's upload and not the original. Google's Ads Transparency Center
shows one combination of a responsive search ad, cuts long descriptions with "...", and hides text inside frames.
So recommend the manual route in `input/README.md`: the person saves the media from their own files or ad account,
pastes the text into the CSV, and puts each ad's link in the `source` column. For Google search ads, export the
assets from the Google Ads account. If you do fetch a file for them, list every version on offer with its size and
ask before downloading, quoting the size of the one you will take. A browser extension is optional; never depend on it.

## 1. Start the run

```
python3 scripts/job.py config            (add --example for the sample)
python3 scripts/job.py prepare           (add --example, and --languages fr,es if given)
```

If config is not ready, say so and suggest `/setup`. Prepare prints the run folder, called RUN below
(for example `output/2026-10-20-0930`), and lists the images and videos it found. If it warns that a text ends in
"...", ask the person for the full text before translating; never translate half a sentence. A GIF with one
picture counts as an image; an animated GIF counts as a video with no sound, and its draft comes out as an MP4.

Read the company files now: `config/company.md`, `config/markets.json`, `config/glossary.md`
(for the sample: the same names under `examples/config/`).

## 2. Read the text inside images and videos (skip if there are none)

**Images** (needs a Mac, plus Pillow and NumPy). For each image NAME.png in the input folder:

1. `python3 scripts/reset_image_text.py detect INPUT/NAME.png RUN/images/NAME.boxes.json`
   (INPUT is `input`, or `examples/input` for the sample. If `config/fonts.txt` exists, add `--fonts config/fonts.txt`
   at the end.) It finds each block of text and measures its box, color, font and size.
2. Look at the image and at `RUN/images/NAME.boxes.json`. Every block starts as `"action": "review"`. Set ad copy to
   `"replace"`. Set `"preserve"` for logos, names under "Never translate" when the block holds nothing else,
   product screenshots, and any text sitting on a photo. Fix OCR misreads in `source_text`. If a block is set in
   capitals, add `"transform": "upper"`. If `company.md` says which font each kind of text uses, check each
   block's `font` against it and change it to that font's file when the match picked another. A label in a button
   has a `shape` and `"align": "center"`: it stays centered in the button.
3. For each `replace` block add an item to `RUN/media-text.json`, with the block id:

```json
{"items": [
  {"id": "NAME.b3", "file": "NAME.png", "surface": "image", "text": "Stop sorting site photos at your desk.", "block": "b3"}
]}
```

**Videos** (an animated GIF is a video too). For each one run `python3 scripts/video.py prepare RUN input/NAME.mp4`
(for the sample: `examples/input/NAME.mp4`). It saves the audio, a frame every 2 seconds in
`RUN/video/NAME/frames/`, a sheet of 12 frames (`frames/sheet.jpg`) and the transcript if `NAME.transcript.txt`
sits next to the video. If the frames show a lot of English text on screen, run the same command again with
`--every 0.5`: reading those frames makes the times and boxes below much easier to set.

- **Voice-over, or only music?** Ask early, unless prepare already says "no sound". Show the frame sheet if it
  helps. Do not try to detect speech with a tool on this computer. If the person is not sure, offer the paid
  transcription (estimate first) as below.
- **Music only:** run prepare again with `--music-only`. There is nothing to transcribe, separate, record or dub,
  so nothing is paid: add no `spoken` item and go straight to the text on screen. The kit labels it
  "Voice: none (music only)".
- **Voice-over without a transcript?** Ask the person: add `NAME.transcript.txt` themselves (free), or pay for
  transcription. For the paid route run `python3 scripts/voice.py transcribe RUN --video NAME`, show the
  estimate, and only after a yes run it again with `--confirm`.
- Add the voice-over as one item: `{"id": "NAME.script", "file": "NAME.mp4", "surface": "spoken", "text": "<transcript>"}`.
- **Text on screen.** Look at the frames. For each piece of English text add one item with its kind, when it shows
  and where:
  `{"id": "NAME.s1", "file": "NAME.mp4", "surface": "screen", "kind": "title", "text": "Introducing Field Mode", "start": 9.5, "end": 12.2, "box": [246, 332, 756, 78], "frame": 11.0}`.
  `text` is the whole text once it is complete (all its lines). `start` is the last frame before it appears and
  `end` the first frame after it is gone, so the window covers its whole entrance and exit. `frame` is a time
  where it is fully shown, fully opaque and not moving; `box` is where it sits then, in the video's pixels, around
  all its lines. Add `"align"` (`left`, `center`, `right`) when the lines share an edge.

  `kind` decides what happens:
  - `title`: a headline or caption ("Introducing Field Mode"). Translated.
  - `callout`: a floating card or label laid over the product ("Inspection saved · 3 photos"). Translated, keeping
    names, IDs and numbers as written.
  - `ui-small`: a small interface element: a typed prompt box, a chip, a toast ("Show me last week's
    inspections"). Translated.
  - `dashboard`: a data-dense product screen: tables, charts, forms, the full app. Never translated.
  - `logo`: a logo or a line made only of names under "Never translate". Never translated.
  - `footage`: text that is part of filmed footage (a street sign). Never translated.
  Record the never-translated kinds too, so the kit shows they were seen and left on purpose.

  How the text is redrawn: one line on a plain background follows its zoom, typing and fade. A block of several
  lines, or text over a gradient or picture, is followed as it slides and fades; a block that zooms or turns is
  flagged and left in English. If `company.md` names the fonts, set `"font"` on the item (a file name such as
  `"Avenir Next.ttc#7"`, or a path from `config/fonts.txt`). When some words are in a highlight style (bold italic,
  another colour), set `"highlight_font"` too. To pick a font by eye after a first `screen` run, draw the closest
  fonts next to the original: `python3 scripts/reset_image_text.py fonts RUN/video/NAME/CODE/screen/ITEM/fNNNNN.png
  RUN/video/NAME/CODE/screen/ITEM.boxes.json RUN/video/NAME/ITEM.fonts.png` (fNNNNN is the item's `frame` as a
  frame number), look at the sheet and pin the best one. If a logo sits inside a line of text, add its box to `"keep_boxes": [[x, y, w, h]]`
  so it is not erased.

Then refresh the lines: `python3 scripts/job.py prepare RUN`. Text in images and on screen now shows about how
many characters fit its box (`limit.recommended`).

## 3. Translate (you, in this session)

Read `RUN/lines.json`. Each line has `line_id`, `language`, `text`, the platform and field, its `limit` and the
`names` that must stay unchanged. Write `RUN/drafts.json` following "How to translate" in `CLAUDE.md`: one
entry per line and language, a short version with a note whenever the full one is over a limit. For text on
screen set over several lines, add `"lines"` with the line breaks and `*highlights*` (look at the frame for which
words are highlighted). For many lines, work one language at a time.

## 4. Check, back-translate, judge meaning

```
python3 scripts/job.py check RUN
python3 scripts/blind.py RUN
```

Fix every error the check reports (missing lines, changed names) and run it again until it shows 0 errors.
A "fail" (over the platform limit) with a short version that fits is fine; without one, write a short version
or explain in `review_note` why nothing faithful fits.

Then read `RUN/back-translations.json` and write `RUN/meaning.json` as described in `CLAUDE.md`. If a version
changed meaning by mistake, fix the draft, then run `check` and `blind.py` again (it only sends what changed)
and update `meaning.json`. Do at most two repair rounds; after that, leave the flag for the person.

## 5. Image ads

For each image and language:

```
python3 scripts/job.py words RUN NAME CODE
python3 scripts/reset_image_text.py apply INPUT/NAME.png RUN/images/NAME.boxes.json RUN/images/NAME.CODE.words.json RUN/images/NAME.CODE.png
```

The first command writes the checked translation for each block (and the short version as a fallback); it
refuses while the drafts have check errors. The tool erases the English and sets the translation in the same box,
same font, color and alignment, shrinking the type to 85% at most. Text that still doesn't fit is **flagged, not
squashed**: tell the person which line, and offer a shorter wording (new short version, then check, blind and
meaning again, then `words` and `apply` again; earlier images move to `RUN/images/old/`). Look at every output
image yourself before moving on.

## 6. Video ads (paid: ask first)

For each video and language:

1. **Voice.** If `voice_id` is empty for this language in `config/markets.json`, run
   `python3 scripts/voice.py voices --language CODE`, offer three or four voices that suit the ad (name, accent,
   preview link) and let the person choose. Save the chosen `voice_id` in `config/markets.json`.
2. **Separate the music** once per video: `python3 scripts/voice.py stems RUN --video NAME`. It prints an
   estimate and stops. Ask: "This uses about N ElevenLabs credits (you have M left). Go ahead?" Only after a yes,
   run the same command with `--confirm`.
3. **Record the voice**: `python3 scripts/voice.py speak RUN --video NAME --language CODE` (add `--short` to
   record the short version). Same pattern: estimate, ask, `--confirm` after a yes.
4. **Mix**: `python3 scripts/video.py dub RUN --video NAME --language CODE`. Each translated sentence is laid
   where the English sentence starts (found from the pauses in the separated English voice), over the original
   music at its original level, and the sound is cut to the picture. Read `alignment` and `sentences_moved_late`
   in what it prints. If it says the voice is too long, record the short version (or write one, check and
   back-translate it first), then mix again. If it says a sentence would be cut mid-sound, record again with
   `voice.py speak` (it records one clip per sentence, so every cut falls in silence).
5. **Text on screen**: `python3 scripts/video.py screen RUN --video NAME --language CODE` when the video has
   on-screen text items (for a music-only video this is the only step). Every frame the English shows in is
   redrawn in the translation, and the changed frames are read back for leftover English. Look at the frames it
   changed (`RUN/video/NAME/CODE/screen/<item>/out/`): the first, a moving or fading frame, a held frame and the
   last, next to the same frames of the original. If a render is wrong (half-replaced text, a visible patch, a
   wrong colour), set it aside so the kit never shows it as a draft:
   `python3 scripts/video.py reject RUN --video NAME --language CODE --reason "what is wrong"`.

If the person says no to spending, skip the dub; the kit still shows the translated script.

## 7. Build the kit and hand it over

```
python3 scripts/kit.py RUN
python3 scripts/phone_check.py RUN
```

The second command shows every page at phone width (`RUN/checks/phone.html`); with Chrome installed it also lists
anything too wide and saves `RUN/checks/phone.png`. Look at it. Without Chrome, open the page yourself or say
that you did not check phones.

Then tell the person, briefly:
- where the kit is: `RUN/kit/index.html` (one page per language, plus a CSV per language for copying text)
- per language: lines that fit as drafted, lines that need the short version, lines where nothing fits yet,
  and lines to check (meaning changed or longer than recommended)
- ElevenLabs credits used, if any
- what was not checked: native-speaker review, the ad platform's preview, how images and video look to a person
- that everything is an AI draft, not yet reviewed by a native speaker, and nothing was uploaded
