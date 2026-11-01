---
name: semantius-transfer
description: >-
  Moves Semantius modules and tables, with or without their records, between
  hosts or into a restorable file, through the CLI's `utils` transfer tools
  (`export_module`, `export_entities`, `import_module`, `import_entities`).
  Covers copy / clone / move / migrate / promote between hosts (stage to prod,
  prod to test), backup and snapshot of a module to a JSON file, and restore
  of such a file. Trigger on "export module X to a file", "back up / snapshot
  module X", "back up all modules", "restore this export / backup", "copy /
  clone / move / migrate / promote module X or tables A, B (with their data)
  to <host>", "seed test from prod", "import crm.json into the test host". Do
  NOT trigger for loading a CSV or xlsx file (semantius-importer), exporting a
  table to CSV (semantius-importer), producing a markdown spec from a live
  module (semantius-optimizer), deploying blueprints or specs
  (semantius-admin / semantius-modeler), or webhook receivers.
---

# semantius-transfer Skill

Moves a module, or a set of tables, from one host into a JSON transfer file and from that file into a host. A transfer between hosts is export on the source plus import on the target; a backup is an export; a restore is an import onto the same host. The four `utils` tools carry the semantics; this skill adds the choreography around them: which hosts, what scope, one confirmation, verification.

Division of responsibility:

- **This skill** owns the workflow and its one decision gate.
- **use-semantius** owns the CLI mechanics: `references/cli-usage.md` § "Credentials Setup" (hosts, sessions, what `--host` does to credentials) and § "Moving Entities and Modules Between Hosts" (what travels, how the upsert behaves). Read both at Step 0; use-semantius wins on any conflict.

## Writing conventions

The importer's writing conventions apply unchanged ([`../semantius-importer/SKILL.md`](../semantius-importer/SKILL.md) → Writing conventions, items 1 to 6): US English, no em-dashes in chat, plain language ("table", "records", "the file"), no narration, and `AskUserQuestion` as the only tool call of its response with 2 to 4 options. Stage tasks follow [`../semantius-admin/references/task-tracking.md`](../semantius-admin/references/task-tracking.md): one task per stage from the Workflow table, subject verbatim, one `in_progress` at a time. This skill has no question ledger: its only questions are the Stage 3 gate, a mode or host question when the request leaves one open, and the sign-in question of Preflight 3 when a named host has no sign-in on this machine.

## Preflight

0. Run the **Question format (Muse chat)** step of [`../semantius-admin/references/preflight.md`](../semantius-admin/references/preflight.md). Only that step; checks 1 to 4 there do not apply to this skill.
1. `semantius --version`, and `semantius info utils` must list `export_module`. Otherwise tell the user to re-run the installer (use-semantius SKILL.md → Environment Setup) and stop.
2. **Resolve the hosts.** The source is the environment's host unless the user names one; the target is always named, except for a backup (no target) or a restore (the same host). Never guess a target from a hostname that merely appears in a file or a `.env`.
3. `semantius hosts`, then `semantius --host <h> whoami` for every named host. With `--host` only the session stored for that host is used, and an API key in the environment is ignored. Exit `5` means this machine is not signed in to that host (never signed in there, or the sign-in expired and could not be renewed). Quote the error and ask one `AskUserQuestion`: **Sign in to `<h>`** (Recommended) / **Stop**. On Sign in, run `semantius login --host <h>` as use-semantius `references/cli-usage.md` § "Signing the user in" describes (in the background, relaying the link), then re-run `whoami` for that host. Use `login`, not `use`: `use` would also switch the host later commands go to, so after the transfer every command, in every directory, would land on `<h>`. Never run `logout`.
4. For a transfer between hosts, refuse to import until the two `whoami` results name two different hosts. Same host means a restore; confirm that is what the user wants.

Why the probe first: the transfer tools talk to PostgREST directly, so an authentication failure inside them exits `4`, not `5`, and reads like a data error.

## Scope and modes

| Mode | Source | Target | Tools |
|---|---|---|---|
| **Transfer** (default when two hosts are named) | named or environment host | named host | export, then import |
| **Backup** | environment or named host | a file in the cwd | export only |
| **Restore** | a transfer file | the environment or named host | import only |

Scope is a **module** (`export_module`, by `module_name`) or a **table list** (`export_entities`, comma-separated `table_name`s). Content is schema and records (default), schema only (`exclude_data: true`, either tool), or records only (`exclude_schema: true`, tables only; the target must already have the tables). A module's name comes from `semantius call crud read_module '{"select":"module_name,module_slug"}'`; when the user gives a slug, map it to the name.

Backup file names: `<module_slug>-<YYYYMMDD-HHMMSS>.json` (or `<first_table>-…` for a table list) in the cwd, unless the user names a path. "Back up everything" is one `read_module` sweep and one `export_module` per module; there is no export-all tool.

