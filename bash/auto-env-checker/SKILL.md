---
name: auto-env-checker
description: 'Use for environment validation: .env, config.yaml, paths, Python, Git — check + auto-fix + cron every 60min.'
tags:
  - environment
  - validation
  - health-check
  - auto-fix
  - cron
usage: |
  Führe `auto-env-checker.py` für vollständige Umgebungs-Validierung aus.
  Nutze `--fix` für automatische Reparatur und `--json` für maschinenlesbaren Output.
  Der Cron-Job läuft alle 60 Minuten und schreibt Reports nach `logs/auto-env-checker.log`.
---

# Auto-Env-Checker

Vollständige Umgebungs-Validierung für OpenAmer: `.env`, `config.yaml`, paths, Python, Git + Auto-Fix.

## Verwendung

```bash
# Vollständiger Check
python scripts/auto-env-checker.py

# Nur bestimmte Bereiche prüfen
python scripts/auto-env-checker.py --env
python scripts/auto-env-checker.py --config
python scripts/auto-env-checker.py --paths
python scripts/auto-env-checker.py --python
python scripts/auto-env-checker.py --git

# Mit Auto-Reparatur
python scripts/auto-env-checker.py --fix

# JSON-Ausgabe für Weiterverarbeitung
python scripts/auto-env-checker.py --json

# Nur Exit-Code (0=ok, 1=warning, 2=error, 3=critical)
python scripts/auto-env-checker.py --quiet
```

## Exit-Codes

| Code | Bedeutung |
|------|-----------|
| 0    | Alles gut |
| 1    | Warnungen (z.B. fehlende optionale Keys) |
| 2    | Fehler (z.B. fehlende Pfade, defekte Config) |
| 3    | Kritisch (z.B. fehlender API-Key, kein Speicher) |

## Was wird geprüft

### .env
- Existenz der `.env` Datei
- Kritische Keys (`OPENROUTER_API_KEY`)
- Optionale Keys (`OLLAMA_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
- Key-Länge (zu kurze = ungültig)
- Lesbarkeit

### config.yaml
- YAML-Syntax
- Required Sections: `model`, `agent`, `terminal`, `browser`, `display`
- `model.default` und `model.provider`
- `_config_version`
- Auto-Reparatur: Default-Config bei Fehlen

### Paths
- Existenz von: `skills/`, `scripts/`, `cron/`, `memories/`, `config.yaml`, `.env`, `cache/`
- Schreibbarkeit aller Verzeichnisse
- Speicherplatz (<0.5 GB = kritisch, <2 GB = warning)
- Logs-Größe (>100 MB = warning)

### Python
- Version (mindestens 3.10)
- Venv-Status (aktiv? richtiges venv?)
- pip (installiert? outdated packages?)
- uv (installiert?)
- PyYAML (für Config-Check)

### Git
- Git installiert
- Branch-Name
- Uncommitted Changes (klassifiziert nach modified/staged/untracked/deleted)
- Ahead/Behind origin
- Letzter Commit

## Auto-Fix (`--fix`)

Repariert automatisch:
- Fehlende `.env` → leere Datei anlegen (Keys manuell eintragen)
- Fehlende `config.yaml` → Default schreiben
- Fehlende Sections in config → Default-Werte ergänzen
- Fehlende Verzeichnisse → `mkdir`
- Berechtigungen → `chmod`
- Hinterherliegender Branch → `git pull --ff-only`
- Veraltetes pip → pip upgrade
- Fehlendes PyYAML → `pip install pyyaml`

## Cron-Job

Der Cron-Job läuft automatisch alle 60 Minuten und speichert Reports als JSON:

```bash
python "$OPENAMER_HOME\scripts\auto-env-checker.py" --json
```

Reports landen in: `$OPENAMER_HOME\logs\auto-env-checker.log`