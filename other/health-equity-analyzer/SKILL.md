---
name: health-equity-analyzer
description: "Review policies, programs, or studies for health equity implications and disparities."
version: 0.1.0
---

# Health Equity Analyzer

Thorough, evidence-driven review of health equity dimensions in any document (research, policy, intervention plan, data visualization, proposal, analysis). This skill evaluates whether the work adequately considers impacts on marginalized populations, acknowledges and measures health disparities, addresses root causes (structural issues), and includes affected communities.

**Use this AFTER reading the document under review.** health-equity-analyzer is not a checklist tool; it's a design reviewer. You're evaluating equity *thinking* in the document, not just compliance with equity language.

## JTBD (Jobs To Be Done)

### Primary Job
When I have an existing policy, program, report, visualization, or study and need to know who it helps, harms, or ignores,
I want an evidence-backed health equity review,
so I can see whether the work genuinely addresses disparities instead of only talking about them.

### Secondary Jobs
- When a document claims equity impact, I want the underlying population logic pressure-tested, so I can tell whether the claim is real.
- When stakeholders worry about unintended consequences, I want the likely equity risks surfaced, so I can revise before harm is amplified.

### Job Layers
- Functional: Audit existing work for population visibility, disparity measurement, structural causes, community voice, and unintended consequences.
- Emotional: Reduce the uncertainty of shipping work that sounds equitable but may reproduce inequity.
- Social: Helps the user explain equity implications clearly to funders, reviewers, communities, and decision-makers.

### This Skill Is For
- A user with an existing artifact who needs a dedicated equity lens before approval or publication.
- A user testing whether equity claims are substantive rather than symbolic.
- A user trying to anticipate who may be excluded, burdened, or invisibilized by the current work.

### This Skill Is NOT For
- A user starting from scratch and needing to design the work first; use `policy-brief-writer` or `chna-planner` instead.
- A user whose main concern is general research methodology rather than equity-specific consequences; use `research-critic` instead.

### Paired With
- `policy-brief-writer`: Use this when the next job is designing an evidence-backed brief with equity integrated from the start.
- `chna-planner`: Use this when the next job is planning a community health needs assessment or intervention workflow with equity built in.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has an existing artifact with equity claims | The skill pressure-tests who is visible, missing, or harmed | A clearer equity risk picture |
| Has concerns about disparities or unintended effects | The skill surfaces structural blind spots and consequence risks | Evidence-backed equity findings |
| Needs to redesign after review | The skill points to the planning path that should happen next | A remediation route |

### When to Escalate
- If the user needs to design a new equity-aware brief or assessment instead of reviewing an existing artifact, escalate to `policy-brief-writer` or `chna-planner`.
- If the dominant issue is overall methodology rather than equity consequences, escalate to `research-critic`.

## Purpose

Standard document reviews may miss equity gaps:
- Data aggregated by demographics but disparities not explicitly discussed
- Populations benefiting/harmed not clearly identified
- Social determinants of health acknowledged but not addressed
- Community involvement mentioned but superficial
- Interventions target individuals, ignoring structural root causes
- Unintended consequences (widening existing disparities) not considered

This critic evaluates health equity *design decisions*:
- Which populations are visible in the analysis? Which are invisible?
- Are health disparities measured meaningfully (rate differences, risk ratios) or obscured?
- Does the work address root causes (structural racism, poverty, policy) or only symptoms?
- Is intersectionality considered (race × income × geography × disability × language)?
- Is data disaggregated by relevant demographic categories?
- Are affected communities truly involved or tokenized?
- Could this policy/intervention inadvertently widen disparities?

## Use_When

- Reviewing research papers for equity framing
- Assessing health policy documents for population impact
- Evaluating intervention designs for equity considerations
- Cross-reviewing health data visualizations for disparity measurement
- Validating proposals for health equity-focused funding
- You need multi-perspective equity validation: affected community ≠ researcher ≠ implementer ≠ funder
- Invoked as a perspective module by another critic (dataviz-critic, research-critic, policy-critic)
- You need to evaluate whether a document genuinely centers health equity or uses equity language superficially

## Do_Not_Use_When

- You need automated compliance checking for equity language — use text analysis tools instead
- You need a health equity glossary/reference — use `health-equity-standards` (future) instead
- You want to make edits to the document — this is read-only (disallowedTools: Write, Edit)
- You haven't read the document yet — read it first
- You need implementation planning for equity improvements — this reviews existing work, not plans interventions
- Reviewing visual design only — use `ui-design-critic` with health-equity perspective instead

