---
name: paveman
version: 1.0.1
type: skill
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-20
description: >
  Erkennt Aufträge, eine Regel- oder Gedächtnisdatei zu kürzen ("kürze meine CLAUDE.md",
  "MEMORY.md ist zu lang", "komprimiere die Doku, ohne Technik anzutasten", "diese Regeldatei
  wird über die Zeichengrenze abgeschnitten") und nutzt dafür das Modul paveman — ein
  deterministisches, modellfreies CLI-Werkzeug zum Kürzen von Prosa in Markdown-/Textdateien mit
  Trockenlauf als Standard, Rollback und strengem Schutz-Validator für Pfade, Überschriften und
  Code. Nutze diesen Skill bei Sätzen wie "kürze <Datei>", "diese Datei ist zu lang/wird
  abgeschnitten", "shrink this rule file", "komprimiere ohne Inhalt zu verändern" oder wenn eine
  Regel-/Gedächtnisdatei erkennbar an eine Zeichen- oder Zeilengrenze stößt.

# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [kürzen, kompression, regeldatei, gedächtnis, deterministisch, dry-run, rollback, dokumentation]
language: de
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [paveman]
  services: []
  protocols: []
  python: []
  modules: [paveman]

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

<img src="banner.png" width="100%" alt="paveman banner">

# Paveman — Regel- und Gedächtnisdateien deterministisch kürzen

> Dünner, nutzerneutraler Skill-Wrapper um das separat bereitgestellte Modul `paveman`.
> Der Skill erkennt, wann das Werkzeug passt, und beschreibt dessen sicheren Ablauf. Er setzt
> weder einen bestimmten Rechner noch einen festen Installationspfad oder ein persönliches Profil
> voraus.

## Wann dieser Skill greift

Trigger sind Nutzersätze, die eine **bestehende Regel-, Konventions- oder Gedächtnisdatei**
kürzen wollen, ohne ihren fachlichen Inhalt zu verändern:

- „Kürze `<Datei>`“ / „diese Datei ist zu lang“ / „wird bei X Zeichen oder Zeilen abgeschnitten“
- „Komprimiere die Doku, ohne Technik oder Code anzutasten“
- „MEMORY.md oder CLAUDE.md ist zu voll geworden“
- „Mach diese Regeldatei knapper, aber lass die Bedeutung unverändert“
- Jede Variante, die das **Kürzen einer bestehenden Datei** meint, nicht **neues Schreiben** und
  nicht **Übersetzen** (siehe Abgrenzung unten)

**Nicht** dieser Skill:

- **`knappform`** — ändert, wie das Modell selbst in der laufenden Konversation spricht
  (LLM-Kommunikationsstil, modellbasiert, kein Dateizugriff). `paveman` ändert stattdessen den
  Inhalt einer bestehenden Datei deterministisch und ohne Modellaufruf. Beide können
  nebeneinander bestehen; sie sind technisch und funktional getrennt.
- **`bilingual-doc-sync`** — zieht fehlende Sprachfassungen nach. `paveman` kürzt eine Fassung
  und übersetzt nichts.
- **`llm-text-hygiene`** — entfernt KI-Spuren oder Chat-Reste aus Texten. Das ist ein anderer
  Zweck als Kürzen.
- Neuen Inhalt schreiben oder erfinden — `paveman` kürzt nur, was schon da ist.

## Was das Modul kann

`paveman` ist ein regelbasierter, deterministischer Prosa-Kürzer für Markdown- und Textdateien:
kein Modellaufruf, keine Tokens und kein Netzwerkversand. Die Bereitstellung kann je System
unterschiedlich sein; maßgeblich ist der dort autorisierte Modul- oder Paketstand.

| Flag | Wirkung |
|---|---|
| *(kein Flag)* | **Trockenlauf (Standard).** Zeigt Diff und Zeichenersparnis, schreibt nichts. |
| `--apply` | Schreibt wirklich; vorher wird automatisch eine Sicherung angelegt. |
| `--rollback` | Stellt die letzte Sicherung wieder her. |
| `--locker` | Meldet Pfad- oder Überschriftenabweichungen nur als Warnung statt als Fehler. |
| `--kontext N` | Legt die Anzahl der Diff-Kontextzeilen fest. |

Der **Schutz-Validator läuft bei jedem Aufruf**. Codeblöcke, Pfade und Überschriften dürfen nicht
verändert werden. Im Standardmodus verhindert eine Abweichung das Schreiben, statt sie nur zu
melden.

## Ablauf — immer in dieser Reihenfolge

1. **Zuerst Trockenlauf.** `paveman <Datei>` ohne `--apply` ausführen. Zeichenersparnis, Diff und
   Validatorstatus („OK“ oder konkrete Fehlermeldung) dem Nutzer zeigen.
2. **Nur nach ausdrücklicher Freigabe schreiben.** Erst dann `paveman <Datei> --apply` ausführen;
   niemals automatisch vom Trockenlauf in den Schreibmodus wechseln.
3. **`--rollback` vor dem Schreiben erwähnen.** Der Nutzer soll vorher wissen, wie sich ein
   unerwünschtes Ergebnis zurücknehmen lässt.
4. **Validatorfehler ernst nehmen.** `--locker` nicht verwenden, nur um einen Fehler zu umgehen.
   Zuerst prüfen, ob die Abweichung tatsächlich unschädlich ist; der weichere Modus erfordert eine
   bewusste Nutzerentscheidung.
5. **Kuratierte Inhalte respektieren.** Ein regelbasiertes Werkzeug erkennt nicht zuverlässig, ob
   eine Formulierung absichtlich ausführlich ist. Bei Unsicherheit den Trockenlauf-Diff sorgfältig
   prüfen.

## Voraussetzung — Modulverfügbarkeit prüfen

1. Mit `paveman --help` prüfen, ob das CLI in der aktuellen Umgebung verfügbar ist.
2. Fehlt der Befehl, den für dieses System autorisierten Modul- oder Paketweg ermitteln. Keine
   lokale Pfadstruktur, keinen Paketnamen und kein Repository erfinden.
3. Ist keine autorisierte Quelle auflösbar, die fehlende Voraussetzung als eigenen Setup-Punkt
   melden, statt den Skill blind auszuführen oder ein paralleles Modul anzulegen.
4. Nach einer Installation zunächst erneut `paveman --help` und anschließend einen harmlosen
   Trockenlauf ausführen; ein echter Schreibtest bleibt freigabepflichtig.

## Beispiele

```text
User: „Kürze meine CLAUDE.md, sie wird beim Sessionstart abgeschnitten.“

→ `paveman CLAUDE.md` (Trockenlauf)
→ Ergebnis: „12.400 → 9.800 Zeichen (-21 %), Validator: OK.“
→ Diff zeigen und auf `--rollback` hinweisen.
→ Nutzer bestätigt.
→ `paveman CLAUDE.md --apply`
```

```text
User: „MEMORY.md ist zu voll, kürze sie bitte.“

→ Trockenlauf: „893 → 893 Zeichen, keine Regel griff — der Text ist bereits knapp.“
→ Kein `--apply` empfehlen; den fehlenden Mehrwert ehrlich melden.
```

## Changelog

### 1.0.1 (2026-08-20)

- Öffentlichen Wrapper vollständig von Rechnernamen, lokalen Checkoutpfaden, Installationsdaten,
  privaten Ticketreferenzen und lokalen Testergebnissen entkoppelt.
- Nutzerneutralen Verfügbarkeits- und Installationsvertrag ergänzt und echte deutsche Umlaute
  hergestellt.

### 1.0.0 (2026-08-19)

- Öffentliche Erstversion des Wrappers mit Trockenlauf, Freigabeschritt, Rollback und
  Validatorgrenzen.
- Abgrenzung zu `knappform`, `bilingual-doc-sync` und `llm-text-hygiene`.
