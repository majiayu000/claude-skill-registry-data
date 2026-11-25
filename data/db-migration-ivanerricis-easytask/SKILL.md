---
name: db-migration
description: Checklist to add a database migration to EasyTask (new table, column or index in SQLite) and carry the new data everywhere it must go - schema, workspace edit triggers, queries, tree loading, state and undo, trash and archive, templates, copies, cross-note moves, export/import/validate, tests. Use when a feature needs a new table or column, when touching src/db/schema or src/db/initDb.ts, or when new data must survive templates, copies, export or the trash.
---

# Database migration (EasyTask)

The database is SQLite, entirely in TypeScript (`src/db/`); there are no Rust queries. Migrations live in `src/db/initDb.ts`: an ordered array, one entry per version, tracked with `PRAGMA user_version`. A good model of a full migration is **v20** (`section_tag`, commit `600fa15`, PR #160): `git show 600fa15 --stat` lists every place that had to change.

## 1. The migration

- **Append** a new entry at the end of `migrations` with a `// vN: <what>` comment. Never edit an applied migration and never reorder them: users already have those versions.
- Every migration is **idempotent and additive**: `CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`, `ALTER TABLE ... ADD COLUMN` with a default. To drop or reshape a column: a script with its own `BEGIN IMMEDIATE ... COMMIT` (see the comment of `applyMigration`, which writes the version bump inside it).
- The SQL goes in `src/db/schema/<table>.ts`, exported as a `string[]` (`sectionTagSchema`), and re-exported by `schema/initial.ts` like the others.
- Before migrating an existing database the app takes a backup (`beforeMigrate`, `src/db/backup.ts`): do not add another copy.
- Foreign keys with `ON DELETE CASCADE` toward the owner (task, section, group, note, workspace); `deleted_at` only if the row goes to the trash by itself.

## 2. Workspace edit date

`src/db/schema/workspace_edit.ts`: every table inside a workspace must refresh its edit date.
- Add the table to `workspaceOf` (SQL that finds its workspace from the row).
- A table created after v3 goes in `CREATED_LATER`, and its migration includes `...triggersFor("<table>")`.
- Columns that are only view state (open/closed, widths) must not bump the date: see the column-filtered update trigger of v10.

## 3. Where the data must travel

Go through every line; "not needed" is a valid answer, a forgotten one is a bug that tests do not catch.

| Area | Files (v20 as example) |
| --- | --- |
| Queries | `src/db/queries/<area>.ts` (`tag.ts`): set, list, delete, restore |
| Loading the note tree | `queries/note.ts` and the type in `src/types/types.ts` |
| State | `contexts/workspace-data/*` (`types.ts`, the area file), helpers in `src/lib/` |
| Mutations + undo | `src/hooks/use-<area>-mutations.ts`, `contexts/undo/commands.ts`; the list of undo command names in `src/test/mocks.ts` |
| Trash / archive | `schema/trash_index.ts` (`TRASHABLE_TABLES`), `queries/trash.ts`, `queries/archive.ts`; restore must bring the rows back |
| Templates | `queries/template.ts`, `queries/template-draft.ts`, `src/types/template.ts`, automations carried by templates |
| Copies | `queries/duplicate.ts`, `queries/task-paste.ts` |
| Moves between notes | `queries/cross-note.ts` (move and Alt copy), `queries/move.ts` |
| Export / import | `queries/transfer/export.ts`, `import.ts`, `validate.ts` (new optional fields: old files without them must still import) |
| Workspace scope | ids from another workspace must be refused (`assertSameWorkspace` in `move.ts`) |
| UI texts | en + it (skill **i18n-keys**) |

## 4. Tests

- `src/db/initDb.test.ts`: bump `LATEST_SCHEMA_VERSION` and the final `user_version`, and test the migration from the previous version with real rows (data kept, new table/column present, running it twice changes nothing).
- `src/db/initDb.atomic.test.ts`: the version number and the list of all the schemas (search for the last schema name, e.g. `noteBackgroundImageSchema`, in the tests).
- Query tests next to the query file (`queries/<area>.test.ts`): include trash + restore, template round trip, copy, export + import.
- An e2e that reads what was saved with `sql(...)` (skill **e2e-spec**).
- Before push: skill **pre-push**.

## 5. Things to tell the user

- A database migrated by version N cannot be opened by an older app (`newerDbMessage`): say it in the PR when the release goes out, and mention it in the changelog only if users can notice it.
- Export files gain fields: an older app importing a newer file ignores them or refuses it (check `validate.ts`) and say which in the PR.
