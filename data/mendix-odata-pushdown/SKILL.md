---
name: mendix-odata-pushdown
description: Push OData query options into the SQL of a Mendix resource served by a read microflow, so $filter, $orderby, $top, $skip, $count and the key lookup reach the database instead of being silently dropped. Use when publishing an OData resource over data Mendix has no table for — a warehouse view, a legacy database, a Databricks catalogue, a stored procedure, a CSV read through a connector — or when a published resource returns 200 with the wrong rows and nothing appears in the log.
---

# Pushing OData query options into your own SQL

## The problem this exists for

Mendix will publish any entity over OData, including one with no table behind
it: declare the resource non-persistable, give it a read microflow, done. What
the documentation does not say is that Mendix then applies **none** of the query
options to your answer. `$filter`, `$orderby`, `$top`, `$skip`, `$count` and the
key lookup all arrive on the request URI and all stay there. Whatever the
microflow returns is exactly what the client gets.

That is not a 500 and not an empty grid. It is a **200 with the wrong rows**:

- `?$top=5` returns all 917 rows and the widget shows five of them, so paging
  looks correct while every page ships the whole table.
- A client re-reading one held row by key gets the collection back, adopts the
  first row as that object's identity, and **keeps it**. A detail page for one
  record shows another record's data, and nothing logs a word.

The second one is the reason to care. It is not a performance problem; it is
wrong data on screen, and every check is green.

## What the pack gives you

Four Java actions and the entity they return. Nothing in them is specific to any
database or any app.

```
{{MODULE}}.Parse(Uri, Columns, Dialect, MaxTop, DefaultTop,
                 DefaultOrderBy, KeyField, RejectUnsupported) -> {{MODULE}}.Query
{{MODULE}}.Key(Uri, KeyField)                                 -> String
{{MODULE}}.FilterNumber(Uri, Field, Fallback)                 -> Long
{{MODULE}}.CallStatement(Routine, Kind, Parameters, Dialect)  -> String
```

