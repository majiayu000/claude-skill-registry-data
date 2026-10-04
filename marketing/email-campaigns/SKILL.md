---
name: email-campaigns
version: 1.0.0
category: Marketing & Growth
domain: email-marketing
author: Matt Warren
license: MIT
status: production
updated: 2026-02-07
activation_triggers:
  - "email campaign"
  - "welcome sequence"
  - "email sequence"
  - "newsletter"
  - "launch email"
  - "re-engagement"
  - "drip campaign"
  - "email marketing"
  - "abandoned cart"
tools: []
---

# Email Campaigns

Welcome sequences, launch campaigns, re-engagement flows, and segmentation strategy.

## Purpose

Email is the highest-ROI marketing channel for most businesses. This skill creates structured email sequences with clear goals, not one-off blasts.

## Workflow

### Step 1: Gather Context
- Campaign type: welcome, launch, nurture, re-engagement, abandoned cart, winback
- Product/offer being promoted
- Audience segment
- Current list size and engagement
- Email platform (for formatting constraints)

### Step 2: Sequence Design
- Define the campaign goal (sale, engagement, activation)
- Map the sequence: number of emails, timing, triggers
- For each email: subject line, preview text, body, CTA
- Segment logic: who gets what and when

### Step 3: Write Emails
Each email follows:
- **Subject line:** Under 50 chars, curiosity or benefit-driven
- **Preview text:** Complements (doesn't repeat) the subject
- **Opening line:** Personal, relevant, no throat-clearing
- **Body:** One idea per email, conversational tone
- **CTA:** Single, clear action
- **P.S.:** Optional — use for urgency or secondary offer

### Step 4: Segmentation Recommendations
- New vs. returning customers
- Engaged vs. cold subscribers
- Purchase history segments
- Behavioral triggers (opened, clicked, visited)

## Output Format
```markdown
## Email Campaign: [Type] — [Product/Offer]

### Sequence Overview
| # | Email | Send Day | Goal |
|---|-------|----------|------|
| 1 | [Name] | Day 0 | [Goal] |
| 2 | [Name] | Day 2 | [Goal] |

### Email 1: [Name]
**Subject:** [subject]
**Preview:** [preview text]
**Body:**
[email content]
**CTA:** [action]
```

## Constraints
- One CTA per email — never compete with yourself
- Subject lines under 50 characters
- Emails under 200 words (exception: launch/story emails)
- Never use deceptive subject lines (fake RE:, misleading urgency)
- Include unsubscribe reference as a best practice note
