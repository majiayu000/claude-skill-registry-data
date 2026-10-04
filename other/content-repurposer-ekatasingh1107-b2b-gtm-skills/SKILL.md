---
name: content-repurposer
description: Repurpose one piece of content across six formats while maintaining brand voice
tags: [content, repurposing, linkedin, twitter, email, carousel, video]
---

# Content Repurposer

Takes a single piece of source content (blog post, article, transcript, or long-form post) and transforms it into six distribution-ready formats: LinkedIn post, Twitter/X thread, email newsletter, carousel slides, short-form video script, and pull quotes. Reads brand voice and tone rules from `agency.config.json` to ensure consistency across all outputs.

## Prerequisites

- `agency.config.json` at repo root with `outreach`, `services`, `case_studies`, and `agency` sections
- Source content: a blog post URL, pasted article, transcript, or long-form text (minimum 500 words)
- Optional: target audience segment override (defaults to primary ICP segment from config)
- Optional: channels to skip (if you only need 3 of 6 formats)

## Capabilities Used

1. `brand-voice` -- for tone, vocabulary, and sentence structure rules
2. `message-generator` -- for email newsletter formatting and CTA patterns

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name` -- for attribution and sign-offs
   - `agency.founder` -- for personal voice in LinkedIn/Twitter
   - `outreach.tone` -- voice and style guide for all outputs
   - `outreach.banned_phrases` -- phrases that must not appear in any format
   - `services[]` -- for weaving in relevant service mentions where natural
   - `case_studies[]` -- for proof points if the source content references results
   - `icp.segments[]` -- to tailor language to the target audience
3. Accept parameters:
   - `source_content` -- (required) the full text of the source piece, or a URL to fetch
   - `source_type` -- `blog` | `article` | `transcript` | `linkedin-post` | `podcast-notes` | `case-study`. Default: `blog`
   - `target_audience` -- which ICP segment this targets. Default: primary segment
   - `channels` -- array of output formats to generate. Default: all six
   - `cta` -- the call-to-action to include across formats (e.g., "Book a free CRO audit")
   - `author` -- name for attribution. Default: `agency.founder`

## Phase 1: Content Analysis

Parse the source content and extract its structural DNA:

**Core extraction:**
- **Central thesis**: the single main argument or insight in one sentence
- **Key points**: 3-7 supporting points or sub-arguments, ordered by strength
- **Data points**: any statistics, percentages, results, or quantitative claims
- **Quotes**: memorable or punchy lines that work standalone
- **Story elements**: anecdotes, examples, before/after narratives
- **Keywords**: primary topic keywords and secondary related terms
- **Emotional hook**: the pain point, aspiration, or curiosity angle that makes this content compelling

**Content quality assessment:**
- Word count of source
- Depth level: surface, moderate, deep
- Originality markers: unique data, proprietary frameworks, first-hand experience
- Repurpose potential score: 1-10 (based on variety of angles extractable)

Compile:
```
SOURCE ANALYSIS:
---
Thesis: [one sentence]
Key points: [numbered list]
Data points: [list]
Best quotes: [2-3 standalone lines]
Story elements: [list]
Emotional hook: [the core pain/aspiration]
Repurpose potential: [score]/10
```

## Phase 2: Format Transformation

Generate each output format by restructuring the source material, not summarizing it. Each format demands a different structure, length, and hook strategy.

### Format 1: LinkedIn Post

**Structure:** Hook line, value body, CTA, hashtags
**Length:** 150-300 words (optimal for LinkedIn algorithm)
**Rules:**
- Opening line must stop the scroll: use a bold claim, counterintuitive take, or specific number
- One line per paragraph for the first 3 lines (appears above the fold)
- Use line breaks aggressively for readability
- No more than 3-5 hashtags at the end
- CTA should invite comments or discussion, not just link clicks
- Write in first person (founder voice)
- Reference the original content as "deeper dive" but make the post self-contained

### Format 2: Twitter/X Thread

**Structure:** Hook tweet, value tweets (5-10), CTA tweet
**Length:** 5-12 tweets, each under 280 characters
**Rules:**
- Tweet 1: the hook, must work standalone, no "Thread:" prefix
- Each tweet delivers one complete thought
- Use numbers and data in individual tweets where available
- Tweet transitions should flow naturally without "1/", "2/" numbering
- Final tweet: CTA + link to full piece
- Include one "retweet bait" tweet (a standalone insight people want to share)
- No emojis unless they replace words for character savings

### Format 3: Email Newsletter

**Structure:** Subject line, preview text, greeting, body, CTA, sign-off
**Length:** 200-400 words body
**Rules:**
- Subject line: max 50 characters, curiosity or benefit-driven
- Preview text: complements subject, does not repeat it
- Open with the most compelling insight or data point from the source
- Body: 2-3 key takeaways, written conversationally
- One primary CTA (read the full post, book a call, reply)
- Sign off using `outreach.sign_off` from config
- P.S. line with a secondary hook or personal note
- Respect `outreach.banned_phrases`

### Format 4: Carousel Slides

**Structure:** 7-12 slides with title + body per slide
**Length:** 15-30 words per slide body, 3-8 words per slide title
**Rules:**
- Slide 1: Hook slide with attention-grabbing title (question, bold stat, or contrarian claim)
- Slide 2: Context or problem setup
- Slides 3-8: One key point per slide, with supporting detail
- Slide 9-11: Data point or case study result slide
- Final slide: CTA slide with clear next step and handle/brand
- Each slide must be self-contained (readable without context)
- Use consistent slide title format throughout
- No walls of text: if a slide needs more than 30 words, split it

Output as structured JSON array for design tool ingestion.

### Format 5: Short-Form Video Script

**Structure:** Hook, body, CTA
**Length:** 45-90 seconds when spoken (approximately 120-240 words)
**Rules:**
- First 3 seconds: the hook (question, surprising fact, or bold statement)
- Body: 3 key points delivered in rapid succession
- Use conversational language (written to be spoken aloud)
- Include visual/B-roll cues in brackets: `[show product page]`, `[cut to results graph]`
- CTA: follow, comment, or visit link in bio
- Pacing notes: mark pauses and emphasis
- Format for teleprompter readability (short lines, natural break points)

### Format 6: Pull Quotes and Micro-Content

**Structure:** 3-5 standalone quotes or micro-posts
**Length:** 15-40 words each
**Rules:**
- Each quote must work completely out of context
- Suitable for: Instagram stories, quote graphics, presentation slides, social media fillers
- Mix types: data-driven, opinion-driven, actionable tip
- Include attribution format: "-- [Author], [Agency]"

## Phase 3: Cross-Format Consistency Check

Before finalizing, verify consistency across all outputs:

1. **Thesis alignment**: every format communicates the same core thesis
2. **Tone check**: read each format against `outreach.tone`. Flag and rewrite anything off-brand
3. **Banned phrase scan**: check all six outputs against `outreach.banned_phrases`
4. **CTA consistency**: the same primary CTA appears in all formats (adapted to channel)
5. **Fact consistency**: data points and claims are identical across formats (no rounding differences)
6. **Voice consistency**: first person throughout (not switching between "I" and "we" randomly)
7. **No redundancy in distribution**: if someone follows on LinkedIn AND subscribes to the newsletter, the two pieces should feel complementary, not identical

## Phase 4: Output

Return structured JSON:

```json
{
  "source_analysis": {
    "thesis": "The central argument in one sentence",
    "key_points_count": 5,
    "data_points_count": 3,
    "repurpose_potential": 8,
    "source_word_count": 1850
  },
  "linkedin_post": {
    "body": "Full LinkedIn post text with line breaks...",
    "hashtags": ["#D2C", "#Shopify", "#CRO"],
    "word_count": 220,
    "hook_type": "data-driven"
  },
  "twitter_thread": {
    "tweets": [
      "Tweet 1: the hook...",
      "Tweet 2: first point...",
      "Tweet 3: data point...",
      "Tweet N: CTA..."
    ],
    "tweet_count": 8,
    "retweet_bait_index": 3
  },
  "email_newsletter": {
    "subject_line": "Subject line here",
    "preview_text": "Preview text here",
    "body": "Full newsletter body...",
    "ps_line": "P.S. line here",
    "word_count": 310,
    "cta": "Read the full breakdown"
  },
  "carousel": {
    "slides": [
      {"slide_number": 1, "title": "Hook Title", "body": "Slide body text", "design_note": "Bold typography, dark background"},
      {"slide_number": 2, "title": "The Problem", "body": "Context text"},
      {"slide_number": 3, "title": "Point 1", "body": "Detail text"}
    ],
    "total_slides": 10,
    "estimated_read_time": "2 min"
  },
  "video_script": {
    "hook": "First 3 seconds text",
    "body": "Full script with [visual cues]...",
    "cta": "CTA text",
    "duration_seconds": 65,
    "word_count": 175
  },
  "pull_quotes": [
    {"quote": "Standalone quote text", "type": "data-driven", "attribution": "Ekata Singh, Plasho"},
    {"quote": "Another quote", "type": "opinion", "attribution": "Ekata Singh, Plasho"}
  ],
  "distribution_schedule": {
    "day_1": "Publish blog + LinkedIn post",
    "day_2": "Twitter thread",
    "day_3": "Email newsletter",
    "day_5": "Carousel on LinkedIn",
    "day_7": "Short-form video (Reels/Shorts)",
    "ongoing": "Pull quotes as filler content"
  },
  "consistency_check": {
    "thesis_aligned": true,
    "tone_compliant": true,
    "banned_phrases_clear": true,
    "cta_consistent": true,
    "facts_consistent": true
  }
}
```

## Phase 5: Distribution Calendar

Suggest an optimal posting schedule to maximize reach without content fatigue:

- **Day 1**: Publish the source content (blog/article) + LinkedIn post teasing it
- **Day 2**: Twitter/X thread (standalone value, links back to source)
- **Day 3**: Email newsletter to subscriber list
- **Day 5**: LinkedIn carousel (enough gap from the text post)
- **Day 7**: Short-form video on Instagram Reels / YouTube Shorts / TikTok
- **Ongoing**: Pull quotes as filler content between major posts

This schedule ensures the same audience sees the content in different formats across different channels without feeling spammed.

## Example Usage

Trigger phrases:
- "Repurpose this blog post across channels"
- "Turn this article into social content"
- "Create a LinkedIn post, thread, and newsletter from this"
- "Repurpose this for all platforms"
- "Turn this transcript into content"
- "Break this down for social media"

```
User: Repurpose this blog post about Shopify CRO for D2C brands [pastes 2000 word article]
Assistant: [analyzes source, generates all 6 formats, ensures brand voice consistency, returns structured JSON with distribution schedule]
```

```
User: Turn this podcast transcript into a LinkedIn carousel and Twitter thread
Assistant: [analyzes transcript, generates only carousel and thread formats, skips other channels, returns structured JSON]
```
