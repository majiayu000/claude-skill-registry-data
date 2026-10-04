---
license: Apache-2.0
name: email-composer
description: Draft professional emails for various contexts including business, technical, and customer communication. Use when the user needs help writing emails or composing professional messages.
allowed-tools: Read,Write,Edit
category: Productivity & Meta
tags:
  - email
  - composition
  - writing
  - communication
  - templates
---

# Email Composer

## Quick start

Provide context and purpose, and I'll draft an appropriate email using structured decision-making to match tone, length, and formality to your recipient and situation.

## Decision Points

### 1. Recipient Analysis → Email Structure
```
IF recipient is C-level/executive:
  └── Use bullet points, <150 words, subject = "Action Required:" + specific ask
  └── Structure: Context (1 sentence) → Ask → Timeline → Next steps

IF recipient is peer/colleague:
  └── Use conversational tone, 150-250 words, subject = descriptive + purpose
  └── Structure: Greeting → Context → Details → Clear CTA → Thank you

IF recipient is external customer:
  └── Use formal language, 200-300 words, subject = specific issue/order reference
  └── Structure: Acknowledgment → Problem statement → Solution → Follow-up

IF recipient is team/group:
  └── Use structured format, numbered lists, subject = "Update:" + topic
  └── Structure: Summary → Details with headers → Action items → Timeline
```

### 2. Email Purpose → Content Strategy
```
IF purpose = urgent request:
  └── Lead with deadline, use [URGENT] tag, bold key dates
  └── Maximum 3 sentences before the ask

IF purpose = status update:
  └── Use "What/So What/Now What" structure
  └── Include metrics, next milestones, blockers

IF purpose = problem resolution:
  └── Acknowledge → Explain → Apologize (if needed) → Fix → Prevent
  └── Lead with resolution timeline

IF purpose = information sharing:
  └── Use inverted pyramid: key info first, supporting details after
  └── Include "Why this matters" section
```

### 3. Response Timeline → Urgency Indicators
```
IF need response today:
  └── Subject: [ACTION REQUIRED] + specific task + deadline
  └── First line: "I need X by Y time because Z"

IF need response this week:
  └── Subject: Clear ask + "by [date]"
  └── Include specific deadline in closing

IF FYI/no response needed:
  └── Subject: "[FYI]" or "Update:" prefix
  └── State "No response needed" in opening
```

## Failure Modes

### 1. Buried Ask Pattern
**Symptom**: Recipient doesn't respond or asks "What do you need?"
**Root Cause**: Request hidden in paragraph 3+ or implied rather than explicit
**Fix**: 
- Put specific ask in first 2 sentences
- Use "I need..." or "Can you..." language
- Bold or bullet the request

### 2. Wrong Formality Mismatch  
**Symptom**: Response feels cold/distant or inappropriately casual
**Root Cause**: Tone doesn't match recipient relationship or company culture
**Fix**:
- C-suite = formal, direct, minimal pleasantries
- Peers = professional friendly, moderate context
- Customers = empathetic formal, comprehensive explanations

### 3. Context Overload
**Symptom**: No response, or "Can you summarize?" reply
**Root Cause**: Too much background before getting to the point
**Fix**:
- Use "Bottom Line Up Front" (BLUF) structure
- Move context to end or attachment
- Lead with the decision/ask needed

### 4. Vague Subject Death
**Symptom**: Email gets lost in inbox, delayed responses
**Root Cause**: Subject like "Question" or "Following up" gives no priority signal
**Fix**:
- Include specific action: "Review needed: Q4 budget by Friday"
- Add urgency indicator: [ACTION REQUIRED] or [FYI]
- Reference relevant project/ticket numbers

### 5. CTA Ambiguity
**Symptom**: Recipient responds with questions about what they should do
**Root Cause**: Multiple possible actions or unclear next steps
**Fix**:
- End with single, specific request
- Include deadline and method (reply email, schedule meeting, etc.)
- Use "Please confirm by replying" for acknowledgment needs

## Worked Examples

### Example: Executive Update Request
**Scenario**: Need project status for board meeting from busy VP

**Decision Process**:
- Recipient = C-level → bullet format, <150 words, direct ask
- Purpose = urgent request → lead with deadline
- Timeline = need today → [ACTION REQUIRED] subject

**Draft**:
```
Subject: [ACTION REQUIRED] Project Alpha status for board deck by 3pm

Hi Sarah,

I need Project Alpha's current status for tomorrow's board presentation.

Specifically need:
• % complete vs. timeline
• Any blockers requiring board attention  
• Budget variance (if >5%)

Please send by 3pm today so I can incorporate into the deck.

Thanks,
Alex
```

**What novice would miss**: Would write long context paragraph about board meeting importance, bury the ask in paragraph 2, use vague subject like "Board Meeting Question"

**What expert catches**: Leads with deadline, uses bullets for scannability, specifies exact information needed, gives reason for timing

## Quality Gates

- [ ] Subject line includes specific action or clear topic (not "Question" or "Update")
- [ ] Primary request appears in first 50 words of email body
- [ ] Tone matches recipient seniority (formal for executives, conversational for peers)
- [ ] Email length appropriate: <150 words for executives, <300 words for detailed requests
- [ ] Clear call-to-action with specific deadline or response expectation
- [ ] No more than 3 main points or requests per email
- [ ] Context provided without overwhelming the core message
- [ ] Professional greeting and closing appropriate for relationship
- [ ] Proofread for typos and formatting consistency
- [ ] All mentioned attachments actually attached

## Not-For Boundaries

**Don't use email-composer for**:
- Legal communications → Use [legal-writing] for compliance language
- Marketing copy → Use [copywriting] for persuasive sales content  
- Technical documentation → Use [technical-writing] for specifications
- Performance reviews → Use [feedback-delivery] for sensitive personnel topics
- Crisis communications → Use [crisis-communication] for incident response
- Contract negotiations → Use [contract-analysis] for terms and conditions

**Delegate when**:
- Message involves conflict resolution → Use [conflict-mediation]
- Requires data analysis presentation → Use [data-visualization] 
- Needs multiple stakeholder coordination → Use [project-management]