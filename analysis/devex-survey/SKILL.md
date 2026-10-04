---
name: devex-survey
description: Create or analyze Developer Experience surveys. Creation mode outputs a 9-question HaTS-aligned survey; Analysis mode outputs sentiment metrics with theme clustering. Use when running a developer experience survey or analyzing its results.
---

# DevEx Survey

This skill defines how AI assists with Developer Experience surveys in two modes:

1. **Creation Mode** — Generate a statistically credible, longitudinally stable DevEx survey
2. **Analysis Mode** — Analyze survey results into actionable, segmented insights

Both modes enforce strict constraints on question design, statistical reporting, and guardrails against misuse.

See `references/runbook.md` for the full operational playbook covering distribution, cadence, and communication strategy.

---

## Reasoning Framework

This skill exists because developer experience measurement requires survey science rigor (HaTS alignment, Likert scales, longitudinal consistency). Ad-hoc surveys produce unreliable data that can't be compared across quarters.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| Survey (Creation mode) | 9-question survey with scales and rationale | Survey platform / PM |
| Analysis report (Analysis mode) | Markdown with sentiment metrics, themes, leverage opportunities | PM / leadership |

---

## How to Help

When the user invokes this skill, determine which mode applies:

- If the user asks to **create**, **draft**, or **generate** a survey → enter **Creation Mode**
- If the user provides **survey data**, **results**, or **responses** → enter **Analysis Mode**
- If unclear, ask the user which mode they need

---

# CREATION MODE

## Objective

Generate a quarterly Developer Experience survey that:

- Measures workflow sentiment across key developer touchpoints
- Preserves longitudinal integrity (core questions stable quarter-over-quarter)
- Aligns to HaTS (Happiness and Tracking Survey) principles found on https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43221.pdf
- Remains statistically credible with proper confidence intervals
- Minimizes survey fatigue (3-5 minute completion)
- Supports metadata-based post-processing (non-anonymous)

## Research Alignment

Incorporate principles from:

- **HaTS (Happiness and Tracking Survey)** — Google's validated approach to tracking developer happiness over time. Key principles: tie to workflows, use consistent scales, keep surveys short, track longitudinally.
- **JetBrains Developer Ecosystem Report** — Industry benchmark for developer workflow patterns, tool usage, and ecosystem trends.

## Survey Constraints (MANDATORY)

These constraints are non-negotiable. Every generated survey must comply:

| Constraint | Requirement |
|------------|-------------|
| Max questions | 9 total (5 core + 1 pain point + 1 consolidated why + 2 floaters) |
| Scale | 5-point Likert (see below for allowed scales) |
| Phrasing | Non-biased, conversational (see below) |
| Identity | Non-anonymous |
| Completion time | 3-5 minutes |
| Layout | Single page |
| Floater questions | 1-2 allowed |
| Core questions | Must remain stable quarter-over-quarter |

### 5-Point Likert Scales

**Satisfaction scale** (default for core questions):

1. Very Satisfied
2. Satisfied
3. Neutral
4. Dissatisfied
5. Very Dissatisfied

**Ease/difficulty scale** (allowed for floater questions where it fits better):

1. Very Easy
2. Easy
3. Neutral
4. Difficult
5. Very Difficult

Floater questions may use either scale depending on what is being measured. Core questions always use the satisfaction scale.

### Likert Scoring Rules

**Satisfaction %** = (Very Satisfied + Satisfied) / Total Responses

**Dissatisfaction %** = (Very Dissatisfied + Dissatisfied) / Total Responses

Neutrals remain in the denominator. Do NOT generate vanity CSAT scores.

## Core Questions (Stable)

Every survey must include these 5 sentiment questions. They must remain identical across quarters to preserve longitudinal integrity.

Each question uses the phrasing pattern:

> "How satisfied or dissatisfied are you with..."

Write questions the way a developer would talk — use "your code", "merging your code", not abstract process language.

### The 5 Core Workflow Questions

1. **Overall Developer Experience** — "How satisfied or dissatisfied are you with your overall developer experience at [Company]?"
2. **Inner Loop (write, build, test)** — "How satisfied or dissatisfied are you with writing, building, and testing your code?"
3. **Merge Process** — "How satisfied or dissatisfied are you with merging your code?"
4. **Release Process** — "How satisfied or dissatisfied are you with releasing your code to production?"
5. **Documentation Experience** — "How satisfied or dissatisfied are you with the quality and availability of documentation?"

## Pain Point Question

Include exactly one pain point selection question:

> "What are your top 3 pain points?"

- Maximum 10 options listed
- Respondent must select exactly 3
- Options should cover the major workflow friction areas (e.g., build times, test flakiness, CI/CD reliability, environment setup, code review turnaround, documentation gaps, dependency management, deployment complexity, tooling fragmentation, on-call burden)

## Consolidated Why Question

After the core questions and pain point selection, include a single open-ended question:

> "Why did you respond the way you did to the above questions?"

This replaces per-question follow-ups. One consolidated "why" reduces survey fatigue while still capturing the reasoning behind sentiment responses.

