---
name: navkit-database
description: The one SQLite database (navkit/database.py) -- DATABASE, Database.open/transaction/execute, Model/Field/Index/Query, model documents in .nml (`field`/`index`/`unique` lines, navml/model.py), the `_navml_schema` fingerprints and lazy per-model migration, navml/models/ (HistoryEntry), HISTORY persisted, --database and $XDG_STATE_HOME/navigator/navigator.db. Use when adding a table, querying one from a handler, changing a model's fields, or debugging what the database file holds.
---

# The database

One SQLite file, `$XDG_STATE_HOME/navigator/navigator.db` (else `~/.local/state/navigator/navigator.db`;
`--database PATH` for one session), holding what Navigator remembers that is not a setting. `navkit/database.py` is
stdlib only and knows nothing of navml or widgets. `DATABASE` is the one instance, like `SETTINGS` and `HISTORY`.

## Declaring a table

A model is a `.nml` document whose root extends `Model`, in a component directory under a registered library
(`navml/models/`, `navigator/models/`). A root may also extend a plain-Python `Model` subclass that declares no
fields but carries shared behaviour: `ViewRecord` and `EditRecord` extend `navigator/models/file_record.py`'s
`FileRecord`, which provides DN's eviction (at `interface.history_size` records rather than DN's 20), pinning and reordering. It follows the usual two-halves rules (`navml-components`): the
hand-written `.py` adds methods, and its class says `class HistoryEntry(Model)`.

```
from navkit.database import Model

#: One remembered input-line string.
HistoryEntry(Model):
    table: "history"                 # default: the class name in snake_case
    field list_id: str               # no default: the type's empty value ("", 0, 0.0, False, b"")
    field pinned: bool = False       # a default is a literal: it is the SQL DEFAULT too
    field at: datetime | None        # datetime and Path have no empty value: nullable, or say a default
    unique entry: list_id, text      # index names are prefixed with the table's in SQL
    index by_list: list_id, seq
    dropped: "old_column"            # the only way a column is ever removed
```

- **A document with a `field` line is a model document** (`navml.model.is_model`). `build.compile_document` branches
  to `navml/model.py`, which resolves, checks, generates and stubs it. Children, handlers, `style:`, `keys:`, `id`,
  `property`/`alias`/`event` lines are refused. So are a field named `id` and an index over an unknown field.
- Types: `str int float bool bytes datetime Path` (`CODECS`). A new type is a new codec.
- **Every field has a default**, and checks enforce it. That is what makes downgrades safe; see below.
- **After editing a model's `.nml`, rebuild** (`./venv/bin/python -m navml build navkit navml navigator`). The generated
  `__schema__` changes, so `--check` flags a schema change like any other stale markup.

## Using it from a handler

The model's class is the whole API. There is no session or connection to pass around.

```python
HistoryEntry.where(list_id="copy").order("-seq").limit(20).all()
HistoryEntry.where(seq__lt=5, text__like="/home%").values("text")
HistoryEntry.get(list_id="copy", text=path)          # one row or None
HistoryEntry.create(list_id="copy", text=path)       # .id filled in
HistoryEntry.upsert(list_id="copy", text=path, seq=9)  # needs a unique index its values cover; other fields keep theirs
HistoryEntry.where(list_id="copy").update(pinned=True); ...delete()
row.save(); row.delete()
with DATABASE.transaction(): ...                     # BEGIN IMMEDIATE; nested = savepoint
DATABASE.execute(sql, params)                        # the way out
```

Operators are `eq ne lt le gt ge like in`, and `None` compares with `IS`. Names are checked against the model, and
every value is a parameter.

## The schema is examined only when it changed

- The build computes `__ddl__` (`ddl_for`) and `__schema__` (`fingerprint`, sha256[:16]). The run time never derives
  them.
- `Database.open()` reads the whole of `_navml_schema(name, schema, migrated)` into a dict. A model's first touch
  (`Database.ensure`) compares its fingerprint with the dict: on a match it does nothing else and is cached in
  `_ensured` for the rest of the process. **A file that is up to date gets no `PRAGMA table_info` at all**; the
  tests assert this with `set_trace_callback`.
- On a mismatch it migrates under `BEGIN IMMEDIATE`, reading the row again under the lock so the second of two
  processes does nothing. **The diff is against the live table**:
  - a missing table is created;
  - a missing column becomes `ADD COLUMN`;
  - the indexes are dropped and recreated;
  - a changed column definition, or a `dropped:` one, rebuilds the table (create `x__navml_new`, copy the common
    columns, drop, rename).
- **A column the model does not mention is kept**, carried over by a rebuild too. Together with defaults everywhere,
  that lets an older Navigator write rows to a newer file. Flip-flopping between two versions only recreates indexes.
- **A rollback of an outermost transaction re-reads `_navml_schema` and clears `_ensured`**, because a migration that
  ran inside it as a savepoint was undone with it.

## Rules

- `main()` opens the file (`open_database()`, beside `load_settings()`). `Navigator.__init__` never does. A file that
  cannot be opened prints `nav: ...` and falls back to `:memory:`.
- Tests get a fresh `:memory:` database per test (`_fresh_database` in `tests/conftest.py`). A test that needs a file
  calls `DATABASE.open(tmp_path / "x.db")`, and reopening the same path simulates a restart.
- Writes are synchronous on the loop and autocommit per call: small and bounded, in WAL mode. Bulk work goes to
  `asyncio.to_thread` like file operations, and needs a connection of its own (not built yet).
- **The one connection is shared across threads** (`check_same_thread=False`; profiles and recent links are written
  through `asyncio.to_thread`), so `transaction()` holds an `RLock`: another thread's waits instead of nesting as a
  savepoint in it. Nesting is counted per holder (`_depth`), not read off `in_transaction`, which saw the other
  thread's and failed with *no such savepoint* once that one committed (`test_s3.py`, CI on 3.13).
- **Departure from DN**: DN wrote `DN.HIS` on exit (`SaveHistories`, `DNUTIL.PAS`). Each history change is written
  as it happens, so a crash loses nothing.

## History times

`HistoryEntry`, `ViewRecord` and `EditRecord` keep `used` (`time.time()` when last put at the front; 0 for a row
from before the column) -- what the history lists' tooltips say (`country.last_used`). Set wherever `seq` is
bumped (`HistoryEntry.remember`, `FileRecord.store`); `swap` leaves it.

## Read when

| Reference | Read when |
|---|---|
| `reference/why-this-design.md` | why our own layer over SQLAlchemy/peewee, why per-model fingerprints over `user_version`, the downgrade rule |
