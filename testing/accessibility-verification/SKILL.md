---
name: accessibility-verification
description: Use when implementing any UI - verifies accessibility compliance through automated testing (axe-core), keyboard navigation, screen reader verification, and Lighthouse audits; legally required and ensures inclusive user experience
---

# Frontend Accessibility Verification

## Overview

Accessibility testing ensures UI is usable by everyone, including users with disabilities. It's both a **legal requirement** (WCAG compliance) and fundamental to good UX.

**When to use this skill:**
- Implementing any UI component
- Modifying existing UI
- Before marking UI work complete
- During code review (verify accessibility tested)

## The Iron Law

```
NO UI SHIP WITHOUT ACCESSIBILITY VERIFICATION
```

If you created or modified UI:
- You MUST run automated accessibility tests (axe-core)
- You MUST test keyboard navigation
- You MUST verify screen reader announcements
- You CANNOT claim "UI complete" without accessibility evidence

## Why Accessibility Matters

**Legal requirement:**
- WCAG 2.1 Level AA compliance mandatory in many industries
- ADA lawsuits for inaccessible websites
- Section 508 compliance for government contracts

**Better UX for everyone:**
- Accessible sites work better for all users
- Many a11y issues are actual bugs (missing labels, broken keyboard nav)
- If button has no accessible name, it's both unusable AND untestable

**Automated testing catches ~57% of issues:**
- axe-core finds definite violations (zero false positives)
- Manual testing required for remaining ~43%
- Both automated AND manual testing necessary

## Step-by-Step Process

### Step 1: Automated Testing (axe-core)

**Run axe-core on all UI components:**

#### Playwright Integration

```typescript
import { injectAxe, checkA11y } from 'axe-playwright';

test('component is accessible', async ({ page }) => {
  await page.goto('/checkout');

  // Inject axe-core into page
  await injectAxe(page);

  // Run accessibility audit
  await checkA11y(page, null, {
    detailedReport: true,
    detailedReportOptions: {
      html: true,
    },
  });
});
```

#### Cypress Integration

```typescript
import 'cypress-axe';

describe('Accessibility', () => {
  it('has no a11y violations', () => {
    cy.visit('/checkout');
    cy.injectAxe();
    cy.checkA11y();
  });
});
```

