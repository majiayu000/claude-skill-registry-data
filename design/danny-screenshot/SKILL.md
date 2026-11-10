---
name: screenshot
description: "Capture a screenshot of any rendered web page in headless Chrome — full page, viewport, section, or element — for review and motion pipelines."
---

# Screenshot

Loads a URL in headless Chrome and captures exactly what the user asked for — the whole page, one section, a single element, the viewport, or a specific device rendering. Saves a PNG and Reads it back so the result is visible inline.

The engine is `scripts/screenshot.mjs`, which drives the user's installed Google Chrome through `playwright-core` (no bundled-browser download). It prints the saved PNG path on its **last stdout line** — read that path, then Read the PNG to view it.

## When to use this skill

- "Screenshot localhost:3000" / "grab a screenshot of headshotpro.com"
- "Screenshot the pricing section" / "capture the hero" / "the footer"
- "Screenshot the CTA button" / "just the nav bar" / "the `.testimonials` block"
- "Screenshot the whole page" / "the full scrollable page"
- "Screenshot the mobile view" / "how does this look on tablet"
- "Show me how the FAQ renders"

## When NOT to use this skill

- The user wants to **interact** with the page (click, fill, assert, audit a11y/console/network) → that's `expect` / browser-testing tools.
- The user wants a **generated design/mockup**, not a capture of a real page → `frontend-design` / `static-visual` / `visual`.
- Screenshot of the desktop or a non-web app → out of scope.

## CRITICAL

- **Interpret intent first** — the user describes *what* in plain language; you pick the right flag (see the map below). Don't ask which flag; infer it.
- **Last stdout line is the PNG path** (everything else is stderr). Capture it and Read the image to show the user.
- **Always report the FULL absolute path verbatim** in your reply — never abbreviate, truncate, or collapse the temp dir with `…/`. Put it on its own line so it stays copyable/clickable. Also surface the `file://…` line the script prints, since it's cmd/ctrl-clickable in most terminals.
- First run only: if it fails with `Cannot find package 'playwright-core'`, do the one-time install in Step 1.
- Uses the **installed Google Chrome** (`--channel chrome`) — no browser download. If Chrome is absent, see Troubleshooting.

## Intent → flags (the core of this skill)

| What the user said | Flags |
|--------------------|-------|
| "the page", "the whole page", "full page" | `--full-page` |
| "this page" / no target / "what's on screen" | *(omit target → viewport)* |
| "the pricing section", "the FAQ", "the hero" (named area) | `--section "pricing"` (heading match → enclosing `<section>`) |
| "the CTA button", "the nav", "`.hero`", "#footer" (one element) | `--selector ".hero"` |
| "the third section", "section 2" | `--section 3` |
| "the X inside the Y" (element within a container) | `--section "X" --container ".Y"` |
| "mobile view" / "on a phone" | `--device mobile` |
| "tablet" / "desktop" | `--device tablet` / `--device desktop` |
| "at 2x" / "retina" | `--scale 2` (already the default) |
| custom size | `--width 1440 --height 900` |
| "it loads slowly" / "wait for X" | `--wait 1500` or `--wait "<selector>"` |
| logged-in page / "I need to be signed in" | `--cdp <wsUrl>` (see Example 4) |

When in doubt between a *named area* and an *exact element*: try `--section "<text>"` first (it falls back through heading → text → block). Use `--selector` when the user names a CSS selector or a single small control.

## Workflow

```
- [ ] Step 1: Ensure deps installed (first run only)
- [ ] Step 2: Determine URL + map the user's words to a target flag
- [ ] Step 3: Run scripts/screenshot.mjs
- [ ] Step 4: Read the printed PNG path to view it; report where it saved
```

### Step 1: Ensure deps (first run only)

```bash
cd ~/.claude/skills/screenshot/scripts && npm install
```

Installs `playwright-core` only (small, no browser download). Skip if already installed.

### Step 2: Determine URL + target

