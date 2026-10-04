---
name: project-sites
description: >-
  Build any of THREE self-contained, offline, single-file project-site types from a data JSON,
  all sharing ONE stylesheet (the Ramco Nebula / RXD design language — brand blue #316ADD,
  Inter-Tight + JetBrains-Mono, light + dark) so they read as one product: (1) DOCS — a
  documentation / reference / guide site with a sticky grouped sidebar + scrollspy, code blocks
  with copy, callouts, kv/step/table blocks and client-side Mermaid diagrams; (2) TRACKER — a
  status / progress / standup / milestone / KPI dashboard with stat tiles, progress bars, a
  resource-exchange, a calendar month-grid, a daily timeline, AND a dated log archive ingested
  from the project's journal files; (3) TUTORIAL — a multi-section field-course / explainer /
  onboarding / walkthrough with a hero, topic cards, hash-routed section pages and Mermaid
  diagrams. Use this whenever someone wants to make, set up, or KEEP UPDATING a docs site, a
  reference/guide/handbook, a status tracker or progress/delivery/sprint dashboard, a milestone
  or KPI board, a daily-updates/changelog/standup page, a shared-materials/resource-exchange
  page, a tutorial or field course, an explainer, or "a self-contained single-file
  docs/tracker/tutorial page". It prefers the HOST PROJECT's own stylesheet and theme when one
  exists (the skill's sheet is the fallback), can inherit an app's global CSS when embedded as a
  route, ingests mistakes.md/learnings.md/worklog.md into the tracker as a dated archive, and can
  OPTIONALLY password-gate any page (client-side AES-256-GCM, no server). NOT for a live
  dashboard over a database/API (build a real app) or arbitrary charts (use a charting tool).
---

# project-sites

Turn a project's content into **one self-contained `.html`** — a **docs** site, a **tracker**
dashboard, or a **tutorial** course. All three are driven by a single data JSON, rendered by one
zero-dependency Node builder, and skinned by ONE canonical stylesheet so they look like one
product (and can be hosted as routes in the same app).

```bash
node scripts/build.mjs <docs|tracker|tutorial> <in.json> <out.html> [options]
```

## Step 0 — ALWAYS ask which sites first (multi-select)

When invoked to build project sites, the **first thing to do is ask the user, as a multi-select
question, which site(s) they want** — any subset of:

- **Docs** — a documentation / reference / guide site.
- **Tracker** — a status / progress / standup / milestone dashboard.
- **Tutorial** — a field-course / explainer / walkthrough.

Then build only the selected types (one `build.mjs` run each). Do not assume — a request may map
to one, two, or all three. Only skip this ask if the user has already named the exact type(s).

## Create workflow (per selected type)

1. **Start from the matching example** in `assets/examples/{docs,tracker,tutorial}.example.json`
   — copy it into the user's project and edit. `title` is the only required field for every
   type; tracker/tutorial sections auto-hide/omit when empty, so a site can start small and grow.
2. **Read `references/data-model.md`** for the full schema of the chosen type, the shared block
   vocabulary (docs + tutorial), the tag/resource/credentials shapes (tracker), and the colour →
   `--lp-*` token map. It is the contract the templates render.
3. **Build** with the type as the first positional arg. For docs, invent the sections/groups; for
   tutorial, invent the topics and match the reference's depth (rich, layered, concrete — not a
   thin outline). Tracker is data-shaped, not authored prose.
4. **Verify in a real browser** (see below) — do not skip.

## Behaviors

### 1. One shared stylesheet, classes-only
All three templates reference classes from the single `assets/tailwind.css`, banner-marked into
four sections: `/* === base (canonical) === */` (the RXD tokens + utility subset — byte-identical
to the original tracker base), `/* === tracker extensions === */` (`.tk-*` + the archive
`.tk-arc-*`), `/* === docs extensions === */` (`.dp-*`), `/* === tutorial (.tut) extensions === */`.
**Never author inline styles in a template.** If a genuinely-new component (or a look-&-feel
improvement) is needed, ADD its class into the matching banner-marked section in the same
`--lp-*` token style. Every colour goes through the tokens — never hardcode a colour.

### 2. Project-default-style preference (must-have)
The skill's sheet is the **fallback**. If the host project has its own stylesheet, USE IT:
`--project-css <path|url>` inlines/links the project's CSS **after** the skill sheet, so the
project's rules cascade over the skill's (still-emitted) semantic classes — a project re-skins by
overriding the `--lp-*` tokens or any `.tk-*/.dp-*/.tut` class. When the site is **embedded as a
route inside an app**, use `--project-css-only` to ship no default sheet and inherit the app's
global CSS (also drops the CSP so the host controls it), and `--project-theme <light|dark|auto>`
to honor the app's default theme and drop the standalone toggle. `--no-fonts` inherits the app's
fonts. Default (standalone) keeps the RXD sheet + the light/dark toggle. See
`references/data-model.md` → "Project-style overrides" for the exact mapping.

