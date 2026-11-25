---
name: vlog-edit
description: Edit raw selfie or talking-head footage into a captioned 9:16 short with a hook, full-frame data cards, a map, a picked-from-a-list moment, b-roll cutaways and an outro, then check the render with automated judges before anyone watches it. Use when someone hands you phone clips, a vlog, or talking-head takes and wants a Reel, TikTok or Short. Not for generating video from nothing or captioning a finished edit.
---

# vlog-edit

Turn phone footage into a short that looks produced: every cut lands in a pause, captions sit in
one band on every shot, graphics fill the frame and build while he talks, and the judges check
the file before you hand it over.

The engine is `scripts/vlog.py` (Python, ffmpeg, Pillow, numpy, faster-whisper). You author one
file, `EDIT.json`, and everything in it is keyed to **words**, never to seconds you typed.

## Setup (once)

```bash
pip install -r scripts/requirements.txt      # faster-whisper, pillow, numpy
python3 scripts/vlog.py setup                # fetches Inter Display (SIL OFL) to ~/.cache/vlog-edit
```
Needs `ffmpeg` and `ffprobe` on PATH (or set `VLOG_EDIT_FFMPEG` / `VLOG_EDIT_FFPROBE`).

## Workflow

1. **Transcribe.** Write an `EDIT.json` with only `name` and `clips`, then:
   ```bash
   python3 scripts/vlog.py transcribe EDIT.json
   ```
   It prints every word with its index and marks real pauses as `|0.6s|`. Word edges are refined
   with a voice-activity detector, because Whisper closes every pause into the word before it.
   Read the whole transcript before deciding anything. Check the detected language: do not set
   `language` unless you are sure, because forcing English on German speech silently translates.
   Accented English is often transcribed as the speaker's first language; when the speaker says
   what they said, use `fix`, and leave out any stretch you cannot transcribe with confidence.
   `transcribe` re-hears every sentence on its own and prints `DISPUTED` where the two passes
   disagree. The sentence-on-its-own reading is usually right; if a disputed line changes the
   meaning ("it works" / "it doesn't work") and you still cannot tell, cut the line.

2. **Find the story.** Pick `keep` ranges by word index. Drop retakes, false starts and filler;
   keep the best take of each line. Pauses longer than `tighten` (0.35 s) are cut down
   automatically, so do not fight the pacing by hand.

3. **Write the hook.** One line, the reason to keep watching, in the speaker's own framing. It
   covers the first ~2 s and is the thumbnail, so captions wait until it has faded.

4. **Plan the visuals.** At most one visual per sentence, in this order of preference:
   - a **card** when the words name a number, a place, a choice or a prompt
     (`stat`, `map`, `list` with a `pick`, `prompt`);
   - a **b-roll** cutaway from another clip when the words describe what is around him;
   - otherwise stay on his face. A face is not a gap to fill.
   Each visual gets `at` and `until` word references. See `references/edit-json.md`.

5. **Source every figure.** A `stat` refuses to render without `source`. Put on screen only what
   you can cite; if the date or scope of a figure is uncertain, leave it out of the copy rather
   than guessing (say "2026 count", not a month you inferred).

6. **Speech in another language?** Captions stay exactly what was said, in that language, and a
   `subtitles` line underneath carries a faithful translation per sentence. Skip the line when
   the sentence is already in the viewer's language.

7. **Fix the ASR, pick caption keys.** `fix` replaces misheard words ("for your eye" -> "for AI.").
   `captions.keys` are the one or two words per line that carry the meaning; they get the accent
   box. Brand and product names spelled right.

8. **Render and judge.**
   ```bash
   python3 scripts/vlog.py render EDIT.json
   python3 scripts/vlog.py qa EDIT.json
   ```
   `qa` exits 1 on any finding. Fix the cause and re-render; do not tune a threshold to pass.
   Then **look at the contact sheet** (`renders/<name>.contact.jpg`). The judges catch broken
   cuts, not bad taste.

9. **Deliver** the mp4, the one-line judge summary, and anything you left out and why.

## What the judges check (`references/judges.md`)

| judge | fails on |
|---|---|
| cut | GHOST (a dissolve: both pictures at once), FLASH (a shot under 0.4 s), STROBE, FROZEN and CREEP (a card that stops moving), OFFBEAT (a cut inside a word) |
| picture | wrong size, black frames, length off the plan |
| loudness | integrated loudness more than 1 LU off target (-14 LUFS), peak at the ceiling |
| voice over music | the ducked bed within 10 dB of the voice under any kept word |
| speech | a kept word clipped by the cut (Whisper per sentence on the cut voice vs the plan) |

## The rules the engine enforces for you

These came from real cuts that looked broken; `references/editing-grammar.md` has the why.

- A card is a **cut**, never a dissolve, and it lands on content: the title is there on frame one.
- Card and cutaway edges snap to the gap between words, and to a join in the footage when one is
  within four frames. No shot shorter than 0.45 s survives between two cuts.
- A cutaway next to a card slides 0.06 s under it, so no sliver of face flashes between them.
- Everything that moves moves sub-pixel, and every card keeps pushing to its last frame.
- Figures fade in at their final value. Nothing counts up through numbers nobody counted.
- Captions: one band, caps, spoken words full, upcoming words dim, key words boxed, navy on light
  cards, white with a soft shadow on footage, the finished line held through a breath. On footage
  a soft dark ramp sits under the band, because white type vanishes on sky and white walls.

## Files

- `scripts/vlog.py` CLI; `scripts/look.py` every graphic; `scripts/judge_cut.py` the cut judge
- `references/edit-json.md` the full EDIT.json contract with examples
- `references/editing-grammar.md` why each rule exists
- `references/judges.md` what each judge measures and how it was calibrated
- `tests/test_smoke.py` renders a synthetic clip end to end and asserts every judge passes