`Parse` is the whole thing. `Key` and `FilterNumber` are short forms for the
common case — a resource reachable one way only ("the sessions of this
weekend"), whose entire contract is one value out of `$filter`. `CallStatement`
builds the invocation for a resource backed by a stored routine.

### `{{MODULE}}.Query`

| Field | Style | What it is |
|---|---|---|
| `FilterSql` | splice | `" WHERE …"`, or empty |
| `OrderBySql` | splice | `" ORDER BY … LIMIT n OFFSET m"` |
| `SelectSql` | splice | `" a, b, c"` for `$select`, or empty for all columns |
| `SelectedColumns` | bind | the same columns as exposed names |
| `Key` | bind | the key the client is re-reading one row by; empty for a collection |
| `Top`, `Skip` | bind | the page, already clamped to `MaxTop` |
| `SortColumn1/2`, `SortDirection1/2` | bind | the sort, as exposed names and `A`/`D` |
| `WantsCount` | both | `$count=true` — the client wants the size of the set |
| `Rejected`, `RejectReason` | bind | the request asked for something untranslatable. Only a **bind** caller sees these: with `RejectUnsupported = true` (what a splice caller passes) `Parse` throws instead of returning, so a splice caller always has `Rejected = false` |

## Two ways to spend it

Which one you get is decided by whether you own the SQL.

**Splice** — you build the statement, so concatenate the fragments into it.

```
$Q = CALL JAVA ACTION {{MODULE}}.Parse(
  Uri = $Request/Uri, Columns = $Cols, Dialect = 'postgresql',
  MaxTop = 500, DefaultTop = 500, DefaultOrderBy = 'name ASC',
  KeyField = 'driverId', RejectUnsupported = true);

DECLARE $Sql String = $Select + $Q/FilterSql + $Q/OrderBySql;
```

**Bind** — the SQL lives somewhere you cannot rewrite: a named query on a
database connection, a view, a procedure. Take the values, pass them as
parameters. This style is why the module is not simply a SQL builder: most data
worth publishing this way sits behind SQL somebody else owns.

`references/patterns.md` has the working shape of both, including the `CASE`
construction that makes a fixed statement sortable by a parameter.

## `Columns` — the whitelist, and why the type is not decoration

`exposedName:sqlExpression:type`, comma-separated:

```
'name:d.name:text,wins:d.race_wins:number,active:d.is_active:bool,born:d.dob:date'
```

Nothing outside this list can be filtered or sorted on, and a filter naming
something outside it is a **rejection**, not an omission.

Mendix quotes a literal according to what the *widget* believes the attribute
is, which is not always what the column is: a combo box on a numeric key sends
`year eq '1957'` while the grid header above it sends `year eq 1957`. Passing
the quotes through gives the engine `year = '1957'` against a BIGINT — zero
rows, status 200. The type is what makes both spellings mean the same thing.

## What it understands

Everything Mendix's OData client emits, and nothing else.

| | |
|---|---|
| comparisons | `eq` `ne` `gt` `ge` `lt` `le` |
| functions | `contains` `startswith` `endswith` |
| logic | `and` `or` `not`, parentheses, correct precedence |
| literals | text, numbers, decimals, `true`/`false`, `null`, ISO instants |
| options | `$filter` `$orderby` (two terms) `$top` `$skip` `$count` |
| the key | `?$filter=k eq 'v'`, `/Res('v')`, `/Res(k='v')` |
| dialects | `postgresql` `duckdb` `sqlserver` `oracle` `mysql` |

OData itself is far larger — arithmetic, lambdas, `$apply`, date functions,
`any`/`all`. None of it is emitted by a Mendix client, so none of it is here. A
request outside the grammar is **rejected**, not ignored: `Rejected` comes back
true and the caller is expected to fail the request. Dropping a filter you could
not read returns more rows than were asked for and calls it success, which is
the bug the module exists to stop.

## Install

```bash
mxcli skill add mendix-odata-pushdown --apply -p App.mpr
```

Then add `{{MODULE}}.User` to whichever user roles your published service runs
as — the pack cannot do that itself without knowing your role names.

**`--apply` writes to the model**: a module, the `Query` entity, a module role
and four Java actions. Without it the pack only copies its own files.

> **Not installable yet.** `installs.java` is a proposed manifest target that
> mxcli does not implement, and without it the MDL applies but the helper
> classes it delegates to never reach `javasource/`. `references/packaging-gap.md`
> has the detail and the manual fallback.

## Read next

| File | For |
|---|---|
| `references/patterns.md` | splice and bind end to end, and the sortable-fixed-statement `CASE` |
| `references/failure-modes.md` | what breaks, symptom first |
| `references/packaging-gap.md` | why this pack does not install, and how to apply it by hand |

## `$select` narrows the read, it does not fix the answer

`SelectSql` is the one option here that is an optimisation rather than a
correction, and it is worth knowing which before spending time on it.

Mendix applies `$select` to the response **itself** — measured on 11.13, on a
microflow-backed resource as much as on a database read — so the client already
receives only the fields it asked for whatever the microflow does. What pushing
it down saves is *reading* columns nobody will look at: real time over a wide
CSV through a columnar reader, nothing at all over a narrow table.

The consumer drives it. An external entity with attributes removed sends a
narrower `$select`, because it has nowhere to put what it dropped — so the
projection is negotiated end to end without either side arranging it.

Splice it after `SELECT`, and keep your own list when it is empty:

```sql
SELECT {{SelectSql or your full list}} FROM read_csv_auto(?) AS t
{{FilterSql}}{{OrderBySql}}
```

Three behaviours worth relying on:

- **The key is always projected**, even when `$select` omits it. It costs one
  column and stops a caller that dedupes, associates or re-reads by key from
  losing the value it does that with. The client still sees only what it asked
  for, because Mendix projects the response.
- **An unknown column is rejected, not skipped.** A wrong sort order is
  cosmetic and is ignored; a dropped projection is not — answering with a null
  where data was expected is the same "200 and wrong" this component exists to
  prevent.
- **Sort columns are not forced into the projection.** `ORDER BY` may name a
  column the `SELECT` list omits; that is ordinary SQL, and adding them would
  defeat the narrowing.

### What is still not translated

`$expand` is **not** supported, and is rejected rather than ignored when
`RejectUnsupported` is on. It is a different kind of work from everything else
here: not a projection but a join producing a nested object graph, which the
microflow would have to build as associated Mendix objects, with nested options
(`$expand=X($filter=…;$top=3)`) multiplying the surface. `$search`, `$apply` and
the lambda operators (`any`/`all`) are unhandled for the same reason — each is a
new grammar rather than a new clause.

## Checking it without an app

```bash
mkdir -p /tmp/pc/odatapushdown
sed -e 's/{{MODULE_PATH}}/odatapushdown/g' -e 's/{{MODULE}}/ODataPushdown/g' \
    java/ODataQueryParser.java > /tmp/pc/odatapushdown/ODataQueryParser.java
javac -d /tmp/pc /tmp/pc/odatapushdown/ODataQueryParser.java scripts/ParserCheck.java
java -cp /tmp/pc ParserCheck
```

`ParserCheck` exits non-zero on the first failure and prints what it expected.
It covers the projection, the filter grammar's quoting of numeric columns, the
sort terms, the `MaxTop` clamp, `$count`, and that an unreadable filter is
rejected rather than dropped. A dialect regression here is invisible to
`mx check` and to every test that needs an app, which is why it is worth a
second.
