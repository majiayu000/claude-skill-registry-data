---
description: Turn research questions into a defensible study design before data collection.
icon: 📐
name: study-design-planner
tier: analyst
version: 0.1.0
---

# study-design-planner

**Companion to**: research-critic (reviews completed design), lit-review-planner (establishes evidence base), sap-critic (reviews statistical analysis plan), health-equity-analyzer (assesses equity dimensions)

**Best with**: Research teams, epidemiologists, clinical trialists, health services researchers designing new studies

**Entry point**: `/study-design-planner "Your research question and study context"`

---

## JTBD (Jobs To Be Done)

### Primary Job
When I have a research question but no study design — and I know that choosing the wrong design means collecting data that can't answer the question, or running out of power before detecting a real effect — I want a design specification that locks in the right design, sample size, and bias prevention strategy before recruitment starts, so I don't discover three years in that the design can't support the causal claim I need to make.

### Secondary Jobs
- When a study design has been criticized by an IRB, funder, or peer reviewer for design-question mismatch, inadequate power, or uncontrolled confounding, I want a redesign that directly addresses those objections, so the resubmission doesn't repeat the structural flaws.
- When a team is debating RCT vs. observational design — and the tradeoffs between internal validity, cost, and feasibility are unresolved — I want those tradeoffs scored and documented, so the design decision isn't relitigated when the grant review panel asks why you didn't randomize.

### Job Layers
- Functional: Produce a design selection matrix scoring candidate designs on internal validity, external validity, cost, and timeline; a PICO/PICOS specification; a causal DAG; a power analysis with sensitivity table; a population and sampling protocol; a variable specification with measurement instruments; and a bias prevention matrix — all before data collection begins.
- Emotional: Reduce the fear that after 18 months of data collection you'll discover the design can't support causal inference, or that the sample is too small to detect the effect that justifies the intervention.
- Social: Helps the user present a fundable, IRB-approvable, peer-review-defensible design to grant reviewers, ethics boards, and co-investigators who will challenge every design choice.

### This Skill Is For
- A researcher beginning a new study who needs a complete design specification — including sample size justification, confounding control strategy, and bias prevention plan — before any data collection.
- A team whose protocol was rejected by an IRB, funder, or grant reviewer and needs a redesign that directly addresses the stated deficiencies.
- A team debating study design options (RCT vs. cohort vs. quasi-experimental) and needing the tradeoffs made explicit with a documented rationale for the chosen design.

### This Skill Is NOT For
- A user with an existing completed or drafted statistical analysis plan who needs a quality verdict on the analysis approach; use `sap-critic` instead.
- A user with an existing published study who needs a methodology review; use `research-critic` instead.

### Paired With
- `sap-critic`: After the study design is finalized and the SAP is drafted, use it to audit the statistical analysis plan for estimand, multiplicity, and missing-data gaps.
- `research-critic`: Use this when the unresolved problem is reviewing the methodology of existing completed work, not designing a new study.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has a research question but no design | The skill selects the design, sizes the sample, draws the causal DAG, and specifies bias prevention | An IRB-submittable protocol specification |
| Protocol was rejected for design or power flaws | The skill identifies the structural gaps and rebuilds the design to address them | A redesign plan targeting the specific rejection reasons |
| Team is debating RCT vs. observational | The skill scores each design on validity, cost, timeline, and feasibility | A documented design decision with tradeoff rationale |

### When to Escalate
- If the user has a drafted SAP and needs a quality verdict on the analysis plan, escalate to `sap-critic`.
- If the user has an existing published or completed study and needs a methodology review, escalate to `research-critic`.

## Purpose

Well-designed studies are rarely accident. They require careful specification of research questions, explicit design choices, power-driven sample sizing, causal reasoning (directed acyclic graphs), and systematic bias prevention **before data collection**. Yet many researchers skip this phase, jumping straight to recruitment or analysis—leading to:

- **Design-question mismatches** (using observational data to answer causal questions; using cross-sectional designs for longitudinal hypotheses)
- **Underpowered studies** that waste years and millions in funding
- **Unmeasured confounders** that could explain findings but weren't planned for
- **Selection bias** from non-representative recruitment
- **Information bias** from unvalidated instruments or unblinded assessors
- **Attrition bias** from high dropout without intensive follow-up planning
- **Equity gaps** when populations are excluded by design or analyses don't disaggregate by race, gender, socioeconomic status

