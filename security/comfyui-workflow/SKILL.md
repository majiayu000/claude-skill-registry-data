---
name: comfyui-workflow
description: Select, preserve, inspect, validate, patch, convert, and promote complete ComfyUI workflows from Story-Film's extension-local comfyui_workflows library.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# ComfyUI Workflow

## Read

- `../../references/WORKFLOW_SELECTION.md`
- `../../references/COMFYUI_WORKFLOWS.md`
- `../../references/COMFYUI_NATIVE_API.md`
- `../../references/COMFYUI_SECURITY.md`
- `../../references/COMFYUI_BOUNDED_WORKFLOW.md`
- `../../references/COMFYUI_WORKFLOW_CONTRACTS.md`
- `../../references/REFERENCE_AUTHORITY.md`
- `../../references/DIALOGUE_AUDIO_AUTHORITY.md`

## Workflow-first rule

A complete selected workflow is the generation configuration.

Do not ask the user to rebuild its model stack through separate adapter/checkpoint/VAE/text-encoder/LoRA questions. Do not let legacy `model_preferences.json` override the selected workflow.

Before constructing a new graph:

1. read `generation-workflow-setup`;
2. build the relevant numbered workflow catalog with `scripts/workflow_catalog.py`;
3. let the user choose by number;
4. record the selection;
5. materialize a project-owned copy.

Bundled workflow sources are under `../../comfyui_workflows/<task>/<model>/`. They are actual editable workflows, not sanitized blueprints.

## Bounded production workflow path

For ordinary Story-Film production recovery or workflow creation, use the Pi-native `story_comfy_workflow` tool when available after a workflow has been selected/materialized.

1. Start from the exact selected project-owned source.
2. Preserve that source. Never edit the bundled or package-custom extension original in place.
3. Identify UI versus API format.
4. Inspect the graph and required node classes.
5. When a live server is available, validate every required class and input against `/object_info`.
6. Verify the concrete model/resource names already stored in the workflow against the active server and node dropdowns where applicable.
7. Stage current project inputs and references.
8. Patch only named production values that the selected graph actually exposes: approved prompts, project input identities, output prefixes/IDs, requested dimensions, seeds, durations, or other explicit production parameters.
9. Run workflow-family contract validation when a contract applies.
10. For reference-driven graphs, write/audit `04_generation/comfyui/reference_bindings.jsonl` so prompt ordinals, graph inputs, `REF-###`/`MEDIA-###`, staged paths, and hashes agree.
11. Confirm the requested result reaches a live output node or documented retrievable output path.
12. Promote only a live-validated runnable API graph into `04_generation/comfyui/workflows/`.

If finalization reports a graph error, repair only the selected project-owned copy and retry. Do not replace it wholesale with a guessed model-family graph.

## Source discovery

The numbered workflow catalog can contain only:

- Story-Film built-ins under `comfyui_workflows/<task>/<model>/`;
- user/custom workflows under `comfyui_workflows/custom/<task>/<model>/`.

There is no four-choice limit. Story-Film never scans ComfyUI userdata, project workflow folders, arbitrary external paths, or template catalogs. A newly authored/exported workflow becomes selectable only after it is copied into the appropriate `comfyui_workflows/custom/` directory.

## Explicit workflow authoring

Workflow creation remains a supported Story-Film capability when the user explicitly asks to create, build, author, or design a new ComfyUI workflow.

This explicit authoring path is separate from catalog discovery:

1. use `story_comfy` live node/model discovery (`node-search`, `node-info`, model inventory/search, and other approved live-schema operations) to learn what the running ComfyUI actually supports;
2. build exactly one bounded candidate in a project staging/candidate location, never directly in the runnable workflow directory;
3. use only live-discovered class names, inputs, output types, and resource choices;
4. validate required inputs, links, output exposure, and model/resource availability;
5. do not install missing custom nodes or download models without the user's separate approval;
6. promote a project-specific candidate only after validation;
7. when the workflow is intended to become a reusable Story-Film choice, save or copy the validated JSON into `comfyui_workflows/custom/<task>/<model>/`, refresh the catalog, and select the resulting `package-custom` workflow normally.

Do not require a `generate-new` catalog entry before honoring an explicit user request to author a workflow. Conversely, do not silently author a new workflow merely because no existing catalog entry is ideal.

## Model and prompt behavior

The selected workflow owns its concrete checkpoint, diffusion model, VAE, text encoders, LoRAs, audio models, upscalers, and node-specific model fields.

Prompt adapters remain allowed for prompt grammar. Infer the applicable prompt adapter from the selected workflow/model family when needed; do not ask for a second generation model selection.

If a selected workflow names unavailable resources, report the blocker. Do not silently swap to another model or workflow.

## Bundled offline commands

```text
python scripts/comfyui_workflow.py inspect WORKFLOW.json
python scripts/comfyui_workflow.py classes WORKFLOW.json
python scripts/comfyui_workflow.py patch WORKFLOW.json --node 12 --input text --value 'new prompt' --out patched.json
```

Workflow selection and materialization:

```text
python scripts/workflow_catalog.py catalog PROJECT --category video --url http://127.0.0.1:8188
python scripts/workflow_catalog.py choose PROJECT 3
python scripts/workflow_catalog.py materialize PROJECT video --url http://127.0.0.1:8188
```

Live validation:

```text
python scripts/comfyui_control.py validate --workflow WORKFLOW.json
```

## Story-Film mapping

When mapping `comfyui_handoff.json`, process one shot or cue at a time. Map only named inputs that the selected live workflow actually exposes. Canon and approved prompts remain authoritative.

## Done

The workflow choice is durable, the source is preserved, the project-owned copy is known, required node classes and resource names are explicit, requested edits are minimal, and the runnable API graph passes the available preflight checks.
