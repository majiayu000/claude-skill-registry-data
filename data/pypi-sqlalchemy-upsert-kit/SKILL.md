---
name: pypi-sqlalchemy_upsert_kit
description: "Python library sqlalchemy_upsert_kit (v0.3.1): bulk upsert of a list of dicts into a SQLAlchemy Core table on SQLite, PostgreSQL or MySQL, staged through a temporary table and written with one INSERT ... ON CONFLICT (ON DUPLICATE KEY UPDATE on MySQL). Public API: api.sqlite, api.postgres and api.mysql, each with insert_or_ignore, insert_or_replace, insert_or_merge."
---

# sqlalchemy_upsert_kit

Bulk upsert for SQLAlchemy 2.0 Core tables. You pass an engine, a `sa.Table` with exactly one primary key column, and a list of records (dicts keyed by column key). The library loads them into a temporary staging table, then writes them with one native `INSERT ... SELECT ... ON CONFLICT (<pk>)` statement (`ON DUPLICATE KEY UPDATE` on MySQL). Three strategies decide what happens to rows whose primary key already exists. SQLite, PostgreSQL and MySQL have the same three functions with the same signatures and the same results.

Install: `pip install sqlalchemy-upsert-kit` (SQLite), `pip install "sqlalchemy-upsert-kit[postgres]"` (adds the psycopg 3 driver), or `pip install "sqlalchemy-upsert-kit[mysql]"` (adds PyMySQL). Needs Python 3.11+, SQLAlchemy 2.0.28+, SQLite 3.24+, MySQL 8.0+. PostgreSQL support starts at 0.2.1, MySQL at 0.3.1.

## Import

```python
from sqlalchemy_upsert_kit.api import sqlite      # or: postgres, mysql
import sqlalchemy_upsert_kit.api as sqlalchemy_upsert_kit  # then sqlalchemy_upsert_kit.sqlite.insert_or_ignore
```

Pick the module that matches the engine's database: `sqlite.*` for SQLite, `postgres.*` for PostgreSQL (`postgresql+psycopg://`), `mysql.*` for MySQL (`mysql+pymysql://`).

## Public API

Each of `sqlite`, `postgres` and `mysql` exports the same three functions:

- `insert_or_ignore(engine, table, values, metadata=None, temp_table_name=None, conn=None, trans=None) -> tuple[int, int]`: insert new rows; leave existing rows untouched. Returns `(ignored_rows, inserted_rows)`.
- `insert_or_replace(engine, table, values, metadata=None, temp_table_name=None, conn=None, trans=None) -> tuple[int, int]`: insert new rows; overwrite existing rows so they equal the record. **Columns the records leave out are reset to their default or NULL.** Returns `(replaced_rows, inserted_rows)`.
- `insert_or_merge(engine, table, values, columns, metadata=None, temp_table_name=None, conn=None, trans=None) -> tuple[int, int]`: insert new rows; on existing rows update only `columns` (`list[str]` of column keys) and keep every other column. Returns `(updated_rows, inserted_rows)`.

Types: `engine: sa.Engine`, `table: sa.Table`, `values: list[dict[str, Any]]`, `metadata: sa.MetaData | None`, `temp_table_name: str | None`, `conn: sa.Connection | None`, `trans: sa.Transaction | None`. The two counts always add up to `len(values)`.

## Example

```python
import sqlalchemy as sa
from sqlalchemy_upsert_kit.api import sqlite

metadata = sa.MetaData()
t_record = sa.Table(
    "records", metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(50)),
    sa.Column("note", sa.String(50)),
)
engine = sa.create_engine("sqlite:///app.db")
metadata.create_all(engine)
# existing rows: (1, "a", "n1"), (2, "b", "n2"), (3, "c", "n3")

values = [
    {"id": 3, "name": "C", "note": "N3"},
    {"id": 4, "name": "d", "note": "n4"},
    {"id": 2, "name": "B", "note": "N2"},
]
# each line below starts from those rows:
sqlite.insert_or_ignore(engine, t_record, values)    # (2, 1): 2, 3 unchanged; 4 added
sqlite.insert_or_replace(engine, t_record, values)   # (2, 1): 2 -> (B, N2), 3 -> (C, N3)
sqlite.insert_or_merge(engine, t_record, values, columns=["name"])  # (2, 1): 2 -> (B, n2)
```

## Transactions

- **Auto-managed** (default, `conn` and `trans` both None): the call opens a connection, runs in its own transaction, and commits.
- **User-managed** (pass both `conn` and `trans`): the call runs inside your transaction; you commit or roll back. Passing only one of them raises `ValueError`.

```python
with engine.connect() as conn:
    with conn.begin() as trans:
        conn.execute(other_table.insert(), rows)
        postgres.insert_or_merge(engine, t_record, values, columns=["name"], conn=conn, trans=trans)
```

- A failure undoes everything the call did and leaves no staging table. In user-managed mode it undoes **only** the call: your earlier writes stay, and the transaction stays usable (retry, then commit).
- A rollback of your transaction after a successful call undoes the upsert.

## Rules for `values` (else `ValueError`, before any SQL runs)

- Every record has the same keys, and each key is a writable column key of `table` (not a `Computed` column).
- Every record has the primary key, not None, and no two records share one.
- `table` has exactly one primary key column (composite keys are not supported).
- `insert_or_merge`: `columns` is not empty, and each entry is a column key that the records have.
- `temp_table_name`, if given, is not the target table's name.
- Empty `values` is a no-op that returns `(0, 0)`.

## Gotchas

- Keys are SQLAlchemy column **keys** (`sa.Column("Code", ..., key="code")` is written as `"code"`).
- Existing rows are updated in place: update triggers fire; delete triggers and `ON DELETE CASCADE` never do.
- A record that breaks a unique key **other than** the primary key (an existing row's value, or another record's) raises `sqlalchemy.exc.IntegrityError` and the call changes nothing, on every backend. On MySQL the library enforces this itself (`err.orig` is `sqlalchemy_upsert_kit.exc.UniqueKeyConflictError`), since `ON DUPLICATE KEY UPDATE` would silently update the other row.
- Concurrent calls are safe; on SQLite they wait for each other's write lock (up to the driver's busy timeout).
- On PostgreSQL and MySQL, under concurrent writes to the same keys, the split between the two counts can be off; the sum and the rows are always right.
- MySQL: `insert_or_ignore` fires `UPDATE` triggers on ignored rows (no-op update, no `DO NOTHING`); keys compare by collation, so `'a'` and `'A'` are the same key by default.
- Supported drivers: `sqlite3` (stdlib), psycopg 3, PyMySQL. Not supported: async engines, MariaDB.

## More detail

For full API docs see `ref/public-api.md`.
