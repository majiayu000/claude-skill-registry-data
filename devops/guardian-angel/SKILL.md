---
name: guardian-angel
description: "Hermes Agent & Gateway process watchdog — monitors health, detects errors, handles restart sequences with thresholds, auto-recovers, escalates on crash loops."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [guardian, watchdog, monitoring, health, gateway, agent, uptime, recovery]
    triggers:
      - guardian angel
      - gateway watchdog
      - agent monitor
      - process health
      - restart watchdog
      - crash loop
      - uptime monitor
      - hermes health
    related_skills:
      - cron-watchdog
      - infrastructure-self-healing-pulse
      - hermes-nightly-watchdog
      - pim-ingestion-pipeline
---

# Guardian Angel — Hermes Agent & Gateway Watchdog

A dedicated watchdog that monitors the Hermes Agent process and Hermes Gateway, ensuring they stay healthy and signalling when things go wrong. Unlike the Cron Watchdog (which monitors cron job schedules) or the Self-Healing Pulse (which monitors infrastructure), the Guardian Angel focuses **specifically on the Hermes Agent and Gateway process health**.

## Architecture

```
                ┌──────────────────────────┐
                │   Guardian Angel (GA)     │
                │   Runs every 5 min via    │
                │   cron                    │
                └──────┬───────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ Gateway  │  │ Agent    │  │ Error    │
   │ Process  │  │ API      │  │ Logs     │
   │ Check    │  │ Check    │  │ Scan     │
   └──────────┘  └──────────┘  └──────────┘
          │             │             │
          ▼             ▼             ▼
   ┌──────────────────────────────────────┐
   │       Threshold & Decision Engine    │
   │  • 3 consecutive failures = action   │
   │  • 3 restarts/hour = crash loop      │
   │  • 10 errors/hour = error burst      │
   │  • Restart grace period: 5 min       │
   └──────────────┬───────────────────────┘
                  │
        ┌─────────┴────────────┐
        ▼                      ▼
  ┌──────────┐          ┌──────────┐
  │ Auto-    │          │Escalate  │
  │ Recovery │          │To the operator │
  │ (levels) │          │(Discord) │
  └──────────┘          └──────────┘
```

## Restart Signal Protocol

The Gateway signals planned restarts to the Guardian Angel to prevent false flags:

```
Gateway (about to restart):
  guardian-angel.py --signal-restart "reason"

Gateway (back online):
  guardian-angel.py --clear-restart

Guardian Angel detects flag and monitors:
  • Old PID dies ✓
  • New PID appears ✓
  • Timeout if >5 min          → Escalate
  • 3+ restarts in 1 hour      → Crash loop → Escalate
```

## Detection Logic

| Check | Mechanism | Threshold Before Action |
|-------|-----------|------------------------|
| Gateway process | Read `gateway_state.json` + `os.kill(pid, 0)` | 3 consecutive failures |
| Agent API | HTTP GET `/health` on port 8642 | 3 consecutive failures |
| Error logs | Scan `errors.log` for new ERROR lines | 10 errors/hour = burst alert |
| Planned restart | Flag file `guardian-angel-restart.flag` | 5 min grace period |
| Crash loop | Track restart count in 1h window | 3 restarts/hour = escalation |

## Auto-Recovery Levels

| Level | Action | When |
|-------|--------|------|
| **L1** | Graceful restart: `hermes gateway restart` | After 3 consecutive failures (first attempt) |
| **L2** | Force restart: kill PID + start fresh | If graceful restart fails |
| **L3** | Escalate to the operator via Discord alert | If both restarts fail OR crash loop detected |

## Configuration

Default thresholds (configurable in `guardian-angel-state.json`):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `missed_checks_before_action` | 3 | Consecutive failures before auto-recovery |
| `restart_grace_period_seconds` | 300 | How long to wait during planned restart |
| `max_restarts_per_hour` | 3 | Max restarts before crash loop escalation |
| `restart_cooldown_seconds` | 600 | Min time between auto-restarts |
| `error_burst_threshold` | 10 | Errors in window before burst alert |
| `error_burst_window_seconds` | 3600 | Time window for burst detection |

## Backup

Critical config is automatically backed up before any destructive action:
- `config.yaml`
- `.env`
- `gateway_state.json`
- `guardian-angel-state.json` (own state)
- Last 500 lines of `errors.log`

Backups stored in `~/AppData/Local/hermes/guardian-backups/YYYYMMDD_HHMMSS/`.
Auto-pruned after 7 days.

## Usage

