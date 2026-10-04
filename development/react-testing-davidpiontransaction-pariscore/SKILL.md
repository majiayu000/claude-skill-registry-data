---
name: react-testing
description: Testing strategy for React apps — when to reach for Playwright (E2E) vs Vitest (unit/component) vs both, the senior testing pyramid for an SPA, Playwright setup with config + webServer + per-spec project structure, Vitest setup with jsdom + Testing Library, a11y-first locators (getByRole, getByLabel, toBeFocused, toHaveAttribute), assertion patterns for aria-pressed/aria-current/role=alert/focus-on-route-change, @axe-core/playwright for automated a11y audits, running against localhost vs deployed URL via env var, what NOT to test, common flakiness sources and fixes. Use whenever the project needs tests added — interview "would you add tests?" question, real production CI, or post-build polish layer. Triggers on "test", "testing", "playwright", "vitest", "jest", "e2e", "end-to-end", "unit test", "component test", "@playwright/test", "@axe-core/playwright", "getByRole", "testing library", "rtl", "smoke test", "ci tests", "test runner".
---

# react-testing

Senior testing isn't about coverage percentages — it's about catching the regressions that matter while staying fast and stable. This skill gives you the decision framework and paste-ready setup for both layers.

## The senior testing pyramid for a typical React SPA

Most SPAs need **two thin layers**, not five:

| Layer | Tool | What to test | Roughly |
|---|---|---|---|
| **Unit / pure logic** | Vitest | Pure functions, transforms, adapters, the parts of the API client that aren't `fetch` | 20% of test code |
| **E2E** | Playwright | The 4-6 happy paths a real user takes, plus focus / a11y wiring | 80% of test code |
| ~~Component tests in RTL~~ | (skip by default) | Most "component tests" duplicate either unit or E2E coverage with more boilerplate | 0% |

**When to add RTL component tests anyway:**
- A single component has gnarly internal state worth isolating (a complex form, a step machine)
- You have a component library that's the deliverable, and each export needs its own spec
- A11y-sensitive primitive (combobox, listbox) where the internal interaction matrix is the product

For a typical product SPA, **skip the middle layer**. Playwright's `getByRole` queries give you the same a11y guarantees as RTL with the real browser doing the rendering.

## The Playwright recipe (this is what to install)

```bash
npm install -D @playwright/test
npx playwright install chromium
```

Then `playwright.config.ts` — the version that lets one spec suite test both localhost AND the deployed URL:

```ts
import { defineConfig, devices } from "@playwright/test";

const baseURL = process.env.E2E_BASE_URL ?? "http://localhost:5173";
const usingExternalServer = !!process.env.E2E_BASE_URL;

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI ? "github" : "list",
  use: {
    baseURL,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  // Only spin up Vite when we're not pointing at a deployed URL.
  webServer: usingExternalServer
    ? undefined
    : {
        command: "npm run dev",
        url: "http://localhost:5173",
        reuseExistingServer: !process.env.CI,
        timeout: 30_000,
      },
});
```

And the `package.json` scripts:

```json
{
  "scripts": {
    "e2e": "playwright test",
    "e2e:ui": "playwright test --ui",
    "e2e:prod": "E2E_BASE_URL=https://your-app.netlify.app playwright test"
  }
}
```

Why these three and not more:
- `e2e` — local headless run, the daily driver
- `e2e:ui` — debugging a failing spec, time-travel snapshots, locator inspector
- `e2e:prod` — smoke test the live deploy after pushing; CI can run this on a schedule

**`.gitignore`** additions:

```
/test-results
/playwright-report
/playwright/.cache
```

## What to put in `e2e/` — the 4-spec template

For a typical SPA, four spec files cover almost everything worth testing:

```
e2e/
  homepage.spec.ts    Landing/list page: data renders, filters work, pagination wires up
  detail.spec.ts      Navigation in + out of a detail route; focus management
  errors.spec.ts      404, network failure, invalid input — every error state
  a11y.spec.ts        Keyboard order, landmarks, no console errors, axe scan
```

Don't make one giant `e2e.spec.ts`. Per-file describe blocks let Playwright parallelize and let you read failures faster.

## A11y-first locators — the senior signal

Use **role-based queries** by default. Anything else is a smell that you're testing implementation, not behavior.