## Floater Questions (1-2 per quarter)

Floater questions are contextual and may rotate each quarter. Use them to assess:

- New tools recently introduced
- Recent platform investments
- Experimental workflows or process changes
- Process friction (e.g., stewardship approval, on-call experience)

Floater questions do NOT replace core questions. Core questions are always present and unchanged.

Floaters may use the satisfaction scale or the ease/difficulty scale depending on what is being measured. For example, a question about stewardship approval friction fits the ease/difficulty scale better than satisfaction.

## Questions to AVOID

Do NOT ask respondents for:

- Repository or codebase
- Geographic location or country
- Job title or seniority
- Programming language
- Org or team name

These dimensions are available via metadata and will be joined during analysis. Asking for them wastes question slots and increases survey fatigue.

## Optional Elements

- **Open feedback field** — "Is there anything else you'd like to share?"
- **Follow-up consent** — "Would you be open to a follow-up conversation? (Yes / No)"

## Survey Structure

The full survey follows this order:

1. Q1-Q5: Core workflow questions (satisfaction scale)
2. Q6: Pain point selection (select exactly 3)
3. Q7: Consolidated "why" open-text (required)
4. Q8-Q9: Floater questions (satisfaction or ease/difficulty scale)
5. Optional: open feedback + follow-up consent

## Output Format (Creation Mode)

When generating a survey, return:

1. **Survey intro text** (short — purpose, time estimate, non-anonymous notice, close date)
2. **All questions** in order with scale and format specified
3. **Pain point options** (up to 10)
4. **Floater questions** with rationale for why they're included this quarter

---

# ANALYSIS MODE

## Objective

Analyze survey results to produce:

- Sentiment metrics with statistical rigor
- Theme clustering from verbatim responses
- Leverage opportunities (where small moves yield big gains)
- Segmented insights using metadata
- Executive-ready summary

## Analysis Requirements

### 1. Categorize Verbatim Responses

- Read every piece of open-text feedback
- AI-assisted theme categorization is expected
- Count theme frequency across all responses
- Surface representative quotes for each theme

### 2. Detect Sentiment Patterns

- Calculate satisfaction and dissatisfaction % per question
- Detect large sentiment deltas vs. prior quarter
- Identify **dissatisfied to neutral** opportunities (quick wins)
- Identify **neutral to satisfied** leverage (investment opportunities)

### 3. Segment Using Metadata

Join survey responses with organizational metadata to segment by:

- Programming language / tech stack
- Tenure at company
- Geographic location
- Discipline (frontend, backend, infra, mobile, etc.)
- Tool usage patterns
- Team / org distribution

Identify:

- **Hotspots** — teams or segments with unusually low satisfaction
- **Outliers** — individuals or groups that deviate sharply from the mean
- **Sharp deltas** — segments where satisfaction changed significantly quarter-over-quarter

### 4. Champion Identification

Flag respondents who:

- Provided thoughtful, detailed feedback
- Showed deep understanding of workflow friction
- Could serve as DevEx champions or design partners

### 5. Statistical Reporting

Always calculate and report:

| Metric | Required |
|--------|----------|
| Total invited | Yes |
| Total responded | Yes |
| Response rate | Yes |
| Confidence interval | Yes |
| Satisfaction % per question | Yes |
| Dissatisfaction % per question | Yes |

**Target CI: 1-3%.** Never publish sentiment without confidence interval.

## Output Format (Analysis Mode)

Return a structured report with these sections:

1. **Executive Summary** — 3-5 sentence overview of key findings
2. **Statistical Overview** — Response rate, CI, satisfaction/dissatisfaction % per question
3. **Trend Delta Summary** — Quarter-over-quarter changes with direction and magnitude
4. **Top 3 Friction Themes** — Most frequently cited pain points with representative quotes
5. **Segmented Hotspots** — Metadata-driven breakdowns showing where friction concentrates
6. **Leverage Recommendations** — Specific, actionable opportunities ranked by impact
7. **Champion Candidates** — Respondents flagged for follow-up (if applicable)

---

# Guardrails

These rules apply to both modes and must never be violated:

- **Do NOT tie sentiment to performance evaluation.** Survey data is a steering signal, not a performance metric.
- **Do NOT recommend gaming response rates.** Quality over quantity.
- **Do NOT suggest bot-driven or automated outreach.** All follow-ups must be personal and human.
- **Do NOT generate vanity metrics.** Report real satisfaction and dissatisfaction with CI.
- **Preserve trend integrity.** Never modify core questions in ways that break longitudinal comparability.
- **Close the feedback loop.** Always recommend sharing results and connecting improvements back to survey data.

The goal is trust, not vanity metrics.

---

## Related Skills

- `/analyzing-user-feedback` — General user feedback analysis frameworks
- `/designing-surveys` — Broader survey design principles
- `/storytelling-for-impact` — Craft compelling narratives from survey data for shareouts
- `/giving-presentations` — Present survey findings at all-hands and leadership reviews
