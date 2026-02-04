---
name: dara-dataset-expert
description: Warehouse-Prozess-Analyse mit 207 Labels, 47 Prozessen, 8 Szenarien, 10 Triggern. Vollständige Expertise für DaRa Datensatz + REFA-Methodik + Validierungslogik + Szenarioerkennung. 100% faktenbasiert ohne Halluzinationen.
---

# DaRa Dataset Expert Skill – Version 2.4

## Zweck

Dieser Skill ermöglicht Claude die **präzise, faktenbasierte Analyse des DaRa-Datensatzes** für intralogistische Warehouse-Prozesse. Er kombiniert die Datensatz-Dokumentation mit **arbeitswissenschaftlichen Methoden (REFA)**, formaler **Validierungslogik** und **automatischer Szenarioerkennung**.

Der Fokus liegt auf **epistemischer Integrität**: Alle Antworten basieren ausschließlich auf verifizierten Quellen ohne Halluzinationen, Spekulationen oder Annahmen.

### NEU in Version 2.4: Label-Aktivitätsanalyse

Version 2.4 erweitert den Skill um empirische Label-Aktivitätsanalyse:

- **Label-Aktivitätsmatrix** – Dokumentation aktiver/inaktiver Labels pro Kategorie
- **Inaktive Labels identifiziert** – CL104, CL109, CL113 sind in S14 nicht vorhanden
- **Multi-Label-Quantifizierung** – 44.76% der Frames haben 2+ aktive Orders (S7/S8-Detection)
- **CL135-Prävalenz** – 2.82% Error-Frames für S1/S3-Identifikation
- **Optimierte Erkennungslogik** – Inaktive Labels können übersprungen werden

### NEU in Version 2.3: Flexible Szenarioerkennung

Version 2.3 erweiterte den Skill um:

- **Merkmalbasierte Erkennung** anhand der 5 Dimensionen (CC06, CC07, CC08, Strategy, Errors)
- **Keine harten Grenzen** – funktioniert für alle 18 Subjekte ohne Frame-Nummern
- **Flexible Reihenfolge** – keine Annahme über chronologische Szenario-Abfolge
- **Order-Change-Detection** für Storage-Blöcke (S4/S5/S6-Unterscheidung)
- **Korrigierte Multi-Order-Logik** – S7 und S8 haben beide {CL100, CL101}

**Datensatz-Umfang:**

- **18 Probanden (S01-S18)** mit demografischen und Erfahrungsprofilen
- **Session-basierte Aufzeichnungen** mit 3 parallelen Subjekten pro Session
- **8 Szenarien (S1-S8)** für Retrieval- und Storage-Prozesse
- **12 Klassenkategorien (CC01-CC12)** mit insgesamt **207 Labels (CL001-CL207)**
- **REFA-Zeitarten-Mapping** ($t_{R}$, $t_{MH}$, $t_{MN}$, $t_{v}$)
- **Validierungsregeln** (Master-Slave-Abhängigkeiten + Szenario-Validierung)
- **BPMN-Prozesslogik** für Warehouse-Kommissionierung und Einlagerung

**Datensatz-Stand:** 20.10.2025 (DaRa Dataset Description)  
**Skill-Stand:** 31.12.2025 (Version 2.3)

---

## Wann diesen Skill nutzen

### ✅ Verwende diesen Skill für:

1. **Strukturelle Datensatz-Fragen**
   - "Wie viele Probanden gibt es?"
   - "Wie sind Sessions aufgebaut?"
   - "Welche Szenarien existieren?"
   - "Erkläre die Chunking-Trigger T1-T10"

2. **Klassifikations-Queries**
   - "Welche Labels gehören zu CC04 (Left Hand)?"
   - "Was ist der Unterschied zwischen CC08, CC09 und CC10?"
   - "Zeige mir alle Tool-Labels"

3. **REFA & Arbeitswissenschaft**
   - "Welche DaRa-Labels entsprechen der Haupttätigkeit ($t_{MH}$)?"
   - "Wie wird die Erholungszeit basierend auf CC03 berechnet?"
   - "Ist 'Travel Time' eine Nebentätigkeit?"
   - "Berechne die Auftragszeit für ein Szenario"

