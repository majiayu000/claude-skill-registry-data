---
name: impact-report-planner
description: "Plan impact reports — evidence structure, narrative, metrics, stakeholder alignment."
version: 0.1.0
---

# Impact Report Planner

Planner skill for structuring annual impact reports *before* writing them.

Use this skill to plan reports that tell compelling impact stories, select meaningful metrics (not vanity metrics), represent beneficiaries respectfully, and reach the right audiences with the right versions.

## JTBD (Jobs To Be Done)

### Primary Job
When I need to produce an annual impact report and I have program data, financial records, and outcomes metrics but no clear plan for what to measure, whose story to tell, or how to reach funders and the board,
I want a structured impact report design plan before writing starts,
so I can build a coherent impact story instead of assembling whatever data is available at deadline and hoping it adds up to something credible.

### Secondary Jobs
- When I have both output metrics (meals served, clients enrolled, events held) and outcome metrics (health improvements, income changes, housing stability), I want help distinguishing which metrics actually measure impact versus which just measure activity, so the report makes a defensible case for continued funding rather than padding word count with vanity numbers.
- When the report must reach multiple audiences — funders who need ROI language, board members who need governance-level summaries, community members who need to see themselves reflected — I want a version strategy mapped before drafting, so I am not rewriting the same data for four different audiences after the fact.
- When my program data is disaggregated by race, income, geography, or disability status and the aggregate numbers hide disparities, I want a plan that surfaces population-specific outcomes prominently, so the report does not present a false picture of who is and is not being reached.
- When beneficiary stories are central to the report but I have not yet planned consent, representation, or selection criteria, I want a story collection plan before fieldwork starts, so I avoid both tokenism and last-minute scrambling for usable quotes.

### Job Layers
- Functional: Design the metric selection strategy, narrative arc, audience version map, equity disaggregation plan, beneficiary story collection protocol, financial transparency structure, and distribution plan that together make the report credible and actionable before a single paragraph is written.
- Emotional: Replace the annual panic of assembling a report reactively from whatever data exists with a proactive plan that makes the report a genuine accountability document rather than a marketing exercise.
- Social: Helps the user demonstrate organizational rigor to funders, IRS reviewers, and board members by showing that impact measurement was designed intentionally, not reverse-engineered from available data.

### This Skill Is For
- A user planning an annual impact report for a nonprofit, foundation, university department, or government program who wants to design the report before writing it rather than reactively assembling content.
- A user whose previous reports were criticized for leading with activity counts rather than outcomes, for hiding equity gaps in aggregate data, or for lacking financial transparency aligned with IRS 990 or grant requirements.
- A user who needs to serve multiple distinct audiences (funders, board, beneficiaries, public) and wants a differentiated content strategy rather than a single document that satisfies none of them fully.

### This Skill Is NOT For
- A user who has already drafted a report and needs critique; use `copy-critic` or `dataviz-critic` for that.
- A user whose primary unresolved problem is translating findings into audience-appropriate language after the content decisions are made; use `stakeholder-report-writer` for that downstream step.
- A user whose report is primarily a grant proposal narrative rather than an accountability document; use `policy-brief-writer` instead.
- An organization that does not yet have outcomes measurement or program data; design the measurement system first before planning the report.

### Paired With
- `stakeholder-report-writer`: Use after this planning step to design how each audience version translates findings into the right register and format.
- `health-equity-analyzer`: Use when population-specific outcomes require a full equity analysis beyond disaggregation planning.
- `dataviz-planner`: Use to design which metrics get charts, what chart types are appropriate, and how visual design serves the narrative arc.
- `data-planner`: Use when metric calculations, baseline definitions, or year-over-year comparisons need validation before committing to them in the report.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has data but no report structure | The skill designs narrative arc, metric selection strategy, and section-by-section plan | A complete report blueprint a writer can execute without further architectural decisions |
| Has vanity metrics but needs outcome metrics | The skill distinguishes outputs from outcomes and identifies which metrics actually support impact claims | A curated metric set with baseline comparisons and clear rationale for inclusion |
| Serves multiple audiences with different needs | The skill maps audience-specific versions: what each group needs to see, at what depth, through which channel | A version strategy with content differentiation guidance per audience |
| Equity findings are buried in aggregates | The skill plans population-specific disaggregation and identifies where disparities appear prominently in the structure | A report outline that surfaces equity gaps rather than concealing them |
| Needs beneficiary stories but has no collection plan | The skill designs selection criteria, consent protocol, and representation guidance | A story collection plan ready for fieldwork |

### When to Escalate
- If the user already has a drafted report and needs a quality verdict, escalate to `copy-critic`.
- If the downstream problem is audience-specific writing and translation after impact content is chosen, escalate to `stakeholder-report-writer`.
- If the core unresolved problem is a full equity analysis of program outcomes across populations, escalate to `health-equity-analyzer`.

