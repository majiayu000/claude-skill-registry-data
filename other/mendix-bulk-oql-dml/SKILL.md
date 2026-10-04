---
name: mendix-bulk-oql-dml
description: Run set-based INSERT, UPDATE and DELETE against Mendix entities through OQL statements, which the runtime supports and Studio Pro cannot author. Use when a microflow would otherwise retrieve a large list and loop — applying rules across a table, copying a year of records, staging and promoting an import, archiving, backfilling a column — or when a nested retrieve-loop-commit is the reason a screen or a scheduled job is slow.
---

# Bulk DML through OQL statements

## What this is

The Mendix runtime executes OQL **statements**, not just queries. Three calls, all
in `com.mendix.public-api.jar`:

```java
com.mendix.core.Core.createOqlStatement(String)   // -> OqlStatement
OqlStatement.setVariable(name, value)             // -> OqlStatement, chainable
OqlStatement.execute(IContext)                    // -> int rows affected
```

Studio Pro has no activity for this, so the only way to reach it is a Java action.
[`mdl/oql-dml-actions.mdl`](mdl/oql-dml-actions.mdl) is three of them, authored in
MDL with inline Java, ready to apply to any project:

| Action | Use |
|---|---|
| `OQL_Execute(Statement)` | One statement, no variables. Returns rows affected, throws on failure. |
| `OQL_ExecuteWith(Statement, Name/Value/Type ×4)` | Same, with up to four bound, typed variables. |
| `OQL_Try(Statement)` | Returns `OK rows=N` or `ERR …` instead of throwing. For probing, not for production paths. |

```bash
mxcli exec .claude/skills/mendix-bulk-oql-dml/mdl/oql-dml-actions.mdl -p MyApp.mpr
```

## Check the version first

Each statement type arrived in a different runtime release, and the last one is
recent enough that "it works on my app" is not transferable:

| Statement | Available from |
|---|---|
| `DELETE` | 11.1.0 |
| `UPDATE` | 11.3.0 — associations 11.4.0 |
| `INSERT … SELECT` | 11.6.0 — associations 11.7.0 |
| `INSERT … VALUES` | 11.13.0 |

Pin the runtime version deliberately before building on this.

## When to use it, and when not

Use it when the work is **a set** and nobody is looking at the rows: applying
rules over a table, copying a year of records, promoting a staged import,
archiving, backfilling a new column. One statement replaces a retrieve of every
match into memory, a loop, and a commit per object.

Do not use it for a single object a user is editing. And know what it skips —
this is the thing to say out loud before choosing it:

> A statement runs in the database, inside the calling microflow's transaction.
> It does not pass through the object cache, so **no event handlers fire, no
> validation rules run, an object already retrieved keeps its old values, and a
> client holding one is not refreshed.**

If the entity's correctness depends on a before-commit handler, either move that
logic into the statement or do not use a statement.

## Making the result visible

A grid over rows a statement just rewrote keeps showing the old ones, because
nothing told the client. The pattern that fixes it, used on both screens in this
project:

1. The screen has a small non-persistent context object.
2. The grid's datasource is a **database** source constrained on that object
   (`where [Batch = $currentObject/Batch]`).
3. The action ends with `commit $Context refresh;`.

Refreshing the context re-runs the grid's query. Without step 3 the screen is
quietly wrong, which is worse than obviously wrong.

## Patterns that work

Full statements, from three working use cases, are in
[`references/patterns.md`](references/patterns.md):

- **First-match-wins rules** — one `UPDATE` per rule, in order. The precedence
  lives in the WHERE clause: each statement only touches rows still unclaimed,
  so a later rule cannot take a row an earlier one took. No flags, no loop.
- **Copy a year** — `INSERT … SELECT` per month. Idempotent by deleting the
  target window first, in the same transaction.
- **Stage and promote** — land rows in a loader entity, validate them *where
  they landed* with one `UPDATE` per check stamping a reason on the failures,
  then promote the survivors with a single `INSERT … SELECT`. The rejects stay
  behind with their reason, which is the whole argument for a loader table.

## Before writing a statement

Read [`references/gotchas.md`](references/gotchas.md). Four things cost real time
here, and one of them wrote bad data:

1. **An association compared to `null` in a WHERE matches nothing** — in both
   spellings, with no error. A validation written that way passes every row.
2. **Alias every column in an `INSERT … SELECT`.** Two association paths both
   end in `/id` and collide as `Duplicate column name: ID`, naming a column that
   is not in your statement.
3. **Association columns must be module-qualified** — `Ledger.Order_Customer`,
   not `Order_Customer`.
4. **No `substring`.** String surgery has to be done by the caller, which is why
   "copy a year" is twelve statements rather than one.

## Probing safely

The grammar is not discoverable from the model, so find out by running. Use
`OQL_Try` with statements whose WHERE cannot match, from a microflow that logs
each result, and read the log. Sixteen statements in one pass is what mapped the
matrix in `references/patterns.md`.

Two warnings if you use the after-startup microflow as the harness, both learned
the hard way: a statement that throws there **takes the whole app down**, and
the action is one transaction, so a failure at the end **rolls back everything
before it** — including work whose log lines already said it succeeded.
