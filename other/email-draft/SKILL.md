---
name: email-draft
description: "Draft ONE professional email to staff, families, or vendors. Do NOT use for parent notes about a student (use parent-comm) or mass messages."
---

# email-draft

Creates a single professional email draft with appropriate tone, structure, and content for the specified audience (staff, family, vendor, district office).

## Input

```json
{
  "purpose": "Request a meeting with a parent to discuss student progress",
  "audience": "parent",
  "tone": "warm and professional",
  "key_points": ["Student is making progress in math", "Want to discuss reading support strategies", "Flexible on meeting times"]
}
```

## Output

```json
{
  "tool": "email-draft",
  "email": {
    "subject": "Meeting Request — [Student Name]'s Progress",
    "body": "Dear [Parent/Guardian Name],\n\nI hope this message finds you well. I wanted to share that [Student Name] has been making nice progress in math this quarter!\n\nI would love to meet with you to discuss some strategies we can use together to support [his/her/their] reading development. I am flexible on times — would any day next week work for a 20-minute meeting?\n\nPlease let me know what works best for your schedule.\n\nWarm regards,\n[Teacher Name]",
    "tone": "warm and professional"
  },
  "human_review_required": true
}
```

## Do NOT use this atom for
- Mass email campaigns or newsletters
- Parent-teacher conference notes (use parent-comm)
- Emails containing real student data (placeholders only)

## Pipeline note
Follows `references/method.md` at the Generation step (email composition). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — email must be personalized and reviewed before sending.
