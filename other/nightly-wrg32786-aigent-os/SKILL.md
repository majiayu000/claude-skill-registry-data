---
name: nightly
agent: none
description: Canonical seven-leg nightly close-parity protocol. Eleven independently evidenced checkpoints cover synthesis, reconciliation, context hygiene, sweeps, heat, digest, runtime health, cognitive state, ledger capture/review, and vault sync.
allowed-tools: Read, Write, Bash
user-invocable: false
status: PRODUCTION - invoke through /nightly-close-parity
---

# /nightly - canonical seven-leg close-parity protocol

NIGHTLY_LOCAL_PROTOCOL: close-parity-v2-7L-11C

`/nightly-close-parity` is the public fire verb for this seven-leg framework. It first proves that this
project-local protocol is the one being loaded. Do not fall back to another
same-name skill or an installed cache.

The seven legs contain eleven independently recorded checkpoints:

| Leg | Checkpoints |
|---|---|
| A - Dream | `dream` |
| B - Reconcile and context | `reconcile`, `context-hygiene` |
| C - Sweep and heat | `sweep-now`, `heat-index` |
| D - Digest | `digest` |
| E - Runtime health | `system-check`, `cognitive-runtime` |
| F - Measurement ledgers | `ledger-capture`, `ledger-review` |
| G - Vault sync | `vault-sync` |

Every checkpoint is recorded through `daemons/nightly-pass.mjs`. A failed
checkpoint immediately writes a named event to the append-only
`NIGHTLY_ALERTS.jsonl` ledger, writes the same bounded alert to stderr, and
leaves it active for the next SessionStart hook. Local delivery is the complete
default channel; no external coordination service is required.

## Root, memory, date, and environment

Run from the aigent-OS root. The normal operational memory root is
`vault/memory`; the daemon also supports the documented `memory` fallback used
by minimal forks and honors `AIGENT_STATE_HOME_DIR` for isolated probes.

One time zone is used for pass dating, alert scopes, ledger review, and
freshness. Configure it with `AIGENT_NIGHTLY_TIME_ZONE`; the documented default
is `America/Los_Angeles`. Configure the post-fire cutoff with
`AIGENT_NIGHTLY_CUTOFF_HOUR`; the default is `4`. A CLI `--time-zone` or
`--cutoff-hour` override must be threaded through the whole invocation. The
controller stores both values in pass state so a later checkpoint cannot drift
to a different date policy.

Tests and scheduled invocations must set the root, state-home, time zone, and
cutoff explicitly. Ambient values must never decide which memory tree a proof
mutates.

## Evidence controller

Prove the route, then begin:

```text
node daemons/nightly-route-check.mjs --root <aigent-root>
node daemons/nightly-pass.mjs begin --root <aigent-root> [--date YYYY-MM-DD] [--replace]
```

Begin requires both canonical inputs to exist and be readable:

- `vault/memory/MEMORY_CANDIDATES.md`
- `vault/memory/runtime/NIGHTLY_CAPTURE_CANDIDATES.jsonl`

The exact prefix may be `memory/` only when the root uses the documented
fallback layout. Missing input is a failed invocation, never an empty or skip
claim.

`--replace` is recovery-only. It abandons an interrupted `status=running` pass
with a named alert before starting a new pass. It never overwrites completed
evidence.

After each checkpoint:

```text
node daemons/nightly-pass.mjs record --root <aigent-root> \
  --checkpoint <name> --status <pass|skipped|fail> --exit-code <integer> \
  --artifact <file:PATH|git:FULL-40-CHAR-SHA|stdout:CHECKPOINT@exit=N|none:ALLOWLISTED-REASON> \
  --detail "<bounded factual detail>"
```

A `git:` artifact must be the full 40-character commit id, copied verbatim
from `git rev-parse HEAD`; a short id is refused.

Any nonzero exit, missing/stale/noncanonical artifact, illegal skip, or explicit
failure becomes `fail` and raises
`NIGHTLY:LEG_FAIL:<checkpoint>`. A duplicate record is refused, preserves the
first evidence, raises `NIGHTLY:DUPLICATE_CHECKPOINT:<checkpoint>`, and makes
finish red. Only `sweep-now` and `digest` may be skipped under their exact
predicates. Continue collecting other safe evidence after a failure.

Finish:

```text
node daemons/nightly-pass.mjs finish --root <aigent-root>
```

A missing checkpoint raises `NIGHTLY:INCOMPLETE_PASS`. The terminal block is
green only when all eleven checkpoint rows are present once, every validator
receipt is nonempty, no row failed, and terminal `status: PASS` is written.
Terminal `status: FAIL` is always red.

## Artifact and postcondition contract

The controller captures pre-fire Dream, cognitive, and ledger snapshots at
begin. It independently re-runs each known postcondition and stores bounded
literal output in the checkpoint's `validator` field.

