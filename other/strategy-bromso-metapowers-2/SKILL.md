---
description: Review strategy through the lens of a business strategist
---

# Strategy Coaching

Review "$ARGUMENTS" through the lens of a business strategist. Provide mentorship feedback on market positioning, competitive differentiation, value proposition, and growth strategy.

## Prerequisites

None — this is a utility skill that can run anytime.

## Process

1. **Read the target:**
   - Read the business plan, strategy document, product spec, or positioning doc specified in "$ARGUMENTS"
   - If marketing artifacts exist (`.metapowers/marketing/`), read relevant strategy docs
   - If branding artifacts exist (`.metapowers/branding/`), read the brand platform

2. **Read reference material:**
   - Read `plugins/coaching/shared/feedback-format.md` for output structure

3. **Evaluate the strategy:**
   - **Value proposition:** Is it clear, compelling, and differentiated?
   - **Market positioning:** Is the target market well-defined? Is positioning defensible?
   - **Competitive advantage:** What's the moat? Is it sustainable?
   - **Customer-problem fit:** Does the solution address a real, validated problem?
   - **Growth strategy:** Are growth levers identified? Is the approach scalable?
   - **Pricing:** Does pricing reflect value? Is it competitive?
   - **Risk assessment:** Are key risks identified? Are there mitigation plans?
   - **Metrics:** Are success metrics defined and measurable?

4. **Write the coaching report** to `.metapowers/coaching/$ARGUMENTS/strategy-review.md` following the feedback format.

## Output

The strategy coaching report written to `.metapowers/coaching/$ARGUMENTS/strategy-review.md`. Present the score and top 3 suggestions to the user.
