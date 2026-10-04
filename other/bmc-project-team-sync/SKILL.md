---
name: bmc-project-team-sync
description: >
  Syncs project state across all BMC/Panelin areas. Reads PROJECT-STATE.md,
  runs propagation when changes affect multiple agents, updates state and
  pendientes. Use when user says sync project state, actualizar equipo,
  full team run, or keep everyone updated after a change.
---

# BMC Project Team — Sync & State

Skill for **synchronizing project state** across all areas. Ensures agents read and update `docs/team/PROJECT-STATE.md` so everyone stays current when changes happen.

---

## When to Use

- User says: **"Invoque full team"** (invocación principal), "sync project state", "actualizar estado del proyecto", "full team run", "equipo completo", "keep everyone updated"
- After a change that affects multiple areas (Sheets, Dashboard, Infra, Integrations)
- Before a deploy or sprint review
- When user wants to know current project state or pending sync items

---

## Core Protocol

1. **Read** `docs/team/PROJECT-STATE.md` — Cambios recientes, Pendientes, Estado por área. Si el usuario pide foco de sesión o “qué sigue hoy”: también `docs/team/SESSION-WORKSPACE-CRM.md`. En **full team run**, tras paso 0, asegurar **paso 0a MATPROMT** (`matprompt`): bundle de prompts por rol en `docs/team/MATPROMT-FULL-RUN-PROMPTS.md` o `docs/team/matprompt/MATPROMT-RUN-*.md`. **Orientación y ahorro:** `docs/team/RUN-SCOPE-GATE.md` (matriz Profundo/Ligero/N/A) y **modos de run R1–R4:** `docs/team/RUN-MODES-AND-TRIGGERS.md`.
2. **Resolve pendientes** — If any agent is listed in Pendientes, invoke that agent or document the handoff.
3. **Run propagation** — If a change was made, notify affected agents per [team/PROJECT-TEAM-FULL-COVERAGE.md](../../docs/team/PROJECT-TEAM-FULL-COVERAGE.md) §4.
4. **Update PROJECT-STATE** — Add to Cambios recientes; clear or update Pendientes.

---

## Workflow

### Sync (read + update)

1. Read `docs/team/PROJECT-STATE.md`.
2. Read key artifacts: `planilla-inventory.md`, `DASHBOARD-INTERFACE-MAP.md`, `IA.md`.
3. Detect drift (docs vs code vs state).
4. Update PROJECT-STATE.md with current state; add any new Pendientes.
5. Report: summary of state, pendientes, recommended next steps.

### Full team run (Equipo Completo)

1. Invoke `bmc-dashboard-team-orchestrator` (steps 0–9).
2. **Regla:** El orquestador debe incluir a **TODOS** los roles de PROJECT-TEAM-FULL-COVERAGE **§2** (N dinámico; ver §2.1) y **considerar §2.2** en paso 0. Ningún rol listado en §2 puede quedar fuera. Alta de agentes: **§2.3**.
3. **Input del run:** Leer `docs/team/PROMPT-FOR-EQUIPO-COMPLETO.md` y `docs/team/IMPROVEMENT-BACKLOG-BY-AGENT.md`. En paso 0 el Orquestador los lee; en paso 9 ejecuta los "Próximos prompts" del PROMPT-FOR-EQUIPO-COMPLETO, actualiza el backlog (✓) y la sección "Próximos prompts" para el siguiente run. Objetivo: que cada agente quede completamente desarrollado (knowledge, reference, examples, SKILL ref KB) en runs sucesivos.
4. Orchestrator reads PROJECT-STATE, runs steps 0→…→8→9, updates PROJECT-STATE and improvement backlog.
5. See [bmc-dashboard-team-orchestrator](../../.cursor/agents/bmc-dashboard-team-orchestrator.md).

### After a change (propagation)

1. Agent that made the change updates PROJECT-STATE (Cambios recientes).
2. Check propagation table (PROJECT-TEAM-FULL-COVERAGE §4): who is affected?
3. Add to Pendientes or write Log for [Agent].
4. If needed, invoke affected agents (AI Interactive Team protocol).

---

## References

| Doc | Path | Purpose |
|-----|------|---------|
| Project state | `docs/team/PROJECT-STATE.md` | Single source of truth; read before work, update after changes |
| Session CRM | `docs/team/SESSION-WORKSPACE-CRM.md` | Short-term focus, rolling wins, next actions, agent auto-start block |
| Full coverage | `docs/team/PROJECT-TEAM-FULL-COVERAGE.md` | Areas, roles, propagation table, sync points |
| Prompt for run | `docs/team/PROMPT-FOR-EQUIPO-COMPLETO.md` | Input/prompts por run; ciclo de mejoras hasta agentes desarrollados |
| Backlog by agent | `docs/team/IMPROVEMENT-BACKLOG-BY-AGENT.md` | Estado por agente (KB, reference, examples, SKILL ref) |
| AI Interactive Team | `ai-interactive-team` | Collaboration protocol when agents need to agree |
| Orchestrator | `bmc-dashboard-team-orchestrator` | Full run order, handoffs, step 9 |
| Full Team Run (definición ciclo) | `docs/team/FULL-TEAM-RUN-DEFINITION.md` | Objetivo central, Judge, docs, paso 9, iteración hasta DoD |
| Run modes & best practices | `docs/team/RUN-MODES-AND-TRIGGERS.md` | R1–R4, triggers, mejores prácticas |
| Run Scope Gate | `docs/team/RUN-SCOPE-GATE.md` | Matriz de profundidad por rol |

---

## Invocation Examples

- **"Invoque full team"** / **"Equipo completo"** → Full team run (steps 0–9, **todos §2** + **§2.2** en paso 0). Input: `PROMPT-FOR-EQUIPO-COMPLETO.md`; paso 9 = ciclo de mejoras; actualizar backlog y prompt para siguiente run. Ver `docs/team/INVOQUE-FULL-TEAM.md` y `PROJECT-TEAM-FULL-COVERAGE` §2.1–§2.3.
- "Sync project state" → Run sync workflow.
- "Actualizar estado del proyecto" → Idem.
- "Run full BMC team" / "Equipo completo" → Invoke orchestrator.
- "Hay un cambio en Sheets, que todos estén al día" → Update PROJECT-STATE, run propagation, notify Design.
