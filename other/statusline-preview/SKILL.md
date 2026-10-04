---
name: statusline-preview
description: >-
  Render a statusline config against sample data and show it as a terminal
  preview and/or export an SVG screenshot (the same style as examples/*.svg).
  Invoke when the user says things like "preview my statusline", "show me what
  it looks like", "render the statusline", "export an SVG of my bar", or "make a
  screenshot of the statusline".
---

# statusline-preview

Render the statusline against fixed sample data so the user can SEE the result
without waiting for real git / weather / usage, and optionally export an SVG
screenshot that matches the look of `examples/*.svg`.

This skill is **read-only**. It never writes `statusline_config.json`. It only
shells out to the renderer with a chosen config and captures the colored output.
Use the `statusline-config` or `statusline-theme` skills to actually change the
config; use this one to look at the result.

## What it produces

1. A **terminal preview**: the real ANSI-colored status line printed to your
   terminal (truecolor). This is exactly what Claude Code would draw, but driven
   by deterministic sample data (sample git stats, sample weather, sample usage).
2. An optional **SVG screenshot** written to a path you choose, in the same
   visual style as the bundled `examples/*.svg` (dark rounded card, Agave Nerd
   Font with a monospace fallback, truecolor spans, block / eighth-block gauge
   glyphs, emoji drawn as a single cell).

## Files in this skill

- `render_demo.py` — imports `statusline.py` as a module, monkeypatches the
  network/git helpers with believable sample values, feeds the canonical sample
  JSON on stdin, runs the renderer, and prints the ANSI bar. With `--svg <path>`
  it also hands the ANSI to `ansi2svg.py`.
- `ansi2svg.py` — converts the captured ANSI (24-bit SGR runs) into an SVG that
  matches the visual style of `examples/*.svg`. Runnable standalone
  (`python ansi2svg.py < ansi.txt > out.svg`) and importable.
- `assets/sample_input.json` — the canonical Claude Code session JSON used for
  the render (so previews are deterministic and reproducible).

Both `.py` files are **standard-library only** (the project is dependency-free).

## How to run it

The renderer lives at `F:/ai/statusline/statusline.py` (adjust the repo root if
the project lives elsewhere). `render_demo.py` finds it automatically: it sits
three directories above this skill (statusline-preview -> skills -> .claude ->
repo root), but you can also pass `--statusline-dir`.

### 0. Resolve the ACTIVE statusline first (do this every time)

"Preview my statusline" must show what Claude Code is REALLY running — usually
the **deployed** copy (e.g. `~/.claude/statusline.py`), not the repo copy. Before
rendering, resolve the active target with the shared helper that lives in the
`statusline-config` skill (a sibling of this skill):

```
# from this skill's dir, the helper is ../statusline-config/statusline_io.py
python F:/ai/statusline/.claude/skills/statusline-config/statusline_io.py locate
```

It prints one JSON object, e.g.:

```
{"statusline_py": "...", "config_path": "...", "settings_json": "...",
 "launcher": "...", "source": "pointer"|"settings"|"none",
 "pointer_path": "...", "notes": "..."}
```

Use it as follows:

- `source` is `"pointer"` or `"settings"` → render that target: pass
  `--config <config_path>` and `--statusline-dir <dir of statusline_py>`.
- `source` is `"none"` → **ask the user** where the active statusline / config
  is, then render with the path they give. For convenience you may also offer to
  save a pointer via
  `statusline_io.py save-pointer --statusline-py <P> --config <C>` so future
  previews resolve instantly. (Likewise, if `source == "settings"` you may offer
  to save a pointer so future runs are instant — both are optional and not
  required just to preview.)

### 1. Preview the user's ACTIVE config (what's really running)

Point the renderer at the resolved `config_path` and its statusline directory —
this is the deployed/live config, rendered without modifying it.

```
# PowerShell — substitute the resolved paths from step 0
python F:/ai/statusline/.claude/skills/statusline-preview/render_demo.py --config <config_path> --statusline-dir <dir of statusline_py>

# bash / macOS / Linux
python3 /f/ai/statusline/.claude/skills/statusline-preview/render_demo.py --config <config_path> --statusline-dir <dir of statusline_py>
```

If `uv` is available you may use `uv run …` instead of `python …`; plain
`python`/`python3` works because there are no third-party deps. (Running
`render_demo.py` with no `--config`/`--statusline-dir` falls back to the renderer
inferred from this skill's location and its normal `STATUSLINE_CONFIG` / repo
`statusline_config.json` resolution — use that only when `locate` cannot resolve
a target and the user points you at the repo copy on purpose.)

### 2. Preview a SPECIFIC config (e.g. an example or a candidate)

Use `--config <path>`. The skill sets `STATUSLINE_CONFIG` to that path for the
render only — the live file is untouched.

```
python F:/ai/statusline/.claude/skills/statusline-preview/render_demo.py --config F:/ai/statusline/examples/hero.json
```

### 3. Export an SVG screenshot

Add `--svg <output-path>`. You still get the terminal preview as well.

```
python F:/ai/statusline/.claude/skills/statusline-preview/render_demo.py --config F:/ai/statusline/examples/hero.json --svg F:/ai/statusline/examples/hero.svg
```

Useful flags:

- `--config <path>` — config to render (default: the renderer's normal config
  resolution, i.e. `STATUSLINE_CONFIG` or the repo `statusline_config.json`).
- `--svg <path>` — also write an SVG screenshot to this path.
- `--input <path>` — use a different sample session JSON instead of the bundled
  `assets/sample_input.json`.
- `--statusline-dir <path>` — folder containing `statusline.py` (default: the
  repo root inferred from this skill's location).
- `--emoji-cells {1,2}` — how many columns an emoji occupies for the SVG width
  math only (default 1, matching how the SVG draws emoji in a single cell).

## Procedure for Claude

1. Decide which config to render:
   - "preview my statusline" / "show me what it looks like" → resolve the
     **active** target first (see step 0): run
     `python <skills-dir>/statusline-config/statusline_io.py locate`
     (= `../statusline-config/statusline_io.py` from this skill), then pass the
     resolved `--config <config_path>` and `--statusline-dir <dir of
     statusline_py>` so you preview what is REALLY running, not the repo copy. If
     `source == "none"`, ask the user for the config path and render that — and
     you may offer to save a pointer via `statusline_io.py save-pointer
     --statusline-py <P> --config <C>` so future previews resolve instantly
     (optional; previewing does not require it).
   - "render `examples/hero.json`" / a candidate path → pass `--config <path>`
     directly (no `locate` needed; the user named the file).
2. Run `render_demo.py` with the chosen flags. Show the terminal output to the
   user (it is real ANSI — your terminal renders the colors).
3. If the user asked for a screenshot / SVG ("export an SVG", "make a
   screenshot"), add `--svg <path>`, pick a sensible output path (default to
   `examples/<name>.svg` when regenerating an example, otherwise ask), and run
   again. Tell the user where the SVG was written.
4. Mention the rendering assumptions when relevant: the SVG targets **Agave Nerd
   Font** (falling back to a generic monospace), draws **emoji as a single
   cell**, and uses a fixed monospace cell grid — matching the visual style of
   the existing `examples/*.svg` (interior baselines can differ by ~0.1px due to
   rounding, which is imperceptible). The preview uses **sample**
   git/weather/usage data, not the user's real values, so countdowns and stats
   are illustrative.

## Notes

- Sample data baked into `render_demo.py`: weather is a believable
  partly-cloudy day with sunrise/sunset computed for **today** (so `{sun}`
  resolves correctly), usage is `session 41%` / `week 63%` with reset times
  computed at runtime (~3h and ~2d out, so the countdowns look real), and git is
  `main` with `+128 / -34`. The session JSON (model, version, context %, tokens)
  comes from `assets/sample_input.json`.
- Empty lines render nothing (the renderer skips blank rows), so a config that
  only defines `line1` produces a single-line preview and a single-line SVG.
- English only. Standard library only.

## Previewing the status-page indicator (`{status}` / `{status_header}`)

`{status}`, `{status_icon}` and `{status_header}` render EMPTY unless an incident
is currently active, so a normal preview of a status config shows nothing for
those lines — the renderer reads the live incident cache at
`~/.claude/status_cache.json` (refreshing it from status.claude.com only when
it's stale). To preview them with a *guaranteed* active incident without
touching the user's real cache, point `HOME`/`USERPROFILE` at a throwaway dir
that holds a fake cache, then render as usual:

```powershell
# 1. throwaway home with a fake ACTIVE incident cache (PowerShell)
$home2 = "$env:TEMP/sl-status-preview"
New-Item -ItemType Directory -Force "$home2/.claude" | Out-Null
$now = [int][double]::Parse((Get-Date -UFormat %s))
@"
{"ts": $now, "etag": null, "incidents": [
  {"title": "Elevated API error rates",
   "link": "https://status.claude.com/incidents/preview-sample",
   "status": "investigating", "label": "Investigating",
   "text": "We are investigating elevated error rates on the API.",
   "when": "preview", "pub_date": "", "pub_ts": $now,
   "state": "incident", "emoji": "🔍", "updates": 1}]}
"@ | Set-Content -Encoding utf8 "$home2/.claude/status_cache.json"

# 2. render with HOME/USERPROFILE redirected to the throwaway home
$env:HOME = $home2; $env:USERPROFILE = $home2
python F:/ai/statusline/.claude/skills/statusline-preview/render_demo.py --config F:/ai/statusline/examples/status.json --svg F:/ai/statusline/examples/status.svg
```

This works because `statusline.py` resolves its `STATUS_CACHE` path from the
home directory at import time — so the override must be set *before* the
`python` process starts (a subprocess/new shell, not from inside the renderer).
Keep `ts` fresh (within the 120s cache TTL) so `get_incidents()` returns the
cache as-is instead of hitting the network, and `pub_ts` fresh so the incident
passes the config's `max_age_hours` filter. `state` must be `"incident"` (or
`"maintenance"` with `include_maintenance: true`). The bundled
`examples/status.svg` was generated exactly this way. The user's real
`~/.claude/status_cache.json` is never read or written.
