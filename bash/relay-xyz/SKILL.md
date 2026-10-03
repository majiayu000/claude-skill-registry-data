---
name: relay-xyz
description: >-
  Drive an automated /relay review loop on THIS repo with the shipped
  relay-automation harness (relay-drive.sh + codex-turn.sh / agy-turn.sh /
  poll.sh) rather than improvising the handoff by hand. Use when the operator
  wants to "run an automated relay", "have Codex or agy review this
  end-to-end", "drive a relay to completion headless", "run the relay harness",
  or set up the all-Claude hands-free poll loop — and the working tree is a
  clone of the xyz-3-agents-swarm repo (it ships relay-automation/). /relay
  scaffolds the thread and owns the turn protocol; relay-xyz is the repo-specific
  layer that runs the real scripts. NOT for scaffolding a thread from scratch
  (that is /relay), NOT for repos without relay-automation/.
---

# relay-xyz — automated relays on the shipped harness

**ALWAYS locate and run the bundled locator first — never claim the harness is missing without it.**
Resolve the installed skill from stable install roots; do not assume the session CWD is this repo:

```bash
L=""
for candidate in "${XYZ_HARNESS:+$XYZ_HARNESS/skills/1-hourly/relay-xyz/find-harness.sh}" \
                 "$HOME/.claude/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.codex/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.gemini/config/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.gemini/antigravity/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.gemini/antigravity-cli/skills/relay-xyz/find-harness.sh" \
                 "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/relay-xyz/find-harness.sh" \
                 "$(git rev-parse --show-toplevel 2>/dev/null)/skills/1-hourly/relay-xyz/find-harness.sh"; do
  [ -n "$candidate" ] && [ -f "$candidate" ] && { L="$candidate"; break; }
done
[ -n "$L" ] || { echo "relay-xyz: locator not found — install the skill or set XYZ_HARNESS" >&2; exit 1; }
bash "$L" --check
```