#### Jest Integration

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('has no accessibility violations', async () => {
  const { container } = render(<CheckoutForm />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

**Expected result: 0 violations**

```
✅ PASS: 0 accessibility violations found
❌ FAIL: Found violations - must fix before proceeding
```

### Step 2: Keyboard Navigation Testing (MANDATORY)

**Test ALL interactive elements are keyboard accessible:**

#### Checklist for Keyboard Testing

- [ ] **Tab Navigation**:
  - Press Tab repeatedly
  - Verify focus moves through all interactive elements in logical order
  - Verify focus is visible (clear outline/ring)
  - No keyboard traps (can Tab away from all elements)

- [ ] **Enter/Space Activation**:
  - Tab to buttons
  - Press Enter or Space
  - Verify buttons activate

- [ ] **Escape Key**:
  - Open modals/dialogs
  - Press Escape
  - Verify modal closes

- [ ] **Arrow Keys** (for dropdowns/menus):
  - Open dropdown
  - Use arrow keys to navigate options
  - Press Enter to select

#### Automated Keyboard Testing

```typescript
test('can navigate form with keyboard', async ({ page }) => {
  await page.goto('/checkout');

  // Tab to first input
  await page.keyboard.press('Tab');
  await expect(page.locator('[name="email"]')).toBeFocused();

  // Tab to second input
  await page.keyboard.press('Tab');
  await expect(page.locator('[name="password"]')).toBeFocused();

  // Tab to submit button
  await page.keyboard.press('Tab');
  await expect(page.locator('button[type="submit"]')).toBeFocused();

  // Activate with Enter
  await page.keyboard.press('Enter');

  // Verify form submitted
  await expect(page.locator('[data-testid="success"]')).toBeVisible();
});
```

### Step 3: Screen Reader Verification

**Verify all UI elements have proper ARIA labels:**

#### Automated ARIA Checks

```typescript
test('all interactive elements have accessible names', async ({ page }) => {
  await page.goto('/checkout');

  // Get all interactive elements
  const buttons = page.locator('button, [role="button"]');
  const links = page.locator('a');
  const inputs = page.locator('input, textarea, select');

  // Verify each has accessible name
  for (const button of await buttons.all()) {
    const name = await button.getAttribute('aria-label')
                || await button.textContent();
    expect(name).toBeTruthy();
  }

  for (const input of await inputs.all()) {
    const label = await input.getAttribute('aria-label')
                || await page.locator(`label[for="${await input.getAttribute('id')}"]`).textContent();
    expect(label).toBeTruthy();
  }
});
```

#### Manual Screen Reader Testing (Optional but Recommended)

**Mac (VoiceOver):**
```
1. Press Cmd+F5 to enable VoiceOver
2. Press Control+Option+Right Arrow to navigate
3. Verify all elements announced correctly
4. Press Cmd+F5 to disable VoiceOver
```

**Windows (NVDA):**
```
1. Launch NVDA
2. Press Down Arrow to navigate
3. Verify all elements announced correctly
```

**What to verify:**
- Buttons announce as "button" + label
- Links announce as "link" + text
- Form inputs announce label + current value + field type
- Images have alt text (or are marked decorative)

### Step 4: Lighthouse Accessibility Audit

**Run Lighthouse audit (target: 95%+ score):**

#### Command Line

```bash
# Install lighthouse
npm install -g lighthouse

# Run audit
lighthouse http://localhost:3000/checkout --only-categories=accessibility --view
```

#### Chrome DevTools

```
1. Open DevTools (F12)
2. Click "Lighthouse" tab
3. Select "Accessibility" category
4. Click "Analyze page load"
5. Review score and issues
```

**Target score: 95 or higher**

```
✅ PASS: Score 95-100
⚠️ WARNING: Score 90-94 (fix issues if possible)
❌ FAIL: Score <90 (must fix before proceeding)
```

### Step 5: WCAG Compliance Checklist

**Verify compliance with WCAG 2.1 Level AA:**

#### Perceivable
- [ ] All images have alt text (or are decorative)
- [ ] Color is not the only way to convey information
- [ ] Text has sufficient contrast ratio (4.5:1 for normal text)
- [ ] Content works without CSS

#### Operable
- [ ] All functionality available via keyboard
- [ ] No keyboard traps
- [ ] Focus is visible
- [ ] Link/button purpose clear from text

#### Understandable
- [ ] Page language declared (`<html lang="en">`)
- [ ] Labels for all form inputs
- [ ] Error messages are clear and helpful
- [ ] Consistent navigation across pages

#### Robust
- [ ] Valid HTML (no duplicate IDs)
- [ ] ARIA attributes used correctly
- [ ] Name, Role, Value exposed for custom controls

## Framework-Agnostic Patterns

### Pattern 1: Per-Component Accessibility Tests

```typescript
// Works with Playwright, Selenium, Puppeteer
test('component is accessible', async ({ page }) => {
  // Navigate to component
  await mount('<custom-dropdown></custom-dropdown>');

  // Inject axe-core
  await injectAxe(page);

  // Check baseline state
  await checkA11y(page);

  // Check interactive state
  await page.click('[role="button"]');
  await checkA11y(page);
});
```

### Pattern 2: E2E Flow Accessibility

```typescript
test('checkout flow is accessible', async ({ page }) => {
  await injectAxe(page);

  // Check each step
  await page.goto('/checkout');
  await checkA11y(page);

  await page.fill('[name="email"]', 'test@example.com');
  await checkA11y(page);

  await page.click('text=Place Order');
  await checkA11y(page);
});
```

### Pattern 3: Storybook Integration

```typescript
// Storybook 9+ has built-in a11y testing
export default {
  component: Dropdown,
  tags: ['autodocs'],
  // Automatic accessibility tests for all stories
};
```

## Mandatory Verification Checklist

BEFORE claiming UI work complete:

### Automated Testing
- [ ] axe-core test passing (0 violations)
- [ ] Test output captured and included in evidence
- [ ] All violations fixed or documented as exceptions

### Keyboard Testing
- [ ] Tab through all interactive elements successfully
- [ ] Enter/Space activates buttons
- [ ] Escape closes modals/dialogs
- [ ] No keyboard traps found
- [ ] Focus visible on all elements

### Screen Reader Verification
- [ ] All buttons have accessible names
- [ ] All form inputs have labels
- [ ] All images have alt text or are decorative
- [ ] Custom controls have proper ARIA

### Lighthouse Audit
- [ ] Lighthouse accessibility score ≥95
- [ ] Screenshot of score included in evidence
- [ ] Any issues below 95 documented and justified

**If ANY checkbox unchecked**: UI is NOT accessible. Fix before claiming complete.

## Evidence Requirements


## References

For detailed information, see:

- `references/detailed-guide.md` - Complete workflow details, examples, and troubleshooting
