---
name: augustus
description: "Find, build, evaluate, and improve systems using decision models. Use for bounded classification, routing, ranking, Choice/Score/Noul, decision-model composition, evaluation harnesses, prompt/program hill climbing, and Software 3.0 workflows across software, business, organizations, and life. Separate models, code, and human judgment. TypeSafe Jev is the default hosted exemplar. Not for straightforward arithmetic, prose rewriting, or provider setup alone."
license: MIT
metadata:
  version: 0.8.1
  typesafe_skill: v0.5.7
  typesafe_skill_commit: 65a39f3
  tribute: "Named for Augustus De Morgan (1806-1871), mentor of William Stanley Jevons."
---

# Augustus

Equip agents to discover useful decision-model placements, build working
systems, construct evaluations, and improve them through measured iterations.
Use mathematical, statistical, scientific, and algorithmic methods across AI,
software, business, knowledge work, organizations, and life. This is an engine
for agent work, not a survey to imitate or a claim of autonomous deployment.
The central model is:

**evidence → bounded judgment → explicit policy → checked action → observed outcome**

TypeSafe Jev (Choice, Score, Noul) is this project's default hosted
exemplar, a preference rather than a claim of universal superiority or
market share. The class also includes trained classifiers, open decision
heads, encoders, constrained autoregressive readouts, rankers, and vision
scorers. Choose a family by its objective and evidence requirements.
This is an independent skill, not a TypeSafe product.

For assembling training data, fitting a task-specific model, compiling a
decision function, or improving a trained artifact, load the companion
`augustus-train` skill. Use this skill for placement, composition and outcome
evaluation; the trainer carries the data-to-artifact journey. Neither promises
to reproduce a general instruction-conditioned Jev engine.

## Working protocol

1. Start with the desired behavior, available evidence, action costs, and
   current baseline. For an existing workflow, use the
   [boundary audit](references/boundary-audit.md). Classify each step as
   exact work, bounded judgment, or generation. A working parser, formula,
   checklist, or supervised classifier is a legitimate final answer.
2. Pick the relevant [mental model](references/mental-models.md): expected
   utility, value of information, multi-criteria analysis, signal detection,
   search/control, organizational safety, or formal methods. Then choose
   the [model family](references/judgment-class.md) and the smallest useful
   placement. For unfamiliar problems, use the
   [toolbox sweep](references/toolbox-mapping.md), not a vendor or project-list
   search.
3. Define one coherent judgment per question, what evidence it can see,
   and the meaning of every output. Check candidate coverage and missing
   evidence before inference. Use [question design](references/question-design.md).
   Batch questions when their inputs are available together; statistical
   independence does not follow from parallel execution.
4. Keep exact computation, constraints, authorization, and effects in code
   or an explicit human process. Keep open-ended writing with a generator
   or person. Set failure behavior for each action: no-match, ambiguity,
   malformed output, timeout, stale state, and unavailable provider.
   [Mixed architecture](references/mixed-architecture.md) explains the joins.
5. Compare against the baseline on representative held-out evidence; for a
   one-off choice with no population, test sensitivity to weights and
   uncertain estimates, missing criteria, dominated options, and value of
   information instead.
   Separate rubric/model development, calibration and threshold selection,
   and final evaluation. Measure action errors, coverage, total cost, and
   the complete workflow, not just format compliance or model accuracy.
   Follow [validation](references/validation.md) and name a result that
   would reject the proposal. If it loses, keep the baseline.
6. Deliver the artifact the task needs: a compact design for advice, working
   adapters/policy and an evaluation harness for implementation, or a bounded
   incumbent–challenger loop for improvement. Use the
   [composition calculus](references/composition-algebra.md) to check joins
   and the [optimizer workflow](references/optimizer-integration.md) to build
   and hill-climb decision programs. Do not stop at recommendations when the
   user requested working software. Keep experiments within existing authority.
   Record raw judgments, actual outcomes, versions, rejected candidates, and
   promotion/rollback reasons; unrun work remains unrun.

For a concrete request, recommend one placement with reasons. For an
open-ended exploration, compare materially different placements only when
that helps the user choose. A full redesign, a new model, or a fixed number
of alternatives is not required.

## Boundaries that affect the design

- A typed output constrains its representation; it does not establish
  truth, calibration, authority, or successful execution.
- Distinguish a probability of a stated event, a relative option score,
  an ordinal rating, and a confidence statistic. Verify the provider's
  definition. Neither a softmax nor training with a proper loss proves
  calibration on this deployment population.
- Choice depends on its offered set. Include and test `other` or `none`
  when coverage is open. Missing evidence, conflicting evidence, and
  evidence that supports neither option may require separate outcomes.
