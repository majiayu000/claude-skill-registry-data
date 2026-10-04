---
name: architecture-map
description: "Maps verified domains, dependencies, entrypoints, flows and risks for broad changes or review."
---

# Architecture Map

Build a compact, verified architecture map from current files.

## Workflow

1. Read repo instructions and top-level dependency/build files.
2. Identify entrypoints, layers, data flow, external integrations, and tests.
3. Map dependency direction and boundary violations.
4. Record uncertainty separately from verified facts.
5. Keep the output short enough to guide implementation or review.

## Graphify Route

When Graphify is exposed in the current environment and the task is about
architecture, dependencies, call graphs, knowledge graphs, or repeated
onboarding to a large codebase, use Graphify as the preferred Tier 2
knowledge-graph source.

Before building anything, check for existing state:

```bash
test -f graphify-out/graph.json && echo graph-ready
```

If `graphify-out/graph.json` exists, query it first for architecture,
dependency, and call-flow questions. Check whether relevant files changed after
the graph was built, or whether available Graphify metadata points at a
different root/scope. If freshness is uncertain, use the graph as a hypothesis
source and verify against files.

If no graph exists, initialize Graphify only when the map will benefit from a
knowledge graph: broad architecture, dependency/call graph, repeated onboarding,
large subsystem exploration, or multi-agent handoff. Prefer the narrowest useful
scope:

```bash
graphify extract . --code-only
graphify extract <subdir> --code-only
```

Do not create `graphify-out/` for tiny localized tasks. For read-only review,
security review, validation-critical work, or an explicit no-mutation request,
ask before creating Graphify state.

Treat Graphify output as an index, not as final proof. Verify important
architecture claims against repository files, command output, or explicit user
context before reporting them.

If Graphify is unavailable or not useful for the repository shape, fall back to
`rg`, `git ls-files`, targeted file reads, and top-level dependency/build files.

When Graphify state is created or reused, report whether it was existing,
fresh, stale/uncertain, or newly generated.

## Optional Diagram Rendering

Use Archify as an optional renderer when a shareable architecture or process
diagram helps the task and the current runtime is verified. Build its
structured input from source-backed facts after mapping; keep source paths and
revision evidence alongside the diagram. Graphify discovers candidate
relationships; a renderer presents the supplied relationships.

Validate the structured input and rendered artifact, then visually inspect
labels, edges and layout. A valid diagram does not prove a relationship exists
in code, runtime impact, security, or merge safety. Keep uncertain links marked
as hypotheses. Do not add rendering to ordinary localized edits.

For offline/private work, disable the renderer's update check through the
documented runtime option. Keep generated HTML, snapshots and machine paths
outside tracked files unless the user requests a documentation artifact.
No renderer installation or diagram generation is implied by this skill alone.

## Output

- repo shape
- main layers or bounded domains
- important entrypoints
- persistence/integration/config surfaces
- test and validation commands found
- risks and unknowns
- suggested next skill if applicable

## Rule

Do not invent architecture. Every claim must come from files, commands, or
explicit user-provided context.
