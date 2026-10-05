---
name: excalidraw-diagram
description: Generates Excalidraw diagrams for architecture and existing-code flows. Use when the user asks to explain, visualize, or draw a system, request path, runtime interaction, or codebase-backed flow. Explores the codebase when needed, writes a structured diagram spec first, then builds polished .excalidraw output with validation and preview rendering.
---

# Excalidraw Diagram Generator

Generate Excalidraw diagrams that are readable, code-aware, and visually consistent.

Do not freehand raw Excalidraw JSON unless the builder is unavailable. The default path is:

1. discover the real flow
2. choose the right diagram level
3. write a compact diagram spec
4. build the `.excalidraw` file with the builder script
5. validate and preview it

## Trigger Logic

Activate when the user asks to create, explain with, visualize, or draw:

- an architecture
- a flow
- a request path
- a runtime interaction
- an existing code path
- a service/system overview
- a multi-view or scenario pack
- a drill-down into a specific service or phase

Examples:

- "Explain the auth flow with a diagram"
- "Draw the payment processing path"
- "Visualize the customer acquisition architecture"
- "Show me how this service talks to Redis and Postgres"
- "Give me an overview and then a detailed flow for the checkout"
- "Draw an architecture overview plus a drill-down of the auth service"

## Codebase Discovery

### Explore The Codebase When

- the user is asking about an existing system
- the request mentions a repo, solution, project, namespace, service, or feature
- the user wants an explanation of "how it works now"
- the flow likely exists in code but the prompt does not name every component explicitly

### Skip Discovery When

- the user is designing something new
- the user explicitly asks for a generic or conceptual template
- the prompt already contains all components and relationships needed for the diagram

### Discovery Procedure

1. Identify the repo or project path. If none is given, use the current working directory.
2. Read `references/codebase-discovery-prompt.md`.
3. Dispatch an Explore agent and ask it to return the structured output from that prompt.
4. Use the discovered components and flow sequence as the source of truth.
5. If no useful codebase evidence is found, fall back to a conceptual diagram and state that clearly.

## View Modes

Choose one of these view modes for each diagram request:

- **`overview`** — High-level system map showing all major entities with minimal internal detail. Use for "what exists" questions.
- **`focused-flow`** — A single runtime or request path through the system. Use for "what happens when" questions.
- **`drill-down`** — Detailed view of one service, phase, or subsystem. Use for "how does X work internally" questions.
- **`scenario-pack`** — Emits an overview plus one or more focused/drill-down views as separate artifacts. Use for comprehensive documentation or when the user asks for both overview and detail.

### Mode Selection Guidance

| User intent | View mode |
|---|---|
| "Show me the whole system" | `overview` |
| "What happens when a user logs in?" | `focused-flow` |
| "How does the auth service work internally?" | `drill-down` |
| "Document the payment system end to end" | `scenario-pack` |
| "Give me an overview and detail" | `scenario-pack` |

If the user does not specify a mode, infer it from context. Default to `focused-flow` for flow/path questions and `overview` for architecture/system questions.

## Scope Controls

These controls shape what the diagram includes and how it is presented. Set them in the shared model when building the spec.

| Control | Values | Default | Purpose |
|---|---|---|---|
| `detail_level` | `minimal`, `standard`, `detailed` | `standard` | How much metadata to surface (descriptions, technology, evidence) |
| `audience` | `technical`, `executive`, `mixed` | `technical` | Influences label verbosity and abstraction level |
| `scope_filter` | entity ids or group names | all | Limit views to a subset of the model |
| `max_nodes` | integer | none | Advisory node budget per view; triggers auto-split when exceeded |

### Auto-Split Rules

- If a view would exceed `max_nodes` (or ~15 nodes when unset), split into overview + detail artifacts automatically.
- When auto-splitting, emit an overview first, then one detail artifact per dense group or phase.
- Use a base stem like `{date}-{topic}-{shortid}` so multiple runs on the same day do not overwrite each other.

### Drill-Down Continuity

- Overview diagrams should use entity ids that detail diagrams can reference.
- When emitting a scenario pack, share the same model across all views so entity names and ids are consistent.
- Report which overview entities have corresponding drill-down views in the final output.

## Diagram Selection

Read `references/diagram-quality-bar.md` before choosing the diagram kind.

Use a C4-inspired level within each view:

- `dynamic` for request paths, runtime flows, and "what happens when" explanations
- `container` for service/application composition
- `component` for internals of a specific service/container
- `context` for high-level system boundaries
- `architecture` for broad layered overviews that do not fit neatly into one C4 level
- `deployment` for infrastructure and deployment topology
- `data-flow` for data or event movement through the system
- `trust-boundary` for security zones and trust perimeters
- `dependency-map` for static service or package dependencies

### Architecture Overview Defaults

For `overview` views using `layout: layers`:

- keep owned ingress, processing, and persistence groups as horizontal core rows
- put external systems on the left or right when they are communication partners rather than internal tiers
- put queues, topics, and async backbones on the right by default instead of drawing them as a full-width messaging row
- use `overview_style: core-with-sides` when the diagram mixes internal layers with external systems or messaging
- only keep `pure-layers` when the user explicitly wants a stacked tier diagram

