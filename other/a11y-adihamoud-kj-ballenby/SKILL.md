---
name: a11y
description: Run every accessibility check (jsx-a11y lint, scan coverage and contrast unit tests, the diff check, axe on every page in he/en, keyboard and reflow tests) and summarize violations with file:line and the fix. Use after UI changes, before a PR that touches apps/web, or when the Accessibility CI job is red.
---

From the repo root:

```bash
pnpm --filter @kj/web lint
pnpm --filter @kj/web test -- src/lib/a11y
pnpm a11y:diff
pnpm test:scripts
pnpm --filter @kj/web build
pnpm --filter @kj/web test:a11y
```

Notes:

- `test:a11y` runs `e2e/a11y.spec.ts` (axe, every entry in `src/lib/a11y/routes.ts`, both
  locales, Chromium and WebKit) and `e2e/a11y-keyboard.spec.ts`. Add `--project=mobile-chrome`
  for a quicker first pass.
- If another dev server holds `apps/web/.next` or port 3000, build and test with
  `NEXT_DIST_DIR=.next/e2e PORT=3100 NEXT_PUBLIC_SUPABASE_URL= NEXT_PUBLIC_SUPABASE_ANON_KEY=`
  on both commands (demo mode, like CI), and revert `apps/web/tsconfig.json` afterwards.
- A failing axe test prints each violation with its rule, help link, CSS selector and
  `failureSummary`; the full JSON is attached to the test in `apps/web/playwright-report`
  (in CI: the `a11y-report` artifact).
- Fix the cause in the component or token, not the test. `color-contrast` failures usually mean
  white text on `bg-brand`/`bg-brand-2`: use `bg-brand-fill`/`bg-brand-2-fill`.
- "scans every page" failing in the unit tests means a new `page.tsx` needs an `A11Y_SCANS` entry.

Report: green/red per check, each violation as `file:line - rule - who it affects - fix`, and
what you changed.
