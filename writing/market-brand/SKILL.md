---
name: market-brand
description: Brand voice analysis and guidelines generation examining communication patterns across channels.
---

# Brand Voice Analysis and Guidelines Generation

Analyze a brand's voice, tone, and messaging across all available channels
and generate a comprehensive brand voice guidelines document. Examine how the
brand communicates, identify patterns and inconsistencies, and produce
guidelines any writer or marketer can follow to maintain consistency.

## When to use

- User wants to understand or document a brand's voice.
- User needs brand voice guidelines for a team, freelancers, or agency.
- User wants to ensure consistency across marketing channels.
- User is rebranding or refining their brand identity.
- User wants to compare their brand voice to competitors.
- Triggered by `/market brand <url>` or `/market brand`.

## Required input contract

Before launching the analysis:

- **Target URL** (or set of URLs) — must be reachable.
- **Available source types** — at minimum homepage, about, product. Secondary
  channels (blog, social, email) increase confidence.
- **Cross-skill data** — if `/market competitors` ran earlier, reuse its
  competitor data for Step 6.

If only a single page is available, run the analysis and **state the
limitation explicitly** in the deliverable — do not extrapolate.

## Claims and source-quality constraints

- Every dimension score, archetype assessment, and consistency rating must be
  **evidence-backed** with 3-5 quoted examples from the source material.
  No invented quotes.
- Do not fabricate a tagline, boilerplate, or brand story — if missing, flag
  as "Missing" or "Partial" in the messaging hierarchy and recommend creation.
- Do not extrapolate brand voice from a single page. If sources are
  insufficient, state the limitation explicitly in the output.
- Voice and tone are different. Voice is the consistent personality; tone
  shifts by context. Do not conflate them.
- Frame consistency issues as opportunities, not failures.

## Workflow — 10 steps

1. **Gather source material** — primary (homepage / about / product),
   secondary (blog / social / email / support copy), tertiary (jobs / press / ads).
2. **Voice dimensions** — score 1-10 across the four spectra (see below).
3. **Tone mapping** — map across 8 contexts (homepage, product, blog, social,
   error, email subject, CTA, support).
4. **Brand archetype** — Primary + optional Secondary from the five
   (Authority, Innovator, Friend, Rebel, Guide); rate fit Strong/Moderate/Weak.
5. **Vocabulary** — 15-20 characteristic words across action / descriptive /
   value / industry; plus words-they-avoid + signature phrases.
6. **Competitor comparison** — same dimensions + archetype, 2-3 competitors;
   reuse `/market competitors` data if available.
7. **Consistency audit** — score each of 6 channels Consistent / Mostly /
   Inconsistent; compute Overall Consistency Score X/10.
8. **Messaging hierarchy** — Tagline → Value Props → Elevator Pitch →
   Boilerplate → Full Story. Flag missing layers; do not fabricate.
9. **Voice documentation** — Voice Chart (IS / IS NOT pairs) + Writing Do's
   and Don'ts grounded in the analysis.
10. **Copy samples** — 5-8 concrete pieces in the identified voice across
    headline, product, blog, social, email subject, CTA, error, thank-you.

Full step-by-step procedure: `references/brand-workflow.md`.

## Voice dimensions (decision logic)

Each dimension is a spectrum, not a binary. Score 1-10.

| # | Dimension | 1 ← → 10 |
|---|-----------|----------|
| 1 | Formality | Formal ← → Casual |
| 2 | Levity | Serious ← → Playful |
| 3 | Complexity | Technical ← → Simple |
| 4 | Personality | Reserved ← → Bold |

Evidence required: quote 3-5 specific examples per dimension. Full signal
tables, tone mapping, and archetype profiles: `references/voice-tone-and-identity.md`.

## Brand archetypes

| Archetype | One-line | Example brands |
|-----------|----------|----------------|
| The Authority | Expert, trustworthy, data-driven | McKinsey, IBM, Mayo Clinic |
| The Innovator | Forward-thinking, disruptive, visionary | Tesla, Stripe, Notion |
| The Friend | Warm, approachable, helpful | Mailchimp, Slack, Duolingo |
| The Rebel | Bold, challenging conventions, irreverent | Nike, Oatly, Cards Against Humanity |
| The Guide | Wise, patient, methodical | HubSpot, Khan Academy, Ahrefs |

Brands may blend 1-2 archetypes. Output: Primary + (optional) Secondary +
Fit rating (Strong / Moderate / Weak).

## Validation gates

Before delivering the report:

- [ ] Every score has 3-5 quoted examples from real source material.
- [ ] Source coverage is ≥ 3 channels, or single-source limitation is stated.
- [ ] Primary archetype is justified with evidence, not aesthetic preference.
- [ ] Vocabulary lists are non-empty across all four categories.
- [ ] Competitor scores come from observed competitor URLs or `/market competitors` data.
- [ ] Missing tagline / boilerplate / brand story is flagged, not fabricated.
- [ ] Consistency findings are framed as opportunities.
- [ ] Voice (personality) and tone (context-shifted) remain distinct.
- [ ] Output written to `BRAND-VOICE.md` in the current directory.

Full per-step quality checklists + anti-patterns:
`references/competitive-diagnostics-and-validation.md`.

## Output expectations

Generate `BRAND-VOICE.md` containing:

- Voice Summary (2-3 sentences).
- Voice Dimensions (4 scores + evidence + visual voice map).
- Brand Personality (primary + secondary archetype with evidence).
- Tone by Context (8-row table).
- Vocabulary (Words We Use / Avoid / Signature Phrases).
- Voice Chart (IS / IS NOT pairs).
- Writing Guidelines (Do's / Don'ts).
- Brand Messaging Hierarchy (5 layers with status).
- 5-8 Copy Samples in the identified voice.
- Competitor Voice Comparison.
- Consistency Audit (channel table + Overall Score).
- Recommendations (Immediate / Voice Evolution / Consistency).

Full template + worked archetype-keyed copy samples + filled voice map and
consistency audit examples: `references/examples.md`.

## Key principles

- Read like a detective — every word choice, punctuation decision, and
  sentence structure reveals something.
- Always provide **evidence** for every assessment; quote specific examples.
- The deliverable should be usable by a new copywriter who has never seen
  the brand.
- Copy samples are the most valuable artifact — make them diverse so writers
  have references for every context.
- Voice ≠ tone. A customer-complaint reply differs in tone from a launch
  announcement, but stays in the same voice.

## Reference map

| Need | Read |
|------|------|
| Full 10-step procedure with source-gathering checklist | `references/brand-workflow.md` |
| Voice-dimension signal tables, 8-context tone map, full archetype profiles | `references/voice-tone-and-identity.md` |
| Vocabulary categories, messaging hierarchy, Voice Chart, Do/Don't, copy templates | `references/positioning-and-messaging.md` |
| Competitor matrix + differentiation, consistency audit, validation checklists, anti-patterns | `references/competitive-diagnostics-and-validation.md` |
| Full `BRAND-VOICE.md` template + worked copy samples (Friend, Authority) + filled voice map + audit example | `references/examples.md` |
