---
name: coaching-strategy
description: Review a business plan, positioning or product strategy as a business strategist — value proposition, positioning, moat, problem fit, growth, pricing, risks and metrics — in a scored coaching report. Use when the user wants a critical second opinion on their strategy document or pitch before acting on it. Not for creating a brand platform; see /branding-strategy.
metadata:
  argument-hint: "<file-or-topic> [--skip-checks]"
---

# Strategy Coaching

Review "$ARGUMENTS" through the lens of a business strategist. Provide mentorship feedback on market positioning, competitive differentiation, value proposition, and growth strategy.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Derive `<project>` from the argument by taking its basename without extension and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"coaching-strategy","workflow":"coaching","phase":null,"project":"<project>","event":"skipped","artifact":"<artifact file>","note":"<reason or \"none given\">"}`.

## Prerequisites

None — this is a utility skill that can run anytime.

## Process

1. **Read the target:**
   - Read the business plan, strategy document, product spec, or positioning doc specified in "$ARGUMENTS"
   - If marketing artifacts exist (`.singularskills/marketing/`), read relevant strategy docs
   - If branding artifacts exist (`.singularskills/branding/`), read the brand platform

2. **Read reference material:**
   - Read `references/feedback-format.md` for output structure

3. **Evaluate the strategy:**
   - **Value proposition:** Is it clear, compelling, and differentiated?
   - **Market positioning:** Is the target market well-defined? Is positioning defensible?
   - **Competitive advantage:** What's the moat? Is it sustainable?
   - **Customer-problem fit:** Does the solution address a real, validated problem?
   - **Growth strategy:** Are growth levers identified? Is the approach scalable?
   - **Pricing:** Does pricing reflect value? Is it competitive?
   - **Risk assessment:** Are key risks identified? Are there mitigation plans?
   - **Metrics:** Are success metrics defined and measurable?

4. **Write the coaching report** to `.singularskills/coaching/<project>/strategy-review.md` following the feedback format.

## Output

The strategy coaching report written to `.singularskills/coaching/<project>/strategy-review.md`. Present the score and top 3 suggestions to the user.
