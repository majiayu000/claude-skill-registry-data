---
name: infra-monitoring
description: Configure or audit AICP's monitoring stack — Prometheus (`:9090`) + Grafana (`:3000`) + 7 alert rules in `config/alerts.yaml` + AICP's own `:9101/metrics` exporter + LocalAI's built-in `:8090/metrics`. Loads when the operator says "set up monitoring" / "add an alert" / "what dashboards exist" / "audit observability" / "monitoring isn't telling me X".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# infra-monitoring

Configures or audits AICP's monitoring stack. AICP ships a complete
observability layer (Prometheus + Grafana behind a Docker compose profile +
7 baseline alerts + per-component metrics endpoints). This skill is for
working WITH the existing stack — adding/tuning alerts, reviewing dashboards,
verifying metrics flow, debugging missing signals — not for replacing the
stack (replacing would be `architecture-propose` scope).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "set up monitoring", "add an alert", "tune alert X", "what dashboards exist", "audit observability", "monitoring isn't telling me X", "where's the metric for Y"
- **Stage 4 reliability work**: AICP's reliability profile (circuit breaker + warmup + DLQ + reports) emits metrics this skill maintains the dashboards for
- **Post-incident retrospective**: an incident showed a missing signal — what alert SHOULD have fired? Add it.
- **Pre-fleet-rollout**: before AICP serves a fleet, confirm metrics flow + alerts are live + on-call routing works
- **Periodic audit**: quarterly review of which alerts fired, which were noise, which never fired (silent gaps)

Do NOT load when:

