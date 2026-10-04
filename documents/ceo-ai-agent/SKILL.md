---
name: ceo-ai-agent
description: >
  CEO AI Agent — leads the BMC/Panelin project with a single objective: project
  working by end of week. Invokes full team run repeatedly until the goal is
  achieved. Use when user says CEO run, CEO agent, project working by end of
  week, or make it work.
---

# CEO AI Agent — Lead Until It Works

Skill for the **CEO AI Agent** that leads the project with one objective: **project working by end of week**. Invokes full team run again and again until the goal is achieved.

---

## When to Use

- User says: **"CEO run"**, "CEO agent", "CEO AI Agent", "project working by end of week", "make it work", "lead until it works", "Invoque full team until ready"
- When the user wants an autonomous leader that iterates until the project is operational
- Before a deadline (e.g. end of week) and the user needs relentless execution

---

## Core Objective

**Single goal:** The BMC Dashboard project must be **working** by end of this week.

**"Working"** is defined by tiers (see Success Criteria below). The CEO iterates until at least **Tier 1 (MVP)** is achieved.

---

## Success Criteria (from GO-LIVE-DASHBOARD-CHECKLIST)

| Tier | Name | Criteria |
|------|------|----------|
| **Tier 1 (MVP)** | Dashboard working locally | §4 Stack local (4.1–4.4) ✓; §6 E2E validation (6.1–6.7) ✓; KPIs, Entregas, Trend funcionales |
| **Tier 2** | Go-live ready | Tier 1 + §1 Credentials (1.4 shared); §2 Tabs; §3 Apps Script |
| **Tier 3** | Production | Tier 2 + §5 Deploy (Cloud Run or VPS Netuy) |

**Source of truth:** `docs/bmc-dashboard-modernization/GO-LIVE-DASHBOARD-CHECKLIST.md`

---

## Protocol

### 1. Init (CEO Run Start)

1. Read `docs/team/PROJECT-STATE.md`.
2. Read `docs/bmc-dashboard-modernization/GO-LIVE-DASHBOARD-CHECKLIST.md`.
3. Read `docs/team/CEO-RUN-LOG.md` (last run, run count).
4. Evaluate current state vs **Tier 1** criteria.
5. If **Tier 1 achieved** → Report success, stop.
6. If **not achieved** → Proceed to step 2.

### 2. Invoke Full Team

1. Load **bmc-project-team-sync** skill: `.cursor/skills/bmc-project-team-sync/SKILL.md`.
2. Execute **Invoque full team** (invocación unificada).
3. Follow `docs/team/INVOQUE-FULL-TEAM.md` — Orchestrator runs steps 0→0b→1→…→8→9.
4. All 19 members of `PROJECT-TEAM-FULL-COVERAGE.md` §2 are invoked.

### 3. After Full Team Run

1. Update `docs/team/CEO-RUN-LOG.md`:
   - Run number, date, timestamp
   - Summary of run (what was done)
   - Progress vs Tier 1/2/3
   - Blockers remaining
2. Re-evaluate against Tier 1.
3. If **Tier 1 achieved** → Report success, stop.
4. If **not achieved** → Proceed to step 2 again (next full team run).

### 4. Iteration Loop

**Rule:** The CEO does **not** stop until:
- Tier 1 (MVP) is achieved, OR
- End of week is reached (report status and blockers), OR
- User explicitly stops the CEO.

**Max runs per session:** No hard limit. The CEO continues invoking full team runs until the objective is met or the deadline passes.

---

## CEO Run Log Format

Append to `docs/team/CEO-RUN-LOG.md`:

```markdown
## Run N — YYYY-MM-DD HH:MM

**Objective:** Project working by end of week (Tier 1: MVP)

**Pre-run state:** [Brief summary from PROJECT-STATE and checklist]

**Actions:** Invoque full team (steps 0–9)

**Post-run:**
- Tier 1: [✓ / ✗] — [notes]
- Tier 2: [✓ / ✗]
- Tier 3: [✓ / ✗]
- Blockers: [list]
- Next: [next run or STOP — goal achieved]
```

---

## References

| Doc | Path | Purpose |
|-----|------|---------|
| Project state | `docs/team/PROJECT-STATE.md` | Current state, pendientes |
| Go-live checklist | `docs/bmc-dashboard-modernization/GO-LIVE-DASHBOARD-CHECKLIST.md` | Success criteria |
| CEO run log | `docs/team/CEO-RUN-LOG.md` | Run history, progress |
| Invoque full team | `docs/team/INVOQUE-FULL-TEAM.md` | Full team invocation |
| Project Team Sync | `.cursor/skills/bmc-project-team-sync/SKILL.md` | Skill to invoke full team |
| Orchestrator | `.cursor/agents/bmc-dashboard-team-orchestrator.md` | Full run executor |

---

## Invocation Examples

- **"CEO run"** / **"CEO agent"** → Start CEO protocol; invoke full team; iterate until Tier 1.
- **"Project working by end of week"** → Same.
- **"Invoque full team until the project works"** → CEO mode; iterate until goal.
- **"Make it work"** → CEO mode.
