---
name: widgets
description: Give an artifact a small glanceable home-screen widget (one number, next event, a few KPIs) that refreshes itself from a script
---

# Building Widgets

A widget is a small card on the user's home screens — the agent's home page, the app home, and the companion iOS app's home screen. It answers one question at a glance (what's next, how am I doing today, is the number up or down) and keeps itself fresh **without a conversation**: a script you write re-generates it, and the platform renders it everywhere.

Widgets belong to artifacts. An artifact under `/workspace/artifacts/<slug>/` is one unit that can expose a **dashboard** (a `start` script — a destination the user opens), a **widget** (a `gamut.widget` block and usually a `widget` script — a glance), or both. A dashboard with a widget shows the widget in place of its screenshot on the home page, and tapping the widget opens the dashboard. A widget-only artifact is just the glance.

Build a widget when the user wants to *keep an eye on* something; build a dashboard when they want to *explore* it; give a dashboard a widget when they want both.

## Tools

- **`create_widget`** — add a widget to an existing dashboard (pass its slug) or scaffold a widget-only artifact (new slug). It never overwrites: a `widget.html` or `widget.ts` already in the directory is kept and named in the reply — read it before you edit it
- **`refresh_widget`** — run the script, re-render, and return the actual PNG renders (declared size in light **and** dark by default; `previews: "all"` for both size families, `"none"` to skip) plus the path of every file written. This is your QA loop: those images are exactly what the user's home screens and phone show.
- **`list_widgets`** — every widget with its snapshot state
- Regular file tools (`Read`, `Write`, `Edit`) to shape `widget.html` and `widget.ts`

## How it works

```
/workspace/artifacts/<slug>/
├── package.json      # scripts.widget (+ scripts.start if it's also a dashboard), gamut.widget config
├── widget.ts         # what scripts.widget runs: rewrites widget.html and widget.json
├── widget.html       # THE SNAPSHOT: self-contained, responsive, data baked in
├── widget.json       # written by the script: { "validUntil": ISO | null }
├── widget.log        # script output from each refresh
└── snapshots/        # platform-owned PNG renders + snapshot.json (never edit)
```

1. You write `widget.html` (the look) and `widget.ts` (the data, and how long it stays true).
2. A refresh runs `bun run widget` inside this container — the same way the dashboard half runs `bun run start` — with your secrets and connected accounts available, then rasterizes `widget.html` into light/dark PNGs for every size.
3. The platform shows the snapshot instantly wherever the user looks and re-runs the script once `validUntil` has passed **and** the user opens the agent's page, after each of your runs, or when the user taps refresh. **Nothing runs on a timer while nobody is looking.**
4. If the script fails on one of those refreshes, when no conversation is running, the platform opens an automated session that hands you the error and the log and asks you to fix it. Nobody is waiting in that session — fix the script, `refresh_widget` to confirm, and only ask the user something if the fix genuinely needs their decision.

A widget with no `scripts.widget` is static: it only changes when you rewrite `widget.html` during a run (e.g. "log lunch" → you update the macros widget yourself). Use `withScript: false` for those.

## Quick start

