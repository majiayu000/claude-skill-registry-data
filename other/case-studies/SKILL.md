---
name: case-studies
description: "Create compelling B2B customer case studies for the company. Use when asked to write, draft, or help with case studies, customer success stories, customer testimonials, or win stories. Supports both branded case studies (with company name) and anonymous case studies (e.g., 'a customer in the retail space') when NDAs or privacy concerns apply."
---

# Case Study Creation

Create compelling customer success stories that show the value the company delivers, grounded in the positioning and proof points in the brain files.

## Source of Truth

Before writing any case study, consult the brain files:

- **Product facts:** `/brain/truth.md` — All claims must originate here
- **Messaging:** `/brain/positioning-and-messaging.md` (Section 2) — Use approved external messaging
- **ICP:** `/brain/positioning-and-messaging.md` (ICP section) — Ensure customer matches target profile
- **Value props:** `/brain/positioning-and-messaging.md` — Pull key differentiators from here
- **Audience language:** `/brain/audience-language.md` — Use the customer's vocabulary, not vendor-speak
- **Journey intelligence:** `/brain/customer-journey.md` — Understand objections, stall points, and what accelerates deals
- **Voice:** `/brain/voice-and-tone.md` and `/brain/voice-samples.md` (if they exist) — Narrative voice for the framing and connective prose (customer quotes keep the customer's own voice)

If any required information is missing from the brain, mark it `[VERIFY]` and ask.

## Case Study Framework

Every case study follows this five-section structure. Keep it concise — a full case study should be roughly 600-1000 words, not 1500+.

1. **Headline & Executive Summary** — Compelling headline highlighting the main outcome/transformation, plus a 2-3 sentence summary covering customer, challenge, and result.
2. **Before [Company]** — The situation before: environment, what wasn't working, and business impact. Tell this as a narrative, not a bullet list. Use prose to set the scene and create urgency.
3. **Why They Chose [Company]** — Decision factors and what stood out vs alternatives. A few short paragraphs, not a long list.
4. **After [Company]** — The top results, prioritized by business impact. Combine business and technical outcomes into one unified section — do NOT split into separate "Business Results" / "Technical Results" / "Benefits to Customers" subsections. Lead with the outcomes that matter most to the business, weave in technical details only where they support the story. Use a short list (3-5 items) of the most compelling results, then close with a quote if available.
5. **Call to Action** — "Sign up for a demo" with link to [your-site].

## Case Study Types

**Branded**: Full company name and details disclosed. Use `references/template-branded.md`.

**Anonymous**: Customer identity protected (e.g., "a leading fintech company"). Use `references/template-anonymous.md`.

Ask the user which type if not specified.

## Information Gathering

Before writing, gather these inputs from the user (or interview notes):

### Required
- Customer industry and company size
- Current environment and approach before [Company]
- Gaps, challenges, and business impact from their prior approach
- Why they chose the product and what stood out vs alternatives
- What changed after [Company] (business results, technical results)
- Quantifiable results (metrics, KPIs, time savings)

### Optional but valuable
- At least one customer quote
- Benefits to their end customers
- Team/stakeholder reactions

If information is missing, ask targeted questions to fill gaps. See `references/interview-questions.md` for a complete question guide.

## Writing Guidelines

### Voice and Tone
- Professional but accessible — avoid jargon unless the audience expects it
- Let the customer be the hero; [Company] is the enabler
- Use active voice and concrete details
- Match brand tone from `/brain/positioning-and-messaging.md`

### Write Prose, Not Bullet Lists
Case studies are stories, not spec sheets. Default to well-crafted paragraphs and narrative flow. Use bullets sparingly — only when listing 3-5 discrete results in the "After [Company]" section or when a set of items is genuinely easier to scan as a list. If you find yourself writing more than two bullet sections in a row, stop and rewrite as prose.

**Bad:** A wall of bullets under sub-headers like "Environment," "Gaps," "Business Impact," "Technical Results," "Customer Benefits"
**Good:** A few paragraphs that tell the story naturally, weaving environment, challenges, and impact together

### Brevity
Every sentence should earn its place. Cut filler, remove redundant context, and resist the urge to exhaustively document every detail from the source notes. A case study is a highlight reel, not a transcript. If a detail doesn't strengthen the narrative or prove a result, leave it out.

### Metrics Best Practices
- Lead with the most impressive metric in headline/summary
- Be specific: "reduced MTTR from 4 hours to 45 minutes" beats "faster troubleshooting"
- Weave metrics into the narrative rather than isolating them in a separate table

### Quote Guidelines
- Use direct quotes to add authenticity and emotion
- Include speaker name and title for branded studies
- For anonymous: "The Platform Engineering Lead noted..."
- Place quotes where they reinforce the narrative naturally

## Processing Mixed Inputs

When working with multiple information sources, follow this workflow:

### Step 1: Inventory Sources
List what you have:
- [ ] Interview transcript/recording
- [ ] Written questionnaire responses
- [ ] Internal notes (CSM, sales, support)
- [ ] Usage metrics/data

### Step 2: Extract Key Information
From each source, pull:
- **Before state**: Environment, approach, gaps, challenges, business impact
- **Decision factors**: Why [Company], what stood out vs alternatives
- **After state**: Changes, business results, technical results, customer benefits
- **Metrics**: Specific numbers for the Key Results section
- **Quotes**: Direct customer statements (note source and speaker)

### Step 3: Reconcile Conflicts
If sources disagree:
- Prefer customer direct quotes over internal summaries
- Use most recent data for metrics
- Flag contradictions for user to clarify

### Step 4: Identify Gaps
Check against required information list. Ask user to fill gaps before drafting.

### Step 5: Synthesize Narrative
Combine into single coherent story following the six-section framework.

## Output Formats

**Output location:** `marketing/case-studies/[customer-slug]/` — all files from a single run share this folder. Confirm the customer slug with the user before creating files.

Choose the appropriate format based on the use case:

| Format | Use Case | Template |
|--------|----------|----------|
| **Full Case Study** | Website, sales collateral, in-depth sharing | `references/template-branded.md` or `references/template-anonymous.md` |
| **Executive Summary** | Quick 1-pager for prospects, internal briefings | `references/template-executive-summary.md` |
| **Slide Deck** | Sales presentations, webinars, conferences | `references/template-slide-deck.md` |
| **Social Media** | LinkedIn, Twitter, promotional content | `references/template-social-snippets.md` |
| **Web Page** | Website publication with SEO optimization | `references/template-web-page.md` |

## Final Step: Copy-Editing Pass

Before presenting the draft to the user, run a full copy-editing pass using the `copy-editing` skill:

1. **Vale Lint** (Sweep 0): If the draft has been saved to a file, run `vale <filepath>`. Fix all errors, address warnings. If Vale is not installed or the draft isn't saved yet, skip and note "Vale: SKIPPED."
2. **Clarity**: Every sentence immediately understandable. Technical details accessible to the target audience.
3. **Voice**: Consistent tone throughout. Professional but not corporate.
4. **So What**: Every claim answers "why should I care?" Results connect to business impact, not just technical metrics.
5. **Prove It**: Every claim is substantiated — numbers, quotes, or concrete examples. No unearned superlatives.
6. **Specificity**: Vague words replaced with concrete ones. Results include numbers and timeframes.
7. **AI Writing Tics**: Scan for rhetorical negation-pivots, throat-clearing phrases, and repetitive rhythm patterns. One negation-pivot max per piece.
8. **Cross-section phrase repetition**: Scan the full draft for any key phrase appearing more than twice. The headline owns the phrase — vary or cut everywhere else.
9. **Em Dash Check**: Max 5 per case study.

Case studies are long-form and customer-facing — run the full sweep.

---

## Quality Checklist

Before finalizing, verify:
- [ ] Compelling headline with key outcome
- [ ] Executive summary captures full story in 2-3 sentences
- [ ] "Before [Company]" section creates urgency and relatability
- [ ] "Why They Chose [Company]" clearly shows decision factors
- [ ] "After [Company]" shows 3-5 concrete results, business impact first
- [ ] CTA directs reader to sign up for a demo at [your-site]
- [ ] Tone appropriate for technical audience
- [ ] Anonymous details sufficiently obscured (if applicable)
- [ ] All product claims verified against `/brain/truth.md`
- [ ] Copy-editing pass completed (Vale + editorial sweeps)
