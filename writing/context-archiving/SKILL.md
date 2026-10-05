---
name: context-archiving
description: >
  Plan and execute hot-to-cold processkit context archiving while keeping
  archived entity metadata queryable through the shared index.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-context-archiving
    version: "0.2.0"
    created: 2026-04-30T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: index-management
        purpose: Query entity metadata before selecting archive candidates.
      - skill: event-log
        purpose: Record archive execution events when the write path exists.
    provides:
      primitives: []
      mcp_tools:
        - describe_archive_policy
        - plan_archive
        - create_archive
        - extract_archive_payload
      assets: []
---

# Context Archiving

## Intro

`context-archiving` manages the cold tier of processkit context. It identifies
stable archive candidates, packages their Markdown payloads into cold storage,
removes the hot files, and leaves metadata discoverable through
`index-management`.

## Overview

Use this skill when context size is becoming expensive, old completed work is
rarely read, or log/event payloads need to move from the hot tree into a cold
archive while metadata remains queryable.

The cold-tier target shape is:

1. Select stable entities by kind, state, and age.
2. Package payload files into a content-addressed `tar.gz` archive.
3. Keep index rows queryable with `storage_location` pointing at the archive.
4. Extract full payloads on demand for historical queries.

Version `0.2.0` implements this shape with a dry-run-first archive writer and
explicit payload extraction tool.

### MCP Tools

| Tool | Purpose |
|---|---|
| `describe_archive_policy()` | Return the default hot/warm/cold policy. |
| `plan_archive(kind, state, older_than_days)` | Return candidate entities from the live index. |
| `create_archive(kind, state, older_than_days, limit, dry_run)` | Write a `tar.gz` archive plus manifest, remove hot files, reindex, and log the archive event. Defaults to dry-run. |
| `extract_archive_payload(entity_id)` | Resolve an archived entity and return its full Markdown payload from cold storage. |

### Default Policy

- WorkItems: archive terminal states after 30 days.
- DecisionRecords: keep accepted/superseded decisions hot for 90 days.
- LogEntries: shard by month; archive payload shards after 90 days.
- Migrations: archive applied or rejected history after 30 days.
- Never archive active, proposed, blocked, or in-progress entities.
- Never archive files under `context/templates/`.

## Gotchas

- **Do not move entity files by hand.** The index must keep metadata queryable
  after archiving, so any write path has to update `storage_location`
  transactionally.
- **Do not archive active state.** Backlog, in-progress, blocked, proposed, and
  active entities belong in the hot tier.
- **Treat logs as append-only.** A cold log shard can be packaged, but its event
  identity and timestamp metadata must remain queryable forever.
- **Do not trust filesystem age alone.** Use entity metadata timestamps and state
  from the index; git checkout times are not archival age.
- **Keep extraction explicit.** A historical query may need full payload text,
  but routine status and routing queries should stay metadata-only.

## Full reference

`create_archive()` writes two files under `context/archives/YYYY/MM/`: a
compressed tar payload and a JSON manifest. The manifest keeps entity metadata,
the original hot-tree path, the tar member path, a SHA-256 digest of each
payload, and the `storage_location` used by `index-management`.

After writing the manifest, the tool removes the archived hot files, rebuilds
the index, and records a `context_archive.created` event. `dry_run=True` is the
default and returns the exact candidate set without moving files.

Archived entities remain visible through normal index lookups. Use
`extract_archive_payload(entity_id)` only when the full historical Markdown is
needed.
