---
name: fundraise-comms
description: >
  Email templates for investors (warm intro, cold, follow-up), monthly updates, Day 5/10/21 cadence, and style guide.
  Triggers on "investor email", "contact VC", "investor update", "intro email", "follow-up email", "monthly update",
  "투자자 이메일", "VC 연락", "투자자 업데이트", "인트로 이메일", "팔로업 이메일", "월간 업데이트".
---

# Investor Communications

Every investor interaction is an opportunity to build trust. This skill provides a communication framework that strengthens investor relationships from initial contact through regular updates.

## Connectors (Optional)

| Connector | Additional Features |
|-----------|-------------------|
| **CRM** | Investor relationship history, prior communication context |
| **Email** | Draft directly from inbox, track response rates |
| **Data Enrichment** | Latest investor activity, portfolio news |
| **Knowledge Base** | Monthly update history, metric trends |

> **No connectors?** Web research and user input alone create excellent investor communications.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                  FUNDRAISE COMMUNICATIONS                         │
├─────────────────────────────────────────────────────────────────┤
│  Core Features (works standalone)                               │
│  ✓ Investor context (thesis, portfolio, recent activity)        │
│  ✓ Scenario email templates (warm/cold/follow-up/update)        │
│  ✓ Day 5/10/21 follow-up cadence                                │
│  ✓ Monthly investor update template                             │
├─────────────────────────────────────────────────────────────────┤
│  Enhanced Mode (with tool connections)                          │
│  + ~~CRM: investor relationship history, communication log       │
│  + ~~email: draft from inbox, auto-track responses              │
│  + ~~data enrichment: auto-collect latest investor activity     │
│  + ~~knowledge base: reference past updates, metric trends      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Getting Started

```bash
"Request intro email to [Connector] to introduce us to [Investor]"
"Cold email to [VC Fund] [Partner] - [Sector] investment"
"Follow-up after meeting with [Investor] - share data room"
"Monthly investor update - [Month] performance"
```

---

## Output Format

### Investor Outreach Output

```markdown
# Investor Outreach: [Investor Name] @ [VC Fund]
**Date Generated:** [Date] | **Scenario:** [Warm intro/Cold/Follow-up] | **Stage:** [Pre-seed/Seed/Series A]

---

## Investor Context

**Target:** [Name], [Title] at [VC Fund]
**Thesis Fit:** [GREEN/YELLOW/RED] - [sector], [stage], [geography]
**Portfolio:** [Similar companies, 2-3]
**Recent Activity:** [Latest investment or news]
**Approach Path:** [Warm intro/shared portfolio/cold]

---

## Email Draft

**To:** [Email]
**Cc:** [Connector email — warm intro only]
**Subject:** [Personalized subject]

---

[Email body]

---

**Subject Alternatives:**
1. [Option 2]
2. [Option 3]

---

## Rationale for This Approach

| Element | Based On |
|---------|----------|
| Opening | [Thesis fit or shared portfolio] |
| Hook | [Market opportunity + our traction] |
| Evidence | [Key metrics or milestone] |
| CTA | [Clear ask: meeting or data room] |

---

## Follow-up Communications

**Day 5 — Soft Reminder:**
[Brief, new angle]

**Day 10 — Add Value:**
[New traction or news]

**Day 21 — Final Touch:**
[Respectful closing]
```

### Monthly Investor Update Output

