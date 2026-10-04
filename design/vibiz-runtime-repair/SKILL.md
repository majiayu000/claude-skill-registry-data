---
name: vibiz-runtime-repair
description: Use when the sandbox app fails to build, boot, render, authenticate, call AI routes, read offers, or deploy cleanly.
compatibility: opencode
---

# Vibiz Runtime Repair

Repair the real failure. Do not bypass platform contracts to make an error disappear.

Start here:

- Read the exact error, terminal output, browser console, or failing route response.
- Inspect the file named in the stack trace before changing adjacent code.
- Check env-dependent code in `src/lib/auth.ts`, `src/middleware.ts`, `src/lib/sapiom.ts`, `src/lib/api-guard.ts`, and `scripts/migrate.mjs`.
- Check sandbox boot behavior in `e2b.toml` and template build behavior in `Dockerfile`.

Safe repair patterns:

- If auth is unavailable because Turso env vars are missing, preserve landing-page-only mode and existing guards.
- If AI routes fail because `SAPIOM_API_KEY` is missing, keep server-only behavior and return a clear unavailable state.
- If a user-supplied third-party integration truly requires a runtime key, put it in `.env` server-side and keep it out of browser-exposed `NEXT_PUBLIC_*` vars unless the key is designed to be public.
- If offers are missing, preserve `getSeededOffers()` fallback behavior and do not fabricate seeded offers.
- If Tailwind fails, fix class/config/CSS compatibility instead of removing whole sections.
- If Next build fails from runtime-only env assumptions, make the code tolerate absent envs during build without exposing secrets or disabling production behavior.

Verification:

- Run the failing command again after each targeted fix.
- Run `npm run build` before considering runtime repairs complete.
- Search for accidental secret exposure with `rg -n "SECRET|TOKEN|API_KEY|STRIPE"`.
