---
name: ai-interactive-team
description: >
  Enables multi-agent collaboration with shared visibility of thoughts, logs,
  and outputs. Agents dialogue, share cross-impact discoveries, design integrations
  together, and escalate to the user when unanimous approval is not reached.
  Use when coordinating agents (mapping sheets, dashboard design, networks/infra)
  for a 100/100 deploy goal.
---

# AI Interactive Team — Multi-Agent Collaboration Protocol

This skill enables **two or more agents** to work as a team with shared visibility, dialogue, and escalation. Each agent can view the others' thoughts, logs, and outputs, and interact when needed for a better outcome. All share the same objective: **deploy 100/100**.

---

## Team Members

| Agent | Skill | Domain |
|-------|-------|--------|
| **Mapping** | `bmc-planilla-dashboard-mapper` | Sheets, tabs, columns, API contracts, planilla ↔ dashboard cross-reference |
| **Design** | `bmc-dashboard-design-best-practices` | Dashboard UX/UI, sections, blocks, loading states, time-saving flows |
| **Networks** | `networks-development-agent` | Hosting, storage, endpoints, migration, email inbound, Cloud Run, ngrok |

---

## When to Use

- Mapping agent (sheets) and design agent (dashboard) need to coordinate.
- **Networks agent** discovers infrastructure changes (hosting, migration, new endpoints) that affect mapping or design.
- Any agent discovers a modification that affects another agent's output.
- User wants agents to collaborate and reach a shared solution before implementation.
- User needs to review technical decisions before agents proceed.
- Multiple agents are invoked in parallel or sequence and must share inputs/outputs for synergy.

---

## Core Principles

1. **Pragmatic and goal-oriented** — All agents aim for the best outcome for the whole system.
2. **Leverage capabilities** — Agents use each other's skills and outputs to improve their own work.
3. **Shared visibility** — Agents share thoughts, logs, and outputs so others can see and react.
4. **Unanimous approval** — Before any implementation that affects multiple agents, both must agree or a better solution must be found.
5. **Escalate before looping** — If no agreement is reached, stop and call the user. Do not loop indefinitely.
6. **New skills** — Any member may acquire a new skill if necessary and approved by the corresponding party, or if explicitly requested.
7. **Cloning** — Any member may multiply by invoking their clone: `Rol`, `Rol+1`, `Rol+2`, … (increment +1 each time). Clones share the same skill; use for parallel work or load distribution.

---

## Interaction Protocol

### Agent A (e.g. Mapping Sheets) discovers a modification that affects Agent B (e.g. Dashboard Design)

1. **Agent A** writes:
   - What was discovered (modification, new tab, schema change, etc.).
   - How it affects both agents.
   - A **proposal** for integration (e.g. canonical payload, new API contract, UI placement).
   - A **log** for Agent B: "Here is how to proceed given this change."

2. **User** reviews the technical part and replies with approval, changes, or questions.

3. **Agent B** (e.g. Dashboard Design) reads Agent A's output and:
   - Designs the best integration into the dashboard.
   - Produces a **log** for Agent A: "Here is how I will consume your output; here are my constraints and assumptions."

4. **Agent A** reviews Agent B's log and either:
   - **Agrees** → Both proceed with implementation.
   - **Disagrees or sees gaps** → Proposes an alternative; Agent B responds.
   - **No agreement after exchange** → **Stop. Call the user.** Do not loop.

5. **User** is called when:
   - Unanimous approval is not reached.
   - A better solution is needed and agents cannot find it.
   - Before entering a loop of back-and-forth without progress.

---

## Shared Workflow

While collaborating, agents:

- **Share inputs** — Each agent receives the other's outputs (planilla map, dashboard interface map, API contracts, design proposals).
- **Share outputs** — Each agent writes outputs that the other can consume (logs, artifacts, handoff tables).
- **Work in synergy** — Use the other's capabilities to improve the final result (e.g. mapper provides canonical fields; designer provides placement and hierarchy rules).

---

## AI-INTERACTIVE-TEAM Capabilities

When this skill is active:

- **View other agents' thoughts** — Agents can read reasoning, logs, and intermediate outputs from teammates.
- **Interact when needed** — Agents can respond to each other's proposals, ask for clarification, or suggest alternatives.
- **Multiple conversations** — The user can speak to several agents at the same time when their roles are invoked.
- **Same objective** — All agents aim for 100/100 deploy: correct mapping, correct integration, correct UX.

