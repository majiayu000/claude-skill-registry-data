---
name: bugsweep
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-06-13
description: Systematic bug sweep with a codebase-scaled target value, doubling escalation, area tracking, and final verification. Use on /bugsweep or whenever the user requests a systematic bug pass.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="bugsweep banner">

# /bugsweep — Systematischer Bug-Sweep Workflow

Iterative Bug-Suche mit konvergierendem Abbruchkriterium. Skaliert mit der Codebasis, eskaliert bei Verdacht auf oberflächliche Suche, und verhindert Wiederholung durch Bereichs-Tracking.

## 1. Grundrate berechnen

```
LOC = produktive Quellzeilen (src/, lib/ — ohne Tests, Configs, Docs, generated)
x = max(1, ceil(LOC / 1500))
Grundrate = x * 3
```

| LOC | x | Grundrate |
|-----|---|-----------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

Melde dem User: "Codebasis: {LOC} LOC → Grundrate = {Grundrate} saubere Suchläufe."

## 2. Suchschleife

```
zähler = 0
ziel = Grundrate
je_bug_gefunden = False
geprüft = []  # (bereich_name, typ: code|aufgabe)

LOOP:
  bereich = wähle_neuen_bereich()  # Siehe Bereichs-Regeln
  geprüft.append(bereich)
  
  Führe gründliche Bug-Suche durch
  
  IF Bug gefunden:
    je_bug_gefunden = True
    Fix nach bugfix-protocol (Phase 4+5)
    Review: siehe Modell-Regel (neuere Modellklassen: kein externer Review nötig)
    Commit + Push
    zähler = 0  # RESET
  ELSE:
    zähler += 1
    Melde: "✓ Sauber: {bereich} — {zähler}/{ziel}"
  
  IF zähler >= ziel:
    IF NOT je_bug_gefunden:
      # Verdoppelungs-Eskalation: kein einziger Bug → zu oberflächlich?
      ziel = Grundrate * 2
      je_bug_gefunden = True  # Eskalation nur EINMAL
      Melde: "⚠ Kein Bug in {Grundrate} Läufen → Ziel verdoppelt auf {ziel}."
      CONTINUE LOOP
    ELSE:
      GOTO Abschluss-Verifikation
```

### Praxis-Hinweise zur Suchschleife (aus Sweeps gelernt)

- **Nicht-Git-Repos:** Wo es kein `git` gibt (z. B. Cloud-synchronisierte Projektordner), ersetzt ein **versioniertes Backup** das "Commit + Push": vor dem ersten Fix `datei_<ts>.bak` anlegen. **Achtung — das Pre-Fix-Backup ist KEINE Sicherung der Arbeit:** nach dem letzten Fix ein frisches `_FINAL_`-Backup ziehen, sonst ist bei einem Sync-Hiccup die gesamte Fix-Arbeit verloren.
- **Viele vorab bekannte Bugs:** Sind beim Start schon N Bugs bekannt (z. B. aus einem vorherigen Lauf), ist "pro Bug: Fix → Review → Commit → Reset" unpraktikabel. Dann die bekannten Bugs als EINEN Fix-Block abarbeiten (gemeinsamer Review am Ende) und die Grundrate/Suchschleife ab dem ersten NEU gefundenen Bug zählen. Die Reset-Logik gilt weiter für während des Sweeps neu gefundene Bugs.
- **Gleicher Bug an mehreren Stellen:** Ein gefundener Fehler (z. B. ein falsches Regex, eine kaputte Format-Annahme) steckt oft kopiert an weiteren Stellen. Nach jedem Fix per Suche prüfen, ob dasselbe Muster anderswo vorkommt — das ist ein eigener, lohnender "Bereich".

## 3. Bereichs-Regeln (Anti-Gaming)

Ein "Bereich" ist entweder ein **Code-Fokus** oder eine **Aufgabe** (Zweck des Codes).

### Code-Fokus
- Darf zwischen Läufen **erweitert** (mehr Dateien) oder **verschoben** (anderer Teil) werden
- Darf NICHT exakt dieselbe Auswahl sein wie in einem früheren Lauf
- Beispiel OK: Lauf 1 = `maintenance.py`, Lauf 5 = `maintenance.py + orchestrator.py` (erweitert)
- Beispiel NICHT OK: Lauf 1 = `maintenance.py`, Lauf 5 = `maintenance.py` (identisch)

### Aufgabe (Zweck)
- Darf **granulärer** gestellt werden (Subfunktion prüfen) oder **breiter** (zusammenhängende Funktionen)
- Darf NICHT exakt dieselbe Aufgabe sein
- Beispiel OK: Lauf 1 = "Thread-Safety im Watchdog", Lauf 5 = "Thread-Safety Tray gesamt" (breiter)
- Beispiel OK: Lauf 1 = "Prozesserkennung", Lauf 5 = "Store-Marker-Matching in Prozesserkennung" (granulärer)
- Beispiel NICHT OK: Lauf 1 = "Thread-Safety im Watchdog", Lauf 5 = "Thread-Safety im Watchdog" (identisch)

