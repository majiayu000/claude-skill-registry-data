---
name: odui-build
description: Create or evolve an Open Design UI component and its catalogue entry. Use when a designer or developer adds a control, changes its API, states, tokens, examples or adoption status.
---

# Build an Open Design UI component

Read [AGENTS.md](../../../AGENTS.md), the [component guide](../../../packages/open-design-ui/README.md), the [shared design system](../../../packages/design-system/README.md) and the registry before editing.

1. Start with the real use case. Define the states, keyboard behavior, accessible contract, responsive behavior and token roles before writing the recipe.
2. Change the control source in `packages/open-design-ui`. Add the component source, registry item, interactive example, API notes and a real Studio consumer in the same change. Use the `open-design-ui/*` alias from the registry.
3. Register a new control as `adoption.mode: "opt-in"` with a review condition. Keep it optional until one representative Studio use case is verified. Change to `enforced` only when the native rule and baseline are updated in the same change.
4. Keep feature data, domain validation and persistence in the consumer. The component owns shared visual states and interaction mechanics.
5. Run `npm run design:check`, `npm run components:build`, `npm run typecheck:studio` and focused consumer tests. Use `odui-dev` to inspect both themes, keyboard states and the narrow layout.

A component is ready for review only when its preview, registry entry, real consumer and verification evidence are present.