4. **Validierung & Logik**
   - "Darf man 'Walking' annotieren, wenn die Beine 'Standing Still' sind?"
   - "Welche Low-Level-Prozesse sind im Retrieval-Prozess erlaubt?"
   - "Prüfe, ob 'Scanning' ohne Scanner-Tool möglich ist."
   - "Welche Abhängigkeiten bestehen zwischen CC01 und CC09?"

5. **Prozess-Logik-Analysen**
   - "Erkläre den Retrieval-Pfad im BPMN"
   - "Was passiert nach 'Picking Pick Time'?"
   - "Welche Entscheidungspunkte gibt es im Storage-Prozess?"

6. **Datenstruktur-Fragen**
   - "Wie sind Frames synchronisiert?"
   - "Wie viele Klassendateien hat jedes Subjekt?"
   - "Wie werden Szenarien zeitlich abgegrenzt?"

7. **Label-Lookups**
   - "Was bedeutet CL115?"
   - "In welcher Kategorie ist 'Portable Data Terminal'?"
   - "Alle Labels für Locations"

8. **🆕 Szenarioerkennung** (verbessert in v2.3)
   - "Wie erkenne ich die Szenario-Grenzen in den CSV-Daten?"
   - "Was unterscheidet S2 von S1 und S3?"
   - "Wie funktioniert Multi-Order-Picking?"
   - "Welche IT-Systeme werden in welchen Szenarien verwendet?"
   - "Wie validiere ich ein erkanntes Szenario?"

9. **🆕 Label-Aktivitätsanalyse** (NEU in v2.4)
   - "Welche Labels sind in S14 aktiv/inaktiv?"
   - "Wie viele Frames haben mehrere aktive Orders?"
   - "Ist CL104 (Order Unknown) jemals aktiv?"
   - "Wie erkenne ich Multi-Order-Szenarien durch Co-Aktivierung?"
   - "Wie häufig kommt CL135 (Error-Reporting) vor?"

### ❌ Nutze diesen Skill NICHT für:

- Statistische Analysen (z.B. Häufigkeitsverteilungen) → Erfordert Rohdatenverarbeitung
- Visualisierungen oder Plots → Erfordert externe Tools
- Interpretationen oder Hypothesen → Widerspricht dem Fakten-Prinzip
- Modelltraining oder ML-Code → Außerhalb des Skill-Scopes
- Bild-/Videoanalyse → Keine Videodaten im Skill

---

## Skill-Dateien & Navigation

Der Skill ist modular aufgebaut. Jede Datei deckt einen spezifischen Wissensbereich ab:

### 📁 Dateistruktur

```
/mnt/skills/user/dara-dataset-expert/
├── SKILL.md                                    # Diese Datei (Orchestrierung)
├── README.md                                   # Installation & Übersicht
├── knowledge/
│   ├── class_hierarchy.md                      # Alle 12 Kategorien + 207 Labels
│   ├── analytics_refa.md                       # REFA-Zeitarten, Formeln
│   ├── validation_logic.md                     # Basis-Abhängigkeiten
│   ├── validation_logic_extended.md            # 🔄 Szenario-Validierung (V-S1 bis V-S12)
│   ├── processes.md                            # BPMN-Logik CC08-CC10
│   ├── chunking.md                             # Trigger T1-T10
│   ├── semantics.md                            # Semantische Grundprinzipien
│   ├── scenarios.md                            # Szenarien S1-S8 (Beschreibungen)
│   ├── ground_truth_matrix.md                  # Table 3 Ground Truth
│   ├── scenario_label_states.md                # 🆕 Aktiv/Inaktiv pro Szenario (v2.4)
│   ├── picking_strategies.md                   # 🔄 Single vs. Multi-Order (korrigiert)
│   ├── scenario_boundary_detection.md          # 🔄 Erkennungsalgorithmus (überarbeitet)
│   ├── label_activity_matrix.md                # 🆕 Aktive/Inaktive Labels (v2.4)
│   ├── dataset_core.md                         # Probanden, Hardware
│   └── data_structure.md                       # Frames, Synchronisation
└── templates/
    ├── query_patterns.md                       # Häufige Fragetypen
    └── scenario_report_template.md             # Szenario-Bericht-Format
```

