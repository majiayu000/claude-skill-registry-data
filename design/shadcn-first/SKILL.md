---
name: shadcn-first
description: >-
  Build UI with shadcn blocks and components instead of hand-written markup.
  Load this before writing ANY React/Next UI: new screens, redesigns, "make it
  look better", dashboards, sidebars, tables, forms, dialogs, chat surfaces.
  Enforces one standing rule: everything shadcn-based, no hand-rolled UI, as
  little custom code as possible.
---

# shadcn-first

Someone maintains this code after you. Every hand-written `div` with bespoke
classes and every `style={{}}` is a thing they keep alive, and it drifts. Hand-rolled UI also
silently drops the craft that comes free with the library: focus rings, hover and
active states, keyboard navigation, skeletons, empty states, ARIA.

## The order. Never skip a step.

1. **Block.** `ui.shadcn.com/blocks` has whole sidebars, dashboards, logins,
   data tables. Install the block.
2. **Component.** If no block fits, use a component from the registry.
3. **Compose** two or three components.
4. **Write it yourself.** Only here, and the commit message must name which block
   or component you evaluated and why it did not fit.

Adapt the design to the component, not the component to the design. Brand and
visual language are reached through **theme variables in one theme**, never
per-screen CSS beside the component.

## Tools, and which to use

Two MCP servers are configured. They do different jobs.

**`shadcn-official`** (`npx shadcn@latest mcp`) is project-aware: it reads the
repo's `components.json`. Use it for the real work.

| Tool | Use it to |
|---|---|
| `get_project_registries` | confirm the project is initialised at all |
| `search_items_in_registries` | find the component for the job, fuzzy |
| `list_items_in_registries` | see everything available |
| `view_items_in_registries` | read a component's actual source and deps before using it |
| `get_item_examples_from_registries` | copy a real usage example instead of guessing the API |
| `get_add_command_for_items` | get the exact `npx shadcn add …` line, then run it |
| `get_audit_checklist` | **run after writing code.** This is the gate. |

**`shadcn`** (`@jpisnice/shadcn-ui-mcp-server`) is registry-wide and knows blocks
and themes: `list_blocks`, `get_block`, `list_themes`, `get_theme`,
`get_component_demo`. Use it for step 1 and for theming.

If a project has no `components.json`, the official tools error. Run
`npx shadcn@latest init` first, then continue.

For AI chat surfaces use **prompt-kit** (`prompt-kit.com`, shadcn-compatible):
`chat-container`, `message`, `prompt-input`, `scroll-button`, `markdown`,
`code-block`, `loader`. Same rule, install rather than rebuild.

## Components people re-invent instead of installing

`sidebar` (collapsible, with footer user menu), `command` (Cmd+K palette),
`table` + TanStack data-table block, `tabs`, `sheet`, `dialog`, `alert-dialog`,
`popover`, `tooltip`, `skeleton`, `sonner` (toasts), `form` (react-hook-form +
zod), `breadcrumb`, `resizable`, `scroll-area`, `avatar`, `badge`, `separator`,
`dropdown-menu`, `select`, `collapsible`, `chart`.

If you catch yourself building any of these by hand, stop and install it.

## Keyboard shortcuts

Use **Cmd+K** for the command palette; that is the `cmdk` convention the
`command` component ships with. **Cmd+L is reserved by the browser** for the
address bar and cannot be intercepted reliably in Chrome. If someone asks for
Cmd+L, bind Cmd+K, add Cmd+L opportunistically, and say why.

## Done means measured, not claimed

Before reporting done, run `get_audit_checklist` and report the numbers:

- custom UI lines removed
- blocks and components installed
- remaining `style={{}}` occurrences (`grep -rc 'style={{' src/`)
- per screen: elements from `components/ui/` vs hand-written

Anything still hand-written must stand there with a stated reason, not be
overlooked. A screenshot is the proof that the screen renders; the counts are the
proof that the rule was followed. Both, or it is not done.

## Do not

- No emojis in UI. Real SVG icons (Lucide ships with shadcn).
- No text-in-circles for brand logos. Source real SVG paths:
  SimpleIcons > svgl.app > gilbarbara/logos > favicon.
- Max one or two accent colours. No coloured left borders on cards. No gradient
  on every element.
- Do not fork a component to change a colour. Change the theme variable.
