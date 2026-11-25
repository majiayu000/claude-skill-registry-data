---
name: motion
description: How animations and transitions work in EasyTask - the animation speed preference (System, Slow, Normal, None) applied as data-motion on the root, the CSS rules that scale or stop them, durations in JS, the exceptions (spinners, loading dots, live drag), WebKitGTK limits, and how to test them. Use when adding or changing an animation, a transition, an animated icon, or anything that moves on screen, and when auditing animations.
---

# Animations (EasyTask)

Every animation follows the user's preference **Impostazioni > Aspetto > Velocità delle animazioni** (`animationSpeed`: `system`, `slow`, `normal`, `none`). Nothing may move at its own speed.

## How the speed reaches the page

- `src/lib/animation-speed.ts`: `applyAnimationSpeed` writes `data-motion` on `<html>` (`slow` | `normal` | `none`). `system` is resolved to `none` when the OS asks for reduced motion (`prefers-reduced-motion`), otherwise `normal`, and follows OS changes live. Called from `contexts/preferences-context.tsx`.
- `src/index.css` (after `@layer utilities`):
  - `slow` = the original Tailwind durations (150ms), nothing overridden;
  - `normal` = `--default-transition-duration: 90ms` and `--tw-animation-duration: 100ms` (tw-animate-css, set on every element because the variable does not inherit);
  - `none` = every animation and transition at **1ms**, not 0: Radix components wait for the end of their exit animation to unmount. `.animate-spin` keeps turning (it says something is running); `.animate-pulse` (skeletons) stops.

## Writing an animation

1. **Prefer the existing machinery**: Tailwind `transition-*` with the default duration, tw-animate-css classes (`animate-in fade-in-0 zoom-in-95`, the ones shadcn components already use). They follow `data-motion` with no extra code.
2. **A fixed duration** (`duration-300`, `animation: x 1.2s`) does NOT follow `normal`/`slow`: add rules for `:root[data-motion="slow"]` and `:root[data-motion="none"]` next to the keyframes, like `.loading-dot` and `.live-drag-slot` in `index.css`.
3. **With the animations off the element is in its final state**, still and visible (`opacity: 1`, no transform), not hidden.
4. **Before the preference is applied** (first paint) add `@media (prefers-reduced-motion: reduce) { :root:not([data-motion]) ... }` as `.loading-dot` does.
5. **Durations in JS** (WAAPI, `setTimeout` waiting for an animation, rAF-driven moves): read them from `shiftDurationMs(base)` (0 / base / base × `SLOW_MOTION_RATIO`), never a literal. Read it once at the start of the gesture.
6. **Animate only `opacity` and `transform`** (no width, height, top/left, filter, box-shadow): they stay on the compositor, also on WebKitGTK, and do not trigger layout of the note.
7. **Purpose**: an animation confirms an action or shows a state (opening, appearing, saving, loading). No decorative loops; an infinite animation needs a reason (loading) and must stop with `none` unless it is a spinner.
8. Components to reuse: `components/loading-dots.tsx` (`LoadingDots`), `ui/progress-ring.tsx`, `ui/skeleton.tsx`, shadcn `dialog` / `popover` / `dropdown-menu` / `sheet` / `tooltip` (already animated).

## Engines

The app runs on WebView2 (Chromium, Windows), WebKitGTK (Linux) and WebKit (macOS). Avoid features only Chromium has without a fallback: View Transitions, scroll-driven animations, `@starting-style`, `interpolate-size`. Check them with the skill **modern-web-guidance** and keep a plain fallback (no animation) where unsupported.

## Tests

- Unit: `src/lib/animation-speed.test.ts` (resolution of `system`, `shiftDurationMs`). For a component, assert the class or the `data-*` state, not the timing (jsdom does not animate).
- e2e (skill **e2e-spec**): set the speed to `none` and check the final state is shown at once; with `normal` check the class is present. Do not wait on real durations.
- By hand, for the PR: the four speeds, the OS "reduce motion" (Windows: Settings > Accessibility > Visual effects > Animation effects) with `system`, and a look on Linux if possible.
