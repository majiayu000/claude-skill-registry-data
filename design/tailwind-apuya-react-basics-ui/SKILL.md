---
name: tailwind
description: Writes and audits Tailwind CSS v4 in react-basics-ui — the CSS-first setup (@import "tailwindcss", @theme), the arbitrary-value-referencing-CSS-variable convention (bg-[color:var(--semantic-*)]), the cn() helper (clsx + tailwind-merge), and the co-located .styles.ts class-map pattern. Knows the v4 gotcha that tailwind.config.js is only loaded via @config and that named utilities are dead without it. Use when adding or changing Tailwind classes, building a component's styles, choosing between named utilities and arbitrary values, wiring design tokens into utilities, or auditing className usage. Triggers on "tailwind", "tailwindcss", "utility class", "className", "arbitrary value", "var(--semantic", "cn(", "clsx", "tailwind-merge", "twMerge", ".styles.ts", "@theme", "@config", "@apply", "tailwind.config", "responsive variant", "breakpoint", "dark mode tailwind", "hover:", "focus-visible:", "dead utility".
---

# Tailwind CSS (v4) — react-basics-ui Conventions

Write utility classes that resolve to the design-token system and survive the v4 config model. This skill owns **how Tailwind is used here**: the syntax convention, class composition, and where class strings live.

> Tokens themselves (the `--primitive-*` → `--semantic-*` funnel, dark-theme parity, when to add a token) are owned by [`design-systems`](../design-systems/SKILL.md). Presentational-component structure (prop APIs, variants, stories) is owned by [`component`](../component/SKILL.md). This skill is the **Tailwind layer** underneath both.

## Stack Assumptions

Tailwind **v4.1** via `@tailwindcss/postcss`, `clsx`, `tailwind-merge`. No `@apply`, no raw hex in class strings. `src/global.css` is the single stylesheet: it imports Tailwind itself and is also the published artifact (`dist/index.css`, exported as `react-basics-ui/styles.css`).

```
src/global.css       @import 'tailwindcss';
                     @theme { --breakpoint-* ; --animate-* }
                     :root { --primitive-* ; --semantic-* ; --component-* }
                     [data-theme="dark"] { … }  +  @keyframes
postcss.config.js    { '@tailwindcss/postcss': {}, autoprefixer: {} }
src/lib/cn.ts        cn() = twMerge(clsx(...))
**/*.styles.ts       co-located class-map constants (69 files)
src/components/shared/styles/   reusable class-string fragments (FOCUS_RING, …)
tsup.config.ts       builds JS + emits global.css → dist/index.css
```

---

## The v4 config model — and the live gotcha

Tailwind v4 is **CSS-first**. There are two ways to configure the theme, and this library deliberately uses only one:

