---
name: Newsletter Writing
description: Create engaging email newsletters that nurture subscribers and drive conversions
version: 1.0.0
triggers:
  - "newsletter"
  - "email newsletter"
  - "weekly email"
  - "email sequence"
  - "send newsletter"
  - "skill:newsletter"
---

# Newsletter Writing

## Purpose

Build and nurture an email audience through compelling newsletters that:
- Provide consistent value to subscribers
- Establish trust and authority
- Drive traffic to owned platforms
- Convert readers into customers

## When to Use This Skill

- Weekly newsletters for ongoing engagement
- Launch announcements for products/courses
- Nurture sequences for new subscribers
- Re-engagement campaigns for cold leads
- Product updates and announcements
- Curated content roundups

## Core Concepts

### The Newsletter Funnel

```typescript
interface NewsletterFunnel {
  awareness: {
    content: "Top-of-funnel value posts";
    frequency: "Weekly";
    goal: "Build trust";
  };
  consideration: {
    content: "Deep-dive content, case studies";
    frequency: "2x weekly";
    goal: "Demonstrate expertise";
  };
  conversion: {
    content: "Product launches, limited offers";
    frequency: "As needed";
    goal: "Drive sales";
  };
  retention: {
    content: "Onboarding, exclusive content";
    frequency: "Post-purchase";
    goal: "Customer success";
  };
}
```

### Email Anatomy

```
┌─────────────────────────────────────────────────────────┐
│ PREHEADER (Preview text - 40-80 chars)                  │
├─────────────────────────────────────────────────────────┤
│ SUBJECT LINE (30-50 chars - creates curiosity)          │
│ PREHEADER text (40-80 chars - supplements subject)      │
├─────────────────────────────────────────────────────────┤
│ GREETING (Personal, warm - "Hey [Name]")                │
├─────────────────────────────────────────────────────────┤
│ HOOK (1-2 sentences - grab attention)                   │
├─────────────────────────────────────────────────────────┤
│ BODY CONTENT (Scannable, valuable)                      │
│ • Bullet points for readability                         │
│ • Short paragraphs (2-3 sentences)                      │
│ • Bold key phrases                                      │
├─────────────────────────────────────────────────────────┤
│ CTA (Clear action - 1 primary, optional secondary)      │
├─────────────────────────────────────────────────────────┤
│ SIGNATURE (Consistent, builds recognition)              │
├─────────────────────────────────────────────────────────┤
│ PS (Often highest-read section)                         │
└─────────────────────────────────────────────────────────┘
```

## Patterns

### Pattern 1: Weekly Newsletter Structure

```markdown
Subject: [Week of Month Day]: [Intriguing teaser]

Preheader: [Complementary teaser - 50 chars]

---

Hey [Name],

**[HOOK - 1-2 sentences that grab attention]**

**[SECTION 1: Main Value]**
[Headline or subtopic]

[Brief explanation with 2-3 paragraphs]

**[SECTION 2: Deep Dive]**
[Headline or subtopic]

[Practical takeaways with examples]

**[SECTION 3: Curated/Found]**
[Headline]

- [Item 1 with brief description]
- [Item 2 with brief description]
- [Item 3 with brief description]

**[SECTION 4: Upcoming/Preview]**
[What's coming next week or month]

**[CTA]**
[Primary action you want them to take]

Best,
[Your Name]

P.S. [P.S. often has highest open rate - include extra value or reminder]

---

[Unsubscribe] [Privacy] [Web Version]
```

### Pattern 2: Product Launch Email

```markdown
Subject: 🚀 [PRODUCT NAME] is here (and it's a game-changer)

Preheader: After 6 months of development, [result]

---

Hey [Name],

**[BIG ANNOUNCEMENT - 1 sentence]**

[Product name] is finally ready.

Here's what it does:

✅ [Key benefit 1]
✅ [Key benefit 2]  
✅ [Key benefit 3]

**Why I built this:**

[Personal story - 3-4 sentences connecting to reader's pain point]

**What early testers say:**

> "[Powerful testimonial quote]"

**Launch offer (72 hours only):**
- [Discount or bonus]
- [Best price of the year]
- [Exclusive access]

→ [Get [Product Name] now →]

No questions asked, 30-day money-back guarantee.

[Your Name]

P.S. [Urgency element - limited quantity or time]

---

**[EMAIL FOOTER]**
```

