---
name: decision-path
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: >
  Erzeugt aus einem Bestand offener und gefallener Entscheidungen einen
  strukturierten ASCII-Abhängigkeitsgraphen (maximal 100 Spalten) für das
  Terminal. Bewertet Knoten nach fünf festen Kriterien: sinnvoll, empfohlen,
  usertypisch (Richtung und decision-avatar-Konfidenz getrennt), zusammenpassend
  und widersprechend; Kanten tragen Beziehungstyp und Belegstatus. Deckt Blocker,
  Freischaltungen, Reihenfolgen und widersprüchliche Empfehlungen gnadenlos auf.
  Nutze diesen Skill bei "welche Entscheidungen hängen voneinander ab",
  "Abhängigkeitsgraph der Entscheidungen", "Entscheidungspfad visualisieren",
  "Widersprüche zwischen Entscheidungen prüfen", "Reihenfolge der Beschlüsse",
  /decision-path. NICHT nutzen, um Entscheidungen erst zu inventarisieren -- das
  macht decision-briefing; NICHT nutzen, um das empfohlene Gesamtkonzept zur
  Abnahme zu bündeln -- das macht decision-draw; NICHT für kompakte Fünfteiler-
  Einzelblöcke mit Optionen und Pro/Contra -- das macht decision-shot; NICHT für
  die Einzelfall-Erwägung mit Frameworks -- das macht decide.
visibility: public
language: de
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, abhaengigkeiten, ascii-graph, decision-path, visualisierung, routing, widerspruchs-erkennung]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-draw, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
---

<img src="banner.png" width="100%" alt="decision-path banner">

# decision-path — ASCII-Abhängigkeitsgraph offener Entscheidungen

> Entscheidungen fallen nicht im luftleeren Raum. Was isoliert betrachtet
> vernünftig wirkt, blockiert oft Folgearbeiten, erfordert unfertige Vorstufen
> oder hebelt bestehende Schutzverträge aus. decision-path macht Kausalitäten,
> Reihenfolgen und Widersprüche im Terminal transparent sichtbar.

---

## Wann nutzen

- Ein Vorlagenbestand offener Entscheidungen (aus [decision-briefing](../decision-briefing/SKILL.md) Phase 1, einem Session-Kontext oder einer Entscheidungsvorlage) soll strukturiert werden.
- Es muss geklärt werden, welche Entscheidungen sofort frei entscheidbar sind (Wurzelknoten) und welche an Vorbedingungen oder externen Blockern hängen.
- Ein Überblick ist gefragt, welche Empfehlungen miteinander harmonieren und wo sich zwei Beschlüsse logisch oder organisatorisch widersprechen.
- Trigger-Wörter: `/decision-path`, "welche Entscheidungen hängen voneinander ab", "Abhängigkeitsgraph der Entscheidungen", "Entscheidungspfad visualisieren", "Entscheidungsbaum ASCII", "Widersprüche zwischen Entscheidungen", "Kausalitäten prüfen".
- **Nicht** nutzen:
  - Zum erstmaligen Erfassen und Inventarisieren von offenen Fragen — das macht [decision-briefing](../decision-briefing/SKILL.md) Phase 1.
  - Zur Bündelung der empfohlenen Varianten zu einem zusammenhängenden Gesamtbild zur Abnahme — das macht [decision-draw](../decision-draw/SKILL.md).
  - Für kompakte Fünfteiler-Einzelblöcke mit Optionen und Pro/Contra je Option — das macht [decision-shot](../decision-shot/SKILL.md).
  - Zur methodischen Erarbeitung einer einzelnen komplexen Fragestellung (Weighted Scoring, Szenarien) — das macht [decide](../decide/SKILL.md).

---

## Abgrenzung in der Entscheidungs-Familie

| Skill | Aufgabe | Input | Output |
|---|---|---|---|
| `decide` | Erarbeitet **eine einzelne** Entscheidung methodisch | Kriterien, Optionen | Bewertungsmatrix, Einzelentscheidung |
| `decision-briefing` | **Zerlegt viele** offene Entscheidungen in Einzelfragen mit Optionen | Liste offener Punkte | Nummeriertes A/B/C/D-Briefing, Grobmarkierungen, Buchung |
| `decision-path` | **Validiert und visualisiert Kausalitäten und Widersprüche** über viele Entscheidungen | Grobmarkierungen aus Briefing / Register | ASCII-Abhängigkeitsgraph mit 5 Knotenbewertungen und Kantenstatus |
| `decision-draw` | **Bündelt Empfehlungen zu einem Gesamtbild** zur Abnahme als Ganzes | Bündel aus `decision-path` | Konzept, Zusammenspiel (nur empfohlene Variante), Rücktransfer |
| `decision-shot` | Komprimiert **fertige Analysen** auf die Essenz (1 Entscheidung oder enges Bündel) | 1 analysierte Frage oder Gruppe | Fünfteilige Kurzfassung mit Optionen, Pro/Contra und Vollanalyselink |
| `decision-avatar` | Liefert die **Modellierung von Nutzerpräferenzen** | Kontext, bisherige Beschlüsse | Konfidenzbewertung 🟢 / 🟡 / 🔴 |

