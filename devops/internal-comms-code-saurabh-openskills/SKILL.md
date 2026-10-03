---
name: internal-comms
description: Write clear, well-structured internal communications — incident reports, post-mortems, launch announcements, team updates, all-hands summaries, 3P updates (Progress/Plans/Problems), project status updates, leadership briefings, and FAQs. Use when the user needs to communicate something to their team, engineering org, or company — especially under time pressure or when the message needs to be precise and well-received.
---

# Internal Communications

Internal comms fail in two ways: too long (nobody reads them) or too vague (nobody acts on them). The goal is a message that gets read, understood, and acted upon — by the right people, in the right amount of time.

Write for the reader's context, not your own. The reader is busy, has incomplete context, and will skim before they read. Lead with the conclusion.

---

## Internal Comms Principles

- **Lead with the bottom line.** The most important thing goes first. Background and rationale come after. Executives and busy engineers read the first paragraph and stop.
- **One message, one action.** Every communication has exactly one thing it wants the reader to do: approve, acknowledge, unblock, attend, or stay informed. Name it explicitly.
- **Shorter is always harder to write and easier to read.** Spend the extra time to cut.
- **Tone matches urgency and audience.** A P0 incident update is clinical and fast. A team launch announcement is warm and energetic. Read the room.
- **Never bury the ask.** If you need something from the reader, state it in the first 2 sentences or in a clearly labeled "Action Required" section.
- **Facts over feelings in incident reports.** What happened, what broke, what was the impact, what we did, what we're doing to prevent recurrence. No blame. No speculation.

---

## Communication Types

### 1. Incident Report / Post-Mortem

Use when: a production incident, outage, data issue, or security event occurred and needs to be documented.

**Format:**
```markdown
## Incident Report — [Service/Feature] — [Date]

**Severity:** P0 / P1 / P2
**Status:** Resolved / Ongoing / Monitoring
**Duration:** [start time] → [end time] ([X hours Y minutes])
**Impact:** [Who was affected, how many users, what they couldn't do]

---

### Timeline
| Time (UTC) | Event |
|---|---|
| HH:MM | Monitoring alert fired for [metric] |
| HH:MM | On-call engineer paged |
| HH:MM | Root cause identified: [one sentence] |
| HH:MM | Fix deployed to production |
| HH:MM | Service confirmed healthy |

### Root Cause
[One paragraph. What broke, why it broke, what conditions triggered it.]

### Impact
- **Users affected:** [number or percentage]
- **Duration of impact:** [X hours Y minutes]
- **Services affected:** [list]
- **Data loss:** [Yes/No — if yes, describe]

### What We Did
[Ordered list of actions taken during the incident]

### Action Items
| Action | Owner | Due Date | Status |
|---|---|---|---|
| [Prevent recurrence action] | @engineer | YYYY-MM-DD | Open |
| [Monitoring improvement] | @engineer | YYYY-MM-DD | Open |

### What Went Well
- [Something the team handled well]

### What Could Be Improved
- [Process or system gap revealed by this incident]
```

**Tone:** Clinical, factual, blameless. No speculation about causes that aren't confirmed. No emotion.

---

### 2. 3P Update (Progress / Plans / Problems)

Use when: weekly or sprint team updates, project status reports, engineering manager updates to leadership.

**Format:**
```markdown
## [Team/Project Name] — Week of [Date]

### 🟢 Progress (what shipped or was completed)
- [Shipped feature X to 100% of users — link]
- [Completed migration of Y service to new infrastructure]
- [Closed 12 P1 bugs from last sprint]

### 📋 Plans (what's happening next week)
- [Ship feature Z — targeting Thursday]
- [Begin load testing for the Q3 launch]
- [1:1s with all team members re: H2 goals]

### 🔴 Problems (blockers, risks, things leadership should know)
- **[BLOCKER]** Design review for feature Z still pending — need approval from @designlead by Tuesday or we slip the Thursday target
- **[RISK]** Vendor API rate limits may affect the integration launch — investigating alternative approach
- **[FYI]** Two engineers on PTO next week, capacity is reduced

**Requests:** [What you need from the reader — approval, unblocking, decision]
```

**Tone:** Direct, concise. Problems section is the most important — don't soften it. Leaders need accurate signal, not reassurance.

---

### 3. Launch Announcement

Use when: shipping a feature, releasing a product, reaching a milestone — communicating to the broader team or company.

**Format:**
```markdown
## 🚀 [Feature/Product Name] is live

**What shipped:** [One sentence — what users can now do that they couldn't before]

**Why it matters:** [One sentence on the business or user impact]

**Who it affects:** [All users / Enterprise customers / Internal teams / etc.]

---

### What's new
[2-4 bullet points. Concrete, specific, user-facing.]
- Users can now [specific action]
- [Metric improvement]: [X% faster / Y fewer steps / Z hours saved]
- [New capability]: [describe]

### How to access it
[Clear instructions — link, navigation path, or contact]

### Numbers (if available)
- [Metric 1]: [value]
- [Metric 2]: [value]

### What's next
[One sentence on the next milestone or what the team is working on now]

---

**Questions?** [Slack channel / DRI name / documentation link]
**Feedback?** [How to submit it]
```

