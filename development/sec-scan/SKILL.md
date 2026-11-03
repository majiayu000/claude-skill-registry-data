---
name: sec-scan
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Anbieterneutraler Security-Scan eines eigenen Repos: Bedrohungsmodell, Aufteilung nach Vertrauensgrenzen, gezielte Prüfung je Paket (Injection, Authn/Authz, Secrets, Krypto, Deserialisierung, Pfade, SSRF, Konfiguration, verwundbare Abhängigkeiten), Kandidaten mit Evidenz in findings.json und ehrliche coverage.json. Modi standard und deep. Nutzen bei 'Security-Scan', 'Repo auf Schwachstellen prüfen', 'Sicherheitsreview', 'Vollscan', 'Scanner-Ergebnis in das ellmos-Format übernehmen'. Enthält den Adapter für /claude-security und codex-security. Nur Änderungen/PRs: sec-diff-scan. Kandidaten widerlegen: sec-validate. Fremde Berichte importieren: sec-triage. Bericht: sec-report."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, scan, vulnerabilities, sast, source-to-sink, cwe]
language: de
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-scan banner">

# sec-scan

Kern der ellmos-Security-Familie. Der gemeinsame Vertrag (Phasen, Dateien, Lebenszyklus, Severity, Regeln, Adapter) steht in `references/contract.md`, Schemas in `schemas/`, Validator in `scripts/secfind.py` + `scripts/seclib.py` (nur Standardbibliothek). Dieser Skill zitiert den Vertrag, wiederholt ihn nicht. Nachbarn: `sec-threat-model`, `sec-diff-scan`, `sec-validate`, `sec-triage`, `sec-report`.

## Modi

- **standard:** ein Durchlauf, ein Modell, eine Sitzung.
- **deep:** mehrere unabhängige Durchläufe (andere Paketreihenfolge, Zuschnitt oder Modell), Vereinigung per `id`. Nur nach Kostenwarnung und Bestätigung des Nutzers (Vertrag 6.5).

## Ablauf

1. **Ziel und Scope:** Repo, Ref (Commit-SHA oder `working-tree`), ausgeschlossene Pfade. `scanId` vergeben. Das Scan-Verzeichnis heißt `sec-scan-<scanId>/` (Vertrag 1), liegt unter einem Basisordner **außerhalb des Repos** und wird erst nach dem Preflight angelegt.
2. **Preflight:**
   - Eigener oder autorisierter Code? Sonst Abbruch (Vertrag 6.1).
   - Lock-Prüfung für das Repo und den Basisordner des Scan-Verzeichnisses: `python <lock_scan.py> --check-dir '<Pfad>' --json`, Exitcode sofort sichern. 0 = frei, 1 = gesperrt, alles andere (Absturz, unlesbare Ausgabe) = unbekannt = stopp (Vertrag 6.2). Interpreter ausdrücklich aufrufen, nie das Skript "öffnen". Gibt es `lock_scan.py` auf dem Host nicht (kein ellmos-Lock-System), stattdessen `LOCK*.txt` im Repo und in den Elternordnern suchen: keine = frei (im Bericht vermerken), eine oder mehr = stopp.
   - **Egress ansagen:** geht Code an einen Anbieter (gehostete Review-Schicht, Fremdmodell)? Private Repos nur in der lokalen Sitzung (Vertrag 6.6). **Kosten ansagen**, bei `deep` Bestätigung abwarten (6.5).
