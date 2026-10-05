---
name: sap-critic
description: "Review statistical analysis plans for methodology, power analysis, and multiple comparison handling."
tier: analyst
icon: 📊
version: 0.1.1
---


## JTBD (Jobs To Be Done)

### Primary Job
When I have a statistical analysis plan that will lock before database unblinding — and I know that vague language in the SAP ("appropriate methods will be selected") is the mechanism through which p-hacking happens — I want a rigorous pre-lock review that finds every decision point left open to post-hoc choice, so the SAP can't be used to justify analysis decisions that were actually driven by seeing the data.

### Secondary Jobs
- When a regulatory submission (FDA, EMA) requires a SAP that satisfies ICH E9/E9(R1) and I need to know whether the estimand framework, multiplicity control, and missing data strategy will survive regulatory scrutiny, I want a compliance gap assessment before submission, so I'm not revising the SAP under a response deadline.
- When a trial's primary outcome was pre-specified but the analysis team is now proposing sensitivity analyses that weren't in the original SAP, I want a pre-specification rigor audit that distinguishes confirmatory from exploratory and flags any boundaries that look retroactively defined.

### Job Layers
- Functional: Audit all 12 ICH E9 structural elements, the estimand framework against ICH E9(R1), pre-specification timing evidence, missing data mechanism assumptions and method specification, multiplicity strategy coherence, interim analysis boundary completeness, and reproducibility documentation — returning CRITICAL/MAJOR/MINOR findings with SAP-quoted evidence and a REJECT/REVISE/ACCEPT-WITH-RESERVATIONS/ACCEPT verdict.
- Emotional: Reduce the risk of a regulatory rejection or a post-publication integrity challenge because an ambiguous SAP allowed analysis choices that look data-driven in retrospect — the fear that "we always planned to do it this way" won't hold up when the decision trail isn't documented.
- Social: Gives the user a defensible audit trail showing the SAP was reviewed for pre-specification rigor before database lock, which protects the trial team against allegations of selective reporting.

### This Skill Is For
- A biostatistician or clinical researcher with a drafted SAP that needs to be reviewed before database lock or regulatory submission.
- A trial team preparing for an FDA or EMA submission where ICH E9(R1) estimand framework compliance will be scrutinized.
- A researcher or reviewer who needs to distinguish legitimate pre-specified analyses from post-hoc decisions that were retroactively added to the SAP.

### This Skill Is NOT For
- A user designing a new trial from scratch who doesn't yet have a SAP; use `study-design-planner` instead.
- A user who needs a review of the overall study methodology — design-question fit, sampling, confounding control — rather than the statistical analysis plan specifically; use `research-critic` instead.

### Paired With
- `study-design-planner`: If the verdict is REVISE or REJECT due to fundamental design gaps underlying the SAP, use it to address the upstream study design before revising the SAP.
- `research-critic`: Use this when the unresolved problem is whole-study methodology — design choice, sampling adequacy, or interpretive overreach — rather than SAP pre-specification detail.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has a SAP needing pre-lock review | The skill audits all 12 ICH E9 elements, estimand framework, and pre-specification rigor | A REJECT/REVISE/ACCEPT verdict with every open decision point identified |
| Preparing for regulatory submission | The skill assesses ICH E9(R1) compliance gaps and flags elements regulators will challenge | A compliance gap list with specific revision requirements |
| Needs to distinguish confirmatory from exploratory | The skill audits whether analysis boundaries are truly pre-specified or retroactively defined | A pre-specification timeline assessment with evidence |

### When to Escalate
- If the user doesn't yet have a SAP and needs to design the study, escalate to `study-design-planner`.
- If the primary concern is the overall study methodology rather than the statistical analysis plan specifically, escalate to `research-critic`.

## Purpose

Standard SAP review focuses on basic completeness and statistical methods. **sap-critic** goes deeper: it systematically audits pre-specification rigor, estimand framework alignment (ICH E9 R1), missing data strategy appropriateness, multiplicity control, and reproducibility using rigorous biostatistical standards.

### What Standard SAP Review Often Misses:

