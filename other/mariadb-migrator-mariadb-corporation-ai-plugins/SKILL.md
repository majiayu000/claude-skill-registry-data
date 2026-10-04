---
name: mariadb-migrator
description: "Overview and entry point for migrating a MySQL database to MariaDB with the migrator.* tools of the mariadb-shell MCP server — what the tooling is, the two things you may never choose (unconfigured connections, passwords), the resume-safe trap that reports success while migrating nothing, the four tools, and the discover → mode → configure → run → verify workflow. Use when asked to migrate/move/port a MySQL database or schema to MariaDB, when asked to migrate from MySQL (target may be left unstated — assume MariaDB), to configure or run the MySQL-to-MariaDB migration tooling, or when a migration run failed and has to be diagnosed or resumed; then read the focused sub-skill for the step you are on."
---

# MySQL → MariaDB Migration — Overview

The **MySQL-to-MariaDB Migrator** is a standalone program (a Python orchestrator
driving a directory of POSIX shell scripts) that copies databases from a MySQL
source to a MariaDB target. The `migrator.*` tools of the **`mariadb-shell` MCP
server** configure and drive it: you write its `config/migration.yaml`, then run
one of its modes and read its report.

This skill is the map. Read the focused sub-skill for the step you are on.

**Two things are deliberately NOT yours to choose**, and both are enforced by
refusing the configuration rather than by failing later:

1. **Only servers that are already configured MCP connections may be named.**
2. **You can never set a password.** Each is read from the shell's secret store
   at the moment a migration runs.

Get the configuration right first — a wrong one is refused, and a *plausible but
incomplete* one produces a failed run deep in the dump step.

> **The one rule that silently produces a false success:** the orchestrator is
> **resume-safe**. If you point `out` at a directory that already holds a
> `state.json` from an earlier run, the new run reports every step `SKIPPED`,
> **exits 0, and migrates nothing**. Omit `out` for every new migration (a fresh
> `artifacts/<command>_<mode>_<timestamp>` is chosen for you) and pass it only to
> `migrator.resume`. And never trust `succeeded` alone — check that every step in
> the report says `DONE`.

## What LLMs Often Miss

**The whole migration is driven by MCP tool calls, never from the shell.** The
`migrator.*` tools perform the migration; the `db.*` tools — `db.list_connections`,
`db.connect`, `db.list_schemas`, `db.list_objects`, `db.get_object_details`,
`db.execute_sql` — are how you look at either server. **Do not use the Bash tool
to invoke `mariadb`, `mysql`, `mariadb-dump`, `mysqldump`, `mariadb-import`,
`mariadb-mtk` or `mariadb-shell` itself** — not to dump, not to load, not to run
a single `SELECT`, not to read a version, and not to "just quickly check"
something.

| If you reach for… | …call this instead |
| --- | --- |
| `mysqldump`/`mariadb-dump` piped into a client, to move the data | `migrator.run` — that pipeline *is* mode 1 |
| `mariadb -e 'SELECT ...'` for row counts or a spot-check | `db.execute_sql` on the target connection |
| `mariadb -e 'SHOW DATABASES'` / `SHOW TABLES` to see what is there | `db.list_schemas`, `db.list_objects` |
| `mariadb -e 'SHOW CREATE TABLE'` to check a definition or a foreign key | `db.get_object_details` |
| `mariadb --version`, or a client call to read `VERSION()` | `db.connect` + `db.execute_sql` on the configured connection |
| `mariadb-mtk` by hand for a faster load | mode 2 (`two_step`) with `SQLINESDATA_BIN` set — see `mariadb-migrator-modes` |
| `mariadb-shell` on the command line | the MCP tools it already exposes; the CLI is for the operator, not for you |
| `ls`/`cat`/`find` to locate the install or its config | the config path `migrator.set_config` returns, and the `install_dir` a run returns |
| `zcat`/`grep` over a dump to count objects | nothing — report that no independent source count was available (`mariadb-migrator-modes`) |

Three reasons the shell path cannot work, not merely shouldn't:

- **You do not have the passwords, and must not ask for them.** They stay in the
  shell's secret store and are resolved inside the server process at the moment a
  run starts, so a hand-built command line has no credential to offer.
- **Anything done outside the orchestrator is invisible to it.** `state.json`,
  `report.json` and the per-step statuses are what "the migration succeeded" is
  judged from, and a hand-run step appears in none of them.
- **Every shell command is separately approval-gated**, so guessing at a command
  line turns one tool call into a string of prompts.

**Two narrow exceptions, and they are the only shell commands these skills ever
ask for:** `command -v mariadb-mtk`, to learn whether that binary exists at all
(`mariadb-migrator-modes`), and checking a mode 3 dump against its SHA-256
manifest on disk. Both look at the *machine*, not at a database. Nothing else.

## The workflow

