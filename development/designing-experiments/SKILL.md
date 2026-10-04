---
name: designing-experiments
description: "Writes AQVEN experiments: one factor (agent, prompt, use or flow), variants and checks, ground truth, negative controls, one population. Use first when asked whether one prompt, model, node or flow matches or beats another, before editing experiments/, and before claiming an effect."
---

## MUST

- Compared things are variants (rows); measures are checks (columns). Two implementations of a step, two prompts or
  two models are variants of one factor, never two checks on one variant.
- An experiment changes exactly one factor, `varies` with `what` and `nodes`. Everything else that differs
  between variants (data, the set of questions, preprocessing, population) is listed before the run and is zero.
- Correctness is measured only against ground truth (known by construction, such as a planted defect, or a label
  from the source) with a negative control from the same population. Agreement of two readings is
  reproducibility, not correctness.
- One check, one claim. The property a claim is about comes from the case's tag.
- The primary metric is the job of the stage under test, taken from the owner's goal: what its output feeds and
  which error costs more there (a miss, a false alarm, cost, latency). Named before the data.
- The current best configuration is a variant of every comparison; numbers are never borrowed from another series.
- The design is never cut to fit the spend cap: the cap is the owner's decision (`running-series`).
- An experiment that has a series is frozen: a change to its question, metric, factor, variants, cases, plan or
  checks gets a new id whose `experiment.md` links the old id and its series. Only `archived: true` comes later.
- Restate the question in the owner's words and get a yes before building the experiment.

## The experiment folder

```text
experiments/<experiment_id>/
  experiment.yaml
  experiment.md          notes: Contract, Validity, Purpose, Falsifier, Decision, Failure modes
  nodes/<alt>/...        alternative nodes: .node.yaml, .py, .inference.yaml, .prompt.md
  prompts/<name>.md      alternative prompt texts
  flows/<flow_id>/...    local flows: flow.yaml with nodes/, or flow.py
  findings/<series>.yaml written by the server, never by you
```

A module of your own checks may sit in the folder too (`checks.py`, referenced as
`run: "@root.experiments.<experiment_id>.checks:<function>"`). A flow anywhere else in the folder is
`E_ORPHAN_FILE`. Write the files one per call with Write, or start with **New experiment** in Studio's Research
(it writes `experiment.yaml` and prompt files). Code steps of local flows and alternatives: write
`experiment.yaml` first, run `uv run aqven generate <package>`, and copy their class names from the generated
`types.py`; they carry the experiment prefix (`<Experiment><Node>Out`, `<Experiment><Flow><Node>Out`).

| `varies.what` | Slot | A variant's value | Use it for |
|---|---|---|---|
| `agent` | an llm node | an agent id of the project | another model or model settings with the same prompt and schema |
| `prompt` | an llm node | the name of `prompts/<name>.md` | other prompt text with the same inputs, output schema and inference checks |
| `use` | any node | an alternative id from `nodes/` | another algorithm of a step; another container (`map` against `parallel`); a model with a prompt tuned for it, as one alternative llm node with its own agent, inference and prompt |
| `flow` | a `call` node | a flow id, local from `flows/` first, else a project flow | another split of the task into steps; the flow keeps the slot's input and output types |

- A variant sets only `nodes: {<slot>: <value>}`. A variant without `nodes` is the subject as written, and so is
  a factor node a variant leaves out. Keys are local node ids (file names), nested nodes included.
- A `use` alternative runs under the slot's id, so bindings below it (`$aggregate.out.level`) stay; its `in`
  and `out` match the slot, or the compiler error comes back prefixed with `variant <id>: `.
- `subject.flow` finds a local flow of the experiment first, then a project flow; `from` and `to` narrow the run.
- An A/A experiment keeps every variant as written and declares no `varies`: `compare` with `margin: 0`
  measures the noise floor.
- Lumen shows each kind's mechanism, not a design to copy: `agent` in `intent_escalation_agents` and
  `reply_noninferior_mistral`, `prompt` in `panel_judge_prompt`, `use` in `panel_merge_rule`, `flow` in
  `intent_split_long_messages` and `panel_single_judge`, A/A in `panel_aa_noise`.
- A variant's fingerprint comes from the assembled flow: editing an alternative, a prompt from `prompts/` or a
  local flow makes earlier series of it stale.
- An answered experiment gets `archived: true` in `experiment.yaml`, the only edit allowed after a series. Studio
  lists it under Archived; `aqven check` and series treat it as before. Never delete it or reuse its id.

