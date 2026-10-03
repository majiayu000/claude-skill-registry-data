---
name: relay-automation
description: Tick-backed, self-healing automation for the file-based /relay review loop — a hands-free poll driver (poll.sh), a relay-turn supervisor (relay-drive.sh), a liveness watchdog (watchdog.sh), a verdict-gated runner (runner.sh), and headless cross-model turn-takers (`codex-turn.sh`, `agy-turn.sh`). Sibling to the xyz/tick skill; depends on a tick runtime with handoff-exclusive claims. Use to run a Producer↔Reviewer relay with auto turn-taking, stall recovery, and (Option A) headless Codex or agy turns.
---

# relay-automation — sibling skill (bundled package)

Automates the portable `/relay` review loop on top of `tick`: turns pass hands-free
(all-Claude `/loop` poll), a watchdog recovers stalls, and — with the Codex CLI or
Antigravity CLI — a cross-model participant can take its turn **headlessly**
(`codex exec`, `agy -p`). The portable `/relay` skill stays dependency-free; **this**
tick-dependent automation is its sibling.

## Components (in `relay-pkg.tar.gz` beside this file)
| Script | Role |
|---|---|
| `relay-automation/poll.sh` | per-tick poll driver (run under `/loop`): claimability guard + dispatch; `--deadline` self-expiry |
| `relay-automation/relay-drive.sh` | relay-turn supervisor: loop a `RELAY-TURN` token to termination; round-cap + no-progress + close-mismatch escalation |
| `relay-automation/watchdog.sh` | liveness: `tick analyze --format json` → parked `RELAY-TURN` → structured escalation; gated reap stub |
| `relay-automation/runner.sh` | single verdict-gated turn (`VERDICT: PASS\|FAIL\|PARKED`) + artifact-scoped clean-tree gate |
| `relay-automation/codex-turn.sh` | **Option A** headless turn-taker: drives a Codex turn via `codex exec` behind a path-allowlist (no push) |
| `relay-automation/agy-turn.sh` | **Option A** headless turn-taker: drives an agy turn via `agy -p` behind the same path-allowlist boundary (no push) |
| `relay-automation/README.md` | operator usage (`/loop` invocations, self-closing loops, all-Claude boundary) |
| `test/{poll-driver,poll-relay,watchdog-relay,codex-turn,agy-turn}.sh` | the relay-automation suite |

## Dependency — E3 detect-or-extract (capability gate, NOT just presence)
The relay rides the **Phase-1 handoff-exclusive `tick` rule** (a `claim`/`take` of a task
whose `handoff_to` is set and ≠ caller is rejected with **zero events**). A host that has
`tick` but predates that change silently breaks the relay. **Before using, run the gate;**
if it fails, install/patch tick (e.g. via the `xyz` skill, which self-extracts the full
runtime) — then re-run the gate.

```bash
# capability gate — run at repo root after extracting; needs ./bin/tick
gate() {
  local t=./bin/tick d; d="$(mktemp -d)"; TICK_REPO_ROOT="$d" $t init >/dev/null
  TICK_REPO_ROOT="$d" $t log task.created _CAP --agent a >/dev/null
  TICK_REPO_ROOT="$d" $t claim _CAP --agent a --paths "x/**" >/dev/null
  TICK_REPO_ROOT="$d" $t release _CAP --agent a --to b >/dev/null
  local n m; n=$(ls "$d/.tick/events" | wc -l)
  TICK_REPO_ROOT="$d" $t claim _CAP --agent c --paths "x/**" >/dev/null 2>&1   # wrong-handoff: must be rejected, zero events
  m=$(ls "$d/.tick/events" | wc -l); rm -rf "$d"
  [ "$n" = "$m" ] && echo "tick capability OK (handoff-exclusive)" || { echo "FAIL: host tick lacks handoff-exclusive — install/patch tick (xyz skill) first"; return 1; }
}
gate
```

## Install

**Native Claude subscription support requires the full XYZ checkout or the current Tier 1/2
vendored harness** (`xyz-vendor.sh`), which includes the Python runtime under `utils/py/`.
This legacy partial tarball does not contain the Claude/consult adapters or their Python
helpers; extracting it alone does not enable GH-610. Follow the [relay-xyz installation
instructions](../relay-xyz/SKILL.md#concurrent-relays-across-repos-same-machine) for that route.

The relay scripts + tests ship as `relay-pkg.tar.gz` beside this SKILL.md (regenerable
from sources via `make-pkg.sh`). Extract into a repo that already has a capable `tick`
(run the gate first):

```bash
DIR="${1:-.}"                        # target repo root (must contain ./bin/tick)
tar xzf skills/1-hourly/relay-automation/relay-pkg.tar.gz -C "$DIR"
# wire the 4 tests into validate.sh's TESTS=( ... ), then:
cd "$DIR" && bash validate.sh        # the relay-automation tests pass alongside tick's
```

## Usage
See the extracted `relay-automation/README.md` — `/loop` invocations (hands-free relay
turn, designated watchdog poller, single-process supervision), **self-closing loops**
(`--deadline` + self-delete; cron jobs are per-session — always set a deadline), the
**all-Claude boundary** (cross-model stays manual nudge unless driven via `codex-turn.sh`
or `agy-turn.sh`), and the **Option A** headless bring-up paths for Codex and agy
(dispatch-gated, path-allowlisted, no push).
