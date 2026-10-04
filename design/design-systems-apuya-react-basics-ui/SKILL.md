---
name: design-systems
description: Guards react-basics-ui's design token system (primitive → semantic, with a legacy component tier) and the UI primitive component layer. Enforces no raw hex/rgb/px in components, components consuming semantic tokens only, dark-theme parity under [data-theme="dark"], and no dangling var() references. Use when adding or changing design tokens, building or reviewing primitive components, or auditing a codebase for hardcoded visual values. Triggers on "design token", "new token", "semantic token", "primitive component", "raw hex", "hardcoded color", "dark mode parity", "token audit", "css variable", "design system".
---

# Design Systems Engineer

Keep visual decisions flowing through the token system so colors, spacing, typography, and motion stay coherent and survive theme changes.

## The 3-tier funnel

A one-way funnel. Each tier may only reference tiers above it. Never backward.

| # | Tier | Lives in | References | Count | Example |
|---|------|----------|------------|-------|---------|
| 1 | **Primitive** | `src/global.css` `:root` | Raw values only | ~540 | `--primitive-color-gold-500: #fcb711` |
| 2 | **Semantic** | `src/global.css` `:root` + `[data-theme="dark"]` | Primitives only | ~513 | `--semantic-brand-primary-default: var(--primitive-color-gold-400)` |
| 3 | **Component** | `src/global.css` `:root` — **legacy** | Semantics only | ~1530 | `--component-navbar-bg: var(--semantic-surface-base)` |

```
1  Primitive   ← raw values, no var() refs
      ↓
2  Semantic    ← intent, has a dark-theme override
      ↓
   Components  ← consume tier 2 directly
```

**Components consume tier 2.** That is the rule in this library, and it differs
from the classic three-tier model: tier 3 is **legacy**, kept only because
`Navbar` and `Sidebar` still read from it. Do not add `--component-*` tokens, and
do not route new work through tier 3 — style against `--semantic-*` directly.

Components NEVER consume tier 1. Enforce via the primitive-leak audit below.

### The typed mirror — `src/tokens/index.ts`

Separate from the CSS tiers, `src/tokens/index.ts` exports typed objects
(`colors`, `spacing`, `radius`, `shadows`, `typography`, `animation`, `zIndex`)
whose values are `var(--semantic-*)` strings. It exists so consumers can reference
tokens from TypeScript (inline styles, props) with autocomplete instead of
retyping variable names.

It is a **mirror, not a tier** — it introduces no new values. A handful of its
entries still point at `--component-*` vars; those are legacy alongside tier 3.
When you add a semantic token, add it here too (step 4 of the checklist below).

## When to add a token

A new token is a permanent vocabulary entry — it costs a dark-theme override, a TS mirror entry, and mental model. Reuse first.

- Same raw value used ≥ 2 times → tokenize as semantic.
- Single use but intent is brand-coupled or theme-sensitive → tokenize as semantic.
- Truly one-off (e.g. a duration unique to one component) → inline with a comment explaining why.

## Adding a new semantic token — checklist

Do all of these in one change:

1. **Primitive.** Pick or add the primitive holding the raw value.
2. **Semantic.** Add the semantic token referencing the primitive via `var()`.
3. **Dark override.** Redefine the semantic token inside the `[data-theme="dark"]` block at the bottom of `src/global.css`. Skip only if theme-invariant (a size, duration, or font family); leave a comment stating the skip.
4. **TS mirror.** Add to `src/tokens/index.ts` so consumers get autocomplete.
5. **Consumer.** Use it. Unused tokens decay.

Skipping step 3 is the most common silent failure — light theme still works and the dark theme silently inherits the light value.

> **This library keys dark mode off `[data-theme="dark"]`, not `prefers-color-scheme`.** There is no `@media (prefers-color-scheme: dark)` block in `global.css`; `ThemeProvider` sets the attribute. Adding an override to a media query would do nothing.

## Component tokens (tier 3) — legacy, do not extend

