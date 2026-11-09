---
name: model-routing
description: Use when this session is about to dispatch another one — an implementer, a review collector and its lenses, a comments agent, a search subagent, a successor — and must choose the model/effort pair that closes the work in one round at the least cost, however small the job; a general question about the capability tiers, with nothing to dispatch, is not one.
---

# Model routing

**This skill is a decision aid for the orchestrator.** Its tables, its readings, its escalation and its record inform your judgment: you decide the pair, the tier or the model, and the brief carries the choice and its reason. What is not a choice of pair — how the map is bound, the mode an unattended session runs in, how a round and its cost are recorded, never de-escalating inside a phase, never cascading a phase, one notch below and never two, the classes never explored, the false-economy reversion, and reading the record's summary before a wave and reverting what it names — holds as written.

## The principle

**Pay for judgment that nothing downstream re-checks.** Work whose output a machine or you re-check — a test suite, a quality gate, a « nothing observable changed » diff — runs at the cheapest tier that closes it: an error there is caught cheaply. Work that nothing re-checks — your own sequencing, a contract later phases consume, the final verification — runs at the top tier, because an error there is paid N times. The target is the cheapest pair observed to close a class IN ONE ROUND, and a pair comes from measurements and readings taken before the dispatch, never from how hard the phase looks. The cost that ranks pairs is the measured cost of a dispatch closed to satisfaction, its corrective rounds included; never read the subscription gauge to choose.

How the tables are measured, generalised and exported: `references/calibration.md`.

## Pairs, tiers and the map

A dispatch runs on a **pair** `<alias>/<effort>`: a family alias and an effort, one of `low`, `medium`, `high`, `xhigh`, `max`. `spawn --model <alias> --effort <level>` sets it; `--model` without `--effort` is refused, and so is an agent given neither `--tier` nor `--model` (decision 3 of `docs/agent-dispatches.md`). Three tiers name capability: `deep`, `standard`, `light`. Their binding is the operator's, in `<state dir>/models.json`, a model alone (`"a-model"`) or a pair (`{"model": "a-model", "effort": "medium"}`); `iterm-agent.sh resolve-tier <tier>` prints `<model>` or `<model>/<effort>`. `spawn --tier` takes the effort from `--effort`, else from the map, else the effort the plugin ships for the tier — `standard` high, `light` medium — and `deep` runs at your own live effort, read on your transcript. **Read your map before dispatching a wave.** An unbound tier is not an error (the host applies its default model, the tier's effort still typed): when the work needs it, pick the model you judge fit — `--model <name> --effort <level>`, or the host's default model on purpose — write the choice and its reason in the brief, and tell the operator in one line at the spawn. The map is his and binds every project: a binding the mode check refuses is put to him. A pair `pick` returns for one class or one project goes in the brief, the record and `calibrate`'s project table, never in `models.json`, which the module keeps from your writes.

**A tier or a pair names a family alias, never a versioned identifier**; the launcher warns on a versioned binding.

**A session nobody watches runs in the operator's decision mode**, which the launcher checks on the transcript, refusing a spawn that came up in another. A binding the host does not run in that mode is fixed by a rebind, or by `--permission-mode acceptEdits` for an agent of a few edits and allow-listed commands. Name the mode in the brief where you name the pair.

## Where the pair comes from

Before each dispatch, run `routing.py pick --repo <checkout> --class <class> --record <record>
--files <n> --lines <n>` (`${CLAUDE_PLUGIN_ROOT}/skills/model-routing/scripts/routing.py`). It
prints the pair and the table it came from — the project's, its profile's, the global one, a
shipped default, or the tier table below. Write the pair, its source and your reason in the
brief. You may override it: say why. An entry marked `stale` was measured on a model the alias
no longer resolves to; use it, and tell the operator in one line that a bench run would refresh
it.

`--files` and `--lines` are the phase's size, given together or not at all: the files in the
phase's scope and the lines the plan expects it to add and delete, test files left out. Given
them, `pick` adds `size=small` or `size=large` to its first line, and an entry measured only on
small work does not serve a large phase: it goes on down its order to the first entry measured
on large work, or to the tier table, and prints `size=large beyond=<scope>`, naming the first
scope it skipped. That scope was measured on smaller work than this phase: say so in the brief
beside the pair and its source.

**A phase beyond every measured size.** When `pick` served a large phase from a scope after a
`beyond=`, or from the tier table, no table was measured at this size. Before dispatching the
phase, run a read-only search exploration at the `search` class's pair and write its summary
(the files, the contracts, the decisions) into the brief: the pair is a guess, so give it a
map.

