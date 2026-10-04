---
name: Figma MCP
description: >
  Guide for working with Figma designs via the Figma MCP server — translating
  designs to code, pushing code back to Figma, building design systems, and
  managing Code Connect mappings. Use this skill whenever the user mentions
  Figma, wants to implement a Figma design, convert UI to Figma layers,
  build or audit a design system in Figma, set up Code Connect, or work with
  design tokens and variables from Figma. Also triggers on Figma file URLs
  (figma.com/design/..., figma.com/file/...) or references to Figma frames,
  components, or variables.
---

# Figma MCP

Work with Figma designs through the Figma MCP server (`https://mcp.figma.com/mcp`).
The server exposes 16 tools for reading design data and writing back to the canvas.

**Node ID format**: Figma URLs use hyphens in `node-id` parameters (e.g.,
`node-id=1-2`), but MCP tools expect colon-separated IDs (e.g., `nodeId: "1:2"`).
Always convert hyphens to colons when extracting node IDs from URLs.

## Prerequisites

- **MCP server**: Added via `claude mcp add --transport http figma https://mcp.figma.com/mcp`
  or the Claude plugin (`claude plugin install figma@claude-plugins-official`)
- **Authentication**: OAuth via `/mcp` → Figma → Authenticate (one-time browser flow)
- **Seat requirement**: Dev or Full seat on a paid Figma plan for full rate limits.
  Free/Starter plans get 6 tool calls/month.

## Tool Reference

### Reading designs

| Tool | When to use |
|------|-------------|
| `get_design_context` | Primary tool. Returns styling info (defaults to React + Tailwind). Pass `nodeId` from a Figma URL. Customizable to Vue, HTML/CSS, iOS, etc. |
| `get_metadata` | Lightweight XML of layer structure — use first on large designs to pick which nodes to inspect in detail |
| `get_screenshot` | Visual screenshot of a selection — useful for layout fidelity checks |
| `get_variable_defs` | Extract design tokens (colors, spacing, typography) used in the selection |
| `get_code_connect_map` | Retrieve existing Code Connect mappings (Figma node → codebase component) |
| `get_code_connect_suggestions` | Auto-detect potential Code Connect mappings between Figma and your code |
| `search_design_system` | Query connected design libraries for reusable components and variables |
| `get_figjam` | Read FigJam diagram content as XML with node screenshots |
| `whoami` | Check authenticated user identity and plan info |

### Writing to Figma

| Tool | When to use |
|------|-------------|
| `use_figma` | General-purpose write tool — create, edit, delete any Figma object. Executes Plugin API JavaScript on the canvas. |
| `generate_figma_design` | Capture a running web UI and convert it to editable Figma layers ("Code to Figma") |
| `generate_diagram` | Create FigJam diagrams from Mermaid syntax |
| `create_new_file` | Create a blank Figma Design or FigJam file in drafts |
| `add_code_connect_map` | Create mappings between Figma nodes and code components |
| `send_code_connect_mappings` | Finalize Code Connect mappings after reviewing suggestions |
| `create_design_system_rules` | Generate CLAUDE.md / AGENTS.md with design system conventions |

## Core Workflows

### 1. Figma → Code (design-to-code)

This is the most common workflow. A designer creates a UI in Figma, and you
translate it into production code.

**Steps:**

1. The user shares a Figma frame URL (contains `node-id` parameter).
   Extract and convert the node ID (see Node ID format above).

2. For large or complex designs, call `get_metadata` first to understand the
   layer structure without burning tokens on full styling data. Pick the
   specific nodes you need.

3. Call `get_design_context` on the target node(s). By default this returns
   React + Tailwind code — specify a different framework if the user's project
   uses something else.

4. Optionally call `get_screenshot` for a visual reference to verify layout
   fidelity while implementing.

5. **Adapt the output to the project's stack.** The MCP returns reference code,
   not production-ready code. Map to existing components, follow the project's
   naming conventions, and use the project's design token system rather than
   hard-coded values.

