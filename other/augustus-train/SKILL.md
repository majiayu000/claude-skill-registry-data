---
name: augustus-train
description: "Builds and improves task-specific decision artifacts from application requirements and labeled records. Use for data assembly, primitive and base-model selection, fitting, export/reload, inference policy, or bounded data/model/program improvement. Includes rules and no-training outcomes; does not require a rung ladder or training a general Jev."
license: MIT
metadata:
  version: 0.8.1
---

# Augustus Train

Deliver a runnable task specialist and its evidence, or retain a better incumbent.
The artifact may be a rule, classifier, ranker, regressor, adapted encoder,
prompted decision, or compiled program. Fit only what the application needs.
Load the companion `augustus` skill for placement and composition;
this skill carries the chosen component from messy records into inference.

## Start from the application, not a training recipe

Write a short executable contract in the application's own files:

- **Decision:** input available at decision time, unit of work, target and label
  vocabulary, output meaning, and downstream action. Separate exact computation,
  bounded judgment, and freeform generation. A multi-step application can contain
  several bounded components; test the complete path as well as each component.
- **Policy:** action costs or useful outcome metric, hard constraints, ambiguity,
  missing evidence, invalid output, timeout, abstention/fallback, and authority.
  Define tie rules and unknown/no-match separately from a real class.
- **Acceptance:** incumbent, minimum useful change or non-inferiority margin,
  critical slices, deployment latency/memory, available labels and compute,
  maximum trials/spend, and an outcome that would reject this candidate.

An exact rule may finish the task immediately. Small data may justify a bounded
prototype without a generalization guarantee. Missing labels do not justify
fabricating gold. Do not require every task to train, call a zero-shot model,
calibrate, or visit every artifact family before making progress.
For exact rules, verify the authoritative mapping and failure paths directly.
Incidental labeled notes are not automatically a representative holdout; do not
attach population-error bounds without the requisite sampling assumptions.

## Choose a primitive and a small candidate set

| Required behavior | Candidate primitive and base stock | Fit or adapt when useful |
| --- | --- | --- |
| Exact eligibility, arithmetic, fixed vocabulary mapping | Ordinary code, parser, lookup | No model; test boundary and failure cases |
| Stable categorical field in text or records | Sparse features, frozen domain encoder, tabular classifier | Regularized head; SetFit/encoder adaptation if representation is the bottleneck |
| Choice from a changing candidate set | Instruction-conditioned decision model or pair/cross-encoder | Few-shot criteria, readout/head adaptation; test candidate coverage and option order |
| Ordered rating or quantity | Ordinal classifier or regressor with defined target/units | Ordinal loss or regression; do not reinterpret a normalized score as a physical quantity |
| Select or order items for a query | Retriever plus pointwise/pairwise/listwise ranker | Query-grouped relevance labels; evaluate retrieval recall and ranking separately |
| Visual/audio evidence | Modality-appropriate encoder and head | Freeze then adapt only if task evidence supports it; text proxies may omit the signal |
| Stable semantic rule with local high-volume serving | Small instruction model, adapter or compiled program | SFT/distillation with permitted targets; validate emitted vocabulary and runtime |

Use compatible stock already available: pin identity/revision, tokenizer or
preprocessor, feature layer/pooling, modality, language/domain, context limits,
license and training lineage. Check that deployment can run the artifact before
fitting. A larger base may help, but adds memory, latency and provenance costs.
Choose only candidates justified by the task and budget, not by a label-count ladder.

**A task specialist is not a general instruction-conditioned Jev.** A fixed-label
classifier can expose a Choice-shaped response without understanding arbitrary
new criteria/options. Generalization across tasks requires a task-diverse training
mixture and held-out tasks, not merely new rows of one taxonomy. Choice, Score and
Noul describe interfaces; they do not supply a training objective or guarantee
calibration. Record whether each value is an event probability estimate, logit,
relative score, ordinal level or quantity. Shape alone supplies none of those meanings.

For a binary predicate, define the positive event and missing-evidence behavior.
For categorical Choice, bind scores to option identities, including open-set cases.
For an ordered Score, define level meanings and preserve the distribution when
needed; an expected level index is not automatically cardinal utility or a unit.

## Build and exercise the whole path

1. **Assemble data.** Follow [data and splits](references/data-and-splits.md):
   audit raw records, define/adjudicate labels, resolve groups and timestamps,
   preserve unknowns and lineage, then freeze representative data roles.
2. **Make the evaluator executable first.** Test labels, polarity, aliases,
   abstention and loss on hand-calculated cases; use
   [spec defects](references/spec-defects.md) when model and spec disagree.
   Keep the incumbent runnable. A cost-optimal constant, existing rules or current
   workflow is often the useful comparator; a compatible zero/few-shot model is
   optional. Majority class is not always the cheapest constant under unequal costs.
3. **Fit a bounded candidate.** Use [fit and serve](references/fit-and-serve.md)
   for a CPU example and family-specific adaptation steps. Fit transformations
   only on training data, tune on development data, record every tried version,
   and smoke-test the inference seam before a long fit.
4. **Select policy where needed.** Inspect discrimination and task loss, critical
   class recall, errors, fallback and total serving cost. Calibrate only if the
   consumer needs probability meaning or a calibration defect warrants it.
   Choose thresholds on development/policy data, then freeze them. Predicted class
   proportions alone establish neither miscalibration nor threshold causality.
5. **Export, reload and replay.** Save the entire preprocessor/model/label/policy
   bundle and environment. Reload in a fresh process without fit data. Test normal,
   ambiguous, empty, long, invalid and shifted inputs plus action-boundary cases.
   Compare outputs and end-to-end actions under prespecified tolerances, not a
   universal demand for bitwise identity. Measure the actual deployment path.
6. **Improve and confirm.** Follow [bounded improvement](references/improve-and-confirm.md).
   Use development errors to choose the next data, model or program change.
   Search data may be reused descriptively; independent confirmation stays outside
   candidate selection. Stop on acceptance, budget, no useful progress or missing
   authority. An unsupported improvement leaves the incumbent active.

## Match measurements to the claim

Report task loss and the applicable failure modes rather than filling every row
of a universal checklist. Probability consumers need reliability evidence;
option readers need permutation tests mapped back to option identities; rankers
need query-level evaluation; classifiers need per-class and rare-case errors.
All serving paths need resource/failure measurements relevant to their contract.

Use [compute envelope](references/compute-envelope.md) before any expensive run.
No new rental, paid model call, upload or production activation follows merely
from loading this skill. Reuse authorized local resources and existing tooling.
Measure bottlenecks before buying capacity; uncertain projections are not promises.

The companion scripts perform narrow checks, not training or autonomous search.
Use only those needed: binary probability evaluation, paired outcome comparison,
declared provenance, overlap audit, or ledger replay. Their exact inputs and limits
are wired in the references above; do not copy research benchmark drivers into the app.
For the commands, set `AUGUSTUS` to the absolute companion directory reported by
the skill loader (in this checkout, `.agents/skills/augustus`), not this skill's path.

## Finish with a usable result

Deliver the fit and inference commands, versioned artifact and policy, data/split
and source identities, evaluator and representative receipts, rejected trials,
resource cost, and acceptance decision. State whether evidence is fixture,
proxy, adjudicated or observed, and distinguish exploratory from confirmed results.
Keep known-overlap benchmark rows as labeled diagnostics when useful, not clean
generalization evidence. Package-only is not deployed. For authorized promotion,
exercise the application journey, observe independent outcomes and preserve rollback;
otherwise return the runnable candidate with the incumbent retained.
