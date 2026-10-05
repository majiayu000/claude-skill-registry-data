---
name: experiment-planner
description: Use when exploring, continuing, or accepting a deep-learning or computer-science research idea. Converts claims into pilot-first experiment matrices covering diagnostics, failure analysis, authorized execution, evaluation, and paper-story viability.
license: MIT
---

# Experiment Planner

## Overview

Use this skill when the user needs to explore a research idea, continue an
authorized experiment workflow, or accept and interpret results. It turns
claims into a testable story and experiment plan. It is an adapter over existing
research-agent ideas, not a replacement for the user's writing, review,
rebuttal, figure, evidence, or GitHub release skills.

## Core Boundaries

- Default domain: general deep learning and computer science research. Adapt to
  collaborative perception, 3D perception, or autonomous driving only when the
  task context calls for it.
- For discussion-only planning, keep output in chat unless the user asks for a
  saved artifact. When the user asks to implement or run experiments in a
  repository, persist the pre-run result contract: update the paper's final
  LaTeX tables when a manuscript is in scope; otherwise update the existing
  experiment-planning document or create `experiment-plan.md` at the repository
  root.
- Do not launch long experiments, deploy GPU jobs, modify code, or retry failed
  runs unless the user explicitly asks for execution or a still-valid approval
  covers the ordinary continuation. A bounded same-config recovery stays
  within that approval; do not silently expand its scope.
- Do not replace `paper-writing`,
  `paper-review-panel`, `rebuttal-response-skills`, `paper-visual-craft`, or
  `github-project-release`; hand off to them only after the research plan or
  results are ready.
- Treat external projects as references, not installed dependencies. Read
  `references/source-map.md` before discussing provenance or upgrading this
  skill from upstream sources.
- During approved execution, a still-valid earlier user authorization covers
  ordinary implementation, local bug fixes, queueing in-scope runs, and
  evaluation. It does not authorize a new experiment family, dataset, seed
  policy, or paper-only TODO; those remain explicit opt-ins.

## Entry Modes

Choose the mode that matches the current request:

- **Exploration**: turn a new research direction into a falsifiable claim. Use
  the complete matrix for a substantial new study; a small pilot can use the
  minimal question/comparison/protocol-plus-budget/endpoint/decision contract.
- **Approved execution**: continue within the frozen contract and the scope of
  a still-valid user authorization. Do not silently expand the experiment
  family, dataset, seed policy, or resource budget.
- **Acceptance**: compare observed artifacts with the frozen contract and record
  whether the relevant gate passes, fails, or is inconclusive.

For a continuation, load the latest plan, results, and pass receipt when
available.
Reuse still-valid decisions about the claim, baseline, metrics, budget, seed,
and protocol. Do not restart the initial grill, literature pass, or full matrix
unless a material change or unresolved blocker makes it necessary; ask only
questions that affect the next decision.

## Default Workflow

1. **Grill consensus**: for a substantial new exploration, use `$grill-me`
   style interaction to clarify problem, motivation, proposed claim,
   baseline/control, compute budget, success criteria, and unacceptable
   shortcuts. For a small pilot, record only the minimal contract. For a
   continuation, reuse the settled contract and ask only changed or blocking
   questions.
2. **Literature inspiration**: for a substantial new exploration or a changed
   novelty claim, use `$research-evidence` for related papers, novelty risk,
   prior experiment patterns, and unsupported claims. Use `$search-first` when
   the task may need existing code, datasets, tools, or implementations. A
   small pilot may defer this pass when it does not change the decision. Reuse
   prior literature decisions when the claim and scope are unchanged.
3. **Story viability check**: decide whether the idea can support a clean paper
   story: important problem, credible gap, specific method difference, feasible
   validation, and claims that will not outrun the evidence.
4. **Claim freeze**: freeze the smallest verifiable claim before planning runs.
   Avoid changing the story repeatedly while experiments are running.
5. **Contract freeze**: before scheduling a substantial study or full runs,
   define the final main-result, ablation, and necessary diagnostic tables. For
   every metric, record its plain-language definition, unit, direction,
   aggregation, and any delta reference. For a small pilot, freeze only the
   endpoint, comparison, protocol-plus-budget, and decision gate. Use the
   in-scope project's explicit missing-value schema and do not write claims
   from placeholder cells.
6. **Idea validation first**: design the smallest pilot/smoke/sanity experiment
   that can falsify or support the core hypothesis. If multiple GPUs are idle,
   parallelize only independent exploration runs with clear ownership.
7. **Minimum sufficient matrix**: only after the pilot passes, add the main
   result and claim-critical ablations. Add robustness, diagnostics, efficiency,
   qualitative results, or failure analysis only when they support a paper
   claim or answer a credible reviewer question; do not add them for symmetry.
8. **Subagent coordination**: keep the main session responsible for planning,
   task decomposition, and final result acceptance. Use `explorer` for read-only
   repo/config/protocol investigation. Use `worker` for implementation with
   explicit file or module ownership. Do not manually override subagent model or
   reasoning settings unless the user explicitly requests it.
9. **Impact-based validation**: prioritize checks by their ability to block the
   next decision or invalidate the claim. Reuse a passing check or receipt when
   code, data, configuration, protocol, relevant environment, and dependencies
   are unchanged. Run the smallest useful CPU/configuration smoke check, then
   proceed to a feasible authorized GPU pilot; do not add endless CPU gates
   before that pilot. Do not use hashes or hash parity as routine acceptance
   checks.
