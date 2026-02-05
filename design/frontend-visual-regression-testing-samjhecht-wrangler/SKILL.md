---
name: frontend-visual-regression-testing
description: Use when implementing UI components, design systems, or responsive layouts - verifies visual correctness through screenshot comparison and DevTools verification; prevents shipping broken UI
---

# Frontend Visual Regression Testing

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: frontend-visual-regression-testing | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: frontend-visual-regression-testing | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



## Overview

Visual regression testing captures screenshots of UI components/pages and compares them against baseline images to detect unintended visual changes.

**When to use this skill:**
- Implementing new UI components
- Modifying existing UI
- Working on design systems
- Implementing responsive layouts
- Refactoring CSS/styling

## The Iron Law

```
NO UI CHANGES WITHOUT VISUAL VERIFICATION
```

If you changed UI code (HTML, CSS, JSX, templates):
- You MUST take screenshots
- You MUST verify in DevTools
- You MUST compare against baseline (if exists)
- You CANNOT claim "looks good" without evidence

## Visual TDD Cycle

Visual regression testing integrates with TDD through TWO sequential cycles:

### Phase 1: Component Functionality (Traditional TDD)

**RED Phase:**
```typescript
test('checkout form renders with required fields', async ({ mount }) => {
  const component = await mount('<checkout-form></checkout-form>');

  // Test functionality (TDD RED - this will fail)
  await expect(component.locator('[name="cardNumber"]')).toBeVisible();
  await expect(component.locator('[name="expiry"]')).toBeVisible();
  await expect(component.locator('[name="cvc"]')).toBeVisible();
});
```
Run test: FAILS (component doesn't exist)

**GREEN Phase:**
```typescript
// Implement checkout-form component
// Add cardNumber, expiry, cvc fields
```
Run test: PASSES (component renders fields)

**REFACTOR Phase:**
Improve component structure, styling, accessibility

---

### Phase 2: Visual Correctness (Visual TDD)

**After component functionally works**, add visual verification:

```typescript
test('checkout form visual appearance', async ({ mount, page }) => {
  await mount('<checkout-form></checkout-form>');

  // Visual regression test
  await expect(page.locator('.checkout-form'))
    .toHaveScreenshot('checkout-form.png');
});
```

**First run (Baseline Generation):**
- No baseline exists
- Test generates baseline screenshot
- Review baseline: Does it look correct?
- Commit baseline to git

**RED Phase (Visual Regression):**
After baseline exists, make CSS change:
```css
/* Change button color from blue to red */
.submit-button { background: red; }
```
Run test: FAILS (screenshot doesn't match baseline)
Review diff: Is change intentional?

**GREEN Phase (Update Baseline if Intentional):**
If red button is intentional:
```bash
npm test -- --update-snapshots
```
New baseline committed
Run test: PASSES

If red button is NOT intentional (regression):
```css
/* Revert change */
.submit-button { background: blue; }
```
Run test: PASSES

---

### Summary: Two TDD Cycles

1. **Functional TDD** (first): Write test for component behavior → Implement → Refactor
2. **Visual TDD** (second): Generate baseline → Make changes → Verify no regressions

**Integration:**
- Functional tests come FIRST (component must work before visual testing)
- Visual tests come SECOND (component must look right)
- Both follow TDD, but visual baseline generation is a special case
- Baseline generation doesn't violate "watch it fail" - the failure comes when you change CSS and screenshot differs

**Cross-reference:** See test-driven-development skill for core RED-GREEN-REFACTOR principles.

## Step-by-Step Process

### Step 1: Before Implementation

**IF baseline exists** (modifying existing UI):
1. Note current visual state
2. Identify what should change
3. Identify what should NOT change

**IF no baseline** (new UI):
1. Plan visual appearance
2. Prepare to capture initial screenshot

### Step 2: During Implementation

**Write tests first** (TDD):
```typescript
// Test that component renders
test('checkout form renders correctly', async ({ page }) => {
  await mount('<checkout-form></checkout-form>');

  // Take screenshot of component
  await expect(page.locator('[data-testid="checkout-form"]'))
    .toHaveScreenshot('checkout-form.png');
});
```

**Implement component** (GREEN phase)

### Step 3: Visual Verification (MANDATORY)

#### 3.1: Take Screenshot

**Prefer element-level over full-page:**

```typescript
// ✅ GOOD: Element-level (less noise)
await expect(page.locator('.checkout-form'))
  .toHaveScreenshot('checkout-form.png');

// ❌ BAD: Full page (too much noise)
await expect(page).toHaveScreenshot('entire-page.png');
```

#### 3.2: DevTools Verification

**BEFORE claiming UI works:**

1. **Open DevTools Console**:
   - Press F12 or Cmd+Option+I
   - Click "Console" tab
   - Refresh page

2. **Verify NO errors**:
   ```
   ✅ GOOD: Console is empty (or only expected logs)
   ❌ BAD: Red errors visible
   ❌ BAD: Yellow warnings visible (unless documented)
   ```

3. **Take Console Screenshot**:
   - Screenshot showing clean console
   - Include in completion evidence

4. **Check Network Tab**:
   - Click "Network" tab
   - Refresh page
   - Verify expected requests made
   - Verify no failed requests (red)

5. **Test Responsive Breakpoints**:
   - Mobile: 375x667 (iPhone SE)
   - Tablet: 768x1024 (iPad)
   - Desktop: 1920x1080

#### 3.3: Compare Against Baseline

**IF baseline exists:**

```typescript
// Test runs, Playwright compares screenshots
// IF different: Test fails with diff image
```

Review diff image:
- **Green pixels**: New content
- **Red pixels**: Removed content
- **Yellow pixels**: Changed content

**Decision tree:**
```
Are differences intentional?
├─ YES → Update baseline, document why
└─ NO → Fix regression, re-run test
```

**IF no baseline:**
- First run generates baseline
- Visually review screenshot
- Verify it looks correct
- Commit baseline image to git

### Step 4: Baseline Management

**Baseline files:**
```
tests/
  screenshots/
    checkout-form.png           ← Baseline
    checkout-form-diff.png      ← Diff (if different)
    checkout-form-actual.png    ← Actual (if different)
```

**When to update baseline:**
- ✅ Intentional UI changes
- ✅ Design system updates
- ✅ After reviewing and approving diff
- ❌ NEVER: To make test pass without reviewing
- ❌ NEVER: Because "it looks fine to me"

**Updating baseline:**
```bash
# Review diff first!
# If intentional, update baseline:
npm test -- --update-snapshots

# Or Playwright specific:
npx playwright test --update-snapshots
```

## Framework-Agnostic Patterns

### Playwright (Recommended)

```typescript
test('visual regression', async ({ page }) => {
  await page.goto('/checkout');

  // Element-level screenshot
  await expect(page.locator('.checkout-form'))
    .toHaveScreenshot('checkout-form.png', {
      maxDiffPixels: 100, // Allow minor differences
    });
});
```

### Puppeteer

```typescript
test('visual regression', async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:3000/checkout');

  const element = await page.$('.checkout-form');
  await element.screenshot({ path: 'checkout-form.png' });

  // Compare manually or use Percy/Chromatic
  await browser.close();
});
```

### Cloud Solutions (Optional)

- **Chromatic**: Cloud visual testing with Storybook
- **Percy**: Cross-browser screenshot comparison
- **LambdaTest SmartUI**: AI-powered visual testing

## When to Use Visual Testing

**YES** (visual tests appropriate):
- Layout changes detection
- CSS regression prevention
- Cross-browser rendering verification
- Design system component verification
- Responsive design validation

**NO** (use other test types):
- Dynamic content (timestamps, random data)
- Third-party widgets (ads, analytics)
- Content that changes frequently
- Animations mid-transition (unless testing specific frame)

## Configuration Best Practices

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,        // Allow minor rendering differences
      threshold: 0.2,            // 20% threshold for pixel differences
      animations: 'disabled',    // Disable animations for stability
    },
  },
});
```

## Mandatory Verification Checklist

BEFORE claiming UI work complete:

### Visual Verification
- [ ] Screenshot taken for all changed UI elements
- [ ] Screenshot compared against baseline (if exists)
- [ ] Differences reviewed and determined intentional/regression
- [ ] Baseline updated if changes intentional

### DevTools Verification
- [ ] DevTools Console opened
- [ ] Console shows NO errors (0 red messages)
- [ ] Console shows NO warnings (or warnings documented)
- [ ] Console screenshot taken and included in evidence

### Network Verification
- [ ] DevTools Network tab opened
- [ ] Expected API calls made
- [ ] No failed requests (no red in network tab)
- [ ] Response data correct

### Responsive Verification
- [ ] Tested mobile breakpoint (375x667)
- [ ] Tested tablet breakpoint (768x1024)
- [ ] Tested desktop breakpoint (1920x1080)

**If ANY checkbox unchecked**: UI work is NOT complete.

## Evidence Requirements

When claiming UI work complete, provide:

1. **Screenshot evidence**:
   ```
   Screenshot: checkout-form.png (baseline)
   [Attach screenshot]

   Changes: Intentional (updated button styling)
   Baseline updated: YES
   ```

2. **DevTools Console evidence**:
   ```
   Console verification:
   [Screenshot showing empty console]

   Errors: 0
   Warnings: 0
   ```

3. **Network evidence** (if API calls):
   ```
   Network verification:
   [Screenshot showing successful requests]

   Expected requests: ✓ GET /api/products
   Failed requests: 0
   ```

## Red Flags - STOP IMMEDIATELY

If you catch yourself:
- Claiming "looks good" without screenshots
- Skipping DevTools verification
- Updating baseline without reviewing diff
- Taking full-page screenshots for component changes
- Proceeding with console errors visible
- Not testing responsive breakpoints

THEN:
- STOP immediately
- Complete all verification steps
- This is not optional

## Integration with Other Skills

**Combines with:**
- test-driven-development: Visual tests follow TDD cycle
- verification-before-completion: Visual verification required
- frontend-accessibility-verification: Check a11y after visual verification

## Common Rationalizations

| Rationalization | Counter |
|----------------|---------|
| "I can see it looks good" | Your eyes aren't regression tests. Take screenshot. |
| "It's a small change" | Small changes cause visual regressions. Screenshot required. |
| "I'll check it in the browser" | Browser check ≠ automated verification. Take screenshot. |
| "Console errors don't affect appearance" | Errors indicate bugs. Fix before claiming complete. |
| "Full page screenshot is easier" | Element screenshots catch actual changes. Be specific. |

## Example Session

```
Agent: "I'm implementing a checkout form component."

[Uses frontend-visual-regression-testing skill]

1. Write test expecting checkout form renders
2. Take screenshot of component → baseline
3. Run test → PASS (baseline generated)
4. Refactor CSS for better spacing
5. Run test → FAIL (screenshot different)
6. Review diff → Intentional (better spacing)
7. Update baseline
8. Open DevTools console → 0 errors
9. Take console screenshot
10. Test responsive breakpoints → All look correct
11. Provide evidence in completion message:
    - checkout-form.png (baseline)
    - Console screenshot (0 errors)
    - Responsive screenshots (mobile/tablet/desktop)

"Checkout form complete. Visual regression test passing.
Console clean. Responsive breakpoints verified."
```

## References

- Playwright screenshot comparison: https://playwright.dev/docs/test-snapshots
- Testing Library philosophy: Test user-visible behavior
- Modern frontend testing (2024-2025 practices)

---

**Remember**: NO UI CHANGES WITHOUT VISUAL VERIFICATION. Screenshots are evidence, not optional.
