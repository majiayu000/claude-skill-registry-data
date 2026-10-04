---
name: method-engine
description: >
  Activate when the user needs to select, justify, describe, or execute a research
  methodology. Provides method selection guidance, complete method section templates,
  quality criteria, and tool recommendations. Covers SLR, qualitative (case study,
  Gioia, Mayring, Grounded Theory), quantitative (SEM, regression, survey, experiment),
  DSR, mixed methods, action research, ethnography, Delphi study, and simulation.
  Also includes Research Data Management (RDM) guidance for FAIR-compliant data handling.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Method Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (method-engine)
> **Input:** [brief description of the methodology request]
> **Output:** [brief description of what was produced — e.g., "DSR method section drafted with 3 evaluation criteria"]
> ```

# Method Engine

## Method Selection Guide

### Decision Tree

```
What is your primary research goal?
│
├─ "I want to map what the literature says" 
│   → Systematic Literature Review (Section A)
│
├─ "I want to understand a phenomenon in depth"
│   → Qualitative Study (Section B)
│   ├─ Single context, deep → Single Case Study
│   ├─ Multiple contexts, comparison → Multiple Case Study  
│   ├─ Build new theory from data → Grounded Theory / Gioia
│   └─ Analyze text/documents systematically → Content Analysis (Mayring)
│
├─ "I want to test hypotheses / measure relationships"
│   → Quantitative Study (Section C)
│   ├─ Complex model with latent variables → SEM (PLS or CB)
│   ├─ Simpler relationships → Regression
│   └─ Experimental comparison → Experiment / RCT (Section F)
│
├─ "I want to build something (tool, framework, model)"
│   → Design Science Research (Section D)
│
├─ "I want to combine approaches"
│   → Mixed Methods (Section E)
│
├─ "I want to improve practice through iterative intervention"
│   → Action Research (Section G)
│
├─ "I want to understand culture, practices, or lived experience"
│   → Ethnography (Section H)
│
├─ "I want structured expert consensus on a complex issue"
│   → Delphi Study (Section I)
│
└─ "I want to model and test scenarios computationally"
    → Simulation (Section J)
```

---

## Section A: Systematic Literature Review

### Method Section Template (ready to adapt):

```
3. Research Methodology

We conducted a systematic literature review following the guidelines of 
[vom Brocke et al. (2009, 2015) / Webster & Watson (2002) / Kitchenham & 
Charters (2007) / PRISMA 2020 (Page et al., 2021)]. This approach is 
appropriate because [justification: need to synthesize a growing but 
fragmented body of knowledge / field is maturing and needs stock-taking / 
practical guidance requires evidence synthesis].

3.1 Search Strategy

We searched [N] electronic databases: Semantic Scholar, OpenAlex, CrossRef, 
[and arXiv for preprints / and AIS eLibrary for IS-specific venues]. 
The search was conducted in [month/year] using the following query terms:

  [("generative AI" OR "generative artificial intelligence" OR "large language 
  model*" OR "LLM" OR "GPT" OR "foundation model*") AND ("enterprise" OR 
  "organization*" OR "business" OR "implementation" OR "adoption")]

  [("AI agent*" OR "autonomous agent*" OR "agentic AI") AND ("organization*" 
  OR "enterprise" OR "business process" OR "implementation")]

The search was limited to publications from [year] to [year], in 
[English / English and German].

3.2 Selection Criteria

Table [N] summarizes our inclusion and exclusion criteria.

| ID | Criterion | Rationale |
|----|-----------|-----------|
| IC1 | Peer-reviewed journal article or conference paper | Quality assurance |
| IC2 | Focuses on [topic] in organizational context | Scope alignment |
| IC3 | Published between [year] and [year] | Recency |
| IC4 | Available in English [or German] | Accessibility |
| EC1 | Purely technical (no organizational dimension) | Out of scope |
| EC2 | Editorial, book review, or abstract-only | Insufficient depth |
| EC3 | Duplicate publication | Avoid double-counting |

3.3 Search and Screening Process

Figure [N] presents the PRISMA flow diagram of our search and selection process. 
The initial search yielded [N] records across all databases. After removing 
[N] duplicates, [N] records were screened based on title and abstract, of 
which [N] were excluded. The remaining [N] articles were assessed in full text, 
resulting in [N] studies included in the final synthesis.

