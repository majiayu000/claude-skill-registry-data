---
name: memory-maintenance
description: "Use when an agent needs to update, delete, supersede or audit an existing memory entry, or manage its edges, comments and hierarchy - after verification, when a finding goes stale, when a rule needs amendment, recovering a soft-deleted memory, or reading change history. Covers edit vs supersede, the unlink-supersede footgun and the hard-delete gate."
version: "0.11.0"
license: "Apache-2.0"
---

# Maintaining thrum memory entries

> **Before writing or editing any memory or state entry, apply "A memory states the current rule" in `thrum-memory`:** a
  memory states only the CURRENT rule (exceptions allowed), never a timeline of rulings, corrections or reversals, and
  every touch re-examines the whole memory.

## Editing an entry

```bash
cat > /tmp/memory-edit-body.md <<'EOF'
<updated body>
EOF
thrum memory edit <id> --short "@/tmp/memory-edit-body.md"
thrum memory edit <id> --title "<updated title>"
thrum memory edit <id> --add-tag <new-tag>      # repeatable; --rm-tag removes
```

`edit` needs the memory.substrate entitlement; `delete` and `unlink` do not.

Every edit writes a history record. The daemon keeps the prior version:

```bash
thrum memory history <id>             # chronological events touching <id>
thrum memory history <id> --diff      # unified field-level diff of each edit
```

| Situation | Action |
| --- | --- |
| Small correction (typo, clarification, tag refinement) | **Edit**: keeps the identity and records the change in history |
| The fact has changed but the topic is still relevant | **Edit**: same topic, evolving content |
| The entry is superseded by a fundamentally different fact | **Supersede**: write a new entry, delete the old one, and link `supersedes` |

For research notes, a stale `Verified:` stamp is handled by the researcher protocol in your role preamble: re-check the
cited paths, then edit the entry to replace the stamp, or supersede it when the claims have drifted. For role-rules,
staleness is event-driven: when your behavior is corrected or policy changes, edit the entry and update its `Why:` line.

## Deletion

Soft delete is the default. The entry is marked deleted and kept in the store, recoverable through the tombstone
protocol:

```bash
thrum memory delete <id>
```

Soft-deleted entries drop out of default search. Show them with `--include-purged` or `--status all`. Edges stay in
place.

Hard purge is irreversible. It removes the row, tags, edges and full-text shadow, and authorizes JSONL compaction on the
next sync. The confirmation token must match exactly; without `--confirm` the command falls to an interactive prompt
that hangs in non-interactive contexts:

```bash
thrum memory delete <id> --hard --confirm "DELETE <id>"
```

Use hard purge only when the body must be physically removed: credentials or customer PII captured by mistake, a create
that recorded clearly wrong content the team agrees should leave no trace, or a legal requirement. Everything else gets
one of these instead:

- Edit with the corrected content. The audit trail keeps the original.
- Supersede with a new entry. The old one moves to `status=superseded`.
- Soft delete. The audit trail stays.

The audit trail is the reason memory exists beside ad-hoc notes. A hard purge removes it.

## Undelete and recovery

Undelete writes `status=active` back. It needs the memory.substrate entitlement:

```bash
thrum memory edit <id> --status active
```

Undelete works regardless of who won a concurrent edit and delete, and the recovered entry keeps its full provenance.

**Conflict resolution is last-write-wins by event ULID**, not semantic priority. The larger ULID wins.

| Scenario | Result |
| --- | --- |
| Concurrent edits to disjoint fields | Both apply |
| Concurrent edits to the same field | Larger-ULID event wins; the loser stays in the JSONL |
| Concurrent tombstones | Idempotent; one delete wins by timestamp; `status=purged` |
| Edit and delete, delete ULID larger | Final `status=purged` |
| Edit and delete, edit ULID larger and it sets `status=active` | Edit wins: `status=active` (undelete) |
| Edit and delete, edit ULID larger and it does not touch `status` | The patch applies to body and tags; `status=purged` persists |

