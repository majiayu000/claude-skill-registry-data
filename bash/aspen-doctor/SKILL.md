---
name: aspen-doctor
description: Check the Aspen Plus MCP setup (uv, server connection, COM, optimizer extras, docs). Use after installing or updating the plugin, when an Aspen tool call actually errors, or when `claude mcp list` shows the server failed. Not because tools are not listed yet -- they load on demand; search for them first.
argument-hint: "[--fix]"
allowed-tools: [Bash, Read, Glob]
---

# Aspen Doctor

Diagnose the Aspen Plus MCP installation and report a short pass/fail table. Aspen Plus is
Windows-only, so every check below assumes Windows.

With `--fix`, additionally offer the repair for each failed check and, where the repair is
a plain install command, run it after the user agrees. Never run a repair without asking.

## Checks

Run these in order and collect results; do not stop at the first failure.

### 1. uv is installed

```
uvx --version
```

Check `uvx`, not `uv`: a bare `uvx` is the name `.mcp.json` invokes, so that is the one
that has to resolve.

**If it fails, do not conclude uv is missing.** Two very different states look identical
from inside a session, and the wrong repair wastes the user's time. Separate them:

```
powershell -NoProfile -Command "winget list --id astral-sh.uv -e; ([Environment]::GetEnvironmentVariable('Path','User') -split ';' | Where-Object { $_ -like '*uv*' })"
```

- **Nothing listed and no PATH entry** -> uv really is absent. Repair:
  `winget install --id=astral-sh.uv -e`, then hand off for a restart.
- **Listed, with a PATH entry** -> uv is installed correctly and the *client process* is
  carrying a stale environment. Installing again changes nothing. On Windows a process
  inherits `PATH` from its parent, and Explorer caches the environment: relaunching the
  client from that same stale Explorer keeps the stale `PATH`. Say this plainly, and hand
  off with: sign out and back in (reliable), or restart Explorer, or launch the client
  from a terminal where `uvx --version` already works.

Report which of the two it is. Never recommend the install command without checking,
because a reinstall on the second state produces no change and looks like the tool is
broken.

### 2. The `aspen-plus` MCP server is connected

Search for a tool by name -- `list_aspen_sessions` is a good probe. Do not judge by the
visible tool list: these tools load on demand, so they are absent from it until searched
for.

**Not finding them is not yet a failure.** Two things must be ruled out first, and both
are ordinary:

- **The server is still connecting.** It takes several seconds -- `uvx` resolves the git
  ref, then 56 tools go through the handshake. A search run before that finishes comes
  back empty. If the session has said any server is "still connecting", wait and search
  again before concluding anything.
- **The name is namespaced.** Installed through the plugin, the tools are prefixed
  `plugin_aspen-plus_aspen-plus`, not `aspen-plus`. A search for the exact string
  `mcp__aspen-plus__list_aspen_sessions` misses them. Search for the bare tool name.

Only after a search that came back empty *with the server settled* should this read FAIL.
The authority is `claude mcp list`: `Connected` means the server is fine and the tools are
either still arriving or were searched for wrongly; `Failed to connect` is the real
failure.

Repair path (only once `Failed to connect` is confirmed):
- Confirm the plugin is installed and enabled: `claude plugin list`.
- If the session predates the plugin install, a client restart fixes it.
- If it reads `Failed to connect`, this is almost always check 1's stale-environment case
  rather than a broken install -- the client cannot resolve `uvx` even though uv is
  installed and on the persisted PATH. Restarting the client is not always enough, since
  it inherits the same cached environment from Explorer. Follow check 1's second branch.
- Otherwise read the client's MCP server log for the launch error.

If the server needs rebuilding, run the plugin's own setup script -- after asking the user,
and never before:

```
powershell -NoProfile -ExecutionPolicy Bypass -File "${CLAUDE_PLUGIN_ROOT}/scripts/install.ps1"
```

Run *that*, never a bare `uvx --from "<git URL>" ...`. A raw command that downloads and
executes code from a URL is what a permission classifier refuses mid-session; a script
shipped inside the already-installed plugin reads very differently, both to the classifier
and to the user approving it. The script takes the version from `.mcp.json`, so it cannot
install anything other than what this plugin is pinned to, and it is idempotent -- on a
warm cache a re-run costs seconds.

Warn the user that a cold run takes one to three minutes, and that a long pause with no
output is the download rather than a hang.

### 3. Aspen Plus COM is registered

```
powershell -NoProfile -Command "Get-ChildItem 'HKLM:\SOFTWARE\Classes' | Where-Object { $_.PSChildName -like 'Apwn.Document*' } | Select-Object -ExpandProperty PSChildName"
```

