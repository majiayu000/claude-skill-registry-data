---
name: decision-draw
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: >
  Verdichtet gebündelte offene Entscheidungen zu EINEM zusammenhängenden,
  prosa-basierten Gesamtkonzept auf Basis aller empfohlenen Varianten.
  Zeigt, wie die Teilsysteme nach der Umsetzung konkret ineinandergreifen,
  statt den Nutzer durch Dutzende isolierte Einzelfragen zu zwingen. Der Nutzer
  nimmt das Bild als Ganzes ab oder gibt zielgerichtete Korrekturen, die
  automatisch in Einzelentscheidungen übersetzt und über decision-briefing
  Phase 4 ins Register zurückgeschrieben werden. Nutze diesen Skill bei
  "wie sieht das Ganze aus wenn wir allem zustimmen", "zeichne mir das Gesamtbild",
  "Gesamtkonzept der Entscheidungen", "decision draw", /decision-draw, "wie greifen
  die Systeme zusammen". NICHT nutzen, wenn Alternativen pro Einzelpunkt
  diskutiert werden sollen -- das macht decision-briefing; NICHT für den
  Abhängigkeitsgraphen -- das macht decision-path; NICHT für strukturierte
  Einzelblöcke mit Optionen und Pro/Contra (auch bei eng zusammengehörigen
  Gruppen) -- das macht decision-shot; NICHT zur Herleitung einer einzelnen
  Entscheidung -- das macht decide.
visibility: public
language: de
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, konzeptbild, gesamtabnahme, buendelung, zusammenspiel, ruecktransfer, workflow]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-path, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
---

<img src="banner.png" width="100%" alt="decision-draw banner">

# decision-draw — Gesamtbild und Abnahme gebündelter Entscheidungen

> Wenn fünf oder zehn Entscheidungen anstehen, verliert man im Klein-Klein der
> Optionen leicht den Blick für das entstehende System. decision-draw beschreibt
> nicht die Alternativen, sondern das funktionierende Ganze: Wie arbeiten die
> Systeme zusammen, wenn alle Empfehlungen angenommen werden? Der Nutzer nimmt
> das Bild als Ganzes ab oder korrigiert gezielt.

---

## Wann nutzen

- Mehrere zusammenhängende Entscheidungen (aus [decision-briefing](../decision-briefing/SKILL.md) oder einer Entscheidungsvorlage) sollen nicht als zäher Einzelfragen-Katalog abgearbeitet werden.
- Der Nutzer möchte vor dem Beschluss sehen, wie die Komponenten nach der Umsetzung im Alltag tatsächlich zusammenwirken.
- Aus dem Abhängigkeitsgraphen ([decision-path](../decision-path/SKILL.md)) wurde ein Bündel eng gekoppelter Entscheidungen identifiziert, das als funktionale Einheit abgenommen werden kann.
- Trigger-Wörter: `/decision-draw`, "wie sieht das Ganze aus wenn wir allem zustimmen", "zeichne mir das Gesamtbild", "Gesamtkonzept der Entscheidungen", "decision draw", "wie greifen die Systeme danach zusammen", "Bild zur Gesamtabnahme".
- **Nicht** nutzen:
  - Wenn der Nutzer einzelne Optionen je Frage abwägen und per Buchstabe (A/B/C) wählen will — das macht [decision-briefing](../decision-briefing/SKILL.md).
  - Zur reinen Kausal- und Blockaden-Analyse im Terminal — das macht [decision-path](../decision-path/SKILL.md).
  - Zur isolierten Optionen-Abwägung in 5-teiligen Einzelblöcken (Kontext, Pro/Contra je Option, Empfehlung) für Einzelfragen oder eng zusammengehörige Gruppen — das macht [decision-shot](../decision-shot/SKILL.md).
  - Zur methodischen Erarbeitung einer einzelnen offenen Grundsatzfrage — das macht [decide](../decide/SKILL.md).

---

## Abgrenzung in der Entscheidungs-Familie

