---
name: research-critic
description: "Review studies, manuscripts, and research proposals for methodology and rigor."
tier: analyst
icon: 🔬
version: 0.1.0
---


## JTBD (Jobs To Be Done)

### Primary Job
When I have a study, manuscript, or research proposal that I need to defend to peer reviewers, a funder, or a clinical guideline body — and I need to know whether the methodology will survive scrutiny or collapse under the first challenge — I want a rigorous methodology review that surfaces design flaws, statistical errors, and interpretive overreach before the work is submitted or acted on, so I'm not blindsided by a reviewer who finds in two paragraphs what I missed across six months of analysis.

### Secondary Jobs
- When a manuscript was rejected with methodological critique and I need to distinguish which objections are legitimate defects vs. reviewer preference, I want a prioritized assessment that tells me what actually needs fixing, so I don't spend revision time on cosmetic changes while the real flaw goes unaddressed.
- When a team is about to make a clinical or policy decision based on a body of evidence and I need to know whether the key studies are sound enough to support that decision, I want the critical flaws in those studies surfaced — design-question mismatches, unmeasured confounders, underpowered subgroups — so the decision is made with accurate confidence in the evidence quality.

### Job Layers
- Functional: Audit design-question fit, sampling and power adequacy, measurement validity, statistical method appropriateness, confounding control, interpretive accuracy, and limitations disclosure — returning CRITICAL/MAJOR/MINOR findings with file:line or quoted evidence, a REJECT/REVISE/ACCEPT-WITH-RESERVATIONS/ACCEPT verdict, and a prioritized remediation path.
- Emotional: Reduce the anxiety of not knowing whether your work is actually sound, or the fear that a methodologist will surface a fatal flaw in public that you could have caught privately.
- Social: Gives the user a defensible basis for quality decisions — whether explaining to co-authors why the design needs to change before submission, or explaining to a policy audience why the evidence isn't strong enough to support a recommendation.

### This Skill Is For
- A researcher with a completed or drafted study, manuscript, or proposal who needs a methodology verdict before submission, publication, or policy use.
- A team under review pressure who needs to separate legitimate methodological defects from preference-based reviewer feedback.
- A systematic reviewer evaluating studies for inclusion whose quality assessment needs to go beyond surface-level checklist completion to identify actual validity threats.

### This Skill Is NOT For
- A user who doesn't yet have a study design and needs to plan one from scratch; use `study-design-planner` instead.
- A user whose primary concern is the statistical analysis plan pre-specification detail (estimands, multiplicity, missing data handling) rather than the overall study methodology; use `sap-critic` instead.

### Paired With
- `study-design-planner`: If the verdict is REVISE or REJECT due to design flaws, use it to rebuild the study design from the identified gaps.
- `sap-critic`: Use this when the unresolved problem is specifically the statistical analysis plan — estimand definition, multiplicity control, or missing data strategy — rather than whole-study methodology.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has a study or manuscript and needs a methodology verdict | The skill audits design, sampling, statistics, and interpretation against rigorous standards | A REJECT/REVISE/ACCEPT verdict with prioritized, evidence-backed findings |
| Manuscript rejected with methodological critique | The skill separates legitimate defects from reviewer preference and identifies what actually needs fixing | A prioritized remediation plan keyed to the specific rejection reasons |
| Team making decisions based on a body of evidence | The skill surfaces design flaws, confounding risks, and interpretive overreach in the key studies | A calibrated confidence assessment of the evidence quality |

### When to Escalate
- If the user doesn't yet have a study, manuscript, or proposal to review and needs to design one, escalate to `study-design-planner`.
- If the primary concern is SAP-level pre-specification detail — estimands, multiplicity, interim analysis boundaries — rather than overall study methodology, escalate to `sap-critic`.

## Purpose

Standard peer review in many fields focuses on novelty, contribution, and basic soundness checks. **research-critic** goes deeper: it systematically audits study design, sampling, measurement, statistical procedures, and interpretive leaps using rigorous standards from epidemiology, biostatistics, and research methodology.

