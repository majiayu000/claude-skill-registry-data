---
name: seo-content-qa
description: Score an SEO draft before it ships against its brief, checking intent, structure, human voice, product facts, competitor claims, links, images, schema and publishing readiness, with a PASS/FAIL verdict out of 40. Use for "check this draft", "is this article ready to publish", "QA my blog post", "review this before it goes live".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/seo-content-qa
---

# SEO content QA

Gate SEO drafts for intent, usefulness, human voice, factual accuracy, links, assets, schema, and publishing readiness. Use it before a draft is sent for approval, scheduled, published, or handed to a CMS. This is a strict pre-publish gate. It should improve the draft when permitted, then re-score. Do not declare content ready if it fails a critical check. It hands back a PASS/FAIL verdict, a score out of 40, required fixes and residual risks.

> **Romeo's rule:** A beautifully written draft with the wrong price in it is a fail, not a near miss.

## Use this when

- A draft is about to be sent for approval, scheduled, published, or pushed to a CMS.
- You need a pass/fail verdict against the brief, not a style opinion.
- A listicle or comparison needs every featured tool checked for a link and an image.
- A refresh of an already-ranking page needs checking for unapproved title, meta or slug changes.
- Fixes were applied and the draft needs re-scoring before anyone calls it ready.

## Don't use this for

- Writing or rewriting the draft from scratch → `seo-blog-writer`.
- Reviewing a live, published URL against its target query → `on-page-seo-review`.
- Writing or validating structured data in depth → `schema-markup`.
- Experience, expertise and trust signals across the site → `eeat-trust-review`.

## What you need

### Required

- Draft content or URL/readback.
- Content brief.
- Target keyword cluster.
- Content type: how-to, listicle, comparison, alternatives, landing page, refresh, localized page.
- Product facts and prohibited claims.
- Brand voice and banned phrases.
- Required links, assets, and schema.
- Output/CMS constraints.

### Helpful

- SERP notes.
- Existing page data for refreshes.
- Screenshot/image library.
- Analytics/search evidence.
- Source list for competitor claims.
- Readback from CMS.

### No tools?

Everything here works from the draft and the brief alone. If the draft is live or in a CMS preview, use view-source to check that the title, meta description, canonical and JSON-LD actually shipped; paste the JSON-LD into Rich Results Test or the Schema Markup Validator; open every link (or ask for a link-checker export) to catch placeholders and 404s. Verify product facts against the pricing and feature pages the user points you to, and competitor claims against the competitor's own pages. If you can't open a source, flag or soften the claim rather than passing it.

## Ground rules

- The brief is the contract.
- Factual accuracy outranks writing style.
- Search intent match outranks keyword inclusion.
- Human writing quality matters because generic AI prose hurts trust.
- Missing links/images are not minor on listicles or comparisons.
- Do not fail content because it is not written in the QA agent's personal style.
- Prefer targeted fixes over rewriting the whole draft.

## Scoring rubric

Score each area 0-5. Total 40 points.

### 1. Search intent and SERP fit

- 5: Clearly matches intent, page type, depth, and reader problem.
- 3: Mostly matches but misses a major expected subtopic or SERP convention.
- 1: Keyword appears but content answers a different intent.
- 0: Wrong page type or wrong audience.

Check:

- Intent classification matches brief.
- Top section answers the core query fast.
- Content type fits SERP: how-to, listicle, landing page, comparison, support, template, etc.
- Does not drift into generic broad coverage.

### 2. Structure and usefulness

- TL;DR exists and matches content type.
- Answer-first block exists near the top.
- H2/H3 structure is scannable.
- How-to steps are near the top.
- Listicles name all tools early.
- Comparisons give a clear verdict early.
- FAQs are useful and concise.

### 3. Human voice and readability

- Simple words and short paragraphs.
- Varied sentence rhythm.
- Specific examples, numbers, tradeoffs, and concrete use cases.
- No generic AI filler.
- No repetitive section pattern.
- No unsupported hype.
- Banned punctuation/style markers are absent if the style guide sets any.

Red flags:

- Every section starts the same way.
- All list items use identical structure.
- Vague phrases: powerful, robust, seamless, cutting-edge, unlock, harness, delve, game-changing.
- Overly balanced non-opinions where the reader needs a decision.
- Filler intro/conclusion.

### 4. SEO hygiene

