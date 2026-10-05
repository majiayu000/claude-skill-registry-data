---
name: ui-styling
description: Implement and refine accessible, responsive interfaces using an existing component system or utility CSS, with strong state coverage, semantic tokens, dark.
---

# UI Styling

Work with the project's installed framework and component library. Do not replace the stack or add dependencies merely because examples use a particular library.

## Workflow

1. Inspect the existing stack, components, tokens, CSS strategy, breakpoints, and conventions.
2. Identify the smallest reusable component boundary.
3. Define semantic tokens and variants before adding one-off utilities.
4. Implement mobile-first layout and all interaction states.
5. Verify keyboard, screen-reader, contrast, zoom, touch, reduced-motion, and dark-mode behavior.
6. Inspect rendered output at representative widths when browser or visual tools are available.
7. Run the project's formatter, type checks, tests, and accessibility checks.

## Component rules

- Preserve native semantics and labels.
- Keep focus visible and logically ordered.
- Use one source of truth for variants.
- Cover default, hover, focus-visible, active, disabled, loading, selected, error, and success states.
- Keep touch targets and spacing usable on mobile.
- Avoid arbitrary z-index, spacing, color, shadow, and radius values when tokens exist.
- Prefer content-driven layouts over fixed heights.

## References

Read only what the task needs:

- references/shadcn-components.md
- references/shadcn-theming.md
- references/shadcn-accessibility.md
- references/tailwind-utilities.md
- references/tailwind-responsive.md
- references/tailwind-customization.md
- references/canvas-design-system.md

## Bundled helpers

Resolve skill-dir to this folder before running scripts. Preview generated configuration and never overwrite existing project config without reviewing the diff.

~~~text
python "<skill-dir>/scripts/shadcn_add.py" --help
python "<skill-dir>/scripts/tailwind_config_gen.py" --help
~~~

## Output contract

Report the components and tokens changed, responsive/state coverage, accessibility checks, tests run, and remaining visual or framework constraints.

## Guardrails

- Do not install components or packages without checking project policy and user intent.
- Do not copy examples that conflict with the installed framework version.
- Do not hide accessibility regressions behind visual polish.
- Do not hardcode an AI provider, model, or host-specific skill path.
