---
name: follow-up
description: Stage-aware follow-up generator. Takes a contact or deal and generates the right follow-up based on deal stage, time elapsed, and conversation history. Never sends a generic "just checking in." Use when you need to follow up with someone. Triggers on "follow up", "check in", "they went dark", "nudge", "haven't heard back".
---

# Follow-Up Generator -- ACTIVATED

You are generating a follow-up that adds value and moves the conversation forward. Never generic.

---

## Process

### 1. Get Context

- Pull from CRM: deal stage, last activity, notes, history
- Calculate: days since last contact, number of touches, deal age
- If the user provides context ("they went dark", "waiting on decision"), use it

### 2. Determine Strategy

| Stage | Days Silent | Strategy |
|-------|-----------|----------|
| Just met | 0-2 | Reference conversation, suggest next step |
| Post-discovery | 1-3 | Recap value, send proof |
| Proposal sent | 3-7 | New value-add (article, insight, data) |
| Went dark | 7-14 | Permission-based, new angle |
| Ghost | 14-30 | Break-up email |
| Long nurture | 30+ | Trigger-based (news, event, new proof) |

### 3. Select Content

- Pull relevant proof matching their industry/size
- Consider likely unspoken concerns
- Find a genuine value-add (not just "checking in")

### 4. Generate Follow-Up

Produce:
- **Email** with subject line
- **LinkedIn message** variant (shorter)
- One clear CTA

### 5. Update CRM

Suggest CRM updates:
- Log follow-up attempt in notes
- Update deal stage if warranted
- Set next follow-up date

---

## Output Format

```
FOLLOW-UP: [Name] -- [Company] -- [Deal Stage]
Days since last contact: [N]
Previous touches: [N]

STRATEGY: [Stage-appropriate approach]

EMAIL:
Subject: [subject]

[email body]

LINKEDIN:
[shorter message]

CRM UPDATE: [suggested stage change / note / next follow-up date]
```

---

## Rules

- NEVER write "just checking in" or "circling back" -- every follow-up adds value
- Reference something specific from previous conversation
- If 3+ follow-ups with no response, recommend break-up or channel switch
- Include a genuine value-add: article, data point, case study, relevant news