### Pattern 3: Welcome Sequence Email

```markdown
Email 1: Welcome (Day 0)
---
Subject: Welcome to the [Community Name] family! 🎉

Hey [Name],

Thanks for joining [NUMBER] others who receive [newsletter name].

Here's what you can expect:

📈 [Content type 1 - e.g., "Weekly insights on [topic]"]
🎯 [Content type 2 - e.g., "Actionable frameworks"]
🌟 [Content type 3 - e.g., "Exclusive offers"]

To get you started, here's my best [resource]:

[Link to best free resource]

Looking forward to having you in the community.

[Your Name]

---

Email 2: Your Story (Day 2)
---
Subject: My story and why [newsletter] exists

Hey [Name],

Before we dive into [topic], I want you to know who I am and why I send this newsletter.

[3-4 paragraphs about your background, transformation, mission]

[Connect to reader's potential transformation]

This newsletter exists to help you [reader outcome].

[CTA to reply with question]

[Your Name]

---

Email 3: The Framework (Day 5)
---
Subject: The exact framework I use to [result]

Hey [Name],

I promised you actionable frameworks.

Here's the [framework name] I use to [result]:

[Framework steps with explanation]

I've put together a worksheet to help you implement this:

[Link to worksheet]

Let me know what you think.

[Your Name]
```

## Step-by-Step Process

1. **List Segmentation**
   - Identify subscriber categories
   - Personalize based on behavior
   - Tag based on engagement
   - Segment for targeted campaigns

2. **Content Planning**
   - Plan content calendar monthly
   - Batch write emails in sessions
   - Create reusable templates
   - Build email sequence templates

3. **Subject Line Optimization**
   - A/B test subject lines
   - Use curiosity and specificity
   - Avoid spam trigger words
   - Keep under 50 characters

4. **Write and Design**
   - Use pre-written templates
   - Write in conversational tone
   - Optimize for mobile (short paragraphs)
   - Include one clear CTA

5. **Test and Iterate**
   - A/B test send times
   - Test subject lines and preheaders
   - Monitor open rates and CTR
   - Continuously improve based on data

## FrankX Application

```markdown
Subject: You're not broken. You're just undisciplined. Here's the fix.

Hey [Name],

The self-improvement industry wants you to believe you're broken.

You're not.

You're undisciplined.

And discipline is a skill that can be trained.

**Here's the framework:**

The 5 Pillars of Transformative Discipline:

1/ Identity first
Who do you need to become?

2/ Environment design
Your surroundings shape your choices.

3. Micro-commitments
Start so small you can't fail.

4. Accountability systems
External structures for internal change.

5. Progress tracking
What gets measured gets managed.

This works for any transformation:

→ Health
→ Wealth
→ Relationships
→ Consciousness

The golden age demands golden discipline.

[Your CTA here]

[Your Name]

P.S. Reply with your biggest discipline challenge. I read every response.
```

## Anti-Patterns

| Bad Practice | Why It's Bad | Better Approach |
|--------------|--------------|-----------------|
| Long paragraphs | Mobile readers skip | 2-3 sentences max |
| Multiple CTAs | Confuses reader | One primary CTA |
| Clickbait subject lines | Damages trust | Deliver on promise |
| Inconsistent sending | Loses audience | Regular schedule |
| Ignoring unsubscribes | Poor list hygiene | Welcome non-openers |
| No personalization | Feels impersonal | Use name, segment by interest |

## Quick Commands

```bash
# Create weekly newsletter
skill:newsletter, write a weekly newsletter about [THEME]

# Write product launch email
skill:newsletter, create a product launch email for [PRODUCT]

# Build welcome sequence
skill:newsletter, create a 5-email welcome sequence

# Repurpose blog to newsletter
skill:newsletter, turn my blog post [URL] into a newsletter

# Write newsletter about topic
skill:newsletter, write about [TOPIC] for my email list
```

## Related Skills

- `blog-writing` - Create content to repurpose
- `social-media` - Promote newsletters on social
- `content-strategy` - Plan email content calendar
- `seo-optimization` - Optimize newsletter links

## Resources

- `resources/templates.md` - Email templates by type
- `resources/subject-lines.md` - Proven subject line formulas
- `resources/welcome-sequence.md` - Welcome email sequences
- `resources/sequence-triggers.md` - Automated email triggers