- **Vague analysis specifications** that allow post-hoc flexibility (e.g., "appropriate statistical method will be selected," "missing data will be handled appropriately")
- **Missing mechanism assumptions** for missing data (MCAR/MAR/MNAR not stated, enabling analytic choice post-hoc based on results)
- **Incomplete missing data strategies** (multiple imputation mentioned but number of imputations, imputation algorithm, or sensitivity to MAR assumption not specified)
- **Uncontrolled multiplicity** (multiple endpoints analyzed without alpha adjustment, inflated Type I error)
- **Subgroups not pre-specified** but presented as confirmatory (enables selection of subgroups that show benefit)
- **Estimand-analysis mismatch** (no clear mapping between estimand intercurrent event handling strategy and analysis method)
- **Pre-specification timing not documented** (SAP dated before database lock but actually written after unblinding; enables "retroactive" pre-specification)
- **Interim analysis boundaries under-specified** (alpha-spending function not named, futility boundary not defined, allowing data-dependent decisions)
- **Non-inferiority margins unjustified** (margin stated without clinical/regulatory basis)
- **Safety analysis detail sparse** (safety endpoints listed but stopping rules, categorization, or analysis methods not pre-specified)

### What This Adds:

- **Structural completeness audit:** Systematically checks all 12 ICH E9 required elements
- **Estimand framework assessment (ICH E9 R1):** Verifies each estimand is complete (population, variable, intercurrent events, handling strategy, population-level summary)
- **Pre-specification rigor audit:** Distinguishes objective decision rules (analyzable) from vague guidance (enables bias)
- **Missing data strategy deep-dive:** Mechanism assumption, method specification, sensitivity analysis planning
- **Multiplicity strategy coherence:** Confirms alpha adjustment or clear exploratory designation
- **Reproducibility check:** Could another biostatistician execute this SAP identically?
- **Timing verification:** Evidence that SAP was finalized before database lock/unblinding
- **Gap analysis:** Identifies missing sensitivity analyses, missing subgroup pre-specifications, incomplete safety detail
- **Calibrated severity scoring:** Distinguishes structural gaps (fatal), analytical weaknesses (major), and style issues (minor)

---

## Use When

- **Reviewing SAPs before study implementation** to ensure trial integrity and regulatory compliance before database lock
- **Assessing pre-registration documentation** (clinicaltrials.gov, Open Science Framework) for completeness
- **Evaluating published methods sections** of trial manuscripts that include SAP excerpts
- **Reviewing grant applications** proposing confirmatory trials to assess pre-specification rigor
- **Training biostatisticians or clinical researchers** on SAP standards and common gaps
- **Ensuring equity** in trial design (equity-relevant subgroups pre-specified, analytic strategies for PROGRESS-Plus variables documented)
- **Preparing for regulatory submissions** (FDA, EMA, ICH) where SAP completeness and compliance are scrutinized
- **Interim analysis planning** (verify interim boundaries and DMC charter alignment)
- **Multi-center trial coordination** (ensure all sites implement SAP identically; catch ambiguities that could lead to off-protocol deviations)

---

## Do Not Use When

- **Designing a new trial from scratch** (use study-design-planner instead)
- **Analyzing completed trial data** and interpreting results (use research-critic for manuscript review)
- **Reanalyzing or auditing statistical code** (use code-critic for reproducibility, data-critic for analytical questions)
- **Quick protocol screening** without depth (use lit-review-planner for rapid relevance screening)
- **Reviewing non-statistical methodology** (study design, recruitment, informed consent, ethical framework — use research-critic instead)
- **SAP is confidential/under embargo** and scope is limited by NDA or confidentiality (stay within constraints)
- **Reviewing statistical analysis results/findings** (SAP review is prospective; for retrospective manuscript critique use research-critic)

---

## Why This Exists

Statistical Analysis Plans are foundational to research integrity. Weak SAPs lead to:

