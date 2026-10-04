---
name: html-export
version: 1.0.0
description: '[Document Processing] Use when a workflow step or the user asks for an HTML page, deck, mockup or animation export: PNG, vector PDF, MP4/GIF. --to={png|pdf|mp4|gif}.'
disable-model-invocation: false
---

## Quick Summary

**Goal:** Turn a local HTML file into PNG screenshots with a page-error and blank-capture check, a vector PDF, an MP4 or a GIF, through one entry point that reports the result as an exit code.

**Workflow:**

1. **Pick a target** — `--to=png` (render evidence), `--to=pdf` (print or slides), `--to=mp4` / `--to=gif` (deterministic animation recording)
2. **Check setup** — dependencies are opt-in and skill-local; a missing one exits `3` with the setup commands
3. **Export** — `node .claude/skills/html-export/scripts/export.cjs --to=<target> <input...> [options]`
4. **Read the exit code first** — then `report.json` / `frames.json`, then the output; a written file is never proof on its own. A reused `--out` keeps earlier outputs: only the files this run's manifest names belong to it — `report.json` `files[]` (png), `report.json` `output` (pdf), `frames.json` `output` (mp4/gif)

**Key Rules:**

- `--to` is required; there is no default target.
- Nothing is ever installed on the user's behalf. Exit `3` means `NOT VERIFIABLE` plus a setup pointer.
- Render only HTML the project or the user produced; anything fetched or untrusted only with `--offline` (see [Trust](#trust)).
- The HTML stays canonical. Fix the page or pick the right selector; never restructure HTML for the exporter.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# html-export

Agents and users may invoke this skill directly, and other skills may run the script by path. Either way the exporter only renders; it never installs, commits or publishes anything.

## Setup (opt-in only)

Needs Node.js 20 or newer and, in the skill's own `node_modules`, Playwright 1.55.1 or newer (never a parent project's copy). Run these from the project root, only when the user asks; the exporter prints them on exit `3` and never runs them.

```text
# Playwright and pdf-lib go into the skill folder; Chromium goes into Playwright's per-user browser cache
macOS/Linux shell:  (cd .claude/skills/html-export && npm install && npx playwright install chromium)
Linux system libs:  (cd .claude/skills/html-export && npx playwright install --with-deps chromium)
Windows PowerShell: Push-Location .claude/skills/html-export; npm install; npx playwright install chromium; Pop-Location
Windows cmd:        pushd .claude\skills\html-export && npm install && npx playwright install chromium && popd

# ffmpeg, only for mp4/gif (the build must include the libx264 encoder)
Windows:            winget install Gyan.FFmpeg
macOS:              brew install ffmpeg
Linux (Debian/Ubuntu): sudo apt-get install ffmpeg
```

Install from inside the skill folder, never with `npm install --prefix`: run from a project with its own `package.json`, that form makes npm add the host project as a dependency of the skill (it rewrites the skill's `package.json` and links the project root into its `node_modules`).

ffmpeg and ffprobe are looked up only in the absolute directories on `PATH`, never in the current directory.

| Environment variable  | Effect                                                                                                                                                                  |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `HTML_EXPORT_FFMPEG`  | Pins the ffmpeg build instead of the `PATH` lookup. Must be an **absolute** path; on Windows it must also name a `.exe` or `.com` file (never a `.bat` / `.cmd` wrapper). Otherwise exit `3` |
| `HTML_EXPORT_FFPROBE` | The same for ffprobe, with the same rules                                                                                                                              |
| `HTML_EXPORT_DEBUG=1` | Prints the stack trace of an unexpected error to stderr. Set it when an exit `1` names an unexpected error, and quote the stack                                         |

**Removing the skill.** Deleting the skill folder removes Playwright, pdf-lib and every other npm dependency. Chromium stays in Playwright's per-user browser cache (or under `PLAYWRIGHT_BROWSERS_PATH` when that is set); to remove it too, first run `npx playwright uninstall` from inside the skill folder — it removes only the browsers no other Playwright installation still uses — then delete the folder. Regenerate the mirrors afterwards.

## Trust

Render only HTML that the project or the user produced: its own decks, mockups, reports and drafts. For anything fetched from the web or otherwise untrusted, always pass `--offline`. Chromium runs without its OS sandbox, and a page can embed any local file the user can read (for example through an iframe) into the PNG, PDF or video. `--offline` blocks the page's network traffic; it is not a sandbox, and an embedded local file still lands in the output.

A page the project produced stays trusted when it uses fetched files only as verified images through `<img src>` (an SVG loaded as an image runs no script and loads nothing) and loads no remote script, frame or media; remote web fonts through CSS are fine. Inlining fetched SVG markup, or embedding it through `<object>`, `<iframe>` or `<embed>`, makes the page untrusted: pass `--offline`.

## Usage

```bash
node .claude/skills/html-export/scripts/export.cjs --to=png page.html
node .claude/skills/html-export/scripts/export.cjs --to=pdf deck.html --page=1920x1080
node .claude/skills/html-export/scripts/export.cjs --to=mp4 intro.html --duration=4
node .claude/skills/html-export/scripts/export.cjs --help
```

A value flag takes `=value` or the next argument; `--slides` takes only the attached form, so `--slides <css>` reads the selector as an input file. Quote a selector with brackets or spaces in every shell: single quotes in bash, zsh and PowerShell (`--slides='[data-state]'`; unquoted, zsh treats the brackets as a glob), double quotes in cmd.exe.

The dispatcher checks every flag and input before any dependency or target runs, so a bad command exits `2` even when nothing is installed: an input, or a pdf `--order` entry, that is not an `.html` or `.htm` file (any letter case; a positional pdf input may also be a folder), an unknown flag or one the target rejects, `--timeout` or `--scale` not above 0, `--timeout` above 2147483647 (about 24.8 days), a malformed `WxH`, a size listed twice in `--viewport`, or an empty `--slides=`. Three checks need the page, so they run after rendering starts and stop the run at once: a `--slides` selector the browser cannot parse (png, pdf), a pdf selector that matches nothing, and a video with no duration. The video `--keep-frames` folder check runs after the dependency checks, before rendering.

### Generic options

| Option                   | Meaning                                                                                                                                                                                                                                                                                | Applies to |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `--out=<dir>`            | Output directory. Default: `<project>/tmp/html-export/<YYMMDD-HHmm>-<first input name>/`                                                                                                                                                                                               | all        |
| `--viewport=<WxH[,WxH]>` | Viewport size; a comma list only for png                                                                                                                                                                                                                                               | all        |
| `--slides[=<css>]`       | Navigate slides or screens; bare form uses the default selector `section.slide[data-slide-id], [data-export-slide]`                                                                                                                                                                    | png, pdf   |
| `--page=<WxH>`           | PDF page size in CSS pixels, print mode only                                                                                                                                                                                                                                           | pdf        |
| `--scale=<n>`            | Device scale factor, greater than 0                                                                                                                                                                                                                                                    | all        |
| `--timeout=<ms>`         | Timeout in milliseconds (default 30000, at most 2147483647) for load, fonts and each step, and for every call into the page: the `window.__ready` wait, evidence collection, slide navigation, pdf slide isolation, and the video duration, ready, `__seek` and per-frame calls. A page that hangs one of them becomes a logged page fault. It never bounds the browser's own start or stop (see below) | all        |
| `--offline`              | Take the page offline: besides the input itself, only local `file:` URLs load (empty or `localhost` host). Every other request, including `file://<host>/`, and every WebSocket is refused and listed in `blocked[]`; WebTransport, speculation-rules prefetch and service workers are also blocked, silently. The failure message Chromium logs for a blocked request or WebSocket is not a page error; code that then throws still is one | all        |
| `--allow-errors`         | Accept page errors; never a blank capture or a failed step                                                                                                                                                                                                                             | all        |
| `--self-check`           | Render the known-good fixture first; png only                                                                                                                                                                                                                                          | png        |
| `--help`                 | Print usage and exit `0`                                                                                                                                                                                                                                                               | all        |

**Browser start and stop.** Launching Chromium, creating its context and page, setting up the `--offline` route, and closing the browser each get `max(--timeout, 30000)` ms, the same budget as the dependency check, so a short `--timeout` never fails a slow launch. A start call that runs over fails that input as a tool fault (`pageFault: false`, message `<call> did not finish within N ms; the browser is not responding (a busy or broken machine, not the page)`). A close that runs over prints `Warning: the browser did not close within N ms; ...`, the run continues with its exit code unchanged, and the exporter exits on its own instead of hanging; that browser is stopped when it exits.

### `--to=png` — render evidence

Target flag: `--full-page` (opt-in). Inputs: one or more `.html` / `.htm` files; `--self-check` may run with no input to check only the verifier.

- Default viewports `1440x900,390x844`. Each capture is **viewport-only**; `--full-page` adds `<name>@<WxH>-full.png` with the whole scrollable document and its own blank check. `--full-page` with `--slides` exits `2`.
- Writes `<name>@<WxH>.png`, or with `--slides` one `<name>@<WxH>-s<NN>.png` per item, plus `report.json`.
- Log and continue: a failed open, navigation, capture or timeout on one input, viewport or slide goes to `report.json` `failures[]` (each entry with `pageFault`) and stderr, and the rest of the batch still runs. A page that fails to open still lists the errors it raised before that in `errors[]`.
- Exit `4` on a page-caused failure, a blank capture, or a page error (unless `--allow-errors`), even when nothing was captured; a `--slides` selector that matches nothing counts as blank. Exit `1` only for a tool fault with none of those (browser start, a write error) or when `--self-check` reports `verifier broken`. A `--slides` selector the browser cannot parse exits `2` (`report.json` `usageError`). `--page` is a usage error; use `--viewport`.

### `--to=pdf` — vector PDF

Target flag: `--order=<file>` — one `.html` / `.htm` path per line (blank and `#` lines skipped, relative paths resolved against the file's folder). Inputs: HTML files or directories (natural order), or `--order`, never both.

- **Print mode** (default): the page's print CSS. Page size: `--page=WxH` wins over a CSS `@page { size }` rule; without `--page` the CSS size applies, else Chromium's default.
- **Slides mode** (`--slides[=<css>]`): running animations are finished, then each navigated item prints as one viewport-sized page with screen media. `--page` with `--slides` is a usage error; size pages with one `--viewport=WxH`.
- Several inputs, or slides mode, merge into `<out>/<name>.pdf` with pdf-lib. stdout carries only the PDF path; `report.json` (errors, `failures[]`, navigation, `blocked[]`) is written beside it.
- Log and continue: a failed input or slide is recorded (with `pageFault`) and skipped, and the PDF holds every page that printed. Exit `4` when the page caused a failure or reported errors (unless `--allow-errors`), even if nothing printed (then no PDF is written). Exit `1` when only the tool failed, or nothing printed without a page fault; the pages that printed are still written. A merge or PDF-write failure exits `1` with `report.json` `fatal`. A slides selector that cannot be parsed or matches nothing exits `2` with no PDF (`report.json` `usageError`). `--self-check` is rejected.

### `--to=mp4` / `--to=gif` — deterministic recording

Target flags: `--fps=<1-60>` (default 30 for mp4, 15 for gif), `--duration=<seconds>`, `--audio=<local file>` (mp4 only, AAC, trimmed to the shorter stream), `--gif-width=<px>` (gif only, default 960), `--keep-frames`. Input: exactly one HTML file.

- **Units differ:** `--duration` is in **seconds**; the page hook `window.__duration` is in **milliseconds**. `--duration` wins; with neither, the run exits `2` and writes nothing.
- Default viewport `1920x1080`, one viewport only. `--slides`, `--page` and `--self-check` are usage errors. MP4 is libx264 at `-crf 18`; a build without libx264 exits `3`.
- The recorder sets `window.__recording` before page scripts run and hides elements marked `data-export-hide`. Contract: [`references/animation-recording.md`](references/animation-recording.md).
- Writes the video plus `frames.json` (`status` `ok` / `page-errors` / `failed`, `exitCode`, `failure` with `pageFault`, `pageErrors`, `noMotion`, a sha256 per frame). Page errors, including a timer or animation-frame callback that throws while the recorder advances the clock, are recorded and recording continues: exit `4` with the files written (`0` with `--allow-errors`). A page that never loads or becomes ready, a `__seek` that throws, a page that breaks the recorder's setup or animation pinning, or any in-page call or frame step that exceeds `--timeout` exits `4` with no video. A tool fault (browser start, a write error, ffmpeg) exits `1`, or `4` when the page also reported errors that `--allow-errors` does not accept. Identical frames print a warning and set `noMotion` (exit stays `0`).
- `--keep-frames` also keeps every frame in `<out>/frames/`. An existing `frames/` is reused only when it is a real directory holding nothing but the recorder's own frame files; otherwise the run exits `2` and touches nothing. Frames are captured into a work folder and replace the earlier frame files only after the video encoded, so a failed recording or encode leaves an earlier `frames/` as it was. A failed run never writes the video path, and an earlier video stays in place; `frames.json` is rewritten by every run except a usage error.

## Producer selectors

| Producer             | png                                                     | pdf                                                                |
| -------------------- | ------------------------------------------------------- | ------------------------------------------------------------------ |
| presentation-builder | `--slides` (default selector)                           | `--page=1920x1080` (print mode)                                    |
| feature-presentation | `--slides=section.deck__slide`, or `--slides` (default) | `--page=1920x1080` (print mode), or `--slides=section.deck__slide` |
| pbi (mockup mode)    | `--slides='[data-state]'` (every screen)            | —                                                                  |

Any other page can mark its items with `data-export-slide`. feature-presentation slides carry both `slide` and `deck__slide` with a `data-slide-id`, so its existing `section.deck__slide` selector and the default selector find the same slides.

## Exit codes

| Exit | Meaning                                                                                                                                                                               |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`  | Export succeeded and the target's checks passed                                                                                                                                       |
| `1`  | Tool fault, and the page did nothing wrong: the browser did not launch or start in time — including a dependency-check launch that timed out (the message says `timed out`: a busy or broken machine, not a missing browser) — a write error, a pdf merge failure, an unexpected exception (set `HTML_EXPORT_DEBUG=1` for its stack), png `verifier broken`, an ffmpeg failure (a failed GIF pass keeps the MP4 when that name is free). A page fault, blank png capture or unaccepted page error in the same run makes it `4` |
| `2`  | Usage error: missing or unknown `--to`, unknown or rejected flag, bad input or value, an input or pdf `--order` entry that is not an `.html` / `.htm` file (a positional pdf input may also be a folder), `--timeout` above 2147483647; a png or pdf `--slides` selector the browser cannot parse; pdf slides selector matching nothing; video with no duration; `--keep-frames` on a foreign `frames/` |
| `3`  | Dependency missing: Node older than 20, Playwright older than 1.55.1 or absent, Chromium not installed or failing to launch for any reason other than a timeout (for example a missing system library), pdf-lib for a merge, ffmpeg with libx264, or an `HTML_EXPORT_FFMPEG` / `HTML_EXPORT_FFPROBE` that is relative or, on Windows, not a `.exe` / `.com` file |
| `4`  | The page is wrong, even when nothing was produced: page errors (unless `--allow-errors`), a blank png capture, or a page-caused failure (`pageFault: true`) — never loads, never ready, fonts time out, navigation error, an in-page hang, a `__seek` that throws or times out, a page that breaks the video recorder's setup or animation pinning |
| other | Interrupted, for example `130` after Ctrl+C: no verdict and possibly no `report.json`. A video run can leave `<out>/.video-work-*` folders; the recorder removes them on a best-effort basis, and any that remain are safe to delete |

## Calling from other skills

Invoke the skill, or run `node .claude/skills/html-export/scripts/export.cjs ...` by path. Every caller follows the same rule:

- **Exit `0`** → evidence, only within the scope below.
- **Exit `4`** → fix the page and re-run (fix loop); `report.json` or `frames.json` names each failure.
- **Exit `3`** → mark the check `NOT VERIFIABLE` with a one-line pointer to `/html-export` setup. Never run install commands on the user's behalf.
- **Exit `1` / `2`** → tool failure: quote stderr, mark `NOT VERIFIABLE`. Never count it as a design defect or a pass.
- **Any other exit** (such as `130` after an interrupt) → handle it like `1` / `2`.
- **Evidence files** → only those the run's manifest names (`report.json` `files[]` for png, `output` for pdf, `frames.json` `output` for video); a reused `--out` still holds earlier outputs.

## What exit 0 proves

Without `--allow-errors`:

- **png:** each input loaded at each requested viewport; no console error or uncaught exception from load through the last capture; no step failed; every capture held visible text, an image, an SVG or a canvas; with `--slides`, every matched item was shown and captured.
- **pdf:** every input and slide printed into the PDF and no page error occurred.
- **mp4/gif:** the video was encoded from frames captured on the recorder's controlled clock, with no page error.

It does **not** prove the page looks right, that interaction works, anything below the first viewport (unless `--full-page`), other browsers, or that remote assets load. Open the output and judge it; interactive checks stay `NOT VERIFIABLE` unless exercised another way.

## Resources

- [`references/verification.md`](references/verification.md) — png evidence, `report.json` fields, failure signatures, offline rule, self-check, known limits
- [`references/deck-export.md`](references/deck-export.md) — pdf print vs slides mode, page size, per-producer commands, ordering, merge, pdf `report.json`
- [`references/animation-recording.md`](references/animation-recording.md) — the recording contract: time rule, `window.__ready` / `__seek` / `__duration` / `__recording`, `data-export-hide`, `frames.json`
- Tests: `node .claude/skills/html-export/tests/run-tests.cjs` (browser cases report `ENVIRONMENT-BLOCKED` when Chromium or ffmpeg is absent)

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** export HTML to PNG, PDF, MP4 or GIF through `scripts/export.cjs --to={png|pdf|mp4|gif}` and report the result by exit code.

**IMPORTANT MUST ATTENTION** read the exit code before the output — a written file proves nothing; exit `4` still writes files; only the run's manifest (`report.json` / `frames.json`) names this run's outputs
**IMPORTANT MUST ATTENTION** never install dependencies on the user's behalf — exit `3` is `NOT VERIFIABLE` plus a setup pointer
**IMPORTANT MUST ATTENTION** exit `1`/`2` is a tool failure, never a design defect or a pass
**IMPORTANT MUST ATTENTION** `--duration` is seconds, `window.__duration` is milliseconds
**IMPORTANT MUST ATTENTION** the HTML stays canonical — never restructure it for the exporter