### Vertrag und Zuständigkeit gegenüber decision-briefing

`decision-briefing` Phase 1 ermittelt beim Einlesen bereits grob Abhängigkeiten und Reihenfolgen (z. B. aus Signalwörtern wie „Danach automatisch:“, Blockern oder Ticket-Bezügen). `decision-path` leitet diese Struktur nicht stillschweigend ein zweites Mal her, sondern setzt direkt auf diesen Grobmarkierungen auf:

1. **decision-briefing liefert die Grobmarkierungen:** Es stellt das rohe Inventar offener Entscheidungen und deren erste Koppelungssignale bereit.
2. **decision-path validiert, bewertet und visualisiert:** Es prüft die Signale gegen den realen Belegstand, trennt gesicherte von vermuteten Kanten, vergibt die fünf Bewertungen je Knoten und deckt Gate-Kollisionen schonungslos auf.
3. **Rückmeldung bei Diskrepanzen:** Findet `decision-path` eine Abhängigkeit, die im Briefing fehlt oder unvollständig erfasst war, übernimmt es sie niemals stillschweigend, sondern meldet sie als Korrektur-Notiz an das Briefing zurück.

---

## Die fünf Bewertungen je Knoten (und Kanten-Belegstatus)

Die fünf Dimensionen `[S E U Z W]` bewerten die **Knoten** (die anstehenden oder gefallenen Entscheidungen im systemischen Kontext). Kanten tragen ihren semantischen Beziehungstyp (z. B. freischaltend, blockierend, voraussetzend) sowie ihren Belegstatus (gesichert vs. vermutet).

Jeder Knoten im Graphen trägt eine kompakte Bewertungszeile mit genau fünf Dimensionen:

```
[S+ E:<Option> U<Richtung><Konfidenz> Z+ W-]
```

1. **sinnvoll (`S`)** — Fachliche und architektonische Tragfähigkeit:
   - `S+`: Lösung ist robust, löst ein reales Problem, vermeidet unnötige Komplexität.
   - `S~`: Teilweise sinnvoll, birgt aber Wartungs- oder Prozessrisiken.
   - `S-`: Scheinlösung, Aktionismus oder bekannter Holzweg (z. B. Filter am falschen Hebel).

2. **empfohlen (`E`)** — Die konkrete, faktenbasierte Handlungsempfehlung:
   - `E:<Option>`: Klare Option (z. B. `E:A`, `E:B`, `E:klaeren`, `E:Schritt1`).
   - `E-`: Keine Empfehlung möglich (etwa bei fehlenden Fakten oder echter Grundsatzfrage).

3. **usertypisch (`U`)** — Übereinstimmung mit Arbeitsweise und Regeln des Nutzers (via `decision-avatar`):
   Kodiert **Richtung** (Passt die Option zur Arbeitsweise?) und **Belegsicherheit / Konfidenz** getrennt:
   - **Richtung (erstes Zeichen nach U):**
     - `+`: Usertypisch — entspricht historisch belegten Entscheidungen, Richtlinien (`CLAUDE.md`, Policies) oder expliziten Nutzerpräferenzen.
     - `~`: Neutral / offen — keine ausgeprägte Präferenzrichtung belegbar.
     - `-`: Untypisch — bricht mit gewohnter Arbeitsweise oder bisherigen Mustern des Nutzers.
   - **Belegsicherheit / Konfidenz (zweites Zeichen):**
     - Im ASCII-Graphen rein ASCII:
       - `!`: Hoch / gesichert (in Prosa: 🟢 belegt).
       - `~`: Mittel / plausibel (in Prosa: 🟡 Wertungsentscheidung, Nutzerabwägung erforderlich).
       - `?`: Niedrig / ungesichert (in Prosa: 🔴 Neuland, Grundsatzfrage). **Eskalieren statt raten!**
   - *Beispiele:* `U+!` (usertypisch und belegt), `U+~` (usertypisch, aber Abwägungssache), `U-!` (belegt untypisch), `U~?` (offen, keine Vorgabe -> Eskalation).

