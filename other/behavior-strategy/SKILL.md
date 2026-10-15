---
name: behavior-strategy
description: "Suggest ONE function-based behavior support strategy (a BIP component) for a documented concern. Do NOT use for crisis intervention or restraint/seclusion guidance."
---

# behavior-strategy

Given an antecedent and hypothesized function of a behavior, suggests a replacement behavior and support strategy aligned to positive behavior support (PBS/PBIS) principles.

> **Read first — boundaries (`references/security-and-safety.md` §2).** Every strategy here is a
> **draft for the IEP/BIP or MTSS team**, never a behavior determination and never a disciplinary
> one. It must be validated against the student's **actual** BIP/IEP/504 plan and against local and
> state **discipline policy** before use. This atom does **not** decide consequences, placement,
> eligibility, or anything with legal effect, and it is **out of scope for crisis response,
> restraint, or seclusion** — escalate those to the trained team and the district's crisis protocol
> (`references/assumptions-protocol.md`). **Never request, infer, or include real student data —
> placeholders only.**

## Input

```json
{
  "behavior": "Student leaves seat frequently during independent work",
  "antecedent": "Transition to independent math practice",
  "hypothesized_function": "escape",
  "grade": "2"
}
```

## Output

```json
{
  "tool": "behavior-strategy",
  "strategy": {
    "replacement_behavior": "Student requests a 2-minute break using a break card",
    "antecedent_modification": "Pre-teach the task, chunk work into 5-minute segments with built-in movement breaks",
    "consequence_strategy": "Provide specific praise when student uses break card appropriately; reteach if student leaves seat without card",
    "data_collection": "Frequency count of seat-leaving vs. break card use; compare weekly"
  },
  "function": "escape",
  "framework": "PBIS / Positive Behavior Support",
  "human_review_required": true
}
```

## Do NOT use this atom for
- Crisis intervention or restraint/seclusion guidance
- Diagnosing behavior disorders
- Replacing a Functional Behavior Assessment (FBA)
- Using real student data

## Pipeline note
Follows `references/method.md` at the Generation step (behavior strategy). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — behavior strategies must be developed with the behavior support team and family.
