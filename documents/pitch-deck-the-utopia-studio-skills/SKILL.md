---
name: pitch-deck
description: "Generate investor-ready pitch decks as branded PPTX files from founder meeting notes, uploaded decks, DD reports, and strategy docs. Use this skill whenever the user mentions building a pitch deck, turning notes into slides, creating an investor deck, preparing for a co-investor presentation, or helping a portfolio company with their deck. Also trigger when the user uploads Granola meeting notes, founder call transcripts, or company materials and asks for a deck, slides, or presentation for investors. Covers co-investor syndication decks and founder coaching decks. Even if the user just says 'build a deck from these notes' or 'make this into a pitch deck' or 'help [company] with their deck', use this skill."
---

# Pitch Deck Skill

Build investor-ready pitch decks from raw materials — meeting notes, uploaded decks, DD reports, and strategy docs — and output as branded PPTX.

This skill is built for The Studio (Utopia Capital). The default audience is co-investors and syndicate partners. When helping portfolio founders build their own decks, adapt the branding and voice accordingly.

---

## Before You Start

1. Read the pptx skill: `view /mnt/skills/public/pptx/SKILL.md` — then read `pptxgenjs.md` for from-scratch creation
2. Read `references/slide-frameworks.md` — Global Context and Growth Flywheel frameworks (the two signature slides)
3. Read `references/slide-best-practices.md` — research-backed guidance for every slide in the deck
4. Read `references/scoring-rubric.md` — the 15-dimension scoring framework (score inputs and outputs)
5. Read `assets/utopia-branding.md` — Studio brand defaults
6. If a DD report exists or is mentioned, read `references/dd-integration.md` for extraction patterns

All reference paths are relative to this skill's directory.

---

## Step 1: Ingest Source Materials

Read and parse everything the user provides. Typical inputs:

- **Granola meeting notes** — founder call transcripts; extract claims, metrics, positioning, and team context
- **Uploaded pitch decks** (PDF/PPTX) — use `markitdown` or the pdf-reading skill to extract content; note what's strong and what's missing
- **Technical DD reports** — if available, pull key findings, risk flags, and technology assessments (see `references/dd-integration.md`)
- **Ad-hoc docs** — strategy briefs, financials, brainstorm notes, Notion exports

From these materials, extract and organize:

| Category | What to find |
|----------|-------------|
| Company basics | Name, stage, what it does, founding date |
| Problem | Pain points, market gaps, why now |
| Solution | Product, differentiators, technical approach |
| Market | TAM/SAM/SOM, growth rates, industry dynamics |
| Traction | Users, revenue, partnerships, milestones |
| Team | Founders, key hires, relevant domain expertise |
| Business model | Revenue streams, pricing, unit economics |
| Financials | Burn rate, runway, projections |
| The ask | Funding amount, use of funds, milestone targets |
| Competitive landscape | Named competitors, positioning, moats |

**If critical data is missing, ask specific questions before generating.** Never fabricate metrics, financials, or traction numbers. Use `[NEEDS INPUT]` placeholders for gaps the user must fill.

### Score the Input Materials

After ingesting all source materials, score them using the 15-dimension framework in `references/scoring-rubric.md`. Present the input scores to the user before generating the deck — this sets expectations about what the source materials support and where research or user input is needed to improve the output.

For any dimension scoring 6 or below, flag it immediately and ask for additional information or approval to research.

---

## Step 2: Research Industry Context

Supplement the user's materials with current market intelligence using web search:

- **Industry trends** — recent developments, growth forecasts, regulatory shifts
- **Competitive landscape** — key competitors, recent rounds, positioning moves
- **Market sizing** — validate or source TAM/SAM/SOM from credible reports
- **Investor sentiment** — what matters to investors in this space right now

Cross-reference any numbers from the source materials against public data. Flag discrepancies for the user rather than silently correcting.

---

## Step 3: Structure the Deck

The standard co-investor deck follows this sequence. Adapt based on what the materials contain — not every company needs every slide, and some need extras.

### Standard Investor Deck (12–15 slides)

| # | Slide | Purpose |
|---|-------|---------|
| 1 | **Title** | Company name, tagline, round context |
| 2 | **Global Context** | Three structural forces — see `references/slide-frameworks.md` |
| 3 | **Problem** | Pain point with data validation |
| 4 | **Solution** | Product overview, key differentiators |
| 5 | **Product** | Features, architecture, demo flow |
| 6 | **Market Opportunity** | TAM/SAM/SOM with cited sources |
| 7 | **Business Model** | Revenue streams, pricing, unit economics |
| 8 | **Traction** | Metrics, growth trajectory, key milestones |
| 9 | **Growth Flywheel** | How the business scales + defensible moats — see `references/slide-frameworks.md` |
| 10 | **Competition** | Positioning matrix, structural advantages |
| 11 | **Go-to-Market** | Channels, partnerships, CAC/LTV dynamics |
| 12 | **Team** | Founders, advisors, key hires, domain credibility |
| 13 | **Financials** | Projections, key assumptions, path to profitability |
| 14 | **The Ask** | Funding amount, use of funds, milestone targets |
| 15 | **Appendix** | Supporting data, references, backup slides |