### 3. Tracker log-ingestion (`ingest-logs.mjs`)
If the project has `mistakes.md` / `learnings.md` / `worklog.md` (or files you name), ingest their
FULL original content into the tracker JSON as a dated `archive` section:
```bash
node scripts/ingest-logs.mjs --data tracker.json --dir /path/to/project
node scripts/build.mjs tracker tracker.json dashboard.html
```
It parses `##`/`###` date-style headings into per-date entries (else one snapshot dated to TODAY
via `new Date()`), preserves content VERBATIM (escaped at render), and is **idempotent** — keyed
by (file, date), unchanged re-ingest is a no-op, changed content updates that dated entry, a new
date appends a new dated snapshot. The tracker renders the archive as an expandable, dated,
per-file section. Because the tracker then holds the canonical dated originals, the `.md` files
may be deleted afterward — the skill does NOT delete them (that is the user's call). Conditional
on the files existing.

### 4. AI auto-update calendar
Maintenance is trivial and safe to automate: the AI (or a cron/CI step) checks the local date and
appends BRIEF, planned task entries to the correct day via `add-day.mjs` (idempotent per date),
then rebuilds + republishes.
```bash
node scripts/add-day.mjs --data tracker.json --date <today> --bullet "…" --today
node scripts/build.mjs tracker tracker.json dashboard.html
```
Keep `tracker.json` in version control — its diff is the changelog; the HTML regenerates anytime.

### 5. Optional password lock
Wrap ANY finished page (any type) in a client-side AES-256-GCM gate with `--lock <passcode>`
(omit the passcode to be prompted). Decrypts in-browser via Web Crypto — needs a **secure
context** (HTTPS or `localhost`). The whole security reduces to passcode entropy; read
`references/security-model.md` before calling a locked page "secure". No recovery if lost.

## Verify before shipping (do not skip)

Serve the file (`python3 -m http.server`; over `localhost` if locked) and open it in a real
browser. Confirm for each built type: correct render in **both light and dark**; Mermaid renders
(docs + tutorial); the tracker calendar days are clickable and the archive expands; code-copy
works (docs); the sidebar scrollspy + section nav work (docs); prev/next + hash routing work
(tutorial); **zero console errors**; and **zero external network requests** beyond the optional
Google Fonts link (use `--no-fonts` to prove fully-offline). For a locked page, confirm the
correct passcode reveals the content and a wrong one is rejected. Run the tests:
`node --test tests/*.test.mjs`.

## What's in the box

```
project-sites/
├── SKILL.md
├── assets/
│   ├── tailwind.css                # ONE canonical sheet: base + docs/tracker/tutorial extensions (banner-marked), INLINED
│   ├── mermaid.min.js              # Mermaid lib, inlined on demand (docs + tutorial diagrams; no CDN)
│   ├── docs.template.html          # docs shell (client-side safe-DOM renderer: sidebar + scrollspy + blocks)
│   ├── tracker.template.html       # tracker shell (client-side safe-DOM renderer + archive section)
│   ├── tutorial.template.html      # tutorial shell (server-rendered views + hash router + Mermaid runtime)
│   ├── gate.template.html + gate.css   # OPTIONAL lock (AES-256-GCM gate)
│   └── examples/{docs,tracker,tutorial}.example.json
├── scripts/
│   ├── build.mjs                   # the dispatcher: <docs|tracker|tutorial> <in.json> <out.html> [options]
│   ├── add-day.mjs                 # append/update one tracker standup day (idempotent per date)
│   └── ingest-logs.mjs             # ingest mistakes/learnings/worklog into the tracker archive (idempotent)
├── references/
│   ├── data-model.md               # all THREE schemas + conventions + project-css override + themes + ingest-logs schema
│   └── security-model.md           # threat model for the optional lock
└── tests/                          # node --test tests/*.test.mjs
```

## When NOT to use it

- **Live dashboards over a database/API** — that needs a real backend + query layer.
- **Ad-hoc charts/graphs** — use a charting/visualization tool; this renders structured
  primitives (docs blocks, tracker tiles/bars/calendar, tutorial cards), not arbitrary plots.
- **Server-backed auth** — the lock gates static access, not per-user auth/revocation.