Example, Lumen's `intent_escalation_agents`: an `agent` factor on one llm node, run over a range, each agent a
variant, the same checks on every row:

```yaml
apiVersion: "aqven/v1"
kind: "Experiment"
description: "Qwen as the escalation agent decides the support lead's intent at most 0.1 less often than DeepSeek on the recorded triage, with no more invalid first outputs and at most 25% slower at p95"
failure_mode: "intent_misread"
subject:
  flow: "escalation"
  from: "escalate"
  to: "escalate"
varies:
  what: "agent"
  nodes:
  - "escalate"
cases:
  dataset: "support_case_cases"
variants:
- id: "deepseek"
- id: "qwen"
  nodes:
    escalate: "qwen"
- id: "gpt"
  nodes:
    escalate: "gpt"
checks:
- id: "intent"
  kind: "binary"
  use: "expected"
  with:
    fields:
    - "intent"
question:
  kind: "noninferior"
  baseline: "deepseek"
  candidate: "qwen"
  primary: "intent"
  margin: 0.1
  guardrails:
  - metric: "schema_valid_first_try"
    margin: 0.05
  - metric: "latency_p95_ms"
    direction: "lower_is_better"
    margin: 0.25
    relative: true
plan:
  cases: 12
  repeats: 3
```

`deepseek` has no `nodes`: it is the flow as written and the current best. The range takes `prepare` and `triage`
from each case's `node_outputs`, so every variant reads the same upstream output; `gpt` runs on the same cases for
the cost and quality view, and the verdict compares only `baseline` and `candidate`.

A check scores every case it runs on: it returns a `Verdict`, and anything else is an error attempt, not a skipped
case. A rate over part of the cases is an experiment of its own, selected with `cases.tags`: Lumen's
`critique_recall_by_agent` takes `planted: "yes"`, and the clean copies (`planted: "no"`) are the negative control.

Questions: `look`, `threshold` (`metric`, `above` or `below`, `margin`, optional `variant`; without it every
variant must clear the bound), `compare` and `noninferior` (`baseline`, `candidate`, `primary`, `margin`,
`guardrails`). Metrics are check ids or series metrics: `success_rate`, `cost_usd`, `cost_of_pass`,
`latency_p50_ms`, `latency_p95_ms`, `schema_valid_first_try`, `infra_error_rate`.

## Experiment designs

- **Comparing flow designs**: no design is the default. The current flow (the simplest one when nothing runs yet) and
  each candidate are `flow` variants of one `call` slot in a local subject flow, with the same input and output; a
  design that fits one container node is compared with `use` on that node. A candidate that calls the model more
  also meets a variant of equal budget. The project flow stays flat: the winner is written into it later
  (`building-flows`), and the slot leaves with the experiment.
- **Input ablation**: one dataset holds every candidate input (a ticket with or without account history, an
  invoice image with or without its OCR text, a clip with or without its transcript). A `use` factor on a `code`
  step before the llm node blanks what a variant leaves out (a `Text?` field set to null, an empty list), and the
  prompt renders each field under `{% if <field> %}`. k inputs: all of them and each one left out (k+1 variants),
  plus the current best. A `prompt` variant that drops an input fails `E_PROMPT_INPUT_UNUSED`, and media inputs
  are attached whatever the prompt says.
