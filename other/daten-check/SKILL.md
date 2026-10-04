---
name: daten-check
description: >-
  Prüft die Datenqualität einer Umfrage-CSV vor der inhaltlichen Analyse: Befüllungs-/
  Ausfüllquoten, Speeder (über Ausfülldauer), Straightlining, dünn befüllte Spalten. Gibt
  eine Ampel-Einschätzung und Empfehlungen. Ergebnis als Markdown nach reports/. Nutzen
  als ersten Schritt bei einer neuen Datei oder bei Zweifeln an der Datengüte. Aufruf mit
  der Anfrage als Argument, z. B. /daten-check [optional CSV-Pfad].
license: MIT
---

# Datenqualitäts-Check

Ziel: **Vor** jeder inhaltlichen Auswertung prüfen, wie belastbar die Daten sind, damit
aus schwachen Daten keine starken Schlüsse gezogen werden. Ergebnis als Markdown in
`reports/`. Ein Pfad in der Anfrage des Nutzers wählt die CSV, sonst die im Ordner.

## Werkzeug

```
python3 scripts/survey.py quality [--file CSV]
python3 scripts/survey.py profile [--file CSV]
python3 scripts/survey.py freq COL [--file CSV]
```

Aus dem Projekt-Root ausführen. Fehlt `scripts/survey.py`, unter `.claude/scripts/survey.py` nachsehen oder `survey.py` im Projekt suchen.
`quality` liefert direkt:
- **Befüllungsgrad je Spalte** (dünne Spalten < 50 % markiert),
- **Ausfülldauer** (Median, Bereich) und **Speeder** (< 1/3 der Median-Dauer),
- **Straightlining** in erkannten Skalen-Batterien (identische Antwort über ≥3 gleiche Skalen).

`freq` wird nur gebraucht, um einen vermuteten Widerspruch zum Umfrage-Kontext zu belegen
(siehe unten), nicht für die Qualitätskennzahlen selbst.

`--json` für strukturierte Werte.

## Umfrage-Kontext

Liegt neben der CSV ein Kontextdokument (`<name>.context.md`, bei genau einer CSV im Ordner
auch `survey-context.md`), lesen — und dann etwas tun, das kein anderer Skill tut: **es
gegen die Daten prüfen.** Überall sonst ist der Kontext Hintergrund; hier ist er eine
Behauptung auf dem Prüfstand.

Ein Widerspruch zwischen dem, was im Kontext steht, und dem, was die Daten zeigen, ist ein
**eigenständiger Befund** — oft ein schwererer als eine Handvoll Speeder:

- **Grundgesamtheit vs. Verhalten.** „Es wurden nur aktive Nutzer befragt", aber 12 % geben
  an, das Produkt nie zu nutzen → entweder hat die Rekrutierung weiter gereicht als
  angenommen, oder die Frage wird anders verstanden als gemeint. Beides ändert, wie jeder
  spätere Report formuliert werden muss.
- **Feldzeit vs. Zeitstempel.** Der angegebene Erhebungszeitraum passt nicht zu den
  Zeitstempeln in den Daten → womöglich der falsche Export, mehrere zusammengeführte Wellen
  oder veralteter Kontext.
- **Stichprobe vs. Erwartung.** Der Kontext nennt eine Zielgruppe oder Quote, die die Daten
  nicht hergeben (ein Segment, das sich als n = 7 entpuppt).
- **Spalten-Hinweise vs. Realität.** Eine als Leitfrage benannte Spalte ist dünn befüllt,
  oder eine als zusammengehörig beschriebene Batterie gibt es in der Form nicht.

Widersprüche vor dem Berichten mit dem Motor belegen — eine Vermutung ist kein Befund.
Beschreiben, was der Kontext behauptet, was die Daten zeigen und was daraus folgt; nicht
entscheiden, welche Seite falsch liegt. Ein Widerspruch, der wesentlich ändert, für wen die
Ergebnisse sprechen, gehört ins Gesamturteil und nicht nur in die Details: Daten, die sauber
sind, aber eine andere Grundgesamtheit beschreiben als angenommen, sind nicht grün.

