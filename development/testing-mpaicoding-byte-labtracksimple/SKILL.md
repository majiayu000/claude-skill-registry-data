---
name: testing
description: Testing guidance for this repo (unit, component, integration, and E2E). Includes troubleshooting.
---

# Testing (Repo-Specific)

Use this skill when running or troubleshooting tests in this repo. Tests must be run by the agent (automatic); do not ask the user to run them.

## Playwright (E2E)
- **Dev server EPERM**
  - Start `npm run dev` in the host terminal and run tests with:
    - `E2E_BASE_URL=http://127.0.0.1:3000`
- **Supabase target**
  - Tests run against the external Supabase project only; keep `.env.local` pointing to the remote project.
- **System Chrome permission errors**
  - Use bundled Chromium (default) by leaving `PW_USE_CHROME` unset.
  - Only set `PW_USE_CHROME=true` if you explicitly want system Chrome.
- **Missing bundled browsers**
  - Run once: `npx playwright install`
- **E2E entry command pattern**
  - `E2E_BASE_URL=http://127.0.0.1:3000 npm run test:e2e -- <spec>`
- **Review/commit setup**
- Set `SUPABASE_SERVICE_ROLE_KEY` in `.env` so admin seeding is not skipped.
  - Wait for sign-in redirect before navigating to protected review URLs.

## UI Verification (Mandatory)
- Any UI change requires verification using the Chrome DevTools MCP.
- Save verification screenshots in `docs/screenshots` only (remove any other screenshot folders), using `<scenario>_<version>.png` (e.g. `login_001.png`).

## Unit / Component
- Unit: `npm run test` (node --test).
- Component: `npm run test:unit` (vitest + jsdom).

## Integration
- Use Supabase MCP for DB setup, verification or anyting and don't call via cli or use local supabase installation.

## Lint / Typecheck
- Lint: `npm run lint`.
- Typecheck: `tsc --noEmit` (or project script if present).

# General
- If any error is found while testing, or any bug is reported, create a test for that if that doesn't exist
- Supabase MCP is there if you want to interact with supabase outside the unit, e2e, integration tests.
