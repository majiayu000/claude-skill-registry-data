---
name: analyze-comfyui-workflow-json
description: 'Analyze a ComfyUI workflow JSON and produce a structured map of nodes, links, subgraphs, and data flow before making changes. Use when user says "analyze this workflow", "map this comfyui json", "understand this workflow", "analise esse workflow", "what does this workflow do", or needs to audit node types, trace IMAGE/VIDEO/MODEL chains, or extract parameter values from a .json workflow file.'
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

## Process: Analyzing a ComfyUI Workflow JSON

**1. Identify node types**
Scan all `"type"` fields. Categorize into: input nodes (LoadImage, PrimitiveInt, etc.), processing nodes (custom UUIDs or named types), output nodes (SaveVideo, PreviewImage).

**2. Map UUID subgraphs**
UUID-typed nodes (e.g. `"98e3bef8-..."`) are subgraphs. Find their definition in `definitions.subgraphs[]`. Read `"name"` field for human label.

**3. Trace the link graph**
`"links"` array format: `[link_id, source_node_id, source_slot, target_node_id, target_slot, type]`. Build a directed graph: source → target.

**4. Identify data flow backbone**
Follow primary data types (IMAGE, VIDEO, MODEL) through links. Ignore reroute nodes (type `"Reroute"`) — treat them as pass-throughs, collapsing the chain.

**5. Extract parameter nodes**
PrimitiveInt, DF_Float, and similar nodes are constants. Read `widgets_values[0]` for their value. Read `"title"` for semantic meaning.

**6. Find chaining pattern**
Check if output slots (especially IMAGE) of one processing node feed as `start_image` input of another same-type node. If yes → sequential chaining pattern.

**7. Reconstruct computation**
For math nodes (multipliers, converters), read `inputs` labels and `outputs` labels. Infer operation from context (e.g. `seconds × fps → frames`).

**8. Summarize architecture**
Express as: inputs → processing chain → outputs. Include parameter values, segment counts, and any detected patterns (chaining, branching, parallel paths).
