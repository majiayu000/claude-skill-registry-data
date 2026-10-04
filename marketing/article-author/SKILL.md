---
name: article-author
description: Write a complete evergreen pillar article in the author's voice — with source research, full SEO/GEO architecture, and proper citations. This is the main writing skill. It runs planning, corpus research, and writing in sequence. Use when writing any new article for the platform.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

Write an evergreen article about: $ARGUMENTS

$ARGUMENTS should include the topic and optionally: pillar, tier (1/2/3), target keyword, style variant, or an existing article-plan brief to execute. If a brief is provided, skip to Step 3. If only a topic is given, run the full flow.

---

## Step 1 — Strategic Plan

Before writing, establish the brief. If an `article-plan` brief was provided in $ARGUMENTS, use it directly and skip to Step 3.

Otherwise, run the planning logic from `article-plan`:

**Assign pillar** — Read pillar definitions from {{CONFIG_PATH}} or {{BRAND_CONFIG}} to determine which pillar this topic belongs to.

**Assign tier:**
- Tier 1 (Pillar Page): Broadest term in the pillar -- 3,500-4,500 words
- Tier 2 (Cluster): Specific facet -- 2,200-3,200 words
- Tier 3 (Long-tail): Narrow, high-intent -- 1,500-2,200 words

**Establish keywords:** Primary keyword + 3-5 semantic variants. Include "{{AUTHOR_NAME}} [concept]" as a GEO disambiguation variant.

**Draft the outline** using the section architecture in Step 3.

---

## Step 2 — Source Research

Before writing, pull relevant passages from {{CONTENT_CORPUS}}. This grounds the article in the author's actual words and enables proper citations.

### Source material path:
`{{CORPUS_PATH}}`

### Research process:
1. Identify the most relevant source files before reading full content:
   - Glob for available source files
   - Grep for the topic keyword across those files
2. Read the 3-6 most relevant sections in full (not every section -- be selective)
3. Extract:
   - **Direct quotes** (2-5 sentences; verbatim; strong enough to blockquote)
   - **Definitional passages** (crisp enough to be GEO-quoted)
   - **Framework explanations** (how the author explains the concept step by step)
   - **Stories and historical examples** used in context
4. Note the citation for each extract with full attribution

**Citation format:** `**Source:** [Source Title] -- [Section/Chapter Reference]`
Never invent quotes. If paraphrasing, mark it as such.

---

## Step 3 — Write the Article

Write the complete article in markdown following this exact section architecture. All sections are mandatory unless marked optional.

### Author Voice (Apply to Every Section)

Read {{VOICE_GUIDE}} for the author's voice markers and apply them consistently throughout.

Key voice principles:
- Maintain the author's characteristic rhetorical posture and tone
- Use the author's signature vocabulary and metaphor systems
- Follow the author's typical argument structure and idea progression
- Avoid vocabulary or phrasing patterns flagged as off-brand in the voice guide

**Order of ideas:** Reframe -- Meaning -- Depth -- Complexity -- Implication. Application is earned, not appended.

---

### Section 1: Opening Hook (150-250 words, no heading)

- Opens with a **question, reframe, or productive tension** -- never a standalone quote, never a thesis statement
- Primary keyword appears naturally within the first 100 words
- Establishes why this matters NOW -- urgency, not academic framing
- The author's posture: speaking from experience and conviction
- Sets up the Definition Anchor naturally ("So what exactly is..." or a reframe that demands definition)

---

### Section 2: What Is [Term]? (200-350 words)
**H2: "What Is [Term]?"** -- exact match to primary search query

This is the **GEO anchor section**. Write it to be quotable as a standalone -- AI systems will pull this paragraph.

Structure:
- **Opening definition sentence:** Crisp, complete, 20-30 words. "[Term] is [X]." Not vague.
- **Expand the definition:** 3-4 sentences unpacking what the definition means and why it's richer than it sounds
- **Situate in framework:** 2-3 sentences connecting it to the broader framework ecosystem
- **GEO disambiguation line:** "{{AUTHOR_NAME}} coined/developed [term] in [source/year] as a framework for..." -- helps AI attribute correctly

Tone: Definitional precision + the author's natural register. More clarity here, less intensity -- that comes later.

If the term has components (e.g., an acronym or a numbered list of elements), name them here but don't define each yet -- that's Core Teaching.

---

### Section 3: Why This Matters — The Problem (250-400 words)
**H2:** Question or declarative that names the stakes (e.g., "Why This Can't Be Ignored", "What We've Lost -- and Why It Matters")

This is the **Diagnosis section**. Name what has been lost, reduced, or overlooked.

- Follow with a **historical parallel or case study** -- with specific data, not vague generalities
- Draw the transferable principle from the example
- Close with the implication: this is not an academic problem, it's a lived reality

Do NOT rush to solution here. Sit with the problem. Application is earned later.

---

### Section 4: Core Teaching (600-1,200 words, 2-4 H2s with H3s inside)

The substantive framework content. This is where source material is most heavily drawn upon.

**Structural rule:** Each H2 is a distinct facet of the concept -- not "Part 1, Part 2" but genuinely different angles. H3s are sub-points within each.

**Headline rule:** H2s should mirror questions people actually ask. Imagine the "People Also Ask" box for your primary keyword.

**Pattern to use:**
- **Pattern A:** Reframe -- Ground in example -- Extract principle -- Connect to framework -- Land with implication
- **Pattern B:** Story -- Tension -- Evidence woven -- Resolution -- Application preview
- Choose the pattern that fits; patterns can nest across the H2s