### What Standard Study Planning Often Misses:

- **Design-question fit audit:** Does this design actually answer your research question, or are you misaligning (e.g., using cross-sectional for a causal question)?
- **Explicit trade-off analysis:** Every design trades internal validity, external validity, cost, and timeline. RCTs maximize internal validity but cost $500K+; observational cohorts are cheaper but confounding risk. These trade-offs must be visible.
- **Power-driven sample sizing:** Sample size should flow from primary outcome, minimum detectable effect size, alpha/beta, variance estimates—not guessed or based on budget alone.
- **Causal DAG-informed confounding control:** Confounding is not intuition-based. Drawing a directed acyclic graph (DAG) specifies which variables must be measured and adjusted for to estimate treatment effects.
- **Systematic bias prevention by design:** Bias is best prevented through design choices (randomization, blinding, prospective exposure measurement, validated instruments) rather than post-hoc statistical adjustment.
- **Scope-appropriate protocol depth:** A simple prevalence survey doesn't need the same protocol detail as a Phase III RCT. The planner scales to research complexity.

---

## Use When

- You are **beginning a new research study** (RCT, cohort, case-control, cross-sectional, quasi-experimental)
- Your team needs to **specify the research question** in operationalized PICO/PICOS framework
- You want to **justify the study design** (why RCT vs. observational? why this population?)
- You need **sample size calculation** with documented assumptions and sensitivity analysis
- You're designing a **confounding control strategy** using causal reasoning (DAG-informed)
- You need to **systematically identify and prevent bias** (selection, information, confounding, attrition)
- You're **planning an intervention study** (RCT, quasi-experiment) and need regulatory/ethical guidance
- You want to ensure **protocol compliance** with reporting standards (CONSORT, STROBE, SPIRIT)
- You're assessing **equity dimensions** of study design (differential impacts across populations)

---

## Do Not Use When

- You are **conducting a published study review** (use research-critic to audit methodology)
- You're **planning a literature review or systematic review** (use lit-review-planner)
- You need **detailed statistical analysis code** (use sap-critic for Statistical Analysis Plan)
- You're **designing qualitative research** (use qualitative methodology frameworks)
- You're **debugging statistical software** (use code-critic)
- You're doing **post-hoc analysis of existing data** (consult biostatistician; this tool is for NEW study design)
- You're **writing a manuscript about a completed study** (use copy-critic or research-comms-critic)

---

## Why This Exists

Research design flaws are **irreversible**. Once data are collected:
- Unmeasured confounders cannot be recovered
- Underpowered studies cannot gain power retroactively
- Selection bias and biased sampling cannot be corrected
- Unvalidated measurement cannot be re-validated

Poor study design wastes years and millions in research investment and can lead to:

1. **Erroneous treatment recommendations** if internal validity is compromised (promotes ineffective/harmful interventions)
2. **Wasted research resources** if studies are underpowered or infeasible (replication failures, null findings in underpowered small studies)
3. **Missed equity insights** if populations are excluded by design or subgroup analyses are not pre-specified
4. **Regulatory rejection** of drug/device applications due to design deficiencies
5. **Replication crises** when flawed studies are published and later fail to replicate

**study-design-planner** prevents these failures by requiring explicit specification of every phase of design before data collection. A well-architected protocol ensures the study will be internally valid, ethically sound, and publishable.

---

## When to Use Each Study Design

| Design | Best For | Internal Validity | External Validity | Cost | Timeline | Feasibility |
|--------|----------|-------------------|-------------------|------|----------|-------------|
| **RCT** | Causal inference; treatment efficacy | Excellent | Often limited | High ($$$) | Long (12–36mo) | Requires equipoise, funding |
| **Prospective Cohort** | Risk factors, natural history, real-world effectiveness | Good | Good | Moderate ($$) | Long (mo–years) | Requires infrastructure for follow-up |
| **Retrospective Cohort** | Hypothesis-testing with existing data (EHR, claims, archives) | Good | Limited | Low ($) | Fast (weeks–mo) | Depends on data availability |
| **Case-Control** | Rare outcomes; efficient etiologic studies | Good | Limited | Low ($) | Fast (mo) | Good for rare disease |
| **Cross-Sectional** | Prevalence; hypothesis-generation; feasibility | Low (for causality) | High (if representative) | Low ($) | Fast (weeks–mo) | Easy to execute |
| **Quasi-Experimental** | Policy evaluation; natural experiments | Moderate | Good | Moderate ($$) | Varies | Depends on policy timeline |
| **Adaptive/Platform** | Precision medicine; rapid drug development; rare diseases | Good | Moderate | Very High ($$$) | Can be shorter | Complex; requires DSMB |

