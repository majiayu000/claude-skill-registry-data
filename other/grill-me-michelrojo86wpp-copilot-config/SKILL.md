---
name: grill-me
description: Relentless sequential interview that stress-tests a plan or design until every decision branch is resolved. Use when the user wants to "grill me", "stress-test the plan", "interrogate my design", "resolve the decision tree", or whenever a plan feels hand-wavy, under-specified, or carries hidden coupling that planning phases must surface before execution. Pairs with the discuss phase and blocks execution until alignment is reached.
---

<objective>
Interview the user one question at a time until every material branch of the decision tree is resolved and you both share one mental model of the plan. Output is not a document — it is alignment. Surface hidden assumptions, kill fuzzy language, and walk the dependencies between decisions instead of asking everything in parallel.
</objective>

<core_principle>
**ONE QUESTION AT A TIME.** Parallel questions destroy dependency order — the answer to Q2 is often contingent on the answer to Q1, and asking both at once forces the user to reason about a combinatoric space instead of a single fork. Ask, wait, absorb, ask the next.

**RECOMMEND AN ANSWER.** Every question ships with your recommendation and a one-line reason. The user confirms, overrides, or redirects — not generates from scratch.

**CODEBASE BEFORE QUESTION.** If the answer exists in the repo — a convention, an existing pattern, a prior decision — find it and cite it rather than asking.
</core_principle>

<process>

## Step 1: Map the decision tree silently

Read what the user has said plus any existing context files. Build a private list of every decision the plan depends on, in dependency order. Do not show this list.

## Step 2: Ask Question 1

Pick the root decision — the one most other decisions depend on. Format:

```
**Q1:** <precise question>.

**Recommendation:** <your pick>, because <one sentence>.

Alternatives: <A | B | C>.
```

Stop. Wait for the answer.

## Step 3: Absorb and branch

Take the answer. Cross off resolved branches. Add new ones. If the answer is ambiguous, ask ONE clarifying follow-up — not three.

## Step 4: Continue until the tree is closed

Repeat in dependency order. Stop when:
- Every open decision is resolved or explicitly deferred
- The user says to stop
- Nothing remaining would materially change the plan

## Step 5: Offer to capture decisions

Options: append to a decisions file, update context docs, or leave as conversation context. Ask which — do not auto-write.

</process>

<anti_patterns>
- Parallel questions: ask one at a time
- Yes/no railroading: offer options, not binary
- Recommendation-free questions: always include your pick
- Asking what the codebase already answers
- Grilling past useful horizon (implementation details = stop)
</anti_patterns>
