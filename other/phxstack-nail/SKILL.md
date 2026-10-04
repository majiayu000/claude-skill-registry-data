---
name: phxstack-nail
description: Clarify or deeply resolve a task, plan, or design before planning. Use when behaviour, scope, success criteria, or dependent design decisions remain open. For commercial viability, use phxstack-roast instead.
---

# phxstack-nail

Turn an unclear request or design into confirmed implementation intent. Do not
plan or act on it.

Inspect the relevant code first. Never ask for facts the repository or tools
can answer.

Map the unresolved decisions as a **design tree**: every decision branches
into the decisions that depend on it.

Work the tree in **rounds**. The **frontier** is every decision whose
prerequisites are settled: the questions you can ask now without guessing at
answers you have not heard yet. Ask the whole frontier in one round. Number
each question and give your recommended answer.

Format each question like this:

```text
Q1 — <question title>
<question, context, and concrete choices>

RECOMMENDATION
<recommended answer and deciding reason>
```

Each answer reshapes the tree. Recompute the frontier and ask the next round.
A question that depends on an answer still open in the current round belongs
to a later round.

The interview is complete when the frontier is empty. Summarize the shared
understanding exactly as:

```text
BUILD
<one concise description>

DECISIONS
- <resolved decision needed for planning>

MAIN CONSTRAINT
<one constraint>

SUCCESS
<one observable outcome>
```

Ask the developer to confirm the summary. For a clear task with no unresolved
decisions, recommend `phxstack-plan` instead.

