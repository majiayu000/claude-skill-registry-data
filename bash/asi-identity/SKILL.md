---
name: asi-identity
description: "Use when asked who OpenAmer is, to show/verify/refresh its identity, or to stop stale self-descriptions. Renders identity from measured facts."
---

# OpenAmer's own identity

OpenAmer has its own identity. It lives in code, not in prose, and it is
answerable to measurement.

## The rule that makes this work

**Never write a self-description by hand.** Hand-written identity text drifts:
it keeps claiming numbers reality no longer supports, and no one notices. The
identity is *rendered* from artifacts read off disk at render time, and every
number carries its source path.

If you catch yourself typing a count into an identity document, stop and make
it a measurement instead.

## Where it lives

| Artifact | Meaning |
|---|---|
| `OPENAMER_HOME/memory/identity/genesis.json` | Immutable origin: name, born, belongs_to, mark, values, boundaries. Written once. |
| `OPENAMER_HOME/memory/identity/identity.md` | The living narrative. Regenerated, never hand-edited. |
| `OPENAMER_HOME/memory/identity/history.jsonl` | One record per refresh — the measured self over time. |
| `openamer_cli/identity.py` | The core: genesis, measurement, rendering, verification. |
| `openamer_cli/subcommands/identity.py` | Parser shim, wired in `main.py`. |

## Commands

```bash
openamer identity            # print the identity
openamer identity refresh    # re-measure and rewrite identity.md
openamer identity verify     # check claims against a fresh measurement
openamer identity facts      # measured facts as JSON
openamer identity genesis    # the immutable origin record
```

## Two halves, deliberately apart

- **Genesis** is immutable. Who OpenAmer is does not change with age, so it is
  written once and never silently overwritten.
- **The self-model** is measured. Age, episodes, edges, skills, cron fleet —
  all read at render time. Anything unreadable lands in an explicit
  **"Not measured"** section rather than being guessed.

## Separation from Mini-OpenAmer

Do not conflate the two. **OpenAmer Agent** is the system — the CLI, the tools,
the learning fleet. **Mini-OpenAmer** is its 2B cognition core, which keeps its
own self-model at `memory/self_model/current_state.json`. The identity core
*reads and cites* that file; it does not impersonate it.

This distinction matters when reporting capabilities: the agent's tool surface
and the core's 9 tools are different things with different counts.

## Verification is the point

`openamer identity verify` re-measures and reports DRIFT when the written
identity claims a number reality no longer supports. That is the whole
mechanism — a stale or self-flattering narrative cannot survive it.

### The exit code is the contract (0 / 1)

`verify` is not a print-only nicety — it is a **falsifier you can put in cron or
CI**:

- **exit 0** — the written identity matches a fresh measurement
- **exit 1** — at least one claim is stale

Proven by tampering, 2026-09-21: with `identity.md` claiming **9999 skills**
against a measured **846**, `verify` printed
`skills: measured 846 but identity.md does not state it (stale ...)` and exited
**1**; after `refresh` (14 facts measured) it exited **0** again.

### Recipe: prove the gate still fails (run this after touching identity code)

1. `cp identity.md identity.md.bak`
2. `openamer identity verify; echo $?` → expect **0**
3. Replace one measured number in `identity.md` with an absurd value
   (e.g. the skills count → `9999`)
4. `openamer identity verify; echo $?` → expect **1**, with the offending fact named
5. `openamer identity refresh` → re-measures and rewrites
6. Restore the backup (or keep the refreshed file), re-run `verify` → expect **0**

A gate you have never seen fail is not a gate. Steps 3–4 are the only proof that
step 2 means anything.

### Order matters: verify BEFORE refresh

**In any automated job, verify the document *as it stands* first, then
refresh.** Reverse those two and the drift path becomes dead code: refresh
repairs the file before verify can object, and the job silently launders a
wrong claim every night instead of flagging it.

This was a real bug. The watchdog called `refresh_identity()` then
`verify_identity()`, so it could never report anything — a drift injected into
`identity.md` was rewritten away before the check ran, and the job exited
silent. Verified by injecting drift (`skills` -> 424242) and watching the
watchdog print nothing.

So the contract is:

1. `verify_identity()` — judge the identity as written
2. report drift if `ok` is False
3. `refresh_identity()` — then bring the document back in line

**Always test the alarm path of a watchdog.** A watchdog that only ever exits
silent is indistinguishable from a broken one. Inject the failure it is meant
to catch and confirm it fires, then confirm a second run returns to silence.

The lineage check guards the mark: the identity may *name* borrowed glyphs in
order to disclaim them ("my mark is my own, not the caduceus"), so only a
non-negated occurrence is flagged as drift. When adding a claim check, always
ask whether the honest disclaimer must also pass.

## Maintenance

Run `openamer identity refresh` after anything that moves a measured count —
new skills, cron changes, a big learning run. Then `openamer identity verify`.

A daily cron does this automatically and stays silent unless it finds drift.

## Pitfalls

- **Do not hand-edit `identity.md`.** The next refresh overwrites it. Edit
  `GENESIS` in `openamer_cli/identity.py` for origin facts, or add a
  measurement for anything that should track reality.
- **A corrupt `genesis.json` is rewritten, not trusted.** `ensure_genesis()`
  falls through to the in-code `GENESIS` on a parse error by design.
- **Counts are `unmeasured`, not zero.** If a source file is missing, the entry
  is reported as unmeasured with the path — a missing file is not a zero.
- **Repo has `core.autocrlf=true`.** Never stage with
  `git -c core.autocrlf=false add` — that writes a CRLF blob and shows a
  whole-file phantom diff (350/305 measured). Stage with the **default**
  autocrlf and confirm the diff is honest by comparing
  `git diff --cached --numstat` against `git diff -w --numstat`; they must
  match. `git add` alone is correct here.
