---
name: superpowers-sage:sage-design-system
description: >
  Design system implementation in Sage/Tailwind v4 — Figma to @theme tokens,
  design tokens CSS, Tailwind v4 @theme, color tokens, typography tokens,
  spacing scale, Blade UI components, kitchensink page, design-to-code,
  @layer base @layer components, CSS custom properties, resources/css/app.css,
  Paper MCP, Figma MCP, design file to code, SVG icons, responsive layout,
  design system audit, UI component library, atom design, layout components
user-invocable: true
argument-hint: "[design tool URL or path, or 'detect' to auto-detect]"
---

# Sage Design System — Visual Foundation

Establish the complete visual foundation of a Sage/Acorn theme: design tokens → UI atoms → layout components → kitchensink → structural layouts. This must run before any block, view, or page implementation.

**Announce at start:** "I'm using the sage-design-system skill to establish the visual foundation."

## When to use

- **Standalone**: user invokes `/sage-design-system` at project start
- **Auto-gate from `/architecting`**: before any architecture discovery, `/architecting` checks if design system is validated (kitchensink route exists + `design-tokens.css` present). If not, it invokes this skill first and waits.
- **Resuming**: if some phases are already complete, detect which files exist and skip completed phases

## Inputs

$ARGUMENTS

If a design tool URL or path is provided, use it. Otherwise invoke `/designing` to detect the active design tool (Figma / Paper / Pencil / Stitch).

---

See [references/tokens-setup.md](references/tokens-setup.md) for design token extraction workflow.

See [references/component-phases.md](references/component-phases.md) for component implementation phases.

---

## Completion

After all phases:

1. Confirm `resources/css/design-tokens.css` exists with traceability comments
2. Confirm `resources/views/components/ui/` has all 5 atoms
3. Confirm `resources/views/components/layout/` has all 5 structure components
4. Confirm kitchensink screenshot was taken and saved
5. Commit:

```bash
git add resources/css/design-tokens.css \
        resources/views/components/ui/ \
        resources/views/components/layout/ \
        resources/views/kitchensink.blade.php \
        routes/web.php \
        docs/plans/<active-plan>/assets/kitchensink-ref.png
git commit -m "feat(theme): design system foundation — tokens, ui, layout components, kitchensink"
git push
```

**Do NOT proceed to `/architecting` or `/building` until this commit exists.**
