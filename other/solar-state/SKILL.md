---
name: solar-state
description: >
  What is in the runtime state: tasks, the router audit, cross-channel
  continuity and the events of A3 mandates, in one SQLite base that only this
  skill opens. `solar-paths` says where; this says what. Use when a component
  needs to read or change shared runtime state — never by opening the files or
  the base directly.
---

# Solar State

`solar-paths` answers **where** runtime state lives. This skill answers **what
is there**, and is the only thing that reads or writes the state more than one
component uses.

**Status: the shared runtime is one sqlite base.** Tasks, the router audit,
cross-channel continuity and A3 mandate events are read and written only
through this skill. A runtime whose format is not `sqlite` is refused.
`solar client update` and `solar client sync` call `migrate`; `rollback` is
the way back. The base belongs to one workspace (`workspace-owner.json`).
`session` reads that workspace's id from `$SOLAR_WORKSPACE/.solar/settings.json`.

## Required MCP

None

## What lives here

| In the base | What it is |
|---|---|
| `tasks` | One row per async task: status, the frontmatter as an ordered list, the body |
| `transitions` | Every allowed status move. A move not in the table fails |
| `task_links`, `task_events` | Parent–child relations; every status change, with who made it |
| `audit` | The router audit, one JSON line per row, verbatim |
| `continuity` | The cross-channel intention, one JSON document |
| `delegation_events`, `delegation_streams` | The `events` and `shadow` streams of each A3 mandate; a stream exists even when empty |
| `subtask_plans` | The children a parent declared, JSON verbatim |
| `cancellation_requests` | Pending cancellation requests |

Not here, on purpose: the mandates themselves (YAML that Louis writes in
`sun/delegations/`), execution logs (files; a task keeps the path), and state
only one component reads (router conversations, `gateway/`, `host/`, `mcp/`).

## How to use it

Python:

```python
_STATE_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "solar-state" / "scripts"
if str(_STATE_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_STATE_SCRIPTS))

import solar_state  # noqa: E402

with solar_state.session() as state:
    task_id = state.task_create([("title", '"Review the plan"'), ("priority", "normal")],
                                body="# Review the plan\n", status="queued")
    if state.task_claim(task_id, worker="worker-1"):
        ...

with solar_state.read_session() as state:
    state.task_get(task_id)   # shared lock, no daily backup, creates nothing
```

`read_session()` opens the existing `state.lock` shared and holds it for the
whole read. It does not create the lock, the database, or the daily backup.
It refuses when the lock, the owner, the format, or the schema is missing.
Writers keep using `session()`.

Bringing existing state in, verbatim (for the cutover):

```python
state.task_import(document_text, status="queued")   # the pairs, untouched
state.audit_import_line(line)                        # the JSON line as written
state.delegation_event_import_line(mandate, "events", line)
state.continuity_import_text(text)
```

and back out: `task_export`, `audit_lines`, `delegation_event_lines`,
`continuity_text`.

Bash, through the CLI (JSON out; exit 2 on a refusal, 3 on a lost claim):

```bash
python3 "$SCRIPT_DIR/../../solar-state/scripts/solar_state.py" task claim "$TASK_ID" --worker "$$"
python3 "$SCRIPT_DIR/../../solar-state/scripts/solar_state.py" task show "$TASK_ID"
python3 "$SCRIPT_DIR/../../solar-state/scripts/solar_state.py" status   # says why it would refuse
```

## The rules that keep it the owner

1. **Only this skill opens `state.sqlite`.** Nobody else writes SQL against it.
2. **It imports nothing but `solar-paths`.**
3. **Every operation holds the shared lock from start to finish**; a cutover
   holds it exclusive. Nobody checks before and writes after.
4. **This code only speaks `STATE_FORMAT=sqlite`.** Any other value, a missing
   base or an older schema refuses with `StateUnavailable`. It never falls
   back to reading the old files.
5. **Schema migrations run only inside a cutover**, with a copy of the base
   first. A session never upgrades under other readers. **A released migration
   never changes**: v1 is pinned by a test; changes go in a new version.
6. **What comes in verbatim goes out verbatim.** A task's frontmatter is
   stored as `[key, text after the colon]` in order, and the columns are a
   projection of it, rewritten in the same transaction. Audit lines, mandate
   events and the continuity document are stored as the text they were.
7. **One id per task, and it must be a file name.** A frontmatter `id` that
   differs from the one given, a key that appears twice, or an id with a path
   separator, a control character or a climbing `..` is refused. The cutover
   checks every destination again on the way out: ids and file names are data.

## Cutover

`scripts/solar_state_cutover.py` moves a runtime from files to the base and
back. Both directions hold the exclusive lock throughout, wait for anything
still running (an active task, a live executor — a reused pid does not count —
or old router / async-tasks code), copy the sources aside, import or export,
verify, and only then change the format and move the old files aside.

```bash
python3 scripts/solar_state_cutover.py rehearse          # import into a throwaway base, verify; touches nothing
SOLAR_STATE_ALLOW_CUTOVER=1 python3 scripts/solar_state_cutover.py migrate
SOLAR_STATE_ALLOW_CUTOVER=1 python3 scripts/solar_state_cutover.py rollback
```

- **Migrate.** Tasks take the status of the folder they sit in. Logs are copied
  to `task-logs/`. Task folders, handles, subtask plans, cancellations and logs
  move to `async-tasks.migrated-<stamp>/`; `tmp/`, `hooks/` and anything unknown
  stay. The audit, continuity and mandate streams are renamed
  `*.migrated-<stamp>`. The originals are also copied to `pre-state-<stamp>/`.
  Killed at any step, running it again completes it. A run that finds
  `STATE_FORMAT=sqlite` checks the marker, the base and its schema first, waits
  for running code, and brings in what old code wrote to the files meanwhile
  (new tasks with their children, a child that arrives later for a parent that
  already named it, logs, a clean tail of audit or mandate lines)
  before moving them. Anything else — a task, log or subtask plan that changed,
  a shortened or rewritten audit or mandate stream, a different continuity, or a
  source that is neither still in place nor already under `*.migrated-<stamp>` —
  is refused, and nothing is moved aside.
- **Rollback.** Writes every task back under its original file name, restores
  logs, subtask plans, cancellations, audit (an empty file comes back empty),
  continuity and mandate streams (an empty stream comes back empty). Everything is written to a staging folder
  and verified there; only then the files move into place, listed with their
  hashes in `state-rollback.json`. Killed halfway, the next run removes what it
  had placed — only files still byte for byte what it wrote — and starts over;
  killed after the format changed, the next run finishes. A copy of the base
  goes to `pre-rollback-<stamp>/`. It refuses to overwrite a file that exists.
- **Stopping and starting** what Solar runs is the caller's job: this skill
  imports only `solar-paths`.

## Backups

- Before each schema migration: `state-backups/pre-migration/`, never rotated.
- Daily: `state-backups/daily/`, 7 kept. Taken when a session opens and the
  newest copy is older than 24 h, so it does not depend on the orchestrator.
- `inspect_backup(path)` opens a copy read-only and reports schema, integrity
  and counts.
