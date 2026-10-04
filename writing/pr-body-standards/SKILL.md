---
name: pr-body-standards
description: >-
  PR-Body-Erstellung mit echtem Test-Execution-Vorlauf. 4-Abschnitt-Struktur (Was / Verifiziert / Risk-Register / Deferred), Pre-Existing-vs-Introduced-Trennung, Root-Cause-Tracing auf Code-Pattern-Ebene. Liefert Abnahme-fähige Handoff-Dokumente, keine Commit-Log-Wiederholungen.
version: 1.0.0
author: Yuno
license: MIT
lane: worker-flash
reasoning_effort: high
agent: Writer
routing_hint: |
  **Agent-Scope:** Long-form content, docs, proposals, copy. Off-scope: code, design, data modeling — return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# PR Body Standards – Verification-Driven Construction

Der PR-Body ist das Abnahme-Handoff-Dokument für den Reviewer. Seine Glaubwürdigkeit steht und fällt mit **echter Test-Execution**, nicht mit zitierten Briefing-Assertions.

## Wann laden

- User sagt: "Erstelle den PR-Body für Branch XY"
- User sagt: "Schreibe die PR-Beschreibung"
- User sagt: "Dokumentiere die Änderungen als PR"
- User reviewed einen eigenen Branch und fragt nach einem PR-Body

## Non-Negotiable Pre-Writing Steps

Diese Schritte MÜSSEN vor dem ersten PR-Body-Entwurf durchlaufen sein. Reihenfolge ist fix.

### 1. Lokale Tests selbst ausführen

NIEMALS Behauptungen wie "X/Y Tests grün" aus Briefings, anderen Agenten, `daily-briefing`-Snapshot-Tabellen oder Kommentaren übernehmen.

```bash
# Projekt-spezifisch — immer `jest --ci` oder das äquivalente Test-Tool live laufen lassen
cd <repo>
jest --ci 2>&1 | tail -30
```

Ausgabe zeigt echte Pass/Fail-Counts. Diese sind die einzig gültige Basis.

### 2. Introduced-vs-Pre-Existing trennen

Wenn ein Test-Failure **oder** TypeScript-Compile-Fehler auftritt: gehört er zum Branch oder war er schon vorher da?

**Für Test-Failures** (bestehend):

```bash
git stash                          # eigene Änderungen weglegen
jest --ci <test-file> 2>&1 | tail -10   # auf base-commit laufen lassen
git stash pop                      # eigenen Code zurück
```

**Für TypeScript-Compile-Fehler** (parallel check, wenn das Repo TypeScript enthält):

```bash
git stash                          # eigene Änderungen weglegen
npx tsc --noEmit 2>&1 | head -30   # auf base-commit checken
git stash pop                      # eigenen Code zurück
```

- Failure/Error erscheint AUCH auf base-commit → **Pre-Existing**. Nicht in PR-Tabelle aufführen. In separaten Punkt "Pre-Existing Failures (nicht durch diesen PR)" dokumentieren.
- Failure/Error erscheint NUR nach `stash pop` → **Introduced**. Root-cause, dokumentieren, Fix-Optionen angeben.
- Bei gemischten Ergebnissen (z.B. neue TS-Fehler im Branch + pre-existing depp-Fehler): separat listen. Pre-existing errors sind kein PR-Blocker, aber als Fund (Section 3) notieren.

### 3. JEDEN eingeführten Failure root-causen

Nicht einfach sagen: "Test X schlägt fehl". Root-Cause auf Code-Pattern-Ebene:
- Welche Rolle/ Klasse/ Modul ist betroffen?
- Welches Mapping/Profil/Config fehlt oder ist falsch?
- Was müsste sich ändern, damit der Test grün wird?

Beispiel guter Root-Cause:
> "task.owner='orchestrator' initial → withKernel übergibt role='orchestrator' + toolName='orchestrator-phase:plan' → orchestrator-Profil in TOOL_PROFILES enthält dieses Pseudo-Tool nicht → assertToolAllowed blockiert."

### 4. Reale Test- und TypeScript-Ergebnisse notieren

Ausgabe von `jest --ci` in der Form `X passed, Y total` exakt übernehmen.
Keine Rundung, keine Schätzung, keine "expected to pass"-Annahmen.
Wenn `cronjob-adapter.test.js` auf base-commit schon rot war: nicht als "bestehend" listen.

Zusätzlich: wenn das Repo TypeScript enthält, `npx tsc --noEmit` auf dem Branch laufen lassen und die Fehleranzahl notieren. In der Verifikationstabelle separat aufführen:

```
Suite                        | Ergebnis
kernel.test.ts               | 16 passed / 16 total
orchestrator.test.ts         | 5 passed / 5 total
npx tsc --noEmit             | 5 errors (alle pre-existing in depp/*)
```

## PR-Body-Struktur (2 Varianten)

Welche Variante du wählst, hängt vom PR-Scope ab:

| Kriterium | Full (Architektur) | Compact (Fix PR) |
|-----------|-------------------|-------------------|
| Dateien geändert | >5 Dateien, neues Modul | <5 Dateien |
| LOC-Änderung | >200 LOC, neues Design | <200 LOC, Bugfixes |
| Test-Impact | Neue/sich ändernde Tests | Minimale Änderung, bestandene Tests |
| Architektur-Änderung | Neue Patterns, Module, APIs | Keine |
| Risiko | Mittel-Hoch | Gering-Mittel |

Bei Unsicherheit: **Full** wählen. Compact ist die Ausnahme für schnelle Bug-Fix-PRs.

### Variante A: Full (Architektur / Feature)

Vier Pflicht-Abschnitte für PRs mit Design-Impact, >5 Dateien oder >200 LOC:

```
## 1) Was

Architektonische Beschreibung. Welches Problem löst der PR? Was wurde neu geschaffen?
Welche Dateien/Module sind betroffen? KEINE Git-Log-Wiederholung — Design erklären.

Drei Sub-Blöcke:
- **Neue Dateien** (jede mit Zweck + wichtigem Detail)
- **Geänderte Dateien** (was wurde wo ergänzt/umgebaut)
- **Entfernte Dateien** (falls zutreffend)
```

```
## 2) Wie verifiziert

Tabelle: Suite | Ergebnis (echte Counts).

Danach: Liste der getesteten Verträge. Jeder Vertrag = eine verifizierte Aussage:
- "failOpen deckt NICHT tool-profiles ab (bleibt immer fail-closed)"
- "approvalHook ist optional: bei false blockiert, bei true durch, ohne Config übersprungen"
- "Orchestrator ohne Kernel läuft unverändert durch (Rückwärtskompatibilität)"
```

```
## 3) Architektur-Funde (Risk Register)

Inkonsistenzen, Nebenstrukturen oder Patterns, die IM ZUGE DER ARBEIT gefunden,
aber NICHT behoben wurden. Jeder Fund muss mit echten `ls`-Befehlen und Code-Lese
bestätigt sein — nichts aus dem Gedächtnis.

Pro Eintrag: **Fund** → **Warum relevant** → **Empfohlener nächster Schritt**

Oberflächliche Funde weglassen (z.B. "es gibt eine package.json" — das ist keine Erkenntnis).
Nur echte strukturelle Entdeckungen aufnehmen.
```

```
## 4) Was bewusst NICHT gemacht wurde

Features, Refactors oder Patterns, die explizit aus dem PR-Scope ausgeschlossen wurden.
Schützt den Reviewer vor der Frage "Warum wurde X nicht gleich mitgemacht?".

Pro Eintrag: Fix-or-Defer-Entscheidung mit 2-4 konkreten Optionen + Empfehlung.
ROTEN Test hier aufführen, wenn bewusst nicht gefixed.
```

### Variante B: Compact (Fix PR / kleine Änderungen)

Für Bugfix-PRs ohne Architektur-Impact (<5 Dateien, <200 LOC). Sechs Abschnitte:

```
## Zusammenfassung

Ein Satz: Was wurde gefixt und warum? (keine Git-Log-Wiederholung)

## Was ändert sich

Pro Datei eine Tabelle: Zeile(n) | Fix-Typ | Beschreibung

| Datei | Zeile | Fix |
|-------|-------|-----|
| `src/foo.src` | 50-55 | null-Guard ergänzt (Crash bei import_code) |
| `src/bar.src` | 147 | Return-Typ-Guard von `== 'string'` auf `!= 'shell'` korrigiert |

Jeder Eintrag mit Begründung _warum_ der alte Code falsch war.

## Tests

```
Build: X/Y PASS (vorher X/Y PASS — reine Defensiv-Erweiterung)
```

Oder wenn Tests vorher nicht grün waren: Vorher/Nachher.

## Out of scope / False positives

Was Scouts oder Analyse gefunden, aber NICHT angewendet hat — mit Begründung.
Dieser Abschnitt schützt den Reviewer vor "Habt ihr X gesehen?"-Nachfragen.

| Fund | Status | Begründung |
|------|--------|------------|
| `is_closed` ohne `()` | FP | Eigenschaft, keine Methode in GS 1.5.1 |
| Umlaute in Kommentaren | FP | GS 1.5.1 parsed UTF-8 in Kommentaren |

## Kontext

- Branch: `<name>` (von `<base>` abgezweigt)
- Vorgänger: `<commit-hash>` (Commit-Message)
- Doku: `<pfad>` (Abschnitt)
- Cluster/Issue: ggf. Referenz auf verwandte Issues

## Checkliste

- [ ] Build grün (X/Y)
- [ ] Keine neuen Warnings
- [ ] Scope minimal (nur echte Funde, keine Refactors)
- [ ] Reviewer-Hinweis bei kniffligen Änderungen
- [ ] In-Game smoke-test: (Status, optional manuell)
```