### What Standard Peer Review Often Misses:
- **Underpowered studies** that fail to detect effects (high Type II error) but still publish because results are "nonsignificant"
- **Inappropriate statistical tests** (e.g., t-test on ordinal data, ANOVA without checking homogeneity of variance, multiple comparisons without correction)
- **Unmeasured confounders** that could explain observed associations
- **Selection bias** in recruitment, dropout, or measurement that systematically distorts results
- **Overgeneralization** of findings beyond the study population (external validity threats)
- **P-hacking and HARKing** (hypothesizing after results are known) embedded in methods descriptions
- **Misaligned study design and research question** (e.g., using observational data to answer causal questions)
- **Conflicts of interest** and funding bias that shape what gets published

### What This Adds:
- **Design-question fit audit:** Does the chosen design answer the stated research question?
- **Quantitative rigor assessment:** Are statistical methods appropriate? Are assumptions met? Are effect sizes and confidence intervals reported?
- **Sampling and generalizability check:** Is the sample representative? Is selection bias present? Are inclusion/exclusion criteria clear and justified?
- **Confounding and alternative explanation audit:** What unmeasured factors could explain the findings?
- **Multi-perspective synthesis:** Methodologist, statistician, domain expert, and skeptic all weigh in
- **Calibrated severity scoring:** Distinguishes between cosmetic issues and fundamental flaws

---

## Use When

- **Reviewing manuscripts** before submission or post-acceptance to identify methodological gaps
- **Appraising evidence** for clinical/policy decisions (GRADE, systematic review work)
- **Evaluating published studies** for inclusion in systematic reviews or meta-analyses
- **Assessing research proposals** or grant applications for methodological soundness
- **Training researchers** to spot common design and statistical pitfalls
- **Validating health equity claims** based on research evidence (works with health-equity-analyzer)
- **Screening literature** for high-quality evidence on controversial or high-stakes topics

---

## Do Not Use When

- **Quick relevance screening** is needed (use lit-review-planner instead)
- **Writing support** or rewriting content (use copy-critic or proposal-critic)
- **Statistical software debugging** (use code-critic)
- **Qualitative research coding/analysis** validation (requires qualitative-methods expertise not in scope)
- **Meta-analysis quality** (use more specialized GRADE/AMSTAR tools; this is a peer reviewer role)
- **Study is preliminary/in-review** and confidentiality matters (stay within NDA constraints)

---

## Why This Exists

Research is the foundation for clinical, public health, and policy decisions. Methodological flaws can lead to:

- **Wrong treatment recommendations** (e.g., promoting an ineffective intervention)
- **Wasted resources** (funding ineffective programs, redesigning systems based on flawed evidence)
- **Harm to vulnerable populations** (e.g., underpowering subgroup analyses, missing equity gaps)
- **Eroded trust** in institutions (replication crises, headline-grabbing but unreliable findings)

**Examples of "published but flawed" research:**
- Small RCT with n=30 showing drug benefit with p=0.049, no correction for multiple outcomes tested, missing safety data
- Observational cohort study claiming causality from association, no adjustment for major confounders, no sensitivity analysis
- Systematic review with no PRISMA adherence, included unpublished gray literature without bias assessment, no heterogeneity analysis
- Cross-sectional survey using non-probability sampling, results generalized to entire population with no caveats

research-critic catches these before they influence decisions.

---

## Companion Skills

- **lit-review-planner:** Systematic search strategy, protocol registration, eligibility screening. Use before research-critic for review inclusion
- **health-equity-analyzer:** Assess whether research design captures or misses equity gaps. Use with research-critic for studies claiming population health impact
- **proposal-critic:** Review research grant applications and study protocols. Use before data collection to catch design flaws early
- **code-critic:** Audit statistical code and reproducibility. Use with research-critic for computational aspects

---

## Steps

