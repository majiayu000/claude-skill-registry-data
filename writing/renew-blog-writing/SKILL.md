---
name: renew-blog-writing
description: Workflow for writing Renew Implant Centre blog posts (MDX in content/blog) optimized for SEO, GEO, AEO, and AI-chat citation, and for sending readers to the implant candidate quiz. Enforces the answer-first + extraction-table + sourced-stat + FAQ skeleton, the exact frontmatter schema, the clinical/compliance guards, and the test gate. Use when drafting, editing, or reviewing any Renew blog post, or when the user mentions Renew blog content, dental implant articles, or "get cited by AI".
---

# Renew Blog Writing

Every post follows one skeleton so each article is easy for Google and for an LLM to quote, then hands the reader to the quiz at `/implant-candidate-quiz`. Strategy and entity facts live in [docs/search-visibility.md](../../../docs/search-visibility.md). The general playbook is the [seo-geo-aeo](../seo-geo-aeo/SKILL.md) skill.

## Preflight

1. Pick one `primaryQuery` a patient would type or ask a chatbot ("are dental implants worth it for seniors").
2. Pick a `cluster` from `BLOG_CLUSTERS` in `src/lib/blog.ts`.
3. Research with Firecrawl first. Find 3–5 primary sources (PubMed studies, canada.ca, RCDSO, CDA). Never cite another clinic's blog.
4. Read one existing post in `content/blog/` as a style reference.

## Post skeleton (in this order)

1. **Answer-first paragraph** — the direct answer in 2–4 sentences, key verdict in bold.
2. **`<ExtractionTable>`** — exactly one self-contained comparison table near the top.
3. **`<BlogCta />`** — the quiz CTA. No `href`; the page adds the quiz URL and UTM tags.
4. **Question H2s** — every `##` is a real question, `Sources`, or starts with `Why `. The first sentence under it answers it on its own.
5. **Sourced numbers** — use `<KeyStat value label source />` for headline figures. Every number links to its source.
6. **Why Renew** — one short section: surgeon, denturist, and on-site lab under one roof; free consultation with a 3D scan.
7. **`## Sources`** — bulleted list of every cited source.

Add 2–3 internal links to service pages or sibling posts.

## Frontmatter (validated by zod in `src/lib/blog.ts`)

```yaml
---
title: "≤ 70 characters, leads with the primaryQuery intent"
description: "110–165 characters, contains the primaryQuery"
datePublished: "YYYY-MM-DD"   # future dates stay hidden until that day
dateModified: "YYYY-MM-DD"
cluster: "all-on-4 | dentures-vs-implants | candidacy-recovery | cost-coverage | anxiety-sedation"
primaryQuery: "..."
author: "tom-szarski"
quizCtaLabel: "Short CTA text, no time claim faster than 2 minutes"
order: 6
heroImage: "/media/..."
heroImageAlt: "..."
faqs:            # at least 3; rendered on the page and as FAQPage JSON-LD
  - q: "Real patient question?"
    a: "Self-contained 2–4 sentence answer, no markdown."
---
```

Only add `reviewedBy` and `lastReviewed` (together) after a real clinical review has happened. They publish a MedicalWebPage `reviewedBy` claim.

## Clinical and compliance guards (hard fails in `src/lib/blog.test.ts`)

| Rule | Why |
|---|---|
| No prices or dollar amounts | Pricing is quoted only after the consultation. |
| Tom Szarski is a denturist (DD) — never "Dr. Tom" or "Dr. Szarski" | Regulated title. |
| No "guarantee" language | RCDSO advertising rules; outcomes vary. |
| CDCP covers dentures and overdentures (with preauthorization), not most implants | Keep coverage claims exact; link canada.ca. |
| Never invent stats, studies, or patient quotes | Cut the claim instead. |

## Gate

```bash
npx vitest run src/lib/blog.test.ts src/components/blog
```

This checks frontmatter, lengths, the skeleton, the guards, related-post linking, and that the MDX compiles with anchored headings, a table, and a quiz link. Then add the new URL to `public/llms.txt` (its test fails until you do) and run `npm run indexnow` after deploying.