**Source citations:** This is where pulled passages go. Use blockquotes for direct quotes:
> "Verbatim quote..." -- *Source Title*, [Section Reference]

For paraphrases, close-reference: `(Drawing from *Source Title*, [Section Reference])`

**Metaphor density:** Actively embed the author's signature metaphor systems. Reference {{VOICE_GUIDE}} for the preferred metaphor domains.

**Evidence/scripture/data:** Woven where it clarifies, not where it proves. No stacked quotations.

**If the concept has enumerable components** (e.g., an acronym or a numbered framework): define each within H3s, but make them feel like a developing argument, not a glossary. Use transitional sentences that build forward.

---

### Section 5: Common Misunderstandings (300-500 words)
**H2: "Common Misunderstandings About [Term]"** or "What [Term] Is NOT"

2-3 H3s, each one:
- Names the misunderstanding directly (readers recognize themselves)
- Opens into the fuller, richer understanding ("The fuller reality is...")
- First-person voice: "I've encountered this confusion again and again..."

**Why this section matters:** Highest GEO value after the Definition Anchor. AI systems pull disambiguation content. Featured snippet territory for Google.

Name the misunderstanding, then expand the reality. Say "[Term] tends to flatten into [reduction]. The fuller reality is [expansion]."

---

### Section 6: Foundational Evidence (200-350 words)
**H2:** Something specific and grounded (e.g., "The Research Behind [Term]", "What the Evidence Shows")

- 1-2 key evidence points -- introduced because they clarify, not prove
- Brief insight connecting the evidence to the concept
- Historical or etymological note where relevant
- This is argument, not lecture.

*This section can be integrated into Core Teaching for Tier 3 articles where length requires it.*

---

### Section 7: What This Means in Practice (250-400 words)
**H2:** Something actionable but not prescriptive (e.g., "What This Opens Up", "Living Into [Term]")

- Application is **earned here** -- this section is paid for by everything above it
- Direct address: "you" and "we" -- second person deliberately
- Not a list of steps. Prose with embedded implications.
- Challenge woven in: "What would it mean if your community/organization took this seriously?"
- Practical enough to be actionable; expansive enough to feel like vision

---

### Section 8: How This Connects (150-250 words) — Required for Tier 1, optional for Tier 2/3
**H2:** "How [Term] Connects to [Related Framework/Concept]"

- Shows where this concept sits in the broader framework ecosystem
- 2-3 internal links with natural anchor text to related articles, pathways, courses
- "If this resonated, the natural next layer is..." -- invitational forward movement

---

### Section 9: Formation Invitation / CTA (100-200 words, no heading or soft H2)

- Warm, invitational close -- not a sales pitch
- "If you want to go deeper with this..." -- link to pathway or course (one CTA only)
- Ends with an **open question or challenge** -- leaves productive tension

---

### FAQ Section (Optional — High GEO Value, 200-400 words)

If included, place at the very end. 3-5 Q&A pairs.

Format:
**Q: [Question people actually ask -- exact phrasing]**
A: [2-5 sentence answer in the author's voice -- complete and self-contained, GEO-ready]

Best FAQ questions:
- "What does [term] mean?"
- "What is the difference between [term] and [related term]?"
- "How do you apply [term] in practice?"
- "Who developed the [term] framework?"
- "What is {{AUTHOR_NAME}}'s view on [topic]?"

---

## Step 4 — SEO/GEO Final Check

Before delivering, verify:

**SEO:**
- [ ] Primary keyword in: H1 (article title), first 100 words, at least one H2, meta title, meta description
- [ ] 3-5 semantic variants woven naturally (not stuffed)
- [ ] H2/H3 headlines mirror search intent questions
- [ ] Internal links: minimum 3 (to related articles/pathways/courses), maximum 8
- [ ] Meta title: 50-60 chars, leads with keyword, ends with `-- {{AUTHOR_NAME}}`
- [ ] Meta description: 140-160 chars, includes keyword, contains question/tension
- [ ] URL slug: short, keyword-anchored, no stop words, all lowercase with hyphens

**GEO:**
- [ ] Definition Anchor (Section 2) is clean, complete, and quotable as a standalone
- [ ] "{{AUTHOR_NAME}} [concept]" disambiguation phrase present
- [ ] Factual specificity in examples (numbers, dates, locations -- not vague)
- [ ] Direct quotes from source material present with citations
- [ ] FAQ section included (or note that it should be added before publishing)
- [ ] Author byline references {{AUTHOR_NAME}} and {{ORGANIZATION_NAME}}

**Voice:**
- [ ] All voice markers from {{VOICE_GUIDE}} present and at target levels
- [ ] No off-brand vocabulary or phrasing patterns (check failure modes in voice guide)
- [ ] Application appears after meaning and depth (Section 7, not before Section 4)
- [ ] First-person narrative present (minimum 2 instances)
- [ ] Ends with challenge or open question
- [ ] Overall voice coherence at target threshold

---

## Output Format

Deliver the article as:

```
---
title: [Full article title]
slug: /[url-slug]
pillar: [pillar name]
tier: [1/2/3]
primary_keyword: [keyword]
meta_title: [50-60 chars]
meta_description: [140-160 chars]
word_count: [approximate]
sources_cited: [list of sources used]
cta_target: [pathway or course slug]
---

[Full article content in markdown]
```

If saving to a file: `{{CONTENT_OUTPUT_PATH}}/articles/[slug].md`

Always ask before writing to a file if the destination is unclear.
