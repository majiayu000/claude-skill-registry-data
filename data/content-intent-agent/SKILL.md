---
name: content-intent-agent
description: Verifies content matches user search intent to maximize sales, leads, digital sales, and mailing list growth through 34 verification modules and 16-part scoring system
---

# Content Intent Agent Skill

## Purpose
Verifies every piece of content matches user search intent to maximize:
- Sales (e-commerce, products, services)
- Leads (quotes, consultations, demos)
- Digital sales (courses, memberships, digital products)
- Mailing list growth (email subscribers, newsletter signups)

**34 verification modules** + **16-part scoring system** = Complete conversion optimization framework with veto power.

## Prerequisites

Requires `.claude-project-config.json` in project root with:
- Jurisdiction & compliance frameworks
- Target demographics (age, income, disabilities, location)
- Psychographics (pain points, desires, fears, buying triggers)
- Conversion goals (primary and secondary)
- Intent rules (query classification, required modules)
- Offer library (lead magnets, calculators, coupons)
- KPI requirements (analytics events to track)
- Conversion optimization settings

User must research and populate all sections before using skill.

---

# THE 34 VERIFICATION MODULES

## TRADITIONAL SEARCH INTENT (1-15)

### 1. Deep Semantic Intent Matching
Verifies headlines/CTAs mirror search query + intent modifiers ("buy", "how", "reviews").

**Veto if:** H1 missing primary keyword, intro doesn't address query in first 100 words.

### 2. Query Classifier & Stage Inference
Auto-classifies: transactional/commercial/informational/navigational/local/branded/problem-aware
Maps to: BOFU/MOFU/TOFU

**Veto if:** TOFU content with hard "Buy Now" CTA, BOFU with weak "Learn More".

### 3. Intent-Template Validator
Enforces required components per intent:
- **Transactional:** above-fold price/CTA, trust badges, phone tap, financing, FAQ, returns
- **Commercial:** comparison table, pros/cons, "best for" segments, social proof, soft CTA
- **Local:** NAP, service area map, call button, hours, GBP cues
- **Informational:** answer box, step list, FAQ schema, lead magnet

**Veto if:** Missing any required module for detected intent class.

### 4. Dynamic User Intent Feedback Loop
Simulates persona flows - validates target users can complete desired actions.

**Veto if:** Persona simulation shows confusion, can't complete conversion, trust insufficient.

### 5. Competitor Intent Gap Analysis
Analyzes top 10 SERP competitors for same keywords, flags missing USPs/trust elements.

**Veto if:** Missing critical elements present on all top 3 competitors.

### 6. SERP Pattern Mirror & Differentiation
Parses top-10 patterns (lists, tables, FAQs, calculators), enforces common modules + 1 unique element.

**Veto if:** Missing patterns present in 70%+ of top 10, or zero differentiation.

### 7. Ad-to-Landing Parity Guard
Validates headline/USP/price/phone consistency between ads and landing pages.

**Veto if:** Ad keyword not in H1, price differs, phone number differs, USP absent.

### 8. Negative-Intent & Disqualifier Filter
Detects mismatched sub-intents ("free", "DIY", "jobs"), forces alternate offers.

**Veto if:** Hard conversion CTA on "free" intent, no lead magnet on informational query.

### 9. Offer/Lead Magnet Selector
Maps offer type to intent + persona: pricing PDF for BOFU B2B, coupon for ecommerce.

**Veto if:** Wrong offer type for intent, no offer for MOFU/TOFU traffic.

### 10. Trust Signal Orchestrator
Manages persona-weighted placement of logos, testimonials, certifications, guarantees.

**Veto if:** No trust signals above fold BOFU, outdated proof, trust density insufficient for high-ticket.

### 11. Conversion Readiness Scorecard
Computes 16 scores (0-100 each): Intent Fit, Scent, Trust, UX Friction, Accessibility, Offer Fit, LLM Optimisation, Affiliate Performance, Momentum Flow, Objection Coverage, Urgency Integrity, Exit-Rescue, Revenue Expansion, Multi-Device, CRM Tagging, Zero-Friction.

**Veto thresholds:** See config - typically 75-100 per score.

### 12. Schema-by-Intent Enforcer
Validates structured data: Product/Service, FAQ, Review, LocalBusiness, HowTo, ItemList, Breadcrumb.

**Veto if:** Missing required schema for intent class.

### 13. Calculator/Quote Trigger
Detects pricing intent ("cost", "price", "calculator"), enforces working estimator.

