---
name: code-visualization
description: See the codebase — diagrams-as-code, dependency and call graphs, architecture maps, history views.
version: 1
triggers: code visualization, dependency graph, call graph, architecture map, diagram the codebase
category: Engineering & code
blurb: See the codebase — diagrams as code, dependency and call graphs, architecture maps.
archetype: knowledge
example: Map this codebase's architecture so I can see how it fits together.
---

# Code Visualization

A codebase you can't see is a codebase you can't reason about. Render structure on demand: dependencies, calls, flows, history — as code, so diagrams stay alive.

## When to use
- Onboarding to (or re-entering) an unfamiliar codebase.
- Explaining architecture to others; design reviews.
- Spotting cycles, god-modules, and dependency tangles.

## Method
1. **Diagrams-as-code over drag-drop**: Mermaid/Graphviz/PlantUML in the repo — versioned, diff-able, regenerated on change; screenshots rot, source doesn't.
2. **Dependency views**: module/package import graphs (tool or a 20-line script); highlight cycles and layering violations; keep a "known bad" list.
3. **Call & flow views**: call graphs for hot paths (profiler output or static analysis); sequence diagrams for critical journeys; data-flow for pipelines.
4. **Architecture maps**: C4-lite — context → containers → components; one page per level; annotate owners and boundaries (ADRs live beside them).
5. **Metrics visualization**: complexity heatmaps; change-frequency × complexity "hotspots"; coverage overlays — where attention pays.
6. **History views**: churn timelines, ownership maps (who touches what), incident overlays — patterns jump out of time series.
7. **Keep it honest**: label generated-at + tool + scope; generate what can be generated; delete stale diagrams rather than let them lie.

## Quality gates
- [ ] Key diagrams exist as code in-repo (regenerable).
- [ ] Cycles/layering violations visible; known-issues list maintained.
- [ ] Hotspot view (churn × complexity) considered for refactor targets.
- [ ] Each diagram labeled with scope + generation source.

## Red lines
- No stale diagrams shipped as truth; no unlabeled hand-drawn maps guiding decisions — regenerate or remove.

## Related
`semantic-analysis` · `architecture-decisions` · `technical-writing`.