| Skill | UX & Fokus | Haltung zu Optionen | Abnahmeform |
|---|---|---|---|
| `decision-briefing` | **Zerlegt** in Einzelfragen | Zeigt alle Optionen A/B/C/D | Buchstabencodes (`1A 2C 3B`) |
| `decision-path` | **Strukturiert** Kausalitäten | Bewertet Optionen im Graphen | Diagnose im Terminal (ASCII) |
| `decision-draw` | **Zusammenhängendes Zielbild** (bündelt vernetzte Entscheidungen) | Beschreibt **nur die empfohlene Variante** (Alternativen verlinkt) | Gesamtabnahme oder Korrektursatz |
| `decision-shot` | **Strukturierte Einzelblöcke** (für Einzelfragen oder enge Gruppen) | Zeigt Optionen mit 2–4 Pro/Contra-Punkten | Executive Decision / Einzelabnahme |
| `decide` | **Erarbeitet** Einzelfall | Bewertungsmatrix (Kriterien) | Analytische Empfehlung |

> **Zentrale Regel:**
> `decision-draw` beschreibt **ausschließlich die empfohlene Variante**. Die verworfenen Alternativen sind nicht verschwunden — sie sind in [decision-briefing](../decision-briefing/SKILL.md), [decision-shot](../decision-shot/SKILL.md) oder den verlinkten Tickets dokumentiert und werden im Header verlinkt. Ein Draw ohne diesen Verweis würde dem Nutzer die Wahl nehmen, statt sie ihm zu erleichtern.

---

## Verbindliche Stilregel: Nutzertexte ohne Kürzel und Nummern

> **Kanonische Nutzeranweisung (Feedback 2026-09-13 / Ticket T-20260913-883789445):**
> *„Die decision draws sind mir zu technisch, das muss ohne Nummer sein, die kennst du im Hintergrund oder nutzt du zur Texterstellung [...].“*

1. **Keine technischen Kürzel im sichtbaren Nutzertext:**
   Im sichtbaren Fließtext für den Menschen (Bündel, Konzept, Zusammenspiel, Umsetzung, Abfrage) stehen **keine** internen Kürzel (wie `BH-A`, `MD-A`, `HA-A`, `PRA`), keine Ticketnummern (`T-2026...`), keine D-Nummern (`D-2026...`), keine relativen Pfade, Git-Hashes oder Messwerte.
2. **Je Posten 2–4 Sätze Alltagssprache in Ich-Form:**
   Jeder Posten des Bündels wird nach dem Dreiklang formuliert:
   - *Lage:* Was ist die aktuelle Ausgangssituation?
   - *„Ich mache …“:* Was plane ich konkret / was ist meine Handlungsempfehlung?
   - *Rückfall:* Was passiert, wenn das scheitert oder was entscheidet der Nutzer danach?
   *(Beispiel: „Hermes unterstützt bei Tasks nur Englisch. Ich melde das bei Hermes als Issue und für uns bauen wir einen Workaround. Es liegen im Moment nicht nutzbare Altsessions vor. Ich versuche die wieder nutzbar zu machen. Wenn das nicht klappt, gebe ich dir eine zufällige Stichprobe aus 10 Sessions und fasse diese zusammen — so kannst du entscheiden, ob eine Rettung sinnvoll ist.“)*
3. **Klartext-Titel zur Orientierung:**
   Jeder Posten trägt einen verständlichen deutschen Titel (z. B. *„Modell-Backend als eigenes Herzstück“*, *„Sichere Deploy-Schlüssel auf dem Mac“*). Der Nutzer interagiert über diesen Titel oder gibt eine Gesamtabnahme.
4. **Technische Zuordnung ausschließlich im Anhang:**
   Die Übersetzung zwischen Klartext-Titel, internem Kürzel, Ticket-ID und Register-Zustand erfolgt **ausschließlich in einer abschließenden Anhangstabelle** am Ende des Dokuments. Dort — und nur dort — greifen die automatisierten Parser und Register-Rückschreiber.

---

## Verbindlicher Aufbau (acht Teile)

Ein vollständiger `decision-draw` folgt ausnahmslos dieser Struktur:

### 1. Bündel und Umfang (im Klartext)
Übersicht der gebündelten Posten in Alltagssprache (Ich-Form, 2–4 Sätze je Punkt, keine IDs/Kürzel im Text).

### 2. Konzept
Der angestrebte Zielzustand als zusammenhängender Fließtext in Prosa:
- Was für eine Systemlandschaft oder welcher Workflow entsteht, wenn alle Empfehlungen genau so umgesetzt werden?
- Keine Optionen-Gegenüberstellung, kein Konjunktiv-Nebeneinander („man könnte auch“).
- Klarer, präziser Indikativ: So arbeitet das System im Zielzustand.