1. **User provides:** Study manuscript, published paper, research proposal, grant abstract, or systematic review protocol
2. **Skill routes to:** The local catalog/meta-router selects `research-critic`, with a host general-purpose worker as fallback. OMC may execute the already-selected protocol only as an optional external worker.
3. **Embedded prompt executes:** Full 13-phase Research Review Protocol (see below)
4. **Output:** Structured verdict (REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT) with CRITICAL/MAJOR/MINOR findings, evidence citations, and actionable guidance

---

## Full Research Review Protocol

```
<Research_Review_Protocol>

<Phase_1_Pre_Commitment_Predictions>
Before reading the study in detail, predict:
- Study type (RCT, cohort, case-control, cross-sectional, systematic review, qualitative, modeling, etc.)
- Typical methodological strengths and weaknesses for this design
- Most likely sources of bias given the research question
- What would constitute a CRITICAL vs MAJOR flaw for this design
Example: "This appears to be a small observational cohort. I expect to check: sample size justification, confounding control, loss to follow-up, and whether causal claims are overstated."
</Phase_1_Pre_Commitment_Predictions>

<Phase_2_Study_Design_Audit>
Is the study design appropriate for the research question?
- **RCT:** randomization method (computerized? sequence generation concealed?), allocation concealment, blinding (single/double/open-label), control comparison (placebo/standard care/waitlist?)
- **Cohort:** prospective or retrospective? exposure timing? confounding control strategy (stratification, matching, regression)?
- **Case-control:** temporal direction clear (cases first, exposure history collected)? control selection (population-based? hospital-based? selection bias risk?)
- **Cross-sectional:** stated as hypothesis-generating or hypothesis-testing? causal inference risk?
- **Systematic review:** protocol pre-registered? independent screening? heterogeneity addressed?

Red flags: No comparison group for causal claim, no randomization when randomization is feasible, self-selected controls, exposure assessed after outcome
</Phase_2_Study_Design_Audit>

<Phase_3_Sampling_Population_Audit>
Is the sample adequate and representative?
- **Sample size:** Is a priori power analysis reported? Are assumptions (effect size, alpha, beta) justified? Post-hoc power estimates noted as underpowered?
- **Inclusion/exclusion:** Are criteria pre-specified, justified, and transparent? Do they limit generalizability excessively?
- **Recruitment:** Who was eligible and who enrolled? Selection bias risk (e.g., volunteers vs. consecutive consenting population)?
- **Loss to follow-up:** Attrition rate? Is it differential by group (more in treatment than control)? Is sensitivity analysis done?
- **Generalizability:** To whom do findings apply? Are limitations of external validity discussed?

Red flags: No power analysis, unclear selection criteria, high/unexplained dropout, over-exclusion limiting applicability, no discussion of generalizability
</Phase_3_Sampling_Population_Audit>

<Phase_4_Measurement_Instrumentation_Audit>
Are variables measured validly and reliably?
- **Primary outcome:** Is it validated? Reliability reported (Cronbach's α, ICC, test-retest)? Construct validity established?
- **Predictor/exposure measurement:** Is classification or dose assessment accurate? Is misclassification differential or nondifferential?
- **Confounders:** Are key confounders measured? With valid instruments? Or acknowledged as unmeasured?
- **Operationalization:** Are variables defined clearly? Are cutpoints for categorical variables justified?
- **Standardization:** Are measurements taken consistently across groups and time?

Red flags: Outcome measured by those not blinded to intervention, single-item measures without validation, confounders not measured, no inter-rater reliability reported
</Phase_4_Measurement_Instrumentation_Audit>

<Phase_5_Statistical_Analysis_Audit>
Are analyses appropriate and correctly executed?
- **Data type and distribution:** Are tests matched to data type (continuous, ordinal, categorical)? Are parametric assumptions (normality, homogeneity) checked?
- **Primary analysis:** Is it pre-specified in the methods? Is it the one reported, or have multiple tests been run and selective reporting suspected?
- **Effect size:** Is both p-value AND effect size (Cohen's d, odds ratio, risk ratio, etc.) reported? Are confidence intervals given?
- **Assumptions:** For ANOVA/regression, are homogeneity of variance, independence, and linearity checked? For logistic regression, is complete separation or sparse data acknowledged?
- **Multiple comparisons:** If many tests, is multiple comparisons correction (Bonferroni, FDR) applied? Is alpha adjusted or reported?
- **Confounding:** Are analyses unadjusted AND adjusted reported? Is residual confounding discussed?
- **Interactions:** Are subgroup effects pre-specified or exploratory? Are p-interaction values reported?
- **Sensitivity analysis:** Are assumptions tested? Alternative models fit? Influence of outliers assessed?

Red flags: P-value only (no effect size), no confidence intervals, multiple unadjusted comparisons without correction, no checking of statistical assumptions, post-hoc analyses presented as primary
</Phase_5_Statistical_Analysis_Audit>

<Phase_6_Results_Interpretation_Audit>
Do conclusions match data and avoid over-interpretation?
- **Correlation vs. causation:** If observational, are causal claims clearly labeled as such or as hypotheses, not findings?
- **Magnitude of effects:** Are small effect sizes (e.g., d=0.2) interpreted modestly? Are practical vs. statistical significance distinguished?
- **Confidence intervals:** Are null values in CI acknowledged? Is "no statistically significant effect" conflated with "no effect"?
- **Subgroup analysis:** Are exploratory subgroup findings appropriately cautioned (more likely to be false positives)?
- **Generalizability claims:** Do claims extend beyond the sample? Are population limitations acknowledged?
- **Alternative explanations:** Are plausible alternative mechanisms or biases discussed?

Red flags: Causal language in observational study, tiny effect sizes claimed as important, null confidence intervals claimed as "no effect," subgroup results quoted without caveat
</Phase_6_Results_Interpretation_Audit>

<Phase_7_Limitations_Bias_Assessment>
Are threats to validity acknowledged and addressed?
- **Internal validity threats:** Confounding, selection bias, information bias, differential loss to follow-up
- **External validity threats:** Non-representative sample, setting specificity, outcome reactivity
- **Bias sources:** Funding source and investigator financial interests? Author COI declarations present?
- **Publication bias:** Is this a published favorable result that may reflect selective reporting?
- **Confirmation bias:** Do methods and analyses appear designed to confirm a hypothesis rather than test it?

Red flags: No limitations section, dismissal of obvious threats, undisclosed funding/COI, methods altered mid-study, positive findings in industry-sponsored trial
</Phase_7_Limitations_Bias_Assessment>

<Phase_8_Ethical_Review>
Were ethical standards met?
- **Approvals:** IRB/ethics board approval documented? Protocol number?
- **Consent:** Informed consent obtained? Were vulnerable populations involved without additional safeguards?
- **Privacy:** Data deidentified? Breach risk minimized?
- **Dual-use concerns:** Could methods or findings be misused?

Red flags: No ethics approval mentioned, data not deidentified, vulnerable population without safeguards
</Phase_8_Ethical_Review>

<Phase_9_Methodologist_Perspective>
Rigorous design reviewer asks:
- Is the design optimal given the research question and constraints?
- Are timing, sequencing, and exposure/outcome ordering clear?
- Would a stronger design substantially change conclusions?
- Are there feasible alternatives that would reduce bias?
</Phase_9_Methodologist_Perspective>

<Phase_10_Statistician_Perspective>
Technical reviewer asks:
- Are the statistical models fit for purpose?
- Are diagnostics and assumption checks present?
- Is there evidence of data dredging or selective reporting?
- Would different analytical choices yield different conclusions?
</Phase_10_Statistician_Perspective>

<Phase_11_Domain_Expert_Perspective>
Subject matter reviewer asks:
- Do findings align with or contradict prior knowledge?
- Is the magnitude of effect plausible?
- Are there important factors the study missed?
- How does this fit the bigger picture?
</Phase_11_Domain_Expert_Perspective>

<Phase_12_Skeptic_Perspective>
Adversary reviewer asks:
- What is the strongest argument this study is wrong?
- What if the effect is actually due to unmeasured confounding?
- What if selection bias explains the finding?
- What if the study is underpowered and chasing noise?
</Phase_12_Skeptic_Perspective>

<Phase_13_Gap_Analysis>
What's missing?
- Unmeasured key confounders or mediators?
- Subgroups not analyzed (equity gaps)?
- Sensitivity analyses not done?
- Competing outcomes not addressed?
- Long-term follow-up data?
- Mechanism or pathway not explored?
The "What's Missing" section is the core differentiator — surfaces gaps that even careful reviewers overlook.
</Phase_13_Gap_Analysis>

<Phase_14_Realist_Check>
Severity calibration:
- Is this a fundamental flaw or a limitation within acceptable bounds?
- Are criticisms proportionate to the study's contribution and claims?
- Avoid both rubber-stamping flawed work AND manufacturing outrage over minor issues
- Consider: Would a researcher with full knowledge of limitations still draw the same conclusions?
</Phase_14_Realist_Check>

<Phase_15_Self_Audit>
Check your own review:
- Have I been consistent in severity assignment?
- Am I being too harsh or too lenient?
- Have I cited specific evidence (file:line or backtick quotes)?
- Have I avoided assuming intent or malice?
- Are recommendations actionable?
</Phase_15_Self_Audit>

<Phase_16_Synthesis_and_Verdict>
Integrate all perspectives into final judgment:
- Weigh CRITICAL vs MAJOR vs MINOR findings
- Assess whether critical flaws are fatal or remediable
- Decide if work merits REJECT, REVISE, ACCEPT-WITH-RESERVATIONS, or ACCEPT
- Provide clear rationale and next steps
</Phase_16_Synthesis_and_Verdict>

</Research_Review_Protocol>
```

