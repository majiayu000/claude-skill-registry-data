---
name: debrief
description: Post-conversation processor. Takes meeting notes (name, company, context) and creates CRM records, drafts follow-up email, logs everything. Use after any meeting, call, coffee, or event encounter. Triggers on "met someone", "just had a call", "debrief", "meeting notes".
---

# Debrief -- ACTIVATED

You are processing a conversation the user just had. Turn it into a qualified pipeline entry with follow-up.

---

## Process

### 1. Extract Info from Input

Parse whatever is shared. Minimum: who, what company, where they met.
Ask for missing critical info (don't guess):
- Name
- Company (if not provided, research from name)
- What was discussed / their situation

### 2. Enrich

- Search your contact database for existing records
- If not found: web search for company + person

### 3. Qualify

Score ICP fit:
- **Primary ICP** -- B2B service business, $500K-$5M revenue, 5-50 employees
- **Secondary ICP** -- Adjacent fit (right size but different industry, or right industry but different size)
- **Not a fit** -- Disqualification criteria met

Recommend pipeline tier based on company size and expressed needs.

### 4. Create CRM Records

Create or update:
- **Contact:** name, email (if available), company, title, source, notes
- **Company:** name, domain, industry, size estimate
- **Deal:** stage, estimated value, source, conversation notes
- Link all three records

### 5. Draft Follow-Up

Generate:
- **Email** -- personalized to their specific pain/interest. Reference something specific they said.
- **LinkedIn connection request** -- shorter, warmer variant
- Include one clear next step

### 6. Log

Record to your logging system:
```
### [Debrief]
- Met [Name] ([Company]) at [Place]
- ICP fit: [fit level] -- [reason]
- CRM: contact + company + deal created
- Follow-up: drafted, pending review
- Next step: [what was agreed]
```

---

## Output Format

Present:

```
DEBRIEF COMPLETE

CONTACT: [Name] -- [Title] -- [Company]
ICP FIT: [level] [one-line reason]
TIER: [tier]

CRM: Contact created | Company created | Deal created ($[X]/mo est.)

FOLLOW-UP EMAIL:
Subject: [subject]

[email body]

LINKEDIN MESSAGE:
[shorter message]

NEXT STEP: [what was discussed or recommended]
```

---

## Rules

- Never send anything automatically -- always show the sender first
- If email address isn't available, flag it and draft LinkedIn-only follow-up
- If it's clearly not a fit, still create the contact (tagged "not ICP") but skip deal
- For high-value opportunities, flag prominently
- Always be specific in follow-ups -- reference what they actually said
