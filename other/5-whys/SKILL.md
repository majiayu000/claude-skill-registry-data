---
name: 5-whys
description: Root cause analysis. Keep asking why until the real cause surfaces. Use for systemic bugs and recurring issues.
user-invocable: true
---

# 5 Whys Analysis

For the problem stated by the user (or the current bug/issue), drill down through 5 layers of "why."

## Process

1. State the observable problem
2. Ask "Why?" and answer with evidence (file paths, logs, code, not guesses)
3. Repeat 4 more times, each time asking why the previous answer is true
4. The 5th answer is usually the root cause

## Rules

- Every answer MUST cite evidence: file path, line number, log output, or DB state
- If an answer is a guess, say so and verify before proceeding
- Stop early if root cause is obvious before layer 5
- Go past 5 if still not at root cause

## Output Format

```
5 WHYS - [problem]

1. WHY: [observable problem]
   BECAUSE: [answer + evidence]

2. WHY: [why is #1 true?]
   BECAUSE: [answer + evidence]

3. WHY: [why is #2 true?]
   BECAUSE: [answer + evidence]

4. WHY: [why is #3 true?]
   BECAUSE: [answer + evidence]

5. WHY: [why is #4 true?]
   BECAUSE: [answer + evidence]

ROOT CAUSE: [the real thing to fix]
FIX:        [what to change, where]
SYSTEMIC:   [is this a one-off or pattern? if pattern, what prevents recurrence?]
```
