---
name: seo-advisor
alias: /seo-advisor
description: "Structural SEO review — discoverability, intent alignment, content structure. Not keyword-volume or SERP data."
invokable: true
perspective_module: true
disallowedTools: Write, Edit
version: 0.1.0
---

# SEO Advisor

## JTBD (Jobs To Be Done)

### Primary Job
When I already have content and need to know whether it is discoverable and aligned with what the reader actually came looking for,
I want a structural SEO and intent review,
so I can fix invisible discoverability problems before the content ships.

### Secondary Jobs
- When content is strong editorially but may be hard to find, I want a structural audit, so I can improve search-readiness without pretending I have external SEO data.
- When a broader copy review needs an SEO lens, I want a focused discoverability perspective, so the final recommendation includes structural search concerns.

### Job Layers
- Functional: Review content structure, intent alignment, metadata, and internal discoverability patterns.
- Emotional: Reduce the frustration of publishing good content that fails because its structure and intent are off.
- Social: Helps the user demonstrate that content quality includes discoverability, not just tone or correctness.

### This Skill Is For
- A user with existing content who wants to know if searchers will recognize they are in the right place.
- A user reviewing headings, metadata, internal linking, and search-intent alignment before publishing.
- A user adding a structural SEO perspective to a broader editorial review.

### This Skill Is NOT For
- A user who needs keyword volume, ranking data, SERP analysis, or competitive SEO intelligence; use dedicated SEO tools.
- A user who needs a full content brief before writing; use `copy-planner`.

### Paired With
- `copy-critic`: Use it as the primary content review, then apply SEO Advisor as a discoverability perspective.
- `copy-planner`: Use it earlier when the job is to structure content before drafting, not to review an existing draft.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has a draft and wants discoverability review | SEO Advisor audits structure and intent | Structural SEO findings and fixes |
| Has strong copy but unclear search alignment | SEO Advisor tests whether the opening and structure match likely intent | An intent-alignment diagnosis |
| Needs SEO as one perspective in a broader review | SEO Advisor contributes a focused lens | Search-readiness input without overclaiming data |

### When to Escalate
- If the user needs data-driven keyword or ranking analysis, escalate to dedicated SEO platforms outside this repo.
- If the user needs to create the content brief before writing, escalate to `copy-planner`.

## Purpose

SEO Advisor reviews **structural SEO quality** and **search intent alignment** — two dimensions that content writers, product managers, and copy editors often miss or deprioritize.

Structural SEO flaws compound: broken heading hierarchies confuse both search crawlers and users. Meta descriptions written lazily waste click-through opportunities. Missing internal links orphan pages and hide topic relationships. Missing alt-text fails accessibility and image search.

Search intent misalignment is subtler but fatal: you can have perfect structure on content that nobody was searching for, or that answers a question your audience didn't ask.

This skill surfaces both problems **without claiming to do keyword research, SERP analysis, or competitor ranking work**. It reads the content itself and audits against established SEO structural patterns.

### What This Skill Does

- ✓ Audits heading hierarchy (single H1, logical progression, no skips)
- ✓ Reviews title tags and meta descriptions (length, clarity, alignment)
- ✓ Maps search intent (informational/navigational/transactional/commercial, matched within first 100 words)
- ✓ Identifies featured snippet opportunities (direct answers, lists, tables, FAQ patterns)
- ✓ Flags technical SEO issues (missing alt-text, broken URLs, accessibility concerns)
- ✓ Checks internal linking structure (orphaned content, anchor text quality)
- ✓ Audits content completeness vs. topic scope
- ✓ Works as a standalone reviewer OR integrated perspective within copy-critic

### What This Skill Does NOT Do

- ✗ Provide keyword search volume data (use Ahrefs, SEMrush, Moz)
- ✗ Analyze SERP results or competitor pages
- ✗ Make ranking predictions based on data
- ✗ Suggest specific keywords to target (that requires data you provide)
- ✗ Audit page speed, server response time, or Core Web Vitals
- ✗ Review backlink profiles or domain authority

**If you need data-driven SEO work, use dedicated tools. If you need structural and intent alignment review, use this skill.**

## Use_When

- **Content draft has structural SEO issues**: Heading hierarchy is messy, too many H1s, meta descriptions are missing
- **Uncertain about search intent match**: Does this content actually answer what people are searching for?
- **Building a topic cluster**: Need to verify internal linking strategy and content relationships
- **Writing detailed/long-form content**: Featured snippet opportunities, FAQ structure, topic completeness
- **Reviewing HTML/Markdown source**: Alt-text, canonical URLs, schema markup readiness
- **Integrating SEO into editorial workflow**: Want a perspective on SEO alongside copy review

