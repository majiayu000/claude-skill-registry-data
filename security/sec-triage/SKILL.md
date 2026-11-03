---
name: sec-triage
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Überführt vorhandene Funde (Scanner-Berichte, SARIF, GitHub Code Scanning, Dependabot, Tickets) in das findings.json-Format der ellmos-Security-Familie, entdoppelt sie per id, legt Severity und Priorität nach der Sicherheitsrichtlinie des Repos (SECURITY.md) fest und verknüpft Tickets. Nur statische Auswertung. Nutzen bei 'Scan-Ergebnisse einordnen', 'Dependabot-Alerts priorisieren', 'Code-Scanning-Funde importieren', 'Backlog an Sicherheitsfunden sortieren'. Neue Schwachstellen suchen: sec-scan. Widerlegen oder nachstellen: sec-validate. Bericht: sec-report."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, triage, sarif, dependabot, code-scanning, prioritisation]
language: de
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-triage banner">

# sec-triage

Phase 4 der ellmos-Security-Familie. Vertrag: `sec-scan/references/contract.md` (Dateien 1, Lebenszyklus 2, Severity 3, id 4, Regeln 6). Validator: `sec-scan/scripts/secfind.py`. **Nur statische Evidenz:** keine Neuentdeckung (`sec-scan`), keine Laufzeitvalidierung (`sec-validate`).

## Eingang

Vorhandene Funde: SARIF-Dateien oder Berichte von Scannern, GitHub Code Scanning und Dependabot (Export per `gh` oder aus der Weboberfläche, Egress beachten), Tickets, Audit-Listen. Liegt schon ein `findings.json` vor, wird es fortgeschrieben, sonst neu angelegt (Scan-Verzeichnis nach Vertrag 1). Preflight wie `sec-scan` Schritt 2 (Eigentum, Lock-Prüfung fail-closed).

## Ablauf

1. **Abbilden:** je Quellfund ein Eintrag. `rule` auf dotted lowercase normalisieren (`py.sql-injection`; die Original-Regelkennung in `description` mit Quelle), `cwe` aus den Tags der Quelle, `location` aus dem Alert, `severity` zunächst wie die Quelle sie angibt, `status: candidate`.
2. **Evidenz sichern:** Code-Ausschnitt aus dem Alert, sonst die Stelle in der angegebenen Datei lesen und zitieren. Lässt sich keine Evidenz belegen (Datei fehlt, Zeile verschoben, Alert ohne Code), den Fund **nicht** mit erfundener Evidenz aufnehmen, sondern in `coverage.limits` als nicht importiert mit Grund listen. Geheimniswerte maskieren (Vertrag 4). Für Abhängigkeits-Alerts: `rule` z. B. `dep.vulnerable-dependency`, `location` = Manifest-/Lockfile-Zeile, `evidence` = diese Zeile; Advisory-ID und betroffene Version in `description`.
3. **Entdoppeln:** `id` per `python sec-scan/scripts/secfind.py id RULE PATH -` bilden. Gleiche `id` (auch aus mehreren Quellen) werden zu einem Fund zusammengeführt, die Quellen in `description` aufgelistet; bei abweichender Severity die höhere übernehmen und das vermerken.
4. **Richtlinie lesen:** `SECURITY.md` (Severity-Definitionen, Fristen, unterstützte Versionen, Meldeweg) und ggf. Projekt-Entscheidungen. Fehlt sie, gilt Vertrag 3 und das wird im Ergebnis genannt.
5. **Severity und Priorität festlegen:** Severity gegen die Richtlinie prüfen und begründet anpassen; Priorität aus Severity, Exposition und Fristen ableiten und in `priority` eintragen (`P0`-`P4`, P0 am dringendsten; Stufen der Richtlinie darauf abbilden), die Begründung in `description`.
6. **Status:** `triaged` verlangt laut Validator `validatedBy.verdict == confirmed`. Bereits validierte Funde (`validated`) werden `triaged`. Importierte, noch nicht validierte Funde bleiben `candidate` mit gesetzter Severity/Priorität und gehen an `sec-validate`. Ausschluss nur, wenn die Richtlinie ihn ausdrücklich deckt (z. B. nicht unterstützte Version): `rejected` mit `rejectedReason`.
7. **Tickets:** nur wenn der Nutzer oder die Richtlinie es verlangt: `ticket_writer.py` (nie Ids von Hand) oder GitHub Issue/Draft-Advisory; Schwachstellen in öffentlichen Repos als **privater** Advisory-Entwurf, nicht als öffentliches Issue. Referenz in `ticket` eintragen. Keine Geheimniswerte in Tickets (Vertrag 6.4).
8. **Coverage:** ein reiner Import scannt nichts. `scanned: []`, `notScanned` mit Eintrag "Import ohne eigenen Scan, Repo nicht gelesen" (damit `complete: false`), `limits` mit Quellen, Importstand und nicht importierten Funden. `provider.name` = Quelle (z. B. `github-code-scanning`), `model` = `n/a`, `engine` = Quellwerkzeug.
9. **Prüfen:** `python sec-scan/scripts/secfind.py validate findings.json coverage.json`, Exitcode zeigen. Dann `sec-validate` für Kandidaten, `sec-report` für den Bericht.

## Changelog

### 0.1.0 (2026-10-31)

- Erstfassung: Import, Entdoppelung per id, Richtlinien-Triage.
