---
name: anthill-test-environment
description: "Use when running AntHill tests: SetupFlowTests failing (stray AntHill.Web on 5252), Lore.Tests skipping ~47 or failing with Disconnected from server, merge.rs:303 or merge waiting to be committed. Also before trusting any AntHill run, when Client.Tests skips drop from 3 to 1, or when Lore.Tests failures sit in fixtures your change never touched."
---

# AntHill test environment

Two AntHill suites gate tests on live external state, so unchanged code can read green, red or
half-skipped depending on what is running. Put each suite's dependency in its baseline state
and compare all three counts before blaming code.

## 1. Know what each suite gates on

| Suite | Gate | Wrong state → signature |
|---|---|---|
| `tests/AntHill.Lore.Tests` | Lore server on 41337 plus the shared on-disk testbed `D:/AntHillTesting` | server down → ~47 tests **skip** and the run still looks green |
| `tests/AntHill.Client.Tests` | `tests/AntHill.Client.Tests/SetupFlowTests.cs` gates its `[SkippableFact]`s on `Reachable("localhost", 5252)` (const `DashboardUrl`) | anything on 5252 that is not the real dashboard backed by a live database → exactly 2 **fail**, skips 3 → 1 |

Lore.Tests, observed on this repo:

| Server | passed | failed | skipped |
|---|---|---|---|
| down | 50 | 10 | **53** |
| up | 100 | 7 | 6 |

Starting the server moved **47 tests from skipped to actually running**: a "50 passed" run was
testing about half of what it appeared to.

Client.Tests with 5252 free: `Passed: 271, Skipped: 3, Failed: 0` (as recorded; the pass count
grows with the suite). The discriminator is skips back to 3 and failures at 0.

**Always report the skipped count**, not just passed/failed. Rising skips = the environment
regressed; skips falling while failures appear = something un-gated them. rtk swallows the
summary line; capture it with `dotnet-test-verdict-capture`.

## 2. Check both ports before running

```powershell
Get-NetTCPConnection -State Listen | Where-Object LocalPort -in 41337, 5252 |
  Select-Object LocalAddress, LocalPort, OwningProcess
Get-Process -Id <pid> | Select-Object ProcessName, Path
```

Filter by port, not address: the 5252 squatter was seen on `[::1]`. Use this rather than
`netstat`: it names the owning PID in one step, and `netstat` through the `rtk` proxy has been
unreliable.

**41337 must be the Lore server.** Start it, then wait on the port:

```
loreserver.exe --config D:/AntHillTesting/loreconfig     # cwd D:/AntHillTesting
```

- binary `C:/Users/alex.mollard/bin/loreserver.exe`; that dir is on PATH and also holds the
  client CLI `lore` (`D:/AntHillTesting/tools/lore.exe` is the same build; verified 2026-09-24)
- config dir `D:/AntHillTesting/loreconfig`, auth disabled; see
  `docs/superpowers/notes/loreserver-local.toml`

**5252 must be free, or the real dashboard with its database up.** The classic squatter is a
leftover debug `AntHill.Web.exe` under `src/AntHill.Web/bin/Debug/net10.0/` from
`dotnet run src/AntHill.Web` (an agent's repro, say) whose database container was already
removed. Once `Get-Process` shows that path, `Stop-Process -Id <pid> -Force` (never stop the
user's own dashboard), then re-run `dotnet test tests/AntHill.Client.Tests`
and see the skip baseline before calling the code innocent. Leave unrelated listeners alone:
41337 is the Lore server; `anthill-db-1` on 5432 is the dev compose stack.

The two failures are `Once_told_where_the_server_is_it_can_list_the_titles` and
`A_machine_that_loses_the_network_still_knows_what_it_saw`. The third gated test also needs
41337 and skips when the server offers no checkoutable titles, which is why a broken stray
server leaves one skip.

Any workflow that boots `AntHill.Web` for repro or verification must kill the process (not just
the containers) and verify 5252 is free before yielding.

## 3. Attribute Lore.Tests failures before blaming code

With the server up, failures may still come from the testbed's state. The error text names the
cause:

- `Disconnected from server` → server down. Back to section 2.
- `There is a merge waiting to be committed in <branch>. Send it back first` → AntHill's own
  refusal: the failing test's workspace holds a merge.
- `at lore-revision\src\branch\merge.rs:303:1` / `Invalid merge type` → Lore cannot read that
  workspace's merge state. Environmental, not an AntHill code failure.

Leftover merge state once contaminated **7 tests across four unrelated fixtures**
(`SelectiveFetchTests`, `CherryPickTests`, `BranchSwitchTests`, `BareWorkspaceTests`). None of
them were about merging.

Fixtures are their own workspaces under `D:/AntHillTesting` (`ANTHILL_TEST_BED` overrides the
root): never one the client registered in `workspaces.json`, and never `artist`, which is on the
clean-up script's never-sweep list. Each test names its workspace in a `const string` or via `TestBed.*` (e.g. `branch-cricket26`,
`demo2`), so read it rather than guess, then clear that fixture with `lore-stuck-merge-recovery`.

**Never clear `D:/AntHillTesting/ui-b`.** It holds a merge on purpose: four tests in
`SelectiveFetchTests` and `BranchSwitchTests` skip with `That workspace has no merge waiting.`
once it is gone (verified 2026-09-24).

Some fixtures are built by the tests themselves (`<name>-<8 hex>`, swept by
`tools/clean-test-bed.ps1`), so a failure that survives cleaning the on-disk fixtures is likely
pre-existing and not caused by your change.

Probe testbed state directly rather than guessing:

```
lore --repository <workspace> -P status
lore --repository <workspace> -P history --only-branch
```

Both can succeed while merge commands fail; see `lore-stuck-merge-recovery`.

Confirm attribution positively: run only the tests that cover your change and show them passing.

```
dotnet test tests/AntHill.Lore.Tests/AntHill.Lore.Tests.csproj --filter "FullyQualifiedName~<YourType>"
```

Failures in fixtures your change never touches, plus an error naming the testbed, are
environmental.

## 4. Build locks are not test results

A running `AntHill.Web` locks `AntHill.App.dll`; a running `AntHill.Client` locks its own
`.exe`. The build then fails with `MSB3026`/`MSB3027`/`MSB3021` and `locked by: "<proc> (pid)"`
and prints no test counts: the suite never ran. Stop the holder only if you started it, then
retry; if it is the user's dashboard or Visual Studio, leave it running and report which suites
were skipped. The lock table and the rule are in `dotnet-test-verdict-capture`. A dashboard you
stopped for a build that touches `AntHill.App` must be restarted afterwards, otherwise the
client stops seeing the real catalogue.

## Cost

A full `AntHill.Lore.Tests` run is **5–8 minutes**. Budget for it, and prefer `--filter` for
attribution passes.
