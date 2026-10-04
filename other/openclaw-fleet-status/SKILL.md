---
name: openclaw-fleet-status
description: Check fleet operational status — tasks (pending / in-progress / completed today), agents (registered, running, idle, stuck), board state (Plane / Mission Control), recent activity, blockers. Read-only — produces a human-readable status report. Loads when the operator says "fleet status", "what's the fleet doing", "are agents running", "anything blocked".
allowed-tools: Read, Bash, Glob, Grep
effort: low
---

# openclaw-fleet-status

The read-only operational checkup skill for an OpenClaw fleet deployment. Produces a single concise report that answers: how many tasks are in flight, which agents are healthy, what's blocked, what's been done today. Distinct from `openclaw-health` (deeper system audit) and `openclaw-fleet-status` MCP tool (programmatic — this is the human-facing variant).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "fleet status", "what's the fleet doing", "are agents running", "anything blocked", "show me the board", "how busy are we".
- **Morning/EOD check-in**: operator opens a session and asks for an orientation snapshot before deciding what to work on.
- **Pre-deploy gate**: about to ship a change that affects fleet behavior; want to know current state before touching anything.

Do NOT load when:

- Deeper diagnostic needed (system health, hooks, integrations) — load `openclaw-health`.
- Operator wants to add a new agent — load `openclaw-add-agent`.
- Operator wants Mission Control re-connected — load `openclaw-configure-mc`.
- The status request is for a specific task ID — use the task-tracking skill (`aicp-ops-tasks`) or read the task file directly.

## Operations

This skill has 2 named operations. Execute in order. The first is the bulk of the work; the second is presentation.

### Operation 1: Gather signals from each fleet surface

**Trigger**: skill loaded.

**Process**:

1. **Fleet daemon / Make targets** — from the fleet project root (`openfleet/` or operator-named):
   ```bash
   make status   # if defined; otherwise:
   openclaw agents list           # registered agents + their workspaces
   openclaw agents status --all   # running / idle / stuck per agent
   ```
   Capture: agent count, per-agent state, last heartbeat timestamp.
2. **Mission Control board** — read board file or hit MC API:
   ```bash
   cat openfleet/board.json 2>/dev/null    # if file-based
   curl -s http://localhost:<mc-port>/api/board   # if MC API exposed
   ```
   Capture: tasks per column (todo / in-progress / done-today), oldest in-progress, recent activity timestamps.
3. **Plane integration** — if Plane is wired (per [docs/architecture/fleet-integration.md](../../../docs/architecture/fleet-integration.md)):
   ```bash
   curl -s -H "Authorization: Bearer $PLANE_API_KEY" \
     https://plane.<host>/api/v1/workspaces/<ws>/issues/?state=in_progress
   ```
   Capture: linked Plane issues open under each agent, age of the oldest.
4. **AICP backend health** — fleet agents call AICP for inference; if AICP is down, fleet is stuck:
   ```bash
   .venv/bin/aicp --check 2>&1 | head -20
   ```
   Capture: backend availability summary (the failover-chain line is the most informative).
5. **Recent work** — past 24h activity:
   ```bash
   find openfleet/agents/*/logs -name "*.log" -mtime -1 | head
   ```
   Capture: log freshness per agent. Stale logs (>2h on a "running" agent) is a stuck-agent signal.
6. **Identify blockers**: any task in_progress for >2h with no log activity, any agent registered but not running, any Plane issue waiting on operator review.

**Quality bar (Operation 1 done when)**:

- [ ] All 6 signal sources queried (or explicitly skipped with reason: "Plane not wired", etc.).
- [ ] Per-agent state captured (registered / running / idle / stuck).
- [ ] Board state captured (count per column).
- [ ] AICP backend health captured.
- [ ] Blocker list assembled with evidence for each (timestamp, task ID, log path).

### Operation 2: Format the status report

**Trigger**: Operation 1 signals gathered.

**Process**:

Produce a single concise report in this shape:

```
FLEET STATUS — <timestamp>

Agents (<N> registered):
  ● <name>       running   last activity 12 min ago    on T<NNN>
  ● <name>       idle      last activity  2 hr ago     queue empty
  ⚠ <name>       stuck     last activity  4 hr ago     on T<NNN> — no log progress

Board (Mission Control / Plane):
  todo:        <N> tasks  (oldest <age>)
  in-progress: <N> tasks  (oldest <age>)
  done-today:  <N> tasks

AICP backend:
  failover chain: local → k2_6_openrouter → openrouter → claude
  health:        <X/Y backends OK>

Recent (24h): <N> tasks completed across the fleet.

Blockers:
  ⚠ T<NNN> — in-progress 4h on <agent>, no log activity. Likely stuck.
  ⚠ T<NNN> — Plane issue waiting on operator review since <timestamp>.
  (none) if no blockers.

Suggested next: <single-line operator action OR "all clear">
```

Notes on the report:

- ≤30 lines total. Operator should grok the picture in <15s.
- Use ●/⚠ symbols for visual scan; avoid heavy formatting.
- Times are RELATIVE ("12 min ago"), not absolute timestamps — easier to read at a glance.
- Suggested next action is concrete and singular ("kick T042 — stuck for 4h" not "review your blockers").

**Quality bar (Operation 2 done when)**:

- [ ] Report ≤30 lines.
- [ ] Per-agent line includes state + last activity + current task (or "queue empty").
- [ ] Board breakdown by column with oldest age.
- [ ] AICP backend health line present.
- [ ] Blockers section either lists each with evidence OR states "(none)".
- [ ] Suggested-next-action is specific.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Counting registered agents as "running"

`openclaw agents list` returns 10 agents. Report says "10 agents running". But 7 of them are registered-and-stopped (the orchestrator never started them, or they crashed). Operator thinks fleet is healthy; actually 70% of capacity is dark.

**The rule**: state always comes from `openclaw agents status`, not from `agents list`. Distinguish "registered" from "running" in the report. Stuck agents (running but no log progress >2h) get the ⚠ marker — they look running but aren't doing work.

### Gotcha 2: Stale log = OK

An agent's last log entry is 4 hours old. Report flags it as "stuck". But the agent is correctly idle — its queue is empty, nothing to log about. False alarm wastes operator attention.

**The rule**: cross-reference last log activity with current task assignment. Log silence + assigned-task = stuck (real flag). Log silence + no assigned task = idle (correct, no flag). The Operation 1 step 5 must capture both.

### Gotcha 3: Reporting raw JSON

Pasting `openclaw agents list --json` output verbatim. Operator gets 200 lines of JSON, has to parse it themselves. Defeats the point of a status report.

**The rule**: Operation 2 produces a HUMAN-READABLE summary. Capture JSON for evidence in Operation 1; render to ≤30-line prose in Operation 2. If operator wants raw JSON, they ask for it — don't dump it preemptively.

### Gotcha 4: Plane / MC URL wrong, silent failure

Operator's deployment uses Plane on a different host or MC on a different port than the skill assumed. The curl returns 404 / connection refused. Skill silently treats "no tasks" as "no tasks", reports an empty board.

**The rule**: every external call has explicit failure handling. If the curl fails, the report says "Plane unreachable at <url> — board state unknown" — not silent zero. Operator must see the gap, not be misled by it.

### Gotcha 5: "No blockers" when AICP is degraded

Backend chain is `local → k2_6_openrouter → openrouter → claude`; LocalAI is down. Routes still work (failover to k2_6_openrouter), but every fleet task pays cloud-token cost it shouldn't. Report says "no blockers" because tasks are completing.

**The rule**: AICP backend degradation IS a blocker even if work proceeds. Report the failover state (which backend is currently the primary route) and flag if it's not the expected primary. Operator decides whether to surge.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill spans **AICP and OpenFleet projects**. AICP provides backend health visibility (`aicp --check`); OpenFleet runs the fleet that this skill audits. The report is the operator's morning glance + on-demand checkup tool.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| openclaw-health | Deeper system audit (hooks, integrations, daemons) | This skill is operational snapshot; openclaw-health is system audit |
| openclaw-add-agent | Add a new agent | This skill reports current state; add-agent changes it |
| openclaw-setup | Bootstrap OpenClaw | This skill reports an existing deployment; setup creates one |
| aicp-ops-runtime | Audit AICP itself in detail | This skill summarizes AICP backend in 1 line; ops-runtime drills in |
| pm-status-report | Multi-day project status with metrics | This skill is now-state snapshot; pm-status-report is reporting cadence |
