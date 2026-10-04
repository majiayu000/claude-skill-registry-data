---
name: tidy-up
version: 1.1.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-19
description: >
  Einmaliger Tasksolver+Writer+Maintainer-Durchlauf fuer den Projektordner, in dem die Session
  gerade sowieso gearbeitet hat (inkl. Unterordner) — kein systemweiter Sweep. Loest offene
  triviale/autonome Register-Punkte, aktualisiert Dokumentation auf den gemessenen Ist-Stand
  (im Projekt UND in der Root der Pipeline, in der das Projekt liegt) und raeumt Strays/Temp-
  Dateien nach dem Papierkorb-Prinzip weg. Nutze diesen Skill bei /tidy-up, "raeum das Projekt
  auf", "mach hier sauber bevor wir weitermachen", am Ende einer Arbeitssitzung an einem Projekt,
  oder als faellige autonome Aufgabe innerhalb von /work-autonomous + /goal.

# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: dev
tags: [hygiene, maintenance, cleanup, documentation, tasksolver, writer, maintainer, autonomy, goal, work-autonomous, ticket-master]
language: de
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: [work-autonomous, bilingual-doc-sync]
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="tidy-up banner">

# Tidy Up — Tasksolver+Writer+Maintainer-Durchlauf fuer den aktiven Projektordner

## Zweck

Am Ende einer Arbeitssitzung an einem Projekt bleibt typischerweise Kleinkram liegen: ein
erledigter TODO-Punkt, der nie abgehakt wurde; eine README, die den alten statt den gemessenen
Stand zeigt; eine Handvoll Testdateien, die niemand mehr braucht. `tidy-up` ist ein **einmaliger,
selbstbegrenzter Durchlauf**, der genau das fuer **einen** Projektordner nachzieht — den, in dem
die Session ohnehin gerade gearbeitet hat. Kein Dauerloop, kein systemweiter Sweep.

Der Durchlauf besteht aus drei Rollen, die das Modell selbst nacheinander einnimmt:

1. **TASKSOLVER** — offene, triviale/autonome Punkte des Projekt-Registers loesen oder korrekt
   einsortieren.
2. **WRITER** — Dokumentation auf den gemessenen Ist-Stand aktualisieren, im Projekt UND in der
   Root der Pipeline, in der das Projekt liegt.
3. **MAINTAINER** — Hygiene: Strays/Temp-Dateien einsammeln (Papierkorb-Prinzip), Register-/
   Katalogpflege, offene Reste ablegen statt nur im Chat zu erwaehnen.

**Gemessen vor dem Bau dieses Skills:** Es existieren in dieser Bibliothek (Stand 2026-08-19)
**keine** eigenstaendigen Skills oder Rollen namens `tasksolver`/`writer`/`maintainer` — weder als
Skill-Name noch als dokumentierte Rolle in einem anderen Skill (Volltextsuche ueber
`skills/**/SKILL.md`, keine Treffer ausser einem unverwandten Namen `privat-mail-writer`). Die
drei Rollen sind deshalb direkt unten als Abschnitte definiert, nicht extern orchestriert. Sollten
spaeter eigenstaendige `tasksolver`/`writer`/`maintainer`-Skills entstehen, uebernimmt `tidy-up`
sie per Verweis statt die Logik weiter zu duplizieren (Pruefpflicht bei jeder Weiterentwicklung
dieses Skills).

## Scope — was zaehlt als "der aktive Projektordner"?

- Der Projektordner, an dem die Session in diesem Kontext gearbeitet hat, **inklusive aller
  Unterordner**. Kein Sprung in Nachbarprojekte, kein Sweep ueber eine ganze Pipeline oder gar
  `.TOPICS/` insgesamt.
- **Eine** gezielte Ausnahme: Dokumentations-/Registeraktualisierung darf zusaetzlich die
  **Root-Ebene der Pipeline** beruehren, in der das Projekt liegt (z. B. eine Statuszeile fuer
  dieses eine Projekt in einer pipeline-weiten Uebersichtstabelle) — aber nur die Zeile/den
  Abschnitt, der dieses Projekt betrifft, nicht die ganze Pipeline-Root neu ordnen.
