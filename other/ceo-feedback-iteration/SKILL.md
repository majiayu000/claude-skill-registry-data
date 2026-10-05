---
name: ceo-feedback-iteration
description: Use when an Agent is asked to classify and improve open repository feedback through the managed feedback-iteration capability. The Skill owns the bounded diagnosis and decision protocol; the service owns capability state, persistence, and lifecycle transitions.
metadata:
  managed_by: ceo-agent-service
  version: 1
---

# CEO Feedback Iteration

Use only the local Console API at `http://127.0.0.1:8765/api/console/feedback`.
Read the batch and every selected detail before changing a Skill, configuration,
or code. Treat `feedback_key` as the stable identity. The supplied persisted
summary, detail references, runtime configuration, loaded revision numbers, and
SHA values are factual context; do not ask a model to regenerate a summary or
invent IDs. Direct SQLite writes are forbidden.

## Bounded discussion profile

1. Establish the observed behavior and loaded capability facts, then identify
   the likely root-cause class.
2. Use brainstorming only if a material product or policy uncertainty remains.
   Ask one focused user question at a time, offering alternatives and a
   recommendation. Do not require discussion when the facts establish the path.
3. Before any change, persist one typed decision through
   `POST /api/console/feedback/batches/{batch_id}/decisions`. Include the
   current `feedback_key` values, persisted references, root cause, acceptance
   scenario, expected behavior, and verification.
4. Use exactly one scope: `skill_only` when policy/procedure is deficient but
   data, tool, and route exist; `runtime_config` when a valid capability is
   incorrectly bound or disabled; `code` when a required capability is missing
   or defective; `mixed` only when both are needed; `needs_human` for missing
   reusable policy, authorization, or indispensable business facts.
5. Execute only the persisted path. `needs_human` never resolves feedback.

## Verification boundary

Read back the decision and batch history. Record path-specific evidence through
the feedback API; a later resolution must prove the selected path, including
the active runtime/load receipt for Skill or configuration work, or commit and
tests for code work. Never claim a new batch while feedback iteration is
disabled, and never change generic `brainstorming` to encode this protocol.