The **Global Context** (slide 2) and **Growth Flywheel** (slide 9) are the two signature slides that distinguish a Studio deck from a generic pitch. They are non-negotiable for co-investor decks. Read `references/slide-frameworks.md` before generating these.

### Audience Adaptation

- **Co-investor / syndicate** (default) — lead with market thesis, emphasize structural forces, highlight risk-adjusted returns, include DD-backed technical assessment if available
- **Founder coaching** — help the founder tell their story; adapt branding to the portfolio company; focus on what investors in their specific round will care about

---

## Step 4: Generate Slide Content

For each slide, consult `references/slide-best-practices.md` for research-backed guidance on what great looks like, what to avoid, and how investors evaluate that specific slide. Then produce:

- **Headline** — an insight, not a label. "A $47B market growing 23% annually" beats "Market Size"
- **Body content** — 3–5 bullets or a concise paragraph with evidence
- **Visual direction** — what chart, diagram, or layout would strengthen this slide
- **Speaker notes** — 2–3 sentences of talking points

### Content Principles

- Every claim must be backed by data from the source materials or research
- Use specific numbers: "3,200 MAU" not "thousands of users"
- One key message per slide — if it has two, split it
- Write for the audience's priorities (co-investors care about returns and risk; founders care about traction and vision)

### Industry-Specific Emphasis

Adapt language and metrics by sector:

| Sector | Key Metrics |
|--------|------------|
| SaaS | ARR, churn, NRR, CAC payback, LTV/CAC |
| Biotech/Health | Regulatory pathway, clinical milestones, IP |
| Marketplace | GMV, take rate, liquidity, network effects |
| Hardware | BOM cost, manufacturing scale, distribution |
| AI/ML | Model performance, data moats, compute costs |
| Fintech | Regulatory compliance, transaction volume, trust |

---

## Step 5: Build the PPTX

Use the pptx skill's `pptxgenjs` approach (from-scratch creation). Before writing code:

1. Re-read `/mnt/skills/public/pptx/pptxgenjs.md` for the full API reference
2. Apply the branding from `assets/utopia-branding.md` (Studio default) or the portfolio company's brand if specified
3. Follow the pptx skill's design guidance — no boring slides, vary layouts, use visual elements on every slide

### Branding Logic

- **Studio deck for co-investors** → Use Studio branding (Deep Navy, Steel Blue, Gold accent, Arial). Include "The Studio — Utopia Capital" footer and "Strictly Confidential" marking.
- **Founder coaching deck** → Ask the user for the company's brand colors, logo, and font preference. Fall back to a clean neutral palette if not provided.

### Layout Variety

Do not repeat the same layout across slides. Rotate through:

- Title + large stat callouts
- Two-column (text left, visual right)
- Icon + text rows in grid
- Full-width visual with overlay text
- Comparison columns (before/after, us/them)
- Timeline or process flow
- The Global Context three-column layout
- The Flywheel circular/cyclical diagram

---

## Step 6: QA

Follow the pptx skill's QA process exactly:

1. Convert to images: `python scripts/office/soffice.py --headless --convert-to pdf output.pptx` then `pdftoppm`
2. Visually inspect every slide — check for overlaps, cut-off text, alignment issues, low contrast
3. Content check: `python -m markitdown output.pptx` — verify no missing content or placeholder text
4. Fix issues and re-verify

---

## Step 7: Score the Output & Review

After generating the deck, score it again using the same 15-dimension framework from `references/scoring-rubric.md`. Present a before/after comparison:

```
PITCH DECK QUALITY SCORECARD
                              Input    Output    Delta
 1. Narrative Clarity          X/10     X/10     +X
 2. Problem Definition         X/10     X/10     +X
 ...
TOTAL                         X/150    X/150    +X
GRADE                                  [A/B/C/D/F]
```

Then provide:

- **Gap analysis** — flag slides with weak evidence or `[NEEDS INPUT]` markers
- **Narrative check** — does the story flow from global context → problem → solution → proof → ask?
- **Data verification** — confirm statistics are sourced
- **Dimension-specific recommendations** — for any dimension still scoring 6 or below, explain what's missing, what to do, and how many points it could gain
- **Top 3 priorities** — the three most impactful improvements the user can make

Target a minimum grade of **B** (90+/150) before sharing a deck with co-investors. Anything below B needs another iteration.

---

## Handling Edge Cases

### Sparse Source Material
- Build a skeleton deck with all slides
- Mark gaps with `[NEEDS INPUT: specific question]`
- Offer to research publicly available information
- Ask targeted questions: "What's your current MRR?" not "Tell me more about traction"

### Multiple Sources / Contradictions
- Synthesize overlapping information
- Prioritize the most recent data when conflicts exist
- Flag contradictions for the user to resolve

### Existing Deck Improvement
When the user uploads an existing pitch deck and asks to improve it:
- Extract all content first
- Identify structural gaps (missing Global Context? No flywheel?)
- Propose specific improvements before rebuilding
- Preserve any content the founder has clearly crafted carefully

### DD Report Available
When a Technical DD report exists:
- Read `references/dd-integration.md` for extraction patterns
- Pull technology assessment findings into the Product and Solution slides
- Surface risk flags in speaker notes (not on-slide — these are for the presenter)
- Reference the DD report's evidence ratings where relevant
