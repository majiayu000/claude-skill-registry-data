---
name: market-launch
description: Product/service launch playbook generator producing week-by-week tactical plans with templates and metrics tracking.
---

# Product/Service Launch Playbook Generator

## Skill Purpose

Generate a complete, week-by-week launch playbook for any product, service, or feature launch. This skill produces a tactical plan with templates, checklists, email sequences, social posts, and metrics tracking — everything needed to execute a successful launch.

## When to Use

- User is planning to launch a new product, service, feature, or offering.
- User asks for a launch plan, go-to-market strategy, or launch checklist.
- User wants to coordinate a multi-channel launch campaign.
- Triggered by `/market launch` or `/market launch <product description>`.

## Reference map

| When | Read |
|---|---|
| Generating the week-by-week task list (Step 3) | [`references/timeline.md`](references/timeline.md) |
| Writing the email sequences (Step 4) | [`references/email-templates.md`](references/email-templates.md) |
| Writing the social-media posts (Step 5) | [`references/social-templates.md`](references/social-templates.md) |
| Press outreach + partner coordination (Steps 6 & 7) | [`references/outreach.md`](references/outreach.md) |
| Full KPI benchmarks + the common-mistakes catalog (Steps 8 & 9) | [`references/metrics-and-antipatterns.md`](references/metrics-and-antipatterns.md) |

## How to Execute

### Step 1: Gather launch context

Collect these inputs from the user (ask if not provided):

1. **What are you launching?** (product, service, feature, course, event)
2. **Who is the target audience?** (demographics, pain points, existing list size)
3. **What is the primary launch goal?** (revenue target, signups, downloads, awareness)
4. **What is the launch date?** (or desired timeline)
5. **What channels do you have access to?** (email list size, social following, ad budget, partnerships)
6. **What is the price point?** (if applicable)
7. **Do you have existing customers/users?** (for beta, testimonials, case studies)
8. **What is the budget?** (bootstrapped, moderate, well-funded)

### Step 2: Determine launch type

Select the primary launch strategy based on the user's context:

| Launch Type | Best For | Key Channel | Timeline |
|---|---|---|---|
| Product Hunt | SaaS, dev tools, consumer apps | Product Hunt + Twitter/X | 4-6 weeks prep |
| Email List Launch | Course, info product, SaaS with existing list | Email | 6-8 weeks |
| Social Media Launch | Consumer product, personal brand | Twitter/X, LinkedIn, Instagram | 4-6 weeks |
| Paid Ads Launch | E-commerce, established product | Facebook/Google Ads | 2-4 weeks prep |
| Community Launch | Niche product, developer tools | Reddit, Discord, Slack communities | 6-8 weeks |
| Partner Launch | B2B, enterprise, marketplace | Partner channels | 8-12 weeks |
| Hybrid Launch | Any high-stakes launch | Multi-channel coordinated | 8-12 weeks |

### Step 3: Generate the 8-week launch timeline

Plan backwards from the user's launch date. Phases (full per-week tasks + deliverables in [`references/timeline.md`](references/timeline.md)):

| Phase | Weeks | Objective |
|---|---|---|
| **Foundation** | 1–2 | Lock in positioning, build assets, set up infrastructure (positioning statement, landing page, email-capture, analytics, asset library). |
| **Audience Building** | 3–4 | Grow the launch list, warm the audience, line up partners (lead magnet, social cadence, partner outreach, "build-in-public" updates). |
| **Pre-Launch Intensification** | 5–6 | Open beta / waitlist, build social proof, schedule launch content (early testimonials, case studies, scheduled email sequence, scheduled social posts). |
| **LAUNCH WEEK** | 7 | Hour-by-hour launch-day plan: launch sequence emails, scheduled social, partner activation, monitoring, real-time response. |
| **Post-Launch** | 8 | Sustain momentum, capture insights (post-launch emails, retrospective, customer-success follow-up, second-wave activation). |

Always include a **"minimum viable launch"** option for users with limited resources.

### Step 4: Email sequence templates

Generate customized versions of the **pre-launch sequence (weeks 5–6)** and the **launch sequence (week 7)** for the user's product. Full templates: [`references/email-templates.md`](references/email-templates.md).

### Step 5: Social media launch posts

