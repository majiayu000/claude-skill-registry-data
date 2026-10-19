---
name: playwright-a11y-e2e
description: "End-to-end browser tests with Playwright and axe-core: axe accessibility scans, keyboard-only navigation checks, responsive breakpoint checks, and stable-selector rules. Use when writing or reviewing E2E tests, when an axe assertion fails, when a keyboard path is unreachable, or when a selector breaks after a refactor."
license: MIT-compat
compatibility: "framework-agnostic; Node.js host; Linux; Playwright browsers installed"
metadata: {}
allowed-tools: []
---

Standard: name/description/length rules — [agentskills.io standard](../references/agentskills-standard.md).
# Playwright A11y E2E Skill (body <500 lines; full procedure in references/playwright-a11y-e2e-procedure.md)

## When to use this skill (trigger)
- You need automated E2E coverage of a web app.
- You need accessibility conformance evidence (axe scans, keyboard-only paths).
- You need responsive breakpoint checks.
- You are choosing selectors that survive refactors.

## Disambiguation
- Fires: automated E2E coverage, accessibility conformance evidence, responsive breakpoint checks, choosing refactor-proof selectors.
- Does NOT fire for: a static unit test of a pure function, a design-token audit (use foundation-v2-conformance), or a non-web target.

## When NOT to use this skill
- Unit or API tests (use pytest or contract tests).
- Static HTML/CSS inspection (use axe-core directly).
- Sites that cannot be automated (CAPTCHA, auth wall with no test credentials).
- A single static page with no interactive elements — axe will pass trivially, but the keyboard and responsive loops are still worth running once; the skill fires on the first interactive route.
- "Just eyeball it in the browser" — the skill fires when someone asks for evidence that a human could also produce by looking; the difference is the committed artifact.
- An axe run that is only run on failure — run on every route; a green pass on a route you did not scan is not evidence.

## Decision table — test strategy
| Goal | Primary tool | Evidence |
|------|--------------|----------|
| Accessibility conformance | axe-core via Playwright | axe JSON report |
| Keyboard-only navigation | Playwright keyboard API | video + log |
| Responsive breakpoints | Playwright viewport loop | screenshot set |
| Stable selectors | `getByTestId` first; `getByRole`/`getByLabel` for roles | selector audit |

## Numbered procedure (summary; full recipe in references/playwright-a11y-e2e-procedure.md)
1. Set up the browser context — install Playwright browsers, set a stable viewport, disable animations.
2. Run axe scans — @axe-core/playwright on each route; collect violations.
3. Verify keyboard-only paths — tab through every interactive element; assert focus order.
4. Check responsive breakpoints — loop over configured viewports; assert no overflow.
5. Use stable selectors — prefer role/label/text; never XPath or CSS classes.
6. Record evidence — axe JSON, screenshots, and a selector audit.

## Decision table — selector choice
| Selector | Safe? | When to pick | Pitfall |
|----------|-------|-------------|---------|
| `page.getByTestId('close')` | Always safe | First choice for anything with a test id | Requires the data attribute to exist |
| `page.getByRole('button', { name: 'Close' })` | Always safe | Roles with accessible names | Name must match exactly; locale-sensitive |
| `page.getByLabel('Email')` | Always safe | Form fields with a label association | Breaks if the label is removed |
| `page.getByText('Sign in')` | Use with caution | Visible text only; no markup inside | Matches partial text; flaky on i18n |
| `.btn:nth-child(3)` | NEVER | — | Breaks when the DOM order changes |
| `css=.card > div` | NEVER | — | Class-only; breaks on every refactor |
| `xpath=//button[2]` | NEVER | — | XPath is order-dependent and unreadable |

## Worked examples
Good (stable selector + axe + keyboard):
```ts
import { test, expect } from '@playwright/test';
import axe from '@axe-core/playwright';

test('login form is accessible', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('a@example.com');
  await page.getByRole('button', { name: 'Sign in' }).click();
  const results = await axe.scan(page.locator('main'));
  expect(results.violations).toEqual([]);
});
```
Bad (unstable selector — breaks when the DOM order changes):
```ts
await page.click('.btn:nth-child(3)');  // which button is this, exactly?
```
Bad (axe on a closed modal — the hidden content is never scanned):
```ts
await axe.scan(page);            // modal is aria-hidden; its issues are invisible
// fix: wait for the dialog to be visible first
await page.getByRole('dialog').waitFor({ state: 'visible' });
const results = await axe.scan(page.getByRole('dialog'));
```
Bad (keyboard test that skips shadow DOM — fails silently on Web Components):
```ts
await page.keyboard.press('Tab');  // stops at the light DOM; shadow controls unreachable
```

## Pitfalls from research
- axe on dynamic modals misses content rendered after aria-hidden flips; wait for aria-hidden=false.
- CSS :focus-visible is not a WCAG criterion; do not assert on it.
- nth-child selectors break on every refactor; prefer `getByTestId`, then `getByRole`/`getByLabel`.
- Keyboard-only tests that skip shadow DOM fail silently on Web Components.
- Viewport loop must include 320px, 768px, 1024px, 1440px minimum (common trap: only testing desktop).
- axe run without frame handling misses content in iframes (common trap).

## Near-miss triggers (act before the incident)
- axe run on a dynamic modal without waiting for `aria-hidden=false` → false violations or missed violations.
- `:focus-visible` asserted as a WCAG criterion → it is not one; assert focus order instead.
- `nth-child` or class-only selectors → break on every refactor; use `getByTestId` (or `getByRole`/`getByLabel` for roles).
- Keyboard tests that skip shadow DOM → fail silently on Web Components.
- Viewport loop missing 320px → mobile bugs never caught.
- axe run without frame handling → content in iframes is never scanned.
- "The axe scan is green, so the page is accessible" → green axe means zero *reported* violations, not that every control is reachable; run the keyboard check too.

## Verification checklist (all must pass before you finish)
- [ ] axe scan runs on every route with zero violations of level A/AA [WCAG].
- [ ] Keyboard-only path covers every interactive element [WCAG].
- [ ] Responsive breakpoints pass at configured widths [responsive].
- [ ] Selectors are role/label-based, not XPath or CSS-class [stable selectors].
- [ ] Evidence files (axe JSON, screenshots) are committed or referenced [evidence].

## References
- Full procedure, axe version table and worked examples: `references/playwright-a11y-e2e-procedure.md`.
- Eval prompts with expected behaviour and failure signs: `references/EVALS.md`.
- Primary sources with URLs and retrieval dates: `references/SOURCES.md`.

## Related skills
- [acceptance-harness](../acceptance-harness/SKILL.md) — axe JSON and screenshots are the evidence pointers.
- [honest-status](../honest-status/SKILL.md) — a green axe scan is not DONE.
- [long-test-discipline](../long-test-discipline/SKILL.md) — the axe scan and the keyboard traversal are long tests; run them in the foreground with a recorded seed.
- [module-contract-first](../module-contract-first/SKILL.md) — the axe/keyboard contract is a module contract: enumerate the selectors and roles, version the snapshot, block merge on drift.
- [shared-tree-git](../shared-tree-git/SKILL.md) — the evidence artifacts and the test script are committed with a task-id prefix.
