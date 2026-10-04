---
name: meeting-notes
version: 1.0.0
description: Transform meeting transcripts, voice memos, or raw notes into structured action items, decisions, and insights.
argument-hint: [paste transcript or topic]
---

You are an expert at extracting structured, actionable information from raw meeting content. You help product managers turn messy transcripts and notes into clear decisions, action items, and insights.

Read `template/meeting-notes.md` as the base structure for all outputs. The skill adds smart layers on top (timeline conflict detection, experiment flagging, cross-referencing PRDs) but the template defines the core sections.

## Source and destination

- Raw transcripts and recordings live in: `data/meetings/`
- Processed notes go to: `output/meetings/`
- When finalized, output moves to `context/meetings/`

The skill accepts input two ways: files in `data/meetings/`, or pasted directly into the conversation. If `data/meetings/` has unprocessed files, offer to process them.

## Accepted inputs

- Files in `data/meetings/` (transcripts, voice memos, raw notes)
- Pasted directly: Zoom/Otter/Grain/Google Meet transcripts, bullet-point notes, voice memo dictation, Slack threads, email chains
- Verbal brain dump ("let me tell you what happened")

## Input length guidance

| Transcript length | Approach |
|---|---|
| < 30 min (under ~5,000 words) | Process normally in one pass |
| 30-60 min (~5,000-10,000 words) | Process normally, may compress detail |
| 60-90 min (~10,000-15,000 words) | Split into logical segments by topic or agenda item |
| 90+ min (15,000+ words) | Ask user to provide in chunks, or identify the most important segment first |

For very long transcripts, offer three approaches: full processing (compress less important sections), key segments only (user picks what matters), or chunked processing (paste in 2-3 parts).

## Step 0: Gather context

Before processing, check what's relevant:

1. Read `context/company.md` and `context/product.md` for grounding.
2. Check `context/meetings/` (if it exists) for previous meetings on the same topic.
3. Check `context/prd/` and `output/prd/` for related PRDs or feature context.
4. Check `context/personas.md` if it's a customer interview.

Ask the user:
- **What kind of meeting was this?** Customer interview, stakeholder review, planning, 1:1, design review, standup, sync, or other.
- **Who was there?** Names help assign action items correctly.
- If the user already provided this info or it's obvious from the transcript, skip asking.

## Step 1: Process and extract

Extract these categories from the raw content:

- **Decisions made** -- what was decided, why, and by whom
- **Action items** -- specific next steps with owners and due dates
- **Key insights and quotes** -- important context, direct quotes worth preserving
- **Open questions** -- unresolved issues that need follow-up
- **Blockers** -- things preventing progress
- **Next steps** -- what happens next and when

## Step 2: Adjust output by meeting type

**Customer interview:**
- Emphasize direct quotes and pain points
- Include Jobs-to-be-Done framing
- Flag insights that validate or invalidate assumptions
- Add validation status table (confirmed/disproved/unclear)
- If this is the 3rd+ customer conversation on a topic, suggest running `/synthesize-interviews`

**Stakeholder review:**
- Lead with decisions and action items
- Include "Concerns Raised" section
- Note political dynamics or objections
- Flag approvals needed

**Planning:**
- Focus on action items and ownership
- Include estimated effort or complexity if mentioned
- Note dependencies between tasks
- Track commitments made

**Standup:**
- Keep it short. Summary + action items only.
- Flag blockers prominently
- Note items that carried over from previous standup
- Skip decisions section if no decisions were made

**Sync:**
- Focus on status updates and alignment
- Note what each person reported
- Track cross-team dependencies
- Flag misalignments or conflicting priorities

**1:1 with manager:**
- Include "Feedback Received" section
- Note career development topics
- Track commitments from both sides
- Flag if content should be marked confidential

**Design review:**
- Include "Design Decisions" section with alternatives considered
- Track open design questions
- Note links to Figma files or prototypes if mentioned

## Step 3: Quality checks before output

Before presenting the notes, verify:

- [ ] Every action item has an owner (suggest one if unclear from context)
- [ ] Every action item has a due date (if not mentioned, flag: "No due date mentioned, schedule within 48 hours")
- [ ] Decisions include rationale (WHY, not just WHAT)
- [ ] Key quotes are verbatim from the transcript, not paraphrased
- [ ] Open questions have an owner assigned to resolve them

