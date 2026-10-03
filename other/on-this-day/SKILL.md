---
name: on-this-day
description: Fetch the official Wikimedia On This Day feed for a given date, then turn it into a polished daily history brief or a refined macOS-style web app. Use when Codex needs reliable same-day historical events, births, deaths, or holidays without inventing facts or losing the presentation layer.
---

# On This Day

Use this skill when the user wants a same-day historical briefing, a source-linked digest, or help building and refining the matching macOS-style web app.

Use `on-this-day-bar` for the native menu bar app.

Default product shapes:
- a desktop-first web app that feels at home on macOS, with glass panels, a date picker, curated historical cards, strong source linking, and resilient fallback behavior
- a deterministic helper that renders a compact brief or JSON snapshot from the official Wikimedia feed

## Quick Start

1. Decide the exact day, timezone, and feed slice the user wants.
2. Prefer the official Wikimedia Feed API endpoint for the day:
   - `https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/{MM}/{DD}`
3. Run `bash scripts/run_on_this_day.sh doctor` before editing the web app or checking local preview readiness.
4. Run `bash scripts/run_on_this_day.sh inspect` before changing `apps/on-this-day/`.
5. Use `bash scripts/run_on_this_day.sh fetch --date 2026-03-27 --type selected --limit 5` for a deterministic local snapshot.
6. Use `bash scripts/run_on_this_day.sh run` when you need the web app preview server and browser handoff. If the port cannot be bound, the runner falls back to opening `index.html` directly.
7. If the user wants the native menu bar app, hand them to `on-this-day-bar`.
8. Return either an `on-this-day-brief`, a `history-day-digest`, or an `app-refresh-plan`, depending on the request.

## Accepted Inputs

- a date like `2026-03-27` or a relative date like `today`
- the user timezone when the date should respect local midnight boundaries
- a slice such as `selected`, `events`, `births`, `deaths`, or `holidays`
- a preferred language, with English as the default when none is given
- a limit for how many entries should be shown
- whether the user wants a quick digest, a richer editorial brief, or app changes
- whether the result should favor concise fact cards, links, or visual presentation

## Output Artifact

Primary artifacts:
- `on-this-day-brief`
- `history-day-digest`
- `app-refresh-plan`

Default `on-this-day-brief` sections:
- Date and timezone basis
- Curated entries with years
- Why each entry is interesting now
- Source links

Default `history-day-digest` sections:
- Day summary
- Selected highlights
- Secondary categories like births, deaths, or holidays
- Editorial note or takeaway
- Source and fallback notes

Default `app-refresh-plan` sections:
- User-facing goal
- Data source and fetch behavior
- UI changes
- Empty, loading, and error states
- Validation notes

## Workflow

### Lock The Date First

- Resolve relative dates like `today` against the user's timezone.
- Use absolute dates in the final output when there is any ambiguity.
- If the request is date-sensitive, say which date you used.

### Prefer Official Data

- Use the official Wikimedia Feed API instead of copying facts from arbitrary recap sites.
- Prefer the `all` feed when building UI so counts and category switching stay in sync.
- Use `selected` when the user wants a tighter editorial cut.
- Keep links back to the underlying Wikipedia pages whenever possible.

### Use The Helper Script When Precision Matters

- Run `python3 scripts/fetch_on_this_day.py --date YYYY-MM-DD --type selected --limit 5` for a clean deterministic brief.
- Use `--format json` when another tool or app needs structured output.
- If `selected` is empty, the helper script falls back to `events` and makes that fallback explicit.

### Shape The Presentation

- Default to a polished Mac-style reading experience, not a dump of bullets.
- Keep hierarchy clear:
  - date and source confidence first
  - strongest entries next
  - secondary context after that
- Use restrained motion and strong spacing instead of generic card spam.
- Preserve a desktop-first macOS feel when editing the web app in `apps/on-this-day/`.

### Web App Workflow

- Open `apps/on-this-day/README.md` before editing the browser surface.
- Prefer `bash scripts/run_on_this_day.sh run` over a manual `python3 -m http.server 4173` preview. When the machine cannot bind the preview port, the runner falls back to opening `index.html` directly.
- Use `bash scripts/run_on_this_day.sh fetch --date YYYY-MM-DD --type selected --limit 5` after changing feed logic, date handling, or digest formatting.
- Keep the static app desktop-first and honest about live versus cached data.

### Handle Failure Honestly

- If the live feed fails, prefer cached data in the web app and label it clearly.
- If no cached snapshot exists, say the request failed instead of inventing entries.
- Do not paraphrase historical claims as certain if the source could not be fetched.

### Mac Product Shapes

- Prefer a polished web app with:
  - faux macOS window chrome
  - `Today`, previous, next, and random-day navigation
  - a date picker
  - segmented category controls
  - a spotlight card and a scrollable historical timeline
- Keep the main layout readable between 1280 px desktop widths and narrower laptop screens.
- Use local storage for last date, last category, and cached day snapshots so the app feels dependable.

### Safety Boundaries

- Do not invent historical facts, dates, or source links.
- Do not attribute a claim to Wikipedia if you did not fetch it from the official feed or linked page.
- Keep present-day commentary separate from historical event text.
- Be careful with violent or tragic entries: keep the tone factual, not sensational.

## Example Prompts

- `Use $on-this-day to fetch today's official On This Day feed in Singapore and turn it into a polished daily history brief with five entries and source links.`
- `Use $on-this-day to build a macOS-style day browser that lets me switch between curated events, births, deaths, and holidays for any date.`
- `Use $on-this-day to give me the most interesting March 27 historical events, explain why they matter, and keep the output grounded in the official Wikimedia feed.`
- `Use $on-this-day to refine the web app UI, improve empty and error states, and keep the design professional on Mac.`

## Resources

- `scripts/run_on_this_day.sh`: local doctor, inspect, fetch, serve, run, and stop helper for `apps/on-this-day`.
- `scripts/fetch_on_this_day.py`: deterministic CLI helper for the official On This Day feed
- `references/product-spec.md`: product family spec, fetch model, fallback states, and visual direction
- `references/project-map.md`: web app target map, main files, and preview notes
- `../../apps/on-this-day/`: the matching web app codebase
