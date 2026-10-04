---
name: umfrage-kontext
description: >-
  Erfasst den Kontext einer Umfrage — Zweck, Gegenstand, Rekrutierung, wer fehlt, Publikum
  und Erwartungen — in einem kurzen Interview und legt ihn als Markdown-Dokument neben die
  CSV (<name>.context.md). Alle anderen Umfrage-Skills lesen es, wenn es da ist, damit
  Reports das Erhebungsdesign benennen statt es zu erraten. Nutzen vor der ersten Analyse
  eines neuen Datensatzes, zum Aktualisieren eines bestehenden Kontextdokuments oder um ein
  vorhandenes Briefing in eines zu überführen. Aufruf mit CSV-Pfad oder Briefing-Text als
  Argument, z. B. /umfrage-kontext [CSV-Pfad].
license: MIT
---

# Umfrage-Kontext

Ziel: festhalten, **was die Daten über sich selbst nicht sagen können** — warum die Umfrage
lief, wen sie gefragt hat, wie die Teilnehmenden rekrutiert wurden, wer dadurch fehlt und
welche Entscheidung ansteht. Ergebnis ist ein kurzes Markdown-Dokument neben der CSV. Alle
anderen Skills dieses Toolkits lesen es, wenn es existiert, damit ihre Reports die
tatsächliche Erhebung beschreiben statt einer plausiblen Allerweltserhebung.

Das ist ein **Interview, kein Formular**. Kurz halten und niemals eine Antwort für den
Nutzer erfinden.

## Wo das Dokument liegt

Neben der CSV, die es beschreibt, und nach ihr benannt:

```
kundenumfrage.csv  →  kundenumfrage.context.md
```

Die Endung ist in jeder Sprache `.context.md` — nur der Inhalt wird in der Sprache des
Nutzers geschrieben. Liegt genau eine CSV im Ordner, wird auch ein schlichtes
`survey-context.md` akzeptiert (das ist der Name für ein von Hand geschriebenes Dokument,
zu dem noch keine Datei existiert).

Die Datei steht absichtlich in der `.gitignore`: Sie kann heikler sein als die CSV, weil
darin anstehende Entscheidungen, Strategie und interne Kennzahlen stehen. Das am Ende
einmal erwähnen.

## Werkzeug

```
python3 scripts/survey.py profile [--file CSV]
```

Aus dem Projekt-Root ausführen. Fehlt `scripts/survey.py`, unter
`.claude/scripts/survey.py` nachsehen oder `survey.py` im Projekt suchen.

`profile` liefert n, die Spaltenliste mit Indizes und Typen sowie die Befüllungsgrade.
Nutze es, damit das Interview nichts fragt, was schon in den Daten steht.

## Ablauf

1. **CSV finden.** Ein Pfad in der Anfrage hat Vorrang, sonst die CSV im aktuellen Ordner.
   Bei mehreren CSVs und ohne Pfadangabe nachfragen — das Dokument gehört zu einem
   bestimmten Datensatz.
2. **Auf ein vorhandenes Dokument prüfen.** Existiert `<name>.context.md` bereits, lesen,
   in zwei Zeilen zusammenfassen, was schon drinsteht, und beim ersten leeren oder mit
   „nicht angegeben" markierten Abschnitt weitermachen. Bestehende Antworten nie
   stillschweigend überschreiben; vor dem Ändern eines gefüllten Abschnitts nachfragen.
3. **`profile` ausführen.** n, Spaltenzahl und die Fragetexte notieren — daraus ergibt sich
   schon viel über den Gegenstand.
4. **Liegt ein Briefing vor?** Enthält die Anfrage (oder eine Datei, auf die sie zeigt)
   bereits Projekthintergrund, alles daraus übernehmen, das Dokument schreiben und danach
   nur die leer gebliebenen Abschnitte erfragen. Das Interview füllt das Format — es ist
   nicht der einzige Weg dorthin.
5. **Dokument sofort anlegen**, mit Kopf und leeren Abschnitten, bevor die erste Frage
   gestellt wird. Dann die sechs Fragen **einzeln nacheinander** stellen und **die Datei
   nach jeder Antwort aktualisieren**. Ein nach Frage drei abgebrochenes Interview muss ein
   brauchbares Dokument hinterlassen.
