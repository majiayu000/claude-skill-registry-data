---
name: first-principles
description: Structured reasoning before building. Breaks assumptions, finds the real problem, validates the approach.
user-invocable: true
---

# First Principles Analysis

Before building anything, answer these questions. Write answers inline, not in a separate doc.

## 1. What problem are we solving?

State it in one sentence. No jargon. If you can't, the problem isn't clear yet.

## 2. Who has this problem?

The chef? The client? The developer? The system? Be specific.

## 3. What assumptions are we making?

List every assumption. Challenge each one:

- Is this actually true? How do we know?
- What if the opposite were true?
- Are we solving a symptom or the root cause?

## 4. What's the simplest possible solution?

Strip away all complexity. What's the minimum that solves the stated problem? Start here.

## 5. What are we NOT doing?

Explicitly state what's out of scope. Prevents creep.

## 6. What could go wrong?

Top 3 failure modes. For each: how likely, how bad, how to detect.

## 7. Decision Framework Check

Run against the developer's 7-question framework (memory/feedback_decision_framework.md):

- Sustainable? Cost-efficient? Learning value? Profitable? Preserves autonomy? Alternatives considered? Risk acceptable?

## Output Format

```
FIRST PRINCIPLES - [topic]

PROBLEM:      [one sentence]
WHO:          [who has it]
ASSUMPTIONS:  [list, each challenged]
SIMPLEST FIX: [minimum viable approach]
OUT OF SCOPE: [what we won't do]
RISKS:        [top 3]
FRAMEWORK:    [pass/flag on each of 7 questions]
VERDICT:      [build / rethink / need more info]
```

Keep under 400 words. Dense, not verbose.
