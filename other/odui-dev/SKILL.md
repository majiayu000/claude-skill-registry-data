---
name: odui-dev
description: Run and use the local Open Design UI catalogue while designing or reviewing components. Use when a designer or developer needs live previews, tokens, states, examples, code, HMR or screenshots.
---

# Develop with Open Design UI

Read [AGENTS.md](../../../AGENTS.md) and the [component guide](../../../packages/open-design-ui/README.md). The catalogue uses the same component source as Studio and does not require the Studio backend.

1. From the repository root run `npm ci` once when dependencies are missing, then run `npm run components:dev`.
2. Open the local URL printed by Vite. Use Components for the live state matrix, Design tokens for semantic values and Contribution guide for the workflow.
3. Use Preview and Code on a component page. Check keyboard, focus, disabled/loading, both themes and relevant narrow widths. Use Copy to Agent or Copy migration prompt when handing work to another Agent.
4. Keep the dev server running while editing. Saving a component or example should update the page. If a change needs Studio behavior, use `odui-apply` after the catalogue check.
5. For a shareable artifact run `npm run components:build` and inspect the built route before reporting it.

Do not treat a catalogue preview as proof that a Studio consumer is correct. The real consumer and its focused test remain part of the handoff.
