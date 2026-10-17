---
name: diagram-generator
description: |
  Generate diagrams of any kind from a description, ticket, spec, or file. Outputs Mermaid syntax (renders natively in GitHub, Notion, Confluence, Obsidian, Slack with apps) plus an optional single-file HTML preview that renders the diagram in the browser.

  Use this skill when the user says:
  - "draw a flowchart", "create a diagram", "visualize this flow"
  - "sequence diagram", "state diagram", "ER diagram", "class diagram"
  - "user journey", "mindmap", "timeline", "gantt", "org chart"
  - "sankey", "quadrant chart", "git graph"
  - or pastes a ticket / spec / description and asks for a visual
  Picks the right Mermaid diagram type for the input, asks if ambiguous, then emits clean syntax + an optional preview file.
---

# Diagram Generator

Turn any input into a clean diagram. Supports the full Mermaid diagram set so one skill handles flowcharts, sequence diagrams, state machines, ER diagrams, journeys, mindmaps, timelines, gantt charts, sankey, quadrants, class diagrams, and git graphs.

## Inputs

- **Ticket / PRD / spec** — read it and pick the right diagram type.
- **File path** — read the file and diagram from contents.
- **Verbal description** — diagram directly from the prompt.
- **Existing diagram** — refactor / restyle / fix.

## Workflow

### Step 1 — Pick the diagram type

If the input is unambiguous, pick directly. Otherwise ask which fits best:

| User intent | Mermaid type |
|---|---|
| Process flow, decision tree, "if X then Y" | `flowchart` |
| API calls, message passing, who-talks-to-whom over time | `sequenceDiagram` |
| Object lifecycle, finite-state machine | `stateDiagram-v2` |
| Database schema, entities + relationships | `erDiagram` |
| End-to-end customer/user experience with sentiment | `journey` |
| Hierarchical brainstorm, taxonomy, idea tree | `mindmap` |
| Dated events, milestones | `timeline` |
| Project schedule with durations + dependencies | `gantt` |
| Flow of quantity between sources/targets | `sankey-beta` |
| 2x2 categorization (importance/urgency, effort/impact) | `quadrantChart` |
| OOP class hierarchy with methods | `classDiagram` |
| Git branching strategy | `gitGraph` |

### Step 2 — Extract the diagram content

From the input, pull out the right primitives for the chosen type:
- **Flowchart:** decision points, actions, states, edge cases, scenarios.
- **Sequence:** actors, messages, ordering, async vs sync.
- **State:** states, transitions, triggers, terminal states.
- **ER:** entities, attributes, relationships, cardinality.
- **Journey:** stages, tasks per stage, sentiment scores.
- **Mindmap:** root concept + branches.
- **Timeline:** sections + events per section.
- **Gantt:** sections + tasks with dates/durations + dependencies.
- **Sankey:** source → target → value rows.
- **Quadrant:** axis labels + items with (x, y) scores.
- **Class:** classes + members + inheritance/composition.
- **GitGraph:** branches, commits, merges.

If multiple distinct scenarios exist (e.g., happy path + error path), produce SEPARATE diagrams rather than one mega-diagram.

### Step 3 — Emit Mermaid syntax

Always wrap output in:
````markdown
```mermaid
{type-specific code}
```
````

Follow the type-specific rules below.

### Step 4 — Offer a preview file (optional)

After printing the Mermaid block, ask: *"Want me to generate a single-file HTML preview that renders this locally?"*

If yes, write `diagram.html` to the current directory using the template under "HTML preview template" below.

## Type-specific rules

### Flowchart

- **Line breaks in labels:** ALWAYS `<br>`, NEVER `\n`.
- **Node shapes:**
  - `([text])` — start / end (stadium)
  - `[text]` — action / process
  - `{text}` — decision
  - `[[text]]` — subroutine
  - `[(text)]` — database
  - `((text))` — circle (event)
- **Direction:** `flowchart TD` for processes, `flowchart LR` for timelines/pipelines.
- **Edge labels:** `-- text -->` for conditional paths.
- **Colors (apply via `style` lines at the end):**
  - `fill:#4CAF50,color:#fff` — success / start (green)
  - `fill:#EF5350,color:#fff` — error / blocked (red)
  - `fill:#FF9800,color:#fff` — warning / modified (orange)
  - `fill:#2196F3,color:#fff` — informational (blue)
- **Subgraphs:** group related items with `subgraph Name ... end`.
- **No special characters** (quotes, colons, pipes) inside node labels.
- **Node text:** max 4 lines.

### Sequence diagram

