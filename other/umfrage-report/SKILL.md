---
name: umfrage-report
description: >-
  Beantwortet eine Frage zu quantitativen Umfragedaten aus einer CSV und schreibt einen
  kurzen, belegten Report als Markdown nach reports/. Funktioniert mit beliebigen
  Umfrage-CSVs (Spaltentypen werden automatisch erkannt). Aufruf mit der Anfrage als
  Argument, z. B. /umfrage-report <deine Frage>. Nutzen, wenn der Nutzer eine Auswertung,
  Zahlen, Auszählung, Kreuzvergleich oder eine These zu Umfrage-/Survey-Daten wünscht.
license: MIT
---

# Umfrage-Report

Ziel: Aus einer Umfrage-CSV die **gestellte Frage** faktenbasiert beantworten und
einen **kurzen Report als Markdown** in `reports/` speichern.

Die Frage des Nutzers ist die Anfrage, mit der dieser Skill aufgerufen wurde. Enthält sie einen
Datei-Pfad/Namen, ist das die zu nutzende CSV; sonst automatisch die CSV im Ordner.

## Werkzeug

Alle Zahlen kommen aus dem beigelegten Skript — **niemals Werte schätzen oder aus
Rohdaten „im Kopf" zählen**. Nur Standardbibliothek, kein pandas nötig.

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Aus dem Projekt-Root ausführen. Fehlt `scripts/survey.py`, unter `.claude/scripts/survey.py` nachsehen oder `survey.py` im Projekt suchen.

- `profile` — Überblick: n, alle Spalten mit **Index**, erkanntem Typ (META /
  EINFACH / MEHRFACH / FREITEXT), Befüllungsgrad. **Immer zuerst ausführen.**
- `freq COL [--by COL2] [--filter "COL=WERT"] [--top N]` — Häufigkeitsverteilung;
  `--by` = Kreuztabelle; `--filter` mehrfach möglich (Teilmenge). Bei MEHRFACH ist
  die Summe der Prozente > 100 % (das ist korrekt und im Report so zu erklären).
- `text COL [--filter ...] [--sample N]` — Freitext-Antworten für qualitative Themen.

`COL` = Spaltenindex (aus `profile`) **oder** eindeutiger Teil des Spaltennamens.
Alle Kommandos akzeptieren `--json` für maschinenlesbare Ausgabe.

## Umfrage-Kontext

Liegt neben der CSV ein Kontextdokument (`<name>.context.md`, bei genau einer CSV im Ordner
auch `survey-context.md`), vor dem Schreiben lesen. Darin stehen Gegenstand, Glossar,
Publikum und Erhebungsdesign. Für Einordnung und Begriffe nutzen — die Zahlen kommen
weiterhin ausschließlich aus dem Motor. Was darin die Aussagekraft einschränkt, vor allem
der Abschnitt **„Wer fehlt"**, gehört in Interpretation und Methodik dieses Reports. Dort
genannte Erwartungen sind **Prüfgegenstand, nie Beleg**: nie als Beleg zitieren und nie die
Formulierung eines Befundes davon beeinflussen lassen. Gibt es kein solches Dokument, wie
bisher auswerten und am Ende der Antwort einmal auf `umfrage-kontext` hinweisen.

## Ablauf

1. **Profilieren.** `profile` ausführen, um n, Spaltenindizes und -typen zu kennen.
2. **Frage in Auswertungen übersetzen.** Passende Spalte(n) wählen und die dafür
   richtigen Kommandos ausführen:
   - „Wie viele / welcher Anteil / Verteilung" → `freq` auf der Zielspalte.
   - „Unterscheidet sich X nach Y / Zusammenhang / Vergleich" → `freq X --by Y`.
   - „… bei Gruppe Z" → `--filter "Z-Spalte=Wert"`.
   - „Warum / was schätzen / typischer Ablauf / Wünsche" → `text` auf Freitext,
     bei vielen Antworten `--sample 40–60`, Themen bündeln und mit ~2–3 wörtlichen
     Kurzzitaten belegen.
   Meist braucht es 2–4 Analysebefehle **zusätzlich zu** `profile` — eine reine
   Verteilung ist selten die ganze Antwort. Bei offenen Fragen ruhig mehrere
   Blickwinkel kombinieren (Verteilung + relevanter Kreuzvergleich + Freitext-Themen).
3. **Report schreiben** (siehe Format), Zahlen exakt aus der Skript-Ausgabe.
4. **Speichern** nach `reports/`. Ordner bei Bedarf anlegen. Dateiname:
   `YYYY-MM-DD_kurz-titel.md` (Datum via `date +%F`, Titel kebab-case aus der Frage).
   Bei einer bereits existierenden Datei einen `-2` etc. anhängen, nichts überschreiben.
5. Dem Nutzer in der Antwort **kurz** die Kernaussage nennen und den Report-Pfad angeben.

## Report-Format (kurz halten)

```markdown
# <Frage als knappe Überschrift>

**Datenbasis:** <Dateiname> · n = <Antworten> · Report vom <Datum>

## Kernaussage
1–3 Sätze mit der direkten Antwort auf die Frage.

## Ergebnisse
- Belegte Punkte mit **Zahlen (absolut + %)**. Tabellen für Verteilungen/Kreuztabellen.
- Bei Mehrfachauswahl vermerken: Mehrfachnennung möglich, Summe > 100 %.

## Interpretation
Was bedeutet das? Auffälligkeiten, Zusammenhänge, Einschränkungen (z. B. niedriger
Befüllungsgrad einer Spalte, kleine Teilmenge bei Filtern, Grenzen des Erhebungsdesigns
laut Umfrage-Kontext).

## Methodik
Genutzte Spalten und Filter in einem Satz, damit nachvollziehbar/reproduzierbar. Wurde ein
Kontextdokument genutzt, den Rekrutierungsweg und die dadurch fehlende Gruppe nennen.
```

## Regeln

- **Genauigkeit vor Umfang.** Nur behaupten, was die Ausgaben hergeben. Prozente auf
  die *Befragten mit Antwort* der jeweiligen Spalte beziehen (gibt das Skript aus).
- Aggregate („insgesamt positiv", Top-2-Box) aus den **absoluten Zahlen** rechnen, nie
  durch Addieren gerundeter Prozentwerte: 73 von 140 sind 52,1 %, nicht 13,6 % + 38,6 %.
- Statistik im Klartext (`Chi² = 12.094`, `p = 0.438`, `Cramérs V = 0.17`), kein LaTeX.
  Verlässlichkeits-Warnungen der Engine weitergeben, nicht weglassen.
- Bei Filter-Teilmengen mit kleinem n (< ~30) ausdrücklich zur Vorsicht raten.
- Sprache des Reports = Sprache der Frage (Standard: Deutsch).
- Keine personenbezogenen Rohdaten (z. B. einzelne Ids/Zeitstempel) auflisten.
- Report **knapp** halten — es ist ein Kurzreport, keine vollständige Studie.
