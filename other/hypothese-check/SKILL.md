---
name: hypothese-check
description: >-
  Prüft eine formulierte Hypothese/These gegen quantitative Umfragedaten (CSV) und
  urteilt: bestätigt / teilweise bestätigt / widerlegt — inklusive Chi²-Signifikanztest,
  Effektstärke und Gegenprüfung. Ergebnis als Markdown nach reports/. Nutzen, wenn der
  Nutzer eine Annahme, These oder Vermutung verifizieren/falsifizieren will. Aufruf mit
  der Anfrage als Argument, z. B. /hypothese-check <Hypothese>.
license: MIT
---

# Hypothese-Check

Ziel: Eine in der Anfrage des Nutzers formulierte **Hypothese** wissenschaftlich
sauber gegen die Daten prüfen und ein **belegtes, gerichtetes Urteil** abgeben — nicht
nur beschreiben, sondern testen. Ergebnis als Markdown in `reports/`.

## Werkzeug (gemeinsamer Analyse-Motor)

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Aus dem Projekt-Root ausführen. Fehlt `scripts/survey.py`, unter `.claude/scripts/survey.py` nachsehen oder `survey.py` im Projekt suchen.
- `profile` — Spaltenüberblick (Index, Typ, Befüllung). **Immer zuerst.**
- `freq COL [--by COL2] [--filter "COL=WERT"] [--top N] [--sig]` — Verteilung/Kreuztabelle.
  **`--sig`** (nur Einfachauswahl × Einfachauswahl) liefert Chi², p-Wert, Cramérs V und
  eine Warnung bei zu kleinen erwarteten Zellhäufigkeiten.
- `text COL [--filter ...] [--sample N]` — Freitext für qualitative Belege.

`COL` = Index (aus `profile`) oder eindeutiger Namensteil. `--json` für maschinenlesbar.

## Umfrage-Kontext

Liegt neben der CSV ein Kontextdokument (`<name>.context.md`, bei genau einer CSV im Ordner
auch `survey-context.md`), vor der Prüfung lesen. Darin stehen Gegenstand, Glossar und
Erhebungsdesign; für Einordnung und Begriffe nutzen, nie für Zahlen. Rekrutierungsweg und
der Abschnitt **„Wer fehlt"** gehören in die Einschränkungen dieses Reports — eine These
kann in der Stichprobe gelten und für genau die Gruppe scheitern, die die Stichprobe nicht
erreicht, und das ist einen Satz wert.

Der Abschnitt **Erwartungen** verlangt hier besondere Sorgfalt, weil dieser Skill ihm am
stärksten ausgesetzt ist:

- Hat der Nutzer **keine** Hypothese genannt, darfst du eine aus der Erwartungsliste
  nehmen — dann sagen, welche du gewählt hast und dass sie aus dem Kontextdokument stammt.
- **Deckt sich** die Hypothese des Nutzers mit einer notierten Erwartung, ändert das nichts
  daran, wie hart du prüfst. Die Erwartung ist kein Vorab-Beleg, die Gegenprüfung wird
  nicht milder, und ein Grenzfall-Urteil kippt dadurch nicht.
- Eine widerlegte Erwartung ist ein **Ergebnis, kein Misserfolg**. Das klar sagen: „Das war
  so erwartet; die Daten zeigen es nicht." Das ist der wertvollste Report, den dieses
  Toolkit schreibt.

Gibt es kein solches Dokument, wie bisher prüfen und am Ende einmal auf `umfrage-kontext`
hinweisen.

## Vorgehen

1. **Hypothese operationalisieren.** Zerlege die These in prüfbare Aussagen: Welche
   Variable(n)? Erwartete Richtung? Welche Vergleichsgruppen? Formuliere sie als
   testbare Aussage (implizite Nullhypothese: „kein Unterschied / kein Zusammenhang").
2. **Profilieren** und passende Spalten identifizieren.
3. **Testen — richtungsbewusst.**
   - Zusammenhang zweier Kategorien → `freq X --by Y --sig`: Signifikanz (p) sagt „real
     oder Zufall?", Cramérs V sagt „wie stark?". **Beides zusammen bewerten** — ein
     signifikanter, aber vernachlässigbarer Effekt bestätigt die These praktisch nicht.
   - Verteilung/Anteil als These → `freq` und die behauptete Größenordnung prüfen.
   - Qualitative These → `text`, Themen zählen/belegen.
4. **Gegenprüfung (aktiv falsifizieren).** Suche mindestens eine Auswertung, die der
   These *widersprechen* könnte (alternative Erklärung, Störgröße, Teilgruppe, in der es
   nicht gilt). Ein Researcher versucht, die eigene Hypothese zu widerlegen.
5. **Urteil fällen:** **BESTÄTIGT** / **TEILWEISE BESTÄTIGT** / **WIDERLEGT** /
   **NICHT ENTSCHEIDBAR** (z. B. zu kleine Stichprobe, fehlende Variable).
6. **Report speichern** nach `reports/` (`date +%F` + kebab-Titel, nicht überschreiben)
   und Kernurteil + Pfad in der Antwort nennen.

## Report-Format

```markdown
# Hypothese-Check: <These in einem Satz>

**Datenbasis:** <Datei> · n = <…> · <Datum>

## Urteil
**BESTÄTIGT / TEILWEISE / WIDERLEGT / NICHT ENTSCHEIDBAR** — 1–2 Sätze Begründung.

## Prüfung
- Operationalisierung: welche Variablen, welche erwartete Richtung.
- Belege mit Zahlen + Test: „Chi²(df)=…, p=…, Cramérs V=… (Effekt: …)".
- Statistische Einordnung in Klartext: ist der Unterschied real und relevant?

## Gegenprüfung
Was wurde getestet, um die These zu widerlegen? Ergebnis.

## Einschränkungen
Stichprobengröße/Teilgruppen, Zellhäufigkeits-Warnungen, Konfundierung, Kausalität
(Korrelation ≠ Kausalität!) sowie die Grenzen des Erhebungsdesigns laut Umfrage-Kontext
(wen die Rekrutierung nicht erreichen konnte).

## Methodik
Genutzte Spalten, Filter, Tests — reproduzierbar in einem Absatz.
```

## Regeln
- **Signifikanz UND Effektstärke** gemeinsam interpretieren; p allein genügt nie.
- Bei der Warnung „erwartete Häufigkeit < 5" das Ergebnis ausdrücklich relativieren.
- Chi² zeigt **Zusammenhang, keine Kausalität** — nie kausal formulieren ohne Vorbehalt.
- Nur behaupten, was die Ausgaben hergeben. Kleine Teilgruppen (n < ~30) kennzeichnen.
- **Die These prüfen, nie für sie argumentieren** — auch und gerade dann, wenn im
  Umfrage-Kontext steht, dass jemand sie erwartet hat.
- Sprache = Sprache der Hypothese (Standard Deutsch). Report knapp halten.
