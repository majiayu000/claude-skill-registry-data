---
name: comfyui-handoff
description: Build a standalone, portable ComfyUI-ready generation manifest containing canon links, references, briefs, prompt files, selected workflow identities, input requirements, output IDs, stale scope, and unresolved requirements without hardcoded machine details.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# ComfyUI Handoff

This skill creates a portable generation package. It does not require ComfyUI or another skill pack to be installed for planning.

## Workflow

1. Read the standalone contract, core contract, dependency rules, `WORKFLOW_SELECTION.md`, ComfyUI portable package contract, state, canon, continuity, references, and generation briefs.
2. Determine the smallest requested scope by sequence, scene, shot, cue, or stale asset.
3. Ensure model-neutral briefs exist for that scope.
4. For each generation task that will be executed through ComfyUI, use `generation-workflow-setup` to record the selected complete workflow. Do not run the retired model-resource interview.
5. Run the prompt adapter implied by the selected workflow only when prewritten model-specific prompts are part of the requested package.
6. Write `04_generation/comfyui_handoff.json` using project-relative paths only.
7. Include `workflow_preferences`, selected workflow identities or materialized workflow paths, prompt files, reference IDs and roles, required input media, expected output IDs, durations or dimensions when required, stale IDs, and unresolved requirements.
8. Never invent node class names, widget indices, personal model paths, or private custom-node schemas. The portable manifest describes intent plus the explicit selected workflow identity.
9. Run `prompt-qc` on included prompt documents.
10. If the user also requests execution, route next to `comfyui`: materialize the selected source, preserve a project-owned copy, validate against live node schemas, stage inputs, submit, and collect outputs.

## Workflow authority

The selected workflow owns the concrete checkpoint/model, VAE, text encoders, LoRAs, audio models, upscalers, node choices, and generation settings stored in its graph.

If a selected workflow cannot run on the active ComfyUI server, record that as an unresolved blocker. Do not silently choose another workflow or another model.

## Done

The standalone package contains enough generation intent and workflow identity for ComfyUI, another workflow compiler, another agent, or a human operator to map each task without reading the originating conversation. When execution was also requested, each submitted task is traceable to a live-validated workflow and returned prompt ID.
