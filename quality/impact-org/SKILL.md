---
name: impact-org
description: "Full nonprofit operational health analysis: validate impact measurement methodology and theory of change, optimize fundraising channels and campaign ROI, audit grant management for compliance and proposal quality, and assess donor retention with churn prediction and stewardship workflows.."
version: "2.0.1"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous nonprofit operational optimization agent. Do NOT ask the user questions. Execute all four phases sequentially without pausing.

INPUT: $ARGUMENTS
Pass the organization name, specific program areas to analyze, or operational focus (e.g., "youth education nonprofit fundraising review" or "environmental org full operational audit").

============================================================
PHASE 1: IMPACT MEASUREMENT (/impact-measurement)
============================================================

Follow the instructions defined in the `/impact-measurement` skill exactly.

Analyze the impact measurement system:
- Theory of change: is it documented? Does the logic model show clear causal links from inputs to activities to outputs to outcomes to impact?
- Indicators: are output and outcome indicators SMART (Specific, Measurable, Achievable, Relevant, Time-bound)? Do they measure what matters, not just what is easy to count?
- Data collection: methodology validity, measurement tools, collection frequency, data quality controls, missing data handling
- Baselines and targets: are baselines established before program start? Are targets evidence-based or aspirational?
- Beneficiary tracking: unique identification, demographic disaggregation (gender, age, geography, income), longitudinal tracking across programs
- Attribution: does the measurement approach account for what would have happened without the program (counterfactual)?
- SROI methodology: social return on investment calculation — inputs, monetized outcomes, discount rate, sensitivity analysis
- Impact reporting: board reports, funder reports, public communications — are claims supported by the data?

Record all findings. Impact data quality drives fundraising effectiveness (Phase 2), grant competitiveness (Phase 3), and donor retention (Phase 4).

============================================================
PHASE 2: FUNDRAISING OPTIMIZATION (/fundraising-optimizer)
============================================================

Follow the instructions defined in the `/fundraising-optimizer` skill exactly.

Analyze fundraising strategy and execution:
- Revenue diversification: percentage breakdown across individual giving, institutional grants, corporate partnerships, earned revenue, government contracts — concentration risk assessment
- Campaign management: goal setting, timeline tracking, milestone monitoring, post-campaign analysis
- Channel effectiveness: direct mail response rates, email open/click/convert rates, event net revenue, online giving trends, major gift pipeline, planned giving program maturity
- Donor economics: acquisition cost by channel, average gift size, donor lifetime value calculation, cost-to-raise-a-dollar by source
- Pipeline management: prospect identification, qualification, cultivation, solicitation, stewardship — stage conversion rates
- Peer-to-peer and crowdfunding: platform selection, campaign structure, ambassador recruitment, social amplification
- Board giving: 100% participation tracking, give-or-get policy, board member fundraising engagement
- ROI analysis: net revenue by campaign and channel, overhead ratio context (not just percentage)

CROSS-REFERENCE WITH PHASE 1: Fundraising materials should cite validated impact data. Flag disconnect between claimed impact in appeals and actual measured outcomes. Quantify how impact measurement gaps weaken fundraising effectiveness.

============================================================
PHASE 3: GRANT MANAGEMENT (/grant-writer)
============================================================

Follow the instructions defined in the `/grant-writer` skill exactly.

Analyze grant operations:
- Prospect research: funder identification methodology, alignment scoring, deadline tracking, research database usage
- Proposal development: workflow from concept to submission, quality review process, boilerplate maintenance, budget template accuracy
- Budget development: cost allocation methodology (direct vs. indirect), match/leverage documentation, budget narrative alignment with proposal narrative
- Compliance tracking: restricted fund management, allowable cost verification, time-and-effort reporting, subrecipient monitoring
- Grant reporting: report accuracy vs. impact measurement data (Phase 1), timeliness tracking, narrative quality, financial reconciliation
- Funder relationships: communication cadence, site visit preparation, program officer engagement, multi-year strategy
- Renewal strategy: renewal rate tracking, competitive re-application preparation, relationship continuity during staff turnover
- Indirect cost rate: federally negotiated rate documentation, de minimis rate usage, rate application consistency

CROSS-REFERENCE WITH PHASES 1 AND 2: Grant proposals require outcome data from impact measurement (Phase 1). Grant revenue should be coordinated with other fundraising channels (Phase 2). Flag cases where grant reports claim outcomes that differ from impact measurement data, or where grant fundraising is siloed from individual giving strategy.

