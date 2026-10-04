---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
category: engineering-method
---

<!-- Source: mattpocock/skills skills/productivity/grilling — MIT, see THIRD_PARTY_NOTICES.md -->

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## In AOS

This is the primitive. Two skills compose it, and neither duplicates it:

- **`grill-me`** — the interview alone. Use without a working directory, or when the output is a decision rather than a document.
- **`grill-with-docs`** — the interview plus `domain-modeling`, leaving a paper trail. Prefer it whenever there is a repo to leave one in.

Grilling produces a shared understanding, not a plan. Once the frontier is empty, hand off to whichever pipeline the work actually needs — `/startcycle` for a straight run, `/startcycle-graph` when the durable record and repair loop earn their overhead, `/startcycle-graph-user` for a throwaway fan-out. `/bdbrainstorm` and `/bdbmediastorm` invoke this skill as their own interview step rather than restating it.

**Do not use the `AskUserQuestion` tool for a grilling round.** A round is numbered questions with recommended answers, answered in prose, in whatever order the user likes — several at once, or one with a correction to another. Forcing that into fixed-choice widgets loses exactly the nuance the interview exists to surface.

**When the grilling ends in a written plan,** run `aos-plan-canvas modes` and offer the planning mode before opening it: standard plan-canvas (preselected) or, if detected, the pro planner. Ask every time. See "Planning mode choice" in the `plan-canvas` skill.
