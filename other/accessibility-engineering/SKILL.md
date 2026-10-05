---
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
description: 'Build and maintain accessible web applications at scale. Covers automated
  testing

  integration, accessibility auditing workflows, component library patterns, and

  WCAG 2.2 remediation strategies. Use when implementing accessibility testing in

  CI/CD, auditing existing applications, building accessible component systems,

  or fixing accessibility violations. Triggers on a11y testing, axe-core,

  accessibility audit, WCAG compliance, accessibility CI, screen reader testing.'
name: accessibility-engineering
---

# Accessibility Engineering

Build, test, and maintain accessible web applications at scale. This guide covers automated testing integration, audit workflows, accessible component patterns, and practical remediation strategies.

## When Accessibility Testing Matters

Not every project needs the same level of accessibility rigor. Choose your approach based on risk:

| Context | Minimum Approach | Recommended |
|---------|------------------|-------------|
| Internal tools | Axe-core in dev | Add keyboard testing |
| Public marketing sites | Axe-core CI + manual spot checks | Full VPAT audit |
| SaaS products | Axe-core CI + keyboard + basic SR | Component-level testing |
| Healthcare, finance, government | Full automated suite + manual audit | External VPAT certification |
| Mobile apps (native) | Platform-specific tools | Quarterly manual audit |

## Automated Testing Strategy

### The Testing Pyramid for Accessibility

```
                    ▲
                   /│\
                  / │ \     Manual Testing (5%)
                 /  │  \    - Real screen reader validation
                /───┼───\   - Cognitive/motor disability testing
               /    │    \
              /     │     \  Integration Testing (25%)
             /      │      \ - Page-level axe scans
            /       │       \- Full keyboard navigation
           /────────┼────────\
          /         │         \
         /          │          \ Component Testing (70%)
        /           │           \- Unit tests with axe-core
       /            │            \- Focus management tests
      /─────────────┴─────────────\
```

### Axe-Core Integration

Axe-core is the industry standard. Integrate it at multiple levels.

#### Jest/Vitest Component Tests

```typescript
// setup.ts
import { configureAxe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

// Configure for your needs
const axe = configureAxe({
  rules: {
    // Disable rules that don't apply to your context
    'region': { enabled: false }, // Fragments don't need landmark regions
  },
});
```

```typescript
// Button.test.tsx
import { render } from '@testing-library/react';
import { axe } from 'jest-axe';
import { Button } from './Button';

describe('Button accessibility', () => {
  it('has no violations in default state', async () => {
    const { container } = render(<Button>Click me</Button>);
    expect(await axe(container)).toHaveNoViolations();
  });

  it('has no violations when disabled', async () => {
    const { container } = render(<Button disabled>Disabled</Button>);
    expect(await axe(container)).toHaveNoViolations();
  });

  it('has no violations with icon-only variant', async () => {
    const { container } = render(
      <Button aria-label="Close dialog">
        <CloseIcon aria-hidden="true" />
      </Button>
    );
    expect(await axe(container)).toHaveNoViolations();
  });
});
```

#### Playwright Page-Level Tests

```typescript
// a11y.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('home page has no critical violations', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    // Log violations for debugging (useful in CI)
    if (results.violations.length > 0) {
      console.log('Accessibility violations:',
        JSON.stringify(results.violations, null, 2));
    }

    expect(results.violations).toEqual([]);
  });

  test('critical user flows are keyboard accessible', async ({ page }) => {
    await page.goto('/login');

    // Tab through form
    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Email')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Password')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Sign in' })).toBeFocused();
  });

  test('modal focus is trapped correctly', async ({ page }) => {
    await page.goto('/dashboard');
    await page.getByRole('button', { name: 'Settings' }).click();

    const modal = page.getByRole('dialog');
    await expect(modal).toBeVisible();

    // Focus should be inside modal
    const activeElement = page.locator(':focus');
    await expect(activeElement).toBeAttached();

    // Tab to end of modal
    for (let i = 0; i < 10; i++) {
      await page.keyboard.press('Tab');
    }

    // Focus should still be inside modal (trapped)
    const focusedElement = await page.evaluate(() => document.activeElement?.closest('[role="dialog"]'));
    expect(focusedElement).toBeTruthy();

    // Escape should close modal
    await page.keyboard.press('Escape');
    await expect(modal).not.toBeVisible();
  });
});
```

