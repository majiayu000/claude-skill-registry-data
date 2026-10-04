---
name: pitch-deck
description: "Creates professional investor or client pitch decks in Canva from a conversational brief about the business, product, or service. Use when a user needs a presentation for fundraising, client proposals, partnership pitches, or keynote talks."
allowed-tools: Read Write Glob mcp__claude_ai_Canva__generate-design-structured mcp__claude_ai_Canva__request-outline-review mcp__claude_ai_Canva__get-design mcp__claude_ai_Canva__get-design-content mcp__claude_ai_Canva__start-editing-transaction mcp__claude_ai_Canva__perform-editing-operations mcp__claude_ai_Canva__commit-editing-transaction mcp__claude_ai_Canva__cancel-editing-transaction mcp__claude_ai_Canva__export-design mcp__claude_ai_Canva__get-export-formats mcp__claude_ai_Canva__list-brand-kits mcp__claude_ai_Canva__get-design-thumbnail
metadata:
  author: matthewhitcham
  version: "1.0"
---

# Pitch Deck

## When to Use This Skill

Use this skill when the user needs:
- An investor pitch deck for a fundraising round (pre-seed through Series B)
- A client proposal deck to win new business or contracts
- A partnership pitch to secure strategic alliances or sponsorships
- A keynote or demo day presentation for startup events
- A sales deck for high-value prospects

**DO NOT** use this skill for:
- Internal team presentations (use a general slide builder)
- Educational or training decks (different structure entirely)
- One-page pitch summaries (those are documents, not decks)

## How It Works

EVERY SLIDE MUST COMMUNICATE ONE IDEA IN UNDER 30 WORDS OF BODY TEXT — IF YOU CANNOT SAY IT IN 30 WORDS, SPLIT IT INTO TWO SLIDES.

---

### Phase 1: Extract Pitch Elements

Gather the six core pitch elements through conversation. Ask the user directly — do not assume or fabricate any business details.

1. **Ask for the business brief** — request a 2-3 sentence description of what the business does, or accept a file/URL the user provides
2. **Extract these six elements** from the conversation:

| Element | What to Capture | Required? |
|---------|----------------|-----------|
| **Problem** | Who suffers, what the pain is, why existing solutions fail | Yes |
| **Solution** | What the product/service does, core value proposition | Yes |
| **Market Size** | TAM/SAM/SOM or target audience size | Yes |
| **Traction** | Revenue, users, growth rate, key milestones, testimonials | If available |
| **Team** | Founders, relevant experience, advisors | If available |
| **The Ask** | Funding amount, deal terms, partnership scope, or next steps | Yes |

3. **Identify the deck type** based on context:
   - **Investor deck** — emphasize market size, traction, financials, and funding ask
   - **Client deck** — emphasize problem/solution fit, case studies, pricing, and next steps
   - **Partnership deck** — emphasize mutual benefit, audience overlap, and proposed terms

4. **Present the extraction summary** to the user before proceeding:

```
## Pitch Elements

**Deck type:** Investor pitch
**Problem:** [extracted problem statement]
**Solution:** [extracted solution]
**Market:** [TAM/SAM/SOM or audience size]
**Traction:** [key metrics or "early stage — focusing on vision"]
**Team:** [founders and relevant background]
**The Ask:** [specific amount or action requested]

Ready to build the slide outline? (yes / adjust)
```

**GATE: Do not proceed to Phase 2 until the user confirms the extraction is accurate.**

---

### Phase 2: Build Slide Outline

Construct a 10-12 slide outline using the standard pitch deck structure. Each slide gets a title and 1-3 bullet points summarizing the content.

1. **Map elements to slides** using this default structure:

| Slide # | Title | Content Guidance | Max Words |
|---------|-------|-----------------|-----------|
| 1 | Title Slide | Company name, one-line tagline, presenter name, date | 15 |
| 2 | The Problem | Pain point in concrete terms. Use a stat or story. | 30 |
| 3 | The Solution | What you built and why it works. Lead with the outcome. | 30 |
| 4 | How It Works | 3-step process or product screenshot description. Visual-first. | 25 |
| 5 | Market Opportunity | TAM/SAM/SOM with sources. One chart description. | 25 |
| 6 | Business Model | How you make money. Pricing tiers or revenue streams. | 25 |
| 7 | Traction | Key metrics: revenue, users, growth %. Use numbers, not words. | 20 |
| 8 | Competition | 2x2 matrix or comparison table. Show your unique position. | 25 |
| 9 | The Team | Founder photos, names, one-line bios. 2-4 people max. | 30 |
| 10 | Financials | Revenue projections, unit economics, or key financial metrics. | 25 |
| 11 | The Ask | Specific amount, use of funds breakdown, timeline. | 25 |
| 12 | Contact | Name, email, website, social links. Clean and simple. | 15 |

2. **Adapt for deck type:**
   - **Client deck:** Replace slides 5, 7, 10 with Case Study, Testimonials, Pricing
   - **Partnership deck:** Replace slides 7, 10, 11 with Audience Overlap, Proposed Terms, Mutual Benefits

