---
name: openclaw-health
description: Comprehensive health check of the OpenClaw ecosystem — gateway, Mission Control backend + frontend, Docker services, registered agents, recent error logs. Deeper than `openclaw-fleet-status` (operational snapshot); this skill audits the SYSTEM health to find what's broken vs what's just idle. Loads when the operator says "is OpenClaw healthy", "audit the fleet stack", "something feels off", "why isn't X working".
allowed-tools: Read, Bash, Glob, Grep
effort: low
---

# openclaw-health

The system-audit skill for an OpenClaw deployment. Distinct from `openclaw-fleet-status` (snapshot of fleet operational state — who's running what) — this skill is the deeper "is the stack itself healthy" check covering gateway, Mission Control, Docker, agent connectivity, and recent errors.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "is OpenClaw healthy", "audit the fleet stack", "something feels off", "why isn't X working", "is the system OK".
- **Diagnostic context**: a fleet operation is failing or behaving strangely; need to determine if the stack itself is the issue.
- **Periodic check**: weekly/before-major-change health audit.
- **After a known disruption**: post-Docker restart, post-update, post-power-loss — verify everything came back.

Do NOT load when:

- Operator wants the operational snapshot (who's working on what) — load `openclaw-fleet-status`.
- A specific incident needs response — load `ops-incident` (incident response with diagnosis + fix + report).
- Adding a new agent — load `openclaw-add-agent`.
- Bootstrapping OpenClaw — load `openclaw-setup`.

## Operations

This skill has 2 named operations: gather then report. Designed to be cheap (≤30 seconds) so it's run-frequently.

### Operation 1: Probe each system surface

**Trigger**: skill loaded.

**Process**:

1. **OpenClaw gateway** — the orchestrator daemon:
   ```bash
   openclaw status            # gateway up/down, version, uptime
   openclaw agents list       # registered agents
   ```
   Capture: gateway state, version, agent count.
2. **Mission Control backend** — the API serving the board:
   ```bash
   curl -sS -m 5 http://localhost:8000/health 2>&1 | head -3
   ```
   Capture: HTTP status, response body. 200 = healthy; connection refused = down; 5xx = up but degraded.
3. **Mission Control frontend** — the UI:
   ```bash
   curl -sS -m 5 -o /dev/null -w "%{http_code}\n" http://localhost:3000
   ```
   Capture: HTTP status. 200 = serving; non-200 = check.
4. **Docker services** — supporting infrastructure (DB, MC, etc.):
   ```bash
   docker compose ps --format json 2>/dev/null
   ```
   Capture per-service: state (running / restarting / exited), health (healthy / unhealthy / starting / no healthcheck), uptime.
5. **Recent errors** — last 100 log lines from each component, filter for ERROR / FATAL:
   ```bash
   tail -100 /var/log/openclaw/gateway.log 2>/dev/null | grep -iE "error|fatal|exception" | tail -10
   tail -100 openfleet/mission-control/backend.log 2>/dev/null | grep -iE "error|fatal" | tail -10
   for log in openfleet/agents/*/logs/*.log; do
     tail -100 "$log" 2>/dev/null | grep -iE "error|fatal" | tail -3
   done
   ```
   Capture: error count per component over the recent window.
6. **AICP backend** (fleet agents depend on AICP for inference):
   ```bash
   .venv/bin/aicp --check 2>&1 | grep -E "^\s*\[(OK|FAIL)\]"
   ```
   Capture: per-backend health line.

**Quality bar (Operation 1 done when)**:

- [ ] All 6 surfaces probed.
- [ ] Each probe has a 5-second timeout (so down-services don't hang the audit).
- [ ] Probe failures captured as data (not skipped) — "MC backend connection refused" is information.
- [ ] Recent error counts captured per component.

### Operation 2: Format the health report

**Trigger**: Operation 1 probes done.

**Process**:

Produce a single concise report:

```
OPENCLAW HEALTH — <timestamp>

Gateway:           ● up    (vN.N.N, uptime <duration>, <N> agents registered)
Mission Control:
  backend (:8000): ● healthy (200 OK)
  frontend (:3000): ● serving (200 OK)
Docker services:
  ● mc-backend     running (healthy, uptime 4d)
  ● mc-frontend    running (healthy, uptime 4d)
  ⚠ postgres      restarting (3 restarts in 1h — investigate)
AICP backend chain:
  [OK]  local
  [OK]  k2_6_openrouter
  [OK]  openrouter
  [OK]  claude

Recent errors (last 100 log lines per component):
  gateway:    0
  mc-backend: 2  (DB connection timeout x2 around <ts>)
  agents:     1  (architect-1: skill load failed at <ts>)

Verdict: ⚠ DEGRADED — postgres flapping is upstream of the mc-backend errors.
Suggested next: `docker compose logs postgres --tail 50` to find the cause.
```

Notes:

- ●/⚠/✗ symbols for visual scan: ● = healthy, ⚠ = degraded but functional, ✗ = down.
- Verdict line is single-word: HEALTHY / DEGRADED / DOWN.
- "Suggested next" is concrete and actionable — names the EXACT command or skill to invoke for the highest-leverage fix.
- ≤25 lines total; operator should grok the system state in <15s.

**Quality bar (Operation 2 done when)**:

- [ ] Report ≤25 lines.
- [ ] Each surface has explicit state symbol (●/⚠/✗) — never absent.
- [ ] Verdict assigned (HEALTHY / DEGRADED / DOWN) consistent with findings.
- [ ] Suggested next action is a literal command or skill name, not a vague suggestion.
- [ ] Recent error counts are real numbers, not "some" or "many".

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Optimistic timeout

Probe runs without `-m <seconds>`. A wedged service makes the probe hang for 30+ seconds; operator types "skip" or aborts before the audit completes. Audit is useless because it never finishes.

**The rule**: every external call has an explicit short timeout (5s for HTTP probes, 10s for orchestrator commands). Audit must complete in ≤30s total. If a probe times out, that IS the data: report "no response within 5s — likely wedged."

### Gotcha 2: "0 errors" from missing log file

Skill greps a log path that doesn't exist on this deployment. Returns 0 errors. Report says "0 errors in mc-backend log". Operator thinks all is well — but the actual mc-backend log is at a different path the skill never checked.

**The rule**: distinguish "log file exists, 0 errors" from "log file missing". For each log path, check `[ -f <path> ]` before tailing. If missing, report "(log path not found at <path> — likely different in this deployment)" rather than "0 errors".

### Gotcha 3: Healthy verdict when services restart-loop

`docker compose ps` shows postgres as "restarting" right now. Skill captures the snapshot but doesn't realize this is the 3rd restart in an hour. Verdict says HEALTHY because at the moment-of-probe everything else was up.

**The rule**: probe restart count, not just current state. `docker inspect <container> | jq .RestartCount` (or equivalent). If restart count >2 in the last hour, that's DEGRADED even if currently up. Bake this into the verdict logic.

### Gotcha 4: No correlation across error sources

mc-backend log has "DB connection timeout" errors. postgres is restarting. The two are obviously linked. Skill reports them as two separate issues; operator chases the symptom (mc-backend) instead of the cause (postgres).

**The rule**: in the verdict line, when you see >1 issue, attempt one-line causal correlation. "postgres flapping is upstream of mc-backend errors" beats "mc-backend has 2 errors" + "postgres restarting" reported separately. The "Suggested next" action targets the upstream cause.

### Gotcha 5: Skipping the AICP backend check

The skill's tradition mentions "OpenClaw + Mission Control + agents" but skips AICP. Fleet agents call AICP for inference; if AICP is down or its primary backend is degraded, fleet agents fail or pay surge cost. Audit reports HEALTHY because OpenClaw itself is fine.

**The rule**: AICP backend chain is part of the OpenClaw health surface. Probe `aicp --check` and include the per-backend OK/FAIL line. If primary backend is down (failover engaged), report DEGRADED even if OpenClaw is up — fleet is paying cloud surge.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill spans **AICP and OpenFleet projects**. AICP provides the inference health probe (`aicp --check`); OpenFleet runs the OpenClaw gateway, Mission Control, and the agents.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| openclaw-fleet-status | Operational snapshot — who's working on what | This skill is system audit; fleet-status is fleet operations |
| ops-incident | Active incident response with diagnosis + fix + report | Incident response is reactive + restorative; this skill is proactive audit |
| aicp-ops-runtime | Drill into AICP runtime specifically | This skill summarizes AICP in 1 section; ops-runtime drills in |
| infra-monitoring | Configure monitoring system | This skill uses existing monitoring; infra-monitoring authors it |
| openclaw-setup | Bootstrap OpenClaw | This skill audits an existing deployment; setup creates one |
