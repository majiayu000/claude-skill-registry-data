---
name: copywriting
description: Brand-voice copywriting with psychology frameworks
author: "@namanwtf"
version: 3.0.0
requires: brand-context, marketing-psychology
category: content
---

# 📝 Copywriting Agent

**Purpose:** Create conversion-optimized copy that matches your brand voice and applies proven psychology frameworks. Never write bland copy again.

---

## When to Use

```bash
# Create homepage copy
@copywriting create homepage

# Write landing page for product launch
@copywriting create landing-page "Product X Launch"

# Optimize existing copy
@copywriting optimize meta-ads --variant B

# Write email sequence
@copywriting email-sequence welcome

# Create social media content
@copywriting social --platform instagram --campaign "Summer Sale"
```

---

## Capabilities

### 1. Brand Voice Training
Automatically reads your `brand-context.md` and adapts:

```yaml
Brand Voice: Bold & Energetic
→ Headlines: Action verbs, power words
→ Tone: Confident, youthful, exciting
→ CTAs: "Claim", "Grab", "Dominate" (not "Buy", "Submit")
```

### 2. Psychology Frameworks Auto-Applied

Every piece of copy includes:

```markdown
## SPECIFICITY PRINCIPLE
❌ "Long battery life"
✅ "48-hour battery — 2 days heavy use"

## SOCIAL PROOF
❌ "Trusted by many"
✅ "Join 50,000+ users who never look back"

## SCARCITY
❌ "Limited time offer"
✅ "Only 500 units at launch price"

## PRICE ANCHORING
❌ "$199"
✅ "Was $249 | Now $199 | You save $50"

## AUTHORITY
❌ "Good quality"
✅ "Engineered with aerospace-grade materials"
```

### 3. Multi-Language Support
For global markets:
- English (US/UK/AU)
- Spanish
- French
- German
- Localized CTAs and cultural references

### 4. Industry-Specific Copy
Auto-detects your industry and emphasizes relevant features:
- **SaaS**: Features, integrations, ROI
- **E-commerce**: Product benefits, shipping, returns
- **Mobile/Tech**: Specs, performance, battery
- **Fashion**: Style, materials, exclusivity
- **Food**: Taste, ingredients, experience

---

## Configuration

Add to your `brand-context.md`:

```yaml
copywriting:
  voice: "bold-energetic"  # Options: professional, friendly, luxury, tech-savvy, playful
  languages: ["english", "spanish"]
  
  messaging-pillars:
    - "Quality"
    - "Value"
    - "Innovation"
  
  psychology-frameworks:
    - "specificity"
    - "social-proof"
    - "scarcity"
    - "price-anchoring"
    - "authority"
  
  forbidden-words:
    - "cheap"
    - "budget"
    - "entry-level"
  
  preferred-words:
    - "value" (instead of cheap)
    - "premium features" (instead of budget)
    - "smart choice" (instead of entry-level)
    
  industry: "saas"  # saas, ecommerce, mobile, fashion, food, etc.
```

---

## Usage Examples

### Example 1: Homepage Hero Section
```
User: @copywriting create homepage-hero

Agent: 📝 HOMEPAGE COPY OPTIONS

OPTION 1: Bold & Direct
────────────────────────
**Headline:** Scale Faster. Work Smarter.
**Subheadline:** The platform that automates your workflow.
Used by 10,000+ teams worldwide. Starting at $29/month.
**CTA:** Start Free Trial →

Psychology applied:
✅ Action verbs ("Scale", "Work")
✅ Specifics (10,000+ teams, $29/month)
✅ Outcome-focused ("Smarter")

OPTION 2: Challenge-Based
────────────────────────
**Headline:** Your Current Tools Are Holding You Back.
**Subheadline:** Switch to the platform that actually works.
10,000+ teams already made the move.
**CTA:** See Why →

OPTION 3: Social Proof
────────────────────────
**Headline:** Join 10,000+ Teams Working Smarter.
**Subheadline:** The workflow automation platform that 
saves 10 hours every week. Starting at $29/month.
**CTA:** Join Free →

RECOMMENDATION: Option 1 (A/B test with Option 2)
```

