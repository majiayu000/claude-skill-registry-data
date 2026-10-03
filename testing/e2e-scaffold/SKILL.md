---
name: e2e-scaffold
description: Scaffold a reusable Playwright fixtures/config/smoke-test layer once per project. Trigger on "set up e2e/playwright testing", "add playwright", or before the first Playwright spec in a project without one.
---

# E2E Scaffold — Write the Plumbing Once, Reuse It Forever

Generating a full Playwright script from scratch for every test case burns tokens on
setup that never changes. This skill scaffolds the reusable layer — config, fixtures,
a smoke test — once per project. After that, new coverage is a few lines against
existing fixtures/Page Objects, not a new script.

Pairs with `coding-standards/qa/e2e-testing.md` (RULE QA-E2E-01–05) if the standards
system is installed — that file is the *rule*, this skill is the *scaffold* that makes
following it the path of least resistance. Works standalone if standards aren't installed.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — a stack this needed extra handling
   for, a detection heuristic that guessed wrong. Merge instead of duplicating.

## Step 1 — Check whether the scaffold already exists

Look for `playwright.config.ts`/`.js` at the project root and a `tests/e2e/fixtures.*`
file. If both exist, **do not re-scaffold** — read the existing `fixtures.ts` and any
`*.pom.ts` files and extend them for whatever new coverage was asked for. Re-running
this skill on a project that already has the layer is a bug, not idempotent setup.

## Step 2 — Detect the stack

Read `package.json` (or the project's manifest) to determine:
- Dev command and default port (`next dev` → 3000, `vite` → 5173, `astro dev` → 4321, etc. — verify the actual configured port rather than assuming the framework default, since projects often override it)
- Package manager (npm/pnpm/yarn) from the lockfile present
- Whether `@playwright/test` is already a dependency

If `@playwright/test` is missing, tell the user what will be installed and why, then
install it as a dev dependency — this is a `package.json` change and follows the same
confirm-before-acting posture as any other dependency addition. Also ensure the
Chromium browser binary is installed (`playwright install chromium`).

## Step 3 — Write the scaffold

Create the three files in `e2e-scaffold.templates.md` (same skill folder), adapting
the `{{PORT}}`/`{{DEV_COMMAND}}` placeholders to what Step 2 found. Keep the fixtures
file to **universal concerns only** — no feature-specific selectors, no guessed Page
Object methods. Feature coverage is written later, per Step 5.

## Step 4 — Wire it up

- Add a `"test:e2e": "playwright test"` script to `package.json`.
- Add to `.gitignore` (create the block if absent):
  ```
  /test-results
  /playwright-report
  /blob-report
  /playwright/.cache
  ```
- If `coding-standards/qa/e2e-testing.md` is installed, it needs no edits — it already
  documents this layer. If the project has no coding-standards system, briefly note to
  the user that RULE QA-E2E-01–05's discipline (specs updated in the same commit as the
  behaviour they cover, never left stale-but-green) still applies even without the file.

## Step 5 — Verify, then stop

Run `test:e2e` and confirm the smoke test passes before reporting done — an unverified
scaffold is worse than none. **Do not** generate additional feature-specific specs at
this point; that's the next request, done against the fixtures/POM layer just built,
not a blind batch of guessed coverage (see QA-E2E-02/03 if the standard is installed).
