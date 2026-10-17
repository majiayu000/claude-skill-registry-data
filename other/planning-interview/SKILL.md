---
name: planning-interview
description: Use when a plan, design, or decision must be stress-tested with the user before any spec or code, by interviewing in rounds over a design tree until every branch is settled and the domain language is written down.
license: MIT
---

# Planning Interview

## Purpose

Reach a shared understanding of a plan before anything is specified or built. Map the plan as a **design tree**: each decision branches into the decisions that depend on it. Interview the user in **rounds**, asking every question that can be answered now, until no branch is left open or silently assumed.

## Activate when

- the user asks to be grilled, interviewed, or challenged on a plan or design
- a feature idea is too loose to specify
- `planning-spec` or `planning-wayfinder` needs decisions the conversation has not made
- a Rails change has open questions about ownership, data shape, or boundaries that the code cannot answer

## Repository inspection

Before the first round:

- read the repository's domain glossary and decision records (see `ruby-domain-modeling`), so questions use the project's terms and do not reopen recorded decisions;
- inspect the code the plan touches: models, schema, routes, and the owning skills' change contracts;
- note facts the code answers, so they are never asked of the user.

## Decision rules

1. **Facts are your job; decisions are the user's.** When a question needs a fact from the repository, documentation, or tools, look it up instead of asking. Use a sub-agent for long lookups when one is available. Put each decision to the user and wait for the answer.
2. **Ask the whole frontier each round.** The frontier is every open decision whose prerequisites are settled. Number the questions, and give your recommended answer for each.
3. **Defer dependent questions.** A question whose answer depends on another question still open this round belongs to a later round.
4. **Recompute after every round.** Settled answers unblock new branches; ask those next. A pending lookup blocks only the questions downstream of it.
5. **Keep the language sharp as you go.** When the user's term conflicts with the glossary, or is vague ("account": customer or user?), raise it in the round. Record settled terms, and offer a decision record only for hard-to-reverse, surprising trade-offs, following `ruby-domain-modeling`.

Format each round like this:

```text
Q1 — <question title>
<the question, with options when there are real alternatives>
Recommended: <your answer and the one-line reason>

Q2 — <question title>
...
```

## Completion criterion

The interview is done only when the frontier is empty: every branch of the design tree has been asked or resolved by a looked-up fact, and nothing is assumed silently. Summarize the settled decisions and ask the user to confirm the shared understanding. Do not start a spec, tickets, or code before they confirm.

## Critical invariants

- Never answer your own decision questions on the user's behalf; an interview with no user answers has not happened.
- Never ask the user for a fact the repository, its documentation, or available tools can supply.
- Never ask a question whose answer depends on another question in the same round.

## Reference example

A first round for "let customers issue partial refunds", after reading the `Refund` and `Invoice` models:

```text
Found in the code: refunds are full-invoice only today (Refund belongs_to :invoice,
amount_cents equals invoice.total_cents); tax is stored per invoice line.

Q1 — Refund granularity
Can a partial refund target specific invoice lines, or only an amount?
Recommended: specific lines. Tax is stored per line, so line-level refunds keep the tax split exact.

Q2 — Who may refund
Is this for support staff only, or for account owners too?
Recommended: support staff only in the first release; owners raise a request.

Deferred to round 2 (depend on Q1): how tax is recomputed, and what the ledger records.
```

## Agent review checklist

- [ ] glossary, decision records, and touched code read before round 1
- [ ] every question in a round was answerable now
- [ ] facts were looked up, not asked
- [ ] each question carried a recommended answer
- [ ] terms settled in the interview were recorded where the repository keeps them
- [ ] the user confirmed the summary before any spec or code

## Failure modes

- asking one question at a time when several are independent, or batching dependent ones
- asking the user what the schema or code already shows
- stopping when the conversation feels finished rather than when the frontier is empty
- drifting into implementation before the user confirms
- inventing new names for concepts the glossary already defines

## Verification

Check the final summary against the design tree: every branch has an answer or a recorded fact, and the user's confirmation is in the conversation.

## Source foundation

Adapted, in this repository's words, from the `grilling` and `grill-with-docs` skills in https://github.com/mattpocock/skills (MIT License, Copyright (c) 2026 Matt Pocock). The glossary and decision-record work is delegated to this repository's `ruby-domain-modeling`.
