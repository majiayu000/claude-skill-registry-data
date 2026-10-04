---
name: "mermaid-view"
description: "Convert Mermaid diagram code into high-fidelity SVG or PNG preview. Generate diagrams for architecture, flowcharts, sequence diagrams, and class models directly from CLI."
version: "1.0.0"
author: "Human Skills Team"
tags: ["mermaid", "diagram", "visualization", "png", "svg", "architecture", "flowchart"]
trigger_patterns:
  - "mermaid"
  - "mermaid diagram"
  - "generate diagram"
  - "render mermaid"
  - "mermaid-view"
  - "architecture diagram"
---

# mermaid-view — Diagram Renderer & Preview Generator

> *"Turn Mermaid code into crisp, high-fidelity PNG and SVG images instantly."*

---

## Overview

`mermaid_view` is a standalone tool that converts any Mermaid diagram code (flowcharts, sequence diagrams, class diagrams, state machines, entity-relationship diagrams, Gantt charts, etc.) into high-resolution **PNG** or **SVG** image files.

---

## Tool Reference: `mermaid_view`

### 📝 Arguments

| Argument | Type | Required | Description |
|:---|:---:|:---:|:---|
| `diagram_code` | `string` | **Yes** | The raw Mermaid code to render (e.g. `flowchart TD\n A --> B`). Markdown code fences (\`\`\`mermaid) are automatically stripped if present. |
| `path` | `string` | No | Target directory or explicit file path (e.g. `/home/user/my-project` or `/home/user/my-project/arch.png`). Defaults to current directory. |
| `preview` | `string` | No | Output format: `"png"` (default) or `"svg"`. |
| `file_name` | `string` | No | Optional custom file name (e.g. `architecture.png`). Defaults to `diagram.<preview>`. |
| `theme` | `string` | No | Mermaid theme: `"default"`, `"dark"`, `"neutral"`, `"forest"`, or `"base"`. Default: `"default"`. |

---

## Supported Diagram Types
* Flowcharts (`flowchart TD`, `graph LR`)
* Sequence Diagrams (`sequenceDiagram`)
* Class Diagrams (`classDiagram`)
* State Diagrams (`stateDiagram-v2`)
* Entity Relationship Diagrams (`erDiagram`)
* User Journey (`journey`)
* Git Graphs (`gitGraph`)
* Mindmaps (`mindmap`)
* Timelines (`timeline`)

## Usage Examples

### Render PNG, SVG Flowchart, Vector Diagram, Architecture Diagram
```bash
human-skills '{
  "tool_name": "mermaid_view",
  "tool_args": {
    "path": "/home/username/my-project", # e.g. `/home/user/my-project/arch.png`, default is `path`
    "preview": "png", # e.g. `svg`, default is `png`
    "file_name": "diagram.png", # e.g. `architecture.png`, default is `diagram.<preview>`
    "theme": "neutral", # e.g. `dark`, `neutral`, `forest`, `base`, default is `dark`
    "diagram_code": "flowchart TD\n    A[Client] --> B[API Gateway]\n    B --> C[Auth Service]\n    B --> D[Data Service]\n    D --> E[(PostgreSQL)]"
  }
}'
```
