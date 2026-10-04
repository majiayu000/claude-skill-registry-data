---
name: rotation-check
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-03
description: >
  Standard-Gerüst für rotierende Pipeline-Checks: Pro Lauf genau ein Ziel aus einer Menge
  (Projekte, Ordner, Repos) wählen — bevorzugt das am längsten ungeprüfte —, den Check
  durchführen, Ergebnis in einer Check-Registry und einem Verlaufslog festhalten. Nutze
  diesen Skill, wenn ein wiederkehrender Check über viele Projekte verteilt werden soll
  („prüfe regelmäßig alle X auf Y"), wenn eine Automatisierung Doppelprüfungen vermeiden
  muss, wenn eine Check-Registry/CHECKS-LOG-Struktur angelegt oder benutzt wird, oder wenn
  eine periodische Qualitätsrunde (Quellencheck, Style-Check, Health-Check, Audit) über
  eine Pipeline fair verteilt werden soll.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [automation, check, rotation, registry, pipeline, log, audit, wartung]
language: de
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="rotation-check banner">
# Rotation-Check — ein Ziel pro Lauf, faire Abdeckung, Gedächtnis

## Zweck

Wer eine Pipeline mit vielen Projekten periodisch prüfen will (Quellen, Stil, Gesundheit,
Sicherheit, Übersetzungen, …), steht vor einem Verteilungsproblem: Alle Projekte pro Lauf zu
prüfen ist zu teuer; ohne Gedächtnis prüft jeder Lauf zufällig dasselbe. Das Rotations-Muster
löst beides: **genau ein Ziel pro Lauf, Auswahl nach „am längsten ungeprüft", Registry als
Gedächtnis.** So deckt auch ein seltener Takt (täglich/wöchentlich) über Wochen die ganze
Pipeline ab — nachweisbar und ohne Doppelarbeit.

Bewährt als Rückgrat eines gewachsenen Bestands produktiver Automationen über mehrere
Projekt-Pipelines hinweg.

## Bausteine

### 1. Zwei Dateien pro Pipeline (einmalig anlegen)

| Datei | Inhalt | Charakter |
| --- | --- | --- |
| `CHECKED-REGISTRY.md` | eine Kompaktzeile pro Check: Ziel, Datum, Checktyp, Ergebnis, nächster Schritt | Zustandsübersicht — wird VOR jeder Zielauswahl gelesen |
| `CHECKS-LOG.txt` | kurzer Verlaufseintrag pro Lauf mit Details/Evidenz | Journal — append-only |

Beide liegen im Pipeline-Root (nicht im Einzelprojekt), damit ein Lauf sie mit einem Read
erfassen kann. Registry-Zeilenformat:

```text
| <ziel> | <YYYY-MM-DD> | <checktyp> | <ok|befund|übersprungen> | <nächster schritt> |
```

### 2. Auswahlregel

1. Registry und Log lesen (Pflicht, VOR der Auswahl — sonst Doppelprüfung).
2. Kandidaten: Ziele, die für DIESEN Checktyp noch nie oder am längsten nicht geprüft wurden.
3. Ausweichen, wenn das Ziel kürzlich von einem **eng verwandten** Check angefasst wurde
   (z. B. Zitations-Check direkt nach Quellencheck bringt nichts) oder gerade gesperrt/in
   Bearbeitung ist (Locks respektieren).
   **Geschwister-Cooldown:** Laufen mehrere verwandte Checks über dieselbe Zielmenge
   (z. B. Entwicklung, Bugsuche und Review derselben Pipeline), eine Karenzzeit vereinbaren
   (Erfahrungswert: ~24 h), in der ein von einem Geschwister-Check bearbeitetes Ziel nicht
   erneut gewählt wird — verhindert Kollisionen und widersprüchliche Parallel-Änderungen.
4. Vorziehen außer der Reihe nur mit gutem Grund (z. B. große Überarbeitung seit letztem
   Check) — den Grund im Log nennen.

### 3. Check durchführen — mit Read-only-Exit

Den eigentlichen Check (frei definierbar: Quellencheck, Style-Check, Security-Audit, …)
auf das EINE gewählte Ziel anwenden. Zwei gültige Ausgänge:

- **Befund:** beheben was in den Scope passt; Größeres als Folgeaufgabe in die projektlokale
  TODO/AUFGABEN-Datei eintragen (der Check muss nicht alles selbst lösen).
- **Nichts zu tun:** kurz dokumentieren und enden. Ein Leerlauf ist ein Ergebnis, kein
  Scheitern — keinesfalls den Scope ausweiten, um „etwas gefunden zu haben".

### 4. Dokumentieren

- Registry-Zeile ergänzen (kompakt), Log-Eintrag schreiben (Details/Evidenz).
- **Log-Hygiene:** Werden Registry/Log unübersichtlich (Erfahrungswert: mehrere hundert
  Zeilen), alten Stand nach `_archiv/` verschieben, frische Datei anlegen, im Kopf auf den
  Vorgänger verweisen (Pfad + Datum).
- **Pfad-Drift:** Zeigt ein erwarteter Pfad ins Leere (Ziel verschoben/umbenannt), NICHT neu
  anlegen — über die maßgebliche Statusdatei/Registry der Pipeline korrigieren und den
  Fehlpfad in einem Failure-Log festhalten.

### 5. Takt

Frequenz an die Änderungsrate des Geprüften koppeln: Rotations-Checks über stabile Bestände
laufen gut wöchentlich (ein Ziel pro Lauf ≈ ganze Pipeline pro Quartal bei ~12 Zielen);
schnelllebige Checks (z. B. auf aktive Arbeit) täglich. Praxiserfahrung: anfangs stündliche
Checks wurden fast alle auf täglich/wöchentlich reduziert — die Abdeckung blieb, die Kosten
fielen.

## Prompt-Vorlage (für Scheduler/Automation)

```text
VORBEREITUNG: Lies <PIPELINE_ROOT>/<POLICY-DOKUMENTE> sowie <REGISTRY> und <LOG>.

AUFGABE: Wähle genau ein Ziel aus <ZIELMENGE>. Bevorzuge Ziele, die für den Check
"<CHECKTYP>" noch nie oder am längsten nicht geprüft wurden. Wurde ein Ziel kürzlich
von diesem oder einem eng verwandten Check geprüft oder ist es gesperrt: ausweichen
oder read-only mit Logeintrag enden.

CHECK: <konkrete Prüf-/Pflegeaufgabe und was bei Befund zu tun ist; Folgearbeiten in
die projektlokale TODO-Datei>.

Wenn keine Arbeit anfällt: kurz dokumentieren, Lauf beenden.

DOKUMENTATION: Registry-Zeile in <REGISTRY> (Ziel, Datum, Checktyp, Ergebnis, nächster
Schritt) + Verlaufseintrag in <LOG>. Bei Überlänge: alten Stand nach _archiv/ und
frische Datei mit Verweis.

ABSCHLUSS: Kurzbericht (Ziel | getan | Ergebnis | Folgeaufgaben).
```

## Red Flags

| Gedanke | Realität |
| --- | --- |
| „Ich wähle einfach ein interessantes Projekt" | Auswahl nur über die Registry — sonst Lieblingsprojekt-Bias und blinde Flecken. |
| „Registry lese ich nach dem Check" | Vorher. Sie ist das Auswahlkriterium, nicht nur das Protokoll. |
| „Mehrere Ziele pro Lauf schaffen mehr" | Ein Ziel hält Läufe kurz, idempotent und abbrechbar; Menge kommt über die Rotation. |
| „Der Leerlauf war umsonst" | Ein dokumentierter Leerlauf aktualisiert das Gedächtnis — das ist der halbe Wert des Systems. |

## Verwandte Skills

- `workflow-extract` — baut aus Sessions/Fremd-Automationen Automatisierungen; nutzt dieses
  Gerüst als Standard-Baustein.
- `pipeline-optimizer` — für den strukturellen Umbau einer Pipeline (Rotation-Check pflegt,
  Optimizer renoviert).

## Changelog

### 1.1.0 (2026-07-03)
- Geschwister-Cooldown als Auswahlregel ergänzt (Anti-Kollision zwischen verwandten
  Checks über dieselbe Zielmenge; Befund aus der Vollklassifikation des Automations-Bestands).

### 1.0.0 (2026-07-03)
- Initiale Version. Abstrahiert aus dem Codex-Automations-Bestand (Rotations-Muster in
  ~40 von 77 Automationen: Research-/Software-/Roblox-Checks mit CHECKED-REGISTRY/CHECKS-LOG).
