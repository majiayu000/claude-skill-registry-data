---
name: condition
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-25
updated: 2026-07-28
description: >
  Flexible Bedingungssprache für Ziele, Prompts und Aufträge. Übersetzt Bedingungen,
  Zeitpunkte und Reihenfolge-Abhängigkeiten in prüfbare Gates, damit ein Teilschritt erst
  nach belegter Freigabe ausgeführt wird. Immer verwenden bei /condition, /if, /if-only,
  /when, /after, /and oder /or sowie bei Formulierungen wie "erst wenn", "sobald",
  "nur falls", "nachdem", "warte bis", "danach" oder "vorher nicht". Auch verwenden,
  wenn mehrere Teilziele voneinander abhängen oder ein Goal eine spätere Freigabe enthält.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [condition, gate, prompt-language, goal, trigger, blocker, timing, dependency, workflow]
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
  origin_path: "condition/SKILL.md"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="condition banner">
# condition — Bedingungssprache für Ziele und Prompts

## Leitidee

Fließtext-Bedingungen leicht übersehen. Deshalb jede relevante Bedingung in ein benanntes,
prüfbares Gate übersetzen:

> Beim Lesen großzügig, beim Belegen unnachgiebig.

Die Eingabe darf natürlichsprachlich und unvollständig sein. Die interne Übersetzung muss
dagegen eindeutig festhalten:

1. welche Bedingung erfüllt sein muss,
2. welcher Teilschritt blockiert ist,
3. welche Werkzeugabfrage als Beleg gilt,
4. ob Nichterfüllung Verzögerung oder Verbot bedeutet.

Nur den betroffenen Teilschritt sperren. Unabhängige Arbeit fortsetzen.

## Sprachbausteine

| Ausdruck | Semantik | Beispiel |
| --- | --- | --- |
| `/condition <Bedingung> -> <Schritt>` | Kanonisches Gate | `/condition Tests grün -> Release bauen` |
| `/if <Bedingung> -> <Schritt>` | Synonym für `/condition` | `/if Review abgeschlossen -> mergen` |
| `/when <Bedingung> -> <Schritt>` | Ausführen, sobald die Bedingung eintritt | `/when Export fertig -> Bericht prüfen` |
| `/if-only <Bedingung> -> <Schritt>` | Nur bei Erfüllung; sonst gar nicht ausführen | `/if-only Backup belegt -> Altbestand löschen` |
| `/after <Dauer> -> <Schritt>` | Zeitversatz ab dem Setzzeitpunkt | `/after 30 minutes -> Status prüfen` |
| `/and` | Alle verknüpften Bedingungen müssen gelten | `/if Tests grün /and Review da -> mergen` |
| `/or` | Mindestens eine Bedingung genügt | `/if Freigabe da /or Notfallregel aktiv -> starten` |

Nummerierte Bedingungen wie `/condition 1 ...` und `/condition 2 ...` verwenden, wenn ein
Prompt mehrere Gates enthält. Bei gemischtem `/and` und `/or` keine stillschweigende
Operatorrangfolge erfinden: Klammern oder nummerierte Teilbedingungen verwenden. Bei
weiterhin mehrdeutiger Bedeutung nachfragen, bevor ein riskanter Schritt freigegeben wird.

`/if-only` als Verbot behandeln. Kann die Bedingung nicht belegt werden, den Schritt nicht
ausführen. Bei unklarer Formulierung und irreversiblen Folgen die strengere Lesart wählen.

## Ablauf

### 1. Bedingung normalisieren

Die Eingabe in einen prüfbaren Satz übersetzen. Relative Zeiten beim Setzen in einen absoluten
Zeitpunkt mit Zeitzone umrechnen.

| Eingabe | Normalisierte Bedingung | Belegklasse |
| --- | --- | --- |
| `time 06:00` | Systemzeit ist mindestens 06:00 in der vereinbarten Zeitzone | Uhr-/Zeitwerkzeug |
| `after 2 hours` | Systemzeit ist mindestens Setzzeitpunkt plus zwei Stunden | Uhr-/Zeitwerkzeug |
| `wenn Worker A fertig ist` | Abnahmeartefakt oder Taskstatus von A zeigt Abschluss | Task-/Dateiwerkzeug |
| `wenn Tests grün sind` | Vorgeschriebener Testlauf endet erfolgreich | Prozess-/Testwerkzeug |
| `nach dem Push` | Ziel-Remote enthält den vorgesehenen Commit | Versionskontrollwerkzeug |
| `wenn der User zustimmt` | Explizite Zustimmung liegt in der Konversation vor | Nutzereingabe |

Ist kein objektiver Belegweg erkennbar, das offen benennen. Kein Gate so formulieren, dass es
nur durch Vermutung geschlossen werden kann.

### 2. Gate-Zustand festhalten

Wenn ein persistenter Gate-, Task- oder Memory-Store verfügbar ist, dort mindestens diese
Felder speichern:

```text
id
condition
blocks
mode = wait | only
proof_method
status = open | met | dropped
created_at
evidence
```

