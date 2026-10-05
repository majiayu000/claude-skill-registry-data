---
name: dataviz-planner
description: "Plan charts, figures, and visualizations — data mapping, chart selection, interaction design."
version: 0.1.0
---

# Data Visualization Planner

Planner skill for designing data visualizations *before* you create them.

Use this skill to plan visualizations that answer specific questions, fit your audience's literacy level, and make disparities visible rather than hiding them in aggregates.

## JTBD (Jobs To Be Done)

### Primary Job
When I need to create a chart or visualization but haven't yet resolved what question it answers, what data pattern it shows, or whether my audience can interpret it correctly,
I want a concrete visualization design plan before I start building,
so I can avoid creating something that looks polished but misleads viewers or hides the patterns that actually matter.

### Secondary Jobs
- When the audience for a visualization has a different data literacy level than I assumed — executives who can't read confidence intervals, or a general public audience that will misread a logarithmic scale — I want the encoding choices matched to who will actually see it, so the chart informs rather than confuses.
- When a dataviz-critic review returned REVISE or REJECT and I need to redesign rather than just patch, I want a redesign plan that addresses the root encoding or framing failures, so I don't rebuild the same mistake with better typography.

### Job Layers
- Functional: Resolve chart type selection, data encoding strategy, audience literacy match, accessibility requirements, and equity implications before any tool is opened or code is written.
- Emotional: Reduce the anxiety of committing to a chart type or design approach and discovering after publication that it was the wrong one for the data pattern or audience.
- Social: Helps the user present a defensible design rationale to editors, reviewers, or stakeholders — "this is why we chose a small-multiples layout over a single stacked bar" — backed by planning rather than instinct.

### This Skill Is For
- A user about to create a chart or visualization who hasn't yet answered: what question does this answer, for whom, and which encoding suits the data pattern?
- A user working with disaggregated or equity-sensitive data who needs to plan how to make disparities visible rather than letting them vanish into an aggregate.
- A user building multiple visualizations for a report, dashboard, or presentation who needs consistent encoding choices and a coherent visual language before creating any individual chart.
- A user whose previous visualization received a REVISE or REJECT verdict and needs a redesign plan that goes back to the question and encoding level, not just surface fixes.

### This Skill Is NOT For
- A user with an existing chart who primarily needs a quality verdict on what was built; use `dataviz-critic` instead.
- A user whose unresolved problem is end-to-end dashboard architecture and KPI hierarchy rather than individual chart design; use `dashboard-planner` instead.

### Paired With
- `dataviz-critic`: After the chart or visualization is created, use it to audit whether the encoding choices are honest, accessible, and effective.
- `dashboard-planner`: Use this when the unresolved problem is the architecture of a multi-chart dashboard rather than the design of any individual visualization within it.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has data and a goal but no chart type or encoding plan | The skill resolves the question, data pattern, chart type selection, and encoding strategy before creation begins | A concrete design specification: chart type, axes, encoding choices, accessibility requirements |
| Has an audience literacy or context mismatch (complex data, general audience) | The skill identifies the mismatch and adapts the encoding, annotation, and framing choices to the actual audience | A design approach calibrated to what this audience can reliably interpret |
| Has a failed visualization after a REVISE or REJECT verdict | The skill diagnoses the root encoding or framing failure and produces a redesign plan | A redesign plan addressing root causes, not surface cosmetics |

### When to Escalate
- If the user already has a built visualization and needs a quality verdict rather than a design plan, escalate to `dataviz-critic`.
- If the user's problem is the end-to-end architecture of a dashboard system rather than the design of individual charts, escalate to `dashboard-planner`.

## Purpose

Plan data visualizations strategically, not reactively:

- **Clarify the question**: What question does this visualization answer?
- **Know your audience**: Who is viewing it? What's their data literacy?
- **Assess the data**: Is your data complete? Are sample sizes adequate? Can you disaggregate by population groups?
- **Choose the right chart type**: Comparison vs. trend vs. distribution vs. composition — each needs different visualization
- **Design for accessibility**: Color-blind safe palettes, patterns for colorblind users, clear annotations
- **Make equity visible**: Disaggregate data by population; prevent disparities from hiding in aggregates

This skill produces a detailed plan that guides actual visualization creation.

## Use_When

- Planning a visualization before starting design (planning vs. reactively creating charts)
- Building dashboards, reports, or presentations with multiple visualizations
- You need to disaggregate data by population and show disparities
- Determining what visualization type answers your question best
- Ensuring visualizations are accessible to all users (colorblind, low vision, etc.)
- Creating publication-quality visualizations that will be reviewed
- You want to test whether a visualization effectively communicates its intended message

## Do_Not_Use_When

- You've already created a visualization and want critique (use dataviz-critic instead)
- You need quick exploratory charts (this is for intentional design)
- The visualization is a throwaway internal sanity check
- You're just learning data visualization basics (use visualization-standards reference instead)

## Companion_Skills

- **dataviz-critic**: Use AFTER creating visualizations to review design decisions and identify gaps
- **stakeholder-report-writer**: Use when planning visualizations for reports or presentations
- **visualization-standards**: Reference for color palettes, chart type conventions, accessibility guidance

## Steps

1. **Identify the question and data**: Provide the research/business question and the data you'll be visualizing

2. **Determine audience and context**: Clarify:
   - Who is the audience? (Clinician, board member, community group, researcher, general public)
   - Where will it be displayed? (Report, presentation, dashboard, website, social media, print)
   - What decision should it support?
   - Data literacy level? (Low, moderate, high)

3. **Invoke the dataviz-planner subagent**: Delegate to subagent with the full planning protocol below:
   - **Local routing authority (default)**: Route through the repository agent named by this skill; if it is unavailable, use a host general-purpose worker with the full protocol. The catalog/meta-router owns route and model selection.
   - **Optional OMC worker**: The local router may delegate the already-selected protocol to OMC when available. OMC does not choose the route or model policy.

4. **Return planning output**: Present the structured visualization plan with:
   - Question and audience clarity
   - Data assessment and quality assurance
   - Chart type selection with rationale
   - Design specifications (color, typography, annotations)
   - Equity review and testing plan

The plan guides actual visualization creation. Use dataviz-critic to review the completed visualization.

## Tool_Usage

When invoking dataviz-planner:
- Use Read to load data files and understand structure
- Use Grep to verify data fields, completeness, value ranges
- Use Bash to run basic data exploration (row counts, unique values, ranges)
- Understand the data thoroughly before planning chart design

## Related_Skills

- **dataviz-critic**: Post-creation review of visualization design decisions
- **stakeholder-report-writer**: When planning visualizations for reports
- **visualization-standards**: Reference for accessibility, color, chart type conventions
