---
name: multi-agent-work
description: '/multi-agent-work — Von Research bis Implementierung in einem Durchlauf. 6-Phasen-Workflow: Research → Fixes
  → Synthese → Implementierung → Evaluierung (lokaler Critic) → Finalizing. V1.3: Lokaler deepseek-r1:8b Critic via Ollama,
  differenzierte Phasen-Timeouts.'
version: 1.7.0
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - multi-agent
    - research
    - implementierung
    - workflow
    - slash-command
    category: software-development
author: Hermes Agent
license: MIT
lane: koenigin
reasoning_effort: xhigh
---
# /multi-agent-work

> **Von Research bis Implementierung in einem Durchlauf — oder Testlab für Orchestrierungs-Experimente.**
> Kombiniert `multi-agent-research` + `ki-murks-verhindern` + `rag-pipeline-python` + `critic-gate` + `output-validator`.
>
> **Metapher: Bienenkönigin und Schwarm.** Der Parent (Queen) orchestriert spezialisierte Worker (Hivemind). Jeder Worker hat eine enge Rolle und liefert ein konkretes Artefakt. Die Queen synthetisiert, prüft und entscheidet über Freigabe.

## Referenzen

**Detail-Dateien (dieser Skill):**
- `references/phase-0-gate-check.md` — Gate-Smoke-Test, Gate-Fix-Befehle, Modus-Verhalten
- `references/phase-details.md` — Phasen-Timeouts, Experten-Scopes, Context-Template, Beispiel-Durchlauf, Output-Struktur
- `references/critic-and-retry-gate.md` — Ollama-Critic-Script, Output-Schnittstelle, Retry-Gate-Config, DMZ Dual-Review-Pattern
- `references/queen-rule-and-quality-gates.md` — Claude-Flow-Transfer, Queen-Rule, Quality Gates, Anti-Patterns
- `references/greyscript-deployment.md` — GreyScript In-Game Deployment, Syntax-Regeln, greybel-vs Mock-Env
- `references/pitfalls.md` — Vollständige Pitfall-Liste (Orchestrierung, Git, TS, Memory, GreyHack)
- `references/artifact-spec-dispatch.md` — Artifact-Specification Dispatch: Voll-Vorlage + 5-Lane-MaxClaw-Buildout (2026-07-04)
- `references/slash-command-setup.md` — Slash-Command Registrierung + Verwandte Skills

> **Note:** Die folgenden Session-Referenzen wurden beim Slim-Down entfernt, da die referenzierten Dateien nie existierten und nur als Bullet-Liste dokumentiert waren. Workflow-Inhalte sind vollständig in den oben gelisteten `references/`-Dateien erhalten.

## Architektur (V1.2)

```
┌─────────────────────────────┐
│  SUPERVISOR (Orchestrator)  │
│  • Decomposition            │
│  • Budget-Tracking          │
│  • Retry-Gate               │
└───────────┬─────────────────┘
        ┌───┼───┐
        ▼   ▼   ▼
  ┌────────┐ ┌────────┐ ┌──────────┐
  │ WORKER │→│ CRITIC │ │RESEARCHER│
  │ owl-α  │ │ r1:8b  │ │ r1:8b    │
  │ (API)  │ │(GPU,0€)│ │ (RAG)    │
  └────────┘ └───┬────┘ └──────────┘
                 │ FAIL → Feedback
                 └─→ zurück an WORKER (max 2x)
```

Details zu Critic-Script + Retry-Gate: `references/critic-and-retry-gate.md`

## Unterschied zu `/research`

| `/research`        | `/multi-agent-work`           |
|--------------------|-------------------------------|
| Nur Recherche      | Research + Implementierung    |
| Doku am Ende       | Code läuft am Ende            |
| 4 Phasen           | 6 Phasen                      |
| Experten berichten | Experten bauen                |

## Betriebsmodi

Der Skill kennt zwei Betriebsmodi. Wähle vor dem Start:

| Modus          | Fokus                                      | Wann                                                              | Phase 0 | Retro-Tiefe                  | Artefakte                              |
|----------------|--------------------------------------------|-------------------------------------------------------------------|---------|------------------------------|----------------------------------------|
| **Delivery**   | Produktiv-Code ausliefern                  | User sagt „mach", „baue", „implementiere"                         | Überspringbar | Kurz (Phase 6)               | Nur Build-Code + Doku                  |
| **Experiment** | Orchestrierung lernen, testen, verbessern  | User sagt „probier", „lerne", „teste", GreyHack-Testprojekt       | Pflicht | Ausführlich (Phase 6 + Lessons) | Zusätzlich: Experiment-Report, Lessons |

**Regel für Experiment-Mode:** GreyHack ist das Testlab — hier darf mehr schiefgehen. Jeder Blockade (Gate, fehlendes Tool) ist **Lerngelegenheit**, nicht Stoppschild. Dokumentiere was funktioniert hat UND was nicht. Phase 6 schreibt `~/docs/system/orchestration-experiment-<datum>-<tool>.md`. Der User erwartet Learnings, nicht nur ein fertiges Produkt.

**Regel für Delivery-Mode:** Code muss laufen, Tests müssen grün sein. Weniger Retro, mehr Produktivität. Quality Gates sind härter — kein „kann man später machen".

## 🐝 Variante: System-Repair-Schwarm (3-Rollen-Parallel)

> **Wann:** System-Level-Reparatur/Ops-Aufgaben mit klaren Fix-Schritten (Waydroid installieren, Docker reparieren, Module laden, Configs fixen).
> **Nicht verwenden bei:** Code-Implementation, Software-Entwicklung, Research — dafür ist der volle 6-Phasen-Workflow da.

### Architektur

```
┌────────────────────────────────────────────┐
│  ARCHITEKT (Parent = Yuno)                 │
│  • Scouts auswerten, Ist-Zustand erfassen  │
│  • Optionen entwickeln (max 4 konkret)     │
│  • User entscheiden lassen                 │
└────────┬──────────┬────────────┬───────────┘
         │          │            │
         ▼          ▼            ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ IMPLEMENTIERER │ │ IMPLEMENTIERER │ │  VALIDATOR     │
│ A (Kernel)     │ │ B (App-Level)  │ │ C (Prüfung)    │
│ • Module laden │ │ • Config/bauen │ │ • Service start│
│ • /dev nodes   │ │ • LXC-Mounts   │ │ • Logs checken │
│ • Pakete       │ │ • Symlinks     │ │ • Resultat      │
│ • Sudo-Befehle │ │ • Init         │ │ • GATES: OK/NEIN│
└────────────────┘ └────────────────┘ └────────────────┘
        │                  │                   │
        └──────────────────┘───────────────────┘
                           ▼
              ┌──────────────────────┐
              │ SYNTHESE (Architekt) │
              │ • Läuft's?          │
              │ • Eskalation nötig? │
              │ • Doku schreiben    │
              └──────────────────────┘
```

### Rollenverträge (KRITISCH)

Jeder Subagent bekommt **exakt einen Rollenvertrag** — klare Trennlinie, keine Überschneidungen:

| Rolle | Macht | Macht NICHT | Sudo? |
|-------|-------|-------------|:----:|
| **Architekt (Parent)** | Scouts lesen, Optionen bauen, User entscheiden lassen, Synthese schreiben, Doku machen | Keine System-Schreibzugriffe, kein Code-Ausführen | ❌ |
| **Implementierer A** | Kernel-Module (`modprobe`), `/dev`-Nodes, Paket-Installation (`apt`), `modules-load.d`, udev-Regeln, `sysctl` | Keine Application-Config, keine LXC-Sachen, kein Init | ✅ |
| **Implementierer B** | Waydroid-Init, LXC-Mount-Config, Symlinks, `.conf`-Files, Service-Restarts, User-Session | Keine Kernel-Operationen | ✅ |
| **Validator C** | Service-Status checken (`systemctl`, `waydroid status`), Logs auswerten (`tail`), Device-Nodes prüfen (`ls -la /dev/*`), Ergebnis "RUNNING/STOPPED/BROKEN" melden | Keine Schreibzugriffe, keine Config-Änderungen | ❌ |