```markdown
# Investor Update — [Month]
**Sent:** [Date] | **Audience:** [Existing investors / Prospects / All]

---

## TL;DR

[3-line summary]
- [Key achievement 1]
- [Core metric 2]
- [This month highlight 3]

---

## Key Metrics

| Metric | This Month | Last Month | Change | vs Target |
|--------|-----------|-----------|--------|-----------|
| [Metric 1] | [Value] | [Value] | [+X%] | [90%] |
| [Metric 2] | [Value] | [Value] | [+X%] | [105%] |
| [Metric 3] | [Value] | [Value] | [-X%] | [85%] |

**Interpretation:** [Brief explanation]

---

## This Month's Highlights

1. **[Category: Product/Customer/Team/Funding]**
   - [Specific achievement]
   - [Impact or meaning]

2. **[Category]**
   - [Achievement]
   - [Impact]

3. **[Category]**
   - [Achievement]
   - [Impact]

---

## Challenges & Learning

- **[Challenge 1]:** [Situation] → [Our response] → [Result]
- **[Challenge 2]:** [Situation] → [Our response] → [In progress]

**Transparency:** [Honest about tough situations, but clear on resolution]

---

## Asks for Help

[Concrete, actionable requests — 2-3 items]
- [ ] [Intro request: specific person/company]
- [ ] [Advice request: specific area]
- [ ] [Hiring support: specific role]

---

## Next Month Goals

- [Goal 1] by [Date]
- [Goal 2] by [Date]
- [Goal 3] by [Date]

---

## Thank You

[Genuine gratitude + next update preview]

**Next Update:** [Next month, Day X]
```

---

## Execution Flow

### Step 1: Identify Scenario

```
Analyze input pattern:
- "introduce us to [Investor]" → Warm intro (forwardable blurb)
- "cold email to [Investor]" → Cold outreach
- "follow up with [Investor]" → Follow-up (post-meeting / no response)
- "monthly update" → Monthly investor update
```

### Step 2: Investor Research (for outreach)

**Internally uses investor-research skill:**
```
1. Web search investor background
2. Thesis match (sector/stage/check size/geography)
3. Portfolio analysis (similar companies)
4. Confirm recent activity (investments, news, tweets)
5. Identify approach path (warm intro potential)
```

**Must confirm before writing:**
- Investor's investment thesis
- Similar companies in portfolio
- Recent investment activity
- Personalization hook

### Step 3: Template Selection & Personalization

```
Templates by scenario:
1. Warm intro request → Forwardable blurb for connector
2. Cold outreach → Thesis fit + traction
3. Post-meeting follow-up → Discussion recap + next steps
4. No-response follow-up → Day 5/10/21 cadence
5. Monthly update → 7-section structure
```

### Step 4: Message Composition

**Investor outreach structure (AIDA + investor context):**
```
SUBJECT: [Personalized, thesis-related, <50 characters]

[Opening: Thesis fit + hook]

[Interest: Market opportunity 1-2 sentences]

[Desire: Our traction + differentiation]

[Action: Clear CTA — meeting or data room]

[Signature]
```

**Monthly update structure:**
```
1. TL;DR (3 lines)
2. Key metrics table
3. Highlights (3-4 items)
4. Challenges & Learning
5. Asks for Help
6. Next Month Goals
7. Thank You
```

### Step 5: Email Delivery

```
When email connector available:
1. Generate draft with to, subject, body
2. Suggest optimal send time if scheduling available
3. Return draft link

When unavailable:
1. Output email text
2. Note: "Copy to your email client"
```

---

## Template Library

### 1. Warm Intro Request (Forwardable Blurb)

**Email to Connector:**
```
Subject: Quick intro to [Investor Name] at [VC Fund]?

Hi [Connector Name],

Hope you're doing well! I'm reaching out because we're raising [Amount] [Round]
for [Company], and [Investor Name] at [VC Fund] would be a perfect fit given
[Specific reason: thesis, portfolio similarity].

Would you be open to making an introduction? Happy to send over a forwardable
blurb to make it easy.

Thanks for considering!
[Signature]
```

**Forwardable Blurb:**
```
[Connector Name],

I wanted to introduce you to [Founder Name], founder of [Company].

[Company] is [one-sentence description]. They've achieved [key traction] in [timeframe] and
are currently raising [Amount] [Round].

Given [VC Fund]'s investments in [similar portfolio companies], I thought this
would be highly relevant to your thesis on [Sector].

[Founder], meet [Investor]. [Investor], meet [Founder].

I'll let you two take it from here!
```

