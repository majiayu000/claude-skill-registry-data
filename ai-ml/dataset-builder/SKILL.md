---
name: dataset-builder
description: Turn field artefacts into a labelled dataset and 20+ golden cases — the seed of the eval suite that gates the build. Attaches a ground-truth label to every real artefact, scores each label on the evidence ladder, and clears each case through four gates (provenance, ground-truth, unreachable, held-out) so a foundation model cannot pre-pass its own memorised test. Fires on "make our own dataset", "create golden cases", "label this", "turn our field logs into a test set the model hasn't seen", "seed the eval suite". Not for finding which sources are proprietary in the first place (use yoda-data-sourcing, section 03), not for composing the labelled cases into the four-band spread / autonomy level / cost budget of a scoreable spec (use eval-first-spec, section 07), not for splitting an expert's teachable procedure from show-only judgment (use explicit-vs-tacit-capture, section 03).
type: generator
supersedes: none
---

## What it does

Takes the field artefacts a fellow already holds — the moat-seed rows `yoda-data-sourcing` surfaced — and turns them into two things: a labelled dataset (every artefact paired with a ground-truth label and its provenance) and the ≥20 golden cases carved out of it. A case earns "golden" only by clearing four gates: it cites the real artefact it came from, its label is ground truth on the evidence ladder (not a rater's opinion), a foundation model has never seen the input and cannot narrate the label from training, and it is held out from the build so the model cannot be tuned against it. The artefact is the filled `template.md`: the labelling ledger plus the golden seed. That seed is the honest test — the data a model cannot pre-pass — and it is what `eval-first-spec` composes into the scoreable v1 spec. A dataset a model could reproduce is not shipped; it measures nothing.

## The Icarus reframe

A dataset a foundation model can already reproduce cannot tell you whether your product works — the model passes its own memorised test and you learn nothing. So a golden case is golden only when it clears two gates a generic labelling job skips. First, the input is unreachable: a model has never seen it and cannot reconstruct the label from training — the YODA test, aimed this time at the eval set, not the moat. Second, the label is ground truth on the evidence ladder — what actually happened, not what a rater thinks; an opinion label scores 0.1 and is a hypothesis to resolve, not a golden case. The labelled dataset is the moat made measurable: the one test a competitor's model cannot pre-pass.

## When to use / When NOT

Use once a fellow holds real field artefacts (from `yoda-data-sourcing`'s P rows, from probes, from historical records) and needs to turn them into a labelled dataset and the golden cases that will gate the build. Trigger phrases: "make our own dataset", "create golden cases", "label this", "turn our field logs into a test set the model hasn't seen", "seed the eval suite".

Do not use when:

| Request | Belongs to |
|---|---|
| "Which of our candidate sources are actually proprietary / where is our moat data?" | `yoda-data-sourcing` (section 03). It finds and bands the sources; this labels the artefacts those sources produce. Run it first; this second. |
| "I have my 20 labelled cases — now compose them into the typical/edge/adversarial spread, pick the autonomy level, and set the cost-per-outcome budget." | `eval-first-spec` (section 07). This skill hands it the labelled seed; that skill writes the job line, the band composition, the pass/fail contract, autonomy, and cost. Do not poach the spec. |
| "Which of the expert's knowledge is teachable procedure vs show-only judgment?" | `explicit-vs-tacit-capture` (section 03). This skill uses inter-rater disagreement to flag an unsettled label; deciding what is codifiable at all is that skill's job. |
| "Is this one signal strong enough evidence?" | `evidence-ladder` (section 02). This skill borrows the ladder to score a label; scoring a lone signal is that skill's job. |

Do not use it to invent cases. If there are no real artefacts to label, the input is not ready. Say so, send the fellow back to `yoda-data-sourcing` and the probes, and never pad the count with synthetic rows.

## Method

Fill in `template.md`. Six steps, then the kill-line check.

### Step 1 — Pull the source, don't re-source it

Start from the moat-seed rows `yoda-data-sourcing` already produced. Name the field artefacts you will label and which P row each comes from. Do not re-run the sourcing. One hard check: if the only artefacts available are model-reachable (yoda's R rows — public standards, tutorials, a Kaggle set), stop. A model has already memorised that data; a dataset built on it measures nothing. That is the kill line, and the honest output is to route back to the workflow-trapped pile, not to label commodity data.

### Step 2 — Fix the label schema before labelling anything

Decide the one thing each case is labelled with, and — the part fellows skip — what the ground-truth authority is. State it as: **input X → label Y, where Y is true because [what actually happened / an agreed adjudicator resolved it]**. Ban opinion labels here, at the schema, not case by case. "The expert thinks this reading is unsafe" is not a schema; "the reading was unsafe, confirmed by the outcome logged after the call" is.

### Step 3 — Label each artefact and score the label on the ladder

Attach the label to every artefact. Tag the label's source on the evidence ladder (see Evidence standard) and mark it `[Fact]`, `[Assumption]`, or `[Hypothesis]`. Where the label is a judgment call, have two qualified people label it independently. Record whether they agree.

### Step 4 — Run the four gates on every case

A row is golden only if it clears all four. Any failure sends it to `train`, `hold`, or `discard`, not to the golden set.

| Gate | Test | Fails to |
|---|---|---|
| 1 Provenance | Cites the real artefact and the yoda row it came from? | `discard` — no source, not a case |
| 2 Ground truth | Label scores ≥ 0.5 on the ladder (what actually happened / adjudicated), and agreed if it is a judgment? | `hold` — opinion-only or contested label is a hypothesis, resolve it first |
| 3 Unreachable | A model has not seen the input **and** cannot narrate the label from training (Step 5)? | `discard` — reproducible, measures nothing |
| 4 Held out | Quarantined from the build — never few-shot, prompt-tuned, or fine-tuned against? | `train` — once the build sees it, it is training data, not a test |

### Step 5 — The contamination check (the YODA test on the case)

Gate 3 has two parts. Run both; a case must clear both to be unreachable.

| Leak | Question | If it leaks |
|---|---|---|
| Input-leak | Is the input published, indexed, or memorised — a public benchmark, a dataset you released, a common example? | Model has seen it. Discard; pull from the workflow-trapped pile instead. |
| Label-leak | Could a model produce the correct label from world knowledge alone, with no access to your outcome? | The label is common knowledge, not your ground truth. Discard or replace with a case whose answer only your data holds. |

Also refuse model-generated labels: labelling with the model under test (or a near-clone) makes the test agree with the model by construction. Ground truth comes from outside the model — the outcome, or a human authority.

### Step 6 — Count the golden cases and assemble the seed

Fill the ledger in `template.md`, one row per artefact:

| # | Input (artefact + provenance: yoda row) | Label (ground truth) | Label source (ladder + tag) | Leak checks (input / label) | Inter-rater (agreed?) | Split (golden / train / hold / discard) | Golden? |
|---|---|---|---|---|---|---|---|

Then count the `golden` rows. Two floors:

- **≥ 20 golden cases.** Fewer is not a smaller version of done; it is not done. If you have 13, the finding is "go get 7 more real artefacts from the next probe or yoda row," never 7 synthetic ones.
- **Spread, not padding.** The 20 must span the real variety of the input, not 20 near-copies of one artefact. A monotonous dataset is both a leakage smell (one pattern a model generalises instantly) and useless as a test. Note the coverage in plain terms. Do **not** compose it into the formal typical/edge/adversarial/must-refuse band floors or write per-case pass conditions — that is `eval-first-spec`'s job. This skill hands over a clean, varied, ground-truth-labelled seed; that skill turns it into the scoreable contract.

Close with the verdict: the golden count, the rows held or discarded and why, and the handoff line to `eval-first-spec`.

**Kill line.** The output ships only with ≥ 20 golden cases that clear all four gates, AND a dataset no foundation model could reproduce. Fewer than 20, any golden row that is opinion-labelled / contaminated / model-generated, or a dataset a model already reaches — auto-fail. Report the gap; do not dress a reproducible or padded set as a golden set.

## Evidence standard

Every Icarus skill weights behaviour and money over opinion. Here the ladder scores the **label** — whether the answer key is real — not whether the source exists (that was `yoda-data-sourcing`'s job).

| The label is true because… | Score | Golden? |
|---|---|---|
| The outcome moved money — the deal closed at that price, the SLA credit was paid | 1.0 | Yes |
| The behaviour was observed — the machine stopped, the operator overrode, the outage happened | 0.7 | Yes |
| An artefact records it — the issued permit, the filed report, the human-assigned category of record | 0.5 | Yes |
| Someone committed to it verbally — "we'd have flagged that one" | 0.3 | Hold |
| It is one rater's opinion — "looks unsafe to me", no outcome behind it | 0.1 | No |

The floor for a golden label is **≥ 0.5**. A label at 0.1–0.3 is a hypothesis: hold the case out until an outcome or an agreed adjudicator settles it. If two qualified labellers disagree, the label is not settled either — adjudicate it, or the honest answer is that the case is ambiguous (which may itself be a legitimate "not enough signal" case, but only once you have named it so). Tag every label `[Fact]`, `[Assumption]`, or `[Hypothesis]`. A dataset labelled at 0.1 teaches the build to match a rater's vibe, and no eval score computed against it means anything.

## Gotchas

Benchmark contamination mistaken for a golden set. Pulling cases from a public dataset — or one you published — means the model has already memorised the answers. It will score near 100% and you have measured nothing. Golden cases come from the workflow-trapped pile (yoda's P rows), never from a public benchmark, however convenient.

Opinion dressed as a label. "The expert says X" is not ground truth unless X is what actually happened or was resolved by an agreed authority. A dataset labelled by one rater's judgment trains the build to reproduce that judgment, not to be right. When labellers disagree, the label is not settled — adjudicate it or mark the case ambiguous; do not average two guesses into a fake answer.

The golden set burned by leakage into the build. The moment you few-shot, prompt-tune, or fine-tune against a golden case, it stops measuring generalisation — the model has seen the answer. A golden case is single-use as a held-out test. Once the build sees it, retire it to the training pile and replace it, or every future score is inflated.

Padding to 20 with synthetic cases. If you have 12 real labelled cases, the honest output is "go get 8 more from the next artefact batch," not 8 model-generated ones. A case invented and labelled by the model you are testing is a mirror, not a test: it will pass by construction and hide the failure you built the set to catch. Fewer than 20 real cases is the finding, not a rounding error.

Volume mistaken for a dataset. Ten thousand rows a model labelled in an afternoon is not a golden set; twenty real artefacts with ground-truth labels a model cannot reproduce is. The value is in the unreachable label, not the row count. A bigger synthetic pile is a bigger mirror.

## Examples

`examples/sample.md` — a full labelled dataset and golden seed for Mentix's operator-correction data: each artefact is one copilot suggestion plus the operator's accept/edit/override and what the line did afterwards, labelled with the correct first action and ground-truthed on the outcome. It scores every label on the ladder, discards a case pulled from a public predictive-maintenance tutorial (input-leak), holds a case whose only label is an engineer's opinion, retires a case the team had already few-shotted against, lands at 22 golden cases, and hands the seed to `eval-first-spec` without composing the bands.

## Related skills

`yoda-data-sourcing` (section 03) — finds and bands the proprietary sources; this labels the artefacts those P rows produce. Its moat seed is this skill's raw material. Run it first.

`eval-first-spec` (section 07) — consumes this skill's golden seed. It writes the one-sentence job line, composes the cases into the typical/edge/adversarial/must-refuse spread, sets the L0–L4 autonomy level and cost-per-outcome budget. This skill produces the labelled data; that skill turns it into the scoreable spec. Keep the boundary: labelling and hygiene here, composition and scoring there.

`explicit-vs-tacit-capture` (section 03, sibling) — decides which expertise is teachable procedure vs show-only judgment. This skill's inter-rater test flags when a label rests on unsettled tacit judgment; resolving what is codifiable at all is that skill's job.

`evidence-ladder` (section 02) — owns the rungs this skill borrows to score whether a label is ground truth. Send a fellow there to weigh one lone signal.

Supersedes: none. New skill; no prior dataset-labelling skill exists in the pack to absorb or beat.
