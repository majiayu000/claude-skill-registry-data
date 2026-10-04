---
name: hydra-deep-research-self-healing
description: Run deep-research loops with HYDRA/Clawbot using self-healing workflow methods (sense, plan, execute, verify, recover), combining arXiv routing, Playwright evidence capture, synthesis smoke checks, and CI triage hooks. Use when operating long-running 24/7 research automation with deterministic cross-talk logging.
---

# Hydra Deep Research Self-Healing

Use this skill for terminal-first research operations that must run continuously and recover from failures.

## Loop Stages

1. `SENSE`
- Route arXiv research lane.
```powershell
python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\browser_chain_dispatcher.py --domain arxiv.org --task research --engine playwriter
```
- Capture deterministic page evidence.
```powershell
python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task title
python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task snapshot
```

2. `PLAN`
- Run synthesis planner packet.
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\system\run_hydra_clawbot_synthesis.ps1
```

3. `EXECUTE`
- Run stack readiness + OpenClaw lane.
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\system\run_hydra_research.ps1 -All
```

4. `VERIFY`
- Run full-system smoke and export summary.
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\system\run_synthesis_pipeline.ps1
```

5. `RECOVER`
- Start watchdog for self-healing restart loop.
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\system\bootstrap_24x7_local.ps1 -RunWatchdogNow -StartWatchdogLoop -WatchdogIntervalMinutes 5
```

## CI Triage Hook

When research code is blocked by failing GitHub checks, route to CI triage lane:

```powershell
python C:\Users\issda\.codex\skills\gh-fix-ci\scripts\inspect_pr_checks.py --repo "C:\Users\issda\SCBE-AETHERMOORE"
```

## Cross-Talk Contract

Emit packet each state transition (`start`, `blocked`, `done`) with where/why/how metadata:

```powershell
& C:\Users\issda\SCBE-AETHERMOORE\scripts\system\terminal_crosstalk_emit.ps1 -TaskId "DEEP-RESEARCH-LOOP" -Summary "Loop update" -Status "in_progress" -Where "hydra-loop" -Why "continuous governed research" -How "sense-plan-execute-verify-recover"
```

## 24/7 VM Operations

Use VM control wrapper for remote operation:

```powershell
& C:\Users\issda\SCBE-AETHERMOORE\scripts\system\vm_clawbot_24x7.ps1 -Action status -VmHost <VM_IP> -User ubuntu -KeyPath <SSH_KEY>
```

Run deep-research loop continuously:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\issda\SCBE-AETHERMOORE\scripts\system\run_deep_research_self_healing.ps1 -Topic "your topic" -Continuous -SleepSeconds 120 -UsePlaywriter -RunCiTriage
```

## Safety Gate: Onion/Tor

- Do not run automated Tor or dark-web crawling/mapping from this skill.
- If onion sources are needed for compliance or threat-intel validation, require explicit legal approval and perform manual, narrowly scoped checks outside autonomous loops.
- Keep autonomous verification on public-web + first-party sources + archived snapshots.
