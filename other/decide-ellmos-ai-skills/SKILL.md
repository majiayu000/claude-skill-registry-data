---
name: decide
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "Structured decision making: Pro/Con matrix, weighted scoring, decision tree, scenario analysis, and Eisenhower matrix."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [decision, evaluation, prioritization, framework]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/decide.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="decide banner">

# Decide — Strukturierte Entscheidungsfindung

> Rationale Entscheidungen durch strukturierte Frameworks und Bewertungsmethoden

---

## Wann nutzen?

- Zwischen Optionen entscheiden
- Pro/Con Liste braucht
- Mehrkriterien-Entscheidung
- Unsicher bei wichtigen Entscheidungen

**Trigger-Woerter:** entscheiden, waehlen, vergleichen, evaluieren, abwaegen

---

## Frameworks

### 1. Pro/Con Matrix (einfach)

Schnelle Entscheidungen zwischen 2 Optionen.

```
PRO A:                    CON A:
- Vorteil 1               - Nachteil 1
- Vorteil 2               - Nachteil 2

PRO B:                    CON B:
- Vorteil 1               - Nachteil 1
- Vorteil 2               - Nachteil 2

Empfehlung: [A/B] weil [Begruendung]
```

---

### 2. Weighted Scoring (komplex)

Multi-Kriterien Entscheidungen mit Gewichtung.

| Kriterium | Gewicht | Option A | Score A | Option B | Score B |
|-----------|---------|----------|---------|----------|---------|
| Kriterium 1 | 30% | 8 | 2.4 | 6 | 1.8 |
| Kriterium 2 | 25% | 7 | 1.75 | 9 | 2.25 |
| TOTAL | 100% | - | X.XX | - | X.XX |

**Prozess:**
1. Kriterien sammeln
2. Gewichte festlegen (Summe = 100%)
3. Optionen bewerten (1-10 Skala)
4. Scores berechnen (Bewertung x Gewicht)
5. Vergleichen und empfehlen

---

### 3. Decision Tree (sequenziell)

Entscheidungen mit klaren Wenn-Dann-Pfaden:
1. Start-Frage definieren
2. Erste Verzweigung (wichtigstes Kriterium)
3. Naechste Ebene (zweitwichtigstes)
4. Bis zu finaler Option

---

### 4. Scenario Analysis (Unsicherheit)

```
Best Case (X% Wahrscheinlichkeit):
  Ergebnis: +Y Punkte -> Erwartungswert: +Z

Realistic Case (X%):
  Ergebnis: +Y -> Erwartungswert: +Z

Worst Case (X%):
  Ergebnis: -Y -> Erwartungswert: -Z

Gesamt-Erwartungswert: [Summe]
```

---

### 5. Eisenhower Matrix (Priorisierung)

```
              DRINGEND        NICHT DRINGEND
WICHTIG       1. TUN          2. PLANEN
NICHT WICHTIG 3. DELEGIEREN   4. ELIMINIEREN
```

---

## Quality Checklist

Vor finaler Empfehlung pruefen:
- [ ] Alle relevanten Kriterien identifiziert?
- [ ] User-Werte beruecksichtigt?
- [ ] Langfristige Auswirkungen bedacht?
- [ ] Risiken identifiziert und bewertet?
- [ ] Bias-Check durchgefuehrt?
- [ ] Reversibilitaet geprueft?

---

## Best Practices

### Kriterien definieren
- Spezifisch und messbar
- Nicht zu viele (3-7 ideal)
- Unabhaengig voneinander

### Gewichtung
- Summe = 100%
- Wichtigstes Kriterium >= 25%
- Keine Gewichte < 5%

### Empfehlung
- Klar und begruendet
- Alternativen erwaehnen
- Risiken benennen
- Reversibilitaet beachten

---

## Workflow

```
1. User Request
2. Entscheidung verstehen
3. Optionen identifizieren (2-5)
4. Framework waehlen
5. Kriterien sammeln
6. Framework anwenden
7. Bias-Check (optional)
8. Empfehlung aussprechen
9. Reasoning dokumentieren
```

---

## Changelog

### 1.0.0 (2026-03-15)
- Portiert aus BACH v3.8.0

---

*Portiert aus BACH v3.8.0 | Standalone-Version*

**Siehe auch:** [think](../think/SKILL.md) (Analyse, Root Cause, SWOT) | [brainstorm](../brainstorm/SKILL.md) (Kreativmethoden, Ideenfindung) | [decision-shot](../decision-shot/SKILL.md) (die Ausgabe dieser Analyse auf eine executive Kurzform mit Empfehlung und Link zur Vollversion verdichten)
