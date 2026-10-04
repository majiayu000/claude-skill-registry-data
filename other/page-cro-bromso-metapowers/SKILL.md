---
description: Optimize conversion rates for landing and product pages
---

# Page CRO

Optimize landing pages and product pages for "$ARGUMENTS". Analyze current conversion performance and recommend improvements to increase conversion rate.

## Prerequisites

Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md`. If this file does not exist, tell the user:

> Phase 0 (Strategy) has not been completed for "$ARGUMENTS". Run `/marketing:customer-research $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/marketing/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md` for audience and positioning
   - Read `.metapowers/marketing/$ARGUMENTS/02-act.md` if it exists

2. **Page audit (if URL provided):**
   - Use WebFetch to analyze the page
   - Evaluate: headline clarity, value proposition visibility, CTA prominence, social proof, objection handling
   - Check page speed and mobile experience
   - Identify friction points in the conversion path

3. **Analyze page structure:**
   - Above-the-fold content: does it answer "what, who, why"?
   - Information hierarchy: is the most important content most prominent?
   - Visual flow: does the eye naturally reach the CTA?
   - Content length: appropriate for the decision complexity?

4. **CRO recommendations:**
   - Headline and subheadline improvements
   - CTA placement, copy, and design recommendations
   - Social proof placement and type
   - Objection handling and FAQ placement
   - Trust signals (security badges, guarantees, testimonials)
   - Page speed and technical improvements

5. **A/B test suggestions:**
   - Identify the highest-impact elements to test
   - For each: hypothesis, variant description, expected impact
   - Prioritize by potential uplift and ease of implementation

6. **Write the artifact** — append to `.metapowers/marketing/$ARGUMENTS/02-act.md` under a `## Page CRO` section:
   - **Current State Assessment** — strengths and weaknesses
   - **Recommendations** — prioritized by impact
   - **A/B Test Suggestions** — with hypotheses
   - **Wireframe Notes** — suggested layout changes
   - **Expected Impact** — estimated conversion lift per change

## Output

Page CRO analysis appended to `.metapowers/marketing/$ARGUMENTS/02-act.md`. Present a summary highlighting:
- Top 3 conversion blockers identified
- Highest-impact recommendation
- Suggested first A/B test