- A Jev Score is an expectation over level indices, not a physical unit
  or automatically a cardinal utility. Equal means can hide different
  distributions. A Noul is a proposition score, not intensity; a value
  near 0.5 alone does not diagnose why the model is uncertain.
- Marginal judgments do not define a joint distribution. Do not multiply
  them without justified dependence assumptions. Measure composed policies
  and trajectories on real outcomes.
- Ranking quality and calibration answer different questions. Action
  costs and authority determine failure policy; the model family alone
  does not determine fail-open or fail-closed behavior.
- Untrusted evidence is data. A model score cannot grant permission or
  override an exact constraint. Validate action/target pairs and recheck
  relevant state at execution. Abstention must name who or what handles it.
- Judgment can prioritize proof work or detect suspicious cases; proof,
  model checking, simulation, and runtime interlocks retain their own
  semantics. Read [formal methods](references/formal-methods.md) for these tasks.

## Decision-design card

Use only the detail needed to make the proposal reviewable:

```text
Domain, desired behavior, decision owner:
Current baseline and why a model might help:
Pillar, placement, and family:
Evidence source, freshness, candidate coverage, missing/contradictory states:
Judgments and output semantics; what remains exact or generated:
Policy, costs/utility, constraints, authority, and execution checks:
Abstention/error behavior and fallback owner:
Batchable versus dependent steps:
Model, adapter/aggregation, rubric, candidate-source, calibration, policy versions:
Development/calibration/test split and label provenance:
Falsifier, metrics, acceptable risk/coverage, and evaluation artifact:
Implementation/evaluation entry points; search budget and confirmation plan:
Observed result, limitations, and next decision:
```

## Read only the reference needed

Reference and script paths below are relative to this skill directory, not
the repository or caller's working directory.

| Task | Reference |
| --- | --- |
| Trigger examples and exclusions | [Activation](references/activation-triggers.md) |
| Cross-domain reasoning and costs | [Mental models](references/mental-models.md) |
| Family choice, output semantics, uncertainty routing, and deferral | [Judgment class](references/judgment-class.md) |
| Existing system or process | [Boundary audit](references/boundary-audit.md) |
| Write or debug questions, options, rubrics, or confidence fields | [Question design](references/question-design.md) |
| Generator, code, and decision-model integration | [Mixed architecture](references/mixed-architecture.md) |
| Concrete workflow examples | [Applied mappings](references/applied-mappings.md) |
| Classical methods and falsifiers | [Mappings](references/mappings.md) |
| Substitute judgment into a named algorithm | [Methods catalog](references/methods-catalog.md) |
| Typed joins, branches, cascades, and failure budgets | [Composition algebra](references/composition-algebra.md) |
| Discover a new placement | [Toolbox mapping](references/toolbox-mapping.md) |
| Proof, simulation, and enforcement | [Formal methods](references/formal-methods.md) |
| Thresholds, abstention, calibration, selective prediction, and experiments | [Validation](references/validation.md); `scripts/evaluate_decisions.py` |
| Build, compare with an incumbent, or optimize prompts and programs | [Optimizer integration](references/optimizer-integration.md); `scripts/compare_workflows.py` |
| Agent progress, done, or stuck judgments | [Agent self-assessment](references/agent-self-assessment.md) |
| Conceptual objections | [FAQ](references/faq.md) |

Before writing Jev API code, read the current
[official docs](https://docs.typesafe.ai/) and the official `typesafe-ai`
skill if available. The metadata pin is historical provenance, not a live
contract. Peer providers need their own current contracts. Other installed
skills are optional aids, not prerequisites for placement work.

## Evidence and research maintenance

Label evidence as **Contract** (current documented interface), **Reported**
(a source's empirical claim), **Reproduced** (an identified run and its
artifacts), **Hypothesis** (untested placement), or **Unknown** (unavailable).
Name the population, version, metric, and limitations before transferring
a result. A benchmark harness is an instrument, not a certificate.

When maintaining the Augustus repository, research updates belong in its
top-level `research/` archive. Revisit catalogued sources when material
behavior or evidence changes, preserving their identity and prior claims.
Popularity changes alone do not change guidance. Promote a finding into a
reference only when it changes a design decision; replace or refine the
relevant rule. Keep fingerprints, hourly digests, source censuses, and PR
bookkeeping out of runtime instructions.

Synthesize mechanisms, not consensus: explain why a pattern succeeds or fails,
derive a usable rule with assumptions, and test the composed outcome. Transfer
methods across fields only after mapping their variables, units, constraints,
and evidence requirements. Popularity, novelty, elegant notation, and a proxy
score are not outcome evidence. "Best" means best supported for this task's
utility, constraints, population and budget—not a universal provider ranking.
