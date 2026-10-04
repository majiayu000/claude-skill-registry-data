---
name: mvp
description: >
  Guide building a minimum viable product through manual-first, then processized, then productized stages.
  Use when someone is ready to build their first product or struggling with scope.
compatibility:
  models: [any-llm]
  use-case: product-development
  frameworks: [minimalist-entrepreneur, lean-startup]
---

# MVP (Minimum Viable Product)

Build as little as possible to deliver value to customers. Go manual → processized → productized.

## Use This Skill When

- User is ready to build their first product
- User is struggling with MVP scope creep
- User is deciding what to build and how to build it
- User is at the "idea to shipping" stage
- User says phrases like "product roadmap", "feature list", "should I build", "what's the MVP", "how do I launch"

## When NOT to Use

- User is optimizing existing products (use product-optimization skill)
- User is building growth infrastructure (use growth skill)
- User is designing user experience/UI (use product-design skill)

## Context: Product Development Stage

**Idea phase**: Problem identified; no product yet  
**Manual phase**: Founder delivering service manually  
**Processized phase**: Repeatable documented process  
**Productized phase**: Automated product; customers self-serve → **Target for MVP completion**

## Core Principle

**Build as little as possible.** Your goal is to start delivering value to your community as quickly as possible. Not beautiful, not polished, not complete—just valuable and working.

## Instructions

### The Three Stages of Product Development

**Progress through these in order. Do not skip stages.**

#### Stage 1: Manual (Do It Yourself)
**Timeline**: Week 1–2  
**Process**: You solve the problem by hand for each customer

- You are the entire product: customer service, fulfillment, engineering
- Document every step you take — these steps become your system
- Record common questions and answers
- Collect data on how long each step takes
- **Goal**: Prove customers will pay, and understand what they value

**Example**:
- Before Gumroad automated payouts, Sahil manually collected PayPal emails, processed transfers, and sent confirmations
- Before hiring, Stripe founders personally onboarded early customers via calls
- Before building, many SaaS founders offer their service as a done-for-you service

**Key success metric**: At least 5 customers willingly paying for manual service

#### Stage 2: Processized (Systematize)
**Timeline**: Week 3–4  
**Process**: Codify your manual work into repeatable, documented steps

- Write down every step on paper (or in Notion)
- Another person should be able to follow your "magic piece of paper" and deliver the service
- Identify bottlenecks and friction points
- Optimize for speed and consistency
- **Goal**: Understand your operations deeply before automating

**Example deliverable**:
```
CUSTOMER ONBOARDING PROCESS:
1. Customer sends email with X request
2. Check if they meet criteria (yes/no)
3. If yes, send welcome email + setup guide
4. Schedule 15-min call
5. After call, send invoice
6. Collect payment
7. Deliver [deliverable]
8. Follow-up email in 1 week
9. Document feedback for next customer
```

**Key success metric**: Consistent delivery, documented process, time-per-customer is known

#### Stage 3: Productized (Automate)
**Timeline**: Week 5+  
**Process**: Automate the processized work so customers serve themselves

- Only automate what's proven to work manually
- Use tools (Zapier, Airtable, no-code) before writing code
- Start with forms → lists → workflows
- **Goal**: Let customers self-serve without your involvement

**Example automation**:
- Manual email form → Typeform (collects requests)
- Typeform + Zapier → Google Sheets (organizes data)
- Google Sheets + Zapier → Stripe (sends invoice)
- Stripe → Email automation (delivers product)

**Key success metric**: Customers getting value without your manual involvement

### The Four MVP Build Questions

Before building anything, answer all four:

| Question | Purpose | Good Answer |
|----------|---------|------------|
| **Can I ship it in a weekend?** | Scope discipline | Yes: one feature, not ten |
| **Does it make customer's life better?** | Value test | Yes: measurable improvement |
| **Is someone willing to pay?** | Market validation | Yes: at least 3 customers prepaid |
| **Can I get feedback quickly?** | Iteration speed | Yes: daily/weekly customer contact |

**If you can't answer "yes" to all four, reduce scope.**

### What to Build

**Scope rules**:
- **One thing**: Your product does one thing well, not ten things poorly
- **Forms and lists**: Most products are just CRUD (Create, Read, Update, Delete) operations
- **No polish**: CraigsList is never been pretty. Functionality > aesthetics for MVP
- **Charge something**: Free vs. $1 has a psychological cliff (zero-price effect). Charge even if it's just $5/month
- **Use existing tools**: Use Carrd, Gumroad, Stripe, Airtable, Google Forms, Zapier, Notion—whatever ships fastest
- **One workflow**: Nail one user journey completely before adding secondary features

**Technology choices**:
- No-code first (Zapier, Airtable, Make)
- Low-code second (Webflow, Bubble)
- Custom code last (only after validating the model)

### What NOT to Build

- Don't build features you "might" need someday — build for today's customers
- Don't build for scale — you don't have scale problems yet (1–100 customers)
- Don't build a mobile app when a website works
- Don't write code when a spreadsheet or no-code tool works
- Don't hire a designer when basic, functional design works
- Don't optimize performance/security before proving the idea
- Don't add authentication/payments until customers are actually paying

### Versioning and Iteration

**Key insight**: Avoid the "v2" trap

- Gumroad has never shipped "v2"—just thousands of incremental improvements
- Each ship is a small iteration: gather feedback, improve, ship again
- Your goal is to move from founder-dependent to customer-driven feedback loops
- Expect to iterate weekly, not monthly

**Feedback loops**:
- Weekly: Direct customer interviews
- Biweekly: Email survey
- Monthly: Usage analytics review
- Each iteration = 1–2 small improvements, not rewrites

### Launch Readiness Checklist

Before shipping your MVP, confirm:

**Branding**:
- [ ] Business name (two real words > made-up name; passes "radio test")
- [ ] Domain registered (~$10/year; use NameCheap or Vercel)
- [ ] Brand presence (logo, color, tone established)

**Online presence**:
- [ ] Website/landing page (Carrd, Webflow, or Notion)
- [ ] Social media accounts (personal + business)
- [ ] Email address (name@domain.com, not gmail)

**Payments & Legal**:
- [ ] Payment processor set up (Stripe, Square, or Gumroad)
- [ ] Pricing decided (cost + 50%+ margin)
- [ ] Terms of service (basic, template is fine)

**Customer communication**:
- [ ] Email funnel (welcome → onboarding → support)
- [ ] Support channel (email, Slack, or form)
- [ ] Feedback collection method (form, survey, or call)

**Documentation**:
- [ ] Product walkthrough guide (written or video)
- [ ] FAQ (common questions from beta customers)
- [ ] Contact/help page

## Output

For each user building an MVP, define:

1. **The single thing** (What problem does this solve? In one sentence.)
2. **Manual implementation** (Can you deliver this to 5 customers by hand?)
3. **This week's goal** (What ships this weekend? Not this quarter.)
4. **Initial price** (Cost + 50% margin, or value-based pricing)
5. **Feedback mechanism** (How will you talk to customers weekly?)
6. **Timeline to productized** (When will manual become processized? Then productized?)

**Example MVP plan**:
- **One thing**: Meal plan generator for busy parents
- **Manual**: You manually create 3 meal plans per week, email them to customers
- **Ship this week**: Landing page + email signup
- **Price**: $10/month
- **Feedback**: Weekly email survey + monthly customer calls
- **Timeline**: Manual (week 1–4) → Processized (week 5–8) → Productized (week 9+) with templated plans → Automated with AI generation
