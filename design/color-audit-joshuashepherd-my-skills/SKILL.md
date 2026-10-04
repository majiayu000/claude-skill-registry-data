---
name: color-audit
description: Expert color palette audit for movemental — verify semantic token completeness, WCAG contrast compliance, 60-30-10 distribution, and tonal stacking correctness. Light-primary site with regional Midnight sections.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Expert color palette audit — verify semantic token completeness, WCAG contrast compliance, 60-30-10 distribution, and tonal stacking correctness across the movemental platform.

Target: $ARGUMENTS

If no target is provided, audit the full palette in `globals.css` and spot-check usage across `src/components/` and `src/app/(site)/`.

## Before Starting

1. Read `src/app/globals.css` — extract ALL color tokens from `@theme inline` and `:root` blocks.
2. Read `docs/design/DESIGN.md` — confirm the palette spec (The Digital Curator: blue primary #0053db, light surface palette, Midnight for inverse sections).

## Palette Reference (DESIGN.md)

| Token | Value | Role |
|-------|-------|------|
| `--background` | `#f7f9fb` | Surface — default canvas |
| `--foreground` | `#2a3439` | Ink — never pure black |
| `--section` | `#f0f4f7` | surface_container_low — tonal shift |
| `--card` | `#ffffff` | surface_container_lowest — cards |
| `--elevated` | `#e1e9ee` | surface_container_high — accent band |
| `--primary` | `#0053db` | Actions, CTAs, focus — NOT large backgrounds |
| `--primary-dim` | `#0048c1` | Gradient endpoint for CTAs |
| `--inverse-surface` | `#101820` | Midnight hero sections |
| `--inverse-foreground` | `#f7f9fb` | Text on inverse-surface |
| `--muted-foreground` | `#566166` | on_surface_variant — subtitles |
| `--border` | `rgba(169,180,185,0.15)` | Form fields ONLY |

## Audit Dimensions

### 1. TOKEN COMPLETENESS

Verify all required tokens exist in `globals.css`:
- Background surface ramp: `--background`, `--section`, `--card`, `--elevated`, `--surface-highest`
- Foreground tokens: `--foreground`, `--card-foreground`, `--muted-foreground`
- Primary set: `--primary`, `--primary-dim`, `--primary-foreground`
- Inverse set: `--inverse-surface`, `--inverse-foreground`
- Utility: `--border`, `--input`, `--ring`, `--destructive`
- Custom: `--shadow-ambient`, `--gradient-primary`, layout tokens

### 2. CONTRAST COMPLIANCE (WCAG 2.1 AA)

**Required ratios:**
- Normal text (< 18px): 4.5:1 minimum
- Large text (≥ 18px / ≥ 14px bold): 3:1 minimum
- UI components: 3:1 minimum

**Critical pairs to check:**

| Pair | Background | Foreground | Context |
|------|-----------|------------|---------|
| Body text | `--background` (#f7f9fb) | `--foreground` (#2a3439) | Main content |
| Card text | `--card` (#fff) | `--foreground` (#2a3439) | Cards |
| Muted text | `--background` (#f7f9fb) | `--muted-foreground` (#566166) | Subtitles |
| Primary CTA | `--primary` (#0053db) | `--primary-foreground` (#fff) | Buttons |
| Midnight text | `--inverse-surface` (#101820) | `--inverse-foreground` (#f7f9fb) | Dark sections |
| Midnight muted | `--inverse-surface` (#101820) | inverse-foreground/55 | Dark subtitles |

### 3. TONAL STACKING AUDIT

Verify the surface ramp is monotonic (no lightness inversions):
`background (#f7f9fb)` → `section (#f0f4f7)` → `elevated (#e1e9ee)` → `surface-highest (#d7dfe5)`

Check that `card (#ffffff)` is lighter than all — it sits ON these surfaces to create Ghost Lift.

### 4. 60-30-10 DISTRIBUTION

Audit usage across key pages:
- **60% (dominant):** `--background` + `--foreground` — the base canvas
- **30% (secondary):** `--card`, `--section`, `--elevated`, `--muted-foreground` — structure
- **10% (accent):** `--primary` (#0053db) — CTAs, highlights, focus rings ONLY

**Red flags:**
- Primary blue used as background for large sections (kills CTA impact)
- `text-muted-foreground` used for main body text (too low contrast)
- Multiple competing accents visible in one view
- `bg-white` or `bg-black` used instead of semantic tokens

### 5. COMPONENT SPOT-CHECK

Scan component files for color violations:
- Hardcoded colors: `bg-blue-*`, `text-gray-*`, hex values, rgb()
- Mismatched pairs: `bg-primary` without `text-primary-foreground`
- Opacity dropping below WCAG: `text-foreground/50` as body text
- `text-white` outside of `variant="midnight"` Section wrappers
- Borders used for section separation (should be tonal stacking)

## Output Format

```
## Color Palette Audit

### Token Inventory
| Token | Value | Present | Status |
|-------|-------|---------|--------|

### Contrast Report
| Pair | Ratio | WCAG AA | Status |
|------|-------|---------|--------|

### Issues Found
1. [SEVERITY: CRITICAL/HIGH/MEDIUM/LOW] — description
   - Current: value
   - Recommended: value

### Tonal Stacking Assessment
- Surface ramp: [PASS/ADJUST]
- 60-30-10 distribution: [PASS/ADJUST]
```

## Rules

- This is a **light-primary** site. There is NO global dark mode.
- Midnight sections are regional — scoped to `<Section variant="midnight">` or `bg-inverse-surface`.
- Primary brand color is `#0053db` blue — do not change without user approval.
- Never use pure black (`#000`) — foreground is `#2a3439`.
- Never use pure white (`#fff`) as a background — surface is `#f7f9fb`. Card is the only white token.
- Present the full audit before making any changes.
- This audit complements `tailwind-cleanup` — color-audit checks the palette, tailwind-cleanup checks usage.