### 2. Cold Outreach

```
Subject: [Company] - [Sector] opportunity [thesis keyword]

Hi [Investor Name],

[Personalized opening - mention their recent investment or content].

We're [Company], solving [Problem] for [Customer]. The market is [market size/opportunity],
but current solutions [limitations of existing solutions].

Early traction: [2-3 key metrics] in [timeframe]. We're backed by [existing investors]
and raising [Amount] to [specific goal].

Given [VC Fund]'s thesis on [Sector] and investments like [Portfolio Company],
would love to share more details.

Open to a 15-min intro call this week?

Best,
[Signature]
```

### 3. Post-Meeting Follow-up

```
Subject: Thanks for the meeting - [Company] follow-up

Hi [Investor Name],

Thanks for taking the time yesterday. Great to discuss [Discussion topic].

As requested, here are the materials we discussed:
- Data room: [Link]
- Financial model: [Link]
- [Other requested materials]: [Link]

Quick recap of your questions:
- [Question 1]: [Brief answer + location of detailed materials]
- [Question 2]: [Answer]

[Add any new traction or news mentioned in the meeting]

Looking forward to next steps. Happy to set up a follow-up call or connect
with other partners at [VC Fund].

Best,
[Signature]
```

### 4. No-Response Follow-up Sequence

**Day 5 — Soft Reminder:**
```
Subject: Re: [Original Subject]

Hi [Investor Name],

Following up on my email from last week. I know you're busy, but wanted
to make sure this didn't get buried.

[One sentence with new angle or update]

Still interested in exploring this together?

Best,
[Signature]
```

**Day 10 — Add Value:**
```
Subject: [Company] update: [New Traction]

Hi [Investor Name],

Quick update since my last email: [Specific new achievement or news].

This reinforces the [market opportunity or our differentiation] we discussed.

If the timing's better now, I'd love to reconnect. If not, happy to keep
you posted on future milestones.

Best,
[Signature]
```

**Day 21 — Final Touch:**
```
Subject: Last follow-up - [Company]

Hi [Investor Name],

I know you're likely swamped, so this will be my last follow-up for now.

If timing doesn't work right now, totally understand. Happy to reconnect
when [specific milestone - e.g., "we hit Series A metrics" or "we launch in Q2"].

Feel free to reach out anytime.

Best,
[Signature]
```

### 5. Monthly Investor Update (Full Template)

```
Subject: [Company] update - [Month] | [Key highlight one-liner]

Hi everyone,

Here's our [Month] update. TL;DR: [3-line summary].

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Key Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Metric | This Month | Last Month | Change | vs Target |
|--------|-----------|-----------|--------|-----------|
| [Metric 1] | X | Y | +Z% | 90% |
| [Metric 2] | X | Y | +Z% | 105% |
| [Metric 3] | X | Y | -Z% | 85% |

[Brief interpretation 2-3 sentences]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Highlights
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Product
   - [Specific achievement]
   - [Impact]

2. Customers
   - [Achievement]
   - [Impact]

3. Team
   - [Achievement]
   - [Impact]

4. Funding
   - [Current runway]
   - [Burn rate]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Challenges & Learning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [Challenge 1]: [Situation] → [Response] → [Result]
- [Challenge 2]: [Situation] → [Response] → [In progress]

[Transparent but clear on resolution]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🙏 Asks for Help
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Concrete, actionable requests]
- [ ] [Intro: specific person/company]
- [ ] [Advice: specific area]
- [ ] [Hiring: specific role]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Next Month Goals
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [Goal 1] by [Date]
- [Goal 2] by [Date]
- [Goal 3] by [Date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thanks for your continued support. Always happy to discuss any of this
in more detail.

Next update: [Next month Day X]

Best,
[Signature]
```

---

## Communication Cadence

### During Active Fundraise