#### Storybook Integration

```typescript
// .storybook/test-runner.ts
import { getStoryContext } from '@storybook/test-runner';
import { injectAxe, checkA11y } from 'axe-playwright';

export const preVisit = async (page) => {
  await injectAxe(page);
};

export const postVisit = async (page, context) => {
  const storyContext = await getStoryContext(page, context);

  // Skip a11y tests for specific stories
  if (storyContext.parameters?.a11y?.disable) {
    return;
  }

  await checkA11y(page, '#storybook-root', {
    detailedReport: true,
    detailedReportOptions: {
      html: true,
    },
  });
};
```

### CI/CD Pipeline Integration

#### GitHub Actions

```yaml
# .github/workflows/accessibility.yml
name: Accessibility

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  a11y-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run component a11y tests
        run: npm run test:a11y

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Build app
        run: npm run build

      - name: Start server
        run: npm run start &

      - name: Wait for server
        run: npx wait-on http://localhost:3000

      - name: Run Playwright a11y tests
        run: npx playwright test --project=a11y

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: a11y-results
          path: |
            playwright-report/
            test-results/
```

#### Preventing Regressions

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    {
      name: 'a11y',
      testMatch: /.*\.a11y\.spec\.ts/,
      use: {
        ...devices['Desktop Chrome'],
      },
    },
    {
      name: 'a11y-mobile',
      testMatch: /.*\.a11y\.spec\.ts/,
      use: {
        ...devices['iPhone 14'],
      },
    },
  ],
  // Fail CI on any a11y violations
  expect: {
    toHaveNoViolations: {
      // Optionally configure impact levels to fail on
      // 'minor' | 'moderate' | 'serious' | 'critical'
      failOnImpact: 'serious',
    },
  },
});
```

## Focus Management Patterns

### Focus Trap for Modals

Focus must stay within modal dialogs. Here's a production-ready implementation:

```typescript
import { useEffect, useRef, useCallback } from 'react';

interface UseFocusTrapOptions {
  enabled?: boolean;
  returnFocusOnClose?: boolean;
}

export function useFocusTrap<T extends HTMLElement>(
  options: UseFocusTrapOptions = {}
) {
  const { enabled = true, returnFocusOnClose = true } = options;
  const containerRef = useRef<T>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  const getFocusableElements = useCallback(() => {
    if (!containerRef.current) return [];

    const selector = [
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      'a[href]',
      '[tabindex]:not([tabindex="-1"])',
    ].join(', ');

    return Array.from(
      containerRef.current.querySelectorAll<HTMLElement>(selector)
    ).filter((el) => {
      // Exclude hidden elements
      return el.offsetParent !== null && getComputedStyle(el).visibility !== 'hidden';
    });
  }, []);

  useEffect(() => {
    if (!enabled) return;

    previousFocusRef.current = document.activeElement as HTMLElement;

    // Focus first focusable element or container
    const focusables = getFocusableElements();
    if (focusables.length > 0) {
      focusables[0].focus();
    } else {
      containerRef.current?.focus();
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      const focusables = getFocusableElements();
      if (focusables.length === 0) {
        e.preventDefault();
        return;
      }

      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);

      if (returnFocusOnClose && previousFocusRef.current) {
        previousFocusRef.current.focus();
      }
    };
  }, [enabled, returnFocusOnClose, getFocusableElements]);

  return containerRef;
}
```

### Roving Tabindex for Composite Widgets

For toolbars, menus, and tab lists, use roving tabindex instead of individual tab stops:

```typescript
import { useState, useCallback, KeyboardEvent } from 'react';

