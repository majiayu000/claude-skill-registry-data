---
name: reversible-bulk-file-consolidation
description: "Design and prove a bulk move/merge/delete over shared or production storage (network share, asset repo, dump archive) so it is dry-run-first and byte-exactly reversible — use when asked to \"tidy up\", \"merge duplicate folders\", or \"clean up\" a directory tree that other people or tools depend on."
---

# Reversible bulk file consolidation

For any task that moves, merges, or deletes many files on storage you do not
solely own — a UNC share, an asset repo, a crash-dump archive, a shared
scratch volume. The blast radius is other people's data, so the design is
fixed before any code: **plan → refuse → log → act → undo**.

## 1. Establish who else writes there, first

Before proposing anything, grep the codebase for every write rooted at the
target path — `open(`, `write_text`, `mkdir`, `shutil.copy*`, `shutil.move`,
`rmtree`, `unlink` — and classify each as READ or WRITE. Two findings change
the design:

- **An existing writer** means a concurrent process may be mid-write. Find its
  trigger and whether it must be stopped during your operation.
- **A stale "read-only" claim in a docstring or config comment.** Trust the
  call sites, not the prose; comments about shared storage rot silently.

Also read whatever *consumes* the layout (a scanner, an importer, an indexer).
Its expectations constrain the merge — see §3.

## 2. Split into `plan` / `apply` / `undo`

```python
@dataclass(frozen=True)
class Move:      src: Path; dest: Path
@dataclass
class MergePlan: canonical: Path; moves: list[Move]; empties: list[Path]
                 retained: list[Retained]     # could not be emptied, and why
                 before: str; after: str      # the index/manifest text
                 batch_id: str                # deterministic hash of the plan
```

- `plan()` is **pure but for reading**. Prove it: hash the whole tree before
  and after calling it, assert equality.
- `apply(plan, undo_log)` performs it.
- `undo(undo_log, batch_id)` reverses one batch, newest action first.

`batch_id` = hash of canonical + the move pairs. Deterministic, so re-planning
names the same batch and the operator can undo without having captured a
return value.

## 3. Respect the consumer's layout

The most common design error is merging at the wrong depth. If a scanner
identifies units by a *naming pattern* (timestamps, hashes, a prefix), nesting
one unit inside another hides it. Find the pattern (`_STAMP_RE`-style regex,
glob, suffix rule) and merge **at the level the scanner enumerates**, not the
level the request literally described. Say so plainly when correcting the ask:
name the regex/line that forces it.

## 4. Refuse before acting, never mid-way

All validation runs before the first mutation:

- a unit missing its index/manifest file — merging it produces something the
  consumer silently skips;
- any path under an archive/quarantine/retired subtree;
- a destination that already exists (suffix instead of overwrite — reuse the
  project's existing collision convention rather than inventing one);
- a source holding anything unexpected → leave it standing, record it in
  `retained`, never force-remove.

## 5. Log before you act

Append one fsync'd JSON line **before** each move/delete, not after, so a
process killed mid-run is still reversible. Store deleted content inline
(small text files like the index/manifest) so `undo` never depends on the
share being reachable.

Keep the undo log on **local** storage, not the target — a log inside a
directory the operation removes is not a log.

## 6. Preserve bytes exactly

- Read with `read_bytes` / `open(..., newline="")`, never `read_text` +
  `write_text`: on Windows that silently converts CRLF→LF and rewrites every
  line of the file, defeating byte-exact undo.
- Write via temp-file + `os.replace`, never in-place.
- Keep the untouched prefix of any edited index file byte-identical, and
  assert that in a test.

## 7. Make it re-runnable

A move whose destination already exists is a no-op, not an error. A second
`apply()` must leave both the tree hash **and the undo-log size** unchanged —
assert both; re-logging a no-op is a bug.

## 8. Prove it without touching production

1. Build a fixture in a temp dir mirroring the **real** layout (copy a real
   index file's structure, not an invented one).
2. Assert after `apply`: the consumer's own scanner sees one unit with the
   combined count; the index still satisfies every parser that reads it;
   second apply is a no-op; `undo` restores a whole-tree sha256 match.
3. Assert every refusal fires and leaves the tree hash unchanged.
4. Assert a half-finished run (moves logged, index rewrite never reached) is
   still fully reversible.
5. **Dry-run against production read-only**, print the plan, then re-list the
   target and show the entry count is unchanged.

## 9. Ship it dry-run-first

The CLI default writes nothing. `--apply` is explicit. Also provide
`--tickets-only`-style partial modes so the safe half (metadata, database
links) can proceed when the share is unreachable — never make the local work
depend on a network path.

Refuse `--apply` while the consuming service is running, naming why
("it re-ingests the share on a cycle and would be scanning folders as they
move"), with `--force` to override.

Process groups **one at a time**, catching per-group failures and continuing —
one bad unit must not abandon the other twenty-six.

## Hand back

Report: what would change, the undo command, and what is still unauthorised.
Applying to shared storage is the operator's call even when they approved the
*policy* earlier — approving a design is not approving a specific batch.
