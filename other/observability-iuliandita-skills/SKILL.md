---
name: observability
description: >
  Instrument, audit, and debug telemetry: metrics, traces, logs, alerts, SLOs, Prometheus, OpenTelemetry, Grafana.
license: MIT
compatibility: "Optional: prometheus, otelcol, grafana, promtool, amtool, jq"
metadata:
  source: iuliandita/skills
  date_added: "2026-06-14"
  effort: high
  argument_hint: "[service-or-stack]"
---

# Observability

Design and audit the signals a running system emits so failures are visible before users report
them. This skill builds the standing pipeline - instrumentation, metrics, traces, structured
logs, alert rules, SLOs, and dashboards-as-code - and audits a repo for the gaps that leave a
service blind.

**Target versions**: see `references/versions.md` (verified per the receipt date
in that file). Do not restate version numbers here.

## When to use

- Adding instrumentation to a service: metrics (Prometheus/OTLP), traces (OpenTelemetry), or
  structured logs
- Writing or reviewing alert rules, recording rules, and Alertmanager routing
- Defining SLOs and error budgets, and the multi-burn-rate alerts that back them
- Building dashboards as code (provisioned JSON, grafonnet/Grizzly)
- Designing the signal collection layer: OTel Collector pipelines, exporters, scrape config
- Auditing a repo for observability gaps: uninstrumented services, no SLOs, alert-fatigue
  patterns, cardinality risks, logs with no trace correlation

## When NOT to use

- Profiling and optimizing an identified application bottleneck - use **performance-debugging**.
- Broker acknowledgement, redelivery, dead-letter, or replay semantics - use **message-queues**.
- Checking whether a live cluster is healthy right now (point-in-time, read-only diagnostics) -
  use **kubernetes-health**
- Writing or reviewing Kubernetes manifests, Helm charts, or the Prometheus Operator CRDs as
  K8s objects - use **kubernetes**
- Wiring CI/CD pipelines (the skill defines what they should emit and gate on, not the pipeline
  itself) - use **ci-cd**
- Localizing an unknown-layer live failure once signals exist (consuming signals to find root
  cause) - use **debug-triage**
- Application security review or secret scanning in telemetry - use **security-audit**
- Database engine health, native metrics, query plans, or engine-specific tuning - use **databases**

---

## AI Self-Check

AI tools produce the same observability mistakes. Before returning any generated instrumentation,
rule, pipeline, or dashboard, verify:

- [ ] **Metric cardinality bounded**: no unbounded label values (user IDs, request paths with IDs,
  timestamps, full URLs) on metrics. High cardinality is the top cause of Prometheus OOM.
- [ ] **Rules validated**: PromQL/alert rules pass `promtool check rules`; routing passes
  `amtool config routes`. AI invents plausible-but-wrong PromQL functions and label matchers.
- [ ] **Alerts are actionable**: every alert has `for:`, severity, a runbook link, and fires on
  symptoms (SLO burn, user-facing error) not raw causes. No alert that a human cannot act on.
- [ ] **SLO math is real**: error budget = `1 - SLO`; burn-rate alerts use multi-window
  multi-burn-rate, not a single threshold. State the window and budget explicitly.
- [ ] **Trace context propagated**: W3C `traceparent` propagation is configured end to end;
  spans carry `service.name`. Logs include `trace_id`/`span_id` for correlation.
- [ ] **No secrets in telemetry**: no tokens, auth headers, PII, or full request bodies in span
  attributes, log fields, or metric labels.
- [ ] **Versions and signals real**: exporter names, OTLP receiver/exporter names, PromQL
  functions, and Grafana panel types verified against current docs - not assumed.
- [ ] **Sampling intentional**: trace sampling rate is stated and justified (head vs tail), not
  silently defaulted; 100% sampling on a hot path is flagged.
- [ ] Cross-cutting agent hygiene applied - see `references/agent-hygiene.md`

---

## Workflow

When building artifacts, copy this checklist and track progress:

```markdown
- [ ] Step 1: Questions and signal set named per service
- [ ] Step 2: Collection path chosen from the defaults table
- [ ] Step 3: Requested artifacts written for the detected stack
- [ ] Step 4: Every validator run and passing (fix and return to Step 3 on failure)
```

### Step 1: Identify the signals and the questions

Pin down what the system must answer before choosing tools. For each service: what does "broken"
look like to a user, and which signal proves it? Map to the **golden signals** (latency, traffic,
errors, saturation) or **RED** (rate, errors, duration) for request-driven services and **USE**
(utilization, saturation, errors) for resources. Pick the minimum signal set that answers those
questions - do not instrument everything because you can.

