---
name: auto-backup
description: "Use when setting up OpenAmer auto-backup."
---

# Auto-Backup Skill

Automatische Sicherung aller wichtigen OpenAmer-Daten.

## Pfade die gesichert werden

| Quelle | Pfad |
|--------|------|
| skills | `HOME/skills/` |
| scripts | `HOME/scripts/` |
| cron-jobs | `HOME/cron/jobs.json` |
| config | `HOME/config.yaml` |
| env | `HOME/.env` |
| security-cve | `HOME/.security-cve/` |
| logs | `HOME/logs/` |

**HOME** = `%LOCALAPPDATA%\openamer-laptop` ($OPENAMER_HOME)

## CLI

```bash
# Backup jetzt ausführen
python scripts/auto-backup.py --now

# Backup mit Verschlüsselung
python scripts/auto-backup.py --encrypt --now

# Alle Backups anzeigen
python scripts/auto-backup.py --list

# Backup wiederherstellen
python scripts/auto-backup.py --restore 2026-08-21

# Backup auf externes Laufwerk
python scripts/auto-backup.py --external D:\backup --now

# Nur simulieren
python scripts/auto-backup.py --dry-run --now
```

## Exit-Codes

| Code | Bedeutung |
|------|-----------|
| 0 | OK |
| 1 | Backup fehlgeschlagen |
| 2 | Kein Speicherplatz |

## Rotation

- 7 tägliche Backups
- 4 wöchentliche Backups (Montag)
- 3 monatliche Backups (erste Woche des Monats)

## Verschlüsselung

Nutzt Fernet (AES-128-CBC) aus der `cryptography`-Bibliothek.
Der Schlüssel liegt in `HOME/.backup_key`. Entfernen → Backups unlesbar.

## Cron-Job

Der Cron-Job läuft alle 24 Stunden (`interval: 1440`) als Script-Job
mit `no_agent: true` — direktes Python-Script, kein Agent-Verbrauch.

## Troubleshooting

- **Windows `nul`-Datei in scripts/**: Wird automatisch ignoriert (reservierter Name).
- **PermissionError bei Restore**: Windows-reservierte Dateien werden übersprungen.
- **Verschlüsselter Restore ohne Key**: Script sucht `HOME/.backup_key`. Alternativ `--encrypt-key PFAD` nutzen.