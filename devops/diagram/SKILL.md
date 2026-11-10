---
name: diagram
zh_name: "代码图表"
en_name: "Diagram"
emoji: "🧭"
description: "Designed diagrams of real systems — architecture, flowchart, entity-relationship, state machine or sequence — drawn from the code you read, laid out by the browser and styled by the active design system."
zh_description: "根据真实代码绘制的架构图、流程图、ER 图、状态图和时序图, 由浏览器排版, 使用当前设计系统的样式"
en_description: "Designed diagrams of real systems — architecture, flowchart, entity-relationship, state machine or sequence — drawn from the code you read, laid out by the browser and styled by the active design system."
category: diagram
scenario: engineering
tags: ["diagram", "architecture", "flowchart", "erd", "sequence", "state machine", "图表", "架构图"]
triggers:
  - "diagram"
  - "architecture diagram"
  - "flowchart"
  - "flow chart"
  - "sequence diagram"
  - "er diagram"
  - "erd"
  - "state machine"
  - "system diagram"
  - "how does this work"
  - "架构图"
  - "流程图"
od:
  mode: prototype
  craft:
    requires:
      - color
      - accessibility-baseline
  platform: desktop
  scenario: engineering
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  example_prompt: "Diagram how this repo's packages depend on each other: read each package.json and the imports, group the shared packages and the hosts, and mark build-time copies differently from runtime dependencies."
---

# Diagram

**Intent.** One clear, designed diagram of a real system, true to the code, that someone can read in ten seconds. It is an HTML page: you write the content (nodes, links, groups) and the browser lays it out. Never hand-place coordinates.

## 1. Read before you draw

Every node and link must come from something you read, never from what such systems usually look like.

- **Architecture / dependencies:** package manifests (`package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`), workspace config, import statements, service and deployment config (`docker-compose.yml`, Kubernetes manifests).
- **Flowchart / request flow:** the entry point and the functions it calls, route definitions, middleware, queue consumers.
- **Entity-relationship:** schema files (`schema.prisma`, migrations, ORM models, `.sql`).
- **State machine:** the reducer, state enum or transition table.
- **Sequence:** one concrete call path, followed through the code in order.

Keep the list of files you read: you register them as `sources`. If the user's question is broader than what you can read (another service's repo), say what you could see and draw only that.

## 2. Decide the graph, then the grid

Pick **5–25 nodes**. Merge leaf details into their parent; split into two diagrams rather than drawing 40 boxes.

Each node gets two small integers:
- `data-rank`: its step along the flow direction (1 = first). Sources, entry points or foundations come first; things that depend on or are called by earlier nodes come later.
- `data-lane`: its position across the flow (1 = top for `right`, left for `down`). **Order lanes so linked nodes sit next to each other**: that is what keeps links short and off other nodes. Two nodes may not share the same rank and lane.

Direction: `right` for flows and dependency graphs (wide screens), `down` for hierarchies and state machines with long chains.

Groups (`data-group`) mark real boundaries: a package set, a process, a network zone, a team. Members of one group should occupy a contiguous block of ranks and lanes, or the group's box will cover other nodes.

## 3. Write the page

One self-contained HTML file: a title, an optional one-line subtitle saying what the diagram shows and as of when (commit or date), the diagram, a small legend when you use more than one link style, and a **Sources** footer listing the files you read.

```html
<div data-od-diagram data-direction="right">
  <div class="node" data-od-node="api" data-rank="2" data-lane="1" data-group="backend" data-od-source="services/api/package.json">
    <strong>api</strong><small>Express, REST</small>
  </div>
  …
  <i data-od-group="backend" data-label="Backend" hidden></i>
  <i data-od-link data-from="web" data-to="api" data-label="HTTPS" hidden></i>
  <i data-od-link data-from="api" data-to="queue" data-style="dashed" hidden></i>
</div>
```

- Node content is yours: a name, optionally a one-line role, an icon drawn in inline SVG. Keep labels short (2–4 words); widths stay similar across a rank.
- Link labels only where they add information (protocol, event name, cardinality). Use `data-style="dashed"` for a second kind of link (async, optional, build-time) and explain it in the legend.
- **Entity-relationship:** each table is a node whose content lists its key columns (primary key first, foreign keys marked); links carry the cardinality as their label (`1 — n`).
- **State machine:** states are nodes (the initial state at rank 1), transitions are links labelled with the event; use `direction="down"` when there are more than 5 states in a row.
- **Sequence:** `<div data-od-diagram="sequence">` with participants (`data-od-participant`, in order left to right) and messages in order (`<i data-od-message data-from data-to data-label hidden>`, `data-kind="return"` for replies). Use 3–6 participants and at most 15 messages.

Style from the active design system: node background from `--surface`, border from `--border`, text from `--fg`, secondary text from `--muted`, one emphasised node at most with `--accent`. Set the link and group look on the container with the runtime's custom properties (`--od-edge-color`, `--od-edge-width`, `--od-group-border`, `--od-group-bg`, `--od-rank-gap`, `--od-lane-gap`). Don't style the generated SVG or labels any other way.

## 4. Add the runtime, register, check

1. Call `add_open_design_diagram_runtime` with the entry path. It inserts the layout runtime into the file. Never write, copy or edit that `<script data-od-runtime="diagram">` block yourself.
2. Call `register_open_design_artifact` with kind `diagram`, the title, and `sources` set to the files you read in step 1.
3. Call `check_open_design_artifact`. Fix every `diagram-error` (unknown ids, missing rank or lane). For `edge-through-node`, `node-overlap` or `group-overlap`, reorder lanes or ranks rather than nudging anything with CSS. Look at the screenshot: the main path should read left to right (or top to bottom) without the eye jumping back.

When `stale-sources` is reported later, offer to redraw from the changed files.
