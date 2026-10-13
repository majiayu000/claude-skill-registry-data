---
name: accessibility-testing
description: Test web and mobile applications for WCAG 2.1/2.2 AA conformance using automated tools (axe, Lighthouse, Pa11y) and manual techniques (keyboard navigation, screen reader testing). Covers the POUR principles, common a11y failures, CI integration, a11y bug severity rubric, legal risk (ADA, EN 301 549), and writing accessible acceptance criteria.
triggers:
  - "accessibility testing"
  - "a11y"
  - "WCAG"
  - "screen reader"
  - "keyboard navigation"
  - "accessible"
  - "color contrast"
  - "aria"
  - "inclusive design"
  - "axe"
  - "VoiceOver"
  - "NVDA"
  - "JAWS"
  - "ADA compliance"
  - "focus indicator"
  - "alt text"
audience: qa, engineer
---

# Accessibility Testing

## Context

Accessibility (a11y) testing verifies that software can be used by people with disabilities — including those using screen readers, keyboard-only navigation, switch access, magnification, or high contrast modes. It is both a legal obligation (ADA, Section 508, EN 301 549) and an engineering quality standard.

WCAG 2.1 Level AA is the most widely adopted conformance target for commercial software. It is the standard referenced in most legal settlements, government procurement requirements, and enterprise vendor agreements.

Use this skill when:
- A new feature or component is being designed or built and a11y acceptance criteria are needed
- QA is performing a release-gate accessibility check
- An accessibility audit has flagged issues that need to be prioritized and fixed
- A legal or compliance review requires WCAG conformance documentation
- Automated accessibility checks need to be added to CI

---

## Core Concepts

### WCAG 2.1 Conformance Levels

| Level | Description | Use Case |
|---|---|---|
| **A** | Minimum. Failure is a severe barrier. | Never ship below this. |
| **AA** | Standard. Required by most regulations and contracts. | The target for all commercial software. |
| **AAA** | Enhanced. Not always achievable for all content. | Aspire to where feasible; not required everywhere. |

WCAG 2.2 (published October 2023) adds 9 new criteria to AA, primarily around cognitive and motor accessibility. Adoption is increasing; start planning for it now.

### The POUR Principles

Every WCAG success criterion maps to one of four principles:

| Principle | Meaning | Examples |
|---|---|---|
| **Perceivable** | Information must be presentable in ways users can perceive | Alt text, captions, sufficient color contrast, no information conveyed by color alone |
| **Operable** | UI must be operable by everyone | Keyboard access, no seizure-triggering content, focus management, sufficient time limits |
| **Understandable** | Content and operation must be understandable | Clear labels, error messages, consistent navigation, language identified |
| **Robust** | Content must be interpreted by assistive technologies | Valid HTML, ARIA used correctly, no broken roles/states |

---

## Automated vs. Manual Testing

