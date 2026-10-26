---
name: mjdesign
description: Turn a post, moment, note, chart or idea into an MJ Research visual explainer — a 4:5 still image (1080x1350 PNG) and a 9:16 short video (1080x1920 MP4, ~11s, preview frame = final image), optional looping GIF where the diagram draws itself and the headline builds word by word. Drex-style editorial format (line-art diagram, engraved hatching, one emphasised headline word) in MJ Research colours (linen/enamel, oxide/cadmium/cobalt/verdigris) and type (Bricolage Grotesque + Departure Mono). Use when the user says /mjdesign, or asks to "make a visual / graphic / reel / short video / carousel image / post image" for a post, insight, market moment, release or idea, especially for Mario Jude / MJ Research.
---

# /mjdesign

One idea in, one picture and one short video out. The format: a mono kicker bar, a hairline rule, a line-art figure that *explains* the idea, a heavy headline with one word in italic caps and accent colour, a short body line, an optional big mono stat, a mono footer. Linen ground with grain by default.

Inspiration is drex.design (visual explainers for writers: diagrams and engraved illustration that make an idea legible at a glance). Copy the *method*, not the work: every image must carry a diagram of this post's actual idea.

## Steps

1. **Distil the post** into: a headline of 4–9 words with exactly one `*word*` (the turn of the idea), one body sentence (≤ 18 words), optional stat (`value` + short `label`), a kicker (`MJ Research · <topic>`), an index (`No. 0xx`) and a footer (`mjresearch · DD.MM.YYYY`). Write in British English.
2. **Draw the figure** — this is the part that matters. Write an inline SVG that shows the mechanism of the idea, not decoration: two lines diverging, a funnel narrowing, a ladder, a before/after split, a node graph, a sunburst from one cause. Rules:
   - `fill="none" stroke="currentColor"` on the root; stroke widths 1.2–2 for structure, 4–6 for the one line that matters.
   - Mark the one element that carries the point with `class="accent"` (gets the accent colour). Only one or two accent elements.
   - Engraving texture: `fill="url(#hatch)"`, `url(#cross)` or `url(#dots)` on areas. No solid colour blocks, no gradients, no text inside the SVG (the headline does the talking).
   - Order elements in the order they should draw: axes/frame first, context next, the accent last. Stroked shapes draw themselves over 1–5s; hatched fills fade in after their outline; dashed strokes (`stroke-dasharray`) fade instead of drawing.
   - Keep it under ~120 elements. Any `viewBox` works; it is fitted to the figure area.
   - No idea for a diagram? Use a built-in motif: `"figure": "sunburst"` (a single cause radiating), `"tunnel"` (depth, focus, a frame within a frame) or `"orbit"` (a system, cycles, things around a centre).
3. **Write the spec** to the session scratchpad (never the repo), e.g. `post.json`:
   ```json
   {
     "slug": "breadth-narrowing",
     "kicker": "MJ Research · Breadth", "index": "No. 014",
     "headline": "The index climbs while its *base* thins",
     "body": "Fewer names carry the tape. Ten stocks now explain most of this year's gain.",
     "stat": { "value": "27%", "label": "of S&P 500 above their 50-day" },
     "accent": "oxide", "ground": "linen",
     "footer": "mjresearch · 24.10.2026",
     "figure": "<svg viewBox='0 0 900 560' fill='none' stroke='currentColor' stroke-width='2'>…</svg>"
   }
   ```
   `accent`: `oxide` (default, rust — risk, warning, the point), `cadmium` (gold — gain, insight), `cobalt` (blue — data, structure), `verdigris` (green — health, growth). `ground`: `linen` (default) or `enamel` (dark). Optional `duration` (seconds, default 10). Full examples: `examples/breadth.json`, `examples/conviction.json`.
4. **Render** (first run only: `npm install` in this skill directory; it uses the system Google Chrome, no browser download):
   ```bash
   node ~/.claude/skills/mjdesign/render.mjs post.json <outdir>          # both
   node ~/.claude/skills/mjdesign/render.mjs post.json <outdir> --still  # PNG only
   node ~/.claude/skills/mjdesign/render.mjs post.json <outdir> --video  # MP4 only
   node ~/.claude/skills/mjdesign/render.mjs post.json <outdir> --gif    # add a looping 4:5 GIF (720x900, 12fps)
   ```
   The MP4 and GIF open on the finished composition for 1s, fade to the empty page, build, then hold. Platforms use the first frame as the preview, so the preview is the final image. Do not remove this intro.

   **Which file for where:** MP4 is the default for LinkedIn, Instagram Reels and X. LinkedIn autoplays native video muted in the feed, and the quality is far better. Use the GIF only for a looping inline image (a LinkedIn *image* post uploaded through the photo button, Slack, email, docs). LinkedIn's GIF limit is reported at 2–5MB, so the renderer warns above 2MB. The GIF has no grain, because noise breaks GIF compression.
   It fails loudly if a font does not load (Bricolage comes from Google Fonts, so it needs network) or the template throws.
5. **Look at the output before handing it over.** Read the PNG. For the video, tile frames and read that (frame 0 must be the finished image):
   `ffmpeg -i x.mp4 -vf "select='eq(n\,0)+eq(n\,60)+eq(n\,150)+eq(n\,341)',scale=360:-1,tile=4x1" -frames:v 1 -vsync vfr strip.png`
   Check: the figure reads as the idea without the caption, nothing overlaps the headline, the headline fits in ≤ 3 lines, one accent word only. Fix the spec and re-render; do not hand over a first draft you have not seen.
6. Send the files to the user (SendUserFile) with one line saying what the figure shows.

## Do not

- Edit `template.html` to make one post fit. Shorten the copy or redraw the figure instead. Change the template only when the format itself should change, and say so.
- Use colours or fonts outside the tokens in `template.html` (copied from `ai-hedge-fund/frontend/src/index.css` in the Mario Jude Fund repo; keep them in sync if the brand changes).
- Put a client's or a third party's logo, likeness or branding in the figure.
