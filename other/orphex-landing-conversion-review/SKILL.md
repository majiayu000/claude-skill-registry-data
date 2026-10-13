---
name: orphex-landing-conversion-review
description: "Locate observed landing and funnel friction, then propose diagnostic checks or experiments without asserting untested causes."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Landing Conversion Review

Review supplied page copy, screenshots, funnel exports, experiment notes, and analytics documents. Orphex MCP may provide data when already available and authorized, but the review must also work from files the user supplies. Do not claim to have opened or inspected an unprovided live page.

## Define the funnel

Record the page or variant, target audience, traffic sources, date range, account timezone, device or locale segments, and the intended conversion. Name each funnel event and denominator, such as sessions to form starts to submitted leads to qualified leads. Do not call unlike stages the same conversion.

For each stage, show counts and the relevant rate. State whether the denominator is sessions, users, clicks, or a prior funnel stage. Check for duplicate submissions, consent or bot filters, missing pages, and event-definition differences when source documents provide evidence. Mark unavailable stages and zero denominators explicitly.

Segment only where the supplied data supports it. Device, source, campaign, locale, returning status, and page variant can explain aggregate movement through mix changes. Show the segment's volume before comparing rates. Do not infer that a device experience caused a gap when traffic intent or campaign mix also differs.

When screenshots or copy are supplied, connect each proposed friction point to visible evidence, such as unclear offer language, mismatched message, hidden action, form burden, or missing reassurance. Separate what the artifact shows from what needs live usability or performance evidence. Do not diagnose load time from a screenshot.

## Explain limits and choose next checks

Treat observational conversion gaps as associations. A before-and-after change may also reflect traffic, seasonality, spend, or tracking shifts. Use a properly documented randomized experiment for causal claims. If sample size or assignment details are missing, say so and propose a test or additional cut rather than declaring a winner.

Prioritize hypotheses by likely user impact, evidence strength, and ease of checking. For each one, state the observed pattern, possible explanation, next measurement or test, primary metric, guardrail, and relevant segment. Preserve one main change per test when the goal is to learn causality.

## Recommended output

State the conversion definition and period first. Show a funnel table with counts and rates, then a short list of observed friction signals and testable hypotheses. Close with missing evidence and the next check that would most reduce uncertainty.
## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py weighted-ratio < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
