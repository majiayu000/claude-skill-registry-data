---
name: grilling
description: >
  Question the user relentlessly about a plan, decision, or idea until nothing is silently assumed. Use on request only: "grill me", "stress-test this plan", "poke holes in this", "what am I missing here". Asks in rounds, each question with a recommended answer. For writing the plan itself, use the plan-change skill.
license: MIT
metadata:
  upstream: mattpocock/skills@49dd158d skills/productivity/grilling
---

# Grilling

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
**Q1 - <question title>**: <question body, might be multiple paragraphs, including multiple choices>

Recommended: <your recommended answer>

---

**Q2 - <question title>**: <question body, might be multiple paragraphs, including multiple choices>

Recommended: <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (the filesystem, a tool, the code), look it up; don't ask the user for anything you could find yourself. If your agent can delegate, hand the lookup to a subagent and don't block on it: a running lookup is an unsettled prerequisite, so only the questions downstream of it wait for the answer. Ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

Use the `plan-change` skill to turn the settled decisions into a plan, and the `break-into-issues` skill to split that plan into issues.
