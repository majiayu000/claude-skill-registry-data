---
name: lit-review-planner
description: "Plan literature reviews — search protocol, inclusion criteria, synthesis methodology."
version: 1.0.0
author: Zivtech
---

# lit-review-planner

**Companion to**: research-critic, health-equity-analyzer
**Best with**: Teams planning SRs, scoping reviews, rapid reviews, or meta-analyses
**Entry point**: `/lit-review-planner`

## JTBD (Jobs To Be Done)

### Primary Job
When I need to conduct a systematic review or evidence synthesis and cannot afford to have my search strategy challenged as cherry-picked or my protocol dismissed as ad hoc,
I want a rigorous review protocol designed before any searching begins,
so I can produce a PRISMA-compliant, reproducible review that survives peer scrutiny and isn't overturned because the inclusion criteria drifted mid-review.

### Secondary Jobs
- When a team is debating review type — systematic vs. scoping vs. rapid — and the tradeoffs between rigor, timeline, and available databases are unresolved, I want those decisions made explicit upfront, so we don't redesign the protocol after screening has already started.
- When a prior review attempt was flagged for incomplete search coverage or missing grey literature, I want a remediation protocol that fixes the structural gaps, so the revised review isn't dismissed for the same reasons.

### Job Layers
- Functional: Produce a PICO/PICOS framework, database selection matrix, Boolean search strings, screening protocol with inter-rater reliability targets, risk-of-bias tool selection, and synthesis approach — all specified before the first database search runs.
- Emotional: Reduce the anxiety that your review will be dismissed as biased or incomplete because the protocol wasn't rigorous — the fear that missing 40% of relevant evidence in specialized databases will surface only after months of work.
- Social: Helps the user register a defensible protocol on PROSPERO or OSF before screening, so the review is credible to journal editors, guideline bodies, and policy audiences who scrutinize search methodology.

### This Skill Is For
- A researcher beginning a systematic, scoping, or rapid review who needs a complete protocol before the first database search — not a partial checklist to fill in later.
- A team that has a research question but hasn't yet specified PICO, database coverage, screening criteria, or quality assessment tools, and knows that starting without these leads to scope creep and biased evidence synthesis.
- A reviewer whose previous protocol was rejected or required major revision due to incomplete search strategy or undefined inclusion/exclusion criteria.

### This Skill Is NOT For
- A user with a completed or in-progress review who needs a quality verdict on what was done; use `research-critic` instead.
- A user who wants quick guidance on which papers to read, with no intent to run a replicable, documented review protocol.

### Paired With
- `research-critic`: After the review is conducted and synthesized, use it to audit the result for methodology gaps and interpretive overreach.
- `manuscript-planner`: Use this when the review is complete and the unresolved problem is how to structure the synthesis manuscript for submission.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has a research question but no protocol | The skill builds PICO framework, database matrix, search strings, and screening criteria | A PROSPERO/OSF-registerable protocol |
| Team disagrees on review type or scope | The skill scores SR vs. scoping vs. rapid on rigor, timeline, and feasibility | A documented design decision with tradeoffs |
| Prior review was rejected for incomplete coverage | The skill identifies the structural gaps and rebuilds the search and screening protocol | A remediation plan addressing the specific rejection reasons |

### When to Escalate
- If the user already has a completed review and needs a verdict on its quality, escalate to `research-critic`.
- If the user's primary problem is structuring the synthesis manuscript rather than designing the review protocol, escalate to `manuscript-planner`.

## Purpose

Conducting a systematic literature review requires rigorous design before the search begins. Yet many research teams start searching without a clear PICO framework, database strategy, or quality assessment plan—leading to incomplete evidence synthesis, missed studies, and unreplicable results.

The lit-review-planner guides researchers through **structured protocol development** for five evidence synthesis methodologies:
- **Systematic Reviews** (PRISMA-compliant, gold standard)
- **Scoping Reviews** (PRISMA-ScR, mapping the landscape)
- **Rapid Reviews** (abbreviated systematic reviews for timely evidence)
- **Narrative Reviews** (structured narrative synthesis with transparency)
- **Meta-Analysis Planning** (quantitative synthesis design before extraction)

This skill operationalizes best practices from the Cochrane Collaboration, PRISMA Statement, and JBI guidance to ensure your review is reproducible, comprehensive, and defensible.

## Use When

- You are beginning a **systematic review, scoping review, or evidence synthesis**
- Your team needs to **design search strategies** mapped to PICO/PICOS elements
- You're **planning quality assessment** and risk of bias evaluation
- You need to **specify inclusion/exclusion criteria** with operational definitions
- You're designing a **meta-analysis protocol** with heterogeneity and subgroup plans
- You want to ensure **PRISMA checklist compliance** from the start
- You're conducting an **equity-focused review** and need PROGRESS-Plus framework integration