| Checkpoint | Accepted green artifact |
|---|---|
| dream | canonical `file:` path to `DREAM_LOG.md` |
| reconcile | `stdout:reconcile@exit=0` |
| context-hygiene | `stdout:context-hygiene@exit=0` |
| sweep-now | canonical `file:` path to `SWEEP_LOG.md` |
| heat-index | canonical `file:` path to `HEAT_INDEX.json` |
| digest | canonical `MEMORY_CANDIDATES.md` file, or `none:no-staged-candidates` when re-parsing proves zero |
| system-check | `stdout:system-check@exit=0` |
| cognitive-runtime | `stdout:cognitive-runtime@exit=0` |
| ledger-capture | canonical candidate file/stdout, or `none:no-ledger-candidates` when the begin snapshot proves no append |
| ledger-review | `stdout:ledger-review@exit=0` |
| vault-sync | current `git:<HEAD>`, or `none:nothing-to-commit` after a clean-tree predicate |

A checkpoint may not certify itself by echoing an artifact string. File paths
must remain inside the selected root and resolve to the canonical product.
Stdout receipts cause the deterministic daemon to run again. `none:` reasons
are allowlisted and reproduced from live state.

## Human-gate invariants

- Dream improvements start `proposed`; only an exact operator decision can
  approve them.
- Digest only counts and surfaces staged candidates unattended; it never
  changes status.
- Reconcile reports drift; it never reprioritizes.
- Context hygiene archives before removal, uses compare-and-swap, and refuses
  unfamiliar shapes.
- Cognitive updates write only explicit or mechanically evidenced deltas.
- Judgment-bearing ledger entries are staged. Direct mutation requires an
  allowlisted executable predicate and the existing ledger owner.
- Sweep results remain proposals.
- Meta-improvement consumes approved candidates only and never self-merges.
- Vault sync never force-pushes, resolves conflicts, stages unrelated work, or
  acts without the configured repository authority.

## Leg A - Dream

Execute `skills/dream/SKILL.md` directly. The leg runs on every fire and appends
one canonical dated synthesis, including an explicit zero-lesson result when
there is no new signal.

PASS requires:

- the newest real Dream header matches the pass date;
- the Dream and Lessons products retain their pre-fire byte prefixes;
- every appended JSONL row parses, uses a valid next id, and satisfies the
  admission predicate;
- every improvement candidate starts `status: proposed`;
- exact source references and mutation-proof fields are present.

Record the canonical Dream file. The controller runs
`DREAM_CONTRACT PASS`; serialization errors, self-approval, legacy paths, or a
missing dated entry are failures.

## Leg B - Reconcile and context

### B1 - `reconcile`

Run:

```text
node daemons/nightly-reconcile.mjs --root <aigent-root> --as-of <pass-date>
```

The daemon computes an exact seven-calendar-day attention window from explicit
Tier-1 intended shares. Missing intended shares return the named failure
`intended-share-input-absent`; the leg must not invent percentages or call the
absence a skip. Record `stdout:reconcile@exit=<literal-exit>`.

### B2 - `context-hygiene`

Execute `skills/context-hygiene/SKILL.md`. It archives old dated Session Log
blocks before removal, keeps the documented five-entry newest-first live
window, and requires one operating-mode heading plus one to five priorities
under Tier 1-3 headings. It refuses ambiguous content and uses pre-write
SHA-256 compare-and-swap.

Run the read-only checker after any edit:

```text
node daemons/nightly-context-hygiene.mjs --root <aigent-root>
```

Only `CONTEXT_HYGIENE PASS` is green. Record
`stdout:context-hygiene@exit=<literal-exit>`.

## Leg C - Sweep and heat

### C1 - `sweep-now`

Reuse `skills/sweep-now/SKILL.md`. Preserve its seven-day cadence:

- skip only when the newest real `### YYYY-MM-DD` `SWEEP_LOG.md` header is within
  cadence;
- otherwise run the existing tracker, heat, and link proposal pass;
- surface every untracked path by name.

A cadence skip records `status=skipped exit=0` with the canonical sweep-log
file. Missing or unparseable cadence evidence is failure.

### C2 - `heat-index`

Always run:

```text
node daemons/memory-heat/compute-heat.js
```

The daemon atomically replaces `HEAT_INDEX.json`. Re-read it and require valid
JSON, a current parseable `generated_at`, an array `hot_top_20`, and a
nonnegative integer `total_notes`. A fresh mtime with stale content is red.

## Leg D - Digest

Read the canonical `MEMORY_CANDIDATES.md` table and count exact
`status=staged` rows by type. Do not promote, skip, supersede, or simulate an
operator answer.

- Zero staged rows: `status=skipped exit=0
  artifact=none:no-staged-candidates`.
- One or more: `status=pass exit=0` with the canonical file. The controller
  re-parses it and records the derived count.

