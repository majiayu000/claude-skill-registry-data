---
name: seo-blog-writer
description: Research-driven SEO content writer that produces publication-ready markdown articles built around search intent, verified claims, and original value. Use this skill whenever the user asks for a blog post, article, long-form content, "content for our site", a post targeting a keyword, a content refresh or audit of an existing article, or anything meant to be published on a website — even if they never say "SEO". Also use it when the user mentions keywords, search rankings, organic traffic, content marketing, meta descriptions, keyword cannibalization, or asks to "write something about X for the blog". If a piece of writing is destined for the web and could benefit from search visibility, use this skill.
---

# SEO Blog Writer

Write content that deserves to rank. Search engines reward content that satisfies the searcher and adds something the existing results don't — so every rule here serves the reader first. A perfectly formatted article with no original insight is a failure; a useful, authoritative article with a 163-character meta description is not.

The workflow: **gather inputs & validate format → research & build evidence → write → verify against the rubric**. The research stage is what separates content that ranks from content that merely exists — don't skip it.

## Stage 1: Gather inputs and validate the format

Establish these from the user's request. Infer aggressively; confirm only what's genuinely ambiguous. When running non-interactively, make the most defensible choice and state the assumption.

1. **Primary keyword** — the search query this content targets. If the user gives only a topic, derive a plausible keyword and state your choice so they can correct it.
2. **Search intent** — informational, commercial investigation, transactional, navigational, local, or mixed. Identify the reader's desired *outcome*, not merely the keyword.
3. **Audience & brand voice** — who reads this and how the brand talks. A professional-but-warm default is acceptable if the user doesn't care.
4. **Business goal** — what this content should do for the business. This shapes the CTA and internal-link suggestions.
5. **Word count** — treat any requested count as a planning target, not a quality signal, unless the user states a strict publishing requirement. If unspecified, let intent coverage decide. Prefer a shorter complete article over a longer repetitive one.

**Format fit — challenge the assumption that every keyword deserves a blog post.** Before writing, confirm an article is the correct page type for the intent. If the searcher clearly wants a calculator, service provider, pricing page, product comparison, location page, glossary, or resource hub, say so and recommend that page type instead (or alongside). Writing a "10 Tips" article for a query that wants a tool wastes everyone's time.

## Stage 2: Research and build the evidence base

Follow `references/research-protocol.md` for the full procedure. In brief:

- **SERP analysis** — search the primary keyword and analyze what ranks: dominant intent, page types, recurring subtopics, questions and objections, freshness, entities present, search features, and — critically — weaknesses and omissions. Synthesize; never reproduce a competitor's heading structure or phrasing.
- **Information gain — the non-negotiable.** Before drafting, state the article's unique value: at least one meaningful element the ranking pages don't provide (original examples, calculations, frameworks, decision criteria, local data, process details, templates, proprietary observations). If no original value is available from the user's context or your research, identify what the client should supply, and say so in the deliverable. Do not merely summarize or remix the ranking pages.
- **Claim ledger** — before drafting, list every material claim the article will make, whether it needs verification, the preferred source, and its status (verified / qualified / removed / awaiting client evidence). Prefer primary sources; don't cite one blog because it cites another blog.
- **Freshness** — identify claims that may have changed in the last 12–24 months (laws, prices, statistics, product features, platform behavior) and verify them with dated sources. Don't put a year in the title unless the article genuinely contains current-year information.
- **Site-context check** — when the client's domain, sitemap, or existing content is available, check for pages targeting overlapping intent. Decide whether to create, merge, redirect, expand, or refresh; recommend updating an existing page when a new article would be redundant. Identify real internal-link sources and destinations.

If web search is unavailable, say so and proceed from the user's inputs and your own knowledge — but flag that competitive positioning and time-sensitive claims are unverified.

## Stage 3: Write

### Structure

- **Title (one H1):** descriptive, concise, distinctive, likely to display clearly in search. Prefer roughly 45–65 characters when practical, but never sacrifice clarity for a character count — Google has no fixed limit and may rewrite title links anyway. Offer 2–3 options in the front-matter.
- **Meta description:** accurately summarizes the page and gives a compelling reason to click. Prefer roughly 140–165 characters when practical; prioritize accuracy and usefulness over length.
- **Slug:** short, lowercase, hyphenated, keyword-bearing, no stop words.
- **Opening:** lead with the reader's problem or a concrete payoff — never throat-clearing. Work the primary keyword into the opening naturally if it fits; don't force it.
- **Headings:** reflect the searcher's major questions, decisions, or subtopics. Primary and related terminology appears where contextually relevant. No heading exists primarily to hold a keyword. A reader skimming only headings should get the argument.
- **Paragraphs:** deliberately uneven — mostly 1–5 sentences, mixing short punchy paragraphs with longer ones. Lists and tables only where genuinely parallel items aid scanning; bold sparingly. Rhythm rules live in `references/voice-and-tells.md`.
- **FAQ (conditional):** include one only when distinct, unanswered questions remain after the main article. Never repeat what the body already answers clearly, and never add an FAQ for length, keywords, schema, or rich-result targeting — Google no longer shows FAQ rich results.
- **CTA:** aligned to the business goal from Stage 1, not a generic "contact us".

### Language and coverage