- Ist unklar, was "der aktive Projektordner" ist (z. B. Session hat in mehreren Ordnern
  gearbeitet), das naechstliegende gemeinsame Projekt-Root nehmen (dort, wo README/TODO/CLAUDE.md
  des Projekts liegen) — im Zweifel lieber enger fassen als zu breit.

## Rolle 1 — TASKSOLVER

Ziel: das Projekt-Register (`TODO.md`/`AUFGABEN.txt`/vergleichbare lokale Konvention) auf einen
korrekten, aktuellen Stand bringen.

1. Projekt-Register lokalisieren (lokale Konvention hat Vorrang vor einer neuen Datei — siehe
   Regel "Uebriggebliebene Aufgaben gehoeren abgelegt, nicht erwaehnt" im globalen Regelwerk).
2. Jeden offenen Punkt einzeln bewerten:
   - **Bereits erledigt** (z. B. durch die gerade beendete Sitzung) → als erledigt markieren/nach
     `DONE.md` bzw. der lokalen Erledigt-Konvention verschieben.
   - **Trivial und autonom loesbar** (keine Nutzerentscheidung/-freigabe/-daten/-hardware/-sitzung
     noetig, siehe Abgrenzungstabelle in `work-autonomous`) → jetzt loesen, dann als erledigt
     einsortieren.
   - **Nicht trivial oder nicht autonom** → NICHT anfassen, aber korrekt einsortiert lassen (nicht
     kommentarlos liegen lassen, wenn eine bessere Ablage existiert — z. B. ein Punkt, der laengst
     eine `USER/*`-Ticket-Kategorie verdient haette).
3. Keine neuen Aufgaben erfinden — `tidy-up` loest vorhandene Reste, es erzeugt keine neue Agenda.

## Rolle 2 — WRITER

Ziel: Dokumentation zeigt den **gemessenen**, nicht den erinnerten oder erhofften Stand.

1. Im Projekt: README/CHANGELOG/Statuszeilen gegen die tatsaechliche Code-/Ordnerlage pruefen
   (z. B. genannte Dateien existieren noch, genannte Versionsnummer stimmt, "in Arbeit"-Markierung
   ist nicht laengst erledigt).
2. In der Pipeline-Root: falls dort ein Register/eine Statustabelle existiert, die dieses eine
   Projekt auffuehrt (z. B. `.TOPICS/<Pipeline>/ROADMAP.md`, `STATUS.md`, eine Projekttabelle in
   der Pipeline-README) — dessen Zeile/Abschnitt fuer GENAU dieses Projekt aktualisieren.
3. **Kuratierte Inhalte niemals ersetzen, nur messen+aktualisieren.** Tabellen, Changelogs oder
   sorgfaeltig formulierte Abschnitte bleiben in Form und Ton erhalten — nur Fakten (Zahlen,
   Status, Dateinamen, Versionen) werden korrigiert. Bei Unsicherheit, ob ein Abschnitt kuratiert
   ist: lieber einen Vermerk ergaenzen als eine bestehende Formulierung ueberschreiben.
4. Kein Neuschreiben von Grund auf, wenn ein Update reicht.
5. **Uebersetzungs-Nachzug** (Ergaenzung 2026-08-19, User-Auftrag live): Fehlt fuer das Projekt
   eine Sprachfassung, die laut **Policy P-006** (`.SYNC/_policies/library/P-006_sprachstufen.md`)
   fuer seine Stufe Pflicht ist, oder ist eine vorhandene Fassung erkennbar veraltet — das zieht
   der WRITER-Schritt nach. P-006 in Kurzform: **Core-Set (DE+EN) ist Pflicht** fuer jedes
   veroeffentlichte Repo/katalogisierte Objekt (Repo: `README.md` EN + `README_de.md`; Skill:
   `SKILL.md` DE + `SKILL.en.md`); Full-/World-Set (ES/ZH/JA/RU bzw. +FR/HI/AR/BN/PT) sind das
   Zielbild, werden aber **nach und nach** nachgezogen, nicht in einer Kampagne durch `tidy-up`.
   **Werkzeug: der bestehende Skill `bilingual-doc-sync` wird orchestriert (aufgerufen), seine
   Logik wird NICHT dupliziert** — er deckt genau "fehlende Fassung nachziehen" +
   Abschnitts-Paritaetspruefung + Divergenzbehebung bereits ab. `tidy-up` liefert ihm nur den
   Anstoss (welches Objekt, welche laut P-006 fehlende Pflichtsprache) fuer den aktiven
   Projektordner; Uebersetzungsqualitaet, Struktur-Paritaet und Leitsprachen-Regel bleiben
   `bilingual-doc-sync`s Verantwortung. **Grenzen wie bei P-006:** nur bis zum gemessenen Ist-Stand
   uebersetzen, keine Inhalte erfinden, echte Diakritika/Umlaute, Repo-Cooldown (<24h seit letztem
   Commit) und aktive Locks respektieren — dann diesen Punkt unuebersetzt lassen und als offenen
   Punkt ablegen (Rolle 3) statt zu erzwingen.

