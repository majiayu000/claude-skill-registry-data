---
name: substack-editor
description: Transform topics or documents into engaging, optimized Substack articles with authentic voice, storytelling, and maximum engagement. Use when user wants to create a Substack post from an idea, topic, or existing document.
---

# Substack Editor

Transform any topic or document into a publication-ready Substack article that's engaging, optimized, and authentic.

## When to Use This Skill

Use this skill when the user wants to:
- Create a Substack article from a topic or idea
- Transform a report, document, or draft into an engaging Substack post
- Write content that follows best practices for engagement and SEO
- Generate HTML ready to paste into Substack editor

## Quick Start Workflow

### Step 1: Understand the Input

Ask the user for:
- **Topic/idea** they want to write about, OR
- **Document/draft** they want to transform

If they provide a document, read it thoroughly to understand the core message and value.

### Step 2: Load the Style Guides

ALWAYS read these references before writing:

1. **`references/eb-style-guide.md`** - Core writing voice and tone
2. **`references/humanization-checklist.md`** - Make it sound genuinely human
3. **`references/substack-content-optimization-guide.md`** - Substack-specific optimization

Read these files to internalize the writing style, humanization techniques, and Substack best practices.

### Step 3: Create the Article

Write an engaging article that includes:

**Structure:**
- Compelling headline (60 chars max)
- Hook in first 100 words (controversial, surprising, or story-based)
- 1,200-2,500 words total
- Short paragraphs (1-3 sentences)
- Clear visual hierarchy (H2/H3 headings)

**Voice & Style:**
- Enthusiastic, supportive, engaging tone
- Authentic human voice with personal touches
- Varied sentence length (5-25 words for natural rhythm)
- NO AI-isms ("delve," "leverage," "tapestry")
- NO em dashes (—) - use commas, periods, or colons instead
- Include personal anecdotes and real examples

**Engagement:**
- Subscribe CTA after first paragraph
- Multiple CTAs throughout (use button format)
- Open-ended question at end for comments
- Scannable structure with visual breaks

**SEO:**
- Target keyword in headline, first 100 words
- Suggested URL slug (3-5 words, keyword-included)
- 3-5 opportunities for internal links (note where previous posts could link)
- Alt text suggestions for any images

### Step 4: Deliver the Package

Provide the user with:

1. **HTML Artifact** - Create an artifact with the rendered HTML so user can copy directly from the preview
   - Save as `article.html`
   - User can select rendered content and copy/paste directly into Substack
   
2. **Metadata summary** (in your response text) including:
   - Headline
   - URL slug suggestion
   - Meta description (150 chars)
   - Email subject line (different from headline)
   - Target keyword
   - Internal linking opportunities
   - Image suggestions with alt text
   - Engagement question for end of post

**Critical**: Always create the HTML as an artifact so it renders in Claude's interface. The user will copy the rendered HTML directly into Substack's editor.

## Article Structure Template

```
# [Compelling Headline - 60 chars max]

[Hook paragraph - 100 words with immediate value]

[Subscribe CTA button]

## Introduction
[Context and "one promise" - what reader will get]

## [Main Content Sections]
[Clear H2/H3 hierarchy]
[Short paragraphs]
[Personal examples]
[Reality check sections]

## Conclusion
[Key takeaway]
[Open-ended question]

[Final CTA button]
```

## Critical Requirements

**Always follow:**
- ✅ Read all three reference files before writing
- ✅ Use enthusiastic, supportive EB voice
- ✅ Apply humanization checklist (varied sentences, no AI-isms)
- ✅ Follow Substack optimization guide (hooks, CTAs, SEO)
- ✅ Create HTML artifact (not just a file) so it renders in Claude's interface
- ✅ Include complete metadata package in response text

**Never do:**
- ❌ Use em dashes (—)
- ❌ Use AI-ism phrases
- ❌ Write walls of text without breaks
- ❌ Skip the subscribe CTA in first 300 words
- ❌ Forget to include an engagement question
- ❌ Create HTML file instead of artifact (user needs to copy rendered HTML)

## Output Format

Create the article as an HTML artifact that renders in Claude's interface:

**Use artifact with `.html` extension** so it renders properly and user can copy/paste rendered content.

HTML formatting:
- `<h1>` for main headline
- `<h2>` for major sections
- `<h3>` for subsections
- `<p>` for paragraphs
- `<strong>` for emphasis
- `<em>` for italics
- `<blockquote>` for key insights
- `<ul>/<li>` for bullet lists

No complex CSS or JavaScript - just clean, semantic HTML that renders in Claude's artifact viewer and pastes perfectly into Substack's editor.

The user will copy the rendered HTML from the artifact preview directly into Substack.

## Reference Files

- **`eb-style-guide.md`** - Complete voice and tone guidelines
- **`humanization-checklist.md`** - 5-stage humanization workflow
- **`humanization-strategy.md`** - Deep dive on authenticity
- **`substack-content-optimization-guide.md`** - Complete Substack optimization rubric

## Example Interaction

**User:** "Write a Substack post about the benefits of async communication in remote teams"

**Claude:** 
1. Reads all three core reference files
2. Creates engaging article with:
   - Hook about remote work chaos
   - Personal story of team communication breakdown
   - 5 practical benefits with real examples
   - Reality check section on when async doesn't work
   - Engagement question about reader's experience
3. Delivers HTML artifact (renders in Claude's interface for easy copy/paste) + metadata package

User copies rendered HTML from artifact and pastes directly into Substack editor.

Ready to create engaging Substack content that people actually want to read.
