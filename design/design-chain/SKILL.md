---
name: design-chain
description: Audit and enforce the five-layer design chain (tokens → Tailwind → primitives → sections → pages) across all components and pages. Finds hardcoded values, layer violations, broken mode parity, and missing primitives.
user-invocable: true
allowed-tools: Read, Edit, Grep, Glob, Bash, Agent, TodoWrite
---

Audit and enforce the five-layer design chain across components and pages: $ARGUMENTS

If no target is provided, audit the entire codebase. If a specific file, directory, or layer is given, scope the audit accordingly.

**Supported arguments:**
- `(no args)` — full codebase audit across all five layers
- `src/components/hero/` — audit a specific component directory
- `src/app/(public)/about/` — audit a specific page
- `L1` / `L2` / `L3` / `L4` / `L5` — audit a single layer
- `--fix` — auto-fix violations (default is report-only)

## Before Starting

Read these files to establish the design chain ground truth:

1. `_docs/_build/design/DESIGN_CHARTER.md` — the chain rules and anti-patterns
2. `src/app/globals.css` — L1 token definitions (`:root` and `.dark`)
3. `tailwind.config.ts` — L2 utility mappings
4. `_docs/_build/_prompts/design/COLOR_PALETTE.md` — canonical color reference

## The Five-Layer Design Chain

```
L1  Tokens        globals.css          CSS custom properties (HSL)
    ↓
L2  Tailwind      tailwind.config.ts   Utility classes mapped to tokens
    ↓
L3  Primitives    src/components/ui/   Radix + CVA components
    ↓
L4  Sections      src/components/*/    Composed feature sections
    ↓
L5  Pages         src/app/(public)/    Route-level composition
```

**Core rule:** Types flow downstream only. Fix at the source layer.

## Audit Dimensions

### D1 — Hardcoded Values (L1/L2 violations)

Search for values that should be tokens or utilities:

**Colors:**
```
# Hardcoded hex colors
grep -rn '#[0-9a-fA-F]{3,8}' src/components/ src/app/ --include='*.tsx'

# Tailwind default palette (should be semantic)
grep -rn 'bg-\(blue\|red\|green\|gray\|slate\|zinc\|stone\|neutral\|amber\|yellow\|indigo\|purple\|pink\|rose\|orange\|teal\|cyan\|emerald\|violet\|fuchsia\|lime\|sky\)-' src/components/ src/app/ --include='*.tsx'

# Inline style colors
grep -rn 'color:\s*[#rgb]' src/components/ src/app/ --include='*.tsx'
grep -rn "style={{.*color" src/components/ src/app/ --include='*.tsx'
```

**Exempt:** SVG `stroke`/`fill` using `hsl(var(--token))` or `currentColor` are allowed. Colors in `globals.css` token definitions are allowed.

**Fonts:**
```
# Hardcoded font-family
grep -rn 'font-family' src/components/ src/app/ --include='*.tsx'
grep -rn "fontFamily" src/components/ src/app/ --include='*.tsx'
```

**Radius:**
```
# Hardcoded border-radius
grep -rn 'rounded-\(full\|none\|xl\|2xl\|3xl\)' src/components/ --include='*.tsx'
```
Note: `rounded-full` on avatars/badges is acceptable. `rounded-2xl` and above should use `rounded-lg` (the token) unless explicitly needed.

**Spacing:**
```
# Magic number padding/margin (not from scale)
grep -rn 'p[xytrbl]\?-\[' src/components/ --include='*.tsx'
grep -rn 'm[xytrbl]\?-\[' src/components/ --include='*.tsx'
```
Arbitrary values `p-[7px]` etc. should use the Tailwind spacing scale.

**Motion:**
```
# Hardcoded durations
grep -rn 'duration-\(75\|100\|150\|200\|300\|500\|700\|1000\)' src/components/ --include='*.tsx'
```
Should use `duration-fast`, `duration-normal`, or `duration-slow` from L2.

### D2 — Primitive Bypass (L3 violations)

Search for raw HTML that should use L3 primitives:

```
# Raw buttons (should be <Button>)
grep -rn '<button\b' src/components/ src/app/ --include='*.tsx' | grep -v 'components/ui/'

# Raw inputs (should be <Input>)
grep -rn '<input\b' src/components/ src/app/ --include='*.tsx' | grep -v 'components/ui/'

# Raw selects (should be Select primitive if one exists)
grep -rn '<select\b' src/components/ src/app/ --include='*.tsx' | grep -v 'components/ui/'
```

**Exempt:** Inputs in forms where the primitive doesn't support the needed type (e.g., `type="file"`). The HeroSectionVariant's read-only input is a known pattern.

### D3 — Layer Import Violations

Check that imports respect the downstream-only rule:

```
# L3 (ui/) importing from L4 (sections)
grep -rn "from.*@/components/" src/components/ui/ --include='*.tsx' | grep -v '/ui/'

# L4 sections importing from other L4 sections (sections are peers)
# This requires checking each section directory doesn't import from sibling sections

# L5 pages importing L3 primitives directly (should use L4 sections)
grep -rn "from.*@/components/ui/" src/app/ --include='*.tsx'
```