4. **zusammenpassend (`Z`)** — Weiche stilistische und architektonische Passung mit Nachbarn:
   - `Z+`: Passt stilistisch und architektonisch nahtlos zusammen; bildet ein schlüssiges Ganzes ohne Reibung.
   - `Z~`: Leichte stilistische Reibung oder organisatorischer Mehraufwand, aber funktional verträglich.
   - `Z-`: Reibt spürbar im Systemverbund (z. B. Konfigurations-Wildwuchs, unsaubere Kopplung, Paradigmenbruch), verletzt aber noch keine harte Regel.

5. **widersprechend (`W`)** — Harter Widerspruch und Regel-/Gate-Verletzung (**wichtigste Ausgabe — Alarm!**):
   - `W-`: Widerspruchsfrei gegenüber anderen Empfehlungen, verbindlichen Richtlinien und aktiven Schutz-Gates.
   - `W+`: **Harte Kollision / Alarm!** Hebt eine andere Empfehlung auf, verletzt eine verbindliche Policy (`CLAUDE.md`, P-00x) oder missachtet ein aktives Schutz-Gate. Kollidierende Knoten werden immer zwingend im Abschnitt `WIDERSPRUECHE` mit Ursache und Auflösungsweg aufgeführt.

---

## Kanten-Typen und Ableitungsregeln

Abhängigkeiten werden **strikt aus den Quelltexten abgeleitet**, niemals spekulativ erfunden. Kanten tragen ihren Beziehungstyp und ihren Belegstatus:

| Signal im Text | Kanten-Typ | Notation | Bedeutung |
|---|---|---|---|
| „Danach automatisch: …“, „gibt frei“, „ermöglicht“ | Schaltet frei | `+-->` | Zielentscheidung wird erst durch Quellentscheidung ausführbar (belegt) |
| „blockiert“, „verhindert“, „Schutz-Gate greift“ | Blockiert | `=>` | Ziel ist blockiert, solange Quelle nicht gelöst ist |
| „setzt voraus“, „braucht zuvor“, „Vorbedingung“ | Setzt voraus | `-->` | Ziel verlangt chronologisch und logisch den Quellentscheid |
| „Folgeentscheidung“, „Schritt 2 danach“ | Reihenfolge | `-->` | Logischer Folgeschritt nach Vollzug |
| „ist durch Messung widerlegt“, „überholt“, „hinfällig“ | Entwertet | `--X-->` | Quellerkenntnis macht Zielposten obsolet |
| Gleiche D-ID, Ticket-ID oder gleiches System ohne Textbeleg | Vermutet | `?-->` | Plausible Koppelung ohne expliziten Kausalnachweis (unbelegt) |

> **Regel für unbelegte Kanten:**
> Wo kein expliziter Kausalbeleg im Text vorliegt, wird die Kante als vermutet (`?-->`) gekennzeichnet — niemals als gesicherte Tatsache. Wo gar kein Zusammenhang belegt ist, stehen die Knoten unabhängig nebeneinander.

---

## Formatvorgaben für den ASCII-Graphen

1. **Monospace & Terminal-Gerecht:** Maximale Zeilenbreite **100 Spalten**. Keine breiten Tabellen, die im Terminal umbrechen.
2. **Zeichensatz & Reinheit:** Reines ASCII. Innerhalb des Graphen-Codeblocks dürfen keine Emojis (🟢🟡🔴) vorkommen; Konfidenzen werden dort ausschließlich über ASCII-Zeichen (`!`, `~`, `?`) codiert.
3. **Knoten-IDs:** Ausschließlich vorhandene Kürzel (`PD-A`, `MD-A`, `BH-A`, `VM-A`, `QR-A`, `CL-A`, `MO-A`, `D-001`, `732597768`). Niemals neue Kunst-IDs erfinden! Fehlt ein Kürzel, gilt die Postennummer. Interne Folgeschritte werden als unnummerierte Annotationen `(...)` an der Kante geführt.
4. **Ebenen-Gliederung:**
   - `EBENE 0 - haengt an nichts`: Wurzelknoten, unblockierte Entscheidungen, externe Hebel.
   - `EBENE 1 - haengt an genau einer`: Direkte Folgeentscheidungen.
   - `EBENE 2 - haengt an mehreren / tiefe Kette`: Mehrfach abhängige oder nachgelagerte Knoten.
   - `WIDERSPRUECHE`: Harte Widersprüche, Gate-Kollisionen und inkonsistente Empfehlungen (`W+`).
   - `LEGENDE`: Pflichtbestandteil jedes Graphen. Jedes im Graphen verwendete Strukturzeichen (`|`, `=Option`, `(...)`, Kantenpfeile) muss in der Legende aufgeführt und erklärt werden.
