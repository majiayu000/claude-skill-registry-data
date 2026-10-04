---
name: hypothesis-design
description: Builds an answer-first plan by stating disprovable hypotheses and, for each, the "what would prove me wrong" test and the exact analysis that settles it, so the team tests instead of boiling the ocean.
---

# Hypothesis Design

## When to use
Use this when the team is about to gather data with no point of view, at risk of analyzing everything and concluding nothing. It is the right skill when you want an answer-first approach: state the likely answer up front as a set of disprovable hypotheses, then spend effort only on the analyses that could confirm or kill them. It is the counter to boiling the ocean.

## What it does
It turns a question into a small set of sharp, disprovable hypotheses and pairs each with its decisive test. A good hypothesis is a specific claim that could be wrong, and for which you can name the evidence that would disprove it. The skill produces a prioritized hypothesis set and, for each, the single analysis that would settle it, so the workplan is lean and pointed.

## Method
The skill runs hypothesis-led problem solving, the practice of leading with a provisional answer and testing to disprove it.

1. State the provisional answer. Given the key question and what the team already knows, write the best current guess at the answer in one sentence. This is deliberately committal. An answer-first plan needs an answer to test.

2. Decompose the answer into component hypotheses. Break the provisional answer into the two to five claims that must each hold for the answer to be right. Draw these from the issue tree branches where one exists. Each becomes a hypothesis.

3. Write each hypothesis to be disprovable. A well-formed hypothesis is:
   - Specific: it names the driver, the direction, and where it applies.
   - Falsifiable: you can state a result that would make it false.
   - Consequential: if true, it changes the recommendation.
   Rewrite vague hypotheses ("marketing could improve") into sharp ones ("the binding growth constraint is activation in the mid-market segment, not top-of-funnel demand").

4. Define the disproof condition. For each hypothesis, complete the sentence "I would abandon this hypothesis if I saw ___." Naming the disproof up front is what prevents the analysis from quietly turning into a hunt for supporting evidence.

5. Name the decisive analysis. For each hypothesis, identify the single analysis or piece of evidence that most cheaply distinguishes true from false. Prefer the test that could kill the hypothesis fastest. Note the data required and roughly how hard it is to get.

6. Prioritize the hypothesis set. Rank hypotheses by two factors: how central each is to the answer, and how uncertain it currently is. Test the central, uncertain ones first. If the lead hypothesis is disproved early, revise the provisional answer and re-derive, rather than pressing on.

7. Set the branch logic. State what you will conclude and do next under each outcome (hypothesis holds, hypothesis fails). This makes the plan a decision tree, not a data-collection list.

## Inputs
- The key question (from problem definition) and any issue tree.
- What the team already believes the answer might be.
- A sense of which claims are most uncertain.

## Output format
A hypothesis plan:
- Provisional answer: the one-sentence committal guess.
- Hypothesis set: each hypothesis as a specific, falsifiable claim.
- For each hypothesis: the disproof condition ("I would abandon this if..."), the single decisive analysis, and the data it needs.
- Priority order: the hypotheses ranked by centrality and uncertainty.
- Branch logic: what happens to the recommendation under each outcome.

## Example
Key question: why is revenue growth stalling, and what recovers it fastest?

Provisional answer: growth is stalling because the largest segment is churning faster than new logos replace it, so the fastest recovery is retention, not acquisition.

Component hypotheses:
- H1: net revenue retention in the top segment has fallen below replacement. Disproof: retention is flat or rising in that segment. Decisive analysis: cohort retention by segment over eight quarters. Data: billing records by cohort.
- H2: churn is driven by a specific unmet need, not price. Disproof: churned accounts cite price as the primary reason. Decisive analysis: structured exit interviews coded by reason. Data: churned-account contacts.
- H3: acquisition is healthy, so it is not the constraint. Disproof: new-logo volume is also falling. Decisive analysis: new-logo trend by source.

Priority: H1 first (central and uncertain). Branch logic: if H1 holds, the recommendation centers on retention and H2 tells us the lever; if H1 fails, the provisional answer is wrong and the plan pivots to acquisition, re-deriving from H3.
