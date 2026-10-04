---
name: piggyback-hosting
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-02
updated: 2026-08-07
description: Hosting-Muster, um eine lokal gebaute Anwendung (eigene Datenbank, eigener API-Key, In-Process-State) sicher hostbar zu machen, ohne Nutzerverwaltung zu bauen. Kernzug — der Host speichert nichts, der Browser des Besuchers speichert alles — sodass Pro-Besucher-Accounts, Zugriffsprüfungen und Löschfristen gegenstandslos werden, statt gelöst werden zu müssen. Nutzen, wenn eine lokal gebaute App für mehrere Besucher gehostet werden soll, bei "mach das ohne Login hostbar", "keine Nutzerkonten bauen", "Datenschutzerklärung für ein gehostetes Tool verkleinern", "wer ist verantwortlich, wenn wir nichts speichern" oder beim Wählen/Implementieren eines Server-Modus (`local`, `huckepack-gift`, `huckepack-only-host`, `pay-membership`). Liefert eine Data-Flow-Plan-Vorlage, eine Datenschutz-Vorlage und eine rechtliche Ersteinschätzung (DSGVO/TDDDG/UWG, deutsch) als Referenzen.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [hosting, privacy, gdpr, dsgvo, byok, client-side-storage, deployment, no-login]
language: de
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
---

<img src="banner.png" width="100%" alt="piggyback-hosting banner">

# piggyback-hosting

**Ein Hosting-Muster für Anwendungen, die von vornherein niemals fremde
Daten annehmen.**

> Blaupause entstanden am 2026-08-02 beim Bau dreier Call-Agenten.
> Wiederverwendbar für jede Anwendung, die für einen einzelnen lokalen
> Nutzer entworfen wurde, aber auch für andere hostbar sein soll.

## Zum Namen

Im Englischen heißt dieses Muster **piggyback** — auf fremder
Infrastruktur mitreiten ist dort bereits der Fachbegriff dafür. Englischer
Fließtext in diesem Skill sagt daher *piggyback*; **"huckepack" ist der
deutsche Arbeitstitel**, unter dem das Muster gebaut wurde, und zugleich
der Name des Repositories, aus dem dieser Skill migriert wurde. **Die
wörtlichen Modus-Werte bleiben `huckepack-gift` und `huckepack-only-host`**
— sie sind das, was in Code und Konfiguration verschifft wird, genau so
geschrieben, unabhängig davon, in welcher Sprache der umgebende Fließtext
steht.

## Das Problem

Eine Anwendung wird lokal gebaut: eine Datenbank, ein API-Key, State, der
im Prozess lebt. Auf der eigenen Maschine ist das schlicht korrekt. Sobald
jemand sie für andere hostet, wird jede dieser drei Annahmen zu einem Bug —
jeder Besucher teilt sich denselben State, dieselbe Datenbank, denselben
Key. Wer die Seite öffnet, sieht die Daten aller anderen.

Die übliche Lösung ist Nutzerverwaltung: Accounts, Login, Zugriffsprüfungen,
Löschfristen, eine Datenschutzerklärung, ein Auftragsverarbeitungsvertrag.
Oft ein größeres Unterfangen als die Anwendung selbst.

## Die Idee

**Der Besucher behält alles auf dem eigenen Gerät. Der Host behält nichts.**

Das löst die Nutzerverwaltung nicht — es macht sie **gegenstandslos**. Wo
keine fremden Daten auf dem Server liegen, gibt es nichts zwischen
Besuchern abzuschotten, nichts nach Zeitplan zu löschen, und die
Datenschutzerklärung schrumpft auf das, was der Dienst tatsächlich tut.

## Die drei Modi

| Modus | API-Key | Daten | Nutzerverwaltung |
|---|---|---|---|
| **`huckepack-gift`** | vom Host | auf dem Gerät des Besuchers | keine |
| **`huckepack-only-host`** | vom Besucher | auf dem Gerät des Besuchers | keine |
| **`pay-membership`** | des Hosts, abgerechnet | Server | erforderlich |

