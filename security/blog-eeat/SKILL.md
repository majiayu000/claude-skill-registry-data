---
name: blog-eeat
description: 'Create, refresh, or audit blog content and blog templates for E-E-A-T signals: first-hand experience, expertise, authoritativeness, trustworthiness, source quality, creator attribution, editorial review, update freshness, original evidence, and user proof. Use when improving SEO blog posts, blog structured data, content briefs, author/reviewer sections, citations, or content operations.'
---

# Blog E-E-A-T

Use this skill when writing, refreshing, or auditing blog content for search quality and reader trust.

## Core Rule

Do not fake authority. Promote real evidence, real expertise, clear sourcing, and honest limitations. If a trust signal cannot be supported, recommend the smallest operational change needed to create it.

## E-E-A-T Model

Evaluate every blog page through these signals:

- Experience: first-hand use, tested workflows, original screenshots, before/after images, benchmarks, examples, and lessons learned.
- Expertise: named authors, contributors, reviewers, credentials, domain-specific reasoning, and accurate technical explanations.
- Authoritativeness: topical depth, internal links to related resources, external references, mentions, backlinks, and reusable assets others can cite.
- Trustworthiness: factual accuracy, current dates, visible updates, clear caveats, contact/help paths, privacy/security confidence, and source transparency.

Trust is the center of the model. Experience, expertise, and authority should make the page more reliable, not merely more decorated.

## Blog Post Checklist

For each post, check:

- A named author or accountable team profile is visible near the top.
- High-risk claims, statistics, platform requirements, prices, laws, standards, and product capabilities have credible citations.
- The post includes original evidence where possible: actual tool output, real image tests, pixel dimensions, file size changes, screenshots, settings, or before/after comparisons.
- A reviewer or editor is credited when the topic has technical, legal, financial, medical, or conversion-impact claims.
- Published, modified, and reviewed dates are accurate and not copied blindly from creation dates.
- The content explains when the recommended workflow does not apply.
- CTAs are relevant to the problem and do not interrupt source-critical sections.
- Related posts and tools reinforce the topic rather than generic site navigation.
- Images have descriptive alt text and are not purely decorative when used as proof.

## Template And Schema Checklist

When auditing or changing a blog template, look for structural support for:

- Author cards with name, role, short bio, profile URL, credentials, and sameAs links.
- Reviewer/editor metadata and visible "reviewed by" UI where appropriate.
- `BlogPosting` JSON-LD with `author`, `publisher`, `datePublished`, `dateModified`, `reviewedBy` or `editor` when real data exists, `citation` for cited sources, and accurate image metadata.
- A source/citation section or inline citations that can be represented in schema.
- Update notes or "last reviewed" blocks for evergreen posts.
- Original media metadata: alt text, caption, source/test context, and whether the media is generated, screenshot, or user-provided.
- UGC proof where appropriate: testimonials, examples, Q&A, comments, or customer-submitted workflows with moderation.
- Editorial standards page linked from author/reviewer or footer areas.

## Workflow

1. Inspect the content model first:
   - Find frontmatter, database fields, API validation, generated JSON, and schema builders.
   - Identify which E-E-A-T signals can be represented today and which require model changes.

2. Audit the visible template:
   - Check above-the-fold author/date/read-time display.
   - Check post footer, related content, CTAs, source sections, image rendering, and breadcrumbs.
   - Verify that the page does not claim expertise without proof.

3. Audit the content:
   - List unsupported claims and stale facts.
   - Prioritize adding original tests, examples, screenshots, citations, or caveats over generic rewrites.
   - For AI/image content, prefer test methodology, source image description, upscaler settings, output dimensions, observed artifacts, and repeatable steps.

4. Recommend improvements:
   - Separate quick template wins from content operations and larger data-model work.
   - Tie every recommendation to an E-E-A-T signal.
   - Include likely files, fields, schema properties, and tests to update.

5. If implementing:
   - Add fields and render support before mass-editing posts.
   - Preserve backward compatibility for existing posts.
   - Add tests for schema output, metadata, and visible author/reviewer/source blocks.

## Output Format For Audits

Lead with prioritized findings:

- Priority: P0/P1/P2.
- Signal: Experience, Expertise, Authoritativeness, or Trustworthiness.
- Location: file and line where possible.
- Gap: what is missing or weak.
- Fix: concrete implementation or content operation.

End with the smallest useful next implementation step.