[Forward and backward citation tracking (snowballing) on the [N] most-cited 
included studies identified an additional [N] relevant papers, bringing the 
total to [N] studies.]

3.4 Data Extraction and Analysis

From each included study, we extracted: [list categories: research question, 
theoretical lens, methodology, sample/context, key findings, limitations, 
and contribution type].

We synthesized findings using a concept-centric approach (Webster & Watson, 2002), 
organizing results in a concept matrix that maps studies against key themes 
identified through iterative reading and coding.
```

### PRISMA Flow Diagram (text version):

```
Identification:
  Records from Semantic Scholar:     [n]
  Records from OpenAlex:             [n]  
  Records from CrossRef:             [n]
  Records from arXiv:                [n]
  Records from manual/snowballing:   [n]
  ─────────────────────────────────
  Total identified:                  [N]
  Duplicates removed:               -[n]
  Records after deduplication:       [N]

Screening:
  Title/abstract screened:           [N]
  Excluded:                         -[n]
  Full-text assessed:                [N]

Eligibility:
  Full-text excluded (with reasons): -[n]
    - Not organizational context:    [n]
    - Not empirical/conceptual:      [n]  
    - Not accessible:                [n]

Included:
  Studies in final synthesis:        [N]
```

---

## Section B: Qualitative Methods

### Case Study (Yin, 2018 / Eisenhardt, 1989)

Method section template:
```
3. Research Methodology

We employed a [single/multiple] case study approach (Yin, 2018) to investigate 
[phenomenon] in [context]. Case study research is appropriate when investigating 
a contemporary phenomenon within its real-world context, particularly when the 
boundaries between phenomenon and context are not clearly evident (Yin, 2018).

3.1 Case Selection

[For single case:] We selected [case] as a [revelatory/critical/typical/extreme] 
case (Yin, 2018) because [justification].

[For multiple cases:] Following [theoretical/literal] replication logic 
(Yin, 2018), we selected [N] cases based on [selection criteria]. Table [N] 
provides an overview of the cases.

| Case | Industry | Size | AI Maturity | Selection Rationale |
|------|----------|------|-------------|---------------------|
| A    | [X]      | [X]  | [X]         | [X]                 |
| B    | [X]      | [X]  | [X]         | [X]                 |

3.2 Data Collection

We collected data from multiple sources to enable triangulation (Yin, 2018):
- [N] semi-structured interviews with [roles] (average duration: [X] minutes)
- Internal documents: [list types]
- [Observation / workshop protocols / system logs]
- [Archival data: annual reports, press releases]

All interviews were recorded and transcribed [verbatim / in summary form].

3.3 Data Analysis

We analyzed the data using [thematic analysis (Braun & Clarke, 2006) / 
the Gioia methodology (Gioia et al., 2013) / qualitative content analysis 
(Mayring, 2014)]. [Method-specific description — see subsections below.]

3.4 Research Quality

We ensured research quality through:
- **Construct validity**: Multiple data sources, chain of evidence
- **Internal validity**: Pattern matching, explanation building
- **External validity**: [Replication logic across cases / analytical generalization]
- **Reliability**: Case study protocol, case study database
```

### Gioia Methodology (Gioia et al., 2013)

```
Data analysis followed the Gioia methodology (Gioia et al., 2013). First, we 
engaged in open coding of interview transcripts and documents, identifying 
first-order concepts that remained close to informant language. This yielded 
[N] initial codes. Through constant comparison and iterative abstraction, we 
grouped these into [N] second-order themes reflecting more abstract, 
researcher-driven categories. Finally, we aggregated themes into [N] 
overarching dimensions that form the basis of our emerging framework.

Figure [N] presents the resulting data structure.
```

### Mayring Content Analysis (Mayring, 2014)

```
We analyzed the data using qualitative content analysis following Mayring (2014). 
We employed [deductive / inductive / mixed] category formation. 

[Deductive:] Categories were derived from [Theory/prior framework] and applied 
to the material. Coding rules and anchor examples were defined a priori.

[Inductive:] Categories emerged from the data through systematic paraphrasing, 
generalization, and reduction of text passages. After coding [X]% of the 
material, the category system was revised and finalized.