## Do Not Use When

- You are **conducting screening or data extraction** (use research-critic for quality assessment)
- You already have a published protocol and need **implementation support** (use protocol-executor)
- You're writing a **finished review manuscript** (use review-writer for synthesis narrative)
- You need **statistical analysis guidance** (consult a statistician; this is planning architecture)

## Why This Exists

Literature reviews without clear planning frameworks often fail because:

1. **Incomplete PICO specification**: Questions formulated ad-hoc lead to drifting inclusion criteria mid-review
2. **Database selection without justification**: Teams use PubMed only, missing 40% of relevant evidence in specialized databases (CINAHL for nursing, PsycINFO for psychology)
3. **Search strategies unmapped to concepts**: Boolean operators applied without MeSH term mapping, reducing sensitivity and precision
4. **No quality assessment plan**: Teams choose risk-of-bias tools after seeing studies, introducing bias
5. **Missing grey literature strategy**: Unpublished studies and dissertations account for 30–40% of evidence in many topics
6. **Unplanned synthesis approach**: Teams discover too late that their heterogeneous data can't be meta-analyzed
7. **Equity gaps unidentified**: Reviews often miss barriers, harms, and impacts on marginalized populations

This skill **prevents** these failures by requiring explicit specification of every phase before search begins.

## When to Use Each Review Type

| Review Type | When | Effort | Timeline |
|-------------|------|--------|----------|
| **Systematic Review** | Answer a focused clinical/policy question; high-stakes decision required | 18–36 months | Years |
| **Scoping Review** | Map evidence landscape; identify research gaps; clarify concepts | 9–18 months | 6–12 months |
| **Rapid Review** | Need evidence in 3–6 months (policy deadline, urgent decision) | 3–6 months | Weeks to months |
| **Narrative Review** | Discuss state of knowledge; not a primary evidence synthesis | 6–12 months | Months |
| **Meta-Analysis** | Combine quantitative results from homogeneous RCTs/cohort studies | Embedded in SR | Months (after SR complete) |

## Steps

1. **Confirm review type** and scope with your team
2. **Invoke the planner**: `/lit-review-planner "Your research question or topic area"`
3. **Work through the 5-phase protocol** with the planning subagent
4. **Output deliverables**:
   - PICO/PICOS/PCC framework document
   - Search strategy with Boolean strings for each database
   - Screening and selection protocol with operational criteria
   - Data extraction form template
   - Risk of bias tool selection with justification
   - Synthesis and reporting plan (PRISMA checklist mapping)
   - Equity assessment framework if applicable
5. **Register your protocol** (PROSPERO for SRs; OSF for scoping reviews) before screening begins

## Full Lit Review Planning Protocol

