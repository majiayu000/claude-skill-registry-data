---
name: db-migration
description: Plans and makes database migrations through the project's migration tool (shipped for Prisma). Use when asked to "plan a migration", "add a field to the Prisma schema", "rename this column", or "check this migration", when changing a database schema, migrating a model, field, enum, or relation, or creating, fixing, or auditing a migration. Not for general questions about ORMs or comparing tools.
allowed-tools: Read, Glob, Grep
---

# Database migration

Take a schema change from the schema file to a migrated development database and regenerated client, through the project's own migration tool. The rules here hold for every tool; every command, file name, and error signature comes from the tool's adapter.

## Project settings

On every invocation, read `.claude/shipyard/db-migration.md` in the project root if it exists; its settings win over the adapter and over what's discovered below. It can name the `tool`, set the `schema path`, `migrations path`, and `working directory`, replace any adapter command with the project's own (a package script, for example), and say how environment variables are loaded, where application types live, whether to lint migrations, and which database hosts besides local ones count as development (`allowed hosts`) or must never be written (`never-write hosts`). Its shape is in [references/overlay-example.md](references/overlay-example.md).

If that file is missing and `.claude/shipyard/prisma-workflow.md` exists, read the old file as the settings file, with `tool: prisma`. Its hosts, commands, and paths apply as written; `references/overlay-example.md` lists what its older key names mean. Tell the user once, in the reply that reports how the run ended, even when it stops early: `Read settings from .claude/shipyard/prisma-workflow.md, the old name. Rename it to .claude/shipyard/db-migration.md; the old name may stop being read in a later release.` If both files exist, read `db-migration.md` as the settings file and also treat every host the old file lists under `never-write hosts` as never-write. Then tell the user once, in that same reply: `Read never-write hosts from the old .claude/shipyard/prisma-workflow.md as well as .claude/shipyard/db-migration.md. Merge the old file into the new one, then delete the old file.`

## Adapter

An adapter is one file per tool under `references/tools/`, in the format of [references/tools/format.md](references/tools/format.md); the steps below name its fields in backticks. Pick it on every invocation, after reading the settings:

1. The settings file's `tool` wins: load `references/tools/<tool>.md`.
2. Otherwise read the `enabled:` line and the `- load-when:` line of every adapter file in `references/tools/` (all but `format.md`), skip any that doesn't say `enabled: yes`, and load the one whose `load-when` matches the project.
3. If none matches, or more than one does, ask the user which tool the project uses.

Say which adapter you loaded and why: the settings file's `tool`, or the `load-when` entry that matched. If the tool has no adapter file, say that this skill has no adapter for it and has checked nothing, then hand the request back to the normal session. If its adapter doesn't say `enabled: yes`, it's a draft no eval has checked: say so, show the adapter's `Why it isn't enabled` section, and `STOP — WAIT` until the user says to use it for this run with those gaps.

The skill pre-approves no commands, so each one asks for permission unless the project has pasted the adapter's `allowlist` into its agent settings. If the user has to approve commands one by one, point them to it once; the adapter's `other agents` covers agents without such settings.

## Output

