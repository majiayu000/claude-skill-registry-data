---
name: worked-example
description: "Write ONE worked example with a step-by-step solution. Do NOT use for practice sets or assessments."
---

# worked-example

Creates a single worked example with numbered steps, reasoning annotations, and common-error callouts. Designed for teacher modeling during direct instruction.

## Input

```json
{
  "objective": "Students will solve two-step equations.",
  "grade": "7",
  "subject": "Math",
  "difficulty": "medium"
}
```

## Output

```json
{
  "tool": "worked-example",
  "example": {
    "problem": "Solve for x: 3x + 7 = 22",
    "steps": [
      {"step": 1, "action": "Subtract 7 from both sides", "result": "3x = 15", "reasoning": "Isolate the variable term by undoing addition"},
      {"step": 2, "action": "Divide both sides by 3", "result": "x = 5", "reasoning": "Undo multiplication to find x"}
    ],
    "check": "3(5) + 7 = 15 + 7 = 22 ✓",
    "common_error": "Students may try to divide by 3 first, getting x + 7/3 = 22/3 — remind them to undo operations in reverse order (PEMDAS backward)"
  },
  "human_review_required": true
}
```

## Do NOT use this atom for
- Practice problem sets (use activity-generate)
- Assessment items (use assessment-item)
- Problems without step-by-step solutions

## Pipeline note
Follows `references/method.md` at the Generation step (worked example). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — mathematical accuracy and grade-level appropriateness must be verified.
