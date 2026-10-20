---
name: build-git-datastore
description: >-
  Load this skill when an app needs persistence but not a database yet (a prototype, MVP, or
  internal tool), even if git is never mentioned: its gate often says no. Trigger on "no-DB", "just
  use files", "git as a database", "how do we defer the database decision".
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the git CLI (2.x) on PATH and Python 3.9+ to run the bundled `scripts/gitstore.py` and
  `scripts/sync.py`, which use the standard library only - no pip install, no database, no
  database driver. Deployment also needs a persistent local disk; `sync.py` needs network access
  and push permission on the backup remote.
license: Apache-2.0
---

# Git-backed datastore

A bare git repo as the data layer for an app that does not have a database yet.
One repo per deployed instance; one **orphan branch per project**; JSON records
in trees under that branch.

The task is done when the gate verdict is stated. If the gate passes, it is also done when the
store sits behind the store interface, backup is wired, and the migration trigger is in the README.

The design is sound but narrow. Most of the value of this skill is in applying
the gate honestly first, and in never touching a working tree second.

## Procedure

### Start with the gate

Run this before writing code. Answer honestly — talking someone out of this is
a good outcome, and much cheaper than a migration in three months.

| Question                     | Fits                                                 | Does not fit                                                        |
| ---------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------- |
| Sustained writes per project | under ~10/sec                                        | steady double digits or bursts of concurrent writers on one project |
| Records per project          | up to ~50k                                           | hundreds of thousands                                               |
| Record size                  | JSON documents, KBs                                  | images, video, large binaries                                       |
| App servers                  | one node, persistent disk                            | several nodes, autoscaling, or serverless                           |
| Queries                      | fetch by id, list a collection, filter in app memory | ad-hoc filters, joins, aggregates, full-text search                 |
| Cross-project reads          | rare or none                                         | dashboards spanning all tenants                                     |
| Deletion                     | soft delete is fine                                  | hard "erase every trace" requirement                                |

Two of these are disqualifying rather than merely awkward:

**Serverless or multi-node hosting.** The store is a directory on a disk. Two
app nodes with two disks are two different databases. Lambda/Vercel-style
runtimes have no durable disk at all, so every write would have to push to a
remote — putting network latency and API rate limits in the request path. If
the deployment target is serverless, stop here and use SQLite on a volume, a
hosted Postgres, or a managed document store.

**Right to erasure.** Git history is append-only by construction. "Delete this
user's data" means rewriting every commit that touched it and force-updating the
ref, which invalidates every clone and backup. If the app handles personal data
under GDPR/CCPA-style erasure obligations, either keep personal data out of the
git store entirely (store an opaque id and keep the PII in something you can
actually DELETE from) or do not use this pattern.

If the gate passes, say so and build. If it fails, see Stop conditions.

### What you get that plain JSON files do not

Worth stating explicitly, because "just write JSON files to disk" is the obvious
alternative and this has to beat it:

- **Atomic multi-record writes.** Several records change in one commit, or none
  do. A crash mid-write leaves nothing half-applied.
- **Lock-free concurrency that is actually correct.** `git update-ref` is an
  atomic compare-and-swap, so it holds across processes and worker pools.
- **Snapshot reads.** A commit sha is an immutable point-in-time view of the
  whole project. This is what makes the eventual migration tractable.
- **History, audit, and undo for free.** Who changed what, when, and the ability
  to read any record as it was at any past moment.
- **Backup is `git push`.** Restore is `git clone`. Both are boring and proven.

### Architecture

```
data.git/                         bare repo -- ONE per deployed instance
  refs/heads/main                 instance-level config (optional)
  refs/heads/project/<pid>        ORPHAN branch, one per project
      meta.json                   { id, name, created_at, schema_version }
      collections/
        tasks/<record-id>.json
        comments/<record-id>.json
```