### Example 2: Product Page
```
User: @copywriting create product-page product-x

Agent: 📝 PRODUCT-X PRODUCT PAGE

HERO SECTION:
**Headline:** Automate Your Workflow. Reclaim Your Time.
**Subheadline:** 
• Save 10+ hours/week with smart automation
• Integrate with 100+ tools you already use
• Start free, upgrade when you grow

**Price:** $29/month
**Launch Offer:** $19/month (first 3 months)

KEY FEATURES:
⚡ **Automation That Actually Works**
    Build workflows without code. Connect your tools.
    Let the system handle the repetitive work.

🔗 **100+ Integrations**
    Slack, Notion, HubSpot, Salesforce, and more.
    If you use it, we connect to it.

📊 **Analytics Dashboard**
    Track time saved, ROI, and team productivity.
    Make data-driven decisions.

🔒 **Enterprise Security**
    SOC 2 compliant. GDPR ready. Your data is safe.

SOCIAL PROOF:
"Saved our team 15 hours/week" — Tech Company CEO
★★★★★ 4.9/5 from 2,000+ reviews

CTA: **Start Free Trial →** (No credit card required)
```

### Example 3: Meta Ad Copy
```
User: @copywriting create meta-ad "product-x-launch"

Agent: 📝 META AD OPTIONS

AD 1: Problem-Solution
──────────────────────
**Primary Text:**
Tired of repetitive tasks eating your day? 😤

Meet Product-X — automation that actually works.
Save 10+ hours/week. Starting at $29/month.

Teams are switching. Here's why 👇

**Headline:** Automate Your Workflow
**Description:** Save 10+ hours/week | $29/month
**CTA:** Start Free Trial

AD 2: Social Proof
──────────────────────
**Primary Text:**
10,000+ teams made the switch this year.

The reason? Product-X delivers:
✅ 10+ hours saved weekly
✅ 100+ integrations
✅ Starts at $29/month

Join them. Free trial available 🔥

**Headline:** Trusted by 10,000+ Teams
**Description:** From $29/month | 14-day free trial
**CTA:** Start Free

AD 3: Urgency
──────────────────────
**Primary Text:**
⚠️ Launch offer ends in 48 hours

Product-X at $19/month (normally $29)
Save 35% — forever.

10+ hours saved weekly. 100+ integrations.

Don't miss out →

**Headline:** 35% Off Ends Soon
**Description:** Launch offer + free onboarding
**CTA:** Claim Offer

RECOMMENDATION: Run all 3. Budget split: 40/40/20
```

### Example 4: Email Sequence
```
User: @copywriting email-sequence onboarding

Agent: 📝 ONBOARDING EMAIL SEQUENCE

EMAIL 1: Welcome (Send immediately)
────────────────────────────────
Subject: Welcome to Product-X! Let's get you set up 🚀

Hi [First Name],

Welcome to the 10,000+ teams using Product-X to save time!

Here's what happens next:
✅ Connect your first integration (takes 2 minutes)
✅ Build your first automation workflow
✅ Start saving hours every week

[CTA: Connect Your First Tool →]

Need help? Reply to this email — we read every one.

Cheers,
The Product-X Team

---

EMAIL 2: Quick Win (Send after 24 hours)
────────────────────────────────
Subject: Your first automation is waiting 🎯

Hi [First Name],

Most Product-X users save 5+ hours in their first week.

Here's a 5-minute automation that'll save you 2 hours/week:

[Walkthrough: Connect Slack + Calendar]

Try it now → [CTA]

---

EMAIL 3: Social Proof (Send after 3 days)
────────────────────────────────
Subject: How [Similar Company] saved 15 hours/week 📈

[Case study email with customer story]
```

---

## Copywriting Frameworks Applied

### PAS (Problem-Agitate-Solution)
```
**Problem:** You waste hours on repetitive tasks
**Agitate:** You're falling behind. Your competitors are faster.
           You're stuck doing work a machine could handle.
**Solution:** Product-X — automate the boring stuff.
```

### AIDA (Attention-Interest-Desire-Action)
```
**Attention:** Scale Faster. Work Smarter.
**Interest:** 10,000+ teams save 10 hours/week
**Desire:** Imagine what you could do with that time
**Action:** Start Free Trial →
```

### FAB (Features-Advantages-Benefits)
```
**Feature:** 100+ integrations
**Advantage:** Connects to tools you already use
**Benefit:** No migration headache, works immediately
```

---

## Related Skills

- **pricing-optimizer**: Price messaging and offers
- **meta-ads-optimizer**: Ad copy optimization
- **email-sequence**: Email marketing automation
- **social-content**: Social media copy

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
