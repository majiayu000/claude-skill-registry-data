---
name: antfarm-crash-dedup-merge
description: "Use when asked to dedupe AntFarm (D:/NightSmith) crash tickets or tidy the //psrecap crash share, when ticket counts grow or a ticket named archive appears after a merge, or when changing how duplicate crashes are matched or auto-linked at ingest."
---

# AntFarm crash dedup and share merges

For D:/NightSmith. Reduces duplicate crash tickets and consolidates their folders on the
shared crash drive. The share is other people's data — every step is dry-run-first and
reversible.

## The two traps that cost real tickets

**1. A merge changes a crash's identity unless you pin it.**
`crashes._read_folder` reads subdirectories `sorted(..., reverse=True)` — newest first — and
takes `fingerprint`/`lua_stack`/`stack` from the first instance with a manifest. The group key
is `sha256` of that `cause` (`ident = repr(min(cause))`), and that key IS the ticket id. So
moving a *newer* bundle into a canonical folder changes its cause, its key, and its ticket id:
the next ingest files a brand new ticket for the crash you just tidied.

Fix already in the tree: `crash_merge.apply` writes `.antfarm-crash-key` (`crashes.IDENTITY_PIN`,
JSON `{"key": "crash-..."}`) into the canonical **before any bundle moves**, and
`group_by_fingerprint` prefers the pinned key over the evidence. If you add a code path that
moves bundles, it must write the pin too.

A folder merged *before* the pin existed keeps its post-merge id. Fix by hand, and do it
**before** linking the stray as a duplicate — otherwise the link absorbs a ticket nothing
points at:

```python
from antfarm.crashes import IDENTITY_PIN, DERIVED_KEY_RE
from antfarm.tickets import crash_ticket_id
assert DERIVED_KEY_RE.match(key) and crash_ticket_id(key) == key
(folder / IDENTITY_PIN).write_text(json.dumps({"key": key, "note": "..."}) + "\n", encoding="utf-8")
```

**2. `archive/` was ingested as one giant fake crash.**
`scan()` walked every top-level directory and `_read_folder` counts every subdirectory as an
occurrence, so retiring a crash re-filed it. `scan` now skips `crashes.ARCHIVE_DIR`. If a ticket
literally named `archive` appears, that skip has been lost.

## Matching rules

`dedupe.groups()` matches on **same crash site and masked detail** (`crash_family.family_of`)
**or** the first 3 **culpable** frames (`dedupe._culpable_frames`). Culpable means after
dropping the funnel — every stack here starts `ucrtbase` → `std::terminate` → `AbortImmediate`
→ `paInstallCrashHandler` → `ntdll`, so raw top-frame matching matches everything. Exclusions
live in `crash_title._is_handler_frame`, `crash_history.ABORT_PLUMBING` and
`dedupe.LUA_BRIDGE_PLUMBING` (`paluaerrorhandler.cpp`, `paluabindfunction.h`,
`paluaclassbinder.h`, `lj_api.c`, `paluabindinvoker.h`).

Adding a frame to the plumbing list is the safe direction (fewer merges). Measure before and
after on a **copy** of the DB:

```python
con = sqlite3.connect("file:.antfarm/antfarm.db?mode=ro", uri=True)
con.backup(sqlite3.connect(tmp))          # never open the live DB for writing
before = dedupe.groups(Store(tmp, log), log)
```

## Procedure

1. **Dry run** — `.venv/Scripts/python.exe -m antfarm.queen_cli dedupe`. Default writes nothing.
   Read the per-group plan: moves, empties, `retained`, info.md line delta. The dashboard's
   Ready-to-Fix panel and `GET /api/duplicates` show the same groups.
2. **Stop the colony** — `.venv/Scripts/python.exe -m antfarm.queen_cli stop`, then confirm
   `.antfarm/run.lock` is gone. `--apply` refuses while it runs (it re-ingests the share on a
   cycle) unless `--force`.
3. **Record pre-state** — top-level folder count per share, ticket counts by state,
   `count(*) where duplicate_of<>''`.
4. **Apply** — `.venv/Scripts/python.exe -m antfarm.queen_cli dedupe --apply`. It moves the
   timestamped occurrence bundles into the canonical folder, merges `info.md` (combining the
   `## Machines` table and updating `*First seen:*`) and removes the emptied duplicate folders.
   Variants: `--tickets-only` (no share writes), `--group HANDBALL-176`, `--undo BATCH_ID`.
5. **Restart** the colony detached, as in `antfarm-colony-ops` (from Git Bash use `cmd //c`;
   single-slash `cmd /c` runs nothing) — and verify the churn is closed: **total ticket count and
   `max(created_at)` must be unchanged**. A rise means the identity pin is not being written or read.
6. Expect `/api/duplicates` to report 0 groups.

Undo log is `.antfarm/crash-merge-undo.jsonl` — local on purpose, because the share may be down
when the undo is needed and a log on the share could sit inside a folder the merge removes.

## Automatic linking at ingest

Automatic ticket linking is on by default (`pipeline.link_duplicates: true` in `antfarm.yaml`):

- Ingest only absorbs tickets created or reopened by *that specific pass*.
- Incumbent tickets already on the board always keep their write-ups and canonical status.
- Tickets in `needs_clarification`, `needs_file`, or with open questions are never absorbed.
- The automatic pass **never** moves share folders — share consolidation stays an explicit
  `dedupe --apply`.

## Verifying counts

Folder-count arithmetic that does not add up is usually **a second project's share**
(`antfarm.yaml` configures Handball 27 *and* Cricket 8). Check the rmdir paths' parents in the
undo log before assuming folders appeared or vanished:

```python
top = [p for p in rmdirs if p.parent == share]   # the rest are another project
```

## Interpreter

`.venv/Scripts/python.exe`, never a bare `python`; why a bare one fails silently is in
`antfarm-colony-ops`.