---

## Steps

1. **User provides:** Research question, study context, constraints (budget, timeline, population access, team capacity)
2. **Skill routes to:** The local catalog/meta-router selects `study-design-planner`, with a host general-purpose worker as fallback. OMC may execute the already-selected protocol only as an optional external worker.
3. **Embedded protocol executes:** Full 9-Phase Study Design Protocol (see below)
4. **Output deliverables**:
   - **Design Selection Matrix** (scoring candidate designs; justifying chosen design)
   - **PICO/PICOS Specification** (operationalized research question)
   - **Causal DAG** (directed acyclic graph showing exposure → outcome, confounders, mediators, effect modifiers)
   - **Power Analysis** (sample size calculation with assumptions, sensitivity table)
   - **Population & Sampling Protocol** (inclusion/exclusion, recruitment strategy, representativeness plan)
   - **Variable Specification Table** (all variables, measurement instruments, validation status)
   - **Temporal Architecture** (timeline, follow-up schedule, attrition planning)
   - **Bias Prevention Matrix** (all bias sources, prevention strategies, detection methods)
   - **Statistical Analysis Framework** (primary model, confounding adjustment, sensitivity analyses)
   - **Ethical & Regulatory Specification** (IRB requirements, informed consent, data governance, safety monitoring, trial registration)

---

## Full Study Design Protocol

