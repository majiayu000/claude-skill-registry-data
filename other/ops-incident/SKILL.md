---
name: ops-incident
description: Active incident response — restore service first, identify root cause second, file the incident report third. For AICP this means triaging which backend is degraded (LocalAI / OpenRouter / Claude), checking circuit breakers + DLQ + ntfy alerts, applying the smallest restoration (profile switch / failover engagement / circuit reset / rollback), then writing `docs/incidents/INC-<YYYY-MM-DD>-<slug>.md`. Distinct from `openclaw-health` (proactive audit) and `ops-rollback` (revert mechanic — one tool an incident might use). Loads when the operator says "production is down", "AICP is broken", "incident", "something just broke", "fleet stopped", "prod alert fired".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# ops-incident

The reactive-and-restorative skill for active incidents on AICP or sister fleet projects. Strict 3-phase ordering: restore (stop the bleeding), diagnose (understand the cause), report (capture the lesson). Distinct from `openclaw-health` and `aicp-ops-runtime` (proactive audits — they look for problems; this skill responds to one) and from `ops-rollback` (a mechanism this skill may invoke, not the skill itself).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "incident", "outage", "production is down", "AICP is broken", "fleet stopped", "alert fired", "something is on fire", "this is breaking right now".
- **Fresh failure signal**: ntfy alert just landed, Grafana panel red, `aicp --check` returning FAIL, `docker compose ps` shows Restarting, smoke test in `ops-deploy` Operation 3 just failed.
- **User-impacting symptom**: operator reports an action is failing now (CLI hangs, LLM returns errors, agent stuck, DLQ growing fast).

Do NOT load when:

- The system is healthy but the operator wants verification — load `openclaw-health` (full audit) or `aicp-ops-runtime` (`aicp --check`).
- A specific known-good rollback is what's needed — load `ops-rollback` directly.
- DLQ has grown but no service is failing — load `aicp-ops-dlq`.
- It's a slow degradation over weeks (memory leak suspicion, drift) — load `quality-performance`.
- Post-incident retrospective only (incident is over) — write the report directly using this skill's Operation 3 template, no live response needed.

## Operations

This skill has 3 named operations. Execute in strict order — no diagnosing while production is bleeding, no reporting while the cause is still uncertain.

### Operation 1: Restore service (stop the bleeding)

**Trigger**: skill loaded; system is in a degraded or failing state.

**Process**:

1. Snapshot the failure state IMMEDIATELY — evidence preservation must precede mutation:
   ```bash
   ts=$(date -u +%FT%TZ); mkdir -p /tmp/incident-$ts
   docker compose ps > /tmp/incident-$ts/compose-ps.txt
   docker compose logs --tail 200 > /tmp/incident-$ts/logs.txt 2>&1
   .venv/bin/aicp --check > /tmp/incident-$ts/aicp-check.txt 2>&1
   .venv/bin/aicp --dlq-status > /tmp/incident-$ts/dlq.txt 2>&1
   git log --oneline -10 > /tmp/incident-$ts/recent-commits.txt
   ```
2. Classify the failure scope (which determines minimum-disruption fix):
   - **Single backend** (e.g., LocalAI down, others fine) → engage failover, no full restart.
   - **Single service** (e.g., Mission Control crashed, gateway fine) → restart only that service.
   - **Stack-wide** (compose orchestration, network, shared volume) → full restart.
   - **Code-bug** (regression in last deploy) → roll back via `ops-rollback`.
3. Apply the SMALLEST restoration that returns service:
   ```bash
   # Backend degraded — failover should already be engaging; verify:
   .venv/bin/aicp --route-show
   # Single service crashed — restart just it:
   docker compose restart <service>
   # Circuit breaker tripped — reset only if breaker state caused the outage:
   .venv/bin/aicp --circuit-reset <backend>
   # Active deploy is the cause — roll back:
   git checkout "$(cat /tmp/predeploy-sha-<env>.txt)"; docker compose up -d
   ```
4. Verify restoration — DO NOT proceed to Operation 2 until this is green:
   ```bash
   .venv/bin/aicp --check 2>&1 | tail -10
   .venv/bin/aicp --backend local --prompt "say ok" 2>&1 | tail -3
   docker compose ps | grep -v "running (healthy)"   # should be empty
   ```
5. Tell the operator: service restored at `<timestamp>`, mechanism was `<failover|restart|rollback|breaker-reset>`. State that you are now moving to diagnosis.

**Quality bar (Operation 1 done when)**:

