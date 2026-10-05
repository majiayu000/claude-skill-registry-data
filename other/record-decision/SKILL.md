---
name: record-decision
description: Use when a real architectural or structural decision is made — choosing between approaches, adopting or rejecting a technology, changing a contract, or any L3 task. Records the decision, the reasons, and the rejected alternatives in docs/decisions/.
---

# Record Decision

Goal: six months from now, "why did we do it this way?" has a written answer —
including what was rejected and why.

A journal entry says what was done. A decision record says what was **chosen**,
what was **not**, and why. They answer different questions.

## When to record

Record a decision when the project hit a real fork in the road:

- Two or more viable approaches existed and one was chosen.
- A technology, library, or pattern was adopted — or deliberately rejected.
- A contract, schema, or architectural boundary changed shape.
- Any L3 task (these always get a decision record).

Do NOT record routine choices that follow from existing conventions. If there
was no real alternative, there is no decision to record.

## Steps

1. **Write the record** to `docs/decisions/NNNN-<slug>.md` using
   `templates/decision.md`. `NNNN` is the next sequence number (0001, 0002...).
   Half a page maximum. It must contain:
   - **Context** — the problem that forced a choice, in two sentences.
   - **Decision** — what was chosen, stated plainly.
   - **Alternatives** — each serious option and the one-line reason it lost.
   - **Consequences** — what this makes easier, what it makes harder, what
     risk is accepted.

2. **Keep it immutable.** A decision record is a point-in-time fact. If the
   decision changes later, write a NEW record and mark the old one
   `Superseded by NNNN` — never rewrite history.

3. **Link it** from the task's journal entry, and mention it in your Done
   report: `Recorded: <journal> + docs/decisions/NNNN-<slug>.md`.

## Do not

- Do not write a record for every task — that buries the real decisions.
- Do not omit the rejected alternatives. "We chose X" without "over Y,
  because Z" is half a record.
- Do not edit an accepted record to match a new reality. Supersede it.
