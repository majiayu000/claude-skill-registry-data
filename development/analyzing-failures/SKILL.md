---
name: analyzing-failures
description: "Turns AQVEN runs into agreed failure modes: first failing node, owner-read traces, riskiest hypothesis first, one check per claim. Use first when runs are in but answers look wrong, when asked for a check of how often an output fails, and before any hypothesis."
---

## MUST

- Offer the owner the first traces. If the owner declines, record it, read them yourself and write the notes; the
  owner confirms the modes. Never invent modes without reading traces.
- A question about the data is asked through a check of an experiment, never through your own script over REST
  or over `.aqven/`: the engine scores a check on every attempt and the owner sees it. A stage is measured by an
  experiment whose subject range ends at that node (`designing-experiments`).
- New check functions need no server restart: project Python reloads on the next run.
- Test the owner's premise on data already paid for before spending more.
- Outputs of a series are read in bulk with `series_outputs` (or `aqven series export`), never one `run_get` per
  attempt, never `.aqven/`; both return working cases only, and held-out cases are read only as totals.
- Web search is for literature only, never for facts about the engine.

## Procedure

| # | Step | Exit criterion |
|---|---|---|
| 1 | A `look` experiment on `dev` with cheap deterministic checks and `repeats: 1`, or `series_start` with `look` over named cases; then `series_get` `view: "summary"` for the failure groups per variant, and `series_outputs` `{series_id, split: "dev", outcome: "failed"}` (then `"error"`) with `fields` naming the output pointers and node ids you need | every failing row read |
| 2 | For each failed attempt: the first failing node (`debugging-runs`), infrastructure error or counted failure | a table attempt → node → code |
| 3 | Offer the owner about 30 traces: failures first, then a few passing ones, each with its `run_id` from the `series_outputs` rows, the Studio link `/runs/<run_id>` and the first failing node; ask for one short note per trace. A decline is recorded in the look experiment's `experiment.md`; then you read the traces and write the notes | notes received, or written by you after a recorded decline |
| 4 | Group the notes into modes: an id, a one-line definition, a count, 2 or 3 `run_id`s | the list agreed and written under "Failure modes" in the look experiment's `experiment.md` |
| 5 | Filter: specification gap, wiring, infrastructure, generalization gap | experiments only for generalization gaps |
| 6 | Scan literature and the web for the riskiest assumptions, and for designs others measured on this kind of task, each written down as an option to test, not a plan; mark domain assumptions that need an expert | sources cited |
| 7 | Order: first the hypothesis that could kill the product, then by count and harm; check ordinal fields for a pull to the middle | the hypothesis list agreed with the owner |
| 8 | One check per claim: what the claim is about comes from the case (a tag or `expected_output`), never from what the model happened to say; "returned something" never measures "returned the right thing" | every claim has a check that can refute it |
| 9 | Test the owner's premise, and any proposed design, on paid outputs before building it. Any design built from outputs already paid for (a rule in code over several variants' outputs, a filter, a merge): a test with `pytest_run` over `series_outputs` rows (`split: "dev"`, `fields` naming the pointers and node ids the rule reads) or `aqven series export --format jsonl`; `map` items, branches and loop passes are not in `node_outputs`, so read those with `run_get_node`. A downstream model stage: its ceiling from a range experiment on that stage with the upstream truth in `node_outputs`, next to its value on the upstream outputs it really gets. Each result is a hypothesis until a variant runs the design | a conclusion from outputs already paid for, or from one small range experiment, before the design is built |
| 10 | Label audit on the cases every variant fails: open each input and its label next to every variant's answer (`series_outputs` `{series_id, case}`), count the disputed labels, hand them to the owner or an expert | the count handed over; no label changed without sign-off |

Stop adding modes when about 20 new failing traces add none. Few failures means the cases are too easy, not
that the flow is done.

## Pitfalls

| What goes wrong | Do instead |
|---|---|
| Traces promised to the owner and never delivered; failure-mode ids invented by the agent | offer the traces; after a recorded decline read them yourself, and the owner confirms the modes |
| Experiments designed before the risks were ranked, so the owner has to point at the riskiest assumption | step 7 before any experiment |
| A check that passes when the output holds anything at all: "extracted a total" passes on an invoice where the model read the tax line | a check per claim, its subject from the case tag or `expected_output` |
| Series analysed for hours with a private script over REST, on the belief that new checks need a restart | write the check; the engine reloads it |
| Outputs of hundreds of runs collected by subagents making one read each, then read from the engine's files under `.aqven/` | `series_outputs` pages of up to 200 rows, or `aqven series export` |
| Series after series score how often two model readings agree, not whether either one is right | ground truth and a negative control (`designing-experiments`) |
| A combination of three event taggers on warehouse camera clips, estimated from their separate series, promised more than the combined step delivered | the estimate is a hypothesis; a variant that runs the combination confirms it |
| Every model "failed" on the same call recordings, whose labelled intent the caller never stated | step 10: a label audit before blaming the models |
| The owner spots problems in the case rows before the agent does | read the case rows and traces yourself after every series |
| Good: a design the owner proposed (combining two readers' outputs, adding a second stage) was estimated on outputs already paid for, and the estimate decided whether to build it | do the same |

## Tools and commands

- `aqven` MCP `series_start` (`look`), `series_get` (`view: "summary"`, `include_cases: true`), `series_outputs`
  (`split`, `variant`, `case`, `outcome`, `fields`, `cursor`), `run_get_node`, `run_events`, `pytest_run`.
- `uv run aqven series export <series_id> --path <package> --split dev [--format jsonl|csv] [--fields F …]`.
- Never `.aqven/` files or server logs: what `series_outputs`, `run_get_node` and `run_events` cannot give is a gap
  in AQVEN; tell the owner.
- Web search and fetch for literature only.

## References

- `references/concepts/finding-the-node-that-went-wrong.md`: the first failing node and cascades. Read at step 2.
- `references/mcp-cli/research-loop.md`: finding what to test, failure mode to experiment, cases and checks,
  designs estimated on paid outputs. Read before step 3 and at steps 8 and 9.
- `references/mcp-cli/experiments-and-series.md`: `series_get` `view: "summary"`, `series_outputs` rows, filters
  and `fields`, the split. Read before step 1.
- `references/studio/investigate-a-run.md`: what the owner sees at `/runs/<run_id>`. Read before step 3.
- `references/engine/custom-evaluator.md`: writing a `run:` check. It returns a `Verdict` on every attempt, so
  a rate on part of the cases gets its own experiment with `cases.tags`. Read at steps 8 and 9.
- `references/concepts/hypothesis-categories.md`: categories of hypotheses and their setups. Read at step 7.
- `references/concepts/literature-scan.md`: where to search, what to write down, how to mark what is
  unverified. Read at step 6.
