---
name: statusline-theme
description: >-
  Owns ALL color decisions for the Claude Code statusline. Use when the user
  wants to "theme my statusline", "apply Catppuccin/Dracula/Nord/Gruvbox/Tokyo
  Night/One Dark/Solarized/Monokai/Rose Pine/Everforest/Ayu", "change the
  colors", "use a <palette> color scheme", "make <element> <color>" (e.g. "make
  branch green", "turn the model name red"), "recolor the branch/path/time", or
  "snap my colors to <palette>". Three modes: apply a whole palette, recolor
  named elements, or snap existing colors to the nearest palette color.
---

# statusline-theme

Set the `colors` block of `statusline_config.json` for the usage-aware Claude
Code statusline. You handle three jobs:

- **(A) Apply a palette** — map every non-semantic color KEY onto a bundled
  palette and write the resolved hex values.
- **(B) Recolor element(s)** — change only the specific keys the user named
  ("make branch green", "model should be #ff0066").
- **(C) Snap to a palette** — replace each current color with the nearest color
  in a chosen palette, measured by CIEDE2000 (perceptual distance).

## Hard rules (never violate)

1. **Never recolor the SEMANTIC band keys** —
   `ctx_bar`, `ctx_bar_mid`, `ctx_bar_high`, `ctx_bar_crit`, `ctx_bar_max`,
   `ctx_bar_track` — unless the user **explicitly opts in** ("also theme the
   gauge bands", "recolor the severity bands too"). These encode a green to red
   severity ramp shared by the context gauge AND the usage gauges; recoloring
   them silently would break the meaning. When in doubt, leave them out and say
   so.
   Likewise, **never recolor the SEMANTIC status/incident keys** —
   `status_investigating`, `status_identified`, `status_monitoring`,
   `status_maintenance`, `status_default`, `status_title`, `status_count`,
   `status_header` — unless the user explicitly opts in ("also theme the incident
   colors", "recolor the status indicator too"). These encode Claude service
   incident severity and have universally understood meaning; recoloring them
   silently would make the statusline misleading.
2. **Confirm before writing.** Always: resolve the ACTIVE config (Step 0) ->
   read it -> compute new colors -> show BEFORE/AFTER swatches + a diff ->
   test-render -> get explicit confirmation -> only THEN commit (via the helper's
   `commit`, see "Writing the result"). Never write without a yes.
3. **Only touch the `colors` block.** Preserve `templates`, `weather`,
   `emoji_width`, `ctx_bar_empty`, and every `_comment` / `_`-prefixed key
   exactly as-is. Commit the whole file back, changing only `colors`.
   Never blind-overwrite the active config; install only via the helper's
   history-aware `commit` so the prior version is snapshotted first.
4. **Valid hex only.** Every value must be `#RRGGBB`. Invalid values are
   silently ignored by the renderer, so never emit them.
5. **English only** in everything you show and write.

## Files in this skill

- `palettes.json` — 15 palettes, each with 9 ROLES
  (`text, muted, red, peach, yellow, green, sky, blue, mauve`), verified hex.
- `rolemap.json` — the KEY -> ROLE map for "apply palette" mode, plus the
  optional band opt-in map.
- `colorutil.py` — stdlib-only: hex<->rgb, sRGB->XYZ->Lab, `ciede2000`,
  `nearest_color`, and `swatch_line` / `print_swatches` for truecolor previews.
- `assets/sample_input.json` — canonical Claude Code session JSON for test renders.

Read `palettes.json` and `rolemap.json` on demand (don't paste them inline
unless needed). Run `colorutil.py` via the shell for math and swatches.

The shared **active-config + history helper** lives in the sibling
`statusline-config` skill (one copy only, stdlib): from this skill it is
`../statusline-config/statusline_io.py`. You call it as a CLI subprocess; you
never import it.

## Step 0 — Resolve the ACTIVE statusline (do this first)

Claude Code runs a specific statusline — usually the **deployed** copy (e.g.
`~/.claude/statusline.py`), NOT the repo copy. You MUST theme the config that
the active renderer actually reads, not a hardcoded repo path. Resolve it with
the sibling helper:

```
python <skills-dir>/statusline-config/statusline_io.py locate
```

`<skills-dir>` is the directory containing this skill; from here the helper is
`../statusline-config/statusline_io.py`. Parse the JSON it prints and read
`config_path` (the active config you will theme) and `statusline_py` (the
renderer used for test renders). Handle `source`:

- **`"pointer"`** — a saved pointer resolved it. Use `config_path` directly.
- **`"settings"`** — derived from the active `settings.json`. Use `config_path`,
  and OFFER to save a pointer so future runs are instant:
  `python <skills-dir>/statusline-config/statusline_io.py save-pointer
  --statusline-py <statusline_py> --config <config_path> [--settings <settings_json>]
  [--launcher <launcher>]`.
- **`"none"`** — nothing resolvable. **Ask the user** where their statusline is
  installed (the `statusline.py` and its `statusline_config.json`), then offer to
  save a pointer via `save-pointer` for next time.

Use the resolved `config_path` everywhere below as the live config to read and
(after confirmation) commit to. Never assume the repo path. If `config_path` is
missing or unreadable, fall back to renderer defaults but tell the user and
prefer to confirm the real path.

## Config locations

- Live config: the `config_path` returned by Step 0 — the file the ACTIVE
  renderer reads (usually the deployed `statusline_config.json` next to the
  deployed `statusline.py`, or the path in `$STATUSLINE_CONFIG` baked into the
  `statusLine.command`). Do NOT hardcode the repo path; the repo copy is often
  not the active one.
- The full set of non-semantic color KEYS you may set:
  `time, version, model, effort, peak, offpeak, offpeak_warn, usd, ctx_label,
  ctx_value, ctx_percent, ctx_icon, model_icon, total_icon, total, bracket,
  input, separator, output, cached_icon, cached, path, git_icon, branch,
  git_status, changes, weather, ctx_bracket`.
- The **status/incident color keys** (`status_investigating`, `status_identified`,
  `status_monitoring`, `status_maintenance`, `status_default`, `status_title`,
  `status_count`, `status_header`) are semantic and excluded from automatic
  palette application. They may only be set on explicit user opt-in (see Hard
  rule 1 and Mode A).
- The user's config may only define a subset of these. When applying a palette,
  set the keys the rolemap covers that are already present, plus any the user
  asks for. Don't invent keys the user never had unless they explicitly want a
  full palette application across every key.

## Listing palettes

When the user asks "what palettes / themes are there?", read `palettes.json` and
list each id with its `_label`. Optionally render a one-line swatch per palette
so they can see it (see "Showing swatches"). The ids are:

`catppuccin-latte, catppuccin-frappe, catppuccin-macchiato, catppuccin-mocha,
dracula, nord, gruvbox-dark, tokyo-night, one-dark, solarized-dark,
solarized-light, monokai, rose-pine, everforest-dark, ayu-dark`.

Accept fuzzy names: "catppuccin" -> ask which flavor (default mocha); "solarized"
-> ask dark vs light; "tokyonight"/"tokyo" -> `tokyo-night`; "rose pine" ->
`rose-pine`; "everforest" -> `everforest-dark`; "ayu" -> `ayu-dark`.

## The standard loop (every mode)

0. **Resolve** the ACTIVE config first (see "Step 0") and use its `config_path`
   as the live file for every step below.
1. **Read** the active `config_path`. Capture the existing `colors` object (call
   it BEFORE). If the file is missing/invalid, start from the renderer defaults —
   but tell the user, and prefer to ask for the real path.
2. **Compute** the AFTER `colors` object per the chosen mode (below).
3. **Preview**: print BEFORE vs AFTER truecolor swatches and a key-by-key diff
   (only the keys that change). Note explicitly that the semantic band keys are
   left untouched (unless opted in).
4. **Validate**: every AFTER value matches `^#[0-9a-fA-F]{6}$`.
5. **Test-render** with the canonical sample input against a CANDIDATE config so
   the live file is untouched (see "Test render").
6. **Confirm**: ask the user to approve. Only on an explicit yes do you commit.
7. **Commit** the full config (only `colors` changed) history-aware via the
   helper's `commit` subcommand (see "Writing the result").

---

## Mode A — apply a whole palette

1. Resolve the palette id (ask to disambiguate flavors if needed). Read its role
   hex values from `palettes.json`.
2. Read `rolemap.json` -> `roles`. For each KEY in `roles`, look up its ROLE,
   then the role's hex in the palette. That hex becomes the new value for that
   key.
3. Build AFTER = current `colors` with those keys overwritten. **Do not add the
   band keys.** If the user has band keys already set, leave them as they are.
4. **Band opt-in:** only if the user explicitly asked to theme the bands, also
   apply `rolemap.json` -> `bands_optin` (ctx_bar/ctx_bar_mid -> green,
   ctx_bar_high -> peach, ctx_bar_crit/ctx_bar_max -> red, ctx_bar_track ->
   muted). Otherwise say "leaving the severity bands at their defaults".
5. **Status opt-in:** only if the user explicitly asked to theme the incident/
   status colors ("also theme the incident colors", "recolor the status
   indicator too"), also apply `rolemap.json` -> `status_optin`
   (status_investigating -> peach, status_identified/status_header -> red,
   status_monitoring -> blue, status_maintenance -> sky, status_default ->
   yellow, status_title/status_count -> muted). Otherwise say "leaving the
   incident severity colors at their defaults".
6. Preview, validate, test-render, confirm, commit (history-aware, see "Writing
   the result").

Mapping reference (authoritative copy is `rolemap.json`):

```
time->yellow  version->muted  model->red  effort->blue
ctx_label/ctx_value/ctx_icon/model_icon/total_icon->muted
git_icon/bracket/separator/cached_icon->muted
ctx_percent->text  ctx_bracket->text
total->green  input->red  output->blue  cached->mauve
path->blue  branch/git_status/changes->yellow
weather->sky  peak->red  offpeak->green  offpeak_warn->peach  usd->green
```

## Mode B — recolor named element(s)

The user names one or more elements and a color each ("make branch green",
"path #88c0d0", "turn the time gold").

1. Map each named element to a KEY. Common phrasings:
   - "branch" -> `branch` (consider also `git_status`/`changes` if they say
     "git status colors" — ask if ambiguous).
   - "path"/"cwd"/"directory" -> `path`.
   - "model"/"model name" -> `model`. "time"/"clock" -> `time`.
   - "version" -> `version`. "weather" -> `weather`. "effort" -> `effort`.
   - "context %"/"ctx percent" -> `ctx_percent`. "brackets" -> `bracket` (and/or
     `ctx_bracket` — ask). "input/output/cached tokens" -> `input`/`output`/
     `cached`. "total" -> `total`.
   - "status indicator"/"incident indicator"/"investigating color" ->
     `status_investigating`; "identified color" -> `status_identified`;
     "monitoring color" -> `status_monitoring`; "maintenance color" ->
     `status_maintenance`; "status default color" -> `status_default`;
     "status title color" -> `status_title`; "status count color" ->
     `status_count`; "status banner"/"incident banner"/"status header" ->
     `status_header`. When the user says "recolor the status/incident colors"
     without specifying a severity, ask which states they want to change (or
     offer to apply the full `status_optin` palette mapping).
   - If the named element is one of the **band keys** or **status/incident keys**,
     STOP and confirm the opt-in first, because that overrides the severity ramp.
2. Resolve the requested color:
   - A hex (`#rrggbb` or `#rgb`): use it (normalize via `colorutil.hex_to_rgb`/
     `rgb_to_hex`).
   - A color word ("green", "gold", "sky blue"): pick a sensible hex. If a
     palette is in play (the config already looks like a known palette, or the
     user mentions one), prefer that palette's matching role. Otherwise use a
     reasonable common value and SHOW it so the user can veto.
3. AFTER = current `colors` with just those keys changed. Preview only the
   changed keys, validate, test-render, confirm, commit (history-aware).

## Mode C — snap to the nearest palette color

"Snap my colors to Nord", "make my current colors match Gruvbox as closely as
possible." This keeps the user's per-key intent but pulls each color onto the
chosen palette.

1. Resolve the palette id; read its 9 role hexes as the candidate set.
2. For each NON-SEMANTIC key currently in `colors`, compute the nearest palette
   color by CIEDE2000 and use it as the AFTER value. Use `colorutil`:

   ```
   python <skill>/colorutil.py  # self-test (<skill> = this skill's directory)
   ```

   For the snapping itself, import the helper or run a tiny inline script. On
   macOS/Linux a bash heredoc works; on Windows/PowerShell write the snippet to
   a temp `.py` file and run it (PowerShell has no heredoc). Use the **active
   `config_path` from Step 0** for the config you read, and this skill's own
   directory for `colorutil.py` / `palettes.json`. Bash example (substitute the
   resolved `config_path` for `<config_path>` and this skill's dir for `<skill>`):

   ```bash
   python3 - <<'PY'
   import json, sys
   sys.path.insert(0, "<skill>")
   import colorutil
   pal = json.load(open("<skill>/palettes.json"))
   cur = json.load(open("<config_path>")).get("colors", {})
   roles = [v for k, v in pal["nord"].items() if not k.startswith("_")]
   bands = {"ctx_bar","ctx_bar_mid","ctx_bar_high","ctx_bar_crit","ctx_bar_max","ctx_bar_track"}
   status = {"status_investigating","status_identified","status_monitoring","status_maintenance","status_default","status_title","status_count","status_header"}
   for key, hexv in cur.items():
       if key.startswith("_") or key in bands or key in status:   # never snap band or status keys by default
           continue
       try:
           best, de = colorutil.nearest_color(hexv, roles)
       except ValueError:
           continue
       print(f"{key}: {hexv} -> {best}  (dE00={de:.2f})")
   PY
   ```

   Swap `nord` for the chosen palette id and adjust the paths (the active
   `config_path` and this skill's dir). **Skip the band keys** (and `_`-prefixed
   keys) in the loop unless the user opted in.
3. AFTER = current `colors` with each non-semantic key replaced by its nearest
   palette hex. Preview (show the per-key delta-E so the user sees how far each
   moved), validate, test-render, confirm, commit (history-aware).

---

## Showing swatches (BEFORE/AFTER preview)

Use `colorutil.swatch_line` / `print_swatches` to render truecolor blocks so the
user can actually see the colors in the terminal. Example: build a list of
`(label, hex)` for the changed keys and print two lines, BEFORE and AFTER. On
Windows/PowerShell write the snippet to a temp `.py` file and run it (no
heredoc); the bash heredoc below is illustrative for macOS/Linux.

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "<skill>")   # this skill's directory
import colorutil
before = [("model","#E06C75"), ("branch","#E5C07B"), ("path","#61AFEF")]
after  = [("model","#f38ba8"), ("branch","#f9e2af"), ("path","#89b4fa")]
print("BEFORE:"); colorutil.print_swatches(before)
print("AFTER: "); colorutil.print_swatches(after)
PY
```

Also show a plain text diff of just the changed keys, e.g.:

```
  model   #E06C75 -> #f38ba8
  branch  #E5C07B -> #f9e2af
  path    #61AFEF -> #89b4fa
  (semantic bands ctx_bar* left unchanged)
```

## Test render (do not touch the live file)

The canonical sample input is bundled as `assets/sample_input.json`. Write the
candidate config to a temp path, then run the **resolved active renderer**
(`statusline_py` from Step 0) with `STATUSLINE_CONFIG` pointed at the candidate
so the user's live file stays untouched until they confirm. A non-empty colored
line means success.

Use the `statusline_py` from Step 0 wherever `<statusline.py>` appears, and this
skill's bundled `<skill>/assets/sample_input.json` for the sample. Do not
hardcode any particular machine's path.

PowerShell:

```powershell
$env:STATUSLINE_CONFIG="<candidate.json>"; Get-Content <skill>/assets/sample_input.json | uv run <statusline.py>
# fallback: ... | python <statusline.py>
```

bash:

```bash
STATUSLINE_CONFIG=<candidate.json> uv run <statusline.py> < <skill>/assets/sample_input.json
# fallback: python3 instead of uv run
```

## Writing the result (history-aware commit)

Never blind-overwrite the live config. On explicit confirmation, install the new
config through the sibling helper's `commit` subcommand, which snapshots the
current config and appends a changelog entry before writing.

1. Build the full new config object in memory: the current config with ONLY the
   `colors` block changed. Keep key order stable, keep all `_comment` keys and
   every `_`-prefixed key, preserve `templates`/`weather`/`emoji_width`/
   `ctx_bar_empty` exactly, and keep it valid JSON. (This is the same CANDIDATE
   you test-rendered.)
2. **Write that new config to a temp file** (e.g. in the OS temp dir) so large
   JSON never goes through argv.
3. Run the helper's `commit` against the **active `config_path`** from Step 0:

   ```
   python <skills-dir>/statusline-config/statusline_io.py commit \
     --config <config_path> --new <temp-config> \
     --skill statusline-theme \
     --summary "<what changed, one line>" \
     --why "<the user's intent>" \
     --diff "<the changed-key list, e.g. model #E06C75 -> #f38ba8 ...>"
   ```

   The helper validates the temp file is JSON (exits 4 touching nothing if not),
   snapshots the about-to-be-replaced config into
   `.statusline-config-history/YYYYMMDD-hhmm.json` next to the active config,
   writes the new bytes to `config_path`, and appends a human entry to
   `.statusline-config-history/YYYYMMDD.md`. For `--summary` keep it to the color
   change (e.g. "Applied Catppuccin Mocha palette" or "Recolored branch ->
   green"); for `--diff` pass the same per-key BEFORE -> AFTER list you previewed.
4. Read the JSON the helper prints (`snapshot`, `changelog`, `config_path`) and
   tell the user what changed in one line plus the snapshot + changelog paths,
   and how to revert (restore the snapshot file, re-run this skill, or restore
   from git). The snapshot is the easiest undo.

Do NOT write the live config any other way (no direct file write) — always go
through `commit` so history is recorded.

## Notes on specific palettes

A few palettes don't have a distinct color for every role; the closest named
color is reused (this is intentional and documented in `palettes.json`):

- **Monokai**: no separate blue — cyan `#66d9ef` serves both `sky` and `blue`.
- **Rose Pine**: gold `#f6c177` serves `peach` and `yellow`; foam `#9ccfd8`
  serves `sky` and `blue`; pine `#31748f` is the `green` role.
- **Solarized dark/light**: the accent hues are identical; only `text`/`muted`
  differ between the two variants.
- **Catppuccin** comes in four flavors (latte/frappe/macchiato/mocha); Latte and
  Solarized Light are light themes — flag that if the user is on a dark terminal.
