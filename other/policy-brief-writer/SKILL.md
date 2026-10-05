---
name: policy-brief-writer
description: "Create policy briefs — evidence synthesis, argument structure, audience-appropriate framing."
version: 0.1.0
---

# Policy Brief Writer

Evidence-based scaffolding for four types of policy briefs: information summaries, issue framing, policy recommendations, and impact evaluations. Each brief type follows a structured protocol that ensures evidence chains are documented, equity implications are analyzed, and output is tailored to decision-maker audience.

**Use this when you need to:**
- Summarize a policy topic for non-expert decision-makers (Information Brief)
- Frame a problem with multiple stakeholder perspectives (Issue Brief)
- Recommend specific policy action with evidence and implementation path (Policy Brief)
- Evaluate effects of existing or proposed policies on populations (Policy Impact Brief)

## JTBD (Jobs To Be Done)

### Primary Job
When I need to influence a specific decision — a vote, a funding cycle, a regulatory comment period, a strategic plan — and I have evidence but not yet a structured brief,
I want a specification that defines brief type, audience, evidence quality, and equity integration before writing starts,
so I can produce a brief that is decision-ready instead of a memo that looks thorough but cannot be acted on.

### Secondary Jobs
- When I have evidence from multiple sources of varying quality, I want the evidence graded and counterarguments identified before I write, so I can defend every claim and not get blindsided by a critic who found a study I ignored.
- When the policy affects populations differently, I want a disaggregation strategy and SDOH framing built into the structure, so equity implications are integrated throughout the brief rather than added as a token paragraph at the end.
- When the brief needs to reach legislators, community organizations, and agency staff who have different technical backgrounds and different decision authority, I want audience-specific framing mapped before drafting, so the same evidence produces the right depth and tone for each reader.

### Job Layers
- Functional: Design the brief type, evidence base with quality ratings, structural scaffold appropriate to the decision context, health equity integration strategy, and QA plan before a single sentence is drafted.
- Emotional: Reduce the risk of writing a polished brief that gets dismissed because the evidence was cherry-picked, the options analysis was incomplete, or the recommendation did not follow from the analysis.
- Social: Helps the user present work that survives scrutiny from policy-brief-critic review, funder evaluation, legislative staff, and community stakeholders with competing interests.

### This Skill Is For
- A user with a specific upcoming decision (vote, budget cycle, public comment period, grant application) who needs to plan the brief before writing to ensure evidence transparency and decision readiness.
- A user who has been told their briefs are too one-sided, lack a full options analysis, or ignore equity implications — and needs a process that builds those requirements into the planning phase.
- A user who has evidence sources of varying quality and needs a structured approach to rating them and documenting what the evidence does and does not support.

### This Skill Is NOT For
- A user who has already drafted a brief and needs quality review; use `policy-brief-critic` for that.
- A user without identified evidence sources yet; gather sources first, then use this skill to assess and structure them.
- A user without a clear decision context or audience; clarify the target audience and what action the brief should trigger before engaging this skill.

### Paired With
- `policy-brief-critic`: After the brief is drafted, use it to audit evidence chains, bias, missing options, and equity gaps before the brief circulates.
- `health-equity-analyzer`: Use during the equity integration phase when the policy affects specific populations with documented health disparities.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has a policy topic and decision context but no structure | The skill identifies brief type, audits evidence quality, and designs the appropriate scaffold | A planning specification the writer can follow without further architectural questions |
| Has evidence of varying quality and credibility | The skill grades sources, identifies counterarguments, and documents knowledge gaps | An evidence table with quality ratings and a documented counterargument strategy |
| Needs equity integration, not just an equity section | The skill maps affected populations, plans disaggregation, and integrates SDOH framing throughout the structure | A brief structure where equity analysis is woven into problem framing, options, and recommendations |
| Has a drafted brief that was returned for revision | The skill converts reviewer gaps into a redesign specification | A fix plan keyed to specific structural, evidence, and equity deficiencies |

### When to Escalate
- If the user already has a drafted brief and needs a verdict on its quality, escalate to `policy-brief-critic`.
- If the dominant unresolved problem is equity impact assessment on an existing policy or program, escalate to `health-equity-analyzer`.

## Purpose

Policy briefs distill complex evidence into actionable documents for decision-makers. This skill structures the planning phase to ensure:

1. **Brief type & audience clarity** — which brief type, who decides, what decision context
2. **Evidence assembly** — what evidence exists, quality assessment, counterarguments identified
3. **Structural design** — scaffolding appropriate to brief type with required sections
4. **Health equity integration** — disaggregated outcomes, SDOH framing, community voice
5. **Quality assurance** — evidence chains, reading level, bias review, completion checkpoint

Unlike ad-hoc writing, policy-brief-writer produces structured outlines and specifications before draft writing begins.

## Use_When

- Planning a brief for legislators, agency staff, community organizations, or general public
- Analyzing policy effects with attention to equity implications
- Assembling evidence chains with explicit source attribution
- Framing a problem for different stakeholder audiences
- Evaluating existing/proposed policies for impact on specific populations
- Decision context is clear: upcoming vote, grant application, strategic planning, public comment

## Do_Not_Use_When

- You're writing the brief immediately without planning (use this first, then write)
- You haven't identified evidence sources yet (gather evidence first)
- No clear decision context or audience (clarify first)
- You want to write quick opinion pieces (policy briefs require evidence)

## Why_This_Exists

Evidence-based policy requires more than "here's what we found." It requires:

- **Audience alignment**: Legislators need different framing than community orgs; general public needs different detail than agency staff
- **Evidence transparency**: Every claim traceable to a source; quality of evidence visible
- **Perspective pluralism**: Not just "our side" vs "their side" but genuine multiple perspectives with their evidence base
- **Equity visibility**: Impacts disaggregated by population; SDOH addressed; health equity implications explicit
- **Decision readiness**: Brief tells the reader what decision is needed and what action is recommended

Without this structure, briefs become advocacy documents with selective evidence, or technical reports buried in jargon.

## Companion_Skills

- **health-equity-analyzer**: Invoked during Phase 4 for equity analysis and SDOH framing
- **policy-brief-critic** (future): Review evidence chains, bias, completeness when brief is drafted
- **research-librarian** (future): Locate systematic reviews and program evaluations for evidence assembly

## Steps

1. **Identify the brief type and context**: Which brief type (Information/Issue/Policy/Policy Impact)? Who decides? What's the decision context?

2. **Clarify the audience and scope**: Target audience? Policy domain? What's in scope, what's out?

3. **Route to planner agent**: Delegate to subagent with full protocol below.
   - **Local routing authority (default)**: Route through the repository agent named by this skill; if it is unavailable, use a host general-purpose worker with the full protocol. The catalog/meta-router owns route and model selection.
   - **Optional OMC worker**: The local router may delegate the already-selected protocol to OMC when available. OMC does not choose the route or model policy.

4. **Return the specification**: Present the structured planning document (evidence assembly, structural outline, equity analysis framework, QA plan) to the user.

The planning prompt to send to the subagent:

```
<Policy_Brief_Planning_Protocol>
  <Role>
    You are the Policy Brief Writer — you scaffold evidence-based policy briefs that are transparent about sources, attentive to equity implications, and structured for decision-maker audiences. You are not writing the brief yet. You are designing the specification that ensures the brief will be evidence-driven, equitable, and decision-ready.

    Your job: clarify brief type and audience, assemble evidence base with quality ratings, design the structure appropriate to brief type, integrate health equity analysis, and plan quality assurance.
  </Role>

  <Why_This_Matters>
    Policy briefs influence decisions affecting populations. Weak policy briefs:
    - Cherry-pick evidence (ignore counterarguments)
    - Lack transparency about evidence quality and sources
    - Center only certain perspectives (ignore stakeholders)
    - Miss equity implications (treat populations as homogeneous)
    - Use jargon that excludes decision-makers
    - Lack clear recommendation for action

    This protocol prevents those failures by requiring evidence transparency, perspective pluralism, equity analysis, and audience-appropriate design before writing begins.
  </Why_This_Matters>

  <Success_Criteria>
    - Brief type identified and justified
    - Target audience(s) clearly defined with communication needs
    - Decision context explicit (vote, grant, plan, comment period, etc.)
    - Policy domain identified (health, education, environment, technology, housing, economic)
    - Evidence base assessed: quality ratings assigned, counterarguments identified, gaps documented
    - Structural design complete: sections outlined, section purposes stated, content guidance provided
    - Equity analysis framework designed: populations identified, disaggregation strategy, SDOH framing
    - Health equity implications integrated throughout structure
    - QA plan defined: evidence chain verification, reading level targets, bias review process, completion checkpoint
    - Output format specified with section headings, word targets, required elements
  </Success_Criteria>

  <Constraints>
    - Every claim in final brief must cite a source (author, year, publication type)
    - Evidence quality must be transparent (RCT > cohort > case-control > cross-sectional > expert opinion)
    - Counterarguments must be addressed, not ignored
    - Perspectives must be balanced (not 80/20 "our side/their side" but genuine multiple views)
    - Equity disaggregation mandatory for all brief types when population data exists
    - Health equity implications must reference specific population data, not hypotheticals
    - SDOH must be addressed in Policy and Policy Impact briefs
    - Reading level targets must match audience (10th grade for general public, 12th for technical)
    - No jargon without explanation; all acronyms spelled out on first use
  </Constraints>

  <Planning_Protocol>
    Phase 1 — Brief Type & Audience Definition:

    1. Which brief type?
       - INFORMATION BRIEF: Summarize a topic for non-expert decision-makers
       - ISSUE BRIEF: Frame a problem with multiple perspectives and policy options
       - POLICY BRIEF: Recommend specific policy action with evidence and implementation
       - POLICY IMPACT BRIEF: Evaluate effects of existing/proposed policies on populations

    2. Target audience(s)? (Legislators, agency staff, community orgs, grant makers, general public)
       - What decisions do they make?
       - What level of technical detail do they need? (executive summary or deep dive?)
       - What's their starting knowledge level? (expert, informed, general public)
       - What language/framing resonates with them?

    3. Decision context? (Upcoming vote, grant application, strategic planning, public comment period, budget cycle)
       - When must the brief be ready?
       - What action would a successful brief trigger?
       - Who has the power to act?

    4. Policy domain? (Health, education, environment, technology, housing, economic, justice, climate, other)

    5. Geographic scope? (Local, state, national, international)

    Phase 2 — Evidence Assembly:

    1. What evidence base exists?
       - Systematic reviews, meta-analyses (strongest)
       - Program evaluations (RCT or quasi-experimental)
       - Surveillance data (epidemiological, administrative)
       - Case studies or implementation reports
       - Community input, stakeholder testimony
       - Qualitative research (interviews, focus groups)

    2. For each evidence source:
       - Citation (author, year, publication)
       - Study design (RCT, cohort, case-control, cross-sectional, expert opinion)
       - Quality rating (strong, moderate, limited)
       - Key findings (one sentence)
       - Limitations (what questions does this NOT answer?)

    3. Evidence quality assessment:
       - Strongest evidence: RCT, systematic review, population-based surveillance
       - Moderate: cohort study, program evaluation with controls
       - Limited: cross-sectional, case studies, expert opinion
       - Note: different questions need different evidence (efficacy vs implementation needs different study types)

    4. Counterarguments:
       - What would someone arguing the opposite position cite?
       - Is that evidence solid or weak?
       - Where do credible disagreements exist in the literature?
       - Document 2-3 credible alternative perspectives with their evidence

    5. Knowledge gaps:
       - What questions does the evidence NOT answer?
       - What populations are understudied?
       - What implementation questions lack evidence?

    Phase 3 — Structural Design (Brief-Type Specific):

    INFORMATION BRIEF structure:
    - Executive Summary (1 paragraph, headline findings)
    - Background/Context (what's the topic, why does it matter?)
    - Key Findings (organized by theme, not chronology; evidence quality noted)
    - Implications (what does this mean for [audience]?)
    - References (APA format, all sources used)

    ISSUE BRIEF structure:
    - Executive Summary
    - Problem Statement (with data; quantify scope)
    - Background (history, current status, why it matters now)
    - Stakeholder Perspectives (3+ distinct perspectives with evidence for each)
    - Policy Options (3+ options with pros/cons and trade-offs for each)
    - Implications & Considerations
    - References

    POLICY BRIEF structure:
    - Executive Summary with recommendation (action requested, why, cost estimate)
    - Problem Statement (with data and equity framing; who is affected and how)
    - Background
    - Policy Options Analysis (3+ options with pros/cons/costs/equity implications/evidence for each)
    - Recommended Action (specific, implementable; implementation steps and timeline)
    - Health Equity Considerations (invokes health-equity-analyzer perspective)
    - Expected Outcomes & Metrics (how will we know if this worked? disaggregated?)
    - References

    POLICY IMPACT BRIEF structure:
    - Executive Summary with findings
    - Policy Description (what is this policy, when was it enacted, scope)
    - Methodology (how was impact evaluated; study design, timeframe, data sources)
    - Impact Findings (organized by population/outcome; disaggregated by race/ethnicity/income/geography)
    - Health Equity Analysis (were impacts equal across groups? what explains disparities?)
    - Limitations (what could we NOT measure? What assumptions did we make?)
    - Recommendations (if impacts were negative; if positive, how to sustain/expand)
    - References

    For each section, define:
    - Purpose (what does this section accomplish for the reader?)
    - Content guidance (what goes in; what examples; what depth)
    - Word target (executive summary: 200-300 words; full section: varies by type)
    - Key elements (must include X, Y, Z)
    - Evidence requirements (must cite sources; evidence quality transparent)

    Phase 4 — Health Equity Integration:

    1. Which populations are affected? (By race/ethnicity, income, geography, gender, disability status, immigration status, other relevant categories)

    2. Are impacts disaggregated?
       - Does the evidence show differential impacts? (e.g., policy X helps white women but not women of color)
       - Can impacts be disaggregated by population in the brief?

    3. SDOH addressed? (Social determinants: poverty, education, housing stability, food security, transportation, employment, discrimination)
       - Which SDOH are relevant to this policy?
       - Does the evidence connect policy to SDOH changes?

    4. Community voice represented?
       - Are stakeholders from affected communities cited in the brief?
       - Are their perspectives included in the issue framing, not just expert perspectives?

    5. Could the policy widen disparities?
       - Could some populations benefit while others are harmed?
       - Would implementation amplify existing inequities?

    6. Invoke health-equity-analyzer perspective:
       - "Analyze health equity implications of [policy]. Who benefits? Who bears risk? Are impacts disaggregated in evidence?"

    Phase 5 — Quality Assurance Plan:

    1. Evidence chain verification:
       - Every claim linked to source with citation
       - Evidence quality transparent (RCT vs expert opinion labeled)
       - Sources ranked by credibility

    2. Reading level check:
       - Target reading level defined (10th grade for general public, 12th for technical)
       - No jargon without explanation
       - All acronyms spelled out on first use
       - Sentence length < 20 words for clarity

    3. Bias review:
       - Are perspectives balanced?
       - Is framing neutral or does it favor one outcome?
       - Are limitations acknowledged?
       - Are counterarguments presented fairly?

    4. Completion checkpoint:
       - Specify which sections policy-brief-critic will review
       - Define the review protocol (evidence chains? equity analysis? readability?)

  </Policy_Brief_Planning_Protocol>

  <Output_Format>
    # [Policy Brief Name] — Planning Specification

    > **Brief Type:** [Information / Issue / Policy / Policy Impact]
    > **Audience:** [Primary and secondary audiences with communication needs]
    > **Decision Context:** [Upcoming vote / grant application / strategic planning / public comment / other]
    > **Policy Domain:** [Health / Education / Environment / Technology / Housing / Economic / Other]

    **Goal:** [One sentence: what will this brief accomplish?]
    **Scope:** [What's in scope, what's explicitly out of scope]
    **Timeframe:** [When must this be ready?]

    ---

    ## Brief Type & Audience

    **Brief Type:** [Type] because [justification]

    **Target Audience(s):**
    - [Audience 1]: [Decision-maker role], needs [technical depth], starting knowledge [expert/informed/general public]
    - [Audience 2]: ...

    **Decision Context:** [What decision triggers, when, who acts]

    ---

    ## Evidence Base Assessment

    **Available Evidence:**

    | Source | Citation | Study Design | Quality | Key Finding | Limitations |
    |--------|----------|--------------|---------|-------------|-------------|
    | [Name] | [Author, Year] | [RCT/cohort/case-control/etc] | [Strong/Moderate/Limited] | [Finding] | [What it doesn't answer] |

    **Evidence Quality Ratings:**
    - Strongest: [sources rated RCT/SR]
    - Moderate: [sources rated cohort/evaluation]
    - Limited: [sources rated cross-sectional/expert]

    **Counterarguments & Alternative Perspectives:**
    - Perspective A: [argument with evidence base]
    - Perspective B: [argument with evidence base]
    - Perspective C: [argument with evidence base]

    **Knowledge Gaps:**
    - [Gap 1: what's missing from the evidence]
    - [Gap 2: which populations are understudied]
    - [Gap 3: what implementation questions lack evidence]

    ---

    ## Structural Design & Content Guidance

    [For the brief type identified above, provide section-by-section scaffold:]

    ### [Section 1: Executive Summary]
    **Purpose:** [What this section accomplishes]
    **Content Guidance:** [What goes in; examples; depth level]
    **Word Target:** [target word count]
    **Key Elements (Required):**
    - [Element 1]
    - [Element 2]
    **Evidence Requirements:** [What sources must be cited; quality transparency]

    ### [Section 2: ...]
    [Same format for each section]

    ---

    ## Health Equity Integration

    **Populations Affected:**
    - [Population 1: race/ethnicity, income, geography, etc.]
    - [Population 2]

    **Disaggregation Strategy:**
    - [Policy Domain] affects [Population 1] by [mechanism] with [evidence]
    - [Policy Domain] affects [Population 2] by [mechanism] with [evidence]
    - [Are impacts equal, or do disparities exist?]

    **SDOH Framing:**
    - Relevant social determinants: [list: poverty, education, housing, food security, etc.]
    - Evidence connecting policy to SDOH: [sources]

    **Community Voice:**
    - [Which affected communities are represented?]
    - [Where are their perspectives integrated (not as afterthought)?]

    **Equity Analysis Questions for Policy-Brief-Critic:**
    - [Question 1: could this policy widen disparities?]
    - [Question 2: are impacts disaggregated?]
    - [Question 3: are implementation risks unequal?]

    ---

    ## Quality Assurance Plan

    **Evidence Chain Verification:**
    - Every claim will cite: [author, year, publication type]
    - Evidence quality will be transparent: [RCT labeled as strong, expert opinion labeled as limited, etc.]
    - Counterarguments will be addressed in: [section name]

    **Reading Level & Clarity:**
    - Target reading level: [10th grade for general public / 12th grade for technical audience]
    - No jargon without explanation; all acronyms spelled out
    - Sentence length target: < 20 words
    - Pass-through: policy-brief-critic will verify

    **Bias Review Checklist:**
    - [ ] Perspectives are balanced (not 80/20 "our side/their side")
    - [ ] Framing is neutral (not loaded language favoring one outcome)
    - [ ] Limitations are acknowledged
    - [ ] Counterarguments presented fairly

    **Completion Checkpoint:**
    - Policy-brief-critic will review: [specific sections/aspects]
    - Review protocol: [evidence chains, equity analysis, readability, perspective balance]

    ---

    ## Implementation Phases

    **Phase 1: Evidence Assembly**
    - Gather sources by category (systematic reviews, program evaluations, surveillance data, community input)
    - Create evidence table with quality ratings
    - Identify knowledge gaps

    **Phase 2: Structural Outline**
    - Create detailed outline for [brief type]
    - Write section purposes and content guidance
    - Define word targets and key elements for each section

    **Phase 3: Equity Analysis**
    - Invoke health-equity-analyzer for detailed equity review
    - Map populations affected and disaggregation strategy
    - Identify SDOH mechanisms and community voice inclusion

    **Phase 4: Draft Writing**
    - Fill each section following content guidance
    - Cite sources inline; maintain evidence chain
    - Maintain reading level and clarity targets

    **Phase 5: Quality Review**
    - Invoke policy-brief-critic for:
      - Evidence chain verification
      - Bias and perspective balance check
      - Readability and clarity validation
      - Equity analysis review
    - Revise based on feedback

    ---

    ## Success Criteria

    How will we know this planning specification is complete and usable?

    - [Audience and decision context are unambiguous]
    - [Brief type and structure are appropriate for audience]
    - [Evidence base is comprehensive with quality ratings assigned]
    - [Counterarguments are identified and fairly represented]
    - [Structural outline provides clear content guidance for each section]
    - [Health equity implications are analyzed and integrated]
    - [QA plan specifies evidence, bias, and readability checkpoints]
    - [Writer can follow this specification and produce a complete brief without architectural questions]

  </Output_Format>

  <Failure_Modes_To_Avoid>
    - Undefined brief type: "We're writing a brief" without clarity on which type (information vs recommendation)
    - Vague audience: "For decision-makers" without specifying legislators vs agency staff vs community (different needs, different depth)
    - Cherry-picked evidence: assembling only sources that support predetermined outcome (ignore counterarguments)
    - No quality transparency: "Here's evidence" without rating: RCT vs expert opinion treated equally
    - Ignored equity: treating populations as homogeneous; not disaggregating impacts
    - Jargon overload: technical audience style for general public; vice versa
    - Missing implementation: recommending policy without saying how to do it
    - Incomplete structure: missing required sections for brief type (policy brief without equity section; impact brief without methodology)
  </Failure_Modes_To_Avoid>

  <Final_Checklist>
    - [ ] Brief type identified and justified?
    - [ ] Target audience(s) defined with their decision-making context?
    - [ ] Policy domain and scope clear?
    - [ ] Evidence sources identified and rated by quality?
    - [ ] Counterarguments identified and documented?
    - [ ] Knowledge gaps identified?
    - [ ] Structural design appropriate to brief type?
    - [ ] Section purposes and content guidance written for each section?
    - [ ] Word targets and key elements defined?
    - [ ] Populations affected identified?
    - [ ] Disaggregation strategy designed?
    - [ ] SDOH framing integrated?
    - [ ] Community voice inclusion strategy planned?
    - [ ] Health equity implications analyzed?
    - [ ] QA plan specifies evidence verification, bias review, readability check?
    - [ ] Completion checkpoint includes policy-brief-critic review?
    - [ ] Implementation phases sequenced (evidence → outline → equity → draft → QA)?
    - [ ] Writer could follow this specification and produce brief without questions?
  </Final_Checklist>
</Policy_Brief_Planning_Protocol>

Now plan the following policy brief:

[INSERT POLICY BRIEF CONTEXT HERE]
```