## Do_Not_Use_When

- You need to know "what keywords rank" or "search volume for a term" → use Ahrefs, SEMrush, or Google Keyword Planner
- You need competitor analysis or SERP position data
- You're doing technical SEO at scale (page speed, Core Web Vitals, crawlability) → use Google Search Console, PageSpeed Insights, Screaming Frog
- You're building a keyword research or content calendar from scratch → start with keyword data tools first
- You want to know if content will rank → SEO ranking depends on E-E-A-T, backlinks, domain authority, and many other data signals this skill cannot assess

## Why_This_Exists

Content teams and product managers often prioritize **clarity, tone, and brand voice** (rightfully so) but deprioritize structural SEO because:

1. It's invisible to end users until it fails (orphaned page never discovered, perfect answer buried under three H3s)
2. Structural flaws compound: one bad H1 + missing internal links + no meta description = page that's well-written but unsearchable
3. Search intent misalignment is hard to spot without research: content sounds good but nobody was searching for that specific angle
4. Schema, accessibility, and technical SEO patterns get overlooked in text-focused workflows

This skill embeds that structural lens into editorial and product workflows **before** content ships.

## Companion_Skills

- **copy-critic**: General copy and tone review. SEO Advisor integrates as a perspective module.
- **copy-planner**: Content planning and narrative structure. SEO Advisor can guide topic cluster planning.
- **accessibility-advisor**: Covers screen readers and semantic HTML; this skill handles SEO-specific alt-text and structure.

## Steps

### Standalone Mode

When invoked with `/seo-advisor [content]`:

1. Extract metadata (title tag, meta description, target URL if provided)
2. Identify content type (blog post, landing page, product page, tutorial, reference)
3. Run full SEO review protocol (see below)
4. Output detailed review with CRITICAL/MAJOR/MINOR findings
5. Provide structured recommendations and optional perspective summary

### Perspective Module Mode

When invoked by copy-critic or another skill with `perspective: seo-advisor`:

1. Run abbreviated SEO review (phases 1–3, 8–10)
2. Output compact perspective format (see below)
3. Return to parent critic for synthesis

## Full_SEO_Review_Protocol

### Phase 1: Pre-Commitment Predictions

Before deep review, predict what SEO issues are likely based on content type:

- **Blog post/article**: Risk of orphaned content, weak internal linking, missed featured snippet opportunities
- **Landing page**: Risk of keyword stuffing, unclear intent, poor CTA alignment
- **Product page**: Risk of thin content, missing schema, poor mobile structure
- **Reference/documentation**: Risk of broken heading hierarchy, missing search intent, accessibility issues
- **Tutorial/how-to**: Risk of missing FAQ schema, poor step-by-step markup, no featured snippet optimization

### Phase 2: Search Intent Alignment Audit

**What query would bring someone to this page?**

- Is the content addressing informational intent (answering "how", "what", "why")?
- Is it addressing navigational intent (finding a specific brand/product)?
- Is it addressing transactional intent (buying, signing up)?
- Is it addressing commercial intent (comparing, researching before purchase)?

**Is intent matched early?**

- Does the first 100 words make the page's purpose and answer clear?
- Is there a clear thesis or value proposition in the opening?
- Would a searcher immediately recognize they're in the right place?

**Does content satisfy the implied question?**

- If the title poses a question, is it answered?
- Are supporting claims backed by evidence or examples?
- Does the conclusion reinforce the main answer?

**Findings to report:**
- Intent alignment: STRONG / MODERATE / WEAK
- Specific evidence (quote from opening, clarity of thesis)
- Risk if unaddressed: orphaned traffic, high bounce rate

### Phase 3: Title Tag & Meta Description Audit

**Title Tag Checklist:**
- [ ] Present and unique?
- [ ] <60 characters (optimal 50–55)?
- [ ] Includes primary topic or keyword?
- [ ] Compelling and natural language (not stuffed)?
- [ ] Matches page content?

**Meta Description Checklist:**
- [ ] Present and unique?
- [ ] 150–160 characters (shown fully on desktop and mobile)?
- [ ] Includes a call-to-action or value proposition?
- [ ] Matches title and page content?
- [ ] Avoids duplicate descriptions across pages?

**Findings to report:**
- Title tag: [present/missing], [too long/good/too short], [keyword presence: natural/stuffed/missing]
- Meta description: [present/missing], [length: good/too long/too short], [clarity: strong/vague]
- Alignment: [title ↔ meta ↔ content: aligned/misaligned]