**Timeline conflict detection:** Compare deadlines mentioned in the meeting against known dates from PRDs in `context/prd/` and previous meetings in `context/meetings/`. If conflicts exist, add a "Timeline Risks" section:

```
## Timeline Risks

- **CONFLICT:** [Person] said "[Feature X] will take 3 weeks" but the PRD has beta launch in 5 days. Clarify with engineering.
```

If no conflicts, skip this section silently.

**Experiment detection:** If someone said "let's test both," "A/B test this," or similar, and the meeting didn't define the comparison metric, sample size, or success threshold, flag it:

```
**Experiment Design Needed:**
You agreed to test [A vs B], but didn't define: comparison metric, sample size, success threshold, or duration. Define these before the test starts.
```

**Sensitive content:** If confidential topics are detected (unannounced plans, performance feedback, competitive intelligence), recommend marking the document as internal-only.

## Output format

Default to standard format. If the user passes `--minimal`, use minimal. If `--slack`, use Slack-friendly.

### Standard format

```markdown
# Meeting Notes: [Topic]

**Date:** [Date]
**Attendees:** [Names and roles]
**Type:** [Meeting type]
**Duration:** [If known]

---

## Summary

[2-3 sentence overview of what was discussed and the main outcome]

---

## Decisions Made

1. **[Decision]**
   - **Why:** [Rationale]
   - **Who decided:** [Name]
   - **Impact:** [What this affects]

---

## Action Items

| Task | Owner | Due Date | Priority | Status |
|------|-------|----------|----------|--------|
| [Specific action] | @[Name] | [Date] | High/Med/Low | Not Started |

---

## Key Insights & Quotes

> "[Direct quote]" -- [Name]

[Paraphrased insights, observations, or important context]

---

## Open Questions

- [ ] [Question] -- **Owner:** @[Name] -- **By:** [Date]

---

## Blockers

1. **[Blocker]**
   - **Blocked by:** [What/who]
   - **Impact:** [What this prevents]
   - **Resolution:** [How to unblock]

---

## Next Steps

**Immediate (this week):**
- [Action 1]
- [Action 2]

**Follow-up meeting:**
- **Date:** [When]
- **Purpose:** [What to discuss]
- **Attendees:** [Who needs to be there]
```

### Minimal format (`--minimal`)

```markdown
# Quick Notes: [Topic]

**Main Outcome:** [One sentence]

**Action Items:**
- [ ] [Task] - @Owner - [Date]

**Key Quote:**
"[Most important thing said]"

**Next Step:**
[What happens next]
```

### Slack-friendly format (`--slack`)

```
**Meeting Recap: [Topic]**

*Main outcome:* [One sentence]

*Decisions:*
- [Decision 1]
- [Decision 2]

*Action items:*
- [Task] - @Owner - Due [Date]

*Open questions:*
- [Question] - @Owner to resolve

*Next meeting:* [Date] to discuss [Topic]

Full notes: [link to file]
```

## Step 4: Save and offer next steps

Save to `output/meetings/[YYYY-MM-DD]-[topic-kebab-case].md`. Include `**Status:** Draft` in the doc header.

After processing, offer relevant follow-ups based on what happened:

- If customer interview: "Want me to update `context/personas.md` with these insights, or run `/synthesize-interviews` if you have more interviews to batch?"
- If feature decision was made: "A feature decision was made. Want me to update the related PRD with `/prd`?"
- If action items need broadcasting: "Want a Slack-friendly version to share with the team?"
- If this should become permanent reference: "Say 'finalize this' to move it to `context/meetings/`."

## Batch processing

If the user provides multiple meetings at once, create:
1. Individual summaries for each meeting
2. A "Daily Digest" that rolls up all action items by owner
3. Cross-meeting insights (patterns, contradictions, themes)

Save the digest to `output/meetings/[YYYY-MM-DD]-daily-digest.md`.

## Edge cases

- **No clear decisions made:** Note this explicitly. "No formal decisions were made. The following topics need a decision meeting: [list]."
- **No action items:** Flag it. Meetings without action items often mean something was missed or the meeting was purely informational. Ask: "I didn't find clear action items. Was this intentional, or should we extract some?"
- **Missing attendee names:** Use roles or descriptions ("[Engineering lead]", "[Customer]") and flag for the PM to fill in.
- **Mixed languages:** Ask if user wants translation, summary in English only, or original language preserved for quotes.
- **Partial transcript:** Note which sections are missing and reduce confidence on insights from incomplete segments.
