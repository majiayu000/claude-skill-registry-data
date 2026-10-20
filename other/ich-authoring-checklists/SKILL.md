---
name: ich-authoring-checklists
description: Authoring checklists for ICH M4 CTD summaries (M4Q, M4S, M4E), ICH E6(R3) Good Clinical Practice content and ICH E9(R1) estimands and sensitivity analyses. Use when drafting or reviewing Module 2 overviews and summaries, protocol or CSR sections, or statistical sections, and to verify guideline currency and internal consistency through the Concept2Cure connector.
---

# ICH authoring checklists (M4 / E6(R3) / E9(R1))

You draft; the platform verifies. Before citing a guideline revision or
asserting a fact is current, ask the connector. Before claiming two documents
agree, sweep them.

## Start every drafting task the same way

1. `c2c_lookup_ich_guideline` for each guideline you will cite (e.g. `M4E(R2)`,
   `E6(R3)`, `E9(R1)`) and quote the corpus's title, status and scope.
2. `c2c_check_regulatory_currency` with the topic and jurisdiction (and
   `drafted_on` when revising an older document) — report facts that are
   superseded, mandatory-upcoming or stale.
3. Extract the quantitative claims you will rely on (endpoint results, doses,
   sample sizes, dates) with their source locations and run
   `c2c_sweep_contradictions` before you write. A contradiction blocks the
   draft until resolved by the author.

## M4E — Module 2.5 Clinical Overview checklist

- [ ] 2.5.1 Product development rationale: indication, pharmacological class, regulatory history, scientific advice
- [ ] 2.5.2 Overview of biopharmaceutics: formulation bridging, BA/BE, food effect
- [ ] 2.5.3 Overview of clinical pharmacology: PK, PD, dose–response, special populations, DDI
- [ ] 2.5.4 Overview of efficacy: study design, populations, endpoints, results, subgroups, persistence, limitations
- [ ] 2.5.5 Overview of safety: exposure, AEs by system, SAEs, deaths, labs, special groups, DDIs, withdrawal
- [ ] 2.5.6 Benefits and risks conclusions: therapeutic context, benefits, risks, benefit–risk assessment
- [ ] 2.5.7 Literature references
- [ ] Every number traces to 2.7 or a Module 5 report; run `c2c_sweep_contradictions` across 2.5/2.7/CSR values

## M4Q — Module 2.3 Quality Overall Summary checklist

- [ ] 2.3.S: general information, manufacture, characterisation, control (specification justified against ICH Q6A/Q6B), reference standards, container closure, stability (ICH Q1A(R2))
- [ ] 2.3.P: description/composition, pharmaceutical development (Q8), manufacture, excipients, control, reference standards, container closure, stability
- [ ] Specification acceptance criteria consistent between 2.3 and 3.2; sweep them

## E6(R3) — GCP content checklist (protocol / CSR / oversight)

- [ ] Quality by design: critical-to-quality factors identified and risk-proportionate controls described
- [ ] Informed consent process, data protection and participant safety reporting described
- [ ] Investigator, sponsor and IRB/IEC responsibilities and delegation documented
- [ ] Data governance: source, traceability (ALCOA+), computerised systems validation, audit trail
- [ ] Monitoring strategy (risk-based) and its justification
- [ ] Essential records identified and retention stated

## E9(R1) — estimand framework checklist (SAP / protocol / CSR)

- [ ] Each primary and key secondary objective has an estimand with all five attributes: treatment, population, variable, intercurrent events with the strategy per event (treatment policy, hypothetical, composite, while-on-treatment, principal stratum), population-level summary
- [ ] Main estimator aligned to the estimand; missing-data assumptions stated
- [ ] Sensitivity analyses target the SAME estimand under different assumptions; supplementary analyses are labelled as such
- [ ] Multiplicity and hierarchy consistent between protocol, SAP and CSR — sweep the alpha allocation and hierarchy statements

## Rules

* Do not state a revision number, effective date or status from memory; the
  connector's corpus is the citation.
* Do not compute sample sizes, power or p-values yourself; the platform's
  deterministic solvers are the source of statistical figures.
* When the corpus has no entry, say so and cite ich.org for the user to
  confirm; do not fill the gap.