If the user asks for multiple levels at once, use `scenario-pack` mode to generate the higher-level overview first plus detail views.

## Required References

Read these before writing the spec:

- `references/diagram-quality-bar.md`
- `references/diagram-spec.md`
- `references/color-palette.md`

Use these as examples when helpful:

- `references/examples/enhanced-auth-flow.spec.json` — legacy single-view sample
- `references/examples/multi-view-auth.spec.json` — multi-view model sample
- `references/examples/overview-example.spec.json` — overview view mode
- `references/examples/focused-flow-example.spec.json` — focused-flow view mode
- `references/examples/drill-down-example.spec.json` — drill-down view mode
- `references/examples/scenario-pack-example.spec.json` — scenario-pack with evidence metadata
- `references/examples/simple-flow.excalidraw`
- `references/examples/architecture.excalidraw`

## Generation Process

### Step 1: Choose View Mode And Scope

Determine the view mode from the user's intent (see View Modes above). Set scope controls:

- Pick `detail_level` and `audience` based on context.
- Set `max_nodes` if the system is large or the user wants a focused view.
- Set `scope_filter` if the user names specific services or phases.
- For `scenario-pack`, plan which views to include before writing the spec.

### Step 2: Build A Shared Model

Build one semantic model that captures all entities and relationships relevant to the request. This model is the single source of truth — all views derive from it.

The model must include:

- `title` — system or project title
- `model.entities` — all components with ids, labels, roles, and groups
- `model.relationships` — all connections with labels and kinds
- Scope controls: `detail_level`, `audience`, `scope_filter`, `max_nodes` as needed

When discovery was performed, include evidence metadata on entities and relationships:

- `evidence_source`: `code`, `inferred`, or `user-specified`
- `confidence`: `high`, `medium`, or `low`
- `owner`, `boundary`, `runtime` when known

### Step 3: Define Views

Add one or more views to the `views` array. Each view selects from the shared model.

Each view must include:

- `view_id` — unique identifier for artifact naming
- `view_mode` — `overview`, `focused-flow`, `drill-down`, or `scenario-pack`
- `diagram_kind` — the abstraction level
- `layout` and `direction` for flow diagrams
- `overview_style` for layered overview/container/context views when side columns help readability
- ordered `groups`
- `entity_ids` — subset of model entities to include (null means all)

For single-view requests, you may use the legacy single-view format (flat `nodes`/`edges` without `model`/`views`). The builder supports both.

Quality rules:

- Give every important arrow a label.
- Use real class/service/system names when discovery was performed.
- Include `node_type`, `technology`, and short `description` fields when they help explain the flow.
- Use `sequence` on the main interactions in dynamic diagrams.
- Use `shape: "decision"` only for meaningful branches.

### Step 4: Save The Spec

Create:

```bash
mkdir -p docs/diagrams/specs
```

Save the spec to:

```text
docs/diagrams/specs/<date>-<topic>-<shortid>.diagram.json
```

### Step 5: Build The Excalidraw File

Run:

```bash
python <skill-dir>/references/build_excalidraw_diagram.py <spec-file> --output docs/diagrams/<date>-<topic>-<shortid>.excalidraw
```

The builder handles layout, containers, legends, node sizing, and arrow label placement.

### Step 6: Validate Structure

Run:

```bash
python <skill-dir>/references/validate_excalidraw.py <diagram-file>
```

If validation fails, fix the spec first and rebuild. Do not hand-edit raw JSON unless the problem is obviously builder-specific.

### Step 7: Render Preview

Run:

```bash
python <skill-dir>/references/render_excalidraw.py <diagram-file>
```

If Playwright or browser rendering is unavailable:

- keep the `.excalidraw` file
- tell the user preview rendering was skipped

### Step 8: Visual Review

Check the preview for:

- crowded lanes or layers
- labels that are too vague
- unlabeled important arrows
- too many boxes for one story
- missing legend or unclear line styles

If the diagram is weak, edit the spec and rebuild. Prefer spec changes over raw JSON tweaks.

### Step 9: Done

Report:

- the `.excalidraw` path(s) — list all artifacts when multiple views were generated
- the spec path
- the preview path if rendering succeeded
- the view mode used
- whether the diagram is codebase-accurate or conceptual
- for multi-view output: which overview entities have drill-down views available
- evidence summary: how many entities are code-derived, inferred, or user-specified

## Constraints

### Quality Bar

- Every diagram needs a title.
- Important relationships need labels.
- Every node should explain what it is, not just name it.
- Prefer 6-10 primary nodes.
- Split mixed abstraction levels instead of forcing them together.

### Complexity Limit

If the discovered flow is too large for one readable diagram:

1. Use `scenario-pack` mode to emit an overview plus detail views.
2. Or set `max_nodes` in the model to trigger auto-split.
3. The compiler will split large models into overview + detail artifacts with deterministic naming.

Artifact naming for multi-view output:

- `{output_stem}-{view_id}.excalidraw` for each view
- Single-view output uses the `--output` path directly
- If the requested output path already exists, the builder appends a short unique suffix automatically to avoid overwriting artifacts

### Iteration Rule

Iterate on the spec at most 2 times unless the user asks for more refinement.

### Fallback

Only generate raw Excalidraw JSON directly if the builder script is broken or unavailable. If that happens, say so.
