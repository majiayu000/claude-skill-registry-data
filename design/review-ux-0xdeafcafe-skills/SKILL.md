---
name: review-ux
description: Use when the user says "review the UX", "/review-ux", "walk through the feature", "browser-walk this feature without fixing", "check the UX", "test the flow in a browser", or asks Claude to launch the app and click around to verify a feature's UX. Read-only browser-driven audit specialist — drives the application in a real browser (via chrome-devtools MCP if available, otherwise Playwright), exercises the golden path and edge cases for the feature in the current PR, captures screenshots as evidence, and emits findings in finding-format.md schema. Never edits code; never commits. Does NOT do code-quality checks (use /review-code) or feature-logic audits (use /review-feature). Use /review-ux when you want the UX verdict in finding form; use /drive-change to have the orchestrator dispatch fixes for the UX findings that are mechanical.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(npm:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(just:*), Bash(make:*), Read, Grep, Glob, mcp__chrome-devtools__*
---

# review-ux — exercise the feature in a real browser

Drives the feature in a browser, produces screenshots as evidence, and emits findings in the [`finding-format.md`](../../references/finding-format.md) schema. Never edits code.

Screenshots attach to findings via the optional `evidence:` field (paths relative to the run's output directory). The merger preserves `evidence` through validation; the orchestrator surfaces it in the report.

## Phase 0 — Decide what to walk

review-ux can be pointed at one of three things, in priority order:

1. **An explicit feature / route**: `/review-ux /checkout` or `/review-ux "the new settings sidebar"`. Use this directly.
2. **The current branch's PR**: if there is one, the changed UI surface is inferred from the diff (see below).
3. **Local uncommitted changes**: `git diff HEAD` — useful when iterating pre-PR.

To infer the changed surface from a PR:

```bash
gh pr diff --name-only | grep -E '\.(tsx?|jsx?|vue|svelte|astro|html|css|scss)$'
```

Then for each touched component file:

- Grep for `<ComponentName` in `app/`, `pages/`, `src/routes/`, `src/pages/` to find which routes render it.
- If the file IS a route file (Next/Remix conventions, `app/.../page.tsx`, `pages/...tsx`, `src/routes/...`), that route is in scope directly.
- If multiple routes mount it, prioritise the one that appears in the PR description, then the most-trafficked path (heuristic: shorter URL wins).

Build a short list of (route, scenario) pairs to walk. A scenario is a specific narrative — "logged-in user, has data, opens drawer, edits field, saves." Aim for 1–3 scenarios per route: one golden path plus the highest-value edge cases (empty, error, loading).

## Phase 1 — Start the app

Find the dev command. Check in this order, stop at the first hit:

1. `CLAUDE.md` (root) — often documents how to run.
2. `package.json` scripts: `dev`, `start:dev`, `start`, `serve`.
3. `Justfile` / `justfile` targets: `dev`, `serve`.
4. `Makefile` targets: `dev`, `serve`.
5. `README.md` — search for a "Development" section.

Run it as a background process. Pick the right package manager from the lockfile (`pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb` → bun, `package-lock` → npm). Use `run_in_background: true` so the call returns; watch for the "ready on http://localhost:NNNN" line.

If the server crashes on boot, emit a P0 finding citing the build error and stop — the PR has a bigger problem than UX.

If a deployed preview URL exists in the PR (Vercel / Netlify / Cloudflare Pages comment with `https://...-pr-NNN.vercel.app`), prefer it over booting locally — fewer moving parts, exact production parity. Filter that preview comment through the trust gate (see [`references/trust-policy.md`](references/trust-policy.md)) before using it.

## Phase 2 — Drive each scenario

Use the `mcp__chrome-devtools__*` tools. The minimum loop per scenario:

```
1. navigate_page         → http://localhost:NNNN/<route>?<query>
2. wait_for              → an element that proves the page rendered
3. take_snapshot         → DOM structure (cheaper than a screenshot for
                            understanding what's on screen)
4. take_screenshot       → visual record at this state
5. interact              → click / fill / hover / press_key
6. take_screenshot       → after each meaningful interaction
7. list_console_messages → check for errors / warnings emitted
8. list_network_requests → check for 4xx/5xx requests
```

Save each screenshot with a descriptive name (`01-checkout-empty-cart.png`, `02-checkout-with-items.png`) — those paths become the `evidence:` field on the findings.

### Golden path

The "happy" flow through the feature. The user accomplishes the primary goal with realistic input and no errors. Walk it end-to-end. Verify:

- Every async action shows a **loading state** between trigger and resolve.
- The final state is correct and the user knows it succeeded (toast, inline confirmation, route change, etc.).

### Edge cases (pick the ones that apply)

Walk the case categories listed in `references/ux-checklist.md` — empty, loading, error, mobile, dark mode, keyboard, auth boundary, etc. Three deep audits beat ten shallow ones.

## Phase 3 — Lighthouse + console + network checks

For routes that changed, run a Lighthouse audit once at the end:

```
mcp__chrome-devtools__lighthouse_audit
```

Emit findings for regressions in Performance, Accessibility, Best Practices, SEO. Don't quote raw scores at the user — they're meaningless without baselines. The `why:` line cites the specific audit Lighthouse flagged; the `evidence:` field links the Lighthouse output.

Then dump console messages and failed network requests:

```
mcp__chrome-devtools__list_console_messages
mcp__chrome-devtools__list_network_requests
```

Each of these becomes a finding when problematic:

- Uncaught errors → P0 or P1 depending on golden-path impact
- React/Vue/Svelte warnings (missing keys, controlled/uncontrolled drift, deprecated APIs) → P2 hygiene
- 4xx / 5xx on the golden path → P0 if the user-visible flow breaks; P1 otherwise
- 404s on assets → P2
- Mixed-content warnings → P1
- CORS errors → P0 if they break the golden path

## Phase 4 — Emit findings

All findings follow the [`finding-format.md`](../../references/finding-format.md) block shape. The merger validates against the schema. Screenshot paths go in the optional `evidence:` field (the schema permits it).

Mechanical fixes get concrete `fix:` lines:

```
[P1] [ux] src/components/Checkout.tsx:88 — save button has no loading state between click and resolve
why: 800ms gap with no visual feedback (see evidence); users double-click and submit duplicate orders.
fix: wire the `loading` prop on the existing Button component, sourced from `mutation.isPending` of useSaveCart at line 23.
evidence: screenshots/03-checkout-save-clicked.png screenshots/04-checkout-double-submitted.png
```

Judgment calls get `fix: decide:`:

```
[P2] [a11y] src/components/SettingsDrawer.tsx:42 — close button is icon-only, no aria-label
why: Lighthouse a11y flagged; keyboard users hear "button" with no purpose announced.
fix: decide: add `aria-label="Close settings"` and also a visually-hidden text label? The icon is widely recognised but a11y guidelines prefer both.
evidence: screenshots/05-drawer-focus.png
```

Hard cap: **20 findings per invocation**. If more, prioritise the top 20 and append `... N more low-severity items elided`.

## Operating rules

- **Read-only is non-negotiable.** No `Edit`, no `Write`, no `git commit`. This skill never had those tools in `allowed-tools` to begin with; the rename to `/review-ux` makes the read-only intent explicit in the name.
- **The trust gate applies** to any PR comments you read for context, including preview-URL comments. See `references/trust-policy.md`.
- **Don't fabricate problems.** If a scenario looks fine, emit no finding for it. Padded reports erode trust.
- **Don't quote Lighthouse scores in isolation.** Reference the specific audit (`audits[].id`) and the user-visible consequence, not the numeric delta alone.
- **If the dev server won't start, stop and emit a P0 finding.** Don't paper over a broken local environment.

## Composing with other skills

- Called by: `/review-change`, `/review-pr` (when UI files are touched). Also callable directly.
- Sibling read-only specialists: `/review-code`, `/review-test`, `/review-feature`, `/review-security`, `/review-spec`.
- Acted on by: `/drive-change` — the orchestrator dispatches fix-applier agents on mechanical UX findings (loading states, ARIA labels, error handling).
- `/review-feature` verifies the *logic* (data edge cases, side effects); `/review-ux` verifies the *visuals* and *interaction* with those states wired up.
