---
name: nuxt-ui
description: Use when implementing or debugging UI features with Nuxt UI components, designing forms, tables, modals, or any user interface work - fetches current documentation to ensure accurate component APIs
---

# Nuxt UI Skill

**Source of Truth:** `https://ui.nuxt.com/llms.txt` for all Nuxt UI component APIs.

Nuxt UI v4 is actively developed with frequent changes. Training data may be outdated. Always verify component APIs before implementing.

## When to Use This Skill

- Implementing any Nuxt UI component (UForm, UTable, UModal, UButton, etc.)
- Designing forms with validation
- Creating data tables with loading/empty states
- Building modals, slidevers, or overlays
- Working with toasts and notifications
- Uncertain about component props, slots, or events

## Mandatory Workflow

### Step 1: Fetch Targeted Documentation

Before implementing ANY Nuxt UI component, execute a WebFetch request:

```
WebFetch to https://ui.nuxt.com/llms.txt with prompt:
"Extract ONLY the documentation for [UComponent] from Nuxt UI.
Include: Props, Slots, Events, code examples.
Exclude everything else. Return a concise summary."
```

**CRITICAL**: Never fetch the full documentation. Use targeted extraction to avoid context bloat (1-3k tokens vs 50k+).

### Step 2: Read Project Patterns

Read the `DESIGN_GUIDE.md` file (symlinked in this directory) for:
- Project-specific code patterns and conventions
- Form validation with Zod
- Table patterns with useFetch
- Modal and slideover conventions
- Toast notification usage
- Common mistakes to avoid

### Step 3: Implement with Type Safety

All implementations must use:
- Zod schemas for form validation
- Proper TypeScript types
- `FormSubmitEvent<Schema>` for form handlers

## Red Flags - Stop and Fetch Docs First

| Warning Sign | Why It's Dangerous |
|-------------|-------------------|
| "I know how UModal works" | API may have changed |
| "This is a simple component" | Simple tasks have highest error rates |
| "I'll check docs if it doesn't work" | Debugging takes 10x longer than verification |
| "The prop is probably called X" | Guessing props causes subtle bugs |
| Using `@close` instead of `v-model:open` | Event names change between versions |

## Quick Reference

See `DESIGN_GUIDE.md` for complete patterns on:
- **Forms**: Zod schemas, UFormField, validation, error handling
- **Tables**: useFetch with computed queries, loading/empty states
- **Modals**: v-model:open, responsive fullscreen with VueUse
- **Buttons**: Variant hierarchy (solid/outline/ghost)
- **Dropdowns**: Nested array structure for menu items
- **Toasts**: useToast() for all user feedback
- **Accessibility**: ARIA labels, keyboard navigation
