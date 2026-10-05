---
name: decisions-open-design
description: Use Open Design for agent-native UI prototypes, decks, motion, and hand-drawn diagrams — complementary to Decisions Mermaid viewer for technical charts.
---

# Decisions + Open Design

**I am using Open Design when the deliverable is a design artifact (screen, deck, motion clip) — not a Mermaid technical chart.**

Open Design is the open-source Claude Design alternative: local-first desktop app, 150+ `DESIGN.md` systems, skills, plugins, and an MCP server for coding agents.

## When to use Open Design vs Mermaid

| Need | Tool |
|------|------|
| ER diagram, sequence, flowchart, deployment graph | **Decisions Mermaid** (`decisions-mermaid-diagrams`, `/diagram/`) |
| UI screen / prototype in real CSS | **Open Design** Studio → Prototype |
| Pitch deck / slides | Open Design Studio → Deck |
| Hand-drawn / whiteboard / Excalidraw style | Open Design skill `hand-drawn-diagrams` |
| Motion / HyperFrames MP4 | Open Design Studio → HyperFrame |
| Brand-grade still image | Open Design Studio → Image |

## Reference clone

`../reference/open-design` — [nexu-io/open-design](https://github.com/nexu-io/open-design)

Do not vendor the full monorepo into DecisionsAI; run the app or CLI from the reference clone.

## Setup (one-time)

1. **Desktop app (recommended):** [Download release](https://github.com/nexu-io/open-design/releases) or build from `../reference/open-design` (Node 24 + pnpm — see `QUICKSTART.md`).
2. **MCP for Cursor / Codex / Claude Code** (with Open Design daemon running):
   ```bash
   cd ../reference/open-design
   pnpm install   # first time
   od mcp install cursor   # or codex, claude, copilot, …
   ```
3. Recalibrate Decisions harness MCP after install: `bin/setup.py` (merges catalog entries).

Open Design MCP proxies project tools to the local daemon — it is **not** a cloud npx server. The app must be running.

## Workflow in Decisions tickets

1. Clarify artifact type (prototype vs deck vs diagram).
2. If technical structure only → stay in Decisions Mermaid viewer.
3. If UI/product artifact → open Open Design, pick design system + skill, brief in Studio.
4. Export HTML/PDF/PPTX/MP4 from Open Design; link paths in the ticket result packet.

## Diagram skills inside Open Design

The reference repo ships diagram-category skills (`hand-drawn-diagrams`, `d3-visualization`, `frame-flowchart-sticky`, …). Use those for **visual** diagrams; use Decisions Mermaid for **text-native** diagrams the agent can edit in chat and reopen from History.

## Pairing

| Also use | When |
|----------|------|
| `decisions-mermaid-diagrams` | Same ticket needs architecture chart + UI mockup |
| `decisions-visual-plan` | Plan approval before Open Design generation |
| `decisions-design-references` | Mobbin/Refero before UI direction |
| `decisions-ui-ideation` | Ideation pass before Studio work |
