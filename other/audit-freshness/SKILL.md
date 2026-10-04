---
name: audit-freshness
description: Prüft alle Themen-Factsheets auf veraltete Daten und erstellt eine priorisierte Aktualisierungsliste. Verwenden für regelmäßige Datenpflege, nach längerer Pause oder wenn unklar ist, welche Themen ein Update brauchen.
allowed-tools: Read, Glob, Grep, WebSearch, Agent, Bash(node *)
---

# Daten-Frische-Audit über alle Themen

Read-only-Analyse: Dieser Skill ändert keine Inhalte. Ergebnis ist eine priorisierte Liste von Update-Kandidaten; die Umsetzung erfolgt anschließend per `/update-topic {topicId}`.

## Bestandsaufnahme (live)

Alle Themen nach `lastUpdated` (älteste zuerst):

!`node -e 'const fs=require("fs");fs.readdirSync("public/data").filter(f=>f.endsWith(".json")&&f!=="topics.json").map(f=>JSON.parse(fs.readFileSync("public/data/"+f,"utf8"))).sort((a,b)=>String(a.lastUpdated).localeCompare(String(b.lastUpdated))).forEach(d=>console.log(d.lastUpdated+"  "+d.id))'`

## Ablauf

### 1. Alters-Triage

Nach `lastUpdated` einordnen:
- **> 18 Monate**: prioritär prüfen
- **12–18 Monate**: prüfen
- **< 12 Monate**: nur prüfen, wenn Schritt 2 zeitkritische Angaben findet

### 2. Zeitgebundene Angaben scannen

Jedes Kandidaten-JSON auf Inhalte prüfen, die unabhängig vom Dateialter veralten:

- Konkrete Jahreszahlen in Fakten und Antworten („2024 war …", „Stand 2025")
- Preise, Fördersätze, Regelsätze, Steuerbeträge (ändern sich meist jährlich)
- Prognosen, deren Zieljahr erreicht oder überschritten ist
- Regulatorik mit Stichtagen (Gesetzesfahrpläne in `timeline`-Blöcken)
- Formulierungen wie „aktuell", „derzeit", „in diesem Jahr"

### 3. Stichprobenprüfung gegen neuere Daten

Für die prioritären Kandidaten per WebSearch (parallele Explore-Subagents) prüfen, ob die Herausgeber der referenzierten Quellen inzwischen neuere Ausgaben publiziert haben (z. B. Folgejahres-Statistik, aktualisierte Studienlage). Nur Existenz und Größenordnung der Abweichung feststellen — die vollständige Verifizierung übernimmt später `/update-topic`.

### 4. Priorisierter Bericht

```
# Daten-Frische-Audit ({Datum})

## Prioritär aktualisieren
| Topic | lastUpdated | Grund | Betroffene Stellen | Neuere Quelle |
|-------|-------------|-------|--------------------|---------------|
| {id}  | {datum}     | {z. B. Regelsatz 2026 veröffentlicht} | {section-ids, argument-ids} | {url/Publikation} |

## Beobachten (noch aktuell, aber zeitkritisch)
...

## Aktuell (keine Aktion)
...

Empfehlung: /update-topic {topicId} für die prioritären Kandidaten, beginnend mit {id}.
```

## Regeln

- **Read-only** — keine Änderungen an `public/data/`; Umsetzung ausschließlich über `/update-topic`
- **Kein Vollabgleich** — dieser Skill stellt Update-Bedarf fest, er verifiziert keine einzelnen Zahlen
- **Priorität nach Wirkung** — Themen mit falsch gewordenen highlight-Fakten oder keyStats vor Themen mit bloß gealterten Randdaten
