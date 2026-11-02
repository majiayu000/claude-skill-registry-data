---
description: Run a runtime accessibility audit using axe-core via Playwright and review the results
---

# Accessibility Audit

Run the axe-core runtime accessibility audit and analyze the results.

## Steps

1. **Run the a11y E2E test** to get current violations:
   ```bash
   E2E_MOCK=true npx playwright test e2e/specs/a11y-audit.spec.ts --project=web-chromium --reporter=list 2>&1
   ```

2. **Analyze the output**:
   - The test scans multiple pages/states of the app using axe-core
   - Each violation includes: rule ID, impact level (critical/serious/moderate/minor), affected elements, and a help URL
   - Violations are printed as structured JSON in test failure output

3. **Triage the results** and present a summary grouped by impact:
   - **Critical/Serious**: These should be fixed — they block assistive technology users
   - **Moderate**: Should be fixed when touching those components
   - **Minor**: Nice to have, low priority

4. **For each violation**, explain:
   - What the issue is in plain language
   - Which component/file is likely responsible (map CSS selectors back to source)
   - The recommended fix

5. **Ask the user** which violations they'd like to fix before making changes.

## Key files

- `e2e/specs/a11y-audit.spec.ts` — The Playwright test that runs axe-core scans
- `.eslintrc.json` — Static a11y lint rules (eslint-plugin-jsx-a11y)

## Notes

- The E2E test runs against the mock dev server (E2E_MOCK=true), so it audits the real rendered DOM
- axe-core checks WCAG 2.1 AA by default
- Some violations may come from third-party components (shadcn/ui, Radix) — note these separately
- Do NOT run `npm build` — the test uses the Vite dev server
