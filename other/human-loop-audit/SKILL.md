---
name: human-loop-audit
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: >
  Interaktives Reißverschluss-Audit-Verfahren für eine Serie von Apps/Prüfobjekten: der
  User testet live und gibt kurzes Feedback im Chat, der Agent startet dabei bereits das
  nächste Objekt UND wertet parallel das Feedback des vorigen aus (strukturiert erfassen,
  Reparaturaufträge sofort an Worker delegieren) — statt sequenziell zu warten. Nutze
  diesen Skill bei "human-loop-audit", "lass uns die Apps im Reißverschluss durchtesten",
  "ich teste, du wertest aus und reparierst", oder wenn eine Reihe von GUIs/Produkten
  gemeinsam mit dem Nutzer durchgetestet werden soll und Befunde sofort in Reparaturen
  münden sollen. Abschluss ist eine strukturierte Befundliste je Objekt
  (Funktioniert/Defekt/Wunsch) plus die Liste der bereits gestarteten Reparaturen.

# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: dev
tags: [audit, usertest, human-in-the-loop, gui-test, reissverschluss, delegation, feedback]
language: de
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: []
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="human-loop-audit banner">

# Human-Loop-Audit

> **Nicht zu verwechseln mit `reissverschluss-merge`:** Der Name teilt sich das
> "Reißverschluss"-Bild, aber `reissverschluss-merge` ist ein **Git-Merge-Verfahren**
> (abschnittsweise zwei Code-Branches zusammenführen). `human-loop-audit` hier hat mit Git
> nichts zu tun — es ist ein **Test-/Audit-Ablauf mit dem Nutzer**. Beide Skills nutzen den
> Reißverschluss nur als dieselbe Grundidee (zwei Stränge Zahn um Zahn ineinanderführen,
> nicht Strang für Strang nacheinander).

## Zweck & Rollenverteilung

Die Zeit des Users ist der **serielle Engpass**: Nur er kann eine App wirklich live bedienen
und in Sekunden sagen, ob sie sich richtig anfühlt. Alles andere — Objekte öffnen, Feedback
strukturiert erfassen, Reparaturen anstoßen — übernimmt der Agent, und zwar **während** der
User schon am nächsten Objekt ist, nicht danach. Der Agent ist Cockpit-Betreiber und
Auswerter gleichzeitig.

**Der Kern ist die Überlappung, nicht die Reihenfolge selbst:** Ein rein sequenzielles
"App öffnen → warten → auswerten → nächste App öffnen" verschwendet die Wartezeit, in der
der User testet. Human-Loop-Audit nutzt genau dieses Fenster.

## Ablauf

1. **"start"** vom User → Agent öffnet das **erste** Prüfobjekt. Es reicht, den Prozess zu
   starten (z. B. `Start-Process <exe>` bzw. das passende Startkommando des Objekts) —
   **keine Desktop-Übernahme nötig**, der User bedient selbst. Kurz bestätigen, dass es offen
   ist.
2. **User testet und schreibt Feedback in den Chat** — kurze Stichpunkte reichen, nichts
   umformulieren, was die Bedeutung ändert.
3. **Sobald das Feedback eingeht, laufen zwei Dinge parallel, nicht nacheinander:**
   - Der Agent **öffnet sofort das nächste Prüfobjekt**, damit der User ohne Wartezeit
     weitertesten kann.
   - **Gleichzeitig** wertet der Agent das eingegangene Feedback aus: Befund je Objekt
     strukturiert festhalten (**Funktioniert** / **Defekt** / **Wunsch**, mit kurzer
     Beschreibung), und bei einem Defekt oder klaren Wunsch **sofort einen
     Reparaturauftrag an einen Worker delegieren** (nicht sammeln und "später" beauftragen —
     die Reparatur soll laufen, während der User weitertestet).
4. **Wiederholen** bis alle Objekte durch sind (zurück zu Schritt 2/3 für jedes weitere
   Objekt).
5. **Abschluss:** Befundliste (je Objekt Funktioniert/Defekt/Wunsch) + Liste der gestarteten
   Reparaturen (Worker/Auftrag/Status) dem User vorlegen.

## Befundstruktur (je Prüfobjekt)

| Objekt | Status | Befund | Reparatur delegiert an |
|---|---|---|---|
| `<App/Objekt-Name>` | Funktioniert / Defekt / Wunsch | kurzer Stichpunkt, unverändert vom User-Wortlaut | Worker-Name/Session, falls delegiert |

Ein Objekt kann mehrere Zeilen bekommen (mehrere Befunde). Nichts wird stillschweigend
zusammengefasst — der Abschluss liest sich aus dieser Tabelle, nicht aus dem Gedächtnis.

## Abgrenzung zu verwandten Skills

- **`reissverschluss-merge`** (s. Hinweis oben) — reines Git-Merge-Verfahren, keine
  inhaltliche Überschneidung trotz gleichem Namensbild.
- Verwandte, aber enger gefasste Wellen-/Store-Einreichungs-Testzyklen mit fest verdrahteten
  Zusatzphasen (Assets-Review, Submission-Sheets, ID-Rückschreibung) und **sequenzieller**
  Umsetzung ("Umsetzung der Punkte läuft getrennt") existieren als projektlokale Verfahren.
  `human-loop-audit` ist bewusst der **generische** Ablauf für **beliebige** App-/GUI-Serien
  und delegiert Reparaturen **sofort und parallel**, nicht als separaten späteren Schritt.
- **`bugsweep` / `bugfix-protocol`** — die eigentliche Reparaturarbeit, an die
  `human-loop-audit` delegiert; dieser Skill selbst repariert nicht.

## Fallstricke

- **Nicht auf die Auswertung warten, bevor das nächste Objekt geöffnet wird** — ein rein
  sequenzielles "warten, dann auswerten, dann nächstes öffnen" verschenkt genau die
  Überlappung, die diesen Skill ausmacht.
- **Feedback sofort strukturiert festhalten**, nicht im Chat-Verlauf sammeln — bei
  Sessionabbruch wäre es sonst weg.
- **Objekte nicht blind starten**, wenn ein Objekt bekanntermaßen instabil ist — kurz
  Startfähigkeit prüfen, bevor der User live davorsitzt.
- **Delegation sofort, nicht gesammelt am Ende** — sonst startet die Reparatur erst, wenn der
  User längst fertig getestet hat, und der Zeitvorteil des Verfahrens geht verloren.

## Trigger-Beispiele

- "human-loop-audit"
- "Lass uns die Apps im Reißverschluss durchtesten."
- "Ich teste, du wertest aus und reparierst."
- "start" (nach vorheriger Ankündigung eines Human-Loop-Audits, als Startsignal für Schritt 1)

## Changelog

### 1.0.0 (2026-08-18)
- Initiale Version. Verfahren aus einer Nutzer-Definition vom 2026-08-18 übernommen:
  Reißverschluss-Audit mit paralleler Auswertung + sofortiger Reparatur-Delegation,
  abgegrenzt von `reissverschluss-merge` (Git-Merge, gleiches Namensbild, kein Bezug) und
  von engeren, projektlokalen Wellen-Testzyklen (sequenzielle Umsetzung statt parallel).