- **P-hacking and selective reporting:** Researchers test many analyses post-hoc, report only those reaching p<0.05. Result: inflated false-positive rate, non-replicable findings.
- **HARKing (Hypothesizing After Results Known):** Subgroups, populations, or endpoints "discovered" during analysis, reported as confirmatory. Result: high false-positive risk, wasted resources on failed replications.
- **Outcome switching:** Primary endpoint changed during trial without documentation. Result: statistical significance on "new" primary endpoint may be false positive; originally-planned primary outcome buried.
- **Unmeasured multiplicity:** Many tests performed, no correction applied, selective reporting of significant results. Result: 15-30% false-positive rate reported as 5%.
- **Missing data chaos:** Mechanism assumed but not stated, method vague, no sensitivity analysis. Analyst chooses imputation method/deletion approach post-hoc based on which yields desired result. Result: conclusions not reproducible.
- **Regulatory rejection:** FDA, EMA request major revision or reject submission citing SAP ambiguity or inadequate pre-specification.
- **Publication failure and retraction:** Findings non-replicable; post-hoc analysis exposed; journal retracts; institutional trust eroded.

**Real examples of "published but flawed" SAPs:**
- RCT with three primary endpoints, no multiplicity adjustment, all three p<0.05 (expected rate: ~14% false positive under null; study likely chased noise)
- Observational cohort SAP states "missing data will be handled via multiple imputation" without specifying mechanism, number of imputations, or sensitivity analysis; analyst later chooses m=5 and MCAR assumption (non-standard, enabling flexibility)
- Trial SAP finalized after interim analysis (dated in final protocol but evidence shows written post-unblinding); interim findings influenced SAP decisions
- Non-inferiority SAP sets margin at 8% without clinical or regulatory justification; margin inflated to show non-inferiority despite clinically meaningful difference

sap-critic catches these gaps before they compromise trial integrity.

---

## Companion Skills

- **study-design-planner:** Design new trials, develop protocols, specify analysis strategies from scratch. Use BEFORE writing SAP to ensure design is sound.
- **research-critic:** Comprehensive review of published trial methodology, statistical analysis, and interpretation of results. Use AFTER trial completion to audit manuscript.
- **health-equity-analyzer:** Assess whether trial design and analysis capture or miss equity gaps (race/ethnicity, sex, age, comorbidity, socioeconomic status). Use with sap-critic to pre-specify equity-relevant subgroups.
- **proposal-critic:** Review research grant applications and funding proposals. Use for SAP sections of grant applications.
- **data-critic:** Audit statistical code, reproducibility, computational methods. Use to verify SAP can be executed in software as specified.

---

## Steps

1. **User provides:** Statistical Analysis Plan (SAP) document, study protocol with SAP section, or pre-registration (clinicaltrials.gov, OSF) with analysis specifications
2. **Skill routes to:** The local catalog/meta-router selects `sap-critic`, with a host general-purpose worker as fallback. OMC may execute the already-selected protocol only as an optional external worker.
3. **Embedded prompt executes:** Full 8-phase SAP Review Protocol (see below)
4. **Output:** Structured verdict (REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT) with:
   - ICH E9 Compliance Checklist (12 elements: present/absent/partial with evidence)
   - Estimand Assessment (ICH E9 R1 alignment)
   - Pre-Specification Timeline Assessment
   - CRITICAL/MAJOR/MINOR findings with evidence citations
   - What's Missing (gap analysis)
   - Strengths and recommendations

---

## Full SAP Review Protocol

The protocol below is embedded in the sap-critic agent. It is executed in full for every SAP review.