Generate platform-specific posts for the user's chosen channels (pick from Twitter/X thread, LinkedIn post, Instagram/visual). Full templates: [`references/social-templates.md`](references/social-templates.md).

### Step 6: Press and media outreach

Only if the launch warrants press (newsworthy hook, novel product, fundraising tie-in). Generate the pitch email + media list + timing. Full template + media-list patterns: [`references/outreach.md`](references/outreach.md).

### Step 7: Influencer and partner coordination

Generate the partnership outreach email + coordination timeline (4 weeks out → launch day → post-launch). Full template + cadence: [`references/outreach.md`](references/outreach.md).

### Step 8: Launch metrics dashboard

Build the metrics dashboard the user will track during and after launch. Categories:

- **Acquisition** — landing-page traffic, conversion rate, paid-ad CTR/CPC, organic-vs-paid mix, email signups.
- **Engagement** — email open / click rates per sequence, social impressions / engagement rate / saves, video watch time, comments.
- **Revenue** — units sold, gross/net revenue vs goal, AOV, conversion rate by channel, refund/churn rate.
- **Brand** — share of voice, sentiment, branded search volume, press mentions, partner-driven reach.

Full KPI tables with target benchmarks per launch type: [`references/metrics-and-antipatterns.md`](references/metrics-and-antipatterns.md).

### Step 9: Common launch mistakes to avoid

Top 5 to call out in every playbook:

1. Launching to a cold audience (no list / no community warmed up).
2. Single-day launch with no pre- or post-launch runway.
3. No social proof — testimonials, case studies, or beta wins.
4. Vague positioning — generic value props nobody can act on.
5. No real-time response plan for launch day (questions, refunds, bugs).

Full catalog (≈12 mistakes with prevention checklist each): [`references/metrics-and-antipatterns.md`](references/metrics-and-antipatterns.md).

### Step 10: Budget allocation guide

| Budget Level | Allocation |
|---|---|
| **Bootstrapped ($0-500)** | 100% organic: content, communities, email list, personal outreach |
| **Moderate ($500-5,000)** | 40% paid ads, 30% influencer/partner, 20% tools/software, 10% design |
| **Well-Funded ($5,000-25,000)** | 35% paid ads, 25% influencer/partner, 20% PR/media, 10% events, 10% tools |
| **Enterprise ($25,000+)** | 30% paid ads, 20% events/webinars, 20% PR, 15% influencer, 10% content, 5% tools |

### Step 11: Post-launch analysis framework

After the launch, generate a retrospective covering:

1. **Goal vs Actual** — did you hit your targets?
2. **Channel Performance** — which channels drove the most conversions?
3. **Email Performance** — open / click / conversion rates by email.
4. **Top Converting Content** — which posts, pages, or ads drove the most action?
5. **Customer Feedback Themes** — what are people saying?
6. **What Worked** — top 3 things that drove results.
7. **What Didn't Work** — top 3 things to change next time.
8. **Unexpected Insights** — surprises from the data.
9. **Next Steps** — immediate actions based on learnings.

## Output Format

Generate a file called `LAUNCH-PLAYBOOK.md` with:

```markdown
# Launch Playbook: [Product Name]
## Launch Date: [Date]
## Launch Type: [Type]
## Primary Goal: [Goal with specific target]

---

## Week-by-Week Plan
[Detailed week-by-week tasks with checkboxes]

## Email Sequences
[Complete email templates customized for the product]

## Social Media Content
[Platform-specific posts ready to customize and schedule]

## Partner/Influencer Plan
[Outreach templates and coordination timeline]

## Launch Day Checklist
[Hour-by-hour launch day plan]

## Metrics Dashboard
[Metrics to track with target benchmarks]

## Budget Allocation
[Specific dollar amounts based on stated budget]

## Post-Launch Plan
[Week 8+ activities and analysis framework]
```

## Key Principles

- Every recommendation should be tied to the user's specific product, audience, and resources. Generic advice is useless.
- Include specific templates they can copy-paste and customize, not just frameworks.
- If the user has run previous skills (market audit, market landing, market brand), incorporate those findings into the launch plan.
- Time the playbook to their stated launch date and work backwards.
- Always include a "minimum viable launch" option for users with limited resources.
