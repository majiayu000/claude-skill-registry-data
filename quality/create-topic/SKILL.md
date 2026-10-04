---
name: create-topic
description: Erstellt ein vollständiges neues Themen-Factsheet von Grund auf, inklusive Recherche, JSON-Erstellung und Qualitätssicherung. Verwenden, wenn ein neues Thema zum Fakten-Stammtisch hinzugefügt werden soll.
argument-hint: "[topicId] [topicTitle]"
allowed-tools: Read, Glob, Grep, Edit, Write, WebFetch, WebSearch, Agent, Bash(npm run lint), Bash(npm run build), Bash(node *), Bash(curl *)
---

# Neues Thema erstellen: `public/data/$ARGUMENTS[0].json`

End-to-End-Workflow für ein neues Fakten-Stammtisch-Thema. Orchestriert Recherche mit integrierter Quellenverifizierung, Inhaltserstellung und die bestehenden Quality-Gate-Skills (`review-content`, `verify-sources`).

## Arbeitsmodus: Autonome Abarbeitung

Der gesamte 6-Phasen-Prozess läuft **standardmäßig vollständig autonom** durch — ohne auf Nutzerbestätigung zu warten. Die in den Phasen definierten Berichte (Gliederung, Quellenbericht, Abschlussbericht) werden als **Zwischenberichte ausgegeben und dokumentiert**, danach geht es direkt weiter. Angehalten wird nur bei echten Blockern:

- Das Thema hat insgesamt keine belastbare Datenbasis (nicht nur einzelne Lücken)
- Die `topicId` existiert bereits und der Auftrag ist nicht eindeutig als Neuanlage erkennbar
- Der Build schlägt nach 2 Korrekturversuchen fehl (siehe AGENTS.md)

Einzelne Sektionen ohne belastbare Daten sind **kein** Blocker: Sektion streichen oder mit einer Nachbarsektion zusammenlegen und die Entscheidung im Zwischenbericht dokumentieren. Nur wenn der Nutzer ausdrücklich um Rücksprache gebeten hat, an den Berichts-Punkten auf Bestätigung warten.

## Live-Benchmarks aus dem Bestand

Aktueller Bestand (beim Skill-Start ermittelt — diese Werte sind der Qualitätsmaßstab, nicht statische Zahlen in der Referenz):

!`node -e 'const fs=require("fs");const fl=fs.readdirSync("public/data").filter(f=>f.endsWith(".json")&&f!=="topics.json");const st=fl.map(f=>{const d=JSON.parse(fs.readFileSync("public/data/"+f,"utf8"));const t=new Set();(d.sections||[]).forEach(s=>(s.content||[]).forEach(b=>t.add(b.type)));return{s:(d.sections||[]).length,a:(d.arguments||[]).length,q:(d.sources||[]).length,t:t.size}});const med=k=>{const v=st.map(x=>x[k]).sort((a,b)=>a-b);return v[Math.floor(v.length/2)]};console.log(st.length+" Themen im Bestand | Median: "+med("s")+" Sektionen, "+med("a")+" Argumente, "+med("q")+" Quellen, "+med("t")+" verschiedene Block-Typen pro Thema")'`

## Voraussetzungen

- `src/types/index.ts` lesen für das `Topic`-Schema
- `${CLAUDE_SKILL_DIR}/reference.md` lesen für Strukturvorlagen und Blocktyp-Auswahl
- Autor-Leitplanken aus `.claude/skills/review-content/SKILL.md` (Checklisten dort sind kanonisch)

## 6-Phasen-Prozess

### Phase 1: Themenanalyse & Scoping

