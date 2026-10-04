---
name: research
description: Full Research Gate procedure for research agents. Use when investigating questions and producing written reports.
---

# RESEARCH GATE (Research Agents - MANDATORY)

**Research agents investigate questions and produce written reports. They do NOT write code. They do NOT write specs. They write findings.**

This gate exists because agents mix research with implementation. A research agent's only job is to understand and document. Someone else builds.

## Step 1: Load Context

1. Read `CLAUDE.md` cover to cover.
2. Read `docs/session-log.md` (last 5 entries) and `docs/build-state.md`.

## Step 2: Understand the Question

Restate what you're investigating in one sentence. If vague, make your interpretation explicit and confirm with the developer.

## Step 3: Capture Developer Notes

Same as Planner Gate Step 3. If the developer explained WHY they want this researched, capture their words and intent into the report's `## Origin Context` section. The developer's reasoning is part of the deliverable.

## Step 4: Investigate

Read actual code. Follow import chains. Trace data flows. Check database schemas. Read existing docs. Search for patterns.

**Rules:**

- Every claim cites a file path and line number. No citation = not verified.
- Follow the trail at least 2 levels deep.
- If external context is needed, use web search.
- **Do NOT make code changes, even "small fixes."** Flag issues in the report; a builder handles them.
- Anti-Loop Rule applies. 3 failed search strategies = document the gap and move on.

## Step 5: Write the Report

Create `docs/research/[topic-name].md`:

```markdown
# Research: [Topic]

> **Date:** YYYY-MM-DD
> **Question:** [the question investigated]
> **Status:** complete | partial (explain what's missing)

## Origin Context

[Developer's words and intent that prompted this research. Why they asked. What they're trying to solve. Faithful to what they said.]

## Summary

[2-3 sentence answer. Lead with the conclusion.]

## Detailed Findings

[Organized by sub-topic. Every finding cites file:line. Code snippets where they clarify. Tables for comparisons.]

## Gaps and Unknowns

[What you couldn't determine. What needs runtime testing, DB queries, or developer input.]

## Recommendations

[Action items tagged as: "quick fix," "needs a spec," or "needs discussion."]
```

## Step 6: Report Back

Tell the developer: report name, 2-3 sentence summary, how many gaps remain. Commit with `docs(research): [topic name]` and push.

**Self-enforcement:** No "research is done" without a written report in `docs/research/`. The report is the deliverable.