**Automated tools catch ~30–40% of WCAG issues.** They are fast, scalable, and essential for CI — but they cannot test:
- Logical reading order (visual ≠ DOM order isn't always detectable)
- Usefulness of alt text (present ≠ meaningful)
- Focus management after dynamic interactions
- Screen reader announcement quality
- Cognitive clarity of error messages

**Manual testing is required for production-ready a11y.** Automated tools are a floor, not a ceiling.

| Test Type | What It Catches | Tools |
|---|---|---|
| Automated static | Missing labels, contrast failures, invalid ARIA, missing alt text | axe, Lighthouse, WAVE, Pa11y |
| Keyboard-only | Focus order, focus visibility, keyboard traps, missing skip links | Browser only |
| Screen reader | Announcements, landmark navigation, dynamic content updates | NVDA + Chrome, VoiceOver + Safari, JAWS + Chrome |
| Color / visual | Contrast ratios, color-only information, zoom reflow | Colour Contrast Analyser, browser zoom |
| Cognitive | Plain language, consistent UI, error recovery | Human review |

---

## WCAG 2.1 AA Checklist

The most common AA compliance target. Mark each as Pass / Fail / N/A.

### 1. Perceivable

```
TEXT ALTERNATIVES
[ ] 1.1.1  All non-text content has a text alternative (alt text for images,
           labels for form inputs, titles for iframes)                     P/F/N/A

TIME-BASED MEDIA
[ ] 1.2.1  Audio-only / video-only content has a transcript or alternative P/F/N/A
[ ] 1.2.2  Captions provided for all prerecorded video                    P/F/N/A
[ ] 1.2.3  Audio description or media alternative for prerecorded video   P/F/N/A
[ ] 1.2.4  Captions for all live video                                    P/F/N/A
[ ] 1.2.5  Audio description for all prerecorded video                    P/F/N/A

ADAPTABLE
[ ] 1.3.1  Structure and relationships conveyed via markup (headings,
           lists, tables, form labels)                                     P/F/N/A
[ ] 1.3.2  Reading order makes sense when styles are removed              P/F/N/A
[ ] 1.3.3  Instructions do not rely solely on sensory characteristics
           (shape, color, size, position)                                  P/F/N/A
[ ] 1.3.4  Orientation: content not restricted to single orientation      P/F/N/A
[ ] 1.3.5  Input fields identify their purpose (autocomplete attributes)  P/F/N/A

DISTINGUISHABLE
[ ] 1.4.1  Color is not the only means of conveying information           P/F/N/A
[ ] 1.4.2  Audio playing > 3 sec can be paused/stopped or volume adjusted P/F/N/A
[ ] 1.4.3  Text contrast ratio ≥ 4.5:1 (normal text), ≥ 3:1 (large text) P/F/N/A
[ ] 1.4.4  Text can be resized to 200% without loss of content/function   P/F/N/A
[ ] 1.4.5  Text used instead of images of text (except logos)            P/F/N/A
[ ] 1.4.10 Reflow: content reflows in 320px wide without horizontal scroll P/F/N/A
[ ] 1.4.11 Non-text contrast ≥ 3:1 for UI components and graphics        P/F/N/A
[ ] 1.4.12 Text spacing: no loss of content when line/letter/word spacing
           is increased to specified values                                P/F/N/A
[ ] 1.4.13 Content on hover/focus is dismissible, hoverable, persistent   P/F/N/A
```

### 2. Operable

```
KEYBOARD ACCESSIBLE
[ ] 2.1.1  All functionality available via keyboard                       P/F/N/A
[ ] 2.1.2  No keyboard trap (user can always navigate away)               P/F/N/A
[ ] 2.1.4  Single-character key shortcuts can be remapped or disabled     P/F/N/A

ENOUGH TIME
[ ] 2.2.1  Time limits can be adjusted, extended, or turned off           P/F/N/A
[ ] 2.2.2  Moving/blinking/scrolling content can be paused/stopped        P/F/N/A

SEIZURES
[ ] 2.3.1  No content flashes more than 3 times per second                P/F/N/A

NAVIGABLE
[ ] 2.4.1  Skip navigation link available (bypass blocks)                 P/F/N/A
[ ] 2.4.2  Pages have descriptive titles                                  P/F/N/A
[ ] 2.4.3  Focus order is logical and preserves meaning                   P/F/N/A
[ ] 2.4.4  Link purpose is clear from link text or context                P/F/N/A
[ ] 2.4.5  Multiple ways to find pages (search, sitemap, nav)             P/F/N/A
[ ] 2.4.6  Headings and labels are descriptive                            P/F/N/A
[ ] 2.4.7  Keyboard focus is visible (focus indicator present)            P/F/N/A

INPUT MODALITIES (WCAG 2.1)
[ ] 2.5.1  Pointer gestures have single-pointer alternatives              P/F/N/A
[ ] 2.5.2  Pointer actions can be aborted or undone                       P/F/N/A
[ ] 2.5.3  Labels visible in UI match accessible name                     P/F/N/A
[ ] 2.5.4  Functionality not restricted to device motion                  P/F/N/A
```

### 3. Understandable

```
READABLE
[ ] 3.1.1  Page language is set (<html lang="en">)                        P/F/N/A
[ ] 3.1.2  Language of parts identified for sections in other languages   P/F/N/A

PREDICTABLE
[ ] 3.2.1  No context change on focus (no auto-submit on tab)             P/F/N/A
[ ] 3.2.2  No context change on input without warning                     P/F/N/A
[ ] 3.2.3  Navigation is consistent across pages                          P/F/N/A
[ ] 3.2.4  Components that function the same are identified consistently  P/F/N/A

INPUT ASSISTANCE
[ ] 3.3.1  Errors are identified and described in text                    P/F/N/A
[ ] 3.3.2  Labels or instructions provided for all inputs                 P/F/N/A
[ ] 3.3.3  Error suggestions provided when input error detected           P/F/N/A
[ ] 3.3.4  Important submissions are reversible, checkable, or confirmed  P/F/N/A
```

### 4. Robust

```
COMPATIBLE
[ ] 4.1.1  No HTML parsing errors that affect AT (duplicate IDs,
           unclosed tags, invalid nesting)                                 P/F/N/A
[ ] 4.1.2  All UI components have name, role, and state/value accessible  P/F/N/A
[ ] 4.1.3  Status messages conveyed via role or live regions
           without requiring focus                                         P/F/N/A
```

---

## Manual Testing Script

### Keyboard-Only Navigation (no mouse)

| Check | Pass? | Notes |
|-------|-------|-------|
| All interactive elements reachable via Tab | | |
| Focus indicator always visible | | |
| Focus order is logical (top→bottom, left→right) | | |
| No keyboard trap | | |
| Dropdowns/modals: focus enters on open, Esc closes, focus returns | | |
| Skip-nav link appears on first Tab press | | |
| Custom widgets follow ARIA keyboard patterns | | |
| Forms submittable with Enter; errors associated with inputs | | |

### Screen Reader Test

Test with: **NVDA + Chrome** (Windows) · **VoiceOver + Safari** (macOS/iOS) · **TalkBack + Chrome** (Android)

| Check | Pass? | Notes |
|-------|-------|-------|
| Page has `<main>` landmark and logical heading hierarchy | | |
| Decorative images hidden (`alt=""` / `aria-hidden`); informative images have alt text | | |
| All form inputs announced with their label; required/error states announced | | |
| Buttons/links have meaningful accessible names (not "click here") | | |
| Modals: SR announces heading on open, focus trapped, background inert | | |
| Alerts/toasts announced via `role="alert"` or `aria-live` | | |
| Dynamic content updates announced without requiring focus | | |

---

## Automated CI Integration

### axe-core with Jest (React / unit test level)

```javascript
// Install: npm install --save-dev jest-axe
// jest.setup.js
import { configureAxe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

// Usage in component tests:
import { render } from '@testing-library/react';
import { axe } from 'jest-axe';
import { LoginForm } from './LoginForm';

test('LoginForm has no accessibility violations', async () => {
  const { container } = render(<LoginForm />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### axe-core with Playwright (integration / E2E level)

```javascript
// Install: npm install --save-dev @axe-core/playwright
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('homepage has no critical a11y violations', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])  // Target AA
      .exclude('#third-party-widget')               // Exclude unowned content
      .analyze();

    // Attach full report as a test artifact
    await test.info().attach('axe-results', {
      body: JSON.stringify(results.violations, null, 2),
      contentType: 'application/json',
    });

    expect(results.violations).toEqual([]);
  });

  test('checkout flow has no critical a11y violations', async ({ page }) => {
    await page.goto('/checkout');
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2aa'])
      .analyze();
    expect(results.violations.filter(v => v.impact === 'critical')).toEqual([]);
  });
});
```

### Pa11y in CI (GitHub Actions)

```yaml
# .github/workflows/a11y.yml
name: Accessibility Check

