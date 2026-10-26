---
name: pulse-audit
description: Read-only Gesamtprüfung des Pulse-Branches vor größeren Änderungen oder Merge. Prüft Architektur, offene Regressionen, Berechtigungen, Datenintegrität, Tests, Ressourcenverbrauch und Secrets; liefert priorisierte, belegte Befunde statt spekulativer Fehlerlisten.
argument-hint: [diff | Bereich | PR-Nummer]
disable-model-invocation: true
disallowed-tools: Edit, Write, NotebookEdit
---

# Pulse-Audit (nur lesen)

Diese Prüfung ändert nichts. Keine Dateien schreiben, keine Commits/Pushes/Merges, keine Kommentare auf GitHub, keine echten Discord-/OAuth-Aufrufe und kein VPS-Deployment. `.env` und Laufzeitdaten niemals öffnen oder ausgeben.

## Vorgehen
1. Arbeitsbaum und Branch prüfen: `git status --short`, `git branch --show-current`, `git log -1 --oneline`. Nutzeränderungen nicht überschreiben.
2. Umfang bestimmen: ohne Argument den relevanten Branch-Diff gegen `main`; mit Bereich/PR gezielt Dateien und direkte Aufrufer prüfen. Große Dateien nur in passenden Ausschnitten lesen.
3. Aktiven Kontrollfluss nachverfolgen: insbesondere überschriebenen Dashboard-Routen in `pulse_pro.py`, serverseitige Rechte, Same-Origin/CSRF und echte Schreibpfade.
4. Datenänderungen auf Rückwärtskompatibilität, Backup, atomare Speicherung und sichere Migration prüfen.
5. Ressourcen: 250-MB-RAM-Ziel, begrenzte Caches/Queues, Event-Loop-Blockaden, SQLite-Abfragen, Scheduler und Discord-429-Verhalten prüfen.
6. Tests zuordnen: vorhandene Regressionstests, Negativfälle und E2E-Abdeckung identifizieren. Keine Testresultate behaupten, ohne sie auszuführen.
7. Diff auf Secrets, echte Laufzeitdaten, versehentliche Löschungen und Funktionsverlust prüfen. Keine `.env` lesen.

## Ausgabe
- **Blockierend / wichtig / Hinweis**, jeweils Datei und Zeile, konkretes Szenario und Beleg.
- Fehlende Tests, die den Befund nachweisbar abdecken würden.
- Tatsächlich ausgeführte Tests mit echten Resultaten; nicht ausgeführte Tests klar kennzeichnen.
- Gesamtempfehlung: freigeben / mit Auflagen / nicht freigeben. Keine unbelegten Befunde erfinden.