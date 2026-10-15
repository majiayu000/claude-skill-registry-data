---
name: parent-comm
description: "Draft ONE parent note or email for a specific purpose, placeholders only. Do NOT use for IEP communications (use special-education-support) or legal notices."
---

# parent-comm

Drafts a single parent/guardian communication. Supports email, paper note, and short text-message summary formats. The tone is warm, professional, and jargon-free. No student PII — uses placeholders ([Student Name], [Parent/Guardian]).

## Input

```json
{
  "purpose": "upcoming_unit | behavior_concern | progress_update | event_reminder | celebration | general_info",
  "grade": "4",
  "subject": "Math",
  "teacher_notes": "We are starting our fractions unit next week. Students will need 2 pencils and a ruler.",
  "tone": "warm_professional | formal | friendly_casual",
  "format": "email | paper_note | text_summary",
  "language": "English",
  "include_call_to_action": true
}
```

`purpose`: drives the template structure. `teacher_notes`: key facts/details the teacher wants included. `language`: English by default; specify Spanish, Portuguese, Haitian Creole, etc. for a translated draft.

## Output

```json
{
  "tool": "parent-comm",
  "format": "email",
  "purpose": "upcoming_unit",
  "draft": {
    "subject_line": "Exciting News: Starting Our Fractions Unit Next Week!",
    "greeting": "Dear [Parent/Guardian],",
    "body": "I hope this message finds you well! I am excited to share that [Student Name]'s class will begin our fractions unit on [Date]. This unit focuses on understanding fractions greater than one and placing them on a number line — skills we will build on all year.\n\nTo be prepared, your student will need:\n• 2 sharpened pencils\n• A ruler\n\nPlease feel free to reach out with any questions. I look forward to a great unit!",
    "closing": "Warm regards,\n[Teacher Name]\n[Grade] [Subject] Teacher\n[School Name]"
  },
  "placeholders_used": ["[Parent/Guardian]", "[Student Name]", "[Date]", "[Teacher Name]", "[Grade]", "[School Name]"],
  "note": "Replace all bracketed placeholders before sending. No real student data has been included.",
  "human_review_required": true
}
```

## Do NOT use this atom for
- IEP/504 parent notices (use special-education-support)
- Legal notices or formal disciplinary letters
- Any communication containing real student names, scores, or identifiable information
- Bulk mail-merge generation (this atom drafts one at a time)

## Pipeline note
Follows `references/method.md` at the Generation step. Output conforms to `references/metadata-schema.md`. Generation step only. Review and fill placeholders before sending. `human_review_required: true` — teacher must verify tone, content, and facts before sending to families.