1. **Reichweite verstehen** — Was ist die Kerndebatte? Was macht das Thema stammtischtauglich?
2. **5–10 Teilaspekte identifizieren**, die jeweils eine eigene Sektion verdienen (z. B. für „Wohnen": Mietentwicklung, Neubau, Sozialwohnungen, Mietpreisbremse, Enteignungsdebatte, internationaler Vergleich)
3. **6–12 typische Stammtisch-Behauptungen sammeln** — diese werden zu `arguments`. Dabei:
   - **Richtungs-Check**: Verbreitete Fehlannahmen aus **allen** politischen Richtungen aufnehmen, sofern sie im realen Diskurs existieren — nicht nur die einer Seite. Die Auswahl folgt der Verbreitung, nicht einer Quote; aber eine komplett fehlende Richtung trotz existierender Parolen ist ein Mangel.
   - **Empirie-Test pro Claim**: Für jeden Claim festhalten, ob er empirisch prüfbar ist (→ bekommt ein Verdict, inkl. `true` für schlicht zutreffende Behauptungen) oder eine normative Werteposition (→ kein Verdict, Antwort weist Faktenbasis und Wertkonflikt aus). Siehe `review-content`, Dimension 9a.
4. **ContentBlock-Mix planen** — Jedes Thema sollte mindestens 3–4 verschiedene Block-Typen für visuelle Abwechslung nutzen. Alle 13 Typen aus `src/types/index.ts` stehen zur Verfügung — siehe reference.md für die Auswahl-Hilfe (inkl. `myth_fact`, `pictograph`, `target_progress`).
5. **Gliederung als Zwischenbericht ausgeben** (normative Claims als „ohne Verdict" kennzeichnen), dann direkt mit Phase 2 fortfahren:

```
Geplante Struktur für "{topicTitle}":

Sektionen:
1. {section-title} — {Kurzbeschreibung}, geplante Blöcke: stat_grid, fact
2. {section-title} — ...
...

Stammtisch-Argumente:
1. "{claim}" — Kernaussage der Antwort: ...
2. "{claim}" — ...
...
```

### Phase 2: Quellenrecherche mit Inline-Verifizierung

Belastbare, verifizierbare Quellen für jede geplante Sektion recherchieren **und sofort verifizieren**. Parallele Subagents verwenden.

**Quellenhierarchie** (höhere bevorzugen):
1. Amtliche Statistiken (Destatis, Eurostat, Bundesministerien)
2. Forschungsinstitute (Fraunhofer, DIW, ifo, IW Köln) und peer-reviewed Studien/Meta-Analysen
3. Stiftungen und Denkfabriken (Bertelsmann Stiftung, Agora) — Interessenlage beachten
4. Offizielle Verbände und Körperschaften (GDV, ADAC, BDA, DGB) — Interessenlage beachten
5. Qualitätsjournalismus (nur wenn Originaldaten zitiert werden)

**Unabhängigkeitsregel** — Angriffsfläche „Die Zahl kommt doch vom Lobbyverband" von vornherein schließen:

- Quellen der Stufen 3–4 sind **interessengebunden**: Verbände, Stiftungen mit Agenda und Auftragsstudien haben ein Eigeninteresse an bestimmten Ergebnissen.
- **Zentrale Datenpunkte** (highlight-Fakten, Kernzahlen in Argument-Antworten, Zahlen in `keyStats`) brauchen entweder eine Quelle der Stufen 1–2 **oder** eine unabhängige Zweitquelle, die die Größenordnung bestätigt.
- Wo nur eine interessengebundene Quelle existiert, die Herkunft im Text transparent machen („laut Branchenverband GDV …") statt die Zahl als neutralen Fakt zu präsentieren.
- Generell pro Sektion anstreben, dass die Datenbasis nicht an einem einzigen Herausgeber hängt.

**Pro Sektion sammeln und inline verifizieren:**
- 2–4 konkrete Datenpunkte mit exakten Zahlen; zentrale Kennzahlen möglichst durch zwei voneinander unabhängige Quellen belegen
- Die Quell-URL für jeden Datenpunkt
- Das Veröffentlichungsdatum (Daten der letzten 2 Jahre bevorzugen)

**Inline-Verifizierung — jede URL sofort prüfen:**

Für jeden recherchierten Datenpunkt direkt im Anschluss:

1. **URL abrufen** — Quell-URL per WebFetch laden
2. **Zahlen extrahieren** — die konkreten Datenpunkte aus dem Seiteninhalt herausziehen
3. **Abgleich** — jeden notierten Wert gegen die extrahierten Daten prüfen und einordnen:
   - ✓ **VERIFIZIERT**: Zahl stimmt mit Quelle überein → in Ergebnisliste aufnehmen
   - ⚠ **ABWEICHUNG**: Zahl weicht ab → korrigierte Zahl aus Quelle übernehmen
   - ❓ **NICHT VERIFIZIERBAR**: URL nicht erreichbar oder Zahl nicht auffindbar → als Lücke markieren, alternative Quelle suchen

**Sonderfälle** (Details in `.claude/skills/verify-sources/reference.md`, Abschnitt „Sonderfälle"):
- **PDF-Quellen** (Destatis, GDV, Ministerien publizieren oft als PDF): per `curl -L` in den Scratchpad laden und mit dem Read-Tool prüfen — nicht vorschnell als ❓ einstufen
- **Paywall / JS-lastige Seiten**: als ❓ mit Vermerk führen und Ersatzquelle suchen; die Quelle ist deshalb nicht falsch
- **Tote URLs**: Wayback-Machine-Snapshot prüfen (`https://web.archive.org/web/<url>`); bestätigt der Snapshot die Daten, Archiv-URL verwenden
- **Widersprüchliche Quellen** (zwei seriöse Quellen, unterschiedliche Zahlen): Methodik/Abgrenzung/Stichtag vergleichen, methodisch aktuellere bevorzugen oder Spanne angeben; die Abweichung im Inhalt transparent machen, nicht stillschweigend eine Zahl wählen

**Gate:** Nur Datenpunkte mit Status ✓ oder ⚠ (korrigiert) kommen in die Ergebnisliste. ❓-Datenpunkte brauchen eine Ersatzquelle oder werden gestrichen.

**Nach Abschluss aller Sektionen — Quellenbericht als Zwischenbericht ausgeben, dann fortfahren:**

```
Recherche-Ergebnis für "{topicTitle}":

Verifizierte Quellen:
✓ {source-id} — {Kernaussage} (Quelle: {url})
✓ {source-id} — ...
⚠ {source-id} — korrigiert: {alt} → {neu} (Quelle: {url})

Geschlossene/gestrichene Lücken:
❓ Sektion "{section}" — kein belastbarer Datenpunkt für {Aspekt} gefunden → {Entscheidung: Ersatzquelle / Sektion gestrichen / mit {section} zusammengelegt}
```

**Quellen-ID-Konvention:** `{herausgeber-kebab}-{themen-stichwort}` (z. B. `destatis-mietpreisindex-2025`)

### Phase 3: Strukturierung

Gesammelte Daten der Sektionsstruktur zuordnen:

1. Für jede Sektion ContentBlock-Typen wählen:
   - Einleitender Kontext → `text`-Block
   - Kernzahlen → `stat_grid` (max. 4 Einträge) oder `fact`-Blöcke
   - Vergleiche → `comparison` oder `range_bar`
   - Zeitreihen → `timeline`, `line_chart` oder `bar_chart`
   - Detaildaten → `table`
   - Aufschlüsselungen → `progress_stack`
   - Verbreitete Irrtümer kompakt richtigstellen → `myth_fact`
   - Einen Anteil anschaulich machen („x von y") → `pictograph`
   - Ist-Stand gegen Zielwert → `target_progress`

2. Für jedes Argument festlegen:
   - Welche Sektionen die Belege liefern (`relatedSections`)
   - Welche Stichwörter jemand benutzen würde, der diese Behauptung aufstellt (`keywords`, 4–6 pro Argument)

3. Das `sources`-Array mit `id`, `label` und `url` für jede Quelle anlegen

### Phase 4: JSON-Erstellung

`public/data/{topicId}.json` entsprechend dem `Topic`-Interface schreiben.

**Autor-Leitplanken anwenden:** Die Checklisten „Neues Argument" und „Neuer Abschnitt" aus `.claude/skills/review-content/SKILL.md` sind die **kanonische** Vorgabe — vor dem Schreiben lesen und jeden Punkt anwenden (keine Kopie hier, um Drift zu vermeiden).

**Strukturregeln:**
- `id`-Felder: kebab-case
- `lastUpdated`: heutiges Datum im Format `YYYY-MM-DD`
- Jeder `sourceRef` muss im `sources`-Array existieren
- `highlight: true` auf max. 1–2 Fakten pro Sektion (die wichtigsten)
- Schlicht zutreffende empirische Claims bekommen `verdict: "true"` — dann keine `rhetoricalPattern`/`counterQuestions` (nichts zu korrigieren)

### Phase 5: Quality Gate

Beide Quality-Gate-Skills nacheinander auf das neue Thema anwenden.

**Schritt 1 — Inhaltliche Qualitätsprüfung:**

```
/review-content {topicId}
```

Alle ✗ PROBLEM-Befunde beheben. ⚠ VERBESSERBAR-Befunde soweit möglich adressieren.

**Schritt 2 — Quellenverifizierung (Sicherheitsnetz):**

```
/verify-sources {topicId}
```

Die Inline-Verifizierung in Phase 2 sollte die meisten Fehler bereits abgefangen haben. Dieser Durchlauf stellt sicher, dass auch beim Schreiben der JSON in Phase 4 keine neuen Fehler eingeflossen sind (z. B. verrutschte sourceRefs, versehentlich geänderte Zahlen). Verbleibende Abweichungen korrigieren, nicht verifizierbare sourceRefs entfernen.

### Phase 6: Integration & Validierung

1. **In die Startseiten-Reihenfolge einordnen** — die neue `topicId` in der `TOPIC_ORDER`-Liste in `scripts/generate-topic-index.mjs` an der thematisch passenden Position eintragen (Blöcke: Klima/Energie/Mobilität · Arbeit/Verteilung · Gesellschaft · Staat/Bildung/Wissen). Ohne Eintrag landet das Thema mit Build-Warnung am Ende der Startseite.

2. **Validieren** — `npm run build` generiert automatisch den `topics.json`-Index aus der neuen Topic-Datei:
   ```bash
   npm run lint && npm run build
   ```

3. **Abschlussbericht ausgeben** — was erstellt wurde, welche Entscheidungen autonom getroffen wurden (gestrichene Sektionen, korrigierte Zahlen, Verdict-Einstufungen), Ergebnis der Quality Gates

## Regeln

- **Autonome Abarbeitung**: Alle 6 Phasen ohne Bestätigungspausen durchlaufen; Berichte dokumentieren die Entscheidungen. Stopp nur bei den oben definierten Blockern.
- **Keine halluzinierten Daten** — jede Zahl muss aus einer verifizierten Quelle stammen
- **Quellen-Unabhängigkeit** — zentrale Datenpunkte nicht allein auf interessengebundene Quellen stützen (Unabhängigkeitsregel in Phase 2)
- **Politische Neutralität** — die Seite bezieht Position für die Evidenz, nicht für ein Lager: Claims aus allen Richtungen sammeln, Verdicts nur auf empirisch prüfbare Aussagen (inkl. `true` für zutreffende), keine Plädoyers in Antworten (siehe `review-content`, Dimension 9)
- **Konservative Sprache** — bei Unsicherheit abschwächen, niemals übertreiben
- **Visuelle Vielfalt** — mindestens 3 verschiedene ContentBlock-Typen pro Thema; auch die neueren Typen (`myth_fact`, `pictograph`, `target_progress`) in Betracht ziehen
- **Mindestumfang** — mindestens 5 Sektionen, 6 Argumente, 8 Quellen; an den Live-Benchmarks oben orientieren

## Referenz

Siehe `${CLAUDE_SKILL_DIR}/reference.md` für Strukturvorlagen, ContentBlock-Typ-Auswahl und Qualitäts-Benchmarks aus bestehenden Themen.
