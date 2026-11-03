---
name: sales-call-prep
description: Prepare for one upcoming sales call, including the first discovery call — the goal, an agenda, who attends and what each cares about, open questions for the deal's unknowns, and the one next step to ask for. Use when a seller has a call coming up and wants to walk in prepared. Not for writing up a call that has happened; see /sales-discovery.
metadata:
  argument-hint: "[deal] [call]"
---

# Call prep

Prepare the call in "$ARGUMENTS".

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

When `$ARGUMENTS` or the request names a deal, use that name as `<deal>` whether or not its folder exists yet in `.singularskills/sales/`. With no deal named: with exactly one deal folder there (not `playbook`), use it; with several, ask which; with none, read none and continue. Read whichever of `01-qualify.md` to `05-close.md` exist for the deal.

## Process

1. **The goal:** the one thing this call must achieve (learn the decision process, meet the economic buyer, agree the close plan).

2. **Who attends:** each person, their role and what they care about, from the deal's artifacts or the user; anyone important who is not attending, and how to reach them.

3. **The agenda:** a short opening to confirm time and goals, then the buyer talking first.

4. **Questions** for the deal's unknowns, as `references/qualification.md` describes: open, one at a time, following up on the buyer's words, about their situation, problem, its impact and the cost of doing nothing, before any pitch. For a first discovery call, cover the MEDDPICC elements that are unknown.

5. **The next step to ask for,** specific and dated.

6. **Honest selling.** No false urgency, no fake scarcity, no misrepresentation of the product or a competitor, and no commitment (discount, term, date, feature) beyond the policy the user stated; anything beyond it is marked **for approval**, with who approves.

## Output

In chat: the goal, attendees, agenda, questions and the next step to ask for. This skill writes no file; after the call, `/sales-discovery` writes it up from the notes.