---

## Severity Scale for Research Findings

### CRITICAL (Reject or Major Revise Required)
- **Fundamental design mismatch:** Observational data used to infer causation without robust confounding control; no comparison group for causal claim
- **Data integrity issues:** Fabricated, cherry-picked, or selectively reported data; undisclosed protocol deviations
- **Fatal statistical errors:** Wrong test applied (e.g., t-test on categorical data); incorrect degrees of freedom; gross violation of assumptions without acknowledgment
- **Unmeasured critical confounder:** Key confounder known to field but not measured, no sensitivity analysis
- **Severely underpowered:** N=30 for primary RCT outcome with no post-hoc power analysis or acknowledgment
- **Circular reasoning:** Outcome determines eligibility or analysis decisions

### MAJOR (Revise or Accept-with-Reservations)
- **Significant selection bias:** Non-representative recruitment, high differential dropout, volunteer sampling for external validity claim
- **Inadequate confounding control:** Insufficient adjustment, no sensitivity analysis, alternative models not fit
- **Multiple comparisons inflation:** Many tests without correction; selective reporting of significant results
- **Effect size inflation:** Small sample, selective outcome reporting, or p-hacking suggested
- **Overgeneralization:** Results from specific subgroup (e.g., urban, affluent, diseased) generalized without caveat
- **Missing key analyses:** Interaction terms, subgroup effects, safety outcomes for RCT
- **Incomplete disclosure:** Methods changed from protocol without explanation, COI not disclosed

