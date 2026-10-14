---
name: styling-tailwind-v4
description: Tailwind CSS v4 conventions used in this template — CSS-first @theme config, OKLCH tokens, and variant composition.
paths: ["src/**/*.css", "src/**/*.tsx"]
---

- Design tokens are declared in `src/styles.css` under `@theme`, in OKLCH
  (`--color-brand-500: oklch(0.55 0.18 260);`), not in a `tailwind.config.js` — Tailwind v4 is
  CSS-first, there is no JS config file in this template.
- Reference tokens through the generated utility classes (`bg-brand-600`, `text-brand-700`),
  never hard-code a raw color value in a component — if a new brand color is needed, add it to
  `@theme` first.
- Compose conditional/variant classes with `cva` (see `component-conventions` skill) and merge
  with `cn()` (`clsx` + `tailwind-merge`) so conflicting utility classes (e.g. two different
  `px-*` values) resolve predictably instead of both landing in the class list.
- Prefer Tailwind's built-in responsive/state variants (`sm:`, `hover:`, `focus-visible:`,
  `disabled:`) over custom CSS — reach for `src/styles.css` only for `@theme` tokens or truly
  global resets, not component-level styling.
- Respect `color-scheme: light dark` (set on `body` in `src/styles.css`) — do not hard-code a
  light-only background/text color pair on a full-page container without checking it also
  works against a dark system theme.
