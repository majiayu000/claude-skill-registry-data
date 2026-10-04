---
name: selecting-models
description: Wraps host.bridge.model_registry_client.discover() so the planner can ask "which models are installed for capability X?". Returns either a list of ModelHandle dicts or a MissingModelEnvelope. Used during planning, before any comfyui_execute sub-goal lands.
v1_2_match:
  kinds: [model_resolve]
  capability: selecting-models
v1_2_output: model_handle
---

# selecting-models

Planning-category skill (v1.2 Stage 6). Scripts:

- `scripts/select.py` — stdin `{"capability": str, "requested_for": str?}`,
  stdout either a `ModelHandle` JSON or a `MissingModelEnvelope` JSON.

## Behavior

1. Build a `ModelRegistry` against the live ComfyUI base URL.
2. Call `reg.resolve(capability, requested_for)`.
3. If a match: emit the `ModelHandle` (capability, folder, name, matched_glob).
4. If no match: emit a `MissingModelEnvelope` with the sanctioned download
   candidates from `policies/model_sources.yaml`. The planner is responsible
   for deciding whether to insert a `model_download` sub-goal or surface the
   envelope to the user.

## CLAUDE.md compliance

- §12 #3 — registry is discovery-driven; this skill never reads a hardcoded list.
- §12 #5 — missing model surfaces an envelope, never silently substitutes.
