---
name: product-market-fit
description: >
  Assess and improve product-market fit. Use when the user says "product-market fit",
  "PMF", "do we have PMF", "why aren't users retaining", "we're not growing",
  "users aren't sticking", "PMF pyramid", "find our target customer",
  "are we building for the right person", or wants to diagnose why a product
  isn't growing or retaining - even if they don't explicitly say "product-market fit".
---

## Overview

Based on **The Lean Product Playbook** by Dan Olsen. Olsen's PMF Pyramid is a structured framework for diagnosing and improving product-market fit. The pyramid has five layers - each layer must be solid before the next one matters. Most teams skip to layer 4 or 5 (features, UX) when the real problem is layer 1 or 2 (wrong customer, wrong need).

**The PMF Pyramid (bottom to top):**
1. Target customer
2. Underserved needs
3. Value proposition
4. Feature set
5. UX

## Workflow

### Step 1: Validate the target customer (Layer 1)
Who exactly is this product for? Be specific:
- Demographics or firmographics
- Behavior patterns (what do they do today?)
- Psychographics (what do they care about?)

If the answer is "everyone" or "anyone who needs X" - the target customer is not defined. Narrow it.

Test: can you describe a specific person by name and context? "A solo founder building their first SaaS product, pre-revenue, doing all support themselves." That's a target customer.

### Step 2: Map underserved needs (Layer 2)
What needs does the target customer have that are not being met well today?

Olsen's importance-satisfaction framework:
- List 10-15 needs/jobs the customer has
- Rate each: How important is this? (1-5)
- Rate each: How satisfied are they today with existing solutions? (1-5)
- **Underserved needs = High importance, Low satisfaction**

These are your opportunities. Build for underserved needs, not just any need.

### Step 3: Define the value proposition (Layer 3)
For the top 2-3 underserved needs: what is your specific claim about how you serve them better?

Format: "For [target customer] who [underserved need], [product name] is [category] that [key benefit]. Unlike [alternatives], we [key differentiator]."

If you can't write this cleanly, the value proposition isn't clear enough to test.

### Step 4: Audit the feature set (Layer 4)
Map current features to underserved needs. For each feature ask:
- Which underserved need does this serve?
- Is this feature good enough to be a key differentiator?
- Is this a table-stakes feature (must have but not differentiating)?

Remove or deprioritize features that don't map to the top underserved needs.

### Step 5: Assess UX (Layer 5)
Does the UX deliver on the value proposition clearly?
- First-time user test: can a target customer reach the core value in under 5 minutes?
- Does the onboarding communicate the value proposition before asking for effort?

### Step 6: Measure PMF
Sean Ellis test: survey users with "How would you feel if you could no longer use [product]?"
- Very disappointed / Somewhat disappointed / Not disappointed
- **40%+ "very disappointed" = strong PMF signal**
- Below 40%: go back to layers 1-3 before investing in growth

### Step 7: Identify the layer to fix
PMF problems are almost always in layers 1-3, not 4-5. Diagnosis:
- Low retention - likely layer 2 (needs not underserved enough)
- High churn after onboarding - likely layer 3 (value prop not landing)
- Users use it but won't pay - likely layer 1 (wrong target customer) or layer 3

## Anti-Patterns

**1. Optimizing UX before validating the need**
Bad: Redesigning the UI to improve retention when users are churning because the core need isn't met.
Good: Fix layers 1-3 before investing heavily in layers 4-5.

**2. Target customer too broad**
Bad: "Our target customer is small business owners."
Good: "Our target customer is solo consultants doing $10-100k/yr who invoice clients manually and lose track of unpaid invoices."

**3. Importance-satisfaction done in a meeting**
Bad: Team guesses importance and satisfaction scores internally.
Good: Survey or interview actual target customers for real scores.

**4. Chasing the 40% number with the wrong segment**
Bad: Averaging "very disappointed" scores across all user types.
Good: Segment by target customer. 40% among your core segment is the signal that matters.

## Quality Checklist

- [ ] Target customer defined specifically (not "everyone")
- [ ] Underserved needs mapped using importance-satisfaction framework
- [ ] Value proposition written in structured format
- [ ] Feature set mapped to underserved needs - orphaned features flagged
- [ ] UX assessed: can target customer reach core value in under 5 minutes?
- [ ] Sean Ellis PMF survey run or planned
- [ ] Weakest pyramid layer identified and prioritized for improvement
