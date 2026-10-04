---
name: excalidraw
description: Generate Excalidraw architecture diagrams from natural language descriptions. Use when creating system diagrams, architecture visualizations, data flow diagrams, or when user mentions "diagram", "excalidraw", "draw architecture", "visualize system", or "generate diagram".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Excalidraw Diagram Generator

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

You generate production-quality Excalidraw diagrams from natural language descriptions or codebase analysis. Diagrams should argue, not just display — visual structure maps to conceptual structure.

## Process

### Step 1: Understand What to Diagram

1. **From description** — Parse the user's natural language description
2. **From codebase** — Analyze source code to extract component relationships
3. **Determine diagram type**:
   - System architecture (components + connections)
   - Data flow (how data moves through the system)
   - Sequence diagram (request lifecycle)
   - Deployment topology (infrastructure layout)
   - Entity relationship (data model)

### Step 2: Map Concepts to Visual Structure

Apply these design principles:
- **Fan-out structures** for one-to-many relationships
- **Timeline/sequence layouts** for sequential flows
- **Convergence shapes** for aggregation points
- **Grouping boxes** for bounded contexts or services
- **Color coding** for different concerns (data stores = blue, services = green, external = orange, clients = purple)
- **Never use uniform card grids** — structure must reflect the actual relationships

### Step 3: Generate Excalidraw JSON

Generate a valid Excalidraw JSON file with:
- Properly positioned elements (no overlaps)
- Arrow connections between related components
- Consistent font sizes (title: 28, component: 20, label: 16, annotation: 14)
- Adequate spacing (minimum 40px between elements)
- Grouped related elements

### Step 4: Self-Validate

Before delivering, check:
- [ ] No overlapping text or elements
- [ ] All arrows connect to the correct source/target
- [ ] Layout is balanced (not lopsided)
- [ ] Labels are readable (not truncated)
- [ ] Color usage is consistent and meaningful

## Color Palette

```
Primary (services):     #1e90ff (DodgerBlue)
Secondary (data):       #10b981 (Emerald)
Accent (external):      #f59e0b (Amber)
Danger (critical path): #ef4444 (Red)
Neutral (infra):        #6b7280 (Gray)
Client (frontend):      #8b5cf6 (Purple)
Background groups:      #f0f9ff (LightBlue), #f0fdf4 (LightGreen), #fefce8 (LightYellow)
```

## Element Templates

### Service Box
```json
{
  "type": "rectangle",
  "width": 180,
  "height": 60,
  "strokeColor": "#1e90ff",
  "backgroundColor": "#dbeafe",
  "fillStyle": "solid",
  "roundness": { "type": 3 }
}
```

### Data Store (cylinder shape via rectangle + label)
```json
{
  "type": "rectangle",
  "width": 160,
  "height": 50,
  "strokeColor": "#10b981",
  "backgroundColor": "#d1fae5",
  "fillStyle": "solid",
  "roundness": { "type": 3 }
}
```

### Arrow Connection
```json
{
  "type": "arrow",
  "strokeColor": "#6b7280",
  "strokeWidth": 2,
  "points": [[0, 0], [200, 0]]
}
```

## Output

Save the diagram to: `{project_path}/docs/diagrams/{name}.excalidraw`

Report to user:
- **File saved**: path to .excalidraw file
- **Components**: count of elements in diagram
- **Open with**: "Open in Excalidraw (excalidraw.com) or VS Code Excalidraw extension"
- **Export**: "Use Excalidraw to export as PNG/SVG for documentation"

## Tips for Quality Diagrams

1. **Include real names** — Use actual service names, endpoint paths, table names from the codebase
2. **Show data on arrows** — Label what data flows between components (e.g., "JWT token", "order payload")
3. **Mark async vs sync** — Dashed arrows for async, solid for sync
4. **Annotate decisions** — Add small text notes explaining non-obvious design choices
5. **Group by deployment boundary** — Show what runs in the same container/server vs separate

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
