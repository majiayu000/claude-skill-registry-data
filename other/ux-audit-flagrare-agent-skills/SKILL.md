---
name: ux-audit
description: "Goal-locked UX audit. Drives a real browser through every reachable route (or a user-specified scope) and every visible affordance, screenshots each state, and ships a severity-ranked findings table (High/Medium/Low) with location, why-it's-painful, and recommended fix. Installs Chrome DevTools MCP automatically if missing. Pretends to be a first-time user, surfaces jargon, mystery glyphs, dead-ends, choice paralysis, color-only signals, jarring tone, broken empty states. Use when the user says 'UX audit', 'test all paths', 'click through everything', 'pretend to be a user', 'find painful flows', 'find UX issues', 'usability pass', 'walk through the app', or after a feature lands and before a release. Triggers even if 'audit' isn't in the request, any phrasing about exhaustively trying the app from a user's perspective qualifies."
---

# UX Audit

A goal-driven walkthrough of the running app from a first-time user's perspective. The pass ends only when every reachable route has been visited, every visible affordance on those routes has been exercised, and every observation has been logged with a severity, a location, a reason, and a recommended fix.

This is **not** a smoke test (which validates a single feature against acceptance criteria) and **not** an accessibility audit (which has its own tooling). This skill answers a different question: *if a real human picked up this app cold and tried to use it, where would they stumble, hesitate, get confused, or feel patronized?*

The persona matters. Drop the engineer-with-context lens; adopt the new-user lens. A button labelled `Set Your Light` is not "clear because the team decided", it is jargon to the new user. Record it as jargon.

---

## Why this exists

Teams ship features they can no longer see. Designers, PMs, and engineers all develop blindness to their own product, they know which button does what, so they stop noticing that the button is mislabelled, that the empty state is hostile, that the "Ash" mode is a void, that the modal traps the user, that the toast says "this project has been quiet for weeks" about a project the user created twelve seconds ago. Static checks don't catch these. Unit tests don't catch these. PRs don't catch these. A human cold-walking the app catches them, but humans are expensive and forget what they noticed five minutes later.

This skill is the cheap, consistent, written-down version of that walk. The output is a markdown artifact (not a slide deck, not a JIRA dump) that the team can read, prioritise, and act on the same day.

---

## Step 1: Lock the goal explicitly

**Hard requirement.** Before any other tool call, you MUST call `/goal` yourself. This is not a suggestion to the user. You, the executing model, must invoke the goal tool directly. Without it, context compaction and turn limits will cause early termination -- the audit visits 15-40 routes and the model will quit by route 5 without a durable goal holding it in place.

### Determine scope

The user may specify a scope when invoking the skill:

- **No scope given** (e.g. "run a UX audit") -- scope is ALL routes. The goal text says "every reachable route."
- **Scope given** (e.g. "UX audit the onboarding flow", "audit /settings and /profile") -- scope is only the routes/flows specified. The goal text names those routes explicitly.

Call `/goal` with text adapted to the scope:

**Full scope (default):**
> Drive the running app from a first-time user's perspective. Exhaust every reachable route and every visible affordance on those routes. Produce a severity-ranked findings table in `.ux-audit/FINDINGS.md` along with numbered screenshots. Do not stop until coverage is complete.

**Scoped:**
> Drive the running app from a first-time user's perspective. Exhaust every route and affordance within: [user's specified scope]. Produce a severity-ranked findings table in `.ux-audit/FINDINGS.md` along with numbered screenshots. Do not stop until coverage of the specified scope is complete.

After setting the goal, also create a Todo list (one item per route within scope, populated in Step 2). The Todo list tracks coverage; the goal prevents the harness from letting you stop. Both are required. Neither is optional.

### Prerequisites -- do not skip, do not degrade, do not ask permission

