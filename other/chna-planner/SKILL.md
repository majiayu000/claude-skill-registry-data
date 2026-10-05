---
name: chna-planner
description: "Plan community health needs assessments — data collection, stakeholder engagement, reporting."
version: 0.1.0
---

# CHNA Planner

## JTBD (Jobs To Be Done)

### Primary Job
When a nonprofit hospital is entering a new CHNA cycle and faces the simultaneous pressure of IRS §501(r)(3) compliance, genuine community engagement, health equity methodology, and a hard board-adoption deadline,
I want a complete 9-phase CHNA design and execution plan before any fieldwork begins,
so I can run an assessment that is legally defensible, community-centered, and equity-forward — not one that was assembled reactively under deadline pressure and leaves the organization exposed to regulatory audit or community mistrust.

### Secondary Jobs
- When the service area includes medically underserved populations — low-income residents, non-English speakers, immigrants, justice-involved individuals — and standard engagement methods will not reach them, I want a targeted community engagement strategy that identifies specific methods, partners, and accessibility accommodations per population, so the CHNA reflects the health needs of those most affected rather than those easiest to survey.
- When the hospital completed a CHNA three years ago and needs to determine what changed, what implementation strategies succeeded, and where the prior assessment left gaps, I want a continuity and gap analysis built into the planning phase, so the new cycle builds on prior work rather than starting from scratch or repeating the same omissions.
- When the prioritization process will involve clinicians, hospital leadership, community advisory board members, and public health officials with competing priorities, I want a structured multi-stakeholder scoring methodology with explicit equity weighting built in, so health needs of marginalized populations are not systematically deprioritized in favor of conditions that affect the majority or that the hospital already has capacity to address.
- When the CHNA findings will feed directly into the hospital's implementation strategy, IRS Form 990 Schedule H reporting, and community benefit documentation, I want explicit alignment between the CHNA plan and downstream reporting requirements built into the design, so there are no gaps between assessed needs and documented community benefit investments.

### Job Layers
- Functional: Design all 9 phases — scope and regulatory context, community profile, engagement strategy, data collection and analysis, prioritization framework, implementation strategy, report structure, equity integration, and implementation timeline — into a single executable plan with month-by-month tasks, regulatory checkpoints, and companion skill handoffs.
- Emotional: Replace the dread of managing a sprawling 9-month compliance process with a structured plan that makes every decision point explicit, every regulatory requirement traceable, and every equity commitment visible before the hospital commits resources.
- Social: Helps the hospital present a CHNA process to its board, community partners, and IRS reviewers that is demonstrably rigorous, community-centered, and equity-forward — not a box-checking exercise.

### This Skill Is For
- A nonprofit hospital starting or renewing a 3-year CHNA cycle under IRS §501(r)(3) that needs a structured, compliant, and equity-centered design before fieldwork begins.
- A hospital whose prior CHNA was criticized for insufficient community engagement with underserved populations, for treating health equity as a section rather than a lens, or for prioritization processes that centered institutional interests over community voice.
- A CHNA project lead who needs to coordinate across hospital leadership, clinical departments, community advisory board members, and CBO partners and wants a clear phase-by-phase plan with defined roles, timelines, and decision points.

### This Skill Is NOT For
- A hospital updating a CHNA mid-cycle for a tactical data refresh; use an incremental update protocol instead.
- An organization whose primary goal is grant writing or fundraising narrative rather than community accountability; use `policy-brief-writer` for that.
- An assessment scoped to a single clinical program rather than an organization-wide community benefit strategy.
- A hospital that lacks community engagement infrastructure or senior leadership commitment to the process.

### Paired With
- `health-equity-analyzer`: Apply at Phase 8 to audit whether equity is genuinely integrated throughout — disaggregated data, community voice in prioritization, SDOH root causes addressed — or whether equity language is present without substantive analysis.
- `research-critic`: Use when the CHNA's data collection methodology or quantitative analysis approach needs independent review for rigor.
- `dataviz-planner`: Use at Phase 7 to design disparity maps, health needs rankings, implementation timelines, and community-accessible visualizations.
- `stakeholder-report-writer`: Use at Phase 7 to develop the plain-language community summary, board presentation, and audience-specific versions of the report.
- `policy-brief-writer`: Use when prioritized health needs produce actionable policy recommendations that need to be structured for legislators or government agencies.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Starting a new CHNA cycle with no existing plan | The skill designs all 9 phases with month-by-month tasks, regulatory checkpoints, and companion skill handoffs | A complete CHNA execution plan ready for project kickoff |
| Has a previous CHNA and needs continuity analysis | The skill builds a gap and continuity review into Phase 1 scope-setting | A plan that explicitly addresses what changed, what succeeded, and what the new cycle must correct |
| Needs equity centered in design, not added at the end | The skill integrates health equity at every phase with specific actions, not a standalone equity section | A CHNA design where equity is structural, not cosmetic |
| Has a hard board-adoption deadline and needs realistic sequencing | The skill maps a 9-month timeline from scoping to public posting with board adoption as a fixed end point | A phased timeline with explicit milestones and contingency points |
| Needs to align CHNA with IRS Form 990 Schedule H | The skill documents §501(r)(3) compliance requirements and connects implementation strategies to community benefit reporting | A plan with regulatory compliance built in at every phase |

