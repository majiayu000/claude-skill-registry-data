---
name: ai-decision-engine
description: "Produces a multi-framework strategic product recommendation from all available project context - Product Requirements Documents (PRDs), research, metrics, competitive intelligence, and roadmaps - with a source log, situation model, weighted scoring, second-order effects, a pre-mortem, and explicit conditions that would change the call. Use when making product prioritization decisions; running quarterly planning; evaluating build, ship, or kill trade-offs; resolving conflicting stakeholder input; deciding what to build next; or answering any strategic question that needs synthesis across multiple sources."
---

# AI Decision Engine

> Read everything, apply four frameworks, and show the reasoning chain behind the call.

## What this skill is

A strategic reasoning system for product decisions. It first assembles every relevant source in the working directory, builds an explicit model of the situation, then runs four frameworks in parallel and looks for convergence. The result is a recommendation with a stated confidence level, visible trade-offs, and the evidence that would reverse it.

## What it solves

- Decisions made from the last conversation or loudest stakeholder instead of the full evidence base
- Single-framework analysis that hides what other lenses would reveal
- Recommendations with no stated confidence, trade-offs, or opportunity cost
- Contradictions between research, metrics, and roadmap that go unnoticed
- Plans that never ask how they could fail or what would change the answer
- "Do nothing" never being considered as a real option

## When to invoke

- Choosing between competing initiatives for the next quarter
- Deciding whether to build, ship, iterate, or kill a feature
- Stakeholders disagree and the team needs an evidence-based resolution
- A strategic question spans research, metrics, competitive, and roadmap sources
- Pressure-testing a decision before presenting it to leadership

## Phase 1: Context assembly

Before answering any strategic question, scan the working directory for:
- `CLAUDE.md` or `README.md` - product context, team, constraints
- `docs/` or `specs/` - existing PRDs and feature specs
- `research/` - user research, interview notes, survey results
- `data/` or `metrics/` - analytics exports and dashboards
- `competitive/` - competitor analysis and market research
- `roadmap/` - planning artifacts

Log each source found:

| Source | Key signal | Recency | Confidence |
|--------|------------|---------|------------|
| [filename] | [what it tells us] | [when updated] | [high / medium / low] |

If critical context is missing, say so: "I don't have [X]. My recommendation will be stronger with it."

## Phase 2: Situation model

Write this out before reasoning:
- **Product stage** - early, growth, mature, or turnaround
- **Primary constraint** - engineering capacity, market timing, revenue pressure, technical debt, or competitive threat
- **Active bets** - what is being built now and why
- **Unresolved tensions** - where the evidence conflicts
- **Decision type** - one-way door (irreversible) or two-way door (reversible)

## Phase 3: Impact and confidence matrix

List every option, including "do nothing."

| Option | Expected impact | Confidence | Evidence sources |
|--------|-----------------|------------|------------------|
| [A] | [quantified if possible] | [high / medium / low] | [which documents] |

## Phase 4: Strategic alignment scoring

Score each option 1-5 per dimension and calculate the weighted total. Show the math.

| Dimension | Weight |
|-----------|-------:|
| User pain severity | 25% |
| Business impact (revenue, retention, expansion) | 25% |
| Strategic fit (alignment with vision) | 20% |
| Timing sensitivity (competitive urgency) | 15% |
| Execution feasibility | 15% |

```
Weighted score = sum of (dimension score x weight)
```

## Phase 5: Second-order effects and pre-mortem

For the top two or three options:
- **Effect chain** - direct effect → second-order effect → third-order effect
- **Opportunity cost** - what gets delayed or killed
- **Team effect** - morale, skills, hiring
- **Market signal** - what the choice tells customers and competitors

Then run a pre-mortem: "It is six months from now and this failed. What happened?"

| Failure scenario | Probability | Early warning signal |
|------------------|------------:|----------------------|
| [specific scenario 1] | [%] | [signal] |
| [specific scenario 2] | [%] | [signal] |
| [specific scenario 3] | [%] | [signal] |

## Phase 6: Synthesis and recommendation

- **Summary** - one sentence: what to do and why
- **Confidence level** - high, medium, or low, with the reason
- **Framework convergence** - what each framework says, where they agree and disagree, and what the divergence reveals
- **The recommendation** - two to three paragraphs of clear reasoning
- **What would change this recommendation**
  1. If we learned [X], we might instead do [Y]
  2. If metric [Z] changes by more than [N%], reconsider
  3. If a competitor does [W], reassess
- **Immediate next steps (this week)** - three specific actions with owners

## Output

- Source log with signal, recency, and confidence per source
- Situation model
- Impact and confidence matrix including "do nothing"
- Weighted alignment scores with the math shown
- Second-order effects and pre-mortem for the leading options
- Recommendation with confidence level, reversal conditions, and next steps

## Operating rules

**Always**
- Assemble and log the context before reasoning
- Show reasoning chains and the scoring math
- Quantify where possible and state confidence levels
- Include "do nothing" as an explicit option
- Separate observation from interpretation

**Never**
- Rely on a single framework
- Ignore contradictions between sources
- Recommend without stating trade-offs and opportunity cost
- Agree with the framing of the question just because it was asked that way
- Hide missing context instead of naming it