| Mechanism | Lives in | Loaded? | Holds |
|---|---|---|---|
| `@theme { … }` | `src/global.css` | **Always** (it's CSS) | `--breakpoint-*`, `--animate-*` |
| `tailwind.config.js` | *(deleted)* | — | — |

> ⚠️ **v4 does not auto-detect `tailwind.config.js`.** It is loaded **only** if a CSS file contains `@config`.

There is **no `tailwind.config.js`** in this repo. One existed and was removed: no stylesheet declared `@config`, so it was never loaded — deleting it produced byte-identical `dist/index.css` and `dist/index.js`. If you are tempted to add one back, remember it does nothing until a stylesheet declares `@config`.

Dead utilities are dangerous precisely because they look fine: `body` sets `color: var(--semantic-text-primary)`, so a dead `text-primary` is invisible, while a dead `text-error` renders in ordinary text colour instead of red. Nothing warns you.

### The convention here — configure in CSS, not in the JS config

Anything Tailwind must generate goes in the `@theme` block of `src/global.css`, where it is guaranteed to load:

```css
/* src/global.css */
@import 'tailwindcss';

@theme {
  --breakpoint-md: 640px;
  /* A --animate-* entry is what generates the animate-<name> utility. */
  --animate-skeleton-wave: skeleton-wave var(--component-skeleton-duration) ease-in-out infinite;
}
```

Everything else reaches tokens through **arbitrary values** (below), which need no config at all.

> **Do not reintroduce a JS config.** The old one was deleted precisely because it could never take effect, and wiring `@config` would switch on ~400 dormant classes at once — a large, untested visual change. If a named utility is genuinely wanted, add it to `@theme` instead.

---

## Reaching a token from a class string

### Arbitrary value referencing the CSS variable — the convention here

This is how essentially every component in the library is styled. It works without any config, and reaches semantic vars that have no named mapping. **Always include the type hint** (`color:` / `length:`) so v4 parses it correctly.

```tsx
className="bg-[color:var(--semantic-brand-secondary-default)] h-[length:var(--semantic-height-default)] gap-[length:var(--semantic-space-compact)] rounded-[length:var(--semantic-radius-md)]"
```

| Bracket form | When |
|---|---|
| `bg-[color:var(--semantic-…)]` | any color property (bg, text, border, ring, fill) — `color:` hint required |
| `h-[length:var(--semantic-…)]`, `gap-[length:var(--semantic-…)]`, `size-[length:var(--semantic-…)]` | dimensions/spacing/radius — `length:` hint required |
| `duration-[var(--semantic-…)]`, `opacity-[var(--semantic-…)]`, `ring-[var(--semantic-…)]` | unitless / token-typed values — bare `var()` |

Tailwind's **built-in** utilities (`flex`, `truncate`, `animate-pulse`, `sm:`, `hover:`) are unaffected and are used freely. Only named utilities that would have come from a JS config are unavailable — there is no such config.

**Never** write a raw value in brackets to skip the token system:

```tsx
// BAD — raw value, bypasses the funnel
className="bg-[#fcb711] h-[36px] rounded-[8px]"
// GOOD — token via arbitrary value
className="bg-[color:var(--semantic-brand-secondary-default)] h-[length:var(--semantic-height-default)]"
```

---

## Class composition — `cn()`

All conditional/merged class strings go through `cn()` from `@/lib/cn`:

```ts
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));   // clsx flattens conditionals; twMerge dedupes conflicts
}
```

- **`clsx`** flattens arrays, objects, and falsy conditionals: `cn('px-2', isActive && 'bg-secondary')`.
- **`twMerge`** resolves Tailwind conflicts so the *last* wins: `cn('p-2', 'p-4')` → `'p-4'`. This is why `className` overrides from props compose correctly — pass the prop's `className` **last** to `cn()`.

```tsx
const classes = cn(BASE_CLASSES, SIZE_STYLES[size], VARIANT_STYLES[variant], block && BLOCK_CLASSES, className);
```

> ⚠️ `tailwind-merge` only understands **default-named** utilities and known arbitrary patterns. It will *not* dedupe two conflicting `bg-[color:var(--a)]` vs `bg-[color:var(--b)]` reliably across every property — it does for common ones, but don't rely on merge to resolve two arbitrary color values; pick one upstream.

---

## Where class strings live — the `.styles.ts` pattern

A component with variants/sizes does **not** inline long class strings in JSX. It extracts them into a co-located `<Component>.styles.ts` (this library has 69 of them) and composes with `cn()`.

```ts
// Button.styles.ts
import { FOCUS_RING } from '@/components/shared/styles/focus.styles';
import { DISABLED_CLASSES } from '@/components/shared/styles/disabled.styles';
import { TRANSITION_COLORS } from '@/components/shared/styles/transitions.styles';

export const BASE_CLASSES = `inline-flex items-center justify-center rounded-[length:var(--semantic-radius-md)] ${TRANSITION_COLORS} ${FOCUS_RING} ${DISABLED_CLASSES}`;

export const SIZE_STYLES = {
  small: 'h-[length:var(--semantic-height-default)]',
  default: 'h-[length:var(--semantic-height-medium)]',
  large: 'h-[length:var(--semantic-height-large)]',
} as const;

export const VARIANT_STYLES = {
  primary: 'bg-[color:var(--semantic-brand-secondary-default)] text-[color:var(--semantic-accent-sand-default)] hover:bg-[color:var(--semantic-brand-secondary-hover)] …',
  // …
} as const;
```

Rules:

- **Variant/size maps are `Record<Variant, string>` objects with `as const`** — never a chain of ternaries. The component indexes `VARIANT_STYLES[variant]`.
- **Compose, don't repeat.** Cross-component fragments live in `src/components/shared/styles/` and are concatenated into `BASE_CLASSES`:

| Fragment | Constant | Covers |
|---|---|---|
| `focus.styles.ts` | `FOCUS_RING`, `FOCUS_RING_TIGHT` | focus-visible ring via tokens |
| `disabled.styles.ts` | `DISABLED_CLASSES` | disabled cursor + opacity |
| `transitions.styles.ts` | `TRANSITION_COLORS`, `TRANSITION_ALL`, … | transition + token duration |
| `statusColors.styles.ts`, `textColors.styles.ts`, `spacing.styles.ts`, `iconSizes.styles.ts`, `floating.styles.ts` | various | reusable token-bound class sets |

- **`.styles.ts` files are tested.** Each shared fragment has a co-located `.test.ts` asserting the class string. New shared fragments get one.
- **Inline classes are fine** for one-off layout in a `.tsx` (`'inline-flex shrink-0 items-center'`). Extract to `.styles.ts` once there's a variant axis or the string is reused.

For how the extracted styles then bind to a component's prop API and variant matrix, see [`component`](../component/SKILL.md).

---

## Responsive, state, and dark variants

- **Breakpoints** are the only `@theme` customization: `xs 375 · sm 480 · md 640 · lg 768 · xl 1024 · 2xl 1440`. Use `md:`, `lg:` as normal. These differ from Tailwind defaults — don't assume `sm` = 640.
- **State variants** (`hover:`, `focus-visible:`, `active:`, `disabled:`, `aria-disabled:`, `has-[:focus-visible]:`) compose with the arbitrary syntax: `hover:bg-[color:var(--semantic-surface-hover)]`. This is how every `VARIANT_STYLES` entry is built.
- **Dark mode** is handled in the **token layer**, not in utilities. Semantic vars are redefined under `[data-theme="dark"]` in `global.css`; a single `bg-[color:var(--semantic-surface-base)]` follows the theme automatically. **Do not** write `dark:` variants in components — that splits the source of truth. See [`design-systems`](../design-systems/SKILL.md).

---

## Audits

Run from the repo root. Each is a grep that surfaces a specific drift.

### 1. Raw values in class strings (token bypass)

```bash
grep -rnE "(bg|text|border|ring|fill|h|w|gap|p|px|py|m|rounded|size|shadow)-\[#" src --include="*.ts" --include="*.tsx"
grep -rnE "(h|w|gap|p|px|py|m|rounded|size)-\[[0-9]+(px|rem|em)\]" src --include="*.ts" --include="*.tsx"
```

Each hit: replace with a named utility or a `var(--semantic-*)` arbitrary value. If no token exists, propose one (see `design-systems`) — don't hardcode.

### 2. Dead named utilities

```bash
# Confirm the config is still unloaded (it should be).
grep -rn "@config" src/*.css || echo "no @config → correct; there is no JS config to load"
grep -rnoE "\b(bg|text|border)-(primary|secondary|success|warning|error|info)(-[a-z]+)?\b" src --include="*.ts" --include="*.tsx" | sort
```

Every match is a no-op class that emits nothing. Convert each to the arbitrary `var()` form — do **not** wire `@config` to make them work.

### 3. Missing type hint in arbitrary color/length values

```bash
# color properties missing the color: hint
grep -rnE "(bg|text|border|ring|fill)-\[var\(--semantic" src --include="*.ts" --include="*.tsx"
# dimension properties missing the length: hint
grep -rnE "(h|w|gap|size|min-[hw]|max-[hw])-\[var\(--semantic" src --include="*.ts" --include="*.tsx"
```

Hits parse unreliably in v4. Add `color:` / `length:` inside the brackets.

### 4. `dark:` variants in components (should be token-driven)

```bash
grep -rn "dark:" src/components src/features --include="*.tsx"
```

Each hit moves the difference into a dark-theme token override in `global.css`.

### 5. `@apply` (banned here)

```bash
grep -rn "@apply" src --include="*.css"
```

Expected: zero. `@apply` re-hardcodes utilities in CSS and defeats `twMerge`. Compose with `cn()` + `.styles.ts` instead.

### 6. Long inline class strings that should be a `.styles.ts`

```bash
# className literals with a variant-shaped conditional or 8+ utilities inline
grep -rnE "className=\{?[\"'\`][^\"'\`]{120,}" src/components --include="*.tsx"
```

Each hit is a candidate for extraction into `<Component>.styles.ts`.

---

## Decision flowchart

```
Need to style an element
  │
  ├─ Is there a SEMANTIC token for this intent?  (design-systems owns this)
  │     └─ NO → add the token first (primitive → semantic → dark override). Don't hardcode.
  │
  ├─ Is there a built-in Tailwind utility or a `@theme` entry for it?
  │     └─ YES → use the named utility:  text-error  bg-secondary  rounded-md
  │
  ├─ No named mapping (or reaching a var with no map)?
  │     └─ arbitrary value WITH type hint:  bg-[color:var(--semantic-…)]  h-[length:var(--semantic-…)]
  │
  ├─ Conditional / merged / prop-overridable classes?
  │     └─ compose through cn(...) — pass incoming `className` LAST
  │
  ├─ Variant or size axis, or reused string?
  │     └─ extract to <Component>.styles.ts as a Record<…, string> `as const`; reuse shared/styles/* fragments
  │
  └─ Dark-mode difference?
        └─ NOT a `dark:` utility — redefine the semantic var under the dark theme in global.css
```

---

## Common mistakes

| Mistake | Why it's wrong | Fix |
|---|---|---|
| `bg-[#fcb711]`, `h-[36px]` | Bypasses the token funnel | `var(--semantic-*)` arbitrary value or named utility |
| `text-error` | Dead class — emits nothing, renders inherited colour | `text-[color:var(--semantic-status-error-default)]` |
| `bg-[var(--semantic-x)]` (no `color:`) | v4 may mis-parse the type | `bg-[color:var(--semantic-x)]` |
| `dark:bg-…` in a component | Splits theme source of truth | Dark override on the token in `global.css` |
| `@apply btn-base` in CSS | Re-hardcodes utilities, breaks `twMerge` | `BASE_CLASSES` string + `cn()` |
| Ternary chain of variant classes in JSX | Unreadable, untestable | `VARIANT_STYLES` record `as const` in `.styles.ts` |
| Passing `className` prop first to `cn()` | Consumer override loses to internal classes | Pass incoming `className` last |
| Assuming `sm:` = 640px | Here `sm` = 480px | Check the `@theme` breakpoints in `global.css` |
