---
name: hypothesis-proximity-update
description: Update hypothesis proximity state by invoking the canonical embedding bridge for one hypothesis.
---

# hypothesis-proximity-update

Goal:

- Update hypothesis proximity state by invoking the canonical embedding bridge for one hypothesis.

Inputs:

- optional existing `state/PROXIMITY_GRAPH.json`
- target `hypothesis_id`
- run-frozen embedding provider settings from `state/RESOLVED_RUN_CONFIG.json`

Outputs:

- updated `state/proximity_receipts/<hypothesis_id>.json`
- updated `state/PROXIMITY_STATUS.json`
- updated in-memory `ProximityGraphContract`
- updated `state/PROXIMITY_GRAPH.json` when the provider returns a valid embedding
- updated `state/PIPELINE_STATE.json`
- updated `state/CURRENT_STAGE.json`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/state.py` and confirm the exact `ProximityGraphContract` shape before writing `state/PROXIMITY_GRAPH.json`.
- Read `packages/agent_contracts/proximity.py` and confirm the proximity receipt and status schemas before interpreting provider outcomes.
- Read `packages/agent_contracts/pipeline_runtime.py` before updating `state/PIPELINE_STATE.json` or `state/CURRENT_STAGE.json`.
- Load the current proximity graph if it exists. If it does not exist yet, start from an empty `ProximityGraphContract`.
- Treat embedding generation as a bridge/tool concern. Host agents must not generate, infer, paste, or hand-write numeric embeddings in prompt output.
- Do not skip this skill merely because no embedding vector is already present in the execution context.

Execution Contract:

- This skill is deterministic and must not call an LLM.
- Use `from tools import sync_pipeline_stage_artifacts` as the canonical paired write surface for entering the `Proximity` substage.
- On entry, call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Proximity", current_skill="hypothesis-proximity-update")`.
- Use `from tools import update_hypothesis_proximity` as the stable invocation surface.
- The exported bridge is implemented in `packages/agent_mechanics/hypothesis_embedding.py`.
- The canonical hypothesis-to-embedding text formatter is implemented in `packages/agent_mechanics/hypothesis_embedding_text.py`.
- The helper signature is `update_hypothesis_proximity(run_dir, hypothesis_id, config=None, provider=None) -> ProximityEmbeddingReceiptContract`.
- The bridge formats the hypothesis text, reads the run-frozen proximity provider settings from `state/RESOLVED_RUN_CONFIG.json` unless an explicit test config is passed, calls the configured provider when enabled, records a proximity receipt/status, and updates `state/PROXIMITY_GRAPH.json` only when a valid embedding is returned.
- Provider-specific backends such as `openai_compatible` and `gemini` must remain behind `tools.update_hypothesis_proximity(...)`; host agents must not call provider SDKs directly or paste provider-returned vectors into artifacts.
- The lower-level graph helper remains `tools.update_proximity_graph(...)`, implemented in `packages/agent_mechanics/proximity_update.py`; host agents must not call it with prompt-fabricated vectors.
- This skill must not hand-write embeddings, infer embeddings from hypothesis prose, or fabricate placeholder numeric vectors.
- If the provider is disabled, unavailable, invalid, or fails, preserve the bridge-written receipt/status, do not fabricate a graph update, and return control to ranking with receipt-gated fallback semantics.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/state.py`, `packages/agent_contracts/proximity.py`, and `packages/agent_contracts/pipeline_runtime.py` before writing proximity or run-level stage artifacts.
2. Before running the bridge, call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Proximity", current_skill="hypothesis-proximity-update")`.
3. Confirm the target `hypothesis_id` identifies an existing canonical `hypotheses/<id>/HYPOTHESIS.json` artifact.
4. Call `tools.update_hypothesis_proximity(run_dir, hypothesis_id)` exactly once for the target hypothesis.
5. Inspect the returned `ProximityEmbeddingReceiptContract` and the persisted `state/proximity_receipts/<hypothesis_id>.json`.
6. If the receipt status is `succeeded`, validate the updated `state/PROXIMITY_GRAPH.json`.
7. If the receipt status is `skipped_disabled`, `skipped_provider_unavailable`, `failed_provider_error`, or `failed_invalid_embedding`, preserve the receipt/status and return control to ranking. Do not infer or fabricate placeholder embeddings from text, IDs, or manual feature heuristics.
8. Validate the updated receipt/status artifacts before declaring completion.

Artifact Rules:

- `state/PROXIMITY_GRAPH.json` must remain the canonical persisted graph artifact.
- `state/proximity_receipts/<hypothesis_id>.json` is the canonical per-hypothesis embedding bridge receipt.
- `state/PROXIMITY_STATUS.json` is the canonical run-level proximity bridge status artifact.
- Similarity edges must stay symmetric across both hypothesis IDs.
- Each persisted graph embedding should include metadata for provider, model, dimensions, input text hash, and embedding config hash.
- If the graph already contains the target hypothesis ID with the same embedding input hash and embedding config hash, the bridge may confirm the existing state through a `succeeded` receipt with `graph_updated=false`; do not duplicate entries.
- If the graph already contains the target hypothesis ID with different or missing input/config metadata, preserve the bridge receipt and do not overwrite the existing embedding in prompt code.
- Placeholder embeddings, manually engineered stand-in vectors, or prose-derived pseudo-embeddings must never be written into the canonical graph artifact.

Completion Rule:

- This skill is complete only when `tools.update_hypothesis_proximity(run_dir, hypothesis_id)` has returned a persisted receipt and either `state/PROXIMITY_GRAPH.json` validates after a `succeeded` receipt or the receipt/status explicitly records why the graph was not updated.