```ts
// Good — describes user intent
await page.getByRole("button", { name: /audio/i }).click();
await page.getByRole("heading", { level: 1, name: "Post title" });
await page.getByRole("alert");
await page.getByRole("navigation", { name: "Pagination" });
await page.getByRole("link", { name: /skip to main content/i });
await page.getByLabel("Email");

// OK — when role isn't expressive enough
await page.getByText(/\d+ shown/);
await page.locator("main article");

// Smell — testing structure, not behavior
await page.locator(".filter-chip-button");        // CSS class
await page.locator("#filter-3");                  // generated ID
await page.locator("[data-testid='filter']");     // testid is a last resort
```

Order of preference (matches React Testing Library guidance):
1. `getByRole` with name (matches what a screen reader announces)
2. `getByLabel`, `getByPlaceholder`, `getByText`
3. `getByTestId` — only when nothing semantic exists, which should be rare

If you can't find a role-based query, that's often a signal the UI itself is missing semantics.

## Assertion patterns for the four a11y wirings you'll most often test

These are the patterns that came up in the kratecms-reader build. Memorize them.

### Focus moves to the H1 on SPA route change

```ts
await page.getByRole("link", { name: "Some post" }).click();
const h1 = page.getByRole("heading", { level: 1 });
await expect(h1).toBeFocused();
await expect(h1).toHaveAttribute("tabindex", "-1");   // confirms it's the right pattern
```

### `aria-current="page"` on the active nav / pagination item

```ts
const pagination = page.getByRole("navigation", { name: "Pagination" });
await expect(pagination.getByRole("button", { name: "Page 1" }))
  .toHaveAttribute("aria-current", "page");

await pagination.getByRole("button", { name: "Page 2" }).click();
await expect(pagination.getByRole("button", { name: "Page 2" }))
  .toHaveAttribute("aria-current", "page");
```

### `aria-pressed` on toggle buttons (filter chips, etc.)

```ts
const audioChip = page.getByRole("group", { name: "Filter by category" })
  .getByRole("button", { name: /^audio/ });
await audioChip.click();
await expect(audioChip).toHaveAttribute("aria-pressed", "true");
```

### `role="alert"` for error states

```ts
await page.goto("/posts/99999");
const alert = page.getByRole("alert");
await expect(alert).toBeVisible();
await expect(alert).toContainText(/not found/i);
// 4xx errors shouldn't offer retry
await expect(alert.getByRole("button", { name: /try again/i })).toHaveCount(0);
```

### Skip link revealed on first Tab

```ts
await page.goto("/");
await page.keyboard.press("Tab");
await expect(page.getByRole("link", { name: /skip to main content/i }))
  .toBeFocused();
```

## The `no-console-errors` spec — every project should have this

Catches the bugs that don't break a render but ship a noisy console:

```ts
test("no console errors on a typical browse session", async ({ page }) => {
  const errors: string[] = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });
  page.on("pageerror", (err) => errors.push(err.message));

  await page.goto("/");
  // walk a real path
  await page.locator("main article").first().getByRole("link").first().click();
  await page.waitForURL(/\/posts\//);
  await page.getByRole("link", { name: /back|all posts/i }).click();

  // filter out known third-party noise
  const ownErrors = errors.filter(
    (e) => !/soundcloud\.com|youtube\.com|X-Frame-Options/i.test(e),
  );
  expect(ownErrors, ownErrors.join("\n")).toHaveLength(0);
});
```

Two key things:
1. Listen on both `console` (`msg.type() === 'error'`) **and** `pageerror` (uncaught exceptions).
2. Filter known third-party noise — third-party iframes are notorious for `X-Frame-Options` complaints that you can't fix.

## @axe-core/playwright for automated a11y scans

```bash
npm install -D @axe-core/playwright
```

```ts
import AxeBuilder from "@axe-core/playwright";

test("homepage has no axe violations", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

Axe catches ~30-40% of automatable a11y issues (color contrast, missing alt, mis-wired ARIA). It's not a substitute for manual testing — but landing it in CI prevents regressions from sneaking in.

Common refinements:
```ts
const results = await new AxeBuilder({ page })
  .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])   // pin standards
  .disableRules(["color-contrast"])                          // if a known design exception
  .exclude("iframe")                                         // skip third-party content
  .analyze();
```

## The Vitest recipe (only if you need it)

```bash
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/jest-dom
```

`vitest.config.ts`:

```ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./vitest.setup.ts"],
    globals: true,
  },
});
```

`vitest.setup.ts`:

```ts
import "@testing-library/jest-dom/vitest";
```

Then a spec that tests the parts worth isolating — pure functions, not components:

```ts
// src/api/client.test.ts
import { describe, it, expect } from "vitest";
import { normalizeMeta } from "./client";

