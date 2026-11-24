---
name: game-godot-chat-e2e
description: Verify samples/Game.Godot.Chat end to end with its dedicated script. Use when changing the Godot chat sample, its shared chat/login contracts, its server hotfix/app code, Lakona game server hosting, WebSocket transport, MemoryPack serializer behavior, generated RPC client/server glue, or when the user asks to run a precise real server/client E2E test for samples/Game.Godot.Chat.
metadata:
  internal: true
---

# Game Godot Chat E2E

## Overview

Run the sample-specific E2E script. Do not substitute unit tests, loopback transports, raw protocol probes, or the generic Lakona.Tool matrix unless the user explicitly asks for those.

The script builds and launches the real `samples/Game.Godot.Chat` server, compiles a temporary console client harness from the sample's own `LoginClient.cs` and `ChatClient.cs`, sends real WebSocket/MemoryPack RPC requests, verifies the login response, binds chat, sends a message, verifies the pushed callback, and stops the server.

When validating hotfix watcher behavior, run the same script with `-VerifyHotfixWatcher`. That mode edits `samples/Game.Godot.Chat/Server/Hotfix/Chat/ChatService.cs`, rebuilds `Server.Hotfix`, relies on the generated `reload.signal`, sends another real RPC message, and verifies that the running server logs the new `SendAsync` token before restoring the source file.

## Authorization Boundary

For verification-only or review-only requests, run the requested checks and
report failures with proposed fixes; do not implement permanent repairs.
Explicitly requested watcher verification may use the temporary source edit
described above and must restore it afterward. For implementation or repair
requests, fix and rerun within the existing authorized scope; ask only when
the next action requires a material decision or exceeds that scope.

## Command

From the repository root:

```powershell
pwsh -NoProfile -File samples/Game.Godot.Chat/test-game-godot-chat-e2e.ps1
```

Useful options:

- `-Port <port>`: override the endpoint port through inherited .NET configuration.
- `-TimeoutSeconds <seconds>`: extend startup and callback waits on slow machines.
- `-PlayerName <name>` and `-MessageText <text>`: change the exact payload asserted by the harness.
- `-VerifyHotfixWatcher`: mutate `ChatService.SendAsync`, rebuild the hotfix project, and prove the running server loaded the changed code through the real watcher.
- `-KeepArtifacts`: keep the generated harness under `samples/Game.Godot.Chat/_artifacts/e2e/client-harness`.

## Workflow

1. Read `CONTRIBUTING.md` first if not already loaded.
2. Run the dedicated script from the repo root with `pwsh`.
3. If it fails, inspect:
   - `samples/Game.Godot.Chat/_artifacts/e2e/server.out.log`
   - `samples/Game.Godot.Chat/_artifacts/e2e/server.err.log`
   - `samples/Game.Godot.Chat/_artifacts/e2e/client.out.log`
4. For verification-only requests, report the failing layer and proposed fix. When repair is authorized, fix that layer within scope and rerun the same script.
5. Also run `pwsh -NoProfile -File tests/Scripts/test-game-godot-chat-e2e-script.ps1` after editing the script itself.

## Expected Coverage

The E2E run must verify all of these in one process lifecycle:

- `dotnet build` of `samples/Game.Godot.Chat/Server/App/Server.App.csproj`
- real server process startup with `dotnet run --no-build`
- temporary client harness build against local source projects
- `LoginClient.ConnectAsync`
- `LoginClient.LoginAsync`
- `ChatClient.BindAsync`
- `ChatClient.SendAsync`
- `LoginClient.OnMessageReceived` receiving the sent chat message

With `-VerifyHotfixWatcher`, the run must additionally verify:

- `ChatService.cs` is restored after the run
- `Server.Hotfix` rebuild writes `reload.signal`
- the running server observes the watcher-triggered reload
- a later `ChatClient.SendAsync` reaches the changed hotfix code, proven by the new server log token

## Common Failures

- Port busy: prefer rerunning with a free `-Port`. Before stopping a conflicting process, verify its identity and ownership; stop it only if this verification run started it or the user has authorized stopping it. Do not stop an unrelated process merely to free the port.
- Server exits early: read `server.err.log`; hotfix loading and DI failures usually appear there.
- Client build fails: check generated RPC client properties and project references in the harness project.
- Login succeeds but push times out: inspect chat bind/session callback wiring before changing transport code.

Keep this skill specific to `samples/Game.Godot.Chat`. Do not generalize it into a sample matrix or scaffold verification workflow.
