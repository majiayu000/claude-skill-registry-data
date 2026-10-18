---
name: prioritization
description: >
  Use for prioritization, or when there are more tasks than capacity: "what should we do first?", "rank this backlog", "cut scope for the MVP", "RICE score these". Picks a method (RICE, ICE, MoSCoW, impact-effort), scores items and sets a cut line. Skip for choosing between two designs.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.10.5"
---

# Prioritization

Order a list of work by value and cost, and draw a cut line. Pick the lightest method that fits the situation; precision beyond the quality of your inputs is noise.

## When to use

- A backlog, roadmap, bug list, feature list or task list larger than capacity.
- "What first?", "what can we cut?", "MVP scope", "RICE / ICE / MoSCoW".
- A stakeholder disagreement about order that needs a transparent method.

Skip: choosing between two or three alternative designs or vendors on tradeoffs, or estimating a single number.

## Before you start

1. State in one block: **Goal** the ranking serves, **Capacity or deadline**, **Items** (count), and **Pass** (Pick method, Score, Rank, Cut line, Sanity check).
2. **Gather first.** Read the backlog, tickets, usage data, customer requests and past estimates. Never invent reach or effort numbers; mark guesses `[ESTIMATED]` and give a range. Ask up to 3 questions only for goals and capacity tools cannot answer.
3. **Light path.** Small ask: pick a method in one line, score in one table, name the top 3 and the cut line.

## Steps

### 1. Pick the method

| Situation | Method |
|-----------|--------|
| Many items, some data on users and effort | **RICE** |
| Many items, quick gut-level estimates | **ICE** |
| Fixed deadline or MVP, need to cut scope | **MoSCoW** |
| Few items, fast triage in a meeting | **Impact-effort 2x2** |
| Personal or team task triage | **Eisenhower** (urgent x important) |

State the choice and why in one line.

### 2. Score
- **RICE** = Reach x Impact x Confidence / Effort. Reach: people or events per period. Impact: 0.25 minimal, 0.5 low, 1 medium, 2 high, 3 massive. Confidence: 100%, 80% or 50%. Effort: person-months.
- **ICE** = Impact x Confidence x Ease, each 1-10.
- **MoSCoW:** Must, Should, Could, Won't (this time). Keep Musts to roughly 60% of capacity so there is room for surprises.
- **Impact-effort:** place each item in quick wins (high impact, low effort), big bets, fill-ins or avoid.

Show the table with one-line basis for each score.

### 3. Rank
Sort by score. Break ties by dependencies (what unblocks others), risk reduction, and cost of delay.

### 4. Cut line
Mark where capacity runs out. Name what is deliberately **not** done.

### 5. Sanity check
Compare the top of the list with your intuition. If they disagree, find the input that drives the difference and decide whether the score or the intuition is wrong.

## Pitfalls

- False precision: scores of 41.2 vs 39.8 are a tie.
- Everything is a Must. If Musts exceed capacity, the method has not helped yet; force a cut.
- Scoring effort in the author's own optimistic hours. Ask the people who will do the work.
- Ignoring dependencies: the highest score may need a lower item first.
- Gaming: the scorer favors a pet item. Have someone else check the top 3 inputs.
- Hiding that the ranking serves a goal. State the goal; a different goal changes the order.

Worked example: [references/example.md](references/example.md).

## Checklist

- [ ] Goal, capacity and item count stated
- [ ] Method chosen with a reason
- [ ] Every score has a basis; guesses marked `[ESTIMATED]`
- [ ] Ties broken by dependencies, risk and cost of delay
- [ ] Cut line drawn; not-doing list named
- [ ] Sanity check done
