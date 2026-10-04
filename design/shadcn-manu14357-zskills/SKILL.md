---
name: shadcn
description: >
  Complete shadcn/ui component management for adding, searching, fixing, styling,
  and composing UI in any React project. Use this skill whenever the user mentions
  shadcn, shadcn/ui, adding UI components, building forms or dashboards with Radix,
  working with component registries (@shadcn, @magicui, @tailark), or any task
  involving npx shadcn CLI commands. Also trigger when the user asks to fix styling
  issues, build a settings page, dashboard, or modal flow in a project that uses
  shadcn/ui — even if they don't say "shadcn" explicitly. This skill manages the
  full component lifecycle: search, add, view, diff, smart-merge upstream updates,
  and enforce critical rules for forms, composition, styling, and icons.
compatibility:
  tools: [shell]
  requires: npx shadcn@latest (or pnpm dlx / bunx equivalent)
---

# shadcn/ui

A framework for building UI, components, and design systems.
Components are added as source code directly into the project via the CLI.

> **IMPORTANT:** Always run CLI commands using the project's package runner.
> Check `packageManager` from project context and substitute accordingly:
> `npx shadcn@latest` · `pnpm dlx shadcn@latest` · `bunx --bun shadcn@latest`
> All examples below use `npx shadcn@latest`.

---

## Step 0 — Get Project Context First

**Always do this before any other step.**

```bash
npx shadcn@latest info --json
```

This returns the project config and installed components. Key fields to read:

| Field | What it controls |
|---|---|
| `aliases` | Import prefix — use exactly, never hardcode `@/` |
| `isRSC` | If `true`, any file using hooks/events/browser APIs needs `"use client"` |
| `tailwindVersion` | `v4` → `@theme inline` blocks; `v3` → `tailwind.config.js` |
| `tailwindCssFile` | The one global CSS file for variables — always edit this, never create a new one |
| `base` | `radix` or `base` — affects `asChild` vs `render` prop and available APIs |
| `iconLibrary` | Determines icon imports — `lucide-react`, `@tabler/icons-react`, etc. Never assume lucide |
| `style` | Visual treatment — `nova`, `vega`, `maia`, etc. |
| `resolvedPaths` | Exact file-system destinations for components, utils, hooks |
| `framework` | Routing and file conventions (Next.js App Router, Vite SPA, etc.) |
| `packageManager` | Use for any non-shadcn dependency installs |
| `components` | Already installed — check before adding or importing anything |

---

## Principles

1. **Use existing components first.** Search before writing custom UI.
2. **Compose, don't reinvent.** Settings page = Tabs + Card + form controls. Dashboard = Sidebar + Card + Chart + Table.
3. **Use built-in variants before custom styles.** `variant="outline"`, `size="sm"`, etc.
4. **Use semantic colors only.** `bg-primary`, `text-muted-foreground` — never `bg-blue-500`.

---

## Critical Rules

Violations of these rules are bugs, not preferences. Enforce them on every output.

### Styling

- **`className` for layout only.** Never override component colors or typography via className.
- **No `space-x-*` / `space-y-*`.** Use `flex` with `gap-*`. Vertical stacks: `flex flex-col gap-*`.
- **`size-*` when width = height.** `size-10` not `w-10 h-10`.
- **`truncate` shorthand.** Not `overflow-hidden text-ellipsis whitespace-nowrap`.
- **No manual `dark:` color overrides.** Use semantic tokens (`bg-background`, `text-muted-foreground`).
- **`cn()` for conditional classes.** Never write manual template literal ternaries.
- **No manual `z-index` on overlay components.** Dialog, Sheet, Popover manage their own stacking.

### Forms & Inputs

- **`FieldGroup` + `Field` for all form layout.** Never use raw `div` with `space-y-*` or `grid gap-*`.
- **`InputGroup` requires `InputGroupInput`/`InputGroupTextarea`.** Never raw `Input`/`Textarea` inside `InputGroup`.
- **Buttons inside inputs → `InputGroup` + `InputGroupAddon`.**
- **2–7 toggle options → `ToggleGroup`.** Don't loop `Button` with manual active state.
- **Grouped checkboxes/radios → `FieldSet` + `FieldLegend`.**
- **Validation → `data-invalid` on `Field`, `aria-invalid` on control.**
- **Disabled → `data-disabled` on `Field`, `disabled` on control.**

### Composition

