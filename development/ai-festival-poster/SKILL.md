---
name: ai-festival-poster
description: >-
  Turn someone's real AI usage into a desert festival lineup poster, painted in Python.
  Scans local Claude Code and Codex session logs (plus an optional ChatGPT export),
  counts the sessions in which each tool, model and MCP server was actually used, books
  the most-used as headliners across three days (Build, Think, Create), and paints a
  dusk scene with brush strokes. No image model and no invented acts or numbers. Use for
  "make my AI festival poster", "Instafest for my AI tools", "my AI usage as a lineup".
---

# AI Festival Poster

A lineup poster where every act is a tool the person really used, billed by how often.

## Rules

- **Real data only.** Every act comes from `scan_usage.py` counts. Never add a tool, model or number
  by hand; never estimate usage from spend. Acts under `--min` sessions (default 3) are dropped.
- **Local only.** The logs never leave the machine. Do not paste log contents into chat; report counts.
- **No image model.** The background is painted by `scripts/pp` (stroke-based painter) from a scene
  built in code: dusk sky, low sun, ridges, a Ferris wheel, tents, palms, field lights.
- **Privacy check before sharing.** Look at the act list: MCP server or tool names can reveal clients
  or private projects. Ask before keeping any that look private; drop them by setting `"verified": false`.

## Steps

1. `python3 scripts/get_fonts.py` (Anton, Archivo Narrow, Inter; SIL OFL, downloaded once).
2. `python3 scripts/scan_usage.py [--chatgpt-export ~/Downloads/chatgpt-export.zip] --out usage.json`
   prints the act list per day. Show it to the user and apply the privacy check.
3. `python3 scripts/render_poster.py --usage usage.json --presenter "<Name>" --dates "<MON YYYY> TO <MON YYYY>"`
   writes `out/poster-1080x1350.png` (4:5, feed size) and `out/poster-2160x2700.png`. About 2 minutes on
   a desktop CPU; `--under` previews the scene in seconds.
4. Look at the poster. If a day has few acts or a line wraps awkwardly, you may move acts between days
   (say so) but never change a count. Dates: first and last month of the logs you scanned.

## How billing works

Each day: a boxed day label, one headliner (most sessions), then full-width lines of 3, 4 and 6 acts,
then the rest. Each line is sized to fill the width, like a real festival bill. Categories: BUILD
(coding agents, dev infrastructure), THINK (chat assistants, models, research tools), CREATE (media and
publishing tools). Unknown MCP servers default to THINK.

## Dependencies

Python 3 with NumPy, SciPy and Pillow.