on:
  pull_request:
    paths:
      - 'src/**'
      - 'public/**'

jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install deps
        run: npm ci

      - name: Start app
        run: npm run build && npm run start:ci &
        env:
          PORT: 3000

      - name: Wait for server
        run: npx wait-on http://localhost:3000

      - name: Run Pa11y
        run: |
          npx pa11y-ci \
            --standard WCAG2AA \
            --reporter cli \
            --threshold 0 \
            http://localhost:3000 \
            http://localhost:3000/login \
            http://localhost:3000/checkout

      - name: Upload results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: a11y-results
          path: pa11y-results.json
```

---

## Accessibility Bug Severity Rubric

Use this when filing and prioritizing a11y bugs. Align with your existing severity taxonomy.

```
SEVERITY 1 — CRITICAL (P0/P1, block release)
─────────────────────────────────────────────
Definition: Completely prevents a user with a disability from completing
a core user journey. No workaround exists.

Examples:
  - Modal dialog traps keyboard focus with no way to close via keyboard
  - Form cannot be submitted using a screen reader
  - Payment or checkout flow is inaccessible to keyboard users
  - Login page has no accessible name on the password field
  - Critical error is communicated only via color (no text, no icon)

SEVERITY 2 — HIGH (P2, fix in current or next sprint)
──────────────────────────────────────────────────────
Definition: Significantly impairs ability to use a core feature.
Workaround may exist but requires effort.