interface UseRovingTabindexOptions {
  orientation?: 'horizontal' | 'vertical' | 'both';
  loop?: boolean;
}

export function useRovingTabindex<T extends HTMLElement>(
  items: T[],
  options: UseRovingTabindexOptions = {}
) {
  const { orientation = 'horizontal', loop = true } = options;
  const [activeIndex, setActiveIndex] = useState(0);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      const prev = orientation === 'vertical' ? 'ArrowUp' : 'ArrowLeft';
      const next = orientation === 'vertical' ? 'ArrowDown' : 'ArrowRight';

      let newIndex = activeIndex;

      switch (e.key) {
        case prev:
          e.preventDefault();
          newIndex = activeIndex - 1;
          if (newIndex < 0) {
            newIndex = loop ? items.length - 1 : 0;
          }
          break;
        case next:
          e.preventDefault();
          newIndex = activeIndex + 1;
          if (newIndex >= items.length) {
            newIndex = loop ? 0 : items.length - 1;
          }
          break;
        case 'Home':
          e.preventDefault();
          newIndex = 0;
          break;
        case 'End':
          e.preventDefault();
          newIndex = items.length - 1;
          break;
      }

      if (newIndex !== activeIndex) {
        setActiveIndex(newIndex);
        items[newIndex]?.focus();
      }
    },
    [activeIndex, items, orientation, loop]
  );

  return {
    activeIndex,
    setActiveIndex,
    getTabIndex: (index: number) => (index === activeIndex ? 0 : -1),
    handleKeyDown,
  };
}
```

### Skip Links

Allow keyboard users to bypass navigation:

```tsx
// SkipLinks.tsx
export function SkipLinks() {
  return (
    <nav aria-label="Skip links" className="skip-links">
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <a href="#main-navigation" className="skip-link">
        Skip to navigation
      </a>
    </nav>
  );
}
```

```css
.skip-link {
  position: absolute;
  left: -10000px;
  top: auto;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.skip-link:focus {
  position: fixed;
  top: 0;
  left: 0;
  width: auto;
  height: auto;
  padding: 1rem 2rem;
  background: var(--color-primary);
  color: white;
  z-index: 9999;
  outline: 3px solid var(--color-focus);
  outline-offset: 2px;
}
```

## Accessible Component Patterns

### Accessible Button

```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  loading?: boolean;
  iconOnly?: boolean;
}

export function Button({
  children,
  variant = 'primary',
  loading = false,
  iconOnly = false,
  disabled,
  'aria-label': ariaLabel,
  ...props
}: ButtonProps) {
  // Icon-only buttons MUST have aria-label
  if (iconOnly && !ariaLabel) {
    console.warn('Icon-only buttons require aria-label for accessibility');
  }

  return (
    <button
      type="button"
      disabled={disabled || loading}
      aria-disabled={disabled || loading}
      aria-busy={loading}
      aria-label={ariaLabel}
      className={cn('button', `button--${variant}`, {
        'button--loading': loading,
        'button--icon-only': iconOnly,
      })}
      {...props}
    >
      {loading && (
        <span className="button__spinner" aria-hidden="true">
          <Spinner />
        </span>
      )}
      <span className={cn({ 'sr-only': iconOnly && loading })}>
        {children}
      </span>
      {loading && <span className="sr-only">Loading...</span>}
    </button>
  );
}
```

### Accessible Form Field

```tsx
interface FormFieldProps {
  id: string;
  label: string;
  error?: string;
  hint?: string;
  required?: boolean;
  children: React.ReactElement;
}

