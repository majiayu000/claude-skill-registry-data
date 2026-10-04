---
name: appflare-schema
description: Define and change the Appflare schema DSL (schema, table, v) and apply D1 migrations. Covers column builders (v.int, v.string, v.boolean, v.date, v.uuid, v.enum, v.array, v.object), modifiers (notNull, unique, default, defaultNow), table options for composite indexes and CHECK constraints, relations with v.one, v.many and v.manyToMany including foreign key naming, relationName pairing and junction tables, and the appflare migrate and migrate:custom workflow. Use when adding a table, column, enum, JSON field, index, constraint or relation, fixing FK or nullability issues, or running migrations in an Appflare project.
metadata:
  author: appflare
  version: "0.3.0"
---

# Appflare schema

## Workflow

- [ ] Open the schema entry (`schemaDsl.entry` in `appflare.config.ts`, usually `schema.ts`)
- [ ] Edit tables inside the exported `schema({...})`
- [ ] Run `bun appflare dev` from the backend package and fix any compiler error it prints
- [ ] Run `bun appflare migrate --local` and review the new SQL file in `drizzle/`
- [ ] Update the handlers and client code that use the changed fields

## Template

```ts
import { schema, table, v } from "appflare";

export const schemas = schema({
	projects: table({
		id: v.uuid(),                                   // text PK, crypto.randomUUID() on insert
		name: v.string().notNull(),
		slug: v.string().notNull().unique(),
		status: v.enum(["active", "archived"]).notNull().default("active"),
		tags: v.array(v.string()),                      // JSON text
		settings: v.object({ color: v.string(), public: v.boolean() }),
		createdAt: v.date().defaultNow(),               // runtime default on insert
		owner: v.one("users"),                          // ownerId (NOT NULL) → users.id
		tasks: v.many("tasks"),                         // adds projectId to tasks
	}),
	tasks: table({
		id: v.int().primaryKey({ autoIncrement: true }),
		title: v.string().notNull(),
		done: v.boolean().notNull().default(false),
		dueAt: v.date(),
		project: v.one("projects"),                     // projectId: matches v.many above
		assignee: v.one("users", { nullable: true }),   // assigneeId (nullable)
		labels: v.manyToMany("labels"),
	}),
	labels: table({
		id: v.int().primaryKey({ autoIncrement: true }),
		name: v.string().notNull().unique(),
		tasks: v.manyToMany("tasks"),                   // junction: labelsTasksLinks (labelId, taskId)
	}),
	accounts: table(
		{
			id: v.int().primaryKey({ autoIncrement: true }),
			status: v.string().notNull().default("active"),
			balanceMinor: v.int().notNull().default(0),
		},
		{
			indexes: [{ columns: ["status", "balanceMinor"] }],        // composite index
			checks: [{ name: "accounts_balance_non_negative", sql: "balance_minor >= 0" }],
		},
	),
});
```

## Several relations to the same table

```ts
messages: table({
	sender: v.one("users", { relationName: "sender" }),                       // senderId
	recipient: v.one("users", { relationName: "recipient", nullable: true }), // recipientId
}),
// on the users side (if you own that table):
sentMessages: v.many("messages", { relationName: "sender" }),
```

A `v.many` whose target has more than one matching `v.one` fails generation unless both sides share a `relationName`. The named `v.many` reuses the `v.one`'s foreign key instead of inferring a new column.

## Rules to apply

- **Primary keys:** use `v.uuid()` for string ids or `v.int().primaryKey({ autoIncrement: true })` for numeric ids.
- **Nullability:** plain columns are nullable and optional. Add `.notNull()` to required fields. FKs from `v.one` and `v.many` are **NOT NULL** unless `{ nullable: true }`.
- **FK names:** `field: v.one("t")` creates `fieldId`. `source.rel: v.many("target")` adds `<singular source>Id` to the target. Give the inverse `v.one` the same name (`project` ↔ `projects.tasks`), or pass the name explicitly (`v.many("tasks", "parentProjectId")`).
- **Many-to-many:** declare `v.manyToMany` on both tables with identical options. The junction holds links only. If the link needs data (a role, a timestamp), create an explicit join table with two `v.one` relations.
- **Defaults:** `.default(x)` is a SQL default. `.defaultFn(fn)`, `.defaultNow()` and `v.uuid()` are runtime defaults applied on insert (not by raw `ctx.$db`). Any column with a default reads back as non-null and rejects an explicit `null`; add `.nullable()` if it really stores nulls.
- **Invariants:** put rules that must always hold in `checks` (or a trigger via `migrate:custom`), because a batch can't abort on a condition. They surface as `CheckConstraintError`/`TriggerAbortError` → HTTP 400.
- **Auth tables** (`users`, `sessions`, `accounts`, `verifications`) come from Better Auth. Reference them (`v.one("users")`) but never define them.
- **SQL naming** is camelCase to snake_case automatically. Use `.sql("name")` or `table(shape, { sqlName })` only to match an existing database.

## Gotchas

- `v.number()` is an alias of `v.int()` and creates an INTEGER column. There is no float column type.
- `v.date()` is stored as epoch milliseconds, and filters accept `Date` or numbers.
- `.defaultNow()` and `.defaultFn()` don't add a SQL default, so rows inserted with raw SQL (and rows written before the default existed) keep `NULL` even though the type says otherwise.
- `checks[].sql` uses **SQL column names** (`balance_minor`), not field names.
- Triggers, views and backfills go in an empty migration: `bun appflare migrate:custom --name add_guards`.
- Reciprocal `manyToMany` declarations with different `junctionTable` or field options fail generation.
- `onDelete: "set null"` requires `nullable: true` on the relation.
- `migrate` reads the compiled schema, so always run `bun appflare dev` first.
- Pass only one of `--local`, `--remote` or `--preview` to `migrate`.
- Adding a Better Auth plugin changes auth tables. Regenerate and migrate afterwards.

## References

- Read [references/column-api.md](references/column-api.md) when you need every `v.*` builder, option or modifier, or the SQL and TypeScript mapping.
- Read [references/relations.md](references/relations.md) when configuring relation options (custom FK names, reference fields, junction names, FK actions, self-relations) or debugging a relation compile error.