### Step 2: Choose the collection path

| Need | Default |
|---|---|
| Metrics | Prometheus scrape, or OTLP metrics through the OTel Collector to a Prometheus-compatible store |
| Traces | OpenTelemetry SDK -> OTLP -> Collector -> Tempo (or vendor backend) |
| Logs | Structured JSON -> OTel Collector -> Loki (Alloy where a Grafana agent is already deployed) |
| Unified pipeline | OpenTelemetry Collector as the single ingest/route/transform layer |

Prefer OTLP and the OTel Collector as the vendor-neutral seam: instrument once, re-route backends
in config. Use direct Prometheus scrape where pull and existing exporters already fit.

[Promtail reached EOL on March 2, 2026](https://grafana.com/docs/loki/latest/send-data/promtail/).
Migrate existing Promtail agents to Alloy or another supported client. Check the security
notes in `references/versions.md` when selecting Alloy or Grafana authentication settings.

### Step 3: Instrument and configure

When the user asks to build or configure observability artifacts, load
`references/runnable-examples.md` and return each requested concrete artifact: Collector
configuration, Prometheus alert or recording rule plus its rule-test fixture, and/or provisioned
dashboard JSON. Limit output to the requested signals and the detected stack.

- **Metrics**: use auto-instrumentation where it exists; add custom metrics only for
  domain-specific questions. Keep labels low-cardinality. Add recording rules for expensive
  queries that dashboards or alerts repeat.
- **Traces**: enable context propagation, set `service.name` and resource attributes, choose a
  sampling strategy (head sampling at the SDK, or tail sampling in the Collector for
  error/latency-biased retention).
- **Logs**: emit structured JSON, include `trace_id`/`span_id`, avoid logging what a metric
  already counts.
- **Alerts and SLOs**: write symptom-based alert rules, define SLOs with explicit windows, back
  them with multi-window multi-burn-rate alerts, route by severity in Alertmanager.
- **Dashboards**: keep them as code (provisioned JSON by default; grafonnet when generating many
  similar dashboards) so they are reviewable and reproducible, not click-built.

### Step 4: Validate

Run the matching validator for every artifact produced. On failure, fix the artifact, return to
Step 3, and rerun until it passes. Detect the tools first and record any missing one as skipped:
`for t in promtool amtool otelcol jq; do command -v "$t" >/dev/null || echo "missing: $t"; done`

- `promtool check config` / `promtool check rules` for Prometheus config and rules
- `promtool test rules` for rule-test fixtures against sample series
- `otelcol validate --config` for Collector pipelines
- `amtool config routes test` / `amtool check-config` for Alertmanager routing
- A JSON parser plus the target provisioning/import check (when available) for dashboard JSON
- Confirm a test signal traverses the full path (emit -> collect -> store -> query -> alert) on at
  least one service before declaring coverage
- Report the validator results: name each command you ran and its outcome, and list any check
  skipped because the tool or backend was unavailable. Never present an unrun check as passing.

---

## Signals reference

### Metrics

- Naming: `unit`-suffixed, base units (seconds, bytes), `_total` for counters. Follow Prometheus
  and OpenTelemetry semantic conventions; do not invent metric names where a convention exists.
- Cardinality is the budget. Series count = product of label-value sets. Keep label values bounded
  and finite. Per-entity detail (user, request, order, full path) belongs on a trace attribute or
  log field, never a metric label. Exemplars link a metric sample to a trace - enable them for
  latency histograms.
- Recording rules precompute heavy expressions; alerting rules fire on conditions. Keep them in
  version control and unit-test them with `promtool test rules`.

### Traces

- One trace = one request across services, stitched by propagated context. Without propagation you
  get disconnected spans, not traces.
- Sampling: head sampling is cheap and simple but blind to rare errors; tail sampling (in the
  Collector) keeps error/slow traces at the cost of buffering. State which and why.
- TraceQL queries Tempo; exemplars and `trace_id` in logs are the cross-signal jumps that make a
  trace findable from a metric spike or a log line.

### Logs

- Structured over free text: JSON fields are queryable (LogQL), prose is grep-only. Include
  `service`, `level`, `trace_id`, `span_id`, and a stable message key.
- Logs are the most expensive signal per byte of insight. If a metric can answer it, count it;
  reserve logs for the context a metric cannot carry.

### Alerts and SLOs

- An SLO is a target on an SLI (e.g. 99.9% of requests < 300ms over 30 days). Error budget is the
  allowed failure: `1 - SLO`. Alert on **budget burn rate**, not on every breach.
- The burn-rate alert threshold is `burn_rate * (1 - SLO)` compared against the error-*ratio* SLI -
  not the raw error rate against a bare multiplier (a common off-by-budget bug). Standard tiers for
  a 99.9% SLO: fast-burn 14.4x (1h + 5m windows, page), slow-burn 6x (6h + 30m, page), erosion 3x
  (24h + 2h, ticket). Both windows in a tier must breach together before the alert fires - express
  as an `and`: `ratio_rate1h > 14.4*(1-SLO) and ratio_rate5m > 14.4*(1-SLO)`.
- Multi-window multi-burn-rate alerting (fast-burn + slow-burn windows) catches both acute
  outages and slow erosion while suppressing flapping. A single static threshold does neither.
- Alert hygiene: page only on user-impacting symptoms with a runbook; everything else is a ticket
  or a dashboard. Alert fatigue is an outage you stop seeing.

### Dashboards as code

- Provision dashboards from version-controlled JSON or generate them with grafonnet/Grizzly. A
  click-built dashboard is an undiffable, unreviewable, un-restorable artifact.
- Committed-in-git is necessary but not sufficient: an *exported* JSON blob (regenerated on each
  export, never hand-edited) still drifts from the running dashboard and diffs unreadably. The
  source of truth is authored or generated config that flows file -> Grafana, not the reverse.

---

## Audit lens (Wave 3 in repo-audit)

When auditing a repo for observability, report findings on:

- **Coverage gaps**: services that emit no metrics/traces/logs; endpoints with no latency or error
  signal; background jobs with no success/failure metric.
- **No SLOs / no error budget**: alerting exists but is threshold-based with no SLO backing.
- **Alert anti-patterns**: cause-based alerts with no `for:`, no runbook, no severity; duplicate or
  flapping alerts; paging on non-actionable conditions.
- **Cardinality risk**: unbounded labels (IDs, paths, emails) on metrics; high-cardinality log
  fields used as metric labels.
- **Broken correlation**: logs without `trace_id`; traces without `service.name`; metrics without
  exemplars on key histograms.
- **Untested rules**: alert/recording rules with no `promtool test rules` coverage.
- **Drift risk**: dashboards stored as exported blobs nobody edits, or not in version control.

Report only what the repo files show. Do not assume a running backend exists; flag "signal defined
but no evidence it is collected" as a gap, not a pass.

---

## Output Contract

See `references/output-contract.md` for the full contract.

- **Skill name:** OBSERVABILITY
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **audit a repo for observability gaps** (the Wave 3 lens), apply the reporting size and evidence rules in `references/output-contract.md` and write the deliverable to `docs/local/audits/observability/<YYYY-MM-DD>-<slug>.md`. When invoked to **build instrumentation, rules, pipelines, or dashboards**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit mode).

