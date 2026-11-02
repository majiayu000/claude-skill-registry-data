---
name: gif-analysis
description: "Use when a GIF arrives and you can't see its motion."
version: 1.0.0
---

# GIF Analysis — see the full animation, not just frame 1

## Trigger
A GIF arrives in conversation (user-sent, or a media URL) and you only ever
see the FIRST frame — a frozen still that loses the punchline. Or you need to
describe what a GIF actually *does* (motion, expression change, meme arc).

## The problem
Discord/media delivery flattens GIFs to their first frame for the agent's
vision. A "suspicious" meme that is a person lowering a peace sign while their
stare intensifies reads as just "a guy with a peace sign" from frame 1. The
joke lives in the motion.

## The fix — contact-sheet extraction
`scripts/gif2sheet.py <path-or-url> [--cols 4] [--max-frames 24] [--outdir DIR]`

- Extracts frames with Pillow (already installed), samples evenly if the GIF
  has more frames than `--max-frames`
- Saves each frame to `<outdir>/frames/frame_001.png` (full res)
- Builds `<outdir>/sheet.png` — a numbered grid (each cell labeled `N/total`)
  so a single vision pass reads the whole sequence in order
- Prints the sheet path on stdout; exit 0 on success, 2 on load/read failure

Then call `vision_analyze` on `sheet.png` with a question that asks for the
**arc**: "Describe what happens across the frames — motion or expression
change between frame 1 and frame N?" The numbered cells let the vision model
report the timeline (e.g. "frames 1-8 peace sign up, 9-12 hand lowers,
13-24 intense stare").

## Workflow
1. User sends GIF / you spot a `.gif` URL → save it or pass the URL directly
   (the script handles http(s) sources itself).
2. Run the script, capture the sheet path.
3. `vision_analyze(sheet_path, question="describe the motion across frames")`.
4. Reply referencing the arc — you now know the joke.

## Pitfalls
- Pillow is present on this box (12.x) — no install needed. imageio is NOT
  guaranteed; the script only needs Pillow.
- GIFs with hundreds of frames: cap with `--max-frames` (default 24) — the
  script samples evenly so you still get the arc without a huge sheet.
- `im.seek()` indices must be ints — the sampling uses a set of rounded ints;
  do not pass a list to seek.
- Tiny GIFs (e.g. 165x149) still work fine — the sheet grid scales to fit.
- When the user says "did you see the gif?" and you only saw a still, say so
  and run this — it turns "I missed it" into "I watched it."
- **Vision models hallucinate source identities.** The auxiliary vision model
  confidently labeled a Dexter "I'm watching you" scene (Doakes, two fingers at
  the eyes) as "Tyrese in 2 Fast 2 Furious" (8/11/26). Report the *visible
  motion* (gesture, expression shift) and never insist on the source/show — the
  human who sent the GIF knows the scene; accept their correction gracefully.
  Also: a two-finger gesture at the eyes is NOT a peace sign — it's a
  surveillance/threat gesture in meme-land.
