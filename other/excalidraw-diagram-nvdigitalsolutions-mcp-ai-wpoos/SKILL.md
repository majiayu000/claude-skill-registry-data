---
type: Skill
name: excalidraw-diagram
description: Generate production-quality Excalidraw architecture diagrams from natural language. Visual structure maps to conceptual structure — fan-out for one-to-many, timelines for sequences, convergence for aggregation. Includes self-validation via Playwright render review.
license: MIT
compatibility: Claude Code, Cursor, Gemini CLI, Codex CLI
---

# Excalidraw Diagram Generator

Generate visual architecture diagrams, sequence diagrams, data-flow diagrams, and system maps from natural language descriptions using Excalidraw's JSON format.

## Install

```bash
npx skills add https://github.com/coleam00/excalidraw-diagram-skill --skill excalidraw-diagram
```

## When to Use

- Documenting architecture decisions for the repository
- Explaining system design to stakeholders or new team members
- Visualising data flow, API call sequences, or deployment topology
- Creating diagrams for RFCs, ADRs, and design documents
- Generating animated GIFs from Excalidraw exports for presentations

## Design Philosophy

**Diagrams that argue, not display.** Every shape and grouping mirrors the concept it represents:

| Concept | Visual pattern |
|---------|---------------|
| One-to-many (fan-out) | Single node → multiple branches |
| Sequential steps | Left-to-right timeline or top-to-bottom flow |
| Aggregation (many-to-one) | Convergence funnel |
| Subsystems / bounded contexts | Grouped rectangles with labelled borders |
| External dependencies | Dashed borders or cloud shapes |
| Data stores | Cylinder shapes |

Never default to a uniform grid of identical cards. Let the shape of the diagram communicate the shape of the system.

## Output Format

Generate Excalidraw JSON that can be opened directly in https://excalidraw.com or the Excalidraw VS Code extension.

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "id": "el1",
      "type": "rectangle",
      "x": 100, "y": 100,
      "width": 160, "height": 60,
      "label": { "text": "API Gateway" },
      "strokeColor": "#1e1e2e",
      "backgroundColor": "#cba6f7",
      "fillStyle": "solid"
    }
  ],
  "appState": { "viewBackgroundColor": "#ffffff" }
}
```

Save the JSON to a `.excalidraw` file:

```bash
cat > architecture.excalidraw << 'EOF'
{ ...generated JSON... }
EOF
```

## Self-Validation Loop

After generating the JSON, validate the rendered output:

```bash
# Render to PNG using Playwright
npx playwright screenshot --url "https://excalidraw.com/#json=..." output.png

# Or use the excalidraw-utils CLI
npx excalidraw-utils export architecture.excalidraw --output output.png
```

Review the rendered image for:

- Overlapping labels or elements
- Arrows pointing to wrong nodes
- Unbalanced whitespace (cluster elements or spread them)
- Missing labels on key flows

Fix any layout issues before presenting the diagram.

## Example Prompts

```
Create an Excalidraw diagram showing how a request flows through
our API gateway, auth middleware, and downstream microservices.

Generate an architecture diagram for a multi-tenant SaaS with
separate database schemas per tenant and a shared analytics layer.

Draw a sequence diagram for our OAuth2 PKCE flow including
the browser, authorisation server, and resource server.

Create a data-flow diagram showing how webhook events move from
Stripe through our queue, processor, and into the database.
```

## Brand Customisation

Store your colour palette in `references/color-palette.md`:

```markdown
# Colour Palette
- Primary:   #7c3aed (purple)
- Secondary: #2563eb (blue)
- Success:   #16a34a (green)
- Warning:   #d97706 (amber)
- Error:     #dc2626 (red)
- Surface:   #f8fafc (light grey)
- Text:      #1e293b (dark)
```

Reference this file in every diagram generation prompt to keep visuals consistent across the project.

## Tips

- Annotate key flows with real API paths or JSON payloads inline, not placeholder text
- For large systems, generate one diagram per bounded context and a high-level overview
- Use Excalidraw's "hand-drawn" style for exploratory/draft diagrams; clean style for documentation
- Export to SVG for embedding in Markdown; PNG for presentations
- Version-control `.excalidraw` files in the repository alongside the code they describe
