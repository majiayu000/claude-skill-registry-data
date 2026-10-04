---
name: think
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "Problem solving and analysis: Structured thinking processes for complex problems. Divide & Conquer, Root Cause Analysis, SWOT, Pareto, and decision heuristics."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="think banner">

# Think — Problemloesung & Analyse

> Strukturierte Denkprozesse fuer komplexe Probleme

---

## Problemloesungs-Ansaetze

### 1. Divide & Conquer

```
Problem -> Teilprobleme -> Loese einzeln -> Kombiniere
```

### 2. Root Cause Analysis

```
Symptom -> Warum? -> Warum? -> Warum? -> Ursache -> Loesung
```

### 3. Constraint Relaxation

```
Unloesbares Problem -> Constraints lockern -> Loesen -> Constraints wieder anziehen
```

### 4. Analogie-Suche

```
Neues Problem -> Aehnliches bekanntes Problem -> Loesung adaptieren
```

---

## Analyse-Methoden

| Methode | Anwendung |
|---------|-----------|
| **SWOT** | Staerken/Schwaechen/Chancen/Risiken |
| **Pro/Contra** | Entscheidungsfindung |
| **Pareto** | 80/20 Priorisierung |
| **Fishbone** | Ursachenanalyse |

---

## Entscheidungs-Heuristiken

### Bei Unsicherheit

```
1. Was ist das Worst-Case-Szenario?
2. Ist es reversibel?
3. Was kostet Nicht-Handeln?
```

### Bei Komplexitaet

```
1. Was ist der einfachste erste Schritt?
2. Was wuerde ein Experte tun?
3. Was waere die 80%-Loesung?
```

---

## Changelog

### 1.0.0 (2026-03-15)
- Portiert aus BACH v3.8.0

---

*Portiert aus BACH v3.8.0 | Standalone-Version*

**Siehe auch:** [brainstorm](../brainstorm/SKILL.md) (Kreativmethoden, Ideenfindung) | [decide](../decide/SKILL.md) (Entscheidungs-Frameworks)