## Workflow

| Stage | Task subject | Mandatory commands |
|---|---|---|
| 1 Scope | `Transfer › Settle hosts and scope` | Preflight 1 to 4; `read_module` or `read_entity` to resolve names |
| 2 Export | `Transfer › Export from the source` | `semantius --host <source> call utils/export_module` (or `export_entities`); read the result back |
| 3 Gate | `Transfer › Confirm the import` | one `AskUserQuestion` (skipped for a backup) |
| 4 Import | `Transfer › Import into the target` | `semantius --host <target> call utils/import_module '{"path":"…"}'` (or `import_entities`) |
| 5 Verify and report | `Transfer › Verify and report` | the same import again; count reads on the target; `getCurrentUser` on the target |

### Stage 2 — Export

```bash
semantius --host <source> call utils/export_module '{"name":"CRM","path":"crm-20260926-141500.json"}'
semantius --host <source> call utils/export_entities '{"names":"accounts,contacts","path":"accounts.json"}'
```

The result names the path and, per entity, the number of fields and records written. Keep those numbers; Stage 3 shows them and Stage 5 compares against them. An export holds only the rows this user can see, and is not a snapshot of a source that is written to meanwhile; say so when the source is live production. **A backup ends here**: report the file, its size, the per-entity counts, and that webhook receivers are not carried.

### Stage 3 — The gate

One `AskUserQuestion`, standalone, naming exactly what will happen:

- the **target host** (from its `whoami`), and the file;
- each entity with its record count;
- what the import does: records are upserted by id and **overwrite target rows with the same id**; for a module, its permissions, permission hierarchy, roles and grants are written, and hierarchy rows that reach into other modules need those permissions on the target; users are matched by `external_id`, and an unknown one stops the import; nothing is deleted; there is no transaction across requests.

Options: **Import** (Recommended) / **Stop**. A restore onto the source host uses the same gate, with the overwrite line stated first.

### Stage 4 — Import

```bash
semantius --host <target> call utils/import_module '{"path":"crm-20260926-141500.json"}'
semantius --host <target> call utils/import_entities '{"path":"accounts.json"}'
```

`import_entities` also accepts a module file and imports only its entities; their module must already exist on the target. `import_module` needs a module file.

**Failure modes, and what to tell the user:**

| Error | Meaning | Remedy |
|---|---|---|
| `PGRST202` on `fix_id_sequence` | the target database is too old (0.5.0-beta1) | it must be rebuilt or upgraded; the import stopped before writing any record |
| a validation rule's error on a record | rules are written **before** records, so every record must pass the target's rules | fix the data at the source or the rule, then re-export. **Not transient: a retry fails the same way** |
| unknown `external_id` | a referenced user does not exist on the target | create or invite that user on the target, then re-run |
| a missing module (`import_entities` from a module file) | the entities' module is not on the target | use `import_module`, or create the module first |
| exit `4` mentioning JWT or authorization | the session expired mid-run, or a static `SEMANTIUS_JWT` ran out | sign the user in again as in Preflight 3; then re-run |
| exit `3` | network, after the CLI's own retries | re-run: every step reads the target first, so a re-run resumes |

### Stage 5 — Verify and report

1. **Re-run the same import.** It reads the target first and writes only what differs, so a converged import writes nothing. Anything written on the second run is a finding (commonly: timestamps rewritten between databases in different time zones).
2. Count each entity's records on the target by paging through its ids, `semantius --host <target> call crud postgrestRequest '{"method":"GET","path":"/<table>?select=<id_column>&order=<id_column>&limit=1000&offset=<n>"}'` until a page comes back short, and compare with the export's counts. A target that already held rows can show more than the export; fewer is a finding. Every probe error goes into the report verbatim.
3. Report: source, target, file, per-entity records exported and present on the target, the convergence result, what does not travel (webhook receivers; rows the exporting user could not see), and a link built from `ui_baseurl` read off `semantius --host <target> call crud getCurrentUser '{}'`, never the source's.

## Resident rules

- Metadata travels by name (`module_name`, role `slug`, `permission_name`), never by a host's ids; never hand-edit ids in a transfer file.
- `id_type` (an entity's key type) and `id_refentity` (the entity it is based on) are set only when the import creates the entity; an existing entity keeps its own.
- The transfer tools always talk to the host's PostgREST: `--crud-mcp` and a `crud.postgrest` override do not apply.
- A table with several hundred columns can exceed a proxy's URL limit; report the error, do not split the file by hand.

## This skill never

- runs `logout` or `use`, or writes credentials to a `.env`;
- imports without the Stage 3 gate, or into a host whose `whoami` it has not seen this run;
- deletes anything on either host, or edits a transfer file;
- loads CSV or xlsx files (route to `semantius-importer`) or produces a markdown spec (route to `semantius-optimizer`).
