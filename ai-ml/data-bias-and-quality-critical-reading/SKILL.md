---
name: data-bias-and-quality-critical-reading
description: "Reads a given dataset or report critically before it's used as the basis for a decision or to train an AI model: identifies missing groups, bias types (selection, survivorship, historical, measurement, aggregation), and separates vanity metrics from decision-driving ones. Use before accepting any data-based claim, model, or recommendation at face value."
---

# Data Bias & Quality Critical Reading

## Purpose

Prevents the most common and costliest data error: accepting data as
unquestioned truth. Data is always the result of someone's choices,
measurements, and history — it is a **representation of reality, not
reality itself** (see the pack's `../../CLAUDE.md`). When an AI model is
trained on biased data, or a decision is made on the basis of incomplete
reporting, the error doesn't show up in the data itself — it only shows up
in the outcome, often too late. This skill produces a systematic check
before that moment.

## Anchored in research

- The "Understanding data" area of data literacy (see
  `../data-literacy-competency-assessment/SKILL.md`): critical thinking
  about a data source's origin, ownership, and representativeness is a
  foundation of data literacy, not a separate specialty.
- The established bias taxonomy from statistics and machine learning (a
  synthesis of multiple sources): selection bias, survivorship bias,
  historical/label bias, measurement bias, aggregation bias — commonly
  recognized, recurring bias types not tied to any single product or
  company.
- The "vanity metric vs. actionable metric" distinction (lean analytics
  tradition): a metric is useless for decision-making if it wouldn't
  change any decision regardless of which direction it moves.

## Method

1. **Ask the provenance questions first** for every significant dataset:
   where does this data come from, who collected it and why, and who
   owns it today? If you can't answer all three, don't make a decision
   based on the data yet — establish provenance first.
2. **Walk through the five bias types explicitly** for every dataset
   driving a decision:
   - **Selection bias:** which cases/entities made it into the dataset
     and which were systematically left out? (e.g. only customers who
     contacted support, not all customers)
   - **Survivorship bias:** does the data only show the cases that
     "survived" a process (e.g. only approved applications, not rejected
     ones), leaving the reasons for failure invisible?
   - **Historical/label bias:** does the data reflect past inequity or
     one-sided decision-making (e.g. who was previously promoted or
     granted credit) in a way that a model would learn to repeat as a
     new "truth"?
   - **Measurement bias:** is the variable used a good proxy for what was
     actually meant to be measured, or is something being measured just
     because it's easy to measure (e.g. clicks instead of actual customer
     satisfaction)?
   - **Aggregation bias:** does meaningful variation disappear when data
     is combined into averages or totals (e.g. average utilization
     masking the fact that two customer groups behave completely
     differently)?
   For every bias found, note: which type, the likely direction of its
   effect, and whether it's correctable or only something to account for.
3. **Explicitly ask what's missing from the data and whose perspective is
   missing.** Missing data is not neutral — it's usually systematically
   missing for a particular group or situation. Name the missing
   group/situation, don't just note "data is missing."
4. **Separate vanity metrics from decision-driving ones.** Test every
   metric presented with the question: *"If this number moved 20% in
   either direction, would it change any decision?"* If the answer is
   no, the metric is "nice-to-know" and doesn't deserve a place at the
   core of decision-making — it can still be useful context, but
   shouldn't be presented as a key justification.
5. **Assess the data's freshness and representativeness over time.** Was
   the data collected under conditions matching the current situation
   (e.g. not collected during an exceptional period), and is it fresh
   enough for the decision it's being used to justify?
6. **Produce a short "reliability note" for every key data finding**
   before it moves forward: which biases were identified, how severe
   they are for the decision, and whether the finding can be used as-is
   or requires further validation.

## What this skill does NOT do

- Doesn't fix the data technically (e.g. reweighting, imputation) —
  identifies and names the bias; correction is a separate technical
  task.
- Doesn't claim every bias must be removed before data can be used —
  many decisions can be made with a known, documented bias, as long as
  it's visible rather than hidden.
- Doesn't replace a statistical or machine-learning technical audit
  (e.g. a model's fairness metrics) — produces a business-level, critical
  first read before deeper technical analysis.
- Doesn't confirm figures or bias claims from memory — bases the
  assessment on data you provide, or marks an assumption clearly
  (`[assumption — verify]`).

## Refinement notes

Areas to keep deepening with real practice:

- your own examples of biases you've found in client data and what they
  would have caused if they hadn't been noticed
- a concrete checklist template for walking through the five bias types
  (into `../../references/`)
- rules of thumb for which industries/data types each bias type is most
  common in

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Before this (if the role is still unclear): `../data-role-diagnosis/SKILL.md`
- Next in this pack: `../data-storytelling-and-business-translation/SKILL.md`
  — use this skill's reliability notes when translating the finding into
  a story, and don't hide a known bias from the narrative.
- Related skill in another pack: `../../../business-case-and-analysis/skills/assumption-and-evidence-audit/SKILL.md`
  — a broader check of assumptions and evidence at the whole business
  case level.
- Related skill in another pack: `../../../ai-strategy-and-governance/skills/responsible-ai-and-governance-check/SKILL.md`
  — if the bias affects an AI model's training data, also check the
  responsibility/risk angle.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
