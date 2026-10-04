---
name: regen-qa-crawl
description: Run a two-agent QA pass over the live regencivics.earth site. Use when you want to check that every page loads, every button and link works, forms submit, text is readable, and copy follows the project writing rules. Triggers on "QA the site", "test the website", "check all the buttons", "crawl the site", "full site audit", "readability pass", "is everything working", "regression check before launch". Produces a prioritized findings report.
---

# ReGen QA Crawl (Two-Agent Site Test)

A repeatable way to test the whole live site with two agents that split the work cleanly:

- **Driver** answers "does it work?" It drives the browser through every route, clicks buttons and links, opens modals, and submits forms with test data. It records load failures, console errors, failed network calls, dead buttons, broken links, and broken flows.
- **Reviewer** answers "does it read and look right?" It audits the screenshots and extracted page text for contrast, legibility, truncation, layout, mobile responsiveness, and copy that breaks the project writing rules.

The two roles never touch the browser at the same time. Driver runs first and saves artifacts to disk. Reviewer reads those artifacts. The orchestrator merges both into one report. This keeps a single browser session safe and lets the Reviewer run as a separate agent on extracted text.

## When to run it

Before a launch, after a big batch of fixes, or on a schedule (a monthly regression pass works well). Run the full route set for a release gate. Run a single section (for example everything under `/community`) for a targeted check.

## Inputs you need

1. A connected browser. Use Claude in Chrome (`mcp__Claude_in_Chrome__*`) for the live run. Or run the bundled `crawl.mjs` locally where Playwright and a real Chromium are installed (Rye's dev machine has both).
2. The route manifest in `routes.json`. Regenerate it any time from `client/src/App.tsx` (see "Keeping routes current").
3. A test account and the test-data conventions below. Never use real investor or payment data.

## Test-data conventions (read before submitting anything)

The action depth is "submit with test data." That means forms get filled and sent, so the data must be unmistakably fake and easy to clean up.

- Email: `rye+qatest@regencivics.earth` (or any `+qatest` alias). Never a real person's address.
- Name / org: prefix with `QA TEST` so rows are filterable in the database and admin views.
- Free-text fields: start the text with `[QA TEST - ignore]`.
- Forum posts and comments: title or first line starts with `[QA TEST]`. Delete after the run, or soft-flag for moderation.
- **Do not** complete real payments, real token claims, or real Hypha bridge handoffs. Stop at the confirmation step, screenshot it, and record "reached confirmation, did not submit." Moving money and on-chain actions are out of scope for a QA pass.
- Keep a list of every artifact created (post IDs, application IDs, signups) so cleanup is mechanical.

## Workflow

### 1. Orchestrator: set up

Load the route manifest. Decide scope (full set or one section). Create an output folder for the run, dated: `qa-crawl/runs/YYYY-MM-DD/`. Make `screenshots/` and `pagetext/` subfolders.

### 2. Driver pass (functional)

For each route, in order:

1. Navigate. Record the final URL (catch unexpected redirects) and whether the page rendered or threw the error boundary.
2. Screenshot at desktop width (1440) and mobile width (390). Save both.
3. Read console messages. Flag any `error` level entries.
4. Read network requests. Flag any 4xx or 5xx, and any image that failed to load.
5. Save the visible page text to `pagetext/<route-slug>.txt` for the Reviewer.
6. Exercise interactive elements:
   - Every primary button: does it respond (navigation, modal, state change)? A button that does nothing on click is a finding.
   - Every nav link and in-content link: does it resolve to a real page, not a 404 or the error boundary?
   - Modals and dialogs: open and close cleanly.
   - Forms: fill with test data, validate inline errors behave, submit, confirm the success or confirmation state. Honor the test-data rules above.
7. Write one row per route to `driver-findings.md` with: route, load status, console errors, network failures, dead buttons, broken links, form result, notes.

Use the Driver prompt in `prompts/driver.md` verbatim when dispatching this as its own agent.

### 3. Reviewer pass (readability + content)

Dispatch the Reviewer as a separate agent. It does not use the browser. It reads `screenshots/` and `pagetext/` and audits:

- **Readability:** text contrast against background, font size, line length, truncation, text overflowing its container, content hidden behind overlays.
- **Layout:** broken responsive behavior on the 390 mobile shots, overlapping elements, off-canvas content, images stretched or squished.
- **Dark mode** (if the page supports it): unreadable low-contrast pairings, invisible icons, white flashes.
- **Copy against the writing rules** (these are hard rules from `.ai/docs/STEERING.md` and the project CLAUDE.md):
  - No em-dashes. Any `—` is a finding.
  - No contrast-framing ("not X, it's Y", "less X more Y").
  - No banned AI words (delve, tapestry, foster, leverage, robust, seamless, unlock, empower, and the rest of the list).
  - No rhetorical-question openers.
  - No passive-inspiration filler ("join us on this journey").
- **Accessibility basics:** heading order, link text that says more than "click here", form labels, image alt text where visible in the text dump.

Use the Reviewer prompt in `prompts/reviewer.md` verbatim. It writes `reviewer-findings.md`.

### 4. Orchestrator: merge and prioritize

Combine both findings files into `REPORT.md` with severity tiers:

- **P0 broken:** page won't load, form won't submit, primary CTA dead, console error that breaks a flow.
- **P1 major:** broken link, unreadable text, form accepts bad input silently, mobile layout broken on a key page.
- **P2 minor:** secondary button quirk, minor overflow, low-contrast on a non-critical element.
- **P3 polish:** copy that breaks a writing rule, spacing, nice-to-have.

Each finding gets: page, what's wrong, evidence (screenshot path, console line, or quoted copy), and a suggested fix. P0 and P1 should be specific enough to hand straight to a fix session (or the `regen-fixes-handoff` skill).

## Keeping routes current

`routes.json` is generated from the router. When routes change, regenerate:

```bash
node .claude/skills/regen-qa-crawl/gen-routes.mjs > .claude/skills/regen-qa-crawl/routes.json
```

The generator pulls every `<Route path=...>` from `client/src/App.tsx`, drops redirect-only routes, and marks routes with `:params` as needing a real sample value (the Driver fills those from links it finds while crawling).

## Running the bundled crawler locally

On a machine with Playwright installed, `crawl.mjs` does the Driver's breadth pass without a human in the loop: it visits every static route, screenshots desktop and mobile, captures console and network failures, and dumps page text. It does not do form submission (that stays with the interactive Driver agent, so test data is deliberate).

```bash
cd .claude/skills/regen-qa-crawl
npm i playwright
npx playwright install chromium
node crawl.mjs --base https://regencivics.earth --out ./runs/$(date +%F)
```

Then dispatch the Reviewer agent at the run folder.

## What this skill does not do

It does not test admin-only or auth-gated flows unless a test account is provided and logged in first. It does not execute payments or on-chain actions. It does not replace the ship gate (`regen-ship-gate`); that checks the codebase, this checks the running site. Use both.

## Static link guard (runs without a browser)

`scripts/audit-links.mjs` in the repo root is a source-level companion to this skill. It reads every route from `client/src/App.tsx`, then validates every internal `<Link>`, `navigate()`, `href`, and `#anchor` in the source against the route table and `client/public`. It exits 1 with a `raw <- file:line` list when a link points at a route that does not exist or an anchor has no landing target. It is wired into `regen-ship-gate` as Gate 4. Run it any time routes or links change:

```bash
node scripts/audit-links.mjs
```

It catches dead links the rendered-page pass can miss, because a broken button looks fine until clicked. It found `/campaigns/${id}` and `/application/${app.id}` as user-facing dead links on 2026-06-23.
