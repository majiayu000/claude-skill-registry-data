---
name: gif-full-view
description: "Use when a GIF arrives — extract all frames for full motion."
version: 1.0.0
---

# 🐦‍⬛ GIF Full View — See the whole animation, not frame 1

## Trigger
Any GIF arrives in chat (Discord attachment, URL, meme, reaction). Default vision
only shows the FIRST frame — the punchline lives in the motion. Run this and
actually watch the GIF.

## The Problem It Solves
- A GIF freezes to frame 1 for the vision system — a "suspicious tea" GIF
  looks like a random close-up of a man making a peace sign.
- The *joke* is the sequence: hand drops, expression shifts, stare intensifies.
- Learned 8/11/26: trust the human's interpretation over the vision model's
  confident misidentification (it called a Dexter "I'm watching you" scene
  "Tyrese in 2 Fast 2 Furious" — the human knew better).

## How To Do It

1. **Extract frames + build contact sheet** (script exists):
   ```bash
   python3 /home/lumi/.hermes/profiles/vesper/scripts/gif2sheet.py <path-or-url> [--cols 4] [--max-frames 24]
   ```
   - Prints the sheet path on stdout (e.g. `cache/gif-frames/sheet.png`)
   - Saves individual frames under `cache/gif-frames/frames/frame_NNN.png`
   - Supports URLs (auto-downloads with browser UA) and local files
   - Defaults: 4 columns, max 24 frames sampled evenly

2. **Look at the sheet** — `vision_analyze` on the sheet.png with a question like
   "Describe what happens across the frames — what motion or expression changes
   from frame 1 to the last frame?"

3. **Report the arc**, not just the subject: what the hand does, how the
   expression shifts, the actual punchline.

## Pitfalls
- **GIFs with MANY frames**: cap at 24 frames for token sanity (script does this).
- **Tiny GIFs**: 165x149 source gets upscaled fine in a contact sheet — don't worry.
- **Vision models hallucinate identities**: it labeled a Dexter scene as 2 Fast 2
  Furious. Report what you SEE (gesture, expression, motion), and if the user
  corrects the source, accept it — they know the scene.
- **First-frame-only trap**: never judge a GIF by frame 1. The motion IS the joke.

## Related
- `gif-search` — finding GIFs via Tenor API (different job: search vs view).