```
═══════════════════════════════════════════════════════════════════════════════
               SYSTEMATIC LITERATURE REVIEW PLANNING PROTOCOL
                    5-Phase Evidence Synthesis Architecture
═══════════════════════════════════════════════════════════════════════════════

PHASE 1: RESEARCH QUESTION & FRAMEWORK DEFINITION
──────────────────────────────────────────────────────────────────────────────

1.1 RESEARCH QUESTION FORMULATION
   □ Narrative question (plain language)
     Example: "What is the effectiveness of cognitive-behavioral therapy for
               adults with generalized anxiety disorder?"

   □ PICO/PICOS framework decomposition:
     • Population: Adults (≥18 years) with diagnosed GAD (DSM-5 or ICD-11)
     • Intervention: CBT delivered in-person or remotely
     • Comparison: Usual care, waitlist, placebo, or alternative psychotherapy
     • Outcome (primary): Symptom severity (GAD-7 scale, HAMA, clinical response)
     • Outcome (secondary): Remission rates, quality of life, dropout rates,
       adverse events, durability at follow-up
     • Study type: RCTs (Level 1 evidence priority), then cohort studies if RCTs
                   insufficient

   □ For SCOPING REVIEWS, use PCC framework instead:
     • Population: Adults with any anxiety disorder
     • Concept: Digital delivery of psychotherapy
     • Context: Low- and middle-income countries

   □ Question type classification (determines search strategy intensity):
     ○ Therapy: What is effective for treating condition X?
     ○ Diagnosis: What test/tool best diagnoses condition X?
     ○ Prognosis: What predicts outcomes in patients with X?
     ○ Etiology/Risk: What causes or increases risk of X?
     ○ Qualitative: What are patients' experiences with X?
     ○ Health equity: How do barriers/benefits differ across populations for X?

1.2 INCLUSION/EXCLUSION CRITERIA SPECIFICATION
   Define with operational precision (not subjective language):

   INCLUSION:
   ✓ Publication type: Peer-reviewed journal articles (define year range)
   ✓ Language: English, Spanish, Mandarin (state all languages team can review)
   ✓ Study design: RCTs (Phase 1 evidence), then quasi-experimental if insufficient
   ✓ Population: Adults ≥18 years; N ≥20 per group minimum
   ✓ Intervention specificity: Named therapy protocols (e.g., "CBT for anxiety"
     not "therapy")
   ✓ Outcome measurement: Validated instruments (e.g., GAD-7, HAMA, diagnostic
     interview)
   ✓ Data availability: Full-text must report effect size or raw data for calculation

   EXCLUSION:
   ✗ Studies involving children or adolescents (unless age-disaggregated data)
   ✗ Comorbid diagnoses only (substance use disorder as primary condition)
   ✗ Editorials, opinion pieces, case reports, uncontrolled case series
   ✗ Studies with >30% attrition without intent-to-treat analysis
   ✗ Published in non-peer-reviewed format (dissertations, conference abstracts
     without full publication)
   ✗ Non-English languages (state reason if applicable)

1.3 PROTOCOL REGISTRATION REQUIREMENT
   □ Systematic Review: Register on PROSPERO (prospero.crd.york.ac.uk)
     – Prevents selective outcome reporting
     – Publicly signals your review to avoid duplication

   □ Scoping Review: Register on Open Science Framework (osf.io)
     – Smaller fee; similar transparency benefit

   □ Record registration date and number for later reference in manuscript


PHASE 2: SEARCH STRATEGY DESIGN
──────────────────────────────────────────────────────────────────────────────

2.1 DATABASE SELECTION WITH COVERAGE JUSTIFICATION

   Primary databases (required):
   ☐ MEDLINE/PubMed
     Justification: Covers 23M citations; includes grey literature (PUBMED CENTRAL)
     Limitation: Indexed with 6-month lag; poor coverage of social sciences

   ☐ Cochrane CENTRAL (Central Register of Controlled Trials)
     Justification: Hand-searched journals; controlled trials flagged
     Cost: Free via institutional subscription or public access
     Limitation: Therapy evidence only; not for etiology

   Secondary databases (discipline-dependent):
   ☐ CINAHL (Cumulative Index to Nursing and Allied Health)
     When: Nursing, allied health, public health questions
     Advantage: Better nursing research coverage than MEDLINE alone

   ☐ PsycINFO (American Psychological Association)
     When: Psychology, mental health, behavioral interventions
     Advantage: 4M+ records; covers dissertations and grey literature

   ☐ Scopus or Web of Science
     When: Interdisciplinary topics; citation tracking capability
     Cost: Subscription required; verify institutional access

   ☐ EMBASE (Excerpta Medica)
     When: Pharmacology, drug efficacy, adverse events
     Advantage: Better European and non-English publication coverage
     Cost: Subscription; consider if budget allows

   Grey literature sources:
   □ ProQuest Dissertations & Theses (US/Canada academic theses)
   □ OpenGrey (European grey literature repository)
   □ Government reports (NIH, CDC, AHRQ, Health Canada, NHS, WHO)
   □ Conference proceedings (manually search: American Psychological Assoc,
     International Society of Behavioral Medicine, etc.)
   □ Clinical trial registries: ClinicalTrials.gov, WHO ICTRP
   □ Author contact for unpublished/in-press work (relevant for recent research)

2.2 SEARCH TERM DEVELOPMENT & MeSH MAPPING

   Step 1: Extract keywords from PICO
   Population: Adult, Anxiety Disorder, Generalized Anxiety
   Intervention: Cognitive Behavioral Therapy, Psychotherapy, Behavioral
   Comparison: Usual Care, Waitlist, Placebo
   Outcome: Symptom Severity, Efficacy, Effectiveness

   Step 2: Identify controlled vocabulary (MeSH for MEDLINE)
   PubMed MeSH Browser (meshb.nlm.nih.gov):
   • "Generalized Anxiety Disorder" (MeSH Heading)
   • "Cognitive Therapy" (MeSH Heading)
   • "Psychotherapy, Brief" (MeSH Heading - includes CBT)
   • "Treatment Outcome" (MeSH Heading)

   PsycINFO Thesaurus (for psychology databases):
   • "Anxiety Disorders"
   • "Cognitive Behavior Therapy"
   • "Psychotherapy Effectiveness"

   Step 3: Build search strings with Boolean operators

   PUBMED/MEDLINE STRING:
   ("Generalized Anxiety Disorder"[MeSH] OR "anxiety disorder*"[Title/Abstract])
   AND
   ("Cognitive Therapy"[MeSH] OR "cognitive behavior* therap*"[Title/Abstract]
    OR CBT[Title/Abstract])
   AND
   ("Randomized Controlled Trial"[MeSH] OR "Controlled Clinical Trial"[MeSH]
    OR RCT[Title/Abstract])
   NOT
   (child* OR adolescent* OR pediatric*)

   PSYCINFO STRING:
   (DE "Generalized Anxiety Disorder" OR TI "anxiety disorder*")
   AND
   (DE "Cognitive Behavior Therapy" OR TI "CBT" OR AB "cognitive behavior* therap*")
   AND
   (DE "Outcome and Process" OR TI "randomized controlled trial*")

   SCOPUS STRING:
   TITLE-ABS-KEY(("generalized anxiety disorder" OR "anxiety disorder*")
   AND ("cognitive behavior* therap*" OR CBT)
   AND (RCT OR "randomized controlled trial*"))

   COCHRANE CENTRAL STRING:
   [MeSH descriptor: Generalized Anxiety Disorder] OR "anxiety disorder*"
   [MeSH descriptor: Cognitive Therapy]

2.3 SEARCH EXECUTION & DOCUMENTATION
   For each database:
   ☐ Search date(s)
   ☐ Exact search string (copy-paste from database)
   ☐ Filters applied (date range, language, publication type)
   ☐ Number of results returned
   ☐ Number of duplicates identified across databases

   Example table:
   | Database  | Date Searched | Search String | Filters      | Results | Duplicates |
   |-----------|---------------|---------------|--------------|---------|------------|
   | MEDLINE   | 2025-03-09    | [string]      | 2015–present | 2,847   | 1,203      |
   | Cochrane  | 2025-03-09    | [string]      | None         | 487     | 389        |
   | PsycINFO  | 2025-03-09    | [string]      | 2015–present | 1,654   | 856        |

2.4 HAND-SEARCHING & CITATION TRACKING
   Hand-search strategy (for in-person/virtual journal browsing):
   ☐ Journal selection: Identify 5–10 key journals in field
     Examples for anxiety: JAMA Psychiatry, American Journal of Psychiatry,
                          Behavior Therapy & Experimental Psychiatry
   ☐ Timeframe: Last 3 years (or per PRISMA guidelines)
   ☐ Assignment: Assign journals to reviewers; document dates searched

   Citation tracking:
   ☐ Forward citation tracking: Use Scopus/Web of Science to find papers citing
     included studies
   ☐ Backward citation tracking: Review reference lists of included studies and
     relevant systematic reviews
   ☐ Tool: Covidence, Rayyan, or manual spreadsheet to track


PHASE 3: SCREENING & SELECTION PROTOCOL
──────────────────────────────────────────────────────────────────────────────

3.1 TITLE & ABSTRACT SCREENING

   Operational criteria (must be mutually exclusive and exhaustive):

   INCLUDE:
   • Study evaluates CBT (or named therapy protocol) for adults with GAD
   • Outcome includes validated symptom measure (GAD-7, HAMA, diagnostic interview)
   • Study design: RCT or quasi-experimental

   EXCLUDE:
   • Population is primarily children or adolescents
   • Intervention is not CBT (e.g., supportive counseling, mindfulness-only)
   • No comparison group reported
   • Full text unavailable; author contact unsuccessful
   • Conference abstract without subsequent publication

   Ambiguous criteria (trigger full-text review):
   "Effective treatment for anxiety" (may or may not be GAD)
   "Brief intervention" (may or may not be CBT)

3.2 FULL-TEXT SCREENING

   Apply inclusion/exclusion criteria with specificity:

   INCLUDE JUDGMENT:
   Study reports: Adults (age ≥18), GAD diagnosis (DSM-5 criteria or clinical
   interview), CBT intervention, RCT design, ≥1 validated outcome measure

   EXCLUDE JUDGMENT & REASON:
   ✗ Age: Mean age 15 years (protocol specifies adults only)
   ✗ Diagnosis: "Anxiety symptoms" (not GAD; per exclusion criteria)
   ✗ Intervention: Group CBT combined with medication (not pure CBT; per protocol)
   ✗ Design: Uncontrolled case series (not RCT; per protocol)
   ✗ Data: Effect size not reportable from presented statistics (per inclusion criterion)

3.3 DUAL REVIEW & CONFLICT RESOLUTION

   All titles/abstracts and full texts reviewed independently by TWO reviewers
   ☐ Assign reviewer pairs to avoid conflicts of interest (no author reviews their
     own work)
   ☐ Use Covidence, DistillerSR, or Rayyan for dual-review workflow
   ☐ Calculate inter-rater reliability (Cohen's kappa) for each phase:
     • ≥0.80: Excellent agreement; minor disagreements resolved by discussion
     • 0.60–0.79: Moderate agreement; third reviewer adjudicates disputes
     • <0.60: Poor agreement; re-train reviewers on criteria; re-screen

   Conflict resolution process:
   ✓ If disagreement on title/abstract: Reviewers discuss; both unsure = INCLUDE
     in full-text review (lower threshold)
   ✓ If disagreement on full text: Third reviewer (senior team member) adjudicates
   ✓ Document reason for each exclusion in PRISMA flow diagram

3.4 PRISMA FLOW DIAGRAM PLANNING
   Structure (mandatory reporting):

   Records identified via database (n = __)
     └─ MEDLINE (n = __); Cochrane (n = __); PsycINFO (n = __)
     └─ Grey literature (n = __)
   │
   Duplicates removed (n = __)
   │
   Records screened (n = __)
   │
   Records excluded (n = __)
   │
   Full texts assessed (n = __)
   │
   Full texts excluded (n = __) with reasons (e.g., wrong population, no outcome data)
   │
   Studies included in review (n = __)


PHASE 4: QUALITY ASSESSMENT & DATA EXTRACTION
──────────────────────────────────────────────────────────────────────────────

4.1 RISK OF BIAS TOOL SELECTION

   Match tool to study design:

   ☐ RCTs → Cochrane Risk of Bias 2 (RoB2)
     Dimensions: Selection, performance, detection, attrition, reporting bias
     Output: Low / Some Concerns / High Risk for each domain

   ☐ Quasi-experimental/observational → ROBINS-I (Risk of Bias In Non-randomized
     Studies of Interventions)
     Includes: Confounding, selection, classification, deviations, missing data,
     measurement, reporting

   ☐ Cohort studies → Newcastle-Ottawa Scale
     Simpler scoring; points for selection, comparability, outcome assessment

   ☐ Qualitative studies → CASP Qualitative Checklist
     Dimensions: Aims clarity, methodology, design, recruitment, data collection,
     analyst-participant relationship, ethics, analysis rigor, statement of findings,
     research value

   ☐ Cross-sectional studies → JBI Critical Appraisal Tool for Cross-Sectional Studies

   Rationale for choice:
   "We selected RoB2 because all included studies are RCTs, and RoB2 aligns with
    PRISMA 2020 recommendations for transparent bias assessment across randomization,
    blinding, and outcome reporting. This tool also allows stratified analysis by
    risk-of-bias domain."

4.2 DATA EXTRACTION FORM DESIGN

   Template structure (pilot test on 5 studies first):

   STUDY IDENTIFIERS:
   • Author(s), year, country
   • Journal, publication type (peer-reviewed journal, preprint, dissertation)
   • Language of publication
   • Study registration (ClinicalTrials.gov ID, PROSPERO ID)

   POPULATION:
   • Sample size (n randomized, n analyzed)
   • Age: Mean (SD), range
   • Sex: % female
   • GAD criteria: DSM-5, ICD-11, clinical interview
   • Comorbidities: Depression (%), PTSD (%), substance use (%)
   • Baseline severity: Mean GAD-7 or HAMA score
   • Setting: Primary care, specialty clinic, online, other
   • Country and income level (high-, middle-, low-income)

   INTERVENTION:
   • Therapy name: Cognitive Behavioral Therapy for Anxiety
   • Format: In-person, telehealth, self-guided with coach
   • Duration: # weeks, frequency (weekly, bi-weekly)
   • Session length: minutes per session
   • Total contact hours
   • Therapist type: PhD psychologist, MSW social worker, trained paraprofessional
   • Fidelity monitoring: Yes/No; tool used (if yes)
   • Adherence rates: % of sessions attended; range across participants

   COMPARISON INTERVENTION:
   • Type: Usual care, waitlist, placebo, alternative therapy
   • Details: Specific comparator therapy (if applicable)

   PRIMARY OUTCOMES (all validated instruments):
   • Instrument: GAD-7, HAMA, Structured Clinical Interview for DSM-5
   • Timepoint: Post-treatment (weeks), follow-up (6 mo, 12 mo)
   • Mean (SD) or % improvement; Group 1 vs Group 2
   • Effect size: Cohen's d, odds ratio, risk ratio with 95% CI
   • Statistical significance: p-value

   SECONDARY OUTCOMES:
   • Remission rates: % achieving GAD remission (GAD-7 <5)
   • Quality of life measures (SF-12, EQ-5D)
   • Dropout rates: # withdrawn from treatment; reasons
   • Adverse events: # participants with serious adverse events; types
   • Durability: Outcomes at long-term follow-up (≥6 months post-treatment)

   FUNDING & CONFLICTS OF INTEREST:
   • Funding source: Government, nonprofit, industry, self-funded, not reported
   • Author COI statement: Present/absent
   • If present: Financial interests, employment relationships

   QUALITY ASSESSMENT:
   • RoB2 domain ratings (applied during extraction)
   • Justification for each domain rating (direct quote from methods, results,
     limitations)

4.3 DATA EXTRACTION PROCESS
   ☐ Dual extraction for all studies (or risk-aversion approach: 100% single
     extraction + 25% verification by second reviewer)
   ☐ Discrepancy resolution: Consensus discussion; escalate to senior reviewer if
     disagreement persists
   ☐ Missing data: Contact authors for unreported effect sizes, SDs, n values
   ☐ Document all attempts to contact authors (date, method, response/non-response)

4.4 META-ANALYSIS PLANNING (if applicable)

   Heterogeneity assessment strategy:
   □ Statistical heterogeneity (I² statistic):
     • I² <25%: Low heterogeneity → Fixed-effects model appropriate
     • I² 25%–75%: Moderate heterogeneity → Random-effects model
     • I² >75%: High heterogeneity → Meta-analysis not advised; narrative synthesis
       instead
   □ Cochran Q test (p < 0.05 suggests heterogeneity)
   □ Visual inspection: Forest plot for magnitude/direction of effect consistency

   Subgroup analysis planning (pre-specify to prevent p-hacking):
   □ Participant subgroups: Age (≥50 vs <50), sex, comorbidity (depression
     present vs absent)
   □ Intervention subgroups: In-person vs telehealth; therapist type (PhD vs trained
     paraprofessional)
   □ Study-level subgroups: Study risk of bias (low vs high); country income level

   Sensitivity analysis:
   □ Removing outlier studies with extreme effect sizes
   □ Removing high risk-of-bias studies; comparing to all-studies analysis
   □ Removing studies with missing data; comparing completers-only vs intention-to-treat

   Publication bias assessment:
   □ Funnel plot (plot effect size vs SE): Asymmetry suggests bias
   □ Egger's regression test (p < 0.05 suggests bias)
   □ Trim-and-fill method (estimates number of missing studies)
   □ Interpretation: Small-study effects may also indicate real subgroup heterogeneity

   Software: RevMan (Cochrane), Comprehensive Meta-Analysis, R packages (metafor,
   meta)


PHASE 5: SYNTHESIS & REPORTING PLAN
──────────────────────────────────────────────────────────────────────────────

5.1 NARRATIVE SYNTHESIS FRAMEWORK (for heterogeneous studies)

   When to use: Studies differ in population, intervention, design, or outcomes
   (prevents meta-analysis)

   Structure:
   ☐ Tabulation: Present all included studies in evidence table with key
     characteristics, outcomes, quality
   ☐ Narrative description: Discuss findings by outcome (efficacy, safety,
     subgroup results); describe range and direction of effects
   ☐ Thematic synthesis: Identify common themes in mechanisms, patient experiences,
     barriers (especially from qualitative studies)
   ☐ Grade of evidence: Assess overall quality using GRADE approach (see 5.3)
   ☐ Limitations: Acknowledge gaps, inconsistencies, bias; discuss implications

5.2 META-ANALYTIC SYNTHESIS (for homogeneous quantitative outcomes)

   Output structure:
   □ Summary effect size: Overall Cohen's d or OR with 95% CI
   □ Interpretation: "CBT is moderately effective for GAD with effect size d = 0.78
     (95% CI 0.65–0.91), representing improvement from moderate to mild anxiety"
   □ Forest plot: Visualize individual study effects and overall effect
   □ Heterogeneity statement: "I² = 42% (moderate heterogeneity); results relatively
     consistent across studies"
   □ Subgroup findings: Effect size by intervention modality, therapist type,
     follow-up duration
   □ Sensitivity analysis results: Effect direction/magnitude stable when removing
     high-bias studies?

5.3 GRADE EVIDENCE QUALITY ASSESSMENT

   Rate overall evidence quality for each outcome:

   ☐ HIGH: Further research unlikely to change effect estimate
     Criteria: ≥3 RCTs, large sample, low heterogeneity, low risk of bias,
     precise estimates

   ☐ MODERATE: Further research may change effect estimate
     Criteria: RCTs with some limitations OR very large observational studies

   ☐ LOW: Further research very likely to change estimate
     Criteria: <3 RCTs, small sample, high heterogeneity, high risk of bias

   ☐ VERY LOW: Very uncertain about effect
     Criteria: Observational studies only OR RCTs with very serious limitations

   Downgrade criteria:
   • Risk of bias: Downgrade 1 level if >25% of evidence from high-bias studies;
     2 levels if >50%
   • Inconsistency: Downgrade if I² >50% and confidence intervals don't overlap
   • Indirectness: Downgrade if population, intervention, outcomes differ from
     question
   • Imprecision: Downgrade if wide CI crosses null effect or MID (minimal important
     difference)
   • Publication bias: Downgrade if funnel plot asymmetry or Egger p < 0.05

   Output: GRADE Summary of Findings table showing outcome, # studies/participants,
   effect, quality rating, interpretation

5.4 HEALTH EQUITY ASSESSMENT (PROGRESS-Plus Framework)

   For equity-focused reviews, assess differential impacts across:

   PLACE: Urban vs rural; country income level; healthcare access
   • Search question: Do CBT benefits differ for rural vs urban populations?
   • Data extraction: Stratify outcomes by geography/setting
   • Analysis: Compare effect sizes across locations

   RACE/ETHNICITY: Racial/ethnic minority populations
   • Search question: Is CBT effective for anxiety in racial/ethnic minorities?
   • Data extraction: % participants by race/ethnicity; disaggregate outcomes
   • Analysis: Examine subgroup effects by race/ethnicity

   OCCUPATION: Employment type, occupational exposures
   • Search question: Do workplace-related anxiety interventions differ from
     clinical CBT?
   • Data extraction: Occupational characteristics; outcome differences

   GENDER: Sex, gender identity, sexual orientation
   • Data extraction: % female; % transgender/non-binary (if reported)
   • Analysis: Compare outcomes by sex; note gender-specific anxiety manifestations

   RELIGION: Religious affiliation, spiritual practices
   • Data extraction: Religiously-tailored vs standard CBT
   • Analysis: Subgroup effect by religious adaptation

   EDUCATION: Educational attainment, literacy
   • Data extraction: Mean years of education; literacy level of intervention materials
   • Analysis: Compare outcomes across education levels

   SOCIOECONOMIC STATUS: Income, asset ownership, employment status
   • Data extraction: % low-income; employment status; cost barriers
   • Analysis: Effectiveness in low-income populations

   SOCIAL CAPITAL: Marital status, family support, social networks
   • Data extraction: Marital status; family support available; social isolation
   • Analysis: Outcomes in socially isolated vs supported populations

   OTHER (age, disability, migration status, incarceration status)

   Equity synthesis output:
   ☐ Table: Outcomes disaggregated by PROGRESS-Plus factor
   ☐ Narrative: Identified harms/barriers for marginalized groups
   ☐ Recommendations: How to deliver more equitable interventions

5.5 PRISMA 2020 CHECKLIST COMPLIANCE MAPPING

   Map your protocol to PRISMA items:

   □ TITLE: Systematic review of CBT for GAD (includes "systematic review")
   □ ABSTRACT: Structured abstract with Background, Objectives, Methods, Results,
     Conclusions (2500 words max)
   □ INTRODUCTION: Rationale (why review matters), objectives
   □ METHODS:
     ✓ Protocol registration (PROSPERO ID and date)
     ✓ Eligibility criteria (PICO)
     ✓ Information sources (databases, hand-search, grey literature)
     ✓ Search strategy (full strings provided)
     ✓ Study selection process (title/abstract/full-text; dual review;
       inter-rater reliability)
     ✓ Data extraction (form design; dual extraction; missing data)
     ✓ Risk of bias assessment (tool, timing, dual review)
     ✓ Effect measures (Cohen's d, odds ratio, etc.)
     ✓ Synthesis methods (meta-analysis, subgroup analysis, sensitivity analysis,
       narrative synthesis)
     ✓ Reporting bias assessment (funnel plot, Egger test)
   □ RESULTS:
     ✓ PRISMA flow diagram (4 phases: identification, screening, eligibility,
       inclusion)
     ✓ Study characteristics table
     ✓ Risk of bias summary
     ✓ Results (effect sizes, forest plots, meta-analysis, subgroup results)
     ✓ Summary of findings table (GRADE quality ratings)
   □ DISCUSSION:
     ✓ Summary of evidence
     ✓ Interpretation
     ✓ Limitations (publication bias, heterogeneity, quality)
     ✓ Implications for practice and research
   □ FUNDING & COI disclosure


EVIDENCE QUALITY STANDARDS
────────────────────────────

For any protocol you develop:

✓ All inclusion/exclusion criteria must be OPERATIONALIZED (not vague)
  Example ✓: "GAD diagnosis per DSM-5 structured clinical interview"
  Example ✗: "People with significant anxiety symptoms"

✓ Search strategies must be MAPPED to PICO elements
  Example ✓: "Population: MeSH 'Generalized Anxiety Disorder';
              Intervention: MeSH 'Cognitive Therapy'"
  Example ✗: "Searched for anxiety and CBT"

✓ Quality assessment tools must MATCH STUDY DESIGNS
  Example ✓: "RoB2 for RCTs; ROBINS-I for observational studies"
  Example ✗: "Used Newcastle-Ottawa for all studies including RCTs"

✓ Synthesis approach must ALIGN WITH DATA CHARACTERISTICS
  Example ✓: "Meta-analysis for homogeneous RCT outcomes (I² = 30%);
              narrative synthesis for qualitative studies"
  Example ✗: "Attempted meta-analysis despite I² = 85% heterogeneity"

```