3. **Submit the outline for review** using the Canva outline review widget:
   - Call `mcp__claude_ai_Canva__request-outline-review` with the slide titles and bullet points
   - Present the interactive review widget to the user
   - Wait for the user to approve or edit the outline through the widget

4. **Apply any changes** the user makes in the review widget before proceeding

**GATE: Do not proceed to Phase 3 until the outline is approved through the review widget.**

---

### Phase 3: Generate the Presentation

Create the actual presentation in Canva using the approved outline.

1. **Check for brand kit** — call `mcp__claude_ai_Canva__list-brand-kits`. If a kit exists, note the ID. If not, use Canva's default professional styling.

2. **Generate the deck** — call `mcp__claude_ai_Canva__generate-design-structured` with the approved outline, design type "presentation", brand kit ID (if available), and a clean professional style direction.

3. **Retrieve and preview** — call `mcp__claude_ai_Canva__get-design` to confirm creation, then `mcp__claude_ai_Canva__get-design-thumbnail` to share a preview link.

4. **Present the result** with the design link, thumbnail, slide count, and brand kit status. Ask if the user wants refinements or is ready to export.

**GATE: Wait for user feedback before entering Phase 4. If the user is satisfied, skip to Phase 5.**

---

### Phase 4: Refine the Presentation

Use Canva's editing transactions to make targeted changes.

1. **Get current content** — call `mcp__claude_ai_Canva__get-design-content` to see text and elements on each slide
2. **Start transaction** — call `mcp__claude_ai_Canva__start-editing-transaction` with the design ID
3. **Apply edits** — call `mcp__claude_ai_Canva__perform-editing-operations` for text changes, repositioning, or content swaps
4. **Commit or cancel** — call `commit-editing-transaction` if correct, or `cancel-editing-transaction` and start fresh if something broke
5. **Show updated thumbnail** — call `get-design-thumbnail` so the user can verify

**IMPORTANT:** Make all related edits within a single transaction. Do not open multiple transactions for one round of feedback.

Repeat Phase 4 for each round of user feedback. **If 3 refinement rounds do not resolve the issue, stop and reassess** — the problem may require manual editing in Canva's UI.

---

### Phase 5: Export the Deck

Export the final presentation in both PPTX and PDF formats.

1. **Check formats** — call `mcp__claude_ai_Canva__get-export-formats` to confirm PPTX and PDF availability
2. **Export PPTX** — call `mcp__claude_ai_Canva__export-design` with format `pptx` (for PowerPoint, Google Slides, Keynote)
3. **Export PDF** — call `mcp__claude_ai_Canva__export-design` with format `pdf` (for email attachments, investor portals, DocSend)
4. **Deliver both download links** and remind the user the deck is saved in their Canva account for future editing

---

## Slide-by-Slide Content Guide

Every slide follows the same rule: **one idea, visual-first, minimal text.**

| Slide | Key Rule | Example |
|-------|----------|---------|
| **1. Title** | Company name large, tagline in one line, presenter + date small at bottom | "AutoInvoice — Smart invoicing for the modern freelancer" |
| **2. Problem** | Lead with pain. One stat or one-sentence story. Frame as audience's problem. | "67% of freelancers spend 10+ hours/week on invoicing instead of billable work" |
| **3. Solution** | One sentence + three benefit bullets (not features) | "AutoInvoice sends, tracks, and collects payment automatically" |
| **4. How It Works** | Three numbered steps, 5-8 words each. Visual-first. | "1. Connect your bank. 2. Set your rates. 3. Invoices send automatically." |
| **5. Market** | TAM/SAM/SOM stacked largest to smallest. Cite sources. One visual. | "TAM: $12B. SAM: $3.2B. SOM: $180M." |
| **6. Business Model** | Model in one line. 2-3 pricing tiers. One unit economic metric. | "SaaS: $19/mo starter, $49/mo pro, $99/mo agency" |
| **7. Traction** | Numbers only, large font. If pre-revenue: waitlist, LOIs, pilots. | "$15K MRR / 2K users / 20% MoM growth" |
| **8. Competition** | 2x2 quadrant, you in top-right. 3-5 named competitors. No bashing. | Axes: "Easy to Use" vs "AI-Powered" |
| **9. Team** | 2-4 people max. Photo, name, title, one credential each. | "Sarah Chen, CEO — Ex-Stripe, 10 years in fintech" |
| **10. Financials** | 3-year projections or run rate. Simple bar chart. Key assumptions small. | "Path to $2M ARR in 18 months" |
| **11. The Ask** | Exact amount. Use-of-funds breakdown (3-4 categories as %). Timeline. | "$1.5M seed. 40% product, 30% growth, 20% team, 10% ops" |
| **12. Contact** | Name, email, website, social. One closing line. No clutter. | "Let's build the future of freelance finance" |

---

## Example 1: SaaS Startup Investor Pitch

**User says:** "I need an investor pitch deck for my SaaS startup. We built an AI-powered invoicing tool for freelancers called AutoInvoice. We have 2,000 users, $15K MRR, growing 20% month-over-month. Raising a $1.5M seed round."