### 3. Zusammenspiel
Das funktionale Herzstück des Skills:
- Wie greifen die entschiedenen Teile **nach** der Umsetzung real ineinander?
- Darstellung bevorzugt entlang eines konkreten End-to-End-Ablaufs statt einer bloßen Komponentenliste.
- Macht Datenflüsse, Schnittstellen und Zuständigkeiten greifbar.

### 4. Umsetzung
Die konkrete Realisierungsreihenfolge:
- Was passiert real in der Praxis?
- Übernimmt Kanten- und Abhängigkeitslogik direkt aus [decision-path](../decision-path/SKILL.md).
- Unabhängige Arbeitsstränge werden ehrlich als parallel dargestellt (keine künstlichen Kausalketten erfinden; ein Bündel darf aus mehreren parallelen Strängen bestehen). Reihenfolgen werden nur dort behauptet, wo belegte Abhängigkeiten oder Fristen existieren.
- Benennt Gates, Migrationsschritte und Checks.

### 5. Was dieses Bild nicht abdeckt
Schutz vor Scheinvollständigkeit:
- Welche Randfragen, offenen Punkte oder 🔴-Konfidenzen bleiben bewusst ausgeklammert?
- Wo liegen die Schnittstellengrenzen zu Nachbarsystemen?
- Ein Bild, das seine Ränder verschweigt, erzeugt falsche Sicherheit.

### 6. Abnahme
Die Interaktion mit dem Nutzer:
- Der Nutzer prüft das Bild als Ganzes.
- Antwortmöglichkeit 1: **Ausdrückliche Gesamtabnahme** („Passt so“, „Abnahme“, „So umsetzen“). Nur hierbei werden alle Posten des Bündels als entschieden verbucht.
- Antwortmöglichkeit 2: **Korrektur über Klartext-Titel oder in Alltagssprache** („Beim Mac-Deploy lieber kein Auto-Restart“, „VersicherungsManager erst mal vertagen“). Führt zur Zerlegung in Einzelentscheidungen; alle unkorrigierten Posten bleiben offen.

### 7. Rücktransfer
Die systematische Übersetzung von Nutzerkorrekturen in Einzelbeschlüsse:
- **Keine automatische Mitbuchung:** Nur bei ausdrücklicher Gesamtabnahme werden die unveränderten Posten gebucht. Eine Teilkorrektur ist **keine** Gesamtabnahme!
- **Isolierung bei Korrekturen:** Kommt eine Korrektur, wird sie in Einzelentscheidungen zerlegt; alle übrigen Posten des Bündels bleiben strikt **offen** (im Quellregister / der Vorlage), bis der Nutzer das bereinigte Bild als Ganzes annimmt oder die verbliebenen Posten einzeln bestätigt.
- **Pflicht-Tabelle des Rücktransfers:** Jede Korrektur-Rückmeldung erzeugt zwingend eine strukturierte Auswertungstabelle mit vier Spalten (Originalkorrektur, Betroffene Kürzel, Domino-Status, Offene Mehrdeutigkeiten).
- **Ausschließlicher Schreibweg über Phase 4:** `decision-draw` besitzt **keinen** eigenen Schreibweg ins Register. Die Verbuchung erfolgt **ausschließlich** über das standardisierte Verfahren aus [decision-briefing](../decision-briefing/SKILL.md) Phase 4.

### 8. Anhang: Technische Referenztabelle (nur für Buchung & Audit)
Kompakte Tabelle am Dokumentenende mit:
`| Klartext-Titel | Internes Kürzel / ID | Ticket-Referenz | Unterstellte Empfehlung | Konfidenz | Link / Details |`

---

## Beispiel (Pilotauszug: Ticket-Master 2026-09-13 — BACH & Systemverbund)

