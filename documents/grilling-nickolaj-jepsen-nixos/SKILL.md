---
name: grilling
description: Interview the user relentlessly about a plan, design or decision until reaching shared understanding, asking the decision tree in rounds. Use when the user wants a plan stress-tested or asks to be grilled, or when another skill says to grill.
---

Interview the user relentlessly until you reach a shared understanding.

- Map the subject as a decision tree: every decision branches into the decisions that hang off it.
- When the skill that invoked you names the open decisions, those and what hangs off them are the tree. Decisions it calls settled are prerequisites, not questions.

## Rounds

- The frontier is every decision whose prerequisites are settled: the questions you can ask now without guessing at answers you haven't heard.
- Ask the whole frontier in one round, wait for the answers, then recompute the frontier from scratch.
- Phrase each question as your recommendation ("Store it in SQLite?") so "yes" accepts it.
- At a real fork, list the alternatives under it as lettered options, one `- **A.** <option>` line each, the recommended one as A.
- A bare "yes" accepts every recommendation in the round. A question the reply skips stays on the frontier.

Format a round like so, with `---` between questions:

```
**Q1. <question>**

<optional body: context>

- **A.** <option>
- **B.** <option>

> **Recommended:** <answer>, and the short reason.

---

**Q2. <question>**
...
```

Use the harness's question tool (pi `ask_user_question`, Claude `AskUserQuestion`) instead of markdown only when every question in the round is simple:

- at most four questions;
- each a pick from 2–4 short options;
- the recommended option first and labelled "(Recommended)".

One question that needs a considered answer makes the whole round markdown, with the simple questions as lettered options. Never split a round between the two: the dialog can hide text written before it. Without a question tool, use markdown. A dialog that times out or is dismissed is not an answer; ask again.

## Facts and decisions

- Finding facts is your job: never ask the user what the environment can answer (code, config, docs, the web).
- Look small facts up inline before sending the round.
- Give research longer than a few tool calls to a fresh subagent (not a fork) in the background with a narrow brief, and send the round without the questions that wait on it.
- If it reports while a round is open, hold its questions until the user answers; they join the next round.
- Decisions are the user's. Put each one to them and wait; never answer your own.

## Ending

- The session is done when the frontier is empty: every branch visited, nothing silently assumed.
- Ask whether you've reached a shared understanding, and don't act on any of it until the user confirms.
- The agreed plan stays in the chat; write it to a file only when the user asks for one or runs `/handoff`.