- Use `participant X as Display Name` to set readable labels.
- Use `->>` for sync, `-->>`  for async, `--x` for failed.
- Use `Note over X,Y: text` for callouts.
- Use `loop`, `alt / else`, `par`, `opt` for control flow.
- Use `activate X` / `deactivate X` to show lifelines.

### State diagram (v2)

- Use `[*] --> StateName` for start, `StateName --> [*]` for end.
- Use `state ChoiceName <<choice>>` for branching.
- Use composite states for nesting: `state Group { ... }`.

### ER diagram

- Cardinality glyphs: `||--o{` (one-to-many), `}o--o{` (many-to-many), `||--||` (one-to-one).
- Use lowercase plural entity names.
- Attribute lines: `{type} attributeName "comment"`.

### Journey

- Three columns per task: `Task name: <score 1-5>: Actor1, Actor2`.
- Group tasks under `section Name`.

### Mindmap

- Indentation defines hierarchy.
- Node shapes: `((text))`, `[text]`, `(text)`, `{{text}}`.

### Timeline

- `section Name` then events as `: YYYY : event text`.

### Gantt

- Always start with `dateFormat YYYY-MM-DD`.
- Tasks: `Name :status, id, start, duration` or `Name :status, id, after otherId, duration`.
- Status keywords: `done`, `active`, `crit`.

### Sankey-beta

- One source-target-value row per line: `Source,Target,42`.
- No header. Comma-separated. Values numeric.

### Quadrant chart

- Required: `title`, `x-axis Low --> High`, `y-axis Low --> High`, four quadrant labels.
- Items: `Item Name: [x, y]` where x and y are 0-1.

### Class diagram

- `Class : +method()` for public, `-` private, `#` protected.
- Relationships: `<|--` inherits, `*--` composition, `o--` aggregation, `-->` association.

### GitGraph

- `commit`, `branch name`, `checkout name`, `merge name`.
- Order matters; reads top-to-bottom.

## Output structure

```markdown
## {Diagram Title}

**Summary:** {one-line description of what the diagram shows}

```mermaid
{code}
```

**Key callouts:**
- {anything non-obvious about the diagram}
```

If multiple diagrams (e.g., happy + error paths), use a header per diagram and render each separately.

## HTML preview template

When the user asks for a local preview, write this single file (no build, no npm; mermaid loaded from CDN):

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Diagram preview</title>
<style>
  body{margin:0;padding:48px;font:16px/1.5 system-ui,sans-serif;background:#F5F1EA;color:#15140F}
  .wrap{max-width:1100px;margin:0 auto}
  h1{font-weight:500;font-size:28px;margin:0 0 24px}
  .mermaid{background:#fff;border:1px solid #D8D2C5;border-radius:10px;padding:24px;overflow:auto}
</style>
</head>
<body>
  <div class="wrap">
    <h1>{TITLE}</h1>
    <pre class="mermaid">
{MERMAID_CODE}
    </pre>
  </div>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true, theme: 'base', themeVariables: {
      primaryColor: '#F5F1EA', primaryTextColor: '#15140F', primaryBorderColor: '#15140F',
      lineColor: '#15140F', fontFamily: 'system-ui, sans-serif'
    }});
  </script>
</body>
</html>
```

Replace `{TITLE}` and `{MERMAID_CODE}` with the actual content. Preview opens directly in the browser (file:// works; no server needed).

## Anti-Patterns

- Don't pick the wrong diagram type to "force fit" the input — ask if it's ambiguous.
- Don't cram multiple scenarios into one diagram; split them.
- Don't use `\n` for line breaks in flowchart node labels — always `<br>`.
- Don't put quotes, colons, or pipes inside node labels (they break Mermaid).
- Don't skip the `style` lines on flowcharts — color coding makes diagrams scannable.
- Don't reach for D3, ReactFlow, or custom HTML; Mermaid is the right tool for almost every case. (If the user wants the magazine-grade animated process flow, point them to the `interactive-flowchart-builder` skill instead.)
- Don't auto-generate the HTML preview unless the user asks — most users just want the Mermaid block.

## Quality Checklist

- [ ] Picked the right diagram type for the input (flowchart vs sequence vs state vs ...).
- [ ] Mermaid syntax parses cleanly (no unescaped special chars in labels).
- [ ] Distinct scenarios split into separate diagrams.
- [ ] Color/style applied where the diagram type supports it (flowchart, sequence highlights, journey scores).
- [ ] Node text is concise (≤4 lines).
- [ ] Summary line + key callouts included with the diagram.
- [ ] If preview requested, single-file HTML written and opens directly in browser.