6. **Die sechs Fragen stellen** (siehe unten). Vorab sagen, dass es sechs Fragen sind, rund
   zwei Minuten, und dass jede übersprungen werden kann. Fortschritt zeigen („Frage 3 von
   6"). Wird eine Antwort übersprungen, `Nicht angegeben.` in den Abschnitt schreiben —
   eine benannte Lücke ist eine Information, Schweigen dagegen ist nicht von „hier gibt es
   keine Einschränkung" zu unterscheiden.
7. **Abschluss**: Pfad nennen, auf die `.gitignore` hinweisen und in einem Satz sagen, dass
   die anderen Skills das Dokument ab jetzt verwenden.

## Die sechs Fragen

In dieser Reihenfolge, in der Sprache des Nutzers, je eine Nachricht. Die Klammerhinweise
sind für dich und werden nicht vorgelesen.

1. **Zweck.** Warum lief diese Umfrage, und welche Entscheidung hängt daran?
2. **Gegenstand.** Was ist das Produkt oder Thema in ein, zwei Sätzen — und welche Begriffe
   oder Kürzel in den Spaltennamen versteht ein Außenstehender nicht?
   *(Die Fragetexte hast du aus `profile`; gezielt nach denen fragen, die nach internem
   Jargon aussehen.)*
3. **Rekrutierung.** Wen wolltet ihr befragen, und wie sind die Teilnehmenden reingekommen?
   *(Danach einmal nachfassen: **wer fehlt dadurch systematisch?** Das ist der wertvollste
   Satz im ganzen Dokument. Sieht der Nutzer keine Lücke, das anbieten, was der
   Rekrutierungsweg nahelegt — ein In-App-Banner erreicht keine abgewanderten Nutzer, ein
   Kunden-Newsletter keine Nicht-Kunden — und bestätigen oder korrigieren lassen.)*
4. **Feldzeit.** Wann lief die Umfrage, und ist kurz davor oder während der Feldzeit etwas
   passiert, das die Antworten prägt — ein Release, eine Preisänderung, ein Ausfall,
   Presse?
5. **Publikum.** Wer liest die Reports, und was sollen die Leser damit tun?
6. **Erwartungen.** Was vermutest du, das die Daten zeigen?
   *(Offen sagen, was mit der Antwort passiert: Sie kommt als Prüfliste ins Dokument, und
   ein Report, der eine Erwartung widerlegt, tut genau seine Arbeit. Nicht drängen, wenn es
   keine gibt — ein leerer Erwartungsabschnitt ist in Ordnung.)*

## Dokumentformat

```markdown
# Umfrage-Kontext: <Kurztitel>

**Datensatz:** <datei.csv>
**Stichprobe:** n = <Antworten> · <Anzahl> Spalten
**Feldzeit:** <Zeitraum, wie vom Nutzer angegeben>
**Kontext erfasst am:** <Datum>

## Zweck und anstehende Entscheidung
Warum die Umfrage lief und was daraus entschieden werden soll.

## Gegenstand und Glossar
Was das Produkt/Thema ist. Begriffe, Abkürzungen und interne Namen, die die Fragetexte
nicht erklären.

## Stichprobe und Rekrutierung
Angestrebte Grundgesamtheit und wie die Teilnehmenden rekrutiert wurden.

## Wer fehlt
Welche Gruppen der Rekrutierungsweg nicht erreichen kann und was das für die Befunde
bedeutet. Dieser Abschnitt gehört in die Einschränkungen jedes Reports.

## Umstände der Feldzeit
Ereignisse während oder kurz vor der Feldzeit, die die Antworten geprägt haben können.

## Spalten-Hinweise
Welche Spalte die Leitfrage ist, welche Items zusammengehören, in welchen Spalten die
geschäftlich interessanten Segmente stecken. Freie Prosa, keine feste Notation.

## Publikum und Verwendung
Wer die Reports liest und was damit entschieden wird.

## Erwartungen (zu prüfen)

**Das sind Vorannahmen der Leute, die die Umfrage durchgeführt haben. Sie sind
Prüfgegenstand, nie Beleg.** Eine Erwartung nicht als Beleg zitieren, nicht beeinflussen
lassen, welche Auswertungen gefahren und wie Befunde formuliert werden. Eine Erwartung nur
dort im Report aufgreifen, wo die Daten sie tatsächlich beantworten, und dann mit
ausdrücklichem Urteil — auch mit „die Daten zeigen das nicht".

- <Erwartung 1>
- <Erwartung 2>
```

Jeder Abschnitt bleibt auch unbeantwortet im Dokument stehen; darunter dann
`Nicht angegeben.`

## Regeln

- **Erfassen, nicht erfinden.** Alles im Dokument kommt vom Nutzer oder aus `profile`. Ist
  eine Antwort vage, einmal nach einem konkreten Detail fragen und dann aufschreiben, was
  tatsächlich gesagt wurde — nicht die aufgeräumte Fassung davon.
- **Fakten und Erwartungen strikt trennen.** Nichts aus Frage 6 darf in einem anderen
  Abschnitt landen. Vermischt eine Antwort beides („wir haben unsere Power-User befragt,
  und die sind sicher zufriedener"), aufteilen und das auch sagen.
- **Kurz schlägt vollständig.** Zwei bis vier Sätze je Abschnitt. Das ist eine
  Kurzunterrichtung, kein Studienprotokoll.
- **Keine personenbezogenen Rohdaten** — keine Namen, Ids oder identifizierenden Zitate.
- **Hier keine Auswertungsfragen beantworten.** Fragt der Nutzer, was die Daten zeigen, auf
  `umfrage-report` verweisen und erst das Interview zu Ende führen.
- Sprache des Dokuments = Sprache des Nutzers (Standard: Deutsch).
