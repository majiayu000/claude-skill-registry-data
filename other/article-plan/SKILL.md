---
name: article-plan
description: Strategically plan a single evergreen article — pillar assignment, keyword targeting, section outline, source references, internal link targets, and CTA. Run this before article-author when you want to align on strategy before writing. Use when deciding what to write or how to structure a specific article.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Plan an evergreen article about: $ARGUMENTS

$ARGUMENTS should be a topic, concept, or keyword. If none given, ask what article to plan.

---

## What This Skill Produces

A complete article brief that can be handed directly to `article-author`. It covers:
1. Pillar assignment and article tier
2. Primary keyword + semantic variants
3. Full section outline with H2/H3 structure
4. Target word count
5. Source references to pull (which materials, which sections)
6. Internal link targets (pathways, courses, related articles)
7. CTA target
8. Meta title + description
9. URL slug
10. Competitor landscape notes

---

## Step 1 — Assign to a Pillar

Every article lives in exactly one content pillar. Assign based on the primary concept being explored.

Read the pillar definitions from {{CONFIG_PATH}} or {{BRAND_CONFIG}} to determine which pillars exist. Each pillar should have:
- A **core question** it answers
- **Flagship concepts** associated with it

Then assign an article tier:

| Tier | Type | Word Count | Competition |
|------|------|------------|-------------|
| **Tier 1 — Pillar Page** | Broadest term in the pillar | 3,500-4,500 | High |
| **Tier 2 — Cluster Article** | Specific facet within the pillar | 2,200-3,200 | Medium |
| **Tier 3 — Long-tail** | Narrow, high-intent question | 1,500-2,200 | Low |

**Rule:** Each pillar should have exactly one Tier 1 pillar page. Cluster articles link up to it. Long-tail articles link up to cluster articles.

---

## Step 2 — Keyword Strategy

**Primary keyword:** The exact phrase your target audience would type into Google or ask an AI.
- Should be 2-5 words
- Should reflect real search intent (informational or definitional)

**Semantic variants (3-5):** Related phrases that should appear naturally in the article body.
- Synonyms, related frameworks, question variants

**GEO-priority terms:** Phrases AI systems are likely to be asked. Include these in the Definition Anchor section specifically.
- Usually the most literal "what is X" form
- Include {{AUTHOR_NAME}} + the concept for entity disambiguation in AI citation

---

## Step 3 — Section Outline

Generate a complete H2/H3 outline. H2s are the major sections; H3s are sub-facets within them. Headlines should mirror real search queries where possible.

**Mandatory sections (all articles):**

1. **[Opening/Hero]** -- No heading. Question, reframe, or tension. Primary keyword in first 100 words.
2. **What Is [Term]?** -- H2 -- GEO-optimized definition anchor
3. **Why This Matters / The Problem** -- H2 -- stakes, diagnosis, historical parallel
4. **[Core Teaching -- 2-3 H2s]** -- Main framework content, H3s within each
5. **Common Misunderstandings About [Term]** -- H2 -- 2-3 H3s (high GEO value)
6. **[Foundational Evidence]** -- H2 -- supporting evidence woven into argument (can merge with core teaching for Tier 3)
7. **What This Means in Practice** -- H2 -- application, earned after depth
8. **[How This Connects]** -- H2 -- optional for cluster; required for pillar pages
9. **[CTA section]** -- No heading or soft H2 -- invitation to go deeper

**For the Core Teaching H2s:** Write them as questions or strong declarative statements that would appear in "People Also Ask" results. Each H2 is a distinct facet of the concept, not just a continuation.

**FAQ section (optional but high GEO value):** 3-5 Q&A pairs at the end. These are what AI systems pull verbatim.

---

## Step 4 — Source References

Based on the pillar and topic, identify which source materials to pull from. Reference {{CONTENT_CORPUS}} to determine available materials.

List the 3-6 specific sections most likely to contain what's needed. The `article-corpus` skill (if available) will retrieve the actual passages.

---

## Step 5 — Internal Link Targets

Check for existing content to link to. Search:
- Existing page routes in the site structure
- Pathways: look for pathway pages related to this pillar
- Courses: look for course slugs in the same pillar
- Related articles: other articles in the same cluster

**Minimum internal links per article:**
- Tier 1 (Pillar Page): 5-8 internal links (to cluster articles, pathways, courses)
- Tier 2 (Cluster): 3-5 internal links (up to pillar page, sideways to related clusters, forward to pathway/course)
- Tier 3 (Long-tail): 3-4 internal links (up to cluster, forward to pathway)

---

## Step 6 — CTA Target

Every article has exactly one primary CTA. Priority order:
1. If a pathway exists for this pillar/topic -- link to the pathway (lower friction)
2. If no pathway but a course exists -- link to the course
3. If neither -- note that a pathway needs to be created before this article publishes

---

## Step 7 — Meta and URL

**URL slug rules:**
- Short, keyword-anchored, no stop words
- Lead with the keyword: `/what-is-[term]`, `/[concept-name]`
- All lowercase, hyphens, no underscores
- Max 5 words

**Meta title (50-60 chars):**
- Lead with keyword
- End with `-- {{AUTHOR_NAME}}` or `| {{SITE_NAME}}`

**Meta description (140-160 chars):**
- Include primary keyword
- Contain a question or tension (drives CTR)
- Preview the value ("Discover how...", "Learn why...", "Explore...")

---

## Output Format

Return the complete article brief as:

---

# Article Brief: [Working Title]

**Pillar:** [pillar name]
**Tier:** [1 / 2 / 3]
**Primary keyword:** [exact phrase]
**Semantic variants:** [3-5 phrases]
**Target word count:** [range]
**URL slug:** `/[slug]`
**Meta title:** [50-60 chars]
**Meta description:** [140-160 chars]

---

## Section Outline

**[Opening -- no heading]**
Reframe or tension: [brief note on the opening approach]

**H2: What Is [Term]?**
Definition anchor -- GEO-optimized, ~[word count] words

**H2: [Stakes/Problem heading]**
[Note on approach -- Diagnosis/Historical Parallel]
  - H3: [specific sub-point]
  - H3: [specific sub-point]

**H2: [Core Teaching 1]**
[Note on what this covers]
  - H3: [sub-facet]
  - H3: [sub-facet]

**H2: [Core Teaching 2]** (if needed)
  - H3: [sub-facet]

**H2: Common Misunderstandings About [Term]**
  - H3: [Misunderstanding 1]
  - H3: [Misunderstanding 2]
  - H3: [Misunderstanding 3]

**H2: [Foundational Evidence or integrated into core]**

**H2: What This Means in Practice**

**[CTA section]**

**FAQ** (optional, 3-5 Q&A pairs)

---

## Source References

*Materials to pull from (run article-corpus for passages if available):*
- [Source identifier] -- sections [list]: [reason]
- [Source identifier] -- sections [list]: [reason]

---

## Internal Link Targets

- [page/pathway/course title] -- `[/route]` -- link in [section]
- [page/pathway/course title] -- `[/route]` -- link in [section]

**CTA target:** [pathway or course name] -- `[/route]`

---

## Notes for Writer

[Any strategic notes: tone considerations, angle differentiation from competitors, specific stories to include, known quotes to feature, warnings about what to avoid]
