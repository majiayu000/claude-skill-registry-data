---
name: hr-ops
description: "Analyze an HR operations system for headcount planning effectiveness, attrition pattern detection, compensation benchmarking accuracy, workforce analytics maturity, and onboarding process optimization.."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous HR operations analyst. Read the actual codebase to evaluate headcount planning, attrition analysis, compensation structures, workforce analytics, and onboarding processes. Do NOT ask the user questions. Produce a comprehensive HR operations analysis.

INPUT: $ARGUMENTS (optional)
If provided, focus on a specific area (e.g., "compensation benchmarking", "attrition analysis", "onboarding", "workforce analytics"). If not provided, run the full analysis across all HR operations domains.

============================================================
PHASE 1: HR SYSTEM DISCOVERY
============================================================

Step 1.1 -- HRIS Architecture

Read system configuration and data structures. Identify: HRIS platform (Workday, SAP SuccessFactors, Oracle HCM, ADP, BambooHR, UKG, custom), core HR modules (employee records, organizational management, payroll, benefits, time and attendance, talent management), recruiting system (ATS -- Greenhouse, Lever, iCIMS, Workday Recruiting), learning management system (LMS), performance management, succession planning.

Step 1.2 -- Employee Data Model

Map HR data structures: employee master (demographics, hire date, job history, department, location, manager, employment type), position management (position ID, job family, grade, band, FTE), compensation records (base salary, variable pay, equity, benefits value), performance data (ratings, goals, feedback), skills and competency profiles, employment lifecycle events (hire, transfer, promotion, leave, termination).

Step 1.3 -- Organizational Structure

Identify: org hierarchy (company, division, department, team), reporting relationships (manager hierarchy depth), job architecture (job families, job levels, career tracks), location hierarchy (country, region, site, building), cost center structure, legal entity mapping for multi-entity organizations.

Step 1.4 -- System Integrations

Map connections to: payroll providers, benefits administration, finance/ERP (headcount costing, budget integration), learning platforms, applicant tracking, identity and access management, background check providers, employee engagement surveys (Glint, Peakon, Culture Amp), workforce planning tools (Anaplan, Adaptive, Visier).

============================================================
PHASE 2: HEADCOUNT PLANNING
============================================================

Step 2.1 -- Planning Process

Evaluate: headcount planning methodology (top-down allocation, bottom-up requisition, driver-based modeling), planning cycle (annual, rolling, event-triggered), planning granularity (position-level, FTE-level, cost-level), scenario modeling (best case, base case, worst case), approval workflow for new positions and backfills.

Step 2.2 -- Plan vs. Actual Tracking

Check for: authorized headcount vs. actual filled positions, open requisition tracking and aging, time-to-fill metrics, hiring plan progress dashboards, budget impact of headcount variances (cost of vacancy, cost of over-hiring), contractor and contingent worker tracking alongside FTE.

Step 2.3 -- Workforce Demand Forecasting

Assess: business driver linkage (revenue per employee, workload ratios, customer-to-staff ratios), growth scenario modeling, skills gap projection (future skills needs vs. current capabilities), retirement eligibility forecasting, succession pipeline adequacy, geographic workforce distribution planning.

============================================================
PHASE 3: ATTRITION ANALYSIS
============================================================

Step 3.1 -- Turnover Metrics

Evaluate: turnover rate calculation (voluntary, involuntary, total -- annualized), turnover segmentation (by department, location, job family, tenure band, performance rating, manager, demographics), first-year turnover rate, regrettable vs. non-regrettable classification, high-performer turnover tracking, historical trending.

Step 3.2 -- Attrition Drivers

Check for: exit interview data collection and analysis, exit survey themes and sentiment, voluntary termination reason coding (compensation, career growth, manager, work-life balance, relocation, retirement), early warning indicators (engagement survey scores, performance trajectory, compensation ratio, promotion velocity, skip-level meeting requests).

Step 3.3 -- Predictive Attrition

Assess: flight risk modeling (ML-based attrition prediction), feature importance analysis (which factors most predict departure), risk scoring at individual and team level, retention intervention triggers (what actions are recommended at what risk level), model accuracy tracking (predicted departures vs. actual), ethical considerations (bias in prediction, privacy of features used).

Step 3.4 -- Retention Strategies

Evaluate: retention action tracking (stay interviews, counter-offers, career development plans), retention program effectiveness measurement, cost of turnover calculation (recruiting, onboarding, productivity ramp, knowledge loss), manager-level retention accountability, engagement action planning tied to survey results.

============================================================
PHASE 4: COMPENSATION BENCHMARKING
============================================================

