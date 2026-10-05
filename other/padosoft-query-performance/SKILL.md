---
name: padosoft-query-performance
description: >-
  Use this skill when writing or reviewing code that reads or writes the database in volume — a listing, an
  export, a report, a cron or queued job that walks a table, a recalculation of a denormalised table, an
  endpoint that got slow as the data grew. Also when the user reports N+1 queries, a job exhausting memory,
  a paginated page that gets slower the deeper it goes, a timeout on a large table, or asks how to process
  a few hundred thousand rows. It covers access patterns, the volume thresholds that change the technique,
  keyset pagination, existence checks, and recalculating without leaving a window of emptiness. Do not use
  it for index and table design (padosoft-database-design) or for tuning the server itself.
license: MIT
compatibility: >-
  Examples use Eloquent and the Laravel query builder; the thresholds and the access patterns apply to any
  ORM over a relational database.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The code was written against the volume that existed then, and the volume moved.
  profiles: data, laravel
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: n+1, pagination, chunk, cursor, eager loading, performance, denormalization, cache, exists
---

# Query performance

Every rule here is about the same thing: **the code was written against the data volume that existed when it
was written**. It worked. The volume moved.

---

## 1. Never query inside a loop

| Need | Instead of a query per iteration |
|---|---|
| Check whether records exist | pluck the ids once, check membership in memory |
| Load a relation | eager-load it **outside** the loop |
| Count per group | one grouped aggregate query |
| Fetch by a list of ids | one `whereIn`, keyed by id |
| Insert many rows | collect and insert in batches — note that a bulk insert skips ORM events and timestamps |

A loop of five queries is fine in development and is five thousand in production.

## 2. Select the columns you need

```php
// ❌ every column, including the text blobs nobody asked for
Article::query()->where('brand_id', $id)->get();
// ✅
Article::query()->select(['id', 'name', 'price'])->where('brand_id', $id)->get();
```

Same inside eager loads — **and include the primary key and the foreign key**, or the relation cannot be
matched back and silently comes out empty:

```php
->with(['prices:id,article_id,price,discounted_price'])
```

## 3. The volume decides the technique

| Rows | Technique | When |
|---|---|---|
| under ~1 000 | load it all | it fits in memory |
| 1 000 – 100 000 | chunk with a callback | batch processing |
| 1 000 – 100 000, stable ids | **chunk by id** | cron and queued jobs — no offset drift when rows are modified mid-walk |
| any, read-only | a lazy collection | one record at a time |
| any, minimum footprint | a database cursor | streaming |

**For any job that walks a whole table: chunk by id, or stream. Never load it all.** The difference between
chunking by offset and chunking by id is correctness, not speed: if the walk modifies rows, offsets shift
and records are skipped.

## 4. Pagination that does not degrade

An offset makes the engine count and discard every preceding row, so page five hundred costs five hundred
pages of work.

| Case | Use |
|---|---|
| Infinite scroll, next/previous | **keyset pagination** — `WHERE id > ?`, no offset at all |
| Walking every page in a job | chunk by id |
| Jumping to an arbitrary page on a large table | deferred join: page the ids with the index, then join for the data |
| Arbitrary pages, small table | a plain offset is fine below roughly ten thousand rows |

## 5. Ask the cheapest question

- **Existence**: use an existence check, never a count compared to zero — one stops at the first match, the
  other counts everything.
- **A subquery returning many rows**: prefer a correlated existence check to a membership test — it stops at
  the first match instead of materialising the whole set.
- **One column of one row**: fetch the value directly rather than hydrating a whole model to read one field.
- **A large list of integers**: use the raw-integer form of the membership test where the ORM offers one;
  the generic version binds every value.
- **Distinct**: usually a sign the join is wrong. Fix the join, or group explicitly; a distinct scans and
  de-duplicates row by row.
- **Join order**: start from the table the `WHERE` actually restricts — the engine works from the smallest
  set outward.

