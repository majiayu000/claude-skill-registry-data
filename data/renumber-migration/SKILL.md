---
description: "STUB — not yet hydrated for this project. Resolve a sequential migration-number collision after another branch landed migrations first: adopt theirs, renumber yours on top, re-parent any snapshot. Hydrate this file against the project's migration tool before invoking it."
---

> ⚠️ **STUB.** This skill has no working procedure yet. Before it can be
> invoked, fill in: the migration tool, the file naming scheme, whatever
> journal/snapshot/checksum files accompany a migration, and the commands to
> regenerate them. Delete this banner once you have. If the project's migrations
> are not sequentially numbered, delete the skill instead.

## What this skill is for

Fixing the collision that happens whenever two branches each add migration
`0042` and one of them lands first. It's mechanical, it's easy to get subtly
wrong, and getting it wrong corrupts the migration history rather than failing
loudly.

## Concerns that hold regardless of stack

Each is something a hydrated version must handle.

### Sequential numbers collide by construction

Any scheme where the next migration is "highest + 1" collides across concurrent
branches. This isn't an edge case; it's the normal cost of readable ordering.
The skill exists because the collision is routine.

### Detect the fork first

Find the point where this branch's migrations diverged from the base's, and
which numbers the base has since claimed. Everything downstream depends on
getting this boundary right.

### Adopt theirs, then renumber yours on top

Take the base's migrations at their existing numbers — they've already run
somewhere — and renumber this branch's on top of them so the sequence stays
contiguous. Never renumber the ones that landed first.

### Never renumber a migration that has already run

The hard rule. If a migration has been applied in _any_ environment, its
identity is recorded there. Renumbering it makes the recorded history and the
repository disagree, and the failure surfaces later, somewhere else, as a
migration that mysteriously re-runs or is mysteriously skipped.

### Re-parent the accompanying files

Most migration tools keep more than the SQL: a journal, a schema snapshot, a
checksum, a "previous migration" pointer. Renumbering the file and leaving those
stale is the most common way this goes wrong. Name every such file in the
hydrated version and say how each is regenerated.

### Verify by replaying

After renumbering, run the migrations from scratch against an empty database and
confirm the resulting schema matches the snapshot. That replay is the only real
proof the sequence is coherent.

## Related

This is usually reached from `/finalize` Step 2, where merging the base branch
is what surfaces the collision in the first place.