### 🧭 Navigationslogik

**Schritt 1: Frage klassifizieren & Datei laden**

```python
# 1. REFA / Arbeitswissenschaft / Zeiten

if "REFA" or "Zeitart" or "Erholung" or "Kalkulation" or "t_MH" or "t_R" in query:
    view("knowledge/analytics_refa.md")

# 2. Validierung / Logik / Regeln / Konsistenz

elif "Validierung" or "Logik" or "Konsistenz" or "Regel" or "Darf ich" or "gültig" in query:
    view("knowledge/validation_logic.md")
    view("knowledge/validation_logic_extended.md")

# 3. Label-Lookup / Definitionen

elif "CC" + number or "CL" + number or "Was ist" + Labelname in query:
    view("knowledge/class_hierarchy.md")

# 4. Prozess-Ablauf / BPMN

elif "Prozess" or "Ablauf" or "nach dem Schritt" or "High-Level" or "BPMN" in query:
    view("knowledge/processes.md")

# 5. Chunking / Trigger

elif "Chunk" or "Trigger" or "Segmentierung" or "T1" to "T10" in query:
    view("knowledge/chunking.md")

# 6. Szenarien (Beschreibungen)

elif "Szenario" or "S1" to "S8" in query:
    view("knowledge/scenarios.md")

# 7. Szenarioerkennung / Grenzen / Ground Truth

elif "Grenze" or "erkennen" or "Ground Truth" or "Table 3" or "Boundary" in query:
    view("knowledge/ground_truth_matrix.md")
    view("knowledge/scenario_boundary_detection.md")

# 7b. Szenario-Label-Zustände (aktiv/inaktiv pro Szenario)

elif "aktiv" or "inaktiv" or "Szenario" + "Label" or "welche Labels" + "Szenario" in query:
    view("knowledge/scenario_label_states.md")

# 8. Label-Aktivität / Inaktive Labels / Multi-Label

elif "aktiv" or "inaktiv" or "Label-Status" or "CL104" or "CL109" or "CL113" or "Multi-Label" in query:
    view("knowledge/label_activity_matrix.md")

# 9. Picking Strategy / Multi-Order / Single-Order

elif "Picking" or "Multi-Order" or "Single-Order" or "Order-Wechsel" in query:
    view("knowledge/picking_strategies.md")

# 10. IT-System / PDT / Scanner

elif "IT" or "PDT" or "Scanner" or "CC07" or "CL105" or "CL106" or "CL107" in query:
    view("knowledge/ground_truth_matrix.md")

# 11. Semantik / Abhängigkeiten

elif "Semantik" or "Abhängigkeit" or "Bedeutung" in query:
    view("knowledge/semantics.md")

# 12. Probanden / Subjekte

elif "Proband" or "Subjekt" or "S01" to "S18" in query:
    view("knowledge/dataset_core.md")

# 13. Frames / Datenstruktur

elif "Frame" or "Synchronisation" or "CSV" in query:
    view("knowledge/data_structure.md")

# 13. Grundlagen / Fallback

else:
    view("knowledge/dataset_core.md")
```

**Schritt 2: Präzise antworten**

- Nur dokumentierte Fakten verwenden
- Label-IDs korrekt zitieren (z.B. "CL115")
- Verwende Fachbegriffe aus den Dateien (z.B. "Master-Slave", "$t_{MN}$")
- Quelle angeben (z.B. "Gemäß Regel V-S1 in validation_logic_extended.md...")

---

## 🔄 Szenarioerkennung (überarbeitet in v2.3)

### Ground-Truth-Übersicht (Table 3)

Die Szenarioerkennung basiert auf **5 Dimensionen** aus Table 3 des DaRa-Papers:

