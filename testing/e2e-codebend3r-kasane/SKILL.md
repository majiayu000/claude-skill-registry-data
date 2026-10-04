---
name: e2e
description: Use when adding or fixing browser-level tests for kasane, when a change touches routing, deep links, the Netlify SPA fallback or MangaDex proxy, or when asked to verify a user journey end to end rather than with unit tests.
---

# End-to-End Tests

Playwright drives the **real `dist/` export**, not a dev server, so the suite covers the bundle that actually ships including the SPA fallback and the MangaDex proxy shape.

## Run it

```bash
bun run e2e:install     # once: downloads chromium
bun run build:web       # required — the suite serves dist/
bun run e2e
bun run e2e -- --headed --project=chromium   # watch it
```

`e2e/serve.ts` serves `dist/` on port 4173 and reproduces the two `netlify.toml` behaviours the app depends on: fallback to `index.html` for any unmatched path, and `/_mdx/*` proxied to `api.mangadex.org`. Playwright starts it via `webServer` and reuses a running one locally.

**A stale `dist/` silently tests old code.** Rebuild before trusting a pass.

## Writing a test

Target visible copy the app owns. React Native Web renders deeply nested unlabelled `div`s whose structure changes whenever a `StyleSheet` does, so CSS selectors and `nth` indexes rot immediately.

| Prefer                                     | Avoid                         |
| ------------------------------------------ | ----------------------------- |
| `getByPlaceholder(/search/i)`              | `locator("input").nth(2)`     |
| `getByText(/quick lookup/i)`               | `locator("div > div > span")` |
| `getByRole("button", { name: "Sign in" })` | `locator(".css-1a2b3c")`      |

Once the `accessibility` skill has annotated a surface, switch its tests to `getByRole` with the accessible name. That makes the e2e suite double as an a11y regression check: a lost `accessibilityLabel` fails a test.

Pick a **stable, fully mapped** catalog entry for detail-route tests (`/series/5114`, Fullmetal Alchemist: Brotherhood). Do not assert on remote AniList or MangaDex copy: titles, descriptions, and cover URLs change upstream and would make the suite flaky.

## What belongs here

| Layer                             | Test it with                            |
| --------------------------------- | --------------------------------------- |
| Pure mapping maths, merge logic   | Jest, via `domain-tests`                |
| A screen renders and responds     | Playwright                              |
| Deep link and SPA fallback        | Playwright, asserting `res.status()`    |
| Auth and progress sync round-trip | Playwright, against a throwaway account |

Do not re-test range arithmetic through the browser. Assert that Quick Lookup _produces an answer_; assert _which_ answer in a Jest test.

## Wiring into CI

`system-check` deliberately does not run e2e: it is the pre-commit and pre-push hook, and a chromium download plus a web build per commit is too slow. Add e2e as a separate CI job after the build step in `.github/workflows/ci.yml`, reusing the `dist/` the build job already produced.

## Common mistakes

| Mistake                                     | Consequence                                                      |
| ------------------------------------------- | ---------------------------------------------------------------- |
| Running `bun run e2e` without rebuilding    | Tests pass against the previous bundle.                          |
| Asserting on AniList titles or descriptions | Upstream edits break the suite for reasons unrelated to the app. |
| Using `waitForTimeout`                      | Flaky. Use `expect(...).toBeVisible()`, which retries.           |
| Adding e2e to `system-check`                | Every commit pays a full web build. Keep it a separate CI job.   |
| Testing arithmetic through the UI           | Slow and imprecise. That is what `domain-tests` is for.          |
