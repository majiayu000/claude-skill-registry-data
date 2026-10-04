---
name: aicp-ops-metrics
description: Inspect AICP live metrics (LocalAI Prometheus + GPU + API call stats) or aggregated history (per-backend tokens/cost/latency) via the CLI surface. Replaces the deprecated aicp_metrics MCP tool per `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md`. Loads when the operator says "show metrics" / "GPU usage" / "API call stats" / "how many tokens" / "what's our cost" / "is LocalAI up" / "performance check".
allowed-tools: Bash, Read
effort: low
---

# aicp-ops-metrics

Inspect AICP performance and resource metrics via the `aicp` CLI. AICP exposes
two complementary metric surfaces: `--metrics` (LIVE LocalAI Prometheus +
GPU + API call stats) and `--stats` (AGGREGATED task history — tokens, cost,
per-backend breakdown). This skill teaches both via the CLI surface, NOT the
deprecated `aicp_metrics` MCP tool.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "show metrics", "what's the GPU usage", "how
  many tokens did we use", "what's our cost", "API call stats", "is LocalAI
  responsive", "performance check", "show me the dashboard summary"
- **Pre-tuning**: operator wants to compare current performance against a
  baseline before changing a profile or model
- **Post-deployment**: after switching profile/model, verify the new config
  is performing as expected
- **Cost concern**: token/cost rollup needed for a project review
- **Resource pressure**: GPU memory or LocalAI worker pool saturation
  suspected — live metrics confirm or rule it out

Do NOT load when:

- The concern is dashboard SETUP (load `infra-monitoring` — Prometheus +
  Grafana stack management)
- The concern is reliability metrics specifically (load `aicp-ops-dlq` for
  DLQ + `--health-report` for trend analysis)
