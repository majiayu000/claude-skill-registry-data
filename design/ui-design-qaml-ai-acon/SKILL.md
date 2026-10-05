---
name: ui-design
description: Typography and visual hierarchy rules for camelAI. Use when choosing font sizes, font families, or text styling in any UI code. Covers the 4-tier type scale and display font usage.
---

# UI Design Guidelines

## Font Size: 4 Tiers Only

| Tier | Class | Use for |
|------|-------|---------|
| **Display** | `text-xl` to `text-2xl` | Page/section headings. Always pair with `font-display`. `text-2xl` for primary page titles, `text-xl` for lighter section headings. |
| **Body** | `text-sm` | Everything else. The default. |
| **Caption** | `text-xs` | Metadata, timestamps, shortcuts, muted helper text. |
| **Micro** | `text-[0.625rem]` | `xs` button variant only. No new uses. |

No arbitrary sizes (`text-[11px]`, `text-[13px]`). No `text-base` for body text or inputs. No responsive size overrides (`md:text-xs`).

Exceptions: avatar initials, PDF rendering, email templates, and the welcome/onboarding splash screen (`text-3xl font-display` — the only place `text-3xl` is allowed).

## Font Families

| Class / Variable | Default | Use for |
|-----------------|---------|---------|
| `--font-sans` (body default) | Figtree | All text unless specified otherwise |
| `font-display` / `--font-display` | Source Serif 4 | Display-tier headings only |
| `--font-mono` | GeistMono | Code blocks, inline code |

The display font is special — use it only for the top-level heading on a page or dialog. Card titles, form labels, sub-sections, and buttons stay in the body font. Differentiate those with `font-medium` or `font-semibold` instead.

## Hierarchy via Weight and Color, Not Size

- **Primary:** `text-sm text-foreground` (add `font-medium` for emphasis)
- **Secondary:** `text-sm text-muted-foreground`
- **Tertiary:** `text-xs text-muted-foreground`

A card or list item should use at most 2 tiers (Body + Caption).

## Don't Override shadcn Defaults

Component font sizes are set in `src/components/ui/`. Don't override them at usage sites — if a default is wrong, fix the component file.
