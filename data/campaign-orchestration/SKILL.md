---
name: campaign-orchestration
description: Create and execute personalized multi-channel campaigns across email, LinkedIn, and phone based on intelligence gathering triggers. Use when planning outreach sequences, optimizing engagement strategies, or executing systematic follow-up campaigns.
---

# Multi-Touch Campaign Builder

## Purpose

This skill helps you create and execute personalized multi-channel campaigns based on intelligence gathering. Different triggers (job postings, RFP signals, competitive vulnerabilities) require different campaign strategies, timing, and messaging.

## When to Use This Skill

- User has identified qualified leads from intelligence gathering
- Planning systematic outreach sequences
- Optimizing engagement strategies across channels
- Executing coordinated multi-touch campaigns

## Campaign Types by Trigger

### Type A: Job Posting Discovery Campaign

**Trigger**: Transportation manager job posting found
**Duration**: 90 days
**Total Touches**: 8-10
**Urgency Level**: Medium (long sales cycle)

#### Sequence

| Day | Channel | Action | Goal |
|-----|---------|--------|------|
| 1 | LinkedIn | Profile view (no message) | Awareness |
| 3 | LinkedIn | Connection request (no pitch) | Access |
| 7 | Email | Headcount replacement angle | Meeting |
| 14 | LinkedIn | Share industry insight | Credibility |
| 21 | Email | Market intelligence report | Value |
| 35 | Phone | Direct call attempt | Conversation |
| 45 | Email | Customer success case study | Proof |
| 60 | LinkedIn | New hire welcome message | Relationship |
| 75 | Email | Free RFP facilitation offer | Trial |
| 90 | Email | Break-up email | Last chance |

#### Day 7 Email Template

```
Subject: Hiring a Transportation Manager? Consider this first.

Hi [Name],

Noticed [Company] posted for a Transportation Manager. Before committing $140K+:

Option A: New hire (all-in): $140,000/year
Option B: CabotageTMS + managed brokerage: $25,000/year
Net difference: $115,000 Year 1

Plus with Option B:
✓ 24/7 team (not limited to business hours)
✓ 10,000+ carrier network (vs. building from scratch)
✓ Zero turnover risk
✓ Immediate start (no 90-day ramp)

Free offer: Let us facilitate your next RFP. Zero obligation.

15 minutes to discuss? [Calendar Link]
```

#### Day 60 Email Template (To New Hire)

```
Subject: Free RFP facilitation for your first 90 days

Hi [Name],

Congratulations on your new role at [Company]!

Your first 90 days will define your success. We've helped 15+ new logistics managers achieve 15% savings in their first 120 days.

We provide (no cost):
✓ Custom RFP template (saves 8-10 hours)
✓ Pre-qualified carrier network
✓ Bid analysis platform
✓ Data-driven recommendations

No obligation. No contracts. Just tools for your success.

Quick intro call? [Calendar Link]
```

---

### Type B: RFP Signal Campaign

**Trigger**: Multiple RFP indicators detected
**Duration**: 30 days (high urgency)
**Total Touches**: 6-8
**Urgency Level**: High (short decision window)

#### Sequence

| Day | Channel | Action | Goal |
|-----|---------|--------|------|
| 1 | Email | Capability statement | Awareness |
| 3 | LinkedIn | Connection + reference signal | Credibility |
| 7 | Phone | Direct approach | Meeting |
| 10 | Email | Customer success story | Proof |
| 14 | LinkedIn | Conference meeting request | Face time |
| 21 | Email | Market rates comparison | Value |
| 28 | Email | Limited time offer | Urgency |
| 30 | Phone | Final attempt | Last touch |

#### Day 1 Email Template

```
Subject: Request to participate in [Company] upcoming RFP

Hi [Name],

Based on [Specific Signal: new facility/conference attendance/hiring], anticipating [Company] may be evaluating transportation providers soon.

Quick credentials:
- MC #[NUMBER] | SmartWay Certified
- $50M+ annual revenue managed
- 97% on-time performance
- 10,000+ carrier network

Request: Add us to your approved vendor list before RFP release.

Attached: Capability statement, insurance, W-9, references

Can we schedule 15 minutes this week?
```

#### Day 21 Email Template

```
Subject: [Industry] market rates for [Their Region] - Benchmark data

Hi [Name],

Wanted to share current market intelligence for your RFP:

[Specific Lane/Region] Rates (Current):
- Dry van FTL: $[X]/mile (market average)
- Our pricing: $[Y]/mile (12% below market)
- On-time: 97% (industry avg: 92%)

If evaluating providers, worth a comparison.

Full market analysis attached. 15-minute call to discuss?
```

---

### Type C: Competitive Displacement Campaign