3. **Bedrohungsmodell:** `threatmodel.md` vorhanden und aktuell? Sonst `sec-threat-model` ausführen.
4. **Pakete bilden:** das Repo nach Vertrauensgrenzen und Einstiegspunkten aus dem Modell teilen, je Paket Dateien und Untersuchungsfragen. Sehr große Pakete teilen, statt oberflächlich zu lesen.
5. **Je Paket prüfen** (Source-to-Sink: Quelle -> Transformation -> Senke, Gegenmaßnahmen auf dem Pfad mitlesen):
   Injection (SQL, Shell, Template, LDAP/NoSQL), Authn/Authz und Mandantentrennung, Secrets im Code, Kryptografie (Algorithmen, Zufall, Schlüsselumgang), unsichere Deserialisierung, Pfad-/Dateizugriff (Traversal, Upload, Symlinks), SSRF und offene Weiterleitung, unsichere Konfiguration (Debug, CORS, Defaults, Rechte), Nutzung bekannt verwundbarer Abhängigkeiten (Muster im Code; Advisory-Abgleich ist `security-tech-stack-check`). Befunde, die der Pfad nicht trägt, nicht aufnehmen; Verdacht ohne Beleg gehört in `coverage.limits`, nicht in `findings`.
6. **Kandidat festhalten:** `rule` dotted lowercase (`py.sql-injection`), `cwe` falls passend, `severity` und `confidence` nach Vertrag 3, `status: candidate`, `location`, `evidence` als zitierter Code/Trace. **Geheimniswerte maskieren** (Vertrag 4). `id` immer per `python scripts/secfind.py id RULE PATH -` (Snippet über stdin), nie von Hand.
7. **Coverage ehrlich führen:** `scanned` mit Tiefe `read` / `skimmed` / `pattern-only`, `notScanned` mit Grund (generiert, vendored, zu groß, Binär, nicht erreichbar), `limits` für Methodengrenzen. `complete: true` nur bei leerem `notScanned` (Vertrag 5). `unknown` ist nicht "sicher".
8. **Validieren:** `python scripts/secfind.py validate findings.json coverage.json`, Exitcode (0/1) und Ausgabe zeigen. Bei Fehlern korrigieren und erneut laufen lassen.
9. **Abschluss:** Anzahl Kandidaten je Severity, Coverage-Stand, nächste Schritte (`sec-validate`, dann `sec-triage`, `sec-report`). Ein partieller Scan wird als partiell gemeldet (Vertrag 6.9).

## deep

Mindestens zwei Durchläufe mit unterschiedlichem Zuschnitt, je eigene Kandidatenliste. Vereinigung per `id`: gleiche `id` zusammenführen (Evidenz ergänzen, bei abweichender Severity die höhere übernehmen und die Abweichung in `description` nennen), neue `id` aufnehmen. Coverage = Vereinigung der gelesenen Pfade; `provider.model` nennt alle beteiligten Modelle.

## Adapter

Ein vorhandener Anbieter-Scanner kann den Scan-Teil übernehmen (Vertrag 7): **Claude** `/claude-security`, **Codex** `codex-security`. Gemini und Kimi haben keinen und folgen dem obigen Ablauf.

1. Scanner nach Preflight (Schritt 2) laufen lassen; seine Ausgabedateien lesen und feldweise auf `findings.json` / `coverage.json` abbilden. Die Dateien und Felder des Scanners werden hier nicht vorweggenommen; das Mapping entsteht beim Lesen der tatsächlichen Ausgabe und wird in `coverage.limits` vermerkt.
2. **Alle Funde starten als `candidate`**, auch wenn der Scanner sie als bestätigt führt. Ein Adapter überspringt die Validierung nie.
3. `provider.name` / `provider.model` nach dem Scan, `provider.engine` = Name des Scanners.
4. Coverage aus dem Scan-Bericht übernehmen. Gibt er keine Abdeckung her, `complete: false` und unter `notScanned` einen Eintrag "Abdeckung des Scanners unbekannt" anlegen (ohne `notScanned`-Eintrag ist `complete: false` laut Validator ungültig; `limits` allein genügt nicht).
5. `id`s per `secfind.py id` neu bilden, damit Funde mit denen anderer Läufe zusammenfallen. Danach Schritt 8.

## Grenzen

Kein Patchen, kein Commit, kein Netzscan (Vertrag 6.1, 6.3). Keine Laufzeit-Exploits; Nachstellen ist `sec-validate`.

## Changelog

### 0.1.0 (2026-10-31)

- Erstfassung: Modi standard/deep, Preflight, Pakete, Adapter.