```markdown
# DECISION-DRAW: BACH-Kernverbund & Betriebsintegrität

## 1. Bündel und Umfang

- **Modell-Backend als eigenes Herzstück:** Die Modellzuteilung ist aktuell eng mit dem Monolithen verzahnt. Ich lagere das Backend als eigenständiges Kernmodul aus, damit Rechte und Budgets unabhängig geprüft werden. Scheitert ein externer Dienst, schaltet das System automatisch auf das lokale Reservemodell zurück.
- **Sichere Deploy-Schlüssel auf dem Mac:** Auf dem Mac laufen Dauerprozesse, die bei harten Updates unsauber abbrechen können. Ich richte einen lesenden Schlüssel und ein Meldeskript ein, das Aktualisierungen anzeigt, ohne laufende Dienste abzuschießen. Sollte ein Dienst dennoch hängen, meldet der Watcher das direkt an die Betriebsübersicht.
- **Einheitliche Konfigurations-Sollwerte:** Die beiden Hauptrechner nutzen teilweise unterschiedliche Spracheinstellungen. Ich gleiche die Konfigurationen über das gemeinsame Sync-Verzeichnis an, lasse dem Laptop aber ausreichend Spielraum für mobile Tests.
- **Feste Zeitzone im VersicherungsManager:** Datumsberechnungen bei Fristen hängen bisher vom Betriebssystem ab. Ich verankere eine feste Zeitzone in den Anwendungseinstellungen, damit Fristen überall auf die Minute genau übereinstimmen.
- **Öffentliche Bereitstellung der USMC-Dokumentation:** Die Modul-Dokumentation ist im Webauftritt noch als privat markiert und löst Prüfwarnungen aus. Ich korrigiere die Sichtbarkeit auf öffentlich, damit der nächtliche Seiten-Bau ohne Fehler durchläuft.

---

## 2. Konzept

Wir etablieren ein sauberes, entkoppeltes Multi-Host-System, bei dem das Modell-Backend
als eigenständiges Kernmodul `agents-heart` betrieben wird. Rechte und Budgets liegen
strukturiert in einer SQLite-Datenbank, während Zuteilungsentscheidungen zweistufig
fallen: BACH ermittelt fachlich fundiert die Kandidatenmenge, clutch wählt darin
preis- und kapazitätsoptimal das finale Modell.

Auf dem Mac Studio laufen die 24/7-Dienste geschützt und stabil über einen read-only
Deploy-Key; Updates ziehen automatisch ein, benachrichtigen den Operator bei laufenden
Diensten aber sanft, statt Hintergrundprozesse hart abzuschießen. Konfigurationen
dürfen dort bewusst hostspezifisch auf Leistung abgestimmt sein, während app-weite
Einstellungen (wie Zeitzonen im VersicherungsManager nach dem bewährten routinika-Muster)
deterministisch fest verdrahtet sind. USMC bleibt der kanonische öffentliche
Memory-Baustein und behält seinen festen Platz im Webauftritt.

---

## 3. Zusammenspiel

Die fünf Posten bilden keine serielle Kausalkette, sondern stellen modular entkoppelte Bausteine der täglichen Betriebsintegrität dar, die im Gesamtsystem parallel ineinandergreifen:

- **Kernarchitektur & Modell-Routing (`BH-A`):** Das Modul `agents-heart` entkoppelt die Modellzuteilung. Trifft eine Aufgabe ein, ermittelt BACH fachbezogen die Kandidatenmenge und clutch wählt kosten- und kapazitätsoptimal das Modell.
- **Host-Konfiguration & Deploy-Integrität (`CF-A`, `MD-A`):** Während auf dem Laptop und der Workstation konsistente Reasoning-Stufen gelten (`CF-A`; hostabhängige Modelle bleiben transparent), betreibt der Mac Studio seine persistenten Hintergrundprozesse unter validierten Einstellungen. Bei Aktualisierungen zieht der Mac den Code via Read-only Deploy-Key (`MD-A`); der GUI-Server startet neu, während langlebige 24/7-Dienste den Update-Bedarf sanft an das Dashboard melden.
- **Domänen-Persistenz & Fristen (`VM-A`):** Applikationen wie der VersicherungsManager schreiben Fristen und Deadlines gegen eine app-weite `settings`-Tabelle nach routinika-Muster. Zeitrechnungen und Deadline-Projektionen operieren über alle Profile hinweg deterministisch auf derselben IANA-Zeitzone.
- **Öffentlicher Auftritt (`PD-A`):** Der nächtliche Seiten-Builder validiert den Zustand der Repositories. USMC wird mit korrigierter `public`-Deklaration fehlerfrei publiziert, ohne Warnungen in den Sicherheits-Gates auszulösen.

---

## 4. Umsetzung

Da die Vorlage für diese fünf Posten im Abhängigkeitsgraphen ([decision-path](../decision-path/SKILL.md)) keine serielle Kette vorgibt, erfolgt die Umsetzung ehrlich in vier voneinander unabhängigen, parallelen Arbeitssträngen (Ausweg a: parallele Stränge statt erfundener Kausalität). Eine sequenzielle Reihenfolge gilt nur dort, wo externe Fristen oder interne Schritte belegt sind:

- **Strang A (Termingebunden — Frist 2026-09-14):**
  1. USMC-Metadaten auf `public` nachziehen (`PD-A`); Draft-PR #2 verwerfen. Duldet wegen des nächtlichen Builder-Laufs keinen Aufschub, ist technisch jedoch von allen anderen Strängen unabhängig.
- **Strang B (Host-Konfiguration & Mac-Deploy — parallel ausführbar):**
  1. B1: Sollwerte in `.SYNC` festschreiben (`CF-A`), Reasoning-Stufe `high` für beide Hosts synchronisieren.
  2. B2 (unabhängig von B1): Read-only Deploy-Key auf Mac Studio hinterlegen und Pull-and-Report-Skript einrichten (`MD-A`).
- **Strang C (Domänen-Datenbank — parallel ausführbar):**
  1. Migration der app-weiten `settings`-Tabelle im VersicherungsManager nach routinika-Vorbild implementieren (`VM-A`), um die saubere Basis für den nachgelagerten Publisher-Bau zu schaffen.
- **Strang D (Architektur-Herauslösung — interner Mehrstufenplan):**
  1. D1: SQLite-Schema für Rollen und Budgets in `agents-heart` anlegen (`BH-A` E1).
  2. D2: Backend-Katalog als Python-Modul ausgründen (`BH-A` E3) und clutch-Seam für Zuteilung binden (`BH-A` E2).
  3. D3: Modul `agents-heart` final herauslösen und anbinden (`BH-A` E5, E6).

---

## 5. Was dieses Bild nicht abdeckt

- **Task-Claiming Race Condition:** Der Integritätsfehler bei doppeltem Task-Claim läuft
  in einem separaten Hotfix-Ticket und ist nicht Teil dieser Freigabe.
- **Cockpit-Frontend:** Das Monitoring-Cockpit (`BH-A` E4) wird bewusst noch nicht gebaut,
  solange das Backend nicht produktiv meldet.
- **Sichtbarkeitsschaltung nach außen:** Reine Bereitstellung von Code schaltet keine
  neuen Repos public; die finale Freigabe bleibt dem Nutzer vorbehalten.

---

## 6. Abnahme

Du kannst diesen Systemverbund als Ganzes abnehmen oder in Alltagssprache korrigieren:

- **Ausdrückliche Gesamtabnahme:** „Passt so, genau so umsetzen.“ (Nur dies führt zur Verbuchung aller Posten).
- **Korrektur-Beispiele:**
  - *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* (Mehrfachtreffer)
  - *„BH-A E5 lieber ocean-heart nennen statt agents-heart.“*
  - *„VM-A erst mal vertagen, der Publisher hat noch Zeit.“*

---

## 7. Rücktransfer

Wird das Gesamtbild abgenommen oder korrigiert, übersetzt der Skill die Rückmeldung:

### Fall A: Ausdrückliche Gesamtabnahme
Nimmt der Nutzer das Gesamtbild ausdrücklich als Ganzes ab (z. B. *„Passt so, genau so umsetzen“*):
- Alle fünf Posten (`BH-A: 1A/2A/3A/4B/5A/6A`, `MD-A: A1`, `CF-A: 1C/2B/3B`, `VM-A: A`, `PD-A: A`) werden als GETROFFEN an [decision-briefing](../decision-briefing/SKILL.md) Phase 4 übergeben.
- Phase 4 übernimmt die Eintragung ins Register `DECIDED-AND-DONE.md` und aktualisiert die fünf Quelltickets.

### Fall B: Teilkorrektur mit Mehrfachtreffer
Gibt der Nutzer eine inhaltliche Korrektur ein, z. B.:
> *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“*

**1. Strukturierte Rücktransfer-Tabelle:**

| Originalkorrektur (Wortlaut des Nutzers) | Betroffene Kürzel | Domino-Status (welche abhängigen Knoten kippen dadurch) | Offene Mehrdeutigkeiten |
|---|---|---|---|
| *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* | `MD-A`, `CF-A` *(Mehrfachtreffer: 1 Aussage bewegt 2 Posten)* | **`MD-A`:** Kippt von A1 auf A2. Erfordert SSH-Write-Key auf Mac Studio, Push-Rechte im GitHub-Repo `bach` und Sicherheitsprüfung des LaunchAgents.<br>**`CF-A`:** Gruppe 1 kippt von C auf A (Laptop-Claude-Desktop wird restriktiver). Gruppe 2 kippt von B auf A (`codex.model` wird starr angeglichen). Gruppe 3 bleibt B (`high`), da bereits synchron. | **`CF-A` Gruppe 1:** Nutzer verlangt Angleichung an Workstation (1=A) — Rückfrage nötig, ob die bisher bewusste Freizügigkeit auf dem Laptop wirklich entzogen werden soll.<br>**`MD-A`:** Unklar, ob Write-Key für alle Repos oder nur für `bach` gelten soll. |

**2. Status der unberührten Posten (Schutz vor ungefragtem Mitbuchen):**
- Die unveränderten Posten `BH-A`, `VM-A` und `PD-A` werden **nicht** gebucht!
- Sie verbleiben im Status **OFFEN** (`PENDING`) in der Vorlage bzw. im Register `TO-DECIDE-USER.txt`.
- Eine Teilkorrektur ist **keine** Gesamtabnahme. Erst wenn das nach Korrektur aktualisierte Gesamtbild vom Nutzer als Ganzes abgenommen wird oder die verbleibenden Punkte einzeln bestätigt werden, dürfen sie verbucht werden.

**3. Buchungsweg:**
- `decision-draw` besitzt keinen eigenen Schreibmechanismus.
- Übergeben wird an **[decision-briefing](../decision-briefing/SKILL.md) Phase 4** nur, was die Tabelle als eindeutig ausweist: `CF-A` Gruppe 2 = A und Gruppe 3 = B.
- **Nicht** übergeben werden `MD-A` und `CF-A` Gruppe 1 — für beide steht in der Spalte *Offene Mehrdeutigkeiten* eine Rückfrage. Eine Mehrdeutigkeit, die man vor der Buchung klären wollte, darf man nicht in derselben Runde als geklärt verbuchen.
- Phase 4 trägt die eindeutigen Teile mit Begründung in Ticket `T-20260913-947070291.txt` ein und aktualisiert `DECIDED-AND-DONE.md`. Ticket `T-20260913-799464688.txt` (`MD-A`) bleibt offen, bis die Rückfrage beantwortet ist.

---

## 8. Anhang: Technische Referenztabelle (nur für Buchung & Audit)

| Klartext-Titel | Internes Kürzel | Ticket / Quelle | Unterstellte Empfehlung | Konfidenz | Link / Details |
|---|---|---|---|---|---|
| Modell-Backend als eigenes Herzstück | `BH-A` | `T-20260913-896336887` | 1A / 2A / 3A / 4B / 5A / 6A | 🟢 | `docs/MODELL-BACKEND-KONZEPT_2026-09-13.md` |
| Sichere Deploy-Schlüssel auf dem Mac | `MD-A` | `T-20260913-799464688` | A1 + Skript (nur Melden für 24/7) | 🟢 | Ticket `T-20260913-799464688.txt` |
| Einheitliche Konfigurations-Sollwerte | `CF-A` | `T-20260913-947070291` | 1C (begründet) / 2B (hostabh.) / 3B (high) | 🟢 / 🟡 | Ticket `T-20260913-947070291.<HOST>.txt` |
| Feste Zeitzone im VersicherungsManager | `VM-A` | `T-20260906-496406575` | A (app-weite settings wie routinika) | 🟢 | Ticket `T-20260906-496406575.<HOST>.txt` |
| Öffentliche Bereitstellung der USMC-Dokumentation | `PD-A` | `T-20260913-609930207` | A (auf public nachziehen, Status quo) | 🟢 | Ticket `T-20260913-609930207.txt` |
```

