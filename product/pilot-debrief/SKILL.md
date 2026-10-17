---
name: pilot-debrief
description: |
  Synthesize pilot observations into structured debrief reports and spec updates. Use this skill when:
  - A pilot has completed and you have observation notes, tickets, or feedback transcripts
  - You need to turn messy pilot data into actionable spec changes
  - You want to generate edge case user stories from field observations
  - You need negative acceptance criteria from pilot bugs
  - You want a structured debrief report for stakeholder communication
---

# Pilot Debrief

Synthesize unstructured pilot data (observations, tickets, feedback transcripts) into a structured debrief report with spec change recommendations. Converts field findings into edge case stories, negative ACs, and design requirements.

## Workflow

1. **Gather pilot inputs** — Read all available pilot data sources
2. **Categorize findings** — Sort into UX issues, bugs, feature requests, positive signals
3. **Map to spec sections** — Link each finding to the spec section it affects
4. **Generate artifacts** — Edge case stories, negative ACs, design requirements
5. **Write debrief report** — Structured report for stakeholders
6. **Output spec change list** — Specific edits to make to existing specs

## Categorization Framework

### 1. UX Issues
Problems with how users interact with the product.
- Navigation confusion, unclear feedback, unexpected behavior
- Accessibility gaps, language/comprehension issues
**Maps to:** Design sections (interaction patterns, states, accessibility)

### 2. Bugs
Things that broke or didn't work as specified.
- Crashes, data loss, wrong behavior, performance issues
**Maps to:** Error States, NFRs

### 3. Feature Requests
Things users wished existed.
- Direct requests from users, observer inferences from user behavior
**Maps to:** Scope (in-scope for next phase or out-of-scope), backlog

### 4. Positive Signals
Things that worked well — validates assumptions and celebrates wins.
- Engagement, comprehension, adoption signals
**Maps to:** Success Metrics, Objectives

## Synthesis Principles

### Observation -> Edge Case User Story
Every unexpected user behavior becomes an edge case story.

### Bug -> Negative Acceptance Criteria
Every pilot bug becomes a "must NOT" criterion on the relevant story.

### UX Confusion -> Design Requirement
Every navigation/comprehension issue becomes an explicit interaction pattern.

### Analytics Gap -> Metric Requirement
Missing data that would have been useful during the pilot.

## Output Format

```markdown
# Pilot Debrief Report

**Pilot:** {name}
**Dates:** {start} - {end}
**Location:** {location}
**Participants:** {count and types}
**Prepared:** {DD-MM-YYYY}

## 1. Executive Summary
{2-3 paragraphs: key findings, overall assessment, top 3 actions}

## 2. Pilot Goals vs Outcomes

| # | Goal | Success Criteria | Outcome | Status |
|---|------|-----------------|---------|--------|
| 1 | {goal} | {criteria} | {actual} | Pass/Partial/Fail |

## 3. Findings by Category

### 3.1 UX Issues ({count})
| # | Finding | Severity | Users Affected | Spec Section | Action |
|---|---------|----------|---------------|-------------|--------|

### 3.2 Bugs ({count})
| # | Finding | Ticket | Severity | Reproducible? | Action |
|---|---------|--------|----------|--------------|--------|

### 3.3 Feature Requests ({count})
| # | Finding | Requested By | Frequency | Recommendation |
|---|---------|-------------|-----------|----------------|

### 3.4 Positive Signals ({count})
| # | Finding | Evidence | Validates |
|---|---------|---------|-----------|

## 4. Generated Artifacts
### 4.1 New Edge Case Stories
### 4.2 New Negative Acceptance Criteria
### 4.3 Design Requirements Updates
### 4.4 New Metrics Required

## 5. Spec Change Recommendations
### Priority: Must Update Before Next Pilot
### Priority: Update Before Next Sprint
### Priority: Backlog
```

## Rules

1. **Every finding gets categorized** — No finding should be left uncategorized
2. **Every bug becomes an AC** — Pilot bugs are the most valuable input for acceptance criteria
3. **Quantify when possible** — "3 out of 5 users" is better than "some users"
4. **Quote users directly** — Direct quotes add credibility and empathy
5. **Don't speculate on fixes** — The debrief identifies *what* needs to change, not *how*
6. **Positive signals matter** — Don't only report problems

## Quality Checklist

- [ ] All findings categorized
- [ ] Every bug has a corresponding negative AC
- [ ] Quantified observations where possible
- [ ] Direct user quotes included
- [ ] Spec change recommendations prioritized
- [ ] Positive signals documented alongside issues
