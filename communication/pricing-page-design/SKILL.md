---
name: pricing-page-design
description: 帮助 SaaS 或应用设计价格梯度、套餐对比、文案和转化策略。借鉴 Marketing Skills 的 pricing / conversion 思路和 Vercel writing guidelines 对 pricing pages 的强调。不提供财务投资建议，只帮助组织定价页表达、套餐结构和 FAQ。当用户需要设计定价页、优化套餐结构、撰写定价文案或处理定价异议时触发。
license: MIT
---

# Pricing Page & Package Design

## Overview

Helps SaaS and app builders design pricing tiers, package comparisons, pricing copy, and conversion-focused FAQs. Focuses on communication and packaging, not financial or investment advice.

## When to Use

- Designing pricing tiers for a new SaaS product
- Optimizing existing pricing page for clarity and conversion
- Creating plan comparisons and feature matrices
- Writing pricing page copy, FAQs, and objection handling
- Deciding between freemium, trial, or paid-only models
- Packaging features into good-better-best tiers

**When NOT to use:** Don't provide financial advice, investment recommendations, or revenue projections. Don't set prices based on cost-plus calculations alone.

## Core Features

- Creates Free, Pro, Team, or Enterprise-style packages based on user segments and product value
- Improves pricing page clarity, plan naming, feature grouping, objections, FAQs, and CTA placement
- Focuses on communication and packaging, not financial or investment advice

## Workflow

1. **Understand** the product, customer segments, value drivers, and monetization goal
2. **Design** pricing tiers and explain which user each tier is for
3. **Generate** pricing page copy, comparison table guidance, FAQs, and objection handling

## Core Principles

### 1. Value-Based Pricing
Price based on perceived value, not cost. Customers pay for outcomes, not features.

```
Value = Outcome × Urgency × Differentiation
```

### 2. Good-Better-Best Structure
Three tiers capture the market:
- **Good**: Entry point, basic needs, price-sensitive
- **Better**: Most popular, best value, target segment
- **Best**: Power users, enterprises, premium features

### 3. Decoy Effect
Add a decoy to make the target tier more attractive:

| Plan | Price | Features |
|------|-------|----------|
| Basic | $29/mo | 5 projects |
| Pro (target) | $49/mo | 15 projects |
| Enterprise (decoy) | $99/mo | 15 projects + support |

The Enterprise tier makes Pro look like a great deal.

## Pricing Page Structure

### 1. Hero Section
- **Headline**: Clear value proposition (not just "Pricing")
- **Subheadline**: Who it's for and what they get
- **Toggle**: Monthly/Annual (annual discount visible)

### 2. Plan Cards
```
┌─────────────────┬─────────────────┬─────────────────┐
│   Starter       │    Pro          │   Enterprise    │
│   $29/mo        │    $49/mo       │   $99/mo        │
│                 │   Most Popular   │                 │
├─────────────────┼─────────────────┼─────────────────┤
│ 5 projects      │ 15 projects     │ Unlimited       │
│ Basic analytics │ Advanced        │ Custom          │
│ Email support   │ Priority        │ Dedicated       │
│                 │                 │                 │
│ [Start Free]    │ [Start Free]    │ [Contact Sales] │
└─────────────────┴─────────────────┴─────────────────┘
```

### 3. Comparison Table
Feature-by-feature comparison for detailed evaluation:

| Feature | Starter | Pro | Enterprise |
|---------|---------|-----|------------|
| Projects | 5 | 15 | Unlimited |
| Team members | 1 | 5 | Unlimited |
| Analytics | Basic | Advanced | Custom |
| Support | Email | Priority | Dedicated |
| API access | ❌ | ✅ | ✅ |
| SSO | ❌ | ❌ | ✅ |

### 4. FAQ Section
Address common objections:

- "Can I change plans later?"
- "What happens after the trial?"
- "Do you offer refunds?"
- "What's included in support?"
- "Can I cancel anytime?"

### 5. Social Proof
- Customer logos
- Testimonials near pricing
- "Join 10,000+ teams" social proof

### 6. Final CTA
- "Still have questions? Chat with us"
- "Need a custom plan? Contact sales"

## Pricing Psychology Tactics

### Charm Pricing
$49 vs $50 — left-digit effect makes it feel significantly cheaper.

### Anchoring
Show the highest price first, then the target price feels reasonable.

### Bundling
Combine features into packages that feel like a deal:
- "Everything in Pro, plus:"
- "Save 20% with annual billing"

### Free Trial Framing
- "Start free for 14 days" (not "Free trial")
- "No credit card required"
- "Cancel anytime"

### Urgency (Use Sparingly)
- "Limited time: 20% off annual plans"
- "Price increases next month"

## Plan Naming Conventions

