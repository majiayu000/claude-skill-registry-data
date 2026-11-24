---
name: agar-three-node-e2e
description: Run the dedicated local three-node E2E smoke test for samples/Game.Unity.Agar through scripts/game/ci/test-agar-three-node.ps1. Use when the user asks to verify the Agar sample end to end, run the three-node topology, validate Docker Compose plus Unity PlayMode smoke behavior, or after changes to Game.Unity.Agar server/client code, cluster routing, gateway/battle/data node startup, Docker Compose configuration, or Unity multiplayer smoke tests.
metadata:
  internal: true
---

# Agar Three Node E2E

## Overview

Use the existing repository script. Do not replace it with ad hoc Docker, Unity, or RPC commands unless you are debugging a specific failure after the script has produced artifacts.

The script starts the real `samples/Game.Unity.Agar` Docker Compose topology for
`postgres`, `redis`, `data-1`, `gateway-1`, and `battle-1`. It verifies the Redis
Membership Table contract and one shared Active view, runs Unity PlayMode
traffic against `127.0.0.1:20000/ws`, restarts `data-1` during the default live
traffic test, fences and replaces `gateway-1`, kills and recovers all three game
nodes, then reruns the default smoke after recovery.

## Default Command

From the repository root:

```powershell
pwsh -NoProfile -File scripts/game/ci/test-agar-three-node.ps1
```

Use PowerShell 7 or newer. The script itself has `#Requires -Version 7.0`.

## Preconditions

Verify these before treating a failure as a product bug:

- Docker with `docker compose` is installed and running.
- Unity is installed, preferably the version in `samples/Game.Unity.Agar/Client/ProjectSettings/ProjectVersion.txt`.
- If Unity is not in the default Hub path, pass `-UnityPath` or set `UNITY_PATH`.
- Required ports are free or owned by the target test project's expected services.
- Run only one three-node test at a time, including across worktrees.
- The working tree can tolerate local artifacts under `.tmp/agar-three-node`.

## Useful Options

- `-UnityPath "<path-to-Unity.exe>"`: force the Unity executable.
- `-TimeoutSeconds <seconds>`: increase the total run deadline; must be at least `60`.
- `-TestFilter <fully-qualified-test>`: run another Unity PlayMode test. The
  default test opens the live `data-1` restart window; another filter runs
  without that synchronized window but still performs gateway and whole-cluster
  recovery checks.
- `-KeepEnvironment`: leave Docker Compose services running after a successful or failed run.
- `-ReuseEnvironment`: retain the target project's containers and data instead of cleaning first; recovery tests still restart and replace nodes. Do not use against an environment serving other work.
- `-SkipBuild`: run Compose without `--build`; use only when the images are known current.
- `-ProjectName <name>`: select the Compose project; default is `lakona-agar-three-node-test`. Ports, container names, and artifact paths remain fixed, so this does not enable parallel runs.

Examples:

```powershell
pwsh -NoProfile -File scripts/game/ci/test-agar-three-node.ps1 -UnityPath "$env:ProgramFiles\Unity\Hub\Editor\2022.3.62f1\Editor\Unity.exe"
pwsh -NoProfile -File scripts/game/ci/test-agar-three-node.ps1 -TimeoutSeconds 900 -KeepEnvironment
pwsh -NoProfile -File scripts/game/ci/test-agar-three-node.ps1 -ReuseEnvironment -SkipBuild
pwsh -NoProfile -File scripts/game/ci/test-agar-three-node.ps1 -TestFilter "SampleClient.Gameplay.Tests.DotArenaTwentyClientLifecyclePlayModeTests.TwentyClientsCompleteMatchBattleSettlementAndLeaderboard" -TimeoutSeconds 600
```

## Failure Triage

On failure, inspect `.tmp/agar-three-node` before rerunning:

- `docker-compose-startup.log`: Compose startup command, stdout, stderr, timeout state, and exit code.
- `docker-compose.ps.json`: Compose service status snapshot.
- `docker-compose.log`: combined Compose logs.
- `unity-editor.log`: Unity batchmode editor log.
- `TestResults.xml`: Unity test result XML.
- `lifecycle-report.json`: node incarnation and recovery observations.

Use the failure phase to guide debugging:

- Preflight failure: check Unity path, Docker availability, or missing sample paths.
- Compose startup failure: inspect `docker-compose-startup.log` and `docker-compose.log`.
- Membership contract failure: inspect the Redis service and the filtered
  `RedisMembershipTableTests` output before changing cluster runtime code.
- Readiness or convergence timeout: inspect service health in
  `docker-compose.ps.json`, node Membership views, and logs for `postgres`,
  `redis`, `data-1`, `gateway-1`, and `battle-1`.
- Gateway port timeout: check `gateway-1` endpoint binding and host port conflicts.
- Unity test failure: inspect `unity-editor.log` first, then `TestResults.xml`.
- Recovery failure: use `lifecycle-report.json` and `docker-compose.log` to
  determine whether an incarnation was reused, a Membership view failed to
  converge, or Actor Directory recovery rejected traffic.

## Cleanup

The script normally runs:

```powershell
docker compose -p lakona-agar-three-node-test -f samples/Game.Unity.Agar/docker-compose.yml -f .tmp/agar-three-node/docker-compose.local-test.override.yml down --volumes --remove-orphans
```

If `-KeepEnvironment` or `-ReuseEnvironment` was used, the script preserves the environment. Clean it manually with the same command when finished.

Keep this skill scoped to `scripts/game/ci/test-agar-three-node.ps1`; do not generalize it into a matrix runner or a replacement for the Godot chat E2E skill.
