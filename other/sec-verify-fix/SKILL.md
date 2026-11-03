---
name: sec-verify-fix
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Prüft unabhängig, ob ein Sicherheitspatch die Schwachstelle wirklich schließt (Source-to-Sink-Pfad am gepatchten Stand erneut verfolgen, Negativ- und Regressionstest), bewertet das Regressionsrisiko und ob automatisches Mergen vertretbar wäre (Standard: nein bei critical/high). Nur lesend und prüfend, wendet nichts an. Auslöser: 'schließt der Patch die Lücke', 'Patch prüfen', 'Fix verifizieren', Status fixed vorhanden. Nicht zum Schreiben des Patches (sec-fix), nicht für allgemeines Code-Review."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, patch, review, verification, regression]
language: de
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-verify-fix banner">

# sec-verify-fix - schließt der Patch die Lücke?

Phase "verify-fix". Vertrag: `sec-scan/references/contract.md` (Lebenszyklus §2, Regel 7 in §6). Setzt einen Fund mit Status `fixed` und `fix.patchFile` voraus.

## Unabhängigkeit zuerst

Der Prüfer ist **nicht** der Patch-Autor (Regel 7): möglichst anderer Anbieter (Claude <-> Codex), sonst ein unabhängiger Subagent der höchsten Stufe mit frischem Kontext, der nur Fund, Patch und Code bekommt - nicht die Begründung des Autors. Wer es dennoch selbst prüfen muss, sagt das im Ergebnis; `verifiedBy` bleibt dann leer und der Status `fixed`.

## Ablauf

1. **Patch in Scratch-Kopie anwenden** (nie im Original); Lock prüfen wie in `sec-fix` (Regel 2). Lässt sich der Patch nicht sauber anwenden, ist das bereits das Ergebnis.
2. **Pfad erneut verfolgen:** den ursprünglichen Source-to-Sink-Pfad aus `evidence` am gepatchten Stand Zeile für Zeile durchgehen. Ist die Senke weiter erreichbar? Gibt es Parallelpfade (andere Aufrufer, Varianten der Eingabe, andere Kodierung), die der Patch nicht abdeckt?
3. **Negativtest:** eine minimale, nicht einsatzfähige Eingabe, die den Fund vorher ausgelöst hätte, muss jetzt abgewiesen oder neutralisiert werden. Nur in der Scratch-Kopie, nur gegen eigenen Code (Regel 1). Ist ein Test nicht sinnvoll ausführbar, als "nicht getestet" ausweisen.
4. **Regressionstest:** Projekttests vorher/nachher; legitime Eingaben laufen weiter. Rote oder nicht gelaufene Tests nennen.
5. **Regressionsrisiko bewerten:** betroffene Laufzeitpfade und Aufrufer, geänderte Verträge (Signaturen, Formate, Fehlerverhalten), Testabdeckung der Stelle, Rückrollbarkeit (reiner Codepatch vs. Datenmigration/Konfiguration). Stufe niedrig/mittel/hoch mit Gründen.
6. **Automatisches Mergen?** ja/nein mit Gründen. **Standard nein bei critical/high**; ja nur, wenn Pfad geschlossen, Negativ- und Regressionstest grün, Risiko niedrig und Rückroll einfach. Entscheidet nie allein der Prüfer; Merge-Regeln des Repos gehen vor.

## Ergebnis

- **Schließt:** ja / teilweise / nein, mit der konkreten Stelle, die offen bleibt. Bei "nein"/"teilweise" bleibt der Status `fixed` und es geht zurück zu `sec-fix`; der Fund wird nicht verworfen.
- **Bei "ja":** `status: verified`, `fix.verifiedBy: "<provider>/<model>"` und `python scripts/secfind.py validate findings.json coverage.json` (Skript in `sec-scan`). Begründung, Risikostufe und Merge-Empfehlung stehen im Bericht an den Nutzer; der Vertrag kennt dafür kein eigenes Feld, also keines erfinden.
- Wendet nichts an, committet und pusht nichts (Regel 3).

## Changelog

### 0.1.0 (2026-10-31)
- Erstfassung.