describe("normalizeMeta", () => {
  it("unboxes [v, v] arrays back to scalars", () => {
    expect(normalizeMeta({
      current_page: [3, 3], last_page: [5, 5], per_page: [15, 15], total: [73, 73],
      from: 31, to: 45, path: "x",
    }).current_page).toBe(3);
  });

  it("passes through scalar values unchanged (forward-compat with fixed API)", () => {
    expect(normalizeMeta({
      current_page: 3, last_page: 5, per_page: 15, total: 73,
      from: 31, to: 45, path: "x",
    } as any).current_page).toBe(3);
  });
});
```

**When to add a Vitest component test:**
- The component has internal state that's hard to drive via a real browser
- You'd otherwise need 20 lines of E2E setup to test one branch
- The component is a primitive in a design system

**When NOT to add a component test:**
- The "component test" would be `render() → click → assert text` — that's an E2E with extra steps
- The behavior depends on routing, network, or browser APIs — use Playwright
- You're testing prop combinations — use a TypeScript test (`expectTypeOf`) instead

## What NOT to test

| Don't test | Why |
|---|---|
| Implementation details (state shape, internal hooks) | Refactors break the test for no reason |
| Third-party iframe content | You don't own it; flake guaranteed |
| Exact pixel layouts (use visual regression instead) | Pixels shift with font hinting, AA |
| The framework itself (does `useState` work?) | Not your code |
| Every prop combination (use TS types) | TypeScript catches this at compile time |
| Snapshots of large trees | Reviewers blind-accept; not a real test |

## Flakiness — the 5 most common causes and fixes

| Cause | Fix |
|---|---|
| `await page.waitForTimeout(500)` | Use `waitForURL`, `waitForResponse`, or auto-retrying assertions. Hard timeouts are flake-bait. |
| Asserting on text that depends on live API data | Assert on **structure** ("at least one card visible") not specific titles. Pin to a stable record for content assertions. |
| Animations not finished when asserting | `await expect(thing).toBeVisible()` waits for stable layout. If still flaky, gate animations on `prefers-reduced-motion` in the test fixture. |
| Network race between two fetches | `await page.waitForResponse(url)` before asserting on the result. |
| State leaking between tests | Use `test.beforeEach` to reset. Never share `page` instances across tests. |

## Running against localhost vs the deployed URL

The `E2E_BASE_URL` pattern in the config above lets one suite serve two purposes:

```bash
npm run e2e         # localhost — daily driver, runs Vite via webServer
npm run e2e:prod    # deployed URL — smoke test after a deploy
```

For CI: run `npm run e2e` on every PR (catches regressions before merge). Schedule `npm run e2e:prod` to run hourly or after deploys (catches infra drift).

**Don't** point `E2E_BASE_URL` at production for the PR run — every PR would hit your live site dozens of times.

## When the interviewer asks "what about tests?"

Senior answer follows this skill:

1. "I'd add Playwright for the routing, focus management, and filter behavior — those are the 4-6 happy paths a user takes."
2. "Vitest for the pure helpers — `normalizeMeta`, the YouTube ID extractor. Not for components; the E2E covers them."
3. "I skip component-level RTL by default unless I have a primitive that needs prop-by-prop coverage."
4. "axe in CI for automated a11y regressions, plus manual keyboard pass before shipping."
5. "I'd run E2E against localhost in PRs and against the deployed URL on a schedule."

That's the answer, in 30 seconds, that signals senior.

## Narration phrases

- "I used `getByRole` everywhere — if I can't find a role-based query, that's a signal the UI is missing semantics."
- "The focus-on-route-change spec is a one-liner: `await expect(h1).toBeFocused()`. That's the single highest-value a11y assertion for an SPA."
- "I have one `no-console-errors` spec walking a typical browse path — catches the bugs that don't break a render but ship a noisy console."
- "I skipped component tests — Playwright covers them with the real browser, and Vitest covers the pure helpers. The middle layer would duplicate both."
- "Vitest config for `normalizeMeta` is six lines including imports. Not worth a heavier framework."

## Authoritative references

- Playwright docs: https://playwright.dev/docs/intro
- Playwright a11y testing: https://playwright.dev/docs/accessibility-testing
- Playwright locators: https://playwright.dev/docs/locators
- @axe-core/playwright: https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright
- Vitest docs: https://vitest.dev/
- React Testing Library: https://testing-library.com/docs/react-testing-library/intro
- Testing Library guiding principles: https://testing-library.com/docs/guiding-principles
- Kent C. Dodds — testing trophy: https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
