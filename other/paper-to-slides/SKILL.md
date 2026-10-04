---
name: paper-to-slides
description: Read a research paper and write the narration script and HTML slides for a paper video (stages 1-3 of paper-to-video). Use when extracting a paper's text/figures, cropping figures, writing narration.json, designing or fixing slides/*.html, or when render_slides.py --check reports layout problems.
---

# Paper -> script -> slides

## 1. Extract the paper

```bash
uv run scripts/extract_paper.py PAPER.pdf -o P/paper        # text, page renders, embedded images
uv run scripts/extract_paper.py main.tex  -o P/paper        # LaTeX: inlined source + all figures as PNG
```

- Read `P/paper/paper.md` (or `paper.tex`) fully. Note: contribution, method, study design, key numbers,
  main figures.
- Raster figures are in `P/paper/images/`. Vector figures (plots, diagrams) are not embedded images: open
  the page render `P/paper/pages/page-NN.png`, estimate the figure's box as page fractions, and crop at
  300 dpi:
  ```bash
  uv run scripts/extract_paper.py PAPER.pdf crop --page 4 --frac --bbox 0.08 0.10 0.92 0.45 -o P/figures/fig3.png
  ```
  Open the crop and adjust until it holds the whole figure with no caption text or neighbouring columns.
- Copy figures you will show into `P/figures/` with readable names. With LaTeX sources, prefer the original
  figure files (sharper than crops).

## 2. Write narration.json

```json
{
  "tts": {"provider": "openrouter", "model": "google/gemini-3.1-flash-tts-preview",
          "voice": "Charon", "style": "Read this clearly at a brisk, professional pace, with short pauses: "},
  "verify": {"model": "openai/gpt-audio-mini", "min_similarity": 0.9, "retries": 3},
  "segments": [
    {"id": "01-title", "text": "..."},
    {"id": "02-problem", "text": "..."}
  ]
}
```

- `id` = `NN-short-name`; the slide file, PNG, audio clip and timeline item all share it. Use two-digit
  prefixes so names sort in order; leave gaps (10, 20, 30) if many inserts are expected.
- A segment may also narrate a video clip (no slide with that id); the timeline attaches it to the clip.
- Length: ~2.6 spoken words per second. A 3-minute video is ~450 words.
- Write for the ear: short sentences, no parentheses, no citations, no "as shown in Figure 3", spell out
  symbols ("p less than point zero five" only if essential; prefer "significantly"). Expand acronyms on first
  use. Numbers as words when they are read aloud awkwardly.
- Typical arc: title and one-line claim; problem and why it matters; approach; setup or study; results
  (one slide per main finding); demo footage if any; takeaway.

## 3. Write the slides

`init_project.py` puts `theme.css` and layout examples (`_title`, `_points`, `_figure`, `_split`,
`_stats`, `_takeaway`) into `P/slides/`. For each segment, copy the closest layout to `P/slides/<id>.html`
and edit it. Files starting with `_` are never rendered into the video.

- Frame is exactly 1920x1080. All content goes inside `<div class="slide"> ... <div class="pad">`.
- Keep the `.kick` (section label) and `.pageno` ("03 — 09") chrome consistent across the deck.
- Figures: `<img src="../figures/x.png">` inside `.fig` (it scales to fit). Never upscale tiny images;
  re-crop at higher dpi instead.
- Per-slide tweaks go in a `<style>` block scoped by an id on `.slide`, e.g. `#s05 h2{font-size:64px}`.
  Change theme colours/fonts only in `theme.css` `:root`, and keep `settings.background` in
  `timeline.json` equal to `--paper` so fades match.
- Text budget: a headline of at most ~8 words; at most 4 bullets of one line each; captions one line.

Render and check:
```bash
uv run scripts/render_slides.py P --check            # all slides
uv run scripts/render_slides.py P --only 05-results --check
uv run scripts/render_slides.py P --pdf              # also out/slides.pdf for sharing
```
`--check` exits non-zero and lists elements outside the 72 px safe area, clipped text, and images that
failed to load. Fix them all, then **open every PNG and look**: --check cannot see poor contrast,
awkward line breaks, empty-looking slides, or unreadably small figure text.