- **`huckepack-gift`** — der Host liefert seinen eigenen Key und verschenkt
  die Ausführung. Eine reibungslose Einladung, das Tool auszuprobieren.
- **`huckepack-only-host`** — der Besucher bringt seinen eigenen Key mit.
  Der Host zahlt nichts und speichert nichts.
- **`pay-membership`** — bewusst als Stub belassen. Hier wird alles wieder
  nötig, was die anderen beiden vermeiden — Accounts, Abrechnung,
  serverseitige Speicherung. Ein eigenes Unterfangen, kein Schalter zum
  Umlegen.

Es gibt immer einen **`local`**-Standard: wer nichts konfiguriert, bekommt
die Anwendung genau so, wie sie vorher lief, auf der eigenen Maschine.

## Die Bausteine

| Baustein | Zweck |
|---|---|
| Modus als Install-Time-Einstellung | eine Eigenschaft des Deployments, nicht der Session |
| Austauschbare Speicherschicht | dieselbe Datenbank, anderer Ort |
| SQLite im Browser (WASM + OPFS) | dasselbe Schema, dieselben Queries, anderer Ausführungsort |
| Key-Feld, maskiert | nur im `only-host`-Modus, nie geloggt |
| Export und Import | **nicht optional** — Browser-Daten sind flüchtig |
| Beleg als herunterladbare Datei, Zielordner wählbar | kein Server an der Auslieferung beteiligt |

Der eigentliche Engineering-Aufwand liegt darin, die Speicherschicht
austauschbar zu machen: die Anwendung schreibt so oder so nach SQLite,
aber eine Zwischenschicht entscheidet, ob dieses Schreiben auf dem Server
oder im Browser des Besuchers landet (`sql.js` / der offizielle
SQLite-WASM-Build, persistiert über das Origin Private File System). Die
Browser-Speicher-Optionen nach Gewicht ordnen, falls WASM zu schwer ist:
SQLite-WASM + OPFS (eine echte Datenbank, größte Kapazität) > IndexedDB
(strukturiert, eigenes Query-Modell) > `localStorage` (nur für Kleinigkeiten
wie Sprache und Theme geeignet).

## Was dieses Muster nicht löst — offen gesagt

- **Gelöschte Browser-Daten heißt, alles ist weg.** Es gibt keine
  serverseitige Kopie. Deshalb ist Export eine Bedingung, kein Nice-to-have.
- **Kein Gerätewechsel** ohne Export und Import.
- **Der im Browser lebende Key** (`only-host`) ist weniger geschützt als
  einer auf einem Server. Er gehört aber dem Besucher, und die Alternative
  wäre, ihn dem Host zu übergeben — nicht offensichtlich die sicherere Wahl.
- **Die Ausführung läuft weiterhin über den Host.** Bei Diensten, die einen
  Dritten erreichen — etwa einen Telefonanruf — verarbeitet der Host die
  Daten dieses Dritten unabhängig davon, wo die eigenen Aufzeichnungen des
  Besuchers liegen. Eine Datenschutzerklärung wird dadurch nicht
  überflüssig, nur kurz.

## Was die Rechtsprüfung ergab

Eine rechtliche Ersteinschätzung (`references/RECHT.md`, deutsch — sie
prüft deutsche und EU-Vorschriften, weshalb ein Zitieren in Übersetzung
weniger genau, nicht zugänglicher wäre) prüfte das Muster gegen DSGVO,
TDDDG und UWG. **Ersteinschätzung mit Fundstellen, keine Rechtsberatung.**
Drei Befunde in je einer Zeile:

- **Der Host bleibt Verantwortlicher, auch wenn er nichts speichert.**
  Art. 4(7) DSGVO knüpft die Verantwortlichkeit an das Entscheiden über
  Zwecke und Mittel, nicht an die Speicherung; der EuGH hat das ausdrücklich
  so gesagt (C-683/21). Gegenstandslos wird die **Nutzerverwaltung**, nicht
  die Verantwortung.