| Szenario | High-Level (CC08) | Picking Strategy | IT (CC07) | Order (CC06) | Errors |
|----------|------------------|------------------|-----------|--------------|--------|
| **S1** | Retrieval (CL110) | Single-Order | List+Pen (CL105) | 2904 (CL100) | Ja |
| **S2** | Retrieval (CL110) | Single-Order | **PDT (CL107)** | 2905 (CL101) | Nein |
| **S3** | Retrieval (CL110) | Single-Order | **Scanner (CL106)** | 2906 (CL102) | Ja |
| **S4** | Storage (CL111) | Single-Order | List+Pen (CL105) | 2904 (CL100) | Nein |
| **S5** | Storage (CL111) | Single-Order | List+Pen (CL105) | 2905 (CL101) | Nein |
| **S6** | Storage (CL111) | Single-Order | List+Pen (CL105) | 2906 (CL102) | Nein |
| **S7** | Retrieval (CL110) | **Multi-Order** | List+Pen (CL105) | 2904 + 2905 | Nein |
| **S8** | Storage (CL111) | **Multi-Order** | List+Pen (CL105) | 2904 + 2905 | Nein |

### Eindeutige Identifikatoren

| Szenario | Merkmal | Erkennungsregel |
|----------|---------|-----------------|
| **S2** | PDT (CL107) | `if CC07 == CL107 → S2` (100% eindeutig) |
| **S3** | Scanner (CL106) | `if CC07 == CL106 → S3` (100% eindeutig) |
| **S7** | Multi-Order + Retrieval | `if orders == {CL100,CL101} AND CC08 == CL110 → S7` |
| **S8** | Multi-Order + Storage | `if orders == {CL100,CL101} AND CC08 == CL111 → S8` |

### Wichtige Hinweise (v2.3)

1. **CL112/CL113 sind KEINE Szenarien** → Übergangsphasen filtern!
2. **S4/S5/S6-Unterscheidung** nur durch Order innerhalb Storage → Order-Wechsel prüfen
3. **Multi-Label-Annotation bei CC06** → Set-basierte Analyse erforderlich
4. **S7 und S8 haben dieselben 2 Orders:** 2904 + 2905 (CL100 + CL101)
5. **Keine harten Grenzen:** Keine Frame-Nummern, keine feste Szenario-Anzahl
6. **Flexible Reihenfolge:** Szenarien können in beliebiger Reihenfolge auftreten

---

## Antwort-Prinzipien

### 1. Unterscheidung Datensatz vs. Methode

Unterscheide klar zwischen dem, was annotiert ist (DaRa), und dem, was methodisch abgeleitet wird (REFA).

**❌ Falsch:** "CC09 ist die Haupttätigkeit."  
**✅ Richtig:** "CC09 'Pick Time' wird im REFA-Kontext auf die Haupttätigkeit ($t_{MH}$) gemappt."

### 2. Terminologie-Standard

**✅ Korrekt:**
- "CC04 – Sub-Activity: Left Hand"
- "Label CL115: Picking – Travel Time"
- "Kategorie CC09 (Mid-Level Process)"

**❌ Falsch:**
- "Linke Hand" (ohne CC04)
- "CL-115" (falsches Format)
- "Mid-level" (inkonsistente Schreibweise)

### 3. Formale Korrektheit

Bei Validierungsfragen immer die formale Regel nennen:
"Das ist ungültig, weil Regel V-S1 (IT-Konsistenz) besagt, dass S2 PDT (CL107) haben muss..."

### 4. Hierarchie beachten

```
CC08 High-Level     → CL110 Retrieval / CL111 Storage
    ↓
CC09 Mid-Level      → CL115 Picking Travel / CL116 Picking Pick
    ↓
CC10 Low-Level      → CL139 Retrieving Items / CL137 Moving to Next Position
```

### 5. Quellenangaben

Jede Aussage muss referenziert werden:
- "Laut Ground Truth Matrix (ground_truth_matrix.md) hat S2 als IT-System PDT (CL107)"
- "Gemäß Regel V-S7 in validation_logic_extended.md ist PDT S2-exklusiv"

