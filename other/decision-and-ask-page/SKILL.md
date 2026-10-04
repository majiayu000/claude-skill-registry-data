---
name: decision-and-ask-page
description: Build the decision page that converts the recommendation into a specific, votable ask, with options considered, the recommended option, and what approval commits the board to.
---

# Decision and Ask Page

## When to use
Use this skill for the page that asks the board to decide. It is the right skill whenever the pack needs an approval, a mandate, a budget, or a go or no-go, and you want the board to leave the meeting with a clear, recorded decision rather than a vague sense of direction.

## What it does
It produces a decision page that states the question, lays out the options that were genuinely considered, names the recommended option with its rationale, and spells out exactly what approving it commits the board to. It turns "we think we should" into a motion the board can carry.

## Method
The skill runs a structured options-to-recommendation method. Boards approve choices, not ideas, so the page must show the choice.

1. State the decision question in one line, phrased as the board would vote on it. "Approve the reallocation of capital across the initiative portfolio" is votable. "Discuss our cost program" is not.

2. Establish the decision criteria up front. Name the two to four criteria the options are judged against (for example, margin impact, execution risk, time to effect, reversibility). Criteria stated after the recommendation look like rationalization; state them first.

3. Lay out the real options, including the do-nothing baseline. A decision page with one option is not a decision page. Show at least the recommended option, a credible alternative, and the status quo. Each option gets a one-line description and its read against each criterion.

4. Score the options against the criteria as prose or a glued comparison grid, never a dense table. Use a simple read such as strong, adequate, weak, or a directional arrow. Do not invent precise scores you cannot defend.

5. Name the recommendation and say why it wins on the criteria that matter most. Be explicit about the trade-off you are accepting. A recommendation with no acknowledged downside reads as naive to a board.

6. Spell out what approval commits the board to: the money, the mandate, the timeline, and what changes the day after the vote. Also state what approval does not commit them to, to head off hesitation.

7. State the consequence of not deciding. If delay has a cost (a window closing, a competitor moving, a contract lapsing), say so plainly.

8. Pre-empt the hard questions. List the two or three objections a skeptical director will raise and answer each in one line. This is the war-gaming that keeps the meeting on track.

## Inputs
- The recommendation and the governing thought from the narrative.
- The options considered and the analysis behind each.
- The decision criteria that matter to this board.
- The resource, timeline, and mandate implications of the recommended option.

## Output format
Return the page as structured prose:
- Decision question: one votable line.
- Criteria: two to four named criteria.
- Options: each with a one-line description and a read against the criteria, including the status quo.
- Recommendation: the chosen option and the explicit reason and trade-off.
- What approval commits: money, mandate, timeline, and what it does not commit.
- Cost of delay: one line.
- Anticipated questions: two or three objections with one-line answers.

## Example
Decision question: Approve reallocating capital from the three stalled cost initiatives into the two over-delivering ones, within the existing budget envelope.

Criteria: margin impact, execution risk, time to effect.

Options:
- A. Reallocate now (recommended): strong on margin impact, low execution risk because the receiving initiatives are already running, fast time to effect.
- B. Hold and give the stalled initiatives one more quarter: weak on margin impact, raises the risk of missing the recovery commitment.
- C. Status quo with no change: weakest, locks in the one-quarter slip.

Recommendation: Option A. It protects the margin commitment with the lowest execution risk, accepting the trade-off that the three stalled initiatives are wound down earlier than planned.

What approval commits: redeploying the approved capital across initiatives, with no new funding. It does not commit the board to headcount changes; those would return as a separate ask.

Cost of delay: a quarter of lost margin recovery that compounds into the next plan period.

Anticipated questions:
- "Are we giving up on the stalled initiatives too early." Two of the three missed two consecutive checkpoints; the third is folded into a working initiative.
- "Does this change the full-year guidance." No. It is designed to hold guidance, not change it.