### Das Sudo-Problem (KRITISCH — Live-Lesson 2026-07-04)

Die Terminal-Umgebung hat **kein interaktives TTY**. `sudo -v` kann nicht programmatisch eingegeben werden.

**Phase-Planung muss das einplanen:**

1. **Phase 1: Scouts + Architekt (ohne Sudo)** — Read-only: Ist-Zustand erfassen, Optionen entwickeln, User entscheiden lassen
2. **Phase 2: Sudo abholen** — User: `sudo -v` im echten Terminal → 15 Min Timer
3. **Phase 3: Implementierer feuern (mit Sudo)** — Parallel A+B starten. WEIL Sudo-Credentials existieren (15 Min), können exakt 2-3 terminal()-Calls mit `sudo` durchlaufen. **Danach erneut `sudo -v` wenn länger gearbeitet wird.**
4. **Phase 4: Validator + Synthese** — Read-only: läuft's?

**Wenn Sudo tot ist (kein interaktiver Zugang zum Terminal):**
- Alles vorbereiten (Scripte, Config-Blöcke, Befehlsliste)
- Dem User als **einen Block zum Copy-Paste** präsentieren
- Danach: User sagt "weiter" oder posted Log-Ausgabe → Validator übernimmt

### Template für Implementierer-Context

```
AUFGABE: <ein Satz, was in dieser Rolle zu tun ist>

IST-ZUSTAND (Architekt-Erkenntnis):
- <konkreter Befund 1>
- <konkreter Befund 2>

LIEFER-ARTEFAKTE (müssen auf dem System existieren):
- <Pfad zur Config-Datei>
- <geladenes Modul / /dev-node>
- <installiertes Paket>

QUALITÄTS-GATES:
- [ ] <Bedingung 1> — prüfbar via `ls`, `lsmod`, `cat /proc/...`
- [ ] <Bedingung 2>

WARNUNG:
- **Sudo-Prompt wird nicht funktionieren** — `set -e` ABBRICHT bei erstem `sudo`-Fail mit Fehler. Wenn du `sudo -A` siehst, warte auf User-Input.
- Code-Kommentare immer DEUTSCH
- Nach jedem Schritt: `ls`/`cat`/`lsmod` zur Verifikation
```

### Beispiel: Waydroid-Reparatur (Session 2026-07-04)

Siehe `references/system-repair-schwarm.md` für die vollständige Waydroid-Case-Study mit:
- Scout-Fragenkatalog (5 Lanes parallel)
- Chicken-and-Egg-Problem host-permissions ↔ binder_linux
- Sudo-Fallback-Strategie (Copy-Paste-Block)
- Validierungs-Checkliste

### Vergleich: System-Repair-Schwarm vs. andere Modi

