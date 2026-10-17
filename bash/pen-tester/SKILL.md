---
name: pen-tester
description: 'Port-scan, deps, permissions, network, password hygiene.'
category: security
version: 1.0.0
---

# pen-tester — Automatisierter Security-Audit

Führt vollständigen Security-Audit durch: Port-Scan, Dependency-Audit, File-Permissions, Network-Exposure, Password-Hygiene. Erzeugt HTML + JSON Reports mit CVSS-ähnlichem Scoring.

## CLI

```bash
# Quick-Modus (Port + Permissions) — ideal für Cron alle 4h
python scripts/pen-tester.py --quick

# Full-Modus (alle Checks)
python scripts/pen-tester.py --full

# Mit Report-Speicherung
python scripts/pen-tester.py --full --report reports/

# Nur Console (keine Dateien)
python scripts/pen-tester.py --quick --stdout
```

## Exit-Codes

| Code | Bedeutung |
|------|-----------|
| 0 | Sicher / keine Funde |
| 1 | Warnungen (low/medium) |
| 2 | Kritisch (high/critical) |

## Checks

1. **Port-Scan** — 30+ Common Ports (22,80,443,3306,5432,6379,27017,…) auf localhost + LAN-IP. Threaded parallel (50 Worker), ~4s.
2. **Dependency-Audit** — `pip-audit` (falls installiert) sonst `pip list --outdated`. Erkennt CVEs.
3. **File-Permissions** — `.env`, `config.yaml`, `.backup_key` auf korrekte Berechtigungen. Windows: Everyone/Users. Unix: group/other Bits.
4. **Network-Exposure** — `netstat -ano` auf 0.0.0.0/[::]-Bindungen. Warnt bei externer Erreichbarkeit.
5. **Password-Hygiene** — Scannt Configs auf Standard-Passwörter (admin, password, 123456, your-api-key) + API-Key-Zählung.

## Reports

- **HTML**: Dark-Theme mit Risk-Score-Ring, Summary-Cards, Findings-Tabelle.
- **JSON**: Maschinenlesbar mit CVSS-Scoring und Severity-Zählung.

## Pfad

Script: `$OPENAMER_HOME/scripts/pen-tester.py` (Default: `~/AppData/Local/openamer-laptop/scripts/`)