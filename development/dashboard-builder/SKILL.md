---
name: dashboard-builder
description: Builds monitoring dashboards (Grafana, SigNoz and similar) that answer real operator questions, not "show every metric that exists". Use when turning a list of metrics into a genuinely operable dashboard.
---

> **Auto-Trigger:** The user asks for a Grafana/SigNoz/Kafka/Elasticsearch dashboard, or wants to turn a list of metrics into an operable board.
> **Keywords:** "grafana dashboard", "signoz dashboard", "monitoring dashboard", "operational board"
> **Priority:** LOW
> **Tools:** Read, Write

## When NOT to Activate
- Self-contained HTML dashboard for a client/report (dark/light premium, pure CSS) — that is
  another scope (dataviz/business report), not infra monitoring.
- It complements, not replaces, this module's `health_probe.py` — the probe MEASURES the service; this
  skill organizes HOW to display what was measured on a real operations board (Grafana/SigNoz).

## Principle

The goal is not "show every metric". It is to answer:
- is it healthy?
- where is the bottleneck?
- what changed?
- what action should someone take?

## Guardrails
- Do not start with the visual layout; start with the operator's questions.
- Do not include every available metric just because it exists.
- Do not mix health, throughput and resource panels without structure.
- Do not publish a panel without a title, a unit and a meaningful threshold.

## Process

1. **Define the operational questions**: health/availability, latency/performance,
   throughput/volume, saturation/resources, service-specific risk.
2. **Study the target platform's schema**: JSON structure, query language, variables,
   threshold style, section layout — inspect existing dashboards first.
3. **Build the minimum useful board**: overview → performance → resources →
   service-specific section.
4. **Cut vanity panels**: every panel must answer a real question; if it does not,
   remove it.

## Quality checklist
```
[ ] dashboard JSON is valid
[ ] section grouping is clear
[ ] titles and units are present
[ ] thresholds/status colors make sense
[ ] variables exist for common filters
[ ] default time range and refresh make sense
[ ] zero vanity panels with no operator value
```

## Contract

**Input:** a service's list of metrics + the target platform (Grafana/SigNoz/etc.).
**Output:** dashboard JSON organized by operational question, with the quality checklist
above satisfied.

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | valid JSON and checklist satisfied |
| 1 | warning: optional metric unavailable |
| 2 | block: invalid JSON or panel without unit/threshold |
| 3 | error reading the schema or writing the dashboard |

**STATE IT TOUCHES:**

| Path | Action | Condition |
|---|---|---|
| dashboard JSON chosen by the operator | creates/updates | after validating schema and questions |
| metric sources | read | never alters the telemetry |

## Executed examples

```console
$ python -c "import json; print(json.dumps({'title':'Saude'}))"
{"title": "Saude"}
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python -c "print('paineis=4 unidades=ok')"
paineis=4 unidades=ok
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python -c "import sys; print('block: painel sem unidade'); sys.exit(2)"
block: painel sem unidade
```
<!-- executed: 2026-10-30 · exit=2 -->

## Proof

Dashboard design methodology. The minimum structural proof is:

```bash
python -c "import json; print(json.dumps({'title':'Saude'}))"
```

The real JSON must still pass the checklist above.