6. If Code Connect is set up, `get_design_context` returns your *actual*
   component code instead of generated approximations — much higher fidelity.

**Example prompt:** "Implement this Figma design: https://figma.com/design/abc123?node-id=42-1337"

### 2. Code → Figma (code-to-design)

Push a running web UI back into Figma as editable layers. Useful for
designer-developer handoff in reverse.

1. Build and preview the feature locally (e.g., `localhost:3000`)
2. Call `generate_figma_design` — it captures the live UI and creates
   editable Figma layers
3. The designer can then refine, annotate, and explore variants in Figma
4. Pull updated designs back via Workflow 1

### 3. Design System in Figma

Build or update a complete design system in Figma from your codebase.
This is a phased, multi-call workflow:

- **Phase 0 — Discovery**: Analyze codebase tokens and components; inspect
  existing Figma file structure
- **Phase 1 — Foundations**: Create variable collections (primitive + semantic tokens)
- **Phase 2 — Typography**: Load fonts, create text styles
- **Phase 3 — Components**: Build one component per `use_figma` call, combine as variants
- **Phase 4 — Documentation**: Create documentation pages

Checkpoint with the user between phases — this can involve 20-100+ tool calls.

### 4. Code Connect Setup

Map Figma components to their code counterparts so future `get_design_context`
calls return real component code.

1. Call `get_code_connect_suggestions` with the Figma file URL
2. Review each suggestion — match Figma components to codebase files
3. Call `send_code_connect_mappings` to finalize

## Writing to the Canvas — Key Rules

When using `use_figma` to modify the Figma canvas, follow these Plugin API rules:

- **Colors are 0–1 floats**, not 0–255. `{ r: 1, g: 0, b: 0 }` is red.
- **Use `return {}` at the end** — `figma.closePlugin()` crashes the MCP
  execution context, so always return an object instead
- **Top-level await** is supported — no async IIFE wrappers needed
- **Load fonts before text changes**: `await figma.loadFontAsync({ family: "Inter", style: "Regular" })`
- **Build incrementally**: One section per `use_figma` call. Validate with
  `get_screenshot` after each call before proceeding.
- **Prefer targeted fixes over rebuilding entire screens** — rebuilding is
  expensive (one `use_figma` call per section) and risks losing manual
  adjustments the designer made

## Error Handling

- **Auth failure**: Call `whoami` to verify authentication status. If expired,
  tell the user to re-authenticate via `/mcp` → Figma → Authenticate.
- **Rate limit (free plan)**: Warn the user immediately — free/Starter plans
  only get 6 tool calls/month. Batch questions and use `get_metadata` to plan
  before committing expensive calls like `get_design_context`.
- **Node not found**: Verify the `nodeId` format (colon-separated, e.g., "1:2",
  not hyphenated). Confirm the URL points to the correct file. Ask the user to
  re-copy the link with "Copy link to selection."
- **`use_figma` script error**: Read the error message carefully. Common causes:
  missing font load, wrong color format (0-255 vs 0-1), or referencing nodes
  that don't exist yet. Fix the specific issue and retry — do not restart the
  entire script.

## Tips

- **Start small.** Begin with a single component or frame, not an entire page.
  Iterate outward once the base component is working.
- **Selection-based URLs.** Right-click a frame in Figma → "Copy link to
  selection" for the most precise results.
- **Token management.** `get_design_context` on large frames can return a lot
  of data. Use `get_metadata` first to scope down to specific nodes.
- **Design tokens over hard-coded values.** Call `get_variable_defs` to extract
  the design token system, then use those tokens in your implementation rather
  than copying raw hex colors or pixel values.
- **Check Code Connect first.** If the project has Code Connect set up,
  `get_code_connect_map` tells you which Figma components already map to code —
  no need to re-implement those from scratch.