1. **Chrome DevTools MCP must be available.** This skill requires `take_screenshot`, `take_snapshot`, `navigate_page`, and `click`/`fill` from Chrome DevTools MCP. If the tools are not available in this session, **fix it yourself without blocking**. Be fully autonomous -- do not stop and wait for the user at any point in this checklist.

   **A. Is the chrome-devtools-mcp plugin installed?**
   - Check: look for `chrome-devtools-mcp:chrome-devtools` in the available skills list
   - If missing: install it. Try in order: `npm i -g chrome-devtools-mcp@latest` (disable sandbox) → `npm i -g chrome-devtools-mcp@latest --prefix ~/.local` (if EACCES) → `pnpm add -g chrome-devtools-mcp@latest`

   **B. Is Chrome running with remote debugging?**
   - Launch Chrome yourself. Run this command (disable sandbox):
     - macOS: `open -a "Google Chrome" --args --remote-debugging-port=9222`
     - Linux: `google-chrome --remote-debugging-port=9222 &`
   - If Chrome is already running without the flag, kill it first: `pkill -f "Google Chrome"` (macOS) or `pkill chrome` (Linux), wait 2 seconds, then launch with the flag.
   - Do NOT ask the user to do this. Do it yourself. You CAN launch Chrome from a bash command.

   **C. Are the MCP tools appearing?**
   - After launching Chrome, invoke the `chrome-devtools-mcp:chrome-devtools-cli` skill if available, or run `chrome-devtools status` to verify connection.
   - If tools still don't appear in your deferred tools list after Chrome is running, tell the user: "Run `/reload-plugins` -- Chrome is now running with debugging, but Claude Code needs to reconnect its MCP server." This is the ONE thing that may require user action.

   **D. While waiting for reload (if needed), start Step 2.**
   - Do NOT block. Begin enumerating routes from source (Step 2) in parallel. The route list doesn't require Chrome. By the time you finish enumeration, the tools should be available.

   **Rules:**
   - Be fully autonomous. Launch Chrome, install tools, configure -- do everything yourself.
   - The ONLY user action that may be needed is `/reload-plugins` or restarting Claude Code if the MCP server won't connect after Chrome is running.
   - Do NOT stop and describe what needs to happen. Just do it.
   - Do NOT offer alternatives. Do NOT present options. Do NOT ask questions about setup.
   - If after all of A-C the tools genuinely cannot appear (e.g., the user is on a headless server with no display), then and only then explain why it cannot proceed.

2. **Dev server must be running.** Check if it's already running (`lsof -i :3000` or similar for common ports, or check the project's `package.json` scripts for the dev port). If not running, start it yourself in the background. If it requires specific env vars or setup you can't determine, ask the user for the start command -- but try `npm run dev` or `pnpm dev` first.

---

## Step 2: Enumerate routes from the source

The app's filesystem is the source of truth for reachable pages. Scan it before opening a browser. If a scope was specified in Step 1, filter the route list to only routes within that scope (but still enumerate from source to ensure nothing is missed within the scoped area).

Detect the framework from the project layout:

| Layout | Framework | Where routes live |
|---|---|---|
| `src/routes/**/+page.svelte` | SvelteKit | `find src/routes -name '+page.svelte'` |
| `src/app/**/page.tsx` | Next.js App Router | `find src/app -name 'page.tsx'` |
| `pages/**/*.tsx` | Next.js Pages Router | `find pages -name '*.tsx' -not -path '*/api/*'` |
| `src/pages/**/*.vue` | Nuxt / Vite-Vue | `find src/pages -name '*.vue'` |
| `app/views/**/*.html.erb` | Rails | `find app/views -name '*.html.erb'` |
| `templates/**/*.html` | Django / Flask | `find templates -name '*.html'` |
| `src/routes.ts` / `App.tsx` with `<Route>` | React Router | `grep -r 'path=' src/ \| grep -i route` |

If the framework isn't on this list, look for a router/config file and ask the user where routes live. Don't guess, a missed route is a missed finding.

