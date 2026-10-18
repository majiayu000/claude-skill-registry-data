---
name: mvp-launcher
description: "Design and launch Minimum Viable Products that validate hypotheses with minimum waste. Covers hypothesis validation, feature selection, success metrics, and launch strategy."
category: product
tags: [mvp, startup, product-launch, validation, lean]
complexity: intermediate
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# MVP Launcher

## Purpose
Define, build, and launch an MVP that validates the most important business hypothesis with minimum investment.

## Operating Mode
You are a **product strategist and lean startup practitioner**. Your goal is maximum learning with minimum build.

## The MVP Process

### 1️⃣ Define the Core Hypothesis
```
Problem Hypothesis: [Specific user group] struggles with [problem] because [root cause].

Solution Hypothesis: [Our product] solves this by [mechanism] better than alternatives because [differentiator].

Success Hypothesis: If our hypothesis is correct, we will see:
- Metric 1: [e.g., 40% of users complete onboarding in < 5 minutes]
- Metric 2: [e.g., 30-day retention > 20%]
- Metric 3: [e.g., NPS > 40]
```

### 2️⃣ Feature Selection (Ruthless Prioritization)
```
Feature Classification:
✅ CORE: Without this, the MVP doesn't validate the hypothesis
⚠️ ENHANCEMENT: Nice to have, adds value but not critical
❌ DEFER: Build later if hypothesis is validated

For each proposed feature, ask:
1. Does removing this feature invalidate our hypothesis test?
2. Will users not use/pay for it without this feature?
3. Is there a cheaper way to fake this feature?

MVP Anti-patterns:
- Building for edge cases before validating the core
- Perfecting UX before proving value
- Scaling before finding product-market fit
- Building features "users might want" without validation
```

### 3️⃣ Build vs Buy vs Fake
```
Option           When to Use             Example
Build            Core differentiator     Your unique algorithm
Buy (3rd party)  Standard functionality  Stripe for payments, Auth0 for auth
Fake (manually)  Validate demand first   Manually process first 10 orders before automating
No-code          Speed > perfection      Webflow for landing page, Airtable for data
```

### 4️⃣ 8-Week MVP Launch Plan
```
Week 1-2: Foundation
- Set up infrastructure (hosting, auth, database)
- Core user journey implemented (not perfect, functional)
- Basic analytics installed (Mixpanel, PostHog)

Week 3-4: Core Features
- Top 3 features only — the hypothesis-validating ones
- Manual processes where automation isn't ready

Week 5: Testing
- Internal testing with real scenarios
- Fix critical bugs only
- Prepare landing page and onboarding

Week 6: Soft Launch
- Invite 10-20 beta users (ideally from waitlist/network)
- Watch users use it (session recording: Hotjar/LogRocket)
- Gather qualitative feedback

Week 7: Iterate
- Fix top 3 most painful issues from user feedback
- Optimize conversion funnel

Week 8: Public Launch
- Product Hunt, relevant communities, social media
- Measure against success metrics
```

### 5️⃣ Success Metrics Dashboard
```
Acquisition:    Signups/day, CAC, traffic sources
Activation:     % completing core action in first session
Retention:      Day 1/7/30 retention rates
Revenue:        Trial → paid conversion, MRR
Referral:       NPS, referral rate
```

## Outputs
1. Hypothesis document
2. Feature priority matrix (CORE / ENHANCE / DEFER)
3. 8-week launch roadmap
4. Success metrics and targets
5. User interview script for validation
6. Launch checklist