Existiert kein persistenter Store, den Zustand sichtbar im aktuellen Goal, Taskplan oder
Übergabedokument führen. Nur dann behaupten, dass ein Gate Sessions überlebt, wenn der
verwendete Speicher tatsächlich dauerhaft ist.

Ein vorhandener Runtime-Adapter darf andere Befehlsnamen verwenden. Funktional braucht er:
`open`, `list`, `meet` und `drop` oder gleichwertige Operationen.

### 3. Arbeit umsortieren

Ein offenes Gate blockiert nicht den gesamten Auftrag. Alle unabhängigen Schritte ausführen
und vor dem nächsten abhängigen Schritt den Gate-Zustand erneut prüfen.

Nicht aktiv in kurzen Agentenschleifen pollen. Für längere Wartezeiten einen Scheduler,
Hintergrundjob oder ein Ereignis verwenden, das bei Eintritt einmalig meldet. Nach dem
Wecksignal die eigentliche Bedingung trotzdem erneut mit dem vorgesehenen Werkzeug belegen.

### 4. Streng prüfen und schließen

Erst die Werkzeugabfrage ausführen, dann das Gate mit konkreter Evidenz schließen. Geeignete
Belege sind zum Beispiel:

- Zeit: gemessener Zeitstempel mit Zeitzone,
- Datei: Pfad, Metadaten oder Hash des erwarteten Artefakts,
- Tests: ausgeführter Befehl, Exit-Code und relevante Zusammenfassung,
- Repository: Branch, Commit-ID und Remote-Abgleich,
- Prozess oder Task: stabile ID und gemessener Endstatus,
- Zustimmung: eindeutige Nutzerantwort im aktuellen Kontext.

Eine Schätzung, ein erwarteter Zustand oder die bloße Behauptung eines anderen Workers genügt
nicht, wenn ein unabhängiger Beleg verfügbar sein sollte.

Ist ein Gate durch Auftragsänderung hinfällig, es mit Begründung als `dropped` markieren. Bei
`/or` die nicht mehr benötigten Alternativen ebenfalls schließen oder verwerfen, damit keine
Zombie-Gates verbleiben.

### 5. Eskalieren

Wenn alle unabhängigen Schritte erledigt sind:

1. prüfen, ob die blockierende Vorarbeit innerhalb des Auftrags aktiv erledigt werden kann,
2. bei reiner Wartebedingung einen passenden Scheduler oder Hintergrundjob verwenden,
3. bei Nutzerentscheidung oder externer Abhängigkeit mit offenem Gate und klarem Zwischenstand
   übergeben.

Keine zusätzliche Berechtigung aus einer Bedingung ableiten. Ein erfülltes Gate ändert nur die
Reihenfolge; es erweitert nicht den autorisierten Umfang des Auftrags.

## Beispiele

### Goal mit Zeitbedingung

```text
Ziel: Daten prüfen und Bericht veröffentlichen.
/condition time 16:00 Europe/Berlin -> Veröffentlichung starten
```

Die Datenprüfung darf vorher stattfinden. Die Veröffentlichung bleibt gesperrt, bis eine
aktuelle Zeitabfrage mindestens 16:00 Uhr belegt.

### Prompt mit mehreren Bedingungen

```text
/condition 1 Tests erfolgreich
/condition 2 Review freigegeben
/if condition 1 /and condition 2 -> mergen
```

Beide Gates getrennt belegen. Erst danach mergen.

### Verbot statt Verzögerung

```text
/if-only verifiziertes Backup vorhanden -> alte Dateien löschen
```

Ohne belegtes Backup nichts löschen und das offene Verbot im Abschlussbericht nennen.

## Fallstricke

- Bedingung nur im Fließtext wiederholen, statt sie als Zustand zu führen.
- Ein gesamtes Goal pausieren, obwohl nur ein Teilschritt blockiert ist.
- Relative Zeit ohne Setzzeitpunkt und Zeitzone speichern.
- Werkzeugbeleg durch Annahme oder Selbstauskunft ersetzen.
- `/if-only` wie ein bloßes Warten behandeln.
- Nach `/or` nicht mehr benötigte Alternativ-Gates offen lassen.
- Anbieter-, Modell-, Benutzer- oder Hostnamen in die allgemeine Mechanik einbauen.
- Einen lokalen Runtime-Pfad als Voraussetzung für die Sprache selbst behandeln.

## Changelog

### 1.1.0 (2026-07-28)

- Anbieter-, benutzer- und systemneutral für gemeinsame Skill-Runtimes formuliert.
- Nutzung in Goals und Prompts explizit gemacht.
- Runtime als austauschbaren Adapter beschrieben; feste lokale Pfade und Modellnamen entfernt.
- Mehrdeutige `/and`-/`/or`-Verknüpfungen, dauerhafte Zustände und Autorisierungsgrenzen geklärt.

### 1.0.0 (2026-07-25)

- Erste Fassung mit `/condition`, `/if`, `/if-only`, `/when`, `/after`, `/and` und `/or`.