```
═══════════════════════════════════════════════════════════════════════════════
         EPIDEMIOLOGICAL & CLINICAL STUDY DESIGN PLANNING PROTOCOL
                    9-Phase Architecture for Rigorous Research
═══════════════════════════════════════════════════════════════════════════════

PHASE 1: RESEARCH QUESTION AUDIT
──────────────────────────────────────────────────────────────────────────────

Goals:
  ✓ Extract the specific research question (not vague)
  ✓ Decompose into PICO/PICOS framework (Population, Intervention, Comparator,
    Outcome, Study type)
  ✓ Classify question type (descriptive, analytic, causal; therapy, diagnosis,
    prognosis, etiology, mechanism, equity)
  ✓ Identify design-question mismatches early

Probing Questions:
  • "What exactly are you measuring or comparing?"
    (Prevalence? Efficacy of treatment? Risk factors?)
  • "Is this causal (does X cause Y?) or associational (are X and Y related)?"
  • "Who is the population? Specific inclusion/exclusion criteria?"
  • "What is the exposure/intervention? (name, dose, duration)"
  • "What is the primary outcome? Secondary?"
  • "Timeline and budget constraints?"
  • "Equity dimensions? (Does effect differ by race, gender, SES?)"

Output:
  □ PICO/PICOS decomposition (operationalized, not vague)
  □ Question type classification (descriptive/analytic/causal)
  □ Conceptual model (exposure → outcome; known relationships)
  □ Feasibility constraints (budget, timeline, team size, population access)


PHASE 2: DESIGN SELECTION
──────────────────────────────────────────────────────────────────────────────

Goals:
  ✓ Evaluate candidate designs (RCT, prospective cohort, retrospective cohort,
    case-control, cross-sectional, quasi-experimental, adaptive)
  ✓ Score each design on internal validity, external validity, cost, timeline,
    ethical constraints, feasibility
  ✓ Recommend best-fit design
  ✓ Justify why alternatives were rejected (trade-offs explicit)

Output:
  □ Design Selection Matrix (comparing internal validity, external validity,
    cost, timeline, ethics, feasibility for each candidate)
  □ Recommended design with justification
  □ Explicit trade-offs documented (internal vs. external validity; cost vs.
    timeline; power vs. feasibility)
  □ Comparison to rejected alternatives


PHASE 3: POPULATION & SAMPLING
──────────────────────────────────────────────────────────────────────────────

Goals:
  ✓ Define target population (who findings should generalize to)
  ✓ Specify source population (who is accessible for recruitment)
  ✓ Document inclusion/exclusion criteria (operationalized)
  ✓ Describe recruitment strategy and sampling method
  ✓ Plan for representativeness assessment

Output:
  □ Population specification table (target, source, study; criteria)
  □ Sampling frame and recruitment flowchart
  □ Inclusion/exclusion criteria (operationalized; justified)
  □ Attrition prevention plan (follow-up strategies, expected retention %)
  □ Representativeness assessment plan (how will selection bias be detected?)


PHASE 4: POWER & SAMPLE SIZE
──────────────────────────────────────────────────────────────────────────────

Goals:
  ✓ Specify primary outcome and minimum detectable effect size (MDE)
  ✓ Calculate required N using alpha, beta, variance estimates
  ✓ Account for attrition, clustering, design complexity
  ✓ Provide sensitivity analysis (vary assumptions)

Output:
  □ Power Analysis Table (multiple scenarios: vary effect size, dropout, ICC)
  □ Justification of assumptions (where did effect size come from? SD estimate?)
  □ Adjusted N for attrition, clustering, unequal randomization
  □ Sensitivity analysis (how robust is N to ±20% change in assumptions?)
  □ Statement of feasibility (can this N be achieved in timeframe?)


PHASE 5: VARIABLE SPECIFICATION
──────────────────────────────────────────────────────────────────────────────

Goals:
  ✓ Define every variable (exposure, outcome, confounders, mediators, effect
    modifiers)
  ✓ Specify measurement instruments with validation status
  ✓ Draw causal DAG showing relationships
  ✓ Document operationalization rules (cutpoints, timing, definitions)

Output:
  □ Variable specification table (all variables, instruments, validity evidence)
  □ Causal DAG (Mermaid syntax; exposure → outcome; confounders, mediators,
    colliders, effect modifiers)
  □ Measurement schedule (when is each variable assessed?)
  □ Data collection forms or instrument citations


PHASE 6: TEMPORAL ARCHITECTURE
──────────────────────────────────────────────────────────────────────────────

Goals:
  ✓ Specify enrollment windows (when, how many per month?)
  ✓ Define follow-up periods (duration of contact)
  ✓ Establish measurement timepoints (when is outcome assessed?)
  ✓ Plan for attrition (differential dropout analysis, retention strategies)

Output:
  □ Timeline diagram (Gantt chart: enrollment, treatment, measurement,
    follow-up)
  □ Measurement schedule table (which variables, when?)
  □ Attrition prevention plan (phone/text reminders, flexible visits, incentives)
  □ Lag time justification (why is this follow-up duration sufficient for
    primary outcome?)


PHASE 7: BIAS PREVENTION BLUEPRINT
──────────────────────────────────────────────────────────────────────────────

Goals:
  ✓ Systematically identify all bias sources (selection, information,
    confounding, attrition)
  ✓ For each bias, specify prevention strategy (designed into protocol)
  ✓ Plan detection methods (how will residual bias be assessed?)
  ✓ Estimate residual risk (what bias remains despite prevention?)

Output:
  □ Bias Prevention Matrix (bias source, mechanism, prevention strategy,
    detection method, residual risk)
  □ Design safeguards (specific features preventing bias)
  □ Monitoring plan (how will bias be detected during study conduct?)
  □ Sensitivity analysis plan (what will be varied to test robustness?)


PHASE 8: STATISTICAL ANALYSIS FRAMEWORK
──────────────────────────────────────────────────────────────────────────────

Goals:
  ✓ Specify primary statistical model(s)
  ✓ Justify model assumptions; document assumption checking
  ✓ Pre-specify confounding adjustment approach (DAG-informed)
  ✓ Plan sensitivity analyses (robustness to assumptions)
  ✓ Pre-register all subgroup analyses
  ✓ Document missing data handling plan

Output:
  □ Primary analysis model (test, assumptions, alternative if violated)
  □ Confounding adjustment set (justified by DAG)
  □ Effect size and CI reporting standards
  □ Multiple comparison plan (primary vs. secondary; Bonferroni/FDR if needed)
  □ Subgroup strategy table (pre-specified subgroups, rationale, sample size)
  □ Missing data plan (MCAR/MAR/MNAR assumption; imputation approach)
  □ Sensitivity analysis specifications (what will be varied?)


PHASE 9: OPERATIONAL & ETHICAL SPECIFICATION
──────────────────────────────────────────────────────────────────────────────

Goals:
  ✓ Document IRB/ethics requirements and approval plan
  ✓ Specify informed consent design (what will participants be told?)
  ✓ Outline data governance (HIPAA, GDPR, data security, retention)
  ✓ Plan safety monitoring (DSMB for trials; trigger alerts for AEs)
  ✓ Define stopping rules (when might trial pause or terminate early?)
  ✓ Specify trial registration (ClinicalTrials.gov, PROSPERO)

Output:
  □ Ethical review plan (IRB/ethics committee; risk assessment)
  □ Informed consent form (draft; addresses all required elements)
  □ Data security plan (encryption, access control, retention/destruction)
  □ Safety monitoring protocol (DSMB charter if applicable; AE reporting)
  □ Stopping rules (safety, futility, efficacy; thresholds)
  □ Trial registration plan (ClinicalTrials.gov/PROSPERO; timing)
  □ Quality assurance plan (audits, re-training, protocol adherence)

```

