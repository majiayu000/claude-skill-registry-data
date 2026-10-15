---
name: differentiate
description: "Adapt ONE existing piece of content for one profile (ELL, IEP, 504, gifted, below/above grade). Do NOT use to create new content (use activity-generate)."
---

# differentiate

Takes one piece of instructional content (activity, passage, question, instructions) and returns a differentiated version for the specified learner profile. Keeps the learning target constant; only modifies scaffolding, vocabulary, format, and support level.

> **Read first — boundaries (`references/security-and-safety.md` §1-2).** A profile here — `IEP`,
> `504`, `ELL`, `Gifted` — is a **generic scaffolding pattern, not a student's plan**. The output is
> decision support and must be validated against the student's **actual** IEP/504/ELL plan and local
> policy before it is used with them; matching a profile name confers no accommodation and no legal
> entitlement. Where a request needs a specific student's plan details, **escalate** rather than
> assume (`references/assumptions-protocol.md`). **Never request, infer, or include real student
> data — placeholders only.**

## Input

```json
{
  "content": "Complete the number line by placing these fractions: 5/4, 3/2, 7/4.",
  "content_type": "activity_instructions | passage | question | rubric | directions",
  "profile": "ELL | IEP | gifted | below_grade | above_grade | 504",
  "grade": "4",
  "subject": "Math",
  "standard_code": "MA.4.FR.1.1",
  "notes": "Student reads at grade 2 level; native language Spanish"
}
```

`profile`: the differentiation target. `notes`: optional additional context about the learner (no real student names or IDs — use descriptors only).

## Output

```json
{
  "tool": "differentiate",
  "profile": "ELL",
  "original": "Complete the number line by placing these fractions: 5/4, 3/2, 7/4.",
  "differentiated": "Put each fraction on the number line. Use the word bank below.\n\n• 5/4 means 5 pieces of size 1/4\n• 3/2 means 3 pieces of size 1/2\n• 7/4 means 7 pieces of size 1/4\n\n[Word bank: number line, fraction, place, between]",
  "supports_added": ["simplified vocabulary", "visual word bank", "decomposed fraction meaning"],
  "supports_NOT_changed": ["learning target", "standard alignment", "required fractions"],
  "human_review_required": true,
  "note": "Verify the differentiated version still meets the standard before use. No real student data used."
}
```

## Profiles reference
- **ELL**: simplified vocabulary, sentence frames, visual supports, native-language glossary note
- **IEP**: chunked instructions, reduced items, visual schedule, extra time note, reduced reading level
- **Gifted**: extension question, independent research prompt, higher DOK, open-ended variation
- **504**: formatting adjustments, reduced visual clutter, extended time note
- **below_grade / above_grade**: Lexile and vocabulary adjustment, keeping standard alignment

## Do NOT use this atom for
- Generating new content (use activity-generate first, then differentiate)
- Writing IEP goals (use iep-goal)
- Real student PII — descriptors only (grade level, language, profile type)

## Pipeline note
Follows `references/method.md` at the Differentiation step. Output conforms to `references/metadata-schema.md`. Runs after Generation (activity-generate / assessment-item). `human_review_required: true`.
