---
name: resource-monitor
category: system
description: Live-CPU/RAM/DISK/NET-Dashboard + Top-Prozesse + Alarm.
---

# Resource Monitor

Live-Terminal-Dashboard für CPU, RAM, Festplatte, Netzwerk und Top-Prozesse mit Alarm bei Schwellwertüberschreitung.

## Standort

- **Skript**: `scripts/resource-monitor.py` im OpenAmer Home (`~/AppData/Local/openamer-laptop/`)
- **Skill**: `resource-monitor`

## Verwendung

```bash
# Einmalige JSON-Ausgabe
python3 scripts/resource-monitor.py --once

# Live-Modus (aktualisiert alle 2s)
python3 scripts/resource-monitor.py --watch

# Alarm-Modus: Exit-Code 1 bei Überschreitung
python3 scripts/resource-monitor.py --alert
```

## Datenquellen

- **psutil** (Python): CPU, RAM, DISK, NET, Prozessliste
- **Keine externen Dependencies** (psutil ist bei OpenAmer vorinstalliert)

## CLI-Optionen

| Flag | Beschreibung |
|------|-------------|
| `--once` | Einmalige JSON-Ausgabe aller Metriken |
| `--watch` | Live-Dashboard (alle 2 Sekunden aktualisiert) |
| `--alert` | Prüft Schwellwerte, Exit-Code 1 bei Überschreitung |

## Schwellwerte (Alarme)

| Metrik | Schwelle | Beschreibung |
|--------|----------|-------------|
| CPU | 90% | Zu hohe CPU-Auslastung |
| RAM | 85% | Zu hohe Speicherauslastung |
| DISK | 90% | Zu hohe Festplattenauslastung |

## Anzeige-Modi

- **Rich** (bevorzugt): Farbiges Layout mit Tabellen und Panels
- **Echo+Clear** (Fallback): Einfacher Terminal-Output, wenn Rich nicht verfügbar

## Anzeige-Inhalte (Live-Modus)

1. **Zeile 1**: CPU% | RAM% | DISK% | NET↓↑
2. **Top 5 Prozesse** nach CPU
3. **Top 5 Prozesse** nach RAM
4. **Letzte Alarme** (RAM>85%, DISK>90%, CPU>90%)

## Cron-Job

Der Cron-Job `resource-monitor-alert` läuft alle 5 Minuten im `--alert`-Modus.
Bei Schwellwertüberschreitung wird eine Benachrichtigung ausgelöst.

## Troubleshooting

- **`psutil` nicht gefunden**: `pip install psutil`
- **`Rich` nicht gefunden**: `pip install rich` (Fallback-Modus wird automatisch genutzt)
- **Keine Daten**: Skript benötigt Leseberechtigung für `/proc` (Linux) oder entsprechende Windows-APIs