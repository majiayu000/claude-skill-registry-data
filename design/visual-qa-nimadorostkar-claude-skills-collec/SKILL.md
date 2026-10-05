---
name: visual-qa
description: Use when verifying that a UI renders correctly. Covers visual regression testing, responsive checks across breakpoints, cross-browser verification, and screenshot-based review of an implementation against a design.
metadata:
  category: frontend
  version: 1.0.0
  tags: [visual-testing, regression, screenshots, responsive, qa]
---

# Visual QA

## Purpose

Catch visual defects before users do. Functional tests confirm the button works; they say nothing about the button being invisible, overlapping, or off-screen on a phone.

## When to Use

- Verifying an implementation against a design.
- Setting up visual regression testing.
- Checking responsive behavior across breakpoints.
- Reviewing a UI change that a unit test cannot meaningfully assert on.

## Capabilities

- Visual regression testing with deterministic screenshots.
- Responsive verification across a defined breakpoint set.
- Cross-browser and cross-platform rendering checks.
- Design-to-implementation comparison.
- Detection of layout shift, overflow, and truncation.

## Inputs

- The design reference, if there is one.
- The breakpoints and browsers that are in scope.
- The pages or components under test, and their states.

## Outputs

- Baseline screenshots committed to the repository.
- A diff report for each change, with the pixel delta.
- A list of visual defects with viewport and browser.

## Workflow

1. **Enumerate the states** — Not just the happy one. Empty, loading, error, long content, and the state with a 60-character name in a field designed for eight.
2. **Make screenshots deterministic** — Freeze time, seed data, disable animations, and wait for fonts and images. A flaky visual test is worse than no visual test; it will be ignored, then deleted.
3. **Capture at every breakpoint** — Mobile (375), tablet (768), desktop (1280), wide (1920). Check the boundaries themselves, where layouts switch.
4. **Diff against the baseline** — Review each diff. Approve intentional changes to update the baseline; investigate the rest.
5. **Check the overflow cases** — Long words, long lists, missing images, and a 200% browser zoom. These are where layouts break, and where designs rarely go.

## Best Practices

- Animation and time are the two causes of visual-test flakiness. Disable both in the test environment before you do anything else.
- Screenshot the component, not the whole page, when testing a component. A full-page baseline changes every time anything on the page does.
- A visual diff threshold that is too tight flags anti-aliasing noise; too loose and it misses a 4px misalignment. Tune it once, on real diffs.
- Test the states that are hard to reach manually — error, empty, and loading — because those are the ones nobody looks at before shipping.
- Run visual tests in a container so the fonts and rendering engine are identical to CI. Screenshots taken on macOS will not match those taken on Linux.
- Review the diff, do not just approve it. A rubber-stamped baseline update defeats the entire mechanism.

## Examples

**Deterministic Playwright visual test across breakpoints and states:**

```typescript
const VIEWPORTS = [
  { name: "mobile",  width: 375,  height: 812 },
  { name: "tablet",  width: 768,  height: 1024 },
  { name: "desktop", width: 1280, height: 800 },
];

for (const vp of VIEWPORTS) {
  test.describe(`order card @ ${vp.name}`, () => {
    test.use({ viewport: { width: vp.width, height: vp.height } });

    for (const state of ["default", "loading", "error", "long-content"] as const) {
      test(state, async ({ page }) => {
        await page.clock.setFixedTime(new Date("2026-01-15T12:00:00Z")); // freeze time
        await page.goto(`/storybook/order-card?state=${state}`);
        await page.waitForFunction(() => document.fonts.ready);          // fonts settled

        await expect(page.getByTestId("order-card")).toHaveScreenshot(
          `order-card-${state}-${vp.name}.png`,
          { animations: "disabled", maxDiffPixelRatio: 0.01 },
        );
      });
    }
  });
}
```

**Catching overflow that a functional test would pass:**

```typescript
test("long customer name does not overflow the card", async ({ page }) => {
  await page.goto("/orders/ord_1?customer=Bartholomew%20Wintersmith-Kensington");

  const card = page.getByTestId("order-card");
  const overflows = await card.evaluate(
    (el) => el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight,
  );
  expect(overflows).toBe(false);
});
```

## Notes

- `page.clock` (Playwright 1.45+) freezes both `Date` and timers, which is what makes relative timestamps ("2 hours ago") stable in screenshots.
- Storybook plus a visual-testing runner gives you every component state in isolation, which is far cheaper to screenshot than navigating the real application into each state.
- Visual tests are not a substitute for accessibility testing. A screenshot cannot tell you the contrast is 2.1:1.