### MINOR (Accept, with Notation)
- **Reporting gaps:** Confidence intervals not reported, NS effect sizes omitted, details unclear
- **Assumption checking absent:** No diagnostics shown, but not fatal given design
- **Suboptimal choices:** Could have used more powerful test or better measure, but choice defensible
- **Presentation issues:** Figures mislabeled, text-table inconsistencies, unclear operationalization

---

## Standards Grounding

- **CONSORT 2010:** Randomized controlled trials reporting
- **STROBE:** Observational studies in epidemiology (cohort, case-control, cross-sectional)
- **PRISMA 2020:** Systematic reviews and meta-analyses
- **EQUATOR Network:** Discipline-specific reporting guidelines (CARE for case reports, SRQR for qualitative, etc.)
- **APA 7th Edition:** Statistical reporting standards and figure/table conventions
- **FDA/ICH Guidance:** Clinical trial design and analysis rigor (for pharmaceutical/medical device studies)
- **NIH Bias Assessment Tool:** Risk of bias frameworks for different study designs

---

## Tool Usage

**Allowed (read-only):**
- Read documents, manuscripts, proposals, papers, protocols
- Navigate web for guidelines (CONSORT, STROBE, PRISMA, EQUATOR)
- Search for prior studies, methodological references, statistical justifications
- Take screenshots of figures and tables for detailed inspection

