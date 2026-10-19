---
name: how
description: >-
  Investigate how a feature is implemented on backend or mobile/frontend,
  trace the flow, and generate C4, sequence, activity, ERD, state, and
  file-graph diagrams. Use only when the user invokes /how.
disable-model-invocation: true
---

# Investigate Feature

The user will provide a short feature description. Trace how it works on whatever stack is present (backend, mobile/frontend, or both), explain it with file paths, then generate the diagram HTML.

## Phase 1: Research

Do not search the repo yourself first. Launch **parallel Task subagents** in one turn, then stitch their results. These are built-in agent types, not skills in this pack. The names below are Cursor's; in Claude Code use `Explore` for `explore` and `general-purpose` for `generalPurpose`.

1. Skim only enough to guess which surfaces exist (mobile, backend, or both).
2. Start 2–3 subagents together:

| Subagent | Type | Thoroughness | Job |
| --- | --- | --- | --- |
| Keywords | `explore` | medium | Files, symbols, and call sites matching the feature keywords |
| Backend | `explore` | medium | Routes, handlers, jobs, services, models, tables, queues — skip if no backend |
| Mobile / UI | `explore` | medium | Screens, navigation, view models, hooks, stores, clients, native modules — skip if no UI |

3. If one path is still unclear after they return, launch one `generalPurpose` follow-up to trace that path. Do not start the write-up until the first wave is back.

Each subagent should return: relative paths, package/app name, key functions, and how the files connect. Skip layers that are not in the repo.

## Phase 2: Explain

```
## Feature: [Name]

### How it works
[2-3 sentence end-to-end summary]

### Flow
1. Step → `file path` → what happens
...

### Key Files
| File | Project | Role |
|------|---------|------|
| `path/to/file` | app-or-package | What it does |
```

Add only the sections that research found:

- **Screens / Navigation** — screen, route, how the user gets there
- **Client state** — store, hook, view model
- **Types** — important types or props
- **Database tables** — only if the feature reads or writes a DB

## Phase 3: Diagrams

Write one HTML file: header "[Feature Name] — Codebase Investigation", sticky tab bar, Architecture open first.

| Tab | Include when... |
|-----|-----------------|
| Architecture | Always (C4: Context, Container, Component) |
| Sequence | Always |
| File Graph | Always |
| Activity | Conditional logic, branching, or error paths |
| ERD | Reads or writes database tables |
| State Machine | An entity, screen, or flow has a status/state lifecycle |

### Tab 1: Architecture Overview (C4)

Draw the feature with the C4 model: Context, Container, Component. One Mermaid diagram per level (`C4Context`, `C4Container`, `C4Component`). Do not mix levels. Skip C4 Code — files go on File Graph.

Level switcher inside this tab: **Context** | **Container** | **Component**. Default **Container**. Omit a level only when research found nothing for it.

| Level | Show | Nodes |
| --- | --- | --- |
| Context | People and systems around the feature | `Person`, `Person_Ext`, `System`, `System_Ext`, `SystemDb`, `SystemQueue` |
| Container | Deployable pieces | `Container`, `Container_Ext`, `ContainerDb`, `ContainerQueue` in a `System_Boundary` |
| Component | Modules inside the container that owns the feature | `Component`, `Component_Ext`, `ComponentDb` in a `Container_Boundary` |

A mobile app, web app, API, worker, and database are all containers. Screens, view models, routers, and domain services are components. Use `Rel(from, to, "label")` or `Rel(from, to, "label", "tech")`. Prefer real protocols (`HTTPS`, `SQL`, `navigation`). No `[]` or `<` in titles or labels.

```
C4Container
title Container diagram for Feature
Person(user, "User", "Starts the feature")
System_Boundary(sys, "This system") {
  Container(mobile, "Mobile app", "React Native", "Screens and local state")
  Container(api, "API", "Node.js", "Handles the request")
  ContainerDb(db, "Database", "PostgreSQL", "Stores records")
}
Rel(user, mobile, "Taps action")
Rel(mobile, api, "Calls API", "HTTPS")
Rel(api, db, "Reads and writes", "SQL")
```

### Tab 2: Sequence Flow