**The order `pick` reads, class by class:** the project's table, its profile's table, the global table (all three measured, in `<state dir>/routing/tables/`), the shipped profile then global defaults (`defaults/`, in tier form, read through the map), and last the tier table below, the map binding the tier the class falls to. `models.json` is the last fallback, not the default: it decides every class no table measures. A new project with no table of its own gets, for each class, the first of its profile's and the global table that measures it, and the tier map for the rest. Measured tables stay in the operator's state directory: `defaults/` ships only its README until the operator commits an `export`, so on a fresh install the same project falls to the tier map.

`routing.py profile <checkout>` prints the inferred `<language>/<kind>`; a `profile` in the project's manifest overrides it, and `pick` takes the override first. A line `pair=host-default` means the class's tier is unbound: the paragraph on unbound tiers above applies.

## Calibrating a new project

`/orchestrator-calibrate <checkout> --max-usd <cap> --class <class> --pr <n>...` does it: it runs steps 1 to 4 below in order, stops at the first failure, and leaves 5 and 6 to the operator. It refuses to run without his cap and never picks one. Run by hand, these are the `routing.py` subcommands, in this order. Everything lands under `<state dir>/routing/`; `references/calibration.md` has the detail of each step.

1. `harvest <repo> --class <class> --pr <n> [--pr <n>]... [--test-command <cmd>] [--test-glob <glob>]... [--budget-usd <x>]`: needs merged pull requests whose merge commit is in the local clone. Drafts one task per pull request in `projects/<slug>/manifest.json`, its brief in `projects/<slug>/briefs/pr-<n>.md`.
2. `ready <slug> <task-id>...`: the control run. Needs the manifest's `test_command` and `test_globs`. Runs the tests on each task's merged commit and marks it `ready`, or `void` when its own reference fails.
3. `bench <slug> --max-usd <n>`: the spend cap, given by the operator and required; `--budget-usd` caps each trial. Needs ready tasks and the `deep` tier bound (the judge). Runs the grid of pairs on the ready tasks and appends each trial to `projects/<slug>/trials.jsonl`.
4. `calibrate <slug>`: writes the project's table, `tables/project-<slug>.json`, which `pick` reads first.
5. `generalize`: no argument. Pools every project's trials into `tables/profile-<language>-<kind>.json` (two projects of a profile or more) and `tables/global.json`.
6. `export [--to <dir>]`, on the operator's word only: writes the profile and global tables in tier form into the plugin's `defaults/`, the only step that ships anything.

## The table

The floor `pick` lands on when nothing is measured: the class's tier, through the map. The slug is the `--class` `pick` and the record take.

| Class of work | Slug | Tier | What re-reads its output |
|---|---|---|---|
| You, your successor, a decision round | `orchestrator`, `successor`, `decision-round` | `deep` | nobody |
| A phase that **defines a contract** a later phase consumes verbatim | `contract-phase` | `deep` | nothing until phase N+1 pays for it |
| The final verification phase (spec conformity, norms over the full diff, E2E) | `final-verification` | `deep` | nobody |
| A behaviour phase with the contract already fixed | `behaviour-phase` | `standard` | the test suite, then the review round |
| A conversion phase (move, rename, extract) | `conversion-phase` | `standard` | « nothing observable changed »: the suite judges |
| An N-bis corrective on a findings list | `n-bis` | `standard` | you, on the artifact: the diff, the decisive tests |
| A review collector, a comments agent | `review-collector`, `comments` | `standard` | you verify every finding |
| The review lenses, dispatched as the subagent type `orchestrator:lens` | `review-lens` | `standard` | the collector, then you |
| The screenshot audit of a pull request, dispatched as the subagent type `orchestrator:screenshots` | `screenshot-audit` | `standard` | you, on a capture in doubt |
| Read-only search subagents | `search` | `light` | they locate; they never judge |

The tabs you launch and the subagents launched inside a session read this one table: say the lenses' pair in the review brief.

## The five readings

For a phase that does not sit plainly on a row, take these before dispatching, from the plan and the decision log:

1. **Contract novelty** — does the phase publish a signature a later phase consumes verbatim?
2. **Proof shape** — « nothing observable changed », or « the behaviour changed and a test drives it »?
3. **Blast radius** — files in scope, consumers downstream.
4. **Residual ambiguity** — questions still open on this phase in the decision log.
5. **Repair history** — findings that survived a round on this phase or its class.

Read the third and the fourth concretely. **Blast radius** is high when the phase touches files > 3 or lines > 50 (the thresholds of `--files` and `--lines`, so the reading and `pick` agree), creates a new file, or touches more than one module. **Residual ambiguity** is high when one question or more is open on the phase. The counts of the blast radius are what `pick` is given.