### Benennung
- Bereich MUSS VOR der Suche benannt werden (kein nachträgliches Zuordnen)
- Format: `"{Name}" ({typ}: code|aufgabe)`

## 4. Abschluss-Verifikation

Nachdem zähler >= ziel UND je_bug_gefunden:

**Schritt A — bugfix-protocol Phase 5:**
- [ ] Vollständige Test-Suite grün (`pytest`)
- [ ] **Geänderten Ausführungspfad mindestens einmal REAL durchlaufen** — nicht nur Tests. Grüne Unit-Tests an Code, der die geänderte Stelle gar nicht aufruft, sind Scheinsicherheit. Den tatsächlich geänderten Pfad ausführen (Dry-Run, Smoke-Lauf, CLI-Aufruf) und auf Tracebacks / Signatur- / Namensfehler prüfen. `py_compile` bzw. Import allein prüft NUR Syntax — nicht, ob der Pfad läuft.
- [ ] **Jeder Fix hat mind. einen Test, der ihn berührt** — ein Fix ohne Test, der die geänderte Verzweigung tatsächlich auslöst, gilt als ungeprüft (für Orchestrierungs-/Netzwerkpfade ggf. mit Mock + Dry-Run kombinieren).
- [ ] Type-Check (wenn konfiguriert)
- [ ] Lint (wenn konfiguriert)
- [ ] Edge Cases der Session-Fixes geprüft

**Schritt B — Review (Modell-Regel):**
- **Neuere Modellklassen (z.B. Claude 5 / Fable-Klasse):** KEIN externer Advisor-/Zweitmodell-Review erforderlich.
  Schritt A (Tests + realer Smoke-Lauf) ist die Verifikation. Optional bei echter
  Unsicherheit: frischer Review-Subagent — dessen Befunde aber empirisch gegenprüfen
  (Test gegen unveränderten Code), bevor sie als Bug gewertet werden.
  Hintergrund (Sweep-Erfahrung 2026-06-11): Der Zweit-Reviewer war nicht verfügbar, der
  Ersatz-Subagent lieferte 1 Befund (Konfidenz 85), der sich per Test als Nicht-Bug
  erwies — externer Review änderte das Ergebnis nicht.
- **Ältere Modelle:** Abschließende Besprechung mit Advisor (Fallback: zweites
  Modell als Reviewer); Advisor bestätigt oder findet Lücken.

**Bei Bug-Fund in Verifikation:**
→ Fix + Test + Commit
→ RESET: zähler = 0, ziel = Grundrate (frisch, KEINE Verdoppelung)
→ Zurück zur Suchschleife (geprüft-Liste bleibt, je_bug_gefunden = True)

**Bei sauberer Verifikation:**
→ FERTIG. Commit + Push. Protokoll ausgeben.

## 5. Protokoll (am Ende)

```markdown
## Bug-Sweep Ergebnis

- **Codebasis:** {LOC} LOC
- **Grundrate:** {Grundrate} (eskaliert: {ziel})
- **Geprüfte Bereiche:** {len(geprüft)}
- **Bugs gefunden:** {anzahl}
- **Resets:** {anzahl_resets}
- **Verdoppelung ausgelöst:** ja/nein
- **Fixes:**
  - {titel} — {commit_hash}
  - ...
- **Finale Test-Suite:** {passed}/{total} grün
- **Review-Verdict:** Selbstverifikation (neuere Modellklasse) / Advisor bestätigt / Lücken benannt
```

## Wann diesen Workflow nutzen

- Nach Feature-Entwicklung (Qualitätssicherung)
- Vor einem Release (Abnahme-Sweep)
- Periodisch als Hygiene-Check
- Wenn der User `/bugsweep` tippt

## Interaktion mit anderen Skills

- **bugfix-protocol:** Fix-Verfahren (Phase 4+5) für jeden gefundenen Bug
- **systematic-debugging:** Bei schwer reproduzierbaren Bugs innerhalb des Sweep
- **code-review:** Kann als Aufgaben-Bereich genutzt werden

---

## Changelog

### 1.1.0 (2026-06-13)
- Modell-Regel für Schritt B zurückportiert (aus lokaler Skill-Installation, Stand 2026-06-11): neuere Modellklassen verifizieren per Tests + realem Smoke-Lauf selbst, kein externer Review nötig; Protokoll-Feld "Review-Verdict" entsprechend erweitert

### 1.0.0 (2026-06-13)
- Erstveröffentlichung in der Skill-Bibliothek (übernommen aus lokaler Skill-Installation, Stand 2026-06-01)
