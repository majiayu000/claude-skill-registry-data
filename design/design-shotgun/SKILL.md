---
name: design-shotgun
description: "Use when you need 3-5 intentionally different UI directions before committing to a single design approach"
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# /design-shotgun $ARGUMENTS

Generate multiple intentional design directions for a feature brief or plan. This is divergence before commitment.

**Do NOT write code. Do NOT edit the plan.** Your output is design options plus a recommendation strong enough to carry into `/product-review DESIGN` or `/plan-design-review`.

## Arguments

- `$ARGUMENTS` = brief text, plan path, or empty
- `--count N` = number of directions, default `3`, clamp to `3-5`
- If empty, use the most recent plan in `docs/plans/`
- If no brief or plan exists: ask the user for a short feature description, then stop until you have one

## Phase 1: Ground in Reality

Before inventing directions:

1. Read the brief or plan
2. Check for `DESIGN.md`, design-system docs, or existing UI patterns
3. Reuse product vocabulary that already exists in the repo
4. Extract hard constraints:
   - target users
   - device posture
   - accessibility expectations
   - trust or safety requirements
   - existing brand or component constraints

If the repo already has a strong design language, push variation through hierarchy, interaction model, pacing, and emotional tone. Do not propose something that obviously fights the product's established visual system.

## Phase 2: Generate Distinct Directions

Produce `N` directions that are meaningfully different, not cosmetic reskins.

Each direction must include:

### 1. Name

A short memorable label.

### 2. Core Idea

Two to three sentences describing the concept and the user impression it creates.

### 3. Information Hierarchy

What the user sees first, second, and third.

### 4. Interaction Model

What the main interaction pattern is:
- dashboard
- guided flow
- command surface
- editorial narrative
- split-pane workspace
- feed/timeline
- another concrete pattern

### 5. Mobile and Responsive Posture

How the concept changes on smaller screens. Not "stack it on mobile." Be specific.

### 6. Accessibility and Trust Watchouts

What needs care so the design stays usable and credible.

### 7. Why This Is Not Generic

Name the exact choices that keep it from becoming AI slop. If the direction still sounds like "clean modern cards," rewrite it.

### 8. Implementation Risk

Call out where this direction is easy, medium, or high risk for the current codebase.

## Phase 3: Force Separation

After drafting the directions, compare them directly. If any two would produce roughly the same screen with different styling, rewrite until they diverge on structure or behavior.

Use a compact comparison table:

| Direction | Best For | Main Risk | Distinguishing Move |
|-----------|----------|-----------|---------------------|
| ... | ... | ... | ... |

## Phase 4: Recommend One

Pick a single recommended direction and explain:
- why it fits the product and codebase best
- what it sacrifices versus the other options
- what must be preserved if the team proceeds

## Required Ending

Finish with:

### Recommended Handoff

Give the user the exact next step:
- `/product-review DESIGN` if the concept still needs product challenge
- `/plan-design-review` if a plan exists and needs design completion

### Design Handoff Block

Provide a short block that can be pasted into a plan:

```markdown
Recommended direction: ...
Primary user impression: ...
Hierarchy: ...
Interaction model: ...
Responsive posture: ...
Accessibility/trust requirements: ...
Must-not-lose differentiators: ...
```

## Rules

- Default to 3 directions unless the user asks for more
- Do not exceed 5 directions
- Specificity over vibes
- Reuse existing design language when present
- Variation must be structural, not palette-swapping
- No implementation plan, no component inventory, no code suggestions