- The concern is detailed task forensics (load `--history` / `--replay` via
  this skill's reference, or use `aicp-ops-dlq` for failed-task analysis)

## Operations

### Operation 1 — Live snapshot (LocalAI + GPU + API)

**When**: operator wants the CURRENT state of the inference stack.

**Process**:

1. Run `aicp --metrics`
2. Output sections:
   - LocalAI: URL, goroutines, memory_alloc/sys MiB, loaded models, backends
   - API Call Stats table: per-method count + total_ms + avg_ms (from `/metrics`)
   - GPU: name, VRAM used/total %, utilization %, temperature
3. The output's closing `NEXT:` recommends `--stats` for aggregates or
   `--health-report` for trend analysis
4. If LocalAI is unreachable, the output will say so and the NEXT line will
   recommend `docker compose up -d localai` — verify with `aicp --check` if
   needed

**Quality bar**: a healthy snapshot has GPU memory <70% (color-coded green),
goroutines stable across calls, and API avg_ms within historical norms.
Anomalies in any of these signal investigation.

### Operation 2 — Aggregated history (per-backend tokens/cost)

**When**: operator wants to see the overall trend, not the current instant.

**Process**:

1. Run `aicp --stats`
2. Output sections:
   - Summary table: tasks today/week/total, avg latency, error rate, prompt
     tokens, completion tokens, total tokens, est. cost USD
   - Per-backend breakdown table: tasks/avg_latency/error_rate/tokens/cost
     per backend (local, claude, openrouter, fleet)
3. The output's closing `NEXT:` recommends `--history <N>` for per-task
   detail or `--health-report` for trend deltas
4. If `total_tasks == 0`, the output says "No history yet" and the NEXT line
   recommends running a task first

**Quality bar**: per-backend breakdown should match the operator's expected
mission progress (per CLAUDE.md `## The Mission`: more tasks should be hitting
local than claude as Stage 3 progresses). If claude's task count exceeds
local, the routing is wrong (or the workload is genuinely too complex —
investigate).

### Operation 3 — Health trend analysis

**When**: operator wants delta-over-time, not point-in-time, on system health.

**Process**:

1. Run `aicp --health-report`
2. Output is a generated trend report comparing current state to a baseline
   (per `aicp/core/health_report.py`); save_report() also persists to disk
3. The output's closing `NEXT:` recommends `--check` for live status or
   `--dlq-status` if the report flagged failures
4. Trend deltas highlight degradation (e.g., latency creeping up, error rate
   trending higher) before they become incidents

**Quality bar**: a baseline-vs-current report should be the FIRST signal
operator sees during periodic health reviews; live `--metrics` is a deeper
follow-up if the trend report flags something.

### Operation 4 — Tune metric collection

**When**: operator wants to change Prometheus endpoint, scrape interval, or
metric retention.

**Process**:

1. Edit `config/default.yaml` `prometheus:` section (port, retention)
2. Restart AICP to pick up changes (`docker compose restart` for the LocalAI
   side; AICP CLI re-reads on each invocation)
3. For Grafana dashboards, refer to `infra-monitoring` skill — this skill
   teaches CONSUMING metrics, not authoring dashboards

**Quality bar**: changes to scrape interval must be coordinated with Grafana
dashboard refresh rates (mismatched rates produce visible gaps in graphs).

## Gotchas

- **Detection**: agent uses `aicp_metrics` MCP tool instead of `aicp --metrics` CLI.
  **Rule**: NEVER call `aicp_metrics` MCP tool — it's deprecated and will be removed.
  **Reasoning**: per audit decision, MCP overhead is paid per turn for a tool used
  during specific workflows; CLI+Skills loads this skill on demand only when the
  operator's request matches the trigger phrases above.

- **Detection**: agent confuses `--metrics` (live snapshot) with `--stats` (aggregated history).
  **Rule**: `--metrics` shows what's happening NOW; `--stats` shows what HAS HAPPENED.
  **Reasoning**: live snapshot answers "is it healthy right now?"; aggregated history
  answers "how have we performed?". Operator question phrasing usually disambiguates;
  if unclear, ask before running.

- **Detection**: agent treats GPU temperature as a primary KPI.
  **Rule**: GPU temp is informational; the primary GPU KPI is VRAM utilization %
  (which directly affects whether models can load) and GPU utilization % (which
  affects throughput).
  **Reasoning**: GPU temperature is bounded by the hardware's thermal throttling;
  unless thermal throttling is suspected, it's not actionable.

- **Detection**: agent reports raw cost numbers without context.
  **Rule**: cost is meaningful only against the mission target — CLAUDE.md `## The
  Mission` Stage 5 = "80%+ Claude token reduction". Always frame cost in terms of
  that target, not absolute USD.
  **Reasoning**: AICP's cost optimization is structural (route to local), not
  per-token frugality; an absolute USD number doesn't show whether the routing
  is doing its job.

- **Detection**: agent re-runs `--metrics` repeatedly in a tight loop.
  **Rule**: each call queries LocalAI's `/metrics` endpoint plus runs `nvidia-smi`;
  tight-loop calls add load to the inference stack and don't add information.
  Wait at least 5-10s between calls if monitoring transient behavior.
  **Reasoning**: live snapshots are point-in-time; multiple within seconds of each
  other observe noise, not signal.

## Reference exemplars

- `aicp/cli/main.py` `_run_metrics()` line 1386+ for live snapshot implementation
- `aicp/cli/main.py` `_run_stats()` line 1462+ for aggregated history implementation
- `aicp/core/metrics.py` for the underlying `aggregate()` and `offload_report()` helpers
- `aicp/core/health_report.py` for the trend analysis backend
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` — Category D rationale for this skill's existence
- `wiki/decisions/00_inbox/aicp-cli-mcp-outputs-adopt-gateway-output-contract.md` — explains the `NEXT:` lines this skill's commands produce

## Domain context

AICP exposes metrics at three levels: LocalAI's built-in `/metrics` (Prometheus
format on port 8090), AICP's own metrics exporter (`/metrics` on port 9101 per
CLAUDE.md `## Observability`), and aggregated task history (file-based, read by
`--stats`). The optional Grafana stack (`make monitoring-up`) provides the
dashboards on port 3000 (admin/aicp). This skill operates at the CLI summary
layer; the visualization layer is `infra-monitoring`'s scope.

## Related skills

| Skill | When to use |
|-------|-------------|
| `infra-monitoring` | When setting up Prometheus + Grafana stack or adding alerts |
| `aicp-ops-dlq` | When the metric concern is reliability/failure (DLQ growth specifically) |
| `quality-performance` | When the concern is performance regression analysis (uses these metrics as input) |