5. **Optionale Mermaid-Projektion:** Darf bei Bedarf als zusätzliches Code-Fence (`mermaid`) angehängt werden, wenn es ohne Mehraufwand abfällt. Der ASCII-Graph bleibt die verbindliche primäre Ausgabe.

---

## Beispiel (Pilotauszug: Ticket-Master 2026-09-13)

Realer Auszug aus der Entscheidungsvorlage des Ticket-Masters (`732597768`, `MO-A`, `CL-A`, `QR-A`, `387521104`, `CL-B`):

```
====================================================================================================
DECISION-PATH: ABHAENGIGKEITSGRAPH (Pilot Ticket-Master 2026-09-13)
====================================================================================================

EBENE 0 - haengt an nichts (Wurzelentscheidungen & externe Blocker)
  [732597768] GitHub-Billing klaeren                        [S+ E:klaeren U+! Z+ W-]
      |  schaltet frei
      +--> [MO-A] Welle 2 freigeben                         [S+ E:A       U+~ Z+ W-]

  [CL-A] clutch Admin-Merge PR #6 & PR #8                   [S+ E:A       U+! Z+ W-]
      |  blockiert durch: [Gate "1 Approving Review" (Self-Approval unmoeglich)]
      --> (Folgeentscheidung: Branchschutz auf 0 oder Bot anpassen)

  [QR-A] Queue-Rename Junction (_TICKETS -> TICKETS)        [S+ E:B       U+! Z+ W-]
      +--> [387521104] Nachtfenster faehrt                  (belegt: nur unter B)

  [CL-B] Review-Gate-Pilot: Mac-Signierschluessel           [S+ E:Schritt1 U+~ Z+ W-]
      --> (Folgeschritte 2-4: Modell-Automatisierung nach Schluessel-Bereitstellung)

EBENE 1 - haengt an genau einer Vorbedingung
  [MO-A] Welle 2 freigeben                                  [S+ E:A       U+~ Z+ W-]
      |  setzt voraus: [732597768] (Billing geklaert, Remote-CI-Gates wieder aktiv)
      |  setzt voraus: [Gate PRIVATE.txt "gruenes Remote-CI"]
      --> (Folgeschritt: Sichtbarkeit schalten bleibt reine Nutzerhandlung)

EBENE 2 - haengt an mehreren / tiefe Kette
  [387521104] Nachtfenster Migration autonom fahren         [S+ E:B       U+! Z+ W-]
      |  setzt voraus: [QR-A]=B (NTFS-Junction gesetzt)
      |  setzt voraus: (Junction auf dem zweiten Host per Transfer-Ticket gesetzt -
      |                  Ticketnummer in der Vorlage nicht genannt)

----------------------------------------------------------------------------------------------------
WIDERSPRUECHE & GATE-KOLLISIONEN
----------------------------------------------------------------------------------------------------
  [MO-A]=B  X  [Gate PRIVATE.txt "gruenes Remote-CI"]
               Konflikt: Option B wuerde Welle 2 rein auf lokaler Testbasis freigeben,
               obwohl zwei Modulvertraege ausdruecklich gruenes Remote-CI fordern.
               Aufloesung: Empfehlung A erzwingt erst [732597768] (Billing), heilt Kollision.

  [CL-A]=StatusQuo  X  [Gate "1 Approving Review" (Self-Approval unmoeglich)]
               Konflikt: master verlangt 1 Review, einziges Repo-Konto ist lukisch.
               Aufloesung: Empfehlung A (Admin-Merge) bricht Blockade legitim auf.

----------------------------------------------------------------------------------------------------
LEGENDE & BEWERTUNGSSCHLUESSEL
----------------------------------------------------------------------------------------------------
  Kanten & Struktur:
    +-->   schaltet frei (Kausalitaet im Quelltext belegt)
    =>     blockiert / verhindert (Gate oder externer Blocker)
    -->    setzt voraus / Reihenfolge (Vorbedingung oder Folgeschritt)
    ?-->   vermutete Abhaengigkeit (Koppelung plausibel, aber unbelegt)
    --X--> entwertet / ueberholt (macht Zielposten obsolet)
    X      Widerspruch / Kollision (Gate- oder Regelverletzung)
    |      vertikaler Verbindungsstrang / Attribut-Zuordnung
    [ID]   Entscheidungsknoten (Kuerzel oder Postennummer aus Vorlage)
    [Gate]  externes Gate / Regel / Vertrag - KEIN Entscheidungsknoten
    =Opt   spezifische Option eines Knotens (z. B. [MO-A]=B)
    (...)  unnummerierte Kanten-Annotation / Folgeschritt (keine neue ID)

  Knoten-Status [S E U Z W]:
    S: Sinnvoll      (+ tragfaehig / ~ mit Vorbehalt / - ungeeignet)
    E: Empfohlen     (A, B, C, klaeren, Schritt1, - keine Empfehlung)
    U: Usertypisch   (Richtung: + typisch / ~ neutral / - untypisch;
                      Konfidenz: ! gesichert / ~ Abwaegung / ? Eskalation)
                      [! = belegt (Prosa gruen), ~ = Nutzerabwaegung (Prosa gelb),
                       ? = ungesichert / Eskalation (Prosa rot)]
    Z: Zusammenpass. (+ harmoniert stilistisch / ~ Reibung / - Architektur-Bruch)
    W: Widerspruch   (- widerspruchsfrei / + harte Kollision mit Gate oder Regel)
====================================================================================================
```