## Tool Usage

This skill uses the **lit-review-planner agent** selected by the local catalog/meta-router to:
- Interview you about your research question, team capacity, and timeline
- Guide you through PICO/PICOS framework construction with examples
- Generate database-specific search strings with Boolean operators
- Design screening protocols with inter-rater reliability targets
- Select appropriate risk-of-bias tools with justification
- Plan narrative or meta-analytic synthesis approaches
- Map your protocol to PRISMA 2020 checklist

**Output format:**
- PICO/PICOS specification document
- Database selection matrix with coverage rationales
- Search strings (copy-paste ready for each database)
- Screening and selection protocol with operational criteria
- Data extraction form template (editable in Word/Google Docs)
- Risk of bias assessment plan
- Synthesis and reporting roadmap
- PRISMA checklist mapping

## Examples

**Example 1: Systematic Review of Psychotherapy for GAD**
```
User: /lit-review-planner
"We want to review the effectiveness of cognitive-behavioral therapy for
adults with generalized anxiety disorder. We have a team of 3 (1 PhD
psychologist, 2 master's-level clinicians) and 18 months."

Agent: [Guides through PICO framework; recommends Cochrane CENTRAL + MEDLINE
+ PsycINFO; designs dual-review protocol; selects Cochrane RoB2; plans
random-effects meta-analysis; outputs PRISMA-compliant protocol]
```

