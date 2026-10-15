---
name: market-landing
description: Landing page CRO analysis with section-by-section teardown and prioritized actionable conversion fixes.
---

# Landing Page CRO Analysis

## Skill Purpose

Perform a comprehensive Conversion Rate Optimization (CRO) analysis on any landing page. This skill produces a section-by-section teardown with prioritized, actionable fixes that directly impact conversion rates.

## When to Use

- User provides a landing page URL and asks for conversion optimization.
- User asks for landing page feedback, review, or audit.
- User wants to improve signup, lead capture, or purchase rates.
- Triggered by `/market landing <url>` or `/market cro <url>`.

## Reference map

| When | Read |
|---|---|
| Running the 7-section CRO framework (Step 2 — per-section checklists, scoring criteria, supporting models like 4U, social-proof ranking, objection table, CTA copy tiers) | [`references/cro-framework.md`](references/cro-framework.md) |
| Running form / mobile / page-speed audits (Steps 4–6 — full checklists + page-speed benchmark table) | [`references/audits.md`](references/audits.md) |
| Generating A/B test recommendations + heat-map interpretation (Steps 7–8 — 10 example tests, F vs Z pattern, rage-click zones) | [`references/testing-and-heatmaps.md`](references/testing-and-heatmaps.md) |

## Compliance, claims, and CRO-honesty constraints

These rules apply to every recommendation generated.

- **No fabricated proof.** Recommendations like "add testimonials" must specify real testimonials only. No invented customer names, results, statistics, awards, logos, or media mentions.
- **No fake urgency or scarcity.** "Only 3 spots left", "Sale ends midnight", "247 people viewing now" must be true. Faked urgency violates FTC guidance and damages trust.
- **No deceptive comparisons** with named competitors without verifiable evidence.
- **Substantiate quantified claims.** "Cut reporting time by 75%" must reference a real source or be marked as placeholder.
- **Risk reversal must be honest.** "Money-back guarantee", "Cancel anytime", "Free trial" — only recommend if the user actually offers these terms.
- **CTA promises must match destination.** "Start My Free Trial" must lead to a free trial, not a paywall. Flag any ad-to-page mismatch.
- **Accessibility is non-negotiable.** Recommendations must preserve WCAG 2.2 AA — color contrast for CTA buttons (≥4.5:1 for text, ≥3:1 for large text), text size (≥16px body), keyboard navigation, alt text, focus indicators.
- **Privacy compliance.** Form recommendations must respect GDPR / CCPA — explicit opt-in for marketing, no pre-checked boxes, link to privacy policy near the form.
- **No dark patterns.** Hidden costs revealed only at checkout, confusing opt-outs, manipulative "Yes" / "No, I don't want savings" wording, forced continuity — banned by FTC and damaging long-term.
- **Conversion-impact estimates are ranges, not promises.** "Typically lifts 15–30%" beats "Will increase by 22%". Past benchmarks ≠ guaranteed future results.
- **Mobile-first.** 60%+ of web traffic is mobile. Don't recommend desktop-only patterns. Test recommendations against the mobile checklist in `references/audits.md`.

---

## How to Execute

### Step 1: Identify the page type

Determines benchmark expectations and scoring weights.

| Page Type | Primary Goal | Good CR | Great CR |
|---|---|---|---|
| **Lead Capture** | Email / form submission | 5–10% | 15%+ |
| **SaaS Signup** | Free trial or freemium signup | 3–7% | 10%+ |
| **E-commerce Product** | Add to cart / Purchase | 2–4% | 5%+ |
| **Webinar Registration** | Register for event | 20–30% | 40%+ |
| **App Download** | Install app | 10–15% | 20%+ |
| **Waitlist** | Join waitlist | 15–25% | 35%+ |
| **Consultation Booking** | Schedule a call | 5–10% | 15%+ |
| **Nonprofit Donation** | Make a donation | 2–5% | 8%+ |

### Step 2: Run the 7-point CRO framework

Score each section 1–10. Weighted total = overall CRO score (out of 100).

| # | Section | Weight | Score thresholds |
|---|---------|-------:|------------------|
| 1 | **Hero Section** | 25% | 9–10 benefit-driven + clear CTA + supporting visual + trust signals; 1–2 no clear headline or CTA |
| 2 | **Value Proposition** | 20% | Useful / Urgent / Unique / Ultra-specific (4U) |
| 3 | **Social Proof** | 15% | ≥2 types, named testimonials w/ photos, specific (not rounded) numbers |
| 4 | **Features and Benefits** | 15% | Feature → benefit translated; scannable; 3–7 key features |
| 5 | **Objection Handling** | 10% | FAQ for top 3–5 objections; risk reversals; pricing transparency |
| 6 | **Call-to-Action** | 10% | Value-not-action copy; visually dominant; first-person; specific |
| 7 | **Footer + Secondary Elements** | 5% | Final CTA repeated; legal links; no competing links |