```
<Full_SAP_Review_Protocol>

<Phase_1_Pre_Commitment_Predictions>
Before reading the SAP in detail, predict:
- What trial type is this? (Confirmatory RCT, NI/NTo, adaptive, observational, Bayesian, interim, etc.)
- What are common completeness gaps for this type?
- What are likely analytical weaknesses?
- What would constitute CRITICAL vs. MAJOR vs. MINOR gaps?
Example: "This is a confirmatory RCT SAP. I expect to check: sample size justification, primary endpoint operationalization, missing data mechanism and method, multiplicity control, interim boundaries (if any), estimand framework, subgroup pre-specification. Common gaps: missing data strategy incomplete, multiplicity not addressed, subgroups added post-hoc."
</Phase_1_Pre_Commitment_Predictions>

<Phase_2_Structural_Completeness_Audit>
Systematically verify all 12 ICH E9 required elements:
1. Study objectives and hypotheses (primary/secondary/exploratory distinction)
2. Primary, secondary, exploratory endpoints (operationalization, timing, measurement)
3. Analysis populations (ITT, mITT, PP, safety; objective criteria)
4. Sample size and power (assumptions documented, sensitivity shown)
5. Primary analysis method (model fully specified, test statistic, decision rule)
6. Missing data handling (mechanism assumed, method specified, sensitivity analysis)
7. Sensitivity analyses (enumerated, meaningful to key assumptions)
8. Subgroup analyses (pre-specified vs. exploratory, with rationale)
9. Multiplicity strategy (alpha adjustment or exploratory designation)
10. Interim analyses (boundaries, alpha-spending, futility rules)
11. Blinding/unblinding procedures (roles, timing)
12. Software and version specification (reproducibility)

Red flags: "Appropriate methods will be used," "to be determined," "as deemed necessary," vague language enabling post-hoc choice
</Phase_2_Structural_Completeness_Audit>

<Phase_3_Statistical_Appropriateness_Audit>
Verify methods match data types and are correctly specified:
- Data type alignment (continuous→ANCOVA/MMRM, binary→logistic, time-to-event→Cox)
- Distributional assumptions stated and testable
- Confounding adjustment (observational) justified and complete
- Missing data strategy matched to mechanism assumption (MCAR→LOCF OK; MAR→MI; MNAR→pattern-mixture)
- Sensitivity analyses meaningful (tipping-point, per-protocol, alternative imputation)
- Multiplicity approach coherent (Bonferroni/Hochberg/FDR/gatekeeping appropriate)
- Non-inferiority margins justified (prior data, clinical judgment, regulatory guidance)
- Bayesian priors (if applicable) fully specified and justified

Red flags: Method chosen post-hoc "because it yielded X," no assumption testing, missing data "handled" without mechanism, multiplicity ignored
</Phase_3_Statistical_Appropriateness_Audit>

<Phase_4_Pre_Specification_Rigor_Audit>
Verify SAP enables reproducibility and prevents selective reporting:
- SAP finalized BEFORE database lock/unblinding (evidence: dates, signatures)
- All decision rules objective and testable (reject H0 if p<0.025, not "evaluate results")
- Subgroups pre-specified with biological rationale (not data-driven)
- Could another biostatistician execute SAP identically? (check for ambiguities)
- Interim analysis boundaries fully specified (O'Brien-Fleming, Lan-DeMets alpha-spending)
- Distinction between confirmatory, secondary, exploratory clear
- No vague language allowing post-hoc flexibility

Red flags: SAP dated after interim analysis, ambiguous language, subgroups "to be determined," decision rules subjective ("evaluate as appropriate")
</Phase_4_Pre_Specification_Rigor_Audit>

<Phase_5_Estimand_Framework_Audit>
Verify alignment with ICH E9 R1 estimand framework:
- Each estimand complete (population, variable, intercurrent events, handling strategy, population-level summary)
- Intercurrent events (treatment discontinuation, rescue medication, death, protocol deviation) enumerated
- Handling strategy for each event specified (treatment policy, composite, hypothetical, principal stratum, while-on-treatment)
- Primary analysis method estimates primary estimand
- Sensitivity estimands specified (e.g., per-protocol, while-on-treatment)

Red flags: Estimand not defined, intercurrent events ignored, treatment policy vs. while-on-treatment not distinguished
</Phase_5_Estimand_Framework_Audit>

<Phase_6_Gap_Analysis>
Identify what is MISSING:
- Sensitivity analyses for key assumptions absent?
- Equity-relevant subgroups (race/ethnicity, sex, age, comorbidity) not pre-specified?
- Missing data sensitivity (MNAR analysis) not planned?
- Protocol deviations not addressed (major vs minor, analysis impact)?
- Safety stopping rules not documented?
- PK/PD analysis (if relevant) not specified?
- Software version/reproducibility documentation incomplete?
- Data Monitoring Committee charter not referenced?
</Phase_6_Gap_Analysis>

<Phase_7_Realist_Check>
Calibrate severity:
- Is gap truly fatal or remediable?
- Are criticisms proportionate to study type?
- Am I rubber-stamping or manufacturing outrage?
- Would reasonable biostatistician consider SAP analyzable as-is?
</Phase_7_Realist_Check>

<Phase_8_Synthesis_and_Verdict>
Integrate findings:
- Weigh CRITICAL vs. MAJOR vs. MINOR findings
- Assign verdict (REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT)
- Estimate confidence
- Provide clear guidance for next steps

</Full_SAP_Review_Protocol>
```

