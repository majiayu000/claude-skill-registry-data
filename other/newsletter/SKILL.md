---
name: newsletter
description: Newsletter pipeline skill — drafting, quality assurance, approval flow, scheduling. Use when creating, reviewing, or managing email newsletters.
---

Manage the full newsletter lifecycle from draft to send.

## Draft Pipeline

1. **Source** — Pull top content from the week (news, blog posts, tool updates)
2. **Curate** — Select 3-5 stories, ranked by relevance to audience
3. **Write** — TLDR format: headline → 2-sentence summary → "why it matters"
4. **Weekly Kit** — Include a recurring section (stat of the week, editor's pick, featured prompt)
5. **Quality gate** — Score the draft 0-100. Below 85? Regenerate, max 3 attempts, use best score

## Quality Scoring Criteria

- **Relevance (25%)** — stories matter to the audience right now
- **Voice (25%)** — consistent brand voice throughout
- **Actionability (20%)** — reader can do something with this information
- **Structure (15%)** — clear hierarchy, scannable, not a wall of text
- **CTA (15%)** — clear call to action that isn't forced

## QA Review

After draft, before approval:
1. Fact-check each story against its source URL
2. Check all links work
3. Review tone against brand voice guidelines
4. Verify no duplicate content from previous issues
5. Set `qa_reviewed_at` timestamp

## Approval Flow

```
Draft generated → QA reviewed → Reminders sent → Human approves → Auto-send
```

Reminder schedule (configurable):
- Reminder 1: 30 min after draft
- Reminder 2: Next morning
- Reminder 3: Afternoon
- Reminder 4: Evening

If not approved by send deadline → skip this week, don't send stale content.

## Send Rules

- Only send if `status = 'approved'`
- Update status to `sent` with timestamp after successful send
- Send confirmation to operator
- Never send the same newsletter twice
