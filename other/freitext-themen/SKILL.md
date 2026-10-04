---
name: freitext-themen
description: >-
  Codiert offene Freitext-Antworten einer Umfrage-CSV systematisch: Themencluster mit
  Häufigkeit, Pain Points vs. Lob, repräsentative Zitate. Wertet ALLE Antworten aus (nicht
  nur eine Stichprobe). Ergebnis als Markdown nach reports/. Nutzen für qualitative
  Auswertung offener Fragen / Verbatims. Aufruf mit der Anfrage als Argument, z. B.
  /freitext-themen <Spalte/Frage> [+ Fokus].
license: MIT
---

# Freitext-Themenanalyse

Ziel: Die offenen Antworten der in der Anfrage des Nutzers genannten Frage/Spalte
**systematisch codieren** — Themen bilden, ihre Häufigkeit auszählen, mit Zitaten belegen.
Es geht um qualitative Tiefe über den **vollständigen** Datensatz. Ergebnis nach `reports/`.

## Werkzeug

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Aus dem Projekt-Root ausführen. Fehlt `scripts/survey.py`, unter `.claude/scripts/survey.py` nachsehen oder `survey.py` im Projekt suchen.
- `profile` — Spaltenüberblick; identifiziert FREITEXT-Spalten (immer zuerst).
- `text COL [--filter "COL=WERT"]` — **alle** Antworten der Spalte ausgeben (kein
  `--sample`, damit nichts übersehen wird). `--json` für saubere Weiterverarbeitung.
- `text COL --filter ...` — Freitext einer Teilgruppe (z. B. nur tägliche Nutzer).

`COL` = Index (aus `profile`) oder eindeutiger Namensteil.

## Umfrage-Kontext

Liegt neben der CSV ein Kontextdokument (`<name>.context.md`, bei genau einer CSV im Ordner
auch `survey-context.md`), vor dem Codieren lesen. Der praktische Gewinn ist hier das
**Glossar**: Befragte schreiben in internen Kürzeln, Feature-Namen und Abkürzungen — ohne
Glossar liest du sie falsch oder zerlegst ein Thema in mehrere. Die **Umstände der
Feldzeit** erklären Ausschläge: Ein Release oder ein Ausfall während der Feldzeit taucht
als Thema auf und sollte auch so benannt werden, nicht als dauerhafte Beschwerde.

Trotzdem **bottom-up codieren**: Die Themen kommen aus den Antworten, nie aus dem Vokabular
des Kontextdokuments und nie aus dem, was jemand erwartet hat. Dort genannte Erwartungen
sind **Prüfgegenstand, nie Beleg** — kein Thema aufblasen, weil es erwartet wurde, und
keines weglassen, weil es nicht erwartet wurde. Die Rekrutierungsgrenzen (**„Wer fehlt"**)
in die Methodik übernehmen. Gibt es kein solches Dokument, wie bisher vorgehen und am Ende
einmal auf `umfrage-kontext` hinweisen.

## Vorgehen

1. **Profilieren**, Ziel-Freitextspalte festlegen. Befüllungsgrad notieren (wie viele
   haben geantwortet? die Nicht-Antwortenden sind Teil der Wahrheit).
2. **Alle Antworten laden** mit `text COL` (ohne `--sample`). Bei sehr vielen Antworten
   in mehreren Durchläufen/„chunks" lesen, damit keine verloren geht.
3. **Codieren (Bottom-up).** Wiederkehrende Themen/Codes bilden, Synonyme
   zusammenfassen. Jede Antwort kann mehreren Themen zugeordnet sein. **Nennungen je
   Thema zählen** (ungefähre Häufigkeit, transparent als Schätzung kennzeichnen).
4. **Strukturieren.** Themen nach Häufigkeit ordnen; wo sinnvoll trennen in Pain Points
   (Probleme/Wünsche) vs. Lob/geschätzte Aspekte vs. Neutral/Verhalten.
5. **Belegen.** Je Thema 1–2 **wörtliche** Kurzzitate (unverändert, ggf. gekürzt mit […]).
6. **Report speichern** nach `reports/` (`date +%F` + kebab-Titel, nicht überschreiben)
   und Top-Themen + Pfad in der Antwort nennen.

## Report-Format

```markdown
# Freitext-Themen: <Frage>

**Datenbasis:** <Datei> · Antworten n = <befüllt> von <gesamt> · <Datum>

## Überblick
2–3 Sätze: Was dominiert? Grundtenor (positiv/kritisch/gemischt)?

## Themen (nach Häufigkeit)
### 1. <Thema> — ~<N> Nennungen
Kurzbeschreibung. Beleg: „<wörtliches Zitat>" · „<Zitat 2>"

### 2. …

## Pain Points vs. geschätzte Aspekte
Kompakte Gegenüberstellung der wichtigsten Kritik-/Wunsch- und Lob-Themen.

## Implikationen
Was folgt daraus für Produkt/UX/Priorisierung?

## Methodik
Ausgewertete Spalte, Grundgesamtheit, Codierlogik und — aus dem Umfrage-Kontext — wer
befragt wurde und wer nicht erreicht werden konnte. Nennungszahlen sind qualitative
Schätzungen (Antworten können mehreren Themen angehören).
```

## Regeln
- **Vollständigkeit vor Bequemlichkeit**: alle Antworten sichten, nicht nur eine Stichprobe.
- Zitate **wörtlich** übernehmen (keine Glättung/Erfindung); nur mit […] kürzen.
- Nennungszahlen ehrlich als Näherung kennzeichnen — es ist qualitative Codierung.
- Nicht-Antwortende und niedrigen Befüllungsgrad erwähnen (Verzerrungsrisiko).
- Keine personenbezogenen Details aus Zitaten offenlegen, die Einzelne identifizierbar machen.
- Sprache = Sprache der Antworten (Standard Deutsch).