[Both:] Inter-coder reliability was assessed using [Cohen's κ / Krippendorff's α], 
yielding a value of [X], indicating [substantial/excellent] agreement.
```

---

## Section C: Quantitative Methods

### Survey + PLS-SEM

```
3. Research Methodology

3.1 Research Model and Hypotheses
[Refer to Section 2 where hypotheses were developed]

3.2 Measurement
All constructs were measured using validated scales from prior literature. 
[Construct 1] was measured with [N] items adapted from [Author] (Year). 
[Construct 2] used [N] items from [Author] (Year). All items were assessed 
on a [7-point Likert / 5-point Likert] scale. Table [N] lists all 
measurement items with their sources.

3.3 Data Collection
Data were collected via an online survey distributed to [target population] 
through [distribution channels] between [month] and [month year]. 
After removing incomplete and inattentive responses (attention check items, 
completion time < [X] minutes), our final sample comprised N = [N] responses.

3.4 Analysis Method
We employed partial least squares structural equation modeling (PLS-SEM) 
using SmartPLS [version] (Ringle et al., Year). PLS-SEM is appropriate 
for our study because [exploratory nature / complex model / formative 
constructs / prediction-oriented / small sample] (Hair et al., 2019).

3.5 Measurement Model Assessment
[Convergent validity:] All indicator loadings exceed 0.708, composite 
reliability (CR) values are above 0.70, and average variance extracted 
(AVE) exceeds 0.50 for all constructs (Table [N]).

[Discriminant validity:] The Fornell-Larcker criterion is satisfied, and 
HTMT values are below 0.85 (Table [N+1]).

[Common method bias:] We assessed common method bias using [Harman's 
single-factor test / marker variable technique / ULMC]. Results suggest 
that CMB does not pose a significant concern.

3.6 Structural Model Assessment
[Report: path coefficients, significance (bootstrapping, N=5000), R², f², Q²]
```

---

## Section D: Design Science Research

### Method Section Template (Peffers et al., 2007):

```
3. Research Approach

We follow the Design Science Research Methodology (DSRM) by Peffers et al. 
(2007), complemented by the guidelines of Hevner et al. (2004). DSR is 
appropriate because our objective is to develop [artifact type: a framework / 
a model / a method / a prototype] that addresses [practical problem].

Our research process comprises six activities:

(1) Problem identification: [Derived from literature review + practice, Section 2]
(2) Solution objectives: [Design requirements, Section 3.1]
(3) Design and development: [Artifact construction, Section 4]
(4) Demonstration: [Application to real-world scenario, Section 4.x]
(5) Evaluation: [Evaluation method and results, Section 5]
(6) Communication: [This paper]

3.1 Design Requirements

Based on our problem analysis (Section 2) and [N] expert interviews / 
[analysis of practice], we derived the following design requirements:

| ID  | Design Requirement | Source | Type |
|-----|-------------------|--------|------|
| DR1 | The [artifact] must [capability] | Literature: Author (Year) | Functional |
| DR2 | The [artifact] should [quality] | Expert interview #[N] | Non-functional |
| DR3 | [Users] need to [capability] | Practice analysis | User |

3.2 Kernel Theories

Our design is grounded in [Theory 1] (Author, Year) and [Theory 2] (Author, Year). 
[Theory 1] informs the design by [specific mechanism → design decision]. 
[Theory 2] guides [specific aspect] because [reasoning].

3.3 Evaluation Strategy

Following Venable et al. (2016), we employ [evaluation strategy: 
human risk & effectiveness / technical risk & efficacy / quick & simple]. 
Specifically, we evaluate the artifact through [method: expert interviews / 
user study / field experiment / case study application / scenario-based].
```

---

## Section E: Mixed Methods

```
3. Research Methodology

We employed an [explanatory sequential / exploratory sequential / convergent] 
mixed methods design (Creswell & Creswell, 2018; Venkatesh et al., 2013).

[Explanatory sequential:] First, we conducted a quantitative [survey/experiment] 
(Phase 1) to [test hypotheses / identify patterns]. Subsequently, we conducted 
qualitative [interviews/case studies] (Phase 2) to explain and deepen the 
quantitative findings.

