---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Read [the portable runtime contract](../superdev-mode/references/portable-runtime.md) before following this workflow.

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

At the top of every round, state exactly how many currently mapped questions remain in the grill session, including the questions in that round. Recompute the count after every answer. If an answer adds or removes downstream questions, briefly explain why the count changed. When the frontier is empty, explicitly say that 0 questions remain.

For every question:

- Show all answer options as a vertical Markdown list, with one option per bullet. Never bury options in prose or put several options on one line.
- Include an `Other: <write-in answer>` option when the listed choices may not cover the user's answer.
- Name one listed option as the recommendation.
- Always give a concrete reason for the recommendation. Tie the reason to the user's goals, constraints, evidence, or a clear tradeoff. Never label an option as recommended without explaining why.

Format a round like so:

```
Questions remaining: <count, including this round>

## Q1

**<question title>**: <question body, might be multiple paragraphs, including multiple choices>

Options:

- A. <option>
- B. <option>
- C. Other: <write-in answer>

Recommendation: **B. <option>**

Reason: <why this option best fits the user's goals, constraints, evidence, or tradeoffs>

---

## Q2

**<question title>**: <question body, might be multiple paragraphs, including multiple choices>

Options:

- A. <option>
- B. <option>
- C. Other: <write-in answer>

Recommendation: **A. <option>**

Reason: <why this option best fits the user's goals, constraints, evidence, or tradeoffs>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
