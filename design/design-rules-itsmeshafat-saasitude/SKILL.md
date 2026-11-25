---
name: design-rules
description: "Load before creating or editing any Blade view, component, or CSS. Enforces the Cobalt Pro design system: tokens, component kit, density rules, WCAG compliance, and naming conventions."
version: 1.0.0
target: "saas-boilerplate-laravel"
---

# Design Rules — Cobalt Pro

Load this skill whenever you create or modify Blade views, `x-ui.*` components, CSS, or anything visible in the UI.

## Token rule (the only rule that matters for colors)

**Use CSS variables. Never hard-code hex, rgb, or hsl values in Blade or CSS.**

```blade
{{-- ✓ correct --}}
<div class="bg-[var(--primary)] text-[var(--primary-foreground)]">

{{-- ✗ wrong --}}
<div class="bg-[#2563eb] text-white">
```

All tokens are defined in:
- `resources/views/vendor/tyro-dashboard/partials/shadcn-theme.blade.php` (dashboard)
- `resources/css/app.css` (public pages)
- Full spec: `design-system/saas-boilerplate/MASTER.md`

## Component kit — reuse before writing

Always check `resources/views/components/ui/` before writing a new component or inline styles.

| Need | Use |
|------|-----|
| Button | `<x-ui.button variant="primary\|secondary\|outline\|ghost\|danger\|link" size="sm\|md\|lg">` |
| Text input | `<x-ui.input label="…" error="…" hint="…">` |
| Card/panel | `<x-ui.card :header="…" :footer="…">` |
| Badge/tag | `<x-ui.badge variant="default\|secondary\|success\|warning\|danger\|info\|muted\|outline">` |
| Subscription status | `<x-ui.status-pill :status="$subscription->status" />` |
| Quota/usage bar | `<x-ui.usage-meter label="…" :used="n" :limit="n" unit="…" />` |
| Pricing card | `<x-ui.plan-card :plan="$plan" price="$9" :featured="true">` |
| Zero-state | `<x-ui.empty-state title="…" description="…">` |

## Density

- Interactive elements: **44px min height** (`h-11` = 2.75rem)
- Buttons: `h-11 px-4` (md), `h-8 px-3` (sm), `h-12 px-6` (lg)
- Inputs: `h-11 px-3`
- Table rows: `min-h-12` (48px)
- Card padding: `p-6` / `px-6 py-5`

## Border radius

Always use `rounded-[var(--radius)]` (8px) for interactive elements.
Outer wrappers that contain rounded elements: `rounded-[calc(var(--radius)+2px)]`.

## Typography classes

```blade
{{-- headings --}}
<h1 class="text-2xl font-semibold text-[var(--foreground)]">
{{-- body --}}
<p class="text-sm text-[var(--foreground)]">
{{-- meta / secondary --}}
<p class="text-sm text-[var(--muted-foreground)]">
{{-- label --}}
<label class="text-sm font-medium text-[var(--foreground)]">
```

## Semantic color shortcuts

```blade
{{-- success feedback --}}
<span class="text-[var(--success)]">Saved</span>
{{-- warning --}}
<span class="text-[var(--warning)]">Renews soon</span>
{{-- error --}}
<span class="text-[var(--destructive)]">Payment failed</span>
```

## Status pill shortcut

```blade
{{-- always use the component, never inline a subscription status badge --}}
<x-ui.status-pill :status="$subscription->status" />
```

## WCAG AA — do not break these pairs

| Foreground | On background | Min ratio |
|------------|---------------|-----------|
| `--foreground` | `--background` | 17.5:1 ✓ |
| `--primary-foreground` | `--primary` | 4.82:1 ✓ |
| `--muted-foreground` | `--card` | 4.53:1 ✓ |

If you add a new color combination, verify contrast ≥ 4.5:1 before shipping. Document it in `design-system/saas-boilerplate/MASTER.md`.

## Dark mode

All components use CSS variables, so dark mode is automatic when `.dark` is applied to `<html>`. Do not add `dark:` variants to variable-based classes — they already adapt.

## Admin overrides

The `DashboardColors` system in `storage/app/dashboard-colors.json` can override any CSS variable at runtime. This is intentional — never hard-code fallbacks in a way that blocks that system.
