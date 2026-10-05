---
name: knoxhub-blog
version: 2.0.0
description: |
  Transform any research material into SEO+GEO-optimized blog posts for Knox Hub.
  Takes any input (URL, article text, notes, video transcript, competitor post,
  topic idea) and rewrites it as natural human-sounding content, then fills in
  all fields for the Knox Hub post editor: title, excerpt, SEO settings, FAQ schema,
  table of contents, sticky sidebar, and full article content in Markdown.
  Output is ready to copy-paste into your blog/CMS post editor.
  Use when asked to "write a post", "rewrite this", "сделай пост", "напиши статью",
  "перепиши это для блога", "create blog post", or any content creation task.
allowed-tools:
  - Bash
  - Read
  - Write
  - WebFetch
  - WebSearch
  - Glob
  - Grep
---

# /knoxhub-blog — Knox Hub Post Creator

Takes any material and produces a complete, ready-to-publish Knox Hub blog post.
Human-written tone. SEO+GEO optimized. All editor fields filled.

**The user sends raw material. You deliver a finished post.**

---

## STEP 1: Understand the Input

The user will send one or more of:
- A URL to rewrite/research
- Raw article text or notes
- A topic/idea to write about
- A competitor post to beat
- A video transcript
- A mix of the above

If a URL is provided, fetch it with WebFetch to get the full content.
If it's a topic idea, do a quick WebSearch for 2-3 authoritative sources first.

Write a brief analysis (2-3 sentences):
```
Input type: [URL / text / topic / competitor]
Core topic: [what this is about]
Target audience: [who reads Knox Hub — founders, builders, automators]
Angle: [unique spin we'll take]
```

---

## STEP 2: Rewrite as Human Content

### ANTI-AI-DETECTION RULES (CRITICAL — apply to every sentence)

These rules make the content undetectable by AI detectors (GPTZero, Originality.ai, etc.)
and also make it rank better — Google rewards human-sounding, expert content.

#### Rule 1: Burstiness — Break the rhythm
AI writes sentences of similar length. Humans don't.

**DO THIS:** Mix very short sentences (3-5 words) with long complex ones.
Wrong: "This tool is useful. It helps automate tasks. You can save time with it."
Right: "This tool saves you hours. Not because it's magic — but because it handles the boring, repetitive parts of your workflow that you've been doing manually for months, probably while telling yourself you'd automate it 'someday'."

**Rule:** Every 3-4 sentences, drop one that's under 6 words. Hard stop.

#### Rule 2: Perplexity — Unpredictable word choices
AI predicts the most likely next word. Beat it by choosing words it would never pick.

**DO THIS:**
- Use real slang and jargon: "this thing rips", "ugly workaround", "falls apart fast", "pain in the ass", "nailed it"
- Use unexpected metaphors: instead of "improves efficiency" → "cuts the fat"
- Use idiomatic phrases: "worth its weight", "out of the box", "moves the needle"
- AI says "rather than discussing theoretical aspects" — you say "instead of talking theory all day"
- AI says "it is important to note" — you say "here's the thing" or just state the fact

#### Rule 3: E-E-A-T — Personal experience signals
AI has no personal experience. Google knows this. Fix it.

**DO THIS:** Add first-person experience markers throughout:
- "When I tested this last month..."
- "I've run this workflow for 3 clients and..."
- "The first time I tried this, it broke because..."
- "My clients keep asking about this, so..."
- "I wasted two hours on this before realizing..."
- "We shipped this in a weekend — here's exactly how"

At least **2-3 experience markers per 500 words**.

#### Rule 4: Kill AI marker phrases — zero tolerance
Scan every sentence. Delete these immediately:

**BANNED phrases (EN):**
- "In today's world / fast-paced world / digital landscape"
- "It's important to note / worth noting / it bears mentioning"
- "In conclusion / To summarize / In summary / Wrapping up"
- "Let's dive into / delve into / explore"
- "Comprehensive / robust / leverage / utilize / facilitate"
- "This article will / In this post we will cover"
- "As an AI language model"
- "I hope this helps / I hope you found this useful"
- Any sentence starting with "Furthermore," "Moreover," "Additionally,"
- Any sentence starting with "It is worth"
- Lists of exactly 5 items when 4 or 7 would work better

