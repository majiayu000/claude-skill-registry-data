---
name: issue-tree-builder
description: Decomposes one big question into a MECE issue tree or hypothesis tree of testable sub-questions, with branches ranked by impact so the team analyzes what matters first.
---

# Issue Tree Builder

## When to use
Use this once the key question is set and the team needs to break it into parts it can actually work on. It is the right skill when a question is too big to answer directly, when work risks overlapping or leaving gaps, or when nobody can say which analysis to do first. The issue tree is the backbone that connects the question to the workplan.

## What it does
It builds a MECE decomposition of the key question. Mutually Exclusive means branches do not overlap; Collectively Exhaustive means together they cover the whole question with no gap. The skill produces either an issue tree (neutral sub-questions) or a hypothesis tree (each branch stated as a claim to be proved or disproved), then ranks branches by impact so effort flows to the parts that most move the answer.

## Method
The skill applies MECE decomposition with a deliberate choice of logic at each level.

1. Place the key question at the root. Use the single decision-shaped question from problem definition. If there is no clean key question, stop and define one first; a tree built on a fuzzy root will be fuzzy everywhere.

2. Choose the decomposition logic for level one. Pick the structure that best fits the question:
   - Formula or algebraic break (for example, profit = volume times price minus cost) when the question is quantitative.
   - Conceptual or component break (for example, demand-side vs supply-side) when drivers are qualitative.
   - Process or stage break (for example, awareness, purchase, retention) when the question follows a flow.
   - Segment break (by customer, geography, product) when heterogeneity is the issue.
   Name the logic explicitly so the branches are obviously exhaustive.

3. Draft level-one branches and test for MECE. Check two things: no branch overlaps another (mutually exclusive), and the branches together cover the root with nothing missing (collectively exhaustive). Add a "structural / other" branch only if it is truly needed, and if it is large, it means the logic is wrong.

4. Decompose each branch one or two levels deeper, using the same discipline at each node. Stop decomposing a branch when the leaf is a question a single analysis could answer. That leaf is a unit of work.

5. Convert to a hypothesis tree where useful. For each branch, if the team already holds a view, restate the neutral sub-question as a disprovable claim (for example, "retention, not acquisition, is the binding constraint"). Hypothesis trees are faster because they tell you what evidence would settle each branch.

6. Rank branches by impact. Score each level-one branch on how much the overall answer would move if that branch resolved one way versus another, and on how uncertain it currently is. The high-impact, high-uncertainty branches are where analysis pays off. Mark the top branches as the critical path.

7. Prune. Cut or park low-impact, low-uncertainty branches. A good tree is not the most complete tree; it is the one that concentrates work on what changes the decision.

## Inputs
- The key question (from problem definition).
- Any early views or hypotheses the team already holds.
- Rough sense of where uncertainty is highest, if known.

## Output format
An indented tree, rendered as nested prose or an outline:
- Root: the key question.
- Level one: the branches, with the decomposition logic named and a MECE check noted.
- Level two and below: sub-questions or hypotheses down to analyzable leaves.
- Impact ranking: the branches ordered, with the critical-path branches marked.
- Parked branches: what was pruned and why.

## Example
Key question: "How do we return the business to double-digit profit growth within two years?"

Level-one logic chosen: algebraic, profit = revenue minus cost, then revenue = volume times price.

Branches (MECE check: revenue and cost together are exhaustive; volume and price do not overlap):
- Revenue
  - Volume: are we losing customers, or failing to add them? (split by segment)
  - Price and mix: is realized price falling, and is the mix shifting to lower-value products?
- Cost
  - Cost to serve: is unit cost rising faster than price?
  - Overhead: is fixed cost growing ahead of revenue?

Hypothesis restatement of the top branch: "The binding constraint is volume in the mid-market segment, not price." That branch is marked critical path because it is both high-impact and highly uncertain, so it is analyzed first. The overhead branch is parked as low-uncertainty for now.