Examples:
  - Focus is lost after closing a modal (moves to top of page)
  - Image carousel has no keyboard controls
  - Form error messages are not associated with the input field
  - Heading hierarchy skips levels (h1 → h4), confusing SR navigation
  - Interactive elements have contrast ratio below 3:1

SEVERITY 3 — MEDIUM (P3, schedule within 2 sprints)
────────────────────────────────────────────────────
Definition: Reduces usability or convenience for users with disabilities.
Workaround exists.

Examples:
  - Decorative image has non-empty alt text, adding noise to SR
  - Link opens new tab without warning
  - Non-critical status message not announced via live region
  - Focus indicator is visible but low-contrast (passes minimum but poor UX)
  - Placeholder text used as visible label (disappears on focus)

SEVERITY 4 — LOW (P4, add to backlog)
──────────────────────────────────────
Definition: Minor deviation from best practice. Minimal user impact.

Examples:
  - aria-label on element that already has visible text (redundant but harmless)
  - Missing lang attribute on a secondary page section
  - Icon button has accessible name but not matching visible tooltip
  - Autocomplete attribute missing on non-critical input
```

---

## Accessibility Acceptance Criteria Template

Add these to user stories and tickets when building new components or features.

```
ACCESSIBILITY ACCEPTANCE CRITERIA
===================================
Feature/Component: _______________

KEYBOARD
--------
Given I am navigating with keyboard only,
  [ ] I can reach [element] using Tab
  [ ] I can activate [element] using Enter or Space
  [ ] Focus is visible at all times (not hidden or clipped)
  [ ] After [action], focus moves to [expected target]
  [ ] No keyboard trap is introduced

SCREEN READER
-------------
Given I am using a screen reader (NVDA, VoiceOver, JAWS),
  [ ] [Element] is announced as [expected role and name]
  [ ] [Form field] announces its label and required/optional state
  [ ] [Error message] is announced when the error state occurs
  [ ] [Dynamic update / toast / alert] is announced without requiring focus
  [ ] [Image] is announced as [descriptive alt text] or is hidden if decorative

VISUAL
------
  [ ] Text contrast ratio ≥ 4.5:1 (< 18px) or ≥ 3:1 (≥ 18px / bold)
  [ ] UI component (button border, focus ring) contrast ≥ 3:1 against background
  [ ] Information is not conveyed by color alone
  [ ] Component is usable at 200% browser zoom without horizontal scroll
  [ ] Focus indicator meets 2px minimum and ≥ 3:1 contrast (WCAG 2.2 target)

ARIA (if custom widget)
-----------------------
  [ ] Role is semantically appropriate for the widget type
  [ ] aria-expanded, aria-selected, aria-checked, etc. reflect actual state
  [ ] aria-label or aria-labelledby provides meaningful accessible name
  [ ] aria-describedby links to help text or error message where applicable

AUTOMATED TEST
--------------
  [ ] axe-core / jest-axe passes with no violations in component test
  [ ] Playwright a11y scan passes with no critical violations in integration test

DEFINITION OF DONE
------------------
  [ ] WCAG 2.1 AA checklist items for this component are all Pass
  [ ] Manual keyboard test passed
  [ ] Screen reader test passed on [NVDA + Chrome] and/or [VoiceOver + Safari]
  [ ] No new a11y violations introduced (verified via CI axe scan)