## Why_This_Exists

Health equity language is increasingly common, but execution often falls short. Examples:

- Public health report states "disparities exist" but doesn't measure them or explain why (data gap)
- Intervention plan targets "underserved communities" but doesn't disaggregate data — disparities remain invisible in aggregated statistics
- Policy acknowledges structural racism but proposes only individual-behavior-change solutions
- Document claims "community engagement" but shows no evidence of community involvement in design or decision-making
- Data visualization shows differences across racial groups but doesn't contextualize within health equity framework
- Proposal would benefit some populations while inadvertently worsening outcomes for others (unintended consequences unidentified)

This skill surfaces equity design decisions, not compliance with diversity statements.

## Companion_Skills

- **health-equity-standards** (future): Health equity frameworks (Healthy People 2030, WHO Social Determinants, CDC equity definitions), terminology, measurement standards
- **research-critic**: Comprehensive research methodology review where health equity is one of several perspectives; use health-equity-analyzer for deep equity-specific analysis
- **dataviz-critic**: Design review for data visualizations; invokes health-equity-analyzer as a perspective module
- **policy-critic**: Policy document review; invokes health-equity-analyzer for equity impact assessment

## Steps

1. **Identify the target**: Determine which document (research paper, policy brief, intervention plan, data visualization, proposal) needs equity review. If no target provided, ask the user what they want reviewed.

2. **Read the document thoroughly**: Understand the document's purpose, claims, data, methodology, and proposed outcomes.

3. **Route to agent**:
   - **Standalone mode** (primary use): Route to health-equity-analyzer agent with full 8-phase protocol
   - **Perspective module mode** (invoked by another critic): Generate focused equity section without full report structure

4. **Invoke the health-equity-analyzer subagent**:
   - **Local routing authority (default)**: Route through the repository agent named by this skill; if it is unavailable, use a host general-purpose worker with the full protocol. The catalog/meta-router owns route and model selection.
   - **Optional OMC worker**: The local router may delegate the already-selected protocol to OMC when available. OMC does not choose the route or model policy.

5. **Return findings**: Present structured verdict to user with all findings, gaps, and specific equity improvements.

## Perspective_Module_Mode

When invoked by another critic (e.g., `dataviz-critic` requesting equity analysis of a visualization), produce a focused section:

```
**Health Equity Lens:**

- **Populations served/harmed/invisible**: [Identify which populations the work benefits, harms, or makes invisible in analysis]
- **Disparity measurement**: [Is this adequate, insufficient, or absent? Are meaningful comparisons made?]
- **SDOH coverage**: [Which social determinants are addressed? Which are absent?]
- **Data disaggregation**: [Is data broken down by relevant demographics? Or are disparities hidden in aggregates?]
- **Intersectionality**: [Are intersecting identities considered, or is analysis siloed by single demographics?]
- **Community voice**: [Present/absent/tokenized? Evidence of involvement in design, data collection, interpretation?]
- **Unintended consequences**: [Could this inadvertently widen disparities? Create new barriers?]
- **Equity strength**: [1-2 sentence assessment of equity framing]
- **Equity recommendation**: [1-3 specific, actionable improvements]
```

Return this section to the requesting critic without a full standalone review structure.

## Full_Review_Context

See embedded agent.md file for complete 8-phase review protocol:
- Pre-commitment equity predictions
- Population impact audit
- Disparity measurement audit
- Social determinants coverage audit
- Data disaggregation audit
- Community voice assessment
- Unintended consequences analysis
- Realist Check (severity calibration)
- Self-audit
- Synthesis

## Tool_Usage

When invoking health-equity-analyzer:
- Use Read to load the document under review and ALL referenced source materials (studies, data, policy references)
- Use Grep to verify claims about populations, disparities, SDOH coverage in the document
- Use Bash with git to verify document history, recent changes, citations
- Read context around referenced studies/data — understand the full equity picture, not isolated statistics

## Severity_Scale_For_Health_Equity

- **CRITICAL**: Document actively harmful to marginalized populations. Reinforces harmful stereotypes without structural context. Ignores known health disparities in a way that could worsen outcomes. Uses deficit framing without addressing root causes. Example: intervention targeting "obesity in Black communities" without acknowledging food access/environmental factors.