**Trigger**: Competitor vulnerability detected
**Duration**: 60 days (medium urgency)
**Total Touches**: 7-9
**Urgency Level**: Medium (requires nurture)

#### Sequence

| Day | Channel | Action | Goal |
|-----|---------|--------|------|
| 1 | LinkedIn | Engage with their complaint | Empathy |
| 3 | Email | Acknowledge pain point | Understanding |
| 10 | Email | Similar customer success | Hope |
| 17 | LinkedIn | Share relevant article | Value |
| 24 | Email | Free lane analysis offer | Engagement |
| 35 | Phone | Trial proposal | Commitment |
| 45 | Email | ROI calculator | Logic |
| 52 | Email | 30-day trial offer | Action |
| 60 | Email | Final incentive | Urgency |

#### Day 3 Email Template

```
Subject: Re: [Their LinkedIn Post about Service Issues]

Hi [Name],

Saw your post about delays with [Competitor]. Frustrating - especially when it impacts your customers.

We've helped 8 companies transition from [Competitor] in the past year. Common themes:
- Same service issues you mentioned
- Feeling like small account despite size
- Difficulty getting responsive service

No pitch today - happy to share what others did to solve this if helpful.

Coffee/call? 15 minutes.
```

#### Day 52 Email Template

```
Subject: 30-day trial - Your 3 worst lanes, zero risk

Hi [Name],

Simple proposal: Give us your 3 worst-performing lanes for 30 days.

No contract. If we don't beat [Competitor], no obligation.

Our average trial results vs. incumbent:
- 18% cost reduction
- 95%+ on-time (industry avg: 92%)
- 50% fewer check calls
- Real-time visibility

Worst case: 30 days of great service + market data
Best case: Permanent solution

Test on [Specific Lane They Mentioned]?
```

## Message Personalization Framework

### Level 1: Basic Personalization
**Minimum Required**:
- {{First Name}}
- {{Company Name}}
- {{Industry}}
- {{City/Region}}

**When to Use**: Initial cold outreach, low-priority leads

**Example**:
"Hi John, noticed ABC Logistics in Chicago..."

---

### Level 2: Intelligence-Based Personalization
**Data Points**:
- Specific job posting mentioned
- Conference they're attending
- Recent company news/expansion
- LinkedIn post referenced
- Competitor mentioned by name

**When to Use**: Qualified leads, triggered campaigns

**Example**:
"Hi John, saw ABC Logistics posted for a Transportation Manager last week. Also noticed you're attending CSCMP in October..."

---

### Level 3: Deep Personalization
**Data Points**:
- Exact pain point from social media
- Specific competitor failure mentioned
- Particular lane/route discussed
- Industry-specific challenge referenced
- Mutual connection mentioned

**When to Use**: High-value targets, final push efforts

**Example**:
"Hi John, read your post about late deliveries to your Phoenix facility from [Competitor]. We've helped 3 other food manufacturers solve this exact issue on the Chicago-Phoenix lane..."

## Channel Selection Rules

### Email

**Best For**:
- Detailed value propositions
- Case studies and data
- Formal proposals
- Attachments (capability statements, insurance)
- Calendar links

**Pros**:
- Permanent record
- Can include rich content
- Easy to forward internally
- Trackable (opens, clicks)

**Cons**:
- Easy to ignore
- Gets buried in inbox
- Low urgency perception

**Best Practices**:
- Subject lines <50 characters
- Body text <150 words
- Single clear CTA
- Mobile-friendly formatting

---

### LinkedIn

**Best For**:
- Initial connections
- Casual check-ins
- Content sharing
- Social proof (mutual connections)
- Warm introductions

**Pros**:
- Less formal than email
- Higher visibility (notifications)
- Profile provides context
- Easy to research sender

**Cons**:
- Message length limited
- Not suitable for formal proposals
- Can seem too casual

**Best Practices**:
- Connection requests: No pitch (acceptance rate 2x higher)
- Messages: Conversational tone
- Reference mutual connections
- Share relevant content

---

### Phone

**Best For**:
- Creating urgency
- Handling objections in real-time
- Building rapport quickly
- Trial closes
- Complex conversations

**Pros**:
- Immediate feedback
- Builds relationship faster
- Harder to ignore
- Can pivot in real-time

**Cons**:
- Time-intensive
- Easy to screen
- No written record
- Can feel intrusive

**Best Practices**:
- Reference previous email/LinkedIn message
- Have specific reason to call
- Respect time (ask for 5 minutes, not 15)
- Follow up with email summary

## A/B Testing Framework

### Subject Line Tests

**Test A**: Question format
```
"Hiring a Transportation Manager?"
```

