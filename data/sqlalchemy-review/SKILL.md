---
name: kit-sqlalchemy-review
description: Review Python code that uses SQLAlchemy (Core or ORM, sync or asyncio, including SQLModel) for correctness, safety, session and transaction handling, and performance, and report findings with severity and file locations. Use when asked to review database query code, repositories, models, or data-access changes in a project that uses SQLAlchemy. Do not use for projects without SQLAlchemy, for writing migrations or new queries (use kit-database-design or kit-feature-implementation), or for general code review; this skill reports and does not edit code.
---

# SQLAlchemy review

Report findings without modifying code unless the user asks for fixes.

## 1. Understand the models and conventions

- Find the engine and session setup (`sessionmaker`, `async_sessionmaker`, `expire_on_commit`), the declarative models, relationships and their `lazy` settings, and whether the code uses 2.0-style `select()` or the legacy `Query` API.
- Note how sessions are scoped (per request through a dependency, a context manager, or a global), how transactions are committed, and how errors are handled.
- Read Alembic migrations or model constraints when uniqueness or indexing matters.

## 2. Check each query

**Correctness**

- `update()` and `delete()` without `where`, and `session.query(...).delete()` without a filter, affect every row. Flag them unless that is clearly intended.
- `scalar_one()` raises when nothing or more than one row matches, `scalar_one_or_none()` returns `None` for no rows but raises for several, `session.get()` returns `None`, and `first()` silently drops extra rows. Check the result handling matches the intent.
- Pagination needs a deterministic `order_by`. Bulk `update()`/`delete()` statements bypass per-object ORM events and relationship cascades; loaded objects go stale only with `synchronize_session=False` or legacy `Query` code that sets it.

**Safety**

- `text()` with bound parameters (`:name`) is parameterized. f-strings, `%` formatting, or `.format()` inside `text()`, `literal_column()`, or `exec_driver_sql()` are injection: require bound parameters or an allowlist for identifiers.
- Check authorization filters (tenant or owner IDs) are present on every query that needs them.

**Sessions and transactions**

- One session per request or unit of work; never share a session across threads or concurrent tasks. Sessions must be closed (`with Session() as s:` or the dependency's `finally`).
- Writes need a commit inside `session.begin()` or an explicit `commit()`, with rollback on error. Flag commits inside loops and slow external calls while a transaction is open.
- In asyncio code, accessing an unloaded lazy relationship raises `MissingGreenlet`; require `selectinload`/`joinedload` or `AsyncAttrs`. Accessing attributes after commit with `expire_on_commit=True` triggers a reload or fails once the session is closed.

**Performance**

- Accessing relationships in a loop (N+1) should use `selectinload` or `joinedload`, or one query with `in_(ids)`.
- Select only needed columns for large rows, check that filters and sort columns are indexed, and flag a flush or commit per row; for many rows use `session.execute(insert(Model), rows)` or `add_all()` with one flush.

## 3. Verify and report

Confirm each finding by reading the query, the models, and its callers; run the project's tests or type checker when available. Report findings ordered by severity (critical, high, medium, low) with `file:line`, the problem, a concrete scenario, and a fix. If there are no findings, say so and list what was checked.

## Examples

- Use: "Review the queries in app/repositories/orders.py." "Check this service for SQLAlchemy session mistakes."
- Skip: "Write an Alembic migration that adds a status column." "Review this Django ORM query." "Add an endpoint that lists orders."
