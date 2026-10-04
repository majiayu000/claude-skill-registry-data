---
name: design-chain-audit
description: Unified design chain audit for Movemental — flushes drift across all 5 layers (Stitch → tokens → primitives → components → layouts) covering color, typography, Tailwind hygiene, pattern, a11y, and interaction fidelity against the "Warm Scholarly Authority" design system. Use before shipping any UI or after a large build sprint.
disable-model-invocation: true
---

**Cursor:** Read this skill when the user asks for a design audit, design chain check, token audit, color audit, typography audit, Tailwind cleanup, or "flush drift." This is the **unified** audit — it supersedes running `design-audit`, `color-audit`, `tailwind-cleanup`, and `typography-polish` individually by combining all four with chain-specific rules.

## Before starting

1. Read the design chain reference:
   `_docs/_build/_stitch/_design-system/DESIGN-CHAIN.md`
2. Read the runtime tokens:
   `src/app/globals.css` (the `@theme { }` block)
3. Identify the target scope from the user (specific files, a route, or "full sweep").

If the user says "flush" or "flush drift," run all 5 layers as a full sweep across `src/`.

---

## Layer 1 — Token Drift

**Goal:** No hardcoded colors exist where semantic tokens should be used.

### Checks

```bash
# Hardcoded hex in className
grep -rn "bg-\[#" src/components src/app --include="*.tsx"
grep -rn "text-\[#" src/components src/app --include="*.tsx"
grep -rn "border-\[#" src/components src/app --include="*.tsx"
grep -rn "from-\[#" src/components src/app --include="*.tsx"

# Tailwind palette colors (should be semantic tokens)
grep -rnE "(bg|text|border|ring|divide)-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-[0-9]" src/components src/app --include="*.tsx"

# Raw hex/rgb in inline style
grep -rnE "style=.*#[0-9a-fA-F]{3,8}" src/components src/app --include="*.tsx"
grep -rnE "style=.*rgb" src/components src/app --include="*.tsx"
```

### Severity

- **CRITICAL** if found in dashboard/shell components (these must be 100% token-aligned)
- **HIGH** if found in editor components (except known dark-theme exceptions)
- **INFO** if in known exception list (see DESIGN-CHAIN.md "Known Intentional Exceptions")

### Token replacement map

When fixing, use this map (not exhaustive — refer to DESIGN-CHAIN.md Layer 1 tables):

| Hardcoded | Replace with |
|-----------|-------------|
| `bg-[#fbf9f4]` | `bg-surface` |
| `bg-[#ffffff]` | `bg-surface-container-lowest` |
| `bg-[#f5f3ee]` | `bg-surface-container-low` |
| `bg-[#f0eee9]` | `bg-surface-container` |
| `bg-[#eae8e3]` | `bg-surface-container-high` |
| `bg-[#37285e]` | `bg-tertiary-container` |
| `bg-[#14006a]` | `bg-primary` |
| `bg-[#260b9e]` | `bg-primary-container` |
| `bg-[#e3dfff]` | `bg-primary-fixed` |
| `text-[#1b1c19]` / `text-[#121311]` | `text-on-surface` |
| `text-[#352f3d]` / `text-[#4c4451]` | `text-on-surface-variant` |
| `text-[#a290ce]` | `text-on-tertiary-container` |
| `text-[#14006a]` | `text-primary` |
| `text-[#938bff]` | `text-on-primary-container` |
| `border-[#7d7483]` / `border-[#5f5668]` | `border-outline` |
| `border-[#cec3d3]` / `border-[#b5a8c4]` | `border-outline-variant` |
| `from-[#14006a]` | `from-primary` |
| `to-[#260b9e]` | `to-primary-container` |
| `text-black` | `text-on-surface` |
| `bg-white` | `bg-surface-container-lowest` |
| `text-white` (on dark bg) | `text-on-tertiary` or `text-on-primary` (context-dependent) |

### ve-* scope check

Confirm `ve-*` tokens appear **only** in:
- `src/components/video-editor/`
- `src/components/ai-suite/Audiobook*`
- `src/app/(editor)/video/`

Flag any `ve-*` usage on cream dashboard surfaces.

---

## Layer 2 — Primitive Drift

**Goal:** Design system rules are encoded once in `src/components/ui/` and composed
everywhere else — not reimplemented.

### Checks

```bash
# Raw <button> outside ui/ (should use Button primitive)
grep -rn "<button" src/components src/app --include="*.tsx" | grep -v "components/ui/" | grep -v "type=\"button\""

# Raw <input> outside ui/ (should use Input primitive)
grep -rn '<input\b' src/components src/app --include="*.tsx" | grep -v "components/ui/"

# Inline gradient reimplementation (should use Button variant="primary" or documented pattern)
grep -rn "from-primary to-primary-container" src/components src/app --include="*.tsx" | grep -v "components/ui/"

# Inline status color mapping (should use StatusChip)
grep -rnE "bg-(secondary-container|primary-fixed|tertiary-fixed|error-container).*text-(on-secondary-container|on-primary-fixed|on-tertiary-fixed|on-error-container)" src/ --include="*.tsx" | grep -v "components/ui/"
```

