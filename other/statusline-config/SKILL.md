---
name: statusline-config
description: >
  Guided LAYOUT setup for the usage-aware Claude Code statusline — decides WHAT the bar
  shows (which lines/elements, usage display style, context gauge form, weather, incident
  status indicator, emoji width) by chatting, complementing the TUI editor. Invoke when
  the user says things like "set up the statusline", "configure my statusline", "change
  which lines/elements show", "add weather to the bar", "show usage in the statusline",
  "switch to a compact usage display", "hide the git line", "configure the context gauge",
  "show Claude status in the bar", or "add an incident indicator". This skill does NOT
  change colors — colors are owned by /statusline-theme; route any color/theme request
  there instead.
---

# statusline-config — guided layout setup

You configure **what the statusline shows** by editing `statusline_config.json`. You set
**layout only**: which lines exist, which element blocks appear, the usage display style,
the context-gauge form, weather, and `emoji_width`.

**You do NOT touch colors.** The `colors` block is owned entirely by `/statusline-theme`.
Leave `colors` exactly as you found it (preserve it byte-for-byte). If the user asks about
colors/themes/palettes, tell them to run `/statusline-theme` and do not edit `colors` here.

Never present `{peak_label}` as an option — Anthropic removed peak-hour limits; it exists
only for back-compat. Only emit placeholders from the list below. English only.

---

## Step 1 — Locate the ACTIVE statusline and read its config

You edit the **ACTIVE** statusline — the one Claude Code is really running. That is usually
the **DEPLOYED** copy (e.g. `~/.claude/statusline.py` and `~/.claude/statusline_config.json`),
**NOT** the repo copy. Do not assume the repo. Resolve the active target with the shared
helper that lives beside this file, `statusline_io.py`:

```
python statusline_io.py locate
```

(Run it with the absolute path to `statusline_io.py` in this skill's own directory; fall
back to `python3` if `python` is unavailable.) It prints a single JSON object:

```json
{"statusline_py": <abs or null>, "config_path": <abs or null>,
 "settings_json": <path or null>, "launcher": <str or null>,
 "source": "pointer"|"settings"|"none",
 "pointer_path": <abs path where the pointer would live>,
 "notes": <short human string>}
```

Use `config_path` as the file you will write back to, and `statusline_py` as the renderer.
Handle `source` as follows:

- **`pointer`** — a saved pointer resolved the target. Use it as-is.
- **`settings`** — resolved by parsing the active `settings.json` (`statusLine.command`).
  Use it, then **OFFER to save a pointer** so future runs are instant:
  ```
  python statusline_io.py save-pointer --statusline-py <statusline_py> --config <config_path> [--settings <settings_json>] [--launcher <launcher>]
  ```
- **`none`** — nothing resolvable. **ASK the user** where their statusline is installed
  (the path to the active `statusline.py`); the config is `statusline_config.json` beside it
  unless they set `STATUSLINE_CONFIG`. Then OFFER to `save-pointer` with those values.

Always make clear to the user that you are editing the **ACTIVE (often deployed `~/.claude`)
config**, not the repo copy. Never write to a directory the renderer will not read from.

Now **read the resolved `config_path`**. If it is missing or invalid JSON, note that you'll
start from built-in defaults (the bar always renders even with no config). Then **summarize
what is currently active**:

- Which `templates` keys start with `line` (those are ON, in order) vs `_disabled_*`/`_*`
  (those are OFF).
- Which element blocks each active line contains (session header / weather / git / usage /
  status incident indicator).
- Which usage style is in use, if any (`{usage_bars}`+`{usage_resets}` / `{usage_micro}` /
  `{compact_usage_micro}` / none).
- Which context-gauge form is in use (`{ctx_micro}` inline / bare `{ctx_bar}` / `{ctx_bar:N}`
  / just `{ctx}`/`{ctx_percent}`).
- `emoji_width`, and weather `name` + `show_*` flags.
- Whether a `status` block is present and whether any active line uses a status placeholder
  (`{status}`, `{status:N}`, `{status_icon}`, `{status_header}`).

---

## Step 2 — Gather choices (use the AskUserQuestion tool)

### Fast path first
Offer the user a choice up front:

- **Start from a preset** (recommended) — pick one of the four presets below, then
  optionally tweak.
- **Customize (ask me everything)** — go through the custom rounds.

**Presets** (mirror the repo's `examples/`):

| Preset | Lines | What it shows |
|---|---|---|
| **Minimal (1 line)** | line1 | model + context label/percent + inline ctx micro. No weather, no usage, no git. |
| **Two-line (weather + compact usage)** | line1, line2 | sun + time + model + effort + ctx percent on line1; weather + `{compact_usage_micro}` on line2. |
| **Three-line (context bar + git)** | line1, line2, line3 | header on line1; weather + big auto-aligned `{ctx_bar}` on line2; path/git/changes on line3. |
| **Four-line (full usage)** | line1..line4 | header on line1; path/git on line2; `{usage_bars}` on line3; `{usage_resets}` on line4. |

The exact preset templates are in the **Preset templates** section near the end of this
file — copy them verbatim when a preset is chosen.

### Custom rounds (only if the user picked "customize")
Ask in clear, separate rounds:

1. **Element blocks** (`multiSelect`): `session header`, `weather`, `git`, `usage`,
   `status` (incident indicator — zero-cost when nothing is active; the whole line is
   suppressed automatically).
2. **Usage style** (single select — pick at most ONE, never mix):
   - **Full bars (2 lines)** — `{usage_bars}` on one line, `{usage_resets}` on the next.
     Most detail; costs two lines.
   - **Micro (1 line)** — `{usage_micro}`: one line, full-word labels ("session 41%…").
   - **Compact micro (1 line)** — `{compact_usage_micro}`: one line, terse ("s 41%…w 63%…").
   - **None** — no usage segment.
3. **Context gauge** (single select):
   - **Inline micro** — append `{ctx_micro}` to line1 (tiny `▕<cell>▏`).
   - **Big auto-aligned bar** — bare `{ctx_bar}` on its own line (see composition rule).
   - **Fixed N-cell** — `{ctx_bar:N}` (ask N, e.g. 28); sits anywhere.
   - **Percent text only** — just `{ctx}` and/or `{ctx_percent}`, no gauge.
4. **Weather** (only if `weather` chosen): ask the **city** (free text), then which parts
   to show (`multiSelect` over `show_name`, `show_icon`, `show_temp`, `show_humidity`,
   `show_wind`), then **sun glyph** on/off (`{sun}`).
5. **Emoji width** (single select): `2` (default; most terminals) or `1` (tip: choose 1 if
   emoji render single-width and the bar looks shifted).

---

## Step 3 — Geocode the city (only if weather is ON)

Resolve the city name to coordinates via the Open-Meteo **geocoding** endpoint (this is
separate from the forecast call `statusline.py` makes):

```
GET https://geocoding-api.open-meteo.com/v1/search?name=<CITY>&count=1&language=en&format=json
```

Read `results[0]`: use `.latitude`, `.longitude`, and `.name` (and `.country` to confirm).
Write `name`/`latitude`/`longitude` into the `weather` block and **confirm the resolved
city + country** with the user before composing. If geocoding returns no results, ask the
user to refine the city name.

Do NOT ship a config that uses `{weather}`/`{sun}` without a geocoded `weather` block — if
`latitude`/`longitude` are missing the renderer falls back to the default placeholder
location (Newyork / 56.25 / -5.2833) and shows bogus weather.

---

## Step 4 — Compose the templates

Build the active `line1..lineN` from the chosen modules using the **Fragment recipes**
below, then enforce the **composition rules**.

### Placeholders (the COMPLETE list — emit nothing else)

```
Color/format:  {c.NAME}  {r}
Session:       {time} {version} {model} {effort}
Context:       {ctx} {ctx_percent} {ctx_bar} {ctx_bar:N} {ctx_micro} {align_pad}
Tokens:        {total} {input} {output} {cached}
Usage gauges:  {usage_bars} {usage_resets} {usage_micro} {compact_usage_micro}
Path/git:      {path} {branch} {added} {removed}
Weather:       {weather} {sun}
Status:        {status} {status:N} {status_icon} {status_header}
```

`{effort}` renders like `(high)` or empty when unsupported. Do **not** use `{peak_label}`.

`{status:N}` caps the label+title at N characters (0 = unlimited), exactly like `{ctx_bar:N}`.
All four status placeholders render **empty** (and suppress their whole line) when no incident
is active — the RSS feed is fetched only when a rendered line actually uses one of them.

### Fragment recipes (module → fragment)

| Module | Fragment |
|---|---|
| session header | `{sun} {c.time}[{time}]{r} {c.version}{version}{r} {c.model}{model}{r}{c.effort}{effort}{r} Ctx:{ctx} {c.ctx_percent}({ctx_percent}%){r}` |
| inline ctx micro (append to header) | `{ctx_micro}` |
| weather line | `{c.weather}{weather}{r}` |
| git line | `{c.path}{path}{r} {c.git_icon}(git)/{r}{c.branch}{branch}{r} ({c.output}+{added}{r},{c.input}-{removed}{r})` |
| usage full (two lines) | line A = `{usage_bars}` ; line B = `{usage_resets}` |
| usage micro line | `{usage_micro}` |
| usage compact line | `{compact_usage_micro}` |
| weather + compact usage on one line | `{c.weather}{weather}{r}  {compact_usage_micro}` |
| status indicator | `{status}` (or `{status:N}` to cap width) |
| status icon only | `{status_icon}` |
| status header banner | `{status_header}` — on its OWN line, ABOVE the line containing `{status}`; appears only when an incident is active |

If the user chose the inline-micro gauge **and** no `{sun}` glyph, drop the leading `{sun} `
from the header. Include `{sun}` only when the user opted into it.

### Usage display styles (pick exactly ONE — never mix)

- (a) **FULL BARS** → two lines: `{usage_bars}` then `{usage_resets}`.
- (b) **MICRO** → one line: `{usage_micro}`.
- (c) **COMPACT** → one line: `{compact_usage_micro}`.
- or **none**.

A config must use **at most one** of these. Never combine (a)+(b), (b)+(c), etc.

### Context-gauge forms (3) + composition rules

1. **INLINE MICRO** — append `{ctx_micro}` to line1.
2. **BIG AUTO-ALIGNED `{ctx_bar}`** — on its OWN line. It auto-sizes to align under the
   line1 segment that starts at `{effort}`. THEREFORE **line1 MUST contain `{effort}`**, and
   the bar line MUST include `{align_pad}` before the opening bracket:
   - without weather: `{align_pad}{c.ctx_bracket}▐{r}{ctx_bar}{c.ctx_bracket}▌{r}`
   - with weather: `{c.weather}{weather}{r}{align_pad}{c.ctx_bracket}▐{r}{ctx_bar}{c.ctx_bracket}▌{r}`
3. **FIXED `{ctx_bar:N}`** — fixed N cells, sits anywhere, no `{align_pad}`, e.g.
   `{c.ctx_bracket}▐{r}{ctx_bar:28}{c.ctx_bracket}▌{r}`
4. **Just text** — `{ctx}` and/or `{ctx_percent}`.

### Line ordering and disabling
Order lines sensibly: **header → weather/usage → git** (gauge line usually right after the
header). Assign active lines as `line1`, `line2`, … in display order.

**Status incident lines** follow a special rule: `{status_header}` MUST appear on its OWN
line placed ABOVE the line that contains `{status}`. Both lines vanish together when no
incident is active. The shipped config already contains a ready-to-enable pair — enable both
by renaming them from `_disabled_*` to `line*` keys:

```json
"_disabled_status_header": "{status_header}",
"_disabled_status_line":   "{status}"
```

Rename `_disabled_status_header` to `line_status_header` (or similar) and
`_disabled_status_line` to `line_status` — or insert them as `line2`/`line3` etc. in the
display order. Never place `{status_header}` on the same line as `{status}`.

To turn OFF an existing line **without deleting it**, rename its key to `_disabled_<name>`
(keys not starting with `line` are ignored). **Preserve every existing `_comment*` key.**
Do **NOT** alter the `colors` block.

---

## Step 5 — Show a unified DIFF

Present a unified diff of the old `statusline_config.json` vs the new one so the user sees
exactly what changes (templates, weather, emoji_width). Confirm `colors` is unchanged.

---

## Step 6 — Validate

Before rendering, check ALL of:

- JSON parses.
- Every `{placeholder}` used appears in the placeholder list above (no `{peak_label}`).
- `emoji_width` is `1` or `2`.
- At least one active line (a key starting with `line`).
- Usage style is not mixed (at most one of full/micro/compact).
- Big-bar rule: if any line uses bare `{ctx_bar}`, then line1 contains `{effort}` **and**
  that bar line contains `{align_pad}`.
- If any active line uses `{weather}` or `{sun}`, the `weather` block has a geocoded
  `name`/`latitude`/`longitude` (not the default placeholder).
- If any active line uses `{status}`, `{status:N}`, `{status_icon}`, or `{status_header}`:
  no special config is required (the `status` block has sensible defaults and is optional);
  the RSS fetch happens only when these placeholders appear in a rendered line. If
  `{status_header}` is used, confirm it is on a separate line placed ABOVE the line
  containing `{status}`.
- `colors` block is byte-for-byte unchanged; `_comment*` keys preserved.

Fix any failure before proceeding.

---

## Step 7 — Test-render with the sample input

Render the **new** config against `assets/sample_input.json` (bundled with this skill).
Point `STATUSLINE_CONFIG` at a **temp copy** of the new config so the user's live file is
untouched until they confirm — the live config is never written until Step 8's `commit`.

Use the **`statusline_py` path you resolved in Step 1** (from the helper's `locate` JSON)
wherever `<statusline.py>` appears below — the absolute path to the active renderer (the
deployed copy, e.g. `~/.claude/statusline.py`, or wherever `locate` reported). Do not
hardcode any particular machine's path. Write the candidate config to a temp path (e.g. the
OS temp dir), then:

**PowerShell:**
```
$env:STATUSLINE_CONFIG="<temp-config>"; Get-Content <skill>/assets/sample_input.json | uv run <statusline.py>
```
(fallback: replace `uv run` with `python`)

**bash:**
```
STATUSLINE_CONFIG=<temp-config> uv run <statusline.py> < <skill>/assets/sample_input.json
```
(fallback: `python3` instead of `uv run`)

A non-empty colored line = success. Show the rendered bar to the user.

---

## Step 8 — Confirm, then commit (history-aware)

Only on **explicit user confirmation** (after the Step 5 diff, Step 6 validate, and Step 7
test-render), install the new config. Otherwise iterate from Step 2. Never write the live
config without confirmation.

**Never write the live config directly.** Instead, write the fully-built new config object
(comments / `_disabled_*` / `colors` preserved exactly as required above) to a **temp file**,
then hand that file to the shared helper, which snapshots the about-to-be-replaced config and
records a human changelog entry next to the active config:

```
python statusline_io.py commit --config <config_path> --new <temp-new-config> \
    --skill statusline-config \
    --summary "<what changed, e.g. switched to three-line preset; added weather + big ctx bar>" \
    --why "<the user's intent in their words>" \
    --diff "<the key changes, e.g. the unified diff from Step 5>"
```

- `<config_path>` is the ACTIVE config resolved in Step 1.
- `<temp-new-config>` is the temp file holding your fully-formed new config (the same content
  you test-rendered in Step 7 — reuse that temp file).
- The helper validates the temp file parses as JSON before touching anything, snapshots the
  current config into `.statusline-config-history/YYYYMMDD-hhmm.json` next to the active
  config, writes the new bytes to the active config, and appends to
  `.statusline-config-history/YYYYMMDD.md`.

It prints `{"snapshot": <path or null>, "changelog": <path>, "config_path": <abs>}`. **Report
the snapshot and changelog paths to the user** so they know where the previous version and
the change note were saved.

---

## Preset templates (copy verbatim when a preset is chosen)

Set the listed `templates`, `weather`, and `emoji_width` fields; **keep the existing
`colors` block and all `_comment*` keys untouched**. (The presets below show
`emoji_width: 1` to match `examples/`; if the user's emoji render 2-wide, use `2`.)

For any preset that uses `{weather}`/`{sun}` you MUST first run **Step 3** geocoding and
fill the `weather` block's `name`/`latitude`/`longitude` with the resolved values before
writing — do not ship the placeholders shown below.

**Minimal (1 line):** (no weather)
```json
"emoji_width": 1,
"templates": {
  "line1": "{c.model}{model}{r}  {c.ctx_label}Ctx{r} {c.ctx_value}{ctx}{r} {c.ctx_percent}({ctx_percent}%){r} {ctx_micro}"
}
```

**Two-line (weather + compact usage):** (replace the `weather` placeholders with the
Step 3 geocoded city)
```json
"emoji_width": 1,
"weather": {
  "name": "<geocoded name>", "latitude": <lat>, "longitude": <lon>,
  "show_name": true, "show_icon": true, "show_temp": true,
  "show_humidity": true, "show_wind": true
},
"templates": {
  "line1": "{sun} {c.time}[{time}]{r} {c.model}{model}{r}{c.effort}{effort}{r}  {c.ctx_label}Ctx{r} {c.ctx_percent}({ctx_percent}%){r}",
  "line2": "{c.weather}{weather}{r}   {compact_usage_micro}"
}
```

**Three-line (context bar + git):** (replace the `weather` placeholders with the Step 3
geocoded city)
```json
"emoji_width": 1,
"weather": {
  "name": "<geocoded name>", "latitude": <lat>, "longitude": <lon>,
  "show_name": false, "show_icon": true, "show_temp": true,
  "show_humidity": false, "show_wind": false
},
"templates": {
  "line1": "{c.time}[{time}]{r} {c.version}{version}{r} {c.model}{model}{r}{c.effort}{effort}{r} Ctx:{ctx} {c.ctx_percent}({ctx_percent}%){r}",
  "line2": "{c.weather}{weather}{r}{align_pad}{c.ctx_bracket}▐{r}{ctx_bar}{c.ctx_bracket}▌{r}",
  "line3": "{c.path}{path}{r} {c.git_icon}(git)/{r}{c.branch}{branch}{r} ({c.output}+{added}{r},{c.input}-{removed}{r})"
}
```

**Four-line (full usage):** (no weather)
```json
"emoji_width": 1,
"templates": {
  "line1": "{c.time}[{time}]{r} {c.model}{model}{r}{c.effort}{effort}{r} Ctx:{ctx} {c.ctx_percent}({ctx_percent}%){r}",
  "line2": "{c.path}{path}{r} {c.git_icon}(git)/{r}{c.branch}{branch}{r} ({c.output}+{added}{r},{c.input}-{removed}{r})",
  "line3": "{usage_bars}",
  "line4": "{usage_resets}"
}
```

---

## Status config block

The `status` block is **optional** — if absent, all status placeholders use these defaults.
Add or edit the block to override specific keys; the rest remain at their defaults.

```json
"status": {
  "show_icon":             true,   // show the incident emoji in {status}
  "show_label":            true,   // show the status label (Investigating / Identified / Monitoring …)
  "show_title":            true,   // show the incident title text
  "show_count":            true,   // show "(+N)" hint when multiple incidents are active
  "show_header":           true,   // allow {status_header} to render
  "include_maintenance":   false,  // also surface scheduled / in-progress maintenance events
  "max_len":               48,     // global char cap for {status} (0 = unlimited)
  "max_age_hours":         48,     // only incidents updated within this many hours count (0 = no limit)
  "title": "⚠️ Claude have some issues"  // banner text shown by {status_header}
}
```

**Key notes:**

- `max_len` is the global cap for `{status}`; `{status:N}` overrides it per-line (0 = unlimited
  for that line).
- `include_maintenance: false` (default) hides scheduled/in-progress maintenance events; set
  to `true` to surface them alongside incidents.
- `max_age_hours: 0` disables the age filter — every parsed incident counts regardless of
  when it was last updated.
- A leading emoji in `title` is auto-spaced from the words; no manual spacing needed.
- The `status` block does **not** live inside `colors` — it is a sibling of `templates`,
  `weather`, and `emoji_width`.
- Color keys for the status indicator (`status_investigating`, `status_identified`,
  `status_monitoring`, `status_maintenance`, `status_default`, `status_title`,
  `status_count`, `status_header`) live in the `colors` block and are owned by
  `/statusline-theme`; do not touch them here.
