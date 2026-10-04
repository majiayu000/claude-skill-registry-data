---
name: entscheidungsvorlage
description: >-
  Erstellt aus quantitativen Umfragedaten (CSV) eine strukturierte Entscheidungsvorlage
  (Decision Memo): Ausgangslage, Optionen mit Pro/Contra und Datenbeleg, begründete
  Empfehlung, Risiken/Annahmen. Ergebnis als Markdown nach reports/. Nutzen, wenn eine
  Entscheidung ansteht, die mit Research-Evidenz gestützt werden soll. Aufruf mit der
  Anfrage als Argument, z. B. /entscheidungsvorlage <zu treffende Entscheidung / Frage>.
license: MIT
---

# Entscheidungsvorlage (Decision Memo)

Ziel: Zu der in der Anfrage des Nutzers genannten **Entscheidung** eine
handlungsleitende Vorlage bauen, in der **jede Option mit Daten belegt** ist und eine
**klare Empfehlung** ausgesprochen wird. Für Entscheider:innen, nicht für Analyst:innen.
Ergebnis als Markdown in `reports/`.

## Werkzeug

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Aus dem Projekt-Root ausführen. Fehlt `scripts/survey.py`, unter `.claude/scripts/survey.py` nachsehen oder `survey.py` im Projekt suchen.
- `profile` — Spaltenüberblick (immer zuerst).
- `freq COL [--by COL2] [--filter "COL=WERT"] [--sig]` — Verteilung/Kreuztabelle,
  `--sig` für Signifikanz + Effektstärke (Einfach × Einfach).
- `text COL [--filter ...] [--sample N]` — O-Töne/Freitext als Beleg.

`COL` = Index (aus `profile`) oder eindeutiger Namensteil.

## Umfrage-Kontext

Liegt neben der CSV ein Kontextdokument (`<name>.context.md`, bei genau einer CSV im Ordner
auch `survey-context.md`), zuerst lesen — dieser Skill profitiert davon am meisten, weil
darin die anstehende Entscheidung und das Publikum der Vorlage stehen. Ausgangslage,
Gegenstand und Glossar daraus übernehmen; die Zahlen kommen weiterhin nur aus dem Motor.
Rekrutierungsweg und der Abschnitt **„Wer fehlt"** gehören unter Risiken und Annahmen: Eine
Option, die unter den Antwortenden stark aussieht, kann bei den nie Erreichten anders
aussehen. Dort genannte Erwartungen sind **Prüfgegenstand, nie Beleg** — nie eine Erwartung
darüber entscheiden lassen, welche Option gewinnt. Gibt es kein solches Dokument, wie
bisher vorgehen und am Ende einmal auf `umfrage-kontext` hinweisen.

## Vorgehen

1. **Entscheidung schärfen.** Was genau ist zu entscheiden? Welche Optionen sind
   plausibel? Wenn nicht vorgegeben, leite 2–4 realistische Optionen ab (inkl. „Status
   quo / nichts tun" als Referenz).
2. **Profilieren** und die entscheidungsrelevanten Variablen finden.
3. **Evidenz je Option sammeln.** Für jede Option gezielt die Daten befragen, die dafür
   oder dagegen sprechen (Verteilungen, Kreuzvergleiche, ggf. Signifikanz, Freitext-
   Bedarfe). Auch die Größe betroffener Nutzergruppen quantifizieren (Impact).
4. **Abwägen und empfehlen.** Optionen anhand der Evidenz vergleichen, eine begründete
   Empfehlung geben. Trade-offs offenlegen, nicht verstecken.
5. **Report speichern** nach `reports/` (`date +%F` + kebab-Titel, nicht überschreiben)
   und Empfehlung + Pfad in der Antwort nennen.

## Report-Format

```markdown
# Entscheidungsvorlage: <Entscheidung>

**Datenbasis:** <Datei> · n = <…> · <Datum>

## Empfehlung
Klare Aussage in 1–2 Sätzen: welche Option, warum.

## Ausgangslage
Warum steht die Entscheidung an? Relevanter Datenkontext in 2–4 Sätzen.

## Optionen im Vergleich
| Option | Dafür (Daten) | Dagegen (Daten) | Betroffene (Impact) |
|---|---|---|---|
| A … | … (Zahl) | … (Zahl) | … % der Nutzer |
| B … | … | … | … |
| Status quo | … | … | … |

## Begründung der Empfehlung
Warum die empfohlene Option die Abwägung gewinnt — mit den entscheidenden Zahlen.

## Risiken & Annahmen
Was muss zutreffen? Was könnte schiefgehen? Datenlücken/Unsicherheiten — einschließlich
wen die Umfrage nicht erreicht hat (aus dem Umfrage-Kontext) und was das für die Empfehlung
bedeuten kann.

## Nächste Schritte
2–4 konkrete, priorisierte Schritte.

## Methodik
Genutzte Spalten/Filter/Tests in einem Absatz.
```

## Regeln
- **Jede** Option braucht Datenbeleg (pro *und* contra) — keine Bauchentscheidung.
- Empfehlung eindeutig aussprechen, aber Trade-offs und Unsicherheiten transparent machen.
- Signifikanz/Effektstärke nutzen, wo Gruppenunterschiede die Entscheidung tragen.
- Impact quantifizieren (wie viele Nutzer/welcher Anteil betroffen).
- Sprache = Sprache der Anfrage (Standard Deutsch). Entscheider-Ton: knapp, konkret.
