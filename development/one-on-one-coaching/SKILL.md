---
name: one-on-one-coaching
description: Run effective 1:1s that develop engineers, surface problems early, and build trust. Covers the GROW coaching model, SBI feedback framework, 1:1 structure (it's their meeting), question banks by scenario, career and performance conversations, and skip-level 1:1 guidance.
triggers:
  - "prepare for a 1:1"
  - "1:1"
  - "one on one"
  - "coaching conversation"
  - "feedback conversation"
  - "career conversation"
  - "performance conversation"
  - "give feedback"
  - "engineer is struggling"
  - "underperforming engineer"
  - "skip level"
audience:
  - manager
---

# One-on-One Coaching

The 1:1 is the highest-leverage management tool you have. Done well, it surfaces problems before they become crises, accelerates career growth, and builds the trust that makes everything else possible. Done poorly, it's a status update meeting that neither person needs.

**The fundamental rule**: it's their meeting, not yours. Your job is to listen, ask questions, and create conditions for the engineer to solve their own problems.

> For feedback on a specific PR or technical artifact, use the `code-review` skill.  
> For tracking team goals that surface in 1:1s, use the `okr-engineering-alignment` skill.

---

## What 1:1s Are (and Are Not)

| This ✅ | Not this ❌ |
|---|---|
| Private space for them to raise concerns | Status update (use standups/async for that) |
| Coaching toward growth and problem-solving | Manager directing what to do next |
| Feedback in both directions | Monologue of manager observations |
| Long-term relationship and trust building | A recurring calendar placeholder |
| Career development over time | Annual review as a surprise |

---

## 1:1 Cadence and Format

**Weekly 30 min** for most engineers. This is the default.  
**Bi-weekly 45–60 min** for senior ICs or engineers who are strong and self-directed.  
**Increase frequency** for: new hires (weekly 60 min for 90 days), struggling engineers, engineers in a critical moment (promo cycle, PIP, major life event).

**Structure (30-minute format)**:
1. **Check-in** (2 min): "How are you doing?" — and actually listen to the answer
2. **Their agenda** (15–20 min): What they brought; your job is to ask, not tell
3. **Your agenda** (5–8 min): Feedback, context to share, decisions they need to know
4. **Close** (2 min): Capture any commitments; confirm next week's agenda items

**Don't cancel 1:1s.** Reschedule if you must, but cancelling signals the engineer doesn't matter.

---

## Listening vs. Problem-Solving Mode

Most managers default to problem-solving mode. The engineer describes a problem; the manager offers a solution. This feels helpful but prevents growth and creates dependency.

**Switch between modes deliberately**:

| Mode | When to use | What it sounds like |
|---|---|---|
| **Active listening** | They're processing, venting, or figuring something out | "Tell me more." / "What's that like for you?" |
| **Coaching** | They need to think through a problem they can solve | GROW model questions (see below) |
| **Advising** | They've exhausted their own thinking and explicitly ask | "Here's what I'd consider..." |
| **Directing** | Urgent, safety, or they are very new | "Here's what I need you to do." |

A useful question before responding: *"Do they need me to listen, coach, advise, or direct right now?"*

---

## The GROW Coaching Model

Use GROW when an engineer is stuck on a problem they have the capability to solve themselves.

### Goal
What do they want to achieve in this conversation?  
*(Not the problem — the outcome they want from discussing it)*

- "What would be most useful to focus on today?"
- "What would a good outcome from this conversation look like?"
- "What are you hoping to figure out?"

### Reality
What is actually happening right now? (Facts, not interpretations)

- "What's the situation as it stands today?"
- "What have you already tried?"
- "What's the impact of this problem — on you, on the team, on the work?"
- "What's getting in the way?"

### Options
What could they do? (Generate possibilities before evaluating)

- "What are your options?"
- "What else could you try?"
- "If you couldn't fail, what would you do?"
- "What would you tell a colleague in the same situation?"
- "Is there anything you haven't considered?"

### Will (Way Forward)
What will they actually do? (Commitment, not just ideas)

- "Which of those options feels right?"
- "What's the first step, and when will you take it?"
- "What might get in the way — and how will you handle that?"
- "How can I support you?"

> GROW works because it respects the engineer's intelligence. They usually know what to do — they need space to reach the answer.

---

## SBI Feedback Framework

Use SBI when delivering feedback — positive or developmental.

**Situation** → **Behavior** → **Impact**

- **Situation**: Specific time and place — not "always" or "sometimes"
- **Behavior**: Observable action — not interpretation or judgment
- **Impact**: Effect on you, the team, the project — not character or intent

### SBI Feedback Template

```
"I want to share some feedback about [something recent].

In [SITUATION: specific meeting/PR/incident], I noticed [BEHAVIOR: what you
specifically observed — not interpreted]. The impact was [IMPACT: concrete
effect on you, team, or work].

[For developmental feedback]: What's your take on that? / What was going
through your mind at that point?

[Optional]: Going forward, what would help is [specific alternative behavior]."
```

### SBI Examples

**Positive feedback:**
> "In yesterday's incident (Situation), you took ownership of the communication to stakeholders without being asked and kept updates going every 30 minutes (Behavior). That let the rest of the team stay heads-down on the fix and meant stakeholders weren't escalating to me (Impact). I really appreciated it."

**Developmental feedback:**
> "In the architecture review on Tuesday (Situation), you talked over Sarah twice when she was making her point (Behavior). I could see her disengage for the rest of the meeting, and we may have lost her perspective on the design (Impact). What was happening for you in that moment?"

**Anti-patterns to avoid:**
- "You're always late to things." (No situation, no behavior, judgment)
- "I feel like you don't care about quality." (No situation, interpretation not behavior)
- "People have noticed that..." (No situation, vague, cowardly)

---

## Career Development Conversations

Hold a dedicated career conversation at least once per quarter — separate from regular 1:1 check-ins.

### Career Conversation Framework (30–60 min)

1. **Where they want to go** (not where you think they should go):
   - "Where do you see yourself in 2–3 years?"
   - "What kind of problems do you want to be solving?"
   - "What does 'success' look like for you — not just at work?"

2. **Where they are now**:
   - "What are you most proud of in the last 6 months?"
   - "Where do you feel most stretched? Most stagnant?"
   - "What skills do you feel are underdeveloped?"

3. **The gap and the path**:
   - "What would someone at [next level] be doing that you're not doing yet?"
   - Share your own observations: use SBI to give specific evidence
   - Identify 1–2 concrete growth areas to focus on this quarter

4. **Commitments**:
   - What will they work on?
   - How will you support them? (Sponsorship, stretch assignments, introductions)
   - When will you check in on progress?

---

## Question Bank by Scenario

### New to the team (first 90 days)
- "What's been the most confusing part of how we work?"
- "What's been easier or harder than you expected?"
- "What do you wish you'd known on day 1?"
- "What would help you feel more confident right now?"
- "Is there anything blocking your ability to contribute?"

### Engineer who seems disengaged or checked out
- "On a scale of 1–10, how excited are you about what you're working on right now?"
- "What would make your work more interesting?"
- "Is anything going on outside of work that's affecting things?" (offer, don't pry)
- "What was the last time you felt really energized by your work here? What was different?"
- "Is there a problem you wish someone would ask you to solve?"

### Engineer who is stuck or struggling
- "Walk me through what you've tried so far."
- "What specifically is the blocker — is it unclear requirements, technical uncertainty, or something else?"
- "Who else has faced this kind of problem — have you talked to them?"
- "What would 'good enough for now' look like?"
- "What would you do if you had to ship something by Friday?"

### Promotion-ready engineer
- "How would you describe your impact over the last 6 months to someone who doesn't know your work?"
- "What have you done that you think is above your current level?"
- "What's your read on where you stand? What do you think is still missing?"
- "Who in the organization has visibility into your work besides me?"
- "Are you comfortable advocating for yourself in a promotion conversation?"

### Underperforming engineer
- "I want to share some observations and get your perspective."
  (Then use SBI — give specific examples, ask for their take)
- "What do you think is getting in the way?"
- "What would it look like if things were going well?"
- "What do you need from me to make progress on this?"
- "I want to be direct: this is a pattern that needs to change. Let's agree on what specifically needs to be different."

### Engineer under stress or burning out
- "How are you really doing — not the work, you?"
- "What's your capacity like right now?"
- "Is there anything on your plate that could be dropped or handed off?"
- "When did you last take a proper break?"
- "What does your workload feel like — is it sustainable?"

---

## Skip-Level 1:1s

Skip-levels (meeting with reports of your reports) give you signal on team health that you can't get any other way.

**Frequency**: Every 6–8 weeks for each skip-level report.

**What to communicate upfront to the manager in between**: "I'm doing skip-levels to get team context. I won't undermine you — if someone has feedback about you, I'll encourage them to share it with you directly, and I'll tell you I heard concerns."

**Good skip-level questions:**
- "What's one thing the team is doing really well right now?"
- "What's one thing you wish were different about how the team operates?"
- "Do you feel like you know what success looks like in your role?"
- "Is there anything you want leadership to know that might not be getting through?"
- "How's [their manager] doing? Is there anything they could do differently to support the team better?"
- "What are you most proud of recently?"

**What to do with what you hear:**
- Information about team health → synthesize and act on patterns
- Direct feedback about a manager → encourage them to share it directly; tell the manager you heard concerns (but don't share specifics)
- Blockers you can remove → remove them promptly and visibly

---

## 30/60/90 Day Check-In Template

Use at day 30, day 60, and day 90 with new hires:

```markdown
## [Name] — [Day 30 / 60 / 90] Check-In

### What's going well?
[Their answer — capture it]

### What's been harder than expected?
[Their answer]

### What's still unclear?
- About the codebase / systems?
- About how decisions get made?
- About what good looks like in this role?

### Feedback for the team / manager
- What could we do better in onboarding?
- Is there anything you needed that you didn't get?

### Their confidence level (1–10)
- Technical contribution: __
- Team integration: __
- Role clarity: __

### Commitments
- They will: [specific action]
- Manager will: [specific action]
- Review at: [next check-in date]
```

---

## 1:1 Preparation Template

Fill in before each 1:1 (takes 5 minutes):

```markdown
## 1:1 Prep — [Name] — [Date]

### Their recent work
What have they shipped or worked on since last week?
What blockers or challenges might they be facing?

### My agenda items
- [ ] [Feedback to give — use SBI]
- [ ] [Context/decisions to share]
- [ ] [Career development thread to continue]

### Questions to ask
- [1–2 questions based on what I've observed or what they mentioned last week]

### From last 1:1
- They committed to: [X] — did it happen?
- I committed to: [Y] — did I follow through?

### Notes from this 1:1
[Fill during the meeting]

### Actions
- They: [commitment + deadline]
- Me: [commitment + deadline]
```

---

## Output Format

When applying this skill, the agent should:
- Ask which scenario applies (new engineer, struggling engineer, career conversation, etc.) before generating questions
- Produce a 1:1 prep template populated with scenario-specific questions
- If feedback is needed, draft it using the SBI framework with the details provided
- If it's a GROW coaching scenario, provide the full GROW question sequence
- Flag if the situation sounds like it warrants a more formal performance conversation vs. a coaching conversation

---

## References
- Camille Fournier: *The Manager's Path* — Core reference on 1:1s and engineering management
- Michael Lopp: *Managing Humans* — Practical patterns for engineering manager 1:1s
- LeadDev: [How to have better 1:1s with your engineers](https://leaddev.com/management)
- Sir John Whitmore: *Coaching for Performance* — Origin of the GROW model
- Kim Scott: *Radical Candor* — Framework for feedback that is both caring and direct
- LeadDev: [Giving feedback that lands](https://leaddev.com/management)
