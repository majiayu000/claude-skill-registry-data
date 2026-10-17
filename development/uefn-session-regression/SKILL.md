---
name: uefn-session-regression
description: Run a play-in-editor smoke or the modify, build, push, log, verdict cycle with ValkyrieToolset.SessionToolset (StartSession, StartGame, PushChanges, StopGame, StopSession) plus VerseToolset WriteFile/BuildAll. Use for session health, always-close and regression verdicts. Requires uefn-mcp-lab-guard and uefn-verse-build.
last_reviewed: 2026-10-16
sources: [original]
---

# uefn-session-regression

Source: `Claude/docs/mcp/session-regression.md` (incl. T-015 C2 update), `recipes.json` (only `tool-ok` or `proven`; `proven` = the same call form already worked in real work), `SKILLS-PROPOSAL.md` B6.

## Read first
1. Read `uefn-mcp-lab-guard` and `uefn-verse-build`.
2. Ping with a cheap read before the first write and before every session action.
3. If the MCP does not answer: stop and report. Never close or kill a running editor (after a crash: `uefn_session.py recover`, opt-in), never loop on a hung MCP.

## Rules
- Paths in arguments: GUID form `/09e4e8d3-83f9-4ee0-9777-072ed3984380/root_ai_lab/...`.
- The guard is not bypassed; a refusal is reported verbatim.
- If a recipe fails: exact error text, then STOP.
- Always `StopGame` then `StopSession` in try/finally and verify `GetSessionStatus` = `Disconnected`. Never leave a session open.
- Do not start a session while a disallowed actor is in the level (see TargetPoint trap).
- One process for session actions; a second process may poll with read tools only (replies can cross).

## Verified recipes (toolset `ValkyrieToolset.SessionToolset`)

| Tool | Args | Measured / note |
|---|---|---|
| GetSessionStatus | `{}` | Disconnected, Connected, UpdatingContent; 0.01 s |
| GetGameState | `{}` | Unconnected, CanStart, Running; CanStart does NOT mean StartGame works |
| StartSession | `{}` | ~88 s (67-87 s measured: 11 s upload, ~13 s beacon + client launch, ~65 s cook). The reply text may be an unrelated stale error: confirm with GetSessionStatus = Connected |
| StartGame | `{}` | 0.28 s after Connected (0.27-0.4 s), GetGameState Running at once, Verse begins ~0.8 s later. Only after StartSession returned AND status Connected after UpdatingContent; otherwise `The Start Game command is not currently available.` |
| PushChanges | `{bVerseOnly:true}` | 7.9 s; needs a real Verse change, else `The Refresh command is not currently available.` |
| StopGame | `{}` | 1.3-1.5 s |
| StopSession | `{}` | null, status Disconnected; FortniteClient processes stay alive afterwards |
| LogsToolset/GetLogEntries `#why_startsession_failed` | `{category:"", maxEntries:0, pattern:"UEFNValidation"}` | reason of `Failed: Validation failed` |
| Verse runtime output | `LogsToolset/GetLogEntries {category:"", maxEntries:0, pattern:"<marker>"}` | forwarded as `LogVerse: : <text>` ~0.8-4 s after StartGame |

Full smoke (R1): ping, StartSession (ignore reply text), poll GetSessionStatus until Connected, StartGame, check Running, finally StopGame + StopSession, status Disconnected.

Cycle (R3, ~10 s without StartSession): `WriteFile`/`Replace` -> `BuildAll` (`[]` = PASS, else FAIL with code+span; this is the gate) -> only if PASS and Connected: `PushChanges {bVerseOnly:true}` -> read new log lines -> verdict with timings.

## Traps
- TargetPoint: an actor of class `/Script/Engine.TargetPoint` makes StartSession answer `Failed: Validation failed` (`UEFNValidation: Error: Disallowed reference to /Script/Engine.TargetPoint`), and the editor MCP then stops answering for minutes. Do not place such classes; diagnose with the `UEFNValidation` log recipe above.
- StartGame too early (16 s in the old loop) fails because status is still Connected-early/UpdatingContent: poll GetSessionStatus, not GetGameState.
- With a broken source, PushChanges only answers "Refresh command is not currently available" (session stays healthy): the BuildAll result is the verdict, not the push.
- Closing or killing a running editor is refused by design; relaunch after a crash only with `uefn_session.py recover --wait 150` (opt-in, max 2 in 30 min; the project reopens by itself about 47 s later with Load on Startup = Most Recent Project).

## To try (not verified)
- `GetClientLogEntries {pattern, maxResults, startLine}`: status unverified. Always `No client log was found; start a play-in-client session first.` in every state (10+ attempts, live client running); `Pattern must not be empty.` for an empty pattern. Use the LogsToolset recipe instead. Cause not found, owner decision pending.
- Runtime "missing event" test and placing a lab-built Verse device in a session: not possible, the guard refuses the placing route (level-devices area).
