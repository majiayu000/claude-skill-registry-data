---
name: story-film
description: Route story writing, books, screenwriting, directing, creative decision discovery, production specifications and work units, narrative state, creative review, storyboards, executable production, resource-safe AI media generation, generalized asset approval, audio mastering, timeline rendering, finished-film mastering, trailers, social campaigns, deterministic media editing, production documents, Kdenlive/Shotcut project export, and release packaging through a standalone file-based story-to-screen-and-release pipeline.
author: Alan Guice (Badgids)
license: Apache-2.0
compatibility: Pi Agent or another Agent Skills harness with file read/write tools. Python 3 is optional for validation scripts.
---

# Story Film

This is the general entry point for Story-Film Skills. The package is standalone.

When the user explicitly invokes Story-Film, this router, its selected playbook, and `00_project/pipeline_progress.json` are the Story-Film execution authority. Do not substitute stage sequences, pipeline commands, or routing rules from unrelated installed skill packs unless the user explicitly asks to combine them.

Resolve every relative path in this skill from this `SKILL.md`, not from the user's project directory or the package root. `CATALOG.md` is the file beside this router (`skills/story-film/CATALOG.md` in a Git package). Every `playbooks/<name>.md` path is relative to this router, so its Git-package path is `skills/story-film/playbooks/<name>.md`; never try `<package>/playbooks/<name>.md`. The listed router, catalog, playbooks, scripts, references, and sibling skills are known package paths. Do not use Bash, `find`, `ls`, or directory scans to rediscover them.

## Start

1. Read `../../references/STANDALONE_CONTRACT.md`.
2. Read `../../references/CORE_CONTRACT.md`.
3. Read `../../references/DOCUMENT_COMPANIONS.md`.
4. Read `../../references/WORKFLOW_SELECTION.md`.
5. Read `CATALOG.md` beside this file.
6. Match the request to exactly one playbook in `playbooks/`.
7. Read that playbook in full from `skills/story-film/playbooks/<playbook>.md` in a Git package.
8. For a new project with a multi-step playbook, initialize the project and authoritative progress ledger atomically with `../../scripts/init_story_project.py <project> [--title TITLE] [--format FORMAT] --playbook <playbook>`. Do not create `pipeline_progress.json` or `workflow_preflight.json` manually.
9. If the project already exists, or it was initialized without `--playbook`, read `../pipeline-progress/SKILL.md` and run `../../scripts/pipeline_progress.py init <project> --playbook <playbook>` before writing any story, canon, screenplay, preproduction, or generation artifact. A film/video project with an inactive progress ledger is not ready for creative production.
10. Pipeline initialization for a mapped ComfyUI-backed playbook creates the matching workflow-preflight state and makes `generation-workflow-setup` the first current target. Complete that target before any story or canon artifact is created; use `generation-workflow-setup` for every missing category until `workflow_preflight.py status` reports `complete`.
11. Do not begin story, canon, screenplay, preproduction, or generation-brief work while a required ComfyUI workflow preflight is incomplete. Later playbook stages reuse the durable selections and do not ask again unless the user explicitly requests a workflow change.
12. If ComfyUI is unavailable or a required workflow cannot be selected, mark the workflow-preflight target blocked. Do not continue into creative work and do not promise to return to preflight later.
13. If a matching progress ledger already exists, resume its current target instead of reconstructing progress from chat history or replacing the ledger.
14. Execute the playbook in order. Before each specialist step, read the named sibling `SKILL.md`.
15. After each actionable progress leaf, validate its artifact before checkpointing it complete. A blocking validation failure must remain on the same leaf and become `blocked`; it must not advance. Do not start a later specialist or write a later artifact until the current leaf is validated and checkpointed.
16. Update `00_project/state.json` after each completed artifact.
17. If an approved upstream artifact changes, run `project-impact` before rebuilding downstream work.
18. Run continuity, narrative-state, production-coverage when applicable, dramaturgy, prompt, standalone, and style checks at the gates required by the playbook.

## Routing rule

Do not invent a new workflow while a listed playbook fits. If more than one fits, choose the one whose final deliverable most closely matches the user request.

## Small-model rule

Work one artifact at a time. Save it. Validate it. Checkpoint the corresponding pipeline leaf. Then continue. For long work, process one chapter, scene, sequence, or stale dependency slice at a time. After restart or compaction, read `00_project/pipeline_progress.json` and `00_project/HANDOFF.md` before opening unrelated context.

