---
name: sales-objection
description: Draft a response to one objection in one live deal — questions that find what lies behind it before assuming, and an answer grounded in the deal's facts — never deceptive or pressuring. Use when a buyer has raised a concern in a deal and the seller needs to respond well. Not for the team's objection-handling guide; see /marketing-sales-enablement.
metadata:
  argument-hint: "[deal] <objection>"
---

# Objection

Help the seller respond to the objection in "$ARGUMENTS".

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

The objection, in the buyer's words if possible, and the context. When `$ARGUMENTS` or the request names a deal, use that name as `<deal>` whether or not its folder exists yet in `.singularskills/sales/`. With no deal named: with exactly one deal folder there (not `playbook`), use it; with several, ask which; with none, read none and continue. Read the team's objection guide in the seller's own marketing project in `.singularskills/marketing/*/` (marketing projects are named after the seller's product or company, not the buyer: with exactly one folder there, use it; with several, ask once which is the seller's) when it exists.

## Process

1. **Do not assume what it means.** The same words ("too expensive", "we'll keep using spreadsheets", "not now") can mean different things. Write two or three possible concerns behind it, each marked **possible**, not known.

2. **Questions to ask first:** open questions that let the buyer say what lies behind it ("what would have to be true for this to be worth it?", "what's working well about the spreadsheets today?"), one at a time.

3. **A response for each likely concern,** grounded in the deal's facts (the buyer's own pains and metrics from the deal's artifacts) and in what the product really does. If the objection is right (the product does not fit), say so and suggest the honest next step.

4. **Honest selling.** No false urgency, no fake scarcity, no misrepresentation of the product or a competitor, and no commitment (discount, term, date, feature) beyond the policy the user stated; anything beyond it is marked **for approval**, with who approves.

## Output

In chat: the possible concerns, the questions to ask first, and the responses. This skill writes no file.
