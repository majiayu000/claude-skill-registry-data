---
name: ui-review
description: Automated UI/UX review of a web page or app using the agent-browser CLI. Detects text overflow/clipping, awkward wrapping, horizontal scroll, overlapping elements, tiny tap targets, broken/distorted images, placeholder-text leakage, and responsiveness defects across common resolutions (mobile/tablet/laptop/desktop), then visually inspects screenshots. When run against a local dev server with the codebase available, maps findings back to source files and can fix them. Supports regression mode - save a baseline, later runs diff against it and only inspect what changed. Trigger with /ui-review [url], "/ui-review baseline", "/ui-review components" (shared component library audit), "review the UI", "check responsiveness", "find layout bugs", "text overflow check".
allowed-tools: Bash(agent-browser:*), Read, Glob, Grep
---

# ui-review

Audit a web page across common breakpoints with `agent-browser`, combining
programmatic in-page checks (this skill's `scripts/detect.js`) with visual
screenshot inspection. Report findings; fix only if the user asked.

## When to run this without being asked

Two situations warrant a standard pass even when nobody typed `/ui-review`:

- **You just edited a frontend page or component** and are about to report the
  task complete: run the standard sweep on the affected route(s) first. If the
  project's CLAUDE.md has a house rule like "screenshot + brand-test-matrix
  measurements before claiming a UI change works", this review is how you
  satisfy it — don't wait to be told.
- **The user reports a visual or layout bug**: run the review on that route as
  the first diagnostic step. detect.js + per-breakpoint screenshots localize
  the defect faster and more completely than manually eyeballing one
  screenshot.

## Inputs

- **URL**: from the user's message. If none given, detect a local dev server
  (try `agent-browser open localhost:3000` then 5173, 8080, 4200 — a page
  title confirms a hit) or ask.
- **Pages**: default to the given page only. If the user says "the whole app",
  snapshot the nav (`agent-browser snapshot -i -u`) and review the top ~5 routes.
- **Codebase**: if the URL is a local dev server and the project source is in
  the working directory, findings must be mapped to source files (see
  "Codebase mapping" below).
- **Auth**: if the page sits behind a login wall, log in once via
  `agent-browser fill` / `click` before the breakpoint loop. Don't close the
  browser mid-review — that drops the session and forces a re-login.

## Breakpoints

| Name | Viewport |
|---|---|
| mobile | 360 x 800 |
| tablet | 768 x 1024 |
| laptop | 1366 x 768 |
| desktop | 1920 x 1080 |

## Workflow

Work in a scratch dir for screenshots — create it first, and **always use
absolute paths for file arguments** (screenshot output, diff baselines):
agent-browser resolves relative paths against its own process cwd, not your
shell's, and fails with "No such file or directory". `DETECT` = this skill's
`scripts/detect.js` (resolve path relative to this SKILL.md).

```bash
SHOTS=<absolute scratch dir>/shots && mkdir -p "$SHOTS"
agent-browser open <url>
agent-browser wait --load networkidle

# Settle rendering before ANY measurement: freeze animations/transitions and
# wait for webfonts. Font swap and mid-flight transitions cause false
# clipped/wrapped/overlap findings and noisy pixel diffs. Re-run this after
# any reload or SPA navigation.
agent-browser eval "const s=document.createElement('style');s.textContent='*,*::before,*::after{animation:none!important;transition:none!important}';document.head.append(s);document.fonts.ready.then(()=>'settled')"

# If the page renders a list or table: before the breakpoint loop, select or
# load the row/item with the widest realistic content in the current data
# (most tags/badges, longest strings) — not the first row, not an empty state.
# Wrapping/overflow bugs concentrate in the widest row. (Synthetic-injection
# variants live in thorough mode's content-stress.md; this cheap version is
# always on.)

# Per breakpoint (repeat for each row of the table):
agent-browser set viewport 360 800
agent-browser wait 300                              # allow reflow/media queries
agent-browser eval --stdin < <DETECT>               # -> JSON defect report
agent-browser screenshot --full "$SHOTS/mobile.png"

# After all breakpoints:
agent-browser console | grep -E '^\[(warning|error)\]'  # unfiltered output buries real warnings in [debug]/[info] HMR noise
agent-browser errors                                # page errors
agent-browser network requests --status 400-599     # failed assets/API calls
agent-browser close
```

If the review target is (or includes) a specific new or changed interactive
element — a form field, a tag input, a modal — exercise its states as part of
the standard sweep; don't gate this behind thorough mode. Type an invalid then
a valid entry, confirm dependent controls (e.g. a Save button) enable/disable
correctly, open/close and re-check. Recipes:
[references/interaction.md](references/interaction.md). The full interaction
pack across the whole page remains a thorough-mode step.

Optional extras (newer agent-browser builds only). Unsupported builds respond
in either of two ways — generic help text, or a JSON error like
`{"error":"Unknown command: a11y","success":false}`. Both mean "unsupported":
do not parse them as results; skip the step and suggest `agent-browser
upgrade` in the report footer. (`vitals --json` works from 0.31.x; `a11y`
requires a newer build.)

```bash
agent-browser a11y --tags wcag2aa --json    # axe-core audit: contrast, labels, alt text
agent-browser vitals --json                 # CLS / LCP / INP
```

Notes:
- `agent-browser type <selector> <text>` requires the selector — called with
  text only, it silently does nothing.
- `eval --stdin` output is JSON-encoded **twice**: parsing once yields a
  string, not an object — parse that string again to get the report (e.g.
  `json.loads(json.loads(out))`). Categories:
  `viewportMetaMissing`, `horizontalScroll` + `offenders`, `clippedText`,
  `overlaps`, `tinyTapTargets`, `brokenImages`, `distortedImages`,
  `overflowingMedia`, `smallText`, `wrappedControls`, `placeholderText`,
  `fixedOverlays` (viewport % covered by fixed/sticky bars).
  Each entry has a readable selector.
- Only flag `tinyTapTargets` and `smallText` as real issues on mobile/tablet.
  Flag `fixedOverlays` as degraded when `pct` exceeds ~25 on mobile/tablet
  (sticky header + cookie banner + bottom nav eating the screen).
- detect.js pierces open shadow roots. Closed shadow roots and iframes are
  NOT reachable — if the page relies on them, say so in the report as
  uncovered surface instead of implying full coverage.
- If the app has a dark mode: `agent-browser set media dark`, re-screenshot at
  laptop size, and compare — `agent-browser diff screenshot --baseline
  shots/laptop.png -o shots/dark-diff.png` highlights unstyled regions.
- For real-device fidelity on mobile, `agent-browser set device "iPhone 14"`
  can replace the raw mobile viewport.

## Regression mode (baselines + diffs)

Baselines live in the reviewed project at `.ui-review/<page-slug>/` (slug from
the URL path, `root` for `/`). Committable, so CI and teammates share them.

**Save a baseline** (`/ui-review baseline [url]`): run the normal per-breakpoint
loop, but store artifacts instead of writing a report:

```
.ui-review/<page-slug>/
  mobile.json  mobile.png       # detect.js output + full screenshot
  tablet.json  tablet.png       # ...one pair per breakpoint
  snapshot.txt                  # agent-browser snapshot > snapshot.txt (desktop)
```

Do the visual inspection once here — a baseline with known defects should have
them listed in `.ui-review/<page-slug>/KNOWN.md` so later runs don't re-report
them.

**Masking dynamic regions**: pages with timestamps, live counters, ads, or
carousels pixel-diff "changed" on every run forever — and a check that always
fails gets ignored. If `.ui-review/<slug>/ignore.txt` exists (one CSS selector
per line), hide each match before **every** screenshot, in baseline and
compare runs alike:

```bash
agent-browser eval "document.querySelectorAll('<selector>').forEach(e=>e.style.visibility='hidden')"
```

`visibility` rather than `display`, so layout doesn't shift. When a compare
run keeps flagging an intentionally-live region, suggest adding its selector
to ignore.txt.

**Compare** (default when a baseline exists): per breakpoint —

```bash
agent-browser set viewport 360 800
agent-browser eval --stdin < <DETECT>          # -> current JSON
agent-browser screenshot --full "$SHOTS/mobile.png"
agent-browser diff screenshot --baseline "<project abs path>/.ui-review/<slug>/mobile.png" -o "$SHOTS/mobile-diff.png" -t 0.2
```

Then triage cheaply, in order:

1. Diff the two JSONs yourself (baseline vs current) — new entries are
   regressions, vanished entries are fixes. This is plain text, costs almost
   nothing.
2. If the pixel diff reports no/near-zero change AND the JSON diff is empty:
   **skip the Read of that breakpoint's screenshot entirely** — that's the
   token saving. Say "unchanged" and move on.
3. Only when pixels changed: Read the `-diff.png` (changed regions are
   highlighted) and the current screenshot, judge whether the change is a
   regression or an intended edit.
4. `agent-browser diff snapshot --baseline .ui-review/<slug>/snapshot.txt`
   catches content/structure changes screenshots blur over.

Report only deltas: `regressed / fixed / unchanged` per breakpoint, plus
anything in KNOWN.md that got fixed (suggest pruning it). After the user
confirms current state is good, offer to refresh the baseline.

If baselines exist for other pages in this project but not for the requested
URL, the report must state it as its own finding — "no baseline exists for
this route — it has never been reviewed" — before falling back to a fresh
standard review. Untested surface must be visible, not indistinguishable from
"reviewed and clean".

To run baseline + compare automatically on frontend diffs (pre-commit hook or
CI job), see [references/ci.md](references/ci.md).

## Thorough mode (deep QA scenarios)

`/ui-review thorough [url]` (or "deep review", "full QA"). Run the standard
sweep first, then pick scenario packs by what the page actually is — don't run
everything everywhere:

- [references/interaction.md](references/interaction.md) — focus/keyboard,
  modals, loading/empty/error states, forms, silent network failures,
  double-submit, invisible overlays. For any app with forms, modals, or API
  calls.
- [references/content-stress.md](references/content-stress.md) — long-string
  and i18n injection, 200% zoom (≡ 640x512 viewport) and 320px reflow (WCAG
  1.4.4/1.4.10), list-size extremes (0/1/1000, page-9999), pluralization and
  template leaks, truncation correctness. For anything rendering user data.
- [references/rendering.md](references/rendering.md) — dark-mode contrast and
  baked-white images, prefers-reduced-motion, sticky/fixed occlusion, hi-DPI
  blur, fonts (FOIT/tofu/metric jump), landscape phones, 100vh/safe-area. For
  themed or animated UIs.

Rules:
- Stress injections mutate the DOM — run them last on each page and reload
  between packs.
- Some checks are static-only in headless Chrome (iOS 100vh, safe-area,
  scrollbar gutter, cross-engine CSS): report as "flagged, verify on
  device/engine", never as confirmed failures.
- Within each pack, run the top-tier recipes first; go deeper only where the
  page type warrants it.

## Component mode (shared UI primitives)

`/ui-review components [url]` — audit the shared component library directly
instead of one page at a time. A defect in a shared primitive (a Button
missing `white-space: nowrap`, a Badge that clips past 13 characters) has
blast radius across every page that uses it; the page-by-page workflow only
catches it by luck, once per page.

- If the project has a Storybook or component-showcase route, review that:
  open each story/section and run the standard per-breakpoint detect +
  screenshot loop against it.
- Otherwise, synthesize a temporary kitchen-sink page: one scratch route (or
  a static HTML file the dev server can serve) rendering every variant and
  size of the app's core primitives — buttons, badges, inputs, tags — each
  with both a short label and a realistically long one. Run the standard
  sweep against it, then delete the scratch page.

Report findings per component (`file:line` of the component source), not per
page.

## Visual inspection (mandatory)

The JS checks can't judge aesthetics. Read every screenshot with the Read tool
and look for what only eyes catch:

- Awkward line wrapping: single-word orphans in headings, buttons wrapping to
  two lines, labels breaking mid-word.
- Truncation that loses meaning (ellipsis hiding the important part).
- Misalignment: inconsistent gutters, off-grid cards, uneven spacing between
  siblings.
- Content cut off at the fold or behind fixed headers/footers.
- Elements that overlap visually even if detect.js missed them (transforms,
  canvas, absolutely positioned art).
- Contrast that looks illegible, images stretched/squashed, empty states that
  render blank.

## Codebase mapping

When the reviewed app's source is available locally, every finding gets a
source location, not just a DOM selector:

1. Take the finding's class name, id, or visible text from the selector.
2. Grep the project source (components, templates, CSS/SCSS, Tailwind
   classes) for it. Utility-class-only selectors: grep the visible text
   instead.
3. Report `file:line` next to the finding.
4. If the user asked for fixes: fix in source (CSS/component), let the dev
   server hot-reload, re-run the same breakpoint's detect + screenshot to
   confirm the finding is gone. Fix the **broken** tier first, then move down.

## Report

One section per breakpoint, ranked by severity. For each finding:
`[severity] element — what's wrong — file:line (if mapped) — suggested fix (one line)`.
Severity: **broken** (content unusable/unreadable) > **degraded** (works but
looks wrong) > **polish**. End with console/page errors and failed network
requests if any. If everything passes, say so plainly — don't invent findings.

Multi-page ("whole app") sweeps: when the same selector pattern (identical
class list, or the same component file via codebase mapping) produces the same
finding category on 3+ pages, collapse them into ONE finding attributed to the
shared component/file, with the affected pages listed under it. One root
cause, one row — N duplicate per-page rows obscure that it's a single fix.

Besides the chat summary, always write the full report to
`.ui-review/<page-slug>/REPORT.md` in the reviewed project (same folder the
baselines use) so it can be committed, diffed, and shared. Structure:

```markdown
# ui-review: <url> — <date>
Mode: standard | thorough | compare · agent-browser <version> · ui-review <version>

## Summary
<counts by severity, one-line verdict>

## <breakpoint>  (repeat per breakpoint)
| Sev | Element | Issue | Source | Fix |
...

## Console / network
...
```

Reference screenshots by relative path (`./mobile.png`) when they're kept in
the same folder. In compare mode the report lists regressed/fixed/unchanged
instead of re-describing known findings.

Alongside REPORT.md, write `.ui-review/<page-slug>/report.json` — the
machine-readable summary the CI gate in [references/ci.md](references/ci.md)
reads:

```json
{ "url": "...", "date": "...", "mode": "standard",
  "counts": { "broken": 1, "degraded": 2, "polish": 0 },
  "findings": [ { "severity": "broken", "breakpoint": "mobile",
    "category": "horizontalScroll", "selector": "div.hero",
    "source": "src/components/Hero.css:12", "fix": "max-width:100%" } ] }
```
