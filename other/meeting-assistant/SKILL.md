---
name: meeting-assistant
description: Join meetings, take notes, extract action items, send follow-ups
version: 1.0.0
---

# Meeting Assistant

_Automated meeting documentation & follow-up_

## 🎯 Purpose

Make meetings more productive:
- Join calls (via API integration)
- Transcribe conversations
- Extract key points & decisions
- Identify action items
- Generate meeting notes
- Send follow-ups automatically

## 📊 Features

### Pre-Meeting
```
- Agenda review
- Participant research
- Background prep
- Goal setting
- Question preparation
```

### During Meeting
```
- Live transcription
- Speaker identification
- Key point extraction
- Decision logging
- Action item capture
- Sentiment analysis
```

### Post-Meeting
```
- Meeting summary
- Action items list
- Decision log
- Follow-up emails
- Calendar updates
- Task creation
```

## 🛠️ Capabilities

### Transcription
```
- Real-time speech-to-text
- Speaker diarization (who said what)
- Timestamp markers
- Keyword highlighting
- Search capability
```

### Note Taking
```
- Executive summary
- Key discussion points
- Decisions made
- Open questions
- Next steps
```

### Action Item Extraction
```
- Identify commitments
- Assign owners
- Set due dates
- Track completion
- Send reminders
```

### Follow-up Automation
```
- Thank you emails
- Meeting summary distribution
- Action item assignments
- Scheduling next meetings
- Resource sharing
```

## 💬 Response Templates

### Meeting Summary
```markdown
## 📋 Meeting Summary

**Meeting:** [Title]
**Date:** [Date & Time]
**Duration:** [X minutes]
**Attendees:** [List]

### Executive Summary
[Brief 2-3 sentence overview]

### Key Discussion Points

1. **[Topic 1]**
   - [Point A]
   - [Point B]
   - **Decision:** [What was decided]

2. **[Topic 2]**
   - [Point A]
   - [Point B]
   - **Decision:** [What was decided]

### Decisions Made
- ✅ [Decision 1]
- ✅ [Decision 2]
- ✅ [Decision 3]

### Action Items

| Task | Owner | Due Date | Status |
|------|-------|---------|--------|
| [Task 1] | [Name] | [Date] | ⏳ |
| [Task 2] | [Name] | [Date] | ⏳ |
| [Task 3] | [Name] | [Date] | ⏳ |

### Open Questions
- ❓ [Question 1] - [Owner]
- ❓ [Question 2] - [Owner]

### Next Meeting
**Proposed:** [Date/Time]
**Agenda Items:** [List]

### Recording & Notes
- 📹 Recording: [Link]
- 📝 Full Transcript: [Link]
- 📊 Slides: [Link]

---
_Sent to all attendees_
```

### Action Item Assignment
```markdown
**Action Item Assigned**

Hi [Name],

From today's meeting, you're owner of:

**Task:** [Description]
**Due:** [Date]
**Context:** [Background]

**Next Steps:**
1. [Step 1]
2. [Step 2]

Reply if you have questions!
```

### Follow-up Email
```markdown
**Subject:** Summary: [Meeting Name] - [Date]

Hi everyone,

Thanks for the great meeting today!

**Key Decisions:**
- [Decision 1]
- [Decision 2]

**Action Items:**
- [Name]: [Task] (Due: [Date])
- [Name]: [Task] (Due: [Date])

**Next Meeting:** [Date/Time]

Full notes attached. Let me know if I missed anything!

Best,
[Your name]
```

## 📋 Usage Examples

### Example 1: Join Meeting
```
User: "Join my 3pm client call and take notes"

AI:
"✅ Joined meeting: 'Client XYZ Kickoff'

**Attendees:** 5 people
**Duration:** 47 minutes

**Summary:**
- Discussed project scope
- Agreed on timeline (6 weeks)
- Budget approved: $50K

**Action Items Created:** 7
**Decisions Logged:** 4

Notes sent to all attendees. Tasks added to your todo list.
```

### Example 2: Extract Actions
```
User: "What action items from yesterday's meeting?"

AI:
"From 'Team Standup - Apr 9':

**Your Actions:**
- [ ] Review PR #234 - Due: Today
- [ ] Schedule client call - Due: Tomorrow
- [ ] Update docs - Due: Friday

**Team Actions:**
- Sarah: Deploy to staging (Done ✅)
- Mike: Fix bug #567 (In Progress)
- Lisa: Write tests (Due: Tomorrow)

**Overdue:** None 🎉
```

## 🎯 Success Metrics

✅ Accurate transcription  
✅ Action items correctly identified  
✅ Meeting notes are useful  
✅ Follow-ups sent on time  
✅ Attendees find value  
✅ Meetings more productive  

---

**Status:** Active  
**Version:** 1.0.0  
**Last Updated:** 2026-04-10
