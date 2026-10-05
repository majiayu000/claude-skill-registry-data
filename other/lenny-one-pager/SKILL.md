---
name: lenny-one-pager
description: "Drafts concise product one-pagers in the style of Lenny Rachitsky's 1-pager: short, evidence-backed, decision-oriented product briefs. Use when the user asks for a 1-pager, product brief, product hypothesis, lightweight PRD, executive product memo, or wants to turn an idea into a crisp product decision document."
---

# Lenny One-Pager

## Goal

Create a genuinely short product 1-pager. It is not a comprehensive PRD.

Be direct and opinionated. Every section must earn its place by helping readers decide whether to build, test, defer, or reject the product idea.

## Output Shape

Use exactly these 8 sections unless the user asks otherwise:

1. Description
2. Problem
3. Why
4. Success
5. Audience
6. What
7. How
8. When

Keep the full document skimmable in one page. Prefer tight prose and compact bullets over exhaustive detail.

## Workflow

1. Identify the product, target user, and decision to support.
2. Reduce the problem to one testable hypothesis.
3. Select 3-5 strong evidence points only.
4. State a concrete success metric or a clear success condition.
5. Narrow the audience to a specific segment.
6. Describe the user experience, not internal architecture.
7. Pick the validation approach: build, experiment, prototype, or manual-first.
8. Give a milestone table with dates, owners, and confidence.

If key inputs are missing, make reasonable assumptions and mark them as assumptions. Ask at most 3 clarifying questions only when assumptions would change the decision.

## Section Guidance

### 1. Description

2-3 sentences. Explain what it does and who it is for. Avoid jargon and internal codenames.

### 2. Problem

One sentence. Make it short, focused, need-based, and solution-agnostic. Include what is going wrong and why it matters.

### 3. Why

Use 3-5 evidence bullets. Include quantitative, qualitative, and market signals when available. Add one short "Devil's advocate" note naming the biggest evidence gap or alternative explanation.

### 4. Success

Prefer one primary metric with a believable but ambitious target. If a metric is not possible yet, describe the observable world where the product clearly worked.

### 5. Audience

Name the first user segment, platform, geography, and why this segment comes first. Avoid "all users."

### 6. What

Walk through the core user experience:

1. User starts at...
2. They see/do...
3. The result is...

Focus on what users experience. Do not describe internal architecture unless it directly changes the user experience.

### 7. How

Choose one primary approach: build, experiment, prototype, or manual-first. Include major dependencies, constraints, risks, and unknowns.

### 8. When

Use a compact milestone table:

| Milestone | Target Date | Owner |
|-----------|-------------|-------|
| Design complete | [Date] | [Name] |
| Build complete | [Date] | [Name] |
| Internal testing | [Date] | [Name] |
| Ship / experiment start | [Date] | [Name] |
| Results review | [Date] | [Name] |

End with confidence level and what could slip.

## Quality Bar

- Problem is a single testable hypothesis.
- Evidence is selective, not a research dump.
- Solution describes the product experience, not the system internals.
- Success is measurable or operationally observable.
- Tone is clear, candid, and useful to a product decision-maker.

See [EXAMPLES.md](EXAMPLES.md) for a reusable skeleton and mini-example.
