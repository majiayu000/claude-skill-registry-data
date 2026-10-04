---
name: thrunt-milestone-summary
description: Generate a comprehensive project summary from milestone artifacts for team onboarding and review
argument-hint: "[version]"
allowed-tools: Read, Write, Bash, Grep, Glob
---


<objective>
Generate a structured milestone summary for team onboarding and project review. Reads completed milestone artifacts (HUNTMAP, HYPOTHESES, CONTEXT, SUMMARY, VERIFICATION files) and produces a human-friendly overview of what was built, how, and why.

Purpose: Enable new team members to understand a completed project by reading one document and asking follow-up questions.
Output: MILESTONE_SUMMARY written to `.planning/reports/`, presented inline, optional interactive Q&A.
</objective>

<execution_context>
@.github/thrunt-god/workflows/milestone-summary.md
</execution_context>

<context>
**Project files:**
- `.planning/HUNTMAP.md`
- `.planning/MISSION.md`
- `.planning/STATE.md`
- `.planning/RETROSPECTIVE.md`
- `.planning/milestones/v{version}-HUNTMAP.md` (if archived)
- `.planning/milestones/v{version}-HYPOTHESES.md` (if archived)
- `.planning/phases/*-*/` (SUMMARY.md, FINDINGS.md, CONTEXT.md, RESEARCH.md)

**User input:**
- Version: $ARGUMENTS (optional — defaults to current/latest milestone)
</context>

<process>
Read and execute the milestone-summary workflow from @.github/thrunt-god/workflows/milestone-summary.md end-to-end.
</process>

<success_criteria>
- Milestone version resolved (from args, STATE.md, or archive scan)
- All available artifacts read (HUNTMAP, HYPOTHESES, CONTEXT, SUMMARY, VERIFICATION, RESEARCH, RETROSPECTIVE)
- Summary document written to `.planning/reports/MILESTONE_SUMMARY-v{version}.md`
- All 7 sections generated (Overview, Architecture, Phases, Decisions, Hypotheses, Tech Debt, Getting Started)
- Summary presented inline to user
- Interactive Q&A offered
- STATE.md updated
</success_criteria>
