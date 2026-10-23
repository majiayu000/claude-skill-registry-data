---
name: sampled-evaluation
description: "Use when a batch of generated items (pages, records, translations, test cases, messages) is too large for every item to get the two independent evaluators of gate section 11: stratify, sample, evaluate the sample, fix the cause, resample fresh items, and say only what the sample supports."
---

# sampled-evaluation

Support block for step 7 of the pipeline (`WORKFLOW.md`), next to `skills/gate`. Section 11 of `gate` describes
two independent evaluators for **one** deliverable that ships without a human reading it. This block is what
changes when there are hundreds of such deliverables: full dual evaluation of each costs more than producing
them, and spot-checking a few at random misses the systematic fault that a template or a data source puts into
a whole stratum.

## When
A generator (a person, a script or a model) has produced many items from a few templates or sources, the items
ship without individual human reading, and the cost of a bad one is real (public content, customer-facing
messages, data loaded into a live system). Not for a handful of items (evaluate each) and not for anything a
deterministic check can decide on the whole batch (run that check on all of it, always).

## Steps
1. **Run every deterministic check on the whole batch first.** Schema validity, required fields, length
   bounds, forbidden terms, link and reference resolution, duplicate detection: all cheap, all complete, none
   sampled. Sampling is only for what needs a reader.
2. **Write the rubric once**, in the form `skills/gate` §11 requires: every criterion decidable, answered by
   evidence in the item. The same rubric serves every item and every round.
3. **Stratify the batch by what could make items fail together**: the template, the data source, the
   language, the generator version, the item size, the riskiest content class. A stratum is a set of items
   likely to share a fault.
4. **Sample every stratum, not the batch.** Draw a few items from each stratum, more from the riskier ones and
   from the one the generator is newest at; a flat percentage of the whole batch can miss a small stratum
   entirely. The draw is random within a stratum and the seed is recorded.
5. **Plant a known-bad item in the sample.** A deliberately flawed item, with a flaw the rubric names, is
   added without telling the evaluators. If both miss it, the evaluation is rubber-stamping and its passes are
   worthless (the positive control of `skills/testing-anti-patterns` §5.1, applied to evaluators). If one
   misses it, that seat is replaced or its brief tightened before the round counts.
6. **Evaluate the sample as `gate` §11 prescribes**: two evaluators, no shared context, same rubric, both must
   pass, each item judged by criterion.
7. **Classify each failure by cause, not by item.** Group the flags: the same template wording in six items is
   one cause; a source field missing in a stratum is one cause. A cause is fixed **where it arises** (the
   template, the mapping, the generator's instructions), and a mechanical check for that cause is added to
   step 1 and run over the whole batch, so the fix is verified on all items and not only on those sampled.
8. **Regenerate or repair the affected items, then draw a fresh sample.** The items that were already judged
   are not reused for the next round: they have been looked at and fixed, and a clean verdict on them says
   nothing about the rest. Fresh evaluators, as in `gate` §11.
9. **Stop on a clean round or on the cap.** Done is one round in which every stratum's sample passes both
   evaluators and the planted item was caught. Three rounds is the usual cap; at the cap the batch is held and
   handed to a person with the verdicts, the causes found and the strata still failing.
10. **Report what the sample supports.** "n of N items evaluated across k strata, both evaluators passed, the
    planted item was caught, these causes were found and fixed" is a claim. "The batch is verified" is not. The
    report lists the strata and sample sizes, so a reader can see what was not looked at.

## Output / checkpoint
A sampling report: strata and their sizes, sample sizes and seed, rubric, the planted item and whether each
evaluator caught it, the causes found and where each was fixed, the mechanical checks added, the rounds taken.
It feeds the `verified` checkpoint of `skills/gate` for the batch, with the sampled nature stated.

## Guardrails
- **Not a substitute for a deterministic check.** What can be decided mechanically is decided over all items.
- **Agreement is not evidence of quality.** Both evaluators passing everything, every round, is the symptom of
  a rubric or a brief that cannot fail; the planted item is how that is noticed.
- **A subjective rubric produces drift.** Evaluators flagging taste instead of failures send the loop round
  and round; criteria that cannot be answered from the item are removed from the rubric.
- **Cost is bounded in advance.** The number of items per stratum, the rounds and the evaluator budget are set
  before the first round, and the operator chooses this method knowing it multiplies the cost of evaluating
  the sample by two or more.
- **Track the escape rate.** Defects found after shipping in a stratum that passed are recorded against the
  strata and the sample sizes, and a stratum that escaped once is sampled more the next time.

## Origin
Idea taken from the batch-sampling pattern and the failure-mode table of the `santa-method` skill in the public
ECC repository (MIT licence, read 2026-10-02): sample a fraction of a large batch, group failures by type,
fix systematically, resample. The two-evaluator procedure itself is `skills/gate` §11 and is not restated. What
is ours: sampling every stratum with a recorded seed instead of a flat fraction of the batch, the planted
known-bad item as a positive control on the evaluators, the whole-batch deterministic pass before any
sampling, the rule never to reuse judged items, and the requirement that the report state what the sample
supports. No text was copied; the upstream's stack of cost figures and its target percentages are not taken.