---

## Severity Levels for Design Decisions

### HIGH-CONSEQUENCE Design Decisions

These decisions strongly affect validity and should be carefully justified:

1. **Design Choice (RCT vs. Observational vs. Other)**
   - RCT: Highest internal validity; causal inference
   - Observational: Lower internal validity; confounding risk; better external validity
   - Trade-off: Internal validity vs. feasibility/cost

2. **Sample Size & Power**
   - Underpowered studies: High Type II error; null findings non-informative; wasted investment
   - Overpowered studies: Rare; wastes resources; should still be justified

3. **Confounding Control Strategy**
   - RCT with randomization: Eliminates unmeasured confounding
   - Observational with measured adjustment: Residual confounding likely; sensitivity analysis essential
   - No confounding control in observational study: Causal claims unjustified

4. **Blinding**
   - Unblinded outcome assessment: Information bias risk; introduces bias if outcome is subjective
   - Blinded outcome assessment: Reduces bias; often not feasible for behavioral interventions

5. **Attrition Prevention**
   - High expected dropout (>20%) without intensive follow-up: Attrition bias risk
   - Intensive follow-up planned: Reduces attrition; increases cost

### MEDIUM-CONSEQUENCE Design Decisions

These affect efficiency or interpretation but not fundamental validity:

1. **Inclusion/Exclusion Criteria Stringency**
   - Very restrictive criteria: High internal validity; low external validity; harder to recruit
   - Loose criteria: More applicable; confounding risk if unmeasured confounders

2. **Measurement Instrument Choice**
   - Validated instrument: Lower measurement error; higher cost/burden
   - Non-validated: Higher measurement error; faster/cheaper

3. **Follow-up Duration**
   - Short follow-up: May miss delayed outcomes; cheaper/faster
   - Long follow-up: Captures durability; expensive; attrition risk

4. **Statistical Adjustment Method**
   - Regression adjustment: Relies on model specification; residual confounding if linear assumption violated
   - Matching/stratification: Reduces model dependence; loses some information
   - Propensity score: Balances confounders; complex; requires sufficient sample size

### LOW-CONSEQUENCE Design Decisions

These are correctable or have minimal impact:

1. **Data Collection Methods** (online vs. in-person, mail vs. phone)
   - Different cost/burden tradeoffs; can adjust during pilot

2. **Timing of Measurements** (within ±1 week of target)
   - Minor variation unlikely to change conclusions

3. **Statistical Significance Threshold** (α = 0.05 vs. 0.10)
   - Affects interpretation; doesn't change study design

---

## Scope Scaling Guidance

### Simple Descriptive Study
**Example**: Prevalence survey, needs assessment, feasibility study

**Phases required**: 1 (RQ), 2 (design choice: why cross-sectional?), 3 (sampling/representativeness), 4 (sample size for prevalence estimate)

**Phases minimal**: 5 (basic outcome definition), 6 (one-time; no follow-up)

**Phases skip**: 7 (bias prevention less critical), 8 (simple analysis: descriptive stats, proportions)

**Phase 9 (Minimal depth)**: Standard IRB/ethics review, basic informed consent, no advanced data governance beyond standard confidentiality

**Expected protocol length**: 5–10 pages

---

### Observational Cohort Study
**Example**: Risk factor study, prognostic study, real-world effectiveness

**Phases required**: All 1–9 with substantial detail

**Phases most critical**: 3 (enrollment/retention realistic?), 4 (power analysis with hazard ratios), 5 (DAG for confounding), 6 (follow-up schedule, attrition plan), 7 (confounding bias matrix), 8 (adjustment set, sensitivity analysis)

**Phase 9 (Moderate depth)**: IRB review, informed consent with follow-up contact details, data governance (HIPAA/GDPR if applicable), AE monitoring/reporting