1. `create_widget` — with an existing dashboard's slug to attach, or a new slug for a standalone widget (add `refreshOnTurnEnd: true` if it tracks something you change in conversation)
2. Edit `widget.ts`: replace `loadData()` with the real source (API, file under `/workspace`, connected account, or the dashboard's own data helpers) and return a real `validUntil`
3. Edit `widget.html` if the template's label / value / detail layout doesn't fit
4. `refresh_widget` — look at the returned light and dark renders; iterate until both read at a glance and there are no warnings
5. Tell the user what the widget shows and when it refreshes

## Manifest

```json
{
  "name": "Nutrition",
  "description": "Meals, macros and targets",
  "scripts": {
    "start": "bun run serve.js",
    "widget": "bun run widget.ts"
  },
  "gamut": {
    "widget": { "size": "small", "timeoutSeconds": 30, "refreshOnTurnEnd": false }
  }
}
```

Each half of an artifact is a named script: `start` serves the dashboard, `widget` regenerates the snapshot. `gamut.widget` is the marker that says this artifact has a widget at all, plus the settings the platform needs:

- `size`: `small` (square, 170×170 pt — one focal value) or `medium` (2:1, 364×170 pt — a value plus a short list or a sparkline). One widget per artifact.
- `timeoutSeconds`: script budget, clamped to 120 (ask for more and you get 120). Keep scripts fast — they run while the user is waiting on the page.
- `refreshOnTurnEnd`: re-render after **every** turn you finish, not only once `validUntil` has passed. Turn it on when the data is something you change in conversation — a task list, a food log, a running tally — so the card can never be behind the chat that just updated it. Leave it off for data that comes from outside (weather, prices, a calendar): those already have an honest `validUntil`, and re-running on every turn just burns time. At most one re-render a minute either way.
- There is deliberately **no refresh interval here**. The script decides validity per run (next section) because only the data knows its own cadence.

## The refresh script contract

The refresh runs `bun run widget`, so `scripts.widget` is whatever command builds the snapshot — `bun run widget.ts` from the template, but `python3 -m tools.build` or a chain with flags works just as well. It runs with cwd = the artifact directory, env `WIDGET_SLUG`, `WIDGET_DIR`, `WIDGET_OUTPUT` (absolute path to `widget.html`), `WIDGET_META` (absolute path to `widget.json`), plus everything in the agent's own environment (`.env` secrets, connected-account tokens, `PROXY_BASE_URL`).

- **Write the whole `widget.html`**, atomically (temp file + rename). Bake the data into the markup — no `fetch` in the page, no `<script>` that loads data.
- **Write `widget.json`** with `{ "validUntil": "<ISO-8601>" }` — *when does this snapshot stop being true?* Compute it from the data, not from a constant:
  - a stock price: 5 minutes during trading hours, but the next market open once the market closes;
  - a calendar widget: when the next event starts — and on a free Friday afternoon, Monday morning;
  - daily macros: the next meal time, or midnight;
  - a monthly KPI: the next reporting day.
  `null` means "never on its own" (only a rewrite changes it). If you don't write the file the platform assumes one hour and `refresh_widget` warns you.
- **Escape** every string that came from outside before inserting it into HTML.
- **Exit non-zero on failure.** The previous snapshot keeps serving and the error surfaces in `refresh_widget` and `widget.log`. Never write a blank or "error" widget over good data.
- **Be quiet and fast.** No network retries that blow the timeout; cache under `/workspace` if the source is slow.
- Inside a dashboard artifact, import the dashboard's data code instead of duplicating it — one source of truth for the card and the page. Declared `dependencies` are installed before the script runs if `node_modules` is missing.

## Writing the HTML

The snapshot is displayed with **scripts disabled** and a strict CSP: inline `<style>` and `data:` images only. Anything that needs JavaScript at display time will not work — do the work in `widget.ts` instead. JavaScript *inside* `widget.ts` is unrestricted.

- **One focal element.** A small widget is one big number or one line; a medium widget adds at most three secondary items. If it needs a legend, it's a dashboard.
- **Responsive to the container**, not the viewport: the same HTML renders at 170×170, 364×170, and in ~230–480 px app tiles. Use `height: 100%` flex layouts, `clamp()` font sizes, and `overflow: hidden` on `body`. Never rely on a fixed pixel width. **A widget never scrolls.**
- **Dark mode is mandatory.** Define the light palette on `:root`, then redefine the tokens under BOTH `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { … } }` and `:root[data-theme="dark"] { … }` — the app sets `data-theme` explicitly, the rasterizer sets both. The template does this; keep the structure.
- **System font stack**, tabular numerals for numbers, WCAG AA contrast, don't encode state by colour alone.
- **Show staleness honestly**: include a small "as of 9:41" or "today" line so a cached snapshot is never misleading.
- Keep the file small (well under 200 KB); inline SVG is fine for icons and sparklines. Images must be `data:` URIs; no external assets.

## Review checklist (every `refresh_widget`)

Look at the returned images — do not assume the HTML you wrote renders the way you pictured it.

- The render reads in under two seconds: what is it, what's the value, is it good or bad.
- No clipped text, no scrollbars, no empty regions at either size.
- The numbers are real (the script hit the real source, not the placeholder).
- **The dark render is actually dark** — not the light palette on a dark app background, and not white-on-white. This is the failure the images exist to catch.
- `refresh_widget` reported no error and no warnings, and the reported "valid until" makes sense for the data.
- If the widget tracks something you edit during a conversation, `refreshOnTurnEnd` is on — otherwise the card will sit stale until its `validUntil` passes.
- The final response names the widget, what it shows, when it will refresh next and why, and (if attached) which dashboard it opens.

## Common failures

- A `<script>` in `widget.html` that builds the content → shows blank. Move it to `widget.ts`.
- Fixed `width: 364px` → clipped in the small size and in app tiles.
- Fetching data from the page → blocked by CSP. Bake it in.
- Exiting 0 after a failed fetch and writing "N/A" → destroys good data. Exit 1.
- Not writing `widget.json` → the platform guesses one hour; a `validUntil` of "in 60 seconds" for a slow source → the user waits on every page load. Match validity to the data's real cadence.
- Naming the snapshot `index.html` → that is the dashboard's Vite entry. The widget file is `widget.html`.
- Writing a `widget.ts` but no `scripts.widget` entry → the platform treats the widget as static and never runs it. Declare the command.