---

## Regeln für die Praxis

1. **Kein Konjunktiv im Konzept:** Beschreibe das Gesamtsystem so, als sei es bereits realisiert. Der Nutzer will Klarheit über das Resultat, keine theoretischen Eventualitäten.
2. **Kausalität vor Chronologie:** Die Reihenfolge im Abschnitt *Umsetzung* folgt den Ebenen des Abhängigkeitsgraphen aus [decision-path](../decision-path/SKILL.md). Unabhängige Stränge werden ehrlich als parallel dargestellt und nicht zu einer künstlichen Kausalkette verbogen.
3. **Expliziter Domino-Check im Rücktransfer:** Eine Korrektur des Nutzers darf niemals isoliert eingetragen werden, ohne zu prüfen, ob abhängige Knoten im Graphen entwertet oder beeinflusst werden.
4. **Kein automatisches Mitbuchen bei Teilkorrekturen:** Nur bei ausdrücklicher Gesamtabnahme werden unveränderte Posten gebucht. Bei jeder Teilkorrektur bleiben alle nicht betroffenen Posten strikt offen, bis das Gesamtbild erneut freigegeben oder die Posten einzeln bestätigt werden.
5. **Ausschließlicher Schreibweg über Phase 4:** `decision-draw` besitzt keinen eigenen Schreibweg ins Register. Buchungen erfolgen ausnahmslos über [decision-briefing](../decision-briefing/SKILL.md) Phase 4.
6. **Respektiere die Register-Verträge:** Buchungen erfolgen immer nach den Regeln des Entscheidungsregisters (keine Umnummerierung von IDs, eindeutige Buchungscodes, kanonisches Ziel `DECIDED-AND-DONE.md`).
7. **Nutzertexte ohne technische Nummern und Kürzel:** Im sichtbaren Fließtext für den Menschen stehen keine IDs, Kürzel, Pfade oder Ticketnummern. Jeder Posten wird in verständlicher Ich-Form formuliert; alle Kennungen wandern in die Anhangstabelle.