**Expected protocol length**: 15–25 pages

---

### Randomized Controlled Trial (Phase II or Phase III)
**Example**: Drug efficacy, behavioral intervention efficacy, device comparison

**Phases required**: All 1–9, full detail

**Phases most critical**: 2 (justifying RCT over alternatives; cost/timeline feasibility), 3 (realistic recruitment for N?), 4 (power analysis accounting for attrition/clustering), 5 (blinding verification), 6 (detailed timeline, interim analyses), 7 (blinding loss detection), 8 (ITT analysis, multiple comparison adjustment)

**Phase 9 (Full depth)**: DSMB charter, stopping rules, formal SAE reporting, trial registration, detailed data security plan, comprehensive safety monitoring

**Expected protocol length**: 25–40+ pages (including SPIRIT checklist mapping)

---

### Adaptive/Platform Trial
**Example**: Umbrella trial, basket trial, platform trial

**All 9 phases required, plus**:
- Phase 4: Complex sample size accounting for interim analyses, potential arm additions/closures
- Phase 6: Interim analysis schedule (e.g., after every 50 participants)
- Phase 8: Multiple comparison adjustment (each interim inflates Type I error); response-adaptive randomization
- Phase 9: Enhanced DSMB oversight; decision rules for arm addition/closure

**Expected protocol length**: 40–60+ pages

---

## Companion Skills

- **research-critic**: Reviews a completed study design or protocol for methodological flaws. Use AFTER design is drafted to get critical peer review.
- **lit-review-planner**: Designs systematic literature review protocols. Use BEFORE study design to establish evidence base and prior effect estimates.
- **sap-critic**: Reviews detailed Statistical Analysis Plans. Use AFTER study design to ensure analysis plan matches design.
- **health-equity-analyzer**: Assesses whether study captures differential impacts across populations. Use WITH study-design-planner if equity is a study goal.
- **proposal-critic**: Reviews grant applications and research proposals. Use to ensure protocol is fundable and reviewer-ready.

---

## Standards Grounding

Study design standards applied:
- **CONSORT 2010 Statement**: Randomized controlled trial design and reporting (items 1–25 on trial design)
- **SPIRIT 2013**: Standard Protocol Items for Randomized Trials (protocol pre-registration)
- **STROBE Statement**: Observational studies in epidemiology (cohort, case-control, cross-sectional design elements)
- **EQUATOR Network**: Discipline-specific design guidelines (CARE for case reports, SRQR for qualitative, etc.)
- **ICH E6 GCP**: International Conference on Harmonisation Good Clinical Practice (trials with drugs/devices)
- **GRADE Framework**: Grading of Recommendations, Assessment, Development, and Evaluation (evidence quality assessment)
- **NIH Design Guidance**: NIH review standards for study design rigor (study design section of grant applications)

---

## Examples

### Example 1: RCT Design (GOOD)

**Question**: Does 12-week cognitive-behavioral therapy reduce anxiety in adults with GAD?

**Design Selected**: RCT (2-arm, 1:1 randomization, CBT vs. waitlist control)
- **Rationale**: Causal question; RCT provides strongest evidence; waitlist ethical (known benefit of CBT)
- **Trade-off**: Cost $500K, timeline 18 months vs. cheaper observational cohort, but internal validity premium justified

**Population**: Adults 18–75 with GAD (DSM-5 diagnostic criteria)
- **N = 180** (90 per group, accounting for 15% attrition)
- **Power analysis**: Effect size d = 0.65 (mid-range of prior RCTs); alpha = 0.05, power = 80%

**Primary Outcome**: GAD-7 score at 12 weeks (validated 7-item scale; blind outcome assessor)

**Bias Prevention**:
- **Selection**: Consecutive eligible patients from clinic lists (not volunteers)
- **Information**: Outcome assessor blind to assignment; validated instrument
- **Confounding**: Pre-specified adjustment for baseline severity, medication use (DAG-informed)
- **Attrition**: Intensive follow-up; $50 incentive; intent-to-treat analysis planned

**Verdict**: GOOD. Design-question fit clear; power justified; bias prevention in place; ethical protections outlined.

---

### Example 2: Cohort Study Design (GOOD)

**Question**: Does statin use reduce CVD mortality in adults with dyslipidemia?

**Design Selected**: Prospective cohort (not RCT; randomization infeasible; real-world effectiveness)