**Why orphan branches rather than a directory per project on one branch.**
Not isolation aesthetics — write contention. Every write is a compare-and-swap
on a ref. With one branch, every write in the entire app serialises on that one
ref, and under any concurrency you get a retry storm. With a ref per project,
writes to project A never contend with writes to project B, and throughput
scales with the number of active projects instead of being capped globally.

Three secondary payoffs: deleting a project is deleting a ref; exporting one
project as a standalone repo is trivial; and at migration time you can cut over
project by project instead of all at once.

Orphan branches cost nothing in storage. Git objects are content-addressed and
shared across the whole object database regardless of commit ancestry — "orphan"
severs history, not deduplication.

### Measured behaviour

From `scripts/gitstore.py` on an ordinary container, ~300-byte records:

| Operation                                    | Result                                 |
| -------------------------------------------- | -------------------------------------- |
| Single write (own commit)                    | ~17 ms → ~58 writes/sec on one project |
| Batched write in a transaction               | ~3.4 ms/record                         |
| Point read by id                             | ~1.8 ms (mostly process spawn)         |
| List 700 records                             | ~220 ms via one `cat-file --batch`     |
| List 64 projects                             | ~9 ms via one `cat-file --batch`       |
| 8 processes hammering one project            | 80 writes in ~4 s, zero lost           |
| Repo after 700 writes, before/after `git gc` | 7.5 MB → 0.4 MB                        |

Two things to take from this. Writes are milliseconds, not microseconds — fine
for a CRUD app, wrong for anything write-heavy. And `git gc` matters enormously;
without it you accumulate loose objects until the store is 20x its real size.

If point reads at ~1.8 ms are too slow, keep a long-lived `git cat-file --batch`
process and stream requests to it. That removes the spawn cost and takes reads
into the tens of microseconds. Do this only when measurement says to.

### Build order

1. **Apply the gate.** Report the verdict before writing anything.
2. **Copy `scripts/gitstore.py` into the project** and initialise the repo:
   `python gitstore.py init ./data.git`. No third-party packages are needed; it
   shells out to the `git` binary, so `git` on `PATH` is the one dependency.
3. **Put every data access behind the store interface.** No git command appears
   in a route handler, a template, or a background job — only calls to the store.
   This is what makes the later migration a swap rather than a rewrite; see
   `references/porting.md` for the contract and how to port it to another
   language.
4. **Define collections and record shapes** in `schema/<collection>.json`, and
   stamp `schema_version` on every record. Read `references/data-model.md` for
   record layout, id choice, sharding large collections, and derived indexes.
5. **Wire up backup with `scripts/sync.py`** before launch, not after. It pushes
   to a remote on a background worker, coalescing bursts and backing off on
   failure, so nothing network-shaped ends up in the request path. Then `git gc`
   scheduling, nightly bundles, and a rehearsed restore. See
   `references/operations.md`.
6. **Write the migration trigger down now**, while the reasoning is fresh: the
   record count, write rate, or feature that will mean it is time to move. Put it
   in the README. The `ceh-git-datastore:migrate-git-datastore` skill handles the move itself.

### Files

- `scripts/gitstore.py` — working store implementation and CLI. No third-party
  packages; requires the `git` binary. Tested for concurrency, atomicity, and
  lost updates.
- `scripts/sync.py` — background push to a remote, bundle rotation, restore, and
  a status dict for health checks. Includes a mass-deletion guard.
- `references/plumbing.md` — the exact git command sequences and why each is
  shaped that way. Read when implementing or debugging the storage layer.
- `references/data-model.md` — records, ids, collections, schema versioning,
  sharding, derived indexes. Read when designing the data.
- `references/operations.md` — gc, backup, restore, deployment topology,
  monitoring. Read before shipping to production.
- `references/porting.md` — the store contract, a TypeScript sketch, and the
  rules that keep migration cheap. Read when the app is not Python.

## Rules

### The rules that make it work

