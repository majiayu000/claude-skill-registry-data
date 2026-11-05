---
name: ui-ux-architect
version: 1.0.1
description: UI/UX standards — WCAG 2.2 AA, Radix + Tailwind 4 + shadcn/ui, design-token theming, mandatory loading/error/empty/success states on every async surface, mobile-first responsive, keyboard parity, contrast checked in CI. Use when designing UI components, building a design system, or auditing accessibility.
---

# UI / UX Architecture

Implementation-level standards for accessible, consistent, responsive frontends. Implements the *what* and *how*; framework-specific *where* lives in [react-architect](../../frameworks/react-architect/SKILL.md) and [nextjs-architect](../../frameworks/nextjs-architect/SKILL.md). Component recipes, token templates, and testing setup in [RECIPES.md](RECIPES.md). Pinned dependencies in [STACK.md](STACK.md).

## 1. Accessibility floor — WCAG 2.2 AA

Non-negotiable. Every shipped component meets WCAG 2.2 Level AA; AAA where reasonable.

- **Semantic HTML first.** A `<button>` is a button; a `<div onClick>` is a bug. `<nav>`, `<main>`, `<article>`, `<aside>`, `<header>`, `<footer>` mark landmarks.
- **Every interactive element is keyboard-operable.** `Tab` to focus, `Enter`/`Space` to activate, `Escape` to dismiss, arrow keys inside composite widgets. No mouse-only behavior.
- **Visible focus indicator on every focusable element.** Don't `outline: none` without replacing it. Tailwind: `focus-visible:ring-2 focus-visible:ring-offset-2`.
- **Color contrast** ≥ 4.5:1 for normal text, ≥ 3:1 for large text and UI components. Enforced by `axe-core` in CI; rejected at build.
- **Form labels.** Every `<input>` has a `<label htmlFor>`; placeholder text is *not* a label.
- **ARIA only when semantic HTML can't say it.** `aria-label` for icon-only buttons, `aria-describedby` for inline help, `role="alert"` for live announcements. Don't sprinkle `role="button"` — write `<button>`.
- **`prefers-reduced-motion`** respected — Tailwind: `motion-safe:` / `motion-reduce:` variants. Disable parallax, autoplay, large transitions for users who request it.

## 2. Component primitives — Radix + Tailwind + shadcn/ui

Don't reinvent dialogs, dropdowns, popovers, comboboxes. Modern accessibility is hard; let primitives do the keyboard/ARIA work.

