---
name: ui-figma
description: "Routes Figma creation, editing, inspection, connection, components, or motion to the matching Figma workflow."
---

# UI Figma Router

Use this skill for any Figma-related UI work.

Use complete original skills from the currently exposed Figma plugin. Read
their mandatory prerequisites and use the host's actual invocation. Bible owns
only routing and scope policy. Keep native skill files, references and tooling
under native ownership. Missing skills or a missing Figma connection require
official plugin setup and verified exposure; do not substitute a local summary.

## Workflow

1. Identify the Figma task.
2. Pick the smallest matching Figma skill.
3. Read that skill's `SKILL.md`.
4. Follow the Figma API or design-system workflow from that skill.

## Routing

- Implement Figma as code -> `figma-to-code`
- Sync implemented UI or component mappings back to Figma -> `code-to-figma`
- Create or update screen/view in Figma -> `figma:figma-generate-design`
- Create or update design system/component library -> `figma:figma-generate-library`
- Work directly with Figma Plugin API -> `figma:figma-use`
- Add or inspect motion in Figma -> `figma:figma-use-motion`
- Create or edit Code Connect mappings -> `figma:figma-code-connect`
- Create a new blank Figma file -> `figma:figma-create-new-file`

## Rule

If the prompt also needs evidence or implementation, name `ui-research` or
`ui-build` as the next skill to read after this one. If the prompt asks for
implementation fidelity, name `playwright-visual-qa` after build.