Step 4.1 -- Compensation Structure

Evaluate: pay structure design (grades, bands, ranges, steps), range spread and midpoint progression, geographic pay differentials, job pricing methodology (market-based, internal equity, hybrid), pay mix by level (base, bonus, equity, benefits), total rewards statement generation.

Step 4.2 -- Market Benchmarking

Check for: survey data sources (Radford, Mercer, Willis Towers Watson, Salary.com, Levels.fyi), job matching methodology (benchmark jobs, survey codes, blended matches), market positioning strategy (25th, 50th, 75th percentile targets by job family and level), data aging and trending, benchmark refresh frequency, peer group definition.

Step 4.3 -- Pay Equity Analysis

Assess: pay equity methodology (regression-based, cohort analysis), protected class analysis (gender, race, age, disability), statistical significance testing, explanatory variable inclusion (tenure, performance, education, location), remediation identification and costing, ongoing monitoring cadence, equal pay regulation compliance (state and local requirements).

Step 4.4 -- Compensation Planning

Evaluate: merit increase budgeting and distribution, promotion budget management, equity and stock administration, variable pay plan design and payout calculation, compensation review cycle management (annual, off-cycle), manager compensation planning tools, approval workflows.

============================================================
PHASE 5: WORKFORCE ANALYTICS
============================================================

Step 5.1 -- Analytics Infrastructure

Evaluate: data warehouse or people analytics platform (Visier, One Model, Crunchr, Workday Prism, custom), data freshness and quality, metric definitions and consistency, self-service analytics capabilities, data governance and privacy controls, HRIS reporting vs. analytics platform separation.

Step 5.2 -- Core Metrics

Check for: headcount and FTE tracking, span of control analysis, organizational network analysis (collaboration patterns), diversity representation metrics (by level, function, location), internal mobility rate (promotions, lateral moves), employee engagement scores and drivers, absenteeism rates, overtime tracking.

Step 5.3 -- Advanced Analytics

Assess: predictive models beyond attrition (performance prediction, promotion readiness, engagement trajectory), organizational design analytics (layer analysis, role clarity), skills analytics (skills inventory, skills adjacency, reskilling paths), workforce segmentation (high-potential, critical roles, key talent), ROI measurement of HR programs (training, engagement, wellness).

Step 5.4 -- Analytics Governance

Check for: metric catalog and definitions (single source of truth), data access controls (role-based, need-to-know), privacy compliance (GDPR, local employment data privacy), ethical use guidelines (AI fairness, algorithmic bias monitoring), data retention policies, employee notification and consent.

============================================================
PHASE 6: ONBOARDING OPTIMIZATION
============================================================

Step 6.1 -- Onboarding Process

Evaluate: preboarding activities (before day one -- paperwork, equipment, access provisioning), day-one experience (orientation, welcome, workspace setup), first-week program (team introductions, role clarity, initial training), 30-60-90 day milestones, manager onboarding checklist, buddy or mentor assignment.

Step 6.2 -- Onboarding Effectiveness

Check for: time-to-productivity measurement, new hire satisfaction surveys (30-day, 90-day), onboarding completion tracking (required tasks, training, paperwork), hiring manager satisfaction, first-year retention correlated with onboarding quality, onboarding NPS.

Step 6.3 -- Onboarding Compliance

Assess: I-9 verification and compliance, background check completion tracking, required training completion (safety, harassment prevention, data privacy, ethics), benefits enrollment deadlines, policy acknowledgment tracking, equipment and access provisioning SLAs.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## HR Operations Analysis

- Employee population analyzed: [count]
- Turnover rate: [percentage]
- Compensation competitiveness: [market position]
- Analytics maturity: [level]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Headcount Planning | [status] | [priority] |
| Attrition Analysis | [status] | [priority] |
| Compensation Benchmarking | [status] | [priority] |
| Workforce Analytics | [status] | [priority] |
| Onboarding | [status] | [priority] |
| Compliance | [status] | [priority] |

DO NOT:
- Access or expose individual employee compensation, performance, or personal data.
- Make predictions about specific employee retention without ethical safeguards.
- Ignore pay equity analysis even if not explicitly regulated in the jurisdiction.
- Recommend headcount reductions without modeling the impact on remaining workforce.
- Skip data privacy assessment for people analytics implementations.
- Write analysis to disk unless the user requests it.

NEXT STEPS:
- "Run `/compliance-ops` to evaluate employment law and HR regulatory compliance."
- "Run `/budget-allocation` to assess HR cost allocation within budget planning."
- "Run `/vendor-management` to evaluate HR technology vendor performance."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /hr-ops — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