| Merkmal | System-Repair | Delivery | Experiment |
|---------|:------------:|:--------:|:----------:|
| Phasen | 4 Phasen (Scout→Sudo→Fix→Verify) | 6 Phasen | 6 Phasen |
| Sudo-Problem | **Zentrales Hindernis** — immer einplanen | Selten | Selten |
| Rollenanzahl | 3 parallel (A+B+C) | Sequential (Implement→Review) | Research→Build |
| Validator | 1 Live-Check (läuft's?) | Spec + Quality Dual-Review | Ausführlich |
| User-Eingriff | `sudo -v` erforderlich | Kein zwingender Eingriff | Kann Feedback geben |
| Artefakt-Typ | System-Zustand (geladene Module, laufender Service) | Code + Tests | Code + Doku + Lessons |

## Trigger

```
/multi-agent-work <aufgaben-beschreibung>
```

Beispiele:
```
/multi-agent-work "Baue einen RSS-News-Fetcher der täglich Esports-News zieht und per Telegram ausgibt"
/multi-agent-work "Recherchiere Common Crawl Index-API und baue ein Python-Tool dafür"
/multi-agent-work "Implementiere eine RAG-Pipeline für aktuelle IEM-Cologne-Infos"
```

Slash-Command-Registrierung: `references/slash-command-setup.md`

## Phase 0: Pre-Flight Realitäts-Check (Checklist)

**Pflicht-Checkliste VOR jedem Spawn.** Führe diese Checks parallel über mehrere `terminal()`-Calls aus:

- [ ] **GitHub Auth** — `gh auth status 2>&1` = logged in? Sonst sind PRs/Repo-Pushes unmöglich und subagenten erstellen nur lokale Files, die niemand reviewed.
- [ ] **Cron Health** — `hermes cron list 2>&1` → laufen alle Jobs? Gibt es Provider-Drift-Fehler (#44585)? Ungepinnte Crons brechen bei Modellwechsel — notiere welche neu gepinnt werden müssen.
- [ ] **Ziel-Pfade existieren** — `ls -la` auf alle Pfade die Subagenten verwenden werden. User-Pfade sind HINWEISE, keine Verträge.
- [ ] **Abhängigkeiten prüfen** — Sind die Tools/CLIs installiert, die Subagenten brauchen? (sqlite3, python3, gh, git, jeweilige Compiler)
- [ ] **Ist-Zustand dokumentieren** — Kurz notieren: was ist der Stand-jetzt? (Commits, Crons, Files) → späteres Diff wird möglich.
- [ ] **Smoke-Test** (zweite Welle): `delegate_task` mit `echo GATE_OK` — funktioniert?
- [ ] **Gate-Blocker-Muster prüfen:** `HermesUltraCode gate`, `base_prompt is empty`, `Cannot resolve delegation provider`?
- [ ] **BEI BLOCKER:** Erst Fix-Befehle ausführen (siehe `references/phase-0-gate-check.md`), DANN Fallback
- [ ] **BEI FIX:** Hermes Desktop komplett neu starten (nicht nur `/reset`!)
- [ ] **BEI FIX-SCHEITERN:** Parent-Direct-Fallback

**Modus:**
- **Experiment:** Phase 0 ist Pflicht (dokumentiere was funktioniert hat und was nicht)
- **Delivery:** Überspringbar wenn Subagenten in dieser Session schon einmal funktioniert haben

**Live-Demo (2026-07-04):** Die 5-Lane MaxClaw-Orchestration hatte Phase 0 über 10 terminal-Calls parallel — GitHub-Auth prüfen, Cron-Liste laden, DB-Struktur via sqlite3 .schema abfragen, Ziel-Pfade verifizieren. Erst als alles grün war → Dispatch.

Vollständige Gate-Fix-Befehle + Diagnose: `references/phase-0-gate-check.md`

### Phase 1b: Artifact-Specification Dispatch (für Buildout-Missionen)

Nicht jede Mission braucht 3 Research-Experten. Für **strukturierte Buildout-Missionen** (Repos aufsetzen, Skills schreiben, Konfigurationen bauen, mehrere Subsysteme parallel entwickeln) hat sich das **5-Lane-Artifact-Spec-Pattern** bewährt:

**Wann Phase 1b statt Phase 1a:**
- Du baust mehrere unabhängige Subsysteme (Workflows + Configs + Skills + Security + DB-Tools)
- Die Artefakte pro Lane sind klar definierbar (Datei X muss nach Pfad Y)
- Die Lanes haben keine starken Abhängigkeiten untereinander

**Pattern:**

Jeder `delegate_task`-Task MUSS eine `LIEFER-ARTEFAKTE`-Sektion enthalten — nicht nur ein vages Ziel, sondern exakte Pfade + Qualitäts-Gates:

```
AUFGABE: [1-3 Sätze, was genau zu tun ist]

LIEFER-ARTEFAKTE (müssen real existieren + verifiziert sein):
- /tmp/project/workflows/thing.md (Workflow-Definition für Cron)
- ~/bin/thing.sh (ausführbar, chmod +x, Shell-Skript, set -euo pipefail)
- ~/bin/thing.py (Python, CLI mit argparse)
- ~/docs/system/thing-YYYY-MM-DD.md (Doku auf Deutsch)

WICHTIG:
- Watchdog-Pattern: silent on success, alert on anomaly
- Bash mit set -euo pipefail, aussagekräftige Fehlermeldungen
- YAML-Frontmatter prüfbar (korrektes Format)
- Code-Kommentare immer DEUTSCH
- Verifikation: ls -la + Dry-Run-Output am Ende
```

**Warum:** Ohne Artefakt-Spezifikation liefern Subagenten optimistische Zusammenfassungen ("✅ done") statt echter Dateien. Exakte Pfade + Gates erzwingen reproduzierbare Artefakte und machen den Cross-Check zu einer Datei-Existenz-Prüfung statt Vertrauensfrage.

**Live-Demo (2026-07-04 MaxClaw-Upgrade):** 5 Lanes — DB-Tools, Config-Refactor, Workflows, Skills, Security. Jede Lane hatte 6-10 Artefakte spezifiziert. Alle 5 Subagenten lieferten reale Files, kein „✅ done" ohne Output.

**Siehe auch:** [`references/artifact-spec-dispatch.md`](references/artifact-spec-dispatch.md) — die komplette Vorlage mit Lane-spezifischen Context-Templates.

---

## Der 6-Phasen-Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 1: PARALLEL RESEARCH (3 Experten, ~5-10 min)                │
│  • Expert 1: Architektur & Design                                   │
│  • Expert 2: Implementation & Code                                  │
│  • Expert 3: Testing & Edge Cases                                   │
│  → Jeder liefert: Recherche + konkreten Implementierungsplan        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 1b: ARTIFACT-SPECIFICATION DISPATCH (für Buildout-Missionen)│
│  • Statt 3 Research-Experten: 3–5 parallel Build-Lanes dispatch    │
│  • Jeder Task MUSS LIEFER-ARTEFAKTE mit exakten Pfaden enthalten   │
│  • Qualitäts-Gates pro Artefakt: chmod +x, set -euo pipefail,      │
│    silent-on-success, Code-Kommentare DEUTSCH                       │
│  • Siehe references/artifact-spec-dispatch.md für Voll-Vorlage      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 2: IMMEDIATE FIXES (Parent, während Research/Work läuft)    │
│  • Offensichtliche Quick-Wins umsetzen                              │
│  • Dependencies installieren, Verzeichnisse erstellen, Config-Vorlagen│
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 3: SYNTHESIS & PRIORISIERUNG                                │
│  • Deduplizieren, Konflikte checken, Claims verifizieren            │
│  • Priorisieren: P0 (heute) / P1 (diese Woche) / P2 (später)       │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 4: IMPLEMENTIERUNG (Der wichtigste Unterschied!)            │
│  • Grounding → Execution → Evaluation (Output-Validator + Critic)  │
│  • Finalizing: Diff zeigen, User bestätigen, git commit             │
│  → Nicht nur dokumentieren — CODE MUSS LAUFEN                       │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 5: DOKUMENTATION                                            │
│  • ~/docs/builds/YYYY-MM-DD-<projekt>.md + README.md im Projekt    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 6: RETROSPECTIVE                                            │
│  • Was hat funktioniert? Was nicht? Phantom-Fixes?                  │
│  → In Skill patchen für nächstes Mal                                │
└─────────────────────────────────────────────────────────────────────┘
```

## Post-Subagent: Review- & Fix-Phase (KRITISCH — Live-Lesson 2026-07-04)

**Nachdem Subagenten zurückkommen, MUSS die Queen einen strukturierten Review machen.** Nie blind glauben. Subagenten (besonders auf günstigen Modellen) behaupten mit hoher Wahrscheinlichkeit Testergebnisse, die sie nie ausgeführt haben, oder übersehen Syntax-Fehler, Architektur-Brüche und Repo-Privatheit.

### Review-Checkliste (30-90 Sekunden pro Subagent)

```
BEHAUPTUNG des Subagenten          │ QUEEN-CHECK
───────────────────────────────────┼─────────────────────────────────────
"Tests laufen alle grün"           │ Queen: re-run `npm test` selbst
"Datei existiert an Pfad X"        │ Queen: `ls -la <pfad>` — Existenz + Größe
"Branch ist gepusht"               │ Queen: `git log --oneline -3` im Ziel-Repo
"PR ist offen, Body hat URL Y"     │ Queen: `gh pr view <n> --json body -q '.body'`
"Build 19/19 grün"                 │ Queen: Build-Skript selbst fahren
"Fixes committed"                  │ Queen: `git status --short` + `git log --oneline -5`
```

### Konkrete Bug-Patterns, die die Queen fangen MUSS

| Pattern | Erkannt am | Fix |
|---------|-----------|-----|
| **Einzeiler-`if`** (greybel) | greybel CI 0/19 | `if cond then BODY end if` als 1-Zeiler → greybel build parst nicht. Immer Mehrzeiler |
| **Phased-but-no-permission** | Hermes-v7 orchestrator | Subagent nutzt `task.owner` (initial='orchestrator') für Permission-Checks → failt. Fix: `PHASE_ROLE_MAP` als Single-Source-of-Truth |
| **Fehlender Profile-Eintrag** | Hermes-v7 tool-profiles.ts | Subagent fügt Phase-Logik hinzu aber vergisst Pseudo-Tools in `TOOL_PROFILES` |
| **PR-Body mit 404-URL** | PR #7 hermes-v7 | `raw.githubusercontent.com`-Link für privates Repo. Fix: Im Context mitgeben ob privat, oder Queen prüft nach |
| **CLI-Syntax veraltet** | greyscripts ci-build.sh | Subagent kopiert CI-Skript ohne aktuelle CLI-Syntax zu prüfen |
| **TS-Toolchain ignoriert** | hermes-v7 | `.ts` geschrieben ohne `tsconfig.json`/`typescript`-dep → Tests nie gelaufen |

### Ablauf: Review → Fix → Verifikation → Persistenz

```
1. Subagent zurück: Output + alle Claims kritisch lesen
2. Queen-Checks starten (terminal-Calls batchen):
   - `ls -la` für behauptete Dateien
   - `npm test` / Build-Skript für behauptete Testergebnisse
   - `git log --oneline -3` für behauptete Commits
   - `gh pr view` für PR-Body-URLs auf 404 prüfen
3. BEI FEHLERN: Queen fixen (klein) ODER Subagent erneut delegieren (groß)
4. Nach Fix: Erneut verifizieren (Tests laufen lassen!)
5. Erst dann: PR öffnen, Memory persistieren, Doku schreiben
```

**Faustregel:** 30-90 Sekunden Review pro Subagent spart Stunden Debugging nach Merge.

---

**Phasen-Details (Timeouts, Experten-Scopes, Context-Template, Beispiel-Durchlauf, Output-Struktur):** `references/phase-details.md`

**Retry-Gate, Critic-Script, Ollama-Setup:** `references/critic-and-retry-gate.md`

**Queen-Rule, Quality Gates, Anti-Patterns:** `references/queen-rule-and-quality-gates.md`

**Vollständige Pitfall-Liste:** `references/pitfalls.md`