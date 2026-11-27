---
name: goal-loop
description: Fix rounds toward one measurable goal on N failing scenarios (bench cases, end-to-end cases, evaluation cards). Classifies each failure, fixes in lanes, merges once, measures again. Use when the user says make these pass, or a bench is red.
---

# Goal loop

A **goal loop** is a sequence of fix rounds with one fixed goal: "all N scenarios pass every hard check". A
**scenario** is one bench case or one end-to-end case. A **hard check** is a check whose failure fails the
scenario.

Each round has the same shape, and the owner rules of the project (`AGENTS.md`, sections `## Owner rules` and
`## Test scope`; the split, timebox and merge rules of `shark:operator`) apply to it:

```
run (production settings) --> classify failures (parallel shark:code-debugger) --> owner questions (business rules only)
        ^                                                                              |
        '---- re-run <-- lead merge (shark:lead-engineer / shark:lead-merge) <-- lanes <-- round contract
```

**Project values.** The commands come from `AGENTS.md`, section `## Commands`: `bench` (the costly run of the
scenarios), `gate:fast`, `gate:scoped <paths>`, `test <paths>`, `setup`, `test-db:copy`. If `bench` is missing,
ask the user once how to run the scenarios, and suggest adding the key to `AGENTS.md`. `<scratch>` is the
session scratch folder.

## Files