## Rolle 3 — MAINTAINER

Ziel: Hygiene, ohne dass etwas verloren geht.

1. **Strays/Temp-Dateien einsammeln** (Skriptreste, `*.tmp`, doppelte Kopien, vergessene
   Debug-Ausgaben) — Papierkorb-Prinzip: in einen lokalen `_archive/`-Ordner verschieben (anlegen +
   in `.gitignore` eintragen falls noch nicht vorhanden), **niemals direkt loeschen**. Bei Funden,
   deren Herkunft/Zweck unklar ist: Zweck aktiv ermitteln (Datei lesen), nicht ungelesen wegraeumen
   — siehe Konvention "Fremdaenderungen nachzertifizieren".
2. **Register-/Katalogpflege:** Falls das Projekt Teil eines groesseren Katalogs/einer Registry ist
   (Skill-Registry, Modul-Manifest, Pipeline-Uebersicht), pruefen ob der Eintrag fuer dieses
   Projekt noch stimmt — nicht die ganze Registry neu bauen, nur diesen einen Eintrag.
3. **Offene Reste ablegen statt im Chat erwaehnen:** Was am Ende dieses Durchlaufs uebrig bleibt
   (nicht autonom loesbare Punkte, entdeckte aber nicht behobene Maengel, bewusst Verschobenes)
   wird nach der Regel "Uebriggebliebene Aufgaben gehoeren abgelegt, nicht erwaehnt" abgelegt —
   primaer lokal am Fundort (TODO.md/AUFGABEN.txt-Konvention des Projekts), sonst zentral
   (`ticket-master`/`TASKPLAN`), jeweils mit Kontext (was, warum offen, naechster Schritt).
4. **Locks respektieren:** Vor jeder Aenderung pruefen, ob eine aktive `LOCK.txt`/`LOCK.<scope>.txt`/
   `LOCK.user.*` im Projektordner liegt. Ein `LOCK.user.*` stoppt `tidy-up` fuer den betroffenen
   Bereich vollstaendig — kein Umgehen, kein Teil-Tidy-Up am gesperrten Bereich.
5. **Commit+Push nur nach der Repo-Konvention des jeweiligen Projekts** — bei getrennten
   Planungs- und Entwicklungsflächen Änderungen im autorisierten lokalen Projektklon vornehmen,
   nicht in einer Planungs- oder Projektionskopie.
   Eigene Aenderungen werden nach der globalen Konvention "sofort selbst committen + pushen"
   behandelt, wenn das Projekt das vorsieht.

## Selbstbegrenzung

`tidy-up` ist **ein Durchlauf, kein Loop**. Nach Rolle 3 endet der Skill mit einer kurzen
Zusammenfassung (was geloest, was aktualisiert, was aufgeraeumt, was offen abgelegt wurde) und
kehrt zur aufrufenden Sitzung zurueck. Ein erneuter `/tidy-up`-Aufruf im selben Projekt kurz
danach ist erlaubt, aber nicht automatisch sinnvoll — siehe Faelligkeits-Kriterium unten.

## Verhaeltnis zu work-autonomous