## Related Skills

- **kubernetes-health** - point-in-time, read-only Kubernetes diagnostics ("is it healthy now").
  Observability builds the standing signal pipeline ("can we see it over time"). kubernetes-health
  reads signals live; observability defines and audits them.
- **kubernetes** - authors manifests, Helm, and Operator CRDs as K8s objects. Observability authors
  the instrumentation, rules, and SLO/alert config those objects carry, platform-agnostic.
- **debug-triage** - consumes signals to localize an unknown-layer live failure. Observability
  produces the signals it consumes: producer vs consumer.
- **ci-cd** - wires the pipeline. Observability defines what the pipeline should emit and gate on,
  not the pipeline itself.
- **security-audit** - reviews exploitable vulnerabilities and secret exposure. Observability flags
  secrets-in-telemetry as a gap but does not replace a security review.
- **databases** - owns engine-native metrics, health, query plans, and tuning. Observability owns
  cross-service collection, dashboards, alert routing, and SLOs built from those signals.

## Rules

1. **Cardinality is a hard budget.** Never put unbounded values (IDs, paths, emails, timestamps) in
   metric labels. Bounded label sets only.
2. **Validate before returning.** Run `promtool`, `otelcol validate`, and `amtool` on generated
   config and rules; do not ship unverified PromQL or routing.
3. **No secrets in telemetry.** No tokens, PII, auth headers, or full bodies in labels, span
   attributes, or log fields.
4. **Dashboards as code.** Provision from version control; never treat a click-built dashboard as
   the source of truth.