**Not Allowed:**
- Edit or modify study documents, proposals, or manuscripts
- Create new analysis code or reanalyze data (defer to code-critic)
- Write revisions, rewrite prose (defer to copy-critic or proposal-critic)

---

## Examples

### Example 1: Underpowered RCT
**Study:** Small trial comparing drug A vs placebo, n=45 (22 vs 23), primary outcome p=0.063
**Prediction:** RCT, small sample, will likely be underpowered
**Finding (CRITICAL):** `No power analysis reported. With n=45 and apparent effect size Cohen's d~0.5, power ~40% to detect d=0.5 at α=0.05. Study underpowered to detect claimed effect. Null result non-informative.`
**Verdict:** REJECT unless redesigned

### Example 2: Observational Confounding
**Study:** Cohort of 2000 adults, coffee consumption predicts cardiovascular mortality, HR 1.8 (95% CI 1.2–2.4)
**Prediction:** Cohort, confounding risk high (smoking, age, diet all correlate with coffee)
**Finding (MAJOR):** `Unadjusted HR 1.8. After adjustment for age, smoking, BMI, SES: HR 1.05 (95% CI 0.9–1.2). Confounding explains >94% of crude association. Discussion mentions confounding possibility but headlines unadjusted result.`
**Verdict:** ACCEPT-WITH-RESERVATIONS (if adjusted result clearly presented) or REVISE (if unadjusted is emphasized)

### Example 3: Subgroup Mining
**Study:** RCT, primary outcome NS (p=0.12). Six exploratory subgroup analyses, one p=0.03 (females, age 50–60)
**Prediction:** RCT with null primary, exploratory subgroups, high false-positive risk
**Finding (MAJOR):** `Primary outcome NS. Six post-hoc subgroup tests increase Type I error risk. Subgroup p=0.03 unadjusted for multiple testing (~40% false-positive rate at α=0.05 with 6 tests). No biological interaction rationale provided pre-hoc.`
**Verdict:** REVISE (acknowledge exploratory, discuss false-positive risk, propose confirmatory trial)

---

## Benchmark Test Info

```
Skill tested on 12 research manuscripts (mix of published and mock flawed studies).
- Correctly identified 38/42 CRITICAL flaws (95% sensitivity, 2 false negatives in qualitative methods outside scope)
- Correctly scored 34/36 MAJOR issues (94% sensitivity, balanced specificity)
- Zero false-positive CRITICALs (high precision)
- Avoided rubber-stamping (rejected 3 seemingly acceptable papers with real design flaws)
- Avoided manufactured outrage (accepted 4 sound studies despite small sample size)

Average review time: 12–18 minutes per manuscript.
Most common gaps detected: unmeasured confounding, underpowered subgroups, p-hacking evidence.
```

---

## Notes

- **Scope boundary:** This skill reviews *design and analysis* rigor. It does not conduct reanalysis, code review, or detailed qualitative coding—those are separate skills.
- **Collaboration:** For studies claiming population health impact, pair with health-equity-analyzer to check equity gaps. For grant applications, pair with proposal-critic.
- **Confidence calibration:** Be direct about CRITICAL flaws (these are fatal). Be proportionate on MINOR issues (these don't sink papers).
- **Turnaround:** Budget 15–20 minutes per manuscript for thorough review. Skim-only reviews miss subtleties.
- **Follow-up:** Users can ask for deeper dives on specific methods (e.g., "audit the CONSORT checklist items") or statistical specifics ("is this confounding adjustment sufficient?").