Two readings high or more raises the pair by **one** notch up the class's ladder (the pairs of its table entry, ordered by measured cost per closed dispatch), never more, never as a running total: the readings are retaken at each dispatch.

## The correction round runs one notch above its phase

`pick` ends with `nbis=<pair>`: the phase's pair one effort level up on the same family, the same pair at `max`, and no line for a pair with no effort to raise. The phase's correction round runs at that pair, and the brief names it; the phase itself is never retried at its own pair. `--class n-bis` serves a correction round whose phase's pair is unknown: the round runs at that call's `pair=` line, and its `nbis=` line is not read.

## Explore one notch, never more

`pick` prints `explore=<pair>` (`nbis=` stays last) when the record allows a try one notch below: take it only when the five readings show at most one high, and open the row `--explore`.

`summary` prints `frozen=<class>` after a failed exploration (the class reverts and is not explored again this build) and `promote=<class> <pair>` after three that closed in one round (dispatch the class on that pair, and fold it into the project's table with `routing.py calibrate <slug> --from-record <record>`).

## Escalate on evidence, one step, at a session boundary

Triggers, each a thing you have read:

- the same class of finding survives one N-bis round;
- the agent STOPs twice on the same ambiguity;
- the agent crosses the context gate without a single push.

An escalation IS a rotation — fresh session, resume brief, one notch up the class's ladder, the brief carrying the evidence that triggered it. **Never de-escalate inside a phase**: a drop applies to the next dispatch of that class.

## The false economy

**A pair drop that produces a second corrective round is reverted for that class, and the reversion is recorded, unless you name the mechanism, other than the pair, that cost the round.** The summary's `signal=` lines name those drops (« The record »).

## A second reader, armed by evidence

A defect found later in work already approved is recorded with `dispatch-record.sh escaped <record> <id>`: `summary` then prints `signal=double-read <class> at <pair or tier>`, and that class's next round gets a second reader with a DIFFERENT lens, a finding kept only when both see it.

## The record

One row per dispatch in the project's build state: class, pair (or tier), rounds to close, measured cost, verdict. It corrects the table for this build, and your succession brief points at it. Keep it with `${CLAUDE_PLUGIN_ROOT}/skills/orchestrator/scripts/dispatch-record.sh`:

```
dispatch-record.sh open <record> --class <c> --model <alias> --effort <level> [--explore] --label <what>   # prints the row id
dispatch-record.sh open <record> --class <c> --tier <t> --label <what>   # a tier row, when no pair is chosen
dispatch-record.sh round <record> <id>                                  # a review round happened
dispatch-record.sh review <record> <id> --head <sha> --norms tool|none  # and what it read
dispatch-record.sh fixed <record> <id> --head <sha>                     # the one correction round, verified
dispatch-record.sh surface <record> <id> --ui <owner/repo>#<n>|--minor <reason>|--none  # whether the pull request changes what a user sees
dispatch-record.sh audit <record> <id> --head <sha> --images <n> [--defect "<text>"]...  # the screenshots agent's audit of the images on a --ui pull request, read by ready
dispatch-record.sh ready <record> <id> --head <sha> --e2e "<the E2E line>" [--e2e-waiver "<his words, dated>"]  # refuses a head neither reviewed nor fixed, no surface, a --ui pull request with no image, no E2E line, or E2E: none unvalidated, or a row with no review
dispatch-record.sh exempt <record> --e2e "<his words, dated>"          # the operator exempts every pull request of this session from E2E
dispatch-record.sh close <record> <id> --verdict approved
dispatch-record.sh cost <record> <id> --session <session id>         # after each session of the dispatch ends
dispatch-record.sh summary <record>
```

`review` records instead of `round` the head it read and whether the project's own norms tool ran (`tool`) or the project ships none (`none`). `fixed` records the ONE correction round at the head you verified on the artifact; with no review on the row, or a second time, it replaces the recorded correction and warns. `ready` stands in front of telling the operator a pull request is ready: it passes at the head the last review read or the one its correction round was verified at, and refuses any other, and a row with no review. It is the pre-check of what the github ready gate does not read, never the ready. `cost` adds a session's measured cost to the row once that session ends — its id is the one the spawn verified — so a dispatch's corrective rounds count in what it cost; a model with no price marks the row `cost_incomplete`.

The summary groups rows by class and pair, with `cost_avg=<usd>` over the closed rows whose cost is complete, and prints `frozen=<class>` and `promote=<class> <pair>` for the explorations above.

**Read the summary before a wave, and revert what it names:**

```
signal=n-bis at light averages 2 rounds: the drop did not pay, revert it for this class
```