- The concern is correctness (load `feature-test` or `systematic-debugging`)
- The concern is a live incident (load `ops-incident` first; monitoring tuning is post-incident)
- Setting up tests + coverage (load `foundation-testing`)
- Setting up logging from scratch (load `foundation-logging` — different layer; logs feed metrics but they're separate skills)
- Replacing Prometheus/Grafana with a different stack (load `architecture-propose`)

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Verify the monitoring stack is running + reachable

**Trigger**: skill loaded; monitoring work requested.

**Process**:

1. Confirm the Docker compose monitoring profile is up:

   ```bash
   docker compose ps 2>&1 | grep -E 'prometheus|grafana' || echo "Monitoring stack not running"
   ```

   If down, start it: `make monitoring-up` (Prometheus on `:9090`, Grafana on `:3000` admin/aicp).

2. Verify each metrics endpoint is scrapable:

   ```bash
   curl -sf localhost:9101/metrics | head -5     # AICP's own metrics
   curl -sf localhost:8090/metrics | head -5     # LocalAI built-in metrics
   curl -sf localhost:9090/-/healthy             # Prometheus self
   curl -sf localhost:3000/api/health            # Grafana self
   ```

   Any failure: stop and report. Monitoring config is moot if endpoints are unreachable.

3. Confirm Prometheus is scraping all targets:

   ```bash
   curl -s localhost:9090/api/v1/targets | python3 -c "import json,sys; \
     d=json.load(sys.stdin); print('\n'.join(f\"{t['labels']['job']}: {t['health']}\" \
     for t in d['data']['activeTargets']))"
   ```

   Each target should be `up`. `down` targets mean Prometheus isn't getting metrics — common cause: Docker network mismatch or wrong port.

4. List existing dashboards in Grafana:

   ```bash
   curl -s -u admin:aicp localhost:3000/api/search?type=dash-db \
     | python3 -c "import json,sys; print('\n'.join(d['title'] for d in json.load(sys.stdin)))"
   ```

5. Read `config/alerts.yaml` to capture the 7 baseline alerts: stuck model, latency, errors, swaps, quality, cost, memory. Note their thresholds.

6. Write findings to `wiki/decisions/00_inbox/monitoring-audit-<date>.md` (type=reference). Include: stack health, target health, dashboard inventory, alert inventory.

**Quality bar (Operation 1 done when)**:

- [ ] All 4 monitoring components confirmed running (or started + verified)
- [ ] Each metrics endpoint reachable
- [ ] Prometheus targets all `up` (or down targets investigated)
- [ ] Dashboards listed
- [ ] 7 baseline alerts inventoried with thresholds
- [ ] Audit page created

### Operation 2: Identify the gap (what to add or tune)

**Trigger**: Operation 1 baseline established; operator stated the gap.

**Process**:

1. Frame the gap concretely. NOT "monitoring is incomplete" but ONE of:
   - **Missing metric**: a KPI exists in code (e.g., circuit breaker state transitions) but isn't exposed via `:9101/metrics`
   - **Missing alert**: a metric IS exposed but no alert fires when it crosses a threshold
   - **Noisy alert**: an alert fires too often (false positives degrade trust)
   - **Silent alert**: an alert never fires (threshold too lax OR the underlying metric isn't moving)
   - **Missing dashboard**: data exists but isn't visualized for human consumption
2. For each gap type, the FIX shape is different:
   - **Missing metric** → modify `aicp/core/prometheus.py` (the MetricsCollector) to expose the new counter/gauge/histogram. Then add a Prometheus scrape config if it lives at a new endpoint.
   - **Missing alert** → add to `config/alerts.yaml`. Define expression (PromQL), severity, threshold, alerting message.
   - **Noisy alert** → tune threshold. Capture the past N firings (`grep ALERT /var/log/...` or query Alertmanager) and pick a threshold above the noise floor.
   - **Silent alert** → either lower threshold OR fix the underlying metric (it may not be moving because the code path isn't exercised).
   - **Missing dashboard** → author a Grafana JSON or use the UI to build, then export.
3. For each fix, identify the BLAST RADIUS: who depends on this signal? Affects only solo dev? Affects fleet routing? Affects on-call routing? More dependents = more careful change.

**Quality bar (Operation 2 done when)**:

- [ ] Gap framed as ONE of the 5 categories above (not vague "improve monitoring")
- [ ] Fix shape identified per the category
- [ ] Blast radius assessed
- [ ] Operator approved the fix scope before authoring

### Operation 3: Author the change (alert / metric / dashboard)

**Trigger**: Operation 2 plan approved.

**Process**:

1. **For alert changes** — edit `config/alerts.yaml`. Each alert has the structure (per existing 7 examples):

   ```yaml
   - alert: <PascalCase name>
     expr: <PromQL expression>
     for: <duration before firing, e.g., 5m>
     labels:
       severity: warning  # or critical
     annotations:
       summary: <one-line>
       description: <multi-line context with mitigation hint>
   ```

   New alerts should follow the existing 7's pattern. Don't invent new label schemas.

2. **For metric changes** — edit `aicp/core/prometheus.py`. Add the new counter/gauge/histogram to `MetricsCollector`. Wire in the call site (the code path that should increment). Per [feature-implement Gotcha 1](../feature-implement/SKILL.md): NO ORPHAN. New metric must be incremented by some real code path.

3. **For dashboard changes** — Grafana UI to build, then `Settings → JSON Model → Save to file`. Commit the JSON to `monitoring/dashboards/` (create if missing). Provision via Grafana's `provisioning/dashboards/*.yaml`.

4. After EACH change:
   - Re-run Operation 1 verifications (endpoints reachable, targets up)
   - For new metric: confirm it appears at `:9101/metrics` and Prometheus has scraped it (`curl 'localhost:9090/api/v1/query?query=<metric>'`)
   - For new alert: confirm the alert appears in Prometheus's rules (`curl 'localhost:9090/api/v1/rules'`)
   - For new dashboard: load it in Grafana, verify panels render data
5. Run AICP's full test suite to ensure metric wiring didn't break anything: `pytest tests/ -x --tb=short`.
6. Commit with conventional format: `feat(monitoring): add <X>` or `chore(monitoring): tune <X>`.

**Quality bar (Operation 3 done when)**:

- [ ] Change applied per the category-specific shape
- [ ] Verification ran AFTER the change (not just trusted)
- [ ] No orphan metric (every new metric has a code path that emits it)
- [ ] AICP test suite passes (no test regression)
- [ ] Committed in conventional format

### Operation 4: Document + close out

**Trigger**: Operation 3 change landed.

**Process**:

1. Update the audit page from Operation 1 with the change applied. Include the alert/metric/dashboard name and brief description.
2. If the gap surfaced a SYSTEMIC pattern (e.g., "all backend errors lacked granular metric breakdowns"), contribute back as a lesson: `gateway contribute --type lesson`.
3. If the alert needs runbook entries (when it fires, what does on-call do?), update or create the runbook in `docs/runbooks/` with: trigger condition, immediate mitigation, root-cause investigation steps, escalation path.
4. Run `tools/lint.py` on any wiki content authored.
5. Inform operator: change live, runbook updated, audit page captured.

**Quality bar (Operation 4 done when)**:

- [ ] Audit page reflects the change
- [ ] Runbook updated if the alert needs operational response
- [ ] Lesson contributed if systemic
- [ ] Wiki lint passes

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Adding metrics without alerts (silent capability)

The temptation: add a metric, ship it, "we can alert on it later." NO — a metric without an alert is data that nobody sees until they go looking. Per Quality Standards principle: if it's worth measuring, it's worth alerting on (with appropriate threshold).

**Detection**: did Operation 3 add a metric without a corresponding alert added in the same batch?

**The rule**: every NEW metric ships with at least an "informational" alert (low severity, high threshold) so it appears in the alert inventory. Tuning the threshold later is fine; having no alert is silent.

### Gotcha 2: Alert thresholds set to "never fire" (alert theater)

The temptation: set the threshold so high it never fires (e.g., latency > 60s). It's "always green" so it looks healthy. NO — an alert that never fires means you've added work for the alert system but no signal for the operator. Per Quality Standards anti-pattern: this is "compliance theater for alerts."

**Detection**: review the alert's PromQL expression — would it fire under normal degraded conditions?

**The rule**: thresholds calibrated to actual data. Use the past N days of metrics to find the p95 baseline; set the threshold at p99 + headroom. Never-fires thresholds get flagged in periodic alert review.

### Gotcha 3: Noisy alerts that get muted (worse than no alert)

A noisy alert (fires constantly) gets muted by on-call. Eventually a REAL incident triggers it; nobody sees because the alert was muted. Per Quality Standards principle: false positives kill trust.

**Detection**: check Alertmanager (or Prometheus alert UI) for muted/silenced alerts. Each mute is a sign the alert is broken.

**The rule**: noisy alerts get FIXED, not muted. Either tune the threshold or fix the underlying flaky behavior. Mutes are short-term (during an incident); persistent mutes are technical debt.

### Gotcha 4: Dashboards without the queries (Grafana lock-in)

The temptation: build dashboards in the Grafana UI, save them. The dashboard JSON lives only in Grafana's database — if Grafana restarts cleanly, dashboards are gone. Per CLAUDE.md "IaC only" rule: dashboards should be reproducible via `make setup`.

**Detection**: are dashboards in version control? `ls monitoring/dashboards/*.json 2>/dev/null` should match Grafana's dashboard list.

**The rule**: dashboards are IaC. JSON in `monitoring/dashboards/`, provisioned via Grafana's provisioning config. UI is for AUTHORING; the file is the source of truth.

### Gotcha 5: Auditing alerts vs auditing actual firings

The temptation: review `config/alerts.yaml` and report "we have 7 alerts, all reasonable." But the question wasn't "do alerts exist?" — it was "do alerts work?" Reviewing the YAML doesn't reveal which alerts fired vs which were silent.

**Detection**: did Operation 1 step 5 capture only the alert DEFINITIONS, or also their FIRING HISTORY (last N days)?

**The rule**: alert audits include firing history. An alert that hasn't fired in 90 days is suspicious (silent gap or threshold too lax). Use Prometheus query history or Alertmanager's alert log.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact:

- **Real alerts file**: see [config/alerts.yaml](../../../config/alerts.yaml) — the 7 baseline alerts that this skill maintains/extends
- **Real metrics exporter**: see [aicp/core/prometheus.py](../../../aicp/core/prometheus.py) — the MetricsCollector that emits AICP-specific metrics
- **Monitoring audit page shape**: same as sibling quality audits (coverage / lint / debt / performance) — reference page with per-component findings + recommendations

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). AICP-specific monitoring stack: Prometheus `:9090`, Grafana `:3000` (admin/aicp), AICP `:9101/metrics`, LocalAI `:8090/metrics`. Stack starts/stops via `make monitoring-up` / `make monitoring-down`.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| infra-security | security audit | Different observability dimension (security events vs operational metrics) |
| quality-performance | perf benchmarks | Bench is point-in-time; this skill is continuous monitoring |
| ops-incident | live incident response | Reactive; this skill is proactive (alerts trigger ops-incident) |
| ops-deploy | deployment with checks | Deploy uses health checks (this skill ensures those checks have signals) |
| foundation-logging | structured logging setup | Logs are different from metrics; complementary |
| infra-search | search infrastructure | Different infrastructure category |