[Exploratory sequential:] First, we conducted qualitative [interviews/observations] 
(Phase 1) to explore [phenomenon] and develop [a conceptual model / hypotheses]. 
Subsequently, we tested these through a quantitative [survey] (Phase 2).
```

---

## Section F: Experiment / Randomized Controlled Trial

### Method Section Template:

```
3. Research Methodology

3.1 Experimental Design

We employed a [between-subjects / within-subjects / mixed] experimental design
with [N] conditions: [list conditions, e.g., "AI-assisted (treatment) vs.
manual-only (control)"]. [For factorial designs:] The experiment followed a
[2×2 / 2×3 / ...] factorial design, manipulating [Factor 1] ([levels]) and
[Factor 2] ([levels]).

3.2 Participants

We recruited [N] participants from [population: MTurk / Prolific / university
students / organizational employees]. [Power analysis:] A priori power analysis
(G*Power; Faul et al., 2007) indicated a minimum sample of [N] participants
to detect [medium / small / large] effects (f = [X], α = .05, 1−β = .80).
After excluding [N] participants based on [attention checks / incomplete
responses / manipulation check failures], the final sample comprised N = [N]
([demographics summary]).

3.3 Procedure

[Describe the experimental procedure step by step:]
1. Participants were randomly assigned to one of [N] conditions
2. [Pre-task: consent, demographics, baseline measures]
3. [Task description: what participants did in each condition]
4. [Manipulation: what differed between conditions — be specific]
5. [Post-task: dependent variable measurement, manipulation checks, debriefing]

The average session duration was [X] minutes. The study was approved by
[IRB / ethics board] (protocol #[X]).

3.4 Measures

**Dependent Variable(s):**
[DV1] was measured using [instrument/scale] from [Author] (Year).
[Describe: N items, scale anchors, Cronbach's α]

**Independent Variable(s):**
[IV] was manipulated by [description of manipulation].

**Control Variables:**
[List controls: age, gender, prior experience, tech literacy, etc.]

**Manipulation Check:**
To verify the manipulation was effective, participants [responded to / rated]
[manipulation check item(s)]. Results confirmed successful manipulation:
[statistical test, e.g., t(df) = X.XX, p < .001].

3.5 Analysis

We tested our hypotheses using [ANOVA / ANCOVA / regression / t-tests].
[For ANOVA:] A [one-way / two-way / repeated-measures] ANOVA was conducted
with [IV] as the independent factor and [DV] as the dependent variable.
[Report: F-statistic, degrees of freedom, p-value, effect size (η² or Cohen's d)]
```

### Validity Threats Checklist:
- **Internal validity**: Random assignment, manipulation checks, attention checks
- **External validity**: Sample representativeness, ecological validity of task
- **Construct validity**: Established scales, manipulation strength
- **Statistical conclusion validity**: Power analysis, assumption checks

---

## Section G: Action Research

### Method Section Template (Susman & Evered, 1978; Baskerville, 1999):

```
3. Research Methodology

We adopted an Action Research (AR) approach following [Susman & Evered (1978) /
Baskerville (1999) / Davison et al. (2004)]. AR is appropriate because our
research aims to [solve a practical problem AND generate theoretical insights
simultaneously]. Unlike purely observational research, AR involves the
researcher as an active participant in the change process (Baskerville, 1999).

3.1 Research Setting

The action research was conducted at [organization/context], a [description]
with [N] employees. The organization was facing [practical problem that
motivated the research]. Access was facilitated through [relationship/agreement].

3.2 Action Research Cycle(s)

We conducted [N] AR cycle(s), each comprising five stages
(Susman & Evered, 1978):

**Cycle 1: [Focus of this cycle]**
1. **Diagnosing:** [Problem identification methods — interviews, workshops,
   document analysis]. Key issues identified: [list].
2. **Action planning:** [Collaborative design of intervention with practitioners].
   Planned intervention: [description].
3. **Action taking:** [Implementation of the intervention over [timeframe]].
   [Describe what was done, by whom, and any deviations from plan].
4. **Evaluating:** [Assessment of outcomes using [methods: interviews,
   surveys, performance metrics, observation]].
5. **Specifying learning:** [Theoretical and practical insights extracted].
   This informed the design of Cycle 2.

[Repeat for subsequent cycles]

3.3 Data Collection

Data were collected throughout the AR cycles using:
- [N] interviews with [roles] (pre- and post-intervention)
- Researcher diary / field notes ([N] entries over [timeframe])
- Workshop protocols ([N] workshops with [participants])
- Organizational documents: [types]
- [Quantitative measures: KPIs, usage logs, survey data]

3.4 Data Analysis

We analyzed qualitative data using [thematic analysis / coding approach].
Quantitative measures were tracked longitudinally across cycles.
Researcher positionality and dual role were addressed through [reflexive
journaling / external review / member checking].

3.5 Principles of Canonical Action Research

Following Davison et al. (2004), we ensured adherence to:
- **Researcher-client agreement**: [how formalized]
- **Cyclical process model**: [N] complete cycles
- **Theory-guided**: Informed by [theory]
- **Change through action**: [what was changed]
- **Reflection on learning**: [how learning was captured and generalized]
```

---

## Section H: Ethnography

### Method Section Template:

```
3. Research Methodology

We conducted an [organizational / digital / auto-] ethnographic study
following [Myers (1999) / Van Maanen (2011) / Schultze (2000)]. Ethnography
is appropriate for investigating [phenomenon] because it enables deep
understanding of cultural practices, meanings, and social dynamics as
experienced by participants in their natural setting (Myers, 1999).

3.1 Research Site

The ethnographic fieldwork was conducted at [organization/community/platform]
over a period of [duration: months]. [Description of the site: industry, size,
relevance to research questions]. Access was negotiated through [gatekeepers]
and formalized via [agreement/IRB approval].

3.2 Fieldwork and Data Collection

The primary researcher spent [X hours/days per week] embedded in [setting]
from [start date] to [end date], totaling approximately [N] hours of fieldwork.

Data were collected through multiple methods:
- **Participant observation**: [describe role: observer-as-participant /
  participant-as-observer]. Field notes were recorded [daily / immediately
  after sessions], yielding [N] pages of notes.
- **Informal conversations and interviews**: [N] formal semi-structured
  interviews (average [X] minutes) and [approximately N] informal conversations.
  Formal interviews were [recorded and transcribed / documented in notes].
- **Document analysis**: [types: emails, Slack channels, internal wikis,
  policy documents, meeting minutes].
- **Artifacts**: [photos, screenshots, system logs, physical artifacts].

3.3 Data Analysis

Analysis proceeded iteratively alongside data collection (Hammersley &
Atkinson, 2019). We employed [thematic analysis / interpretive analysis /
grounded theory coding] to identify patterns in cultural practices and
meaning-making. [Describe coding process, categories, and how themes emerged.]

3.4 Reflexivity and Research Quality

We addressed the inherent subjectivity of ethnographic research through:
- **Reflexive journaling**: Regular reflection on researcher positionality
  and assumptions
- **Triangulation**: Multiple data sources and methods
- **Member checking**: Key interpretations shared with [N] informants for
  validation
- **Thick description**: Providing rich contextual detail to support
  transferability (Geertz, 1973)
```

---

## Section I: Delphi Study

### Method Section Template (Dalkey & Helmer, 1963; Okoli & Pawlowski, 2004):

```
3. Research Methodology

We conducted a [classical / modified / ranking-type / policy] Delphi study
following the guidelines of [Okoli & Pawlowski (2004) / Schmidt (1997) /
Paré et al. (2013)]. The Delphi method is appropriate because [our research
question requires structured expert judgment on a complex, uncertain topic
where no definitive empirical evidence exists] (Dalkey & Helmer, 1963).

3.1 Expert Panel Selection

Experts were selected based on [criteria: years of experience, domain
expertise, publication record, organizational role]. Following Okoli &
Pawlowski (2004), we identified experts through [method: literature review,
professional networks, snowball sampling, nomination by peers].

| Criterion | Requirement | Rationale |
|-----------|-------------|-----------|
| Domain expertise | [X] years in [field] | Depth of knowledge |
| Role | [roles: CIO, researcher, consultant] | Diverse perspectives |
| Geographic spread | [regions] | Avoid cultural bias |

[N] experts were invited; [N] agreed to participate ([X]% response rate).
Panel composition: [breakdown by role, sector, region].

3.2 Delphi Rounds

**Round 1: [Brainstorming / Open-ended]**
Experts were asked to [describe the open-ended question/task]. Responses
were [analyzed qualitatively / coded / consolidated] into [N] initial items/factors.

**Round 2: [Rating / Ranking]**
The [N] consolidated items were presented to the panel for [rating on a
[5/7]-point Likert scale / ranking by importance]. Controlled feedback
from Round 1 was provided: [median ratings, IQR, anonymized comments].

**Round 3: [Revision / Final ranking]**
Experts reviewed group results from Round 2 and were invited to revise
their ratings. Items where [Kendall's W > [X] / IQR ≤ [X] / ≥ [X]% agreement]
were considered to have reached consensus.

[Optional: Round 4 if consensus not reached]

3.3 Consensus Measurement

We assessed consensus using [Kendall's W coefficient of concordance /
interquartile range (IQR) / percentage agreement / coefficient of variation].
Consensus was defined as [specific threshold, e.g., IQR ≤ 1 on a 7-point scale /
Kendall's W > 0.7 / ≥ 70% agreement].

3.4 Analysis

Final results were analyzed by [computing mean/median rankings, identifying
clusters of related items, comparing across expert subgroups]. [If applicable:]
Non-consensus items were analyzed qualitatively to understand divergent views.
```

### Panel Size Guidelines:
- Minimum: 10-15 experts (Okoli & Pawlowski, 2004)
- Typical: 15-30 experts
- Attrition: Plan for 20-30% dropout per round

---

## Section J: Simulation / Agent-Based Modeling

### Method Section Template:

```
3. Research Methodology

We employ a [system dynamics / agent-based / discrete event / Monte Carlo]
simulation approach following [Law (2015) / Gilbert & Troitzsch (2005) /
Sterman (2000)]. Simulation is appropriate because [the phenomenon involves
complex dynamic interactions that are difficult to study empirically / we
need to explore scenarios and parameter sensitivities / ethical or practical
constraints prevent real-world experimentation].

3.1 Model Design

The simulation model represents [system/phenomenon] with the following
key components:

**Agents/Entities:**
| Agent Type | Attributes | Behavior Rules | Count |
|------------|-----------|----------------|-------|
| [Type 1] | [list] | [decision rules] | [N] |
| [Type 2] | [list] | [decision rules] | [N] |

**Environment:**
[Describe the simulation environment: topology, resources, constraints]

**Interaction Rules:**
[Describe how agents interact: communication, competition, cooperation]

**Time:** The model runs in [discrete time steps / continuous time] over
[N iterations / time horizon].

3.2 Theoretical Grounding

The model's behavioral rules are grounded in [theory/empirical findings]:
- [Rule 1] is based on [Author (Year)] who found [finding]
- [Rule 2] reflects [theoretical mechanism from Theory X]
- [Parameter values] were calibrated using [empirical data / expert estimates /
  literature values]

3.3 Implementation

The model was implemented in [NetLogo / AnyLogic / Python (Mesa) / Matlab /
Vensim / R] (version [X]). [Key implementation choices and simplifying
assumptions]. The source code is available at [repository URL].

3.4 Verification and Validation

Following Sargent (2013), we conducted:
- **Verification** (does the model run correctly?): [code review, debugging,
  unit tests, trace analysis, comparison with analytical solutions]
- **Validation** (does the model represent reality?): [comparison with
  empirical data, face validation by [N] domain experts, sensitivity analysis,
  extreme condition tests]

3.5 Experimental Design

We explored [N] scenarios varying [parameters]:
| Scenario | Parameter 1 | Parameter 2 | Rationale |
|----------|------------|------------|-----------|
| Baseline | [value] | [value] | Reference case |
| S1 | [value] | [value] | Test [hypothesis/what-if] |
| S2 | [value] | [value] | Test [hypothesis/what-if] |

Each scenario was run [N] times (Monte Carlo replications) to account
for stochastic variation. Results are reported as [mean ± SD / median with
95% CI / distribution plots].
```

---

## Research Data Management (RDM)

### FAIR Principles (Wilkinson et al., 2016)

Every research project should address data management. Use this section as a
checklist and to draft the data availability statement.

| Principle | Requirement | How to Address |
|-----------|-------------|----------------|
| **Findable** | Data has persistent identifier, rich metadata | DOI via Zenodo/Figshare, descriptive README |
| **Accessible** | Data retrievable via standardized protocol | Open repository, clear access conditions |
| **Interoperable** | Data uses shared vocabularies/formats | Standard formats (CSV, JSON, BibTeX), codebooks |
| **Reusable** | Data has clear license, provenance | CC-BY 4.0, data collection documentation |

### Data Management Plan Template

```markdown
## Data Management Plan

### 1. Data Description
- **Type:** [survey responses / interview transcripts / system logs /
  simulation output / literature database / code]
- **Format:** [CSV / JSON / PDF / audio / text]
- **Volume:** [estimated size]
- **Sensitivity:** [public / restricted / confidential]

### 2. Data Collection
- **Method:** [how data will be collected]
- **Tools:** [instruments, platforms, software]
- **Timeline:** [when collection starts and ends]

### 3. Documentation and Metadata
- **Codebook:** [variable descriptions, coding schemes]
- **README:** [project overview, file structure, usage instructions]
- **Provenance:** [data sources, transformation steps, version history]

### 4. Ethics and Legal Compliance
- **Consent:** [informed consent process, template reference]
- **Anonymization:** [strategy: pseudonymization, k-anonymity, aggregation]
- **GDPR/DSGVO:** [legal basis, data protection measures, DPO contact]
- **Ethics approval:** [IRB/ethics board reference number]

### 5. Storage and Backup
- **Active storage:** [institutional server / cloud / local — with encryption]
- **Backup:** [3-2-1 rule: 3 copies, 2 media types, 1 offsite]
- **Retention:** [how long after project completion]

### 6. Sharing and Archiving
- **Repository:** [Zenodo / Figshare / institutional / discipline-specific]
- **License:** [CC-BY 4.0 / CC0 / restricted access with justification]
- **Embargo:** [if applicable: duration and reason]
- **DOI:** [will be assigned upon deposit]

### 7. Responsibilities
- **Data steward:** [name/role]
- **Access control:** [who can access what, and how]
```

### Data Availability Statement Templates

```
[Open data:]
The data that support the findings of this study are openly available in
[repository] at https://doi.org/[DOI], reference number [ref].

[Restricted data:]
The data that support the findings of this study are available from
[source/organization] but restrictions apply to the availability of these
data, which were used under license for the current study, and so are not
publicly available. Data are however available from the authors upon
reasonable request and with permission of [source/organization].

[No data (theoretical/conceptual):]
Data sharing is not applicable to this article as no datasets were
generated or analyzed during the current study.

[SLR data:]
The complete literature database and concept matrix are available as
supplementary materials at [repository/DOI].
```

---

## Quality Criteria Quick Reference

| Method | Key Quality Criteria | How to Address |
|--------|---------------------|----------------|
| SLR | Reproducibility, Comprehensiveness | Protocol, multiple databases, PRISMA |
| Case Study | Construct/Internal/External validity, Reliability | Triangulation, chain of evidence, protocol |
| Gioia/GT | Trustworthiness | Thick description, data structure display, informant validation |
| Content Analysis | Inter-coder reliability | Cohen's κ > 0.7, Krippendorff's α > 0.8 |
| Survey/SEM | Reliability, Validity, CMB | CR > 0.7, AVE > 0.5, HTMT < 0.85, Harman |
| Experiment | Internal validity, Power, Manipulation | Random assignment, power analysis, manipulation checks |
| DSR | Utility, Quality, Efficacy | Evaluation framework (Venable et al.), kernel theories |
| Mixed Methods | Integration quality | Meta-inferences, explicit integration strategy |
| Action Research | Rigor, Relevance, Reflectivity | AR principles (Davison et al.), cycles, dual outcomes |
| Ethnography | Trustworthiness, Reflexivity | Thick description, prolonged engagement, member checks |
| Delphi | Consensus, Panel quality, Stability | Kendall's W, expert selection criteria, round-over-round stability |
| Simulation | Verification, Validation, Sensitivity | V&V framework (Sargent), replications, parameter sweeps |