10. **Run discipline**: test that the command starts and produces plausible
    small outputs; remove test data after smoke checks; launch the full run only
    after the relevant sanity gate passes; inspect early samples, logs, and
    artifacts; stop continuous monitoring once the run is confirmed healthy
    unless the user asks otherwise. Record a compact reusable pass receipt with
    the scope, checks/evidence, decision, and next action; add a command/run
    reference or exception only when needed for interpretation or recovery.
11. **Acceptance discipline**: freeze the acceptance rule, metric, comparison,
    and claim boundary before inspecting the outcome. Never weaken a gate,
    switch the primary metric, or redefine the baseline after seeing a result.
    A diagnostic gate tests a bug, confound, or mechanism; it is not by itself
    the whole scientific verdict.
12. **Explicit-only expansion policy**: record one fixed seed and keep compared
    runs under the same evaluation and checkpoint-selection policy. Use one
    training run by default. New experiment families, datasets, multi-seed or
    repeated-seed policies, or other auxiliary runs require explicit opt-in.
    An earlier authorization covers ordinary implementation, local bug fixes,
    queueing in-scope runs, and evaluation only. A paper TODO, idle GPU, small
    margin, low cost, reviewer expectation, or venue norm is not authorization.
    Keep the resource and time budget honest; mention unrun options only as
    limitations or explicitly opt-in follow-ups.
13. **Default decisions**: ask only questions whose answers materially change
    the plan. If a non-critical choice goes unanswered, use the recommended
    default and record it as an assumption.

## Validation and Failure Taxonomy

Name the relevant gate before running it and do not treat all failures as the
same:

- **Engineering failure**: the command, data path, configuration, checkpoint,
  or artifact contract is broken. Repair the implementation or protocol before
  interpreting scientific results.
- **Optimization failure**: the intended method does not train, converge, or
  improve the fixed target under a fair protocol. Report it as a method or
  tuning failure, not automatically as a failure of the underlying idea.
- **Prototype failure**: a sound, deployable pilot misses its predeclared
  mechanism endpoint, including a negative endpoint despite a plausible
  mechanism. Report that measured benchmark endpoint, but do not infer
  impossibility or falsification of the broader mechanism.
- **Core-construct failure**: the predeclared construct-level test contradicts
  the central hypothesis under the frozen protocol. Close or narrow that claim
  unless new evidence justifies a separately approved design.
- **Inconclusive/blocked**: noisy or confounded evidence, missing support, an
  invalid protocol, or an unresolvable engineering issue prevents a gate from
  being interpreted. Do not relabel this status as a scientific failure.

Diagnostic gates can localize a failure or block a particular interpretation,
but passing one does not establish the entire scientific story. Keep the gate,
evidence, and remaining uncertainty explicit.

## Output Contract

Default to a concise in-chat experiment matrix. Before producing a matrix, read
`references/experiment-matrix.md`. The full 19-field matrix is for a substantial
new study. A small new pilot needs only the minimal
question/comparison/protocol-plus-budget/endpoint/decision contract. For a
continuation, return only changed fields, the next decision, or a compact pass
receipt, and reference unchanged fields from the existing plan.

The substantial-study matrix must include:

- `research question`
- `core hypothesis`
- `paper claim`
- `storyline`
- `literature inspiration`
- `baseline/control`
- `table contract`
- `metric definitions`
- `idea validation experiment`
- `expected signal`
- `failure modes`
- `diagnostic checks`
- `follow-up experiments`
- `subagent/task ownership`
- `compute/resource assumptions`
- `seed policy`
- `success gate`
- `claim gate`
- `next action`

Use the in-scope project's explicit missing-value schema. If none is defined,
use `TBD (pending)`, `N/A (inapplicable)`, or `unknown (needs user input)` as
appropriate; do not force `--` or invent project facts. Keep recommendations
executable, but do not perform execution inside this skill unless the user asks
for implementation or running commands, or a still-valid prior authorization
already covers the ordinary continuation.

## Handoff Rules

- Use `$research-evidence` before making novelty, citation, or literature
  coverage claims.
- Use `$search-first` before proposing new implementation utilities, pipelines,
  tool integrations, or dataset-processing code.
- Use writing skills only after the experiment story is stable enough to draft
  a paper section, rebuttal, review, table, or figure.
- For code work, assign `worker` tasks with disjoint write scopes and remind the
  worker not to revert others' changes.
- For investigation, assign `explorer` tasks that are specific, read-only, and
  non-overlapping with the main session's current work.

## Failure Modes To Catch

- The idea is interesting but not falsifiable with available data or compute.
- The proposed contribution is only a presentation change, not a testable method
  or analysis difference.
- The baseline/control is missing, unfair, or weaker than the claim requires.
- The pilot experiment cannot distinguish mechanism from implementation noise.
- The plan jumps to full benchmark runs before smoke and sanity checks pass.
- The story changes after seeing results without recording a clear reason.
- A continuation reopens settled decisions or asks for the entire initial
  matrix without a material change.
- Engineering, optimization, prototype, and core-construct failures are
  conflated.
- A diagnostic gate is treated as the complete scientific verdict.
- An acceptance threshold is weakened, or the primary metric/baseline is
  changed, after the outcome is visible.
- Validation expands into hash checks or endless low-impact CPU gates instead
  of reaching a feasible downstream pilot.
- A new experiment family, dataset, seed policy, or paper-only TODO is smuggled
  into an existing authorization or budget.
- Subagents receive vague tasks, overlapping write scopes, or authority to run
  long jobs without main-session acceptance.