- **Screen, then confirm**: many candidates get a small `dev` series first, with a drop rule written in
  `experiment.md` before the start (an interval wholly below the best variant's, or below the trivial baseline);
  then a new experiment on the survivors and the current best. Interim numbers decide drops, never claims.
- **One stage**: a range subject (`from` and `to`) ending at the stage's top-level node scores its output with
  every check; a `run:` check on the whole flow reads it from `context.metadata["node_outputs"]`. Derived truth
  informs only when the best constant answer scores well below 1.

## Validity gate

Write every item into the Validity section of `experiment.md`. No series starts while any item is "no".

| # | Step | Exit criterion |
|---|---|---|
| 1 | The question in the owner's words: "the experiment answers…; metric M means…" | the owner said yes |
| 2 | The stage and its metric: which part of the flow, what its output feeds and which error costs more there ("Now" in `EXPERIMENTS.md`) | the primary check measures that stage's job |
| 3 | The factor: kind from the table, slots, values; compared things are variants, measures are checks | `aqven_check` gives no factor code |
| 4 | Everything else that differs between variants: data, the questions or instructions the model gets (a case's category or file name must not choose them), preprocessing, population. A variant that adds or removes an input differs only by the block that renders it; an instruction change in a prompt that reads another step's output is part of the factor and listed | the list is empty or the difference removed |
| 5 | The subject reproduces the production path: the preprocessing production applies (crops and resolution, audio segments, text chunks, OCR or transcription), only inputs production has, a prompt that asks for the measured behavior; the subject's `prompt_preview` matches production except for the factor; read the files in `prompts/` or `nodes/`. Variants and local flows have no preview yet: a one-case smoke, then `run_get_node` on the llm node shows what was sent; an `agent` variant on a project flow's node can be tried on one case with `run_start` `agent_overrides: {<node_id>: <agent_id>}` | previews, files or sent prompts read |
| 6 | Ground truth: known by construction (a planted defect, a generated value) or labels from the source; a negative control from the same population; a synthetic case only when it really has the property it is labelled with (`preparing-media-inputs` for media). Truth inferred from a label of another property is named "proxy", its table marked for the owner's sign-off, and its errors split into "contradicts the label" and "outside the label's scope" | truth and control named |
| 7 | One check per claim: the property from the case tag; a check always returns a `Verdict`, so a rate over part of the cases is its own experiment selected with `cases.tags`; a missing field reads as "unknown", never as "absent"; the unit of the metric is the unit of the claim | the check gives no `no_data` on saved outputs |
| 8 | Trivial baselines (a constant, the majority, "call everything") computed before the threshold, for stage and intermediate metrics too | the threshold is above them |
| 9 | The margin is reachable: `launch.mde`, `launch.recommended.reason` (`no_margin`, `short_of_cases`, `wide`) and `below_recommended` from the `series_start` answer of a `dev` smoke | no `below_recommended`, or the owner agreed |
| 10 | Controls false by construction; a multi-call pattern against a variant of equal budget; a random list of the same length | the control cannot leak |
| 11 | A new check tried on outputs of an earlier series: `series_list` `{experiment_id}` finds it; `pytest_run` over `series_outputs` rows with `split: "dev"` and `fields` for what the check reads, or over `aqven series export <series_id> --path <package> --split dev`; an exact 0.000 or a zero-width interval is a bug until proven otherwise | the check's numbers are plausible |
| 12 | `dev` and `holdout` from one population; the threshold set before the data and never moved after. Numbers from two experiments are compared only when both select the same cases of one dataset: the split hashes the package, the dataset id and the case name, so a dataset built from the same inputs splits them anew, and an input seen on `dev` anywhere is spent for holdout | the splits look alike; case sets agree |
| 13 | Expected outcomes and how to read each written before the first number (Purpose, Falsifier, If confirmed) | written |
| 14 | Anything to change after a series: question, metric, factor, variants, cases, plan or checks | a new experiment id and folder; its `experiment.md` links the old id and series |
| 15 | An intermediate output feeds the step under test | in a 10-case pilot each of its fields varies across the classes the next step separates (`designing-output-contracts`) |

## `aqven check` codes of the factor

| What is wrong | Code | Fix |
|---|---|---|
| more than one variant and no `varies` (unless every variant is as written) | `E_FACTOR_MISSING` | declare the factor |
| a node of `varies.nodes` is not in the subject | `E_FACTOR_NODE_UNKNOWN` | the local node id, the file name |
| `agent` or `prompt` on a node that is not llm; `flow` on a node that is not `call` | `E_FACTOR_KIND` | another factor kind or slot |
| a variant sets a node outside `varies.nodes` | `E_VARIANT_OUTSIDE_FACTOR` | add it to the factor or drop it from the variant |
| an alternative missing from `nodes/`; an alternative with a subject node's id | `E_ALTERNATIVE_UNKNOWN`, `E_ALTERNATIVE_ID_TAKEN` | the alternative's file name |
| no `prompts/<name>.md`; no such agent; no such flow in `flows/` or the project | `E_PROMPT_MISSING`, `E_AGENT_UNKNOWN`, `E_FLOW_UNKNOWN` | the file or the id |
| the plugged flow takes or returns other types than the slot's flow | `E_FACTOR_FLOW_CONTRACT` | align the input and output types |
| a local flow with a project flow's id | `E_ID_DUPLICATE` | rename the local flow |
| an assembled variant does not compile | the compiler's own code at `variants[i].nodes.<slot>`, message `variant <id>: …` | fix the file the message names |
| two variants with the same values; an alternative, prompt or local flow no variant uses | `W_VARIANT_DUPLICATE`, `W_ALTERNATIVE_UNUSED` | remove it |
| keys the variant or subject no longer has, a flow outside `flows/` | `E_UNKNOWN_KEY`, `E_ORPHAN_FILE` | follow the hint in the message |

## Pitfalls

| What goes wrong | Do instead |
|---|---|
| Alternative implementations of one step written as checks on one variant | one variant each, a `use` factor on that node |
| Local flows copied byte for byte just to change one prompt | a `prompt` factor with files in `prompts/` |
| The primary check measured "found anything", not the property the hypothesis is about | a check per claim, the property from the tag |
| A case's category chose which instructions the model got, so variants differed in more than the factor | fix the instructions; list every difference |
| Variants meant to differ in one input also differed in prompt wording | one template; variants differ only by the block that renders the input |
| A comparison read across two series inside their noise band (one variant scored 0.39 to 0.48 across runs) | the current best as a variant of the same series; the cases it lost and won |
| The union of two separately run variants promised more than the combined step delivered | a variant that runs the combination |
| A many-model series was cancelled halfway, then paid again on the same cases | screen, then confirm |
| Proxy truth counted correct findings the label never covered as false positives | split the error metric; the proxy marked for sign-off |
| Many series measured agreement of two readings | ground truth and a negative control |
| Models compared on synthetic data while labelled data sat in the project | an `agent` factor on labelled data |
| A whole-flow threshold put on one step whose job is different | that step's own metric (MUST) |
| One design built as the answer: the owner never saw the alternatives, and nothing measured it | the current or simplest design and the candidates as variants (Comparing flow designs) |
| An agent re-checked with `agent_overrides` on a few cases, reported as a comparison | one run proves one case; a comparison is an `agent` factor |
| Hard cases only in the confirmation data: `dev` and `holdout` disagreed | one population |
| Repeats cut and a series split in two to stay under the spend cap | the design stays; the owner decides spend |
| A downstream decision measured (the ticket was escalated) instead of the claim (the fault was found) | the metric of the claim |
| The subject's prompt forbade the measured behavior | step 5 |
| A stand-in measured instead of the production input: a synthetic "blurry" case sharp where the text is, a downscaled page where production sends crops, a clean transcript where it sends noisy audio, the first 4,000 characters of a long contract | step 5 and step 6; `preparing-media-inputs` |
| Half of the hypothesis tested | one check per part |
| An effect claimed from one run, against a variant whose inputs were empty | n and the inputs first |
| A margin that needs more cases than `dev` holds; a constant answer ("escalate everything") beat every model | step 8 and step 9 |
| Cases the claim does not cover scored as failures; pairs counted where the claim is about single answers | select the covered cases with `cases.tags`; the unit of the claim |
| A control that could pass by a shortcut; a "breakthrough" from a provisional verdict | controls false by construction; wait for `done` |
| The metric swapped, or the variant list cut, in an experiment that already had a series | a new id (step 14) |

Good habits: no guard threshold at n=1; a new check smoked on `dev` first; cases never picked by a model's result.

## Tools and commands

- `aqven` MCP `aqven_check`, `prompt_preview`, `pytest_run`, `series_start` (a `dev` smoke, see `running-series`),
  `run_get_node` (what a variant's llm node sent), `run_start` (`agent_overrides`), `series_list` (earlier series
  of an experiment), `series_outputs` (their outputs on working cases; held-out cases are read only as totals).
- `uv run aqven series export <series_id> --path <package> [--format jsonl|csv] [--fields FIELD …] [--split dev]`.
- `uv run aqven refs experiment:<id> <package>`; `uv run aqven tree <package>` lists local flows and alternatives;
  `uv run aqven generate <package>` writes their classes into `types.py`.

## References

- `references/engine/experiments.md`, `references/reference/experiments.md`: every key, every question kind, all
  `aqven check` codes of experiments, and the experiment designs worked out. Read before writing `experiment.yaml`.
- `references/concepts/validity-gate.md`: the gate above with worked examples. Read before step 1 of the gate.
- `references/concepts/metrics-and-controls.md`: ground truth, negative controls, agreement against
  correctness, one check per claim, a stage and its metric. Read at steps 2, 6 and 7.
- `references/engine/lumen-patterns.md`: a real experiment of every factor kind. Read before the first
  experiment of a factor kind.
- `references/engine/call-node.md`: the `call` slot for a `flow` factor. Read before a `flow` factor.
- `references/concepts/experiments-series-and-findings.md`, `references/concepts/how-a-series-decides.md`: why
  the question comes first, intervals, margins, verdicts. Read at steps 8 and 9.
- `references/engine/custom-evaluator.md`: writing a `run:` check. Read at step 7.
