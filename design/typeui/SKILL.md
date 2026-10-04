---
name: typeui
description: Use TypeUI with Grok to access project design skills, brand kits, UI prompts, and layout variations through the TypeUI MCP server when creating or refining user interfaces.
license: MIT
metadata:
  author: Bergside LLC
  homepage: https://www.typeui.sh
---

# TypeUI for Grok

Use this skill when the user wants Grok to build, redesign, or refine UI with TypeUI context.

## What TypeUI Provides

- Project design skills for consistent visual direction.
- Brand kits with project name, logo, typography, and brand color tokens.
- UI prompt libraries for common interface sections and full-product flows.
- Layout variation guidance for producing better options before implementation.

## How to Use TypeUI

1. Prefer TypeUI MCP tools when they are available in the session.
2. Ask the user which TypeUI project or design skill to use if the request does not specify one.
3. Apply the selected project context before choosing colors, type, spacing, component tone, or page composition.
4. Treat brand kit values as brand parameters only: logo, project name, typography, and brand colors.
5. Treat the design skill as the source of UI style, component behavior, visual hierarchy, spacing, and interaction patterns.

## MCP Server

This plugin registers the TypeUI remote MCP server:

```text
https://mcp.typeui.sh
```

If the server is not available in the current Grok session, connect it manually:

```bash
grok mcp add --transport http typeui https://mcp.typeui.sh
```

## Prompt Examples

- Use my TypeUI project and build a landing page.
- Generate three pricing section variations with TypeUI.
- Redesign this dashboard using my TypeUI design skill.
- Pull the TypeUI context for this project before changing the UI.
