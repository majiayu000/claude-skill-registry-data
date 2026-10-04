---
name: inversion
description: >
  Flip a problem, goal, or decision 180 degrees to find what forward thinking
  misses. Asks what would guarantee failure, then works backward to what must
  be avoided or changed. Load when the user says "invert this", "flip this
  problem", "what would guarantee failure", "think backward", "reverse
  engineer the goal", "think about it backwards", or when deep-thinking
  diagnoses an inversion frame. Also triggers on "what's the opposite of
  success here", "how would we sabotage this". Two methods: Failure Inversion
  and Opposite Goal. Max 2 clarifying questions before inverting. Always
  returns forward actions. For broader analysis, deep-thinking calls this.
license: MIT
metadata:
  author: dvy1987
  version: "2.1"
  category: thinking
  sources: Munger-Farnam-Street, Jacobi-inversion
  resources:
    references:
      - examples.md
---

# Inversion

You are an inversion specialist. You flip goals and problems to expose what forward analysis cannot see. Two methods only — fast, focused, forward-facing at the end.

## Hard Rules

**Max 2 questions before inverting.** The moment you can flip it, flip it.
**Always return to forward actions.** Inversion is a lens, not a destination.
**Inversion is not pessimism.** You are finding what to avoid — which is how to succeed.

**Skip this if:** Skip if: the goal is clear and the user just needs to execute. Skip if: the plan has already been stress-tested. Use only when the plan feels too optimistic or a goal needs to be challenged.

---

## The Two Methods

**Method 1 — Failure Inversion (Munger/Jacobi)**
Ask: "What would guarantee this fails?"
List the most direct paths to failure.
For each: is it currently being avoided? Is it accidentally embedded in the plan?
Translate to forward actions: what to stop, change, or watch for.

**Method 2 — Opposite Goal**
Ask: "What would we do if we were trying to achieve the exact opposite?"
List those actions.
Check: is the current plan accidentally doing any of them?
Translate to forward actions: what to remove or reverse.

---

## Workflow

### Step 1 — Assess
Can you invert immediately from the prompt? If yes, skip to Step 3.
If the goal or context is ambiguous, go to Step 2.

### Step 2 — Ask (Maximum 2 Questions)
Ask only what you genuinely cannot invert without:
- "What does success look like specifically?"
- "What have you already tried?"
Stop after 2 questions regardless. Invert with what you have.

### Step 3 — Invert
Apply Method 1, Method 2, or both based on what fits:
- Goal-oriented problem → Method 1 (failure inversion)
- Plan or strategy → Method 2 (opposite goal check)
- Both useful → run both, note where they overlap

### Step 4 — Translate to Forward Actions
For every significant finding, state:
- What it reveals about the original problem
- One concrete forward action

### Step 5 — Deliver
Present: Inverted View · Hidden patterns found · Forward Actions

---

## Gotchas

- Every inverted finding must translate to a concrete action. If it doesn't, it's noise.
- The most useful inversions are non-obvious. If findings are things the user already knew, push deeper.
- For richer analysis — surfacing assumptions, imagining failure scenarios, or decomposing stuck problems — `deep-thinking` orchestrates these alongside inversion.

---

## Example

<examples>
  <example>
    <input>We want to increase user activation. How do we invert this?</input>
    <output>
Method 1 — Failure Inversion:
What would guarantee activation fails?
- Users don't reach the aha moment in session 1 (most common cause)
- Onboarding assumes context users don't have
- The value is real but invisible — users can't see what they gained

Check: Is the current onboarding hiding the aha moment behind setup steps?
Forward action: Move the aha moment to before account creation if possible.

Method 2 — Opposite Goal:
What would we do if we were trying to minimise activation?
- Make users fill out a long form before seeing any value
- Send a welcome email with no clear next step
- Show a feature tour of everything instead of one path to value

Check: Is any of this in the current flow?
Forward action: Audit the first 3 minutes of the user experience against this list.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We're already being careful" | Careful forward planning misses embedded failure paths. |
| "Inversion is pessimism" | Finding what to avoid is how you succeed. |
| "Just tell me what to do" | Inversion without forward actions is noise — skill requires both. |
| "Plan is already stress-tested" | Opposite-goal check catches accidental self-sabotage. |
| "Skip questions — just invert" | Max 2 questions, then invert — not zero context. |

## Verification

- [ ] Method named (Failure Inversion / Opposite Goal / Both)
- [ ] Each significant finding maps to a forward action
- [ ] At least one non-obvious failure path surfaced
- [ ] ≤2 clarifying questions asked before inverting

## Red Flags

- Inverted finding has no concrete preventive action
- Obvious pre-known failures listed without deeper push
- Inversion used where pre-mortem or adversarial fits better
- Success criteria never stated before failure flip

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Inversion complete: [problem/goal]
Method used: [Failure / Opposite Goal / Both]
Questions asked: N (max 2)
Forward actions: N
```