**Phase 1 extraction presented to user:**
```
**Deck type:** Investor pitch
**Problem:** Freelancers lose 10+ hours/week on manual invoicing and chasing payments
**Solution:** AutoInvoice — AI-powered invoicing that auto-generates, sends, and tracks invoices
**Market:** $12B global invoicing market, $3.2B US freelancer segment
**Traction:** 2,000 users, $15K MRR, 20% MoM growth, 94% retention
**Team:** 2 co-founders — former Stripe engineer and QuickBooks product lead
**The Ask:** $1.5M seed round — 40% product, 30% growth, 20% team, 10% ops
```

**Phase 2 outline submitted to review widget:**
1. AutoInvoice — Smart invoicing for the modern freelancer
2. The Problem — Freelancers spend 520 hours/year on invoicing
3. The Solution — AI that turns bank activity into paid invoices
4. How It Works — Connect, configure, get paid in 3 steps
5. Market Opportunity — $12B TAM, $3.2B SAM, $180M SOM
6. Business Model — SaaS: $19/mo starter, $49/mo pro, $99/mo agency
7. Traction — 2K users, $15K MRR, 20% MoM growth
8. Competition — Faster than FreshBooks, simpler than QuickBooks, smarter than Wave
9. The Team — Stripe + QuickBooks DNA
10. Financials — Path to $2M ARR in 18 months
11. The Ask — $1.5M to capture the solo professional market
12. Get in Touch — founders@autoinvoice.com

**Phase 3-5:** Deck generated with brand kit. Exported as PPTX + PDF. 12 slides, ready for investor meetings.

---

## Example 2: Freelance Consultant Client Pitch

**User says:** "I'm a brand strategy consultant and I need a pitch deck for a potential client — a D2C skincare startup that wants to rebrand. I want to show them my process and pricing."

**Phase 1 extraction presented to user:**
```
**Deck type:** Client pitch
**Problem:** D2C skincare brands struggle to differentiate — generic branding leads to low recall and high CAC
**Solution:** Full-service brand strategy — positioning, visual identity, messaging, launch playbook
**Traction:** 12 brand projects completed, 3 in skincare, average 35% improvement in brand recall
**Team:** Solo consultant — 8 years at Pentagram + Collins, 3 years independent
**The Ask:** $25,000 engagement over 8 weeks (audit, strategy, delivery)
```

**Phase 2 outline (adapted for client deck):**
1. Brand Strategy for [Client Name] — by [Consultant Name]
2. The Challenge — Standing out in a sea of sameness
3. My Approach — Positioning-first brand strategy
4. How We Work Together — Audit, Strategy, Delivery (8 weeks)
5. Case Study — GlowLab: 42% increase in brand recall
6. Case Study — BeautyStack: 28% lower CAC after rebrand
7. Testimonials — What clients say
8. The Deliverables — What you get at the end of 8 weeks
9. About Me — 8 years at Pentagram + Collins, 3 years independent
10. Investment — $25,000 for the full engagement
11. Next Steps — Sign by Friday, kick off Monday
12. Contact — email, portfolio, LinkedIn

**Phase 3-5:** Deck generated with professional default styling. Exported as PPTX + PDF. 12 slides, ready to send to the prospect.

---

## Anti-Patterns

- **DO NOT** put more than 30 words of body text on any slide — pitch decks are visual, not documents
- **DO NOT** exceed 12 slides — investors and clients lose attention after slide 10; every slide beyond 12 must justify its existence
- **DO NOT** skip the Ask slide — the entire deck builds to this moment; leaving it out wastes the audience's time
- **DO NOT** use generic stock imagery descriptions — every visual element should reinforce the specific business story
- **DO NOT** cram financial projections into a wall of numbers — pick 3-4 key metrics and make them large
- **DO NOT** list features instead of benefits on the Solution slide — investors buy outcomes, not feature lists
- **DO NOT** include more than 4 team members — highlight founders and key hires only
- **DO NOT** present multiple pricing options on the Ask slide for investor decks — state one clear number and the use of funds

---

## Recovery

**Design generation fails:** Retry once with the same parameters. If it fails again, simplify to 10 slides (drop Competition and Financials) and retry. If 3 attempts fail, stop and reassess — offer to write slide content as a markdown file for manual import.

**Outline review widget does not load:** Present the outline as a numbered list in chat. Ask the user to approve or edit via text. Proceed with the text-confirmed outline.

**Editing transaction fails to commit:** Call `cancel-editing-transaction` to clean up. Start a fresh transaction and re-apply. If 3 transactions fail on the same edit, skip it and note it for the user to fix in Canva.

**Export fails:** Call `get-export-formats` to check available formats. If PPTX is unavailable, export PDF only. If both fail, provide the Canva design link for manual export.

**No brand kit found:** Proceed with Canva's default professional styling. Inform the user they can apply their brand kit later in Canva's editor.

**Brief is too vague:** Ask three questions: (1) Who is your target customer? (2) What do they pay you for? (3) What should the audience do after this deck? Do not proceed until Problem, Solution, and Ask are clear.
