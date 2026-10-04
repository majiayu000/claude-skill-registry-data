---
name: update-topic
description: Aktualisiert oder erweitert ein bestehendes Themen-Factsheet — Daten auffrischen, Sektionen ergänzen, Argumente überarbeiten oder die Darstellung verbessern (Blocktyp-Vielfalt, UX, Datenverständnis) — inklusive Recherche, Inline-Verifizierung und beiden Quality Gates. Verwenden, wenn ein bestehendes Topic-JSON inhaltlich oder visuell überarbeitet werden soll.
argument-hint: "[topicId] [Änderungsauftrag]"
allowed-tools: Read, Glob, Grep, Edit, WebFetch, WebSearch, Agent, Bash(npm run lint), Bash(npm run build), Bash(node *), Bash(curl *)
---

# Thema aktualisieren: `public/data/$ARGUMENTS[0].json`

Workflow für Änderungen an bestehenden Topic-Factsheets. Nutzt dieselben Qualitätsstandards wie `create-topic`, aber ohne den Scoping-Overhead einer Neuanlage.

Änderungsauftrag: $ARGUMENTS

## Arbeitsmodus: Autonome Abarbeitung

Der Workflow läuft **standardmäßig vollständig autonom** durch. Zwischenberichte dokumentieren Entscheidungen; sie sind keine Freigabe-Gates. Angehalten wird nur, wenn der Änderungsauftrag mehrdeutig ist und die Varianten zu inhaltlich gegensätzlichen Ergebnissen führen würden, oder wenn der Build nach 2 Korrekturversuchen fehlschlägt.

## Ablauf

### 1. Bestand erfassen

