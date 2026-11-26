---
name: asi-capability-summary
description: 'Use for 16-point ASI audit: capabilities, evidence, status.'
---

# ASI Capability Summary

OpenAmer maintains a **16-point ASI capability audit** that honestly scores every cognitive building block of an artificial superintelligence. Each capability is scored:

- **PROVEN** → implementation exists AND a cron job or runtime signal proves it runs
- **PARTIAL** → implementation exists but nothing proven runs it (e.g. tool on a shelf)
- **ABSENT** → implementation is missing

## Current Status (measured — never hand-written)

**Do not hardcode the counts.** They change as crons go live or dark. Read them:

```bash
python C:/Users/damir/AppData/Local/openamer-laptop/scripts/asi_audit.py
python .../asi_audit.py --save     # write the report
python .../asi_audit.py --json     # machine-readable
```

This skill previously carried hand-written tallies ("10/10 PROVEN", "5/6
PROVEN") that had already drifted from reality before anyone noticed — a
stale claim in an *honesty* audit is the worst place for one. The figures now
come only from the script.

`status` is derived, not asserted. Each capability is judged on two
independent axes:

- `evidence_present` — the implementation actually exists on disk
- `runtime_live`    — a cron job or runtime signal proves it *runs*

`runtime_dark` lists a capability whose cron exists but has stopped firing —
that is what separates a real capability from a tool on a shelf.

## The 16 Capabilities

### Level 1 — Foundation
| Capability | Evidence path | ASI Tool |
|---|---|---|
| Recursive self-improvement | `self_improve.py` + Darwin Engine | `asi_trigger(capability='self_improve')` |
| Calibrated self-knowledge | `predict_validate.py` | `asi_trigger(capability='validate')` |
| Self-model | `self_model.py` | `asi_trigger(capability='self_model')` |
| World model | `world_model.py` + `tools/asi/world_model.py` | `asi_remember(query=...)` |
| Episodic memory | `longterm_memory.py` | `asi_remember(query=...)` |
| Analogical transfer | `analogy_engine.py` | `asi_trigger(capability='analogize')` |
| Tool creation | `auto_skill_creation.py` | `asi_trigger(capability='create_skill')` |
| Multi-agent coordination | `swarm_intelligence.py` + `tools/asi/swarm.py` | Heartbeat: swarm-Subsystem |
| Desktop embodiment | cua-driver + desktop_ledger | computer_use tool |
| Continuous learning loop | `internet_learner.py` | `asi_learn(topic=...)` |

### Level 2 — ASI Autonomy
| Capability | Evidence path | ASI Tool |
|---|---|---|
| Domain Mastery Engine | `domain_mastery.py` | Heartbeat: meta-Subsystem |
| Strategic Goal Engine | `goal_engine.py` | Heartbeat: meta-Subsystem |
| Tool Invention Engine | `tool_inventor.py` | Heartbeat: meta-Subsystem |
| Cross-Domain Synthesis | `analogy_engine.py` | `asi_think(question=...)` |
| Self-Directed Research | `research_engine.py` | Heartbeat: meta-Subsystem |
| Continuous Benchmarking | `benchmark.py` | Heartbeat: meta-Subsystem |

## Neue integrierte Architektur (September 2026)

### ASI Core Tools (5 Stück, in-process)
- `asi_status` (🧬) — voller ASI System-Status
- `asi_think` (🧠) — deep recursive reasoning
- `asi_learn` (📚) — internet learning cycle
- `asi_remember` (💭) — episodic memory recall via world model
- `asi_trigger` (⚡) — any capability: self_improve, predict, validate, meta_learn, knowledge_to_action, self_model, consolidate_memory, diary, session_outcome, swarm_route, create_skill, heartbeat

### ASI Heartbeat (zentraler Puls)
- 1 Cron-Job `asi-heartbeat-tick` (alle 5min)
- 10 Subsystem-Pulse: darwin, swarm, a2a, learning, senses, system, security, outreach, infra, meta
- Jedes Subsystem mit eigener Kadenz (5min bis 7d)
- Native Module bevorzugt, subprocess-Fallback
- 84 alte Cron-Jobs pausiert

### ASI CLI (`openamer asi`)
- `status` — voller Status aller 10 Subsysteme
- `think <question>` — Reasoning
- `learn [--topic]` — Internet-Lernen
- `remember <query> [-k N]` — Gedächtnis
- `trigger <capability> [--system] [--force]` — Capability
- `heartbeat [--tick] [--system] [--force]` — Herzschlag

### Native Subsystem-Module (`tools/asi/`)
- `self_model.py` — Self-Model (Direktimport aus scripts/training/self_model.py)
- `world_model.py` — World Model (Direktimport)
- `reasoning.py` — Recursive Reasoning (Direktimport)
- `prediction.py` — Prediction Validation (Direktimport)
- `improvement.py` — Self-Improvement (Direktimport)
- `a2a.py` — Agent-to-Agent Worker
- `darwin.py` — Darwin Engine Evolution
- `swarm.py` — Swarm Intelligence
- `heartbeat.py` — Zentraler Herzschlag (Subsystem-Registry, Kadenz, State)

### CLI (`openamer_cli/subcommands/asi.py`)
- 6 Subcommands: status, think, learn, remember, trigger, heartbeat
- Registriert in main.py: build_asi_parser, BUILTIN_SUBCOMMANDS

### Wichtige Dateien
- `tools/asi_core.py` — 5 Tool-Registrierungen
- `tools/asi/heartbeat.py` — Subsystem-Definitionen + Tick-Logik
- `scripts/asi_heartbeat.py` — Cron-Einstiegspunkt (no_agent)
- `toolsets.py` — asi-toolset + Core-Tools
- `openamer_cli/subcommands/asi.py` — CLI