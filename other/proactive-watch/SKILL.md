---
skill_id: proactive-watch
name: Proactive Watch — Drift Detection
description: "Detect silent drift between what the docs claim and what the repo actually contains — drift check, health check, audit, watch, sync check, /mxm-watch. Runs 13 drift classes and reports gaps before they ship."
version: 1.0.0
category: operational
office: coo
lead_agent: planner
triggers:
  - "session start (light phase)"
  - "/mxm-watch command"
  - "drift check"
  - "health check"
  - "audit"
  - "watch"
  - "sync check"
collaborates_with:
  - executive-router
  - security-analyst     # for compliance-drift
  - enterprise-architect # for contract-drift
  - planner              # for operational drift classes
  - implementer          # for code / dep drift
references:
  framework: composable-skills/frameworks/proactive-watch.md
  adr: documents/ADRs/ADR-002-executable-contracts.md
  config_template: config/watch-profile.TEMPLATE.yml
  schemas: .claude/skills/proactive-watch/schemas/
confidence_default: 🟢 HIGH
---

# Proactive Watch — Drift Detection Skill

> Continuous enforcement of the Executable Contracts meta-principle (ADR-002).
> Catches drift across 10 universal drift classes on every session start.

---

## Skill Purpose

Detect silent drift between declared reality (docs, manifests, inventories, ADRs) and actual reality (filesystem, git state, dependencies, hooks). Report findings with severity, triage routing, and evidence — so drift is fixed while it's cheap, not months later when it's entrenched.

---

## Activation

| Trigger | Behavior |
|---|---|
| **SessionStart hook** | Runs `watch --light` silently; appends summary block to session banner |
| **`/mxm-watch`** | Runs LIGHT manually; shows full report |
| **`/mxm-watch --full`** | Reserved for v1.0.0 — FULL phase with agent triage |
| **`mxm-context.watch_run` MCP tool** | Programmatic invocation from other skills / agents |

---

## Dispatch Path

```
TASK arrives with "check drift" / "audit" / "session start"
  │
  ▼
Maxim skill .claude/skills/proactive-watch/ matches
  │
  ▼
Load config/watch-profile.yml (per project)
  │
  ▼
For each ENABLED checker:
  ├── Run checker (bash watch.sh <checker> OR pwsh watch.ps1 <checker>)
  ├── Capture JSONL report line per drift
  └── On checker error: apply fail-mode policy (hybrid)
  │
  ▼
Aggregate report → .mxm-skills/watch-report.jsonl
Emit summary block to stderr / chat (LIGHT phase)
Route critical drift to triaged office (FULL phase, v1.0.0)
```

---

## Behavioral Framing

Apply Fogg + COM-B + Present-Bias principles when surfacing drift:

1. **Fogg B=MAT** — run at SessionStart when developer is engaged (max M × A)
2. **COM-B** — provide clear Evidence + Action path, not just "something's wrong"
3. **Present-Bias Mitigation** — frame every finding in terms of "fix now vs cost later"

Output language:
- ✗ Bad: "Drift detected"
- ✓ Good: "Declared 90 agents, filesystem has 91 — add to documents/ledgers/AGENT_SKILL_INVENTORY.md §1 (60s fix)"

---

## Proactive Loops

The skill is itself a proactive loop. Additionally:

- After fixing an inventory drift, proactively scan for recurring-pattern opportunities — if 3+ inventory drifts happened in one month, recommend a stronger pre-commit gate
- After fixing a compliance drift, auto-route to CSO for root-cause analysis
- After fixing a contract drift, check whether the underlying ADR needs superseding

---

## Confidence Tagging

| Scenario | Tag |
|---|---|
| LIGHT run with all checkers passing | 🟢 HIGH |
| LIGHT run with drift detected, remediation suggested | 🟢 HIGH |
| FULL run (v1.0.0+) with agent triage complete | 🟢 HIGH |
| Any checker errored (fail-open tier) | 🟡 MEDIUM — report incomplete |
| Compliance or contract checker errored (fail-closed) | 🔴 LOW — action required |
| `super_user.enabled = true` suppresses advice (not drift detection) | 🔵 SUPER USER |

---

## Output Format

### LIGHT summary (SessionStart banner)

```
Maxim WATCH (light)
  Drift detected : 3
  ⚠ inventory-drift: declared 90 agents, filesystem has 91 (severity 3)
  ⚠ version-drift: README badge v1.0.0, registry v1.0.0 (severity 3)
  ⚠ stale-handoff: handoff.md 9 days old (severity 2)
  Checker errors : 0
  Report         : .mxm-skills/watch-report.jsonl
```

### JSONL report (machine-readable)

```jsonl
{"ts":"2026-04-18T12:00Z","phase":"light","project":"maxim","drift_class":"inventory-drift","severity":3,"declared":90,"actual":91,"evidence":"agents/MXM/ceo/new-agent.md","triage":"coo","action":"review-queue"}
```

---

## Checker Execution Model

The skill ships two unified drivers that implement all 11 checkers (Classes 1–10 from v1.0.0; Class 11 surface-claims-drift added v1.0.1 with companion tool `bootstrap/sync-counts.{sh,ps1}` for mechanical propagation):
- `watch.sh` — bash (Linux/macOS/Git-Bash)
- `watch.ps1` — PowerShell 7+ (Windows primary, cross-platform)

Each driver accepts one argument: the checker name. Running `watch.sh all` runs every enabled checker and aggregates output.

```bash
# Run single checker
.claude/skills/proactive-watch/watch.sh inventory-drift

# Run all enabled checkers (LIGHT phase default)
.claude/skills/proactive-watch/watch.sh all
```

---

## Files in this Skill

| File | Purpose |
|---|---|
| `SKILL.md` | this file — skill contract |
| `watch.sh` | unified bash driver implementing all 11 checkers |
| `watch.ps1` | unified PowerShell driver implementing all 11 checkers |
| `schemas/watch-profile.schema.json` | validates per-project `config/watch-profile.yml` |
| `schemas/watch-report.schema.json` | validates JSONL output lines |

---

## Self-Adoption (maxim repo)

This repo ships its own `config/watch-profile.yml` in v1.0.0 — the framework's first consumer is itself. Any drift that sneaks into this repo across multi-session work should surface at the next `/mxm-watch` or SessionStart.

---

## Extending

Projects may add custom checkers by:
1. Writing a script at `.claude/skills/proactive-watch/custom/<name>.sh` (+ `.ps1`)
2. Registering it in `config/watch-profile.yml` under `custom_checkers:`
3. Emitting JSONL lines matching `schemas/watch-report.schema.json`

Custom checkers run after standard checkers.

---

## Related

- Framework doc: `composable-skills/frameworks/proactive-watch.md`
- ADR-002: `documents/ADRs/ADR-002-executable-contracts.md`
- Command: `.claude/commands/mxm-watch.md`
- Hook: `.claude/hooks/session-start.{sh,ps1}` calls `watch --light`
- MCP: `mxm-context` tools `watch_run`, `watch_report`, `watch_configure` (v1.0.0+)

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