Full per-section checklists, scoring rubrics (1–10 criteria), 4U framework, social-proof ranking by persuasion power, common-objections table, CTA copy tiers (Weak / Medium / Strong): [`references/cro-framework.md`](references/cro-framework.md).

### Step 3: Copy scoring

Score the overall page copy on 5 dimensions (1–10 each):

1. **Clarity** — visitor understands the offer in 5 seconds?
2. **Urgency** — reason to act NOW vs later?
3. **Specificity** — concrete numbers, timeframes, outcomes?
4. **Proof** — claims backed by evidence, data, or testimonials?
5. **Action Orientation** — copy drives toward a specific next step?

**Copy Score = average × 10** (0–100 scale).

### Step 4: Form optimization audit

If the page has a form, audit field count (every additional field reduces conversion ~7%; 3–5 fields max for lead capture), labels (inline / floating, not placeholder-only), button text (match value prop), error handling (inline validation, don't clear on error), multi-step with progress indicator, mark optional fields not required, browser auto-fill, mobile-appropriate field types. Full audit checklist: [`references/audits.md`](references/audits.md#form-optimization).

### Step 5: Mobile responsiveness audit

Mobile is 60%+ of traffic. Check thumb-reachable CTA, 16px minimum body text, large tap targets, image resize, no horizontal scroll, <3s load on 4G, click-to-call phone numbers, sticky CTA bar on scroll. Full checklist: [`references/audits.md`](references/audits.md#mobile-responsiveness).

### Step 6: Page-speed impact assessment

| Load Time | Conversion Impact |
|---|---|
| 0–2 s | Baseline (optimal) |
| 2–3 s | −7% conversion rate |
| 3–5 s | −20% |
| 5–8 s | −35% |
| 8+ s | −50%+ |

Common issues: unoptimized images (use WebP + lazy loading), render-blocking JS, missing browser caching, no CDN, excessive third-party scripts, unminified CSS/JS. Full diagnostic list: [`references/audits.md`](references/audits.md#page-speed).

### Step 7: A/B test recommendations

Format every test as a hypothesis: **"If we [CHANGE], then [METRIC] will [IMPROVE / INCREASE] because [REASON]."**

10 example tests to consider (headline variants, CTA color + text, social proof placement, form field reduction, hero image vs video, long vs short page, urgency elements, price anchoring, testimonial format, chat widget): [`references/testing-and-heatmaps.md`](references/testing-and-heatmaps.md#ab-tests).

### Step 8: Heat-map interpretation

Even without actual heat-map data, provide guidance on expected attention zones, F-pattern vs Z-pattern reading, scroll-depth predictions, click-probability zones, rage-click indicators (elements that look clickable but aren't), dead zones. Full guidance: [`references/testing-and-heatmaps.md`](references/testing-and-heatmaps.md#heat-maps).

---

## Output Format

Generate a file called `LANDING-CRO.md` in the project root or output directory:

```markdown
# Landing Page CRO Analysis
## [Page URL]
### Analysis Date: [date]

---

## Overall CRO Score: [X/100]

## Page Type: [identified type]
## Current Estimated Conversion Rate: [estimate based on findings]
## Target Conversion Rate: [realistic improvement target]

---

## Section-by-Section Analysis

### 1. Hero Section [Score: X/10]
**Findings:**
- [specific observations]

**Fixes (Priority: HIGH/MEDIUM/LOW):**
- [specific, actionable recommendations]

[Repeat for all 7 sections]

---

## Copy Score: [X/100]
| Dimension | Score | Notes |
|---|---|---|
| Clarity | X/10 | [notes] |
| Urgency | X/10 | [notes] |
| Specificity | X/10 | [notes] |
| Proof | X/10 | [notes] |
| Action Orientation | X/10 | [notes] |

---

## Form Audit
[findings and recommendations]

---

## Mobile Audit
[findings and recommendations]

---

## A/B Test Recommendations
1. [Hypothesis format test]
2. [Hypothesis format test]
3. [Hypothesis format test]

---

## Prioritized Fix List

### Quick Wins (implement this week)
1. [fix with expected impact]

### Medium-Term (implement this month)
1. [fix with expected impact]

### Strategic (implement this quarter)
1. [fix with expected impact]

---

## Before/After Wireframe Suggestions
[Text-based wireframe descriptions of current vs recommended layout]
```

---

## Key Principles

- **Tie every recommendation to revenue impact.** Don't just say "change the button color" — say "changing the CTA button to a contrasting color typically increases clicks 15–30%, which at your current traffic could mean X more conversions per month".
- **Prioritize by effort-to-impact ratio.** Quick wins first.
- **Be specific.** "Improve your headline" is useless. "Change your headline from 'Welcome to Our Platform' to 'Cut Your Reporting Time by 75% — Automated Analytics for Growth Teams' because it adds specificity, a quantified benefit, and targets a specific audience" is actionable.
- **Reference industry benchmarks** so the client understands where they stand.
- **If you can access the page via browser tools, take screenshots** and reference specific elements.
- **If the user has run `/market audit` previously, incorporate those findings** into the CRO analysis.
