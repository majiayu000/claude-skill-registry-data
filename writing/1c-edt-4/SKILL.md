---
name: '1C EDT: оптимизация запросов'
description: >-
  Use when writing or tuning queries in a 1C:EDT project for indexes, joins,
  virtual tables, balances, and temporary tables.
---
# 1C EDT: оптимизация запросов

Apply when a query in a 1C:EDT project is slow, locks too much, or is being written for a large table. Checklist distilled from ITS v8std, not a copy of the articles. Query text layout is a separate skill.

## Shape of the query (№729)

- Select only the fields and rows you need.
- Leave grouping, sorting, and arithmetic to the DBMS when that stays simple.
- Cut the number of round trips. Do not push every bit of logic into the DBMS.
- Prefer a few simple queries over one clever query.
- Check the actual plan. Do not add a nested query just so the text reads nicely, and do not pile on joins, conditions, and tables without a reason.

## Indexes (№652, №791)

- Conditions in `ГДЕ`, `ПО`, virtual-table parameters, and `ИМЕЮЩИЕ` need an index that fits.
- Every field of the main condition sits at the start of the index, in order, with no gaps.
- A missing index means a scan and extra locks.
- Use the indexes the platform already creates. Add another only when a measurement shows you need it.
- Do not index “just in case”, do not index a low-selectivity field, and do not repeat the register’s first-dimension index.
- Extra indexes speed reads and slow writes.
- Additional indexes (the metadata feature) are for large CORP deployments only. A PROF configuration aimed at small companies must not depend on them.
- The configuration must stay acceptable up to about 100 000–1 000 000 rows without additional indexes. Measure with them on and off. Keep one code path, not a fork. A field that only avoids a table lookup is an included field, not a key.

## Dotted composite references (№654)

- A dot through a reference is a hidden join. Do not dereference a composite reference without looking at the types.
- Do not use “any reference” or “any document” unless the task needs it. Narrow the type list.
- If a value is read often, store it on the source table instead of joining every time.
- In one query, cut the type with `ВЫРАЗИТЬ`. If callers need different types, write a separate query per type.

## Nested queries and virtual tables (№655, №656, №657)

- Do not join to a nested query unless the set is small. Put it in a temporary table.
- If a virtual table is slow inside a join, materialize it first.
- Do not use an implicit nested join. Prefer a chain of queries. If the nesting is real, use a temporary table.
- Do not put a nested query inside a join condition.
- Filters that belong to a virtual table go in its parameters, not in the outer `ГДЕ`.
- Parameters should be simple: dimension equals value. No joins or subqueries in parameters unless there is no other way.
- If a subquery in a parameter is unavoidable, it reads one table and has no joins.
- Do not mix a tabular section with its header attributes, and do not read a tabular section from a subquery on the header.
- Do not put `ГДЕ` on a subquery over a temporary table.
- When several subqueries filter, keep the most selective one in the parameter and move the rest out, or into a temporary table.

## Conditions (№658)

- The main condition uses indexed fields, combined with `И`.
- Leading index fields are equalities. A range is only on the last field.
- The main condition has no functions, arithmetic, `НЕ`, or an inequality the index cannot use.
- Index the correct side of a join: the right side of a left join, the larger table of an inner join.
- A small table or a rare query may break these rules.
- Do not put `ИЛИ` between different indexed fields in the main condition. Split the query or use `В`.
- Do not give one user several roles whose RLS conditions on the same object differ.

## Slices and balances (№708, №733)

- Turn on totals for a large periodic information register that is usually read as the current slice of first or last. Then the virtual table is filtered by dimensions and allowed separators only.
- RLS on that register uses only dimensions and the matching separators. Change queries that do not fit.
- Do not enable totals if queries usually pass a concrete period, or if slice parameters often contain joins or subqueries.
- Do not build a custom totals recalculation. The platform maintains them, unless code has switched that off.
- Current accumulation balances: do not pass a date. Do not use totals splitting if this read must be as fast as possible.
- The outer query uses every dimension of the balance table. Dimension filters go into the `Остатки` parameters and are also used in the outer join. Do not leave a dimension only inside the parameters.

## Temporary tables (№777)

- Use them to keep a plan stable.
- Do not load hundreds of thousands of rows into one temporary table. Process large sets in portions.
- Only the rows and fields the next step needs.
- Do not create and drop the table inside a loop if one table can live for the whole batch.
- Do not copy a temporary table just to rename it.
- Index a large temporary table when the plan benefits. If several indexes compete, index the condition you test most often.

## Sources

- https://its.1c.ru/db/v8std/content/729/hdoc
- https://its.1c.ru/db/v8std/content/652/hdoc
- https://its.1c.ru/db/v8std/content/654/hdoc
- https://its.1c.ru/db/v8std/content/655/hdoc
- https://its.1c.ru/db/v8std/content/656/hdoc
- https://its.1c.ru/db/v8std/content/657/hdoc
- https://its.1c.ru/db/v8std/content/658/hdoc
- https://its.1c.ru/db/v8std/content/708/hdoc
- https://its.1c.ru/db/v8std/content/733/hdoc
- https://its.1c.ru/db/v8std/content/777/hdoc
- https://its.1c.ru/db/v8std/content/791/hdoc
