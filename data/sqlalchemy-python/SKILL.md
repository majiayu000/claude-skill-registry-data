---
name: sqlalchemy-python
description: >-
  Use for writing, reviewing, debugging, migrating, or testing SQLAlchemy 2.x
  Core or ORM code involving Engine, Connection, Session, mapped models,
  select statements, transactions, pooling, results, loading, or AsyncSession.
  Do not use for raw database SQL with no SQLAlchemy boundary, Alembic migration
  design, DuckDB relations, or database administration.
argument-hint: "[Core or ORM task, transaction ownership, database, and scale]"
---

# SQLAlchemy resource and transaction ownership

| Object | Owns | Rule |
|---|---|---|
| `Engine` | Dialect plus connection pool | Create at application scope; it is not an active transaction. |
| `Connection` | Checked-out DBAPI connection and Core transaction state | Scope with a context manager; commit or roll back explicitly. |
| `Session` | ORM identity map and one logical transaction | One unit of work; never a global cache or cross-task singleton. |
| `Result` | Cursor-backed rows until consumed/closed | Consume inside the owning connection/session scope unless materialized. |

## Workflow

1. Inspect SQLAlchemy, driver, dialect, sync/async mode, transaction boundary,
   expected concurrency, isolation, and data volume.
2. Choose Core for explicit relational statements and bulk/data-oriented work;
   choose ORM when identity, relationships, and unit-of-work behavior are part
   of the domain model. Both use 2.x `select()` and transaction semantics.
3. Create Engine/AsyncEngine once per configured database role. Inject a
   connection or session factory; create one Session/AsyncSession per request,
   job, or unit of work.
4. Use `with engine.begin() as connection:` or `with Session.begin() as
   session:` when the block should commit on success and roll back on error.
   Do not confuse `flush()` with commit.
5. Compose values with SQLAlchemy expressions and bound parameters. Never use
   string interpolation for untrusted values or dynamic identifiers.
6. Define relationship loading deliberately. Detect N+1 access and detached
   lazy loads; use joined/select-in loading according to cardinality and result
   multiplication.
7. Test rollback, uniqueness/integrity errors, transaction visibility,
   generated SQL/parameters when relevant, and backend-specific behavior.

## Concurrency and async

`Session` and `AsyncSession` are mutable transactional objects. Do not share one
instance across threads or concurrent tasks. AsyncSession is a proxy over the
same stateful session model; use one per task and an async driver. Do not mix
sync driver calls into the event loop.

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

engine = create_engine(url)


def load_user(user_id: int) -> User | None:
    with Session(engine) as session:
        return session.scalar(select(User).where(User.id == user_id))
```

If the returned mapped object will be used after Session close, ensure required
attributes are loaded and understand expiration/detachment. Read [Core and ORM
decisions](references/objects.md), [transactions and concurrency](references/transactions.md),
and [query verification](references/testing.md).