**Test B**: Statement format
```
"Save $115K on logistics management"
```

**Test C**: Personalized observation
```
"Saw [Company's] Transportation Manager posting"
```

**Winner Criteria**: Open rate >35%

---

### Opening Line Tests

**Test A**: Direct observation
```
"I noticed [Company] posted for a Transportation Manager last week."
```

**Test B**: Value-first
```
"Companies like yours save $115K by outsourcing instead of hiring."
```

**Test C**: Social proof
```
"We've helped 12 companies in [Industry] reduce freight costs 18%."
```

**Winner Criteria**: Reply rate >8%

---

### CTA Tests

**Test A**: Question format
```
"Worth a 15-minute call?"
```

**Test B**: Direct calendar link
```
"Book 15 minutes here: [calendar link]"
```

**Test C**: Low commitment
```
"Can I send you a quick case study?"
```

**Winner Criteria**: Response rate >10%

## Tracking Metrics

### Engagement Metrics (Leading Indicators)

| Metric | Target | Good | Needs Work |
|--------|--------|------|------------|
| Email open rate | 35-40% | 25-35% | <25% |
| Email reply rate | 8-12% | 5-8% | <5% |
| LinkedIn acceptance | 40-45% | 30-40% | <30% |
| Phone connection rate | 15-20% | 10-15% | <10% |

### Progression Metrics (Conversion Funnel)

| Stage | Conversion Rate | Volume (Monthly) |
|-------|----------------|------------------|
| Lead → Meeting | 15-20% | 75 leads → 15 meetings |
| Meeting → Opportunity | 40-50% | 15 meetings → 7 opps |
| Opportunity → RFP | 60-70% | 7 opps → 5 RFPs |
| RFP → Win | 20-25% | 5 RFPs → 1 win |

**Overall Lead → Win**: ~3-4%

### Time Metrics

- First response time: <24 hours
- Meeting scheduled within: 7-10 days
- Campaign duration avg: 45-60 days
- Sales cycle length: 90-120 days

## Automation Setup

### CRM Tags (Must-Have)

Create these tags for campaign triggering:
- `job_posting_lead` → Triggers Type A Campaign
- `rfp_signal_hot` → Triggers Type B Campaign
- `competitor_vulnerable` → Triggers Type C Campaign
- `conference_attendee` → Modified Type B Campaign
- `new_hire_identified` → Day 60 message in Type A

### Automation Rules

**Rule 1**: If tag = "job_posting_lead"
- Action: Start Type A Campaign
- Wait: Send Day 1 message immediately
- Sequence: Follow 90-day schedule

**Rule 2**: If tag = "rfp_signal_hot"
- Action: Start Type B Campaign
- Priority: High (fast-track)
- Sequence: Follow 30-day schedule

**Rule 3**: If tag = "competitor_vulnerable"
- Action: Start Type C Campaign
- Priority: Medium
- Sequence: Follow 60-day schedule

### Follow-Up Rules

**No Response After 3 Touches**:
- Action: Pause campaign for 14 days
- Then: Resume with break-up email
- If still no response: Move to quarterly nurture

**Opened But No Reply**:
- Action: Increase touch frequency
- Method: Add LinkedIn touches between emails
- Goal: Stay top-of-mind without being annoying

**Any Reply Received**:
- Action: Stop automated campaign immediately
- Switch: Move to manual, personalized follow-up
- Update: Change status to "active conversation"

### Tool Recommendations

**Email Automation**:
- HubSpot (free for basics)
- Mailchimp (for sequences)
- Apollo.io ($79/month - includes email + data)

**LinkedIn Automation**:
- Phantombuster ($30/month)
- Dripify ($39/month)
- LinkedIn Sales Navigator ($135/month - manual but powerful)

**CRM**:
- HubSpot (free tier works great)
- Pipedrive ($15/month)
- Folk ($20/month)

## Integration with Other Skills

- Source leads from **Job Posting Intelligence** → Feed into Type A
- Source leads from **RFP Early Detection** → Feed into Type B
- Source leads from **Competitive Displacement** → Feed into Type C
- Coordinate timing with **Master Intelligence Orchestration**

## Pro Tips

1. **Start Automation Simple**: Manual first, automate what works
2. **Personalize Early Touches**: First 2-3 messages should be 100% custom
3. **Test Everything**: A/B test constantly, even small changes matter
4. **Track Religiously**: If you can't measure it, you can't improve it
5. **Respect Unsubscribes**: One person's "not interested" = 100% accurate signal
6. **Multi-Channel Wins**: Email + LinkedIn + Phone = 3x response vs. email alone
7. **Timing Matters**: Tuesday-Thursday, 8-10am or 3-5pm = best response times
