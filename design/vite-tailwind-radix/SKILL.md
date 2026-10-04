---
name: vite-tailwind-radix
category: frontend
description: Use when styling any web UI - style with Tailwind utility classes and design tokens, avoid custom CSS, and build on the existing Radix/shadcn primitives instead of hand-rolling
tech_stack: React
source: shadcn-ui/ui (MIT), adapted
---
# Tailwind, Radix, No Custom CSS

## Overview

Styling is Tailwind-first with a shared token system, on top of Radix/shadcn primitives. Custom CSS and hand-rolled interactive widgets are what this skill exists to prevent — they fragment the design and re-introduce accessibility bugs the primitives already solved.

**Core principle:** Avoid custom CSS. Style with Tailwind utilities and the design tokens; reach for the existing shadcn primitive before building an interactive widget, and its built-in variant before a custom class.

## Rules

- **Tailwind v4 by default.** New Vite projects use `@tailwindcss/vite` and `@import "tailwindcss"`, with tokens defined in `@theme`/`:root` in the main CSS file. A repo already on Tailwind v3 keeps `tailwind.config` — check `package.json` and follow what the repo already uses, don't migrate it mid-task.
- **Tailwind utilities, not custom CSS.** No new `.css` files, no `<style>` blocks, no bespoke class names. Compose utilities; use `cn()` for conditional variants. An inline `style={{}}` object is allowed ONLY for a genuinely dynamic, computed value (a measured width, a transform) — tag it `// ui-guard-allow: <reason>` if the project runs ui-guard.
- **Built-in variants before custom styles.** `<Button variant="outline">`, `size="sm"` — not `className="border border-input bg-transparent hover:bg-accent"`.
- **Semantic tokens, not raw values.** `bg-primary`, `text-muted-foreground`, `border-border` — never `bg-blue-500`, `text-gray-600`, or a hex code. No arbitrary pixel values (`w-[327px]`) — use the scale.
- **`className` is for layout, not restyling.** `w-full`, `max-w-md`, `self-end`, `col-span-2` are fine (spacing between siblings comes from the parent's `gap`, not margins on the child); overriding a component's own colour or typography through `className` is not — change the variant or the token instead.
- **`gap-*` over `space-x-*`/`space-y-*`.** `flex flex-col gap-4`, not `space-y-4`.
- **`size-*` for square elements.** `size-10`, not `w-10 h-10`.
- **No manual `dark:` colour overrides** — the semantic tokens already carry both themes.
- **No manual z-index on overlay primitives.** `Dialog`, `Sheet`, `Drawer`, `Popover`, `DropdownMenu`, `Tooltip` manage their own stacking; never add `z-50`/`z-[999]` to them. The fixed z-scale — `z-10` raised content, `z-20` sticky header, `z-30` dropdown/popover, `z-40` overlay, `z-50` modal/toast — is for your own layered content, never arbitrary `z-[…]`.
- **Build on the primitives.** Dialog, Dropdown, Tooltip, Popover, Tabs, etc. come from the Radix primitives wrapped in `components/ui` — never hand-roll one that exists (you'll lose focus trapping, keyboard nav, and ARIA). `Dialog`/`Sheet`/`Drawer` always render a `Title` (visually hidden with `sr-only` if the design doesn't show one).
- **Forms use the Field pattern.** `Field`/`FieldGroup` (or the project's own `FormField` molecule) — not a raw `div` with `space-y-*`. Validation state is `data-invalid` on the `Field`, `aria-invalid` on the control.
- **Use the component for the job, not a styled div.** `Empty` for empty states, `Skeleton` for loading (no custom `animate-pulse` div), `AlertDialog` for destructive confirmation, `Spinner` composed into `Button` for a pending submit.
- **Match neighbors.** Before styling a new screen, look at an adjacent one and reuse its patterns and token classes.
- **`npm run build` must stay green** — a TypeScript error or failed build is a broken task, not a warning.

## Where things live

- shadcn/Radix primitives are the atom-level vendor layer, generated into `components/ui` — see `component-composition` for the rest of the atomic levels and the import-direction rule.
- A repo with no tokens or folder structure yet: see `web-design-system-foundation` to set up `@theme`, `cn()`, and the base atoms before building the first screen.

## When an inline style / arbitrary value IS ok

| Situation | Verdict |
|-----------|---------|
| Static padding/color/size | Tailwind token class |
| Conditional variant | `cn()` with utility classes |
| Value computed at runtime (measured px, dynamic transform) | inline `style={{}}` — the only valid case, tag `ui-guard-allow:` if ui-guard runs |
| A one-off pixel that "isn't in the scale" | No — use the nearest scale token; extend the scale via tokens if truly needed |
| `grid-cols-[repeat(auto-fit,minmax(...))]`, `max-w-[..ch]`, `aspect-[..]` | Allowed arbitrary values (ui-guard's allow-list) |

## Worked Example

```tsx
// ❌ custom CSS + magic values + hand-rolled dropdown
<div className="my-custom-menu" style={{ padding: "13px", background: "#f5f5f5" }}>
  {/* hand-built menu: no keyboard nav, no ARIA */}
</div>

// ✅ tokens + primitive + built-in variant
<DropdownMenu>                          {/* Radix primitive from components/ui */}
  <DropdownMenuTrigger asChild><Button variant="ghost">Actions</Button></DropdownMenuTrigger>
  <DropdownMenuContent className="p-3">
    <DropdownMenuGroup>
      <DropdownMenuItem onSelect={onExport}>Export</DropdownMenuItem>
    </DropdownMenuGroup>
  </DropdownMenuContent>
</DropdownMenu>
```

The primitive brings focus management, escape-to-close, and ARIA for free; the token classes and `DropdownMenuGroup` keep it visually and structurally identical to every other menu.

## Common Mistakes

- A new `.css` file or `<style>` block instead of utilities.
- Arbitrary values (`w-[327px]`, `text-[#3a3a3a]`) or raw palette classes instead of scale tokens.
- Hand-rolling a dialog/dropdown/tooltip/empty-state/skeleton that already exists in `components/ui`.
- `space-x-*`/`space-y-*` instead of `gap-*`; a manual `z-50` on an overlay primitive.
- `style={{}}` for static styling that a class would cover.

## Red Flags

- Any new custom CSS class or stylesheet in the diff.
- An interactive widget built from raw `div`s with `onClick` instead of a primitive.
- Magic pixel/color values or a manual `dark:` override scattered across the component.
