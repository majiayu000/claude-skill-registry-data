---
name: padosoft-laravel-conventions
description: >-
  Use this skill when writing or reviewing Laravel/PHP code — a controller, a FormRequest, a service, a job,
  a migration, an Eloquent query, a model event, a queued or bulk operation — and whenever a symptom shows
  up: a controller that grew into the business logic, an N+1 found in the logs, a bulk command that runs out
  of memory, a job that retries something it should not, a soft-deleted row reappearing in a count, a model
  event that fires on a mass update and does not. It applies to any Laravel version: the rules are about the
  shape of the application. Do not use it for a security review (padosoft-laravel-security-review),
  for what goes in a log (padosoft-logging-discipline), or for infrastructure and deployment.
license: MIT
compatibility: >-
  Any Laravel version. The rules are about how an application is shaped, not about framework features;
  where a version moved a file rather than changing a rule, the text says so.
metadata:
  version: 0.4.0
  author: Padosoft
  summary: Where the logic lives and what crosses which boundary, on any framework version.
  profiles: laravel
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: laravel, php, eloquent, service, dto, job, queue, migration, n+1, architecture
---

# Laravel conventions

**None of this depends on a framework or language version.** These are rules about how the application is
shaped — where the logic lives, what crosses a boundary, what the database is asked to do — and they were
earned on codebases several major versions apart. A rule that only held on one version would not be a rule,
it would be a release note.

For a **new** project, start from the current Laravel and PHP, a formatter and a static analyser, and the
test framework the repository already chose. On an **existing** codebase apply the same rules with that
project's idiom, and do not mix a new idiom with the legacy one halfway through a file — a file that does
both is harder to read than a file that is consistently old.

Where a version genuinely moved something it is noted inline. In every one of those cases what moved was the
*file*, not the rule.

---

## 1. The flow: FormRequest → DTO → Service → Resource

For any endpoint or form that is not trivial:

1. **`FormRequest`** validates and normalises the HTTP input;
2. the **controller** builds an explicit **DTO**;
3. the **service** (or action) runs the application logic;
4. the **controller** turns the outcome into a response, redirect or `JsonResource`.

What each step buys: the data contract stops being an untyped array crossing boundaries, the service is
testable without HTTP, and the controller has one job — translating.

**The controller never contains business logic.** The signal it has drifted: it queries, it decides, it
formats. Two of the three belong elsewhere.

Never pass `$request->all()` down: pass `validated()`, or better the DTO. An array that "came from the
request" has no shape anyone can rely on three files later.

## 2. Long or asynchronous work: DTO → Service → Job

- **DTO / value object** for the input;
- **service / action** for the logic;
- **job** for queued execution.

**The job orchestrates, it does not implement.** Retry, timeout, backoff and execution context live in the
job; the reusable logic lives in the service, so it can be called synchronously by a command or a test.

In a job, distinguish a **retryable** error from a **permanent** one. Retrying a validation failure burns the
queue; not retrying a timeout loses work. A permanent failure fails the job explicitly rather than throwing
something the queue will retry sixteen times.

## 3. Structure

```
Domain/<Module>/
├── Dto/                 explicit inputs
├── Http/Requests/       HTTP validation
├── Http/Controllers/
├── Services/  (or Actions/)
├── Jobs/
└── Routes/              if the module exposes its own endpoints
```

Symmetrical directories: controller, request, service and **test** follow each other. No bin directories —
`misc`, `common`, `utils`, `various` — and no omnivorous generic service. When a folder stops having one
responsibility, split it.

## 4. Eloquent and queries

- **N+1**: eager load, or write a dedicated query. It is the single most common performance defect, and it
  only shows up with production-sized data.
- Need one value? Do not hydrate a whole model — `value()`, `pluck()`, an aggregate.
- **Never `select *`** on a critical query over a large dataset.
- Before micro-optimising, **measure**: cardinality and the execution plan. An index added by intuition is
  often an index that is never used.
- **`chunkById` or `cursor` for bulk**, never `get()` followed by filtering in PHP. And push the filter into
  SQL: `whereNotIn` with chunked arrays beats loading everything and rejecting it in memory.
- **Soft deletes**: a query that must ignore them says so explicitly. A count that silently includes trashed
  rows is a number nobody can reproduce.

`chunkById` and not `chunk` when the loop **modifies** the rows it iterates: `chunk` pages by offset, so
updating rows shifts the window and silently skips records.

