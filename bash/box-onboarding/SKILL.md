---
name: box-onboarding
description: "Admit a new box to the multibox fleet: install, probe, register identity, key, verify reach."
allowed-tools: ["Read", "Bash", "Glob", "Grep"]
argument-hint: "[box role: secondary | tertiary | headless]"
---

# Box Onboarding

A one-time act, run on the box being admitted. It is not a G-EM turn: there is one network-wide
G-EM, which reaches the admitted box over Unimatrix, and any box may hold it (last writer wins
across the network; `coordinator/skills/group-em/references/multibox.md`, "One G-EM"). A box
without a G-EM is not missing one. Onboarding gives that G-EM a box it can place work on
("Placement") and see on the federated roster ("Federated roster"). Admission of any one job stays
the target box's own verdict ("Local admission per box").

Rules: no hostname, drive letter or user path is a rule; identity comes from `machine-local` and
Claude-klabauter's box registry. No key body, fingerprint or vault content is ever written to a tracked file
(`coordinator/docs/wiki/multibox-key-custody.md`). Steps marked **guarded** stop with a one-line
notice when the engine half has not shipped; a stop is not a failure, record it and continue.

Each step gives one command per host family. `<klabauter-clone>` is the engine clone from
`machine-local get repos.claude_klabauter`.

## Steps

1. **Install coordinator-claude per `INSTALL.md`** (Steps 0-3), then clone the engine (Step 1e).
   - Windows (PowerShell): `claude plugin list`
   - macOS / Linux: `claude plugin list`
   - Done when `coordinator-claude` is listed after a restart.

2. **Run claude-klabauter's setup.** Read every `PASS`/`FAIL` line; non-zero exit means not installed.
   - Windows: `python <klabauter-clone>\scripts\setup.py --i-am-agent`
   - macOS / Linux: `python3 <klabauter-clone>/scripts/setup.py --i-am-agent`
   - Linux headless: also confirm `systemctl is-active sshd`; macOS: `sudo systemsetup -getremotelogin`
     (Remote Login on); Windows: `Get-Service sshd` (running).

3. **Capability probe (guarded).** The probe is claude-klabauter's; absent, print `probe not yet shipped`
   and stop this step.
   - Windows: `python <klabauter-clone>\scripts\setup.py --help | Select-String capability` (no match: print `probe not yet shipped`)
   - macOS / Linux: `python3 <klabauter-clone>/scripts/setup.py --help` (no capability option listed: print `probe not yet shipped`)
   - The probe's record marks UE/p4 present or absent; a UE/p4-absent box never receives UE work.

4. **Register box identity (guarded).** Read back what `machine-local` and claude-klabauter's registry
   know; the registry row is written by the box's owner (EM), not by this skill.
   - Windows: `machine-local keys | Select-String "^box"` ; `machine-local get box.id`
   - macOS / Linux: `machine-local keys` (read the `box.` keys); `machine-local get box.id`
   - No `box.*` keys: print `registry schema not yet shipped` and stop this step.

5. **Issue keys per the custody page.** Keys are named `<role>: <from> → <to>`. Roles:
   `Unimatrix-01` is full shell, break-glass; `Unimatrix-Zero` is the comms relay only;
   `Unimatrix-02` is the project-rag tunnel only (forwarding, no shell). One key per box pair, so
   a leak's blast radius is that pair; Zero is needed one way per pair because the initiating box
   holds the inbox connection. Unimatrix-01 is a full mesh: any one box can be the controller or
   the controlled, so long as the keys authenticate (PM: "we should be able to pick any one box
   as the controller or controlled, so long as the keys authenticate etc etc"). Fetch from the
   1Password Team vault, install the target-side `authorized_keys` line, never copy a private
   half onto this box. 1Password's CLI cannot edit SSH Key items, and a CLI import of an existing
   OpenSSH key lands unparsed: import and rename in the app (`op --ssh-generate-key` is fine).
   - Windows: `op item get "<role>: <from> → <to>" --vault <team-vault> --fields label=public_key`
   - macOS / Linux: `op item get "<role>: <from> → <to>" --vault <team-vault> --fields label=public_key`
   - Place the line: macOS / Linux `~/.ssh/authorized_keys`; Windows `$env:ProgramData\ssh\administrators_authorized_keys` for an admin account.
   - Pin recipe and its tests are project-rag's; issuance is claude-klabauter's.

6. **Verify reach.** From the box holding the G-EM standing, LAN first: on the home network
   verify over the box's LAN address with the tunnel off; try the tunnel address only when the LAN
   address is unreachable (`unimatrix-mechanism.md`, "Transport").
   - SSH no-op, Windows / macOS / Linux alike: `ssh -o BatchMode=yes <box-alias> true; echo $?` (PowerShell: `$LASTEXITCODE`). Expect `0`.
   - Tunnel pin refuses a shell: `ssh -o BatchMode=yes -i <tunnel-key> <box-alias> true` must fail.
   - Tunnel MCP initialize (the port is the tunnel's, carried only over the `Unimatrix-02` key):
     `ssh -N -L 8767:127.0.0.1:8767 <tunnel-alias>` in one shell, then
     `curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8767/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"onboard","version":"0"}}}'`
     (Windows: `curl.exe`; add the bearer-token header if the daemon requires it). Expect `200`.
   - Never route compute or spawning through that port; sessions and jobs use the shell key.

6a. **Optional: Unimatrix cross-account messaging.** Skip when the box shares the primary's
   Claude account: native `/rc` is the first route (`A-SAME-ACCOUNT-CROSS-BOX-USES-NATIVE-RC-FIRST`).
   Check mode first; it refuses outside the verified Claude Code range
   (`A-UNIMATRIX-INSTALL-REFUSES-OUTSIDE-THE-VERIFIED-CLAUDE-RANGE`); `--force` only warns.
   - Windows: `python coordinator\bin\unimatrix-install.py`, then `--install` once it prints `in verified range`
   - macOS / Linux: `python3 coordinator/bin/unimatrix-install.py`, then `--install` once it prints `in verified range`
   - Consumer box (released plugin only): run `python3 "$CLAUDE_PLUGIN_ROOT/bin/unimatrix-install.py"`
     (Windows: `python`) from the installed plugin root, same check-then-`--install` order.
   - Run the install on both boxes of a pair (both directions); either box can hold the network's one G-EM.
   - The relay key follows the custody page (`A-UNIMATRIX-KEY-IS-A-FORCED-COMMAND-RELAY-KEY`).

7. **Record the result.** One line per step, `PASS` / `FAIL` / `GUARDED-STOP`, in the box's
   onboarding handoff. A `GUARDED-STOP` names the engine row it waits on.

## After onboarding

The box appears on the federated roster once claude-klabauter's heartbeat feed lands. Until then a remote
session is unknown, not quiet. The cross-box SendMessage test protocol lives in
`references/multibox.md` ("Cross-box SendMessage"); run it once step 6 passes.
