---
name: sec-threat-model
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Erstellt oder aktualisiert das Bedrohungsmodell eines eigenen Repos (Assets, Vertrauensgrenzen, Einstiegspunkte, Datenflüsse, Angreiferziele, priorisierte Untersuchungsfragen) als threatmodel.md aus dem echten Quelltext. Nutzen bei 'Bedrohungsmodell', 'Threat Model', 'was muss ich in diesem Repo zuerst prüfen', 'Angriffsfläche', vor einem Security-Scan oder wenn sich die Architektur geändert hat. Läuft allein oder als Phase 1 von sec-scan; findet selbst keine Schwachstellen (dafür sec-scan / sec-diff-scan) und prüft keine Abhängigkeits-Advisories (dafür security-tech-stack-check)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, threat-model, attack-surface, trust-boundaries, review]
language: de
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-threat-model banner">

# sec-threat-model

Phase 1 der ellmos-Security-Familie (`sec-threat-model`, `sec-scan`, `sec-diff-scan`, `sec-validate`, `sec-triage`, `sec-report`). Gemeinsamer Vertrag: `sec-scan/references/contract.md` (Abschnitt 1 Scan-Verzeichnis, 6 Regeln). Hier nicht wiederholt.

## Regeln

- Nur eigener oder ausdrücklich autorisierter Code (Vertrag 6.1). Kein Netzzugriff auf fremde Systeme, keine Port-Scans.
- Das Modell entsteht aus **gelesenem Quelltext**, nicht aus README-Behauptungen. Was nur dort steht oder nicht belegbar ist, kommt als `offen` ins Modell, nie als Tatsache.
- Schreiben nur in das Scan-Verzeichnis (`<tmp>/ellmos-security/<repo>/sec-scan-<scanId>/`), nicht in den Quelltext. Vor dem Schreiben Lock prüfen wie in `sec-scan` > Preflight.

## Vorgehen

1. **Scope klären:** Repo, Ref (Commit-SHA oder `working-tree`), ausgeschlossene Pfade. Vorhandenes `threatmodel.md` lesen; dann Update-Modus: nur Änderungen nachziehen, Stand und Ref vermerken.
2. **Struktur lesen:** Manifeste, Build-/Deploy-Dateien, Konfiguration, Verzeichnisbaum. Sprachen und Frameworks aus dem Code ableiten.
3. **Einstiegspunkte finden:** HTTP-Routen, CLI-Argumente, Queue-/Webhook-Consumer, Datei- und Format-Parser, IPC/Sockets, geplante Jobs, Umgebungsvariablen, Plugin-/Skript-Ladepunkte. Je Eintrag Datei:Zeile und Aufruferkreis (anonym, authentifiziert, intern).
4. **Assets benennen:** Geheimnisse und Tokens, personenbezogene Daten, Nutzerdateien, Datenbanken, Rechenzeit, Ausführungsrechte, Reputation/Lieferkette. Ort im Code, nie den Wert.
5. **Vertrauensgrenzen ziehen:** wo Daten von weniger vertrauenswürdig nach vertrauenswürdig wechseln (Netz -> Prozess, Nutzer -> Admin, Mandant -> Mandant, Prozess -> Betriebssystem/Shell/DB, Drittpaket -> eigener Code). Wo die Durchsetzung (Authn/Authz, Validierung, Sandbox) im Code sitzt, oder dass sie fehlt.
6. **Datenflüsse skizzieren:** Source -> Transformation -> Sink für die kritischsten Assets und Einstiegspunkte (Text oder Mermaid, kurz). Sinks: Shell, SQL, Dateisystem, Deserialisierung, Template, HTTP-Client, Logs.
7. **Angreiferziele ableiten:** pro Grenze, was ein Angreifer erreichen will (Codeausführung, Datenabfluss, Rechteausweitung, Manipulation, Ausfall). STRIDE nur als Denkhilfe, nicht als Pflichtraster.
8. **Untersuchungsfragen priorisieren:** konkrete, prüfbare Fragen ("Erreicht `user_id` aus Route X ungeprüft die Query in `db.py`?"), sortiert nach Auswirkung mal Erreichbarkeit. Sie werden in `sec-scan` zu Untersuchungspaketen.

## Ausgabe: `threatmodel.md`

Abschnitte in dieser Reihenfolge: **Stand** (Repo, Ref, Datum, gelesene Pfade) · **Assets** · **Vertrauensgrenzen** · **Einstiegspunkte** (Tabelle: Pfad, Typ, Aufrufer, Auth) · **Datenflüsse** · **Angreiferziele** · **Untersuchungsfragen** (nummeriert, priorisiert) · **Offen** (Annahmen, nicht gelesene Bereiche, Widersprüche zwischen Doku und Code). Kein Geheimniswert, keine Exploit-Anleitung.

## Abgrenzung

Findet keine Schwachstellen und vergibt keine Severity. Ein Modell mit vielen `offen`-Einträgen ist ehrlicher als ein glattes.

## Changelog

### 0.1.0 (2026-10-31)

- Erstfassung als Phase 1 der Security-Familie.