Expect at least `Apwn.Document` plus a versioned entry such as `Apwn.Document.41.0`.
Report the version numbers found -- they tell the user which Aspen release will be driven.

Nothing returned means Aspen Plus is not installed, or is installed for a different
Windows user, or its COM registration is broken. This is not repairable from here: the
user must install or repair Aspen Plus themselves. Say so plainly rather than guessing.

### 4. COM actually responds

Call `list_aspen_sessions`. It should return without error (an empty list is a pass --
it means no Aspen instance is currently open, not that anything is broken).

If it errors or hangs, the usual cause is a zombie `AspenPlus.exe` holding the COM
server. Repair: ask the user before killing anything, then
`powershell -NoProfile -Command "Get-Process AspenPlus -ErrorAction SilentlyContinue"`
and terminate only if the user agrees.

### 5. Documentation resolves

Ask the `aspen-doc` subagent for something certain to exist -- "the input path for RadFrac
reflux ratio", say -- and see whether it comes back with real Aspen paths.

Test it this way rather than by locating the docs directory. The roots are announced in
the server instructions as `ASPEN_DOCS_ROOT` / `ASPEN_USER_DATA`, but do not treat reading
them back as the check: this asks the model to quote its own prompt, which is unreliable
and has already produced a false failure. What matters is whether a lookup works, and this
exercises the real path end to end.

A refusal or an empty answer is the failure signal. It usually means the plugin's agent is
not loaded (see check 2 -- the same restart fixes both) or the installed package shipped
without its docs, which a re-run of the install command in check 6 repairs.

### 6. Optional optimizer extras

The default install is `aspen-mcp[all]`: `[opt]` (NSGA-II/III, PSO, DE, gradient, grid
search) plus `[bo]` (BO, CBO, AFM-CBO — torch, botorch, gpytorch).

Every optimizer imports its library inside the call rather than at startup, so a missing
tier does **not** stop the server: the tools still appear in the list and fail only when
used. That silent-until-used behaviour is exactly why this check matters even when the
session looks healthy.

Probe with the tools themselves: call one `[opt]` optimizer and one `[bo]` optimizer with
`dry_run=True`. A dry run plans the search without evaluating anything, so it is cheap and
touches no Aspen session -- but it still imports the library, which is what is being
tested. A missing tier surfaces as an import error naming the module.

Do **not** shell out to
`uvx --from "aspen-mcp[all] @ git+https://github.com/..." aspen-mcp --check` to check this.
It downloads and runs code from a URL, so a permission classifier will refuse it mid-
session, and it is the wrong instrument anyway: it inspects whatever environment that
command resolves, not the one the running server was launched from. The dry runs above
test the live server.

Repair: a tier reported absent almost always means setup never completed and the client
started the server from a partial cache. Ask the user, then run `scripts/install.ps1` as in
check 2, and have them restart the client. If a tier is deliberately not wanted, check that
`.mcp.json`'s `--from` argument still requests it.

### 7. Pinch analysis backend

Pinch runs in a separate interpreter because OpenPinch needs Python >= 3.14. With `uv`
present this is automatic, but the **first** call provisions Python 3.14 and OpenPinch and
can take several minutes. Call `pinch_analysis` with a two-stream textbook input, allow a
generous timeout, and report whether it returned targets or a setup hint.

A failure here with `uv` installed usually just means provisioning has not finished --
say so and suggest retrying rather than declaring pinch broken.

### 8. Setup state matches the pinned version

Read `%USERPROFILE%\.aspen-mcp\setup-state.json` and compare its `setupCompletedFor` with
the release tag in `.mcp.json`'s `--from` argument.

They should be equal. A mismatch -- or a missing file -- means setup has not run for the
version this plugin now pins, which is the expected state right after a plugin update. The
SessionStart hook already offers the repair at the start of each session; this check only
makes the reason visible when the user is already looking at a failure.

Repair: `scripts/install.ps1`, as in check 2.

## Output

Finish with a compact table -- one row per check, `PASS` / `FAIL` / `NOT READY` / `SKIP`,
plus a one-line note. Then list only the failed checks' repairs, in the order they should
be done. If everything passed, say so in one line and stop; do not pad the report.

`NOT READY` exists so a slow start is never reported as a fault: use it when the server
is connecting or the tools have not arrived yet, and say the check should simply be re-run
in a moment. `FAIL` claims something is broken and sends the user to fix it, so spend it
only on evidence. Checks 4-7 all depend on live tools, so when check 2 is `NOT READY` they
are `SKIP` with the same note -- not a wall of failures, which reads as a broken install
when nothing is wrong.

Checks 1, 3 and 8 read only local state, so they stay real checks even then -- and check 8
is usually the one that explains a `NOT READY` check 2, since a server that was never set
up for the pinned version is exactly a server that will not connect.
