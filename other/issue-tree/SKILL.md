---
name: issue-tree
description: >
  Decompose a business problem MECE using an issue tree, generate hypotheses, and
  prioritize branches for investigation. Use when a consultant says "help me structure
  this problem", "I need to break down this issue", "build me an issue tree", "I don't
  know where to start on this problem", "help me frame the problem", "what are the
  hypotheses here", "we need to prioritize our analysis", or "the client problem is too
  broad". Also trigger when describing a complex or ambiguous business problem that
  needs systematic decomposition before analysis begins, or when an engagement is
  starting and a workplan needs to be structured from a problem statement.
---

## Overview

Based on **"The McKinsey Way"** by Ethan Rasiel and **"Bulletproof Problem Solving"** by Conn and McLean. An issue tree is the primary tool for structuring complex problems before jumping to solutions. The goal is to decompose the problem into its components until each branch is answerable by a single analysis or interview. Done well, it prevents the most common consulting failure: solving the wrong problem rigorously.

The MECE principle (Mutually Exclusive, Collectively Exhaustive) is the test for every level of the tree. No overlap between branches. No gaps in the full set.

## Workflow

### Step 1: Write the Problem Statement

Start with a precise problem statement. Vague problems produce vague trees.

A good problem statement:
- Names who has the problem (the client, a specific business unit, customers)
- States the gap between current state and desired state with data where possible
- Is scoped in time ("by end of Q4" or "over the next 3 years")
- Avoids pre-supposing the cause or solution

Template:
```
[Who] needs to [close gap / achieve outcome] by [when].
Currently: [current state with data]
Target: [desired state with data]
The question: [What needs to be true / what is causing the gap / what should we do]
```

Example:
```
[Your client]'s mid-market division needs to improve gross margin from 18% to 25%
by end of next fiscal year. The question is: what is driving the margin gap and
what levers can realistically close it within 12 months?
```

### Step 2: Choose the Tree Type

Two primary tree structures:

**Diagnostic tree (why)**: Use when the problem is "why is X happening?" Decomposes causes.
```
Problem: Why is gross margin declining?
- Revenue side
  - Price realization declining
  - Mix shift to lower-margin products
- Cost side
  - COGS increasing
  - Overhead not scaling with volume
```

**Solution tree (how)**: Use when the problem is "how do we achieve X?" Decomposes levers.
```
Goal: How do we increase gross margin by 7 points?
- Increase revenue without increasing costs
  - Raise prices
  - Shift mix to higher-margin segments
- Decrease costs
  - Reduce COGS (sourcing, manufacturing)
  - Reduce overhead (eliminate, automate, offshore)
```

Choose the tree type before building. Mixing diagnostic and solution branches in the same tree creates logical confusion.

### Step 3: Build the First Level - MECE

The first level of the tree must be MECE. Start with a standard decomposition structure, then adapt it.

Common first-level frameworks:
- **Business system**: Revenue / Cost / Capital (for margin or profitability problems)
- **Value chain**: Supplier / Operations / Sales / Service (for operational problems)
- **Market**: Market size / Market share / Pricing (for growth problems)
- **Customer**: Acquisition / Retention / Monetization (for customer problems)
- **Time**: Short-term / Long-term (when the decision horizon matters)

MECE test for first level:
1. Can any finding belong to more than one branch? (If yes: overlap - merge or reframe)
2. Could a major cause or lever exist that is not covered? (If yes: gap - add branch)

### Step 4: Build Second and Third Levels

Decompose each first-level branch until you reach "leaf nodes" - issues small enough to be answered by a single analysis or interview series.

Signs a branch is ready to be a leaf node:
- It can be answered with a yes/no or a specific number
- It maps to a single analysis (regression, benchmarking, survey, interview series)
- One person or team owns the relevant data

Signs a branch needs further decomposition:
- It requires multiple different types of analysis
- It spans multiple teams or data sources
- It is still a category, not a testable question

Practical depth: most issue trees are 3-4 levels deep. Deeper than 4 levels usually means the branches need merging, not further splitting.

### Step 5: Generate Hypotheses

For each leaf node, generate a hypothesis - a specific, falsifiable statement about what is true.

Template:
```
Issue: [branch/leaf]
Hypothesis: [specific, testable claim - not "might be" but "is" or "is not"]
Evidence to confirm: [what data would confirm this]
Evidence to refute: [what data would refute this]
Priority: [High / Medium / Low] based on impact and probability
```

McKinsey's hypothesis-driven approach: do not start analysis without a hypothesis. The hypothesis tells you what data to collect. Without it, you collect everything and find nothing.

### Step 6: Prioritize Branches

Not all branches deserve equal analytical effort. Prioritize using two axes:

- **Impact**: if this branch explains the problem, how much of the problem does it explain?
- **Probability**: based on preliminary knowledge, how likely is this branch to be the root cause or most important lever?

Prioritization matrix:
```
High impact + High probability  = Analyze first (critical path)
High impact + Low probability   = Analyze second (high stakes)
Low impact  + High probability  = Analyze third (quick wins)
Low impact  + Low probability   = Deprioritize or drop
```

Document which branches are on the critical path. These are your Week 1 priorities. Low-impact branches are cut or deferred.

### Step 7: Map to Workplan

Convert the prioritized tree into a workplan:

Template:
```
Branch: [issue]
Analysis required: [specific analysis - regression, survey, benchmark study, etc.]
Data needed: [source + owner]
Owner: [team member]
Timeline: [week]
Output: [what this produces - chart, number, interview summary]
Hypothesis to test: [specific statement]
```

This is how an issue tree becomes a project plan. Each leaf node is a work task with an owner and a deadline.

## Anti-Patterns

**1. Solution tree disguised as a diagnostic tree**
Bad: "Why is revenue low? We need better marketing, better sales, better pricing."
Good: Keep the diagnostic tree on causes only. Run a separate solution tree after diagnosing the root cause.
Mixing causes and solutions creates circular reasoning and skips the diagnosis.

**2. Non-MECE first level**
Bad: First level includes "Pricing", "Sales team", and "Market conditions" - these overlap (sales team affects pricing, pricing is affected by market conditions).
Good: Use a standard, tested framework (revenue/cost, acquire/retain/monetize) for the first level, then adapt.
A non-MECE first level cascades errors down the entire tree.

**3. Hypotheses that are not falsifiable**
Bad: "Customer experience might be a factor."
Good: "Customer satisfaction scores below 7/10 are causing 40%+ churn in the enterprise segment."
Unfalsifiable hypotheses cannot be confirmed or refuted. They waste analysis time.

**4. Going too deep too fast**
Bad: Building 5 levels of decomposition before testing the first level for MECE.
Good: Build level 1, check MECE, get a second opinion, then proceed to level 2.
Errors in early levels multiply. Fix them before going deeper.

**5. Treating the tree as the output**
Bad: Presenting the issue tree to the client as the deliverable.
Good: The issue tree is an internal tool. The client sees findings and recommendations, not the analytical structure behind them.

## Quality Checklist

- [ ] Problem statement names who, what gap, what time horizon, and avoids pre-supposing the cause
- [ ] Tree type chosen (diagnostic "why" vs. solution "how") before building
- [ ] First level branches are MECE - no overlaps, no gaps
- [ ] Each leaf node maps to a single analysis or set of interviews
- [ ] At least one hypothesis per leaf node, stated as a falsifiable claim
- [ ] Branches prioritized by impact x probability
- [ ] Critical path branches identified and assigned to Week 1 workplan
- [ ] Total depth is 3-4 levels (not 2, not 6)
- [ ] Framework used for first level is named and justified