Primary use case, chronological. Participants are screens, view models, services, or files. Solid arrows = sync, dashed = async/events/navigation. Group into phases.

### Tab 3: Activity Diagram (conditional)

Branching and error paths. Swim lanes by screen or service. Label each branch.

```json
{
  "swimLanes": [
    { "name": "ServiceA", "file": "path/to/ServiceA.ts" }
  ],
  "nodes": [
    { "id": "start", "type": "start" },
    { "id": "validate", "type": "action", "label": "validate(input)", "lane": "ServiceA", "file": "path/to/file.ts" },
    { "id": "isValid", "type": "decision", "label": "is valid?", "lane": "ServiceA" },
    { "id": "end", "type": "end" }
  ],
  "edges": [
    { "from": "start", "to": "validate" },
    { "from": "validate", "to": "isValid" },
    { "from": "isValid", "to": "end", "label": "yes" }
  ]
}
```

### Tab 4: ERD (conditional)

Tables used by the feature. Mark PK/FK, cardinality, and `usedByFeature` on columns. Include the model or migration path.

```json
{
  "tables": [
    {
      "name": "table_name",
      "file": "path/to/Model.ts",
      "columns": [
        { "name": "id", "type": "UUID", "constraint": "PK", "usedByFeature": true }
      ]
    }
  ],
  "relationships": [
    { "from": "table_a", "to": "table_b", "type": "1:N", "via": "foreign_key_col" }
  ]
}
```

### Tab 5: State Machine (conditional)

Entity, screen, or navigation states. Triggers, guards, and the file that implements each transition. Mark the happy path.

```json
{
  "states": [
    { "name": "created", "description": "Initial state after creation" }
  ],
  "transitions": [
    {
      "from": "created",
      "to": "in_progress",
      "trigger": "start()",
      "guard": "all validations pass",
      "file": "path/to/Service.ts",
      "isHappyPath": true
    }
  ],
  "initialState": "created",
  "finalStates": ["completed", "failed"]
}
```

### File Graph

vis-network graph: drag nodes, scroll to zoom, "Fit view", "Toggle physics", colored groups, click a node for incoming/outgoing edges.

10–30 high-signal files. Prefer direct dependencies.

**Include:**
- Entry points: screens, navigation routes, API routes, jobs, consumers
- UI, view models, hooks, stores
- Domain/services
- Data access, models, local cache, native modules
- Shared types, flags, or clients on the primary path

**Exclude:**
- Test files
- Translation-only files
- Generated files and lock files
- Re-export-only barrel files, unless they do meaningful wiring

#### File Graph data shape

```javascript
{
  nodes: [
    {
      id: 'shortId',
      label: 'FileName.ts',
      group: 'ui' | 'nav' | 'state' | 'api' | 'service' | 'data' | 'native' | 'lib' | 'external' | 'model' | 'migration',
      path: 'relative/path/from/repo/root',
      meta: 'One-line description of this file in the feature flow',
    }
  ],
  edges: [
    { from: 'screen', to: 'api', label: 'calls create()' }
  ],
  levels: {
    screen: 0,
    api: 1
  }
}
```

Edge labels: `imports`, `calls`, `validates`, `persists`, `reads`, `writes`, `emits`, `listens`, `registers`, `publishes`, `consumes`. Top-down `levels`: entry points above dependencies.

### HTML

- Mermaid for Architecture (`C4Context` / `C4Container` / `C4Component`), Sequence, Activity, ERD, State. vis-network for File Graph.
- Pin Mermaid to an explicit version. `startOnLoad: false`. Render each block with `mermaid.render(...)`.
- Keep Mermaid in plain-text blocks. No `<br/>`, raw HTML, `[]`, or unescaped `<` in diagram source.
- Sticky tab bar. Mark the active tab.

## Guidelines

- Parse-check every Mermaid block with the same Mermaid version the HTML loads (`mermaid.parse` or matching `mmdc`). Fix until they pass.
- Verify file paths exist. Name the app or package for each file. Trace across apps when the feature spans mobile and backend.
- Large features: primary flow only; mention secondary paths separately.
- If the feature description is ambiguous, ask before diving in.
