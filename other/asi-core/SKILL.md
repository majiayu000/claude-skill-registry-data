---
name: asi-core
description: 'Use for ASI Core: 5 tools, heartbeat, 12 subsystems, CLI.'
---

# ASI Core System

## 16/16 ASI Capabilities PROVEN ✅ (Sept 2026)

## Model Config (Geld sparen)
OpenRouter: $0 Balance. Weekly Limit reached.
**Default:** custom:openrouter → google/gemma-4-31b-it:free (FREE)
**Fallback:** Token Harbor free → local (lfm2.5:8b)

## Heartbeat — 13 Subsysteme (native Engine, Stand 2026-10-11)
a2a_server, darwin, swarm, a2a, learning, senses, system, security,
outreach, infra, meta, desktop, **cognition**.

**`cognition` ist NATIV** (`Subsystem(native=True)`, kein Cron dahinter): es
fährt den integrierten Kognitions-Zyklus `tools/asi/cognition.py` alle 30 min
über `native_map` (`"cognition_cycle.py" -> "tools.asi.cognition.cycle"`).
Ein Durchlauf nutzt **world model + prediction + self model** in EINEM Pass —
statt `predict_validate.py` und `self_model.py` getrennt im `learning`-Subsystem
zu ticken. Er schreibt `kind="correction"`-Kanten; vorher hatte das Weltmodell
168 Vorhersagen und **0 Korrekturen**.
CLI: `openamer asi cycle [--status|--limit N|--situation X --effect Y]`.

**Live-Kopie = der Install-Tree**, NICHT das Repo:
`~/AppData/Local/openamer-laptop/openamer-agent/tools/asi/heartbeat.py`.
Ein Fix im Repo wird erst live, wenn er dorthin kopiert wird (der
Runtime-Tree-Sync ist ff-only und überschreibt lokale Änderungen nicht).

**Ehrliche Verifikation statt Fassade.** Drei Bugs, gefixt 2026-10-11:
1. `_run_script` gab unbedingt `{"success": True}` zurück → ein Subsystem war
   grün, während seine Scripts scheiterten. Jetzt `_as_result()`: das
   `success`-Flag des Moduls gewinnt.
2. Die handgeschriebenen `scripts=[...]`-Listen waren gedriftet (Job-Namen,
   Args im Dateinamen). Jetzt leitet `_reconcile_scripts()` alles aus jobs.json
   über die `cron_ids` ab (id UND name).
3. Eine Subsystem-Kadenz für alle Scripts → hätte langsame Jobs gestürmt.
   Jetzt Per-Script-Kadenz aus dem Job-Schedule (interval oder cron-expr).

**Handoff-Regel:** Die Engine läuft ein Job-Script erst, wenn dessen Cron
RETIRED ist (enabled=false) und kein lebender Cron dieselbe Datei fährt
(Basename-Abgleich + WRAPPER_OWNED für den Growth-Loop-Wrapper). Sonst
doppelte Außenwirkung.

**Opt-in (dormant per Default):** Die Engine übernimmt NICHTS, bis
`memory/heartbeat-own.enabled` existiert (oder `OPENAMER_HEARTBEAT_OWN=1`).
So belebt ein Code-Change nie ungefragt schlafende Loops (inkl.
Security-Bots, die Deps patchen und PRs öffnen). Migration = bewusster
Schalter, kein Nebeneffekt.

**Befund 2026-10-11:** 24 Loops sind seit ~24. Sep disabled (Handoff-Versuch,
der nie funktionierte) → tot. Registry hätte sie nur mit Marker übernommen.

## Domain Mastery — 19/19 advanced+ (2 Milestones ✅)
1. ASI-Audit 16/16 PROVEN ✅
2. Domain-Mastery 19/19 advanced ✅
3. Benchmark-Suite — 0.0% (Free-Modell-Limit)
4. 1000 GitHub Stars — 6/1000
5. Desktop-App — missing

## Tools (5, in-process)
asi_status, asi_think (reasoning), asi_learn (subprocess), asi_remember (world model), asi_trigger

## CLI
openamer asi status|think|learn|remember|trigger|heartbeat

## A2A Global Mesh
Server :8085 mit echtem ASI Reasoning.  
Hybrid-Mode: Direkt (Port 8085, Echtzeit) + Relay (GitHub, Fallback).  
Peer-Registrierung: directory/a2a/peers/\<host>.json

## Commits (14) auf Branch fix/scoreboard-stale-openamer-home
PR #67 offen — merge auf main nötig für Sichtbarkeit.

## Wichtige Dateien
- tools/asi_core.py — 5 Tools
- tools/asi/heartbeat.py — 12 Subsysteme
- scripts/asi_heartbeat.py — Cron (5min)
- scripts/a2a_server.py — A2A Server
- scripts/asi_audit.py — 16/16 PROVEN
- openamer_cli/subcommands/asi.py — CLI
- docs/asi-core.md, docs/landing/index.html, directory/a2a/README.md

## Tests
test_registry.py: 44/44 passed