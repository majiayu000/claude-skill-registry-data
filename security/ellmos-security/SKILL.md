---
name: ellmos-security
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Einstieg und Router der anbieterneutralen ellmos-Security-Familie (sec-*): ordnet Phasen von Bedrohungsmodell über Scan, Validierung, Triage, Fix, Verifikation und Tracking bis zum Bericht ein und verweist auf den passenden Skill. Auslöser: 'Sicherheitsprüfung', 'Repo auf Schwachstellen prüfen', 'welcher Security-Skill', 'PR sicherheitsprüfen', 'Fremdplugin prüfen', 'SECURITY.md', 'Disclosure'. Führt selbst keine Prüfung aus; die Arbeit machen die sec-*-Skills und die Nachbar-Skills, die hier nur verlinkt sind."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, router, umbrella, vulnerability, appsec]
language: de
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="ellmos-security banner">

# ellmos-security - Einstieg der Security-Familie

Die Familie prüft eigenen Code auf Schwachstellen und führt jeden Fund vom Verdacht bis zum nachverfolgten, verifizierten Fix. Alle Skills teilen einen Vertrag (Dateiformate, Lebenszyklus, Severity, Regeln): `sec-scan/references/contract.md`. Sie laufen bei Claude, Codex, Gemini und Kimi und hängen von keinem herstellerspezifischen Scanner ab; solche Scanner sind nur Adapter (Tabelle unten).

## Phasen

| Phase | Skill | Wann |
|---|---|---|
| Modell | `sec-threat-model` | vor dem ersten Scan: Werte, Vertrauensgrenzen, Einstiegspunkte |
| Scan | `sec-scan` | ganzes Repo oder ein Pfad |
| Scan (Änderung) | `sec-diff-scan` | Pull Request, Commit-Bereich, Diff |
| Validierung | `sec-validate` | jeden `candidate` unabhängig bestätigen oder widerlegen |
| Triage | `sec-triage` | Severity und Priorität gegen die Richtlinie |
| Fix | `sec-fix` | nur auf Wunsch, Patch als Datei |
| Verifikation | `sec-verify-fix` | schließt der Patch die Lücke, Regressionsrisiko |
| Tracking | `sec-track` | Ticket, Issue oder Draft-Advisory |
| Bericht | `sec-report` | `report.md` und `findings.sarif` |

Quer dazu: `sec-policy` (SECURITY.md), `sec-hardening` (strukturelle Maßnahmen), `sec-writeup` (Offenlegungsbericht), `sec-supplychain` (Fremdes vor der Installation).

## Was will ich?

- Ein Repo prüfen -> `sec-scan` (bei neuem Projekt vorher `sec-threat-model`)
- Einen PR oder Diff prüfen -> `sec-diff-scan`
- Einen vorhandenen Fund weiterverfolgen -> `sec-validate` -> `sec-triage` -> `sec-fix` -> `sec-verify-fix` -> `sec-track`
- Ergebnisse als Bericht -> `sec-report`
- Regeln für ein Repo festlegen oder prüfen -> `sec-policy`
- Wiederkehrende Fundklassen grundsätzlich lösen -> `sec-hardening`
- Eine Lücke melden oder offenlegen -> `sec-writeup`
- Ein fremdes Skill, Plugin, einen MCP-Server oder Hook installieren -> `sec-supplychain`

## Nachbar-Skills (getrennt gepflegt, gehören dazu)

- `security-tech-stack-check` + `tech-detect`: Abhängigkeiten und CVEs gegen den gemessenen Tech-Stack.
- `protection-shield`: akute Abwehr und wiederkehrende Log-/Stack-Prüfung auf eigenen Systemen.
- `repo-publish-check`: Veröffentlichungs-Gate vor dem Öffentlichmachen eines Repos.
- Falls auf deinem System vorhanden: ein eigener Security-Wegweiser und ein Skill für persönliche Konten/Daten (kein Code). Sie sind nicht Teil dieser öffentlichen Familie.

## Anbieter-Adapter (Vertrag §7)

| Anbieter | Natives Scan-Werkzeug | Anbindung | Kostenhinweis |
|---|---|---|---|
| Claude | Plugin `/claude-security` | damit scannen, Ausgabeordner auf `findings.json`/`coverage.json` abbilden | Plugin-Scan mit mehreren Agenten: vorher schätzen und warnen (Regel 5); Egress beachten (Regel 6) |
| Codex | Plugin `codex-security` | dasselbe, aus dessen Scanausgabe | wie oben |
| Gemini, Kimi | keines | eigenes Verfahren aus `sec-scan` | Tokens der laufenden Sitzung; `deep`-Scans vorher schätzen |

Adapter überspringen nie die Validierung: abgebildete Funde starten als `candidate`. Genaue Abbildungsschritte: `sec-scan`, Abschnitt Adapter.

## Schnellstart

**Ganzes Repo:** `sec-threat-model` (kurz) -> `sec-scan` -> `python scripts/secfind.py validate findings.json coverage.json` (Skript in `sec-scan`) -> `sec-validate` mit anderem Anbieter -> `sec-triage` -> `sec-report`.

**Pull Request:** `sec-diff-scan` auf den Diff -> Funde des PR direkt an den Autor; bei Bestätigung `sec-validate`, danach wie oben. Abdeckung in `coverage.json` prüfen: nur den Diff gesehen heißt nicht "Code sicher".

**Ein bestätigter Fund bis zum Ticket:** `sec-triage` (Severity gegen `SECURITY.md`) -> auf Wunsch `sec-fix` -> `sec-verify-fix` mit anderem Prüfer -> `sec-track` (Vorschau, Bestätigung, `finding.ticket` zurückschreiben).

## Gemeinsame Regeln (Kurzform, maßgeblich ist der Vertrag §6)

Nur eigener Code · Lock vor jedem Schreiben · Patches statt Commits · keine Geheimnis-Werte in Ausgaben · Kosten- und Egress-Warnung vor großen Läufen · unabhängige Validierung · ein Ergebnis ohne `coverage.json` ist keins.

## Changelog

### 0.1.0 (2026-10-31)
- Erstfassung des Routers.
