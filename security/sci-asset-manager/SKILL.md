---
name: sci-asset-manager
description: Review and maintain research project assets without losing evidence metadata, including cleanup candidates, cold archives, migration manifests, submission keep lists, and deletion risk. Use when deciding what to keep, move, archive, deduplicate, or delete in a research workspace. Default to bounded review; create durable manifests only when needed. Never delete or move protected assets without explicit user authorization.
---

# SCI Asset Manager

Preserve evidence while reducing active-workspace clutter. Follow project-local rules and the provenance safeguards in `sci-research-manager`.

## Read ownership before storage

Start from handoff, experiment index/registry, relevant cards, and claim map. Use known run paths before scanning large artifact directories. Never open large binary weights merely to classify them.

## Always preserve

- experiment/family card;
- frozen config and code commit;
- result summary and authoritative raw result;
- run command/path;
- archive/migration note;
- claim-evidence relation;
- original timestamp/size and optional hash for path-sensitive moves.

Potential cleanup candidates include reproducible caches, duplicate logs, temporary outputs, superseded generated files, and large intermediate checkpoints whose evidence metadata is preserved.

## Review before action

Use the bundled templates for archive, cold-storage, submission-keep, and deletion reviews. Record path, owner, related ID/claim, reason, evidence risk, replacement, recommendation, and rollback.

Before an approved move, snapshot provenance with `sci-research-manager/scripts/provenance_guard.py`; prefer same-volume moves; update old-to-new mappings and links; then verify content, size, timestamp, symlink target, and optional hash.

## Keep deletion separate

Never delete files unless the user explicitly authorizes the exact scope. First produce `delete_review.md`. Treat unknown ownership as `needs_verification`. A cleanup review is not deletion permission.

Review assets when requested or when a concrete storage, provenance, or outgoing-package risk requires it. A probe or phase change alone does not trigger an extra audit, manifest, archive, or deletion workflow. A narrow review may return findings in the conversation; create a durable manifest for an authorized migration/deletion or when the project requires one.