**1. Bare repo. No working tree. Ever.**
If any code path runs `git checkout`, `git add`, or `git commit`, the design is
broken: those need a working tree, and a working tree is a single shared mutable
resource that serialises every request in the app and corrupts under concurrency.
Reads go through `git cat-file`. Writes go through a **temporary index file** per
write, then `write-tree`, `commit-tree`, `update-ref`.

**2. Compare-and-swap on the ref is the concurrency control.**
`git update-ref <ref> <new> <old>` succeeds only if the ref still points at
`<old>`. On failure, retry with backoff. Pass an empty `<old>` to mean "only if
this ref does not exist" — that is a safe create.

**3. Reads inside a write must come from the commit you will CAS against.**
This is the subtle one, and the one that produces silent data loss when missed.
If you read the live ref, compute a new value, then CAS against a base resolved
_afterwards_, another writer can land in between; your CAS succeeds and their
write is gone. Pin the base commit first, read from that sha, and CAS against it.
`scripts/gitstore.py` does this in `atomic()` — use it for anything that reads
before writing (counters, list appends, state transitions).

**4. One git process per operation, not per record.**
Process spawn dominates everything here. Reading 700 records via one
`cat-file --batch` takes ~220ms; as 700 subprocesses it takes minutes. Same for
writes: stage a whole transaction with a single `update-index --index-info`.
This one habit is the difference between "surprisingly fine" and "this is slow".

**5. Sortable ids.**
ULIDs (26 chars, time-prefixed). `git ls-tree` returns paths in byte order, so
sortable ids give you "most recent N" without an index, and they survive the
move to SQL unchanged — unlike an auto-increment integer, which you would have
to invent during migration.

### Anti-patterns

- **Breaking rules 1, 3, or 4 above.** Checking out a branch to serve a request
  (the most common way to wreck this), `git add`/`git commit` against a shared
  index, CASing against a base resolved after the read, or a subprocess per
  record. The first two corrupt under concurrency, the third loses writes
  silently, the fourth is merely slow.
- **Storing binaries in the repo.** Every version of every blob is kept forever.
  Put files in object storage; store the key.
- **Using commit history as application data.** Reading `git log` to answer
  product questions ("who edited this") welds you to git and does not survive
  migration. Keep an `events` collection instead.
- **A `projects.json` index maintained alongside the refs.** Two sources of truth
  that drift. Refs _are_ the index — enumerate them with `for-each-ref` and batch
  the `meta.json` reads.
- **Never running `git gc`.** The store quietly bloats 20x.
- **Backing up with `git push --mirror`.** It also pushes `refs/remotes/*`, so
  deleted projects get resurrected on the remote and can never be garbage
  collected locally. Push `refs/heads/*:refs/heads/*` with `--prune` instead.
- **Pushing inside the write handler.** Couples write latency to the network.
- **Skipping the gate because the prototype is small.** The gate is about where
  the app is going, not where it is.

### This is not your code repository

`data.git` is a bare repo holding application data. It is not the repo your
source lives in, and it must not be handled by the tooling you use for source
control. Two separate things that happen to use the same technology:

|          | Source repo                            | `data.git`                         |
| -------- | -------------------------------------- | ---------------------------------- |
| Contents | code you wrote                         | JSON records                       |
| Commits  | human-authored, reviewed               | machine-generated, tens per second |
| Messages | conventional commits, feed a changelog | `put tasks/01J8ZQ...`, unread      |
| Commands | porcelain: `add`, `commit`, `branch`   | plumbing only                      |

Concretely: never route data operations through commit/branch/PR tooling, which
uses the `git add` that rule 1 forbids; exclude `data.git` from repo-scanning and
changelog tooling, which will otherwise try to make sense of 40,000
machine-written commits; and keep it outside the source tree — `/srv/data.git`,
not `./data.git` inside the checkout. If it must live alongside, `.gitignore` it.

## Stop conditions

- The gate fails on one row → say which row and what you would use instead. Do not build it anyway
  with a warning comment.

## Hands off to

- `ceh-git-datastore:migrate-git-datastore` when the migration trigger from Build order step 6
  fires. That skill handles the move itself.