```

---

## Common Accessibility Failures Quick Reference

| Failure | WCAG Criterion | How to Fix |
|---|---|---|
| Missing alt text on image | 1.1.1 | `<img alt="descriptive text">` or `alt=""` for decorative |
| No label on form input | 1.3.1, 4.1.2 | `<label for="id">` or `aria-label` or `aria-labelledby` |
| Insufficient color contrast | 1.4.3 | Minimum 4.5:1 for body text; use Colour Contrast Analyser |
| No visible focus indicator | 2.4.7 | `outline: 2px solid; outline-offset: 2px;` — never `outline: none` |
| Keyboard trap in modal | 2.1.2 | Trap focus with focus sentinel divs; release on Escape |
| Focus not moved after dialog opens | 2.4.3 | `dialogElement.focus()` after showing; return focus on close |
| Click handler on non-interactive element | 4.1.2 | Use `<button>` or `<a>`, not `<div onClick>` |
| Dynamic content not announced | 4.1.3 | `role="alert"` or `aria-live="polite"` on the container |
| Icon button with no name | 4.1.2 | `aria-label="Close"` on `<button>` containing only an icon |
| Poor heading hierarchy | 1.3.1 | h1 → h2 → h3 in order; no skipping levels |
| Color-only error indication | 1.4.1 | Add icon + text label alongside color change |
| Inaccessible custom dropdown | 4.1.2 | Use native `<select>` or implement ARIA combobox pattern |

---

## Legal Risk Context

Accessibility is a legal obligation in many jurisdictions:

| Regulation | Jurisdiction | Standard Referenced | Who It Applies To |
|---|---|---|---|
| **Americans with Disabilities Act (ADA)** | United States | WCAG 2.1 AA (courts and DOJ) | Places of public accommodation — includes most commercial websites |
| **Section 508** | United States (federal) | WCAG 2.1 AA | Federal agencies and their contractors |
| **EN 301 549** | European Union | WCAG 2.1 AA + additional criteria | Public sector; increasingly applied to private sector |
| **Accessibility for Ontarians with Disabilities Act (AODA)** | Ontario, Canada | WCAG 2.0 Level AA | Organizations with 50+ employees |
| **European Accessibility Act (EAA)** | European Union | EN 301 549 | Private sector products and services (enforcement from 2025) |

> **Key legal exposure**: In the United States, demand letters and lawsuits under ADA Title III for web accessibility have increased steadily. Most claims are settled; typical settlement includes remediation commitment, monitoring, and legal fees ($25K–$250K+). The most common target: e-commerce checkout flows and contact forms.

**Risk mitigation checklist:**
```
[ ] WCAG 2.1 AA conformance tested and documented
[ ] Accessibility policy published on website
[ ] Feedback mechanism for accessibility issues available
[ ] VPATs (Voluntary Product Accessibility Templates) completed for
    enterprise/government sales contexts
[ ] Remediation roadmap documented for known failures
[ ] a11y testing in CI prevents regression on new code
```

---

## Output Format

When applying this skill, the agent should:

1. **Lead with the POUR principle** most relevant to the failure or feature being discussed.
2. **Provide WCAG criterion references** (e.g., 1.4.3, 2.4.7) for every failure identified.
3. **Assign a severity** using the rubric (Critical / High / Medium / Low) for each issue.
4. **Generate acceptance criteria** for new components using the template above.
5. **Provide code snippets** for automated CI integration when asked.
6. **Distinguish automated from manual testing** — never suggest automated scanning alone is sufficient for release.
7. **Call out legal risk** when core user journeys (login, checkout, signup, contact forms) have critical failures.
8. Format checklists as Markdown task lists `- [ ]`. Format code examples as fenced code blocks with language tags.

---

## References

- W3C — [WCAG 2.1](https://www.w3.org/TR/WCAG21/) and [WCAG 2.2](https://www.w3.org/TR/WCAG22/) (w3.org)
- W3C — [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) — keyboard patterns for custom widgets
- Deque — [axe-core](https://github.com/dequelabs/axe-core) and [axe DevTools](https://www.deque.com/axe/)
- WebAIM — [Contrast Checker](https://webaim.org/resources/contrastchecker/), [Screen Reader Survey](https://webaim.org/projects/screenreadersurvey/)
- The A11y Project — [a11yproject.com](https://www.a11yproject.com) — patterns, checklist, resources
- Pa11y — [pa11y.org](https://pa11y.org) — CLI and CI accessibility testing
- Google Lighthouse — built-in browser DevTools + CI via `lighthouse-ci`
- NVDA — [nvaccess.org](https://www.nvaccess.org) (free Windows screen reader)
- LeadDev — ["Building for inclusive engineering"](https://leaddev.com/accessibility)
- Adrian Roselli — [adrianroselli.com](https://adrianroselli.com) — deep-dive a11y implementation articles
