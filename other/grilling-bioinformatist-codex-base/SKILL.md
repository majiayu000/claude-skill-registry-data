---
name: grilling
description: Explicit-only interview loop for stress-testing a plan, decision, or idea. Use only when the user asks to grill, interrogate, interview, or stress-test their thinking before action.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask at most three independent, high-value frontier questions about material unresolved decisions in one round. Prefer a usable structured-question tool when available; otherwise ask concise numbered questions. Give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. Discover repository and environment facts before asking questions, using available tools directly. The _decisions_ are the user's: put each to them and wait.

The session is done when no material unresolved decision remains. Respect choices already settled by the user or authoritative evidence; do not exhaust speculative branches. End by reporting the shared understanding and open decisions. Do not implement automatically; implementation requires a separate user request.