**Example 2: Scoping Review of Digital Mental Health Interventions**
```
User: /lit-review-planner scoping
"We're mapping the landscape of digital CBT and teletherapy for anxiety
disorders in middle-income countries. 6-month timeline."

Agent: [Switches to PRISMA-ScR framework; uses PCC (Population-Concept-Context);
includes grey literature heavily; narrative synthesis; targets rapid publication]
```

**Example 3: Rapid Review for Policy Decision**
```
User: /lit-review-planner rapid
"Policy deadline in 4 months. Does family-based CBT improve outcomes
compared to individual CBT in pediatric anxiety? Existing SRs available."

Agent: [Recommends focused search of recent SRs + 2 key databases; simplified
screening; abbreviated quality assessment; rapid narrative synthesis; maps
to AHRQ Rapid Review guidelines]
```

## Notes

- **Team capacity matters**: Systematic reviews require ≥2 reviewers for all screening phases (dual review prevents bias). Rapid reviews may use single reviewers with spot-checks.
- **PICO precision is non-negotiable**: Vague questions (e.g., "What therapies help anxiety?") lead to unmanageable scope. Spend time on PICO before database access.
- **Protocol registration prevents p-hacking**: Register on PROSPERO/OSF before screening begins. Deviations from protocol must be documented in manuscript.
- **Grey literature is essential**: 30–40% of relevant evidence lives outside PubMed. Dissertations, conference papers, and government reports often represent null/negative findings.
- **Risk of bias ≠ study quality**: A poorly-reported but methodologically sound RCT may score "some concerns" on RoB2 simply due to incomplete reporting. Context matters.
- **Equity integration is not optional**: PROGRESS-Plus framework helps identify differential impacts and harms across populations. Modern reviews expect this.
- **Plan before you search**: A well-designed protocol prevents scope creep, avoids selective outcome reporting, and makes your review reproducible and credible.

---

**Created by Zivtech Meta-Skills Team**
**Last updated**: 2026-03-09
**Model policy**: Resolved by the catalog/meta-router; this wrapper does not override it
