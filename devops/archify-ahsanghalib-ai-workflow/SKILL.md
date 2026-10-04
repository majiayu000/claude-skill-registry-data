---
name: archify
description: >-
  Use when the user explicitly asks for Archify or for a renderer-backed typed
  JSON workflow that produces grounded architecture, workflow, sequence,
  data-flow, or lifecycle diagrams with deterministic HTML/SVG/export checks.
  Do not use for generic diagram design, Mermaid styling, implementation, or
  export when an Archify runtime is not available.
license: MIT
metadata:
  source: tt-a1i/archify
  source_revision: 7a16d30
  source_url: https://github.com/tt-a1i/archify
  compatibility: optional local Archify runtime or explicit harness adapter; source-only fallback
---

# Archify

Create a grounded diagram specification for Archify's typed JSON intermediate
representation and, only when the local renderer is available, deliver its
validated self-contained HTML or requested export. Archify is an optional
renderer workflow; it is not installed or vendored by this repository.

## Routing and capability boundary

Use this skill when the user names Archify or specifically requests its
renderer-backed architecture, workflow, sequence, data-flow, or lifecycle
pipeline. Use `diagram-design` for generic diagrams, Mermaid/Excalidraw
redraws, or diagrams that do not require Archify's typed source and renderer.

Before authoring or running a renderer command:

1. Resolve the exact Archify runtime or harness adapter inside the authorized
   workspace. Do not install packages, fetch a repository, inspect arbitrary
   external directories, or use a global CLI to make the capability appear.
2. If the runtime is present, run its documented diagnostic or equivalent safe
   capability check and record the result.
3. If the runtime is absent, do not claim typed-schema validation, deterministic
   delivery, browser evidence, or image/video export. For an explicit Archify
   request, report the capability gap and offer a source-only specification or
   the existing `diagram-design` fallback with the limitation clearly stated.

An available renderer does not authorize writing outside the workspace,
opening a browser, exporting files, installing dependencies, publishing, or
uploading artifacts. Obtain the normal approval for each consequential action.

## Ground the diagram

Classify every material fact as observed, proposed, inferred, or unknown. For a
repository-backed diagram, inspect the relevant files and pin the inspected
revision where the repository provides one. Record source paths and line ranges
in the artifact or accompanying brief. Never infer live infrastructure,
ownership, runtime traffic, security impact, or deployment state from names
alone.

For a description-only diagram, label it as proposed or illustrative rather
than presenting it as current topology. Preserve exact product names, code
identifiers, protocols, API paths, and environment names.

## Authoring workflow

### 1. Choose the diagram type

Choose one primary type:

- `architecture` for components, services, storage, infrastructure, and trust
  boundaries;
- `workflow` for processes, approvals, tool calls, runbooks, and CI/CD;
- `sequence` for API calls, request lifecycles, async traces, and returns;
- `dataflow` for pipelines, transformations, lineage, governance, and consumers;
- `lifecycle` for states, retries, waits, cancellation, and terminal outcomes.

If the type is ambiguous, state the competing interpretations and ask the
smallest question that changes the topology. Do not silently convert a
sequence into an architecture diagram or add a second layout grammar.

### 2. Inspect the local contract

When the runtime is available, read only the matching schema, the shared schema
contract, and one matching example before authoring. Use examples for field
shape, not facts. Use the runtime's guide command when the type remains
unclear. Keep new stable IDs and domain wording; do not copy example topology.

When the runtime is unavailable, produce a source-only brief that records the
intended type, nodes, relationships, evidence, and unresolved renderer fields.
Do not invent schema fields or reproduce renderer internals from memory.

### 3. Author a sparse source

Start with one obvious main path, short side branches, sparse semantic labels,
and only the nodes needed for the reader's question. Prefer deletion over
adding geometry controls. Keep observed topology separate from proposed changes.

Use semantic node and relationship types supported by the runtime. A label is
information, not decoration: preserve protocol, action, direction,
synchronous/asynchronous behavior, and cross-boundary mechanisms. Do not delete
meaningful labels merely to make validation pass.

Default to static output and the runtime's automatic routing. Enable motion,
presentation, or other viewer features only when requested. Do not infer brand
marks from generic roles; use supplied or explicitly approved brand evidence.

### 4. Validate and repair

With a renderer present, validate after each candidate edit and immediately
before handoff using its documented command. Treat a non-zero result as failure.
Apply only the diagnostic subject and supported fix identified by the renderer;
make one focused correction at a time and revalidate.

Before delivery, confirm:

- schema and semantic relationships are valid;
- source claims and revision evidence are present where required;
- the main path, labels, boundaries, and layout remain readable;
- output files stay within the authorized workspace;
- renderer, browser, and perceptual visual evidence are reported as separate
  claims.

If a renderer check or delivery fails, preserve the last known-good artifact and
report the unresolved diagnostic. Never inspect a stale artifact and call it a
passing result for the failed candidate.

### 5. Deliver only when requested

Delivery is a separate approval-gated action. When requested and supported by
the runtime, use its delivery command once for final acceptance, then collect
any optional browser evidence without modifying the trusted output. Export PNG,
SVG, WebP, WebM, or share-card formats only when requested and supported.

Keep these claims distinct:

- schema/renderer validation proves the typed source passed the available
  machine checks;
- deterministic delivery proves the renderer created the checked artifact;
- browser evidence proves only the inspected runtime behavior;
- human visual review proves perceptual polish.

## Output contract

Return:

- diagram type and intended audience;
- observed/proposed/unknown evidence status and inspected revision, if any;
- typed source path or source-only specification path;
- renderer and delivery validation status;
- browser and perceptual visual-review status;
- exports created, if explicitly requested;
- unresolved diagnostics, capability gaps, and next action.

Never claim Archify rendering, validation, delivery, export, or visual review
when the corresponding capability or fresh evidence is unavailable.
