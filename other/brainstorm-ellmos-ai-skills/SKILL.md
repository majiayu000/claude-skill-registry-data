---
name: brainstorm
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "Structured creativity methods for idea generation: SCAMPER, Six Thinking Hats, Mind Mapping, Reverse Brainstorming, TRIZ, and Rapid Ideation."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [brainstorm, creativity, ideation, scamper, six-hats, innovation]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/brainstorm.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="brainstorm banner">

# Brainstorm

> Strukturierte Kreativitaet fuer Innovation — SCAMPER, Six Hats, Mind Mapping, Reverse Brainstorming, TRIZ, Rapid Ideation

---

## Wann nutzen?

- Neue Ideen gebraucht
- Festgefahren / Kreativitaetsblockade
- Innovation gesucht
- Problem kreativ loesen

**Trigger-Woerter:** brainstorm, ideen, kreativ, innovativ, ideenfindung

---

## Methoden

### 1. SCAMPER

**Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse**

Bestehende Loesungen systematisch verbessern:
- **S**ubstitute: Was kann ersetzt werden?
- **C**ombine: Was kann kombiniert werden?
- **A**dapt: Was kann angepasst werden?
- **M**odify: Was kann veraendert werden?
- **P**ut to other use: Wofuer sonst nutzen?
- **E**liminate: Was kann weggelassen werden?
- **R**everse: Was kann umgekehrt werden?

---

### 2. Six Thinking Hats (Edward de Bono)

6 Perspektiven systematisch durchdenken:

- **White Hat — Fakten:** Welche Informationen haben wir? Was fehlt?
- **Red Hat — Emotion:** Wie fuehlt sich das an? Intuition, Bauchgefuehl
- **Black Hat — Kritik:** Was koennte schiefgehen? Risiken, Schwaechen
- **Yellow Hat — Optimismus:** Was sind die Chancen? Best Case
- **Green Hat — Kreativitaet:** Neue Ideen? Out-of-the-box?
- **Blue Hat — Meta:** Prozess-Kontrolle, Zusammenfassung, naechste Schritte

**Prozess:** Problem definieren (Blue) -> Fakten (White) -> Emotionen (Red) -> Kritik (Black) -> Positives (Yellow) -> Neue Ideen (Green) -> Zusammenfassen (Blue)

---

### 3. Mind Mapping

Gedanken hierarchisch visualisieren:
1. Zentrales Thema
2. Haupt-Aeste (3-7)
3. Sub-Aeste fuer jede Kategorie
4. Details und Ideen hinzufuegen
5. Verbindungen erkennen

---

### 4. Reverse Brainstorming

Problem umkehren: "Wie machen wir es SCHLIMMER?"

1. Problem umkehren
2. Schlechte Ideen sammeln
3. Umkehren = Gute Ideen

Besonders gut wenn direkte Ideenfindung stockt.

---

### 5. TRIZ (Theory of Inventive Problem Solving)

Top 10 Principles fuer Software:
1. **Segmentation:** Teile Monolith in Module
2. **Extraction:** Isoliere stoerende Eigenschaft
3. **Local Quality:** Verschiedene Komponenten, verschiedene Eigenschaften
4. **Merging:** Kombiniere aehnliche Funktionen
5. **Universality:** Ein Element, mehrere Funktionen
6. **Nesting:** Komponenten ineinander
7. **Preliminary Action:** Vorbereitung im Voraus
8. **Feedback:** Monitoring und Anpassung
9. **Self-Service:** System wartet sich selbst
10. **Asymmetry:** Nicht-symmetrische Designs

---

### 6. Rapid Ideation

Quantitaet vor Qualitaet — 50+ Ideen in 20 Min.

**Regeln:**
- KEINE Kritik waehrend Ideation
- WILDE Ideen willkommen
- Auf Ideen anderer aufbauen
- Quantitaet FIRST

**Timer-basiert:**
- Runde 1 (5 Min): Offene Ideation
- Runde 2 (5 Min): Variationen
- Runde 3 (5 Min): Kombinationen
- Runde 4 (5 Min): Extreme Ideen

---

## Workflow

```
1. User Request
2. Ziel verstehen
3. Methode(n) waehlen
4. Ideen generieren (keine Kritik!)
5. Clustering
6. Feasibility/Impact Matrix
7. Top 5-10 Auswahl
8. Output + Empfehlung
```

---

## Changelog

### 1.0.0 (2026-03-15)
- Portiert aus BACH v3.8.0

---

*Portiert aus BACH v3.8.0 | Standalone-Version*

**Siehe auch:** [think](../think/SKILL.md) (Analyse, Root Cause, SWOT) | [decide](../decide/SKILL.md) (Entscheidungs-Frameworks)