**Veto if:** Pricing intent without calculator/quote form, or non-functional.

### 14. Language/Locale & Variants Guard
Enforces jurisdiction-specific: spelling (US/UK/AU/CA), currency, units, date/phone formats.

**Veto if:** Wrong spelling variant, wrong currency, wrong measurement units, generic examples.

### 15. Cannibalisation & Routing Check
Detects multiple pages targeting same intent/keyword, suggests consolidation.

**Veto if:** New page duplicates existing page intent without clear differentiation.

---

## COMPLIANCE & TRACKING (16-17)

### 16. Compliance & Claims Gate
Jurisdiction-aware enforcement:
- **US (FTC):** Material connection disclosure, testimonials reflect typical results, health claims substantiated, up to $43,792 per violation
- **Australia (ACL):** Testimonials genuine/verifiable, "results not typical" required, up to $1.1M fines
- **UK (ASA):** Claims substantiated pre-publication, comparative claims need proof
- **EU (GDPR):** Privacy policy required, right to be forgotten, environmental claims substantiated
- **Canada:** Performance claims need testing, "regular price" must be genuine

**Veto if:** Superlative without proof, fake testimonials, medical claims without disclaimers, missing compliance for jurisdiction.

### 17. KPI Instrumentation Hooks
Asserts events: view_item, generate_lead, begin_checkout, phone_click, scroll_depth, form_error.

**Veto if:** Missing required events, phone not clickable (tel: link), UTM parameters malformed.

---

## ADVANCED CONVERSION (18-21)

### 18. Golden Path & Fallback CTA
Primary CTA + friction-reduced fallback (phone, chat, "email me pricing", WhatsApp).

**Veto if:** Only one CTA, fallback not truly reduced friction, no low-commitment option TOFU/MOFU.

### 19. Automated UX & Accessibility Scans
Scans forms/CTAs for: touch targets (44-48px), contrast (WCAG AAA for elderly), labels, mobile responsiveness.

**Veto if:** Touch targets <44px (elderly demographic), contrast below WCAG AAA, form missing labels, mobile broken.

### 20. AI-Powered Content Personalisation
Proposes segment-specific adjustments: headline variations for elderly vs B2B, CTA rotation for new vs repeat.

**Veto if:** No personalisation strategy for multi-persona pages, single message for conflicting personas.

### 21. Intent-Driven A/B Testing Protocol
Mandatory split-testing: headline, CTA button, trust elements per intent.

**Veto if:** No testing plan for new high-value pages, can't measure results.

---

## LLM/AI SEARCH (22)

### 22. LLM/Conversational Search Intent
Optimizes for ChatGPT, Claude, Perplexity, SearchGPT, Google SGE, voice assistants.