- Primary keyword in title/H1 for new content.
- Primary keyword appears early when natural.
- Secondary terms are natural, not stuffed.
- Headings use query language without spam.
- Internal links support conversion and topic depth.
- Meta title/description, if present, are accurate and CTR-aware.
- Existing ranked refreshes preserve risky title/meta/slug unless explicitly approved.

### 5. Product and brand accuracy

- Product facts match the provided source of truth.
- Pricing/free/free-trial claims are correct.
- Platform support is correct.
- Privacy/security/processing claims are correct.
- Positioning matches brand rules.
- No invented testimonials, review counts, awards, customer names, benchmarks, or features.
- Claims the brand has prohibited are absent.

### 6. Competitor and source safety

- Competitor pricing, platforms, privacy, storage, performance, and review claims are sourced or softened.
- No defamatory or overconfident unsupported claims.
- Comparison verdicts are framed as fit/use-case, not absolute superiority unless evidence supports it.
- External links exist for named tools/products/platforms.

### 7. Links, assets, and schema

- Every named product/tool has a relevant first-mention link.
- Every featured listicle/comparison item has an image/screenshot unless exempted.
- Image alt text is descriptive.
- Internal links prioritize conversion pages where relevant.
- Schema matches visible content.
- FAQ schema questions/answers match visible FAQs.
- URLs are not obviously broken or placeholder-only.

### 8. Publishing readiness

- Output format matches target: Markdown, HTML, CMS JSON, document, etc.
- No layout-breaking markup.
- Required fields are present: title, slug, meta, category/tag, author, date, draft/publish status where applicable.
- Manual follow-ups are listed.
- CMS readback, if available, matches intended content.

## Critical fail conditions

Fail automatically if any are true:

- Search intent is wrong.
- Missing TL;DR when the brief or content type requires it.
- Missing answer-first block.
- Core product fact is wrong.
- Pricing/free-trial/platform/privacy/processing claim is wrong.
- Draft says something is free when it is only a trial.
- Draft invents competitor facts, testimonials, reviews, benchmarks, or features.
- Obvious AI prose dominates.
- Any featured listicle/comparison tool lacks a link.
- Any featured listicle/comparison tool lacks a required image/screenshot.
- Schema contradicts visible content.
- Existing ranking page title/meta/slug was changed without approval/risk note.
- Regulated claims are unsupported.

## Pass threshold

Default PASS requires:

- No critical fail.
- Score >=32/40.
- No area below 3/5.

The site owner may set stricter thresholds.

## Steps

1. **Read the brief first.**
   - Extract acceptance criteria, product facts, prohibited claims, required sections, links, assets, and schema.

2. **Review draft against the brief.**
   - Do not score in isolation. Score against the job it was supposed to do.

3. **Run critical-fail checks.**
   - If any fail, status is FAIL even if score is high.

4. **Score all 8 areas.**
   - Give evidence for low scores.

5. **Apply targeted fixes when allowed.**
   - Fix facts, TL;DR, answer-first, links, missing images, schema mismatches, robotic prose, and obvious SEO gaps.
   - Avoid full rewrite unless structure is broken throughout.

6. **Re-score after fixes.**
   - Only mark PASS when no critical fail remains.

7. **Return final verdict.**
   - Use the format in What to hand back.

## What to hand back

Return exactly this, filled in:

```markdown
**What I found:** <one plain-English sentence on the draft's state>
**What matters most:** <the issue that decides PASS or FAIL>
**What to do first:** <one sentence>

### QA verdict

- Status: PASS / FAIL
- Score: X/40 (intent x, structure x, voice x, SEO x, product x, competitor x, links/assets/schema x, readiness x)
- Critical fails: none / list
- Top 3 issues:
  1. ...
  2. ...
  3. ...

### Required fixes

- Specific fixes, ideally section-level or line-level.

### Optional improvements

- 3-5 high-impact improvements.

### Final notes

- Readiness status.
- Manual follow-ups.
- Residual risks.

### What I could not check

- <e.g. competitor pricing not verified: page blocked; CMS readback not available>
```

## Stop and flag if

The QA process itself fails, and must not hand back a verdict, if it:

- Reviews without reading the brief.
- Ignores product facts.
- Treats formatting as more important than factual/search quality.
- Passes missing images/links in a listicle/comparison.
- Declares ready without re-scoring after fixes.

## Next step

- PASS: run `cms-publishing-adapter` with the approved draft, the QA verdict and its residual risks.
- FAIL on the draft: send the required fixes back to `seo-blog-writer`. FAIL because the brief itself is wrong or missing facts: go back to `seo-content-brief`.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
