---
name: sec-policy
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Definiert, prüft oder aktualisiert die SECURITY.md eines Repos (Geltungsbereich, ausgeschlossene Bereiche, verlangte Sicherheitseigenschaften, Meldeweg, Reaktionszeiten, unterstützte Versionen) und gleicht ihre Aussagen gegen den tatsächlichen Code ab. Die Richtlinie ist die Grundlage für sec-triage. Auslöser: 'SECURITY.md erstellen/prüfen', 'Sicherheitsrichtlinie', 'was gilt hier als Schwachstelle', 'Meldeweg festlegen'. Nicht für Funde (sec-scan), nicht für Offenlegungsberichte (sec-writeup)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, policy, security-md, disclosure]
language: de
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-policy banner">

# sec-policy - SECURITY.md definieren und prüfen

Die Richtlinie legt fest, was in diesem Repo als Schwachstelle zählt. `sec-triage` stuft Funde gegen sie ein (Vertrag `sec-scan/references/contract.md` §2: `triaged` = Severity und Priorität gegen die Richtlinie entschieden). Ohne Richtlinie rät die Triage.

## Inhalt einer SECURITY.md

| Abschnitt | Frage, die er beantwortet |
|---|---|
| Unterstützte Versionen | welche Versionen bekommen Sicherheitsfixes? |
| Geltungsbereich | welche Komponenten, Schnittstellen, Deployments sind gemeint? |
| Ausgeschlossen | was gilt ausdrücklich nicht (Testcode, Beispiele, bekannte Einschränkungen, Angriffe die Zugriff auf das Host-System voraussetzen)? |
| Verlangte Sicherheitseigenschaften | was muss das Projekt garantieren (z. B. "keine Secrets im Repo", "Eingaben aus Netzwerk werden validiert", "Plugins laufen ohne Dateizugriff außerhalb X")? Daran misst die Triage. |
| Meldeweg | wohin melden: Platzhalter `<security-contact>`; oder GitHubs privates Melden von Schwachstellen, falls im Repo aktiviert. **Keine Adresse erfinden.** |
| Reaktionszeiten | Bestätigung, Einschätzung, Fix-Ziel - Werte vom Maintainer, nicht vom Skill; Vorschläge als solche kennzeichnen. |
| Offenlegung | koordiniert, Fristen vom Maintainer; Verweis auf `sec-writeup`. |

## Ablauf

1. **Bestand lesen:** vorhandene `SECURITY.md`, README, Abhängigkeits- und Build-Dateien, Struktur des Codes (Einstiegspunkte, Auth, Dateizugriff, Netzwerk, Plugin-Mechanismen).
2. **Behauptung gegen Befund:** jede Zusage der Richtlinie ("alle Eingaben werden validiert", "keine Telemetrie", "Versionen X.y werden gepflegt") am Code oder an Releases prüfen. Widerspruch = Fund (`sec-scan`) oder Korrektur der Richtlinie, nie stilles Ignorieren. Was sich nicht prüfen lässt: als ungeprüft markieren.
3. **Entwurf oder Diff:** neue SECURITY.md bzw. Änderungsvorschlag mit offenen Punkten (`<...>`-Platzhalter) für Maintainer-Entscheidungen. Fehlt eine Antwort, Frage stellen statt raten.
4. **Ablage:** Entwurf im Chat oder im Scan-Verzeichnis. In das Repo wird nur auf direkten Nutzerauftrag geschrieben (Lock prüfen, Regel 2; kein Commit/Push, Regel 3). Die Datei enthält nie Geheimnisse, Hostpfade oder private Kontakte (Regel 4).

## Abgrenzung

Technische Härtungsvorschläge: `sec-hardening`. Prüfung der Veröffentlichungsreife eines Repos: `repo-publish-check`.

## Changelog

### 0.1.0 (2026-10-31)
- Erstfassung.
