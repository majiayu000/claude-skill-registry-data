---
name: overlay-playwright-runtime
description: Adopt and operate the a11y-overlay runtime in Playwright or browser-agent repos. Use when Codex needs to vendor `a11y-overlay.js` plus `playwright/overlay-client.mjs` into another repo, or when Codex needs to audit a public site, authenticated web app, responsive route surface, attached desktop-shell surface, or visual evidence flow from a persistent Playwright session with reports, annotations, and artifact bundles.
---

# Overlay Playwright Runtime

Use this skill as a case router, not as a single long operator manual.

The runtime stays inside the page as a semantic inspection layer.
Playwright remains the action layer for clicks, typing, assertions, navigation,
and screenshots.

There are two implementation modes underneath everything:

1. `adopt`
2. `operate`

Do not open by asking the user to choose internal helper names.
Classify the case first, present the best-fit workflow in plain terms, then map
to the concrete helper.

## Start Here

Choose the case that matches the current request and read only that file next:

- `Adopt runtime into another repo`
  - read [references/cases/adopt.md](references/cases/adopt.md)
- `Audit current public page only`
  - read [references/cases/public-single-surface.md](references/cases/public-single-surface.md)
- `Audit all public routes across desktop and mobile`
  - read [references/cases/public-responsive-routes.md](references/cases/public-responsive-routes.md)
- `Audit authenticated app after sign-in`
  - read [references/cases/authenticated-surface.md](references/cases/authenticated-surface.md)
- `Audit authenticated navbar routes in the same live session`
  - read [references/cases/authenticated-navbar-routes.md](references/cases/authenticated-navbar-routes.md)
- `Audit attached desktop-shell surface`
  - read [references/cases/desktop-shell.md](references/cases/desktop-shell.md)
- `Capture visual evidence only`
  - read [references/cases/visual-evidence-only.md](references/cases/visual-evidence-only.md)

## Cross-cutting References

Read these only when the selected case needs them:

- persistent sandbox bootstrap and browser reuse:
  - [references/interactive.md](references/interactive.md)
- vendoring details, compatibility rules, temporary install cleanup:
  - [references/adoption.md](references/adoption.md)
- reporting doctrine, allowed claims, and report shape:
  - [references/reporting.md](references/reporting.md)
- Codex hook integration for trust-but-verify visual review:
  - [references/codex-hooks.md](references/codex-hooks.md)

## Default Case Routing

Use these heuristics:

- repo missing `a11y-overlay.js` or `playwright/overlay-client.mjs`
  - prefer `Adopt runtime into another repo`
- public site, one surface matters
  - prefer `Audit current public page only`
- public site, desktop and mobile use different route controls
  - prefer `Audit all public routes across desktop and mobile`
- sign-in required before auditing
  - prefer `Audit authenticated app after sign-in`
- sign-in required and the app is a stable SPA with a top navbar
  - prefer `Audit authenticated navbar routes in the same live session`
- already attached to a desktop shell or embedded browser page
  - prefer `Audit attached desktop-shell surface`
- user only wants screenshots or reviewable evidence
  - prefer `Capture visual evidence only`

When the case is clear, state the best match first and mention one or two
plausible alternatives only if they are genuinely relevant.

## Bundled Assets

This skill bundles its own runtime and sandbox assets so `adopt` and `operate`
stay deterministic:

- `assets/runtime/a11y-overlay.js`
- `assets/runtime/playwright/overlay-client.mjs`
- `assets/runtime/playwright/overlay-client-live.mjs`
- `assets/sandbox/package.json`
- `assets/sandbox/launch-session.mjs`
- `assets/sandbox/overlay-client-live.mjs`
- `assets/templates/accessibility-audit-report.md`
- `assets/templates/accessibility-audit-report.html`

## Guardrails

- Keep Playwright as the browser action layer.
- Keep the overlay runtime as the semantic inspection and annotation layer.
- Prefer the persistent sandbox session for local iteration inside Codex.
- Treat medium/low-confidence annotation placement as trust-but-verify: if a
  review descriptor requires visual review, inspect the returned flat preview
  image before applying or downgrading the placement.
- Do not relaunch the browser every turn unless ownership changed or the session
  is stale.
- Do not mutate a target repo `package.json` or lockfile from `adopt` unless the
  user explicitly asks.
- Do not push workflow policy into the runtime unless there is a concrete need.

## Validate

- skill sanity:
  - `uv run python $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py /absolute/path/to/overlay-playwright-runtime`
- sandbox verification:
  - `node $FRONTEND_GADGET_REPO/tests/verify_overlay_sandbox.mjs`
