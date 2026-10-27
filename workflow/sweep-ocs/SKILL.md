---
name: sweep-ocs
description: >
  Find orphaned OCS chatbots, pipelines, collections, and sessions and delete per-opp clones; the
  template is protected. Needs a live-set from sweep-live-set.
disable-model-invocation: false
---

# sweep-ocs

Find OCS artifacts (chatbots, pipelines, collections, sessions) that no current opp references and triage them. Per-opp chatbots, pipelines, and collections are all owned by a single clone — safe to delete when the clone is. Sessions soft-close via `ocs_end_session`. The golden template chatbot and the shared collection it references are explicitly safe-listed.

## Critical safety boundary — what's per-opp vs shared

Verified 2026-05-15 against `apps/chatbots/views.py:copy_chatbot`, `apps/pipelines/models.py:Node.create_new_version`, and `apps/files/models.py:File`:

| Resource | On clone | Sweep behavior |
|---|---|---|
| Experiment (chatbot) | NEW row created | ✅ Auto-delete orphan clones |
| Pipeline | NEW row created via `create_new_version(is_copy=True)` | ✅ Auto-delete orphan clones |
| Per-opp Collection | NEW row created by Phase 5 `ocs_create_collection` | ✅ Auto-delete orphan clones (cascades to underlying File rows + object-storage blobs + FileChunkEmbedding vectors via `delete_document_source_task`) |
| Shared Collection (`OCS_SHARED_COLLECTION_ID`, typically 350) | SHARED — every cloned pipeline references it via LLM node `collection_id` (the `if not is_copy` branch in `Node.create_new_version` intentionally skips versioning collection refs on clone) | ❌ Never auto-delete — would break every clone |
| Golden template chatbot (`OCS_GOLDEN_TEMPLATE_ID`) | — | ❌ Never auto-delete |
| Files (in any collection) | Each File row is per-collection; no content-hash dedup at the file or blob layer | Cascades when collection is deleted |
| Embedding vectors | Per `(file, collection)` tuple | Cascades when collection is deleted |
| Chatbot version | Created per `ocs_publish_chatbot_version`; tied to parent experiment | Cascades when parent experiment is deleted |

No dedup at the file or vector layer means uploading the same PDD into 19 per-opp collections costs 19× storage + 19× embedding API calls. Deleting orphan per-opp collections reclaims real storage and pays back the embedding cost over the project lifetime.

## Inputs

