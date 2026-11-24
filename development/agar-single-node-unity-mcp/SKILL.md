---
name: agar-single-node-unity-mcp
description: Validate Game.Unity.Agar single-node login, matchmaking, battle, or settlement-adjacent behavior through MCP for Unity with Unity Editor already open, using a verified existing server, local dotnet startup, or managed Compose.
metadata:
  internal: true
---

# Agar Single Node Unity MCP

## Preconditions

- Unity Editor must already be open on `samples/Game.Unity.Agar/Client`.
- MCP for Unity must already be connected locally. The prep script prefers `127.0.0.1:8180` and falls back to the default `127.0.0.1:8080`.
- If either Unity Editor or MCP for Unity is missing, run the prep script and stop when it reports the preflight error. Do not launch Unity Editor from this skill; ask the user to start it manually.
- Use PowerShell 7 (`pwsh`) from the repository root.

## Start Single-Node Server

Prepare once per validation session, selecting the requested scenario:

```powershell
pwsh -NoProfile -File scripts/game/local/test-agar-single-node-unity-mcp.ps1 -Scenario Matchmaking
```

Before preparation or reuse, identify the server process or Compose project,
checkout, configuration, endpoints, and build/image provenance. Record whether
it existed before this session and inspect any PID or Compose marker in the
artifact directory. Readiness alone does not prove ownership or current code.
Do not reuse an instance whose provenance cannot be established or stop an
unrelated instance to obtain the ports.

Reuse the verified instance across tests while relevant server code,
configuration, and required state remain unchanged. Refresh changed client
scripts through Unity. Reprepare when server inputs change or the scenario
requires a state reset. Use `-StopExisting` only after confirming that the
recorded process/topology belongs to this session or its restart is authorized.
The script rejects a live recorded PID before checking readiness, so do not
rerun preparation merely to reuse this session's running dotnet server.

What the script actually does:

- Fails early if Unity Editor or MCP for Unity is not running.
- Reuses a server returning HTTP 200 at port 20080's `/_lakona/health/ready`
  endpoint when no live recorded PID blocks preparation. This branch does not
  build or verify provenance; perform the checks above first.
- If local PostgreSQL or Redis ports are unavailable, delegates startup to
  `samples/Game.Unity.Agar/server-ctl.ps1 start -Topology single` and records
  `server-ctl.started`. This runs the managed Compose topology with dependencies.
- Otherwise builds `Server/App/Server.App.csproj` and
  `Server/Hotfix/Server.Hotfix.csproj`, then starts Server.App using
  `dotnet run --configuration Debug --no-build` with the project path.
- The dotnet branch clears the script's environment overrides, waits for the
  control TCP port and KCP address in the startup log, and records `server.pid`.
  These startup checks do not prove a client RPC or KCP round trip.
- Writes artifacts under `.tmp/agar-single-node-unity-mcp`.

The script defaults to `--no-restore` builds. If package assets are stale, rerun with `-Restore`.

## Unity MCP Test Step

After the script reports `Ready`, drive the client through MCP for Unity:

1. Refresh scripts if Unity code changed: `refresh_unity` with `scope="scripts"`, `mode="if_dirty"`, `compile="request"`, and `wait_for_ready=true`.
2. Clear the Unity console.
3. Run the PlayMode test `SampleClient.Gameplay.Tests.DotArenaThreeNodePlayModeTests.UnityClientCompletesThreeNodeMultiplayerSmoke`.
4. Poll the test job until completion.
5. On failure, inspect the Unity console, PlayMode failure snapshot, and logs
   from the actual server branch: artifact stdout/stderr for dotnet, Compose
   service logs for managed topology, or the verified external instance's logs.

Use MCP for Unity tools/resources for the Unity side. Do not use Unity batchmode for this skill.

## Scenario Mapping

- `Login`: Use `-Scenario Login`. The current PlayMode smoke proceeds past login, so a later matchmaking or battle failure can still prove login succeeded if the snapshot shows the lobby stage, `control=True`, and a player id.
- `Matchmaking`: Use `-Scenario Matchmaking`. The PlayMode smoke validates guest login, `StartMatchmaking`, queued state, the five-second AI-fill path, and receipt of a matched KCP endpoint.
- `Battle`: Use `-Scenario Battle` or `-Scenario Smoke`. The PlayMode smoke validates KCP realtime attach, entering the match, and receiving world state.
- `Settlement`: There is no dedicated Unity MCP settlement PlayMode test yet. Use this skill to validate login/match/battle client-server flow, then run targeted business logic tests when settlement code changed:

```powershell
dotnet test samples/Game.Unity.Agar/tests/BusinessLogic.Tests/BusinessLogic.Tests.csproj --no-restore --filter "FullyQualifiedName~ArenaSimulationRulesTests|FullyQualifiedName~PlayerSessionActorStateTests|FullyQualifiedName~AgarSessionLifecycleTests"
```

## Cleanup

Stop the server/topology created by this session before finishing. Verify the
recorded PID's identity and Compose project ownership before using the cleanup
command; a stale marker is not proof of ownership. Preserve pre-existing
instances that were only reused. Use the same `-ArtifactRoot` if customized:

```powershell
pwsh -NoProfile -File scripts/game/local/test-agar-single-node-unity-mcp.ps1 -Stop
```

## Failure Triage

- Preflight failure: Unity Editor or MCP for Unity is not running; ask the user to start them manually.
- Build failure: inspect build output; rerun with `-Restore` only if restore is needed.
- Server readiness failure: inspect the actual branch's logs and startup
  artifacts; managed Compose and reused instances need not have local dotnet logs.
- Unity failure: inspect the PlayMode failure snapshot first, then Unity console and server logs.

Report server provenance, startup/reuse branch, scenarios actually exercised,
test results, artifacts, and cleanup ownership. `-Scenario` labels preparation;
it does not select a different Unity test. Prefer an existing dedicated login
test if one becomes available; otherwise report the smoke's actual coverage.
A later failure may establish login evidence but never a full smoke pass.