| File | Content | Template |
| --- | --- | --- |
| `<scratch>/goal-loop/rounds.md` | Goal, config, scenarios, owner decisions, one row for each round | `references/rounds-template.md` |
| `<scratch>/goal-loop/run.sh` | The run script of the loop (it calls the project's `bench` command) | `references/run-script.md` |
| `<scratch>/goal-loop/defects-r<n>.md` | The classified failures of round n | `references/rounds-template.md` |
| `<scratch>/goal-loop/contract-r<n>.md` | The round contract | `references/rounds-template.md` |
| `<scratch>/goal-loop/lane-header-r<n>.md` | The header that every lane reads first | `references/lane-header-template.md` |
| `<scratch>/goal-loop/r<n>/` | The saved run files of round n, with `head.txt` (the sha that ran) | written by the run |

## Step 1: set the goal

1. Pick N scenarios that fail today. Name each one in `rounds.md`.
2. Write the goal: "all N pass every hard check".
3. Set the round limit (a good start: 10 rounds).
4. Write the config: the production settings that the run uses. Run at production settings, never at a faster
   or a cheaper setting.
5. Name the regression guard: the scenarios that passed before. They run once after the loop.
6. Set the spend cap of one run, if the run costs money (a token, API or compute limit). Write it in `rounds.md`.

## Step 2: run once

The costly run goes **once per round**, with the project's `bench` command, never inside a lane.

1. Write the run script from `references/run-script.md`. Its rules:
   - **a named arm:** the run has a name that the results show;
   - **a frozen copy of the code:** run the code of a worktree at a fixed sha. A merge can move a branch during
     the run;
   - **start from the checkout that holds the key file, when the run needs one:** `cd` into it. Never copy,
     read or print the key file (`AGENTS.md`, section `## Secrets`);
   - record the sha in `r<n>/head.txt`; put a hard `timeout` and the spend cap on the run.
2. A run that can take longer than 10 minutes needs the owner's OK each time (`## Owner rules`). Say the
   expected time and cost.
3. Start the run in the background. Wait for the notice. Do not poll.
4. Add the round row to `rounds.md`: round, head, pass count, failing checks, notes (cost, folder).

## Step 3: classify every failure

1. Split the failing checks into groups of about 3 to 4 scenarios.
2. Start one `shark:code-debugger` for each group, in parallel. Each one reads the saved run files first (see the
   `shark:debug-rca` skill) and finds the root cause with `file:line`. It leaves one failing test, uncommitted,
   in its own worktree.
3. Give each failure one class:

| Class | The failure comes from |
| --- | --- |
| RULE | a spec or a business rule: the rule is wrong, missing or unclear in the spec, the configuration or a per-customer spec |
| CODE | the implementation: the rule is right and the code does something else |
| DATA | the input, a fixture, a projection or a derived state that carries wrong or stale information |
| MISSING | an implementation that is not there |
| HARNESS | the case, the check or the runner; no effect in production |

4. Write `defects-r<n>.md` with one row for each defect. The columns are in `references/rounds-template.md`.
   Put the defects that need an owner decision in their own section.

### Profile: how a project names its own classes

The five classes are the generic set. A project may keep names that fit its domain, and map each to a generic
class, in `rounds.md` (line "Classes"). Use the project names in the tables and the generic class in the
reasoning. Example of a profile for an agent-conversation bench:

| Project name | Generic class |
| --- | --- |
| SPEC (shared spec or a tenant spec) | RULE |
| TOOL (a tool returns wrong information) | CODE |
| PROJECTION (state or projection of the conversation is wrong) | DATA |
| MISSING | MISSING |
| BENCH (card or check fault) | HARNESS |

Example of a profile for a web-checkout end-to-end suite: PRICING-RULE = RULE, API = CODE, SEED = DATA,
NOT-BUILT = MISSING, FLAKY-TEST = HARNESS. Keep the mapping to one line each. Do not invent a sixth class: a
defect that fits none of the five goes to the owner as a question.

## Step 4: ask the owner only about business rules

- Ask only when the spec, the decisions log and the code do not decide a business rule (class RULE).
- Ask one question for each decision. Put your recommendation first, with its reason, and the alternative in one
  line.
- Record each answer in `rounds.md` as `OD-<n>` (owner decision), with the date and its scope. An example scope:
  "shared default; a per-customer spec can supersede it".
- A new decision that changes an older one supersedes it. Record the link in both rows, with date and scope;
  never call the older one wrong.
- Do not stop the round for a question. The lanes that need no decision start at once.

## Step 5: contract, lanes, merge

1. **Contract.** One agent writes `contract-r<n>.md` in 5 to 10 minutes, before the split. It holds:
   - the base and the scope;
   - each shared name, with its one owner file;
   - every writer and reader of each new or changed event or field;
   - the invariants (`AGENTS.md`, section `## Invariants`) and the owner decisions to keep;
   - the rules to delete, with their callers and their new owner;
   - the lane table.
2. **Lanes.** One cause or one behaviour for each lane. No two lanes on one file or function. Each lane row gives
   the files and functions that it owns, its starting test, and what it must keep. It also gives the snapshot
   differences that it may cause. Start the lanes with the lane header (`references/lane-header-template.md`).
   Timebox 20 minutes for a lane (AGENTS.md › Working rules §2), hard, with the automatic grace of 20 % and the
   rule to ask the operator for more.
   A lane never runs the `bench` command: it checks only its files (`gate:scoped <paths>`).
3. **Merge.** One lead merges the round (`shark:lead-engineer` agent; for many branches, the `shark:lead-merge`
   skill). It runs the fast path (`gate:fast`) once and writes one blocker table.
4. **Re-run.** Run Step 2 again on the merged head. Compare each scenario with the round before.

## Stop rules

Stop the loop when one of these is true:

1. **All pass.** Then run once more as a confirm run. Stop only when the confirm run also passes.
2. **The round limit.** Report the state, the open defects and their classes.
3. **A round finds more than it fixes.** Stop and tell the owner. List the defects again from the start. A
   different method can be the next step: for example, a `shark:port-audit` when the defects come from one large
   rewrite.

After the loop, run the regression guard once (with the owner's OK when it is long).

## Rules

- Accuracy before speed. A speed lever may not cut or degrade a reading or a check.
- No customer name and no customer rule in shared code. Per-customer rules come from the spec or a setting.
- No real customer data to an external model or service. No external model call in a test.
- A lane changes only the behaviour of its row. Any other change outside its row is a stop.
- Lanes never re-record a snapshot. They report each difference and map it to their row.
- Never parse display text to get state: state keeps its native types, and text is made at the presentation edge.
- Measure before you add complexity: a new mechanism needs a baseline of the scenarios that it must improve.

## Lessons

- **A half-ported state gives misleading runs.** On a head with only part of a re-port merged, the pass count can
  stay the same while new failures come in other scenarios. Do not tune on such a head. Analyse the failures
  after all units merged.
- **One run of each scenario has noise.** A run with a model or a timing can pass or fail by chance. Confirm a
  pass with a second run, and compare a failure across two runs before a lane starts on it.
- **The run found lost rules one at a time.** Round after round found the next gap of one rewrite. That is the
  signal of stop rule 3: switch to a `shark:port-audit`.
- **Read the run files before a replay.** The saved run file holds the events, the chosen steps and the refusals
  of each turn. Most causes show there.
