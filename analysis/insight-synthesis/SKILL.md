---
name: insight-synthesis
description: Turns raw findings into ranked insights by laddering each finding up the so-what chain from observation to implication to the action it demands.
---

# Insight Synthesis

## When to use
Use this when you have plenty of findings but no insight: pages of data, interview notes, and analysis that describe what is true but do not yet tell anyone what to do. It is the right skill at the point where a team has finished gathering and starts asking "so what does this all mean," or when a draft reads as a list of observations that leaves the reader to draw their own conclusions. Findings inform; insights change decisions.

## What it does
It converts findings into insights through so-what laddering: for each finding it climbs from the raw observation to what it means to the implication for the decision, until the finding earns a conclusion someone can act on. It then clusters related findings into a smaller number of governing insights, ranks them by how much they should change the decision, and states the action each one demands. The output is a short set of sharp, ranked insights, not a long list of facts.

## Method
1. Collect the findings and separate them from interpretation. Gather every discrete finding (a data point, a pattern, an interview signal) and strip it back to the raw observation. Keep facts and interpretations apart for now; conflating them early produces shallow insight. State each finding plainly.

2. Ladder each finding up the so-what chain. For every finding, ask "so what?" repeatedly and write each rung: the observation (what the data says), the interpretation (what it means), the implication (what follows for the decision or business), and the action (what we should therefore do). Keep asking "so what" until you reach something a decision-maker could act on; a finding that stops at interpretation is not yet an insight.

3. Distinguish the three levels precisely. An observation is a fact ("churn is highest in the first 30 days"). An interpretation explains it ("early churn is driven by a weak first-value experience"). An insight tells you what to do about it and why it matters ("fixing first-value onboarding is the single highest-leverage retention move, worth more than any downstream save"). Push every finding to the insight level or set it aside.

4. Test each candidate insight for the "so what" bar. A real insight is non-obvious, decision-relevant, and specific. Apply three tests: would a smart executive already assume this (if yes, it is not an insight); does it change a decision (if no, it is trivia); and is it specific enough to act on (if it is a platitude, ladder further). Discard candidates that fail.

5. Cluster related findings into governing insights. Many findings point at the same underlying truth. Group them so several observations support one governing insight, rather than presenting twenty findings. This is synthesis: the whole becomes a claim the parts could not make alone. Aim for a handful of governing insights, each backed by multiple findings.

6. Pressure-test each insight against disconfirming evidence. For each governing insight, ask what in the data contradicts it and whether it survives. An insight that ignores contrary findings is a story, not a conclusion. Note the strength of support and any caveat honestly.

7. Rank insights by decision impact. Order the governing insights by how much they should change what the organization does, not by how surprising or how well-evidenced they are alone. The top insight is the one that most alters the decision on the table. This ranking is what turns synthesis into guidance.

8. Attach the action and the owner to each insight. For every governing insight, state the specific action it demands and who would own it. An insight that names no action is an interesting fact; the action is what makes synthesis worth doing.

9. Connect the insights into a single message. Ask what all the governing insights together say. Often they ladder once more into an overarching conclusion, the one thing the whole body of work means. That top-line becomes the governing thought for any memo or deck that follows.

10. Trace every insight back to its evidence. For each governing insight, keep the line from claim to the findings that support it, so the insight is defensible when challenged. Traceability is what separates synthesis from assertion.

## Inputs
- The raw findings: data points, analysis results, interview notes, observations.
- The decision or question the synthesis serves.
- Any known contrary evidence or competing explanations.

## Output format
Return, in this order:
- The decision the synthesis serves.
- So-what ladders for the key findings: each shown as observation to interpretation to implication to action.
- Governing insights: a handful, each stated as an assertive, decision-relevant claim, with the findings that support it and any caveat.
- Ranking: the governing insights ordered by decision impact, with why the top one matters most.
- Action per insight: the specific move each demands and its owner.
- Overarching conclusion: the single thing the whole body of work means.

## Example
Decision: where to focus next year's retention effort (illustrative). Findings include: churn concentrates in the first 30 days; support tickets spike in week one; power users who reach a key milestone rarely churn; the save team recovers few of the accounts it touches.

Ladder on the first finding: observation, churn is highest in the first 30 days; interpretation, most churn is a failure to reach early value, not a late-stage decision; implication, downstream saves address the wrong stage; action, move retention investment upstream to first-value onboarding. The week-one ticket spike and the milestone finding cluster into the same governing insight.

Governing insight, ranked first: "Retention is won or lost in the first 30 days at the first-value moment, so the highest-leverage move is fixing early onboarding, not funding the downstream save team." Support: four findings converge on it; caveat: a small share of churn is genuinely late-stage and price-driven. Action: reallocate save-team budget to an onboarding-and-activation squad; owner: head of customer success. Overarching conclusion: the retention problem is an activation problem, and the whole effort should shift upstream.
