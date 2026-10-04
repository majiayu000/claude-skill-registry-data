---
name: frontend
description: Frontend development patterns — component design, accessibility, performance optimisation, and state management best practices for modern web UIs.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
---

# frontend

Frontend development patterns — component design, accessibility, performance optimisation, and state management best practices for modern web UIs.

## Instructions

Apply these frontend practices when building user interfaces:

## Guidelines

### Type Safety

- **Type-safe props**: every component must have an explicit props type or interface — no implicit `any`, no untyped `children`
- **Validated forms**: use React Hook Form + Zod resolver (or equivalent) for form validation — never trust `event.target.value` directly without parsing
- **API response types**: generate or define types for every API response; never spread untyped API data into state
- **Event handler types**: use precise event types (`React.ChangeEvent<HTMLInputElement>`) instead of `any`

### Error Handling

- Every data-fetching hook must expose `isLoading`, `error`, and `data` states — handle all three in the UI
- Wrap async UI sections in an `ErrorBoundary` component
- Display user-friendly error messages — never render raw `error.message` from API responses directly

### Performance Baseline

- No synchronous expensive computations in the render path — defer with `useMemo`/`useCallback` only after profiling confirms the bottleneck
- Images must have explicit `width` and `height` to prevent layout shifts (CLS)
- Bundle size budget: warn if a single route chunk exceeds 250 kB gzipped

### Accessibility Baseline

- All interactive elements must be operable by keyboard alone
- Colour contrast must meet WCAG 2.1 AA (≥ 4.5:1 for body text)
- Automated accessibility checks (`axe-core` or `eslint-plugin-jsx-a11y`) must pass in CI

---

### Component Design Principles

**Single Responsibility**: each component does one thing. Split large components into smaller, composable pieces.

**Presentational vs. Container components:**
- **Presentational** – pure UI; receives data via props; no side effects
- **Container/Smart** – fetches data, manages state, passes down to presentational components

**Naming conventions:**
- Component files: `PascalCase.tsx` (e.g., `UserCard.tsx`)
- Hooks: `useNoun.ts` (e.g., `useAuthSession.ts`)
- Utilities: `camelCase.ts` (e.g., `formatCurrency.ts`)

### Accessibility (a11y)

Every UI must meet **WCAG 2.1 AA** as a minimum:

- Use semantic HTML: `<button>`, `<nav>`, `<main>`, `<article>`, `<header>`, `<footer>` — not `<div>` for everything
- All interactive elements must be keyboard-focusable and operable
- Images must have meaningful `alt` text (or `alt=""` for decorative images)
- Colour contrast ratio: ≥ 4.5:1 for normal text, ≥ 3:1 for large text
- Form fields must have associated `<label>` elements
- Use `aria-*` attributes only when semantic HTML isn't sufficient
- Test with a screen reader (VoiceOver, NVDA) and keyboard-only navigation

```tsx
// Bad
<div onClick={handleSubmit}>Submit</div>

// Good
<button type="submit" onClick={handleSubmit}>Submit</button>
```

### Performance

**Core Web Vitals targets:**
- LCP (Largest Contentful Paint) < 2.5s
- INP (Interaction to Next Paint) < 200ms
- CLS (Cumulative Layout Shift) < 0.1

**Techniques:**
- Code-split by route: `const Page = lazy(() => import('./Page'))`
- Lazy-load images below the fold: `<img loading="lazy" />`
- Preload critical assets: `<link rel="preload" />`
- Use `useMemo` / `useCallback` only for proven bottlenecks (measure first)
- Virtualise long lists (react-virtual, TanStack Virtual)
- Serve modern formats (WebP, AVIF) for images
- Use a CDN for static assets

### State Management

Choose the right tool for the complexity level:

| Scope | Tool |
|-------|------|
| Local UI state | `useState`, `useReducer` |
| Shared component tree state | React Context (with care) |
| Server state (async) | TanStack Query, SWR |
| Complex global state | Zustand, Jotai, Redux Toolkit |
| Form state | React Hook Form, Formik |

**Rules:**
- Lift state up only as high as needed
- Server state and client state are different — manage them separately
- Avoid putting server-fetched data into global client state manually; use a data-fetching library

### CSS / Styling

- Use design tokens (CSS custom properties) for colours, spacing, typography
- Prefer utility-first CSS (Tailwind) or CSS Modules to avoid class name collisions
- Mobile-first responsive design: base styles for mobile, `md:` / `lg:` for larger breakpoints
- No magic numbers — use spacing scale (4px base, multiples of 4)

### Error Handling in UI

- Every async operation should have loading, success, and error states
- Show meaningful error messages (not "An error occurred")
- Use Error Boundaries to catch render errors
- Never expose stack traces or internal details to end users

## Examples

```tsx
// Accessible form with React Hook Form
import { useForm } from 'react-hook-form';

export function LoginForm({ onSubmit }) {
  const { register, handleSubmit, formState: { errors } } = useForm();

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        aria-invalid={!!errors.email}
        aria-describedby={errors.email ? 'email-error' : undefined}
        {...register('email', { required: 'Email is required' })}
      />
      {errors.email && (
        <span id="email-error" role="alert">{errors.email.message}</span>
      )}
      <button type="submit">Log in</button>
    </form>
  );
}
```

## References

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [Core Web Vitals](https://web.dev/vitals/)
- [TanStack Query](https://tanstack.com/query)
- [React Hook Form](https://react-hook-form.com/)
- [Zustand](https://github.com/pmndrs/zustand)
