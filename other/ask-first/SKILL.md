---
name: ask-first
description: Before starting any task, list the decision points the user has not specified, ranked by how much each would change the result. Use at the start of multi-step tasks, ambiguous requests, or when the user asks "plan first" / "what choices are there" / "list the decision points".
---

# Ask First

Before you start working, surface the decisions the task leaves open — ranked by impact on the outcome. Do not silently choose what the user would care about.

## The rule

On receiving a task, before any implementation:

1. List every decision point in the task that the user has not explicitly specified.
2. Rank them: biggest change-to-result first. Impact = how differently the finished thing would look/behave if you chose differently.
3. Present the list, each with your recommended pick and a one-line trade-off.
4. Then either wait for answers on high-impact items, or proceed with recommendations and mark them as assumed — but the list comes first, always.

## Format

```markdown
Decision points (highest impact first):
1. <decision> — A) <option> (recommended, <why>) / B) <option> (<trade-off>)
2. <decision> — ...
```

Keep it tight: one line per decision. No paragraphs. If there are no open decisions, say "No decision points — fully specified" and start.

## Ranking guide

- **High:** changes architecture, file layout, user-visible behavior, or is hard to reverse.
- **Medium:** changes implementation shape but invisible to the user; easy to swap later.
- **Low:** naming, style, trivial defaults. List only if genuinely ambiguous; otherwise just log the pick (pair with decision-logging).

## Interaction with other skills

- If `decision-logging` is active: every point the user does not answer becomes a logged decision, sourced "assumed after ask-first".
- High-impact items never proceed unasked; medium/low may proceed with a logged assumption if the user says "just go".