- **URL**: a bare path like `/pricing` defaults to the local dev server (`http://localhost:3000` for this Nuxt app) unless the user gives a host. Make sure the dev server is running for localhost URLs.
- **Target**: map the user's phrasing using the **Intent → flags** table above.

### Step 3: Run the script

```bash
node ~/.claude/skills/screenshot/scripts/screenshot.mjs --url "<url>" [target flags] [render flags]
```

Full option list is in the header of `scripts/screenshot.mjs`. Quick reference:

| Flag | Purpose | Default |
|------|---------|---------|
| `--url <url>` | Page to load (required) | — |
| `--full-page` | Whole scrollable page | off |
| `--selector <css>` | One exact element | — |
| `--section <value>` | Heading text, CSS, or Nth `<section>` | — |
| `--container <css>` | Ancestor to capture when matching by heading | nearest `<section>` |
| `--device <name>` | `mobile` \| `tablet` \| `desktop` preset | — |
| `--width / --height` | Viewport size | 1280 × 800 |
| `--scale <n>` | Device scale (retina) | 2 |
| `--wait <ms\|selector>` | Extra wait before capture | none |
| `--pad <px>` | Padding around a section/element clip | 0 |
| `--out <path>` | Output PNG path | timestamped temp file |
| `--cdp <wsUrl>` | Attach to a running Chrome (reuses login) | launches fresh |
| `--headed` | Show the browser window | headless |
| `--channel <name>` | `chrome` \| `msedge` \| `chromium` | chrome |

### Step 4: View and report

The script prints the PNG path as its last stdout line, plus `Saved:` and `Open: file://…` lines on stderr. **Read that PNG** to show it inline, then report the **complete absolute path exactly as printed** — never shorten it with `…`. Include the `file://…` link too (cmd/ctrl-clickable). Default location is the system temp dir; pass `--out <path>` to save somewhere easier to reach (e.g. `~/Desktop`). If the user wants several targets (e.g. mobile + desktop, or three sections), run the script once per target.

## Examples

### Example 1: Whole page
**User:** "Screenshot headshotpro.com"
`node .../screenshot.mjs --url "https://headshotpro.com" --full-page` → Read + show.

### Example 2: A named section on the local app
**User:** "Screenshot the pricing section of /pricing"
`node .../screenshot.mjs --url "http://localhost:3000/pricing" --section "pricing"` → Read + show.

### Example 3: One element, mobile rendering
**User:** "Show me the nav on mobile"
`node .../screenshot.mjs --url "http://localhost:3000" --selector "nav" --device mobile` → Read + show.

### Example 4: A logged-in page (reuse a running Chrome)
**User:** "Screenshot the dashboard sidebar — it needs me logged in"
1. Tell the user to launch Chrome with remote debugging and log in:
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222`
   then get the endpoint from `http://localhost:9222/json/version` (the `webSocketDebuggerUrl`).
2. `node .../screenshot.mjs --url "http://localhost:3000/dashboard" --selector "aside" --cdp "ws://localhost:9222/devtools/browser/XXXX"` → Read + show.

## Troubleshooting

### Symptom: `Cannot find package 'playwright-core'`
**Cause:** First run; deps not installed.
**Fix:** `cd ~/.claude/skills/screenshot/scripts && npm install`

### Symptom: `Failed to launch Chrome (channel "chrome")`
**Cause:** Google Chrome isn't installed at the standard location.
**Fix:** Install Chrome, OR `cd ~/.claude/skills/screenshot/scripts && npx playwright install chromium`, then add `--channel chromium`.

### Symptom: `Could not find anything matching "X"`
**Cause:** No heading/text matched X.
**Fix:** Pass an exact `--selector "<css>"`, or `--section <N>` for the Nth `<section>`. Run `--full-page` first to eyeball the layout and pick a selector.

### Symptom: Capture is blank or missing late-loading content
**Cause:** Content rendered after `networkidle`, or lazy-loaded on scroll.
**Fix:** Add `--wait 1500` (ms) or `--wait "<selector>"`. Sections are auto-scrolled into view, which usually triggers lazy loads.
