---
name: appflare-querying
description: Read and write data in Appflare handlers with the typed ctx.db API, including findMany and findFirst with where operators (eq, in, gt, contains/startsWith/endsWith, exists, includes, geoWithin) and and/or/not combinators, relation loading and filtering with "with", orderBy, limit/offset, iterate and cursor pagination, insert with nested relations, update with increment/decrement expressions and expectRows guards, atomic batch and transaction writes, upsert with target/set, delete, count, sum, avg, min, max and groupBy aggregates, and the ctx.$db raw Drizzle escape hatch. Use when writing database logic, filters, search, joins, pagination, counters, aggregates, upserts, transfers or bulk updates inside Appflare query, mutation, scheduler or cron handlers.
metadata:
  author: appflare
  version: "0.3.0"
---

# Appflare data access (`ctx.db`)

## Default patterns

```ts
// list with filters, relations, sort and limit
const tasks = await ctx.db.tasks.findMany({
	where: {
		projectId: args.projectId,
		...(args.search ? { title: { contains: args.search, options: "i" } } : {}),
		done: false,
	},
	with: { assignee: true, labels: true },
	orderBy: { column: "id", direction: "desc" },
	limit: args.limit,
});

// single row (or undefined)
const task = await ctx.db.tasks.findFirst({ where: { id: args.id } });

// create
const [created] = await ctx.db.tasks.insert({ values: { title, projectId } });

// update (always scope with where, ideally including ownership)
const [updated] = await ctx.db.tasks.update({ where: { id, assigneeId: ctx.user.id }, set: { done: true } });

// delete
const removed = await ctx.db.tasks.delete({ where: { id } });

// counts
const open = await ctx.db.tasks.count({ where: { projectId, done: false } });
```

## Procedure

1. Check the schema for the table name (the key in `schema({...})`) and the field names. Relation FKs are `<relation>Id`.
2. Put every filter in `where`. For optional filters, spread them in conditionally and never pass `undefined` values.
3. Load related rows with `with`. To filter parents by related rows, use the relation name inside `where`.
4. For lists, add `orderBy` and `limit`. For pages, return `{ rows, nextCursor, hasMore }`. For full scans, use `iterate`.
5. For writes, scope `update` and `delete` with `where`, and check the returned array length to detect "not found".
6. When several writes must all land or none, wrap them in `ctx.db.batch` (writes known up front) or `ctx.db.transaction` (writes that depend on a read).

## Counters, money and other concurrent writes

Never read a value, compute in JS, then write it back. Let SQL do it:

```ts
import { decrement, increment } from "appflare";

await ctx.db.accounts.update({
	where: { id: accountId, balance: { gte: amount } },
	set: { balance: decrement(amount) },
	expectRows: 1, // no matching row → AppflareConflictError, nothing written
});
await ctx.db.posts.update({ where: { id }, set: { views: increment() } });
```

## Atomic multi-table writes

```ts
// every write known up front
const [entries, [debited]] = await ctx.db.batch((tx) => [
	tx.ledgerEntries.insert({ values: [{ accountId: from, amount: -cents }, { accountId: to, amount: cents }] }),
	tx.accounts.update({ where: { id: from }, set: { balance: decrement(cents) }, expectRows: 1 }),
]);

// a write that depends on a read
await ctx.db.transaction(async (tx) => {
	const account = await tx.accounts.findFirst({ where: { id: args.id } });
	if (!account) ctx.error(404, "Not found");
	const handle = tx.accounts.update({ where: { id: args.id }, set: { status: "closed" } });
	await ctx.scheduler.enqueue("jobs/notify", { id: args.id }); // sent only after commit
	return handle;
});
```

## Cursor pagination template

```ts
args: {
	cursor: z.coerce.number().int().optional(),
	pageSize: z.coerce.number().int().min(1).max(50).default(20),
},
handler: async (ctx, args) => {
	const rows = await ctx.db.posts.findMany({
		where: args.cursor ? { id: { lt: args.cursor } } : {},
		orderBy: { column: "id", direction: "desc" },
		limit: args.pageSize,
	});
	return { rows, nextCursor: rows.at(-1)?.id, hasMore: rows.length === args.pageSize };
},
```

## Gotchas

- `findMany` returns **100 rows by default** and rejects `limit` above 1000. Pass `limit`, or use `iterate` to walk everything.
- `update` and `delete` **throw** without a filter. Pass `allowAll: true` when you really mean every row. A `where` whose values are all `undefined` counts as empty.
- **Unknown `where` keys throw.** Check spelling and use FK fields (`ownerId`), not relation names, for id equality.
- `contains`/`startsWith`/`endsWith` are substring matches with `%` and `_` escaped; `regex` is an alias of `contains`, not a real regex. Add `options: "i"` for case-insensitive.
- Use `or` / `and` / `not` for boolean logic. `or: []` matches nothing.
- Every write method returns an **array**. Destructure (`const [row] = …`) and check for `undefined`.
- `expectRows` failing throws `AppflareConflictError` and writes nothing, including the rest of a batch.
- Inside `ctx.db.transaction`, writes return **handles, not promises**: read `handle.rows` after the transaction resolves, and do reads before queuing writes because reads don't see them.
- `upsert` defaults `target` to `"id"`; without `set`, each conflicting row updates with its own values.
- `ctx.$db` is still available for raw Drizzle, but it skips runtime defaults, JSON handling and realtime events. Prefer `ctx.db`.
- `v.date()` filters accept `Date` or epoch milliseconds.
- `_count`/`_avg` inside `with` add `<relation>Aggregate` (e.g. `row.commentsAggregate.count`) and are computed in JS; prefer `groupBy` for large relations.

## References

- Read [references/where-operators.md](references/where-operators.md) when building non-trivial filters: all operators, combinators, relation filters, JSON array and object filters, dates, geo distance, ordering, iterate.
- Read [references/writes.md](references/writes.md) when inserting nested relations, using expressions or guards, batching, transacting, updating many-to-many links (`items`/`mode`) or upserting.
- Read [references/aggregates.md](references/aggregates.md) when computing counts, sums, averages, min/max or grouped results.
