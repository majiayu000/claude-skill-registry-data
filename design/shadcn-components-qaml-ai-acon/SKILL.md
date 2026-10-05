---
name: shadcn-components
description: Build UI using shadcn/ui components. Use when creating pages, forms, modals, navigation, sidebars, or any frontend UI. Provides component selection, composition patterns, and installation commands. Always activate before writing custom UI code.
---

# shadcn UI Components

## Required Workflow

Before writing ANY UI code:
1. Check [docs/shadcn-components.md](../../../docs/shadcn-components.md) for relevant primitives
2. Use MCP `mcp__shadcn__search_items_in_registries` to find blocks matching your need
3. Install blocks with `npx shadcn@latest add <block>` before customizing
4. Only build custom components when no shadcn primitive or block exists

## Composition Philosophy

shadcn components are primitives meant to be stacked, not standalone solutions.

**Mental model:** Decompose UI into shadcn primitives first:
- Login page = Card + Form + Field + Input + Button
- Settings page = Tabs + Card + Form + Switch + Select
- Dashboard = Sidebar + Card + Table + Chart + Badge
- Modal form = Dialog + Form + Field + Input + Button

**Pattern:** Container → Layout → Interactive → Feedback
- Containers: Card, Dialog, Sheet, Sidebar
- Layout: Tabs, Accordion, Separator, ScrollArea
- Interactive: Button, Input, Select, Switch, Checkbox
- Feedback: Alert, Toast, Badge, Skeleton

## DO NOT Build Custom Implementations Of:

Buttons, inputs, dialogs, dropdowns, cards, forms, navigation, tables, tooltips, popovers, or any component that exists in shadcn. Use the primitives.

## MCP Tools Available

- `mcp__shadcn__search_items_in_registries` - Search for components/blocks by keyword
- `mcp__shadcn__view_items_in_registries` - View component details and files
- `mcp__shadcn__get_item_examples_from_registries` - Get usage examples
- `mcp__shadcn__get_add_command_for_items` - Get install command

## Project Configuration 

- **Style:** radix-mira (compact/dense interface)
- **Base color:** mist
- **Theme:** mist
- **Chart Color:** mist
- **Heading:** Source Serif 4
- **Font:** Figtree
- **Radius:** Large (0.875rem)
- **Icons:** Lucide
- **Components location:** `src/components/ui/`
- **Preset code:** --preset b4cwnZvlhI

## Styling

- Use `cn()` utility from `@/lib/utils` for conditional classes
- Theme colors use CSS variables in `globals.css`
- Components support light/dark mode via `.dark` class on root
