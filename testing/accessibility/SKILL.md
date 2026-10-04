---
name: accessibility
description: Web accessibility (WCAG 2.2) for Next.js applications — semantic HTML, ARIA, keyboard navigation, screen reader support, and automated testing. Use when building new pages, reviewing component accessibility, or fixing accessibility issues.
trigger: 需要提升网站可访问性
input: 网站代码
output: 可访问性优化建议
next: 无
dependencies: 无
---

# Frontend Accessibility (WCAG 2.2)

Practical accessibility for Next.js applications.

## Baseline Standards (WCAG 2.2 Level AA)

### 1. Semantic HTML

Use native HTML elements before ARIA. Correct semantics solve most accessibility issues.

```tsx
// ❌ Div soup
<div onClick={...} role="button" tabIndex={0}>Click me</div>

// ✅ Native button
<button onClick={...}>Click me</button>

// ❌ Nav as generic div
<div className="nav"><a href="/">Home</a></div>

// ✅ Use <nav>
<nav aria-label="Main"><a href="/">Home</a></nav>
```

### 2. Keyboard Navigation

Every interactive element must be reachable and operable via keyboard.

```tsx
// Tab order — check these in order:
// 1. Do interactive elements have visible focus indicators?
// 2. Is the tab order logical (DOM order = focus order)?
// 3. Can all functionality be reached with Tab / Shift+Tab?
// 4. Can dropdowns/menus/modals be closed with Escape?

const focusRing = 'focus-visible:outline-2 focus-visible:outline-blue-500'
```

### 3. ARIA Labels

Every interactive element needs an accessible name.

```tsx
// Icon buttons need labels
<button aria-label="Search">
  <SearchIcon />
</button>

// Sections need labelled landmarks
<nav aria-label="Footer navigation">...</nav>
<aside aria-label="Related articles">...</aside>
```

## Next.js Specific Considerations

### Link Components

```tsx
// Links need discernible text
<Link href="/articles/1" aria-label="Read article: How to build accessible apps">
  Read more
</Link>
```

### Image alt Text

```tsx
// Decorative images: alt=""
<Image src="/bg.jpg" alt="" role="presentation" />

// Informative images: describe the content
<Image src="/chart.png" alt="Revenue chart: Q1 $10K, Q2 $15K, Q3 $12K" />
```

### Form Validation

```tsx
// Associate errors with inputs
<label htmlFor="email">Email</label>
<input
  id="email"
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? 'email-error' : undefined}
/>
{errors.email && <p id="email-error" role="alert">{errors.email}</p>}
```

## Automated Testing

```bash
# Install axe-core Playwright integration
npm install -D @axe-core/playwright

# Run in CI as part of E2E tests
```

```ts
import { injectAxe, checkA11y } from 'axe-playwright'

test('homepage has no violations', async ({ page }) => {
  await page.goto('/')
  await injectAxe(page)
  await checkA11y(page, null, {
    includedImpacts: ['critical', 'serious']
  })
})
```

## Manual Testing Checklist

- [ ] Navigate all pages with Tab only — is everything reachable?
- [ ] Can all actions be completed without a mouse?
- [ ] Does every image have appropriate alt text?
- [ ] Are focus indicators visible on all interactive elements?
- [ ] Does zooming to 200% break layout?
- [ ] Can forms be submitted with Enter key?
- [ ] Do error messages have `role="alert"`?
- [ ] Is color contrast ≥ 4.5:1 for normal text, ≥ 3:1 for large text?
- [ ] Is the page navigable with a screen reader (VoiceOver / NVDA)?

## Resources

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [Next.js Accessibility Docs](https://nextjs.org/docs/accessibility)
- [Axe DevTools browser extension](https://www.deque.com/axe/devtools/)