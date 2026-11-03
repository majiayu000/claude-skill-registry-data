---
name: decision-shot
version: 1.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-09-18
description: >
  Extrem kurzes, substantielles Ausgabe-FORMAT fuer EINE Entscheidung oder
  Entscheidungsgruppe, wenn die dahinterstehende Analyse bereits existiert (im
  Chat entstanden, aus `decide`, aus `decision-briefing`, aus einem Ticket
  oder Dokument): Kontext in 2-3 Zeilen, Pro/Contra je Option als Stichpunkte
  im paveman/caveman-reduzierten Stil, Talking Points, eine begruendete
  Empfehlung, und ein Pfad/Link zur Vollanalyse zum Komplett-Nachlesen. Nutze
  diesen Skill bei "gib mir das kurz mit Pro Contra und Empfehlung", "executive
  summary zur Entscheidung", "kurzkontext zu <Thema>", "fass die Entscheidung
  X in einer Kurzform zusammen", /decision-shot, oder wenn ein Ergebnis an
  jemanden weitergereicht werden soll, der nur die Essenz braucht, nicht die
  volle Herleitung. NICHT nutzen, um viele offene Entscheidungen zu SAMMELN
  und per Buchstabe abzufragen -- das macht decision-briefing; NICHT nutzen,
  um eine Entscheidung erst zu ANALYSIEREN -- das macht decide. decision-shot
  setzt eine fertige Analyse voraus und komprimiert nur deren Praesentation.
visibility: public
language: de
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [entscheidung, executive-summary, kurzform, pro-contra, talking-points, empfehlung]
status: active

dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, knappform, paveman]

provenance:
  origin: "custom"
  decision_ref: "T-20260824-673115956 (Ticket-Master, User-Auftrag 2026-08-24)"
---

<img src="banner.png" width="100%" alt="decision-shot banner">

# decision-shot

> Die Analyse ist gemacht. Was jetzt gebraucht wird, ist keine zweite
> Herleitung, sondern die Essenz plus der Weg zurueck zum Vollstaendigen.

## Wann nutzen

- Eine Entscheidung (oder eine eng zusammengehoerige Gruppe, z. B. mehrere
  Unterfragen desselben Themas) ist bereits durchdacht -- im Chat, in einem
  Ticket, per `decide`-Framework oder in `decision-briefing`s Phase 2 --
  und muss jetzt jemandem (dem User, einem anderen Agenten, einem
  Uebergabedokument) in Sekunden zugaenglich gemacht werden.
- Trigger-Woerter: "kurz mit Pro Contra", "executive summary", "kurzkontext",
  "talking points dazu", "gib mir das komprimiert mit Empfehlung",
  `/decision-shot`.
- **Nicht** bei mehreren noch offenen, unentschiedenen Punkten, die der User
  nacheinander/im Batch per Buchstabe beantworten soll -- das ist
  [decision-briefing](../decision-briefing/SKILL.md). **Nicht**, um eine
  Entscheidung erst zu erarbeiten -- das ist [decide](../decide/SKILL.md).
  decision-shot ist reine PRAeSENTATION einer bereits vorliegenden Analyse.

## Abgrenzung (Kurzfassung)

| Skill | Tut was | Wann fertig |
|---|---|---|
| `decide` | Erarbeitet EINE Entscheidung mit einem Framework (Pro/Con-Matrix, Weighted Scoring, Decision Tree, ...) | Analyse steht noch aus |
| `decision-briefing` | Sammelt VIELE offene Entscheidungen eines Themas, legt sie als A/B/C/D-Batch vor, nimmt Buchstaben-Antworten entgegen | Mehrere Punkte sind noch unentschieden |
| `decision-shot` | Verdichtet EINE fertige Analyse (egal woher) auf eine executive Kurzform mit Link zur Vollversion | Analyse liegt schon vor, nur die Darstellung fehlt |
| `knappform` | Genereller Antwortstil-Modifikator fuer JEDE Antwort der Session | Sitzungsweit, themenunabhaengig |
| `paveman` | Kuerzt bestehende PROSA-DATEIEN (Regel-/Gedaechtnisdateien) deterministisch | Kuerzt eine Datei, kein Chat-Output |

`decision-shot` konkurriert mit keinem der vier -- es ist das FORMAT, das nach
`decide` oder neben `decision-briefing` zum Einsatz kommt, sobald die
Essenz weitergegeben werden soll. Der reduzierte Sprachstil orientiert sich
an `knappform`/`paveman` (siehe dort fuer die vollstaendige Streichliste),
wird hier aber konsequent auf ein festes fuenfteiliges Format angewendet.

## Format (verbindlich, fuenf Teile)

```
## <Entscheidungstitel>

**Kontext:** <2-3 Zeilen -- worum es geht, warum jetzt, was auf dem Spiel steht>

**<Option A>**
+ <staerkstes Pro-Argument>
+ <zweites Pro-Argument, nur falls es traegt>
- <staerkstes Contra-Argument>

**<Option B>**
+ <Pro>
- <Contra>
- <Contra>

**Talking Points:**
- <Punkt, der im Gespraech/in einer Mail sofort zieht>
- <Punkt, der einen typischen Einwand vorwegnimmt>

**Empfehlung:** <Option> -- <ein Satz Begruendung, keine Wiederholung der Pro-Liste>

**Vollanalyse:** <Pfad oder Link -- Ticket-Datei, Dokument, Chat-Referenz>
```

## Regeln