- **MAJOR**: Significant equity blind spots. Populations invisible in data. SDOH coverage incomplete. No community voice in decision-making. Aggregated data obscures disparities. Unintended consequences not identified. Example: intervention plan claims to address disparities but doesn't disaggregate outcomes data by race/ethnicity.

- **MINOR**: Surface-level equity mentions without depth. Missing intersectional analysis. Terminology improvements needed. Incomplete SDOH coverage. Example: document mentions "health equity" but analyzes all populations together without disaggregation.

- **ENHANCEMENT**: Equity framing adequate but could be strengthened. No access barriers but misses opportunities for deeper equity integration. Example: document disaggregates data but doesn't contextualize disparities within structural framework.

## Frameworks_Referenced

Every finding should ground in recognized health equity frameworks:
- **Healthy People 2030**: Social Determinants of Health framework (economic stability, education access, healthcare access, neighborhood & physical environment, social & community context)
- **WHO Social Determinants**: Structural vs. intermediary determinants; social gradients in health outcomes
- **CDC Health Equity Definition**: "The state in which every person has the opportunity to attain his or her highest level of health" — requires addressing root causes, not just individual behavior
- **Intersectionality**: Acknowledging that people hold multiple identities simultaneously; health disparities result from intersection of these identities + structural systems

## Output_Modes

**Standalone review** (default):
- Full structured report with Pre-commitment Predictions, Critical/Major/Minor Findings, What's Missing, Multi-Perspective Notes, Verdict

**Perspective module** (invoked by another critic):
- Focused "Health Equity Lens" section appended to requesting critic's output
- No standalone verdict; findings integrated into parent review

## Examples

<Good_Use_Standalone>
User: "Review this public health intervention plan for health equity considerations."
1. You read the 20-page intervention plan
2. Invoke health-equity-analyzer agent with full protocol
3. Reviewer checks: population impact, disparity measurement, SDOH coverage, community involvement, unintended consequences
4. Finds: intervention targets "high-risk neighborhoods" without disaggregating by race/ethnicity; SDOH coverage incomplete (healthcare access addressed, economic stability not); community voice absent from design
5. Returns structured verdict with MAJOR findings, gaps, and specific recommendations

**Expected output**: Full review report with Pre-commitment Predictions, Critical/Major/Minor Findings, What's Missing, Multi-Perspective Notes (affected community, researcher, implementer, funder perspectives), Verdict Justification.
</Good_Use_Standalone>

<Good_Use_Perspective_Module>
Dataviz-critic: "Please review this health disparities visualization through a health equity lens for equity gaps"
1. You read the visualization (chart showing mortality rates by race/ethnicity)
2. Invoke health-equity-analyzer agent in perspective mode
3. Reviewer evaluates: Which populations visible? Are disparities measured meaningfully? Context provided? Data quality disclosed?
4. Returns focused equity section (not full review) identifying: "Disparities clearly visualized, but root causes not contextualized. SDOH factors not layered in. Community voice about data interpretation absent."
5. Dataviz-critic integrates this into its output as the equity perspective
</Good_Use_Perspective_Module>

<Bad_Use>
User: "This policy document is harmful. Tell me how to fix it."
Response: "health-equity-analyzer reviews existing documents; it doesn't create policy. If you want to plan equity improvements, let's discuss what specific equity gaps you've identified. Would you like me to do an equity review first?"
</Bad_Use>

## Companion_Skills_and_Integration

| Skill | Role | Integration |
|-------|------|-------------|
| research-critic | Methodology review | health-equity-analyzer as perspective module |
| dataviz-critic | Data visualization design | health-equity-analyzer as perspective module |
| policy-critic | Policy document review | health-equity-analyzer as perspective module |
| health-equity-standards | Health equity frameworks/reference | Citation source for findings |

---

## Benchmark_Test_Info

**Last updated**: 2026-03-09
**Test methodology**: Blinded equity review of public health documents (n=5)
**Baseline**: health-equity-analyzer prototype
**Metrics tracked**:
- Populations identified (visible/invisible/harmed)
- SDOH coverage gaps identified
- Data disaggregation gaps detected
- Unintended consequences flagged
- Community voice assessment accuracy
- Evidence quality (backtick quotes, citations)

**Key calibration**: Gap analysis surfaces 8-12 equity gaps per document vs 2-3 without structured protocol.
