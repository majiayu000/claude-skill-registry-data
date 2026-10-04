---
name: management-summary
description: >-
  Bereitet eine Frage/ein Thema aus quantitativen Umfragedaten (CSV) management-gerecht
  auf: ein Einseiter mit TL;DR, 3–5 Kernbefunden mit Zahl und Implikation und nächsten
  Schritten. Ergebnis als Markdown nach reports/. Nutzen, wenn Ergebnisse für
  Führungs-/Stakeholder-Ebene verdichtet werden sollen. Aufruf mit der Anfrage als
  Argument, z. B. /management-summary <Frage/Thema>.
license: MIT
---

# Management-Summary

Ziel: Zu dem in der Anfrage des Nutzers genannten **Thema** einen
**entscheidungsorientierten Einseiter** für Management/Stakeholder erstellen — verdichtet,
implikationsstark, ohne Methoden-Ballast. Ergebnis als Markdown in `reports/`.

## Werkzeug

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Aus dem Projekt-Root ausführen. Fehlt `scripts/survey.py`, unter `.claude/scripts/survey.py` nachsehen oder `survey.py` im Projekt suchen.
- `profile` — Spaltenüberblick (immer zuerst).
- `freq COL [--by COL2] [--filter "COL=WERT"] [--sig]` — Verteilung/Kreuztabelle (+Signifikanz).
- `text COL [--filter ...] [--sample N]` — Freitext für ein prägnantes O-Ton-Zitat.

`COL` = Index (aus `profile`) oder eindeutiger Namensteil.

## Umfrage-Kontext

Liegt neben der CSV ein Kontextdokument (`<name>.context.md`, bei genau einer CSV im Ordner
auch `survey-context.md`), zuerst lesen. Zwei Teile zählen hier besonders: das **Publikum**
(wer das liest und was damit entschieden wird — den Einseiter darauf zuschneiden) und
**Gegenstand/Glossar** (damit die Summary die Sprache der Leser nutzt, nicht die
Fragetexte). Die Zahlen kommen weiterhin nur aus dem Motor.

Dieses Format hat keine Methodik-Sektion und ist damit die Stelle, an der das
Erhebungsdesign am leichtesten verloren geht — also eines behalten: Schränkt der
Rekrutierungsweg die Botschaft wesentlich ein (Abschnitt **„Wer fehlt"**), das in einem
**Halbsatz** an der passenden Stelle sagen, nicht in einem eigenen Block. „Unter den per
In-App-Banner befragten aktiven Nutzern sind 71 % …" kostet sechs Wörter und verhindert,
dass das Management ein Teilbild für das ganze hält.

Im Dokument genannte Erwartungen sind **Prüfgegenstand, nie Beleg** — eine Summary darf
nicht zur erhofften Bestätigung werden. Gibt es kein solches Dokument, wie bisher vorgehen
und am Ende einmal auf `umfrage-kontext` hinweisen.

## Vorgehen

1. **Profilieren**, dann das Thema in die 2–4 aussagekräftigsten Auswertungen übersetzen
   — diese Zahl kommt zu `profile` hinzu; `profile` ist Pflicht-Startschritt, keine der
   Auswertungen.
2. **Analysieren** und die wichtigsten Zahlen holen. Weniger ist mehr — pro Kernbefund
   eine belastbare Zahl.
3. **Verdichten auf Implikationen.** Für jeden Befund fragen: „Na und? Was heißt das
   fürs Geschäft/Produkt/die Nutzer?" Genau das kommt in die Summary.
4. **Report speichern** nach `reports/` (`date +%F` + kebab-Titel, nicht überschreiben)
   und die TL;DR + Pfad in der Antwort nennen.

## Report-Format (max. eine Seite)

```markdown
# <Thema als aussagekräftige Überschrift>

**Datenbasis:** <Datei> · n = <…> · <Datum>

## TL;DR
2–4 Sätze, die die zentrale Botschaft transportieren. Das Wichtigste zuerst.

## Kernbefunde
1. **<Befund>** — <Zahl absolut + %>. *Implikation:* <was das bedeutet>.
2. …
(3–5 Befunde, je Zahl + Implikation, jeweils eine Zeile)

## Empfehlung / Nächste Schritte
2–3 konkrete, priorisierte Schritte.

<optional ein prägnantes wörtliches Nutzerzitat, wenn es die Botschaft stützt>
```

## Regeln
- **Kurz und implikationsorientiert** — Management liest Botschaften, nicht Tabellen.
  Maximal eine Bildschirmseite.
- Jeder Kernbefund trägt eine konkrete Zahl (absolut + %). Keine vagen Aussagen.
- Fachjargon und Methodendetails weglassen (ggf. ein Satz „Basis: n=…").
- Nichts behaupten, was die Daten nicht hergeben; Unsicherheit in einem Halbsatz benennen —
  auch, wen die Umfrage nicht erreicht hat, wenn das die Lesart der Botschaft ändert.
- Sprache = Sprache der Anfrage (Standard Deutsch).