- **Nutzertexte ohne technische Nummern/Kürzel (Ich-Form in Alltagssprache):**
  Im sichtbaren Text für den Menschen (Titel, Kontext, Optionen, Talking Points, Empfehlung) stehen **keine** internen Kürzel, Ticketnummern (`T-...`), D-Kennungen oder relative Dateipfade.
  Der Kontext beschreibt die Lage und die geplante Handlung in der Ich-Form („Ich schlage vor...“).
  Technische Referenzen (Ticket-ID, genauer Dateipfad) stehen ausschließlich in der abschließenden Zeile `**Vollanalyse:**` bzw. in einer Referenztabelle.
- **Zeilen sind Budget, kein Ziel.** 2-3 Zeilen Kontext, 2-4 Stichpunkte je
  Option, 2-3 Talking Points, 1 Satz Empfehlung -- mehr wird gestrichen, nicht
  gekuerzt-und-trotzdem-behalten. Passt eine Option nicht in 4 Stichpunkte,
  gehoert sie nicht in diesen Skill, sondern in die Vollanalyse.
- **Reduzierter Stil wie `knappform`/`paveman`:** keine Fuellwoerter, keine
  Floskeln, kein Ausweichen. Verneinungen (`nicht`, `nie`, `kein`, `nur`,
  `außer`) bleiben unangetastet -- ihr Streichen kehrt die Aussage um.
- **Pro/Contra sind Stichpunkte, keine Saetze.** `+`/`-` als Praefix, ein
  Gedanke pro Zeile, kein Nachsatz.
- **Talking Points sind kommunikativ, nicht analytisch.** Sie beantworten
  "was sage ich, wenn mich jemand fragt" -- nicht "was steht in der Analyse".
  Duplikate der Pro/Contra-Liste sind ein Zeichen, dass noch nicht verdichtet
  wurde.
- **Die Empfehlung begruendet sich selbst in einem Satz.** Keine Wiederholung
  der Pro-Liste, kein "siehe oben" -- der eine Satz muss auch ohne den Rest
  des Blocks tragen.
- **Der Link/Pfad zur Vollanalyse ist Pflicht, nicht optional.** decision-shot
  ersetzt die Analyse nicht, es macht sie schnell auffindbar. Fehlt eine
  greifbare Quelle (nur muendlich im Chat entstanden, kein Dokument), den
  Chat-/Session-Bezug so konkret wie moeglich nennen (z. B. "diese Session,
  Antwort zu F4") statt das Feld leer zu lassen.
- **Mehrere zusammengehoerige Entscheidungen** (Gruppe, z. B. mehrere
  Unterfragen eines Themas): ein Block pro Entscheidung, durch `---`
  getrennt, gemeinsamer Kontext nur einmal am Anfang wenn er wirklich fuer
  alle gilt.

### Session-Provenienz bei gespeicherten Decision-Shots

Wird der Decision-Shot als wichtiges neues, dauerhaftes Artefakt gespeichert, endet die Datei mit:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

Die Session-ID kommt zuerst aus einer expliziten Laufzeit-/CLI-Angabe, danach aus einer
autoritativen Provider-Umgebung oder einem Hook; fehlt beides, steht `unbekannt`. Werte nie
erraten. Subagenten verwenden die Elternsession. Routine-Chat, Quellen, Policies, `CLAUDE.md`,
READMEs und Altdateien werden nicht pauschal gestempelt oder nachgestempelt.

## Beispiel

```
## Wo laeuft der naechtliche Backup-Job?

**Kontext:** Ich beobachte wiederholte Ausfälle auf dem Laptop, weil das Gerät nachts
schläft. Ich schlage vor, den Job auf den Mac Studio umzuziehen, der rund um die Uhr läuft.

**Laptop (Status quo)**
+ Keine Netzwerkabhaengigkeit
- Job faellt regelmaessig aus, wenn das Geraet schlaeft
- Kein zentraler Log-Ueberblick

**Mac Studio**
+ Laeuft 24/7, keine Ausfaelle durch Schlafmodus
+ Zentrale Logs an einem Ort
- Braucht funktionierendes Tailscale/SSH als Voraussetzung

**Talking Points:**
- "Der Ausfall ist kein Bug im Skript, sondern eine Standortfrage."
- "Tailscale laeuft schon fuer andere Jobs stabil -- kein neues Risiko."

**Empfehlung:** Mac Studio -- einzige Option ohne den bekannten Schlafmodus-
Ausfall, und die Abhaengigkeit (Tailscale) ist bereits im Betrieb bewaehrt.

**Vollanalyse:** `.SYNC/MAC_STUDIO_COMPUTE_HANDOFF.md`, Abschnitt "Backup-Jobs" (Ticket T-20260620-42)
```

## Changelog

### 1.2.0 (2026-09-18)
- Stilregel für verständliche Entscheidungstexte verankert (T-20260913-883789445, Nutzeranweisung 2026-09-13):
  - Keine Ticketnummern, D-Kennungen oder internen Pfade im sichtbaren Text (Titel, Kontext, Talking Points).
  - Kontext und Empfehlung in natürlicher Alltagssprache in Ich-Form.
  - Technische Ticket- und Pfadreferenzen strikt auf die abschließende Vollanalyse-Zeile begrenzt.

### 1.1.0 (2026-09-09)
- P-018 ergänzt den Session-Stempel für wichtige neu gespeicherte Decision-Shots mit enger
  Quellenpriorität und Ausschlüssen.

### 1.0.0 (2026-08-24)
- Erstversion.