```
Week 1: Initial Outreach
  Day 0: Send first email
  Day 5: First follow-up (if no response)
  Day 10: Second follow-up (if no response)

Week 3-4: Meeting Phase
  Day 0: Follow-up immediately after meeting (within 24 hours)
  Day 3: Additional materials or answer questions
  Day 7: Partner meeting or propose next steps

During Due Diligence (DD):
  - Requested materials: provide within 24-48 hours
  - Weekly: check-in on progress
  - Important news: share immediately
```

### Post-Investment

```
Monthly Updates:
  - Same date each month (e.g., first Friday of every month)
  - Maintain consistent format
  - Transparent on both wins and challenges

Quarterly Deep Dives:
  - Once per quarter: strategy review, OKR check
  - 1 week before board meeting: share materials

Ad-hoc Communications:
  - Major milestone: share immediately
  - Crisis: notify within 24 hours
  - Good news: share immediately (morale boost)
```

---

## Email Style Guide

### Investor Communication Principles

1. **Concise but specific** — Busy investors skim. Lead with highlights, detail via links.
2. **Data-driven** — Concrete numbers and metrics over subjective claims.
3. **Transparent** — Share good and difficult news honestly. Trust is built on candor.
4. **Actionable asks** — Specific requests over vague "help us out."

### Tone & Style

**Good Example:**
```
We hit $50K MRR this month (up 40% MoM). Key driver: enterprise upsells
from 3 existing customers ($15K → $30K ACV).

Challenge: Sales cycle for new logos stretched to 45 days (vs 30-day target).
Testing new demo approach with [specific action].
```

**Poor Example:**
```
Things are going great this month! We're seeing really strong growth and
customers love the product. A few challenges here and there but we're
working hard to solve them.
```

### Language to Avoid

**Phrases to skip:** "explosive growth", "game-changer", "revolutionary", "in progress", "coming soon"
**Use instead:** Concrete numbers, dates, growth rates, customer quotes, comparative metrics

### Formatting Rules

