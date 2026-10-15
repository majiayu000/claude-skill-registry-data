---
name: market-copy
description: Copywriting analysis and generation engine scoring existing copy and producing optimized alternatives with proven frameworks.
---

# Copywriting Analysis & Generation

Use this skill for `/market copy <url>` style work: analyze existing website or campaign copy, score it, and produce evidence-backed alternatives with before/after recommendations.

The main file is the operating contract. Load references only when deeper frameworks, channel templates, examples, or troubleshooting detail are needed.

## When To Use

- The user asks to analyze, rewrite, score, or improve marketing copy.
- The user provides a URL, page copy, landing page draft, ad copy, email copy, CTA set, meta description, or positioning text.
- The task needs headline alternatives, section rewrites, CTA optimization, a swipe file, or a `COPY-SUGGESTIONS.md` report.

## Required Inputs

Ask for or infer the smallest safe set of inputs:

- Source: target URL, pasted copy, page file, or draft.
- Business type, offer, audience, market, and conversion goal.
- Page or channel type: homepage, landing page, pricing, about, product, feature, blog, contact/demo, email, ad, or meta copy.
- Brand voice constraints and any existing `BRAND-VOICE.md`.
- Proof available: metrics, testimonials, customer logos, awards, guarantee terms, case studies, or product facts.
- Constraints: regulated category, compliance limits, forbidden claims, required CTA, length, tone, and output format.

Do not invent business facts, customer names, results, testimonials, awards, guarantees, pricing, urgency, or validation evidence.

## Core Workflow

1. Collect the copy and context from the URL, pasted text, or local files.
2. Identify page or channel type and the primary conversion action.
3. Extract headline, subheadline, section headings, body copy, CTAs, navigation labels, meta copy, and social proof.
4. Analyze voice, value proposition, proof, clarity, persuasion, specificity, emotion, and action.
5. Select copy frameworks based on the problem: PAS for pain-led offers, AIDA for attention-led pages, Before-After-Bridge for transformation, 4U for concise headlines.
6. Generate alternatives that preserve brand voice unless the current voice is ineffective; flag any intentional divergence.
7. Validate every claim against available evidence and mark missing proof as a placeholder.
8. Produce terminal summary and a full `COPY-SUGGESTIONS.md` report when requested.

## Decision-Critical Copy Logic

- If the reader cannot understand the offer in 5 seconds, prioritize headline clarity before style.
- If proof is weak, reduce specificity or use placeholder slots such as `[specific result]`.
- If the page is conversion-focused, align headline, subheadline, CTA, and objection handling around one action.
- If the page is trust-focused, prioritize proof, story, credibility, and risk reversal.
- If the channel is short-form, prefer one clear promise over multiple benefits.
- If the category is health, finance, legal, employment, housing, credit, or trading, tighten claims and recommend review.
- If a CTA promises a trial, download, demo, or quote, the destination must match that promise.

## Claims, Evidence, And Compliance Constraints

- Specific claims require real data or clearly marked placeholders.
- Never fabricate testimonials, statistics, customer names, logos, awards, press mentions, partnerships, guarantees, or urgency.
- Do not make unsupported competitor comparisons.
- Do not write copy that targets protected classes, exploits fear of harm, or guarantees regulated outcomes.
- Risk reversal must be real: only mention trials, refunds, cancellation, or guarantees if the business offers them.
- Label frameworks used in swipe-file entries.
- Cite the evidence source or mark evidence gaps in the report.

## Validation Gates

- 5-second clarity test: what it is, who it is for, and why it matters.
- Offer-to-CTA alignment: the CTA action matches the promise.
- Evidence check: all numbers, outcomes, testimonials, and social proof are real or placeholders.
- Voice check: recommendations match documented or observed brand voice.
- Compliance check: regulated claims are softened or flagged for review.
- Specificity check: vague copy is replaced with concrete but supportable language.
- Action check: primary CTA appears above the fold, after major sections, and near the end when appropriate.

## Output Expectations

Return:

- Page or channel type and voice profile.
- Copy score with brief rationale.
- Value proposition gaps.
- Top fixes with before/after examples.
- Headline, subheadline, CTA, meta, and social-proof alternatives as requested.
- Evidence gaps, compliance risks, and assumptions.
- Full report path when writing `COPY-SUGGESTIONS.md`.

For full reports, use this structure: executive summary, voice profile, score breakdown, value proposition analysis, headline recommendations, section-by-section suggestions, CTA optimization, before/after examples, swipe file, and implementation priority.

## Minimal Examples

Headline rewrite:

```text
Before: "Software for growing teams"
After: "Turn scattered customer messages into one prioritized support queue"
Why: clearer audience, concrete task, and specific operational outcome.
```

CTA rewrite:

```text
Before: "Submit"
After: "Get My Demo Plan"
Why: specific value and matches a demo-request flow.
```

## Reference Map

- [Copy workflow and report structure](references/copy-workflow.md)
- [Frameworks and positioning](references/frameworks-and-positioning.md)
- [Channel templates](references/channel-templates.md)
- [Claims validation and compliance](references/claims-validation-and-compliance.md)
- [Examples and troubleshooting](references/examples-and-troubleshooting.md)

## Cross-Skill Integration

- If `BRAND-VOICE.md` exists, use its voice guidelines.
- If `MARKETING-AUDIT.md` exists, reference the Content & Messaging score.
- If `COMPETITOR-REPORT.md` exists, use competitor messaging to shape differentiation.
