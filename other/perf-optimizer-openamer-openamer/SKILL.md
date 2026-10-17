---
name: perf-optimizer
description: >-
  Use when running or debugging the perf-optimizer on Windows.
---

# Perf-Optimizer — KI-Performance-Optimierung

## Beschreibung

Autonomes Performance-Optimierungs-System für OpenAmer auf Windows (Git-Bash/MSYS2).
Führt regelmäßige System-Checks durch und generiert Optimierungsvorschläge.

## Komponenten

```
openamer-laptop/
├── scripts/perf-optimizer.py   # Das Hauptskript
└── skills/perf-optimizer/       # Dieser Skill (Dokumentation)
```

## Funktionen

1. **RAM-Monitoring**
   - Aktuelle RAM-Auslastung (%)
   - Pagefile-Größe und Nutzung
   - Top-10-RAM-Verbraucher (Prozesse)
   - Warmmeldung ab 75%, Kritisch ab 85%

2. **Disk-Monitoring**
   - Speicherplatz pro Laufwerk (GB, %)
   - Temp-Dateien-Größe (User Temp, Windows Temp)
   - OpenAmer Logs-Größe
   - Warmmeldung ab 80%, Kritisch ab 90%

3. **Cron-Timing-Analyse**
   - Cron-Job-Laufzeiten (anhand Datei-Alter)
   - Fehlererkennung in Logs (traceback/exception)
   - Engpass-Erkennung (gleichzeitige Läufe)

4. **Optimierungsvorschläge**
   - Automatisch generierte Handlungsempfehlungen
   - Kategorisiert nach RAM/Disk/Temp/Cron
   - Priorisiert nach severity (high/medium/low)

5. **Auto-Cleanup**
   - Temporäre Dateien löschen (>500 MB)
   - Alte OpenAmer-Logs archivieren (>7 Tage)
   - Im Dry-Run-Modus testbar (`--dry-run`)

## Verwendung

### Einmalig ausführen:

```bash
bash -c 'cd "$(openamer config show home)/scripts" && python3 perf-optimizer.py'
```

### Dry-Run (nur Analyse, keine Löschungen):

```bash
bash -c 'cd "$(openamer config show home)/scripts" && python3 perf-optimizer.py --dry-run'
```

### Ausführliche Ausgabe:

```bash
bash -c 'cd "$(openamer config show home)/scripts" && python3 perf-optimizer.py --verbose'
```

## Exit-Codes

| Code | Bedeutung                              |
|------|----------------------------------------|
| 0    | Alles sauber, keine Optimierung nötig  |
| 1    | Auffälligkeiten erkannt (minor)       |
| 2    | Kritische Probleme (RAM/Disk > Schwelle) |
| 3    | Timeout während der Analyse           |

## Cron-Job (alle 12h)

Der Cron-Job wird via `cronjob`-Tool eingerichtet:

```yaml
schedule: "0 */12 * * *"  # Alle 12 Stunden
command: >
  bash -c 'cd "$(openamer config show home)/scripts" && python3 perf-optimizer.py'
alarm: true  # Alarm bei Exit-Code != 0
```

## JSON-Output-Struktur

Das Skript gibt pro Phase ein JSON-Objekt aus:

- `phase: "ram"` → RAM-Daten
- `phase: "disk"` → Festplatten-Daten
- `phase: "cron_timing"` → Cron-Analyse
- `phase: "suggestions"` → Optimierungsvorschläge
- `phase: "cleanup_executed|cleanup_dry_run"` → Cleanup-Ergebnisse
- `phase: "summary"` → Gesamtbewertung mit Alarm-Status

## Fehlerbehandlung

- Globaler Timeout: 25 Sekunden (verhindert Hänger)
- Encoding-Fallback: utf-8 → cp1252 → cp850 → latin-1
- Powershell-Fallback für WMIC bei fehlenden Berechtigungen
- Alle Exceptions werden abgefangen und als JSON-Fehler gemeldet

## Architektur-Hinweis

Das Skript ist als **externes Python-Skript** in `scripts/` implementiert
(nicht als OpenAmer-Core-Tool), gemäß der OpenAmer-Architektur:
"Capability lives at the edges — baue als Skills + Cron Jobs + Plugins".