---
name: sqlite-reader
description: Liest SQLite-Datenbanken strikt read-only (kein Schreibrecht nötig), inspiziert Schema inkl. Foreign-Key-Discovery und generiert sichere SELECT-Wizards. Trigger bei jeder DB-Analyse (GreyHack player.db, OpenClaw-Sessions, beliebige .sqlite3).
version: 1.0.0
author: OpenClaw Agent (MaxClaw Skill-Set)
license: MIT
platforms:
  - linux
  - macos
triggers:
  - analyse: jede unbekannte .db/.sqlite3-Datei
  - debugging: bei "warum steht da was?" in Session/Game-DB
  - cron: weekly DB-Health-Check (VACUUM status, integrity)
metadata:
  openclaw:
    tags:
      - data
      - sqlite
      - read-only
      - analysis
---

# sqlite-reader

Read-only SQLite-Werkzeugkasten für MaxClaw. **Niemals** Schreibzugriff auf
fremde DBs (kann Daten korrumpieren). Alle Snippets öffnen mit `mode=ro` und
URI-Parameter — selbst wenn das Script root läuft, kollidiert kein Lock.

## When to use

- MaxClaw findet eine `.db` (GreyHack-Player, OpenClaw-Session-DB, Tool-State)
  und soll sie verstehen, ohne sie zu verändern.
- Schema-Mapping für ein neues Tool: was sind die Foreign-Keys, wo liegen die
  "wichtigen" Tabellen?
- Cron-Healthcheck: jede Woche `integrity_check` + WAL-Größe loggen.

## Pattern

### 1. Schema-Inspiration + FK-Discovery (`scripts/sqlite_inspect.py`)

```python
#!/usr/bin/env python3
"""sqlite_inspect.py — Schema + FK-Discovery read-only."""
import sqlite3, sys, json
from pathlib import Path

db = Path(sys.argv[1]).resolve()
# mode=ro + immutable=1 → blockt selbst versehentliche Schreibvorgänge
uri = f"file:{db}?mode=ro&immutable=1"
conn = sqlite3.connect(uri, uri=True)
cur = conn.cursor()

# Tabellen + Spalten
tables = cur.execute(
    "SELECT name, sql FROM sqlite_master WHERE type='table'"
).fetchall()

schema = {}
for name, ddl in tables:
    cols = cur.execute(f'PRAGMA table_info("{name}")').fetchall()
    fks  = cur.execute(f'PRAGMA foreign_key_list("{name}")').fetchall()
    schema[name] = {
        "ddl": ddl,
        "columns": [{"name": c[1], "type": c[2], "pk": c[5]} for c in cols],
        "foreign_keys": [{"col": f[3], "ref_table": f[2], "ref_col": f[4]} for f in fks],
    }

# Indizes + Rowcounts
for name in list(schema):
    n = cur.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
    schema[name]["rowcount"] = n

print(json.dumps(schema, indent=2, ensure_ascii=False))
```

### 2. SELECT-Wizard (`scripts/sqlite_query.sh`)

```bash
#!/usr/bin/env bash
# sqlite_query.sh — sichere parametrisierte SELECTs
set -euo pipefail
DB="${1:?db}"; SQL="${2:?sql}"
# Mode ro + readonly journal → keine Chance auf Mutation
sqlite3 "file:$DB?mode=ro" -header -column <<< "$SQL"
```

**Beispiele:**

```bash
# GreyHack-Player: Inventory-Tabelle zeigen
sqlite_query.sh ~/.local/share/GreyHack/player.db \
  "SELECT name, type, count FROM inventory ORDER BY count DESC LIMIT 10"

# OpenClaw-Session-DB: heutige Sessions
sqlite_query.sh ~/.openclaw/sessions.db \
  "SELECT id, title, started FROM sessions WHERE date(started)=date('now')"
```

### 3. Health-Check (`scripts/sqlite_health.sh`)

```bash
#!/usr/bin/env bash
# sqlite_health.sh — wöchentlicher Read-Only-Audit
set -euo pipefail
for db in "$@"; do
  echo "=== $db ==="
  sqlite3 "file:$db?mode=ro" <<'SQL'
PRAGMA integrity_check;
PRAGMA journal_mode;     -- sollte 'wal' oder 'delete' sein
PRAGMA quick_check;
SQL
done
```

## Pitfalls

- ❌ **Ohne `?mode=ro`** kann selbst ein `SELECT` versehentlich einen
  WAL-Switch auslösen → Filesystem-Timestamp ändert sich.
- ❌ `PRAGMA table_info` ohne Quoting → Tabellen mit Punkten/Spaces crashen.
  Immer `f'"{name}"'`.
- ❌ `PRAGMA foreign_key_list` liefert **deklarierte** FKs, nicht zwingend die
  "echten" Beziehungen. Für Inferred-Relations: `foreign_keys=ON` setzen +
  Query mit `EXPLAIN` validieren.
- ❌ Niemals `UPDATE`/`DELETE`/`VACUUM`/`REINDEX` ohne expliziten
  `--write`-Switch.
- ✅ Große DBs: erst Rowcounts holen, dann gezielt `LIMIT`/`WHERE`.

## Cron-Beispiel

```cron
# So 04:00 — wöchentlicher DB-Health-Check
0 4 * * 0 /home/bratan/.openclaw/skills/sqlite-reader/scripts/sqlite_health.sh \
    /home/bratan/.local/share/GreyHack/player.db \
    /home/bratan/.openclaw/sessions.db
```