Filter out:
- API routes (`/api/*`, controller files without templates)
- Layout / error / not-found files (they're tested implicitly via 404 + nav)
- Route groups (parentheses-wrapped dirs in SvelteKit/Next don't add URL segments)

Produce a flat list of URLs to visit. Note which are auth-gated. If you don't know which test credentials to use, ask the user once, don't try to register your own account silently unless the app supports self-serve signup and the user confirmed it's OK.

---

## Step 3: Setup the browser

Use **Chrome DevTools MCP** for this skill, not Playwright. Chrome DevTools gives you the accessibility tree (`take_snapshot`), screenshots (`take_screenshot`), console messages, network requests, and direct click/fill/navigate. Playwright is for converting findings into permanent specs later (out of scope here).

### Make the browser visible to the user

The user must be able to see what you are doing. After connecting to Chrome DevTools:

1. **Open a new tab or window** dedicated to the audit (don't reuse an existing tab with unrelated content).
2. **Bring the window to the front** on every navigation. Use `bringToFront: true` or the equivalent option on every `navigate_page` call. The user should be watching the audit happen in real time -- if they can't see it, something is wrong.
3. **Confirm with the user** after the first navigation that they can see the browser window. One sentence: "Can you see Chrome showing [URL]?" If they say no, debug the connection before continuing.

### Set the viewport and output folder

Set the viewport. Default to **mobile-first** (390x844, iPhone 14) unless the user explicitly says desktop or the app has no responsive layout. Most modern apps are used on a phone; auditing only at desktop misses the entire mobile experience.

Create the output folder:

```bash
mkdir -p .ux-audit
```

All screenshots and the findings file live here. Numbered prefixes (`01-landing.png`, `02-register.png`, ...) so they sort chronologically.

Open the start URL and `take_snapshot` to confirm the page rendered. Capture the title and visible structure. If the page is blank or 500s, stop, fix the server before continuing.

---

## Step 4: Walk each route, exhaustively

For every route in your enumerated list, do this loop:

### Per-route protocol

1. **Navigate** with `navigate_page` to the route's URL.
2. **Screenshot** to `.ux-audit/NN-route-name.png`. (Use Read on the screenshot afterward, your judgment depends on actually seeing it.)
3. **Snapshot** the accessibility tree (`take_snapshot`) to enumerate every interactive element by uid.
4. **Observe** the page as a first-time user. Before clicking anything, capture initial impressions:
   - What's the first thing the eye lands on?
   - Is the primary action obvious?
   - Is anything below the fold that shouldn't be?
   - Any unexplained jargon, mystery glyphs, or color-only signals?
   - Any visual overlap (FABs over buttons, toasts over content)?
   - Does anything look broken (truncated text, empty dropdowns, dead links)?
5. **Click** every visible interactive element in priority order:
   - Primary CTAs first (orange/filled/large buttons)
   - Secondary actions next
   - Tertiary affordances (icons, chevrons, links in card bodies)
   - Form submissions, try valid input AND deliberately invalid input (short password, empty required field, weird unicode)
6. **After each click**, screenshot the new state, snapshot the tree, and record what happened:
   - Did the page change? Did anything go wrong?
   - Did a modal/drawer open? Is it the right pattern for mobile? (Drawer > Dialog at <768px.)
   - Did a toast fire? Was the message appropriate to the user's actual context?
   - Did a nav badge change? Was that a positive or negative signal?
   - Did scroll happen? Was there hidden content above/below?
7. **Backtrack**: return to the route's main state before moving to the next affordance. Don't let one click cascade you off-route silently.

### Finding triggers (what to flag)

Treat each of these as a candidate finding. Most will be real; document them with severity even when the team will defend the choice, the team can override, but the audit must be honest.

- **Jargon**: any term the user wouldn't know on first contact (internal entity names, branded features, technical acronyms)
- **Mystery glyphs**: unlabelled icons in nav or actions
- **Color-only signals**: red dots, green dots, orange highlights with no text label
- **Dead-end empty states**: empty pages with no CTA to populate
- **Choice paralysis**: three or more equally-weighted CTAs on one screen
- **Premature alarms**: "needs attention" / "this is overdue" / "you've drifted" fired against fresh entities
- **Tone mismatch**: poetic/affirming copy next to operational copy
- **Vertical-center waste**: content stuck in the middle while top-of-fold is dark void
- **Truncated text**: placeholders, button labels, or table cells cut off
- **Tap-target violations**: controls under 44×44pt on mobile
- **Modal on mobile**: Dialog used where Drawer would fit better
- **Silent saves**: no toast / no confirmation after a destructive or important action
- **Vocabulary drift**: same concept named differently across screens
- **Layout collisions**: FAB overlapping content, toast overlapping CTAs, header crowding
- **Form gotchas**: no password show/confirm, browser-native HTML5 validation tooltips on a dark theme, missing inline errors
- **IA gaps**: features reachable only via deep-link, not bottom nav / sidebar
- **Validation bugs**: clicking a thing creates the wrong follow-up state, or fires a notification that contradicts the user's context

The full heuristic list lives in `references/finding-triggers.md`. Read it once at the start of a long audit; refer back when in doubt.

---

## Step 5: Log findings as you go (not at the end)

The discipline that makes this skill useful: **append findings to `.ux-audit/FINDINGS.md` after every route**, not in one big batch at the end. The reason is mechanical, by route 15, you will have forgotten the texture of route 3. Write while it's fresh.

Use the template at `references/findings-template.md` to create the file once at the start. Each finding gets one row in the table:

```markdown
| # | Severity | Location | Issue | Why it's painful | Recommended fix |
|---|----------|----------|-------|------------------|-----------------|
| L01 | Medium | `/login` | Browser-native HTML5 tooltip on dark theme | Light bubble obscures submit button on mobile | Inline validation with app's existing toast pattern |
```

ID prefix conventions (totally optional but useful for grep later):
- `L##` landing/marketing
- `R##` register / `A##` auth
- `ON##` onboarding
- `T##` today / dashboard
- `F##` fleet / list page
- Adapt per-app

Severity rubric (from `references/severity-rubric.md`):

- **High**: blocks or punishes the user's correct action, contradicts the app's stated promise, or breaks a core flow
- **Medium**: causes confusion, mis-taps, or anxiety but the user can still proceed
- **Low**: polish issue, cosmetic friction, easy win

Resist the urge to inflate everything to High. The summary is more useful when the High list is short and damning.

---

## Step 6: Compile the executive summary

After the route loop is complete, write the **Executive Summary** at the top of `.ux-audit/FINDINGS.md` (above the table). This is the deliverable most teams will actually read.

Include:

1. **Totals**: finding count by severity
2. **Top 5 highest-impact issues**: name them, link to the row IDs, give one-line takeaways
3. **Cross-cutting themes**: the patterns that span multiple findings (vocabulary chaos, IA gaps, mobile-first violations, etc.). These matter more than any individual finding because they reveal systemic problems
4. **Coverage**: which routes were tested, which were skipped, and why (auth-gated, requires real device, etc.)

The summary is the only thing some stakeholders will read. Make it self-contained, they should be able to understand the state of the app without reading the table.

---

## Step 7: Hand off

End the audit with one short message to the user:

- Path to `FINDINGS.md`
- Count by severity
- The 3 single most important issues to fix this week
- An explicit "I did not test: …" list

Do not propose fixes inline (the table already does that). Do not start implementing fixes (that's a different skill, `/flagrare:atdd-plan`). The audit's job is to surface; the team's job is to triage.

---

## Coverage discipline

The hardest part of this skill is not stopping early. Models default to "I've seen enough." That's wrong here, the goal is *exhaustive*, not *representative*. Patterns to combat early termination:

- **Maintain a Todo list with one item per route.** Mark each completed only after the per-route protocol fully ran.
- **`/goal` was already called in Step 1.** If for any reason it wasn't, call it now. It blocks termination until the goal text holds true.
- **Resist consolidation.** "Routes 5-10 had similar issues, I'll group them", no. Visit each, log each. Similarity becomes a cross-cutting theme later.
- **Don't skip the "obvious" pages.** Marketing pages, 404 pages, /offline, they often contain the worst findings because nobody has looked at them recently.
- **Re-screenshot after every state change.** Costs nothing, prevents you describing a state you can't see.

---

## When to deviate

This skill is intentionally rigid about *coverage* but flexible about *technique*. Adapt these freely:

- **Viewport**: desktop apps audit at 1440×900; tablet at 834×1194. Confirm with the user once.
- **Persona**: default is "first-time user." If the user asks for "power-user audit" or "returning-user audit," shift the lens, the findings change.
- **Tooling**: Chrome DevTools MCP is required. Step 1 says to install it yourself if missing. Only if installation genuinely fails (npm not available, network down, permission denied after sandbox bypass) is Playwright MCP an acceptable fallback (you lose console diagnostics and the accessibility tree but retain screenshots and navigation). If neither works, **do not run the audit** -- tell the user what failed and stop. Never fall back to a "code-level audit" or static analysis; that is a different activity entirely.
- **Auth**: if the app has no self-serve registration, ask for test creds. If credentials are sensitive, ask whether to test the auth-gated half at all.

---

## Output contract

After this skill runs, the project contains:

```
.ux-audit/
├── FINDINGS.md          ← table + executive summary
├── 01-landing.png
├── 02-register.png
├── …
└── NN-final-state.png
```

That's the whole deliverable. No JSON, no slides, no separate triage file. One markdown, one folder of screenshots, ready to drop into Slack / Notion / PR review.