1. **No markdown in email** — No asterisks (**bold**) or headers (##) in email. Plain text only.
2. **Short paragraphs** — Max 2-3 sentences per paragraph. Whitespace aids readability.
3. **Visual separators** — Use Unicode or plain-text dividers (━━━━).
4. **Tables for metrics** — Organize metrics in simple text tables.

---

## Stage-Specific Considerations

**Pre-seed/Seed:** Vision + team focus, early traction, relationship-driven
**Series A+:** Emphasize data + metrics, unit economics, consistent format
**Korean VC:** Slightly formal tone, warm intro preference, expect quick responses

---

## What Not To Do

**Mistakes to avoid:**
- Lengthy company introduction, excessive technical detail
- Only highlight wins, make excuses or shift blame
- Pushy follow-ups ("need decision by end of week")
- Multiple CTAs at once, vague "in progress" updates

**Recommended instead:**
- One-sentence company description + 2-3 key traction points
- Balance wins and challenges + learning and response plan
- Add-value follow-ups + respectful tone

---

## Related Skills

Skills that pair well with this one:

- **investor-research** — Write customized email after investor research
- **deal-sourcing** — Cold outreach after discovering new investors
- **fundraising-process** — Communication timing across entire fundraising process
- **pitch-craft** — Use pitch deck content in email summaries
- **financial-modeling** — Extract metrics for monthly updates

---

## Examples

### Example 1: Warm Intro Request

**Input:**
"Request intro to Partner Kim Chul-soo at Seoul Investment Partners - our co-investor Lee Young-hee is the connector"

**Output:**

```markdown
# Investor Outreach: Chul-soo Kim @ Seoul Investment Partners

## Investor Context
**Target:** Chul-soo Kim, Partner at Seoul Investment Partners
**Thesis Fit:** GREEN - B2B SaaS, Seed stage, Korean market
**Portfolio:** Similar Company X, Similar Company Y
**Recent Activity:** 3 B2B SaaS investments in Q4 last year
**Approach Path:** Warm intro (co-investor Lee Young-hee)

---

## Email Draft (to Connector)

**To:** lee.younghee@earlystage.vc
**Subject:** Introduction request to Partner Kim Chul-soo

---

Young-hee, hello!

We're raising 2 billion won for our Seed round, and Partner Kim Chul-soo at Seoul Investment Partners
seems like a perfect fit. Your portfolio includes [Similar Company X] in a similar sector, and
this aligns perfectly with your B2B SaaS investment thesis.

Would an introduction be possible? I'm attaching a forwardable blurb below.

Thanks!

---

## Forwardable Blurb

Young-hee,

I'd like to introduce you to [Founder Name], CEO of [Company].

[Company] is [one-sentence description]. They've achieved [key traction] over the last 6 months and
are currently raising 2 billion won for their Seed round.

Looking at Seoul Investment Partners' investment in [Similar Portfolio Company], this is
a perfect match for your B2B SaaS thesis.

[Founder], meet Partner Kim Chul-soo.
[Founder], meet Lee Young-hee.

I think you two should take it from here!
```

### Example 2: Monthly Investor Update

**Input:**
"Create November investor update - MRR 50M won (+25%), DAU 12K (+18%), 3 new enterprise customers"

**Output:**

```
Subject: [Company] November Update | MRR 50M Won Achieved 🚀

Hi everyone,

November update. TL;DR:
- MRR 50M won achieved (+25% MoM)
- 3 new enterprise customers (total 8)
- 2 engineers joined (team now 12)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Key Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Metric | November | October | Change | vs Target |
|--------|----------|---------|--------|-----------|
| MRR | 50M | 40M | +25% | 100% ✓ |
| DAU | 12K | 10.2K | +18% | 95% |
| Enterprise Customers | 8 | 5 | +60% | 110% ✓ |
| Churn | 2.5% | 3.1% | -19% | Improving |

MRR target achieved. DAU expected to accelerate next month with new feature launch.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Highlights
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Product
   - Enterprise dashboard launch → 3 enterprise customers converted immediately
   - API performance improved 40%

2. Customers
   - [Large Company A] pilot confirmed (starts January)
   - NPS improved from 65 to 72

3. Team
   - 2 senior backend engineers joined (ex-Naver, Kakao)
   - Final interviews underway with 3 CTO candidates

4. Funding
   - Current runway: 14 months
   - Burn rate: 50M won/month (stable)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Challenges & Learning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Enterprise sales cycle longer than expected (45 days → 60 days):
  → Standardizing POC process, implementation starting next month

- Early user activation 70% → target 80% shortfall:
  → Started A/B testing onboarding flow, results expected in 2 weeks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🙏 Asks for Help
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [ ] Recommend Head of Sales candidate with enterprise sales experience
- [ ] Intro to [Large Company B] decision maker (POC pitch in progress)
- [ ] Series A prep: mentoring or mock pitch opportunity

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 December Goals
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- MRR 65M won by 12/31
- [Large Company A] pilot kickoff
- CTO hire completed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thank you for your continued support. Always happy to discuss any of this in detail.

Next update: January 5

Thanks,
[Founder Name]
```

---

## Tips

1. **Consistency builds trust** — Send monthly updates on the same date, in the same format.

2. **Transparency is not a double-edged sword** — Share challenges honestly, but always include your response plan.

3. **Data is story material** — Don't just list numbers; provide context on why they matter.

4. **Make asks specific** — "Can you help?" is less actionable than "Can you intro me to person Y at company X?"

5. **Good news immediately, bad news even faster** — Fast communication during crises maintains trust.

6. **Follow-ups add value** — "Did you see my email?" is less effective than "New traction update to share."

7. **Day 5/10/21 rhythm** — Don't follow up more than 3 times on no response. Timing may not be right.

8. **Use CRM** — When ~~CRM is connected, track all communications to maintain relationship history.

9. **Email is the tip of the iceberg** — Investor relationships are built beyond email. Events, intros, and consistent updates are key.

10. **Templates are starting points** — Adapt these templates to your style and company context.
