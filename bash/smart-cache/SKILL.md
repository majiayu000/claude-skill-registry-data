---
name: smart-cache
description: Use for cache scan, cleanup, skill archiving, and warm-cache reports.
category: system
---

# Smart Cache

Cache-Analyse + Auto-Cleanup + Skill-Archivierung + Warm-Cache.

## CLI

```bash
python scripts/smart-cache.py --scan          # Cache-Grössen anzeigen
python scripts/smart-cache.py --clean --force  # Veraltete Dateien löschen
python scripts/smart-cache.py --warm           # Seltene Skills archivieren
python scripts/smart-cache.py --stats          # JSON-Report
python scripts/smart-cache.py --dry-run        # Nur zeigen, nichts löschen
```

## Exit Codes

| Code | Bedeutung         |
|------|-------------------|
| 0    | Alles sauber      |
| 1    | Cache > 1 GB      |
| 2    | Kein Cleanup nötig |

## Automatische Cron-Jobs

- `smart-cache-clean`: alle 6h — `--clean --force`
- `smart-cache-warm`: alle 24h — `--warm`

## Was wird analysiert

| Ordner              | Limit | Lösch-Regel         |
|---------------------|-------|---------------------|
| `skills/.hub/`      | 500MB | Ganzer Cache wenn   |
| `scripts/node_modules/` | 500MB | Ganzer Cache wenn  |
| `logs/*.log`        | 500MB | > 7 Tage            |
| `.security-cve/`    | 500MB | Ganzer Cache wenn   |
| `.predictive-health/`| 500MB | Ganzer Cache wenn   |
| `cron/output/`      | 500MB | > 72h               |
| Temp-Dateien        | —     | > 24h               |

## Skills – Archivierung (Warm-Cache)

Skills die > 30 Tage nicht benutzt wurden werden nach `/.skill-archives/` als ZIP archiviert und aus dem aktiven Skills-Verzeichnis entfernt. Bei Bedarf können sie manuell zurückgeholt werden.

## Pfad

OpenAmer Home: `$OPENAMER_HOME`
Skript: `scripts/smart-cache.py`