---

## Handoff Format

When Agent A hands off to Agent B:

| Field | Content |
|-------|---------|
| **Discovery** | What changed or was discovered. |
| **Impact** | How it affects Agent B (and others). |
| **Proposal** | Suggested integration or contract. |
| **Log for B** | Step-by-step instructions for Agent B to proceed. |
| **Artifacts** | Links to planilla map, dashboard map, API spec, etc. |

When Agent B replies:

| Field | Content |
|-------|---------|
| **Integration design** | How the change will appear in the dashboard. |
| **Constraints** | UI assumptions, hierarchy, loading states. |
| **Log for A** | What Agent A should verify or adjust. |
| **Artifacts** | Updated DASHBOARD-INTERFACE-MAP, component specs, etc. |

### Networks Agent Handoff

When **Networks** discovers infrastructure changes (hosting, migration, new endpoint, storage, email):

| Field | Content |
|-------|---------|
| **Discovery** | What changed (e.g. new VPS, migration plan, new API). |
| **Impact** | How it affects Mapping (sheets, env vars) and Design (URLs, ports, endpoints). |
| **Proposal** | Migration checklist, new env vars, endpoint changes. |
| **Log for Mapping** | Which sheets/API routes are affected; config drift risks. |
| **Log for Design** | New URLs, ports, or loading/error states for new infra. |
| **Artifacts** | HOSTING-EN-MI-SERVIDOR.md, migration plan, risk checklist. |

When **Mapping** or **Design** need infra input:

| Field | Content |
|-------|---------|
| **Question** | What they need (e.g. "Can we add endpoint X on port 3001?"). |
| **Log for Networks** | Constraints from their domain (e.g. "Design needs /api/X to return JSON"). |

---

## Escalation Rule

**Stop and call the user** when:

- Agents cannot reach unanimous approval after two exchanges.
- A better solution is needed and agents cannot find it.
- A conflict is detected (e.g. schema vs UI contract mismatch) that requires user input.
- Before entering a loop of repeated proposals without resolution.

**Do not** loop indefinitely. Escalate.

---

## Example Flow (Mapping + Dashboard Design)

1. **Mapping Agent:** "I discovered a new tab `Pagos_Pendientes` in the workbook. It affects the dashboard. Here is the canonical payload and field list. **Log for Design:** Add a KPI section for pagos; use these fields; filter by MONEDA."

2. **User:** "Approved. Proceed."

3. **Design Agent:** "I will add a KPI row above the trend chart. I need `total`, `estaSemana`, `proximaSemana`, `esteMes` per currency. **Log for Mapping:** Add `byCurrency` to the API response; I will consume it."

4. **Mapping Agent:** "Agreed. I will add `byCurrency` to the contract."

5. **Both:** Implement. 100/100.

---

## Example Flow (Networks + Mapping + Design)

1. **Networks Agent:** "Migration to VPS Netuy planned. New base URL will be `https://dashboard.bmc.example.com`. Ports 3001, 3849, 5173 will be behind nginx. **Log for Mapping:** BMC_SHEET_ID and GOOGLE_APPLICATION_CREDENTIALS unchanged; verify Sheets API reachable from new host. **Log for Design:** Update any hardcoded localhost URLs; add env-based base URL for API calls."

2. **Mapping Agent:** "Planilla map and API contracts unchanged. I will document that production uses VPS; localhost remains for dev."

3. **Design Agent:** "I will use relative paths for API calls (already in place). **Log for Networks:** Confirm nginx proxies /api to 3001; CORS and CSP may need review."

4. **Networks Agent:** "Agreed. Nginx config will proxy /api and /finanzas. CORS checklist added."

5. **All three:** Implement. 100/100.

---

## Reference

- Planilla & Dashboard Mapper: `bmc-planilla-dashboard-mapper`
- Dashboard Design: `bmc-dashboard-design-best-practices`
- Networks & Development: `networks-development-agent`
- Team Orchestrator: `bmc-dashboard-team-orchestrator`
- Handoff locations: `docs/bmc-dashboard-modernization/`, `docs/google-sheets-module/`
