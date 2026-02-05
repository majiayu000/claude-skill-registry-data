---
name: Create Interactive Menu
description: Use this skill when creating dropdowns, context menus, or overlays that need a polished UX (open/close animation, click-outside, Escape, etc.).
---

# Create Interactive Menu

Preferred baseline: reuse the existing Lumina menu patterns (check `src/lumina/components/common/Menu.tsx` first).

## Mandatory UX checklist

Any interactive menu/overlay must include:

1. Open animation (fade-in + small translate/scale)
2. Close animation (fade-out via CSS transitions)
3. Click outside closes
4. Escape closes
5. Pointer-safe UX (hover delay when applicable)
6. Viewport safety (flip/fit near edges when needed)
7. Reduced-motion friendly (opacity/transform, no layout shift)

## Templates

- `template_menu.tsx`: a minimal menu component with animated open/close
- `useMenuInteraction.ts`: click-outside + Escape + optional hover delay

## Style guide (Lumina)

- Background: `bg-white`
- Border: `border border-slate-200`
- Shadow: `shadow-[0_10px_24px_rgba(15,23,42,0.12)]`
- Rounding: `rounded-2xl` / `rounded-xl`