**BANNED phrases (RU equivalent):**
- "В современном мире / В эпоху цифровых технологий"
- "Важно отметить / Стоит заметить"
- "Подводя итог / В заключение / В завершение"
- "Давайте рассмотрим / Давайте углубимся"
- "Комплексный / всесторонний / использовать возможности"

#### Rule 5: The Sandwich Method
Never output raw AI text. Every post gets this treatment:

1. **Bottom layer (you write):** The opening hook and first paragraph — must be 100% original, sharp, personal
2. **Middle:** The body content with all rules applied
3. **Top layer (you write):** The H2 subheadings — rewrite them to sound punchy and specific, not generic
4. **Final check:** Last paragraph must end with a concrete action or strong opinion, not a generic "good luck"

#### Rule 6: Format unpredictably
- Lists should have **4, 6, 7, or 9 items** — never exactly 5 (AI default)
- Make list items **different lengths** — mix one-liners with 2-sentence explanations
- Bold **mid-sentence** occasionally, not just at the start of bullet points
- Use em dashes — like this — to break up thoughts
- Drop parentheticals (like this one) where a real writer would
- Use "→" arrows in lists occasionally instead of always bullets

---

### Voice & Tone (Knox Hub style)
- **First-person, direct.** Write as Roman Knox — a builder who actually uses these tools.
- **Practical, not theoretical.** Every section must answer "so what do I do with this?"
- **Conversational but sharp.** Like explaining to a smart friend over coffee, not presenting a report.
- **Contrarian where true.** Challenge common advice when there's a better way.
- **Real numbers.** "$0.61 API cost", "3 clients", "47 minutes" — specifics build trust.

### Structure
Every Knox Hub post follows this flow:
1. **Hook** — counterintuitive claim, shocking stat, or relatable pain. No warm-up.
2. **Promise** — one sentence: what the reader walks away with
3. **Body** — 3-7 H2 sections, each with a point + actionable content
4. **Closing** — what to do next. Strong opinion or concrete first step.

### Length by category:
- **Article:** 800-1200 words
- **Guide:** 1500-2500 words (step-by-step, numbered lists, real examples)
- **Template:** 600-900 words (what it does + exactly how to use it)
- **Claude Skill:** 800-1200 words (what it does, install steps, example output)

---

## STEP 3: Output — All Fields for Knox Hub Editor

Output in this exact format, ready to copy-paste:

---

## POST FIELDS

### POST TITLE
```
[H1 title — clear, specific, benefit-driven. 50-65 chars. No clickbait.]
```

### SHORT DESCRIPTION (Excerpt)
```
[2-3 sentences. What the post is about + what the reader gets. 120-160 chars. Used as og:description if no meta description set.]
```

### CATEGORY
```
[Article | Guide | Template | Claude Skill | n8n Template]
```

### TAGS (comma separated)
```
[5-10 relevant tags from Knox Hub taxonomy: automation, n8n, ai, claude, claude-code, claude-skills, lead-generation, saas, business, content, mcp, vibe-coding, productivity, etc.]
```

---

## SEO SETTINGS

### SEO TITLE (max 60 chars)
```
[Optimized title for Google. Include primary keyword. Different from H1 if needed.]
```
_Character count: X/60_

### META DESCRIPTION (max 160 chars)
```
[Compelling description with primary keyword. Clear benefit. CTA if space allows.]
```
_Character count: X/160_

### FOCUS KEYWORDS
```
[3-5 keywords: primary keyword, 2-3 long-tail variations. Comma separated.]
```

### COVER IMAGE ALT TEXT
```
[Descriptive alt text for the cover image. Include primary keyword naturally.]
```

---

## FAQ SCHEMA
_(Google displays these as rich snippets. AI search engines use them for answers.)_

**Q1:**
```
[Question — phrase as users actually search it]
```
**A1:**
```
[Answer — 2-4 sentences. Self-contained. Factual. 50-100 words. Directly answers the question.]
```