| Type | Examples | Best For |
|------|----------|----------|
| Feature-based | Basic, Pro, Enterprise | Clear differentiation |
| Usage-based | Starter, Growth, Scale | Usage-driven products |
| Role-based | Freelancer, Studio, Agency | Role-specific tools |
| Outcome-based | Essential, Professional, Business | Outcome-focused |

## Feature Grouping

Group features into logical buckets:

```
Core Features
├── Projects/workspaces
├── Storage/bandwidth
├── Team members
└── API limits

Advanced Features
├── Analytics & reporting
├── Integrations
├── Automation
└── Custom branding

Support
├── Email support
├── Priority support
├── Dedicated account manager
└── SLA guarantees
```

## Objection Handling

| Objection | Response Strategy |
|-----------|-------------------|
| "Too expensive" | Compare to alternative costs, ROI calculator, value demonstration |
| "Don't need all features" | Highlight modular pricing, usage-based options, or lower tier |
| "Cheaper competitor" | Differentiate on value, not price; show total cost of ownership |
| "Need to ask my boss" | Provide one-pager, ROI calculator, team benefits summary |
| "Not sure which plan" | "Most teams start with Pro"; quiz/tool to recommend plan |
| "Locked in" | Emphasize data portability, export options, no long-term contracts |

## CTA Best Practices

### Primary CTA (Target Tier)
- Action-oriented: "Start Free Trial", "Get Started", "Try Pro"
- Color: High contrast, stands out
- Position: Above the fold, repeated below

### Secondary CTA (Other Tiers)
- Lower emphasis: "Choose Starter", "Contact Sales"
- Color: Muted, but still clickable

### Enterprise CTA
- "Contact Sales" (not "Buy Now")
- Form fields: Name, email, company size, use case
- Response time promise: "We'll respond within 24 hours"

## Writing Guidelines for Pricing Pages

### Do
- Use "you" and "your team" (second person)
- Lead with benefits, not features
- Be specific: "Save 5 hours/week" not "Save time"
- Use active voice
- Keep sentences short and scannable

### Don't
- Use jargon without explanation
- Say "cheap" or "expensive" (let them decide)
- Overpromise or mislead
- Use passive voice
- Write long paragraphs

## Example: AI Resume Tool Pricing

### Plan Design

| | Free | Pro | Team |
|---|---|---|---|
| **Price** | $0 | $12/mo | $49/mo |
| **Resumes** | 3/month | Unlimited | Unlimited |
| **AI edits** | 5/month | Unlimited | Unlimited |
| **Templates** | Basic | Premium | Custom |
| **Export** | PDF | PDF, Word, TXT | All + API |
| **Support** | Community | Email | Priority |

### Page Copy

**Headline**: "Pricing that grows with your career"

**Subheadline**: "Whether you're job hunting solo or managing a team, find the plan that fits"

**Free tier description**: "Perfect for occasional job seekers. Create up to 3 polished resumes with AI-powered suggestions."

**Pro tier description**: "For serious job hunters. Unlimited resumes, premium templates, and full export flexibility."

**Team tier description**: "For career services and agencies. Manage multiple clients, custom branding, and API access."

### FAQ

**Q: Can I upgrade or downgrade anytime?**
A: Yes, change plans instantly. We'll prorate any difference.

**Q: What happens when I hit my Free plan limit?**
A: You can wait until next month or upgrade to Pro for unlimited access.

**Q: Is my data safe?**
A: We never share your resume data. Export and delete anytime.

## Verification Checklist

Before launching pricing page:
- [ ] Three tiers with clear differentiation
- [ ] "Most Popular" or "Recommended" badge on target tier
- [ ] Monthly/annual toggle with discount visible
- [ ] Feature comparison table for detailed evaluation
- [ ] FAQ addresses top 5 objections
- [ ] Social proof near pricing section
- [ ] Clear CTAs for each tier
- [ ] Enterprise/contact sales option
- [ ] Mobile-optimized layout
- [ ] A/B test planned for headline, CTA, or pricing

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We need more tiers" | More tiers = more confusion. Three is usually optimal. |
| "We should hide the free plan" | Free plans are acquisition channels. Don't hide them. |
| "Enterprise needs custom everything" | Even enterprise buyers want to see starting prices. |
| "Pricing is set, can't change" | Pricing is a hypothesis. Test and iterate. |
| "Competitors charge less" | Compete on value, not price. Differentiate or die. |

## Red Flags

- No clear "Most Popular" tier
- Features listed without benefits
- No annual discount
- Hidden fees or surprise charges
- No FAQ section
- No free trial or free tier
- Pricing buried or hard to find
- Copy focused on features, not outcomes
- No comparison table
- No enterprise/contact option