- [ ] Snapshot directory `/tmp/incident-<ts>/` exists with logs + ps + check + dlq + recent commits.
- [ ] Failure scope classified (backend / service / stack / code-bug).
- [ ] Smallest restoration applied — full restart only chosen when narrower options ruled out.
- [ ] `aicp --check` returns OK and golden-path inference responds.
- [ ] Restoration mechanism + timestamp explicitly stated to operator.

### Operation 2: Diagnose root cause

**Trigger**: Operation 1 restored service. System is not bleeding anymore — diagnosis is now safe and required.

**Process**:

1. Build the timeline from the snapshot:
   ```bash
   ts=<incident-timestamp-from-op1>
   grep -iE "error|fatal|exception|traceback" /tmp/incident-$ts/logs.txt | head -30
   ```
   Sort by timestamp; identify FIRST error (often the cause; later errors are cascade).
2. Correlate with recent changes:
   ```bash
   git log --since="6 hours ago" --oneline   # what changed in the window before failure
   git diff <last-known-good-sha> HEAD -- config/   # config drift
   ```
3. Check upstream/dependency state at incident time:
   - Cloud provider status pages (OpenRouter, Anthropic, Ollama Cloud) if a cloud backend was implicated.
   - LocalAI's `:8090/metrics` and AICP's `:9101/metrics` for resource pressure (VRAM, RAM, CPU).
   - DLQ pattern: are the failed tasks all from one backend? all of one shape (long context, tool-use)?
4. Form the root-cause hypothesis. Write it as ONE sentence: "X happened because Y, triggered by Z." If you can't write that sentence, diagnosis is incomplete — keep digging.
5. Validate the hypothesis BEFORE writing the report:
   - Reproduce in a safe env if possible (`--dry-run`, isolated profile, smaller scale).
   - Or: identify the change in code/config that, if reverted, would have prevented this. The diff IS the validation.
6. Decide the durable fix vs the emergency fix Operation 1 applied:
   - Was Op1's fix the right permanent solution? (Often: no — Op1 stopped bleeding; Op2 finds the actual fix.)
   - Author the durable fix: code patch, config change, alerting rule addition, runbook update.

**Quality bar (Operation 2 done when)**:

- [ ] Timeline reconstructed: first error timestamp identified, ordered relative to deploys/config changes.
- [ ] Recent-changes window correlated (git log + config diff).
- [ ] Upstream state checked OR explicitly noted "no cloud backend involved".
- [ ] Root-cause hypothesis written as a single "X because Y, triggered by Z" sentence.
- [ ] Hypothesis validated (repro OR identified diff that, if reverted, prevents recurrence).
- [ ] Durable fix differentiated from Op1 emergency fix — both stated.

### Operation 3: File the incident report

**Trigger**: Operation 2 root cause identified and validated.

**Process**:

1. Author `docs/incidents/INC-<YYYY-MM-DD>-<slug>.md` with this structure:
   ```markdown
   # INC-<YYYY-MM-DD>-<slug>

   - **Severity**: <P0 / P1 / P2 / P3>  (P0=full outage, P1=major degradation, P2=minor, P3=cosmetic)
   - **Detected**: <timestamp> via <ntfy / aicp --check / operator / Grafana>
   - **Restored**: <timestamp> (duration <X> minutes)
   - **Operator**: <who responded>

   ## Timeline (UTC)
   - HH:MM — <first symptom>
   - HH:MM — <next event>
   - HH:MM — restoration applied
   - HH:MM — service confirmed back

   ## Root cause
   <one paragraph: X because Y, triggered by Z, validated by W>

   ## Restoration applied (Op1)
   <what was done to stop the bleeding>

   ## Durable fix (Op2)
   <what was/will be done to prevent recurrence — code change, config, alerting>
   - Status: <applied / pending PR / scheduled for next deploy>

   ## Prevention
   <what alerting/check/test would have caught this earlier>

   ## Lessons
   <what we learned that wasn't obvious before>
   ```
2. Cross-link the incident:
   - Add an entry to `docs/DEPLOY-LOG.md` if a deploy was implicated.
   - File a TODO/issue for the durable fix if not yet applied.
   - If the lesson generalizes, contribute to the brain via `python3 -m tools.gateway contribute --type lesson --title "..."`.
3. Notify operator surfaces:
   - ntfy summary (single line: `INC restored sev=Pn dur=Nm cause=<short>`).
   - Update Mission Control / standing-orders if fleet was affected.
4. Close the incident: confirm with operator the report is filed and the durable fix is tracked.

**Quality bar (Operation 3 done when)**:

- [ ] `docs/incidents/INC-*.md` file exists with all 7 sections populated (no TBDs).
- [ ] Severity assigned (P0/P1/P2/P3) consistent with impact.
- [ ] Timeline has at least 4 entries: detected / first-mitigation / restored / closed.
- [ ] Durable fix status is one of: applied / PR pending / scheduled — not "TODO".
- [ ] Brain contribution made IF the lesson is non-AICP-specific (or explicitly noted "AICP-internal only").
- [ ] Operator confirmed report filed.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Mutating before snapshotting

Service is failing; operator is anxious; skill jumps to `docker compose restart` to fix it. The restart succeeds — but logs that lived only in the running container are now gone, the failed-state `docker inspect` output is unrecoverable, and the root cause is now a guessing game. Restoration succeeded; diagnosis is dead.

**The rule**: Operation 1 step 1 is non-negotiable. Snapshot to `/tmp/incident-<ts>/` BEFORE any mutation. The snapshot is cheap (a few seconds); the lost evidence is expensive (next incident is the same one).

### Gotcha 2: Diagnosing while still bleeding

Service is degraded; skill starts grep-ing logs to find root cause. Twenty minutes later, root cause is identified — but customers/the operator have been waiting twenty minutes for service. Op2 is a tax on everyone while Op1 isn't done.

**The rule**: Operation 1 ends when service is restored. Operation 2 begins ONLY after that. If restoration is hard, prefer the brute-force option (full restart, full rollback) — losing a small amount of state is cheaper than minutes of outage. Diagnose during the calm, not the storm.

### Gotcha 3: Cascade error mistaken for root cause

Logs show 50 lines of "ConnectionRefused" errors. Skill identifies cause as "network issue" and proposes firewall fix. But the FIRST error (15 minutes earlier) was a single OOM in the LocalAI container; the network errors are downstream symptoms because the container died. Fixing the firewall does nothing.

**The rule**: in Operation 2 step 1, sort log entries by timestamp and identify the FIRST error in the failure window. Most subsequent errors are cascade. Root cause is at the start of the cascade, not the loudest part of it.

### Gotcha 4: "Restored" by coincidence

Service comes back during the window where you're investigating — perhaps a transient cloud-provider issue resolved itself, perhaps a slow-starting container finished booting. Skill claims credit for the restoration; root cause analysis is then chasing an irrelevant change. Next incident is a repeat with no learning.

**The rule**: Operation 2 step 5 validates the hypothesis. If the only evidence is "I did X, and a minute later it worked", that's correlation, not causation. Validation means: reproducing the failure, or identifying the diff that would have prevented it. If you can't validate, mark the report's root cause as "transient — not reproduced" and add a monitoring task to catch the next instance.

### Gotcha 5: No durable fix, just a closed ticket

Incident is resolved by Op1 (restart). Op2 identifies the cause. Op3 files the report — but Status: TODO. Two months later, the same incident happens. The report is a tombstone, not a fix.

**The rule**: Op3 quality bar requires durable-fix status to be `applied / PR pending / scheduled` — never "TODO" or "to-investigate". If the fix is not yet applied, an issue/task is filed and linked from the report. If the fix is "monitoring this and seeing if it recurs", that's a legitimate plan but it must be EXPLICIT (the alert rule that will detect recurrence is named in the report).

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP incidents tend to fall into a small set of patterns: backend-degraded (LocalAI OOM, OpenRouter rate-limit, Anthropic 5xx), circuit-breaker-tripped-incorrectly, DLQ-growing-fast (failure cascade), profile-misconfiguration-after-deploy, GPU eviction thrash on Tier 0 hardware. The mitigation path nearly always touches one of: `aicp --route-show`, `aicp --circuit-reset`, `aicp --dlq-retry`, `make profile-use`, `docker compose restart <service>`. Severity calibration: a P0 for AICP is "operator workflow blocked" (CLI fails for >10 min) since AICP serves a single operator + fleet; what would be P3 in a SaaS product can be P1 here because the blast radius is the operator's whole day.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| openclaw-health | Proactive system audit | Audit looks for problems; incident responds to one |
| aicp-ops-runtime | `aicp --check` + bench + observe | Diagnostic toolbelt; this skill orchestrates them under incident pressure |
| ops-rollback | Revert a deploy | One mechanism Op1 may invoke; this skill is the broader incident process |
| ops-deploy | Forward deploy with gates | Forward action; this skill is reactive recovery |
| aicp-ops-dlq | DLQ growing or retry needed | DLQ ops is one signal; incident handles the broader failure mode |
| incident-cycle | From incident to fix to prevention (compound) | Compound workflow; this skill is the single-incident response |