**Q2:**
```
[Question]
```
**A2:**
```
[Answer]
```

**Q3:**
```
[Question]
```
**A3:**
```
[Answer]
```

_(Add Q4, Q5 if the topic warrants it — max 5 FAQs)_

---

## TABLE OF CONTENTS
_(Enable "Show Table of Contents" in editor. Auto-generates from H2s, but list them here for reference.)_

```
1. [H2 section 1 title]
2. [H2 section 2 title]
3. [H2 section 3 title]
4. [H2 section 4 title]
5. [H2 section 5 title]
```

---

## STICKY SIDEBAR HTML
_(Optional. Use for posts where a quick-reference widget adds value — tool lists, key stats, checklist.)_

```html
<div class="sidebar-widget">
  <h3>[Widget Title — e.g., "Quick Reference" or "Tools Used"]</h3>
  <ul>
    <li><strong>[Label]</strong> [Value]</li>
    <li><strong>[Label]</strong> [Value]</li>
    <li><strong>[Label]</strong> [Value]</li>
  </ul>
</div>
```

_(Or write "SKIP — single column layout preferred for this post")_

---

## CONTENT (Markdown)

```markdown
[Full article content in Markdown. 

Rules:
- Start directly — no "In this article we will..." intro
- H2 for main sections, H3 for subsections
- Bold key terms and important points
- Use bullet lists for steps, tool lists, comparisons
- Use numbered lists for sequential steps
- Include at least 1 code block if the topic involves code/templates/workflows
- Add [internal link suggestions] in brackets where relevant Knox Hub posts exist
- No H1 in the content — the Post Title field handles H1
- End with a "Next Steps" or "What to Do Now" section
- Last paragraph: point to Knox Community or related content naturally
]
```

---

## STEP 4: Quality Check

Before presenting output, verify:

- [ ] Title is specific and benefit-driven (not generic)
- [ ] No AI filler phrases anywhere
- [ ] Every H2 section has a clear actionable point
- [ ] FAQs are phrased as real user search queries
- [ ] Meta description is under 160 chars and includes primary keyword
- [ ] SEO title is under 60 chars
- [ ] Tags match Knox Hub's existing taxonomy
- [ ] Sidebar HTML is valid (or skipped with reason)
- [ ] Content reads like a real person wrote it, not an AI

---

## STEP 5: End with

```
---
Ready to publish. Copy each section into the Knox Hub editor.

Suggested cover image prompt for generation:
[1-2 sentence prompt for creating a relevant cover image — describe the visual concept]

Want me to:
- Adjust the tone (more expert / more casual)
- Expand any section
- Write a shorter version
- Generate social captions for this post (/social-captions)
```

---

## KNOX HUB CONTENT PILLARS
_(Keep posts aligned with these topics)_

- **AI automation** — n8n, Claude, MCP integrations, workflows
- **Claude Code & Skills** — building, installing, using Claude skills
- **Vibe coding & shipping** — building apps fast, deploying, monetizing
- **Lead generation & outreach** — scraping, enrichment, cold email
- **SaaS & business tools** — tool stacks, CRM, productivity
- **Content & marketing automation** — repurposing, social, SEO

## INTERNAL LINKS TO USE WHEN RELEVANT
_(Link to these posts when the topic connects)_

- How to Stop Re-Explaining Yourself to Claude → `/hub/post/how-to-stop-re-explaining-yourself-to-claude-every-day`
- Magic MCP Turns Claude Code Into a UI Designer → `/hub/post/magic-mcp-turns-claude-code-into-a-ui-designer`
- Stop Building n8n Workflows by Hand → `/hub/post/stop-building-n8n-workflows-by-hand`
- Context Engineering: Why Your AI Builds Break → `/hub/post/context-engineering-why-your-ai-builds-break`
- Master Claude Skills: The Complete Guide → `/hub/post/master-claude-skills-complete-guide`
- Building Your Automation Stack from Zero → `/hub/post/building-automation-stack-from-zero`