- The applied migration: its name and the SQL, shown to the user (from the adapter's `SQL preview` when its migrations are code).
- A regenerated client, when the adapter has a `regenerate client` command.
- Application types, DTOs, and validation schemas updated to match the changed models.
- The final `status` output, verbatim, or the `apply` output when the adapter's `status` is `none`.

## Rules

- **Never create or hand-write a file in the migrations folder when the adapter says `generates: yes`.** The generator always uses the database names from the schema's mapping (the adapter's `physical names`); hand-written SQL can use the schema's own name instead. For example (illustrative), an enum named `OrderStatus` in the schema and mapped to `order_status`, written by hand as `CREATE TYPE "OrderStatus"`, passes tests that mock the database, then fails against a real one, because the client looks for `order_status`. Editing a generated migration is allowed only for the changes in [references/risky-changes.md](references/risky-changes.md), such as turning a drop-and-add into a rename. When the adapter says `generates: no`, migrations are written by hand, so audit each one against the schema, as under Hand-written migrations, before it's applied.
- **Development database only.** A development database is one whose data can be lost without harming anyone. The skill can't see that, so step 1 takes each database's host as the evidence, and a host it doesn't accept ends the run before anything is created and before any of the adapter's `connecting commands` runs. Never edit the settings file to get past that check. Staging and production deploys belong to the project's release process.
- **Never reset, and never bypass migration history.** Never run a command under the adapter's `never run`: a reset deletes the data, and applying the schema without a migration leaves the database out of step with its history. If the tool refuses and says a consent setting is needed (the adapter's `consent setting`), stop; only the user sets it, so never set it or suggest a command that does. If a reset seems needed, stop and explain why.
- **Always name the migration**, with the adapter's `name flag`. Without a terminal, a tool can't prompt for a name and may create the migration unnamed. Names are descriptive snake_case: `add_status_to_order`.
- **Stop on a refusal.** When the tool refuses to go on without a terminal (the adapter's `refusals`: drift, a reset proposal, a data-loss warning, a question it can't ask), stop and report its full output to the user instead of retrying with other flags.
- **Use the project's installed tool**, through the adapter's `invoke` and from its `working directory` (the settings file's, if set), never a download of the latest release: that can be a different major version with different commands.
- **Stop on an unknown command.** If the tool reports a command as unknown (the adapter's `unknown command`), stop and tell the user; never swap in a similarly named command or follow the tool's suggestion of another one. A newer release can reuse a command name for something that isn't a migration, such as running or deploying an app.

## Steps

```
- [ ] 1 Check the CLI, find the files, check the host
- [ ] 2 Edit the schema
- [ ] 3 Create the migration without applying it
- [ ] 4 Review the SQL (gate for risky changes)
- [ ] 5 Apply, regenerate, update types
- [ ] 6 Confirm nothing is pending
```

1. **Check the CLI, find the files, check the host.**
   - Confirm the tool is a project dependency (the adapter's `dependency`) and installed (`installed CLI`). If it isn't a dependency, stop. If it's declared but not installed, ask the user to install the project's dependencies (in a plan-only run, say so in the plan instead): running the tool without an installed copy can download whatever release is published as latest.
   - Run the adapter's `CLI check` with the project's environment loaded (through its wrapper command, if the settings file names one), and read all of stdout and stderr together. Continue only on what the adapter calls a pass. On a fail, or if the tool reports the command as unknown, stop with the CLI-check message below. A configuration or environment error (the adapter's `environment error`) isn't a release problem: load the environment the way the project does and run it again.
   - Find the schema and migrations folder: the settings file's `schema path` and `migrations path`, else the adapter's `discovery`. The schema can be one file or several (`schema shape`). Paths in the settings file are relative to the project root; fill a command's `<schema path>` and `<migrations path>` relative to the directory the command runs from.
   - Check the host of every database the tool will connect to: each of the adapter's `URLs` that the project sets, such as a main URL, a direct URL that migrations use instead of a pooled one, and a shadow database URL. If the adapter's `URLs` is `none`, stop: the host check can't run. For each URL, find the environment variable it reads, load it the way the project does (the settings file's `environment`, else the adapter's), and print only the host. Never open or print the connection string or the file that holds it, since it includes the password; use a script that prints the host or a fixed error word and nothing else, because a failed parse can echo its input. The adapter's `connection-string quirks` say where the host is when it isn't the part after the `@`.
   - If any host is listed under `never-write hosts`, stop with the never-write message below, even when that host is also a loopback address, a unix socket, or a local database file, or is listed under `allowed hosts`. Don't suggest removing it from `never-write hosts` or any other way to migrate it; changing that list is the user's decision. Otherwise continue when every host is a loopback address (`localhost`, `127.0.0.1`, or `::1`, which a URL parser prints as `[::1]`), a unix socket, or a local database file, or is listed under `allowed hosts` in the settings file; else stop with the other-host message below. Either stop comes here, before step 3 creates anything or any of the adapter's `connecting commands` runs.
   - When the user wants only a plan, or no shell is available, skip this step's commands: read the tool's release from the adapter's `version without a shell` (when nothing is installed, that's the range the project declares; say so), find the files, and say in the plan that the CLI and host checks haven't run and must pass before anything is applied.

   Stop messages, with the placeholders filled in (`<settings file>` is the one in use, else `.claude/shipyard/db-migration.md`):

   ```
   Stopped before creating any migration: <host> is listed under never-write hosts, and this skill never migrates it.
   Stopped before creating any migration: <host> isn't a loopback address, a unix socket, or a local database file, and isn't listed under allowed hosts. This skill only migrates a development database; if <host> is one, add it under allowed hosts in <settings file>.
   Stopped at the CLI check: the installed <tool> <release> doesn't provide <what the CLI check looks for>, so this skill doesn't cover that release. Nothing was migrated.
   ```

2. **Edit the schema** with the requested change, matching the file's existing naming, name-mapping style (the adapter's `physical names`), and relation conventions.
3. **Create the migration without applying it.** If the adapter says its `create without applying` first applies migrations already pending in the folder, run the adapter's `status` before it. If any are pending, tell the user that command will apply them, and take each one through step 4, gate included, before running it. When the adapter says `generates: yes`, run its `create without applying` command with a descriptive snake_case name. When it says `generates: no`, write the migration by hand in the adapter's `layout`, using the database names. After the command, whatever its exit code, check its output against the adapter's `refusals` and `known failures`, and confirm a new migration file is in the migrations folder. Stop on a refusal, or when no new file was written; for a known failure, tell the user the fix the adapter gives, such as a shadow database the database user isn't allowed to create.
4. **Review the SQL.** Show the migration's SQL (the adapter's `SQL preview` when its `format` is code) and check every quoted identifier against the schema's database names (the adapter's `physical names`; skip this check when it says `none`). If a migration linter for the database is available, or the settings file names one, run it. `STOP — WAIT` when the SQL contains any change listed in [references/risky-changes.md](references/risky-changes.md): show the SQL and the safer path, with the adapter's risky-change notes for that row, and let the user choose. The migration will later run on production, whose row counts can't be seen from here, so count every table that existed before this migration as large and full, whatever the development copy holds; only a table the same migration creates is exempt. Otherwise continue.
5. **Apply, regenerate, update types.** Apply with the adapter's `apply` command, passing the same name where it takes one. If it fails, check its output against the adapter's `refusals` and `known failures` as in step 3. Then, when the adapter has a `regenerate client` command, always run it explicitly: some releases don't regenerate the client as part of applying. Update application types, DTOs, and validation schemas that mirror the changed models, importing from the adapter's `client import` path, or where the settings file's `application types` says.
6. **Confirm nothing is pending.** Run the adapter's `status` command. Its `status exit code` says what the exit code means; where one code covers both pending migrations and connection errors, read the output rather than the code. If migrations are pending on the development database, apply them with the adapter's `deploy pending` command and run status again. Report the final status output verbatim; a migration left unapplied looks downstream like a missing feature. When the adapter's `status` is `none`, say that nothing confirmed the migrations are applied, and report the `apply` output verbatim instead.

If the tool can't find the database connection, check how the project loads environment variables (the settings file's `environment`, else the adapter's); don't assume the tool reads an env file on its own.

## Hand-written migrations

When asked to check a migration someone wrote by hand, audit it before trusting it. For every quoted identifier in the SQL, find the owning model, enum, or field in the schema and confirm the SQL uses its database name (the adapter's `physical names`), not the schema's own name. The adapter's `diff` command, when it has one, prints what the tool would generate, for comparison; when it's among the adapter's `connecting commands`, run step 1's checks before it. When the adapter says `generates: yes` and the wrong hand-written migration hasn't been applied to any database yet, the fix is to remove it and create it again with step 3's `create without applying` command (the settings file's, if it names one): give the user that exact command, name included, rather than editing the file. If it has been applied anywhere, don't remove it: the fix is a new migration, made through steps 1 to 6, that corrects it: give the user step 3's command for it as well, name included.

## Handoff

`next:` back to the implement stage, with the migration name and the final status output.
