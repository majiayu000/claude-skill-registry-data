---
name: shadcn
description: shadcn/ui — copy-paste component library built on Radix primitives, styled with Tailwind CSS, and managed via CLI.
---

### copy-paste model
Components are owned by you. No npm dependency. Each component is a file in `components/ui/`. Modify anything. No lock-in.

### CLI usage
`npx shadcn@latest add button` — installs component + deps. `npx shadcn@latest init` — sets up config, aliases, CSS variables. `npx shadcn@latest diff` — see upstream changes.

### radix primitives
Built on Radix UI: headless, accessible, unstyled. Dialog, Popover, DropdownMenu, Select, Tabs, Tooltip, Toast, Sheet, etc. Each handles focus trapping, keyboard nav, ARIA attributes.

### theming
CSS variables in `globals.css`. `--primary`, `--secondary`, `--muted`, `--accent`, `--destructive`, `--border`, `--ring`, `--radius`. Switch themes by toggling `class="dark"` on `<html>`. Customize via CSS variable overrides.

### customization
Edit the component file directly. Swap `cn()` with your own utility. Add props, change styles, wrap with your logic. The registry is a starting point, not a constraint.

### registry
JSON-based registry (`https://ui.shadcn.com/r/styles.json`). Each entry: name, dependencies, registryDependencies, files, tailwind config extras, CSS vars.

### Tailwind v4 integration
In v4, shadcn uses `@theme` tokens instead of config. `--color-primary` becomes a Tailwind color. Supports `@variant` directives.

### best practices
Keep `components/ui` flat. Use `cn()` for merging classes. Only install what you use. Extend components with composition, not by editing the primitive.
