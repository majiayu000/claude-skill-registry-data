---
name: penpot
category: design
tags: [penpot, mcp, figma-alternative, open-source-design, design-tokens, ui-ux, design-to-code]
risk: safe
description: >-
  Integrate Penpot (the open-source Figma alternative) with AI agents via the official
  Penpot MCP server and Penpot AI Kit. Read design files, inspect layers, audit design
  tokens and accessibility, build screens/decks, and convert designs to production code.
---

# Penpot & Penpot MCP Skill (penpot)

Penpot is the open-source design & prototyping platform for product teams. Using the official **Penpot MCP Server** and the **14 Penpot AI Kit Skills**, agents can read, inspect, create, audit, and translate design files into production code.

## Official Penpot MCP Tools

When connected to `@penpot/mcp-server`, the agent has access to:
1. **`high_level_overview`**: Retrieve the document structure, pages, boards, and component hierarchy of a Penpot file.
2. **`penpot_api_info`**: Query the Penpot Plugin API documentation and type definitions before writing manipulation code.
3. **`execute_code`**: Execute JavaScript/TypeScript against the live Penpot Plugin API inside the active design file to create shapes, apply tokens, build layouts (Flex/Grid), or inspect layers.
4. **`export_shape`**: Render and export any board, component, or layer as PNG/SVG to visually verify design changes.
5. **`import_image`**: Upload and place raster/vector assets directly onto the Penpot canvas.

## Specialized Penpot Skills in This Catalog

Use these companion skills for targeted workflows:
- `penpot-router`: Route design tasks to the right Penpot sub-skill.
- `penpot-foundations`: Set up color palettes, typography scales, spacing, and design tokens.
- `penpot-build-screen`: Construct responsive UI screens using Penpot Flex & Grid Layout.
- `penpot-build-from-code`: Reverse-engineer existing HTML/CSS/React components into editable Penpot boards.
- `penpot-build-deck`: Build presentation slide decks inside Penpot.
- `penpot-component-factory`: Generate reusable multi-variant UI components.
- `penpot-audit-tokens`: Audit boards for raw hex values or off-scale spacing that violate design tokens.
- `penpot-audit-accessibility`: Check contrast ratios, touch targets, and hierarchy.
- `penpot-anti-slop`: Eliminate generic AI design patterns in Penpot canvases.
- `penpot-design-to-code-review`: Compare implemented frontend code against Penpot source boards.
- `penpot-document-handoff`: Generate developer handoff specs and annotations.
- `penpot-design-md`: Sync `DESIGN.md` specifications with Penpot files.
- `penpot-migrate`: Migrate legacy styles or external designs into Penpot token sets.
- `penpot-rename-layers`: Automatically clean up and semantically rename layers across boards.

## References

- See `references/README.md` for Penpot MCP server & plugin bridge setup.
- See `references/prompts.yml` for official system prompts and code execution patterns.
- See `references/multi-user-mode.md` for multi-user remote configuration.