- **[Radix UI](https://www.radix-ui.com/)** — headless, unstyled, accessible primitives. Focus management, keyboard nav, ARIA wiring all done.
- **Tailwind CSS 4** — utility-first styling on top of Radix. Variables-based theme system, design tokens via CSS custom properties.
- **shadcn/ui** — copy-paste component recipes (Radix + Tailwind). **Components live in your repo, not as a dep**; you own and adapt them.
- **Why not MUI / Mantine / Chakra?** Great but opinionated; harder to evolve a custom design system; ship more JS. Radix + Tailwind gives full control with smaller bundles.

Wrapper example (Dialog) in [RECIPES §1](RECIPES.md#1-radix--shadcn-dialog-wrapper).

## 3. Design tokens

Centralize every visual decision as a token. Components reference tokens; tokens evolve in one place.

- **Semantic over literal names.** `--color-primary` not `--color-blue-500`. Lets you change the palette without rewriting every component.
- **OKLCH for color.** Perceptually uniform, future-proof, supports wider gamuts.
- **Dark mode via CSS variables** — flip a few tokens, every component follows.
- **Spacing scale based on 4 px** (or 8 px). Don't introduce one-off values; reuse `--spacing-N`.
- **Type scale** centralized in tokens too (`--text-sm`, `--text-base`).

Full `@theme` template in [RECIPES §2](RECIPES.md#2-tailwind-4-theme-design-tokens).

## 4. Responsive — mobile-first, container queries when shape matters

- **Mobile-first.** Default styles are mobile; `md:`, `lg:` add desktop overrides.
- **Container queries** (`@container`) when a component's layout depends on its container size, not the viewport. New in Tailwind 4 — use them for components in narrow sidebars *and* wide pages.
- **Breakpoints** sparingly: `sm`, `md`, `lg`, `xl`, `2xl`. Don't invent new ones per project.
- **Touch targets** ≥ 44×44 px on mobile. WCAG 2.2 AA mandates 24×24 *minimum* but 44×44 is the modern usable size.
- **Fluid typography** — `clamp(1rem, 0.9rem + 0.5vw, 1.25rem)` scales smoothly without breakpoint jumps.
- **Test on real devices.** Browser DevTools mobile mode is a poor proxy for actual phones. Minimum: one iPhone, one Android.

## 5. The four required states — loading, error, empty, success

Every UI surface that touches data has four states. Build all four; don't pretend the success path is enough.

- **Loading** — skeletons for content, spinners for "button doing something", `aria-busy="true"`, no flashes under 300 ms.
- **Error** — plain language, retry button, correlation ID visible, no stack traces, different shape per error class (network/auth/validation).
- **Empty** — first-time empty differs from filtered empty; action always present.
- **Success** — tables semantic, cursor pagination, refetch indicator.

Full shape contracts in [RECIPES §3](RECIPES.md#3-required-ui-states--shape-contract).

## 6. Forms

- **Native HTML semantics.** `<form>`, `<label>`, `<input>` with right types (`email`, `tel`, `number`).
- **`autocomplete`** on every relevant field — browsers and password managers depend on them.
- **Inline validation** on blur, not on every keystroke. Submit-time validation is the final gate.
- **Error placement: below the input**, connected via `aria-describedby` — screen readers announce automatically.
- **Submit button disabled while pending** — use `aria-disabled="true"` (not `disabled`, which removes it from tab order).
- **Inline success feedback** — "Saved" with a checkmark for 2 s, then fade. Don't toast critical confirmations away.

## 7. Motion

- **`prefers-reduced-motion: reduce`** respected. Tailwind `motion-safe:transition-*`.
- **Functional motion only** — confirmation feedback, spatial relationships, state changes that wouldn't be perceptible otherwise.
- **No autoplaying video / animation** without user opt-in.
- **Easing**: `ease-out` for entrances, `ease-in` for exits, `ease-in-out` for in-place transitions.
- **Duration** 100–300 ms for UI animation; 0 ms when `prefers-reduced-motion: reduce`.

## 8. Icons

- **One icon set per project.** [Lucide](https://lucide.dev) is the modern default.
- **`aria-hidden="true"` on decorative icons.** **`aria-label` on icon-only buttons.**
- **SVG sprites or per-icon components**, never icon fonts. Fonts cause FOIT and a11y issues.
- **Don't mix icon sets** — visual inconsistency reads as instability.

## 9. Internationalization (when in scope)

- **`<html lang="...">`** always set, even for English-only apps.
- **All copy through a translation function** if i18n is on the roadmap — `t("user.greeting")` even before there's a second language.
- **Directionality:** RTL via `dir="rtl"` and CSS logical properties (`margin-inline-start` not `margin-left`). Tailwind 4's logical-property utilities cover this.
- **Date / number / currency formatting** via `Intl.DateTimeFormat`, `Intl.NumberFormat`.

## 10. Testing accessibility

- **`axe-core`** integrated into Vitest tests + Playwright e2e. Zero WCAG 2.2 AA violations before merge.
- **Manual keyboard pass** on every new component — tab through, activate every control, no mouse.
- **Screen reader pass** on critical flows — NVDA or VoiceOver.
- **Color contrast checker** for every design token decision.
- **Lighthouse a11y score** ≥ 95 in CI. Lighthouse misses things axe catches and vice versa — run both.

Test scaffolds (Vitest + Playwright) in [RECIPES §5](RECIPES.md#5-accessibility-testing-setup).

## 11. Design system maturity ladder

Where a project sits informs how much investment is justified. Five levels from ad-hoc Tailwind to a documented system with visual regression tests — full ladder in [RECIPES §4](RECIPES.md#4-design-system-maturity-ladder).

- **Start at Level 1** (shared primitives in `components/ui/`) for any non-throwaway project.
- **Climb to Level 2** (centralized tokens) when more than one developer touches styles.
- **Level 4** (Storybook + Chromatic) earns its place when there's a real design system team or many product teams consuming the same components.

## 12. Cross-skill ties

- [react-architect](../../frameworks/react-architect/SKILL.md) — client component patterns, hooks, state. This skill is what they render.
- [nextjs-architect](../../frameworks/nextjs-architect/SKILL.md) — server-component shells, server actions, image / font / metadata APIs.
- [rest-api-architect §7](../../protocols/rest-api-architect/SKILL.md#7-error-contracts--rfc-9457-problem-details) — error contracts the UI consumes; correlation IDs surfaced in error states.
- [security-reviewer](../../quality/security-reviewer/SKILL.md) — security headers (CSP), no stack traces in error UI, no PII in URLs.
- [observability-architect §5](../../infra/observability-architect/SKILL.md#5-correlation) — correlation IDs visible in the UI so support can match logs.
- [logic-cleaner](../../refactoring/logic-cleaner/SKILL.md) / [code-design-refactor](../../refactoring/code-design-refactor/SKILL.md) — same rules apply to component code as any other code.