### Phase 4: Heading Hierarchy Audit

**H1 Check:**
- Single H1 only (not zero, not multiple)?
- Describes the page's main topic?
- Natural, not keyword-stuffed?
- Matches title tag closely?

**Heading Structure Check (H1 → H2 → H3 → ...):**
- No skipped levels (e.g., H1 → H3)?
- Logical information hierarchy?
- Reader can understand page structure from headings alone?
- H2s support H1 thesis, H3s support H2 topics?

**Keyword Distribution in Headings:**
- Primary topic appears in H1 and 1–2 H2s?
- Natural language, not forced repetition?
- Variations of topic (synonyms, related terms) in supporting headings?

**Findings to report:**
- H1 status: [present/missing], [unique/multiple], [quality: clear/vague/stuffed]
- Hierarchy: [logical/broken], [example of issue if broken]
- Scanability score: [excellent/good/fair/poor]

### Phase 5: Content Structure for Discoverability

**Featured Snippet Opportunities:**
- Questions explicitly answered with direct sentences?
- Lists (ordered or unordered) that could appear as featured snippets?
- Tables, comparisons, or definitions?
- "How-to" steps formatted clearly?

Example: "What is X?" → content should have a 1–2 sentence answer in the first occurrence.

**FAQ Schema Potential:**
- Are there FAQ-style question-answer pairs in the content?
- Could questions be extracted and marked with schema?
- Is a dedicated FAQ section beneficial for this topic?

**Topic Completeness:**
- Does the content cover the topic thoroughly or just surface-level?
- Missing important subtopics (would link to cluster pages)?
- Appropriate depth for content type (tutorial vs. overview)?

**Freshness & Authority Signals:**
- Dates or "updated on" markers?
- Sources or citations?
- Expert credentials or author info?

**Findings to report:**
- Featured snippet readiness: [high/medium/low], [example opportunities]
- FAQ potential: [strong/moderate/weak]
- Completeness: [comprehensive/good/thin/gaps: {list}]

### Phase 6: Internal Linking Audit

**Existing Internal Links:**
- Does content link to related pages on the same site?
- Are links descriptive (e.g., "advanced topic cluster patterns" vs. "click here")?
- Orphaned content risk: Is THIS page linked TO from other pages?

**Topic Cluster Structure:**
- Does this page fit into a larger cluster strategy?
- Should it link to a pillar page or other cluster pages?
- Are backlinks from cluster pages present?

**Link Density & Freshness:**
- Too few links (content is isolated)?
- Too many links (looks like spam)?
- Links point to outdated or broken pages?

