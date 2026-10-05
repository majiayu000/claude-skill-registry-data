---
name: interviewer
description: "Question the user relentlessly about a plan, decision, or an idea to uncover hidden assumptions, risks, and edge cases. Use when the user wants to sharpen their thinking or uses any 'interview me' trigger phrases."
---

# Interviewer

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree** where every decision branches into the decisions that hang off it.

Work the decision tree in **frontier rounds**.

The **frontier** is every decision whose prerequisites are already settled; the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round; number each question and give your recommended answer. Then wait for the user's answers before the next round.

**Every question this skill puts to the user goes through the `AskUserQuestion` tool**. Each round is up to four questions per call, and a larger frontier is consecutive calls within the same round. When presenting options, provide genuine alternatives, the recommended one should always be first and labeled "(Recommended)", its one-line reason or multi-select when the options are not mutually exclusive. An open-ended question still must go through the tool, whose built-in free-text path carries the user's own words. If a question is worth stopping for, it is worth making answerable in one click. A prose paragraph the user must answer by essay is the failure this rule ends.

**Only when the `AskUserQuestion` tool is unavailable**, fall back to formatting a round like so:

```text
❓ **Q1 - <question title>**: <the question, with real options>

➡️ <your recommended answer>

---

❓ **Q2 - <question title>**: <the question, with real options>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree. Settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

There is no cap on rounds or questions. The session is done when the frontier is empty, every branch of the design tree visited, and nothing is left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Output Format

Format the final output as a summary of the session's discussion and showing the settled decisions.
