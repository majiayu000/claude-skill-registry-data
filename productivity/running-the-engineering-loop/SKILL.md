---
name: running-the-engineering-loop
description: "Orders AQVEN work from request to reliable flow: measurable contract, simplest flow, cases, traces, hypotheses, Explore on dev, Confirm on holdout. Use first when starting to build or improve a workflow, when asked to skip cases or traces and go straight to tuning, and after a series or compaction."
---

## MUST

- When the owner asks to skip a stage, name its cost in one line and let the owner choose.
- Working autonomously, keep going through cheap steps inside the task. At the number of experiments the owner
  allowed, update the journal and report with `reporting-results`, then stop.
- After a compaction, invoke the skill of the current stage; re-read `<package>/EXPERIMENTS.md`, `FINDINGS.md`
  and `series_list` for the series since the last entry. Structure comes from `uv run aqven tree <package>` and the
  files, never the transcript; engine facts from the summary stay unverified until a skill confirms them.
- The owner's plans, hypotheses and data policies go into the Planned section of `EXPERIMENTS.md`, standing rules
  into "Owner's rules" in `AGENTS.md`, the moment they are said. Your host's private memory holds at most a pointer.
- Project Python reloads on the next run: a new step, check or type never needs a server restart and is never a
  reason to work around the engine with your own scripts.
- Before a series on `holdout`, tell the owner in one line which claim it tests, why now and what each verdict
  would mean.
- Keep what you promised as a list in your host's todo or plan tool, and report what you dropped. Give short
  statuses in the owner's language.
- Every design you propose is an option with when it fits and the experiment that would decide it; the owner chooses.

## Procedure

| # | Step | Exit criterion |
|---|---|---|
| 1 | Contract in one message, asking only what is missing: purpose; the input contract (the fields and input kinds that exist at run time, with typical sizes and lengths); output; "done" as a check and a number; budget per run and per series; latency per run. Go on in parallel with work that does not depend on the answers | "done" is measurable; dataset columns production lacks are not inputs; the series budget is `research.spend_cap_usd` set to a number the owner named; the contract is in the Contract section of the look experiment's `experiment.md` |
| 2 | The owner's current goal and the part of the flow built now, with what "good" means for it (what its output feeds and which error costs more there: a miss, a false alarm, cost, latency) | the goal in one sentence under "Now" in `EXPERIMENTS.md`, checked again before every holdout series |
| 3 | Open 3 to 5 real inputs of every kind the flow takes: read documents and tickets, listen to audio, watch clips, open tables. For media, long text or tables, load `preparing-media-inputs` | size, length, language, format, noise and what varies between inputs are named |
| 4 | The simplest flow with `building-flows`, with the checklists of `hardening-flows`, `designing-output-contracts` and `choosing-models` | `aqven_check` clean; the preview of every llm node read; one live run on a real input finished and its output reads well in the run view |
| 5 | Cases with `building-datasets`, the project's labelled data first | the count of tag value × split is shown to the owner |
| 6 | Explore and read the failures with the owner (`analyzing-failures`): offer the owner the first traces; on a decline, read them yourself and let the owner confirm the modes | failure modes agreed with the owner |
| 7 | A specification gap (the prompt or the type never asked for it) is fixed in the prompt or the type, then step 6 again | the mode is gone, or it is a generalization gap |
| 8 | Hypotheses and experiments: order them with `analyzing-failures`, write them with `designing-experiments` | the validity gate passed |
| 9 | Explore on `dev`, confirm once on `holdout` with `running-series`; the one-line claim, reason and reading of each verdict before holdout | `verdict.text` quoted as it is |
| 10 | Apply: the winning variant goes into the project flow with `building-flows` or `hardening-flows`; the project flow stays flat (each added part earns its place by its own experiment); regression cases added; the Decision section of `experiment.md` written | `aqven_check` clean; a regression look on `dev` shows no new failures |
| 11 | Journal and report with `reporting-results` | `EXPERIMENTS.md` updated; the report leads with real data |
| 12 | Continue or stop: every "done" criterion confirmed on holdout, budget left (`series_list` `stats.spend_usd`, judge checks included), experiments run against the number allowed, risks left | a new round, or a report of findings, decisions, spend and risks |

## Pitfalls

| What goes wrong | Do instead |
|---|---|
| A clean `aqven check` is taken for a working flow, one run for proof | `check` proves wiring, a run proves one case, only a holdout series proves a claim |
| Threshold hypotheses before the first run; a failure taxonomy before anyone read traces | run a look, offer the owner the traces, then hypothesize |
| A holdout series started without saying why | the one-line claim, reason and verdict reading first; the owner may say no |
| A threshold meant for the whole flow is put on one part | measure each part by the job its output does downstream, named at step 2 |
| An architecture the owner sketched is built at once, in full, as a nested flow | the sketch is one option: build the simplest version, offer the sketch next to one or two alternatives with when each fits, and let a `flow` factor earn each added level; the project flow stays flat |
| Research kept growing after the owner asked to keep it small: more research subagents, and a vocabulary of 60 labels where the consumer needed 8 | a scope limit binds every later step and every subagent; report the gaps it leaves, do not fill them |
| A proposed step took an input the dataset's metadata has but production does not (the caller's account tier from the CRM, for a flow that only gets the call recording) | filter inputs by the input contract of step 1; such a column is leakage, however predictive |
| Plans and hypotheses the owner stated lived only in the host's private memory, and the next session never saw them | the Planned section of `EXPERIMENTS.md` and "Owner's rules" in `AGENTS.md`, written when they are said |
| After a compaction the journal was re-read but not the skill, and the agent searched its own transcript to recall how a local flow is wired | invoke the stage skill; `uv run aqven tree <package>` and the experiment folders hold the structure |
| A rule from a compaction summary ("new Python needs a restart") steers hours of work | re-read the journal and the skill; the engine reloads project Python by itself |
| The owner's "start from the riskiest hypotheses, read the literature" is treated as a detour | it is step 8: `analyzing-failures` orders hypotheses by risk |

## Tools and commands

- `aqven` MCP `aqven_check` after every change; `series_get` (`view: "summary"` first) to read a finished series;
  `series_list` (`experiment_id`) for the history and its `stats` totals; `series_outputs` for what attempts answered.
- `uv run aqven check <package>` when the MCP server is not connected.
- `uv run aqven tree <package>` for the project's flows, types, agents and experiments, after a compaction too.
- Your host's todo or plan tool for the list of promises.

## References

- `references/concepts/engineering-loop.md`: why each stage exists. Read at the start of a task.
- `references/mcp-cli/research-loop.md`: one round from the agent's side, how to find what to test, and the
  table from failure mode to experiment. Read before step 6 and before step 8.
- `references/concepts/stage-exit-criteria.md`: the exit criterion and the metric of every stage. Read at
  steps 2 and 12, and whenever you are unsure whether a stage is finished.