`tidy-up`-Laeufe **zaehlen als autonom ausfuehrbare Aufgabe im Sinne von `work-autonomous` Ebene 1**
(normale, sichtbare Arbeit — kein Grund, in die teure Ebene-2-Erschoepfungspruefung zu wechseln,
solange ein faelliger `tidy-up`-Lauf vorliegt). Praktisch heisst das: Wird `/work-autonomous`
zusammen mit `/tidy-up` innerhalb eines `/goal` genutzt, gilt das Goal erst dann als abgeschlossen,
wenn auch faellige `tidy-up`-Punkte erledigt sind — sofern sie autonom durchfuehrbar sind (siehe
Abgrenzungstabelle in `work-autonomous`; ein `tidy-up`-Punkt, der eine Nutzerentscheidung braucht,
zaehlt genauso wenig als autonom wie jede andere `USER/*`-gebundene Aufgabe).

**Faelligkeits-Kriterium** (wann ist ein `tidy-up`-Lauf "faellig"?):

1. Die Session hat in diesem Sitzungskontext bereits an einem konkreten Projektordner gearbeitet
   (nicht: reine Recherche/Lesearbeit ohne Aenderungen — dann gibt es nichts aufzuraeumen).
2. Seit dem letzten protokollierten `tidy-up`-Lauf fuer GENAU dieses Projekt ist der Cooldown
   abgelaufen (Default: 1× pro Sitzungsabschluss an diesem Projekt — kein Mehrfachlauf **innerhalb**
   derselben Sitzung ohne neue Aenderungen seit dem letzten Lauf).
3. Kein aktiver `LOCK.user.*` blockiert den Projektordner (siehe Rolle 3, Punkt 4).

Protokollierung des letzten Laufs (analog zum Guard-Muster in `work-autonomous`, aber bewusst
schlanker — `tidy-up` braucht keine vierstufige Kette, nur einen Zeitstempel je Projekt):

```bash
usmc --agent <agent> note "tidy-up: project=<projekt-pfad-oder-slug> at=<ISO-Zeit> result=<done|nothing-to-do>" \
  --type context --priority 2 --tags "tidy-up-log,<projekt-slug>"
```

Vor einem neuen Lauf denselben Tag lesen (`usmc --agent <agent> working --limit 20` gefiltert nach
`tidy-up-log,<projekt-slug>`), um Kriterium 2 zu pruefen.

Ein `/goal`-Konstrukt (sofern eines existiert oder gebaut wird — `work-autonomous` selbst ruft
kein `/goal` auf, siehe dortiger Abschnitt "Bewusst ohne eingebautes `/goal`") liest dieses
Faelligkeits-Kriterium genauso wie es `work-autonomous`s eigenes Abbruchsignal liest: Ist ein
`tidy-up`-Lauf faellig UND autonom durchfuehrbar, ist das Goal noch nicht fertig — unabhaengig
davon, ob `work-autonomous`s eigene Vier-Schritt-Kette bereits "exhausted" meldet.

Der passende, minimal-invasive Gegen-Eintrag im `work-autonomous`-Skill selbst (Ebene 1, neue
Quelle "faellige tidy-up-Laeufe des aktiven Projekts") ist Teil dieses Ausbaus — siehe dortiger
Changelog-Eintrag.

## Verwandte Skills

- **`work-autonomous`** — siehe oben; `tidy-up` ist eine der Quellen, die `work-autonomous`s
  Ebene 1 abarbeitet, kein Ersatz fuer dessen Erschoepfungspruefung.
- **`bilingual-doc-sync`** — wird von Rolle 2 (WRITER) fuer den Uebersetzungs-Nachzug
  orchestriert (siehe dort), nicht dupliziert. `tidy-up` entscheidet nur WAS laut P-006 fehlt,
  `bilingual-doc-sync` entscheidet WIE uebersetzt/synchronisiert wird.
- **`bugsweep`** — systematische Bug-Suche mit Verdopplungs-Eskalation. Anderer Zweck (Fehler
  finden, nicht Register/Doku/Hygiene pflegen) — bei Ueberschneidung (Bugsweep-Fund landet im
  Register) uebernimmt `tidy-up` nur die Registerpflege, nicht die Bugsuche selbst.
- **`dev-cycle`** — 8-Phasen-Rahmen fuer neue Feature-Entwicklung. `tidy-up` ist kein
  Entwicklungsrahmen, sondern ein Abschluss-/Hygiene-Durchlauf nach bereits geleisteter Arbeit.