### When to Escalate
- If the user already has a completed CHNA and needs it reviewed for equity gaps or methodological rigor, escalate to `health-equity-analyzer` or `research-critic`.
- If the user's primary need is extracting policy recommendations from CHNA findings rather than planning the assessment itself, escalate to `policy-brief-writer`.

## Purpose

The chna-planner skill orchestrates the design and delivery of Community Health Needs Assessments (CHNAs) for nonprofit hospitals. It structures the legal requirements (IRS §501(r)(3)), community engagement mandates, health equity integration, and data analysis workflows into a coherent 9-phase planning protocol. The output is a detailed, executable plan and corresponding implementation roadmap that hospital leadership and project teams can follow from scoping through board approval and public posting.

## Use_When

- Nonprofit hospital is initiating or renewing a 3-year CHNA cycle (IRS requirement)
- Organization needs structured approach to community engagement, health equity, and regulatory compliance
- Team wants explicit methodology for health needs prioritization and implementation planning
- Stakeholder alignment and transparent documentation are critical
- Plan must be defensible under regulatory audit or community scrutiny

## Do_Not_Use_When

- Organization is updating a CHNA mid-cycle for tactical data refresh (use incremental update protocol instead)
- Primary goal is grant writing or fundraising narrative (use policy-brief-writer for that)
- Assessment is for a single clinical program vs. organization-wide community benefit strategy
- Hospital lacks community engagement infrastructure or senior leadership commitment

## Why_This_Exists

CHNAs are mandated under the Affordable Care Act (§501(r)(3)) and require hospitals to:
1. Conduct a community health needs assessment every 3 years
2. Document findings and prioritize health needs transparently
3. Develop and adopt an implementation strategy addressing the prioritized needs
4. Make all reports publicly available

The regulatory and community-facing stakes are high. Poorly designed CHNAs expose hospitals to:
- IRS audit findings and operational requirements
- Community mistrust and activist scrutiny
- Health inequity perpetuation (if equity is not centered)
- Misalignment between assessed needs and strategic investments

This skill consolidates domain expertise in regulatory compliance, health equity methodology, community engagement design, and data analytics into a planner-base-protocol workflow. The result is a legally sound, community-centered, equity-forward CHNA plan that hospitals can execute with confidence.

## Companion_Skills

- **health-equity-analyzer**: Apply equity lens at every phase; disaggregate data by race/ethnicity, income, geography, disability; center community voice; conduct power analysis
- **dataviz-planner**: Design data visualizations for community health indicators, priorities, disparities; ensure accessibility and cultural relevance
- **stakeholder-report-writer**: Develop plain-language summaries, board presentations, community-facing reports; manage distribution across languages and formats
- **policy-brief-writer**: Extract policy recommendations from prioritized health needs; align with state/local health department strategic priorities

## Steps

1. **Route to agent** (in order of availability):
   - Use the local catalog/meta-router to select `chna-planner`
   - If unavailable, use a host `general-purpose` worker with the full protocol embedded
   - OMC may execute the already-selected protocol as an optional external worker; it does not choose the route or model policy

2. **Collect context** from user:
   - Hospital name, service area geography (county, zip codes, census tracts)
   - Current year in CHNA cycle (year 1, 2, 3 of previous cycle, or new cycle?)
   - Known regulatory/board deadlines
   - Previous CHNA report (if exists): what was assessed, what changed?
   - Preliminary stakeholder list
   - Budget range and team capacity

3. **Invoke agent** with full planning protocol (see below)

4. **Review output** (plan document + task list):
   - Does it address all 9 phases?
   - Are regulatory requirements explicit?
   - Is health equity centered in design?
   - Are companion skills referenced appropriately?
   - Are timeline and resource assumptions realistic?

5. **Refine with user feedback** on scope, timeline, or constraints

6. **Export and execute**: User can immediately begin community engagement design, data sourcing, or stakeholder convening

## Full_Planning_Protocol

