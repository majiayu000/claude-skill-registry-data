---
name: shadcn
description: shadcn/ui — Radix UI + Tailwind copy-paste; MCP for component install.
---

## Detection Signals

- `components/ui/` directory with component files (`button.tsx`, `card.tsx`, `dialog.tsx`)
- `components.json` at project root
- `@radix-ui/*` and `lucide-react` in `package.json`
- `cn()` utility import from `@/lib/utils`
- `class-variance-authority` (cva) in dependencies

## MCP Setup

shadcn/ui has an official MCP that enables component browsing, searching, and installation via natural language.

**Add to `.claude/settings.json`** (or `.claude/settings.local.json` for local-only):

```json
{
  "mcpServers": {
    "shadcn-ui": {
      "command": "npx",
      "args": ["-y", "shadcn@latest", "mcp"]
    }
  }
}
```

> If auto-configuration fails, ask the user to add the entry manually in their CLI's MCP settings (**Claude Code → Settings → MCP Servers**; the `mcp` block of `opencode.json`; Codex CLI's MCP config). Once active, components can be requested by description and the MCP handles installation.

## Core Concepts

| Concept | Detail |
|---------|--------|
| **Copy-paste** | Components live in `components/ui/` — owned by the project, not a package |
| **Radix UI** | Accessible, unstyled headless primitives under the hood |
| **Tailwind CSS** | All styling via utility classes |
| **`cn()` utility** | `clsx` + `tailwind-merge` — required for safe class merging |
| **CVA** | `class-variance-authority` — defines component variants |
| **CLI** | `npx shadcn@latest add <component>` installs with all dependencies |

## Component Patterns

```tsx
// Always use cn() for className merging — never string concatenation
import { cn } from "@/lib/utils"
<Button className={cn("w-full", isLoading && "opacity-50")} />

// Variants via CVA — check the component file for available variant values
<Button variant="destructive" size="sm" />

// asChild for polymorphism — render as a different element without wrapper hacks
<Button asChild>
  <Link href="/dashboard">Go to dashboard</Link>
</Button>
```

## CLI Reference

```bash
npx shadcn@latest add button          # add single component
npx shadcn@latest add dialog sheet    # add multiple at once
npx shadcn@latest diff                # check for component updates
```

## Critical Rules

- **Never install as a package** — components are meant to be copied into the project; importing from node_modules defeats the model
- **Always use `cn()`** for merging classNames — direct concatenation causes Tailwind class conflicts
- **Customize in `components/ui/`** — that is the intended extension point; no need to wrap or fork
- **Check `components.json`** before adding — it defines path aliases (`@/components/ui`) that must be respected
- **`asChild` for polymorphism** — when a button needs to render as a `<Link>`, use `asChild` not a wrapper div