## 6. Caching, deliberately

| Data | Strategy |
|---|---|
| Immutable within one request | a memoised static, reset at the end of the request — otherwise it leaks across requests in a long-running worker |
| Rarely changing (settings, lookup tables) | a long time-to-live |
| Invalidated by known events | tags, so the event can clear exactly its slice |

A request-scoped memo **must** be reset explicitly on request termination. In a classic request-per-process
model nothing notices; in a persistent worker it serves stale data to a different user.

Tags are not free: on some stores every tag adds a lookup on every read. Use them where invalidation
actually needs them.

## 7. Recalculating a denormalised table

Three rules, and the first one is the one that causes incidents:

- **Never truncate and rebuild.** The table is empty for the whole duration of the rebuild, and everything
  reading it sees nothing — not an error, *nothing*. Instead: delete the rows whose subject no longer
  qualifies, then fan out one job per subject.
- **Per-subject rebuild goes inside a transaction.** Delete plus insert without one leaves that subject
  empty if the job dies in between.
- **Bulk moves belong in the database.** An insert-from-select does in one statement what a read-modify-write
  loop does in thousands of round trips.

See **`padosoft-atomic-invariants`** for the general form, and **`padosoft-durable-effects`** for what the
fan-out needs to be safe.

## 8. Prove it at volume

A performance change verified on a development dataset is verified against the wrong question. If the change
is meant to hold at scale, the evidence comes from a dataset at that scale — the count, the timing, the
query count, before and after. See **`padosoft-evidence-boundaries`**.

---

## How to find it in a diff

```bash
# a query inside a loop
rg -n -B3 "foreach|for\s*\(|while\s*\(" --glob '*.php' -A6 | rg "::(where|find|first|get)\(|->get\(\)"
# count used as an existence check
rg -n "count\(\)\s*[><=!]+\s*0|->count\(\)\s*>\s*0"
# unbounded reads in jobs and commands
rg -n "->get\(\)|->all\(\)" app/Jobs/ app/Console/
# truncate on a cache or denormalised table
rg -n "->truncate\(\)|TRUNCATE TABLE"
# eager loads without a column list
rg -n "->with\(\s*\[?'[a-zA-Z]+'\s*[,\]\)]"
```

Every hit is a candidate; the volume decides whether it is a defect.

## Gotchas

- **Eager loading without the foreign key returns empty relations**, silently, and looks like missing data.
- **A bulk insert skips model events and timestamps.** Whatever those events did, does not happen.
- **Chunking while modifying the chunked set skips rows**, unless you chunk by id.
- **A memoised static in a persistent worker is a cross-request leak**, and it looks like a caching bug in
  someone else's code.
- **`SELECT *` is most expensive on the tables that have a text column**, which are exactly the tables
  somebody will select from in a loop.
- **The slow query is rarely the one in the trace.** It is the one that ran four hundred times.

## Checklist

- [ ] No query inside a loop
- [ ] Explicit column lists, including in eager loads, with the primary and foreign keys
- [ ] Volume technique matched to the expected row count; jobs chunk by id or stream
- [ ] Pagination: keyset or deferred join above ~10 000 rows
- [ ] Existence checks, not counts; direct value reads, not hydrated models
- [ ] No avoidable distinct; join order starts from the restricted set
- [ ] Caches have a stated invalidation; request-scoped memos reset on termination
- [ ] Recalculation: no truncate, per-subject transaction, bulk work pushed into SQL
- [ ] Measured at production-like volume, before and after

## Final report

```
Path: <endpoint / job / report>
Volume assumed: <rows>  ·  measured on: <dataset size>
Queries: <before> → <after>   ·   time: <before> → <after>   ·   peak memory: <…>
Technique: <chunk by id | keyset | deferred join | stream>
Cache: <what, ttl/tags, invalidation>
Recalculation: <fan-out, transaction boundary>
Still unbounded: none | <where>
```
