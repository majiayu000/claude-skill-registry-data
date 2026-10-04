---
name: mermaid-diagramming
description: >-
    Authors, validates, and repairs Mermaid diagrams: type selection, graph logic, layout-engine
    config, an archetype template per diagram kind, and a bundled validator proving each fence
    renders, reads legibly, and holds its graph logic. Committed fences carry structural payload
    only; theming rides one optional reference for a deliverable that explicitly wants a styled
    render. Use when writing, fixing, or embedding a mermaid fence in markdown or a single-file
    HTML page, exporting one to SVG or PNG, or when a fence will not render, overlaps nodes, or
    crosses edges — and whenever a task asks to draw, map, or visualize a system, flow, state
    machine, sequence, schema, dependency graph, protocol seam, chronology, schedule, hierarchy,
    or workflow board, even when mermaid is never named.
---

# [MERMAID_DIAGRAMMING]

Every committed diagram answers one written question, instantiates one catalog archetype or admitted type, carries only structural payload — declaration, nodes, edges, labels, subgraphs, accessibility directives, functional layout keys — and ships only after the validator and the soundness audit pass. Reasoning discipline and engine surface load on demand through the reference routes below.

## [01]-[ROUTING]

- [01]-[METHODOLOGY](references/methodology.md): admission, investigation, node/edge law, type selection, soundness audit, multi-diagram composition
- [02]-[CONSTRUCTION](references/construction.md): per-type — each type's question, what its marks assert, failure modes, truth tests
- [03]-[GRAMMAR](references/grammar.md): link/arrow forms, link lengths, shape registry, containers, subgraphs, structural traps
- [04]-[CONFIG](references/config.md): frontmatter schema, secure keys, layout engines, ELK tuning, accessibility, mmdc and CI, traps
- [05]-[SYNTAX_CORE](references/syntax-core.md): flowchart, sequence, state, class, ER — node metadata, edge IDs, markdown strings, KaTeX, traps
- [06]-[SYNTAX_EXTENDED](references/syntax-extended.md): beyond the core five — admitted rows with working fences and traps, registered rows named
- [07]-[CONCEPT_MAP](references/concept-mapping.md): shape in code, prose, plans, arguments: signals, archetype routes, misfit shapes, composites
- [08]-[EMBEDDING](references/embedding.md): fence law in markdown hosts, inline-SVG law in single-file HTML, export surfaces, source-beside-render
- [09]-[THEMING](references/theming.md): optional appearance system — palette, classDef canon, per-family routes; loads only for a styled render

## [02]-[QUESTION]

A diagram earns its fence only when the reader traces a relation across more marks than a clause holds: three or more nodes with at least one branch, cycle, or crossing relation. Below that, prose owns the fact; one diagram owns one question, and a diagram needing two legends is two diagrams. Authoring discipline is [references/methodology.md](references/methodology.md), per-type mark law [references/construction.md](references/construction.md); raw material with no written question resolves its shape through [references/concept-mapping.md](references/concept-mapping.md).

## [03]-[CATALOG]

Select the archetype by intent, copy its template, and refill — a catalog template is self-sufficient, carrying its archetype's construction law in its own prose. An intent outside the catalog selects its type through the methodology decision table and the extended registry, under the same payload and validation law. A split move partitions a subject the moment a second question appears, and a required legend is itself a split signal.

| [INDEX] | [ARCHETYPE]                                     | [INTENT]                    | [DECLARATION]       | [SPLIT_MOVE]                     |
| :-----: | :---------------------------------------------- | :-------------------------- | :------------------ | :------------------------------- |
|  [01]   | [SPINE](templates/spine.mmd.md)                 | main path through owners    | `flowchart LR`      | split at the readiness gate      |
|  [02]   | [SEAM_GRAPH](templates/seam-graph.mmd.md)       | shapes across a boundary    | `flowchart LR`      | partition by counterpart package |
|  [03]   | [LOGIC_FLOW](templates/logic-flow.mmd.md)       | one operation dispatch      | `flowchart LR`      | extract an arm subflow           |
|  [04]   | [LIFECYCLE](templates/lifecycle.mmd.md)         | guarded state transitions   | `stateDiagram-v2`   | extract the composite lifecycle  |
|  [05]   | [WIRE_SEQUENCE](templates/wire-sequence.mmd.md) | ordered boundary exchange   | `sequenceDiagram`   | split by interaction phase       |
|  [06]   | [SCHEMA](templates/schema.mmd.md)               | persistent entity relations | `erDiagram`         | split by aggregate root          |
|  [07]   | [STRATA](templates/strata.mmd.md)               | layer dependency direction  | `flowchart TB`      | collapse peer layers             |
|  [08]   | [SCHEDULE](templates/schedule.mmd.md)           | dated committed work        | `gantt`             | split by phase                   |
|  [09]   | [BOARD](templates/board.mmd.md)                 | stage-held work now         | `kanban`            | split by workflow segment        |
|  [10]   | [HISTORY](templates/history.mmd.md)             | branch and merge truth      | `gitGraph LR:`      | split by release train           |
|  [11]   | [TOPOLOGY](templates/topology.mmd.md)           | deployables and reach       | `architecture-beta` | split by zone                    |
|  [12]   | [LANDSCAPE](templates/landscape.mmd.md)         | one-zoom system landscape   | `C4Context`         | re-declare at the next zoom      |
|  [13]   | [EVENT_FLOW](templates/event-flow.mmd.md)       | command-event causality     | `eventmodeling`     | split by stream                  |
|  [14]   | [PROFILE](templates/profile.mmd.md)             | two-subject capability map  | `radar-beta`        | one comparison per fence         |
|  [15]   | [DECOMPOSITION](templates/decomposition.mmd.md) | weighted whole-to-part      | `treemap-beta`      | aggregate the tail               |

