---
name: b-drawio
description: >
  Draw formal or editable technical diagrams in draw.io from explicit
  facts, such as cloud or network topology with official icons, ER and UML
  models, sequence diagrams, dense or multi-page flowcharts, and
  repository .drawio files, without inferring topology, ownership, runtime
  behavior, impact, or merge safety. Conceptual whiteboard sketches belong
  to b-excalidraw. Never produces HTML or SVG. Routing signals: draw.io
  diagram, drawio, .drawio file, network topology diagram, cloud
  architecture diagram, ER diagram, UML diagram, class diagram, sequence
  diagram.
metadata:
  phase: Build
  execution_mode: main
---

<!-- Generated from skills/registry.yaml and skills/b-drawio/prompt.md. Edit those sources, not this file. -->

# b-drawio

Draw a formal or editable technical diagram in draw.io from explicit user or repository facts. Do not infer topology, ownership, runtime behavior, impact, or merge safety, and never produce an HTML or SVG artifact.

## When to use

- The user asks for a draw.io diagram, a `.drawio` file, or edits an existing `.drawio` file.
- The diagram needs official cloud or network icons, ER or UML models, a sequence diagram, a dense flowchart (more than about 20 nodes), or multiple pages.
- The result is a committed repository artifact or a formal specification that people will keep editing.

## When NOT to use

- A conceptual, whiteboard, brainstorm, or chat-sized explanation of about 6 steps or fewer -> use **b-excalidraw**.
- Format is unstated and matters: ask one focused question. If it cannot be asked, a repository artifact or formal specification goes to **b-drawio**, and an explanation goes to **b-excalidraw**.
- Diagram scope, facts, or audience are materially unclear -> use **b-plan**.
- The user wants frontend/UI code, including a draw.io embed -> use **b-frontend**.
- The user wants reusable frontend design guidance -> use **b-design**.
- The user wants real-browser evidence or a visual assessment -> use **b-browser**.
- The user needs external facts -> use **b-research** before authoring the diagram.

## Tool guidance

- Use `read` and local discovery for the smallest relevant repository evidence. Select CodeGraph only when a concrete repository-wide architecture, dependency, or call-flow question is central.
- `drawio_search_shapes` is a direct read-only tool (`query`, optional `limit`): use it to find exact shape or icon style names. The managed entry disables the live icon service, so results come from the local stencil index; the first use downloads that index without sending diagram content.
- The `open_drawio_*` tools are approval-gated, so call them through the MCP proxy, for example `mcp({ tool: "drawio_open_drawio_xml", args: { content: "<mxGraphModel XML>" } })`. Use `drawio_open_drawio_mermaid` for Mermaid sequence, ER, and class diagrams and `drawio_open_drawio_csv` only for tabular data. Optional `lightbox` and `dark` flags are not needed by default; `postLayout: "elk"` is for flowcharts only.
- Each call attempts to open the draw.io web editor in the default browser. The launch is asynchronous and its failures are not reported, so the result never proves a window opened. The diagram travels in the URL fragment, which browsers do not send to the server. The tool result always includes the editor URL.
- Write `.drawio` source with native `write` or `edit` to a user-approved path. Read an existing uncompressed `.drawio` file with native `read`.
- Never call `drawio_set_page`. `drawio_list_pages` and `drawio_get_page` are unclassified and always ask; use them only when a `.drawio` page is compressed and cannot be read natively, and report the approval need to the user.
- Do not fetch URLs or inspect live systems from diagram evidence references.

## Steps

1. Confirm the diagram kind, audience, source facts, the target `.drawio` path (or "preview only"), and whether to open a preview. Ask one focused question if any is material and unresolved.
2. Establish the bounded fact set. For repository-based diagrams, distinguish observed source facts from user-provided assumptions; preserve exact paths or symbols only when safe to disclose.
3. Privacy: each `drawio_open_drawio_*` call hands the diagram text to the local draw.io MCP package, which builds an editor URL carrying it in the URL fragment and attempts to open that URL in the browser; delivery to the draw.io web editor is not confirmed. The call's approval prompt is the explicit approval; tell the user this before opening a preview from repository-derived or proprietary content. Never include secrets, customer data, or internal URLs.
4. For an existing `.drawio` file, read it first and change only the facts the user named, preserving page structure, ids, and styles.
5. Author the diagram from the fact set only:
   - One labelled shape per fact node and one edge per fact edge, connected by existing cell ids; use `drawio_search_shapes` for icon styles instead of guessing style names.
   - Express a boundary (VPC, subnet, cluster, swimlane) as a container the member nodes are parented to.
   - Lay out in one direction with consistent spacing. Prefer Mermaid for sequence, ER, and class diagrams.
   - Split larger systems into pages or separate diagrams rather than shrinking text. No invented relationships, traffic, deployment placement, owners, risk, or causal impact.
6. If a target path was approved, write the full `.drawio` file (an `<mxfile>` wrapping uncompressed `<mxGraphModel>` XML) with native tools. A diagram authored as Mermaid is not a `.drawio` file: save the Mermaid source if the repository uses it, or tell the user to save a `.drawio` file from the draw.io editor.
7. If a preview was approved, call the matching `drawio_open_drawio_*` tool through the MCP proxy and repair only the errors it reports. Always give the returned editor URL, and report only that a launch was attempted; do not claim a window opened or the diagram rendered.
8. If the draw.io MCP is unconfigured, fails, or is denied, say "draw.io MCP unavailable" once. Keep the written `.drawio` source if any; never fall back to HTML or SVG.
9. Report the result and state what the diagram does not establish. Route browser-based visual proof to **b-browser** when requested.

## Content rules

- Use only authored nodes and edges. Do not invent relationships, traffic, deployment placement, owners, risk, or causal impact.
- Keep diagrams sparse: include the primary path and necessary boundaries; put supporting detail in labels rather than multiplying edges.
- Evidence references are citations, not live links to inspect, not authorization to disclose protected content, and not proof of runtime behavior.
- Preserve existing diagram source conventions when a repository already has them.
- Do not add external libraries, hosted sharing, or export formats unless separately approved.

## Output format

Report diagram kind, facts represented, the saved `.drawio` path or "not persisted", whether a preview launch was attempted (never that it opened) and the editor URL, and explicit limits or assumptions.

## Rules

- You never see the rendered diagram: do not claim it is visually correct, browser-verified, visually approved, or a complete representation of a system.
- Do not open a preview without the privacy notice in step 3.
- Do not write outside the user-approved path or introduce dependencies.
