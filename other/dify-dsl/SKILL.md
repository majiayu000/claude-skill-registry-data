---
name: dify-dsl
description: Turn natural-language requirements into usable, maintainable, and automatically laid-out Dify Workflow or Chatflow DSL YAML, and review or repair existing DSL before import. Use for graph design, node wiring, selectors, Code-node integration, deterministic layout, portability checks, and editor-rendering failures. Agent, model-config, and RAG Pipeline guidance is experimental. Do not use for deploying or publishing apps to a live Dify instance.
---

# Dify DSL

Create DSL that matches the user's target Dify version, behaves coherently, and imports with a clean left-to-right canvas that should not need routine mouse-based repositioning. Treat exported YAML from that target version as the strongest field-level reference.

## Route The Task

- Read [references/official-sources.md](references/official-sources.md) when version compatibility or current behavior matters.
- Read [references/app-dsl.md](references/app-dsl.md) for top-level `app` and `rag_pipeline` shapes.
- Read [references/workflow-graph.md](references/workflow-graph.md) for Workflow/Chatflow nodes, edges, selectors, loops, and iterations.
- Read [references/agent-chat-dsl.md](references/agent-chat-dsl.md) for `chat`, `completion`, and `agent-chat` apps that use `model_config` instead of a graph.
- Read [references/code-node.md](references/code-node.md) before creating or materially revising a Code node.
- Read [references/tool-bindings.md](references/tool-bindings.md) before using builtin, API, workflow, or plugin tools.
- Read [references/canvas-compatibility.md](references/canvas-compatibility.md) when import succeeds but the editor crashes, hides edges, or renders oversized containers.

## Authoring Workflow

1. Confirm the target kind, app mode, Dify version, inputs, outputs, and required external dependencies. Do not silently choose workspace-specific datasets, tools, credentials, or models.
2. When modifying an existing DSL, preserve its exported field style and stable node IDs unless a change is necessary.
3. Design the graph and each node's input/output contract before writing large YAML blocks.
4. For every new or materially changed Python Code node, also apply the companion `dify-python-code-node` skill. That skill writes the canonical `.py` source and returns the contract; this skill owns selectors and YAML integration.
5. When authoring `dev-dsl/*.yml`, require each Code node source under `docs/dify-code-nodes/`, include `Code source: <path>` in `data.desc`, and embed the exact file text into `data.code`.
6. Keep selectors explicit. Every referenced node, environment variable, and statically known output must exist.
7. Use environment variables with empty defaults for portable configuration. Never embed credentials, signed URLs, dataset IDs, workspace IDs, or credential IDs.
8. For tool bindings, copy identity and schema fields from a target-workspace export or registry response. Never infer opaque IDs from display labels.
9. When canonical source markers are used, synchronize them before validation. This is mandatory for `dev-dsl` repository mode:

   ```bash
   python3 scripts/sync_code_nodes.py path/to/app.yml --source-root docs/dify-code-nodes --write
   python3 scripts/sync_code_nodes.py path/to/app.yml --source-root docs/dify-code-nodes
   ```

10. Apply deterministic layout. Resolve this skill directory, install its pinned Node dependencies once with `npm install`, then run:

   ```bash
   node scripts/layout_dify_dsl.mjs path/to/app.yml --write
   node scripts/layout_dify_dsl.mjs path/to/app.yml --check
   ```

11. Validate final YAML with the bundled validator:

   ```bash
   python3 scripts/validate_dify_dsl.py path/to/app.yml --target-version 0.7.0 --portable
   ```

   If the skill is installed elsewhere, resolve `scripts/validate_dify_dsl.py` relative to this `SKILL.md`.
12. Treat validator, source-sync, and layout errors as blockers. Treat warnings as prompts to compare with a target-version export.
13. State whether the result is a structure draft, a pre-import validated candidate, or a file verified by real import. Static validation does not prove installed dependencies or runtime behavior.

## Portable Output Rules

- Keep `kind`, `version`, `app.mode`, and the selected top-level configuration style consistent.
- Use Workflow `end` nodes for batch workflows and Chatflow `answer` nodes for conversational graphs.
- Prefer readable, stable node IDs for newly authored source files, but preserve numeric IDs from user-owned exports when changing them would add risk.
- Include complete edge metadata and keep `sourceType` and `targetType` aligned with connected nodes.
- Keep product-visible names and descriptions useful to the application user. Put implementation instructions in prompts, code comments, or engineering documentation.
- Use native file-producing outputs for file and vision inputs. Do not invent custom Code node `array[file]` outputs.
- For bodyless HTTP requests, include `body: {type: none, data: []}`.
- Every Document Extractor declares boolean `is_array_file`.
- Every LLM node declares a `context` mapping; use `context: {enabled: false, variable_selector: []}` when context is unused.
- Keep Code node input names aligned with `main(...)` parameters and declared output names aligned with returned keys.
- Keep identifiers concise and preserve existing names unless the target Dify version documents a stricter field limit.

## Version Policy

The bundled validator defaults to App DSL `0.7.0` when it cannot discover a nearby Dify source checkout. Pass `--target-version` for older or newer instances. A version match is necessary but not sufficient because individual node shapes and plugin bindings can change independently.

## Completion Standard

A generated workflow is complete only when:

- graph structure and selectors validate;
- every managed Code node matches its canonical source;
- automatic layout is idempotent and reports no overlap;
- portable mode passes when the artifact is intended for sharing;
- remaining workspace-specific dependencies are disclosed;
- the user is told whether real import/runtime verification was performed.

## Security Boundary

Generated portable DSL must not contain real secrets or workspace-bound identifiers. Use placeholders only when the user explicitly requests a template, and label them clearly. Do not deploy, publish, install plugins, or mutate a Dify workspace unless the user separately authorizes that action.