- **Für die kontaktierte Person schrumpft nichts.** Informationspflichten
  nach Art. 14, eine dokumentierte Abwägung der Rechtsgrundlage, ein
  Auftragsverarbeitungsvertrag mit dem Dienst, der den Kontakt ausführt —
  das sind meist die längsten Abschnitte einer Datenschutzerklärung, und
  das Muster rührt sie nicht an.
- **Die Haushaltsausnahme hilft dem Besucher, nicht dem Host.** Sie deckt
  rein persönliche Nutzung durch eine natürliche Person; ein Dienst, der
  anderen angeboten wird, ist keine rein persönliche Tätigkeit. Genau dort
  beginnt Piggyback-Hosting.

Der Gewinn liegt im **Umfang der Pflichten und der Größe der Angriffsfläche**,
nicht in ihrer Art — was zugleich die ehrlichere Aussage über das Muster ist.

## Wie dieses Muster angewendet wird

1. `references/DATA-FLOW-TEMPLATE.md` lesen und für die tatsächliche
   Anwendung ausfüllen, belegorientiert (jede Zeile braucht ein `file:line`
   oder "nicht gefunden"). Das legt genau offen, welche lokalen Annahmen
   unter Multi-Besucher-Hosting brechen, bevor Code geändert wird.
2. Entscheiden, welche Modi die Anwendung tatsächlich braucht — `local`
   ist immer der Standard; `huckepack-gift` und `huckepack-only-host` sind
   die beiden, die Nutzerverwaltung vermeiden; `pay-membership` bleibt ein
   Stub, solange kein konkreter Grund für echte Accounts besteht.
3. Die Speicherschicht austauschbar machen (der oben genannte Kern-Schritt),
   das maskierte Key-Feld für `only-host` ergänzen und Export/Import
   verdrahten, bevor irgendetwas ausgeliefert wird — es ist das
   Sicherheitsnetz für flüchtigen Browser-Speicher.
4. `references/PRIVACY-TEMPLATE.md` für das konkrete Deployment ausfüllen;
   nicht zutreffende Blöcke löschen, jede Anbieter-Angabe gegen aktuelle
   Verträge prüfen und eine fallbezogene Rechtsprüfung einholen, bevor
   echte Daten verarbeitet werden. Die Vorlage ist ein Ausgangspunkt,
   keine fertige Erklärung.
5. Bei jeder Installation, die echte Dritte betrifft (Telefonanrufe,
   Nachrichten an Personen, die sich nicht selbst angemeldet haben) oder
   Forschungsteilnehmende, die Empfehlungen aus `references/RECHT.md` als
   Checkliste behandeln, nicht als Freigabe — vor dem ersten öffentlichen
   Lauf einen Anwalt einbeziehen.

## Referenzen

- `references/DATA-FLOW-TEMPLATE.md` — Vorlage und Verfahren für einen
  Data-Flow-Plan: jede Zeile braucht ein file:line, sonst ist es eine
  Vermutung, kein Befund.
- `references/PRIVACY-TEMPLATE.md` — Muster-Datenschutzerklärung mit
  markierten Platzhaltern für eine Piggyback-Installation.
- `references/RECHT.md` — rechtliche Ersteinschätzung (deutsch) mit
  DSGVO-, TDDDG- und UWG-Fundstellen.

Beide Vorlagen sind **Muster, keine Rechtsberatung**. Wer eine Anwendung
hostet, passt sie an und ist für das Ergebnis verantwortlich.

## Herkunft

Entstanden beim Bau von HungryCall, Ringedingeding und ResearchCall — drei
Call-Agenten, bei denen ein Data-Flow-Audit zeigte, dass ein unverändertes
Hosting ein Datenschutzvorfall mit angehängtem Namen gewesen wäre. Migriert
aus dem eigenständigen `huckepack`-Repository in diese Skill-Bibliothek.
