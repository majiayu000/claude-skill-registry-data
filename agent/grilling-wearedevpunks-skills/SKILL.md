---
name: grilling
description: Grill a plan, requirement, design, or unclear decision by interviewing every currently unblocked decision in dependency-ordered rounds. Use when the user asks to grill, stress-test, interrogate, or sharpen an idea before building, or when another skill needs the shared grilling primitive.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask *now* without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Each numbered question must state one decision, the explicit question, a concise recommendation, and why it is preferred; when interpretations differ, require a precise choice. Then wait for the user's answers before the next round.

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Treat a branch as settled only when answered, parked, or explicitly deferred. Recompute the frontier. Before asking the next round, restate the locked decisions, assumptions, parked or deferred items, and the next frontier. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

Finding *facts* is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it — don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report — ask the rest of the frontier now. The *decisions* are the user's — put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