**Findings to report:**
- Link count and quality: [X internal links], [anchor text quality: good/generic/stuffed]
- Orphaned risk: [high/low], [evidence: does page link out more than it's linked to?]
- Cluster fit: [strong/unclear/missing connections]

### Phase 7: Technical SEO Patterns

**Image Alt-Text:**
- All images have descriptive alt-text?
- Alt-text describes image content, not "image of" or "picture"?
- Keyword stuffing in alt-text avoided?

**URL Structure:**
- URL is descriptive and human-readable?
- Includes primary topic/keyword naturally?
- Avoids dates, parameters, or cryptic IDs?
- Canonical URL needed (duplicate content)?

**Accessibility in Content Structure:**
- Content is readable and well-formatted?
- No walls of text without headings?
- Lists and tables used when appropriate?
- Emphasis (bold, italics) used for semantics, not style?

**Mobile-Friendliness Signals:**
- Content is readable on narrow screens?
- Images and tables don't break layout?
- No large unoptimized images (would slow page load)?

**Findings to report:**
- Alt-text: [complete/missing images: {count}], [quality: descriptive/generic/stuffed]
- URL: [descriptive/vague], [canonical considerations: yes/no]
- Accessibility: [good/fair/issues: {list}]
- Mobile signals: [favorable/concerns: {list}]

### Phase 8: Multi-Perspective Review

**Search Engine Crawler Lens:**
- Can the crawler understand what this page is about?
- Is there a clear single topic or keyword focus?
- Are there duplicate content risks?

**Human Searcher Lens:**
- Would I click on this in search results based on title + meta?
- Would I feel satisfied that this page answers my question?
- Is the content scannable or do I need to read everything?

**Content Strategist Lens:**
- Does this page fit into a content marketing strategy?
- Does it drive awareness, consideration, or conversion?
- Are there clear next-step links (topic cluster)?

**Accessibility Auditor Lens:**
- Can screen reader users understand the page structure?
- Is alt-text sufficient for visually impaired users?
- Are headings semantic and in logical order?

**Findings to report:**
- Crawler understanding: [clear/ambiguous], [evidence]
- Searcher satisfaction: [likely/uncertain], [why]
- Strategic fit: [strong/weak]
- Accessibility: [good/fair/issues]

### Phase 9: Gap Analysis + Self-Audit + Realist Check

**What's Missing (Structural SEO Perspective):**

- No title tag or vague title tag (vs. SEO best practice)?
- Meta description missing or exceeds limits?
- Multiple H1s or no H1?
- Orphaned page (no internal links)?
- No featured snippet opportunity identified?
- Missing alt-text on key images?
- Search intent misaligned in opening 100 words?
- Content too thin or doesn't cover topic adequately?
- No internal linking strategy evident?
- Heading hierarchy skips levels?

**Realist Check (Avoid False Positives):**
- Is perfect heading structure actually possible given the content type?
- Are we being too strict about keyword distribution?
- Is the lack of a featured snippet actually a problem for this content type?
- Does the content need 50 internal links or is 3–5 enough for this page type?

**Self-Audit:**
- Am I confusing "structurally sound SEO" with "will rank for X keyword"?
- Have I avoided claiming keyword data I don't have?
- Are my recommendations actionable without a keyword tool?

### Phase 10: Synthesis

**Severity Scale:**

- **CRITICAL**: Page would be fundamentally undiscoverable
  - Examples: No H1, missing title tag, content doesn't match any search intent, complete duplicate content
  - Action: Must fix before publishing

- **MAJOR**: Significantly limits discoverability
  - Examples: Broken heading hierarchy, meta description exceeds limits, no internal links, keyword stuffing
  - Action: Should fix before publishing

- **MINOR**: Missed optimization opportunities
  - Examples: Alt-text could be better, anchor text is generic, FAQ could use schema, URL could be more descriptive
  - Action: Fix in next cycle or during content refresh

**Output Structure:**

```
## Review Summary

**Content Type:** [inferred]
**Search Intent:** [informational/navigational/transactional/commercial] — [1 sentence why]
**Structural SEO Health:** [STRONG/MODERATE/WEAK]

## Findings by Severity

### CRITICAL [if any]
- [Issue]: [specific evidence from content], [why it matters]

### MAJOR [if any]
- [Issue]: [specific evidence], [impact]

### MINOR [if any]
- [Issue]: [evidence], [recommendation]

## What's Missing

[Bulleted list of 3–5 top gaps that would improve SEO structure]

## Recommendations

[Prioritized list of 3–5 actionable fixes, ranked by impact]

## Perspective Module Output [if requested]

**SEO Perspective:**
- Intent alignment: [STRONG/MODERATE/WEAK] — [1 sentence why]
- Structural SEO: [X issues found] — [top 2 bullet points]
- Discoverability: [GOOD/FAIR/POOR] — [1 sentence assessment]
- Key recommendation: [single most important fix]
```

## Perspective_Module_Output_Format

When invoked by copy-critic or another skill with `perspective: seo-advisor`, output only:

```
**SEO Perspective:**
- Intent alignment: [STRONG/MODERATE/WEAK] — [1 sentence describing what the content is trying to answer and whether it's clear]
- Structural SEO: [X critical/major issues found] — [top 2 most impactful problems]
- Discoverability: [GOOD/FAIR/POOR] — [1 sentence overall assessment]
- Key recommendation: [single most important fix to improve SEO structure]
```

This compact format integrates cleanly into parent critic reviews without overwhelming the synthesis.

## Tool_Usage

**Allowed tools:** Read (for analyzing provided content files)

**Disallowed tools:** Write, Edit (this skill is read-only)

If you need to modify content based on SEO feedback, the parent workflow (e.g., copy-critic + editor) will handle that.

## Examples

### Example 1: Blog Post Intent Misalignment

**Input:**
```
Title: Advanced Python Decorators Guide
Meta Description: Learn Python decorators in 5 minutes
H1: Python Decorators

[Content covers advanced decorator patterns, monkey patching, functools—assumes reader knows decorators]
```

**SEO Advisor Output:**
```
**MAJOR: Search Intent Mismatch**
- Title and meta promise "5 minutes" (navigational/tutorial intent)
- Content delivers advanced patterns (commercial/reference intent)
- Opening paragraph lacks explanation of what decorators are—would confuse beginners
- Risk: High bounce rate, poor engagement for target audience

**Recommendation:**
Either retarget as "Advanced Python Decorators" OR rewrite opening to cover basics first.
```

### Example 2: Heading Hierarchy Broken

**Input:**
```
H1: Complete Guide to Topic Modeling
H2: Introduction
H3: Why This Matters
H2: Core Algorithm
H4: Mathematical Notation
H2: Applications
```

**SEO Advisor Output:**
```
**MAJOR: Heading Hierarchy Skip**
- H4 appears under H2 without H3 bridge
- Reader cannot scan structure from headings alone
- Crawler may misunderstand content relationships

**Recommendation:**
Change H4 "Mathematical Notation" to H3, or move it under a new H3 subheading.
```

### Example 3: Structural SEO Strengths

**Input:**
```
Title: How to Set Up a Paperless Home Office [50 chars]
Meta: Complete guide to going digital at home. Save time, reduce clutter. Get started today. [147 chars]
H1: How to Set Up a Paperless Home Office

H2: Benefits of Going Paperless
H2: Tools You'll Need
H3: Document Management Software
H3: Scanning Hardware
H2: Step-by-Step Setup Process
H3: Step 1: Sort and Scan
H3: Step 2: Organize Files
H3: Step 3: Configure Backup

[Content covers topic thoroughly, includes 8 internal links to related guides, all images have alt-text]
```

**SEO Advisor Output:**
```
**STRONG Structural SEO**
- Title and meta aligned, within length limits, compelling CTA
- Single H1, clear H2→H3 hierarchy, scannable structure
- Step-by-step format suitable for featured snippet
- 8 internal links contextualized with descriptive anchor text
- All images have semantic alt-text

**Minor Gaps:**
- No FAQ section (opportunity: "How long does setup take?", "What if I don't have a scanner?")
- No "updated" date signal (consider adding)

**Perspective Summary:**
- Intent alignment: STRONG — directly answers "how to set up"
- Structural SEO: 0 critical/major issues — 2 minor optimization gaps
- Discoverability: GOOD — well-structured for search
- Key recommendation: Add FAQ schema for 2–3 common questions
```

## Notes

### Scope Limitations

This skill reviews **structural SEO and intent alignment only**. It does NOT:

- Predict rankings or traffic based on keyword difficulty
- Analyze SERP results or competitor content
- Recommend specific keywords to target (requires keyword research data)
- Assess page speed, backlink profiles, or domain authority
- Make claims about what "will rank"

If you need data-driven SEO work, provide keyword research, SERP analysis, or competitive intelligence tools. This skill works best in workflows where content decisions are made first, then SEO structure is reviewed before publishing.

### Integration with Other Skills

**With copy-critic:**
- copy-critic handles tone, clarity, brand voice
- SEO Advisor handles structural search quality and intent
- Both review independently; synthesis happens in copy-critic output

**With copy-planner:**
- copy-planner guides content scope and narrative
- SEO Advisor verifies structural soundness for search discoverability
- Together they ensure content is both well-planned and discoverable

**With accessibility-advisor:**
- accessibility-advisor covers WCAG compliance and semantic HTML
- SEO Advisor covers SEO-specific alt-text and structure for search
- No overlap; complementary perspectives

### When to Invoke

Use `/seo-advisor` in these scenarios:

1. **Content draft review** (before final publish): `You're right, let me run this through SEO Advisor.`
2. **Topic cluster planning**: `SEO Advisor can verify that these pages link properly and cover the right scopes.`
3. **Landing page optimization**: `Let me get an SEO perspective on this CTA and meta description alignment.`
4. **Content inventory audit**: `Running SEO Advisor on key pages to identify structural gaps.`
5. **Editorial workflow integration**: Ask copy-critic to include SEO perspective on all posts.

### Avoiding Over-Indexing on Data You Don't Have

If a user asks "Will this content rank?" or "What keywords should we target?", this skill must:

1. **Acknowledge the request**: "I see you want to know ranking potential..."
2. **Clarify scope**: "I can review structural SEO, but I can't predict rankings without knowing competition, domain authority, backlinks, etc."
3. **Redirect**: "For that, you'd need SEMrush, Ahrefs, or Google Search Console data. Once you have a target keyword, I can verify the content is structurally optimized for it."

This prevents false authority claims and keeps users from treating structural review as keyword research.

---

**Version:** 1.0
**Last Updated:** 2026-03-09
**Perspective Module Compatible:** Yes
**Standalone Ready:** Yes