export function FormField({
  id,
  label,
  error,
  hint,
  required,
  children,
}: FormFieldProps) {
  const hintId = hint ? `${id}-hint` : undefined;
  const errorId = error ? `${id}-error` : undefined;
  const describedBy = [hintId, errorId].filter(Boolean).join(' ') || undefined;

  return (
    <div className="form-field">
      <label htmlFor={id}>
        {label}
        {required && (
          <>
            <span aria-hidden="true" className="required-marker">*</span>
            <span className="sr-only">(required)</span>
          </>
        )}
      </label>

      {hint && (
        <p id={hintId} className="form-field__hint">
          {hint}
        </p>
      )}

      {React.cloneElement(children, {
        id,
        'aria-required': required,
        'aria-invalid': !!error,
        'aria-describedby': describedBy,
      })}

      {error && (
        <p id={errorId} className="form-field__error" role="alert">
          <span className="sr-only">Error:</span>
          {error}
        </p>
      )}
    </div>
  );
}
```

### Accessible Disclosure/Accordion

```tsx
interface DisclosureProps {
  id: string;
  title: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
}

export function Disclosure({ id, title, defaultOpen = false, children }: DisclosureProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const contentId = `${id}-content`;

  return (
    <div className="disclosure">
      <h3>
        <button
          type="button"
          aria-expanded={isOpen}
          aria-controls={contentId}
          onClick={() => setIsOpen(!isOpen)}
          className="disclosure__trigger"
        >
          <span>{title}</span>
          <ChevronIcon
            aria-hidden="true"
            className={cn('disclosure__icon', { 'disclosure__icon--open': isOpen })}
          />
        </button>
      </h3>
      <div
        id={contentId}
        role="region"
        aria-labelledby={id}
        hidden={!isOpen}
        className="disclosure__content"
      >
        {children}
      </div>
    </div>
  );
}
```

## WCAG 2.2 Compliance Checklist

### New in WCAG 2.2 (December 2023)

| Criterion | Level | Requirement | How to Test |
|-----------|-------|-------------|-------------|
| 2.4.11 Focus Not Obscured (Minimum) | AA | Focused element isn't fully hidden by sticky headers/footers | Keyboard navigate while scrolled |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | Focused element isn't partially hidden | Same, stricter |
| 2.4.13 Focus Appearance | AAA | Focus indicator ≥2px perimeter, 3:1 contrast | Visual inspection |
| 2.5.7 Dragging Movements | AA | Single pointer alternative to drag | Test without mouse drag |
| 2.5.8 Target Size (Minimum) | AA | Interactive targets ≥24×24 CSS px | Measure touch targets |
| 3.2.6 Consistent Help | A | Help in same relative location across pages | Cross-page comparison |
| 3.3.7 Redundant Entry | A | Don't re-ask for same info in same session | User flow testing |
| 3.3.8 Accessible Authentication (Minimum) | AA | No cognitive function tests (CAPTCHA) | Verify auth flow |
| 3.3.9 Accessible Authentication (Enhanced) | AAA | No object recognition or personal recall | Same, stricter |

### Testing Focus Not Obscured

```typescript
// playwright test
test('focused elements are not obscured by sticky header', async ({ page }) => {
  await page.goto('/long-page');

  // Scroll down to trigger sticky header
  await page.evaluate(() => window.scrollTo(0, 500));

  // Tab to each focusable element
  const focusables = await page.$$('button, a, input, [tabindex="0"]');

  for (const element of focusables) {
    await element.focus();

    const boundingBox = await element.boundingBox();
    if (!boundingBox) continue;

    // Get sticky header height
    const headerHeight = await page.evaluate(() => {
      const header = document.querySelector('header');
      return header?.getBoundingClientRect().height ?? 0;
    });

    // Check element is not fully obscured
    expect(boundingBox.y).toBeGreaterThanOrEqual(headerHeight);
  }
});
```

## Remediation Workflow

When you inherit a codebase with accessibility issues:

### 1. Baseline Audit

```bash
# Run axe on deployed site
npx @axe-core/cli https://your-site.com --save results.json

