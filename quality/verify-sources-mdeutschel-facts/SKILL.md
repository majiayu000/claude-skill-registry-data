---
name: verify-sources
description: Alle Quellen und Daten in einem Topic-Factsheet-JSON gegen tatsächliche Online-Quellen prüfen. Verwenden, wenn URLs verifiziert, Datenrichtigkeit geprüft oder sourceRefs validiert werden sollen.
argument-hint: "[topicId]"
allowed-tools: Read, Glob, Grep, Edit, WebFetch, WebSearch, Agent, AskUserQuestion, Bash(npm run lint), Bash(npm run build), Bash(node *), Bash(curl *)
---

# Quellenverifizierung für `public/data/$ARGUMENTS.json`

Topic-JSON-Dateien (`public/data/*.json`) enthalten ein `sources`-Array und `sourceRefs` in Content-Blöcken. Alle Quellen MÜSSEN online verifizierbar sein, um halluzinierte Daten zu vermeiden.

## Wann ausführen

- Nach Erstellung oder wesentlicher Bearbeitung einer Topic-JSON
- Beim Hinzufügen von `sourceRefs` zu Content-Blöcken
- Auf ausdrückliche Anfrage (`/verify-sources {topicId}`)

## 6-Phasen-Ablauf

1. **Analyse** — `public/data/$ARGUMENTS.json` lesen, das `sources`-Array und alle `sourceRefs` aus Content-Blöcken extrahieren. Zuordnen, welche Behauptungen welche Quellen referenzieren.
2. **URL-Beschaffung** — Für jede Quelle OHNE `url`-Feld: im Web nach der korrekten URL suchen. Suchen parallel über Explore-Subagents ausführen.
3. **Quellenverifizierung** — Für jede Quelle MIT URL: URL abrufen, alle konkreten Zahlen und Datenpunkte extrahieren. Abrufe parallel über Explore-Subagents ausführen. Sonderfälle (PDF, Paywall, tote URLs) nach den Regeln unten behandeln — nicht vorschnell als nicht verifizierbar einstufen.
4. **Abgleich** — Für jeden Content-Block mit `sourceRefs` jede Behauptung einordnen:
   - ✓ **VERIFIZIERT**: stimmt mit Quellendaten überein
   - ⚠ **ABWEICHUNG**: Zahl weicht ab (Erwartung vs. Ist dokumentieren)
   - ❓ **NICHT VERIFIZIERBAR**: Quelle enthält diese Info auf ihrer Webseite nicht, oder Inhalt ist maschinell nicht prüfbar (Paywall — mit Vermerk führen)
   - ✗ **FALSCH**: Quelle widerspricht der Behauptung

   Zusätzlich prüfen: **Unabhängigkeit** — zentrale Datenpunkte (highlight-Fakten, `keyStats`, Kernzahlen in Argumenten), die allein auf einer interessengebundenen Quelle beruhen (Verbände, Stiftungen mit Agenda, Auftragsstudien), als ⚠ UNABHÄNGIGKEIT melden und eine unabhängige Zweitquelle (amtliche Statistik, peer-reviewed) suchen bzw. die Herkunft im Text ausweisen.
5. **Bericht** — Strukturierten Bericht ausgeben: alle Befunde mit Status, geplante Korrekturen.
6. **Korrekturen (autonom)** — Direkt anwenden, ohne auf Zustimmung zu warten: fehlende URLs ergänzen, falsche Zahlen korrigieren, unzutreffende `sourceRefs` entfernen, tote URLs durch bestätigte Archiv-Snapshots ersetzen, Fließtext/Argumente an korrigierte Daten anpassen. Jede Änderung im Bericht dokumentieren (alt → neu). Danach `npm run lint && npm run build` ausführen. Ausnahme: Kollabiert durch eine Korrektur die Kernaussage eines Arguments oder einer Sektion, konservativ korrigieren und den Befund prominent im Bericht ausweisen (ggf. per AskUserQuestion klären, falls ein Nutzer erreichbar ist).

## Sonderfälle bei der Verifizierung

- **PDF-Quellen**: Destatis, GDV, Ministerien und Institute publizieren viele Daten als PDF, an denen WebFetch scheitert. Per `curl -L` in den Scratchpad laden und mit dem Read-Tool prüfen. Erst wenn auch das scheitert → ❓.
- **Paywall / JS-lastige Seiten**: Als ❓ mit Vermerk „nicht maschinell prüfbar" führen — das ist kein ✗-Befund. Frei zugängliche Ersatzquelle (Pressemitteilung, Originalstudie) suchen und bevorzugen.
- **Tote URLs**: Zuerst Wayback-Machine-Snapshot prüfen (`https://web.archive.org/web/<url>`). Bestätigt der Snapshot die Daten: Archiv-URL in die Quelle übernehmen (Behörden-URLs sterben regelmäßig bei Legislaturwechseln). Kein Snapshot oder Daten nicht bestätigt: aktuelle Ersatz-URL beim selben Herausgeber suchen, sonst Quelle streichen.
- **Widersprüchliche Quellen**: Liefern zwei seriöse Quellen unterschiedliche Zahlen, Methodik/Abgrenzung/Stichtag vergleichen. Methodisch aktuellere bevorzugen oder Spanne angeben; die Abweichung im Inhalt transparent machen (z. B. per `text`-Block oder `range_bar`), nicht stillschweigend eine Zahl wählen.

## Regeln

- **Autonome Abarbeitung**: Der komplette 6-Phasen-Ablauf läuft ohne Bestätigungspausen durch; der Bericht dokumentiert alle Änderungen. Nur bei ausdrücklichem Rücksprache-Wunsch des Nutzers vor Phase 6 anhalten.
- **Keine Halluzinationen**: Nur Zahlen verwenden, die tatsächlich aus Online-Quellen extrahiert wurden
- **Konservativ**: `sourceRef` eher entfernen als unverifizierte Daten beibehalten
- **Unabhängigkeit**: Zentrale Datenpunkte sollen nicht allein an interessengebundenen Quellen hängen — Zweitquellen vorschlagen oder Herkunft ausweisen
- **Transparenz**: Jede Änderung dokumentieren
- **Quellenintegrität**: Niemals eine Quelle erfinden oder eine URL raten
- **Parallelität**: Parallele Subagents für unabhängige Quellenrecherchen nutzen

## Referenz

Siehe `${CLAUDE_SKILL_DIR}/reference.md` für korrekt strukturierte Beispiele aller Content-Block-Typen (stat_grid, comparison, table, timeline, fact) mit passenden `sourceRefs`.