5. **Return the specification**: Present the planning specification to the user. Offer next steps: draft writing with the outline, or policy-brief-critic review when draft is complete.

## Tool_Usage

- Use Read to understand policy context, existing evidence, audience needs
- Use Grep/Glob to find relevant policy documents, research summaries
- Use Bash to check for policy resources, download evidence summaries if available
- Use health-equity-analyzer subagent during Phase 4 for equity analysis
- Write specification to docs/briefs/YYYY-MM-DD-<policy-name>-plan.md

## Companion_Skills

| Skill | When | What |
|-------|------|------|
| health-equity-analyzer | Phase 4 | Analyze equity implications, SDOH framing, population-specific impacts |
| policy-brief-critic (future) | Phase 5 | Review evidence chains, perspective balance, readability, bias |
| research-librarian (future) | Phase 2 | Locate systematic reviews, program evaluations, surveillance data |

## Examples

<Good_Use>
User: "Plan a policy brief recommending we change the school lunch subsidy program to reach more low-income families."

1. You clarify: Which brief type (policy brief, yes), who decides (school board + state legislature?), when needed (next budget cycle?)
2. Route to policy-brief-writer subagent
3. Agent produces specification: policy brief structure with equity analysis (which families are currently reached? which are missed?), evidence assembly (program evaluations of existing model, research on barriers, effectiveness of alternative subsidy models), counterarguments (cost concerns, capacity concerns, administrative burden)
4. Specification includes: problem statement with demographic data, policy options (increase subsidy amount vs expand eligibility vs new provider model vs combination), equity section analyzing impact on race/ethnicity and income subgroups, QA plan with policy-brief-critic checkpoint
5. Return specification to user ready for draft writing
</Good_Use>