```bash
# Run a check (default — used by cron)
python ~/AppData/Local/hermes/scripts/guardian-angel.py

# Run as persistent daemon (60s check interval, survives session)
python ~/AppData/Local/hermes/scripts/guardian-angel.py --daemon

# Signal planned restart (called before gateway restarts)
python ~/AppData/Local/hermes/scripts/guardian-angel.py --signal-restart "nightly-update"

# Signal restart complete
python ~/AppData/Local/hermes/scripts/guardian-angel.py --clear-restart

# View current state
python ~/AppData/Local/hermes/scripts/guardian-angel.py --status

# Force a backup now
python ~/AppData/Local/hermes/scripts/guardian-angel.py --backup
```

## Complementary System: Hermes Self-Healer

The **Hermes Self-Healer** (`hermes_self_healer.py`) is a companion watchdog that monitors **8 system health dimensions** — broader than Guardian Angel's gateway/agent focus:

| Dimension | Checks | Auto-Repair? |
|-----------|--------|-------------|
| Zombie processes | Firefox.exe >5 instances running | ✅ `taskkill -f -im firefox.exe` |
| Port conflicts | Gateway(8090), brainmd(3000), BiDi(9239) | ✅ Gateway restart |
| Cron failures | auto_action_handler recent errors | 🔍 Reports count |
| Config errors | YAML syntax in config.yaml | 🔍 Reports syntax error |
| API keys | OPENCODE_API_KEY presence | 🔍 Reports missing key |
| Firefox locks | Stale parent.lock >1h old | ✅ Removes stale lock |
| Disk space | C: drive free space <10GB | 🔍 Reports free space |
| MCP servers | brainmd at localhost:3000 | 🔍 Reports unreachable |

**Key difference:** Self-Healer focuses on **environment-level** health (zombies, disk, locks, config). Guardian Angel focuses on **process-level** health (gateway alive, agent responding, restart sequences). They run on different schedules and complement each other.

**Cron job:** `bfcbdb2733e1` — every 15m, no_agent script, silent when healthy.
**Script:** `~/AppData/Local/hermes/scripts/hermes_self_healer.py`

### Auto-Repair Patterns

**Zombie Firefox cleanup** — when >5 firefox.exe detected:
```python
subprocess.run(["taskkill", "-f", "-im", "firefox.exe"])
```

**Stale Firefox lock removal** — lock file >1h old:
```python
os.remove(lock_path)
```

**Gateway port restart** — when port 8090 not listening:
```python
subprocess.run(["taskkill", "-f", "-im", "hermes*"])
```

### Integration Points
- Self-Healer kills zombie Firefox → PIM pipeline can start clean
- Self-Healer removes stale locks → Firefox launches without PermissionError
- Self-Healer kills hermes* → Guardian Angel detects restart and monitors recovery
- Self-Healer reports config errors → Guardian Angel skips restart (broken config wont help)

## Pitfalls

- **CRITICAL: `is_restart_flagged()` must only check the flag file, NOT state** — a bug existed where `is_restart_flagged()` checked both the flag file AND `state["restart_in_progress"]`, causing a self-referential trap. Once `restart_in_progress` was set True, it stayed True forever because the function returned True based on the very state being evaluated. The cron job then entered permanent restart-monitoring mode instead of running health checks. Fixed by only checking the file.
- **First run establishes baseline** — no alarms on first check, only starts tracking from that point forward
- **Restart flag is auto-cleared on next planned restart** — the gateway signals before and after
- **Crash loop detection uses a rolling 1-hour window** — prevents false positives from legitimate restarts spaced hours apart
- **Error burst detection resets when errors stop** — not cumulative forever
- **The guardian does NOT auto-restart in crash loop mode** — it escalates to the operator instead of making things worse
- **Backups are pruned at 7 days** — old backups are auto-deleted to prevent disk fill
- **On Windows, `os.kill(pid, 0)` raises `SystemError` for invalid PIDs** — Python's `os.kill()` on Windows wraps the Win32 `OpenProcess` API, which can return `ERROR_INVALID_HANDLE` (WinError 6). CPython wraps this as a `SystemError` (not `OSError` or `ProcessLookupError`), so a bare `except (OSError, ProcessLookupError): return False` lets it propagate as unhandled and crashes the watchdog. Always catch `SystemError` alongside `OSError`:

  ```python
  def pid_is_alive(pid):
      if pid is None:
          return False
      try:
          os.kill(pid, 0)
          return True
      except (OSError, ProcessLookupError, SystemError):
          return False
      except PermissionError:
          return True  # process exists but no permission — still alive
  ```

- **`.update-incomplete` flag poisoning can block all watchdog checks** — see `references/update-incomplete-flag-poisoning.md`. When a hermes update is interrupted, the stale marker causes every subsequent cron session (including the Guardian Angel's) to hang during init. This produces false "gateway down" alerts because the watchdog can't reach its health check fast enough.