---

## Session-Provenienz

Wird ein Decision-Draw als dauerhaftes Konzeptdokument gespeichert, endet es mit:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- Quellenpriorität: Explizite Laufzeit-/CLI-Angabe, danach autoritative Provider-Umgebung oder Hook, sonst `unbekannt`.
- Subagenten erben die Session-ID der Elternsession.
- Reine Chat-Vorlagen erhalten keinen Stempel.

---

## Changelog

### 1.1.0 (2026-09-18)
- Stilregel für nutzergerechte Entscheidungstexte verankert (T-20260913-883789445, Nutzeranweisung 2026-09-13):
  - Keine technischen Kürzel, Ticket-/D-Nummern, Pfade oder Messwerte im sichtbaren Nutzertext.
  - 2–4 Sätze Alltagssprache in Ich-Form (Lage, „Ich mache …“, Rückfall) je Posten.
  - Sprechende Klartext-Titel zur Identifikation und Abnahme.
  - Technische Zuordnung (Kürzel, Ticket-ID, Register-Zustand) strikt in abschließende Anhangstabelle (Abschnitt 8) verlagert.

### 1.0.1 (2026-09-13)
- Nacharbeit nach Review:
  - Rücktransfer-Vertrag geschärft: Keine automatische Mitbuchung bei Teilkorrekturen; unberührte Posten bleiben strikt offen bis zur Gesamtabnahme.
  - Rücktransfer-Pflicht-Tabelle mit 4 Spalten (Originalkorrektur, Betroffene Kürzel, Domino-Status, Offene Mehrdeutigkeiten) eingeführt.
  - Mehrfachtreffer im Beispiel demonstriert (eine Nutzerkorrektur bewegt `MD-A` und `CF-A` gleichzeitig).
  - Ausschließlicher Schreibweg über `decision-briefing` Phase 4 im Vertrag und Beispiel verankert.
  - Kausalketten-Fehlannahme im Beispiel behoben: Unabhängige Posten ehrlich als vier parallele Arbeitsstränge dargestellt (Ausweg a).
  - Abgrenzung zu `decision-shot` über Ausgabeformat (strukturierte Einzelblöcke mit Pro/Contra vs. zusammenhängendes Zielbild mit Gesamtabnahme) präzisiert.

### 1.0.0 (2026-09-13)
- Erstfassung auf Basis des Nutzerauftrags T-20260913-107991667.
- Siebenteiliger verbindlicher Aufbau (Bündel, Konzept, Zusammenspiel, Umsetzung, Grenzen, Abnahme, Rücktransfer).
- Bündelungslogik auf Basis von `decision-path` und Rückschreibe-Brücke zu `decision-briefing` Phase 4.
