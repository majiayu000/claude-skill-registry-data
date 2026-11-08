---
name: grilling
description: Use when the user asks to grill or stress-test a plan, decision, or idea.
---

Stress-test the material decisions within the user's requested scope. Reuse settled answers. Map unresolved choices as a **design tree**, with each decision connected to the decisions that depend on it. Do not expand the interview into adjacent work that does not affect the requested decision.

Work the tree in **rounds**. The **frontier** contains decisions whose prerequisites are already settled. Ask a manageable, prioritized subset in each round, starting with choices that gate the most important work. Number each question and give your recommended answer. Wait for the user's answers before asking dependent questions.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word yes/no questions so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Find available facts yourself rather than asking the user to look them up. Use direct inspection for cheap filesystem or tool queries. Delegate substantial, independent investigations when their benefit justifies it, using a fresh context and a bounded brief when supported. While an investigation runs, ask independent frontier questions; only dependent questions need to wait.

Material choices about intent and tradeoffs belong to the user. Recommendations are not approval. State routine assumptions without turning each into an interview question, and revisit them if they affect a material choice.

The interview is complete when the material choices needed for the requested decision are settled. If the user pauses or an essential fact cannot be obtained, leave a resumable summary of the blockers rather than declaring the decision settled. Summarize the decisions and assumptions for correction. Answering the interview does not authorize implementation or file edits; those remain separate requested work.

# Programming
Follow these for coding problems:
- Correct code 
- Performant code — think about allocations, data structures, hot paths
- Readable code — every line should earn its place. Use clear names, types, and structure. 
- Find material simplifications in data structures, state representation, control flow, algorithms, and ownership.
- Read first principles from programming skill as needed.