**Components:**
- Conversational Intent Classifier (question type, user stage, pain level)
- Answer Completeness Validator (primary + all sub-questions answered)
- Context Awareness Checker (acknowledges user's situation)
- Follow-up Question Anticipator (pre-answers obvious next questions)
- Citation/Source Optimisation (complete sentences for LLM extraction)
- Conversational Tone Matcher (matches tone to query emotion)
- Multi-Modal Answer Structure (voice, visual AI, code extraction)
- Natural Language Query Mapping (tracks queries to content sections)
- AI Search Behaviour Adaptation (platform-specific preferences)

**Veto if:** Primary question answered <150 words (too shallow), obvious sub-questions not addressed, key facts in bullet fragments LLMs can't extract.

---

## AFFILIATE CONTENT (23)

### 23. Affiliate Offer Intent Matching

**A. Offer-Intent Alignment:** Recommended product genuinely solves stated problem, budget appropriate, commission vs quality resolved in user's favor.

**B. Recommendation Credibility:** Clear methodology, specific testing details, cons disclosed, update dates visible.

**C. Affiliate Disclosure Compliance (Multi-Jurisdiction):**
- **US (FTC):** "We earn from qualifying purchases" - clear & conspicuous, $43,792 per violation
- **Australia (ACL):** Plain English before links, $1.1M fines
- **UK (ASA):** "#ad" or "Advertisement" labels
- **EU:** "Advertising" or "Sponsored" required
- **Canada:** Material connection per recommendation

**D. Comparison Fairness:** Objective criteria, all relevant products, better non-affiliate options included.

**E. Multi-Merchant Conversion:** Multiple retailers, price comparison, in-stock status.

**F. Trust Architecture:** Editorial independence, expert credentials, testing transparency.

**Veto if:** Product doesn't meet requirements, budget ignored, no disclosure, disclosure non-compliant, comparison biased.

---

## CONVERSION ENGINEERING (24-34)

### 24. Conversion Momentum Sequencing
Enforces micro-commitments: quiz → results → email → consultation (not giant leap).

**Impact:** +35-60% conversion.
**Veto if:** Jumps straight to hard conversion, no micro-options, dead ends.

### 25. Intent-Matched Objection Handling
Pre-answers objections at decision points:
- BOFU pricing: "Why this price?" below price
- Local: "What if not in my area?" above service map
- Elderly: "Is this safe/easy?" near CTA
- B2B: "What's ROI?" before pricing

**Impact:** +20-35% completion.
**Veto if:** Obvious objections not addressed, objections buried.

### 26. Post-Search Proof Density Guard

**Zone-based minimums:**
- Hero: 1 trust signal above fold
- Mid-page: 2-3 proof elements
- CTA zone: 2 within 300px (3-4 for high-ticket)

**CRITICAL - FAKE TESTIMONIAL DETECTION (ZERO TOLERANCE):**

**✅ Required:**
- Real people: Full name, city, photo with permission
- Verifiable: Can provide proof if challenged
- Current: Within 18 months or marked [year]
- Disclosure: If paid/incentivized, must disclose

**❌ INSTANT VETO:**
- Stock photos
- AI-generated reviews
- Generic names ("John S.")
- Unverifiable claims
- Exceptional results without disclaimer

**Consequences:** FTC $43,792 per fake, ACL $1.1M, reputation destroyed.

**Impact:** +15-40% lift.
**Veto if:** Zero proof above fold, **ANY fake testimonials = INSTANT VETO**.

### 27. Ethical Urgency & Scarcity Automation

**✅ Allowed:** Real inventory, actual calendar, genuine promos, true batch limits.

**❌ Blocked (INSTANT VETO):** Countdown resets, "Only X left" with infinite stock, fake counters, manufactured urgency.

**Impact:** +30-80% conversion.
**Veto if:** ANY fake scarcity = INSTANT VETO.

### 28. Lead-Rescue Automation
Exit intent + idle triggers with intent-matched offers.

**Impact:** +20-50% additional capture.
**Veto if:** No exit capture, intrusive, triggers repeatedly.

### 29. Revenue Expansion Layer
Upsells/cross-sells at decision point.

**Impact:** +15-40% AOV.
**Veto if:** No expansion options, poorly positioned, forced bundles.

### 30. Multi-Device CTA Continuity
Hand-offs: Mobile→Desktop, Desktop→Mobile, cross-session.

**Impact:** +20-35% from multi-device users.
**Veto if:** No hand-off, cart doesn't persist.

### 31. Search-Intent CRM Tagging
Tags leads: intent_type, funnel_stage, query, device, engagement.

**Impact:** +25-60% email→sale conversion.
**Veto if:** Leads without intent tags, follow-up not differentiated.

### 32. Zero-Friction Conversion Paths
Express checkout, guest checkout, pre-filled forms, social login, max 5 fields.

**Impact:** -30-50% abandonment, +40-60% mobile conversion.
**Veto if:** No express checkout, account required, >5 required fields.

### 33. Exit Intent Precision Rescue
Behavior-specific (not generic): viewed pricing → discount, used calculator → save results.

**Impact:** 20-40% of abandoning visitors captured.
**Veto if:** Generic popup, triggers <10 seconds, covers content.

### 34. Live Engagement & AI Agent
Real-time assistance at high-value moments: pricing, comparison, checkout.

**Impact:** +20-35% for high-ticket/B2B.
**Veto if:** No live option for high-ticket (>$2,000), chat missing on pricing.

---

# 16-PART CONVERSION READINESS SCORECARD

All scores 0-100:

1. **Intent Fit** (< 85 = veto) - H1/intro/body/CTA alignment
2. **Scent** (< 80 = veto) - Ad↔landing parity
3. **Trust/E-E-A-T** (< 70 = veto BOFU) - Proof variety/recency
4. **UX Friction** (< 75 = veto) - Form fields, mobile, load
5. **Accessibility** (< 80 = veto elderly) - Contrast, labels
6. **Offer Fit** (< 75 = veto) - Lead magnet appropriate
7. **LLM Optimisation** (< 75 = veto conversational) - Answer completeness
8. **Affiliate Performance** (< 75 = veto affiliate) - Credibility, disclosure
9. **Momentum Flow** (< 85 = veto) - Micro-commitments present
10. **Objection Coverage** (< 80 = veto) - Top 3 objections addressed
11. **Urgency Integrity** (100 required) - NO fake scarcity
12. **Exit-Rescue** (< 75 = veto) - Exit capture present
13. **Revenue Expansion** (< 70 = veto) - Upsell opportunities
14. **Multi-Device Continuity** (< 75 = veto) - Hand-offs exist
15. **CRM Intent-Tagging** (100 required) - All leads tagged
16. **Zero-Friction** (< 75 = veto) - Express checkout, min fields

---

# CONFIG FILE SCHEMA

Create `.claude-project-config.json` in project root:

```json
{
  "project_name": "Your Project",
  "jurisdiction": {
    "primary_country": "AU",
    "compliance_frameworks": ["ACL"],
    "language_locale": "en-AU",
    "currency": "AUD",
    "measurement_units": "metric"
  },
  "target_demographics": {
    "age": "65-85",
    "income": "middle to upper middle",
    "disabilities": "mobility impaired",
    "location": "Australia"
  },
  "psychographics": {
    "pain_points": ["loss of independence", "fear of falls"],
    "desires": ["maintain dignity", "stay active"],
    "buying_triggers": ["doctor recommendation"]
  },
  "conversion_goals": {
    "primary": "phone_enquiries",
    "secondary": ["email_leads"]
  },
  "intent_rules": {
    "classes": ["transactional", "commercial", "informational", "local"],
    "required_modules": {
      "transactional": ["price_block", "primary_cta", "trust_cluster"]
    },
    "schema_required": {
      "transactional": ["Product", "FAQ"]
    }
  },
  "offer_library": [
    {"id": "buyers_guide", "fits": ["informational"], "goal": "email"}
  ],
  "kpi_assertions": {
    "required_events": ["generate_lead", "phone_click"],
    "utm_policy": "required"
  },
  "psychological_triggers": {
    "elderly": ["safety", "independence", "dignity"]
  },
  "conversion_optimization": {
    "momentum_sequencing": {"enabled": true},
    "urgency_rules": {"fake_scarcity_blocked": true},
    "exit_rescue": {"enabled": true},
    "zero_friction": {"express_checkout_required": true}
  },
  "veto_thresholds": {
    "intent_fit": 85,
    "urgency_integrity": 100,
    "crm_intent_tagging": 100
  }
}
```

---

# USAGE

## Activation
PM orchestrator directs agent when verification needed:
```
Create landing page for "buy mobility scooter Brisbane"
then verify with content-intent-agent skill
```

Agent:
1. Reads `.claude-project-config.json` from project root
2. Evaluates content against all 34 modules
3. Computes 16-part scorecard
4. Returns APPROVED or VETO with detailed feedback

## Feedback Format
```
VETO - Critical issues prevent shipping

Intent Fit: 72 (threshold 85) ❌
Momentum Flow: 68 (threshold 85) ❌

CRITICAL ISSUES:

1. Line 12, H1: Missing transactional intent modifiers
   Why: Informational framing on BOFU query depresses conversion 50-70%
   Fix: Change to "Buy Kymco Mini Comfort - Price & Free Delivery"
   
2. Module 26: Stock photo testimonial detected
   Why: FTC violation $43,792, destroys trust
   Fix: Remove stock photo, use real customer with signed release
```

---

# EXPECTED RESULTS

With all 34 modules:
- Overall conversion: **+60-120%**
- Lead capture: **+50-80%**
- Phone calls: **+40-60%**
- AOV: **+15-40%**
- Mobile conversion: **+40-60%**
- Email→sale: **+25-60%**
- CPA: **-30-50%**

---

# CRITICAL COMPLIANCE

**ZERO TOLERANCE:**
1. Fake testimonials (stock photos, AI, unverifiable) = FTC $43,792 per, ACL $1.1M
2. Fake scarcity (countdown resets, false "only X left") = Regulatory violations
3. Deceptive claims (superlatives without proof) = Fines + reputation damage

---

# VERSION

v1.3.0 - Complete with 34 modules + 16-part scoring

---

# SUMMARY

Complete conversion optimization system verifying content against 34 criteria to ensure maximum sales, leads, and list growth.

**Key principles:**
1. User intent first
2. Conversion engineering
3. Ethical compliance (zero fake tactics)
4. Multi-platform (traditional + AI search)
5. Data-driven (16-part scorecard)

Every visitor has a job to be done. This skill ensures content helps them do that job while achieving business goals.
