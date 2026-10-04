---
name: competitive-analysis
description: Use when user says "research competitors", "competitive analysis", "how do we compare to X", when planning go-to-market and needs competitive positioning, when assessing the competitive landscape before launch, or when objection handling and win/lose scenarios need to be documented.
---

# Competitive Analysis

## Overview

Read `.forge/prd.md` to understand what we're building, then produce `.forge/competitive.md` — an honest assessment of the competitive landscape with actionable positioning. The output must be brutally honest about where we lose, not just where we win.

## When to Use

- `.forge/prd.md` exists and the product is entering a market with existing players
- User asks "who are the competitors" or "how do we differentiate"
- Preparing for GTM and need positioning statements and objection handling
- Investor pitch requires competitive landscape slide

## When NOT to Use

- No PRD exists — run `spec-driven-development` first (you need to know what you're building to compare)
- The product creates a new category with no direct competitors — focus on adjacent alternatives instead
- User wants a quick opinion, not a structured analysis — just answer the question

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We don't have real competitors" | You always have competitors — at minimum, the status quo (spreadsheets, manual process) |
| "We're better at everything" | No product wins on every axis. If your matrix shows all green, you're lying to yourself |
| "Pricing research takes too long" | Public pricing pages take 10 minutes. If pricing is hidden, that IS the data point |
| "Our moat is obvious" | If you can't name it in one sentence, you don't have one |
| "Win/lose scenarios are speculative" | They're based on feature gaps and buyer priorities — that's analysis, not speculation |

## Red Flags

- Feature matrix shows you winning every category (cheerleading, not analysis)
- "Lose" scenarios are empty or dismissive ("unlikely")
- Competitor profiles are surface-level (just website taglines)
- Positioning statement is more than one sentence
- No mention of the status quo as a competitor (incumbent inertia)
- Objection responses are generic ("we're better") instead of specific

## Core Process

### Step 1: Identify competitors

Read `.forge/prd.md`. List:
- **Direct competitors**: same problem, same buyer, similar solution
- **Indirect competitors**: same problem, different approach
- **Status quo**: what buyers do today without any tool (spreadsheets, manual processes, hiring)

Minimum 3 competitors. Include the status quo as a competitor.

### Step 2: Build competitor profiles

For each competitor:
- Company name, founding year, funding/revenue (if public)
- Target customer (their ICP, not yours)
- Core value proposition (one sentence)
- Pricing model and approximate price points
- Key strengths (be honest — what are they genuinely good at?)
- Key weaknesses (specific, not generic)

### Step 3: Feature matrix

Build a comparison table. Columns: your product + each competitor. Rows: features from the PRD's requirements list. Values: ✓ (has it), ✗ (doesn't), ~ (partial/planned).

**Honesty check**: if your product has ✓ in every row, you've cherry-picked the features. Add rows where competitors win.

### Step 4: Win/lose scenarios

For each competitor, write:
- **We win when**: specific buyer profile + situation where we're the better choice
- **We lose when**: specific buyer profile + situation where they're the better choice
- **Switching cost**: what a buyer gives up to switch from them to us

### Step 5: Positioning statement

One sentence: "For [ICP] who [pain point], [product] is the [category] that [key differentiator], unlike [primary competitor] which [their limitation]."

### Step 6: Objection handling

Top 5 objections a buyer raises when comparing to each competitor. For each: the objection, the honest answer, the redirect to our strength.

### Step 7: Moat analysis

Answer: what do we have that competitors can't easily copy? Data? Network effects? Regulatory advantage? Integration lock-in? If the answer is "nothing yet" — say so honestly and identify what to build toward.

## Output

Write `.forge/competitive.md` with all sections above. Prepend a `forge:meta` header (`generated_by: competitive-analysis`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/prd.md]` — paths only, never hashes, `generated_from: {.forge/prd.md: <upstream content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

After writing: "Competitive analysis written to `.forge/competitive.md`. Run `/gtm` to build the go-to-market strategy."

## Verification

- [ ] `.forge/prd.md` read before starting
- [ ] At least 3 competitors profiled (including status quo)
- [ ] Feature matrix includes rows where competitors win
- [ ] Win/lose scenarios are honest — lose scenarios are real, not dismissive
- [ ] Positioning statement is one sentence
- [ ] Objection responses are specific to each competitor
- [ ] Moat analysis is honest (says "none yet" if true)
- [ ] `.forge/competitive.md` written