- `public/data/$ARGUMENTS[0].json` vollständig lesen; `src/types/index.ts` für das Schema
- Betroffene Sektionen, Argumente und Quellen identifizieren
- `lastUpdated` und zeitgebundene Angaben notieren (Jahreszahlen, „aktuell", Preise, Prognosen) — bei Datenaktualisierungen sind das die Prüfkandidaten

### 2. Recherche mit Inline-Verifizierung

Für neue oder zu aktualisierende Datenpunkte gilt Phase 2 aus `.claude/skills/create-topic/SKILL.md` vollständig — insbesondere:

- Quellenhierarchie (amtliche Statistiken vor Instituten vor Stiftungen/Verbänden vor Journalismus)
- **Unabhängigkeitsregel**: zentrale Datenpunkte nicht allein auf interessengebundene Quellen stützen
- Jede URL sofort verifizieren (✓ / ⚠ / ❓); nur ✓- und korrigierte ⚠-Datenpunkte verwenden
- Sonderfälle (PDF via curl + Read, Paywall, Wayback für tote URLs, widersprüchliche Quellen) nach `.claude/skills/verify-sources/SKILL.md`

### 3. Bearbeiten mit Autor-Leitplanken

- Die Checklisten „Neues Argument" und „Neuer Abschnitt" aus `.claude/skills/review-content/SKILL.md` sind kanonisch — auch für geänderte Bestandsinhalte anwenden
- Blocktyp-Auswahl nach `.claude/skills/create-topic/reference.md` (alle 13 Typen, inkl. `myth_fact`, `pictograph`, `target_progress`)
- Ersetzte Zahlen konsistent nachziehen: auch Fließtext, `keyStats`, `sourceNote`, Argument-Antworten und `relatedSections` prüfen — nicht nur den einen Block
- Nicht mehr gestützte `sourceRefs` entfernen; neue Quellen ins `sources`-Array (`id`, `label`, `url`)
- `lastUpdated` auf das heutige Datum setzen (`YYYY-MM-DD`)
- Keine deutschen Anführungszeichen „…" in JSON-Strings (siehe `.claude/rules/data-schema.md`); nach dem Schreiben `node -e "JSON.parse(...)"` ausführen

### 4. Darstellungs-Check (Vielfalt, UX, Datenverständnis)

Prüfen, ob die Inhalte im besten Blocktyp stehen — Blocktyp-Tabelle in `.claude/skills/create-topic/reference.md` als Auswahlhilfe.

**Geltungsbereich:** Immer für die bearbeiteten Sektionen. Für das **gesamte Topic**, wenn der Änderungsauftrag auf Darstellung, Vielfalt, UX oder Verständlichkeit zielt (z. B. „Darstellung verbessern", „Thema aufwerten").

**Upgrade-Heuristiken** — jede Fundstelle in den besser passenden Blocktyp überführen:

| Fundstelle | Upgrade |
|------------|---------|
| ≥ 3 `fact`-Blöcke in Folge (Fakten-Monotonie) | Kernzahlen → `stat_grid`; widerlegte Irrtümer → `myth_fact`; nur die 1–2 wichtigsten als `fact` mit `highlight` behalten |
| `text`-Block mit ≥ 3 Datenpunkten im Fließtext | Zahlen in einen Datenblock ausgliedern, `text` behält die Einordnung |
| Zeitreihe als `table` oder Aufzählung | `line_chart`/`bar_chart` (Tabelle ggf. als barrierefreie Ergänzung behalten, siehe Muster D) |
| „x von y"-Anteil als Text oder `fact` | `pictograph` |
| Ist-Stand vs. Zielwert in Prosa | `target_progress` |
| A-gegen-B-Vergleich in Prosa | `comparison`; Wertespannen → `range_bar` |
| Dieselben Zahlen mehrfach (`stat_grid` UND `table` UND `fact`) | Bestes Format wählen, Dubletten entfernen |
| Topic nutzt insgesamt < 3–4 verschiedene Blocktypen | Vielfalt gezielt erhöhen — aber nur, wo die Daten den Typ tragen |

**Grenzen:**
- Keine Visualisierung erzwingen, die die Daten nicht hergeben — ein präziser `text`-Block schlägt ein schiefes Diagramm
- Reiner Formatwechsel ändert keine Aussagen: Zahlen und `sourceRefs` wandern unverändert mit (kein neuer Verifizierungsbedarf); braucht die Visualisierung **zusätzliche** Datenpunkte → zurück zu Schritt 2
- Mobile-first: Tabellen mit mehr als 3–4 Spalten und überladene Diagramme vermeiden
- Recharts-Typen (`bar_chart`, `line_chart`) sparsam bei Themen mit vielen Sektionen (lazy-loaded, aber Gewicht)

### 5. Quality Gates

```
/review-content $ARGUMENTS[0]
```

Bei geänderten Daten oder Quellen zusätzlich:

```
/verify-sources $ARGUMENTS[0]
```

Alle ✗-Befunde beheben, ⚠-Befunde soweit sinnvoll adressieren.

### 6. Validierung & Abschlussbericht

```bash
npm run lint && npm run build
```

Abschlussbericht ausgeben: geänderte Sektionen/Argumente, alte → neue Zahlen, neue/entfernte Quellen, Darstellungs-Upgrades (alter → neuer Blocktyp mit Begründung), Ergebnis der Quality Gates.

## Regeln

- **Autonome Abarbeitung** (siehe oben) — Berichte dokumentieren, Gates laufen durch
- **Keine halluzinierten Daten** — jede neue Zahl aus einer verifizierten Quelle
- **Kein Strukturbruch** — `public/data/*.json`-Struktur nicht ändern ohne `src/types/index.ts` anzupassen (siehe AGENTS.md)
- **Minimalinvasiv** — nur ändern, was der Auftrag verlangt oder was durch die Änderung inkonsistent würde. Der Darstellungs-Check gehört bei bearbeiteten Sektionen dazu; unbeteiligte Sektionen werden nur bei ausdrücklichem Darstellungs-/Qualitätsauftrag umgebaut