That locator resolves the harness from wherever your CWD is and reports which workers
(tick/codex/agy/cmd/dsh) are on PATH. See
[Preconditions](#preconditions--locate-the-harness-bundled-locator-never-hardcode-a-path) below for the
full env-exporting form (`eval "$(... --env)"` + `cd`) that every recipe in this doc assumes has already
run.

This repo **already ships** the relay automation. Don't reinvent the CLI handoff turn by turn — call
the scripts under [`relay-automation/`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/relay-automation/). `/relay` defines the thread format
and turn protocol and scaffolds the dated file; **`relay-xyz` is the thin repo-specific layer that
drives that thread to completion with the shipped supervisor + turn-takers.**

Use `/relay` to *create* the thread (or reuse one under `relay-system/<date>/`), then `relay-xyz` to
*run* it headless or hands-free.

## When to use

- "Run an automated relay" / "drive this relay to completion" / "run the relay harness."
- "Have Codex or agy review `<file>` end-to-end."
- Setting up the all-Claude hands-free `/loop` poll so two Claude windows self-serialize.
- Running automated relays in **two different repos at the same time on one machine** — see
  [Concurrent relays across repos](#concurrent-relays-across-repos-same-machine) (each repo needs its own
  vendored `.xyz/`).
- You have a relay thread (or are about to scaffold one with `/relay`) **and** the working tree is a
  clone of this repo.

**Not** for: scaffolding a brand-new thread from scratch (that's `/relay`), repos that don't ship
`relay-automation/`, or work that needs a human checkpoint between every turn (use plain `/relay`
manual mode).

## First-time setup on a new clone or machine (make the skill discoverable)

This repo keeps its skills in top-level `skills/`, which Claude Code does **not** scan. A session
finds `relay-xyz` only if it's symlinked into `~/.claude/skills/`. A fresh clone or second machine has
no such symlink, so the skill is invisible in **every** session there — the "other VS Code sessions
can't find the relay-xyz files" failure. Fix it **once per clone** (idempotent, self-locating, no
hardcoded path):

```bash
bash skills/1-hourly/relay-xyz/install.sh   # symlinks this clone's skills/1-hourly/relay-xyz into ~/.claude/skills/
```

It also replaces a stale/dangling symlink and verifies `find-harness.sh` resolves the harness. The
locator below handles *where the harness scripts live*; this step handles *whether Claude Code can
load the skill at all* — a layer the locator can't reach, since it runs only after the skill loads.

## Preconditions — locate the harness (bundled locator, never hardcode a path)

`relay-xyz` ships its own device-agnostic locator, [`find-harness.sh`](find-harness.sh), beside this
skill. It resolves the harness repo (the clone that ships `relay-automation/`) **relative to its own
installed location**, following symlinks — so it works from *any* working directory, including a clone
that has only `relay-system/` thread storage (from `/relay`) but **not** the harness scripts. `$HOME`
and the skill's own symlink are the only anchors; **no machine path is ever hardcoded.** That's what
keeps relay-xyz from "complaining the harness isn't in this repo" when you launch it from a clone
without `relay-automation/` + `bin/tick`.

Run this first. It finds the locator, exports the harness env, `cd`s into the clone that ships the
harness, and prints a one-glance readiness line:

```bash
# Find the bundled locator. The skill installs at one of these — all anchored on $HOME or
# the CWD, never an absolute machine path:
for L in "${XYZ_HARNESS:+$XYZ_HARNESS/skills/1-hourly/relay-xyz/find-harness.sh}" \
         "$HOME/.claude/skills/relay-xyz/find-harness.sh" \
         "$HOME/.codex/skills/relay-xyz/find-harness.sh" \
         "$HOME/.gemini/config/skills/relay-xyz/find-harness.sh" \
         "$HOME/.gemini/antigravity/skills/relay-xyz/find-harness.sh" \
         "$HOME/.gemini/antigravity-cli/skills/relay-xyz/find-harness.sh" \
         "./.claude/skills/relay-xyz/find-harness.sh" \
         "$(git rev-parse --show-toplevel 2>/dev/null)/skills/1-hourly/relay-xyz/find-harness.sh"; do
  [ -n "$L" ] && [ -x "$L" ] && break
done
[ -x "$L" ] || { echo "relay-xyz: locator not found — set XYZ_HARNESS to your xyz-3-agents-swarm clone"; exit 1; }

eval "$("$L" --env)"   # exports HARNESS, TICK, TICK_REPO_ROOT, RELAY_HAS_{TICK,CODEX,AGY,COMMANDCODE,DEEPSEEK}
cd "$HARNESS"
"$L" --check           # prints: harness path + which Path-A workers (tick/codex/agy/cmd/dsh) are on PATH
```

After this, `$HARNESS` is the harness repo root, `$TICK` is the absolute `bin/tick`, and
`TICK_REPO_ROOT` points `tick` at that clone's event log. The relay/turn scripts self-resolve their
own location (`$(dirname "$BASH_SOURCE")/..`), so invoke them with **repo-relative** paths exactly as
the [relay automation README](https://github.com/HiQS-Labs/XYZ-forge/blob/development/relay-automation/README.md) shows.
The relay always operates on **the
harness clone** (its `.tick/` log and guarded git root live there), whatever repo you launched from —
so a clone with only `relay-system/` thread files still drives the real harness next door.

## Concurrent relays across repos (same machine)

`relay-drive.sh`/`marathon-drive.sh` hold **one global driver lock per harness clone**. This is
intentional — two worktrees on the same `ROOT@HEAD` can corrupt git state (GH-42) — but it means
**every repo pointed at the same harness clone shares that one lock**, so their automated relays
*serialize*: a second one blocks (`exit 1`) until the first frees.

### The driver-lock exclusion matrix (GH-354 Phase 3 — canonical)

> This table is the **one canonical statement** of what the driver lock guarantees (PDDA Principle #4).
> Anything else that describes the lock — driver headers, monitor docs — links here rather than
> restating it. A second copy is how the wrong sentence in `marathon-drive.sh:194-196` survived.

Both drivers resolve the lock through **one shared resolver** (GH-448) — `utils/py/rtl.py::driver_lock_path`
and its Bash twin `relay-automation/driver-lock-lib.sh::driver_lock_path_for_repo` — which yields three
shapes:

| Repo shape | Lock path | Display label |
|---|---|---|
| normal clone (`.git` is a directory) | `<root>/.git/relay-driver.lock` | `.git/relay-driver.lock` |
| **linked worktree** (`.git` is a file) | `<git-common-dir>/relay-driver.lock` — i.e. **the parent clone's** | `.git/relay-driver.lock` |
| vendored `.xyz/` (no `.git`) | `<root>/.relay-driver.lock` | `.relay-driver.lock` |

The middle row is the load-bearing one: **a linked worktree does not get its own lane.** It resolves
to the same lock as the clone it was cut from — pinned by `test/gh448-driver-lock-resolver.sh`
(*"worktree case resolves to the git COMMON dir, not `<worktree>/.git/…`"*, plus a bash/python
*"parity"* assertion per shape). So all three driver pairs mutually exclude *per clone*:

| Pair | Excludes? | Pinned by |
|---|---|---|
| marathon ↔ marathon | **yes** | `test/driver-lock.sh` — *"live lock (alive holder) → driver refuses (exit 1)"*, *"live lock left intact (not stolen)"* |
| marathon ↔ relay | **yes** | `test/gh376-relay-drive-lock-parity.sh` — *"THE PIN (bash): relay-drive.sh refuses — the frozen twin agrees with the Python half"* |
| relay ↔ relay | **yes** | `test/gh376-relay-drive-lock-parity.sh` — *"neither lane left a worktree-local lock behind at `$WT/.relay-driver.lock`"*, *"twin parity: both lanes emit a byte-identical REFUSAL"* |

**This became true only in GH-376.** Before it, `relay-drive` used a two-branch guess with no case for
a linked worktree, so it took a *per-worktree* `.relay-driver.lock` while `marathon-drive` took the
shared one — the bottom two rows did **not** exclude, and #354's original premise that the lock was
"the hard blocker (by design)" was false for them. The negative control
(*"pre-fix 2-branch logic sails past the held lock"*) is what pins that it can't return.

**To actually run two swarms concurrently, use separate full clones** — not linked worktrees, which
share the lock by the table above, and not a shared harness, which serializes. Per-run hygiene that
keeps the event stream readable even across clones: distinct `--phase-id` / `--relay-task`, plus
`MARATHON_LANE_NS` for the lane namespace and an explicit `XYZ_SESSION_ID` (its fallback to `PHASE_ID`
cannot tell one run from another).

To run relays in **different repos at the same time on one machine**, give each repo its **own harness**
so each gets its own lock, `.tick/`, and worktrees:

| Install path / Tier | Ships | Relay capability | Releases ledger? | Lock |
|---|---|---|---|---|
| `install.sh` (tick-only) | `bin/tick` + `src/*.js` | ❌ falls back to the centralized harness | ❌ no | shared (serializes) |
| **Tier 1 (default)**: `xyz-vendor.sh <target-repo> [--no-register]` | full core harness (`relay-automation/` minus `xyz-releases-onboard.sh`, `bin/`, `src/`, `test/`, `skills/`, `utils/` minus overlay) into gitignored `.xyz/` | ✅ per-repo | ❌ no overlay | **own** `.xyz/.relay-driver.lock` |
| **Tier 2 (opt-in)**: `xyz-vendor.sh <target-repo> --with-releases` (or auto-detected via `releases.db` at root) | full core harness + RELEASES overlay (`releases_app.py`, `releases_cycle.py`, `releases-merge-resolve.sh`, `release-lanes.sh`, `utils/timeline/`, `xyz-releases-onboard.sh`, `RELEASES-DB-FAQS.md`) | ✅ per-repo | ✅ opt-in overlay | **own** `.xyz/.relay-driver.lock` |

Updating a vendored copy (`xyz-sync.sh update`, or re-running `xyz-vendor.sh` over an existing
`.xyz/`) replaces the harness **code** and preserves the per-repo state above — `relay-system/`,
`.tick/`, `.relay-driver.lock`, and the `XYZ.json*` telemetry ride across the rebuild (GH-312).
Note that RELEASES ledger runtime state (`releases.db`, `releases.sql`,
`RELEASES-PREVIEW.html`) lives at the target repository root, outside `.xyz/`, while `.xyz/`-resident
runtime state is preserved across swaps. This matters because `.xyz/` is gitignored: state lost there
is unrecoverable, with no reflog or stash behind it. A new runtime artifact under `.xyz/` must be added
to the preserve list in `xyz-vendor.sh`'s `materialize_vendor()`, or the next update will delete it.

So: **`xyz-vendor.sh` (not `install.sh`) is the path to concurrent per-repo relays.** Once a repo has
`.xyz/`, `find-harness.sh` prefers it automatically (env → `.xyz/` → current repo → script-relative), and
`find-harness.sh --check` **warns** when you're in a foreign repo with no `.xyz/` (using the shared
harness) and points you at the vendor command. Two vendored repos each run `relay-drive.sh` from their
own `.xyz/relay-automation/`, holding independent locks — no contention. (Editing the central harness
clone also can't disturb a vendored run, since it uses its own pinned `.xyz/` copy.)

## Per-repo persistence (don't cache a path)

Once a target repo has used relay-xyz once, don't leave behind a machine-specific breadcrumb so the
next session skips the "run `find-harness.sh` first" gate above. The only two persistence channels
Claude Code **auto-loads** are:

- **The target repo's memory** — seed a line the first time a run succeeds there, e.g. "this repo uses
  relay-xyz; run `find-harness.sh --check` first."
- **That repo's own `CLAUDE.md`, by skill name** — a pointer such as "for automated relays, use the
  `relay-xyz` skill" (not a path).

Either breadcrumb must be a **portable pointer** — the skill name or the `find-harness.sh` command —
**never a cached absolute path and never a bare root pointer file** dropped into the target repo. A
bare file isn't auto-loaded (a skimming agent skips it exactly like it skips this doc's own body), it's
machine-specific (breaks on the next clone or device), a stale cached path is *worse* than no path at
all, and cleaning one up later has cross-repo blast radius. **relay-xyz never auto-installs any file
into a target repo** — only `install.sh` writes anything, and it writes only into `~/.claude/skills/`
on the machine running it, never into the target repo itself.

## The two automated paths

**Role split (GH-221): Claude Code is the orchestrator/reviewer here, not a default builder.** The
Claude Code session driving `relay-drive.sh`/`marathon-drive.sh` plans, dispatches, and reviews/verifies
turns — it does not spawn itself as the headless build lane. **Agy CLI and Codex CLI are the builders**:
the two cost-blind (subscription-billed, not per-call API) headless turn-takers `--agent-cmd` /
`--builder` default to. **Claude CLI (subscription or API, according to authentication) is not a builder by default** —
`--builder claude` / a `claude-turn.sh` shim stay fully supported, but only as an explicit,
usage-acknowledged choice the *user* makes locally, never something a session reaches for on its own
reasoning that it's "just another supported turn-taker." If a task needs a headless build lane and
neither agy nor codex is on PATH, stop and ask — don't default to spawning a headless Claude CLI turn.

| Path | One session? | Models | Driver |
|---|---|---|---|
| **A. Headless single-session** | yes — Claude drives both roles | Codex / agy as co-equal headless workers | `relay-drive.sh` + a turn-taker shim |
| **B. Hands-free poll** | no — two live Claude windows | all-Claude | `poll.sh` under `/loop` in each window |

Path A is the marquee flow — what "have Codex or agy review this for me" means. Path B is the all-Claude
self-serializing loop: no human nudge, no second model.

### Path A — headless single-session (relay-drive.sh + a shim)

`relay-drive.sh` is the **supervisor** (round cap, no-progress escalation, reads the file's `STATUS:`
as the terminal signal). The **turn-taker** is `--agent-cmd` — a shipped shim (`codex-turn.sh` or
`agy-turn.sh`) that owns the safety boundary: path-allowlist, commit-bypass guard, **no push**.
Whose-turn is a `tick` relay task, handed off with `tick release --to`.

End-to-end headless review of an artifact (run after Preconditions — `$TICK` and `$HARNESS` set, CWD
is the harness clone). Choose either worker. The examples below pass `ALLOW_PATHS="$ARTIFACT"`, which
fits a **build/fix** turn; for a pure **review** turn set `ALLOW_PATHS=""` (relay file only) so the
reviewer reports instead of editing — see the env table's `ALLOW_PATHS` row (note that fixed log paths break concurrent same-machine runs; prefer the shims' per-PID default or use per-PID `$$` variables):

#### The one-line form (GH-346 Phase 3a) — name the reviewer, skip the table

If a profile exists for the model you want, the whole env block below collapses to one call:

```bash
eval "$(relay-automation/resolve-profile.sh 'glm 5.3 max' --env)"
ALLOW_PATHS="" relay-automation/relay-drive.sh \
  --relay-file "$RELAY" --relay-task "$TASK" \
  --agent-cmd "$RELAY_AGENT_CMD" --reviewer "$RELAY_REVIEWER" --review-once
```

`--env` emits the lane's `*_AGENT`, `*_MODEL`, its gateway variable, `*_REASONING_EFFORT`,
`*_FLAGS`, plus `RELAY_AGENT_CMD`, `$HARNESS` and `$TICK`. Profiles live in the `profiles` block of
`~/.xyz/device_config.json`:

```json
"profiles": {
  "glm 5.3 max":  { "harness": "commandcode", "gateway": "self",
                    "model": "zai-org/glm-5.3", "effort": "max" },
  "qwen 3.8 max": { "harness": "deepseek", "gateway": "openrouter",
                    "model": "qwen/qwen3.8-max" }
}
```

`"gateway": "self"` is for a harness that is **its own router** — Command Code resolves models from
its own catalog and has no OpenRouter key or base URL, so naming a third-party router there would
emit a value the shim ignores and telemetry would then record a route that never happened.

Name matching is fuzzy (it reuses `resolve-model-alias.sh`), so `GLM5.3 max`, `glm 5.3 max` and
`max glm 5.3` are one entry. `--list` shows every profile and flags broken ones; `--explain` says
which tier answered.

**This never blocks a turn.** A missing config, malformed JSON, or an unmatched name falls through
to the shims' own defaults — the tables below — and says why on stderr. An explicit `*_AGENT` +
`*_MODEL` already in the environment always wins and is never second-guessed.

The tables below remain correct and are what a fall-through lands on. Use them when no profile
exists, or when you want a one-off that is not worth naming.

| Worker | Availability check | Handoff target | Env prefix | Shim | Log |
|---|---|---|---|---|---|
| Codex | `"$RELAY_HAS_CODEX" = 1` | `codex` | `CODEX_AGENT=codex ALLOW_PATHS="$ARTIFACT" CODEX_LOG="${TMPDIR:-/tmp}/codex-turn-$$.log"` | `relay-automation/codex-turn.sh` | `${TMPDIR:-/tmp}/codex-turn-$$.log` |
| agy | `"$RELAY_HAS_AGY" = 1` | `agy` | `AGY_AGENT=agy ALLOW_PATHS="$ARTIFACT" AGY_LOG="${TMPDIR:-/tmp}/agy-turn-$$.log"` | `relay-automation/agy-turn.sh` | `${TMPDIR:-/tmp}/agy-turn-$$.log` |
| Commandcode | `"$RELAY_HAS_COMMANDCODE" = 1` | `commandcode` | `COMMANDCODE_AGENT=commandcode ALLOW_PATHS="$ARTIFACT" COMMANDCODE_LOG="${TMPDIR:-/tmp}/commandcode-turn-$$.log"` | `relay-automation/commandcode-turn.sh` | `${TMPDIR:-/tmp}/commandcode-turn-$$.log` |
| DeepSeek | `"$RELAY_HAS_DEEPSEEK" = 1` | `deepseek` | `DEEPSEEK_AGENT=deepseek ALLOW_PATHS="$ARTIFACT" DEEPSEEK_LOG="${TMPDIR:-/tmp}/deepseek-turn-$$.log"` | `relay-automation/deepseek-turn.sh` | `${TMPDIR:-/tmp}/deepseek-turn-$$.log` |

**Model selection per worker** (GH-346) — the one lookup that used to mean reading each shim's
source. `RELAY_HAS_*` is set by `find-harness.sh --env`; every worker below also honors
`<PREFIX>_FLAGS` and `RELAY_TURN_TIMEOUT_S`:

| Worker | Model env | Default | Notes |
|---|---|---|---|
| Codex | *(none)* | codex CLI's own | `codex-turn.sh` never passes `--model`; set it in codex's own config |
| agy | `AGY_MODEL` | agy CLI's own | validated against `agy models` — an unlisted id fails fast rather than falling back |
| Commandcode | `COMMANDCODE_MODEL` | `meta/muse-spark-1.2-contributor` | `cmd --list-models` for the live catalog (GLM, Qwen, DeepSeek all reachable here) |
| DeepSeek | `DEEPSEEK_MODEL` | `deepseek/deepseek-v4-pro` | accepts a colloquial alias (`"deepseek v4 pro"`); also `DEEPSEEK_PROVIDER` (`openrouter`\|`deepseek`\|`alibaba`) selecting the endpoint and its key variable. An unrecognised value REFUSES the turn (it used to fall through to DeepSeek silently). `alibaba` is the Alibaba Token Plan, which serves Qwen under bare ids (`qwen3.8-max`, not `qwen/...`) and reads its key from `ALIBABA_TOKEN_PLAN_API_KEY` or, failing that, the file named by `ALIBABA_TOKEN_PLAN_API_KEY_FILE`. |
| Aider | `AIDER_MODEL` | `openrouter/anthropic/claude-sonnet-5`, or `openai/agents-a1` when `AIDER_OPENAI_API_BASE` is set | force `AIDER_FLAGS=--edit-format diff` on GLM |
| Claude | `CLAUDE_MODEL` | `claude-sonnet-4-6` | Explicit operator choice, never a session default; see [subscription setup](https://github.com/HiQS-Labs/XYZ-forge/blob/development/relay-automation/README.md#claude-subscription-mode) |
| Pi | `PI_MODEL` | **none — required** | refuses to guess (GH-295) |

Codex example:

```bash
# 0. The reviewer you want must be on PATH (set by the locator).
[ "$RELAY_HAS_CODEX" = 1 ] || { echo "codex not on PATH — use agy or Path B"; exit 1; }

# 1. Have a relay thread with an embedded "▶ TAKE YOUR TURN" block.
#    Reuse one under relay-system/<date>/, or scaffold a fresh thread with /relay first.
RELAY=relay-system/<date>/<slug>.md
ARTIFACT=<repo-relative-path-the-turn-reviews>     # e.g. skills/1-hourly/relay-xyz/SKILL.md
TASK="RELAY-$(basename "$RELAY" .md)"              # use a per-relay id, not literal RELAY-TURN

# 2. Seed the relay task and hand the first turn to the Codex agent.
"$TICK" log     task.created "$TASK" --agent claude-a
"$TICK" claim   "$TASK" --agent claude-a --paths "$ARTIFACT"
"$TICK" release "$TASK" --agent claude-a --to codex

# 3. Drive it. The shim dispatches ONLY when the token's actor == CODEX_AGENT.
CODEX_AGENT=codex ALLOW_PATHS="$ARTIFACT" CODEX_LOG="${TMPDIR:-/tmp}/codex-turn-$$.log" \
relay-automation/relay-drive.sh \
  --relay-file "$RELAY" \
  --relay-task "$TASK" \
  --agent-cmd  relay-automation/codex-turn.sh \
  --reviewer   "$CODEX_AGENT" \
  --round-cap  4
```

agy example:

```bash
[ "$RELAY_HAS_AGY" = 1 ] || { echo "agy not on PATH — use codex or Path B"; exit 1; }

RELAY=relay-system/<date>/<slug>.md
ARTIFACT=<repo-relative-path-the-turn-reviews>
TASK="RELAY-$(basename "$RELAY" .md)"

"$TICK" log     task.created "$TASK" --agent claude-a
"$TICK" claim   "$TASK" --agent claude-a --paths "$ARTIFACT"
"$TICK" release "$TASK" --agent claude-a --to agy

AGY_AGENT=agy ALLOW_PATHS="$ARTIFACT" AGY_LOG="${TMPDIR:-/tmp}/agy-turn-$$.log" \
relay-automation/relay-drive.sh \
  --relay-file "$RELAY" \
  --relay-task "$TASK" \
  --agent-cmd  relay-automation/agy-turn.sh \
  --reviewer   "$AGY_AGENT" \
  --round-cap  4
```

Commandcode example:

```bash
[ -x "$(command -v cmd 2>/dev/null)" ] || { echo "cmd not on PATH — use codex or agy"; exit 1; }

RELAY=relay-system/<date>/<slug>.md
ARTIFACT=<repo-relative-path-the-turn-reviews>
TASK="RELAY-$(basename "$RELAY" .md)"

"$TICK" log     task.created "$TASK" --agent claude-a
"$TICK" claim   "$TASK" --agent claude-a --paths "$ARTIFACT"
"$TICK" release "$TASK" --agent claude-a --to commandcode

COMMANDCODE_AGENT=commandcode ALLOW_PATHS="$ARTIFACT" COMMANDCODE_LOG="${TMPDIR:-/tmp}/commandcode-turn-$$.log" \
relay-automation/relay-drive.sh \
  --relay-file "$RELAY" \
  --relay-task "$TASK" \
  --agent-cmd  relay-automation/commandcode-turn.sh \
  --reviewer   "$COMMANDCODE_AGENT" \
  --round-cap  4
```

`$TICK` is absolute, so either worker path still works if CWD drifts.

**Important — run the shim OUTSIDE the Bash sandbox.** When *you* (Claude Code) drive this, the
`codex` / `agy` subprocess needs the OS keychain + outbound network to authenticate. Claude Code's
Bash sandbox blocks both: `codex` errors (looks like a keychain/login fault, but it's the sandbox),
and `agy -p` **fails silently — exit 0, empty output** (the shim catches this and exits 5, but only
un-sandboxed). Run these Bash calls with `dangerouslyDisableSandbox: true`. (Memory:
`codex-cli-needs-sandbox-disabled`, `agy-antigravity-cli`.)

**Important — never hand-roll backgrounding for a driven run (GH-183/187 dogfood, 2026-07-10).** A
multi-round `marathon-drive.sh`/`relay-drive.sh` run can easily exceed the calling tool's own
foreground timeout. Always use that tool's **native** background-execution mechanism (e.g. Claude
Code's `run_in_background`), never a manual `nohup ... & disown` — a disown can itself fail (exit
1) while the backgrounded job survives anyway, undetected, and races a subsequent re-fire against
the same repo/worktree state (observed: a stray `git worktree` plus a `tick` token stuck in
`claimed`, never handed off). If a driver call *does* get killed mid-turn: `git worktree remove
--force <path>` (see `git worktree list` for stragglers) then `tick reap <agent> --by <caller>
--task <task>` to clear the stuck claim — `reap` is the sanctioned recovery (logs an auditable
`task.released` event), not a hand-written `tick release`.

#### Inspecting token state, and a one-shot review

- **Inspect whose-turn mid-drive:** `"$TICK" info <task>` prints the token's `status` / `claimer` /
  `handoff-to` (this is what the driver reads internally). The verb is **`info`**, not `status` —
  `tick status` is not a verb and errors with `unknown verb: status`.
- **Single deliberate review turn:** pass `--review-once` to `relay-drive.sh` to drive exactly ONE
  turn and classify the outcome by exit code, so a correct "changes requested" review is not mistaken
  for a stall:

  | Exit | Meaning |
  |---|---|
  | `0` | reviewer Approved/Closed |
  | `5` | reviewer completed a turn and handed back **without** approving ("changes requested") — a *successful* single review, not a stall |
  | `3` | genuine stall — the reviewer did nothing (token + STATUS unchanged) |
  | `4` | escalated by design (`STATUS: Escalated`), round cap, or a close mismatch |

  Without `--review-once` a non-approval handback advances the multi-round loop instead (the producer
  takes the next turn); use `--review-once` when you want exactly one review and a clean exit code.

- **Review an external / cross-repo artifact (a PR or diff from another repo):** pass
  `--artifact-file <path>` to `relay-drive.sh` to seed it READ-ONLY into the isolated worktree at
  `.relay-artifacts/<basename>` — the reviewer reads it there without it being committed into the
  target repo (a reviewer edit fails the turn). To scaffold the thread for such a review, use
  `relay-automation/new-relay.sh --title T --reviewer <agent> --artifact-file <path>` (add `--embed`
  to inline the artifact in a fence-collision-safe block instead of referencing the seed path). The
  scaffolder only writes a thread; you still drive it with `relay-drive.sh` per the paths above.

- **Drive a full relay/build that lands in a DIFFERENT repo (`--target-root`):** the *normal* case —
  the harness lives in `xyz-3-agents-swarm`, the code you want built or reviewed-and-committed lives in
  your own repo. Pass `--target-root <repo>` to `relay-drive.sh` (or `marathon-drive.sh`): the relay
  thread + `tick` token stay in the harness clone, while the worktree base, `ALLOW_PATHS` resolution,
  and the file-scoped commit all route to `<repo>` (the harness clone is never touched). `find-harness.sh`
  (Preconditions) solves discovery of *the harness*; `--target-root` is the inverse — pointing the
  harness **at** your repo. **A same-repo lane must OMIT `--target-root`** — passing it for the harness's
  own repo trips a relay-file off-lane false-positive (exit 6; see [#51](https://github.com/Claude-AI-Tools-Ventura-County/xyz-3-agents-swarm/issues/51)).

- **One-shot cross-repo review without a relay loop (`CONSULT_ROOT`):** to apply a lens to a file in a
  foreign repo with Codex/agy headless — no Producer↔Reviewer loop, advisory only — reach for
  `consult.sh` with `CONSULT_ROOT` set to that repo. Advisors run in a throwaway worktree of
  `CONSULT_ROOT`, so they read it but can never mutate it:
  ```bash
  CONSULT_ROOT=/path/to/your/repo \
  relay-automation/consult.sh --models codex \
    --prompt-file /abs/path/Q.md --out "$TMPDIR/consult"
  ```
  **`$TMPDIR` gotcha:** when a prompt/artifact is *authored* in a sandboxed step and *consumed*
  un-sandboxed (or vice-versa), `$TMPDIR` resolves to a different dir and the path 404s
  (`prompt file not found`). Pass prompts/artifacts by **absolute path**, never a bare `$TMPDIR`-relative one.

### Path B — hands-free poll (all-Claude, two windows)

In each Claude window, run a guarded `/loop` that uses `poll.sh` as the gate, then take the turn from
the relay file's embedded instructions. The token *is* the lock — a window acts only when the token is
claimable by its agent **and** the artifact scope is clean.

Each window is its own shell, so run Preconditions in each one (or `cd` into the `find-harness.sh
--root` output) before the loop — the `relay-automation/` paths below are relative to `$HARNESS`.

```
# In each window (set --agent to that window's id). --claude-agents lists EVERY Claude id in
# the relay so the poller knows whose turns can self-poll vs. which need a cross-model nudge:
/loop 60s run relay-automation/poll.sh --mode relay --agent <claude-a|claude-b> \
  --claude-agents "claude-a,claude-b" \
  --relay-file relay-system/<date>/<slug>.md --artifact <path> \
  --deadline "$(date -v+30M +%s)" --dry-run ;\
  if it prints "DECISION: run-runner", take your turn on that relay file per its embedded \
  instructions (review/produce, append your block, `tick release RELAY-TURN --to <other>` or \
  `tick done` on approve, commit); on "DECISION: stop" CronList+CronDelete this job; else do nothing.
```

`--claude-agents` is load-bearing: a turn belonging to an agent **not** in this list yields
`DECISION: nudge-cross-model` (a one-line "take your turn" for the human to relay to a non-Claude
window), not `idle`. List both Claude ids and Path B stays fully hands-free; omit one and that
window's turns surface as a manual nudge. `60s` keeps the prompt cache warm; the lock/heartbeat is the
real correctness guard, not the timer. Always set a `--deadline` so the loop self-closes — cron jobs
are per-session, and you can't stop another window's loop from yours. `poll.sh` exits `10` on a closed
relay (`STATUS: Approved|Closed`); see `/relay` → "Self-closing loops". Optionally run **one** extra
window with `--watchdog-authority` (longer interval, e.g. `120s`) so a stalled turn escalates exactly
once.

**Worked recipe — "Dueling Claudes":** for the full copy-paste two-window setup (Reporter↔Maintainer,
same machine, with the one human go-gate before commit), see
[relay-automation/DUELING-CLAUDES.md](https://github.com/HiQS-Labs/XYZ-forge/blob/development/relay-automation/DUELING-CLAUDES.md). It carries the exact
`/loop` strings, the fresh-token-per-run rule, and the foreign-CWD `tick` pitfalls for Path B.

### Path B cadence — fixed interval (today) vs adaptive (GH-33)

The `/loop 60s` above is a **fixed** cadence: it wakes every 60s and usually decides "do nothing,"
burning a re-invocation per idle minute. **Adaptive cadence** lets `poll.sh` suggest *when* to wake
next from its own `DECISION`:

- `poll.sh --emit-delay` adds a `DELAY: <seconds> (<reason>)` line (act-now → 0, idle backoff → 300,
  dirty → 30, waiting-for-peer-commit → 90, cross-model → 120; clamped to `--deadline`). Additive —
  the `DECISION:` line is unchanged, so the fixed `/loop 60s` recipe above still works untouched.
- `relay-automation/relay-loop.sh` wraps it. **Default** = one tick that prints `NEXT-POLL: <seconds>`
  and exits `poll.sh`'s code (10 = stop) — the unit a `/loop` **dynamic-mode** tick reads to schedule
  its next wake (via `ScheduleWakeup`), so an idle relay backs off and a live one stays responsive.
- The cadence is **not** Claude-locked: `relay-loop.sh --sleep-loop` self-paces in pure bash
  (tick → sleep `DELAY` → repeat until stop), and the `NEXT-POLL`/`DELAY` output is plain text any
  scheduler (cron, systemd timer) can consume. `/loop` dynamic mode is one option, not a dependency.

Dynamic-mode `/loop` (self-paced) replacement for the fixed recipe — read `NEXT-POLL`, sleep that long:

```
/loop run relay-automation/relay-loop.sh --mode relay --agent <claude-a|claude-b> \
  --claude-agents "claude-a,claude-b" --relay-file relay-system/<date>/<slug>.md \
  --artifact <path> --deadline "$(date -v+30M +%s)" --dry-run ;\
  act on "DECISION: run-runner" as above; on "DECISION: stop" CronDelete this job; \
  otherwise ScheduleWakeup after the printed "NEXT-POLL:" seconds.
```

## Turn-taker shims & their env

Both shims are thin dispatchers over `relay-turn-lib.sh` (the model-agnostic containment core), so
they share the same env shape:

| Env | `codex-turn.sh` | `agy-turn.sh` | Meaning |
|---|---|---|---|
| dispatch gate | `CODEX_AGENT` | `AGY_AGENT` | NO-OPS unless `RELAY_AGENT == this` |
| extra writable paths | `ALLOW_PATHS` | `ALLOW_PATHS` | comma-sep git paths the turn may change (the relay file is always allowed). **For a review turn, set `ALLOW_PATHS=""` — relay file only.** If the artifact is writable, the reviewer tends to start *editing and building* it instead of reviewing (it can read any path regardless), which over-runs the turn cap (exit 7) — observed 2026-06-26. A build/fix turn is the only case that needs the artifact in `ALLOW_PATHS`. **A whole DIRECTORY is a valid lane entry** (GH-90): an entry that names an existing directory, or any entry written with a **trailing slash** (`skills/1-hourly/standup/fixtures/` — the only form that works when the turn is about to *create* the directory), makes that directory and everything beneath it writable. Without either signal the entry is a FILE path, and a file entry is never a bare prefix — GH-59: `green` must not reach `greenfield/output.txt`. Before GH-90 a bare directory entry was unmatchable by construction and the turn failed as a *containment violation*, which reads as a misbehaving builder rather than a malformed lane spec; the off-lane report now names that mistake explicitly. |
| peer id | `RELAY_PEER` | `RELAY_PEER` | so the turn hands off `--to <peer>` (else "the other agent") |
| binary | `CODEX_BIN` | `AGY_BIN` | override the CLI path |
| autonomy | `CODEX_FLAGS` (default `-s workspace-write`) | `AGY_MODEL` / `AGY_FLAGS` | the codex sandbox/approval flags or the agy model |
| transcript | `CODEX_LOG` | `AGY_LOG` | where the CLI transcript lands (default a `$TMPDIR` file) |
| turn ceiling | `RELAY_TURN_TIMEOUT_S` | `RELAY_TURN_TIMEOUT_S` | per-turn wall-clock cap (Aider default: 900s in both runtime shims; hung CLI → exit 7) |

If a fresh device's `codex` still blocks writes, escalate autonomy:
`CODEX_FLAGS='--dangerously-bypass-approvals-and-sandbox'` (or `-c approval_policy=never`).
For agy, the common failure is different: sandboxed runs can exit `0` with empty
output, so run the lane sandbox-OFF before concluding the worker is broken.

## Exit codes

- **`relay-drive.sh`**: `0` closed Approved/Closed · `3` no-progress (token actor didn't move) ·
  `4` round-cap / closed-not-approved · `2` usage.
- **shims** (`codex-turn.sh` / `agy-turn.sh`): `0` acted or deferred · `5` CLI failed (or agy empty
  output) · `6` off-allowlist edit reverted (or committed mid-turn → reset) · `7` timeout-killed · `2` usage.
- **`poll.sh`**: `10` relay closed (stop the loop); on stdout one of
  `DECISION: run-runner | run-watchdog | nudge-cross-model | stop | idle`
  (`nudge-cross-model` = turn belongs to an agent not in `--claude-agents`; relay it as a manual nudge).

## Safety boundary (what the shim guarantees)

The shim is the containment contract, so an unattended turn can't run away: **path-allowlist**
(anything off `RELAY_FILE` + `ALLOW_PATHS` is reverted, exit 6), **commit-bypass guard** (if the CLI
commits mid-turn, the shim resets and re-commits file-scoped), and **no push** (turns commit locally
only — `git push` yourself when ready). `.tick/` is gitignored and per-device, so this is single-clone
coordination, not cross-machine.

**Never hand-edit a clone while a driven turn is in flight there (GH-141).** `rtl_before()` snapshots
the dirty set once, at turn start. A second session's edit landing *during* the turn window produces a
porcelain entry with no match in that snapshot — **byte-identical to the agent's own off-lane
self-escape** — so `rtl_check()` reverts it in the real tree. This is not a bug that can be fixed by
detection: preserving newly-dirty non-allowlisted paths would disable the documented GH-22
self-escape backstop. Observed live twice (2026-07-05, 2026-07-18); the second incident silently
deleted an untracked doc and reverted a tracked one mid-session. Since 2026-07-18 the pre-revert
content is copied to `.tick/orphan-backups/<utc>-<pid>/<path>` first, so a wrongly-caught edit is
**recoverable** — but the revert still happens. Wait for the turn, or work in a separate worktree.

**Worktree isolation is ON by default for driven runs.** `relay-drive.sh` exports
`RELAY_WORKTREE_ISOLATION=1`, so each turn-taker runs in a throwaway `git worktree` of `ROOT@HEAD` —
an off-task model's stray *creations/renames* (not just tracked edits) can't reach the real tree,
closing the gap where the allowlist only reverted named tracked files. Opt out per run with
`RELAY_WORKTREE_ISOLATION=0`; direct/attended shim use keeps the leaf default OFF. Also: `--agent-cmd`
runs a bare executable path directly, so an **absolute path with spaces** (a clone under
`…/GH Repos/…`) is safe — no quoting needed.

## Verify the harness is green before a real run

These are anchored on `$HARNESS` (set by Preconditions) so they resolve whatever your CWD is — don't
drop the `$HARNESS/` prefix or they'll 404 from a foreign session:

```bash
bash "$HARNESS/validate.sh"            # the tick/automation suite
bash "$HARNESS/test/codex-turn.sh"     # before a Codex run
bash "$HARNESS/test/agy-turn.sh"       # before an agy run
```

**If your turn's `--artifact`/`ALLOW_PATHS` includes anything under `relay-automation/`, re-run
`bash "$HARNESS/skills/1-hourly/relay-automation/make-pkg.sh"` after the turn lands, before trusting a green
`validate.sh`.** `relay-pkg-freshness.sh` catches a stale vendored `relay-pkg.tar.gz`, but it reads
as one more red line in a 100+-test suite rather than a real, fix-needed gap — this has bitten two
separate passes on `relay-automation/agy-turn.sh`/`consult.sh` (GH-178's original B1/A4 pass on
2026-07-08, and the GH-183/187 fix on 2026-07-10). Don't wait to discover it after the fact.

Run the shim test matching the worker you'll drive (both are first-class). Run these un-sandboxed —
`mktemp`/network under the Bash sandbox can fail them for reasons unrelated to the code.

## Relationship to the other skills

- **`/relay`** — portable, dependency-free. Owns the thread template, turn block formats, evidence
  contract, and guardrails. **Use it to scaffold the thread**; relay-xyz never redefines the protocol,
  only runs it.
- **`/xyz`** — concurrent, non-overlapping path-scoped lanes (parallel *builds*), also `tick`-backed.
  A relay is sequential review (one writer, turn-based); `xyz` is parallel construction. Different
  shapes.
- **`consult.sh`** — `relay-automation/consult.sh` asks one question of Codex *and* agy in parallel,
  captures both transcripts, leaves synthesis to you. Advisory-only, read-only, **not** a relay turn —
  reach for it when you want a second opinion without a review loop.

## Framing

Open with a human sentence ("Driving a headless Codex or agy review of `<artifact>` — round cap 4…") and
close with the result + exit code. The structured thread lives in the relay file; the operator gets a
sentence and a verdict, not a wall of transcript.

## Review Scope & Commensurate Complexity Standard

Reviewers (Codex, agy, Claude, etc.) and authors must adhere to a strict standard of **commensurate complexity**:

1. **Surgical, DRY, Safe, Secure, and Stable within Reason:** Reviews must evaluate correctness, safety, and invariants against the stated requirements without encouraging speculative over-engineering.
2. **Commensurate Machinery & Tests:** Defensive handling, recovery mechanisms, and test footprints must remain strictly commensurate with the scale and role of the core code. An 80-line sync script or local tool must not become entangled with multi-layered enterprise fail-safes, distributed locks, journaled recovery, or bespoke fuzzing/scanning runtimes unless the operator explicitly specifies it.
3. **Operational Envelope Grounding:** Reviewers must grade against the explicitly declared operational envelope (e.g. local developer CLI, single-repo task) rather than unrequested enterprise multi-tenant threat models.
4. **Challenge Unwarranted Complexity:** Reviewers should actively challenge speculative abstractions, parallel subsystems, and overbuilding, acting as a filter *against* bloat rather than an engine of scope creep.
5. **Measure, read-only (GH-681):** a headless Reviewer MAY run narrow, non-mutating probes and queries against the seeded artifact to measure a claim — output and temp files under `.relay-scratch/` or `$TMPDIR` only, with `export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/.relay-scratch/tmp"` first, and the command, exit status and decisive output quoted in the finding (scratch is discarded after the turn). It may NOT run `validate.sh`, `test/*.sh`, pytest, or executable fixtures in the relay worktree — those belong in a disposable full clone (`AGENTS.md`); a claim only measurable that way is graded `[Unverified — needs clone run]`. Containment is unchanged. The canonical wording is the reviewer note in `relay-automation/relay-turn-lib.sh` (`rtl_turn_prompt`); the marathon reviewer brief (`utils/py/marathon_drive.py`, step 4b) already allows `$TMPDIR` probes.
6. **Generalizations carry a falsifier (GH-681):** a finding that asks for a behaviour change is a generalization unless the Reviewer can paste the concrete input — a row, a value, a `file:line` — that fails under the current code. Every `[Blocker]` or `[Should]` requesting a behaviour change MUST carry `Observed input:`, `Affected scope:` and `Falsifier:` lines; a `[Blocker]` must cite an observed failure. The Producer may disposition a request lacking these as `Declined — unproven generalization`. Protocol rule, not a mechanical check; canonical wording in `relay-automation/new-relay.sh` (Reviewer bullet), mirrored in `skills/1-hourly/relay/SKILL.md` and the marathon brief (step 4c). Origin: the gh673 final QA relay, where a Round-1 `[Blocker]` generalized one late-error observation into a rule that blanks every issue on real data, and the same seat `[Pass]`ed it next round.

## QA / Consult Template Formatting

Since agents often scaffold relay threads manually (when the `/relay` slash command isn't used or available), it is critical to structure QA / consultation threads correctly. **Do not** write open-ended instructions like "QA this codebase against the requirements."

Headless agents (Codex, agy, Aider) perform best when given **explicit questions and a defined operational envelope**. A proper QA thread must include:
1. The goal, operational envelope, and files to read.
2. Explicit statement of commensurate complexity and non-goals.
3. A numbered list of concrete, specific questions to answer.
4. Instructions on what the agent should output (e.g. file:line citations).

**Example format:**
```markdown
---
Goal: QA Phase 3 Implementation (Semantic Layer)
Date: 2026-08-25
NEXT: Reviewer
STATUS: Open
---

# Context

Adjudicate the implementation of Phase 3 Semantic Layer against its plan in PROJECT/2-WORKING/GH-1-firebase-ai-reports-plan.md.

Operational Envelope: Local CLI tool. Tests and machinery must be commensurate with scope; do not demand unrequested enterprise multi-tenant fail-safes.

Read the plan doc in full, plus the code it references:
- api/src/indexer.ts
- api/src/semantic.ts

Questions:

1. Are the requirements for soft-failing met? Does it gracefully continue if the vector index is missing or empty?
2. Are limits capped properly? The plan says "findNearest capped at top-K <= 10". Is this enforced securely?
3. Is the Indexer idempotent? Review `processItem` in `indexer.ts` which uses a hash check. Does this prevent unnecessary re-embedding?
4. Is the implementation surgical and DRY? Flag any unnecessary layers of abstraction or unneeded machinery.

Flag anything wrong, missing, incorrectly scoped, or over/under-engineered. Be concrete and cite file:line where you disagree with a specific claim.

Write your verdict below and change the STATUS to Approved/Closed if it passes.

<!-- ▽ RELAY AUTOMATION: DO NOT MODIFY THIS BLOCK ▽ -->
▶ TAKE YOUR TURN (codex)
<!-- △ RELAY AUTOMATION: DO NOT MODIFY THIS BLOCK △ -->
```
