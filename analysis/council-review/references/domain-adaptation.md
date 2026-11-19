# Domain Adaptation - mapping the gate ladder onto other empirical domains

The gate ladder (Gates 0-11, F, T) is domain-general: it encodes what it takes for
a quantitative empirical claim to be real, in any field. The skill's worked
examples are drawn from in-silico neuro/AI because that is where the panel was
built and battle-tested, but the ladder itself does not assume neural nets or
fMRI. The reporting standards below are the domain-specific instantiations of the
same rigor - each one is a field's own checklist for the same underlying
questions the gates ask. When reviewing a clinical, biomedical, psychology, or
field study, apply the standard that matches the study design, and use it to fill
in gate evidence rather than reasoning from neuro/AI intuitions alone.

## Mapping table

| Standard | Study design it covers | Maps to gates |
|---|---|---|
| CONSORT | Randomized controlled trials | Gate 0 (allocation concealment, randomization integrity), Gate 1 (blinding, power), Gate 9 (participant flow diagram, attrition), Gate 11 (pre-specified primary endpoint) |
| STROBE | Observational studies: cohort, case-control, cross-sectional | Gate 4 (confounding, adjustment set), Gate 7 (selection bias, representativeness of the sample), Gate 8 (exposure/outcome measurement, missing data) |
| PRISMA | Systematic reviews and meta-analyses | Gate 0 (search reproducibility, database + date range + search string), Gate 2 (heterogeneity across included studies), Gate 11 (protocol registration, e.g. PROSPERO) |
| ARRIVE | Animal research | Gate 0 (sample-size justification, randomization to group), Gate 9 (housing/husbandry, blinding of assessors), Gate 10 (welfare and ethical approval) |
| Clinical-trial hooks | Any interventional human trial | Trial registration (ClinicalTrials.gov / ISRCTN) checked at Gate 11; intention-to-treat vs per-protocol analysis checked at Gate 0/7; pre-specified primary vs secondary endpoints checked at Gate 11; adverse-event reporting checked at Gate 10 |

Treat the right-hand column as "which gate this checklist item feeds," not as a
strict one-to-one substitute. A CONSORT flow diagram is Gate-9 evidence for
reproducibility of who-went-where, but a diagram showing large unexplained
attrition is also a Gate-0/Gate-7 problem (is the analyzed sample still the
randomized sample?).

## Domain-specific FAIL tells

- **Outcome switching** - the registered primary endpoint (ClinicalTrials.gov,
  PROSPERO, or a pre-analysis plan) does not match the endpoint reported as
  primary in the write-up. This is a Gate 11 failure: relabel the result as
  exploratory, not confirmatory.
- **Per-protocol analysis hiding dropout** - a trial reports only the per-protocol
  population without an intention-to-treat comparison, and dropout is
  differential across arms. This is a Gate 0/Gate 7 failure: the "sample" being
  analyzed is no longer the randomized sample, and attrition may be informative.
- **Meta-analysis with no I^2 / heterogeneity reporting** - pooled effect
  reported without a heterogeneity statistic or forest-plot inspection. This is a
  Gate 2 failure: specification robustness across the included studies is
  unaddressed, and a high-heterogeneity pool masquerading as one number is a
  knife-edge result.
- **Observational association narrated as causal** - "X reduces Y" language on a
  STROBE cohort/case-control design with no adjustment for known confounders
  (or adjustment for a confounder set that omits an obvious one, e.g. baseline
  severity). This is a Gate 4 / Gate 6 failure: the claim's causal language has
  outrun what an unadjusted or under-adjusted association can support.

## When the standard isn't listed

For a field with a reporting standard not covered above (STARD for diagnostic
accuracy, SPIRIT for trial protocols, TRIPOD for prediction models, SQUIRE for
quality-improvement studies, and so on), ask what reporting checklist the target
venue or field expects and map its items onto the nearest gates using the same
logic as the table above: allocation/randomization and sample provenance feed
Gate 0, blinding and power feed Gate 1, robustness-across-choices items feed Gate
2, confound/adjustment items feed Gate 4, endpoint pre-specification feeds Gate
11, and so on. The gate ladder is the invariant; the checklist is the local
dialect for satisfying it.
