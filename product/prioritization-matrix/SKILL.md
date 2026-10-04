---
name: prioritization-matrix
description: "Score and rank features or initiatives using RICE, ICE, weighted scoring, or custom frameworks. Generates a prioritized backlog with clear rationale. Use for: sprint planning, roadmap decisions, feature trade-offs."
argument-hint: "[list of features or initiatives to prioritize]"
---

# Prioritization Matrix Skill

Score, rank, and prioritize a set of features, initiatives, or ideas using structured scoring frameworks.

## When to Use
- User has a list of features and needs to decide what to build first
- User needs to justify prioritization to stakeholders
- User says `/prioritization-matrix` followed by a list of items
- Any time competing initiatives need to be ranked

## Supported Frameworks

### RICE (Reach, Impact, Confidence, Effort)
Best for: Growth-focused teams with measurable reach data.

| Factor | How to Score |
|--------|-------------|
| **Reach** | # of users/customers affected per quarter |
| **Impact** | 0.25 (minimal) / 0.5 (low) / 1 (medium) / 2 (high) / 3 (massive) |
| **Confidence** | 100% (high) / 80% (medium) / 50% (low) |
| **Effort** | Person-months of work |

**Score = (Reach x Impact x Confidence) / Effort**

### ICE (Impact, Confidence, Ease)
Best for: Fast estimation when detailed reach data isn't available.

| Factor | How to Score (1-10) |
|--------|-------------------|
| **Impact** | How much will this move the needle? |
| **Confidence** | How sure are we about impact and effort? |
| **Ease** | How easy is this to implement? (10 = trivial) |

**Score = Impact x Confidence x Ease**

### Weighted Scoring
Best for: Custom criteria that matter to your team.

Define 4-6 criteria with weights (must sum to 100%):

| Criteria | Weight | Description |
|----------|--------|-------------|
| Strategic alignment | 25% | How well does this support company goals? |
| User impact | 25% | How much does this improve user experience? |
| Revenue potential | 20% | Direct or indirect revenue impact |
| Technical feasibility | 15% | How complex is implementation? |
| Time sensitivity | 15% | Is there a window of opportunity? |

Score each item 1-5 on each criterion. **Weighted score = sum of (score x weight).**

### Value vs. Effort (2x2)
Best for: Quick visual communication to stakeholders.

Plot items on a 2x2 matrix:
- **Quick Wins** (High value, Low effort) → Do first
- **Big Bets** (High value, High effort) → Plan carefully
- **Fill-ins** (Low value, Low effort) → Do if capacity allows
- **Money Pits** (Low value, High effort) → Deprioritize

## Workflow

### Step 1: Clarify
- What are we prioritizing? (features, bugs, initiatives, experiments)
- What timeframe? (this sprint, this quarter, this year)
- What constraints? (team size, dependencies, deadlines)
- What's the primary goal? (growth, retention, revenue, quality)

### Step 2: Choose Framework
Based on the context, recommend the most appropriate framework. If the user doesn't specify, default to RICE for product features and Weighted Scoring for strategic initiatives.

### Step 3: Score
For each item:
- Score on each dimension with reasoning (not just numbers)
- Flag assumptions and confidence level
- Note dependencies between items

### Step 4: Rank & Recommend
- Sort by composite score
- Group into tiers: Must Do / Should Do / Could Do / Won't Do
- Highlight any items where the score conflicts with your intuition (and explain why)

### Step 5: Communicate
Generate a stakeholder-ready summary:
- Top 3 priorities with one-sentence rationale each
- What we're NOT doing and why
- Key assumptions that could change the ranking

## Output Format
Generate a clean markdown table with scores, plus a summary paragraph. Include the rationale for the top and bottom items. Flag any close calls where small changes in assumptions would flip the ranking.

## AI/ML-Specific Considerations
When prioritizing AI features, also consider:
- **Model readiness**: Is the underlying model capable enough?
- **Eval coverage**: Do we have evals to measure success?
- **Safety review**: Does this need safety/red-team review?
- **Data requirements**: Do we have the training/eval data?
- **Cost per query**: What's the inference cost impact?
