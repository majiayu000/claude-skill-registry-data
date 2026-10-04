---
name: idea-mining
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-09-27
description: >
  Ideenschürf-Workflow für festgefahrene, schwere Probleme (Beweise, Forschungsfragen,
  hartnäckige Design-/Architekturprobleme): einen Ideenspeicher über acht Schürftechniken
  füllen (Wiedererkennung, Fern-Disziplin-Analogie, Alltags-Allegorie, Störgefühl/Ästhetik,
  Märchen-Reframing, Web-/Literatur-Recherche, Geschwisterprojekte, Bestandsquerlauf), dann
  gegen bereits Versuchtes filtern, eine Idee wählen und bis zur Substanz verfolgen. Nutze
  diesen Skill, wenn ein Problem trotz mehrerer Anläufe feststeckt, wenn „neue Ideen für X"
  gebraucht werden, bei „wir drehen uns im Kreis", oder für periodische Innovations-Läufe
  über ein Projekt. Für breites, freies Ideensammeln ohne festgefahrenes Problem stattdessen
  brainstorm (SCAMPER, Six Hats etc.).

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [ideen, kreativität, forschung, beweis, analogie, allegorie, recherche, innovation]
language: de
status: active
visibility: public

dependencies:
  tools: []
  services: [websearch]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="idea-mining banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


> **English Translation** — Official English version of `idea-mining`.



# Idea-Mining — Ideen schürfen, filtern, eine durchziehen (Deutsch)

## Übersicht & Zweck

Bei schweren Problemen scheitert Ideenfindung selten am Mangel an Einfällen, sondern an drei
Dingen: Die Einfälle werden nicht **festgehalten**, sie werden nicht gegen **bereits
Versuchtes** geprüft (man rennt in dieselben Sackgassen), und es wird keiner konsequent
**zu Ende verfolgt**. Dieser Workflow trennt die drei Phasen hart: erst divergent schürfen
(ohne Bewertung), dann filtern (gegen die Dokumentation des Projekts), dann EINE Idee
substanziell explorieren.

Herkunft: destilliert aus einem produktiven Forschungs-Automations-Lauf über offene
mathematische Probleme; funktioniert genauso für Architektur-, Design- und Konzeptblockaden.

## Phase A — Ideenspeicher füllen (divergent, ohne Bewertung)

Alle Fundstücke in eine Datei `IDEENSPEICHER.md` im Projektordner schreiben (Stichworte +
2–3 Sätze, Quelle/Auslöser notieren). Die acht Techniken nacheinander durchgehen — sie
zielen auf unterschiedliche Assoziationsräume, deshalb bei wirklich festgefahrenen
Problemen keine überspringen (bei leichteren Blockaden oder knapper Zeit genügt eine
begründete Teilmenge, mindestens aber eine weiche Technik aus 3–5 plus die Recherche):

1. **Wiedererkennung:** Kommt mir das bekannt vor? Habe ich diese Struktur schon einmal
   in anderem Kontext gesehen?
2. **Fern-Disziplin:** Gibt es ein ähnliches Problem/eine ähnliche Formel in einer weit
   entfernten Disziplin (Physik↔Ökonomie, Biologie↔Informatik, …)? Wo genau liegt die
   Verbindung?
3. **Alltags-Allegorie:** Das Problem in einer naturnahen Allegorie erzählen (Wellen,
   Sand, Strömung, Wachstum …). Wirksam: die Allegorie von einem **unbelasteten
   Subagenten** erfinden lassen und dann schauen, wohin sie führt — die eigene Sicht ist
   vom Problem schon deformiert.
4. **Störgefühl / Frosch→Prinz:** Was stört mich am aktuellen Stand, was finde ich
   hässlich? Was müsste sich ändern, damit ich es plötzlich schön fände? Ästhetisches
   Unbehagen zeigt oft auf die falsch gewählte Darstellung.
5. **Märchen-Reframing:** Das Problem als Märchen erzählen: Wer ist der Held, wer die
   Bösewichte, welche Gefahren lauern, was könnte dem Helden helfen? Die Rollenzuweisung
   erzwingt eine Kausalstruktur, die im Formalismus unsichtbar bleibt.
6. **Recherche:** Web, Fachdatenbanken, Preprint-Server, Foren (Reddit/ResearchGate/GitHub)
   nach neuen Veröffentlichungen, Scripts, Ansätzen durchsuchen. Relevante Quellen in einen
   Ordner `_sources/` laden und auf Innovationen lesen — bei Preprints kritisch bleiben.
7. **Geschwisterprojekte:** Verwandte eigene Projekte auf rücktransferierbare Lösungsideen
   prüfen (dort gelöste Teilprobleme, dort gebaute Werkzeuge).
8. **Bestandsquerlauf:** Den gesamten eigenen Projektbestand (Pipeline) auf Ansätze
   durchgehen, die auf DIESES Problem passen könnten.

## Phase B — Filter (gegen bereits Versuchtes)

Den Ideenspeicher gegen die Projektdokumentation abgleichen: Beweisnotizen, Proof-Notes,
Entscheidungs-Logs, TODO/DONE, frühere Ideenspeicher. **Eliminiert wird, was dokumentiert
bereits versucht und abgeschlossen ist** — nicht, was nur „unwahrscheinlich klingt"
(Bewertung nach Attraktivität kommt erst in Phase C). Überlebende nach
`IDEENSPEICHER_FILTERED.md`.

