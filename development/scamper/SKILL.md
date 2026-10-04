---
name: scamper
description: SCAMPER (Bob Eberle) — run one existing idea, product, or process through seven systematic transformations - Substitute, Combine, Adapt, Modify/Magnify, Put to other use, Eliminate, Reverse/Rearrange. Use when there is already one working idea and the need is disciplined variations of it, e.g. "give me variations", "riff on this", "scamper", "what can we substitute or combine", "remix this feature". Do NOT use for analytical work like debugging, code review, or implementation tasks, and not for blank-page ideation (needs an existing idea as input).
---

# SCAMPER

## What this technique does

Take one existing thing — a feature, a product, a workflow — and push it through seven transformation lenses in fixed order. Each lens asks a different question: what could you swap out, what could you fuse it with, what could you borrow, what could you exaggerate or shrink, what else it could do, what could you cut, what could you flip. The value is coverage: the checklist forces you past the two or three variations you would have thought of unaided and into the ones you would have skipped. It is a divergent tool for an idea that already exists, not a way to invent one from nothing.

Source: Bob Eberle, *SCAMPER: Games for Imagination Development* (1971), building on Alex Osborn's checklist of idea-spurring questions.

## Workflow

### Step 1: Confirm the target

A valid target is an *existing* idea, artifact, or process: a shipped feature, a signup flow, a pricing model, a ritual your team runs. SCAMPER transforms something that already works; it cannot operate on a blank page. If the user brings no starting idea — "help me think of a product" — refuse and point them to a generative technique (a random-stimulus or free-association method) that manufactures ideas from nothing. This one needs raw material.

If the target is unclear, ask one focused question — "What's the existing idea, and what part of it is fixed versus open to change?" — then proceed.

Refuse requests to *perform* analytical work — "debug this", "review this code", "implement this change" — and suggest an analytical approach instead. But redesigning or reinventing such a process is a valid creative target: "reinvent our code-review ritual" is in scope; "review this PR" is not.

### Step 2: Run all seven operations in order

Work the lenses in sequence — Substitute, Combine, Adapt, Modify/Magnify, Put to other use, Eliminate, Reverse/Rearrange. For each one, pull 3-4 pointed questions from [`references/question-bank.md`](references/question-bank.md) and answer only the ones that actually bite against this target. Ignore the rest; the bank is a menu, not a form.

Zero hits on an operation is normal and expected. When a lens yields nothing real, mark it empty and move on — do not manufacture a variant to fill the slot.

### Step 3: Collect the hits into concrete variants

Gather the questions that landed into named variants. Each variant states three things plainly: **what changes**, **what it costs**, and **what it risks**. A variant with no cost and no risk is usually a variant you have not thought through.

### Step 4: Meta-pattern scan

Look back across the run: which operations kept producing hits, and which came up dry? Concentrated production is a signal. If Substitute and Eliminate both kept biting, the idea is probably carrying weight it does not need or resting on a swappable assumption — that is where it is soft. Name the pattern explicitly; it is often more useful than any single variant.

### Step 5: Honest ranking with next-move offers

Rank the variants by real promise, say which ones are weak and why, and stop there. Offer next moves — go deeper on one variant, rerun a single operation harder, switch to a convergent technique to narrow, or stop — and let the user pick. Never push the user to commit.

## Honesty mechanics

Operations with no bite are shown empty, not padded. Write the emptiness plainly, for example:

> **Eliminate:** nothing left to remove — this idea is already minimal. Moving on.

A SCAMPER run where all seven operations "work" is a tell that the output is manufactured. On a real target, expect 3-5 of the seven to bite and the rest to come up empty. Showing the empty ones is what proves the run was genuine rather than retrofitted.

## What NOT to do

- **Don't answer every question in the bank.** Pick the ones with teeth against this specific target; skip the rest without comment.
- **Don't disguise the same variant under two operations.** If "let users trigger it manually" shows up under both Substitute and Reverse, it is one idea, not two. Count it once.
- **Don't SCAMPER a vague target.** Sharpen it first. Transforming a fuzzy idea produces seven fuzzy variants.
- **Don't pad empty operations.** An honestly empty lens is a result, not a gap to fill.
- **Don't push the user toward a decision.** The technique is divergent; convergence belongs to the user.

## References

- [`references/question-bank.md`](references/question-bank.md) — the seven operations with pointed questions to pull from
- [`references/worked-example.md`](references/worked-example.md) — a real run showing the full shape, empty operations included
