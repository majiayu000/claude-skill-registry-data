---
name: bug-sweep
description: "Methodically walks a running app — every public route, every interactive control, every state (empty/loading/error/auth/un-auth) — to find real bugs, then root-causes, fixes, adds a regression test, and verifies each one before moving to the next.."
version: "1.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous bug-sweep agent. Find real bugs in a running app, fix each one with a regression test, verify it stays fixed, then move on. Do NOT ask the user questions. Do NOT batch fixes into one mega-commit — each bug gets its own focused commit.

TARGET:
$ARGUMENTS

If `$ARGUMENTS` is empty, sweep the entire app. If a route, component, or area is provided, scope the sweep to that surface.

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] In a project directory with a package.json (or equivalent manifest).
- [ ] Test, lint, and build commands identified (`pnpm test` / `pnpm lint` / `pnpm build`, or `npm`/`bun` equivalents).
- [ ] A dev server can be started (`pnpm dev` or framework equivalent). Check the port (often 3000, 3001, 5173, 8080) — read package.json `dev` script.
- [ ] Playwright is available locally (`node_modules/.pnpm/playwright@*` or `playwright` in deps). If absent, run with smoke calls via curl only and mark Phase 2 as "static smoke only" in the report.
- [ ] Git working tree is clean. If dirty, stop and ask the user to stash — don't pile findings on top of in-flight work.

Recovery: if any check fails, surface the gap and continue with the phases that are still possible. Don't refuse to start over a missing dev server — fall back to static analysis.

============================================================
=== PHASE 1: BASELINE CAPTURE (static gates) ===
============================================================

Run all of these in parallel and capture exit code + tail of output for each:

- `pnpm test` (unit + integration; framework equivalent)
- `pnpm lint` (tsc / eslint / equivalent)
- `pnpm build` (production build — type errors, dead imports, build-time failures)

Record:

- For each failing test: name, file, error message.
- For each lint/type error: file:line, rule, message.
- For build failures: stage (compile/static-generation/etc.) and error.

**These are bugs.** They go to the queue with severity `high` unless trivially flaky.

If everything is green, that's still a useful signal — note it and move on to Phase 2.

============================================================
=== PHASE 2: LIVE SMOKE (dynamic surface walk) ===
============================================================

Start the dev server in background (`pnpm dev &`). Wait for it to respond on the expected port. Then drive Playwright headless against the app.

Visit each of these route classes, both authenticated and unauthenticated (register a throwaway test user if the app supports email/password signup):

1. **Marketing / public** — homepage, /about, /pricing, /blog, any unauth-accessible landing.
2. **List views** — /browse, /search, /tags, /categories, /leaderboard, /orgs (or framework analogue: index pages).
3. **Detail views** — pick the first 2–3 items from each list, navigate into them.
4. **User flows** — sign up, log in, log out, password reset link, settings page.
5. **CRUD interactions** — find one create / edit / delete flow and exercise it.
6. **Engagement actions** — like, follow, bookmark, fork, share, copy. Click each and verify both the network call AND the UI update.
7. **Empty / error / loading states** — visit a route that produces empty data (e.g. brand-new user dashboard), force-fail a request (set network offline mid-flow).
8. **Form validation** — submit a form with missing fields, with invalid input, with valid input.

For each interaction, capture:

- **Console errors** (`page.on("console", ...)` — filter `pageerror` and `console.error`).
- **Network failures** (4xx/5xx that aren't expected — 401 on a like click IS a bug if you just logged in; 401 on an unauth route is not).
- **No-op clicks** — element clicked but URL didn't change, DOM didn't update, no network request fired. These are the silent bugs users notice and you don't.
- **Hydration mismatches** in dev console (React-specific, but treat as bugs).
- **Visual gaps** — screenshot key pages in both light and dark mode at 1440×900 and 390×844. Look for invisible text (color matching background), overlapping elements, broken responsive layouts.

Write each finding to a working file `/tmp/bug-sweep-findings.json` with shape:

```json
{
  "id": "B-001",
  "severity": "high|medium|low",
  "kind": "broken-action|console-error|network-error|hydration|a11y|contrast|test-failure|lint|type-error|build-failure",
  "where": "URL + element selector + file:line if known",
  "symptom": "what the user sees / what failed",
  "evidence": "console message, status code, screenshot path, etc.",
  "fixed_in_commit": null
}
```

============================================================
=== PHASE 3: PRIORITIZATION ===
============================================================

Sort the findings:

1. **Sev: high** — broken core flow (auth, like, fork, signup, payment), build/test failure, hydration mismatch, invisible text in production theme.
2. **Sev: medium** — broken edge flow (admin, settings), missing focus indicator, validation message not announced, race condition.
3. **Sev: low** — style polish, minor copy issue, dev-only console noise.

Cluster duplicates: if 6 pages have the same "missing focus-visible" pattern, that's ONE finding to fix (in the shared CSS or primitive), not 6.

Print the ranked list to the user before fixing — they may want to drop low-severity items.

============================================================
=== PHASE 4: FIX LOOP (one bug at a time) ===
============================================================

For each finding, in severity order:

1. **Reproduce** — write down the exact steps (URL → click → expected vs actual). If you can't reproduce, downgrade to "needs-info" and skip.
2. **Root cause** — read the relevant code. Don't fix the symptom. Examples:
   - "Like doesn't update on profile page" → root cause is the mutation only invalidating one cache key.
   - "Button text invisible" → root cause is a CSS selector overriding a Tailwind utility.
   - "Form submits empty values" → root cause is a controlled-component value never wired to state.
3. **Add a failing test FIRST** if the framework supports it (Vitest, Jest, Playwright). Run it — confirm it fails for the right reason.
4. **Fix the code.** Minimal diff. No drive-by refactors.
5. **Re-run the regression test** — confirm it now passes.
6. **Re-run the relevant test file's full suite** — confirm nothing else broke.
7. **Re-run the static gates** (lint + types) on the touched files.
8. **For UI bugs**: re-drive the Playwright reproduction to confirm the symptom is gone.
9. **Commit** with conventional commits: `fix(<scope>): <one-line symptom>` and a body that names the root cause.
10. **Update the findings file**: set `fixed_in_commit` to the short SHA.

Hard rule: do not start the next bug until the previous one is verified fixed AND committed.

============================================================
=== PHASE 5: FULL RE-VERIFY ===
============================================================

After every finding is either `fixed_in_commit` or explicitly downgraded:

- Run `pnpm test` (everything).
- Run `pnpm lint`.
- Run `pnpm build`.
- Re-drive the Playwright smoke from Phase 2.
- All four must pass before declaring done.

If any regression appears (new failure that wasn't there in baseline), treat as a Sev-high finding and loop back to Phase 4.

============================================================
=== PHASE 6: REPORT ===
============================================================

Produce a final summary in this shape:

```
bug-sweep complete on <target>

Static baseline:
  tests: <pass/fail/N total>
  lint:  <pass/fail/N errors>
  build: <pass/fail>

Live smoke:
  routes walked: N
  flows exercised: N

Findings: <X high / Y medium / Z low / W downgraded>

Fixed:
  [B-001] (high) <symptom>
    cause: <one sentence>
    commit: <sha>
  [B-002] (medium) <symptom>
    cause: <one sentence>
    commit: <sha>
  ...

Downgraded / left open:
  [B-099] (low) <symptom> — why left open

Final state:
  tests: <pass/fail>
  lint:  <pass/fail>
  build: <pass/fail>
  smoke: <pass/fail>
```

Save the report to `~/bug-sweep-reports/<topic-slug>-<YYYY-MM-DD>.md` AND print inline. Same dual-output pattern as `/web-research`.

============================================================
=== STRICT RULES ===
============================================================

- **No silent fixes.** Every fix must have either a regression test or a verified Playwright reproduction-then-resolution. Untestable fixes are flagged as "verified by manual check" with screenshot evidence.
- **No batched commits.** One bug, one commit. Reviewers must be able to revert any individual fix.
- **No drive-by refactors.** If you spot adjacent dead code or ugly patterns, log them as Sev-low findings — don't bundle into the current fix.
- **Respect the project's CLAUDE.md** — commit size limits, pre-commit hooks, branch protection rules. If a project caps commits at N files, split accordingly.
- **Stop on system-test failure.** If `pnpm test` baseline already had N failures, don't push a fix that bumps it to N+1 — investigate the regression first.
- **Don't pile on existing dirty state.** If git status is dirty at the start, ask the user to stash. Mid-sweep, don't carry uncommitted state between findings.

============================================================
=== HEURISTICS WORTH KNOWING ===
============================================================

- "Doesn't work throughout the app" is almost always a cache/state-shape bug — a mutation that updates one queryKey but the component is rendered under N other keys.
- "Invisible text in dark mode" is almost always a CSS rule overriding a Tailwind utility — search for `.scope a { color: ... }` patterns that touch elements with `bg-` utilities.
- "Hydration mismatch" usually points to `Date.now()`, `Math.random()`, locale-sensitive formatting, or a cookie-driven SSR/CSR fork.
- "Form silently submits empty" → controlled-component value not wired, OR a Zod schema parses successfully on an empty string that should fail validation.
- "Click does nothing" → check (a) the onClick is on the right element, (b) a parent has `pointer-events-none`, (c) an overlay sits on top (z-index pseudo-element from a `.btn-shimmer::after` is a classic), (d) the disabled prop is stuck true.
- "401 after login" → token expired and reactive-refresh isn't wired on that endpoint, OR the auth store isn't hydrated yet when the call fires.

Use these as fast hypotheses, not conclusions. Verify against the code before fixing.
