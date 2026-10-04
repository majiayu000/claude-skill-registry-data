---
name: tool-mdb-reader
description: Read Microsoft Access databases (.mdb/.accdb) read-only — info, schema, one table, ad-hoc SELECT, keyword search across all tables, or full-dump every row to a greppable markdown file. Use when the user says "read this mdb", "what's in this Access database", "dump the mdb tables", "query this .accdb", or hands over an Access file from a legacy engineering tool (CYMCAP, ETAP, plant databases). NOT for writing to an Access DB (this tool refuses non-SELECT), and NOT for CSV/XLSX (use the markitdown read provider).
---

# Access MDB Reader Skill

Read `.mdb` / `.accdb` databases. Two modes, mirroring `tool-pdf-reader` and `tool-chm-reader`: **stdout** (info / schema / one table / a SELECT / a search — read as you go) and **full-dump to a markdown file** (token-cheap, re-readable via Read/Grep in this and future sessions).

**Read-only by construction.** Opens with ADO `Mode=1` (adModeRead) and refuses any statement that isn't a `SELECT`. It cannot modify a database.

`SKILL_DIR` below = this skill's directory (`skills/tool-mdb-reader/` in the repo, or `~/.claude/skills/tool-mdb-reader/`).

## Setup

Windows only. Needs **pywin32** (`pip install pywin32`) and the **Microsoft ACE OLEDB provider** (the Access Database Engine — already present on machines running Access-backed engineering tools).

Bitness must match: 64-bit Python needs 64-bit ACE. `pyodbc` is *not* used — the daemon interpreter doesn't have it, and ACE is reachable via COM without any install.

## Usage

### 1. Info — the first call

```bash
python "<SKILL_DIR>/mdb_tool.py" info "path/to/file.mdb"
```

Size, SHA-256, and every user table with row + column counts.

### 2. Schema

```bash
python "<SKILL_DIR>/mdb_tool.py" schema "file.mdb"                 # all tables
python "<SKILL_DIR>/mdb_tool.py" schema "file.mdb" --table CABLES  # one
```

Column names + ADO types (`Double`, `VarWChar`, `SmallInt`, …).

### 3. One table to stdout

```bash
python "<SKILL_DIR>/mdb_tool.py" table "file.mdb" SETTINGS
```

### 4. Ad-hoc SELECT

```bash
python "<SKILL_DIR>/mdb_tool.py" query "file.mdb" "SELECT CODTAB, IFVAL FROM [DEFTAB] WHERE CODTAB='INSU'"
```

Anything not starting with `SELECT` is refused. Bracket table names (`[DEFTAB]`) — Access needs it for names that collide with keywords.

### 5. Search every table

```bash
python "<SKILL_DIR>/mdb_tool.py" search "file.mdb" "jute" --limit 20
```

Case-insensitive across all columns of all tables; prints the matching rows with their 1-based row index.

### 6. Dump everything to markdown (token-saver)

```bash
python "<SKILL_DIR>/mdb_tool.py" dump "file.mdb" "path/to/output.md"
```

Every row of every table, a summary table with anchor links, per-table schema lines, and a SHA-256 of the source. Single-column text tables (report templates) render as fenced blocks rather than mangled markdown tables.

- **Use when** the database will be referenced more than once: dump once, then `Read`/`Grep` the `.md`.
- For a vault MDB, dump beside it as `<name>-extracted.md` (matches the `*-extracted` convention from the PDF/CHM skills).
- A 236 KB / 9-table / 493-row database dumps to ~24 KB of markdown in a second.

## Two source-fidelity decisions (know these before trusting a dump)

Both are **safe for reading and wrong for a write path**:

1. **Doubles render at 15 significant digits.** The stored doubles carry IEEE-754 round-trip noise — a cell Access displays as `13.3` reads back through COM as `13.299999999999999`. Rendering `repr()` makes the dump unreadable *and* breaks a grep for the value the user actually knows. `.15g` matches what Access and the owning application show. **If you need bit-exact doubles, read the MDB, not the dump.**
2. **Trailing NUL record-padding is stripped.** Some tools pad fixed-width records with NUL bytes. `str.rstrip()` will not remove them (NUL isn't whitespace), and a single such row makes the entire output file "binary" to grep — defeating the whole point. An *interior* NUL (never yet seen) becomes a visible `␀` rather than vanishing silently.

The dump's header states both, so a reader who didn't invoke the tool still knows.

## Workflow for a legacy engineering database

1. `info` — how many tables, how big.
2. `schema` — column names + types; spot the lookup tables vs the data tables.
3. `dump` to a sibling `*-extracted.md` — the durable artifact.
4. `search` / `query` for specific values; Read/Grep the `.md` for everything else.

## Notes

- Access exposes no foreign keys in many legacy files — relationships are usually inferred from the data, not declared. Don't assume the schema tells you the joins.
- Table names with spaces work (`[My Table]`); the dump's anchor links slugify them.
- This tool never writes. For a write path, the database's owning app is the right tool — Access rewrites index/catalog structures that a naive writer will corrupt.

## Trigger phrases

| User says | Action |
|-----------|--------|
| "read this mdb" / "what's in this Access db" | `info` → `schema` → `dump` |
| "dump the mdb tables" / "save it as markdown" | `dump` to sibling `*-extracted.md` |
| "search the db for X" | `search` |
| "how many X in the database" | `query` with a SELECT |
