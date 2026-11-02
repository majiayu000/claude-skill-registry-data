---
name: container-benchmark
description: Run the container startup benchmark to measure and validate the full agent-wake → dashboard-visible flow. Use before and after optimization work to catch regressions and compare timings.
---

# Container Startup Benchmark

Runs a real end-to-end benchmark of the container startup + dashboard loading flow through the running dev server. Creates a test agent, seeds a dashboard, starts/stops the container across multiple cycles, and validates every step of the pipeline.

## When to use

- Before and after any changes to the container startup path (`base-container-client.ts`, `container-manager.ts`, `dashboard-manager.ts`)
- When investigating container startup latency reports
- As a regression gate before shipping container-related changes

## Prerequisites

1. Dev server running (`npm run dev` or `npm run dev:electron`)
2. Container runtime (Docker/Lima/Podman) available and running
3. Agent container image built (`superagent-container:latest`)

## Inputs

`$ARGUMENTS` — parse for:
- **`--runs N`** — number of start/stop cycles (default: 3)
- **`--skip-session`** — skip the LLM session/message test (saves API cost, faster)
- **`--base-url URL`** — dev server URL (default: `http://localhost:47891`)
- **`--timeout MS`** — max wait per phase in ms (default: 120000)
- **`--json-out PATH`** — write machine-readable results JSON to file
- **`--keep-agent`** — don't delete the test agent after run (for debugging)

If `$ARGUMENTS` is empty, use defaults: 3 runs, include session test, localhost:47891.

## Procedure

### 1. Verify the dev server is reachable

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:47891/api/agents
```

If not running, tell the user to start it and stop.

### 2. Run the benchmark

The benchmark script lives at `.claude/skills/container-benchmark/benchmark-container-startup.ts`. Run it with:

```bash
npx tsx .claude/skills/container-benchmark/benchmark-container-startup.ts $ARGUMENTS
```

For piping output (recommended — preserves results if terminal scrolls):

```bash
npx tsx .claude/skills/container-benchmark/benchmark-container-startup.ts $ARGUMENTS 2>&1 | tee /tmp/bench-results.txt
```

### 3. Interpret results

The script outputs:
- **Per-run timings** — container start, dashboard start, dashboard first-serve, total start→HTML, session create, message processing, stop
- **Per-run validations** — 8 checks without session, 10 with session (see table below)
- **Summary statistics** — p50, p95, mean, min, max across all successful runs
- **JSON results** — full machine-readable output for diffing

### Validations performed (regression checks)

| # | Check | What it proves |
|---|-------|----------------|
| 1 | POST /start returns 200, status='running' | Container starts |
| 2 | Artifacts poll finds dashboard status='running' | Dashboard boots inside container |
| 3 | Dashboard proxy returns 200 with HTML | Proxy routing works |
| 4 | HTML contains `id="bench-marker"` | Dashboard content is correct |
| 5 | HTML contains SpeechRecognition + window.Anthropic polyfills | Polyfill injection works |
| 6 | SSE received `agent_status_changed` with status='running' | Real-time events work |
| 7 | POST /stop returns status='stopped' | Container stops cleanly |
| 8 | SSE received `agent_status_changed` with status='stopped' | Stop event fires |
| 9 | POST /sessions returns session ID (if not `--skip-session`) | Session creation works |
| 10 | Messages poll finds assistant response (if not `--skip-session`) | Agent processes messages end-to-end |

### 4. Report to the user

Show the summary table and highlight:
- Whether all validations passed
- Key timing metrics (total start→HTML p50 is the headline number)
- Any failures or anomalies

If comparing before/after, note that **cross-session timing comparisons are unreliable** due to environmental factors (Docker state, machine load). The validations are the reliable regression signal. For timing, look for large (>200ms) consistent shifts, not small fluctuations.

## Script architecture

The script (`.claude/skills/container-benchmark/benchmark-container-startup.ts`) is self-contained with no project source imports. It:

1. Discovers the server's data directory via `GET /api/settings`
2. Creates a test agent via `POST /api/agents`
3. Seeds a minimal Bun dashboard directly on the filesystem
4. Connects an SSE listener to `/api/notifications/stream`
5. For each cycle: verifies agent is stopped → starts → polls dashboard → fetches HTML → optionally creates session → stops
6. Cleans up (stop + delete agent)
7. Exits 0 if all validations pass, 1 if any fail

## Key files

- `.claude/skills/container-benchmark/benchmark-container-startup.ts` — the benchmark script
- `src/shared/lib/container/base-container-client.ts` — health check polling, container start
- `src/shared/lib/container/container-manager.ts` — ensureRunning, doStartContainer
- `agent-container/src/dashboard-manager.ts` — scanAndStartAll, bun install, dashboard boot
- `src/renderer/hooks/use-artifacts.ts` — frontend dashboard status polling
- `src/api/routes/agents.ts` — all API endpoints exercised by the benchmark
