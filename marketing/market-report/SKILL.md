---
name: market-report
description: Marketing report generator (Markdown) compiling audit data into client-ready documents with scores and action plans.
---

# Marketing Report Generator

Generate a client-ready `MARKETING-REPORT.md` that compiles available marketing audit data into scores, findings, recommendations, revenue-impact estimates, and a prioritized action plan.

## Invocation Triggers

Use this skill when the user:

- Runs `/market report` or `/market report <domain>`.
- Wants a full marketing report, marketing assessment, scorecard, or client-ready analysis document.
- Has completed one or more market audit skills and wants the findings compiled.
- Needs a Markdown report with executive summary, score breakdown, deep dives, action plan, and roadmap.

## Required Input Contract

Collect or infer:

- Company, domain, product, audience, and report date.
- Available source files and audit outputs.
- Report audience: founder, client, marketing team, executive, or operator.
- Known business model, average deal value, conversion metrics, traffic, and current channels when available.
- Competitor data, SEO data, CRO findings, content findings, social findings, email findings, and ad findings when available.
- Whether estimates are allowed or whether the report must only use verified data.

If no prior data exists, tell the user and offer to run a quick audit first, generate from provided information, or create a fill-in report template.

## Source Data Discovery

Check for:

- `MARKETING-AUDIT.md`
- `LANDING-CRO.md`
- `SEO-AUDIT.md`
- `BRAND-VOICE.md`
- `COMPETITOR-ANALYSIS.md`
- `FUNNEL-ANALYSIS.md`
- `CONTENT-AUDIT.md`
- `AD-AUDIT.md`
- `SOCIAL-AUDIT.md`
- `EMAIL-AUDIT.md`

Use specific findings when available. Label assumptions, estimates, missing data, and confidence levels.

## Core Report Workflow

1. Collect and inspect available source data.
2. Calculate the six-category scorecard:
   - Website & Conversion, 25%.
   - SEO & Organic, 20%.
   - Content & Messaging, 15%.
   - Social Media & Community, 15%.
   - Email & Automation, 15%.
   - Paid Advertising, 10%.
3. Write category deep dives with score, evidence, what is working, gaps, recommendations, and revenue impact.
4. Add competitor comparison when competitor data exists.
5. Summarize content quality, conversion optimization, and SEO health.
6. Build prioritized action plan: this week, this month, this quarter.
7. Build 30-60-90 day roadmap.
8. Add appendix with methodology, tools, glossary, data sources, assumptions, and limitations.
9. Write the final report to `MARKETING-REPORT.md`.

See [report-workflow.md](references/report-workflow.md) for the detailed workflow and category deep-dive guidance.

## Scoring and Estimation Rules

- Use the weighted scorecard formula:

```text
Overall Score = (Website * 0.25) + (SEO * 0.20) + (Content * 0.15) + (Social * 0.15) + (Email * 0.15) + (Paid * 0.10)
```

- Use verified source data where available.
- Do not invent metrics, traffic, conversion rates, revenue, competitors, or tool results.
- If estimating revenue impact, label assumptions and confidence.
- Keep estimates conservative unless the user provides verified inputs.
- If a category has no evidence, mark it as insufficient data instead of fabricating certainty.

See [scorecard-and-estimation.md](references/scorecard-and-estimation.md) for scoring tables, rating bands, and revenue-impact formulas.

## Output Expectations

Create `MARKETING-REPORT.md` with:

- Executive summary.
- Overall marketing score and rating.
- Score breakdown table.
- Top 3 priority actions.
- Detailed findings for all scored categories.
- Competitor comparison when data exists.
- SEO snapshot.
- Conversion optimization summary.
- Revenue impact summary.
- Prioritized action plan.
- 30-60-90 day roadmap.
- Appendix with methodology, tools, glossary, and data sources.

See [report-template.md](references/report-template.md) for the full Markdown structure.

## Safety and Quality Constraints

- Do not include private context, personal identifiers, credentials, tokens, API keys, session records, or local paths.
- Use placeholders for missing client, revenue, or analytics values.
- Do not present estimates as facts.
- Lead with insights and growth opportunities, not blame.
- Make recommendations specific enough to execute.
- Preserve professional formatting with consistent headings, tables, checkboxes, and clear hierarchy.
- Reference source findings and dates where available.

## Validation Rules

Before completion:

- Confirm `MARKETING-REPORT.md` exists and follows the output contract.
- Check every score has evidence, assumption, or insufficient-data labeling.
- Confirm weighted overall score matches category scores.
- Verify all revenue-impact claims have inputs and confidence.
- Ensure action items have impact, effort, expected result, and priority.
- Confirm no private data or unsupported claims entered the report.

## Minimal Examples

```text
/market report example.com
Create a client-ready marketing report from the existing audit files.
Compile SEO-AUDIT.md, LANDING-CRO.md, and COMPETITOR-ANALYSIS.md into MARKETING-REPORT.md with a 30-60-90 plan.
```

## Reference Map

- Detailed workflow, source gathering, category deep dives, competitor/content/CRO/SEO summaries: [report-workflow.md](references/report-workflow.md)
- Scorecard tables, rating bands, revenue impact estimation: [scorecard-and-estimation.md](references/scorecard-and-estimation.md)
- Full `MARKETING-REPORT.md` output template: [report-template.md](references/report-template.md)
- Prioritized action plan and 30-60-90 roadmap details: [action-plan-and-roadmap.md](references/action-plan-and-roadmap.md)
- Report-quality principles and public-safe examples: [examples-and-principles.md](references/examples-and-principles.md)