## [04]-[VALIDATE]

A diagram is not done until its fence passes both stages: graph-logic checks over the source, then a render whose proof is an actual SVG artifact, never a zero exit alone.

```bash template
uv run scripts/validate_mermaid.py <file.md ...>
```

Each fence emits `file:line: STATUS check detail` rows — check kinds `render`, `legibility`, `contract`, `logic`, `export`, `proof`, `setup`, `read`, `collect` — and `--json` emits identical-key NDJSON. Finding-tier rows fire only on findings: a clean fence prints its render row alone, silence from a check is a pass, and contract rows carry accessibility and hygiene — directive order and pairing, families that mis-serve the directives, deprecated init directives, unused classes.

Graph-logic analysis covers the families the validator implements; any family outside that set emits `logic-unimplemented` instead of silent approval. A logic failure blocks on a structural break the graph cannot resolve; a logic warn demands a split or a stated reason, the row naming the exact condition. `--no-render` runs the static checks alone for a fast loop, the process exits nonzero when any fence fails, and a render failure splits `syntax` from `environment` so a missing browser never masquerades as a broken diagram.

After a fence renders, the `legibility` pass parses SVG geometry for the graph families (flowchart, state, ER, class), emitting `node-overlap` (fail), `edge-over-node`, and `edge-crossing-pairs:N` rows — N a lower bound on crossing edge pairs computed from node bounding boxes and edge routing; sequence, gantt, and quantitative families carry inherent crossings and are exempt.

Renderer resolution walks the workspace first — `node_modules/.bin/mmdc` from any cwd ancestor, then PATH `mmdc`, `--renderer CMD` overriding both — and every render binds the pinned Chromium through the generated puppeteer-config `executablePath`; the real Google Chrome app never launches. A fence the resolved renderer rejects re-proves through the pinned release renderer over the pnpm dlx cache: the passing row lands as `rendered-release:`, a fence the pinned renderer also rejects stays a real syntax failure, and a lagging toolchain never masquerades as broken syntax.

`--export DIR` writes every passing fence as an embed-ready SVG — unique root id, aria title and description preserved — the mechanical arm of the embedding contract. `--proof` rasterizes each rendered SVG browserlessly through resvg into a per-run ephemeral dir cleaned on exit (`--keep` preserves it and prints `proof-dir:`), with mmdc's own PNG as the fallback where a family still carries `foreignObject` labels; a proof failure lands as a typed `proof` row, never a silent pass.

## [05]-[CONTRACT]

- A fence body is structural payload alone: the declaration, nodes, edges, labels, subgraphs, accessibility directives, and functional layout keys; appearance belongs to the reader's renderer, and a deliverable that explicitly wants a themed render loads [references/theming.md](references/theming.md).
- Fence frontmatter is functional alone: a flowchart fence opens on the standing `config:` block — `layout: elk` with `flowchart.curve: linear` and `flowchart.padding: 25` — every other family carries only its own geometry knobs and `title:`, and a fence opening with `%%{init:...}%%` converts to frontmatter.
- `accTitle` and `accDescr` follow the header on every committed diagram, stating the encoded relation so the exported SVG reads outside its source.
- `block`, `mindmap`, `sankey`, and `venn` refuse the directives, `ishikawa` mis-handles them as nodes, and `kanban` as columns, so their relation sentence sits beside the fence; `timeline` and `eventmodeling` parse them but emit nothing into the SVG, so their relation sentence rides beside the fence too.
- Node and edge labels carry concept names, never mechanism detail — the owning page carries the bytes.
- Meaning rides structure: shape, containment, edge form, and label carry every semantic, so the diagram reads identically under any theme.

## [06]-[LEGIBILITY]

Legibility bounds a diagram, not syntax capacity. A rendered diagram ships only after the validator's geometry rows clear and the reviewer clears what geometry cannot — untruncated labels, reading-order orientation, type matching subject. A faulted fence converges on its own source across at most five render-inspect-edit rounds; each correction is a minimal text edit to the fence itself, never a sibling file.

## [07]-[REPO_INTEGRATION]

When the host repo declares a docs gate, that gate consumes `scripts/validate_mermaid.py --json`; the bundled script is the same engine everywhere else.
