---
name: log-analyzer
description: Use for log analysis, error tracking, alerts, and dashboard.
---

# Log Analyzer Skill

Integrierte Log-Analyse für OpenAmer: Error-Rate-Tracking, Pattern-Erkennung, Alert-Generation, Trend-Analyse und HTML-Dashboard.

## Script

`C:\Users\damir\scripts\log-analyzer.py`

## Scan-Pfade

| Quelle | Pfad |
|--------|------|
| Cron-Output | `<OPENAMER_HOME>/cron/output/**/*.log` |
| Cron-Output | `<OPENAMER_HOME>/cron/output/**/*.md` |
| Logs | `<OPENAMER_HOME>/logs/*.log` |
| Security-CVE | `~/.security-cve/*.log` |
| Self-Healer | `~/.self-healer/memory.json` |

## CLI-Usage

```bash
python ~/scripts/log-analyzer.py --scan       # Einmaliger Scan
python ~/scripts/log-analyzer.py --watch      # Daemon-Modus (alle 60s)
python ~/scripts/log-analyzer.py --report     # JSON-Report auf stdout
python ~/scripts/log-analyzer.py --dashboard  # HTML-Dashboard erzeugen
python ~/scripts/log-analyzer.py --watch --interval 120  # Watch alle 120s
```

## State

State und Dashboard werden in `~/.log-analyzer/` gespeichert:
- `state.json` — letzter Scan, bekannte Patterns, Error-Historie
- `dashboard.html` — generiertes HTML-Dashboard

## Features

- **Error-Rate**: Fehler pro Minute (letzte 5 Minuten / 5)
- **Top 10**: Häufigste Fehlermeldungen
- **Trends**: Vergleich letzte 30 Min vs. vorherige 30 Min (rising/falling/stable)
- **Pattern-Erkennung**: Clustering ähnlicher Fehler durch Exception-Namen, HTTP-Status, CamelCase-Wörter
- **Alert-Generation**: Alarm bei &gt; 5 ERROR/min, Info bei neuen Patterns
- **HTML-Dashboard**: Dark-Theme mit KPI-Karten, Sparkline, Level-Verteilung, Alerts, Fehler-Tabelle, Pattern-Tabelle, Historie

## Cron-Job

Ein Cron-Job f&uuml;hrt `--scan` alle 15 Minuten aus (siehe OpenAmer-Cron `jobs.json`).

## Wartung

Bei neuen Log-Quellen: `SCAN_PATHS` in `log-analyzer.py` erweitern.
Bei &Auml;nderung des Alert-Schwellwerts: `ALERT_ERROR_RATE_PER_MIN` anpassen.