### Evaluation

Not every raw `<button>` is a violation — toggle buttons, icon-only triggers, and
specialized controls may intentionally skip the primitive. But they must still:
- Use semantic token colors (not raw hex)
- Have focus-visible indicators
- Have accessible names

Report each hit with a **USE PRIMITIVE** or **ACCEPTABLE OVERRIDE** judgment.

---

## Layer 3 — Component & Style Drift

This layer combines the checks from `color-audit`, `tailwind-cleanup`, and `design-audit`.

### 3a. Color & contrast

Read the `@theme` block and verify:

- [ ] Every surface/text pair maintains WCAG AA contrast:
  - Normal text < 18px: **4.5:1** minimum
  - Large text: **3:1** minimum
  - UI controls: **3:1** minimum
- [ ] Critical pairs to check:
  - `on-surface` (#121311) on `surface` (#fbf9f4) — must pass
  - `on-surface-variant` (#352f3d) on `surface` (#fbf9f4) — must pass
  - `on-tertiary-container` (#a290ce) on `tertiary-container` (#37285e) — must pass
  - `on-primary` (#ffffff) on `primary` (#14006a) — must pass
  - `on-primary-container` (#938bff) on `primary-container` (#260b9e) — must pass
  - `on-error-container` (#93000a) on `error-container` (#ffdad6) — must pass
  - `on-lilac` (#311c7e) on `lilac` (#c9beff) — must pass (documented as 7.7:1)
- [ ] Error distinguishable from primary (hue difference, not just lightness)
- [ ] No opacity modifiers pushing text below contrast thresholds

### 3b. Typography

- [ ] **Page titles:** `font-serif` (Newsreader), `text-4xl`+, `font-medium`+, `tracking-tight`
- [ ] **Section titles:** `font-serif`, `text-2xl`+, `font-semibold`
- [ ] **Form labels:** `font-display` or `font-sans`, `text-xs`, `uppercase`, `tracking-wider`
- [ ] **Nav section headers:** `font-sans`, `text-xs`, `uppercase`, `tracking-tight`–`tracking-widest`
- [ ] **Body copy:** `font-sans`, `text-base` (not `text-sm` as default)
- [ ] **Stat numbers:** `font-serif`, `tabular-nums` where alignment matters
- [ ] No `font-serif` used for body paragraphs
- [ ] No `font-sans` used for page-level headlines
- [ ] Long-form prose: `~65ch` max measure, `leading-relaxed` (1.6–1.8 line-height)
- [ ] No orphaned headings (heading at bottom of viewport without content below)

### 3c. Pattern & layout

- [ ] **No-Line Rule:** No `border-b`, `border-t`, `<hr>` between content sections — use background tier shifts
  - Exception: `border-t border-outline-variant/15` as ghost border is acceptable
  - Exception: Input bottom borders are part of the input pattern
- [ ] Consistent spacing: Tailwind scale, no arbitrary spacing where scale suffices
- [ ] Responsive: mobile (~375px), tablet (~768px), desktop (~1280px)
- [ ] No horizontal scroll on any breakpoint
- [ ] Content sections logically grouped
- [ ] Dashboard grids: `grid-cols-12 gap-6`
- [ ] Page padding: `p-8`
- [ ] Content max-width: `max-w-7xl` (dashboard) or `max-w-5xl`–`max-w-6xl` (editors)

### 3d. Roundness

```bash
# Find over-rounded elements (max is rounded-md)
grep -rnE "rounded-(lg|xl|2xl|3xl)" src/components src/app --include="*.tsx"
```

- [ ] No `rounded-lg` or larger (except `rounded-full` for avatars/pills)
- [ ] CTAs use `rounded-sm` (precision-cut)
- [ ] Cards and modals use `rounded-md` maximum

### 3e. Shadows

- [ ] Floating elements use ambient shadow: `shadow-[0_20px_40px_rgba(27,28,25,0.06)]`
- [ ] No `shadow-lg` or `shadow-xl` on cards (use surface tier shifts instead)
- [ ] Shadow color derived from `on-surface`, not generic black

### 3f. Tailwind hygiene

- [ ] No `text-black` / `bg-white` where semantic tokens exist
- [ ] No absurdly long `className` strings (extract to `cn()` or component)
- [ ] No duplicate utilities in the same className
- [ ] `cn()` used for conditional class merging
- [ ] No raw `fetch()` in leaf UI components (use hooks/services)

---

## Layer 4 — Layout & Shell Drift

### Checks

- [ ] `AppSidebar` width matches `DASHBOARD_LEFT_NAV_EXPANDED_PX` (240px)
- [ ] `DashboardMainColumn` uses nav insets context for dynamic left margin
- [ ] `TopBar` is sticky, `h-14`, `z-50`, no bottom border
- [ ] Sidebar uses `bg-tertiary-container` (not a dark substitute)
- [ ] Active nav item has `bg-primary-fixed` left-edge vertical pill
- [ ] Footer border on sidebar uses `border-tertiary-fixed/30` (ghost, not solid)
- [ ] AI panel slides from right, uses frosted glass pattern
- [ ] Command palette opens with ⌘K, uses `surface-container-lowest` base
- [ ] Page scroll is on main content, not on body/sidebar

---

## Layer 5 — Interactions & Accessibility

### Checks

- [ ] Hover states: cream surfaces step up one tier; sidebar items use `hover:bg-tertiary-container/55`
- [ ] Focus visible on all interactive elements: `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary`
- [ ] Input focus: bottom border transitions `outline` → `primary`
- [ ] Button press: `active:scale-95` where used
- [ ] Transitions: `transition-colors` for color; `transition-all duration-150` for compound
- [ ] `prefers-reduced-motion` respected for animations
- [ ] Images have meaningful `alt` text (or aria decorative pattern)
- [ ] No color-only meaning (status uses text label + color)
- [ ] Keyboard: no focus traps
- [ ] Tap targets ≥ 44×44px for touch interfaces
- [ ] Icon-only controls have `aria-label` or accessible name
- [ ] Locked nav items (`pointer-events-none opacity-40`) have "Soon" badge for visual explanation

---

## Output format

```markdown
## Design Chain Audit: [target]

### Chain Health: X/5 layers passing

### Layer 1 — Token Drift
**Status:** PASS | DRIFT DETECTED
- [file:line] — [severity] — description
  Fix: replacement

### Layer 2 — Primitive Drift
**Status:** PASS | DRIFT DETECTED
- [file:line] — [USE PRIMITIVE | ACCEPTABLE OVERRIDE] — description

### Layer 3 — Component & Style Drift
#### 3a. Color & contrast
**Status:** PASS | ISSUES
- ...

#### 3b. Typography
**Status:** PASS | ISSUES
- ...

#### 3c. Pattern & layout
**Status:** PASS | ISSUES
- ...

#### 3d. Roundness
**Status:** PASS | ISSUES
- ...

#### 3e. Shadows
**Status:** PASS | ISSUES
- ...

#### 3f. Tailwind hygiene
**Status:** PASS | ISSUES
- ...

### Layer 4 — Layout & Shell Drift
**Status:** PASS | DRIFT DETECTED
- ...

### Layer 5 — Interactions & Accessibility
**Status:** PASS | ISSUES
- ...

### Summary
- Total issues: N (X critical, Y high, Z medium, W low)
- Files requiring changes: [list]
- Recommended fix order: [prioritized list]
```

---

## Quick flush (CLI)

For a fast automated check without a full report, run:

```bash
# Token drift — should return zero results
echo "=== TOKEN DRIFT ===" && \
grep -rn "bg-\[#" src/components src/app --include="*.tsx" | grep -cv "_stitch" && \
grep -rn "text-\[#" src/components src/app --include="*.tsx" | grep -cv "_stitch" && \
grep -rnE "(bg|text|border)-(slate|gray|zinc|blue|red|green)-[0-9]" src/ --include="*.tsx" | wc -l && \

# Roundness drift
echo "=== ROUNDNESS DRIFT ===" && \
grep -rnE "rounded-(lg|xl|2xl)" src/ --include="*.tsx" | wc -l && \

# Shadow drift
echo "=== SHADOW DRIFT ===" && \
grep -rnE "shadow-(lg|xl|2xl)" src/ --include="*.tsx" | wc -l && \

echo "=== DONE ==="
```

---

## Reference documents

| Document | Path | Use |
|----------|------|-----|
| Design Chain (this audit's bible) | `_docs/_build/_stitch/_design-system/DESIGN-CHAIN.md` | Full token tables, rules, hierarchy |
| Token spec | `_docs/_build/_stitch/_design-system/tokens.md` | Extracted Stitch tokens |
| Design system spec | `_docs/_build/_stitch/_design-system/design-system-spec.md` | Creative North Star, No-Line Rule |
| Component catalog | `_docs/_build/_stitch/_design-system/component-catalog.md` | Token→component mapping |
| Runtime tokens | `src/app/globals.css` (`@theme`) | Live token values |
| Designer dashboard skill | `.claude/skills/designer-dashboard/SKILL.md` | Dashboard-specific guidance |

---

## Rules

- Present the full audit report before applying any fixes.
- Fix at the correct layer: token issue → fix in `globals.css`; primitive issue → fix in `ui/`; component issue → fix in the component.
- Do not change brand primary hue without explicit user approval.
- Contrast fixes: prefer lightness adjustments over hue shifts.
- Do not modify `_docs/_build/_stitch/` HTML files — they are reference only.
- When in doubt about whether a hardcoded value is intentional, check the "Known Intentional Exceptions" in DESIGN-CHAIN.md.