---

## Severity Scale for SAP Findings

### CRITICAL (SAP Unfixable As-Is; Must Revise Before Database Lock)
Gaps that prevent reproducibility, enable selective reporting, or violate regulatory standards:

- **Primary endpoint unspecified:** Ambiguous definition, measurement method, or decision rule ("analysis will be conducted as appropriate")
- **No sample size justification:** Effect size source not documented, no power calculation, assumptions hidden
- **SAP written after unblinding or database lock:** Evidence shows SAP finalized post-hoc
- **No missing data strategy:** Mechanism not assumed, method undefined; analysis proceeds with unclear approach
- **No estimand definition (confirmatory trial):** Estimand not defined per ICH E9 R1; treatment policy vs. while-on-treatment not distinguished
- **Multiplicity unaddressed:** Multiple endpoints or many secondary analyses, no alpha adjustment, no statement
- **Subgroups pre-specified as primary without interaction test:** Claims confirmatory efficacy in subgroup without pre-registered interaction test and alpha control
- **Outcome switching without justification:** Primary endpoint changed from registered protocol without documented reason

### MAJOR (Analyzable but Requires Significant Revision Before Database Lock)
Gaps that limit interpretability or create bias risk:

- **Missing data strategy incomplete:** Mechanism assumed but method vague; no sensitivity to MCAR/MAR/MNAR assumption; no alternate approaches specified
- **No sensitivity analyses:** Zero sensitivity analyses despite key assumptions; single-approach analysis
- **Subgroups not pre-specified but presented as confirmatory:** Subgroups defined during analysis, reported as primary without multiplicity caveat
- **Analysis populations not clearly defined:** ITT/mITT/PP criteria not objective; potential for post-hoc reclassification
- **Interim analysis boundaries not specified:** Interim analyses planned but alpha-spending function, futility threshold, or decision rules undefined
- **Confounding adjustment insufficient (observational):** Key confounders not adjusted; adjustment set incomplete
- **Non-inferiority margin unjustified:** Margin stated without source or clinical meaningfulness
- **Software version not documented:** Reproducibility compromised
- **Intercurrent events not addressed:** Treatment discontinuation, rescue medication, missing data mechanisms not pre-specified
- **Bayesian priors (if applicable) not fully specified:** Distribution shape, parameters, and justification (prior elicitation, historical data, or informative/non-informative rationale) absent; sensitivity to prior choice not planned
- **Confounding adjustment set incomplete (observational SAPs):** Key confounders identified in literature but omitted from adjustment; variable selection method not justified; potential collider adjustment not addressed
- **MNAR sensitivity analysis not planned:** Missing data mechanism assumed MAR without justification; no tipping-point, pattern-mixture, delta-adjusted, or reference-based imputation sensitivity specified
- **Covariance structure for repeated measures not sensitivity-analyzed:** Single structure assumed without testing alternatives

### MINOR (Analyzable; Acceptable with Clarification)
Correctable gaps or within normal SAP constraints:

- **Covariance structure not specified:** Unstructured assumed but not documented
- **Statistical software version missing:** Software named but version not stated
- **Minor operationalization ambiguities:** Outcome definition mostly clear but timing or assessment method not fully detailed
- **Exploratory analyses not detailed:** Exploratory section brief but clearly labeled as hypothesis-generating
- **Safety endpoints described briefly:** Safety listed but specific stopping rules not documented (acceptable if standard pharmacovigilance rules apply)
- **Subgroup analysis list incomplete:** Subgroups pre-specified but additional exploratory subgroups mentioned, clearly labeled exploratory

---

## Standards Grounding

