---
name: health-check
description: Probes a config-driven list of services (HTTP or local command) and writes a JSON cache that another tool (e.g. the statusline) can read without touching the network — never on the hot path itself, it only generates the cache.
---

> **Auto-Trigger:** When setting up service health monitoring for a project, or when the user asks "check whether the services are up", "health check", "health probe".
> **Keywords:** "health check", "service health", "probe", "health probe", "services up", "service status", "monitoring", "uptime"
> **Priority:** MEDIUM
> **Tools:** Bash, Read

## When NOT to Activate
- Checking ONE single, one-off endpoint — use `curl`/`urllib` directly, without the overhead of configuring `health.probes`.
- When the "health" to check is about DATA (a populated table, a job that ran), not about a SERVICE being up — service health ≠ data health; this script only proves the process responds, not that the data inside it is correct.

## Contract

**INPUT:** `health.probes` (list of `{name, type: http|cmd, target}`) from `operator-profile.yaml`.

**OUTPUT:** JSON cache at `paths.health_cache` (default `.claude/health-cache.json`) + printed summary.

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | always — the connector never breaks the caller's flow, even with services DOWN |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `operator-profile.yaml` (`health.probes`, `paths.health_cache`) | Reads | probe config |
| HTTP endpoint / local command | Reads (read-only) | the actual probe |
| `paths.health_cache` | Writes | cache that another tool (e.g. `statusline.py`) reads without network |

## Process
1. **Declare the probes** in the profile: `type: http` (GET via `urllib`, never `curl`/`wget` — deny-list) or `type: cmd` (shell command from the profile, trusted).
2. **Run the probe** — on demand, on `SessionStart`, or via cron:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/health_probe.py
   ```
3. **Consumers** (e.g. `statusline.py`, `health` segment) read ONLY the generated cache — they never call the network on the hot path. The `health` segment shows the per-service detail (`api:OK db:DOWN`) up to 6 services; above that it degrades to the aggregate (`⚕up/tot`).

## Executed examples

```console
$ python scripts/health_probe.py
⚕ 1/2 UP (DOWN: servico-down)
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python scripts/health_probe.py --json
{
  "ts": "2026-10-30 11:05 BRT",
  "health": {
    "services_online": 1,
    "services_total": 2
  },
  "services": {
    "servico-ok": {
      "online": true,
      "type": "cmd",
      "target": "python -c \"import sys; sys.exit(0)\""
    },
    "servico-down": {
      "online": false,
      "type": "cmd",
      "target": "python -c \"import sys; sys.exit(1)\""
    }
  }
}
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python scripts/health_probe.py --quiet
```
(no output — `--quiet` suppresses the summary even with services DOWN, useful for a cron that only wants the cache)
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python statusline/statusline.py --statusline
servico-ok:OK servico-down:DOWN
```
(the same cache above, read by the statusline's `health` segment — per-service detail, the module's acceptance criterion)
<!-- executed: 2026-10-30 · exit=0 -->

## Proof

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/health_probe.py --self-test
python ${CLAUDE_PLUGIN_ROOT}/statusline/statusline.py --self-test
```