```
CHNA Planner Protocol (9 Phases)
=================================

PHASE 1: Scope and Regulatory Context
-------------------------------------
1a. Define the service area
    - Geographic scope (county, multi-county, zip code cluster)?
    - How was previous scope defined? Changes?
    - Align with hospital's community benefit service area definition
    - Map against state health department regional definitions

1b. Establish regulatory timeline
    - IRS 3-year cycle: which year is this cycle? When was previous CHNA completed?
    - Board adoption deadline
    - Public posting deadline (must post within 5 business days of adoption)
    - State health department reporting deadlines (varies by state)
    - Upcoming strategic plan cycles that depend on CHNA findings

1c. Document IRS requirements (§501(r)(3) compliance checklist)
    - [ ] Assessment conducted every 3 years (or triennial)
    - [ ] Reflects input from community members, public health expertise, and underserved populations
    - [ ] Documents process and findings
    - [ ] Identifies health needs and prioritizes them
    - [ ] Adopts an implementation strategy addressing prioritized health needs
    - [ ] Makes findings publicly available (posted and submitted to IRS if requested)
    - [ ] Board resolution formally adopting the assessment and implementation strategy
    - [ ] Community input documented and weighted in prioritization

1d. Identify required stakeholders
    - Community representatives (diverse, including medically underserved and vulnerable pops)
    - Public health experts (county health officer, epidemiologist, state health dept liaison)
    - Hospital leadership (CEO, community benefit officer, clinical leadership)
    - Clinical department heads (emergency, primary care, behavioral health, OB/GYN, pediatrics)
    - Community-based organizations (CBOs, safety-net providers, social services)
    - Academic partners (schools of medicine/public health, research institutions)
    - Previous CHNA leadership (maintain continuity)

1e. Assess prior findings and continuity
    - What health needs were prioritized in the last CHNA?
    - Which implementation strategies were completed/ongoing?
    - What changed in the community since last assessment? (new employers, closures, demographic shifts, pandemic impacts)
    - How will this cycle build on or pivot from prior findings?

1f. Establish resource parameters
    - Budget (staff FTE, consultant, data subscriptions, incentives, events)
    - Timeline: months from today to board adoption
    - Team composition (internal vs. external expertise)
    - Technology needs (survey platform, data analysis tools, visualization)


PHASE 2: Community Profile Design
---------------------------------
2a. Define demographic and health status data sources
    - U.S. Census Bureau (decennial census, American Community Survey)
    - CDC WONDER (mortality, morbidity, behavioral risk factors)
    - BRFSS (Behavioral Risk Factor Surveillance System)
    - State health department vital statistics and disease registry
    - Hospital HCUP (Healthcare Cost and Utilization Project) claims data
    - Hospital emergency department and inpatient utilization data
    - County/regional health department data (immunizations, STI, TB, etc.)
    - Medicaid and Medicare claims (if accessible via partnership)
    - Academic research and community health surveys
    - CMS Hospital Readmissions and 30-Day Mortality Data
    - CMS Preventable Readmissions data by condition and demographics

2b. Select health status indicators (organized by domain)
    - Mortality: age-adjusted mortality rate, cause-specific mortality (CVD, cancer, suicide, unintentional injury, maternal)
    - Morbidity: prevalence of chronic disease (diabetes, hypertension, COPD, depression, substance use), mental health, ACEs
    - Behavioral risk factors: smoking, alcohol use, physical inactivity, food insecurity, housing instability
    - Maternal and child health: teen birth rate, low birthweight, preterm birth, infant mortality, childhood obesity, developmental delays
    - Environmental health: air quality, lead exposure, water quality, traffic-related injury
    - Social determinants of health (SDOH): poverty, unemployment, educational attainment, housing stability, food access, transportation, healthcare access
    - Health care access: uninsured/underinsured, primary care and specialist supply, emergency department utilization patterns
    - Health equity indicators: disaggregate all of the above by race/ethnicity, income, geography, age, disability status, language

2c. Determine geographic granularity
    - County level: standard for CHNA, easy data availability
    - Sub-county (zip code, census tract, neighborhood): richer variation, some data limitations
    - Multi-level analysis: use county for context, drill into zip code/tract for disparities mapping
    - Hospital service area overlays: define hospital's actual patient draw (from claims data)

2d. Plan health equity stratifications
    - Race and ethnicity (use Census categories; consider ethnic subcategories if sample size allows)
    - Income/poverty (% at or below 100%, 200%, 400% federal poverty line; median household income)
    - Age (pediatric, adolescent, working age, older adult; life course lens)
    - Geography (urban/rural; neighborhood deprivation index)
    - Disability status (cognitive, physical, sensory, mental health; data often limited)
    - Language (non-English household, English language learner)
    - Immigration status and documentation (proxy: foreign-born population, recent immigrant)
    - LGBTQ+ identity and sexual orientation (limited data; may require qualitative inquiry)
    - Justice-involved populations (incarceration, reentry)

2e. Identify community assets and existing interventions
    - Health care providers and systems (hospital, community health centers, specialty providers)
    - Community-based organizations (social services, food banks, housing, behavioral health, substance use treatment)
    - Public health infrastructure (health department programs, school health, environmental health)
    - Educational institutions (schools, community college, university research partnerships)
    - Faith-based and civic organizations (community organizing capacity, trust relationships)
    - Informal support networks (community leaders, cultural brokers, peer supporters)
    - Previous CHNA implementation strategy progress (what's working, what stalled)

2f. Plan asset mapping methodology
    - Primary data collection: interviews or survey with community leaders, CBO directors, health care providers
    - Secondary data: aggregation of existing agency databases, online directories
    - Geographic information system (GIS) mapping: overlay assets on demographic/health disparities map
    - Asset inventory format: organization name, service type, population served, contact info, hours, language access
    - Connection mapping: which organizations partner, which gaps exist


PHASE 3: Community Engagement Strategy
--------------------------------------
3a. Design input methods (multi-method approach)
    - Surveys (random sample community survey, targeted population survey, CBO/provider survey): reach breadth, enable quantification
    - Focus groups: 4-6 groups, each 1.5-2 hours, with distinct populations (e.g., youth, seniors, Latinx, Black, Asian, LGBTQ, disabled, justice-involved, rural)
    - Key informant interviews: 15-25 interviews with community leaders, CBO directors, clinical leaders, health department
    - Community forums and listening sessions: 3-5 open public events, multiple times/locations, welcoming tone
    - Online feedback portal: complementary digital option for those unable to attend in-person
    - Community advisory board: standing group (6-12 members) meeting monthly to review findings and inform prioritization

3b. Reach medically underserved and vulnerable populations
    - Partner with trusted CBOs (community health centers, safety-net providers, racial/ethnic cultural organizations, LGBTQ+ centers, disability orgs, immigrant orgs, homeless services, substance use treatment, reentry programs)
    - Hold focus groups and listening sessions in community locations (not hospital), with food and culturally appropriate refreshments
    - Offer childcare, transportation reimbursement, live interpretation, ASL interpretation
    - Conduct surveys in multiple languages
    - Use community health workers and peer leaders as engagement facilitators
    - Address power dynamics: hospital as institution may be distrusted; framing matters

3c. Plan language access and cultural competency
    - Identify top 5-10 languages spoken in service area (census data)
    - Provide interpretation at all in-person events (not just passive materials translation)
    - Translate key materials (survey, summary, final report) into community languages
    - Use certified medical interpreters for sensitive topics
    - Train engagement team in cultural humility and implicit bias
    - Employ bilingual/bicultural staff or contractors in planning and engagement roles

3d. Ensure diverse representation
    - Community advisory board: 50%+ people with lived experience (residents, not providers); intentional diversity (race, ethnicity, income, age, geography, health status, LGBTQ+, disability, language)
    - Survey targets: oversample underrepresented populations to ensure adequate data
    - Focus group sampling: intentional recruitment through partner organizations, not self-selected volunteers only
    - Public events: publicize via trusted channels (CBO listservs, community radio, social media, faith institutions)
    - Feedback mechanisms: make it easy to provide input via phone, online, in-person, mail

3e. Structure community advisory board
    - Size: 8-12 members (large enough for diversity, small enough for engagement)
    - Composition: majority community members; include key institutional partners (health department, hospital, CBO leaders)
    - Selection: intentional recruitment + open application; prioritize historically excluded voices
    - Commitment: 6-12 month engagement, monthly meetings (2 hours), expect preparation time
    - Compensation: stipends ($25-50/meeting) to recognize expertise and address barriers
    - Orientation: clear meeting norms, role clarity, decision-making authority
    - Frequency: monthly during planning and prioritization phases, quarterly during implementation monitoring

3f. Plan incentive and accessibility strategy
    - In-person event logistics: food, refreshments, childcare, transportation reimbursement (actual cost or flat amount $10-20)
    - Timing: evening and weekend events to accommodate working people; weekday options for shifts
    - Venue accessibility: ADA-compliant, accessible via public transit, free parking
    - Communication access: interpretation (spoken and sign), large print materials, plain language
    - Digital access: survey available in multiple formats, online option for those without internet or computer literacy
    - Engagement incentives: raffle prizes, gift cards, meals, and most importantly: demonstrate that input was heard (feedback loop)


PHASE 4: Data Collection and Analysis Plan
------------------------------------------
4a. Identify quantitative data sources and indicators
    - Primary quantitative data: community survey (target n=400-600 for county-level estimates with subgroup analysis)
    - Secondary quantitative data: census, vital statistics, disease registries, hospital utilization, BRFSS, CDC Wonder, state/county health department reports
    - Indicators: see Phase 2b (organized by domain: mortality, morbidity, risk factors, SDOH, health care access)
    - Equity stratification: all indicators disaggregated by race/ethnicity, income, geography, age, disability, language
    - Data quality review: identify data gaps (e.g., small sample sizes by subgroup), assess reliability

4b. Plan qualitative data collection methods
    - Focus groups: semi-structured, 8-12 participants per group, explore specific health needs, barriers, assets, solutions
    - Key informant interviews: 20-30 min, phone or in-person, targeted questions on specific topics or populations
    - Community survey open-ended questions: capture priorities, lived experience, recommendations (minimize, 2-3 per survey)
    - Focus group recordings: transcript and code using thematic analysis (NVivo, Atlas.ti, or manual coding)
    - CBO partner interviews: asset mapping, gap identification, implementation capacity

4c. Plan data triangulation
    - Convergence: where do quantitative and qualitative data align? (e.g., survey shows high diabetes prevalence, focus groups identify barriers to management)
    - Divergence: where do they differ? (e.g., hospital data shows low maternal mortality, but focus groups highlight maternal mental health crisis)
    - Triangulation matrix: by health need, show quantitative evidence, qualitative evidence, asset data
    - Discrepancy resolution: investigate reasons for disagreement (data quality, population differences, hidden need)

4d. Select analysis framework
    - Social determinants of health (SDOH) framework: organize findings around economic stability, education, social/community context, health care access, neighborhood/physical environment
    - Life course approach: recognize how early exposures shape lifelong health trajectories (ACEs, early childhood education, adolescent health)
    - Health equity framework: center power, privilege, and systemic inequities; disaggregate data; examine root causes (not just risk factors)
    - Upstream thinking: distinguish clinical interventions from SDOH interventions from policy-level interventions
    - Intersectionality lens: recognize that individuals hold multiple identities (race + gender + disability + immigration status) and experience compounded inequities

4e. Plan health needs prioritization methodology
    - Criteria for prioritization (all weighted equally or defined differently by committee):
      * Size/magnitude: how many people affected? (prevalence, incidence)
      * Severity: morbidity and mortality impact (DALYs, YLLs)
      * Disparities: health equity impact (is this need worse for certain populations?)
      * Community concern: what does community prioritize? (survey, focus groups, CAB voting)
      * Feasibility: are there evidence-based solutions? Can hospital and partners implement?
      * Existing resources: what partnerships and assets exist to address?
      * Alignment: does this align with hospital's mission and strategic direction?
    - Prioritization methodology: Hanlon method (impact×(confidence+readiness) = priority), multi-criteria scoring matrix, or community voting + clinician input
    - Process: transparent scoring, documented deliberation, community advisory board involvement in ranking
    - Output: 3-5 prioritized health needs (too many dilutes focus; too few may miss equity opportunity)

4f. Plan SDOH vs. clinical needs distinction
    - Clinical needs: conditions that require medical diagnosis and treatment (diabetes, hypertension, depression)
    - SDOH needs: underlying conditions that prevent health (poverty, food insecurity, unstable housing, lack of transportation, social isolation, discrimination)
    - Integration: recognize that clinical and SDOH needs are interconnected; prioritization should address both
    - Hospital role: clinical interventions vs. community partnerships for SDOH (hospital may not be best provider of housing solutions, but can fund/partner with agencies)


PHASE 5: Health Need Prioritization Framework
----------------------------------------------
5a. Define prioritization criteria and weighting
    - Magnitude: size of population affected (0-25 points)
    - Severity: health impact (mortality, morbidity, QOL) (0-25 points)
    - Health equity impact: disproportionate impact on marginalized groups (0-25 points)
    - Community concern: how much does community prioritize this? (0-15 points)
    - Feasibility: evidence-based solutions exist and are implementable (0-10 points)
    - Total possible: 100 points; define scoring guidance for each criterion
    - Weighting: can adjust (e.g., give health equity 40% weight if that's organizational value)

5b. Establish prioritization committee
    - Multi-stakeholder: 8-12 people, representing hospital leadership, clinicians, community members, public health, CBOs
    - Community voice: majority should be community members with lived experience (including CAB members)
    - Diverse expertise: primary care, public health, behavioral health, social services
    - Clear decision authority: who decides if committee is advisory or has final say?

5c. Facilitate prioritization process
    - Education: review all identified health needs, data summary, evidence
    - Individual scoring: each committee member scores each need against criteria (blind, then reveal)
    - Discussion: deliberate on scores, ask for reasoning, surface priorities
    - Iteration: revise scores if new information emerges from discussion
    - Final ranking: 3-5 top needs emerge (consensus, majority vote, or weighted average?)
    - Equity check: are top needs addressing disparities or perpetuating focus on majority population?

5d. Document rationale for prioritization
    - For each prioritized need: why was it ranked high? What data and stakeholder input supported ranking?
    - For needs not prioritized: why were they ranked lower? (transparency reduces community tension)
    - Equity lens: explain how prioritization addresses health disparities and centers marginalized voices
    - Connection to assets: for each prioritized need, identify existing community assets and partnerships

5e. Plan for implementation strategy development (see Phase 6)
    - For each prioritized need: what evidence-based strategies exist?
    - What does hospital do? What do community partners do?
    - What new partnerships are needed?
    - What are timeline and resource implications?


PHASE 6: Implementation Strategy Development
---------------------------------------------
6a. For each prioritized health need, develop strategy components
    Need: [Name]
    - Goal: specific, measurable outcome (e.g., increase colorectal cancer screening rate from X% to Y% by 2029)
    - Root causes addressed: why does this need exist? (e.g., lack of awareness, access barriers, language, insurance, discrimination)
    - Strategies: multi-level interventions
      * Clinical strategies: e.g., implement colorectal cancer screening in primary care, partner with gastroenterologists
      * System/access strategies: e.g., affordable transportation, appointment scheduling in multiple languages, insurance navigation
      * Community/SDOH strategies: e.g., community education, partner with CBOs for outreach
      * Policy strategies: e.g., advocate for expanded Medicaid coverage, address implicit bias in clinical settings
    - Partners and roles: who leads, who partners, who funds?
    - Timeline: phased rollout (e.g., pilot in one clinic, expand to all by year 2)
    - Resources: budget, staffing, technology, training
    - Metrics: process (e.g., screening offered) and outcome (e.g., screening rate) measures
    - Health equity integration: how does strategy address disparities? Disaggregated metrics by race, income, geography

6b. Ensure strategies address root causes and not just symptoms
    - Symptom: high diabetes prevalence in low-income neighborhood
    - Root cause (SDOH): food insecurity, lack of affordable healthy food access, unsafe neighborhoods for physical activity
    - Symptom-level strategy: diabetes education and medication management
    - Root cause strategy: partner with food bank on food-as-medicine program, fund community garden, improve neighborhood safety for walking
    - Integration: address both symptom and root cause; measure both clinical and social outcomes

6c. Identify necessary partnerships
    - Community health centers: primary care capacity, SDOH expertise
    - Specialty providers: if hospital doesn't have in-house expertise (e.g., colorectal surgery)
    - CBOs: trusted relationships with priority populations, expertise in social services
    - Public health department: epidemiology, infectious disease, maternal child health
    - Schools and universities: research partnerships, student engagement
    - Faith-based and civic organizations: community reach, mobilization capacity
    - Government agencies: housing, education, workforce, criminal justice
    - Philanthropic partners: funding for implementation

6d. Define implementation metrics and monitoring plan
    - Process metrics: # of screening offered, # of education sessions, # of people enrolled in program
    - Outcome metrics: % of eligible people who completed screening, diabetes HbA1c control rate, food insecurity among clients
    - Health equity metrics: stratified by race/ethnicity, income, geography to track if disparities are narrowing
    - Data source: hospital EHR, administrative data, survey, partner data sharing
    - Monitoring frequency: quarterly review of metrics, annual deep-dive analysis
    - Accountability: who reports on progress, to whom, how often?

6e. Align implementation with hospital's community benefit reporting
    - Document how each strategy aligns with IRS Form 990 Schedule H (community benefit schedule)
    - Track direct provision (hospital delivers service), financial assistance (hospital funds external provider), community building (partnerships, advocacy)
    - Ensure CHNA-driven strategies appear prominently in community benefit annual report
    - Create feedback loop from community benefit tracking back to CHNA monitoring


PHASE 7: Report Structure and Communication
--------------------------------------------
7a. IRS-compliant report structure
    - Title: [Hospital Name] Community Health Needs Assessment, [Year]
    - Executive summary (2-3 pages): key findings, prioritized health needs, implementation strategy
    - Community profile: demographics, health status, SDOH indicators (with equity stratification)
    - Community engagement process: methods, participants, input summary
    - Identified health needs: all needs (not just prioritized) with supporting data
    - Prioritized health needs: detailed narrative, data, and rationale for each of 3-5 needs
    - Implementation strategy: for each prioritized need, goals, strategies, timeline, resources, metrics
    - Data sources and limitations: transparency about what data was used, reliability, gaps
    - Appendices: survey instrument, focus group guide, CAB member list, detailed data tables
    - Board resolution: formal adoption by hospital board
    - IRS requirements met: checklist showing compliance with §501(r)(3)

7b. Plain language summary
    - 2-4 pages, reading level 8th grade
    - Eliminate jargon; use concrete examples and visuals
    - Highlight findings most relevant to community
    - Explain what "health need" means in accessible language
    - Show what community input was heard
    - Clearly state prioritized health needs and hospital's plans
    - Include call-to-action: how can community stay engaged during implementation?

7c. Data visualization strategy
    - Demographic profile map: age, race/ethnicity, income (invoke dataviz-planner for guidance)
    - Health disparities map: mortality, morbidity by geography and race/ethnicity
    - Health needs ranking: visual comparison of scores and criteria
    - Implementation timeline: Gantt chart of strategies and milestones
    - Community engagement summary: # of surveys, focus groups, events; demographic representation
    - Asset map: overlay of community resources on health needs map
    - Accessibility: every chart in text summary, high contrast colors, cultural relevance (colors, imagery)

7d. Community-accessible formats and distribution
    - Languages: top 5-10 community languages
    - Formats: PDF (accessible, searchable), HTML (screen reader compatible), large print (16pt), plain language summary, infographic summary, video summary (with captions and interpretation)
    - Distribution channels:
      * Hospital website (prominent placement, easily downloadable)
      * Community partners: CBOs, health centers, libraries, community centers
      * Social media: Twitter, Facebook, Instagram with key findings
      * Public media: community radio, ethnic media
      * Government: submit to state health department, local health department, city/county officials
      * Community forums: present findings, provide feedback form for ongoing input
    - Accessibility: ensure website is ADA-compliant, test with screen readers, gather community feedback on comprehension

7e. Board presentation plan
    - Presentation outline: why CHNAs matter, process conducted, key findings, prioritized needs, implementation strategy, resource implications
    - Duration: 30-45 min + Q&A
    - Visual aids: data visualizations, photos/video from community engagement, quotes from community input
    - Speaker: community member + hospital leader (co-present to reinforce community partnership)
    - Materials: one-page fact sheet for board members, full report as reference
    - Discussion: ask board for strategic questions, feedback, formal motion to adopt
    - Approval: board resolution documenting adoption of assessment and implementation strategy

7f. Public posting requirements
    - Timing: post to website within 5 business days of board adoption
    - Content: full CHNA report + implementation strategy + board resolution
    - Metadata: title, date, version control (if updated)
    - Permanence: keep posted indefinitely (not behind login)
    - Format: at least PDF, preferably multiple formats
    - Accessibility: ADA-compliant HTML version, plain language summary
    - Link placement: prominently on hospital homepage or community benefit page
    - Transparency: document where report is posted, how it's promoted


PHASE 8: Equity Throughout
---------------------------
8a. Health equity lens at every phase (invoke health-equity-analyzer)
    - Phase 1: Are underserved populations' interests represented in scope and stakeholder selection?
    - Phase 2: Are data disaggregated by race, ethnicity, income, geography? Are disparities visible?
    - Phase 3: Are engagement methods actively reaching marginalized populations or only those with privilege?
    - Phase 4: Are analysis frameworks centered on systemic inequity and root causes (not individual risk factors)?
    - Phase 5: Does prioritization address equity or perpetuate focus on majority population needs?
    - Phase 6: Do strategies address root causes of inequity or just clinical symptoms? Are SDOH priorities clear?
    - Phase 7: Does report and communication center community voice, especially from historically excluded groups?
    - Phase 8: Is commitment to equity demonstrated in resource allocation and accountability?

8b. Disaggregated data by race/ethnicity, income, geography
    - Collect data: all surveys and data sources should capture race/ethnicity, income, zip code at minimum
    - Analysis: report all indicators stratified by demographic groups, not aggregated
    - Visualization: disparity maps showing where inequities are concentrated
    - Interpretation: explicitly name inequities (e.g., "Black residents have 2x mortality rate of white residents")
    - Avoid: "comparing to state average" without naming group disparities; colorblind analysis

8c. Community voice centering
    - Composition: >50% of planning committee and CAB should be community members with lived experience
    - Decision-making: community members have vote in prioritization, not just input
    - Compensation: pay community members for their expertise and time
    - Framing: avoid "vulnerable population" language; use "priority population," "historically excluded," "those with lived experience"
    - Feedback loop: systematically report back to community on how their input shaped findings and priorities
    - Accountability: if community priorities conflict with hospital priorities, explicitly address and explain decision

8d. Power analysis: whose voices are amplified/marginalized?
    - Hospital perspective: hospital leadership and clinicians have institutional power and resources; frame findings from that lens
    - Community perspective: specific community groups may have more/less access to table (e.g., homeless individuals, migrant workers, undocumented immigrants, formerly incarcerated)
    - CBO perspective: trust broker organizations may speak for community without representative structure
    - Data perspective: what gets counted and measured reflects prior power (e.g., hospitalizations tracked, homelessness hidden)
    - Deliberate action: proactively reach marginalized voices, compensate for representation gaps, make power dynamics explicit

8e. Historical context of health disparities
    - Systemic racism: redlining, segregation, discriminatory policies that created neighborhoods with poor health outcomes
    - Environmental racism: toxic facilities, pollution, food deserts in communities of color
    - Medical racism: historical trauma (slavery, medical experimentation), ongoing discrimination in health care
    - Economic inequity: wealth gaps, employment discrimination, unaffordable health care
    - Immigration enforcement: stress, fear, barriers to care, family separation
    - Criminal justice inequity: incarceration, reentry barriers, police violence, food insecurity during incarceration
    - Indigenous context: if serving Native American communities, acknowledge historical dispossession, health disparities, sovereignty
    - Contextualize: explain that current health disparities are not individual failures but results of systemic inequities


PHASE 9: Implementation Tasks (Ordered Timeline)
-------------------------------------------------
Month 1: Project Setup
  [ ] Finalize CHNA scope, service area geography, timeline, budget
  [ ] Hire CHNA project lead (internal or consultant)
  [ ] Convene internal planning committee (hospital leadership, key clinicians)
  [ ] Regulatory compliance review (IRS requirements, state reporting requirements)
  [ ] Literature review: national CHNA best practices, health equity frameworks

Month 2: Stakeholder Engagement & Data Design
  [ ] Recruit community advisory board members (8-12, majority community voice)
  [ ] Hold CAB orientation meeting: CHNA purpose, process, meeting norms, compensation
  [ ] Finalize community profile data sources and indicators
  [ ] Design community engagement methods (survey, focus groups, forums) with health equity lens
  [ ] Identify and partner with CBOs for outreach and trust-building
  [ ] Create community survey (or adapt validated instrument)
  [ ] Identify language access needs and secure interpretation/translation

Month 3: Community Engagement Begins
  [ ] Distribute community survey (target n=400-600, oversample underrepresented populations)
  [ ] Recruit focus group participants through CBO partners
  [ ] Identify and schedule key informant interviews
  [ ] Promote listening sessions and community forums via trusted channels

Month 4: Qualitative Data Collection
  [ ] Conduct 4-6 focus groups (1.5-2 hours each)
  [ ] Complete 20-30 key informant interviews
  [ ] Host 3-5 community listening sessions/forums
  [ ] Close community survey (continue to accept late responses)
  [ ] Begin data transcription and analysis (qualitative coding, thematic analysis)

Month 5: Data Analysis & Asset Mapping
  [ ] Analyze survey data: descriptive statistics, disaggregate by demographics, identify disparities
  [ ] Code and analyze focus group and interview data
  [ ] Triangulate quantitative and qualitative findings
  [ ] Complete asset mapping: inventory of community resources, partnerships
  [ ] Create disparity maps and visualizations
  [ ] CAB meeting: review preliminary findings, provide feedback

Month 6: Needs Assessment & CAB Deliberation
  [ ] Compile all identified health needs (10-15 needs identified)
  [ ] Present data summary to internal and CAB committees
  [ ] CAB meeting: detailed discussion of each health need, rationale for prioritization
  [ ] Facilitate multi-stakeholder prioritization process using agreed methodology
  [ ] Score and rank health needs (target 3-5 priority needs)
  [ ] Document prioritization rationale (especially equity considerations)

Month 7: Implementation Strategy Development
  [ ] For each prioritized need, convene working groups (hospital + community partners)
  [ ] Evidence review: what evidence-based strategies exist?
  [ ] Draft implementation strategy (goals, strategies, timeline, resources, metrics, partners)
  [ ] Align strategies with hospital's strategic plan and community benefit reporting
  [ ] Identify funding sources and budget requirements
  [ ] CAB meeting: review draft implementation strategies, provide feedback

Month 8: Report Development & Board Preparation
  [ ] Write full CHNA report (community profile, engagement process, identified needs, priorities, implementation strategy, data appendix)
  [ ] Develop plain language summary and infographics
  [ ] Create data visualizations and disparity maps (work with dataviz-planner)
  [ ] Develop community-facing materials (social media, flyers, video summary)
  [ ] Prepare board presentation deck
  [ ] Draft board resolution for adoption
  [ ] Share draft report with CAB for final feedback

Month 9: Board Adoption & Public Communication
  [ ] Present CHNA to hospital quality/community benefit committee
  [ ] Present CHNA to hospital board; seek formal motion to adopt assessment and implementation strategy
  [ ] Board approval and resolution signature
  [ ] Post full report to website (within 5 business days of adoption)
  [ ] Distribute plain language summary to community partners, libraries, government agencies
  [ ] Press release / community announcement
  [ ] Thank and debrief community advisory board members
```
