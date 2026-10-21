---
name: grilling
description: Grill a plan or decision in interview rounds using frontier questions. Use when the user wants to stress-test thinking, or uses grill / grilling trigger phrases. Not for implementing.
---

# Grilling

Interview until shared understanding. Do **not** implement during a grill.

Map the subject as a **design tree**: every decision branches into the decisions that hang off it.

## Rounds and frontier

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — questions you can ask *now* without guessing unanswered ones.

Ask the **whole frontier** in one round. Number each question. Give a recommended answer. Then **wait**.

```
❓ **Q1** - **<title>**: <body; choices if useful>

➡️ <recommended answer>
```

Settled answers push the frontier outward. A question that depends on another still open in this round belongs to a **later** round.

## Facts vs decisions

- **Facts** (repo, CURRENT, ADRs, public sources): look them up. Do not ask the user what you can read.
- **Decisions**: the user's. Put each to them and wait.
- Do not invent ARR, users, or competitors. If unknown, say `unknown`.
- No trading/Nautilus/portfolio gates — this is a personal git-comprehension product.

## Done

The frontier is empty: every material branch visited, nothing silently assumed. Do not act on the result until the user confirms shared understanding. Then offer (do not silently write) an ADR + CURRENT patch if a durable decision crystallized.