`--component-*` variables are an earlier layer that gave each component its own
named variables (`--component-badge-font-size-small`). The library has moved off
it: every component except `Navbar` and `Sidebar` now styles against `--semantic-*`
directly, which is why ~1530 tier-3 tokens remain defined but almost none are read.

- **Adding a new component:** consume semantic tokens. Do not create `--component-*` entries.
- **Touching `Navbar` / `Sidebar`:** migrating them to semantic tokens is welcome, but it is a visual change — verify against both themes rather than folding it into unrelated work.
- **Deleting unused tier-3 tokens** is safe in principle but noisy; only do it as a deliberate, isolated cleanup.

If a component genuinely needs a value with no semantic equivalent, add a
**semantic** token for it (full checklist above) rather than reviving tier 3.

## Primitive components

A primitive is a reusable, domain-free UI building block (Button, Input, Dialog, Toast, Tabs, etc.).

### Must contain

- `var(--semantic-*)` references via CSS or a typed token import.
- One clear public API; sub-parts live alongside with sub-component naming.
- A11y baseline: keyboard reachable, visible focus ring, correct ARIA role.
- Both light and dark behavior via tokens — never theme-detect with JS.

### Must NOT contain

- Raw hex, rgb, hsl, or px values.
- `var(--primitive-*)` references — must route through the semantic tier.
- Feature-domain types or models.
- Data-layer imports (query clients, routers, fetch).
- Business rules — primitives don't know *why* they're used.

## Audits

Run in order, from the repo root.

### 1. Hardcoded visual values

```bash
grep -rn "color: #\|background: #\|background-color: #" src/components
grep -rnE "(bg|text|border|h|w|gap|p|rounded)-\[#" src/components
```

Each hit: replace with a token, or document why this value is local.

### 2. Primitive-tier leaks

```bash
grep -rln "var(--primitive-" src/components
```

Any hit is a bug — the component is skipping the semantic tier and will not respond to theme changes.

### 3. Missing dark-theme overrides

For each colour token in the `:root` semantic block, confirm the `[data-theme="dark"]` block redefines it (or that it is theme-invariant). Size, spacing, duration, and z-index tokens legitimately have no dark override.

### 4. Dangling references

Every `var(--…)` a component reads must be defined, or the whole declaration is
silently dropped — no console warning, no build error. This has produced real
bugs here (see `Divider`, which referenced a `--semantic-spacing-*` family that
never existed).

```bash
# every token defined
grep -oE -- '--[a-zA-Z0-9-]+[[:space:]]*:' src/global.css | sed -E 's/[[:space:]]*:$//' | sort -u > /tmp/def.txt
# every token referenced by source (excluding tests/stories)
find src -type f \( -name '*.ts' -o -name '*.tsx' \) ! -name '*.test.*' ! -name '*.stories.*' -print0 \
  | xargs -0 grep -hoE -- 'var\([[:space:]]*--[a-zA-Z0-9-]+' | sed -E 's/var\([[:space:]]*//' | sort -u > /tmp/used.txt
comm -23 /tmp/used.txt /tmp/def.txt
```

Expect only two kinds of survivor: prefixes built by template literal
(`var(--semantic-space-${size})`) and vars the component sets itself
(`--table-pad-left`). Resolve each dynamic prefix by hand against its value map.

> **Gap:** there is no automated token-resolution test in this project. The audit
> above is the substitute. Adding `src/tokens/tokens.resolution.test.ts` to assert
> each semantic token resolves to its expected primitive would make it enforceable.

## Decision flowchart

```
"I need a color / spacing / radius / duration for X"
  │
  ├─ Does a semantic token already capture this intent?
  │    └─ YES → use it. Done.
  │
  ├─ Does a primitive value already exist with this raw value?
  │    └─ YES → add a semantic token referencing it (full checklist).
  │
  └─ Neither exists.
       └─ Add primitive → semantic → dark override → TS mirror → consumer.
```