**Note:** Pages importing primitives directly is a soft warning, not a hard violation — acceptable for simple compositions, but prefer section encapsulation.

### D4 — Dark Mode Parity

Check that components work in both modes:

```
# Components with dark: prefix usage (verify they have matching light defaults)
grep -rn 'dark:' src/components/ --include='*.tsx' -l
```

For each file with `dark:` classes, verify:
- Every `dark:bg-*` has a corresponding default `bg-*`
- `dark:hidden` / `hidden dark:block` pairs show different content appropriately
- Typography mode shifts are intentional (italic ↔ bold, normal ↔ uppercase)
- No `dark:text-[hex]` or `dark:bg-[hex]` — colors should auto-switch via tokens

### D5 — Tenant String Hardcoding

Search for tenant-specific strings that should come from `tenant.config.ts`:

```
# Hardcoded tenant name
grep -rn '"Brad Brisco"' src/components/ src/app/ --include='*.tsx'
grep -rn "'Brad Brisco'" src/components/ src/app/ --include='*.tsx'

# Hardcoded tenant-specific phrases
grep -rn '"The Soul of"' src/components/ --include='*.tsx'
grep -rn '"neighborhood"' src/components/ --include='*.tsx' -i
grep -rn '"ReNeighbor"' src/components/ --include='*.tsx'
grep -rn '"The Curator"' src/components/ --include='*.tsx'
grep -rn '"Explore Monographs"' src/components/ --include='*.tsx'
```

These should read from `useTenant()` or `tenantConfig`.

### D6 — Section Structure

For each section component, verify:

1. **Wrapping:** Uses `<section>` with `w-full` and vertical padding
2. **Container:** Content constrained with `container mx-auto px-4 md:px-8` or `max-w-*`
3. **Animation:** Uses `motion/react` for entrance animations (optional but preferred)
4. **Responsiveness:** Has mobile/tablet/desktop breakpoints
5. **Semantic HTML:** Uses appropriate heading hierarchy, `<main>`, `<nav>`, etc.

## Fixing Protocol

When `--fix` is provided:

### L1 fixes (tokens)
- Edit `globals.css` — both `:root` and `.dark` blocks
- Never change primary brand colors without user confirmation

### L2 fixes (Tailwind)
- Edit `tailwind.config.ts` to add missing mappings
- Add new tokens to globals.css first, then map

### L3 fixes (primitives)
- Do NOT modify `src/components/ui/*` files for section-specific needs
- Instead, use `className` overrides at the call site

### L4 fixes (sections)
- Replace hardcoded colors with semantic utilities
- Replace raw HTML with L3 primitives
- Replace hardcoded strings with tenant config reads
- Add missing responsive breakpoints
- Add missing dark mode handling

### L5 fixes (pages)
- Move inline styling into sections
- Add missing feature flag guards
- Ensure pages are Server Components (no `"use client"`)

## Output Format

```markdown
## Design Chain Audit — [target]

### Summary
| Layer | Files Scanned | Violations | Fixed |
|-------|--------------|------------|-------|
| L1 Tokens | — | — | — |
| L2 Tailwind | — | — | — |
| L3 Primitives | — | — | — |
| L4 Sections | — | — | — |
| L5 Pages | — | — | — |
| **Total** | — | — | — |

### Violations

#### D1 — Hardcoded Values
| File | Line | Violation | Current | Recommended |
|------|------|-----------|---------|-------------|

#### D2 — Primitive Bypass
| File | Line | Element | Should Use |
|------|------|---------|------------|

#### D3 — Layer Import Violations
| File | Line | Import | Violation |
|------|------|--------|-----------|

#### D4 — Dark Mode Parity
| File | Issue | Missing |
|------|-------|---------|

#### D5 — Tenant String Hardcoding
| File | Line | Hardcoded String | Should Use |
|------|------|-----------------|------------|

#### D6 — Section Structure
| Section | Wrapper | Container | Animation | Responsive | Semantic |
|---------|---------|-----------|-----------|------------|----------|
```

## Rules

- **Report first, fix second.** Always present the full audit before making changes (unless `--fix` is passed).
- **Fix at the source.** If a color is wrong at L1, don't patch it at L4 with a `dark:` override.
- **Downstream only.** Never make a lower layer depend on a higher one.
- **Do not modify `src/components/ui/*`** for section-specific needs. Override via `className`.
- **Preserve Stitch fidelity.** Token values map from Material Design 3 via Stitch — don't invent new tokens without checking the MD3 mapping.
- **Both modes.** Every change must be verified in both light and dark mode.
- **Tenant portability.** Every hardcoded string is a portability violation.
- **Use the charter.** Refer to `_docs/_build/design/DESIGN_CHARTER.md` for anti-patterns and validation checklist.