Cover the subject the way an expert would: related entities, supporting concepts, industry terminology, query variations, subtopics, and user questions arise naturally from comprehensive coverage — never from a keyword list. If any sentence exists only to hold a keyword, delete it.

Voice rules regardless of brand — the full rulebook is `references/voice-and-tells.md`; read it before drafting and run its checklist in Stage 4. The load-bearing rules: take at least one defensible stance a competitor's article wouldn't publish; replace hedges with conditions ("if your lot is under a quarter acre, skip this" — not "results typically vary"); prefer specifics (numbers, dates, prices, tool names, edge cases) over adjectives; write with deliberately uneven rhythm — paragraph lengths vary, section depth follows value rather than symmetry; no signposted transitions ("Moreover", "Let's dive in") and no conclusion that restates the article. Ration the tics: at most one rule-of-three triad per article, em dashes and bold used sparingly, and never the "It's not just X — it's Y" frame. The banned-phrase list lives in the reference file, but the durable rule is stronger than any list: any sentence that could appear unchanged in any article on any topic gets cut or made specific. Make claims confidently — an expert says "sealant fails in 3–5 years", not "sealant may potentially degrade over time". Address the reader as "you" unless the voice dictates otherwise. Never fake humanity: no deliberate typos, no invented anecdotes, no AI-detector tricks — the target is writing that survives close reading by an expert, not fooling a classifier.

### Experience, authority, and anti-fabrication

- Never imply the writer used a product, served a customer, visited a location, ran a test, or observed a result unless supplied evidence supports it.
- Never invent credentials, customer outcomes, quotes, case studies, proprietary processes, awards, or years of experience.
- Separate verified business expertise (from the user's context) from *recommended additions* the client could supply — list the latter in the deliverable, don't fake them.
- Suggest author byline, reviewer, and About-page improvements when they'd strengthen the page.

### Links and evidence

Cite every material claim that requires verification; link authoritative primary sources when available. Add internal links only where they help the reader continue a relevant journey, as `[anchor text](INTERNAL: description of target page)` placeholders — or real URLs when the site-context check found them. No link quotas in either direction; don't add links to satisfy a number, and don't cap sources a technical piece genuinely needs. Don't rely on competing SEO articles as factual backbone — use them for positioning, not facts.

### Images

Recommend image concepts that add value (diagrams, screenshots, tables, original visuals) and describe each image's purpose. Provide draft alt text only when the actual image content is known; describe visible content, don't stuff keywords. Mark decorative images for empty alt attributes. Recommend captions where they add context the image alone can't.

### Schema (conditional)

Recommend structured data only when appropriate to the page: `Article`/`BlogPosting` for standard posts, `HowTo` for genuine step-by-step instructions, `LocalBusiness` where the site context supports it, `BreadcrumbList` when the site uses breadcrumbs — or none. Never default to FAQ schema. Any recommended markup must be accurate to the visible content.

### High-stakes (YMYL) topics

For health, medical, legal, financial, safety, or similarly consequential content: use current authoritative sources only, clearly distinguish education from professional advice, avoid diagnoses/guarantees/definitive recommendations unsupported by evidence, recommend qualified expert review before publication, and include a reviewer field in the deliverable.

## Stage 4: Verify and deliver

Score the draft against `references/quality-rubric.md` — weighted categories, not a flat checklist. Intent satisfaction and accuracy dominate; technical on-page details matter least. Actually evaluate each category and fix what's weak before delivering. As part of the voice pass, run the tells checklist at the end of `references/voice-and-tells.md` — including the 500-companies test: if the article would work for any competitor after swapping the company name, rewrite it.

Deliver as a markdown file:

```markdown
---
title: "Chosen title"
title_options: ["Alternative 2", "Alternative 3"]
meta_description: "The meta description"
slug: post-slug
primary_keyword: "the keyword"
search_intent: "commercial investigation"
unique_value: "One sentence: what this article provides that the ranking pages don't"
schema_recommendation: "BlogPosting | HowTo | none — with one-line rationale"
reviewer: "Recommended for YMYL topics; otherwise omit"
review_date: "Recommended re-verification date for time-sensitive articles; otherwise omit"
word_count: 1234
---

# Chosen Title

[article body]

---

## Publish checklist
- [ ] Replace INTERNAL link placeholders with real URLs
- [ ] Image concepts: [what to create/source and why; draft alt text only where image content is known]
- [ ] Client evidence needed: [first-hand details, data, or examples the client should supply to strengthen E-E-A-T]
- [ ] [any post-specific items — schema validation, expert review, etc.]
```

After creating the file, give the user a two-sentence summary: the angle you chose and the unique value it adds — not a recap of the article.

## Refresh and audit mode

When asked to audit or refresh existing content: read the existing article first, then run Stage 2 research against its target intent. Preserve material that is still accurate and strong — wholesale rewriting destroys accumulated relevance signals for no gain. Verify every time-sensitive claim; update, qualify, or remove what's stale. Check for cannibalization with newer pages on the same site. Deliver a change plan (keep / update / remove / add, with reasons) alongside the revised article, so the client can see exactly what changed and why.

## Partial requests

Users sometimes want a fragment: title ideas, a meta description, an outline, or an SEO review of an existing draft. Use the relevant stage's rules and skip the rest. For reviewing a draft, run Stage 2 research plus the Stage 4 rubric against it and report gaps with specific fixes.
