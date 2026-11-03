---
name: sec-track
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Macht validierte Sicherheitsfunde nachverfolgbar: legt nach Vorschau und Bestätigung ein Ticket (ticket_writer.py), ein GitHub-Issue oder ein Draft-Security-Advisory (gh) an, prüft vorher Duplikate per Finding-id, schreibt keine Geheimnisse in den Text und trägt die Referenz in finding.ticket zurück. Auslöser: 'Fund tracken', 'Ticket für SEC-...', 'Advisory anlegen', 'Funde ins Backlog'. Kein Linear/Jira. Nicht für Fachberichte (sec-report) und nicht für die Offenlegung nach außen (sec-writeup)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, tickets, tracking, github, advisory]
language: de
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-track banner">

# sec-track - Funde nachverfolgbar machen

Phase "track". Vertrag: `sec-scan/references/contract.md` (Regel 4 Geheimnisse, Regel 8 Tickets in §6; Feld `ticket` in `schemas/finding.schema.json`). Nur Funde mit Status `validated` oder weiter - `candidate` wird nicht getrackt.

## Ziel wählen

| Ziel | Wann | Werkzeug |
|---|---|---|
| Ticket im Ticketsystem des Nutzers | Standard, privat, ohne Außenwirkung | `ticket_writer.py` aus ticket-master |
| GitHub-Issue | nur **private** Repos oder reine Härtungslücken ohne Exploit-Pfad | `gh issue create` |
| Draft-Security-Advisory | Schwachstelle in einem **öffentlichen** Repo | `gh api` (Repository-Security-Advisories, Entwurf) |

**Öffentliches Repo + ausnutzbarer Fund: nie ein öffentliches Issue** - das wäre eine Offenlegung (Egress, Regel 6). Dort Draft-Advisory bzw. privates Ticket. Kein Linear, kein Jira.

## Ablauf

1. **Auswahl:** welche Funde, welches Ziel. Mehrere Funde nacheinander, nicht als Sammelticket, damit jede id eine eigene Referenz bekommt.
2. **Duplikatprüfung per Finding-id** (`SEC-<12 hex>`): `finding.ticket` bereits gesetzt? Ticket-Verzeichnisse nach der id durchsuchen; bei GitHub `gh issue list --state all --search "<id>"`. Treffer: bestehende Referenz verwenden, nichts neu anlegen.
3. **Text entwerfen:** id, Titel, Regel/CWE, Severity, Ort (`pfad:zeile`), kurze Wirkung, Empfehlung, Verweis auf Patch-Datei falls vorhanden. **Nie ein Geheimnis-Wert** (Regel 4): nur Fundort. Keine Exploit-Details über das Nötige hinaus.
4. **Vorschau zeigen, Bestätigung abwarten.** Erst danach anlegen - Ticket, Issue oder Advisory sind Außenwirkung bzw. nicht rückholbar.
5. **Anlegen:**
   - Ticket (IDs nie von Hand wählen, Regel 8): `python <ticket-master>/lib/ticket_writer.py --title "<SEC-id> <Titel>" --body "<Text>" --project <projekt> --priority <stufe>`; die CLI gibt den Pfad der angelegten Ticketdatei aus. Die Doku im Modul nennt teils `--urgency`; die CLI selbst kennt `--priority` - vor Gebrauch `--help` lesen.
   - Issue: `gh issue create --repo <owner/repo> --title ... --body-file <datei>`.
   - Advisory: Entwurf über die GitHub-REST-Schnittstelle für Repository-Security-Advisories (`gh api`); genaue Felder vor Gebrauch in der GitHub-Doku prüfen (offen, hier nicht festgeschrieben). Entwurf lassen, nicht veröffentlichen.
6. **Referenz zurückschreiben:** `finding.ticket` = Ticket-Pfad/-id, `owner/repo#nr` oder Advisory-Link; dann `python scripts/secfind.py validate findings.json coverage.json` (Skript in `sec-scan`).

## Changelog

### 0.1.0 (2026-10-31)
- Erstfassung.