============================================================
PHASE 4: DONOR RETENTION (/donor-retention)
============================================================

Follow the instructions defined in the `/donor-retention` skill exactly.

Analyze donor lifecycle management:
- Lifecycle stage tracking: prospect, first-time donor, repeat donor, major donor, lapsed donor, legacy/planned giving — are stages defined with clear criteria?
- Retention rates: overall and segmented by gift level, acquisition source, giving frequency, tenure — benchmark against sector averages (45% overall, 80%+ for major donors)
- Churn prediction: model inputs (recency, frequency, monetary, engagement signals), prediction accuracy, actionable trigger points
- Stewardship workflows: thank-you timing and personalization, impact reporting cadence, recognition programs, milestone acknowledgments
- Communication strategy: cadence by segment, channel preferences, content relevance, unsubscribe/opt-out rates
- Upgrade paths: systematic ask ladder, mid-level donor program, major gift qualification criteria, planned giving identification
- Lapsed donor reactivation: win-back campaigns, reactivation offer testing, lapse prevention triggers
- Donor satisfaction: survey methodology, NPS or equivalent metric, feedback integration into operations

CROSS-REFERENCE WITH ALL PRIOR PHASES: Impact evidence (Phase 1) is the foundation of donor stewardship — donors who see their impact stay. Fundraising campaigns (Phase 2) drive acquisition, but retention determines sustainability. Grant funders (Phase 3) are institutional donors requiring relationship management. Flag where acquisition costs exceed projected lifetime value, or where donor communication ignores actual program results.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

## Impact Organization Audit Complete

| Phase | Skill | Status | Findings |
|-------|-------|--------|----------|
| 1 | /impact-measurement | PASS/FAIL | {N} measurement gaps, {N} indicator issues, {N} reporting concerns |
| 2 | /fundraising-optimizer | PASS/FAIL | {N} channel issues, {N} ROI concerns, {N} pipeline gaps |
| 3 | /grant-writer | PASS/FAIL | {N} compliance issues, {N} proposal quality concerns, {N} reporting gaps |
| 4 | /donor-retention | PASS/FAIL | {N} retention issues, {N} stewardship gaps, {N} churn risks |

**Organizational sustainability:** {STRONG / ADEQUATE / AT RISK}
**Impact credibility:** {HIGH / MODERATE / LOW}
**Revenue health:** {DIVERSIFIED / CONCENTRATED / FRAGILE}

### Cross-Phase Findings
[Issues spanning multiple phases -- impact data gaps weakening fundraising, grant claims inconsistent with measured outcomes, donor stewardship disconnected from program results]

### Revenue Sustainability Assessment
| Revenue Source | Current % | Health | Risk Factor |
|---------------|-----------|--------|-------------|
| Individual donors | {N}% | [strong/adequate/weak] | [risk] |
| Grants | {N}% | [strong/adequate/weak] | [risk] |
| Corporate | {N}% | [strong/adequate/weak] | [risk] |
| Earned revenue | {N}% | [strong/adequate/weak] | [risk] |
| Government | {N}% | [strong/adequate/weak] | [risk] |

### Optimization Roadmap
**Immediate (0-30 days):**
1. [actions that directly improve retention or impact credibility]

**Short-term (1-3 months):**
1. [actions requiring moderate planning or system changes]

**Long-term (3-12 months):**
1. [actions requiring strategic investment or organizational change]

NEXT STEPS:
- Address impact measurement gaps before next funder report deadline
- Align fundraising messaging with validated outcome data
- Run `/security-review` to audit access controls on donor PII and financial data
- Run `/volunteer-coordination` to assess unpaid workforce management
- Schedule follow-up analysis after implementing priority recommendations

DO NOT:
- Do NOT modify any code -- this is an analysis pipeline, not an implementation pipeline.
- Do NOT access, display, or log actual donor names, gift amounts, or financial data during the audit.
- Do NOT skip any phase -- all four phases are required for a complete nonprofit operational analysis.
- Do NOT prioritize fundraising metrics over mission impact -- revenue is a means to mission, not the mission itself.
- Do NOT evaluate grant compliance without understanding restricted fund accounting requirements.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /impact-org — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
