---
name: sec-report
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Erzeugt aus findings.json und coverage.json den Sicherheitsbericht report.md (nach Severity gruppiert, Coverage-Abschnitt mit Lücken, abgelehnte Funde getrennt, Zusammenfassung ohne Schönfärberei) und findings.sarif (SARIF 2.1.0) per Skript render_report.py. Nutzen bei 'Security-Bericht erstellen', 'Ergebnis des Scans zusammenfassen', 'SARIF exportieren', 'Bericht für Code Scanning'. Bricht bei ungültigen Daten ab, ein partieller Scan wird als partiell gemeldet. Neue Funde: sec-scan / sec-diff-scan. Prüfen: sec-validate. Einordnen: sec-triage."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, report, sarif, coverage, findings]
language: de
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-report banner">

# sec-report

Letzte Phase der ellmos-Security-Familie. Vertrag: `sec-scan/references/contract.md` (Dateien 1, Severity 3, Coverage 5, Regeln 6). Das Skript importiert `seclib` aus dem Geschwisterordner `sec-scan/scripts` (im Repo `skills/dev/` und im flachen Deployment `~/.claude/skills/`; beide Ordner müssen nebeneinander liegen). Nur Standardbibliothek.

## Aufruf

```
python scripts/render_report.py FINDINGS COVERAGE OUTDIR [--lang de|en]
```

Interpreter ausdrücklich aufrufen. `OUTDIR` ist das Scan-Verzeichnis; Lock-Prüfung vorher wie `sec-scan` Schritt 2 (fail-closed). Ergebnis: `OUTDIR/report.md` und `OUTDIR/findings.sarif`. Exitcodes: 0 = geschrieben, 1 = Eingabe unlesbar oder ungültig (**nichts** geschrieben), 2 = Aufruf falsch. Exitcode und Ausgabe zeigen.

## Verhalten

- **Validiert zuerst** (`seclib.validate_findings`). Fehler werden gelistet, es entsteht kein Bericht aus kaputten Daten. Erst die Ursache beheben (`sec-scan`, `sec-validate`), dann erneut rendern.
- **report.md:** Kopf (Ziel, Ref, Scanner) · Zusammenfassung · Warnungen · Funde nach Severity (critical bis info) mit Ort, Konfidenz, Status, Validierer, Beleg, Beschreibung, Auswirkung, Empfehlung, Ticket · **abgelehnte Funde getrennt** mit Grund · Coverage (gescannt mit Tiefe, nicht gescannt mit Grund, Grenzen).
- **Ehrlichkeit (Vertrag 5, 6.9):** `complete: false` steht ganz oben als "PARTIELLER SCAN". Keine Funde plus unvollständige Abdeckung heißt "KEIN sauberes Ergebnis". Nur "Keine Funde bei vollständiger Abdeckung" darf wie ein sauberes Ergebnis lesen. Warnungen, etwa gleicher Anbieter bei Finder und Validierer, erscheinen im Bericht.
- **findings.sarif:** SARIF 2.1.0 aus `seclib.to_sarif`; abgelehnte Funde bleiben als `suppressions` im Log. Direkt als Code-Scanning-Upload verwendbar. Hochladen ist eine Veröffentlichung nach außen und braucht den Nutzerauftrag.

## Vor der Weitergabe

Bericht gegenlesen: keine Geheimniswerte (der Validator fängt nur gängige Muster; Vertrag 6.4), nur Fundorte. Berichte in Ticket-Systemen und Chats ebenfalls ohne Werte. Schwachstellen in öffentlichen Repos nicht als öffentliches Issue, sondern über privaten Meldeweg (SECURITY.md).

## Test

`python -m pytest tests -q -p no:cacheprovider` im Skillordner (Bericht, SARIF, partieller Scan, Backtick-Evidenz, Negativfall ohne Ausgabe).

## Changelog

### 0.1.0 (2026-10-31)

- Erstfassung mit `render_report.py`: report.md und findings.sarif aus validierten Daten.