**Population**: 3,000 adults age 40–75 with dyslipidemia (LDL > 100); follow-up 10 years

**Power Analysis**:
- Primary outcome: CVD mortality; expected HR = 0.5 (50% hazard reduction)
- Events needed: ~150; achievable with 3,000 participants

**Confounding Control** (DAG-informed):
- Measure at baseline: Age, sex, LDL, blood pressure, smoking, BMI, diabetes
- Adjust for all in primary analysis
- Sensitivity analysis: E-value for unmeasured confounding by indication

**Bias Prevention**:
- **Selection**: Consecutive clinic patients; document non-enrollment
- **Information**: LDL from lab (objective); statin use from pharmacy records; mortality from death certificates
- **Confounding**: Pre-specified adjustment set from DAG; sensitivity analysis for unmeasured confounding
- **Attrition**: Target <5% loss to follow-up via intensive contact

**Verdict**: GOOD. Prospective design addresses temporal direction; confounding control specified; real-world effectiveness; ethical protections in place.

---

### Example 3: Poorly-Designed Study (BAD)

**Question**: Do dietary antioxidants prevent cancer?

**Design**: Cross-sectional online survey of 1,000 adults

**Problems**:

1. **Design-Question Mismatch** (CRITICAL): Cross-sectional cannot answer causal question; no temporal direction; reverse causality possible (cancer → dietary change)

2. **Selection Bias** (CRITICAL): Online survey non-representative; self-selected respondents; no comparison to source population

3. **Information Bias** (MAJOR): Antioxidant intake self-report (not validated); cancer history self-report (misclassification)

4. **Unmeasured Confounding** (MAJOR): Smoking not adjusted; SES not adjusted; no DAG; no sensitivity analysis

5. **No Sample Size Justification** (MAJOR): N = 1,000 arbitrary; no power analysis

6. **No Protocol Registration** (MAJOR): Likely p-hacking; selective outcome reporting

**Verdict**: REJECT. Fundamental design-question mismatch; unmeasured confounding; selection bias; no temporal direction. Would require prospective cohort or RCT for causal inference.

---

## Benchmark Test Info

```
Tested on internal design scenarios across RCT, cohort, case-control, cross-sectional, and quasi-experimental designs. Peer review recommended for all production study protocols. Systematic benchmarking with published methodology pending.
```

---

## Notes

- **Scope boundary**: This skill DESIGNS studies. It does not execute studies, conduct analysis, debug code, or review published studies (those are separate skills).
- **Feasibility reality check**: If calculated sample size is N = 5,000 but team can recruit 50/month = 100 months = 8+ years, the design is infeasible. Recommend adaptations: smaller effect size? different design? multi-site collaboration?
- **Turnaround**: Budget 30–60 minutes for simple descriptive study; 2–3 hours for observational cohort; 4–6 hours for Phase III RCT. Deep engagement required.
- **Protocol documentation**: Output is a detailed protocol (20–40+ pages depending on complexity). This protocol becomes the roadmap for study conduct and the basis for grant applications, IRB submissions, and protocol publications.
- **Follow-up**: After design is approved, pair with **sap-critic** to review the Statistical Analysis Plan (detailed analysis code, model specification, sensitivity analyses).

---

## Key Principles at a Glance

| Principle | Why It Matters | How We Implement It |
|-----------|----------------|-------------------|
| **Design-Question Fit** | Wrong design = wrong answer | Phase 2 explicitly evaluates design choice vs. research question |
| **Power-Driven Sizing** | Underpowered studies = wasted resources | Phase 4: justify N from primary outcome, MDE, alpha/beta, variance |
| **DAG-Informed Confounding** | Intuition-based confounding control fails | Phase 5: draw causal diagram; Phase 8: specify adjustment set from DAG |
| **Bias Prevention by Design** | Design prevents bias better than statistics | Phase 7: systematic matrix of bias sources + prevention strategies |
| **Explicit Trade-Offs** | Every design trades validity vs. cost/time | Phase 2: comparison matrix showing cost, timeline, validity for each design |
| **Scope-Appropriate Detail** | Over-specification wastes effort | Scale protocol depth to study complexity (simple ≠ Phase III RCT) |
| **Ethical Protections First** | Ethics is not afterthought | Phase 9: IRB, consent, data governance, safety monitoring |
| **Reproducibility & Transparency** | Future researchers must understand decisions | Document all assumptions, trade-offs, alternatives considered |