---

## Was decision-path NICHT tut

1. **Keine Entscheidungen fällen:** Der Skill liefert eine transparente Kartierung der Lage. Die Entscheidungsgewalt verbleibt beim Nutzer.
2. **Keine Optionen erarbeiten:** Der Skill diskutiert keine neuen Varianten oder Kriterienkataloge; das ist die Aufgabe von [decide](../decide/SKILL.md) oder [decision-briefing](../decision-briefing/SKILL.md).
3. **Kein Rückschreiben ins Register:** Der Graph modifiziert keine Register- oder Ticketdateien. Das Rückschreiben nach erfolgter Entscheidung erfolgt durch [decision-briefing](../decision-briefing/SKILL.md) Phase 4 oder über die Rücktransfer-Mechanik von [decision-draw](../decision-draw/SKILL.md).
4. **Keine unverständlichen Kryptokürzel im Fließtext an den Nutzer:** Werden die Ergebnisse des Graphen dem Nutzer erläutert, gilt die verbindliche Stilregel (T-20260913-883789445): 2–4 Sätze Alltagssprache in Ich-Form (Lage, „Ich mache …“, Rückfall). Knotenbeschriftungen nutzen lesbare Kurztitel. Technische Kennungen und Ticketnummern wandern in eine Anhangstabelle.

---

## Session-Provenienz

Wird der Abhängigkeitsgraph als dauerhaftes Analyse-Artefakt gespeichert, endet das Dokument mit:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- Quellenpriorität: Explizite Laufzeit-/CLI-Angabe, danach autoritative Provider-Umgebung oder Hook, sonst `unbekannt`.
- Subagenten erben die Session-ID der Elternsession.
- Routine-Chat und temporäre Terminal-Ausgaben erhalten keinen Stempel.

---

## Changelog

### 1.1.0 (2026-09-18)
- Stilregel für verständliche Entscheidungstexte verankert (T-20260913-883789445, Nutzeranweisung 2026-09-13):
  - Erläuterungen an den Nutzer in natürlicher Ich-Form ohne Nummernflut.
  - Lesbare Kurztitel für Knoten im Terminal-Graph.
  - Technische Zuordnung (Ticket-/D-Nummern) in Anhangstabelle ausgelagert.

### 1.0.0 (2026-09-13)
- Erstfassung auf Basis des Nutzerauftrags T-20260913-107991667.
- Fünfteiliger Bewertungsschlüssel je Knoten (sinnvoll, empfohlen, usertypisch mit getrennter Richtung und Konfidenz via `decision-avatar`, zusammenpassend, widersprechend); Kanten tragen Beziehungstyp und Belegstatus.
- Verbindlicher Vertrag mit `decision-briefing`: Briefing liefert Grobmarkierungen, decision-path validiert und visualisiert; Rückmeldung bei Diskrepanzen.
- Scharfe Abgrenzung zu `decision-shot` über Ausgabeformat (kompakte Fünfteiler mit Optionen und Pro/Contra).
- Korrektur der Kausalstruktur: CL-A am Approval-Gate statt Billing; Beseitigung erfundener IDs zugunsten unnummerierter Kantenannotationen.
- Konsistente ASCII-Spezifikation (max. 100 Spalten) mit einheitlicher Kantennotation `--X-->`, vollständiger Strukturlegende und emoji-freiem Graphencode.
