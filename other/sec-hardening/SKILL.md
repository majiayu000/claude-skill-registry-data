---
name: sec-hardening
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Leitet aus Funden, Vorfallberichten oder Assessments strukturelle Härtungsvorschläge ab statt Einzelpatches: Ursachen bündeln, Vorher/Nachher-Architekturbild (ASCII), Alternativen mit Abwägung (Aufwand, Risiko, Wirkung), Umsetzungsreihenfolge, Evidenz je Vorschlag. Liefert ein Dokument und ändert keinen Code. Auslöser: 'wie härten wir das grundsätzlich', 'warum tauchen immer wieder solche Funde auf', 'Architektur sicherer machen', 'Maßnahmenplan aus dem Vorfall'. Nicht für den Fix eines einzelnen Fundes (sec-fix) und nicht für akute Abwehr (protection-shield)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, hardening, architecture, root-cause]
language: de
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-hardening banner">

# sec-hardening - strukturell statt Stück für Stück

Wiederholen sich Funde derselben Klasse, liegt die Ursache meist in der Struktur (fehlende zentrale Validierung, ungeprüfte Vertrauensgrenze, Geheimnisse im Code). Dieser Skill schlägt Änderungen auf dieser Ebene vor. Vertrag: `sec-scan/references/contract.md` (Funde §1/§2, Regel 4 Geheimnisse, Regel 5 Kosten).

## Eingabe

`findings.json` (idealerweise `validated` oder weiter), Vorfallberichte, Assessments, `threatmodel.md` und das Wissen über den Code. Ohne belegte Eingabe keine Vorschläge; Annahmen als solche kennzeichnen.

## Ablauf

1. **Ursachen bündeln:** Funde nach Wurzel gruppieren (nicht nach Datei): z. B. "jede Route baut SQL selbst", "Zugriffsprüfung in jedem Handler einzeln", "Konfiguration enthält Geheimnisse". Je Gruppe die Fund-ids nennen.
2. **Ist-Architektur skizzieren** als ASCII-Bild: Vertrauensgrenzen, Datenfluss, wo die Prüfung heute (nicht) stattfindet.
3. **Optionen je Ursache** (mindestens zwei, inklusive "nur Einzelpatches"): Beschreibung, **Aufwand**, **Risiko der Umsetzung** (Regressionen, Migration), **Wirkung** (welche Fundklasse verschwindet, welche bleibt), Abhängigkeiten. Als Tabelle.
4. **Empfehlung** pro Ursache mit Begründung und **Soll-Bild** (ASCII) im Vergleich zum Ist-Bild.
5. **Reihenfolge:** was zuerst, weil es mehrere Funde auf einmal schließt oder Voraussetzung für anderes ist; was kann warten. Zwischenschritte, die einzeln auslieferbar sind.
6. **Evidenz je Vorschlag:** Fund-ids, Codestellen (`pfad:zeile`), Messwerte. Ein Vorschlag ohne Beleg wird als Hypothese markiert. Keine erfundenen Aufwandsangaben in Zeit; nur relativ (klein/mittel/groß) oder vom Nutzer vorgegeben.

## Ausgabe

Ein Dokument (z. B. `hardening.md` im Scan-Verzeichnis oder im Chat), Abschnitte: Ausgangslage, Ursachen, Ist/Soll-Bilder, Optionen, Empfehlung, Reihenfolge, offene Fragen. **Ändert keinen Code**, legt keine Patches an und committet nichts (Regel 3); Umsetzung einzelner Schritte läuft über `sec-fix` bzw. normale Entwicklung. Keine Geheimnis-Werte im Dokument (Regel 4).

## Changelog

### 0.1.0 (2026-10-31)
- Erstfassung.
