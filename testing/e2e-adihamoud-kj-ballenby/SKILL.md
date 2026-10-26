---
name: e2e
description: Build the web app and run the Playwright end-to-end suite on mobile viewports. Use after UI changes or when adding a route.
---

```bash
pnpm --filter @kj/web build
pnpm --filter @kj/web exec playwright install chromium
pnpm --filter @kj/web test:e2e --project=mobile-chrome
```

Notes:

- Tests live in `apps/web/e2e/*.spec.ts` and run against `next start` on port 3000 (the config
  starts it). Set `PLAYWRIGHT_BASE_URL` to test a preview deployment instead.
- Without Supabase env vars the auth buttons render disabled and protected routes redirect to
  login; tests are written to pass in that mode so CI needs no secrets.
- A new route needs at least one smoke test: it renders in `/he` with `dir="rtl"` and in `/en`.
- On failure, open `apps/web/playwright-report/index.html` or read the trace in
  `apps/web/test-results/`.