- Live-set file path from `sweep-live-set`.
- `OCS_TEAM_SLUG`, `OCS_GOLDEN_TEMPLATE_ID`, `OCS_SHARED_COLLECTION_ID` from `.env`.
- `OCS_BASE_URL` (e.g. `https://chatbots.dimagi.com`).
- `mode` — `recommend` (default) | `execute`. In `recommend` the skill is **report-only**: diff/score/render + return the recommended-action list; **no mutations** (no deletes, no `ocs_end_session`). In `execute` it mutates only `approvedIds`. The human-confirmation gate between the two is the orchestrator's job — see `agents/sweep.md § Human-confirmation gate`.
- `approvedIds` (`execute` mode only) — the exact chatbot/session ids the human approved in chat. Mutate nothing outside this set (an approved chatbot's paired pipeline + per-opp collections follow it).

## Products

- `ACE/_sweep/<timestamp>/ocs-orphans.md` — human-readable triage report.
- `ACE/_sweep/<timestamp>/ocs-orphans.yaml` — machine-readable `OrphanReport`.
- For approved orphan chatbots: `ocs_delete_chatbot({ experiment_id })` calls.
- For approved orphan pipelines: `ocs_delete_pipeline({ pipeline_id })` calls.
- For approved orphan per-opp collections: `ocs_delete_collection({ collection_id })` calls.
- For approved orphan sessions: `ocs_end_session` calls.

## Process

1. **Read the live-set** via `drive_read_file`.
2. **Augment live-set with safety entries:**
   - Add `OCS_GOLDEN_TEMPLATE_ID` to `liveSet.identifiers.ocsChatbotIds` so the golden template chatbot is never an orphan candidate.
   - Add `OCS_SHARED_COLLECTION_ID` to `liveSet.identifiers.ocsCollectionIds` so the shared collection is never an orphan candidate.
3. **List OCS inventory** using existing atoms:
   - `ocs_list_chatbots` (paginate as needed). **List rows no longer carry
     `versions[]`** — as of ace#1901 the atom returns a two-field
     `versions_summary` ({`count`, `published_version_number`}) in its place,
     because on `connect-ace` the full array was 85.9% of a default page that
     already overflowed the tool-result cap (measured 2026-09-02: 50 rows /
     87,009 chars, of which `versions` was 74,733). `page_size` does not help —
     it shrinks a page, and the problem is the row. Version DESCRIPTIONS are
     read per-chatbot in step 3 below, or in bulk via `write_to_path`.
   - `ocs_list_sessions` (filter to `OCS_TEAM_SLUG`; last 90 days by default).
   - For each chatbot, derive its pipeline_id via `ocs_get_chatbot_pipeline_id({ experiment_id })` (added 0.13.277 — scrapes the pipeline-builder HTML; cached). Per-opp collection ids come from the chatbot's most-recent published version description (e.g. "shared Connect collection 350 + new per-run collection 418") — **read that description with `ocs_get_chatbot({ public_id })`, which still returns the full `versions[]`, and do it only for the chatbots that step 4's diff marked as orphan candidates.** Do not reach for it on the list row: `ocs_list_chatbots` projects `versions[]` away by default (ace#1901), and reading descriptions for every bot on the team is exactly the cost that broke the atom — the orphan set is a small fraction of it. (If you genuinely want every description at once, `ocs_list_chatbots({ write_to_path: '<abs path>' })` writes the unprojected rows to disk and returns only `chatbots_written_to`, so the payload never enters context.) Cross-check against the pipeline's LLM node params via the pipeline-builder page if the description is thin.
4. **Diff** each item's id against the live-set:
   - chatbots → `liveSet.identifiers.ocsChatbotIds` (now includes golden template).
   - sessions → `liveSet.identifiers.ocsSessionIds`.
   - pipelines → derived from orphan chatbots' pipeline_id (one pipeline per chatbot since deep-clone verified).
   - collections → `liveSet.identifiers.ocsCollectionIds` (now includes shared collection). Per-opp collections derived from orphan chatbots' LLM node collection refs minus the safe-list.
5. **Score** each orphan via `scoreOcsItem(item, liveSet, OCS_GOLDEN_TEMPLATE_ID)`. The scorer defensively downgrades items whose id matches `goldenTemplateId` (even though step 2 should have excluded them).
6. **Build the `OrphanReport`** with `system: 'ocs'`. Partition into:
   - **Actionable — auto-delete:** chatbots, their paired pipelines, and their per-opp collections.
   - **Actionable — auto-end:** sessions.
   - **Safe-listed (informational):** `OCS_GOLDEN_TEMPLATE_ID` chatbot + `OCS_SHARED_COLLECTION_ID` collection. Show them in the report so the human can verify the safe-list is correctly applied, but never propose deletion.
7. **Render** + write `ocs-orphans.md` and `.yaml` to the sweep folder.
8. **Recommend — stop here in `mode: recommend`.** Return the structured recommended-action list (orphan chatbots with their paired pipeline + per-opp collection ids; orphan sessions to end — each with id, name, confidence, and the reversibility note that collection deletes also purge File rows + embeddings) plus the safe-listed informational items and the report Drive link, to the orchestrator. **Perform no mutations.** Do not try to prompt the human from this skill — a dispatched subagent can't reach them; the orchestrator runs the confirmation gate (see `agents/sweep.md § Human-confirmation gate`).

## Execute phase (`mode: execute` only)

Runs only when the orchestrator re-dispatches with `mode: execute` + `approvedIds` (the chatbot/session ids the human approved in chat). For each **approved** orphan chatbot, in order:

- Call `ocs_delete_chatbot({ experiment_id })`.
- Call `ocs_delete_pipeline({ pipeline_id })` for the paired pipeline (resolved via `ocs_get_chatbot_pipeline_id` in step 3 — never skip this; pipeline deletes are the only way to clear the per-opp Pipeline row).
- For each per-opp collection_id derived in step 3, call `ocs_delete_collection({ collection_id })` — but ONLY if collection_id ≠ `OCS_SHARED_COLLECTION_ID`. The atom itself doesn't enforce this; the skill must filter.

For each **approved** orphan session, call `ocs_end_session`. Mutate nothing outside `approvedIds`; return the per-item result.

## Failure modes

- **Live-set path doesn't resolve:** abort with "Run `sweep-live-set` first."
- **`OCS_GOLDEN_TEMPLATE_ID` or `OCS_SHARED_COLLECTION_ID` not set in env:** abort. Without them, steps 2 and 9's safe-list filter can't run — refuse to act rather than risk the template or shared collection.
- **`ocs_list_*` returns 401:** session is stale; recommend `/ace:ocs-login` then retry.
- **A session is already ended:** treat as success (no-op).
- **A chatbot/pipeline/collection is already archived** (`is_archived=True`): treat as success (no-op).
- **Per-opp collection delete returns 4xx:** report the item as "delete failed — leaves orphan storage"; don't retry; don't halt the batch.

## Implementation notes for agents

- OCS uses `is_archived` soft-delete on `Experiment`, `Pipeline`, and `Collection` (`apps/experiments/models.py:641`, `apps/pipelines/models.py:115`, `apps/documents/models.py:103`). Collection delete additionally triggers `delete_document_source_task` to async-purge File rows and FileChunkEmbedding vectors.
- The chatbot/pipeline/collection delete URLs are at `/a/<slug>/<resource>/<id>/delete/`. Chatbot is POST (`@require_POST`); pipeline and collection are HTTP `DELETE` method (Django `View.delete()`). The `ocs_delete_*` atoms handle both.
- The "1 chatbot : 1 pipeline : N per-opp collections" invariant matters when computing the deletion batch. Read the chatbot's pipeline_id before deleting; same with the collection refs.
- Collection files use hard-delete via async task (`apps/documents/urls.py:15`). Once `delete_document_source_task` fires, files are gone — not recoverable from OCS admin UI. The `is_archived=True` flag on Collection itself is reversible (admin could unset it), but the underlying files would still be gone. The "deletion" is irreversible in practice.

## Related skills

- `sweep-live-set` produces the live-set this skill diffs against.
