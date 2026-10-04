---
name: rule-accessibility
description: MANDATORY when editing files matching ["frontend/src/**/*.tsx", "frontend/src/**/*.ts"]. Accessibility requirements for all frontend code. WCAG 2.1 AA and Section 508 compliance is legally mandated for this federal project.
---

# Accessibility Rules (WCAG 2.1 AA / Section 508)

> **This is a federal government project.** Section 508 compliance and WCAG 2.1 AA conformance are legal requirements, not optional best practices. Accessibility violations are treated as bugs, not suggestions.

## Jest-axe Testing (Required)

EVERY component test suite MUST include a `jest-axe` accessibility scan. MUST use the `toHaveNoViolations()` matcher. NEVER ship a component without an axe scan in its test file.

Example from codebase:
```tsx
// From frontend/tests/components/manageUsers/InviteLegacyUsersButton.test.tsx
import { axe } from "jest-axe";

it("should not have accessibility violations", async () => {
  const { container } = render(
    <InviteLegacyUsersButton organizationId="org-123" />,
  );
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## ARIA Labels and Roles

EVERY interactive element MUST have a proper ARIA label or accessible name. Icon-only buttons MUST have `aria-label` describing the action. NEVER rely on visual appearance alone to convey meaning.

Example from codebase:
```tsx
// Correct: icon-only button with aria-label
<button aria-label="Close modal" onClick={onClose}>
  <Icon name="close" />
</button>

// Correct: form input with associated label
<label htmlFor="search-input">Search grants</label>
<input id="search-input" type="text" />
```

## Keyboard Navigation

ALWAYS maintain logical tab order. ALWAYS ensure all interactive elements are reachable via keyboard. NEVER use `tabIndex` values greater than 0 (disrupts natural tab order). ALWAYS use `tabIndex={0}` for custom interactive elements and `tabIndex={-1}` for programmatically focusable non-interactive elements.

## Focus Management

ALWAYS use `focus-trap-react` for modals, dialogs, and drawers. ALWAYS return focus to the trigger element when a modal/dialog closes. NEVER trap focus in non-modal UI elements.

Example from codebase:
```tsx
// From frontend/src/components/ modal pattern
import FocusTrap from "focus-trap-react";

<FocusTrap active={isOpen}>
  <div role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <h2 id="modal-title">Confirm Action</h2>
    {/* Modal content */}
    <button onClick={onClose}>Close</button>
  </div>
</FocusTrap>
```

## Heading Hierarchy

ALWAYS maintain logical heading hierarchy (h1 > h2 > h3). NEVER skip heading levels. EVERY page MUST have exactly one `<h1>`. NEVER use headings for visual styling — use CSS classes instead.

## Form Accessibility

EVERY form input MUST be associated with a `<label>` element (via `htmlFor`/`id` or wrapping). ALWAYS use `aria-describedby` for help text and error messages. ALWAYS use `aria-invalid="true"` for fields with validation errors. NEVER use placeholder text as a substitute for labels.

Example from codebase:
```tsx
<label htmlFor="email-input">Email address</label>
<input
  id="email-input"
  type="email"
  aria-describedby="email-help email-error"
  aria-invalid={hasError}
/>
<span id="email-help">We will never share your email.</span>
{hasError && <span id="email-error" role="alert">Please enter a valid email.</span>}
```

## Dynamic Content and Live Regions

ALWAYS use `aria-live` regions for dynamic content updates (loading states, error messages, notifications). ALWAYS use `role="alert"` for urgent error messages. ALWAYS use `role="status"` for non-urgent status updates. NEVER update DOM content without notifying assistive technology.

Example from codebase:
```tsx
// Loading state announced to screen readers
<div aria-live="polite" aria-busy={isLoading}>
  {isLoading ? "Loading results..." : `${count} results found`}
</div>

// Error announced immediately
<div role="alert">
  {errorMessage}
</div>
```

## Color and Visual Design

NEVER convey information solely through color. ALWAYS provide text or icons alongside color indicators. ALWAYS ensure sufficient color contrast (4.5:1 for normal text, 3:1 for large text per WCAG AA). ALWAYS use USWDS design tokens for colors — they meet contrast requirements by default.

## Images and Icons

ALWAYS provide meaningful `alt` text for informational images. ALWAYS use `aria-hidden="true"` or `alt=""` for decorative images and icons. NEVER leave `alt` attributes empty on informational images.

## USWDS Component Usage

ALWAYS prefer USWDS components from `@trussworks/react-uswds` for standard UI elements — they include built-in accessibility. NEVER reimplement functionality that USWDS provides with accessible defaults. ALWAYS verify that custom components meet or exceed USWDS accessibility standards.

## Pa11y-CI Integration

Be aware that pa11y-ci runs in CI on every PR with two configurations:
- **Desktop:** Standard viewport with axe runner
- **Mobile:** 390x844 viewport (iPhone 14 equivalent)
Both wait for `#main-content` visibility before scanning. ALWAYS ensure pages render `#main-content` as a landmark.

## Tables

ALWAYS use semantic `<table>`, `<thead>`, `<tbody>`, `<th>`, `<td>` elements for tabular data. ALWAYS use `scope="col"` or `scope="row"` on `<th>` elements. NEVER use tables for layout purposes. ALWAYS provide a `<caption>` or `aria-label` for data tables.

## Skip Navigation

ALWAYS ensure a "Skip to main content" link exists as the first focusable element on the page. This is handled at the layout level — NEVER remove it.

---

## Context Enrichment

When generating frontend code that affects accessibility, enrich your context:
- Call `get_architecture_section("frontend")` from the `simpler-grants-context` MCP server to understand frontend architecture
- Call `get_rule_detail("frontend-components")` for component structure patterns
- Call `get_rule_detail("frontend-tests")` for jest-axe test patterns
- Call `get_rule_detail("frontend-app-pages")` for page-level accessibility patterns
- Consult **Compound Knowledge** for indexed documentation on accessibility patterns

## Related Rules

When working on accessibility, also consult these related rules:
- **`frontend-components.mdc`** — component structure, USWDS usage
- **`frontend-tests.mdc`** — jest-axe testing requirements
- **`frontend-e2e-tests.mdc`** — E2E accessibility testing
- **`frontend-app-pages.mdc`** — page-level metadata and structure
- **`frontend-i18n.mdc`** — translated strings for accessible labels
- **`cross-domain.mdc`** — cross-cutting conventions

## Specialist Validation

When generating or significantly modifying frontend code:

**For simple changes (< 20 lines, adding aria-label, fixing alt text):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new interactive component, new form, new modal):**
Invoke `accessibility-auditor` to validate WCAG 2.1 AA compliance.

**For complex changes (new page, new layout, new navigation pattern):**
Invoke the following specialists (run in parallel where possible):
- `accessibility-auditor` — deep WCAG 2.1 AA / Section 508 compliance review
- `codebase-conventions-reviewer` — validate against project conventions
- `kieran-typescript-reviewer` — TypeScript-specific quality review

<!-- Hook enforcement: accessibility-checker validates onClick handlers, alt text, tabIndex, label associations -->
