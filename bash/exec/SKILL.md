---
name: exec
description: 'Run one openclaw CLI call against selected instances through the single audited door Arguments: <selector> -- <openclaw args…> [--json] [--timeout <s>].'
---

# Fleet exec

The escape hatch, and the reason it exists: **a hand-written `docker exec` is forbidden here.** Improvised
container calls skip the redactor, skip the refusals, drop the `-T` that `--json` depends on, and leave no
record of what class of operation ran. Everything goes through `ocexec.py` — the small calls included.

Parse `<selector> -- <openclaw args…> [--json] [--timeout <s>]` from "$ARGUMENTS"; everything after `--`
reaches the CLI verbatim. The contract — modes, standing bans, risk classes, output and exit codes, the
zero-retry set — is `fleet-model/references/exec-contract.md`. Load it before the first call.

## 1. Show the resolved call first
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ocexec.py" <instance> --dry-run -- <openclaw args…>
```
Prints the mode (`hot` in the container, `cold` one-off over the state dir), the risk class and the exact
command line. Anything above R0 stops here: name what it would change and let the operator answer.

## 2. Run it
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ocexec.py" <instance> [--json] [--timeout <s>] -- <openclaw args…>
```
`--json` returns a parsed envelope built from stdout only, plus the exit-code meaning for the commands
whose codes carry one. Both streams are redacted either way, and so is the line `--dry-run` prints.

**Above R0, `--yes` is not enough — the call needs the plan it belongs to.** `--yes` says a human saw
this; it does not say a backup and an executable rollback exist. So a mutation carries `--plan-id`,
minted **and recorded** by the command that already showed the eight blocks (`scripts/lib/gate.py plan
mint <command> <instance> --risk <class>`, from `:repair`, `:update`, `:auth`, `:shared-sync`, `:clone`),
or `--plan <file>`, the rendered plan re-validated here. An id is looked up in that registry: it must
name this instance, cover this class, still be inside its TTL, and it is **burned on use** — one plan
authorises one mutation. No plan exists yet? The operation belongs in the command that builds one.

`models auth …` also takes the fleet-wide `fleet-auth` lock for its duration, because the runtime's own
lock is per state directory and serialises nothing across instances; a procedure already holding it
passes `--lock-token <t>`. Reads fan out freely; above R0 go one instance at a time, canary first.

## 3. When it refuses
Exit `64` refused by policy · `65` unknown or unusable instance · `66` no docker. The refusal names the
rule. **Do not route around it** — not with `docker exec`, not by switching `--mode`, not by retrying, and
never by adding `--accept-capabilities`: upstream made it ungrantable by automation, so this plugin prints
it for a human. All refusals are tabled in `exec-contract.md`; these are the ones that surprise people:

| Refused | Because | Go to |
|---|---|---|
| alien instance, or `manage:false` | it failed the layout fingerprint or the operator excluded it | fix the fleet config, or leave it alone |
| `models status --probe` on a live gateway | the probe needs the gateway stopped | `--check` for monitoring |
| R3/R4 argv | needs a backup or a typed confirmation, which only a plan-building command collects | `:repair`, `:update`, `:auth` |
| a plan id never issued, expired, or already used | the id is a record, not a shape | show the plan again, use the id it mints |

## Scope
One CLI call, not a procedure. A named repair belongs in `/openclaw-ops:repair` with a finding id; an
upgrade in `/openclaw-ops:update`; a login in `/openclaw-ops:auth`, which prints interactive logins rather
than running them. Confirm a subcommand's spelling against this instance's own `--help` before quoting
it — verbs drift between versions, and the retry budget for auth, upgrades and installs is zero.