- **Items always inside their Group.** `SelectItem` → `SelectGroup`. `DropdownMenuItem` → `DropdownMenuGroup`. `CommandItem` → `CommandGroup`.
- **Custom triggers → `asChild` (radix) or `render` (base).** Always check the `base` field.
- **Dialog, Sheet, Drawer always need a Title.** Use `className="sr-only"` if visually hidden.
- **Full Card composition.** Always use `CardHeader` / `CardTitle` / `CardDescription` / `CardContent` / `CardFooter`.
- **Button has no `isPending`/`isLoading`.** Compose with `Spinner` + `data-icon` + `disabled`.
- **`TabsTrigger` must be inside `TabsList`.**
- **`Avatar` always needs `AvatarFallback`.**

### Use Components, Not Custom Markup

- **Callouts → `Alert`.** Not custom styled divs.
- **Empty states → `Empty`.** Not custom markup.
- **Toast → `sonner`.** Use `toast()` from `sonner`.
- **Dividers → `Separator`.** Not `<hr>` or `<div className="border-t">`.
- **Loading placeholders → `Skeleton`.** No custom `animate-pulse` divs.
- **Status labels → `Badge`.** Not custom styled spans.

### Icons

- **Icons in `Button` use `data-icon`.** `data-icon="inline-start"` or `data-icon="inline-end"` on the icon element.
- **No sizing classes on icons inside components.** No `size-4` or `w-4 h-4` — components handle sizing via CSS.
- **Pass icons as objects, not strings.** `icon={CheckIcon}` not a string lookup.

### CLI

- **Never decode or fetch preset codes manually.** Pass them directly to `npx shadcn@latest apply --preset <code>`.

---

## Key Patterns

```tsx
// ✅ Form layout: FieldGroup + Field
<FieldGroup>
  <Field>
    <FieldLabel htmlFor="email">Email</FieldLabel>
    <Input id="email" />
  </Field>
</FieldGroup>

// ✅ Validation: data-invalid on Field, aria-invalid on control
<Field data-invalid>
  <FieldLabel>Email</FieldLabel>
  <Input aria-invalid />
  <FieldDescription>Invalid email address.</FieldDescription>
</Field>

// ✅ Icons in buttons: data-icon, no sizing classes
<Button>
  <SearchIcon data-icon="inline-start" />
  Search
</Button>

// ✅ Spacing: gap-*, not space-y-*
<div className="flex flex-col gap-4">  {/* correct */}
<div className="space-y-4">           {/* wrong   */}

// ✅ Equal dimensions: size-*, not w-* h-*
<Avatar className="size-10">    {/* correct */}
<Avatar className="w-10 h-10">  {/* wrong   */}

// ✅ Status colors: semantic tokens or Badge variants
<Badge variant="secondary">+20.1%</Badge>          {/* correct */}
<span className="text-emerald-600">+20.1%</span>   {/* wrong   */}

// ✅ Button loading state: Spinner + data-icon + disabled
<Button disabled>
  <Spinner data-icon="inline-start" />
  Saving...
</Button>
```

---

## Component Selection

| Need | Component |
|---|---|
| Action / submit | `Button` with appropriate variant |
| Text input | `Input`, `Textarea`, `InputOTP` |
| Selection | `Select`, `Combobox`, `RadioGroup`, `Checkbox`, `Switch`, `Slider` |
| Toggle 2–5 options | `ToggleGroup` + `ToggleGroupItem` |
| Date | `DatePicker` (Calendar + Popover) |
| Data table | `Table` |
| Info display | `Card`, `Badge`, `Avatar` |
| Navigation | `Sidebar`, `NavigationMenu`, `Breadcrumb`, `Tabs`, `Pagination` |
| Modal | `Dialog` |
| Side panel | `Sheet` |
| Bottom sheet | `Drawer` |
| Confirmation | `AlertDialog` |
| Toast / notification | `sonner` → `toast()` |
| Inline feedback | `Alert` |
| Progress | `Progress`, `Spinner` |
| Loading placeholder | `Skeleton` |
| Command palette | `Command` inside `Dialog` |
| Charts | `Chart` (wraps Recharts) |
| Layout & structure | `Card`, `Separator`, `Resizable`, `ScrollArea`, `Accordion`, `Collapsible` |
| Empty states | `Empty` |
| Dropdown menus | `DropdownMenu`, `ContextMenu`, `Menubar` |
| Tooltips / info | `Tooltip`, `HoverCard`, `Popover` |

---

## Workflow

Follow this sequence every time:

**1. Get project context**
```bash
npx shadcn@latest info --json
```
Re-run any time config may have changed.

