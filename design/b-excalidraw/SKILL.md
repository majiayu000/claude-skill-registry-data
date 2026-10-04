---
name: b-excalidraw
description: >
  Sketch conceptual, whiteboard, and explanatory architecture, workflow,
  data-flow, and lifecycle diagrams in Excalidraw through the Excalidraw
  MCP from explicit facts, without inferring topology, ownership, runtime
  behavior, impact, or merge safety. Formal, icon-based, ER/UML, sequence,
  or editable .drawio diagrams belong to b-drawio. Never produces HTML or
  SVG. Routing signals: architecture diagram, system map, workflow
  diagram, data-flow diagram, lifecycle diagram, whiteboard sketch,
  brainstorm diagram, Excalidraw diagram.
metadata:
  phase: Build
  execution_mode: main
---

<!-- Generated from skills/registry.yaml and skills/b-excalidraw/prompt.md. Edit those sources, not this file. -->

# b-excalidraw

Sketch a conceptual, whiteboard, or explanatory technical diagram in Excalidraw through the Excalidraw MCP from explicit user or repository facts. Do not infer topology, ownership, runtime behavior, impact, or merge safety, and never produce an HTML or SVG artifact.

## When to use

- The user asks for an Excalidraw diagram, a whiteboard sketch, a brainstorm diagram, or a conceptual architecture, system map, workflow, data-flow, or lifecycle diagram.
- The diagram explains an idea in chat and stays small (about 6 steps or about 20 nodes or fewer), with no need for official icons or later editing as a repository file.

## When NOT to use

- A formal or editable diagram (official cloud or network icons, ER or UML models, sequence diagrams, dense or multi-page flowcharts, or a `.drawio` file) -> use **b-drawio**.
- Format is unstated and matters: ask one focused question. If it cannot be asked, an explanation goes to **b-excalidraw** and a repository artifact or formal specification goes to **b-drawio**.
- Diagram scope, facts, or intended audience are materially unclear -> use **b-plan**.
- The user wants frontend/UI code or visual refresh work -> use **b-frontend**.
- The user wants reusable frontend design guidance -> use **b-design**.
- The user wants real-browser evidence or a visual assessment -> use **b-browser**.
- The user needs external facts -> use **b-research** before authoring the diagram.

## Tool guidance

- Use `read` and local discovery for the smallest relevant repository evidence. Select CodeGraph only when a concrete repository-wide architecture, dependency, or call-flow question is central.
- `excalidraw_read_me` is a direct read-only tool: call it once per session before the first draw and follow its element syntax.
- `excalidraw_create_view` draws the diagram. It is approval-gated, so call it through the MCP proxy: `mcp({ tool: "excalidraw_create_view", args: { elements: "<JSON array as a string>" } })`. The array is limited to 5 MB.
- The widget opens in the system browser or a native window, not in the terminal. The widget's own tools (export, share link, checkpoints) are not model tools: never call them.
- Use native `write` only for a user-approved source path.
- Do not fetch URLs or inspect live systems from diagram evidence references.

## Steps

1. Confirm the diagram kind, audience, source facts, and whether to save the elements source (and where). Ask one focused question if any is material and unresolved.
2. Establish the bounded fact set. For repository-based diagrams, distinguish observed source facts from user-provided assumptions; preserve exact paths or symbols only when they are safe to disclose.
3. Privacy: with the managed remote endpoint, each `excalidraw_create_view` call sends the diagram text to the Excalidraw MCP host, which may retain it as a checkpoint. Tell the user this before drawing from repository-derived or proprietary content; the call's approval prompt is the explicit approval. Never include secrets, customer data, or internal URLs.
4. Call `excalidraw_read_me` unless it was already called in this session.
5. Author the elements array from the fact set only:
   - One labelled shape per fact node: rectangle by default, ellipse for an external actor or start/end, diamond for a decision.
   - One arrow per fact edge, bound to existing element ids at both ends, with an optional label.
   - Show a boundary as a background rectangle plus a text label, since frames are not supported.
   - Lay out in one direction with consistent spacing. Start with a `cameraUpdate` at a 4:3 size that frames the whole diagram.
   - Keep each view small (about 20 nodes or fewer); split larger systems into separate views rather than shrinking text.
   - No images or freehand drawing, and no invented relationships, traffic, deployment placement, owners, risk, or causal impact.
6. Call `excalidraw_create_view`. Repair only the errors it reports. To refine, call it again with `restoreCheckpoint` and `delete` entries rather than redrawing everything.
7. If the user approved saving the source, write the exact elements array to the approved path (suggested name `<name>.excalidraw-elements.json`). Do not use the `.excalidraw` extension: the array uses `label` and pseudo-elements, so it is not a scene file. Tell the user that `.excalidraw`, PNG, and SVG files come from the widget's export, and that a share link uploads the diagram to excalidraw.com, which is their decision.
8. If the Excalidraw MCP is unconfigured, fails, or is denied, say "Excalidraw MCP unavailable" once and stop. Offer only to save the elements source; never fall back to HTML or SVG. If no viewer window opens (headless session or `MCP_UI_VIEWER=none`), report that nothing was displayed and give the adapter's URL notice.
9. Report the result and state what the diagram does not establish. Route browser-based visual proof to **b-browser** when requested.

## Content rules

- Use only authored nodes and edges. Do not invent relationships, traffic, deployment placement, owners, risk, or causal impact.
- Keep diagrams sparse: include the primary path and necessary boundaries; put supporting detail in labels rather than multiplying edges.
- Evidence references are citations, not live links to inspect, not authorization to disclose protected content, and not proof of runtime behavior.
- Preserve existing diagram source conventions when a repository already has them.
- Do not add external libraries, hosted sharing, or export formats unless separately approved.

## Output format

Report diagram kind, facts represented, the `excalidraw_create_view` result (success, error, or checkpoint id), whether a viewer window was expected, the saved source path or "not persisted", and explicit limits or assumptions.

## Rules

- You never see the rendered image: do not claim the diagram is visually correct, browser-verified, visually approved, or a complete representation of a system.
- Do not send diagram content to the MCP without the privacy notice in step 3.
- Do not write outside the user-approved path or introduce dependencies.