- **ICH E9 (2.3):** Clinical trial statistical principles (sampling, populations, hypotheses, analysis, interim, missing data, multiplicity)
- **ICH E9 R1:** Addendum on estimand and sensitivity analyses (estimand framework, intercurrent events, missing data sensitivity)
- **ICH E6 (GCP):** Good Clinical Practice standards (SAP finalization before unblinding, data lock, protocol adherence)
- **FDA Guidance for Industry:** Statistical Principles in Clinical Trial Design, Data Analysis, and Reporting
- **EMA Guideline on Missing Data:** Missing data strategies, MCAR/MAR/MNAR, sensitivity analysis
- **CONSORT-SPI:** Statistical Analysis Plan extension for transparent reporting
- **SPIRIT 2013:** Standard Protocol Items; Recommendations for Interventional Trials (statistical analysis section requirements)
- **FDA Guidance on Interim Analyses:** Group sequential testing, alpha-spending functions

---

## Tool Usage

**Allowed (read-only):**
- Read SAP documents, protocols, appendices, amendments
- Search web for regulatory guidance (ICH, FDA, EMA, CONSORT, SPIRIT)
- Search literature for methodological references
- Take screenshots of SAP tables and algorithms for detailed inspection
- Navigate to cited regulatory documents for fact-checking

**Not Allowed:**
- Write or edit SAP documents
- Conduct analysis or reanalysis (refer to data-critic)
- Create statistical code (refer to code-critic)
- Provide regulatory submission guidance (acknowledge need for regulatory consulting)
- Generate revised SAP prose (refer to copy-critic)

---

## Examples

### Example 1: Confirmatory RCT SAP Missing Multiplicity Control

**Study:** "Efficacy of Drug X vs. Placebo in Schizophrenia: RCT"
- Design: Confirmatory RCT, n=300, 12-week primary endpoint
- Primary endpoint: PANSS score reduction
- Secondary endpoints: Positive Symptom Subscale, Negative Symptom Subscale, Cognitive Battery
- SAP states: "Four endpoints analyzed independently at α=0.05, no multiplicity adjustment"

**Prediction:** Confirmatory RCT with multiple endpoints, no multiplicity plan. Likely MAJOR gap.

**Finding (MAJOR):** `Four endpoints analyzed at α=0.05 without adjustment yields family-wise error rate ≈0.19 (19% false-positive risk). ICH E9 requires multiplicity control. Options: (1) gatekeeping (secondary only if primary succeeds), (2) Bonferroni α=0.05/4=0.0125, (3) Hochberg procedure, (4) label secondary/cognitive endpoints as exploratory.`

**Verdict:** REVISE

---

### Example 2: Observational Cohort SAP with Vague Missing Data Strategy

**Study:** "Hormone Replacement Therapy and Cardiovascular Outcomes: Prospective Cohort"
- SAP states: "Missing baseline covariates will be handled via multiple imputation"
- No mechanism assumption (MCAR/MAR/MNAR)
- No number of imputations specified
- No sensitivity analysis
- No mention of dropout rates or differential dropout by group

**Prediction:** Observational cohort, missing data strategy incomplete. Likely MAJOR gap.

**Finding (MAJOR):** `Multiple imputation mentioned but incompletely specified: no mechanism assumption, no m (number of imputations), no sensitivity to MAR assumption, no MNAR analysis. For long-term cohort with potential differential dropout (sicker women may drop out), MAR assumption questionable. Recommend: (1) state MAR assumption explicitly, (2) specify m≥20, (3) add tipping-point MNAR sensitivity analysis, (4) compare MI result to per-protocol (women with complete follow-up only).`

**Verdict:** REVISE

---

### Example 3: Non-Inferiority SAP with Unjustified Margin

**Study:** "Biosimilar vs. Originator Monoclonal Antibody in Rheumatoid Arthritis: NI RCT"
- Non-inferiority margin: 10% absolute response rate difference
- SAP provides no source for margin, no clinical rationale, no regulatory guidance cited
- Proposed margin appears inflated given study population response rates