- **`folder-flattening`** — restrukturiert verschachtelte Ordnerhierarchien. `tidy-up` raeumt
  Dateien innerhalb der bestehenden Struktur auf, aendert die Struktur selbst nicht.

## Beispiele

```
User: "/tidy-up"
(Session hat gerade am autorisierten lokalen Checkout von `beispiel-projekt` gearbeitet)

→ TASKSOLVER: TODO.md gelesen — 2 Punkte bereits durch die Sitzung erledigt (nach DONE.md
  verschoben), 1 trivialer Punkt ("README-Tippfehler in Zeile 12") autonom geloest, 1 Punkt
  braucht Nutzerentscheidung (unveraendert stehen gelassen).
→ WRITER: README-Versionsangabe war 1.2.0, tatsaechlich 1.3.0 (package.json) — korrigiert.
  Pipeline-Root-Statustabelle: Zeile fuer "beispiel-projekt" von "in Arbeit" auf "aktiv" gesetzt.
→ MAINTAINER: 3 Debug-Skripte im Projektroot gefunden, nach _archive/ verschoben (Zweck geprueft:
  einmalige Testskripte, nicht mehr referenziert). Skill-Registry-Eintrag geprueft: stimmt.
  1 offener Punkt (Nutzerentscheidung) in AUFGABEN.txt belassen, dort bereits korrekt einsortiert.
→ USMC-Log geschrieben: tidy-up: project=beispiel-projekt at=2026-08-19T14:30 result=done
→ Zusammenfassung an Nutzer: 3 geloest, 2 Doku-Stellen aktualisiert, 3 Dateien archiviert, 1 Punkt
  offen (Nutzerentscheidung noetig).
```

```
Kombiniert mit /goal + /work-autonomous:

/goal "Projekt X fertigstellen" mit /work-autonomous + /tidy-up als Bedingungen
→ work-autonomous Ebene 1 findet: ACTIONABLE-Ticket erledigt, dann kein weiteres Ticket mehr,
  ABER tidy-up-Faelligkeitskriterium erfuellt (Session hat an Projekt X gearbeitet, kein
  protokollierter Lauf seit Sitzungsbeginn, kein LOCK.user aktiv) → tidy-up-Durchlauf ausgefuehrt.
→ Erst NACHDEM tidy-up "done" meldet UND work-autonomous Ebene 2 "exhausted" meldet, gilt das
  Goal als abgeschlossen.
```

## Changelog

### 1.1.0 (2026-08-19)
- Ergaenzung aus einem live nachgereichten Zusatz zu T-20260819-461890468 (User, woertlich: "bis
  zu einer uebersetzung nachzuziehen die noch nicht existiert soll auch zum skill gehoeren"):
  Rolle 2 (WRITER) bekommt einen fuenften Punkt, Uebersetzungs-Nachzug nach **Policy P-006**
  (Sprachstufen: Core-Set DE+EN Pflicht, Full/World nach und nach). Werkzeug ist der bereits
  bestehende Skill `bilingual-doc-sync` — wird orchestriert, nicht dupliziert. Frontmatter-
  Dependency + "Verwandte Skills"-Eintrag ergaenzt.

### 1.0.0 (2026-08-19)
- Erstversion aus Ticket T-20260819-461890468. Drei Rollen (Tasksolver/Writer/Maintainer) als
  Abschnitte im Skill definiert, nachdem eine Volltextsuche ueber die Bibliothek bestaetigte, dass
  keine eigenstaendigen `tasksolver`/`writer`/`maintainer`-Skills existieren (sonst waere
  orchestriert statt dupliziert worden). Scope auf den aktiven Projektordner + Pipeline-Root-
  Statuszeile begrenzt. Goal-Integration: `tidy-up`-Laeufe zaehlen als `work-autonomous`-Ebene-1-
  Quelle, mit eigenem, schlankem USMC-Faelligkeits-Log (kein Vier-Schritt-Guard wie bei
  `work-autonomous` selbst — dafuer ist `tidy-up` zu einfach strukturiert). Passender, minimal-
  invasiver Gegen-Eintrag in `work-autonomous` 1.3.0 ergaenzt (siehe dortiger Changelog).