# Generate HTML report
npx axe-report results.json --output report.html
```

### 2. Categorize by Impact and Effort

| Impact | Low Effort | High Effort |
|--------|------------|-------------|
| **Critical** | Do immediately | Schedule sprint |
| **Serious** | This week | Next sprint |
| **Moderate** | Backlog (prioritize) | Backlog |
| **Minor** | Opportunistic fixes | Deprioritize |

### 3. Common Quick Wins

```typescript
// Missing button text
// Before
<button onClick={close}><XIcon /></button>

// After
<button onClick={close} aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</button>
```

```typescript
// Missing form labels
// Before
<input type="email" placeholder="Email" />

// After
<label>
  Email
  <input type="email" />
</label>
```

```typescript
// Missing alt text
// Before
<img src="chart.png" />

// After - informative image
<img src="chart.png" alt="Sales increased 30% in Q4 2024" />

// After - decorative image
<img src="decorative-border.png" alt="" role="presentation" />
```

```css
/* Insufficient color contrast */
/* Before: 2.5:1 contrast */
.muted-text { color: #999; }

/* After: 4.5:1 contrast */
.muted-text { color: #767676; }
```

### 4. Track Progress

```typescript
// a11y-snapshot.ts - Run weekly to track progress
import AxeBuilder from '@axe-core/playwright';
import { chromium } from 'playwright';
import fs from 'fs';

async function generateSnapshot() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const routes = ['/', '/login', '/dashboard', '/settings'];
  const results: Record<string, number> = {};

  for (const route of routes) {
    await page.goto(`http://localhost:3000${route}`);
    const axeResults = await new AxeBuilder({ page }).analyze();
    results[route] = axeResults.violations.length;
  }

  const snapshot = {
    date: new Date().toISOString(),
    results,
    total: Object.values(results).reduce((a, b) => a + b, 0),
  };

  // Append to tracking file
  const history = JSON.parse(fs.readFileSync('a11y-history.json', 'utf-8'));
  history.push(snapshot);
  fs.writeFileSync('a11y-history.json', JSON.stringify(history, null, 2));

  await browser.close();
}
```

## Screen Reader Testing

### Essential Commands

| Action | NVDA (Windows) | VoiceOver (Mac) | JAWS |
|--------|----------------|-----------------|------|
| Start/stop | Ctrl+Alt+N | Cmd+F5 | Insert+J |
| Read next item | ↓ | VO+→ | ↓ |
| Read previous | ↑ | VO+← | ↑ |
| Headings list | Insert+F7 | VO+Cmd+H | Insert+F6 |
| Forms mode | Enter | Auto | Enter |
| Browse mode | Escape | Auto | Num+ |
| Links list | Insert+F7 | VO+Cmd+L | Insert+F7 |

### What to Test

1. **Page title** - Read when page loads
2. **Landmarks** - Can user navigate by region?
3. **Headings** - Logical hierarchy?
4. **Forms** - Labels announced? Errors associated?
5. **Dynamic content** - Live regions announce updates?
6. **Focus** - Can user tell where they are?
7. **Images** - Alt text meaningful?

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `tabindex > 0` | Breaks natural tab order | Use `tabindex="0"` or `-1` only |
| `aria-hidden="true"` on focusable | Focus invisible to SR | Remove aria-hidden or tabindex |
| `role="button"` on `<div>` | Missing keyboard support | Use `<button>` instead |
| Click handlers on `<span>` | Not focusable | Use `<button>` or add tabindex + keyboard |
| `outline: none` without alternative | No focus indicator | Provide visible focus style |
| Placeholder as label | Disappears on input | Use actual `<label>` |
| `aria-label` on non-interactive | Not announced | Only use on interactive or landmark |
| Color-only indicators | Invisible to color blind | Add icon, pattern, or text |
| Motion without `prefers-reduced-motion` | Vestibular triggers | Respect media query |
| `role="presentation"` on interactive | Removes from a11y tree | Don't do this |