## 4b. Put the query language in a builder layer, not in scopes

Model scopes spread query logic across the model, the controller and whatever else reached for it. A
dedicated query-builder class per aggregate keeps it in one place and makes it composable. The convention
that makes such a layer survive a few hundred classes:

| Kind of method | Returns | Named |
|---|---|---|
| Building block | the builder itself, chainable | `whereX()`, `ifWhereX()` (conditional), `joinX()`, `orderByX()`, `withX()` |
| Composition | the builder | a domain phrase: `visibleInCatalogue()`, built **only** by chaining building blocks |
| Complete query | a collection, a model, a paginator, a count | `getX()`, `paginateX()`, `countX()` |

Three prohibitions, and they are what keeps the layer honest:

- **No ambient state inside a builder.** Reading the current tenant, locale or a global setting from inside
  a `where` makes the method untestable and its result dependent on something the caller cannot see. Take
  it as a parameter.
- **No side effects.** A builder builds queries: no state changes, no mail, no dispatch, no API calls.
- **No scopes on the models**, once the layer exists. Two places to look is worse than either one.

When a builder passes roughly a hundred methods, split it by domain into traits — a few dozen methods each,
a handful of traits — rather than letting one class grow past reading size.

**Check for an existing helper before writing query logic by hand.** A project that has accumulated
conditional-clause and formatting helpers has them precisely so the same chain is not re-implemented with a
subtly different edge case; and when the logic is reusable and the helper does not exist, the move is to add
it, not to inline it for the third time.

## 5. Migrations and schema

- One table, one responsibility. No column encoding two concepts.
- Indexes follow the **real read patterns**: if a hot query filters and sorts on the same fields, model the
  index on that.
- Think about cardinality, unique constraints and nullability deliberately — nullable by default is a
  decision nobody made.
- Foreign keys where the stack allows them.
- Derived or denormalised data: **document the source of truth** next to it, or the copy becomes the truth by
  accident.
- Index selection, partitioning, JSON columns and the guard clauses that make a migration re-runnable
  against a schema that does not match the ledger: **`padosoft-database-design`**.
- A migration is run once on production and lives forever in the history: make it idempotent where the
  project's convention requires it, and never edit one that has shipped.

## 6. Model events

They fire on **model** operations, not on query-builder mass operations: `Model::where(...)->update([...])`
does **not** fire `updating`/`updated`. That asymmetry is the bug — a rule enforced in an event silently does
not apply to the bulk path.

So: either the invariant lives somewhere both paths cross (a database constraint, an observer plus an
explicit call on the bulk path), or the bulk path is banned for that table and the ban is written down.

An event that dispatches a job must not assume the transaction committed: use the after-commit dispatch, or
the job runs against a row that is not there yet.

## 7. Types, null and errors

- **Type hints everywhere**: parameters, return types, properties. Whatever the language version allows,
  use all of it — an untyped boundary is where the null gets in.
- Prefer an explicit object to a "magic" helper when it makes the contract clearer.
- **Do not use exceptions for expected user-validation flows** — that is what validation is for. Exceptions
  are for what should not happen.
- Translate infrastructure errors into application-level messages; what may and may not appear in them is in
  **`padosoft-laravel-security-review`** (`SEC-ERRLEAK-001`), and what goes in the log is in
  **`padosoft-logging-discipline`**.
- Null safety: a nullable that reaches a calculation makes a wrong number, not a crash. Decide at the
  boundary — reject it, default it, or make the type non-nullable — never three files downstream.

### The null-safety specifics that keep recurring

- **A find that returns null, followed by a property access.** Either use the failing variant when absence
  is a 404, or return early — never let the next line deal with it.
- **A chain of two calls where one is optional.** Use the null-safe operator with an explicit default, or
  assign to a variable and check it. The return type declares whether it can be null; read it.
- **Loose equality with null, zero or the empty string** is a coin toss: the type juggling makes several of
  them equal to each other. Compare strictly, and cast deliberately when a legacy value really is a string.
- **A date parser given null returns "now"** in more than one library. That is not a crash, it is a wrong
  value that looks plausible for exactly as long as it takes to reach a customer.


Three more that keep a package honest:

- **Make the illegal state unrepresentable.** When two fields are only valid together — a blocked verdict
  with no reason, an accepted amount with no currency — make the constructor private and expose named
  constructors for the valid combinations. A validation rule can be forgotten; a constructor that does not
  exist cannot be called.