**Tone:** Energetic but not hype-y. Lead with what users can do, not what the team built. Concrete metrics > adjectives.

---

### 4. Leadership Update / Executive Briefing

Use when: updating executives, board members, or senior leadership on a project, initiative, or situation.

**Format:**
```markdown
## [Project/Initiative] — [Date]

**Status:** On Track / At Risk / Off Track
**Owner:** [Name]
**Ask:** [One sentence — what decision or action is needed from leadership]

---

### Summary (3 sentences max)
[What we're doing, where we are, what we need.]

### Progress vs. Plan

| Milestone | Target | Status |
|---|---|---|
| [Milestone 1] | [Date] | ✅ Complete |
| [Milestone 2] | [Date] | 🟡 At Risk — [one sentence why] |
| [Milestone 3] | [Date] | ⬜ Not started |

### Key Risks

| Risk | Impact | Mitigation |
|---|---|---|
| [Risk description] | High / Medium / Low | [What we're doing about it] |

### Decision Needed
[If applicable: what decision, by when, what the options are]

### For More Detail
[Link to full project doc, dashboard, or Slack channel]
```

**Tone:** Concise, precise. No padding. Executives read this in 90 seconds or less — every word must earn its place.

---

### 5. All-Hands / Town Hall Summary

Use when: summarizing a company meeting, all-hands, or town hall for those who couldn't attend or as a written record.

**Format:**
```markdown
## [Company/Team] All-Hands — [Date]

**Attendees:** [X people] | **Recording:** [link if available]

---

### Key Announcements
1. [Most important announcement — one sentence]
2. [Second announcement]
3. [Third announcement]

### By the Numbers
- [Metric that was shared] — [value]
- [Metric] — [value]

### Q&A Highlights
**Q: [question that came up]**
A: [answer given]

**Q: [question]**
A: [answer]

### What's Next
- [Next milestone or event]
- [Deadline or decision coming up]

### Resources
- [Link to slides]
- [Link to recording]
- [Link to further reading]
```

---

### 6. FAQ / Common Questions Response

Use when: a change, launch, or situation is generating repeated questions and you need a single source of truth.

**Format:**
```markdown
## FAQ — [Topic]
*Last updated: [date] | Questions? [Slack channel or contact]*

---

**Q: [Most common question]**
A: [Direct answer. One paragraph max. Link to more detail if needed.]

---

**Q: [Second most common question]**
A: [Answer]

---

**Q: What if I have a question not covered here?**
A: [How to get help — Slack channel, DRI, form, etc.]
```

**Tone:** Clear and direct. Answer what was actually asked, not a softer version of it. If the answer is "we don't know yet," say so.

---

## Writing Checklist (Apply to Every Communication)

**Before writing:**
- [ ] What is the single most important thing this message needs to communicate?
- [ ] What action (if any) do I need from the reader?
- [ ] Who is the audience and what do they already know?

**While writing:**
- [ ] Does the first paragraph contain the most important information?
- [ ] Is the ask or action item explicitly stated?
- [ ] Is every sentence necessary?
- [ ] Are there any weasel words? ("somewhat", "might", "could consider")
- [ ] Is the tone right for the urgency and audience?

**Before sending:**
- [ ] Read it as the busiest possible recipient — does it land in 30 seconds?
- [ ] Would someone who missed all context understand what happened and what's needed?
- [ ] Is there anything that could be misread or cause alarm without context?
- [ ] Are all facts verified? No speculation presented as fact?

---

## Tone Guide by Situation

| Situation | Tone | Key words to use | Key words to avoid |
|---|---|---|---|
| P0 incident | Clinical, factual, calm | "confirmed", "identified", "resolved" | "disaster", "crazy", "somehow" |
| Launch announcement | Warm, energetic, specific | "now", "ship", "live" | "excited to announce", "proud to share" |
| Bad news / setback | Direct, honest, forward-looking | "we missed", "here's what happened", "here's the plan" | "unfortunately", "regrettably", "challenging" |
| Leadership update | Precise, concise, confident | "on track", "at risk", "decision needed" | "I feel", "hopefully", "things are going well" |
| Team recognition | Specific, genuine | Name the person, name the impact | "great job", "amazing work" (without specifics) |

---

## Definition of Done — Internal Comms

- [ ] Communication type identified — correct template applied
- [ ] Bottom line / key message stated in first 1-2 sentences
- [ ] Ask or action item explicitly named (or confirmed there is none)
- [ ] Facts verified — no speculation presented as fact
- [ ] Tone matches audience and urgency
- [ ] All weasel words removed
- [ ] Unnecessary context trimmed — reader doesn't need the full story to act
- [ ] Relevant links included for those who want more detail
- [ ] Clear contact or channel for questions
- [ ] Proofread — no typos in names, dates, or metrics
