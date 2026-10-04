---
name: social-content-writer
description: >
  Generates platform-native social media posts for LinkedIn, X/Twitter,
  Instagram, and Reddit. Supports thought leadership, case study snippets,
  hot takes, engagement questions, carousel outlines, and threads.
tags: [social-media, content, linkedin, twitter, instagram, reddit]
---

# Social Content Writer

Generates ready-to-publish social media posts tailored to each platform's native format, algorithm preferences, and audience expectations. Every post is built from brand voice in `agency.config.json`, not generic marketing copy.

## Prerequisites

- `agency.config.json` populated (agency info, case studies, services, outreach tone)
- Topic or theme to write about
- Optional: research output from `blog-researcher` or `linkedin-researcher`

## Phase 0: Intake

Read `agency.config.json`:
- `agency.name`, `agency.founder`, `agency.tagline` -- brand identity
- `outreach.tone` -- voice/style baseline (adapt per platform)
- `outreach.banned_phrases` -- never use these
- `case_studies[]` -- proof points for case study posts
- `services[]` -- service areas for thought leadership angles

Accept parameters:
- `platform` -- (required) one of: `linkedin`, `twitter`, `instagram`, `reddit`
- `post_type` -- (required) one of: `thought-leadership`, `case-study-snippet`, `hot-take`, `engagement-question`, `carousel-outline`, `thread`, `story-caption`
- `topic` -- (required) subject or theme
- `research` -- (optional) output from researcher skills for data-backed posts
- `case_study` -- (optional) specific case study slug from config
- `cta_type` -- (optional) `comment`, `dm`, `link`, `follow`, `none`. Default: `comment`
- `count` -- (optional) number of variants to generate. Default: 2

## Phase 1: Platform Voice Adaptation

Adapt the base `outreach.tone` for each platform:

| Platform | Tone Shift | Format Norms |
|----------|-----------|--------------|
| LinkedIn | Professional, insight-driven, first-person narrative | Line breaks between ideas, use of "I" and "we", no hashtag spam (max 3-5 at end) |
| X/Twitter | Punchy, opinionated, concise | Max 280 chars per tweet, threads use 1/ numbering, hot takes welcome |
| Instagram | Visual-first, aspirational, casual | Caption supports the visual, use line breaks, 5-15 relevant hashtags at end, emoji sparingly |
| Reddit | Helpful, community-native, no self-promo | Match subreddit tone, lead with value, mention experience naturally, no links in first reply |

## Phase 2: Post Type Generation

### Thought Leadership
- Open with a contrarian or surprising insight from the founder's perspective
- Support with data, observation, or experience
- Close with a question or takeaway
- LinkedIn: 150-300 words, line breaks every 1-2 sentences
- Twitter: Single tweet (280 chars) or thread (3-7 tweets)
- Instagram: 100-200 word caption paired with a quote card concept
- Reddit: 150-400 words matching the subreddit's expertise level

### Case Study Snippet
- Lead with the result (number, metric, transformation)
- Brief context (who, what problem)
- What was done (2-3 bullet points max)
- Result reinforced
- Soft CTA
- LinkedIn: 150-250 words, use bullet points for the "what we did"
- Twitter: Single tweet with key metric + thread for breakdown
- Instagram: Stat-forward caption with before/after framing

### Hot Take
- Bold, opinionated statement on an industry trend
- Back it up with one proof point
- Invite disagreement
- LinkedIn: 50-150 words, conversational
- Twitter: Single tweet, max edge without being hostile
- Instagram: Quote-style caption

### Engagement Question
- Ask a genuine question the audience cares about
- Provide 2-3 options or your own take first
- Designed to drive comments
- LinkedIn: Question + context (50-100 words)
- Twitter: Question only (under 200 chars)
- Instagram: Question in caption, use poll sticker concept for stories

### Carousel Outline
- LinkedIn/Instagram only
- 5-10 slides with headline + supporting text per slide
- Slide 1: Hook (scroll-stopping statement)
- Slides 2-8: Core content (one idea per slide)
- Slide 9: Summary or key takeaway
- Slide 10: CTA slide (follow, DM, comment)
- Output as structured slide-by-slide text

### Thread
- Twitter/LinkedIn only
- 3-10 posts in sequence
- Post 1: Hook that promises value ("Here's how we 3x'd conversion rate for a sports brand")
- Posts 2-8: One insight per post, each standalone-readable
- Final post: Summary + CTA
- Number each: 1/, 2/, etc.

### Story Caption
- Instagram only
- Ultra-short (1-2 lines)
- Designed to pair with a visual
- Include engagement prompt (poll, question, emoji slider)

## Phase 3: Quality Check

Before returning, verify every post:

1. **Banned phrase scan**: Check against `outreach.banned_phrases`. Rewrite if any match.
2. **Character limits**: Twitter posts under 280 chars. LinkedIn under 3000 chars. Instagram under 2200 chars.
3. **Tone check**: Re-read against platform voice. Rewrite if it sounds corporate, generic, or salesy.
4. **Hashtag rules**: LinkedIn max 5, Instagram 5-15, Twitter max 3, Reddit zero.
5. **CTA count**: One CTA per post (or none for pure value posts).
6. **Self-promo check for Reddit**: No direct links or pitches. Help first, credibility naturally.
7. **No emojis overload**: Max 2-3 per LinkedIn post, 5-8 per Instagram caption, 0-1 per tweet.

## Phase 4: Output

Return structured JSON:

```json
{
  "platform": "linkedin",
  "post_type": "thought-leadership",
  "variants": [
    {
      "text": "Full post text with line breaks...",
      "hashtags": ["#Shopify", "#D2C", "#Ecommerce"],
      "character_count": 487,
      "word_count": 82,
      "cta": "What's your take? Drop a comment.",
      "visual_suggestion": "Screenshot of a Shopify analytics dashboard showing the metric",
      "best_posting_time": "Tuesday 9-11 AM IST / Tuesday 7-9 AM GMT"
    },
    {
      "text": "Variant 2...",
      "hashtags": ["#ShopifyPartner", "#EcommerceTips"],
      "character_count": 412,
      "word_count": 71,
      "cta": "DM me if you want the full breakdown.",
      "visual_suggestion": "Carousel with 5 key points from the post",
      "best_posting_time": "Wednesday 12-2 PM IST"
    }
  ],
  "topic": "Why most D2C brands underinvest in product page CRO",
  "personalization_source": "Kibi Sports case study",
  "generated_at": "2026-03-13T10:00:00Z"
}
```

## Phase 5: Scheduling Recommendation

For each post, suggest optimal posting time based on platform best practices:

| Platform | Best Times (IST) | Best Days |
|----------|-----------------|-----------|
| LinkedIn | 9-11 AM, 12-1 PM | Tue, Wed, Thu |
| Twitter | 8-10 AM, 12-1 PM, 5-6 PM | Mon-Fri |
| Instagram | 11 AM-1 PM, 7-9 PM | Tue, Wed, Fri |
| Reddit | 6-8 AM EST (for US subs) | Mon, Wed |

For India-focused audience, adjust to IST prime hours. For US/UK audience, adjust to their local times.

## Example Usage

Trigger phrases:
- "Write a LinkedIn post about CRO for D2C brands"
- "Create a Twitter thread about our Kibi Sports results"
- "Write an Instagram caption for a case study post"
- "Generate a hot take about Shopify themes for LinkedIn"
- "Write a Reddit-friendly comment about Shopify development"
- "Create a LinkedIn carousel outline about ecommerce mistakes"
- "Generate 3 engagement questions for LinkedIn this week"
