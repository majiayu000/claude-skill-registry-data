---
name: design-system
description: Design, implement, migrate, and validate scalable token and component systems with primitive, semantic, and component layers; themes; states; accessibility.
---

# Design System

Build a source of truth that connects brand decisions to implementable components. Resolve skill-dir to this folder before running bundled scripts.

## Architecture

Use three layers:

1. Primitive tokens: raw palette, type, spacing, radius, elevation, and motion scales.
2. Semantic tokens: intent such as surface, text, border, action, success, warning, and danger.
3. Component tokens: component/part/state decisions that reference semantic tokens.

Never make components depend directly on arbitrary raw values when a semantic role exists.

## Workflow

1. Inventory existing styles, tokens, components, platforms, and brand constraints.
2. Define naming rules and ownership before generating files.
3. Build primitives, then semantic roles, then component mappings.
4. Define default, hover, focus, active, disabled, loading, selected, error, and success states.
5. Create light/dark or product themes by remapping semantic tokens, not duplicating components.
6. Document component anatomy, variants, content rules, keyboard behavior, and responsive behavior.
7. Migrate incrementally and keep compatibility aliases only with an explicit removal plan.
8. Validate contrast, missing references, cycles, invalid values, and raw-value leakage.

Read the matching reference only when needed:

- references/token-architecture.md
- references/primitive-tokens.md
- references/semantic-tokens.md
- references/component-tokens.md
- references/component-specs.md
- references/states-and-variants.md
- references/tailwind-integration.md

## Bundled tools

Use templates/design-tokens-starter.json as a starting structure, not unquestioned truth.

~~~text
node "<skill-dir>/scripts/generate-tokens.cjs" --help
node "<skill-dir>/scripts/validate-tokens.cjs" <tokens-file>
python "<skill-dir>/scripts/html-token-validator.py" <html-file>
~~~

Run generators on a copy or preview path first. Inspect diffs before replacing user-owned token files.

## Output contract

Provide token architecture, naming decisions, component/state coverage, migration impact, validation results, and remaining exceptions.

## Guardrails

- Do not hardcode brand values inside components.
- Do not rename public tokens without a migration map.
- Do not generate a parallel design system when a working source of truth exists.
- Do not claim accessibility from token names alone; verify rendered combinations and states.
- Do not bind instructions to a provider, model, or host-specific path.