- **A misconfiguration that opens a surface fails at boot.** Warn when a feature is enabled and still
  resolves to its no-op implementation; **throw** when something is exposed with an empty guard list. The
  difference is whether the wrong configuration is merely useless or actively unsafe.
- **Routes shipped by a package default to the stateless middleware group**, not the session one, which may
  not even be registered in the host's test context. Put authentication on the privileged routes and let
  the application add the session group where sessions exist.

Changing a signature or a return type in a hierarchy is its own procedure: **`padosoft-contract-changes`**.
Deciding a branch by environment name is another: **`padosoft-environment-gating`**.

## 8. Code shape

Guard clauses and early return; avoid `else` when a return makes the flow obvious. Small methods, one main
responsibility. Complex branches move into private methods or dedicated services. Comment decisions,
constraints and trade-offs — not the obvious.


Four more, and the first one is the one people argue about:

- **A variable holding a database field keeps the field's name.** Renaming it on the way in breaks the only
  link between the row and the code, and makes the search that would have found every use return nothing.
  Add a suffix when the variable means something narrower than the column, and keep the column's spelling
  underneath it. Free naming is for values that are not a field.
- **Display formatting has one home.** A presenter, a view model, a formatter — the name matters less than
  the fact that there is exactly one, and that neither the model nor the template formats anything itself.
  Otherwise the same value is rendered three ways in three screens and nobody can say which is right.
- **Settings are a namespace, not a flat bag.** One root prefix, then area, then parameter; and a
  convention in the name that says what kind of setting it is — a toggle reads as a toggle. A flat list of
  a few hundred keys is a list nobody greps successfully.
- **Directory and file naming is a convention, so it is one convention.** Two spellings in the same tree
  means every path is a guess, and on a case-insensitive filesystem it also means it works locally and
  fails on the server.

Anti-patterns, in the order they appear: a 150-line method with several responsibilities; business logic
mixed with I/O or rendering; a boolean flag that changes what a method fundamentally does; names like `data`,
`tmp`, `manager`, `utils` with no context.

## 9. Files and storage

Streams and chunks for large files, never the whole thing in memory. Validate type, size and destination
**before** copying. No whole-export concatenation in RAM. Clean up temporary files and intermediate
artefacts — including on the failure path, which is where they accumulate.

---

## 10. Failed jobs are a subsystem, not a table

A job that exhausts its retries and lands in the failed table has failed **silently** unless something
notices. Give every job a common base that, on final failure, notifies — with the retry count and the
backoff as declared properties, and recipients and templates overridable per job for the ones that matter.

The question to answer for each job: **who finds out, and how long after?** If the answer is "whoever
happens to look at the dashboard", it is not a subsystem. See **`padosoft-failure-visibility`** and
**`padosoft-durable-effects`**.

## Gotchas

- **`chunk` while updating skips rows.** Use `chunkById`.
- **Mass updates bypass model events** (§6), and so do mass deletes and `upsert`.
- **A `FormRequest` validating does not make `all()` safe**: it returns everything that was sent.
- **Eager loading inside a loop is still N+1**, just harder to see.
- **An index on a low-cardinality column often does nothing**; measure before adding.
- **A job retried after a partial write repeats the write.** Idempotency is designed in, not hoped for.
- **`dd()` and `dump()` in committed code** — see `padosoft-logging-discipline` §3, and do not delete
  someone else's silently: report it.

## Checklist

- [ ] Controller translates; logic in the service; DTO across boundaries
- [ ] Job orchestrates, service implements; retryable vs permanent distinguished
- [ ] No N+1; no `select *` on hot paths; bulk through `chunkById`/`cursor` with filters in SQL
- [ ] Soft-delete intent explicit in queries that care
- [ ] Migration: responsibility, indexes on real patterns, nullability decided, source of truth documented
- [ ] Bulk paths that bypass model events identified and handled
- [ ] Full type hints; nullability resolved at the boundary
- [ ] Pint and static analysis clean

## Final report

```
Change: <what>  ·  Laravel <version> / PHP <version>
Flow: FormRequest <file> → DTO <file> → Service <file> → Resource <file>
Queries: N+1 checked | bulk strategy <chunkById|cursor|none needed>
Migration: <yes/no — indexes, nullability, source of truth>
Model events: bulk path <not used | handled how>
Pint / static analysis: PASS | FAIL <detail>
```