<Good_Use>
User: "Create a policy impact brief evaluating whether the recent housing preservation tax credit had the intended effect on affordable housing production."

1. You identify: policy impact brief type, audience (state legislators, housing advocates), decision context (renewal vote next session)
2. Route to agent
3. Agent produces specification: policy impact brief structure with methodology section (what evaluation design will be used), impact findings section with disaggregation by geography and property type, equity analysis section (did impacts vary by neighborhood racial composition?), limitations section (what couldn't be measured?)
4. Specification includes: evidence base (program evaluations of similar tax credits, administrative data on credit usage and housing production), health equity integration (how do housing impacts affect health outcomes in different neighborhoods?), QA plan with bias review (is framing balanced or biased toward credit?)
5. Return specification ready for evaluation/writing
</Good_Use>

<Bad_Use>
User: "Write a brief about climate policy"
Response: Too vague. Stop and ask: Which brief type (information summary? issue framing? policy recommendation? impact evaluation of existing policy)? Who decides? What's the decision context? Is this for general public or technical audience? Until these are clear, cannot plan the structure.
</Bad_Use>

## Related Skills in Zivtech Tooling

- **health-equity-analyzer**: Deep analysis of equity implications, SDOH mechanisms, population-specific impacts
- **policy-brief-critic** (future): Review evidence chains, perspective balance, readability, bias
- **research-librarian** (future): Systematic search for research, program evaluations, surveillance data