If the host provides a generic Todo tool, do not duplicate the full Story-Film playbook there. Mirror at most three Story-Film items: current target, immediate next target, and requested endpoint. Refresh that mirror only after the authoritative Story-Film checkpoint advances.

## Standalone rule

Never stop required creative or preproduction work because another skill pack is missing. Create the native portable artifact defined by this suite. ComfyUI is optional for planning and packaging. When the user asks to operate or generate through an available ComfyUI server, route through the native `comfyui` capability rather than assuming another agent extension is installed.

## Creative planning routing

If the requested endpoint is a story bible, deep character/world lock, or durable cast/world development, route through `playbooks/story-bible-development.md`. Story-Film uses its existing distributed brief/canon/story/character/world/state artifacts instead of creating a project-specific skill as a second canon database.

If the user wants to pressure-test an idea, resolve creative ambiguity, turn existing discussion into a durable production specification, split a large production into executable work units, or chart a project whose route is not yet clear, route through `playbooks/creative-planning-and-execution.md`. Facts that can be discovered from files or tools are agent work; creative decisions remain the user's unless explicitly delegated.


## ComfyUI discovery precedence

Before any attempt to locate ComfyUI, determine whether its server is running, inventory installed models, search model filenames, inspect nodes, or discover workflows, read `../comfyui/SKILL.md` and `../comfyui-discover/SKILL.md`.

In Pi, `story_comfy` owns ordinary interactive live ComfyUI discovery. Do not use Bash, `find`, `ls`, `which`, `locate`, guessed personal paths, home-directory scans, model-folder scans, direct comfy-cli discovery commands, or raw ComfyUI HTTP calls for those facts. A failed guessed path or empty guessed folder proves nothing. If the managed Story-Film control surface fails, report that failure and use only the documented deterministic fallback from the ComfyUI skills.

## Generation workflow selection

Workflow choice is front-loaded. When the chosen playbook will require ComfyUI, complete `workflow_preflight.py` and `generation-workflow-setup` before creative production starts. Record every required task workflow in `00_project/workflow_preferences.json`. Later stages consume those selections without reopening the interview.

The selected workflow owns its concrete models, VAEs, encoders, LoRAs, audio models, upscalers, sampler settings, and other graph configuration. Reopen the numbered list only when the user explicitly requests a workflow change. A later dependency failure is a blocker, not authority to reselect silently.

## Production-integrity routing

For reference-driven generation, preserve `REF-###` authority scopes and run `reference-authority`. When adjacent approved shots need motion continuity, use `temporal-continuity`; previous-shot tails are visual-only and cannot import prior audio. When approved dialogue audio exists, use `dialogue-audio-authority` and `dialogue-timing-preflight` before expensive visible-speech generation. For ComfyUI reference graphs, use `comfyui-binding-audit` after staging or conversion. Physical cleanup of rejected media or repair of a disposable runtime copy routes through `media-lifecycle`, never directory sweeps or regeneration of an approved source.

## Resource-safe local generation routing

If the local LLM and ComfyUI cannot safely coexist in RAM or VRAM, route generation through `playbooks/resource-safe-comfyui.md`. Use `llm-model-lifecycle` for native llama-server or Ollama unload/restore. All prompts, workflows, uploads, parameters, dependencies, output destinations, and validation decisions must be finalized before the local LLM is unloaded. While the LLM is unavailable, only deterministic runners and the Pi progress extension may advance or report generation state.

## Rich-document companion rule

Every PDF, DOCX, DOTX, XLSX, XLSM, XLTX, PPTX, PPTM, ODT, ODS, or ODP created by this suite must have a meaningful Markdown file with the same basename beside it. A pointer-only Markdown file does not satisfy the rule.

## Deterministic media editing routing

If the request is about FFmpeg, FFprobe, MLT/melt, ImageMagick, Kdenlive project export, Shotcut project export, or deterministic media manipulation, route through `playbooks/media-editing-and-project-export.md`. Discover the installed runtime before using optional codecs, filters, delegates, devices, MLT services, or hardware features.

## ComfyUI execution routing

If the requested final deliverable is an actual ComfyUI inspection, workflow run, generated asset, queue action, or ComfyUI repair, choose the matching ComfyUI playbook. Live ComfyUI facts must be discovered at runtime.

## User control

If the user names a specific artifact or model, route directly to the corresponding specialist inside the chosen playbook when the supplied upstream inputs are sufficient.
