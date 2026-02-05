---
name: ice-scorer
description: Automatically score growth experiments using the ICE framework (Impact × Confidence × Ease). Use when the user creates a new experiment, mentions scoring or prioritization, or when analyzing experiment backlogs. Helps prioritize experiments by evaluating Impact (1-10), Confidence (1-10), and Ease (1-10).
allowed-tools: [Read, Write]
---

# ICE Scorer Skill

Automatically score growth experiments using the ICE (Impact, Confidence, Ease) prioritization framework.

## When to Activate

This skill should activate when:
- User creates a new experiment without providing ICE scores
- User mentions "score", "prioritize", or "ICE"
- User asks "which experiment should I run first?"
- User wants to evaluate experiment backlog
- User compares multiple experiments

## ICE Framework Scoring Guidelines

### Impact (1-10): How much will this move the key metric?

**Score 8-10: High Impact**
- Affects North Star metric directly
- Expected change ≥15%
- Targets large user segment
- Critical business metric

**Score 4-7: Medium Impact**
- Affects important but secondary metrics
- Expected change 5-15%
- Targets meaningful user segment
- Supports key business goals

**Score 1-3: Low Impact**
- Affects minor or vanity metrics
- Expected change <5%
- Targets small user segment
- Nice-to-have improvement

### Confidence (1-10): How certain are we this will work?

**Score 8-10: High Confidence**
- Strong quantitative data supporting hypothesis
- User research validates the problem
- Similar experiments succeeded elsewhere
- Multiple sources of evidence
- Detailed rationale (>100 characters)

**Score 4-7: Medium Confidence**
- Some supporting data or research
- Analogous experiments showed promise
- Logical reasoning with limited evidence
- Moderate rationale (50-100 characters)

**Score 1-3: Low Confidence**
- Speculative or gut feeling
- No supporting data
- Untested assumption
- Minimal rationale (<50 characters)

### Ease (1-10): How easy is this to implement?

**Score 8-10: High Ease**
- < 1 day of work
- No engineering required, or minimal changes
- No external dependencies
- Can be done with existing tools

**Score 4-7: Medium Ease**
- 1-2 days of work
- Some engineering work required
- May need design support
- Uses existing infrastructure

**Score 1-3: Low Ease**
- > 2 days of work
- Significant engineering effort
- Requires design and multiple teams
- Needs external resources or new tools

## Scoring Process

When scoring an experiment:

1. **Read the experiment file** from the experiments folder

2. **Analyze the hypothesis components**:
   - Proposed change
   - Target audience
   - Expected outcome (look for specific percentages)
   - Rationale (check length and evidence quality)

3. **Evaluate Impact**:
   - Is this a North Star metric or secondary metric?
   - What's the expected percentage change?
   - How many users will this affect?
   - Consider the experiment category (acquisition, activation, etc.)

4. **Evaluate Confidence**:
   - How much evidence supports the hypothesis?
   - Is there user research or data mentioned?
   - How detailed is the rationale?
   - Are there comparable experiments?

5. **Evaluate Ease**:
   - Estimate implementation time
   - Does it need engineering? Design? External resources?
   - How complex is the proposed change?
   - Look for keywords: "redesign" (low ease), "copy change" (high ease)

6. **Calculate total ICE score**: Impact × Confidence × Ease

7. **Interpret the score**:
   - 700+: Critical Priority - implement immediately
   - 500-699: High Priority - strong candidate
   - 300-499: Medium Priority - good experiment
   - 150-299: Low Priority
   - <150: Very Low Priority - deprioritize

8. **Update the experiment JSON** with ICE scores

9. **Move to pipeline if score ≥ 300**

## Scoring Examples

### Example 1: Onboarding Progress Indicators

**Experiment:** Add progress indicators to 5-step onboarding flow

**Analysis:**
- Impact: 7 - Activation is important, expected 15% increase
- Confidence: 6 - User research supports it, but not tested yet
- Ease: 9 - Simple UI element, <1 day of work
- **Total: 378** - Medium-High Priority

**Reasoning:**
- Impact: Activation is a key metric but not the only North Star
- Confidence: User research provides evidence but no previous tests
- Ease: Adding progress bar is straightforward UI work

### Example 2: Social Proof on Pricing Page

**Experiment:** Add customer logos and testimonials to pricing page

**Analysis:**
- Impact: 7 - Affects acquisition and conversion
- Confidence: 8 - Strong industry evidence for B2B social proof
- Ease: 9 - Design change only, no engineering
- **Total: 504** - High Priority

**Reasoning:**
- Impact: Pricing page is high-traffic, affects key conversion
- Confidence: Multiple case studies show 10-15% improvement
- Ease: Simple asset placement, quick implementation

### Example 3: Complete Platform Redesign

**Experiment:** Redesign entire user interface

**Analysis:**
- Impact: 9 - Could affect all metrics significantly
- Confidence: 4 - No data supporting specific improvements
- Ease: 2 - Months of work, multiple teams
- **Total: 72** - Very Low Priority

**Reasoning:**
- Impact: Broad changes could have major impact
- Confidence: Too vague, no specific hypothesis about what will improve
- Ease: Massive undertaking, not a growth "experiment"

## Keywords to Watch

**Low Ease indicators:**
- redesign, rebuild, refactor, overhaul, migration, infrastructure

**High Ease indicators:**
- copy change, button, color, image, text, email, simple

**High Confidence indicators:**
- "data shows", "research indicates", "we tested", "similar experiment"

**High Impact indicators:**
- North Star, conversion, activation, retention, revenue
- Specific percentages (e.g., "15% increase")
- Large user segments

## Output Format

When providing ICE scores, explain your reasoning:

```
ICE Score Analysis for: [Experiment Title]

Impact: [score]/10
Reasoning: [Why this score based on metric importance, expected change, audience size]

Confidence: [score]/10
Reasoning: [Why this score based on evidence, data, research quality]

Ease: [score]/10
Reasoning: [Why this score based on time, resources, complexity]

Total ICE Score: [Impact × Confidence × Ease] = [total]

Priority: [Critical/High/Medium/Low/Very Low]
Recommendation: [What to do with this experiment]

[If score >= 300:]
✓ Moving to pipeline based on strong ICE score
```

## Integration with Commands

This skill works automatically when:
- `/experiment-create` completes - offer to score immediately
- `/hypothesis-generate` creates ideas - suggest preliminary scores
- User asks about prioritization

## Continuous Learning

After experiments complete:
- Compare predicted Impact vs actual results
- Adjust scoring calibration based on outcomes
- Learn patterns for better Confidence scoring
- Refine Ease estimates based on actual time taken
