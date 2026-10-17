---
name: experiment-design
description: >
  Design product experiments to test hypotheses. Use when the user says "run an experiment",
  "A/B test this", "build-measure-learn", "validate this assumption", "test this hypothesis",
  "we don't know if this will work", "minimum viable test", "lean experiment",
  or wants to reduce risk before fully building a feature
  - even if they don't explicitly say "experiment".
---

## Overview

Based on **The Lean Startup** by Eric Ries. The core insight: startups (and product teams) don't fail from lack of execution - they fail from executing on the wrong plan. The build-measure-learn loop is how you find the right plan faster. Every feature is a hypothesis. Every release is an experiment. Validated learning - not shipped features - is the unit of progress.

## Workflow

### Step 1: State the hypothesis
Format: "We believe [action/feature] will cause [user behavior change], resulting in [metric change], because [assumption]."

Example: "We believe adding a progress bar to onboarding will cause more users to complete setup, resulting in a 15% increase in activation rate, because users abandon when they can't see how much is left."

The "because" is critical - it forces you to name the assumption you're testing.

### Step 2: Identify the riskiest assumption
Most hypotheses have multiple assumptions embedded. Find the one that, if wrong, makes the whole hypothesis collapse.

List assumptions - rank by risk - test the riskiest one first.

### Step 3: Design the minimum viable test
What's the cheapest, fastest way to test the riskiest assumption?

Ries's ladder of experiment types (least to most expensive):
1. **Customer interview** - ask 5 users if the problem exists
2. **Fake door / 404 test** - show the feature, measure click rate before building
3. **Concierge MVP** - do the job manually for a few users
4. **Wizard of Oz** - appear automated, run manually behind the scenes
5. **A/B test** - build both versions, split traffic
6. **Full release** - ship to everyone

Start as low on the ladder as possible. Only move up when the cheaper test is insufficient.

### Step 4: Define success criteria before running
Set the threshold before you see results. This prevents moving the goalposts.

"We will consider this experiment successful if [metric] changes by [amount] within [time period] with [sample size]."

### Step 5: Calculate required sample size
For A/B tests: use a significance calculator. Undersized tests produce false results.
- Minimum detectable effect: what's the smallest change that matters?
- Baseline conversion rate: what's the current rate?
- Statistical significance: 95% standard (p < 0.05)

### Step 6: Run the experiment and measure
- Don't peek at results early (peeking inflates false positives)
- Measure the primary metric and guard metrics
- Document what you observe, not what you expected

### Step 7: Extract validated learning
Whatever the result:
- **Confirmed** - assumption was right, proceed with confidence
- **Refuted** - assumption was wrong, pivot or kill
- **Inconclusive** - sample too small or test too short, iterate

Ries: a failed experiment that teaches you something is more valuable than a successful one that teaches you nothing.

## Anti-Patterns

**1. HiPPO-driven decisions instead of experiments**
Bad: "The CEO thinks we should add X, so we're adding X."
Good: "The CEO thinks X will increase retention. Let's run a 2-week experiment with 10% of users."

**2. Moving the goalposts**
Bad: Setting a 20% lift as success, seeing 8%, calling it a win anyway.
Good: Success criteria set before the experiment runs. Results are binary: met or not met.

**3. Testing too many variables at once**
Bad: Redesigning the entire onboarding and A/B testing it.
Good: Change one variable per experiment. Otherwise you can't attribute the result.

**4. Skipping the concierge step**
Bad: Building a full automated feature to test an unvalidated assumption.
Good: Do it manually for 10 users first. If the manual version doesn't work, the automated one won't either.

## Quality Checklist

- [ ] Hypothesis follows "We believe X will cause Y because Z" format
- [ ] Riskiest assumption identified explicitly
- [ ] Minimum viable test chosen (as low on the ladder as possible)
- [ ] Success criteria defined before running
- [ ] Sample size calculated for quantitative tests
- [ ] Guard metrics defined (what must not get worse)
- [ ] Validated learning documented regardless of outcome
