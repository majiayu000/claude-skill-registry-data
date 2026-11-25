---
name: shadcn-component
description: Use shadcn/ui components (Radix + Tailwind v4) for every UI control in EasyTask, add missing ones with the CLI, and keep them in the app style. Use when building UI, adding a control, or replacing a native/hand-made control (select, popover select, menu, dialog, tooltip).
---

# shadcn/ui component (EasyTask)

Rule: wherever shadcn/ui has a component, use it instead of a native or hand-made control (native `<select>`, hand-made popover select, custom dropdown...). Build a custom control only if no shadcn component fits. The user noticed native selects and a hand-made popover select looking inconsistent and asked for the shadcn `Select` (`src/components/ui/select.tsx`).
Also load the `ui-ux-pro-max` skill for design decisions.

## Setup (components.json)
- Style `new-york`, base color `neutral`, CSS variables, icons `lucide`, Tailwind config empty, CSS in `src/index.css`.
- Aliases: `@/components`, `@/components/ui`, `@/lib/utils` (`cn`), `@/lib`, `@/hooks`.

## Already installed (src/components/ui/)
alert, badge, button (+ button-variants.ts), checkbox, collapsible, command, context-menu, dialog, dropdown-menu, empty, input, label, menubar, popover, progress, select, separator, sheet, skeleton, slider, sonner, switch, tabs, textarea, toggle (+ toggle-variants.ts), toggle-group, tooltip.
Radix packages in package.json: checkbox, collapsible, context-menu, dialog, dropdown-menu, label, menubar, popover, progress, select, separator, slider, slot, switch, tabs, toggle, toggle-group, tooltip. Check this list before adding anything.

## Adding a component
1. `npx shadcn@latest add <name>` (npm; do not hand-write what the CLI provides).
2. In this repo the CLI writes to a literal `@/components/ui` folder at the repo root: move the file into `src/components/ui/` and delete the stray `@` folder.
3. Align it to the app style like the existing ui files: square-ish `rounded-xs` (not the shadcn default `rounded-md`), theme tokens (`bg-popover`, `text-muted-foreground`, `border-input`, `ring-ring`...), never hard-coded colors. Tokens and the `.dark` set live in `src/index.css` (dark variant `&:is(.dark *)`; no `--radius`, `--chart-*` or `--sidebar-*` tokens: if the CLI adds them back, remove them unless the new component uses them).
4. Variants that must be importable without the component go in a separate `*-variants.ts` (as `button-variants.ts`, `toggle-variants.ts`).

## Variants in use
- Button variants: `default`, `destructive` (soft red outline), `destructiveSolid`, `outline`, `buttonIcon`, `secondary`, `ghost`, `link`. Sizes: `default`, `sm`, `lg`, `icon`.
- Use `destructive` for losing data, `destructiveSolid` only for irreversible actions.

## App wrappers (reuse, do not duplicate)
- Tooltip: `src/components/tooltip-custom.tsx` (`TooltipCustom` with `text`, `shortcut`, `side`). The app has one shared `TooltipProvider` (`src/App.tsx`); `ui/tooltip.tsx` falls back to its own provider outside it (e.g. in tests).
- Item menus: `src/components/item-menu.tsx` (`ItemMenu` = right click ContextMenu, `ItemMenuButton` = "..." DropdownMenu) render ONE list of entries written with the `Menu*` primitives from `src/components/menu-kind.tsx` (`MenuItem`, `MenuGroup`, `MenuSeparator`, `MenuSub`, `MenuSubTrigger`, `MenuSubContent`). They pick the dropdown or context flavour from `MenuKindProvider`. Add new entries there, never a second list.
- Menu entry: `ButtonInPopover` (`src/components/button-in-popover.tsx`); icons come from its typed `iconMap`: add a name there.
- Confirmations: `ConfirmDialog` (`src/components/dialogs/dialog-confirm.tsx`) for every "are you sure?" (`destructive`, `irreversible`, `initialFocus="cancel"` for what cannot be undone).
- Form errors: `FormError` (`src/components/form-error.tsx`, `role="alert"`, link with `aria-describedby`).
- Focus ring for hand-made focusable elements: `focusRing` in `src/lib/a11y.ts`; `onActivateKey` for Enter/Space.
- Dialogs load lazily: `lazyWithPreload` + `preloadWhenIdle` (`src/lib/lazy-preload.tsx`) and `LazyMount` (`src/components/lazy-mount.tsx`, mounts on first `active`). Do the same for a new heavy dialog.

## Radix pitfalls seen in this app
- A modal ContextMenu gives focus back to its trigger when it closes (even after an outside click), which re-opens a Tooltip on that trigger. Tree rows handle it with `openOnKeyboardFocus` (`src/pages/workspacePage/components/sidebar/tree-row.ts`), used as `<TooltipTrigger asChild onFocus={openOnKeyboardFocus}>` in `Note.tsx` and `Folder.tsx`.
- Radix `composeEventHandlers` skips its own handler when the user handler calls `event.preventDefault()`.
- React inline styles: never pass the string `"undefined"` (e.g. a template literal around a value that may be undefined); the browser drops the invalid value and keeps the old one.
- Portaled content (dialog, menu) still bubbles React events to the parent row: `stopPropagation` as `ConfirmDialog` and `ItemMenu` do.

## i18n
Every visible string goes through react-i18next (`t(...)`) with keys in BOTH `src/i18n/locales/it/*.ts` and `src/i18n/locales/en/*.ts` (Italian is primary). Accessible names too (`aria-label`, e.g. `common.openMenu`, `common.menuOf`). No hard-coded strings in ui components.

## Tests
vitest + Testing Library + jsdom. jsdom matches `:focus-visible` on every focus: to test the keyboard-only path stub `Element.prototype.matches`. Test a component alone and the tooltip still works (own provider fallback).

## Process
- Design/UI reviews cover the whole app, not just the diff; propose a plan first, then apply fixes.
- Verify in light and dark theme.
