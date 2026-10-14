---
name: component-conventions
description: Conventions for creating or editing components under src/components/** — file structure, props/types, composition, and when to reach for a Radix primitive vs a plain element.
paths: ["src/components/**"]
---

- One component per file, named exports, `PascalCase` filename matching the component name
  (see `src/components/Button.tsx`, `src/components/SubscribeDialog.tsx`).
- Props interface named `<Component>Props`, extending the relevant HTML attributes interface
  when the component wraps a native element (`React.ButtonHTMLAttributes<HTMLButtonElement>`,
  etc.) so consumers keep native props like `onClick`, `aria-*`, `disabled` for free.
- Style with Tailwind utility classes via the `cn()` helper (`src/lib/utils.ts`,
  `clsx` + `tailwind-merge`) — never string-concatenate classes.
- Variant-based components (buttons, badges, alerts) use `class-variance-authority` (`cva`),
  not a manual `if/else` chain of class strings — see `Button.tsx` for the pattern.
- Interactive/composite components (dialogs, dropdowns, tooltips, popovers) are built on
  **Radix UI primitives** (`@radix-ui/react-*`), not raw DOM + manual ARIA — Radix owns focus
  management, keyboard interaction, and portal/positioning correctly by default.
  - **Upgrade path (ADR-006):** the template installs Radix because `@base-ui-components/react`
    is still a release candidate (`1.0.0-rc.*`) as of this template's generation date. Once it
    publishes a real `1.0.0` (check with `npm view @base-ui-components/react dist-tags`), Base
    UI is the documented swap in `docs/CUSTOMIZING.md` — the component file structure below
    does not change, only the primitive import.
- Every interactive element needs a visible focus style (`focus-visible:ring-*`, see
  `buttonVariants` in `Button.tsx`) — never `outline-none` without a replacement.
- A component that wraps `asChild`/`Slot` (see `Button.tsx`) must forward `ref` with
  `React.forwardRef` — Radix's `asChild` pattern depends on ref forwarding to work.