## Purpose

Plan impact reports strategically, not reactively:

- **Know your audiences**: Who reads this? Funders, board, staff, beneficiaries, public? Each needs different content.
- **Select meaningful metrics**: Which metrics actually measure impact? Avoid vanity metrics (raw counts, outputs) in favor of outcomes and efficiency.
- **Plan the narrative arc**: Mission restatement → challenge → approach → outcomes → stories → future outlook
- **Make equity visible**: Disaggregate data by population; prevent disparities from hiding in aggregates
- **Plan data visualization**: Which metrics get charts? Which get narrative? Design principles for clarity.
- **Collect impact stories**: Beneficiary stories, staff spotlights, partner acknowledgments with consent and representation
- **Show financial accountability**: Program expenses, fundraising efficiency, overhead ratios, IRS 990 alignment
- **Plan distribution strategy**: Print, digital, social, funder-specific versions, executive summary, accessibility

This skill produces a detailed plan that guides actual report writing.

## Use_When

- Planning an annual impact report before starting writing (planning vs. reactively assembling content)
- Building reports that need to reach multiple audiences (funders, board, staff, public, beneficiaries)
- You need to select metrics that measure actual impact, not just activity
- Determining what beneficiary stories to collect and how to represent them respectfully
- Creating reports that will be reviewed by board, funders, or regulatory bodies
- You want to disaggregate data by population and make disparities visible
- Ensuring the report includes financial transparency aligned with IRS 990 or grant requirements
- Planning visual design and distribution across print, digital, and social channels

## Do_Not_Use_When

- You've already written the report and want critique (use copy-critic or dataviz-critic instead)
- You need a quick internal-only status report (this is for intentional, public-facing design)
- The report is primarily a grant proposal narrative (use policy-brief-writer instead)
- The organization lacks clear outcomes measurement or impact data

## Companion_Skills

- **stakeholder-report-writer**: Use AFTER planning to write sections of the report for specific audiences
- **copy-critic**: Use to review draft report text for clarity, tone, and narrative flow
- **dataviz-planner**: Use to plan data visualizations within the report (which metrics get charts, chart types, design)
- **data-planner**: Use to ensure metrics are calculated correctly and baseline comparisons are valid
- **policy-brief-writer**: Use if report needs to include policy recommendations alongside impact data

## Steps

1. **Identify the organization and report purpose**: Provide:
   - Organization type: nonprofit, university department, foundation, government program
   - Mission and strategic priorities
   - Primary audiences (funders, board, staff, beneficiaries, public)
   - Report frequency and regulatory/funder requirements

2. **Provide existing data and outcomes measurement**: Share:
   - Current metrics and outcomes data (performance data, surveys, program counts)
   - Previous year's report (if available) to identify gaps or changes
   - Financial data: budget, revenue sources, program expenses
   - Beneficiary/program data: demographics, geographic reach, program types

3. **Invoke the impact-report-planner subagent**: Delegate to subagent with the full planning protocol:
   - **Local routing authority (default)**: Route through the repository agent named by this skill; if it is unavailable, use a host general-purpose worker with the full protocol. The catalog/meta-router owns route and model selection.
   - **Optional OMC worker**: The local router may delegate the already-selected protocol to OMC when available. OMC does not choose the route or model policy.

4. **Return planning output**: Present the structured impact report plan with:
   - Audience and purpose mapping
   - Metric selection strategy with baseline and year-over-year comparisons
   - Narrative arc outline (structure and key messages)
   - Data visualization plan (which metrics get visualized, chart types, design principles)
   - Beneficiary story collection plan (selection criteria, consent, representation)
   - Financial transparency plan (program expenses, overhead ratios, 990 alignment)
   - Production and distribution strategy (versions, channels, timeline, accessibility)
   - Compliance checklist (regulatory requirements, funder-specific reporting)

The plan guides actual report writing. Use stakeholder-report-writer to draft sections and copy-critic to review them.

## Tool_Usage

When invoking impact-report-planner:
- Use Read to load financial statements, program data, previous year reports
- Use Grep to search prior reports for metrics, language patterns, audience signals
- Use Bash to analyze data: row counts, demographic breakdowns, year-over-year changes
- Understand the organization's beneficiaries, programs, finances, and audiences thoroughly before planning structure

## Related_Skills

- **stakeholder-report-writer**: Write specific report sections for identified audiences
- **copy-critic**: Review draft report text for clarity, tone, and alignment with narrative arc
- **dataviz-planner**: Plan data visualizations in the report
- **data-planner**: Plan metric calculations and outcome measurement
- **policy-brief-writer**: If report includes policy recommendations or advocacy
