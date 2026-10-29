---
name: apply
description: Research-backed job application workflow emphasizing relationship-building over mass applications
---

# Relationship-Focused Application Workflow

## Research Foundation

This workflow is grounded in career development research:

- **Granovetter (1973)**: 55.6% of jobs found through weak ties (acquaintances, not close friends)
- **Spence (1973)**: Signaling theory—demonstrate quality through portfolios and concrete work
- **Wanberg et al. (2020)**: Networking interventions improve reemployment quality
- **Kanar (2023)**: Informational interviews improve networking self-efficacy
- **Cialdini (1984)**: Persuasion principles—reciprocity, specificity, easy yes/no

---

## Core Philosophy

**The online application is a formality. The real work is relationship-building.**

Traditional approach: 100 applications → 2 interviews → maybe 1 offer

Relationship approach: 10 targeted companies → 5-7 conversations → 3+ interviews → multiple offers

The difference: You're not competing with 600 applicants. You're having conversations before jobs are posted.

---

## The Methodology

### Phase 1: Find People Whose Work Interests You

**NOT:** "Who is hiring for roles I want?"
**YES:** "Whose work do I find genuinely interesting?"

This is the key difference. You're not working backwards from a job posting to find someone to spam.

#### The Interactive Process

**Claude does:**
1. Research people at target companies
2. Find their actual work (papers, talks, projects, GitHub, blog posts)
3. Summarize it - spark notes style
4. Provide links for verification

**User does:**
1. Read the summary
2. Click links if curious
3. Ask honestly: **"Could I talk to this person for 20 minutes and we'd BOTH be fascinated?"**
4. If YES → proceed to draft
5. If NO → move on

**The test:** Could you email this person even if they had no job openings?

---

### Phase 2: Research Their Actual Work

Before reaching out, know:
- What specific project/paper/talk caught your attention
- One real question you have about it
- Something you can offer (insight, connection, resource)

---

### Phase 3: Craft the Outreach

**Three rules for networking emails:**
1. Make it about THEM, not you
2. Be specific (reference their actual work)
3. Make it easy to say yes or no

**Template:**
```
Hi [Name],

My name is [Your Name] and I came across your [specific work]
while [how you found it].

Your [specific thing] really stood out to me — [why it interested you].
I'd love to learn more about [specific aspect].

I know you're busy. If you have 15-20 minutes, I'd be grateful.
If not, totally understand.

Best,
[Your Name]
```

**Subject lines that work:**
- "Quick question"
- "[Mutual connection] said we should connect"
- "Question about [specific project]"
- "Your [paper/talk] on [topic]"

---

### Phase 4: The Informational Conversation

**Goal:** Learn about their work. NOT to pitch yourself.

**Questions to ask:**
1. What's your career path that led here?
2. What does a typical day look like?
3. What's most challenging about your job?
4. What challenges is your team facing right now?
5. What skills are critical for success here?
6. What resources do you recommend for someone interested in this field?
7. **3+ personalized questions based on their specific work**

**Key:** Ask about THEIR experience. Don't pitch yourself.

**After the call:** Thank-you email within 24 hours. Include something valuable if possible.

---

### Phase 5: Value Demonstration (High Priority Only)

For roles you really want, create a deliverable that proves you understand their problems.

**What it is:** A deck, analysis, or prototype showing how you'd approach their challenges.

**Structure:**
1. Identify a real problem (from research, job posting, conversation)
2. Create 5-10 slides or brief analysis
3. Propose your approach (thinking, not full solution)
4. Send: "I put together some thoughts on [problem]. No pressure."

**When to use:** Only for top targets. This is high-effort.

---

### Phase 6: Formal Application

Only after:
1. Researching the company
2. Finding people whose work interests you
3. Building some connection
4. (Optionally) demonstrating value

Now fill out the form. This is the formality, not the strategy.

---

## What NOT To Do

**Don't lead with "I applied for your job"**
- Signals: "I want something from you"
- You become one of 500 applicants asking for attention

**Don't send the same template to everyone**
- Personalization is the point
- If you can't write something specific, don't reach out yet

**Don't pitch yourself in first contact**
- First contact is about THEM
- Earn the right to talk about yourself

**Don't ask for a job**
- Ask to learn
- Jobs come up naturally when relationships exist

---

## Follow-Up Tracking

Track every outreach for appropriate follow-up timing.

| Action | Follow-Up Window | What to Do |
|--------|------------------|------------|
| Cold email sent | 5-7 days | Brief "bumping this up" |
| Informational call | 24-48 hours | Thank you + value-add |
| Application submitted | 14-21 days | Check in on status |
| Second follow-up | 7-14 days later | Final gentle check-in |
| No response after 2 | Move on | Don't spam |

### Follow-Up Templates

**After cold email (no response):**
> Hi [Name], just bumping this up. [Original ask]. No worries if timing doesn't work.

**After application (14+ days):**
> Hi [Name], I applied for [role] a couple weeks ago. Still interested in [specific thing]. Anything else I can provide?

**After informational call:**
> Thank you for the conversation. [Specific learning]. Found [resource] related to [what they mentioned].

---

## Tracking Fields

```json
{
  "company": "Company Name",
  "role": "Role Title",
  "applied_date": "2024-01-15",
  "outreach": [
    {
      "type": "cold_email",
      "recipient": "Jane Smith",
      "sent_date": "2024-01-10",
      "response_date": null,
      "next_follow_up": "2024-01-17"
    }
  ],
  "status": "applied",
  "next_action": "follow_up",
  "next_action_date": "2024-01-29"
}
```

---

## User Rules

- **Never send emails** - draft only, user sends
- **Never click submit** - fill forms, user submits
- **Don't force connections** - if genuine interest isn't there, move on