When `memory edit` returns hint `MEM-009: memory.edit.lww-loser`, the losing value was overwritten. Find the losing edit
in `thrum memory history <id> --diff`, lift the wanted value, and re-apply it as a new edit, which becomes the latest
ULID. If both sides had useful changes, record the alternative wording in a `comment` child instead of overwriting.

## Audit trail

Every event (`memory.create`, `memory.edit`, `memory.delete`, `memory.edge.add`, `memory.edge.remove`,
`memory.purge_executed`) appends to the author's `memories/<agent_id>.jsonl`. The JSONL never mutates; replaying it
rebuilds the projection. Provenance lives in the durable `memory-events-v2/` lane, so it survives events.jsonl
compaction and cold boot.

```bash
thrum memory history <id>                      # chronological, durable lane
thrum memory history <id> --diff               # with field-level patches
thrum memory show <id> --format json           # created_at, created_by, last_edited_by, edit_count
```

The projection keeps `created_at` (first event), `updated_at` (latest), `created_by` (first author) and `last_edited_by`
(latest author). Each history row carries the author, the ULID timestamp, and for edits the field patch.

## Edges

| Kind | Meaning | Use |
| --- | --- | --- |
| `supersedes` | A replaces B. Adding the edge also sets `B.status=superseded`. | A new `arch_decision` overrides an older one; a consolidated summary replaces several stale ones |
| `child_of` | A is a sub-piece of B. Forms a tree; single parent. | A `worktree_status` row under a `session_summary`; a `comment` under its parent |
| `related_to` | A and B share context; symmetric and advisory. | Two `arch_decision`s touching one subsystem |
| `derived_from` | A was generated or distilled from B. | A short summary derived from the full body |

Edge kinds are an open string. New kinds need no schema change.

```bash
thrum memory link <a> supersedes <b>
thrum memory link <child> child_of <parent>
thrum memory unlink <a> supersedes <b>
```

**Read semantics are status-driven.** Adding a supersede edge writes the superseded entry's status in addition to the
edge. Default assembly and search filter on `status=active`. The answer to "is this memory current" is always the status
field, never an edge walk.

**Unlinking a supersede does not restore the old entry.** The edge goes, but `status=superseded` stays. To undo a
supersede, do both steps:

```bash
thrum memory unlink <new-id> supersedes <old-id>
thrum memory edit <old-id> --status active
```

To keep the historical link but surface the old entry, run only the `--status active` edit and leave the edge.

**Cycles.** `supersedes`, `child_of` and `derived_from` are acyclic: a bounded depth-first search at write time rejects
a cycle. The bound is `memory.limits.edge_depth` (default 32). A chain past the bound returns
`ErrMemoryEdgeChainTooDeep` with the chain length, the limit, and a hint to consolidate with `supersedes` or raise the
limit. `related_to` is undirected, so cycles are allowed.

**Plurality.** `child_of` allows one parent per memory. The other kinds allow many: a consolidation can supersede
several entries, and a summary can derive from several sources.

**Comments.** A comment is a memory of kind `comment`:

```bash
thrum memory create --kind comment \
  --title "Note on Tailscale sync" \
  --oneline "Confirmed leaving git a-sync removes the dual-consumer conflict." \
  --parent <X-id>
```

`--parent` creates the `child_of` edge in the same operation. Author is the `agent_id`; timestamp is `created_at`.
Comments carry the same predicates, history, edges and embeddings as any memory.

**Hierarchy navigation.** Edge writes are on the CLI (`link`, `unlink`, `create --parent`). Edge reads are daemon-RPC
only today (`memory.listByEdge`), and `show` does not render edges. Navigate hierarchies by convention: give children a
shared tag (the parent's slug) and walk with `thrum memory search --tag <slug>`.

| Limit | Default | Configurable via |
| --- | --- | --- |
| Edge depth (acyclic kinds) | 32 | `memory.limits.edge_depth` |
| Outbound edges per memory | 64 | `memory.limits.edges_per_memory` |

## Related

- Writing new entries, including supersedes: `thrum-memory`.
- Advanced search: `memory-search-advanced`.
- Your role's memory section in its role preamble: the researcher's cite-stamp and staleness protocol, the coordinator's
  and implementer's write triggers.
