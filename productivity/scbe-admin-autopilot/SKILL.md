---
name: scbe-admin-autopilot
description: Operate SCBE in admin mode through the Issac Command Center, watchdog loops, service launchers, cross-talk relay commands, and verified storage or sync runs. Use when the user asks for always-on agent workflows, command-center automation, repo or system health checks, backup or prune lanes, service bootstrapping, or admin-level orchestration.
---

# SCBE Admin Autopilot

Use this skill to run SCBE from the local command-center surface instead of inventing one-off shell commands.

## Entry Surface

- Start with `issac-help`.
- Prefer `hdoctor` before assuming the local HYDRA surface is healthy.
- Read `references/issac-command-center.md` when you need the exact alias list or grouped command map.
- The aliases live in `scripts/hydra_command_center.ps1`; install them with `scripts/install_hydra_quick_aliases.ps1` if they are missing.

## Core Lanes

1. Command Center Health Lane
- Use `hstatus`, `hqueue`, and `hdoctor` for first-pass health checks.
- Use `hwf`, `hcanvas`, `hbranch`, and `hlattice` to prove the major HYDRA surfaces are reachable.

2. Research + Swarm Lane
- Use `hresearch`, `hdeep`, `hswarm`, `harxiv`, `harxiv-ml`, `harxiv-get`, and `harxiv-outline` for directed research and swarm work.
- Use `hcascade`, `harticle`, or `hmission` when the user wants a multi-step autonomous run instead of a single query.

3. Skill + Memory Lane
- Use `hskills-refresh`, `hskills`, and `hstack` for repo-local skill synthesis and stack composition.
- Use `hremember`, `hrecall`, and `hsearch` to persist or retrieve working facts.

4. Service + Relay Lane
- Use `scbe-api`, `scbe-bridge`, `octo-serve`, and `htunnel` to start the major services and tunnels.
- Use `xtalk-send`, `xtalk-ack`, `xtalk-pending`, and `xtalk-health` to keep agent coordination explicit.

5. Agent Continuity + Storage Lane
- Keep agents moving with:
  - `scripts/system/watchdog_agent_stack_default.ps1`
  - `scripts/system/run_watchdog_loop.ps1`
  - `scripts/system/register_agent_stack_tasks.ps1`
- Run storage shipping, verification, and optional prune with:
  - `python scripts/system/ship_verify_prune.py --source <path> --dest <backup1> --dest <backup2> --min-verified-copies 2 --delete-source`
- Run repo or cloud sync with:
  - `python scripts/system/system_hub_sync.py --help`

## Safety Gates

1. Do not assume the aliases are loaded; verify with `issac-help` or run the installer.
2. Prefer `hdoctor` or `hstatus` plus `hqueue` before long autonomous runs.
3. Never delete local files unless `--delete-source` is explicitly set.
4. Require checksum verification and at least 2 verified copies before prune.
5. Keep secrets in env vars only. At minimum, check `SCBE_API_KEY` before authenticated API work.
6. Record ports, artifact paths, and cross-talk packet IDs in the run summary.

## Output Contract

Each admin run should emit:

- command evidence or service status output
- artifact paths for storage, workflow, or synthesis outputs
- a cross-talk packet or explicit note that no packet was required

## Quick Start

```powershell
# inspect the operator surface
issac-help
hdoctor

# run a multi-step mission
hmission "stabilize the agent workflow stack"

# boot the main API
scbe-api
```