```text
0. discover connections, schemas, and what was asked  →  mariadb-migrator-discovery
        │
        ▼
1. choose the mode                                    →  mariadb-migrator-modes
        │
        ▼
2. write config/migration.yaml (set_config)           →  mariadb-migrator-configure
        │
        ▼
3. plan, then run — or resume a failed run            →  mariadb-migrator-run
        │
        ▼
4. verify on the target, then report the result       →  mariadb-migrator-verify

   anything refused, failed, or defect-shaped         →  mariadb-migrator-troubleshooting
```

## Preconditions

- **The tooling must be installed**, or the `migrator.*` tools are not registered
  at all — a server with no install advertises none of them rather than four
  tools whose every call would fail. Install with
  `mariadb-shell -- mcp setup --installMigrator`. **This takes effect on the next
  server start, not the current one**; if you cannot see `migrator.set_config`,
  that is why.
- **Not available on Windows.** The tooling is a POSIX shell program.
- **Both servers must be configured connections.** Start by calling
  `db.list_connections` and build the configuration out of what it returns. Do
  not invent a host: it will be refused.
- The `mariadb` client and `mariadb-dump` must be on the server's `PATH`, and
  **`pv` should be** (see `mariadb-migrator-troubleshooting`).
- **Never name a host `localhost`.** The MySQL/MariaDB C client reads it as "use
  the Unix socket" and ignores the port entirely, so a source on any other port
  is silently contacted on the wrong instance — or not at all. Use `127.0.0.1`.
  This compounds with the port rule in `mariadb-migrator-configure`:
  `localhost:3307` both looks configured and loses the port from the
  secret-store lookup.
- **The client option files must be clean.** A `verbose` or `vertical` line in
  `~/.my.cnf` or `/etc/my.cnf.d/*` corrupts the single-value captures the phase
  scripts rely on. The tooling probes for this with `--print-defaults` before
  running any query; fix the option file rather than looking for a bypass.

## The four tools

| Tool | Purpose |
| --- | --- |
| `migrator.set_config(mode, env, merge=False)` | Write `config/migration.yaml`. Returns the path, the keys, the example's path, and which connection each account resolved to. |
| `migrator.plan(mode, out=None, timeout=3600)` | Resolve the step list for a mode and validate the configuration. **Executes nothing** and needs no reachable server. |
| `migrator.run(mode, out=None, timeout=3600)` | Perform the migration. **Changes the target**, and in some modes the source. |
| `migrator.resume(mode, out, timeout=3600)` | Continue a failed run from the `state.json` in that run's `out` directory. `out` is required here. |

`out` is always **relative to the install directory** (an absolute path is
refused). Every invocation gets a closed stdin, so an incomplete configuration
fails saying what is missing instead of hanging on a prompt.

## The modes at a glance

This is the short version to show an operator who has to choose. The full table,
the per-mode gates and the mode-specific traps are in
`mariadb-migrator-modes` — read it before configuring.

| # | Mode id | Called | Type | The tradeoff in one line |
| --- | --- | --- | --- | --- |
| 1 | `one_step` | Serial Streaming Copy | offline | Simplest and most predictable — **the default recommendation**. |
| 2 | `two_step` | Parallel Restartable Streaming Copy | offline | Faster on large databases, but needs `mariadb-mtk`, which is not bundled. |
| 3 | `staged` | Offline Copy | offline | Dumps to disk with checksums first, loads separately; needs bash 4. |
| 4 | `binlog` | Replication | online | Low-downtime cutover; needs a MySQL 8.0+ source and **no `JSON` columns**. |

`inplace` and `replace_slave` also exist. **Do not pick them** — see
`mariadb-migrator-modes`.

## Guidelines

- **Build the configuration from `db.list_connections`, never from what the user
  typed.** A host they name that is not configured cannot be migrated to or
  from, and saying so early is more useful than a refused `set_config`.
- **`plan` before every `run`**, including after a `merge=True` edit.
- **Use `merge=True` for a correction**, not a fresh full write — you keep the
  keys you got right, and the merged result is validated as a whole anyway.
- **Report what the report says.** If a step failed, name the step and quote from
  its `output_tail`; the tooling's own diagnosis is almost always the answer.
- Modes 1, 2 and 3 are **offline**: the source is read, not changed, but the
  target is written. Mode 4 leaves replication running. Never run any of them
  against a production target without the user's explicit go-ahead.

## See Also

- `mariadb-migrator-discovery` — starting from a bare request: what to probe, show and ask.
- `mariadb-migrator-modes` — the mode reference and each mode's own gates.
- `mariadb-migrator-configure` — writing `config/migration.yaml` with `migrator.set_config`.
- `mariadb-migrator-run` — `plan`, `run`, `resume`, and checking a run three ways.
- `mariadb-migrator-verify` — verifying on the target and reporting the result.
- `mariadb-migrator-troubleshooting` — known defects and the failure playbook.
- `mariadb-schema-management` — versioned schema lifecycle, for a schema that
  will keep evolving after it has been migrated.
- `mariadb-schema-create-script` — authoring a single MariaDB create script.
- `mysql-to-mariadb` — MySQL/MariaDB dialect and feature differences, for fixing
  up SQL that the migration carried across verbatim.