Voraussetzung ist eine gepflegte Versuchs-Dokumentation — existiert keine, ist der erste
Schritt, sie anzulegen (sonst produziert jeder künftige Lauf Wiederholungen).

## Phase C — Wählen und durchziehen

1. Ein bis drei Ideen aus dem Filtrat kurz anexplorieren (je ein Absatz: was wäre der
   erste konkrete Schritt, was das Erfolgssignal?).
2. **Eine** wählen — die mit der stärksten Anziehung. Attraktion ist hier ein legitimes
   Kriterium: Bei schweren Problemen trägt nur eine Idee, der man nachgehen *will*.
3. Die Wahl bis zum Ende oder zumindest substanziell weiterführen — nicht nach dem ersten
   Hindernis zur nächsten Idee springen (das wäre Phase-A-Verhalten in Phase C).

## Phase D — Dokumentieren

- Erkenntnisse in die Projektdokumentation (Beweisnotiz, Entscheidungs-Log, ADR) —
  **auch die Fehlschläge**, sie sind der Filter für den nächsten Lauf.
- Offene Folgeideen zurück in `IDEENSPEICHER.md` bzw. TODO.
- Kurzbericht: geschürft (Anzahl) | gefiltert (überlebend) | exploriert | Ergebnis | nächster Schritt.

## Phase E — Aussaat (optionaler Rücktransfer nach außen)

Technik 7 holt Ideen aus Geschwisterprojekten HEREIN — Phase E dreht die Richtung um:
Wenn die Exploration etwas Übertragbares ergeben hat (Methode, Werkzeug, Lösungsmuster),
kurz den eigenen Projektbestand durchgehen: Wem würde das helfen?

- **Gezielt säen, nicht streuen:** höchstens ~3 Empfängerprojekte direkt mit einem
  konkreten TODO-Eintrag versehen (was übernehmen, wo es liegt, warum es passt);
  weitere Kandidaten nur als priorisierte Liste im eigenen Projekt notieren.
- Grund für die Grenze: Breites Streuen erzeugt in vielen Projekten vage Aufgaben,
  die niemand aufgreift — drei präzise Saatkörner schlagen zehn diffuse.

## Als periodischer Lauf

Der Workflow eignet sich als wiederkehrende Automation über ein festes Projekt (Innovations-
Runde). Dafür mit dem Rotations-Gerüst kombinieren (`rotation-check`-Skill): Registry
verhindert, dass dieselben Ideen mehrfach „neu entdeckt" werden — der Ideenspeicher und die
Versuchs-Doku sind hier das Gedächtnis.

## Beispiel & Anwendung

```text
Problem: Ein Konvergenzbeweis steckt seit Wochen an einer Abschätzung fest.

A) Schürfen → IDEENSPEICHER.md: u. a. (2) ähnliche Struktur in der Warteschlangen-
   theorie?; (3) Subagent-Allegorie „Sand rieselt durch immer feinere Siebe" →
   Idee: Abschätzung stufenweise statt global; (6) Preprint von 2026 mit neuem
   Lemma, nach _sources/ geladen; (7) Nachbarprojekt hat ein numerisches
   Prüfscript, das sich rücktransferieren lässt.
B) Filter gegen BEWEISNOTIZ.md: „globale Abschätzung verschärfen" wurde 2× versucht
   und dokumentiert verworfen → raus. 3 Ideen überleben → IDEENSPEICHER_FILTERED.md.
C) Prime-Wahl: die Sieb-Idee (stärkste Anziehung) — bis zu einem Teilresultat
   durchgezogen.
D) BEWEISNOTIZ.md aktualisiert (auch der Fehlschlag von Idee 2), Kurzbericht.
```

## Red Flags

| Gedanke | Realität |
| --- | --- |
| „Technik 3–5 sind Spielerei" | Die weichen Techniken liefern die Ideen, die Recherche nicht liefern kann — sie adressieren andere Assoziationsräume. |
| „Ich bewerte schon beim Sammeln" | Bewertung in Phase A tötet die divergente Ausbeute. Erst speichern, dann filtern. |
| „Der Filter dauert zu lange, ich erinnere mich schon" | Gedächtnis glättet Fehlversuche — nur die Doku zählt. |
| „Idee klemmt, ich nehme die nächste" | In Phase C wird durchgezogen; Springen zurück nach A nur mit dokumentiertem Grund. |

## Verwandte Skills

- `brainstorm` — breite Kreativmethoden (SCAMPER, Six Hats) ohne Filter-/Explorations-Pipeline.
- `think` / `decide` — Analyse und Auswahlentscheidung, nutzbar innerhalb Phase C.
- `rotation-check` — Gerüst für den periodischen Einsatz.
- `swarm-operations` — unbelastete Subagenten für Technik 3 und parallele Exploration.

## Änderungsprotokoll

### 1.1.0 (2026-07-03)
- Phase E „Aussaat": optionaler Outbound-Transfer übertragbarer Ergebnisse in
  Geschwisterprojekte (max. ~3 direkte Empfänger) — integriert statt als eigener
  cross-project-transfer-Skill (Dedup-Entscheid).

### 1.0.0 (2026-07-03)
- Initiale Version. Abstrahiert aus der Codex-Automation „ultra-deep-idea-search-single-project"
  (Ideenspeicher → Filter → Prime-Wahl → Exploration) und user-neutral verallgemeinert.