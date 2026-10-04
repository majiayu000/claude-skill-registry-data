---
name: build-orchestration
description: >
  Run a multi-agent build session: the main session acts as manager — cutting a
  goal into units, spawning implementer, tester, and adviser subagents, and running
  the test-and-review loop to completion under anti-thrash guardrails.
disable-model-invocation: true
---

# Build Orchestration

You are the manager: you direct the workers but do not implement features — your
own edits are limited to docs, config, and merge glue.

## Prerequisites

Confirm each agent you intend to spawn is in the available-agents list; if one is
missing, stop and tell the user.

Create `build-orchestration/strike-count.md` empty, overwriting any existing file
(Guardrails).

## Establish the goal

Reconcile three inputs; none alone is authoritative:

- The binding spec under `docs/plan/` (start at `README.md`; milestones in `07-milestones.md`).
- `docs/plan/PROGRESS.md` for where work left off.
- The user's in-session direction — which entry point to continue from, plus any
  added requirements.

If no entry point is stated, ask the user for it.
Cut the work into units. A unit pairs a disjoint file set with a written spec —
what to build for that unit, reconciled from the inputs above.

## Session flow

1. Spawn `design-adviser` and/or `security-adviser` over the unit's *spec*, each
   only if the spec meets its `Deploy when` trigger (Review axes). Neither → skip
   to step 4.
2. Surface the gate findings to the user; the call is theirs, not yours to
   resolve.
3. Record the user's decision in the spec.
4. Spawn `blackbox-tester` and one `implementer` per unit, from the settled spec,
   in parallel.
5. On the `blackbox-tester` report, move its tests from `.agent-scope/` into the
   repo's test-dirs, then clear the jail (Spawning rules). Treat its `Findings` as
   spec gaps: decide each and record it in the spec; surface any that needs a design
   decision to the user first (Reports). Never route a `Finding` to an implementer.
6. Before the first merge, stamp the session base: `agent-worktree.sh start` (finalize
   collapses to it). Then, as each implementer report arrives, integrate it with
   `agent-worktree.sh merge` (Spawning rules). Once a unit's source is merged **and** its
   blackbox tests are landed, run the build and the blackbox suite (via `<test command>`).
7. On failure, follow the escalation ladder (Guardrails).
8. Once the units are merged and green, spawn `whitebox-tester`.
9. When both suites pass, spawn the review layer: each adviser by its `Deploy
   when` trigger (Review axes).
10. Consume each reviewer report (Reports — demand and consume).
11. Rerun both suites after each fix batch; repeat until the reports are clean, or
    log the remainder to build-log as unresolved risk.
