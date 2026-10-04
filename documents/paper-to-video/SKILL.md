---
name: paper-to-video
description: End-to-end workflow that turns a research paper (PDF or LaTeX) into a narrated video — paper -> slides -> voice-over -> assembled video, optionally with other videos spliced in. Use when the user wants a supplementary video, paper video, talk video, video abstract, or "make a video from my paper", or asks to rebuild/update such a video in this repo.
---

# Paper to video

All scripts live in `scripts/` at the repo root. Run them with `uv run` from the repo root
(the venv is managed by uv; run `uv sync` and `uv run playwright install chromium` once if `.venv` is missing).
Every script takes the PROJECT folder as its first argument and has `--help`.

## Stages

| # | Stage | Command | Produces |
|---|---|---|---|
| 0 | Create project | `uv run scripts/init_project.py projects/NAME --paper PAPER.pdf` | folder layout, `paper/` extraction |
| 1 | Read paper | read `paper/paper.md` (or `paper.tex`), look at `paper/pages/*.png` | your understanding |
| 2 | Script | write `narration.json` | voice-over text per segment |
| 3 | Slides | write `slides/NN-name.html`, then `uv run scripts/render_slides.py P --check` | `out/slides/*.png` |
| 4 | Voice | `uv run scripts/generate_voice.py P` | `audio/*.wav` |
| 5 | Timeline | `uv run scripts/make_timeline.py P`, then edit `timeline.json` | ordered items |
| 6 | Video | `uv run scripts/assemble_video.py P --draft --sheet`, review, then without `--draft` | `out/video.mp4` |

Stage details live in the sibling skills: **paper-to-slides** (stages 1-3), **voiceover** (stage 4),
**video-editing** (stages 5-6 and anything involving other videos).

## How to run it

1. **Ask only what you cannot infer.** Before writing, settle: target length (default 3 min of
   narration for a supplementary video), venue limits (size in MB, minutes, anonymity), audience,
   and whether other videos (demo, screen recording, user study footage) should be included and where.
   If the user already said, don't ask.
2. **Script before slides.** Draft `narration.json` first (one segment per slide, ids `NN-short-name`),
   ~150-170 spoken words per minute. Show the user the script and outline; it is cheap to change now and
   expensive after TTS.
3. **Slides follow the script.** One idea per slide; the narration carries detail, the slide carries the
   headline, one figure or 3-4 short bullets. Same id as the narration segment.
4. **Render and look.** Always run `render_slides.py --check` and open the PNGs to look at them
   yourself. Fix every reported issue.
5. **Voice.** Use `--provider say` or `--provider silent` for a free timing draft if the user has no API
   key yet; real TTS needs `OPENROUTER_API_KEY` in `.env`. Report clips flagged `LOW`.
6. **Assemble a draft** with `--draft --sheet`, read the contact sheet PNG to check the order and
   content, then build the final. Report length, size, and any `max_mb` / `max_minutes` warnings.

## Rules

- Never invent results, numbers or claims; everything on slides and in narration must come from the paper.
- Anonymous submissions: no author names, affiliations, logos, or identifying footage (faces, lab names,
  window titles). Ask before including footage that might identify people.
- Keep generated media out of git (`out/`, `audio/*.wav` are ignored); the source of truth is
  `narration.json`, `slides/*.html`, `timeline.json` and `media/`.
- Re-running is cheap: voice clips and video segments are cached and only rebuilt when their inputs change.
