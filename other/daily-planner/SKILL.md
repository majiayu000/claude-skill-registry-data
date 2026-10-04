---
name: daily-planner
description: Build a modular daily-planner one-sheet for an e-ink tablet and deliver it via Folio. Use when the user asks for a daily plan, daily planner, "daily one sheet", morning sheet, day plan, or to send a planner to their reMarkable, Supernote, Kindle Scribe or other e-ink device. Interviews the user, pulls from connected tools (calendar, tasks, GitHub, weather), renders an e-ink-optimized PDF sized for the chosen device, and sends it with Folio.
---

# Daily Planner for e-ink tablets

Produce a single-page daily planner ("Daily One Sheet"), sized and styled for the
user's e-ink device, and deliver it through Folio. The sheet is **modular**: the user
picks which sections to include. Never invent data. Blank ruled space is expected in a
planner; fabricated events or tasks are not.

Work through the steps in order. Ask, do not assume.

## Step 1 - Folio must be connected

This skill delivers through the **Folio MCP**. Check the `mcp__folio__*` tools are
available (try `mcp__folio__list_targets`). If they are not:

> Say: "This needs the Folio MCP to send files to your tablet. Add it at
> **https://myfolio.so/mcp** (it lists devices and delivers the file), then run me
> again." Stop here.

## Step 2 - Figure out the user's location

Location drives the date phrasing, week/day numbers, weather and sunrise/sunset.
- Detect it (e.g. `curl -s https://ipapi.co/json/` gives city, region, timezone, lat/lon).
- If `mcp__folio__get_settings` returns a `timezone`, prefer it; the reference IP lookup
  can be wrong on VPNs.
- **Always confirm with the user**: "Looks like you're in <city>. Right?" Let them
  correct it. Use their confirmed city in the header and for weather.

## Step 3 - Pick the device (and its format)

Call `mcp__folio__list_targets`. Then:
- **reMarkable / Kindle present in Folio**: use the device's live `render` block as the
  source of truth for `page_mm`, stroke weights and guidelines.
- **More than one reMarkable** (or the user wants a different tablet): ask which one.
- **Supernote or Kindle Scribe** (Folio does not list these): use the matching profile in
  `reference/devices.json`. Confirm the exact model with the user (Paper Pro vs rM2,
  Scribe vs Paperwhite, Supernote A5X vs Nomad) because page sizes differ.
- Read `reference/devices.json` for the toolbar side + margin. **Keep the toolbar side
  clear** so the on-screen tool rail never covers content (reMarkable = left by default).

If the user wants it on several devices, render once per device (each has its own size).

## Step 4 - Ask what to include (modules)

Show the module menu from `reference/modules.md` and let the user choose. Offer the core
set (matches the reference sheet): **header, weather, schedule, priorities, follow-up,
notes**. Then suggest extras: **top-3, habit-tracker, time-block, water-health, meals,
workout, gratitude, reading (their Folio queue), quote, mood-energy, sleep, expenses,
daylight, brain-dump**. On a small screen (Kindle, Supernote Nomad) cap it at ~4 modules.

## Step 5 - Ask which connections to pull from

Ask what to pull data from, using whatever MCPs/tools are actually available this session:
- **Calendar** (Google Calendar) -> schedule events
- **Tasks** (Notion, Todoist) -> priorities
- **GitHub** (`gh` CLI or MCP) -> follow-up PRs/issues, assigned priorities
- **Email/Slack** -> follow-up threads owed a reply
- **Weather API** -> weather + daylight (keyed on the confirmed location)
- **Folio** (`mcp__folio__list_articles`) -> reading module

For anything not connected, just ask the user for that section's content. Do not block on
a missing integration; fall back to interviewing.

## Step 6 - Build the HTML from a data file

Put everything you gathered into one JSON file and run the builder. The builder holds all
the fixed design decisions (layout, fonts, e-ink rules, half-hour schedule, week/hourly
weather, blank write-on rows, notes box that fills, toolbar-clear per-page margins, lined
pages) so you only supply *data* and the sheet is reproducible from live data any time.

```
python3 <skill>/scripts/build_sheet.py <data.json> <out.html>
```

The JSON shape and every field are documented at the top of `scripts/build_sheet.py`
(and the look of each module in `reference/modules.md`). See
`reference/example-data.json` for a complete, working example to copy.

**Defaults (the house style - use unless the user says otherwise):**
- Weather `mode: "week"` (7-day outlook). Use `"hourly"` only if the user wants hour-by-hour.
- Schedule `start "09:00" end "17:00" step_min 30` (a half-hour work-day grid).
- `notes: true` (a notes box that fills to the footer) and `lined_pages: 1` (one ruled page).
- `meeting_notes` defaults to true: when the schedule has meetings, each one gets its own
  half-page ruled section (two per page) after the lined page. Set `false` to skip.
- `toolbar_side` from `devices.json` so the tool rail stays clear (reMarkable = left).
- `color: true` only on a colour device (reMarkable Paper Pro); leave false on mono.
- **Blank template**: omit `items` in priorities/followup and set `blank` (a row count),
  but still fill date, location, week/day and live weather.
- Map open-meteo `weather_code` to an icon/condition with the `WMO` table in `build_sheet.py`.

The e-ink rules (pure-black text, 30-40% form lines, whole-pixel strokes, no hairlines /
greys / gradients, everything inside `page_mm`) are already baked into `planner.css`;
do not override them. Write the JSON and HTML to the scratchpad, not the repo.

## Step 7 - Render to PDF

```
python3 <skill>/scripts/render.py <in.html> "<out.pdf>" <width_mm> <height_mm>
```
It uses headless Chrome/Chromium/Edge (falls back to WeasyPrint) and verifies the page
size matches the device before accepting the PDF. If both are missing it prints exactly
what to install.

**No Python available?** The scripts are only a convenience. Build the HTML yourself from
`reference/modules.md` (it is plain string assembly), then render with a direct headless
Chrome command - no Python needed, the CSS `@page` rule sets the exact size:
```
"<chrome>" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="<out.pdf>" "file://<abs path to in.html>"
```

Name the file the Folio way, in the user's **local date**:
`DD.MM.YYYY - Daily Plan - <Device label>.pdf` (e.g. `21.09.2026 - Daily Plan - reMarkable Paper Pro.pdf`).

## Step 8 - Deliver via Folio

- **reMarkable / Kindle**: `mcp__folio__create_upload` (run the returned `curl_command`
  to upload the PDF), then `mcp__folio__send_file` with the matching `target` (pass the
  `device_id` for Kindle). Poll `get_issue` if an issue id comes back.
- **Supernote / any device Folio does not list**: deliver via the **Dropbox** or
  **Google Drive** target the same way (Supernote syncs from cloud), or hand the user the
  PDF path. Tell them which folder it landed in.

Confirm to the user what was sent, to which device, and the file name. Keep it short.

## Notes
- Everything the skill needs is in this folder: `scripts/build_sheet.py` (data -> HTML),
  `scripts/render.py` (HTML -> PDF), `reference/example-data.json` (a full working data
  file to copy), `reference/devices.json`, `reference/modules.md`, `assets/planner.css`,
  `assets/weather-icons.md`.
- Recreate any day: edit a copy of `example-data.json` with live data, run `build_sheet.py`
  then `render.py`. `modules.md` is the reference for hand-building or custom layouts.
- The reference layout: header + full-width weather strip on top, then two columns
  (schedule timeline left; priorities + follow-up right), then a full-width notes box and
  a small footer. Fonts prefer Georgia / Helvetica Neue / Menlo and fall back to Google's
  Gelasio / Arimo / Cousine, loaded by `planner.css`.