12. Write the record (below).
13. Finalize onto your branch. Each `merge` committed the unit as disposable scaffolding
    so the integration could be a real `git merge`; those commits must not become your
    history. Run `agent-worktree.sh finalize` (refuses mid-conflict; only ever drops this
    session's commits, never pre-session or pushed history) — it resets to the `start`
    stamp and leaves the whole integrated result as uncommitted changes. Then produce the
    real commit(s), including the build-log, through the `git-commit` skill, and surface
    the planned commits to the user. The scaffold commits never reach a remote.

## Spawning rules

- Subagents see none of this conversation. Every prompt carries:
  the exact file paths, the spec extract for the unit, the applicable CLAUDE.md
  constraints (`code-commenting` skill, no Claude attribution), and a demand for
  its report back.
- Isolate every Bash agent (`implementer`, `whitebox-tester`, `mcdc-tester`, `debugger`)
  in its own git worktree via `.claude/scripts/agent-worktree.sh`, run from the main
  checkout:
  - `add <unit> [test-dirs] [base-ref]` — for the implementer pass its test-dirs
    (comma-sep) to prune the suite; for whitebox/mcdc/debugger omit test-dirs. Point the
    agent at `.agent-worktrees/<unit>`.
  - On the report, `merge <unit> <permitted-path>...` — permit the implementer's source
    paths, a tester's test-dirs only. Merge nothing from the debugger. Route the two
    failures differently:
    - Scope refusal (out-of-scope path): push it back to the same worker; for an
      implementer unit, bump its `strike-count.md` line (Guardrails).
    - Merge conflict (real line overlap): resolve the markers in main yourself (merge
      glue) and commit, or abort the merge and re-cut so one unit owns the file. Never
      an implementer's job; never a strike.
  - `remove <unit>` once merged or abandoned.
  Give parallel agents separate worktrees; sequence any two units that edit the same
  file, especially a shared integration point (barrel, route table, registry).
- Background by default. Run synchronously only when the next allocation depends
  on the result.
- Batch small findings into one fix unit, not one agent each.
- Spawning an `implementer` for a unit → add its `strike-count.md` line, `<unit>: 0/2`.
- Never pass the test files to an implementer.
- Never let an implementer or tester widen a symbol's visibility for testing.
- For `blackbox-tester`, stage only the spec into `.agent-scope/`, spawn it pointed
  there. On its report, move the written tests into the repo's test-dirs (step 5),
  then clear `.agent-scope/`.

## Review axes

Each adviser owns one axis; deploy per unit by its `Deploy when` condition, not
all-always. A `●` in `Must` makes that condition a floor — never skip it; `—` leaves
the call to you.

| Axis | Agent | Deploy when | Must |
| --- | --- | --- | --- |
| Correctness (logic, edge cases, contract) | `correctness-adviser` | the unit has non-trivial logic or branching (near-default) | ● |
| Security risk | `security-adviser` | the unit touches auth, input handling, crypto, file/network I/O, or secrets | ● |
| Design / architecture | `design-adviser` | the unit adds or changes an abstraction, interface, or module boundary | — |
| Redundancy, over-complication | `simplicity-adviser` | the diff is large or tangled | — |
| Performance, efficiency | `performance-adviser` | the unit loops over unbounded data, hits the DB, or sits on a hot path | — |
| Documentation, comments | `docs-adviser` | the unit changes public API or user-facing docs | — |
| Legal, licensing, compliance | `legal-adviser` | the unit adds a dependency or copied / third-party code | ● |
| Change discipline (diff vs. its mandate) | `change-discipline-adviser` | the diff smells: scope creep, weakened or deleted tests, an outsized diff | — |
| Decision-coverage testing (optional) | `mcdc-tester` | the unit is decision-dense: auth, pricing, validation, state machines | — |
| Root-cause diagnosis on failure | `debugger` | the escalation ladder stalls (Guardrails) | — |

## Guardrails against thrashing

- **Escalation ladder** — after 2 strikes you diagnose, you do not re-attempt; re-read the
  unit's `strike-count.md` line before each escalation decision.
  1. Attempt fails → bump the unit's line, then feed the exact failure back to the same
     implementer via `SendMessage` (context intact). At most twice.
  2. Still failing → **stop changing code. Spawn `debugger` for the root cause.**
     No further edit until the cause is named.
  3. Cause named but the fix fights the design → `alternatives-explorer`, or
     escalate to the human that the approach or the spec may be wrong.

## Reports — demand and consume

Each agent defines its own format; demand it back as the final message with a
first-line `route:` token. Act on `route`, never on a section's presence or the axis
verdict word. Tokens, `+`-combinable: `accept` consume as-is · `fix` → fix unit ·
`decide` a call pends · `redrive` respawn/escalate.

Legal tokens per agent, and the consumption behind them:

- **Advisers** — `accept` \| `fix` \| `decide` \| `fix+decide` \| `redrive`. `fix`: batch the
  `fix`-tagged problems into fix units by severity, each dispatched to an implementer with its
  `directions`; `high`/`medium` block finalize, `low` → build-log as unresolved risk. `decide`:
  surface to the user, never an implementer. `redrive` / an `Out of scope` entry naming an
  unreviewed area: restage that input and respawn, or record the uncovered axis.
- **blackbox-tester** — `accept` \| `decide` \| `redrive`. `Findings` are spec gaps
  you resolve (that's the `decide`), never an implementer's; always consume `Open`.
- **whitebox / mcdc-tester** — `accept` \| `fix` \| `decide` \| `fix+decide` \|
  `redrive`. The tests land on any non-`redrive` route. `fix`: route `Findings`
  (real bugs) to a fix unit — a `Suite` xfail/skip parked on a `Finding` is one such
  bug. `decide`: an `Open` item pends — always consume it. `redrive`: the suite
  wouldn't run → respawn.
- **implementer** — `accept` \| `decide` \| `accept+decide` \| `redrive`. `accept`:
  `Build` passed, no `Open` → integrate the unit. `accept+decide`: integrate too —
  the code still merges — but an `Open` call pends, resolve it. `decide` (bare): it
  stopped before a passing build → do **not** integrate; resolve the `Open` blocker,
  then send the implementer back to finish. `redrive`: `Build: fail` → escalation
  ladder.
- **alternatives-explorer** — `accept`. Take the single `Recommendation` into a
  design decision, then a fix unit.
- **debugger** — `fix` \| `decide` \| `fix+decide` \| `redrive`. `fix`: `Root cause`
  + `Fix location` feed the next fix unit; `redrive` is no-repro (`Root cause:
  none`), an escalation.

## The record

- **Prompt-log** — log every subagent's exact prompt to `build-orchestration/prompt-log/`
  as you spawn it, under the `S<N>-<role>-<n>` id scheme (roles: `impl`, `blackbox`,
  `whitebox`, `mcdc`, `adviser`, `debug`, `altex`). Capture
  only: never a decision input, never paste one prompt into another.
- **Build-log** — write one `build-orchestration/build-log/<yyyy-mm-dd>-<slug>.md`
  per session, committed with the session's work at finalize (step 13). Keep only what a later session needs: the
  option chosen and why, decisions with their reasoning, how the built pieces
  connect to each other and to the plan, and any unresolved risk. Cut
  transcripts, play-by-play, restated plan content, and per-agent credit.
- Run the build-log through the `human-writing` skill before committing.
