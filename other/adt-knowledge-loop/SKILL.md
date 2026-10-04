---
name: knowledge-loop
description: Composite skill — query, capture, improve, and persist knowledge in one workflow. Chains recall (RAG query) → sync-memories (write durable note) → rag-curate (improve weak retrievals) → handoff (durable snapshot if session-ending). Use when the work involves "what did we decide", "remember this", "save where we are", or any closing checkpoint.
user-invocable: true
auto-invoke: end-of-task + recall-questions + checkpoint-requests
metadata:
  owner: global-agents
  tier: contextual
  canonical_source: ~/.claude/skills/knowledge-loop
---

# Knowledge Loop

Unifies the three knowledge systems (RAG index, claude-mem, handoffs) into one workflow
so capture and retrieval stop being separate manual acts.

## Auto-invocation triggers

- User asks "what did we decide about X" / "where did we leave Y" / "is there a memory note for Z"
- End of a meaningful task (commit landed, PR merged, decision reached)
- User explicitly says "remember", "save this", "checkpoint", "handoff"
- Session-budget guard signals approaching context limit

## Workflow

### Phase 1 — Query (always)
Invoke `recall` (or `adt-rag-recall` for repo-scoped queries) with the user's question
or the active task topic. If the user is asking a recall question, return the answer
immediately and skip Phase 2/3 unless they also asked to capture something.

### Phase 2 — Capture (if new knowledge produced)
Invoke `sync-memories` with what was learned, decided, or built this session. Skip if
the session was pure read/recall with no durable output.

### Phase 3 — Improve (conditional)
If recall returned weak hits (cosine <0.40) for a query that should have hit something,
invoke `rag-curate` to add the missing doc or rewrite the weak chunk. Skip if recall
was strong.

### Phase 4 — Snapshot (if session-ending or context-pressured)
Invoke `handoff` to write a durable resume packet. Skip if work continues immediately.

## Reconciliation

Output a single capture summary:
```
KNOWLEDGE LOOP — <topic>
  Recalled:  <n> hits, top cosine <X> (skill: recall)
  Captured:  <memory file paths> (skill: sync-memories)
  Improved:  <chunks rewritten / docs added> (skill: rag-curate)
  Snapshot:  <handoff path> (skill: handoff)
```

If a phase was skipped, mark it `(skipped: <reason>)` so the trail is visible.

## Outputs / Evidence

- Recall results inline
- Memory files written (paths + one-line preview)
- RAG re-index confirmation (chunk delta)
- Handoff path if Phase 4 ran

## Failure / Stop Conditions

- If recall returns nothing AND no new knowledge was produced this session → exit clean,
  no capture needed
- If `sync-memories` and `rag-curate` would write to the same file → consolidate writes
  to avoid double-update churn
- Never skip Phase 4 if context is >80% — handoff is required for cross-session continuity

## Worked example

End of a multi-round token-optimization session that shipped 15 hooks + a /caveman skill + autocompact tuning.

```
KNOWLEDGE LOOP — token optimization rounds 1-4
  Recalled:  3 hits, top cos 0.50 (skill: recall)
  Captured:  token_opt_round4_2026-05-13.md + token_baseline_2026-05-13.md
             (skill: sync-memories — manual write because the work was
              still in-flight when the prompt arrived)
  Improved:  (skipped: RAG hits strong, no curation needed — top cos 0.50
              is above the 0.40 weak-hit threshold)
  Snapshot:  handoffs/latest.md + precompact_snapshot_2026-05-13T23-53-44Z.md
             (skill: handoff — auto-written by PreCompact hook 5 min earlier,
              so phase 4 was effectively idempotent)
```

Key points the example demonstrates:
- Each phase output names the underlying skill, even when invoked indirectly (PreCompact hook fired `handoff` for me).
- A skipped phase says **why**, not just "skipped" — the threshold (cos 0.40) is the audit trail.
- Capture and Snapshot can land in the same turn without conflict; both write to `memory/`.