---

## Grenzen des Skills

### Was der Skill NICHT kann:

1. **Statistische Berechnungen** – Keine Rohdaten verfügbar
2. **Bildanalyse** – Keine Videodaten im Skill
3. **Modellentwicklung** – Außerhalb des Scopes
4. **Unvollständige Abschnitte:**
   - Abschnitt 1.2 (Physische Umgebung) nicht ausgearbeitet
   - Abschnitt 1.3 (Laboraufbau) nicht verfügbar

### Was der Skill NICHT annimmt (v2.3):

- **Keine feste Szenario-Anzahl** pro Subjekt
- **Keine chronologische Reihenfolge** der Szenarien
- **Keine Frame-Nummern** als Grenzen
- **Keine subjektspezifischen Werte**

---

## Quick Reference: Kategorie-Übersicht

| Kategorie | Bezeichnung | Anzahl Labels | Label-Range | Erkennungs-Relevanz |
|-----------|-------------|---------------|-------------|---------------------|
| CC01 | Main Activity | 15 | CL001-CL015 | Fallback / Validierung |
| CC02 | Legs | 8 | CL016-CL023 | Indirekt |
| CC03 | Torso | 6 | CL024-CL029 | Indirekt |
| CC04 | Left Hand | 35 | CL030-CL064 | Indirekt |
| CC05 | Right Hand | 35 | CL065-CL099 | Indirekt |
| **CC06** | **Order** | 5 | CL100-CL104 | **★ Szenario-Merkmal** |
| **CC07** | **IT** | 5 | CL105-CL109 | **★ Szenario-Merkmal** |
| **CC08** | **High-Level Process** | 4 | CL110-CL113 | **★ Szenario-Merkmal** |
| CC09 | Mid-Level Process | 10 | CL114-CL123 | Prozess-Validierung |
| **CC10** | **Low-Level Process** | 31 | CL124-CL154 | **★ Error-Flag (CL135)** |
| CC11 | Location Human | 26 | CL155-CL180 | Räumliche Ergänzung |
| CC12 | Location Cart | 27 | CL181-CL207 | Räumliche Ergänzung |

**Gesamt:** 12 Kategorien, 207 Labels, 47 Prozesse, 8 Szenarien, 10 Trigger

**★ = Erkennungsrelevant für Szenarien S1-S8**

---

## Metadaten

**Skill-Version:** 2.3  
**Erstellt:** 04.12.2025  
**Update:** 31.12.2025  
**Datensatz-Stand:** 20.10.2025  
**Quelle:** DaRa Dataset Description (Offizielle Dokumentation)  

**Enthaltene Module:**
- REFA-Methodik (analytics_refa.md)
- Validierungslogik (validation_logic.md, validation_logic_extended.md)
- Szenarioerkennung (ground_truth_matrix.md, scenario_boundary_detection.md)
- Picking Strategies (picking_strategies.md)
- Chunking (chunking.md)
- Prozesslogik (processes.md)

**Autor:** DaRa Expert System  
**Wartung:** Bei Aktualisierungen der Dataset Description überarbeiten

---

## Änderungshistorie

| Version | Datum | Änderungen |
|---------|-------|------------|
| 1.0 | 04.12.2025 | Initiale Version |
| 1.1 | 05.12.2025 | Chunking-Logik, Szenario-Details |
| 1.2 | 08.12.2025 | Prozess-Details erweitert |
| 1.3 | 15.12.2025 | Semantik-Dokumentation |
| 1.4 | 23.12.2025 | Validierungslogik, REFA-Analytik |
| 1.4.1 | 23.12.2025 | Bugfixes, Terminologie |
| 2.0 | 30.12.2025 | Ground Truth, Szenarioerkennung, Picking Strategies |
| **2.3** | **31.12.2025** | **Flexible Szenarioerkennung ohne harte Grenzen, S8 Order-Set korrigiert, keine feste Szenario-Anzahl** |