## Leg E - Runtime health

### E1 - `system-check`

Run `bash daemons/system-check.sh` from the aigent-OS root with explicit
`AIGENT_ROOT`, vault, time-zone, and cutoff values. Record
`stdout:system-check@exit=<literal-exit>`. A nonzero result is a failed
checkpoint, but later safe legs still run.

### E2 - `cognitive-runtime`

Execute `skills/cognitive-update/SKILL.md`. It may touch only `GOAL_STACK.json`,
`BELIEF_STATE.jsonl`, `SELF_MODEL.json`, and `PROCEDURES.jsonl`. Zero qualifying
updates are valid when the skipped count and sources are recorded.

The controller derives append-only suffixes, id allocation, and alias deltas
from its begin snapshot. Record
`stdout:cognitive-runtime@exit=<literal-exit>`.

## Leg F - Ledger capture and review

### F1 - `ledger-capture`

Execute `skills/nightly-ledger-capture/SKILL.md`. Local capsules, the canonical
Session Log, explicitly referenced Git evidence, and existing ledgers are
discovery inputs. A source cannot verify its own confident claim.

Judgment-bearing proposals append through the sole writer to:

`vault/memory/runtime/NIGHTLY_CAPTURE_CANDIDATES.jsonl`

Direct ledger mutation is legal only through an existing ledger owner after a
green allowlisted executable predicate with structured arguments, observed
result, literal exit, artifact, and receipt hash. Exact already-given decision
outcomes use the dedicated compare-and-swap writer only when matching is
unique, due, and replay-safe.

### F2 - `ledger-review`

Run `daemons/nightly-ledger-review.mjs`. Count open honesty/trust items older
than seven days, executable resolution candidates, and repeated failure
classes. Stage any judgment-bearing resolution or doctrine proposal. On Friday
the literal `FRIDAY_MEASUREMENT` line implements the weekly measurement.

Record `stdout:ledger-review@exit=<literal-exit>` even when every count is zero.

## Leg G - Vault sync

Run last using the existing `daemons/vault-sync.mjs` boundary and the
repository's configured authority:

1. Inspect `git status --porcelain` and name every untracked path.
2. Keep unrelated user work out of the sync.
3. Run the configured vault sync only when its remote and authority predicates
   pass.
4. Record current `git:<HEAD>`, or record
   `none:nothing-to-commit` only when a fresh clean-tree check reproduces it.
5. Finish the evidence controller.

If durable evidence cannot be committed after finish, run
`nightly-pass.mjs evidence-fail` with the literal failure. After a verified
retry, run `evidence-success --sha <commit>` to resolve only that run's alert.
Never force-push, rewrite history, switch branches, resolve divergence, or
claim delivery without readback.

## No-fire watchdog

`daemons/nightly-watchdog.mjs` reads the actual maximum dated Nightly Log
header outside fenced examples. File mtime is ignored. It applies the same
configured time zone and post-fire cutoff, then verifies the selected block:

- exact protocol;
- terminal `status: PASS`;
- valid completion timestamp;
- all eleven checkpoints exactly once;
- no unknown, unparseable, or unreceipted rows;
- no failed or nonzero row under a `PASS` terminal status.

Red raises one of two distinct alerts, because "the pass never ran" and "the
pass ran and failed" are different conditions and must not report as the same
thing:

- **`NIGHTLY:NO_FIRE`** — no block, a stale block, or a structurally incomplete
  one. The pass did not complete.
- **`NIGHTLY:PASS_FAILED`** — a structurally complete block whose terminal
  status is `FAIL`, naming the failed checkpoints. The pass ran every checkpoint
  and reported its failures honestly. Raising this also resolves any stale
  no-fire, so the ledger never carries both claims at once.

Either way the result is red — a failing nightly never reads green. The active
alert is visible at SessionStart even if no optional integration exists, and the
boot renderer interpolates the alert code rather than filtering on it, so a new
code surfaces without a change there. Green resolves only the no-fire alert.

## Betterment flow

Nightly produces lessons, Dream proposals, staged ledger candidates, and
pressure signals. `skills/meta-improve-vault/SKILL.md` may consume only a Dream
proposal that carries exact operator approval. The flow is:

`propose -> operator review -> approved -> independently reviewed implementation`

Nothing auto-applies, auto-promotes, auto-approves, or self-merges.

## What this pass never does

- Never fires or writes nightly evidence merely because the framework is
  installed or tested. Installation may seed only missing empty schema
  templates; tests use disposable operating-system temp roots.
- Never treats a missing input, stub, incomplete checkpoint, invalid artifact,
  or terminal FAIL as green.
- Never uses a capsule or agent-authored summary as its own verification oracle.
- Never requires or reports to an external coordination system.
- Never changes scheduler registration.
- Never lowers a sibling skill's human gate.
