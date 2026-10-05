---
name: creo-ux-competitor
description: >
  Analyze competitor websites for UX patterns, strengths, and weaknesses. Navigates
  external URLs, documents UX patterns, evaluates against Nielsen heuristics, and
  extracts actionable learnings. Trigger keywords: competitor analysis, competitor UX,
  competitive analysis, benchmark, compare competitors.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# Competitor UX Analysis

Analyze external competitor websites to extract UX insights and learnings. Navigates competitor sites as a real user, documents their UX patterns, evaluates against professional standards, and identifies opportunities for differentiation.

## Commands

| Command | Description |
|---------|-------------|
| `/creo ux-competitor <url>` | Analyze a single competitor website |
| `/creo ux-competitor compare <url1> <url2>` | Compare two competitor websites |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Read `competitors` (pre-configured list by tier), `reports_path`
3. Load project extension if it exists at `.claude/skills/creo-ux-competitor/creo-ux-competitor-{project_id}.md`. This file contains project-specific competitor list, positioning, differentiators, and analysis focus areas. `{project_id}` comes from `project-config.md`. Always load it before doing work.
4. If no config exists, ask user for competitor URL

### Phase 1: Competitor Research

Before navigating, gather background info via web search:
- Company background and target audience
- Key features and value proposition
- User reviews (what people love and hate)

Identify key flows to analyze:
- Onboarding / Sign-up
- Core feature experience
- Pricing / Conversion
- Mobile experience

### Phase 2: Live Analysis

Navigation strategy:
1. Start at homepage
2. Follow the primary user journey
3. Screenshot every meaningful screen (use full page capture)
4. Note micro-interactions and feedback
5. Test on multiple viewports (375px mobile, 1440px desktop)

What to capture:
- First impressions (homepage)
- Sign-up / Onboarding flow
- Core feature experience
- Empty states and error handling
- Help / Support access
- Pricing presentation

### Phase 3: Professional Evaluation

#### JTBD Analysis
> When [situation], users want to [motivation], so they can [outcome].

#### Nielsen's Heuristics (Score 0-4)

| # | Heuristic | Questions |
|---|-----------|-----------|
| 1 | Visibility | Do users know what is happening? |
| 2 | Real world match | Is language familiar? |
| 3 | User control | Can users undo/cancel? |
| 4 | Consistency | Are patterns repeated? |
| 5 | Error prevention | Are mistakes prevented? |
| 6 | Recognition | Are options visible? |
| 7 | Flexibility | Are there shortcuts? |
| 8 | Minimalism | Is it clutter-free? |
| 9 | Error recovery | Are error messages helpful? |
| 10 | Help | Is guidance available? |

#### Competitive Dimensions (Rate 1-5)
- **Simplicity** -- How easy to use?
- **Speed** -- How fast to complete tasks?
- **Clarity** -- How clear is the UI?
- **Delight** -- Any wow moments?
- **Trust** -- Does it feel reliable?

### Phase 4: Insights Extraction

#### What They Do WELL (Copy/Adapt)
- Patterns that reduce friction
- Clever interactions
- Effective copywriting
- Trust-building elements

#### What They Do POORLY (Avoid/Improve)
- Friction points
- Confusing flows
- Missing features
- Bad patterns

#### Opportunities for Us
- Gaps in their offering
- Features they lack
- Better approaches possible
- Differentiation opportunities

### Report Structure

```markdown
# Competitor Analysis: [Name]

**URL:** [https://...]
**Date:** [YYYY-MM-DD]

## Executive Summary
## Company Overview (target audience, value proposition, pricing)
## JTBD Analysis
## Flow Analysis (homepage, onboarding, core feature, mobile)
## Heuristic Evaluation (score table, total out of 40)
## Competitive Scorecard (simplicity, speed, clarity, delight, trust)
## Key Insights (what they do well, what they do poorly, opportunities)
## Recommendations for Our Product (immediate actions, consider later)
## Screenshots Gallery
```

### Report Output

Save to: `.claude/reports/competitor-[name]-[YYYYMMDD].md`

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/nielsen-heuristics.md` | Detailed heuristic evaluation guide |
| `references/competitive-scorecard.md` | Scoring methodology |

## Quality Gates

- Screenshots must use full page capture
- Both mobile (375px) and desktop (1440px) viewports must be tested
- Every heuristic must be scored with evidence
- Report must include actionable recommendations for your own product
- Insights must be categorized as learn-from, avoid, or opportunity
- Report must be saved as a file