Beispiel: `references/compact-fix-pr-body.md` zeigt einen vollständigen Compact-PR-Body aus einer realen Session (GreyHack null-guard Fixes, +30/-10, 2 Dateien).

## Pitfalls

- **Briefing-Assertions nicht vertrauen** — Daily-Briefing-Tabellen sind Snapshots, kein Live-Zustand. `x/y grün`-Claims aus anderen Agenten sind Annahmen, keine Fakten. Ein Snapshot kann 21/21 Tests grün zeigen obwohl ein pre-existing cronjob-adapter-Failure existiert — weil die Suite nicht gelaufen ist.
- **Pre-Existing-Failures nicht in die Test-Tabelle aufnehmen** — sie verwirren den Reviewer und erzeugen "Was ist hier kaputt?"-Fragen.
- **Nicht nur Tests, auch TypeScript-Checks vergessen** — in TypeScript-Repos mit `ts-jest` laufen Tests oft grün während `npx tsc --noEmit` 5+ Compile-Fehler wirft. Beide Dimensionen prüfen und separat ausweisen.
- **Root-Cause statt Symptom dokumentieren** — "Test X fails because of Y" statt nur "Test X fails".
- **Architektur-Funde durch `ls` und Code-Lese verifizieren** — nicht nur aus dem Gedächtnis referenzieren.
- **Transparenz bei roten Tests** — wenn ein Test aus Design-Gründen rot bleibt, das klar sagen + warum + was die Optionen sind.
- **Keine Commit-Historie nacherzählen** — Section 1) soll das DESIGN erklären, nicht die Schritt-für-Schritt-Entwicklung.
- **Falsche Variante für den PR-Scope** — ein +30/-10 Bug-Fix-PR mit 2 Dateien braucht nicht die 4-Section-Full-Struktur. Nutze die **Tabelle unter `## PR-Body-Struktur`** zur Auswahl. Umgekehrt: ein neues Modul mit 15 Dateien in Compact zu pressen, wirft Fragen zum Design auf, die nicht beantwortet werden.

## Beispiel: Aus einem realen PR-Body

Section 3) Architektur-Funde, gut formuliert:

> **Zwei parallele Orchestrator-Implementierungen**
> - `src/roles/orchestrator.ts` — TypeScript, Rollen-Sequenz, KERNEL-ANGEBUNDEN
> - `src/modules/orchestrator/index.js` — CommonJS, Lane-Dispatcher, NICHT durch Kernel
> - **Nächster Schritt:** Folge-PR: Vereinheitlichung inkl. Test-Stacks (`*.test.js` vs. `*.test.ts`)

Section 4) Was bewusst nicht gemacht, gut formuliert:

> **Orchestrator-Audit-Test rot** (1 von 5 in `orchestrator.test.ts`)
> - Ursache: `task.owner='orchestrator'` initial → Pseudo-Tool `orchestrator-phase:plan` nur im `planner`-Profil, nicht im `orchestrator`-Profil
> - Option A: `task.owner` VOR erstem `withKernel()` auf `'planner'` setzen
> - Option B: `role` im Kernel-Context aus Phase ableiten statt aus `task.owner`
> - Option C: Phase-Pseudo-Tools ins `orchestrator`-Profil aufnehmen
> - **Empfehlung:** Option B (semantisch sauberste) — Entscheidung liegt beim Reviewer

## Referenzen

- `references/security-kernel-pr-body.md` — Vollständiger PR-Body des `feat/security-kernel`-Branches als Anschauungsbeispiel für die 4-Abschnitt-Struktur
- `references/pre-existing-error-verification.md` — Workflow zur Trennung von Pre-Existing vs. Introduced für Tests UND TypeScript-Compile-Fehler (git stash + jest + tsc --noEmit)
- `references/compact-fix-pr-body.md` — Kompakter PR-Body für Bug-Fix-PRs (<5 Dateien, <200 LOC), mit Out-of-Scope-Tabelle und Checkliste. Aus einer realen GreyHack-Session (2026-07-04).
