---
name: the-dmz-transfer
description: 'Transfer der Multi-Agent Orchestrierungs-Patterns aus the-dmz (TheMorpheus407) auf Hermes/GreyHack. Enthält:
  auto-develop.sh Pipeline-Architektur, Dual-Review-Gate, Sub-Agent Specs (.claude/agents/*.md), Artifact-basierte Kommunikation,
  GitHub-Integration, Cron-Design.'
version: 1.2.0
author: Yuno
license: MIT
platforms:
- linux
- macos
metadata:
  hermes:
    tags:
    - multi-agent
    - orchestrierung
    - greyhack
    - the-dmz
    - pipeline
    - cron
    - github
    category: software-development
lane: worker-heavy
reasoning_effort: xhigh
---
# The DMZ Transfer

> **Pattern-Transfer aus [TheMorpheus407/the-dmz](https://github.com/TheMorpheus407/the-dmz) in unsere Hermes-Orchestrierung.**
>
> DMZ ist ein AAA-Cybersecurity-Spiel (SvelteKit+Fastify), aber die **wahren Goldstücke** sind die Shell-Skripte `auto-develop.sh` und `auto-create-issues.sh`, die einen vollständigen Multi-Agent-Entwicklungs-Workflow orchestrieren.

## Gelernte Pattern

### 1. Pipeline-Architektur (auto-develop.sh)

```

set -euo pipefail
Research → Implement → Review A (correctness) + Review B (issue coverage)
                              ↓
                    Both ACCEPTED? → Finalize (commit, push, close issue)
                    Any DENIED? → Loop back to Implement (max 3x)
```

| Rolle | Aufgabe | Artefakt |
|-------|---------|----------|
| **Research** | Issue + Codebase + Docs lesen, analysieren | `research.md` |
| **Implementer** | Code fixen, Tests schreiben | `implementation.md` + Code-Diff |
| **Reviewer A** | Syntax, Code-Qualität, Build | `review-1.md` (ACCEPTED/DENIED) |
| **Reviewer B** | Löst das den Bug vollständig? | `review-2.md` (ACCEPTED/DENIED) |
| **Finalizer** | Stage, Commit, Push, Issue closen | `finalization.md` |

### 2. Dual-Review-Gate (das Killer-Feature)

| Reviewer | Scope | Frage | ACCEPTED wenn... |
|----------|-------|-------|------------------|
| **A (Correctness)** | Code-Qualität, Security, Build | "Ist der Code korrekt?" | Lint + Build + Tests grün |
| **B (Coverage)** | Anforderungsabdeckung | "Löst der Code das Issue?" | Alle AC-Kriterien erfüllt |

**Gate-Logik:**
- Beide müssen `ACCEPTED` als erstes Wort liefern (erste Zeile, kein Prefix)
- Bei `DENIED`: Delta-Feedback an Worker (kein Full-Rerun)
- Max 3 Retries, dann Eskalation an Supervisor

### 3. Sub-Agent Specs (.claude/agents/)

Jeder Agent bekommt eine dedizierte `.md`-Datei mit:
- **Name & Description** (YAML frontmatter)
- **Tools** (Read/Write/Edit/Grep/Bash etc.)
- **Domain-Wissen** (Architektur, Konventionen, Pfade)
- **Projekt-Layout** (exakte Pfade im Monorepo)
- **Checklisten** (was muss geprüft werden)
- **Verbotene Aktionen**
- **Output-Format** (erste Zeile = ACCEPTED/DENIED)

**DMZ-Specs** (6 Stück): backend, frontend, database, testing, devops, reviewer

**Unsere GreyHack-Specs** (6 Stück, unter `~/greyhack-tools/.claude/agents/`):
- `greyhack-syntax.md` — GreyScript-Syntax-Experte (Build, char(), if/else)
- `greyhack-mission.md` — Game-Logik, Missions-Strategie, Reraldi
- `greyhack-tools.md` — Tool-Architektur, lib_core-Integration
- `greyhack-reviewer.md` — Code-Review-Spezialist (12-Punkt-Checkliste)
- `greyhack-tester.md` — Test-Spezialist (Smoke-Tests, Coverage)
- `greyhack-deploy.md` — Deploy-Spezialist (Fileserver, wget, greybel build)

### 4. Artifact-basierte Kommunikation

Agenten reden über **Dateien**, nicht über Context. Vermeidet Kontext-Verschmutzung:

```

set -euo pipefail
logs/issues/{N}/
├── issue.json           # GitHub Issue Snapshot
├── research.md          # Research-Output
├── implementation-{N}.md # Implementierungs-Summary
├── review-1-{N}.md      # Reviewer A Verdict
├── review-2-{N}.md      # Reviewer B Verdict
├── build-output.txt     # greybel build output
└── finalization.md      # Finalize-Summary
```

### 5. Issue-Erstellung (auto-create-issues.sh)

```

set -euo pipefail
MILESTONES.md → AI Agent liest ALLE Doku → Erstellt 1 Issue → Loops bis DONE×3
```

- Liest SOUL.md, MEMORY.md, AGENTS.md, DDs, BRD, bestehende Issues
- Bestimmt den nächsten logischen Schritt aus dem Milestone-Plan
- Erstellt Issue mit Requirements + Acceptance Criteria
- Bug-Fix-Mode (M1337): Scannt Codebase nach echten Bugs
- 3× DONE in Folge = keine Issues mehr übrig → Exit

## GreyHack-Adaption

### greyhack-auto-fix.sh

`~/greyhack-tools/greyhack-auto-fix.sh`

```bash

set -euo pipefail
./greyhack-auto-fix.sh --bug <N> [--research model] [--implement model] \
  [--review-a model] [--review-b model] [--dry-run]
```

**Model-Aliase (KRITISCH: auf OpenRouter prüfen!):**
- `owl-alpha` → `openrouter/owl-alpha` (0€, 1M Kontext)
- `deepseek-flash` → `openrouter/owl-alpha` (Alias, kein :free mehr!)
- `deepseek-pro` → `deepseek/deepseek-v4-pro` (paid)

**AKTUALISIERT 2026-06-23:** `deepseek/deepseek-v4-flash:free` existiert NICHT auf OpenRouter. Alle Referenzen auf `:free` müssen durch `openrouter/owl-alpha` ersetzt werden.

### greyhack-create-issues.sh

`~/greyhack-tools/greyhack-create-issues.sh`

```bash

set -euo pipefail
./greyhack-create-issues.sh --scan             # Voll-Scan (6 Bug-Patterns)
./greyhack-create-issues.sh --scan --quick     # Schnell-Scan
./greyhack-create-issues.sh --list             # Alle Bugs anzeigen
./greyhack-create-issues.sh --milestone        # Nächstes Issue generieren
```

Scannt 112+ .src-Dateien auf 6 Pattern: char(10)-String, einzeilige if/else, get_shell-Parameter, import_code ohne .src, negative Indizes, Passwort in CLI-Parametern.

### greyhack-daily-scan.sh (no_agent Cron)

`~/.hermes/scripts/greyhack-daily-scan.sh`

Läuft als `no_agent: true` Hermes Cron um **6:00 Uhr**. Führt `--scan --quick` aus, zählt P0/P1 Bugs, prüft Git-Status.

### greyhack-daily-fix.sh (no_agent Cron)

`~/.hermes/scripts/greyhack-daily-fix.sh`

Läuft als `no_agent: true` Hermes Cron um **18:00 Uhr**. Fixiert top 3 P0-Bugs via greyhack-auto-fix.sh, committed und pusht zu GitHub.

### Modell-Strategie (Kostenoptimierung)

| Rolle | Empfohlen | OpenRouter ID | Kosten |
|-------|-----------|---------------|--------|
| Queen (Orchestrator) | deepseek-v4-pro | `deepseek/deepseek-v4-pro` | paid |
| Worker (alle Rollen) | **Owl Alpha** | `openrouter/owl-alpha` | **0€** |
| Critic (lokal) | deepseek-r1:8b | (lokal via Ollama) | **0€** |

**Owl Alpha:** 1.048.756 Token Kontext, 0€/Token, #1 Free-Modell auf OpenRouter. Perfekt für Subagenten-Scouts.

### Kritische GreyScript-Regeln (für Reviews)

- `if/else/end if` MÜSSEN mehrzeilig sein (kein inline-if!)
- `char(10)` für newline (nicht `\n`)
- `0` ist truthy, `null` ist falsy
- Keine negativen Indizes
- `import_code()` mit `.src`-Endung

## GitHub-Integration

**GitHub Remote**: `https://github.com/Toqsick/greyscripts.git`
**gh CLI**: Authentifiziert als `Toqsick`, Scopes: `repo`, `workflow`
**Push-Strategie**: Automatisch nach jedem `greyhack-daily-fix.sh` Lauf

```bash

set -euo pipefail
# Remote setzen (falls nicht vorhanden)
cd ~/greyhack-tools
git remote add origin https://github.com/Toqsick/greyscripts.git
git push -u origin master
```

**Cron-basierte GitHub-Sync:**
- Scan → erkennt neue Bugs (KEIN GitHub Issue, nur lokale Reports)
- Fix → committed + pusht zu GitHub (commit message: `fix(greyhack): ... / Closes #N`)
- Status-Cron (9:00) → prüft GitHub Issues und lokalen Stand

## Cron-Design (DMZ-Pattern)

| Cron | Uhrzeit | Typ | Was |
|------|---------|-----|-----|
| `greyhack-daily-scan` | 06:00 | no_agent | Bug-Scan + Status-Report |
| `greyscripts-daily-status` | 09:00 | LLM + Skills | GitHub-Status + MEMORY.md |
| `greyhack-daily-fix` | 18:00 | no_agent | Fix P0-Bugs + Git Push |

**Design-Regeln (von alten Crons gelernt):**
- Nicht alle 30 Minuten — zu eng, produziert Noise
- Gestaffelt: Scan morgens, Status vormittags, Fix abends
- `no_agent: true` für deterministische Shell-Scripts = 0 Token-Kosten
- LLM-Cron (daily-status) nur 1× täglich + Skills reduziert Tokens

## Artefakte

| Tool | Pfad | Beschreibung |
|------|------|-------------|
| Auto-Fix Pipeline | `~/greyhack-tools/greyhack-auto-fix.sh` | Multi-Agent Bug-Fixing mit echtem `greybel build` |
| Issue Creator | `~/greyhack-tools/greyhack-create-issues.sh` | Bug-Scanner + Issue-Generator (6 Pattern-Typen) |
| MEMORY.md | `~/greyhack-tools/MEMORY.md` | Living Project State (142 Bugs, 12 Tasks, 10 Decisions) |
| Syntax-Spec | `~/greyhack-tools/.claude/agents/greyhack-syntax.md` | GreyScript-Build/Grammatik |
| Mission-Spec | `~/greyhack-tools/.claude/agents/greyhack-mission.md` | Game-Logik, Reraldi-Mission |
| Tool-Spec | `~/greyhack-tools/.claude/agents/greyhack-tools.md` | Architektur, lib_core |
| Reviewer-Spec | `~/greyhack-tools/.claude/agents/greyhack-reviewer.md` | 12-Punkt Code-Review |
| Tester-Spec | `~/greyhack-tools/.claude/agents/greyhack-tester.md` | Smoke-Tests, Coverage |
| Deploy-Spec | `~/greyhack-tools/.claude/agents/greyhack-deploy.md` | Fileserver, 4-Phase-Deploy |
| Daily Scan | `~/.hermes/scripts/greyhack-daily-scan.sh` | no_agent Cron (6:00) |
| Daily Fix | `~/.hermes/scripts/greyhack-daily-fix.sh` | no_agent Cron (18:00) |
| Bug Reports | `~/greyhack-tools/logs/bugs/*.md` | 142 Bug-Reports (#1-#142) |
| Workflow-Doku | `~/greyhack-tools/logs/AUTO-FIX-README.md` | README zur Pipeline |
| Handbook PDF | `~/docs/system/dmz-greyhack-handbook.pdf` | Vollständige Dokumentation |
| DMZ-Referenz | `/tmp/the-dmz/` | Original-Quelle (TheMorpheus407) |

## Pitfalls (aktualisiert 2026-06-24)

1. **Modell-Änderungen brauchen Hermes-Neustart** — `delegation.model`-Changes greifen erst nach Prozess-Neustart.
2. **Subagent-Phantom-Builds** — "hab ich gebaut" ≠ "es läuft". Immer verifizieren!
3. **Dual-Review kann zwiegespaltene Ergebnisse liefern** — Ein Reviewer sagt ACCEPTED, der andere DENIED. Queen entscheidet.
4. **Delta-Feedback nicht vergessen** — Bei RETRY nur das Feedback schicken, nicht den gesamten Task-Wiederholen.
5. **Owl Alpha max_iterations** — 1M Kontext, aber max_iterations (80) kann bei komplexen Tasks erreicht werden.
6. **OpenRouter Modell-Namen ändern sich** — `deepseek/deepseek-v4-flash:free` existiert NICHT. Bei Modell-Fehlern: `curl https://openrouter.ai/api/v1/models` prüfen!
7. **Push-Konflikt mit Remote** (2026-06-24 erfahren) — wenn daily-fix-Cron zwischen lokalem Commit und `git push` läuft, lehnt Push ab. **Lösung:** `git fetch origin && git pull --rebase origin master && git push origin master`. Immer zuerst fetch!
8. **71 Bugs pro Daily-Scan ist viel Stau** — Daily-Fix holt nur 3/Tag. Bei hohem Aufkommen manuell mit Parent-Direct-Fallback arbeiten (siehe neue Sektion).
9. **Bin-Duplikate** — `bin/*.src` sind alte Build-Kopien, kein Source-of-Truth. Fixes immer im Original.
10. **xmem 12/12 Build-Blocker gefallen** (2026-06-24) — `xmem/xmem.src:186 get_shell(username, password)` → `get_shell`. Buildet jetzt! Letzter Lückenbüßer seit 2+ Wochen.
11. **Negative Indices sind buildbar** (Erkenntnis 2026-06-24) — `[-1]`, `[:-1]` werden von greybel akzeptiert. Runtime-Verhalten unbekannt. Kein Build-Blocker.
12. **CI-Pipeline aktiv** — GitHub Actions in `.github/workflows/`: Matrix-Build aller 35 .src + Bug-Scan (05:00 UTC). Badges in README.

## Parent-Direct-Fallback (NEU 2026-06-24)

Wenn der daily-fix-Cron zu langsam ist oder du gezielt Hotspots abräumen willst, kann Yuno direkt im Parent-Modus fixen ohne Subagenten. **3 Rollen** wie bei Subagent-Workflow, aber inline:

| Rolle | Aufgabe | Output |
|-------|---------|--------|
| **Architekt** | Bug-Report + Code-Datei lesen, Pattern erkennen | Liste der zu ändernden Zeilen |
| **Implementierer** | `patch` mit replace_all/mehrere replace-Calls anwenden | Diff |
| **Validator** | `greybel build <datei>` ausführen, vorher/nachher vergleichen | Build-Status |

**Wann einsetzen:**
- Viele mechanische Bugs gleichen Patterns (z.B. einzeiliges if/else) → schneller als Subagenten pro Bug
- Cron-Backlog abbauen
- Hotspot-Dateien mit vielen Issues gleichzeitig aufräumen

**Wann NICHT:**
- Komplexe Logic-Bugs die Recherche brauchen
- Refactorings über mehrere Dateien
- Tests erforderlich

**Beispiel-Session 2026-06-24:** 25 P0 in 3 Dateien (debugcore 8, buildcore 4, hardening 13) manuell gefixt, alle 3 Builds vorher rot → nachher grün, 17 Bug-Reports auf FIXED markiert, 4 Commits erstellt + gepusht. ~20 Min Aufwand statt 8+ Subagent-Runs.
| Deploy-Spec | `~/greyhack-tools/.claude/agents/greyhack-deploy.md` | Fileserver, 4-Phase-Deploy |
| Workflow-Doku | `~/greyhack-tools/logs/AUTO-FIX-README.md` | README zur Pipeline |
| Cron-Scan Script | `~/.hermes/scripts/greyhack-daily-scan.sh` | Täglicher Bug-Scan (6:00) |
| Cron-Fix Script | `~/.hermes/scripts/greyhack-daily-fix.sh` | Täglicher Auto-Fix (18:00) |
| DMZ-Referenz | `/tmp/the-dmz/` | Original-Quelle (TheMorpheus407) |

## Referenzen

- [TheMorpheus407/the-dmz](https://github.com/TheMorpheus407/the-dmz) — Das Original (SvelteKit + Fastify Cybersecurity Game)
- `multi-agent-work` Skill — Hermes' eigener 6-Phasen-Workflow
- `gaming/greyhack` Skill — GreyScript-Syntax-Referenz
- `references/cron-github-integration.md` — Detaillierte Cron- und GitHub-Konfiguration
- `references/session-2026-06-23.md` — DMZ-Transfer Vollausbau (8 Subagent-Tests, 142 Bugs, Handbook)
- `references/session-2026-06-24.md` — Working-Copy Cleanup + Parent-Direct-Fallback Pattern (25 P0 manuell gefixt, Push-Konflikt-Solution)
- `references/session-2026-06-24-round2.md` — 40+ P0 Syntax-Fixes, xmem 12/12 Build-Blocker, CI-Pipeline (GitHub Actions Matrix-Build), Negative-Index-Erkenntnis
- `references/cron-design-patterns.md` — Cron-Architektur und Schema