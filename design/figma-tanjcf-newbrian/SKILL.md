---
name: figma
description: Use when the user wants Figma/FigJam work in NewBrain — generate UI designs, flowcharts, architecture diagrams, design-to-code, or design-system updates that should appear in a Figma file. Also use when a Figma URL is pasted. Without Figma auth, guide the user to connect MCP/token or fall back to Mermaid/Visualize for local diagrams.
metadata:
  short-description: Figma designs and FigJam diagrams
---

# Figma (NewBrain builtin)

Use this router skill for any Figma-related request in NewBrain.

## Auth gate (required for “appear in Figma”)

To **create or edit nodes inside the user’s Figma/FigJam cloud file**, NewBrain must have Figma tools available:

1. Prefer **Figma Desktop MCP** (`http://127.0.0.1:3845/mcp`) via **设置 → MCP → ＋ Figma Desktop MCP** (enable desktop MCP in Figma Dev Mode first), **or**
2. Another connected **Figma MCP** (e.g. remote `https://mcp.figma.com/mcp` if OAuth works), **or**
3. Set **`FIGMA_ACCESS_TOKEN`** in settings → 环境 (Personal Access Token) as a secondary helper.

If neither MCP tools nor token-backed access is available:

- Say clearly that cloud Figma write is unavailable until auth is configured.
- Offer a **local fallback**: render a Mermaid flowchart in chat, or use the **Visualize** builtin for a local HTML diagram.
- Do **not** claim the diagram was written into Figma.

## Skill routing

Load the matching specialized skill under this plugin when needed:

| Intent | Skill |
|--------|--------|
| Create/edit nodes via Plugin API scripts | `figma-use` |
| FigJam boards | `figma-use-figjam` |
| Slides | `figma-use-slides` |
| Motion | `figma-use-motion` / `figma-implement-motion` |
| Design → code | `figma-design-to-code` |
| Generate UI design | `figma-generate-design` |
| Design system / components | `figma-generate-library` |
| **Flowchart / architecture / sequence → FigJam** | `figma-generate-diagram` |
| New Figma/FigJam/Slides file | `figma-create-new-file` |
| Code Connect | `figma-code-connect` |
| SwiftUI | `figma-swiftui` |

## Flowchart guidance

When the user asks for a flowchart / architecture / sequence diagram:

1. If Figma MCP tools such as `generate_diagram` / `use_figma` exist → follow `figma-generate-diagram` so the result **appears in FigJam**.
2. Otherwise → produce Mermaid in chat (and optionally Visualize HTML), and explain how to connect Figma for cloud write.

## Safety

- Never invent Figma file URLs or claim cloud writes without tool evidence.
- Keep `LICENSE.txt` obligations; do not strip attribution when copying assets.
- Prefer smallest edits; confirm destructive deletes with the user.