Gibt es kein Kontextdokument, den Check wie bisher fahren und im Report vermerken, dass das
Erhebungsdesign nicht überprüft werden konnte — das ist kein Mangel der Daten, aber eine
Grenze dieses Checks. Am Ende einmal auf `umfrage-kontext` hinweisen.

## Vorgehen

1. **`quality` ausführen** (und bei Bedarf `profile` für die Spaltentypen).
2. **Befunde einordnen.** Für jede Dimension bewerten, ob unkritisch, beobachten oder
   problematisch:
   - Dünne Spalten → für diese Fragen sind Aussagen nur eingeschränkt möglich.
   - Speeder → wenn nennenswerter Anteil, Verzerrungsrisiko; Ausschluss erwägen.
   - Straightlining → Hinweis auf unaufmerksames Ausfüllen in Batterien.
3. **Kontext gegen die Daten prüfen** (siehe oben), sofern ein Kontextdokument existiert.
   Jeden vermuteten Widerspruch mit einer konkreten `freq`-/`profile`-Ausgabe belegen.
4. **Ampel vergeben** (grün / gelb / rot) mit kurzer Begründung.
5. **Empfehlungen** ableiten (z. B. „Spalte X für Detailfragen meiden", „Y Speeder prüfen/
   ausschließen", „Ergebnisse zu Frage Z nur mit Vorbehalt").
6. **Report speichern** nach `reports/` (`date +%F_daten-check`, nicht überschreiben) und
   Ampel + Pfad in der Antwort nennen.

## Report-Format

```markdown
# Datenqualitäts-Check

**Datenbasis:** <Datei> · n = <…> · Spalten = <…> · <Datum>

## Gesamturteil: 🟢 / 🟡 / 🔴
1–2 Sätze: Sind die Daten für belastbare Auswertungen geeignet?

## Befund
| Dimension | Ergebnis | Bewertung |
|---|---|---|
| Vollständigkeit | Ø-Befüllung, dünne Spalten: … | 🟢/🟡/🔴 |
| Ausfülldauer | Median … min, Speeder … % | … |
| Straightlining | … % in Batterie / keine Batterie | … |

## Dünn befüllte Spalten
Liste der Spalten < 50 % mit Konsequenz für die Analyse.

## Kontext vs. Daten
Nur wenn ein Kontextdokument existiert. Je Widerspruch: was der Kontext behauptet, was die
Daten zeigen (mit Zahl), was daraus folgt. Widerspricht nichts, ein Satz, dass das
angegebene Erhebungsdesign zu den Daten passt. Ohne Kontextdokument: „nicht beurteilbar —
kein Kontextdokument vorhanden; das Erhebungsdesign konnte nicht geprüft werden."

## Empfehlungen
Konkrete Do's/Don'ts für die weitere Auswertung (inkl. möglicher Fallausschlüsse).

## Methodik
`survey.py quality`: Definitionen (Speeder < 1/3 Median-Dauer; Straightlining =
identische Antwort über eine ganze Skalen-Batterie). Das geprüfte Kontextdokument nennen,
falls eines vorlag.
```

## Regeln
- Erst prüfen, dann interpretieren — dieser Check ist bewusst der **erste** Schritt.
- Kennzahlen exakt aus der `quality`-Ausgabe übernehmen, nicht schätzen.
- Fehlende Zeitstempel/Batterien klar als „nicht auswertbar" benennen, nicht als „gut".
  Dasselbe gilt für ein fehlendes Kontextdokument — ungeprüft ist nicht dasselbe wie
  geprüft und in Ordnung.
- Datenqualitätsprobleme benennen, ohne zu dramatisieren; Konsequenzen konkret machen.
- Einen Widerspruch zum Umfrage-Kontext berichten, nicht durch Parteinahme auflösen — und
  nie stillschweigend fallen lassen, weil die Daten sonst sauber aussehen.
- Sprache Standard Deutsch.
