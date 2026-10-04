---
name: solar-system
description: >
  Integrate Solar runtime with the host system. Install and manage a single macOS
  LaunchAgent that orchestrates enabled Solar features from one entrypoint.
---

# Solar System

## Purpose

Provide one system-level control point for Solar runtime operations:
- install and manage a single LaunchAgent on macOS,
- orchestrate enabled features in one periodic tick,
- keep feature ownership inside existing skills.

## Scope

- Phase 1: macOS (`launchd`) support.
- Orchestrate enabled features from `.env`:
  - `async-tasks`
  - `transport-gateway`
  - `host` — Solar console on `:9000` (status, activity and execution logs)
- Keep orchestration deterministic and non-overlapping.

## Required MCP

None

## Validation commands

```bash
# Validate this skill
python3 core/skills/solar-skill-creator/scripts/package_skill.py core/skills/solar-system /tmp

# Basic shell checks
bash -n core/skills/solar-system/scripts/run_orchestrator.sh
bash -n core/skills/solar-system/scripts/install_launchagent_macos.sh
bash -n core/skills/solar-system/scripts/check_orchestrator.sh
bash -n core/skills/solar-system/scripts/write_pass_stamp.sh
bash core/tests/skills/solar-system/test_pass_stamp.sh

# LaunchAgent SOLAR_ROOT binding unit tests
bash core/tests/skills/solar-system/test_plist_root_binding.sh

# Sync core changes to local clients
solar client sync
```

## Runtime configuration

This skill manages a compact `.env` block:

```bash
bash core/skills/solar-system/scripts/onboard_system_env.sh
```

Block format:

```dotenv
# [solar-system] required environment
SOLAR_SYSTEM_FEATURES=async-tasks
```

The LaunchAgent entrypoint is built at `<runtime root>/system/Solar` during install (default path in code; not versioned in `core/`). Override only if needed: `SOLAR_SYSTEM_RUNTIME_DIR` (absolute or relative to repo root).

`SOLAR_SYSTEM_FEATURES` is a CSV selector. Supported values:
- `async-tasks`
- `transport-gateway`
- `host` — preferred on workstations (panel + API on `:9000` in-process)

Legacy token `interface` is ignored (sunset with `solar-interface` skill); use `host` only.

**Note:** `SOLAR_SYSTEM_FEATURES` is also read by `solar-router` to determine if `async-tasks` is available for async draft creation. Keep this value consistent with your active runtime configuration.

## Workflow

1. Bootstrap runtime env block:
   - `bash core/skills/solar-system/scripts/onboard_system_env.sh`
2. Install or update LaunchAgent:
   - `bash core/skills/solar-system/scripts/install_launchagent_macos.sh`
   - Feature-specific runtime blocks stay in the owning skill, for example `solar-router`.
3. Check current status:
   - `bash core/skills/solar-system/scripts/status_launchagent_macos.sh` — supervisor only (plist + launchctl + logs + SOLAR_ROOT binding)
   - `bash core/skills/solar-system/scripts/check_orchestrator.sh` — full orchestrator + feature health (daily operational check); fails when LaunchAgent `SOLAR_ROOT` is missing, incomplete, or differs from the active install
   - `bash core/skills/solar-system/scripts/diagnose_launchagent.sh` — deep troubleshooting when there is an incident
4. Uninstall LaunchAgent (if needed):
   - `bash core/skills/solar-system/scripts/uninstall_launchagent_macos.sh`

After `solar client update` or relocating the global install, re-run `install_launchagent_macos.sh` so the plist embeds the current `SOLAR_ROOT`. `check_orchestrator.sh` reports `plist_root_status` (`ok|missing_key|root_missing|orchestrator_missing|router_missing|mismatch`).

## Orchestrator behavior

`run_orchestrator.sh --once`:
1. loads `.env`,
2. reads `SOLAR_SYSTEM_FEATURES`,
3. acquires a lock to avoid overlapping ticks,
4. runs enabled features in order:
   - async tasks: `core/skills/solar-async-tasks/scripts/ensure_async_tasks.sh` (the script first checks whether async-tasks is already supervised by solar-system, then falls back to the local worker only when needed)
   - transport gateway: `core/skills/solar-gateway/scripts/ensure_transport_gateway.sh`
   - host: `core/skills/solar-app/scripts/ensure_host.sh`
5. writes `<runtime root>/system/pass-stamp.json` through `write_pass_stamp.sh`:
   the time, each feature result (`ok`, `failed`, `deprecated`, `ignored`), and,
   when `transport-gateway` ran, whether the ws, http, and tunnel processes are
   alive, whether local `/health` answered, and whether the connector is ready.
   The probe curls only loopback. The file is replaced atomically. A tick with
   no features, or one that does not get the lock, does not write a stamp.

## Design notes

- Uses one LaunchAgent label: `com.solar.system`.
- Avoids calling full transport setup on every tick when not needed.
- Keeps transport and async logic in their own skills.

## Laptop runtime note (optional)

- This skill can orchestrate long-running local runtime endpoints indirectly (through transport gateway feature).
- If the active host is a laptop, host sleep can stop runtime availability.
- This is a host operations concern, not a mandatory dependency.
- If multiple laptops are used, only one active host should serve the same public route at a time.
