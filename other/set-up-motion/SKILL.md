---
name: set-up-motion
description: Use when adding animation and transitions to a frontend — uses the native View Transitions API for navigation/layout changes and the Motion library (motion/react, formerly Framer Motion) for component enter/exit/gesture animation, with every animation gated behind prefers-reduced-motion.
---

# Set Up Motion

## 1. Audit current state

```bash
cat .claude/stack-profile.md 2>/dev/null || cat ~/.claude/stack-profile.md 2>/dev/null   # frontend.framework, frontend.meta, package_manager
grep -E '"(motion|framer-motion|motion-v|@vueuse/motion)"' package.json 2>/dev/null
grep -rn "startViewTransition\|view-transition-name\|prefers-reduced-motion\|useReducedMotion" src/ 2>/dev/null | head
```

Read `frontend.framework` and `package_manager` (commands use pnpm). `frontend.meta` of `nuxt` ships `motion-v/nuxt` and its own page transitions — prefer those. **Prerequisites:** `@/` alias; pairs with `set-up-routing` (route view-transitions) and `configure-accessibility` (reduced-motion is an a11y requirement, not a nicety).

## 2. Decide what to do
- No motion → full setup.
- Animations present but always-on (ignore reduce-motion) → gate them (step 7) — that's an accessibility bug.

## 3. Detect framework
React → **Motion** (`motion/react`). Vue → **`motion-v`**, the Vue build of Motion (documented on motion.dev; same props, `AnimatePresence`, `MotionConfig`). The View Transitions API is native (no dependency) and works in both. Why: `motion-patterns.md`.

## 4. Install
```bash
pnpm add motion          # React (the package was renamed from framer-motion)
# Vue: pnpm add motion-v
```

## 5. View Transitions for navigation + layout changes

Native, GPU-accelerated, near-zero JS. Wrap any DOM change you want animated:
```ts
// src/utils/withViewTransition.ts
export function withViewTransition(update: () => void | Promise<void>): void {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !document.startViewTransition) {
    void update();
    return;
  }
  document.startViewTransition(update); // the browser snapshots the new DOM after `update` settles
}
```
The callback must finish the DOM change before it returns or its promise settles. React state updates are batched, so flush them inside: `withViewTransition(() => flushSync(() => setView(next)))`. In Vue, await the DOM: `withViewTransition(async () => { await router.push(to); await nextTick(); })`. React 19.3 also ships a stable `<ViewTransition>` component that animates updates made in a `startTransition` / Suspense reveal without calling the API by hand — prefer it for React state changes; keep this helper for Vue and non-React code.

For routing, let the router drive it: TanStack Router has `defaultViewTransition` on `createRouter` and a `viewTransition` prop on `<Link>`; Vue Router has no built-in hook, so wrap the navigation as above. Name shared elements so they morph between routes:
```css
/* the element that persists across routes */
.hero { view-transition-name: hero; }

@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) { animation: none !important; }
}
```

## 6. Component animation with Motion (React)

```tsx
// src/main.tsx — once, at the root: every motion component honours the OS setting
import { MotionConfig } from 'motion/react';
// <MotionConfig reducedMotion="user"><App /></MotionConfig>
```
```tsx
import { AnimatePresence, motion } from 'motion/react';

export function Toast({ open, children }: { open: boolean; children: React.ReactNode }) {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 8 }}
          transition={{ duration: 0.2, ease: 'easeOut' }}
        >
          {children}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```
Under `reducedMotion="user"` Motion drops the transform (`y`) and layout animation and keeps the opacity fade, so the component carries no reduced-motion branch of its own.
`AnimatePresence` is the reason to reach for Motion — it animates **exit**, which CSS can't do on unmount. Vue: `motion-v`'s `<motion.div>` inside `<AnimatePresence>` (same API, wrap the app in its `MotionConfig`), or Vue's built-in `<Transition>`/`<TransitionGroup>` for simple enter/exit.

## 7. Gate everything behind reduced motion

Three layers, all required:
- **Motion:** `<MotionConfig reducedMotion="user">` at the root (above); `useReducedMotion()` only for custom cases such as stopping autoplay video.
- **Tailwind:** author transitions as `motion-safe:transition` / disable with `motion-reduce:transition-none`.
- **View Transitions:** the `@media (prefers-reduced-motion: reduce)` block (step 5) kills them.

Essential feedback (a spinner) may remain; decorative motion (parallax, large slides) must not.

## 8. Verify
```bash
pnpm dev
```
Animations play normally; with OS "Reduce motion" on, transitions are removed/instant and nothing janks. Check the Performance panel: animated properties stay on the compositor (transform/opacity), no layout thrash.

## References
- ./motion-patterns.md — View-Transitions-vs-Motion, animate-transform-not-layout, reduced-motion, motion-is-feedback, performance budget.
- ../configure-accessibility/SKILL.md — reduced motion as an a11y requirement.
- ../_shared/conventions.md — `@/` alias, `utils/` for the pure `withViewTransition` helper.