**Finding (MAJOR):** `Non-inferiority margin of 10% absolute difference stated without justification. FDA and EMA expect margin to be (1) clinically meaningful, (2) supported by prior data, (3) consistent with regulatory guidance. Recomm: document margin source (prior biosimilar trials, clinical expert opinion, regulatory pre-submission), provide justification for why 10% is clinically acceptable (not margin of convenience to show NI).`

**Verdict:** REVISE

---

### Example 4: Well-Specified Confirmatory RCT SAP Achieving ACCEPT

**Study:** "Efficacy of Drug X vs. Placebo in Major Depression: RCT"
- Design: Confirmatory RCT, n=400, 8-week primary
- Primary estimand: ITT, treatment policy (include all randomized, regardless of treatment adherence); endpoint= Mean change in HAMD-17 from baseline to Week 8
- Sample size: 80% power to detect Cohen's d=0.4 (clinical meaningful), alpha=0.05, n=194 per arm; n=400 total (accounts for ~3% dropout)
- Missing data: MAR assumption (dropout due to lack of efficacy, observable via baseline severity); primary analysis= Multiple Imputation (m=25) with baseline HAMD-17, age, site; sensitivity= per-protocol analysis (≥80% protocol adherence)
- Multiplicity: Primary endpoint only (secondary endpoints labeled exploratory, no alpha adjustment, 95% CI for context)
- Interim: One interim at 50% enrolled, Lan-DeMets alpha-spending (O'Brien-Fleming), interim alpha=0.001, final alpha=0.049
- Subgroups: None confirmatory. Exploratory: age, sex, baseline severity (interaction tests reported but not alpha-controlled, labeled hypothesis-generating)
- Software: SAS 9.4, PROC MIANALYZE for MI, R seed=54321
- Safety: Adverse events MedDRA-graded; stopping rule: stop if serious adverse event rate ≥10% in one arm

**Prediction:** Confirmatory RCT, well-structured, likely complete.

**Analysis:**
- Estimand clearly defined (population, variable, intercurrent event treatment policy, population summary)
- Sample size calculated with transparent assumptions, prior data cited
- Missing data: MAR stated and justified; method fully specified (m=25, baseline covariates, algorithm); sensitivity (per-protocol)
- Interim: Boundaries fully specified (Lan-DeMets), alpha budget documented
- Multiplicity: Primary only with one-sided alpha; secondary/exploratory appropriately caveat
- Subgroups: Exploratory, pre-specified with justification, interaction tests reported (not alpha-controlled), labeled hypothesis-generating
- Reproducibility: Software version, macro, random seed documented
- No vague language; all decision rules objective

**Strengths:**
- Estimand framework complete per ICH E9 R1
- Interim analysis rigorous (Lan-DeMets alpha-spending transparent)
- Missing data strategy well-justified and sensitivity-analyzed
- Clear confirmatory/exploratory distinction
- Excellent reproducibility documentation
- Safety stopping rule pre-specified

**Verdict:** ACCEPT

**Confidence:** High

---

## Benchmark Test Info

Tested on internal SAP scenarios across confirmatory RCTs, observational studies, and adaptive designs. Systematic benchmarking with published methodology pending. Peer review of all production SAP assessments recommended.

---

## Notes

- **Scope boundary:** sap-critic reviews SAP documents and pre-specifications. Does not design trials (study-design-planner), analyze completed data (research-critic), or debug code (code-critic).
- **Collaboration:** Pair with study-design-planner if trial design itself needs strengthening. Pair with health-equity-analyzer to ensure equity-relevant subgroups are pre-specified. Pair with research-critic for post-trial manuscript review.
- **Confidence calibration:** Be direct about CRITICAL gaps (these block trial integrity). Be proportionate on MINOR issues (these don't sink SAPs).
- **Timing:** Budget 20–25 minutes per SAP for thorough review. SAPs differ widely in length and complexity; complex adaptive trials require more time.
- **Iterative refinement:** Users can ask for deeper dives (e.g., "audit CONSORT-SPI compliance item-by-item," "assess missing data strategy against EMA guideline," "review interim analysis plan against DMC charter").
- **Regulatory readiness:** This review prepares SAPs for regulatory submission (FDA, EMA). If regulatory engagement is needed, recommend consulting regulatory affairs before submission.
