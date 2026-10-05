---
name: responsive-ui-testing
description: Audit Laravel responsive UI with Playwright across mobile, tablet, desktop, Livewire states, overflow, clipping, forms, tables, modals, and navigation.
tags:
  - laravel
  - php
  - responsive-design
  - playwright
  - visual-testing
  - frontend
---

# Responsive UI Testing

Use this skill when asked to test whether a Laravel application interface is responsive, mobile-friendly, or visually stable across screen sizes.

Do not conclude that a page is responsive merely because it loads on one mobile viewport or has no JavaScript errors.

When the request is to design, redesign, or implement the frontend before auditing it, use `ui-agent-browser` first. This skill is the final responsive and visual-stability gate after the UI and backend contract are already wired.

Use `e2e-playwright` when responsive findings should become durable Playwright regression tests.

## Primary Goals

Verify that the application remains usable and visually correct across:

- small mobile
- standard mobile
- large mobile
- tablet portrait
- laptop
- desktop
- wide desktop when the project has wide layouts or dashboards

## Required Viewports

Test at least these viewports:

| Target | Width | Height |
|---|---:|---:|
| Small mobile | 320 | 568 |
| Standard mobile | 375 | 812 |
| Large mobile | 430 | 932 |
| Tablet portrait | 768 | 1024 |
| Laptop | 1366 | 768 |
| Desktop | 1920 | 1080 |

Also test Playwright mobile device profiles when available, such as an iPhone and a Pixel device.

## Required Checks

For every tested page and viewport:

1. Navigate to the page and wait until network, fonts, images, and Livewire activity settle.
2. Check for horizontal document overflow.
3. Check whether visible elements extend outside the viewport.
4. Detect clipped, overlapping, or unreadable text.
5. Verify the navbar does not stack into unusable controls.
6. Verify the sidebar can open and close on small screens.
7. Verify forms can be completed without horizontal scrolling.
8. Verify buttons and links remain visible, clickable, and large enough for touch.
9. Verify tables have deliberate mobile behavior such as horizontal scroll, stacked cards, hidden secondary columns, or a redesigned mobile layout.
10. Verify modals, dropdowns, date pickers, and select menus fit inside the viewport.
11. Verify fixed and sticky elements do not cover important content.
12. Verify images keep their intended aspect ratio and do not stretch or crop important content accidentally.
13. Interact with Livewire components and repeat layout checks after state changes, validation errors, pagination, filtering, sorting, loading states, and empty states.
14. Test dark mode when the project supports it.
15. Capture screenshots for review.
16. Report failures with page, viewport, browser or device, selector, and evidence.

## Horizontal Overflow Check

Use a browser-side assertion like this:

```ts
const overflow = await page.evaluate(() => ({
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  hasOverflow:
    document.documentElement.scrollWidth >
    document.documentElement.clientWidth + 1,
}));

expect(
  overflow.hasOverflow,
  `Horizontal overflow: ${overflow.scrollWidth}px > ${overflow.clientWidth}px`,
).toBeFalsy();
```

## Element Boundary Check

Inspect visible elements and report those extending outside the viewport:

```ts
const offenders = await page.evaluate(() => {
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  return Array.from(document.querySelectorAll("body *"))
    .filter((element) => {
      const htmlElement = element as HTMLElement;
      const style = window.getComputedStyle(htmlElement);
      const rect = htmlElement.getBoundingClientRect();

      if (
        style.display === "none" ||
        style.visibility === "hidden" ||
        rect.width === 0 ||
        rect.height === 0
      ) {
        return false;
      }

      return (
        rect.left < -1 ||
        rect.right > viewportWidth + 1 ||
        rect.top < -1 ||
        rect.bottom > viewportHeight + 1
      );
    })
    .slice(0, 50)
    .map((element) => ({
      tag: element.tagName.toLowerCase(),
      id: element.id,
      className: String((element as HTMLElement).className),
      text: element.textContent?.trim().slice(0, 80),
      rect: element.getBoundingClientRect().toJSON(),
    }));
});

expect(offenders).toEqual([]);
```

Treat fixed-position overlays and intentionally scrollable containers carefully. Do not automatically mark deliberate off-canvas navigation as a failure.

## Playwright Test Skeleton

Create or update a project-local browser test such as `tests/e2e/responsive.spec.ts` when the project uses Playwright:

```ts
import { expect, test } from "@playwright/test";

const viewports = [
  { name: "mobile-320", width: 320, height: 568 },
  { name: "mobile-375", width: 375, height: 812 },
  { name: "mobile-430", width: 430, height: 932 },
  { name: "tablet-768", width: 768, height: 1024 },
  { name: "laptop-1366", width: 1366, height: 768 },
  { name: "desktop-1920", width: 1920, height: 1080 },
];

const routes = ["/dashboard", "/settings"];

for (const viewport of viewports) {
  test.describe(viewport.name, () => {
    test.use({ viewport });

    for (const route of routes) {
      test(`${route} is responsive`, async ({ page }, testInfo) => {
        await page.goto(route);
        await page.waitForLoadState("networkidle");
        await page.evaluate(() => document.fonts?.ready);

        const overflow = await page.evaluate(() => ({
          documentWidth: document.documentElement.scrollWidth,
          viewportWidth: document.documentElement.clientWidth,
        }));

        expect(
          overflow.documentWidth,
          `Horizontal overflow on ${route}`,
        ).toBeLessThanOrEqual(overflow.viewportWidth + 1);

        await expect(page).toHaveScreenshot(
          `${route.replaceAll("/", "-") || "home"}-${testInfo.project.name}.png`,
          { fullPage: true, animations: "disabled" },
        );
      });
    }
  });
}
```

Adapt routes to the real Laravel app. Seed deterministic data and authenticate through existing project helpers before asserting protected pages.

## Visual Regression Rules

Use screenshots for stable pages after:

- disabling animations
- freezing or mocking dynamic timestamps
- using deterministic seed data
- hiding unstable third-party widgets
- waiting for fonts and images
- avoiding screenshot comparison across inconsistent operating systems

## Laravel-Specific Checks

Inspect:

- Blade layouts and components
- Livewire components after state changes
- validation error messages
- authorization-dependent navigation
- paginated tables
- flash messages
- file-upload components
- loading indicators
- empty states
- long translated strings
- Tailwind or FlyonUI breakpoint classes
- dark mode variants when configured

## Reporting Format

Group findings by severity:

- Critical: the page cannot be used at a tested viewport.
- Major: important content or controls are clipped, inaccessible, overlapping, or impossible to operate.
- Minor: visual spacing or alignment is degraded but functionality remains usable.

For every issue include:

- route or page
- viewport
- browser or device
- affected component
- expected behavior
- actual behavior
- screenshot path
- probable source file
- recommended fix

## Completion Gate

Do not declare the application responsive unless:

- all required viewports were tested
- no unexplained horizontal document overflow exists
- navigation, sidebars, and core forms remain usable
- tables and modals have deliberate mobile behavior
- interactive Livewire states were tested
- dark mode was tested when supported
- failures and untested pages are explicitly reported
