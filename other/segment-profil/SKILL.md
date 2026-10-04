---
name: segment-profil
description: >-
  Erstellt aus quantitativen Umfragedaten (CSV) ein datenbasiertes Vergleichsprofil einer
  Teilgruppe (Segment/Persona) gegenüber dem Rest der Stichprobe: wer sie sind, wie sie
  sich unterscheiden, was sie auszeichnet. Ergebnis als Markdown nach reports/. Nutzen für
  Personas, Nutzertypen oder Zielgruppen-Charakterisierung. Aufruf mit der Anfrage als
  Argument, z. B. /segment-profil <Segment-Beschreibung, z. B. "tägliche Nutzer" oder
  "Branche=Handel">.
license: MIT
---

# Segment-Profil

Ziel: Die in der Anfrage des Nutzers beschriebene **Teilgruppe** datenbasiert
charakterisieren und **gegen den Rest der Stichprobe kontrastieren** — als Grundlage für
Personas/Zielgruppen. Ergebnis als Markdown in `reports/`.

## Werkzeug

```
python3 scripts/survey.py <cmd> [...] [--file CSV]
```

Aus dem Projekt-Root ausführen. Fehlt `scripts/survey.py`, unter `.claude/scripts/survey.py` nachsehen oder `survey.py` im Projekt suchen.
- `profile` — Spaltenüberblick (immer zuerst).
- `freq COL [--filter "COL=WERT"]` — Verteilung im Segment (Filter) vs. gesamt.
- `freq COL --by SEGMENTSPALTE --sig` — Segment als Spalte gegen ein Merkmal, mit
  Signifikanztest, um echte Unterschiede von Rauschen zu trennen.
- `text COL [--filter ...] [--sample N]` — O-Töne des Segments.

`COL` = Index (aus `profile`) oder eindeutiger Namensteil.

## Umfrage-Kontext

Liegt neben der CSV ein Kontextdokument (`<name>.context.md`, bei genau einer CSV im Ordner
auch `survey-context.md`), vor der Segmentdefinition lesen. Die **Spalten-Hinweise** nennen
oft die geschäftlich relevanten Segmente und die Spalte, in der sie stecken — dort
nachsehen, bevor du einen eigenen Schnitt erfindest. Das Glossar hält das Profil in der
Sprache der Organisation. Die Zahlen kommen weiterhin nur aus dem Motor.

Der Abschnitt **„Wer fehlt"** zählt hier doppelt: Ein Segment-Profil beschreibt eine
Teilgruppe *der Antwortenden*, und wenn der Rekrutierungsweg schon eine Gruppe
ausgeschlossen hat, beschreibt das Profil unbemerkt eine gefilterte Grundgesamtheit. Das
gehört in die Methodik. Im Dokument genannte Erwartungen sind **Prüfgegenstand, nie
Beleg** — eine Persona darf nicht auf das zurechtgeschnitten werden, was jemand vermutet
hat. Gibt es kein solches Dokument, wie bisher vorgehen und am Ende einmal auf
`umfrage-kontext` hinweisen.

## Vorgehen

1. **Segment definieren.** Übersetze die Beschreibung in einen konkreten Filter (z. B.
   Nutzungshäufigkeit = „Täglich"). Bestimme die **Segmentgröße** (n und % der Stichprobe).
2. **Profilieren** und die charakterisierenden Merkmale wählen (Demografie, Verhalten,
   Rollen, Aufgaben).
3. **Kontrastieren.** Für jedes Merkmal: Verteilung **im Segment** vs. **Gesamt/Rest**.
   Die interessanten Aussagen sind die **Abweichungen** („überdurchschnittlich oft …").
   Wo möglich mit `--sig` prüfen, ob der Unterschied belastbar ist.
4. **Qualitativ anreichern.** Freitext des Segments für typische Bedürfnisse/Zitate.
5. **Report speichern** nach `reports/` (`date +%F` + kebab-Titel, nicht überschreiben)
   und Kurzcharakterisierung + Pfad in der Antwort nennen.

## Report-Format

```markdown
# Segment-Profil: <Segmentname>

**Datenbasis:** <Datei> · Segment n = <…> (<…% der Stichprobe>) · <Datum>

## Kurzcharakterisierung
2–3 Sätze: Wer ist dieses Segment, was macht es aus?

## Merkmale im Vergleich
| Merkmal | Segment | Gesamt/Rest | Auffälligkeit |
|---|---:|---:|---|
| … | …% | …% | ↑ überdurchschnittlich / ↓ / ≈ |

(Deutliche und ggf. signifikante Abweichungen zuerst.)

## Verhalten & Bedürfnisse
Was tut das Segment (Aufgaben/Nutzung) und was braucht es (Freitext-Themen, 1–2 Zitate)?

## Was das für die Praxis bedeutet
Implikationen für Produkt/Kommunikation/Priorisierung.

## Methodik
Segment-Definition (Filter), verglichene Spalten, genutzte Tests und — aus dem
Umfrage-Kontext — welche Grundgesamtheit die Stichprobe abdeckt und welche nicht.
```

## Regeln
- Immer **relativ** berichten: Segment gegen Gesamt/Rest — absolute Zahlen des Segments
  allein sagen wenig. Abweichungen sind die Story.
- Segmentgröße nennen; bei n < ~30 zur Vorsicht raten.
- Signifikanz nutzen, um zufällige von echten Unterschieden zu trennen.
- Sprache = Sprache der Anfrage (Standard Deutsch). Report knapp halten.