**2. Check installed components**
Before running `add`, check the `components` list from project context or list `resolvedPaths.ui`.
Do not import components not yet added. Do not re-add already installed ones.

**3. Find components**
```bash
npx shadcn@latest search @shadcn -q "sidebar"
npx shadcn@latest search @magicui -q "shimmer"
npx shadcn@latest search @tailark -q "stats"
```

**4. Get docs and examples**
```bash
npx shadcn@latest docs button dialog select
```
Fetch the returned URLs. Always do this before creating, fixing, or composing a component.

**5. Preview before installing**
```bash
npx shadcn@latest add button --dry-run
npx shadcn@latest add button --diff button.tsx
```

**6. Install**
```bash
npx shadcn@latest add button card dialog
npx shadcn@latest add @magicui/shimmer-button
```

**7. Fix imports in third-party components**
After adding from community registries, check added non-UI files for hardcoded `@/components/ui/...` paths.
Use `npx shadcn@latest info` to get the correct `ui` alias and rewrite accordingly.

**8. Review added files**
After every `add`, read the added files and verify:
- No missing sub-components (e.g. `SelectItem` without `SelectGroup`)
- All imports correct
- Composition follows Critical Rules
- Icons match project's `iconLibrary` — swap if different

**9. Never guess the registry**
If the user says "add a login block" without specifying `@shadcn`, `@tailark`, etc., ask which registry. Never default.

---

## Updating Components (Smart Merge)

When updating a component while preserving local changes — **never fetch raw files from GitHub manually**.

```bash
# 1. See all files that would change
npx shadcn@latest add <component> --dry-run

# 2. Inspect diff for each file
npx shadcn@latest add <component> --diff <file>

# 3. Decide per file:
#    - No local changes → safe to overwrite
#    - Has local changes → read local, apply upstream changes, preserve modifications
#    - User says "update everything" → use --overwrite, but confirm first

# ⚠️ Never use --overwrite without explicit user approval
```

---

## Switching Presets

Always ask the user first: **overwrite**, **merge**, or **skip**?

| Mode | Command | Effect |
|---|---|---|
| Overwrite | `npx shadcn@latest apply --preset <code>` | Overwrites components, fonts, CSS variables |
| Merge | `npx shadcn@latest init --preset <code> --force --no-reinstall` then diff each component | Updates config and CSS, smart-merges components |
| Skip | `npx shadcn@latest init --preset <code> --force --no-reinstall` | Updates config and CSS only, leaves components untouched |

> Always run preset commands inside the project directory.
> `apply` requires an existing `components.json`.
> The CLI preserves the current `base` automatically.
> In temp directories, pass `--base <current-base>` explicitly.

---

## Quick Reference

```bash
# New project
npx shadcn@latest init --name my-app --preset base-nova
npx shadcn@latest init --name my-app --preset a2r6bw --template vite

# Monorepo
npx shadcn@latest init --name my-app --preset base-nova --monorepo

# Existing project
npx shadcn@latest init --preset base-nova
npx shadcn@latest init --defaults

# Apply preset to existing project
npx shadcn@latest apply --preset a2r6bw

# Add components
npx shadcn@latest add button card dialog
npx shadcn@latest add --all

# Search registries
npx shadcn@latest search @shadcn -q "sidebar"

# Get docs
npx shadcn@latest docs button dialog

# View without installing
npx shadcn@latest view @shadcn/button
```

**Named presets:** `nova` · `vega` · `maia` · `lyra` · `mira` · `luma`
**Templates:** `next` · `vite` · `start` · `react-router` · `astro` · `laravel`
**Preset codes:** version-prefixed base62 strings from [ui.shadcn.com](https://ui.shadcn.com)

---

## Reference Files

> Read these when the task involves the corresponding domain.

- `rules/forms.md` — FieldGroup, Field, InputGroup, ToggleGroup, FieldSet, validation states
- `rules/composition.md` — Groups, overlays, Card, Tabs, Avatar, Alert, Empty, Toast, Separator, Skeleton, Badge, Button loading
- `rules/icons.md` — data-icon, icon sizing, passing icons as objects
- `rules/styling.md` — Semantic colors, variants, className, spacing, size, truncate, dark mode, cn(), z-index
- `rules/base-vs-radix.md` — asChild vs render, Select, ToggleGroup, Slider, Accordion
- `cli.md` — Full command reference, flags, presets, templates
- `customization.md` — Theming, CSS variables, extending components