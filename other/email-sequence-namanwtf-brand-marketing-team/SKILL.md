---
name: email-sequence
description: Automated email sequences for lifecycle marketing
author: "@namanwtf"
version: 3.0.0
requires: brand-context, copywriting
category: email
---

# 📧 Email Sequence Agent

**Purpose:** Create automated email flows for onboarding, retention, and reactivation.

---

## Email Sequence Types

### Welcome Series (5 emails)
1. **Day 0:** Welcome + product overview
2. **Day 2:** Key features highlight
3. **Day 5:** Social proof + reviews
4. **Day 7:** Special offer
5. **Day 14:** Check-in + support

### Abandoned Cart (3 emails)
1. **1 hour:** Reminder + save cart
2. **24 hours:** Urgency + discount
3. **72 hours:** Final reminder + testimonial

### Re-engagement (3 emails)
1. **Day 30:** "We miss you" + what's new
2. **Day 45:** Special comeback offer
3. **Day 60:** Final attempt + survey

### Post-Purchase (4 emails)
1. **Immediately:** Order confirmation
2. **Day 3:** Shipping update + tips
3. **Day 7:** How to get started
4. **Day 14:** Review request

---

## Commands

```bash
@email-sequence create welcome-series
@email-sequence create abandoned-cart
@email-sequence create re-engagement
@email-sequence create post-purchase
@email-sequence optimize --open-rate
@email-sequence a/b-test --subject-lines
```

---

## Best Practices

- Subject lines: 40-50 characters
- Preview text: Max 90 characters
- Mobile-first design (60%+ open on mobile)
- Single CTA per email
- Send time optimization (test 10 AM - 2 PM in your timezone)
- Personalize with first name and behavior

---

## Configuration

Add to your `brand-context.md`:

```yaml
email-sequence:
  from-name: "Your Brand"
  from-email: "hello@yourbrand.com"
  reply-to: "support@yourbrand.com"
  
  timing:
    timezone: "UTC"
    business-hours: "9 AM - 6 PM"
    
  sequences:
    welcome:
      enabled: true
      delay: "immediate"
    
    abandoned-cart:
      enabled: true
      delays: ["1 hour", "24 hours", "72 hours"]
      
    re-engagement:
      enabled: true
      delay: "30 days"
```

---

## Usage Examples

### Create Welcome Series
```
User: @email-sequence create welcome-series

Agent: 📧 WELCOME SERIES CREATED

EMAIL 1: Welcome (Send immediately)
────────────────────────────────
Subject: Welcome to [Brand]! Let's get you started 🚀

Hi {{first_name}},

Welcome to the 10,000+ [users/customers] using [Brand] to [benefit]!

Here's what happens next:
✅ [Action 1] (takes 2 minutes)
✅ [Action 2]
✅ Start [achieving benefit]

[CTA: Get Started →]

Need help? Reply to this email — we read every one.

Cheers,
The [Brand] Team

---

EMAIL 2: Quick Win (Send after 24 hours)
────────────────────────────────
Subject: Your first [result] is waiting 🎯

Hi {{first_name}},

Most [Brand] users see [result] in their first week.

Here's a 5-minute [action] that'll [benefit]:

[Walkthrough with screenshots]

Try it now → [CTA]

---

[Emails 3-5 generated...]

Total sequence: 5 emails over 14 days
Expected open rate: 45%+
Expected click rate: 12%+
```

### Optimize Open Rates
```
User: @email-sequence optimize --open-rate

Agent: 📊 OPEN RATE OPTIMIZATION

Current Performance:
• Average open rate: 32%
• Industry benchmark: 25%
• Status: ✅ Above average

Optimization Actions:
✅ A/B tested 3 subject line formulas
✅ Optimized send time (moved to 10 AM local)
✅ Improved preview text

New Subject Line Formula:
"[Benefit] + [Curiosity] + [Emoji]"

Example: "Your [result] is waiting 🎯"

Expected improvement: +15% open rate
```

---

## Related Skills

- **copywriting**: Email copy creation
- **analytics-dashboard**: Email performance tracking
- **page-cro**: Landing page optimization for email traffic

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
