---
name: thought-leadership
description: Transform raw transcripts, notes, or topics into polished long-form articles in the founder's voice
tags: [content, articles, thought-leadership, founder-voice, seo, long-form]
---

# Thought Leadership

Transforms raw founder inputs -- transcripts, voice notes, bullet points, hot takes, or topic prompts -- into polished, long-form articles (1500-3000 words). Maintains the founder's authentic voice while adding structure, data points, examples, and SEO metadata. The output reads like the founder wrote it on their best day, not like AI content.

## Prerequisites

- `agency.config.json` at repo root with `agency`, `services`, `case_studies`, `icp`, and `outreach` sections
- Raw input: transcript, notes, bullet points, or topic description
- Optional: existing brand voice document (from `brand-voice` skill)
- Optional: target publication or platform (blog, LinkedIn article, Medium, guest post)

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name` -- for contextual references
   - `agency.founder` -- for author attribution
   - `agency.tagline` -- for thematic alignment
   - `services[]` -- to weave in relevant expertise naturally (never as a sales pitch)
   - `case_studies[]` -- for real examples and data points
   - `icp.segments[]` -- to understand who the reader is
   - `outreach.tone` -- foundational voice guide
   - `outreach.banned_phrases` -- phrases to avoid
3. Accept parameters:
   - `input_type` -- (required) one of: `transcript`, `voice-notes`, `bullet-points`, `topic`, `hot-take`, `interview-qa`
   - `raw_input` -- (required) the source material
   - `target_length` -- word count target. Default: 2000. Range: 1500-3000
   - `article_type` -- `opinion`, `how-to`, `industry-analysis`, `lessons-learned`, `predictions`, `framework`, `case-study-deep-dive`. Default: inferred from input
   - `platform` -- target publication: `blog`, `linkedin-article`, `medium`, `guest-post`, `newsletter`. Default: `blog`
   - `target_audience` -- ICP segment. Default: primary segment from config
   - `seo_keyword` -- (optional) primary keyword to target
   - `related_articles` -- (optional) URLs of the founder's previous articles for voice consistency

## Phase 1: Input Analysis

Parse the raw input to extract its structural DNA.

**For transcripts and voice notes:**
- Identify the core thesis (what is the founder actually arguing?)
- Extract key claims and assertions
- Find specific examples, stories, and anecdotes mentioned
- Note unique phrases, metaphors, and speech patterns -- these are voice gold
- Identify tangents vs. main thread
- Flag any data points or numbers mentioned
- Note emotional peaks (where the founder gets passionate -- these become article highlights)

**For bullet points and topics:**
- Identify the central argument or premise
- Map the logical structure (which points support which?)
- Identify gaps that need filling (claims without evidence, assertions without examples)
- Note the implied depth level

**For hot takes:**
- Identify the contrarian position
- Extract the supporting logic
- Note the implied "versus" (what conventional wisdom is being challenged?)

Compile the analysis:
```
INPUT ANALYSIS:
---
Core thesis: [one sentence]
Key claims: [numbered list]
Supporting evidence available: [list]
Evidence gaps (need research): [list]
Unique voice markers: [phrases, metaphors, patterns]
Emotional peaks: [topics where passion shows]
Tangents to cut: [off-topic threads]
Estimated raw insight density: [high/medium/low]
```

## Phase 2: Research and Evidence Gathering

Fill evidence gaps identified in Phase 1. The article must be opinionated AND substantiated.

**For each claim without evidence:**
- Search for supporting data: industry reports, surveys, studies
- Find relevant examples from other companies or industries
- Check if `case_studies[]` from config provides relevant proof points
- Look for counter-arguments to address (stronger articles acknowledge the other side)

**Data point requirements:**
- Minimum 3 data points per 1000 words
- At least one data point from the agency's own experience (case study)
- At least one from external research or industry data
- Cite sources naturally in the text (not academic footnotes)

**If using WebSearch:**
- Search for: `"{{claim keyword}}" statistics {{current_year}}`
- Search for: `"{{industry}}" trends data report`
- Search for counter-arguments: `"{{thesis}} wrong"` or `"{{thesis}} myth"`

## Phase 3: Article Architecture

Design the article structure based on type and input analysis.

**Article type structures:**

### Opinion article:
```
1. Hook: provocative opening that states the thesis boldly (100-150 words)
2. Context: why this matters now (100-150 words)
3. The argument: main body with 3-4 supporting sections (800-1200 words)
   - Each section: claim + evidence + example + implication
4. Counter-argument acknowledgment: the strongest objection and why it is incomplete (150-200 words)
5. Conclusion: restate thesis with forward-looking implication (100-150 words)
```

### How-to article:
```
1. Hook: the pain point or desired outcome (100-150 words)
2. Why conventional approaches fail (150-200 words)
3. The framework/method: 4-7 steps (800-1500 words)
   - Each step: what, why, how, example, common mistake
4. Case study: the method in action (200-300 words)
5. Getting started: first action the reader can take today (100-150 words)
```

### Industry analysis:
```
1. Hook: the macro trend or shift (100-150 words)
2. Data landscape: what the numbers show (200-300 words)
3. Analysis: what the data means, 3-4 implications (600-1000 words)
   - Each implication: trend + evidence + what it means for the reader
4. What smart companies are doing: examples (200-300 words)
5. Predictions: where this is heading (150-200 words)
6. Action items: what the reader should do (100-150 words)
```

### Lessons learned:
```
1. Hook: the context and stakes (100-150 words)
2. The story: what happened, compressed narrative (200-300 words)
3. Lessons: 5-7 insights, each as its own mini-section (800-1200 words)
   - Each lesson: the insight + the specific moment that taught it + the broader principle
4. What I would do differently: honest retrospective (150-200 words)
5. Takeaway for the reader: how to apply these lessons (100-150 words)
```

### Predictions:
```
1. Hook: the current state and why change is coming (100-150 words)
2. Track record: previous predictions that came true (credibility builder) (100-150 words)
3. Predictions: 5-7 specific, testable predictions (800-1200 words)
   - Each prediction: the prediction + supporting signals + timeline + confidence level
4. What these predictions mean for the reader (200-300 words)
5. Bets: what the founder is personally doing based on these predictions (100-150 words)
```

### Framework article:
```
1. Hook: the problem this framework solves (100-150 words)
2. Why existing approaches fall short (150-200 words)
3. The framework: visual name, 3-5 components (600-1000 words)
   - Each component: what it is, why it matters, how to apply it
4. Framework in action: case study or example walkthrough (200-300 words)
5. Getting started: how to implement the framework today (100-150 words)
6. Download/resource: optional lead magnet tie-in (50 words)
```

## Phase 4: Voice Calibration

The article must sound like the founder, not like AI content. This phase ensures authenticity.

**Voice markers to maintain from input analysis:**
- Sentence length patterns (does the founder use short punchy sentences or flowing ones?)
- Vocabulary level (technical jargon vs. plain language)
- Humor style (dry, self-deprecating, none)
- Storytelling tendency (anecdote-heavy or data-heavy)
- Conviction level (hedging vs. bold assertions)
- Cultural references (industry-specific, regional, generational)

**Voice rules (non-negotiable):**
1. Use first person ("I", "we", "my team") throughout
2. Include at least 2 personal anecdotes or observations
3. Express genuine opinions -- no "on the other hand" hedging on core claims
4. Use the founder's actual phrases from the raw input where possible
5. Avoid AI markers: "In today's landscape", "It's important to note", "Leverage", "Utilize"
6. Read the `outreach.tone` from config and match it
7. Check against `outreach.banned_phrases` and rewrite any matches
8. Vary sentence length: mix 5-word punches with 25-word explanations
9. Use concrete specifics, not abstract generalities ("we found 23% drop-off at checkout" not "there were conversion issues")
10. End paragraphs with strong sentences, not weak ones

**AI content detox checklist:**
- No "In the ever-evolving world of..."
- No "It's worth noting that..."
- No "At the end of the day..."
- No "In conclusion..."
- No "This is a game-changer"
- No "Let's dive in"
- No "Without further ado"
- No starting paragraphs with "So," or "Now,"
- No "synergy", "leverage", "paradigm", "ecosystem" (unless genuinely used by the founder)

## Phase 5: Draft Generation

Write the full article following the structure from Phase 3 and voice from Phase 4.

**Writing process:**

1. **Hook first**: write the opening 2-3 sentences. These determine if anyone reads the rest. The hook must create a knowledge gap, make a bold claim, or tell a compelling micro-story.

2. **Section by section**: write each section as a complete unit. Each section must:
   - Open with a transition from the previous section
   - Deliver one clear idea
   - Include supporting evidence (data, example, or anecdote)
   - Close with a sentence that leads naturally into the next section

3. **Data integration**: weave data points into the narrative naturally. Not "According to a study by X, 73% of..." but "73% of Shopify stores we have audited have this same problem."

4. **Case study integration**: reference case studies from config where they support a point. Keep references brief (2-3 sentences) unless the article type is `case-study-deep-dive`.

5. **Subheadings**: every 200-400 words needs a subheading. Subheadings must be specific and benefit-driven ("Why Your Product Page Loads Too Slow" not "Performance").

6. **Closing**: the final paragraph must be strong. Restate the thesis, but evolved by everything discussed. End with either a forward-looking statement or a call to action (soft, not salesy).

## Phase 6: Editorial Polish

Run these editorial passes over the draft:

**Pass 1: Cut the fat**
- Remove any sentence that does not advance the argument
- Cut adverbs: "very", "really", "extremely", "incredibly"
- Cut filler phrases: "in order to" -> "to", "due to the fact that" -> "because"
- Target: 10-15% word count reduction from first draft

**Pass 2: Strengthen openings**
- Every section opening must hook. If a section starts with background, restructure to lead with the insight.
- First sentence of the article is the most important sentence. Rewrite until it is perfect.

**Pass 3: Verify voice**
- Read aloud (mentally). Does it sound like the founder or like a content writer?
- Replace any generic phrases with specific, opinionated ones
- Add 1-2 more personal touches if the article feels impersonal

**Pass 4: Fact check**
- Verify all data points are accurate
- Ensure case study references match config data
- Check any external claims

**Pass 5: Readability**
- Target Flesch-Kincaid grade level 8-10
- No paragraph exceeds 4 sentences
- No sentence exceeds 30 words
- Vary sentence structure: do not start 3 consecutive sentences the same way

## Phase 7: SEO Optimization

Generate SEO metadata and ensure on-page optimization:

| Element | Specification |
|---------|--------------|
| Title tag | 50-60 chars, primary keyword + benefit + brand |
| Meta description | 150-160 chars, CTA-oriented with keyword |
| H1 | Article headline (contains primary keyword naturally) |
| H2s | Section subheadings (include secondary keywords where natural) |
| URL slug | 3-5 words, lowercase, hyphenated, keyword-rich |
| Primary keyword | Appears in: title, H1, first 100 words, 1-2 H2s, conclusion |
| Keyword density | 0.5-1.5% for primary keyword (never forced) |
| Internal links | Suggest 2-3 places to link to other agency content |
| Alt text suggestions | For any recommended images or graphics |

## Phase 8: Output

Return structured JSON:

```json
{
  "article_metadata": {
    "title": "Article headline",
    "author": "Founder name",
    "type": "opinion",
    "platform": "blog",
    "word_count": 2150,
    "estimated_read_time": "9 min",
    "target_audience": "India D2C",
    "input_type": "transcript",
    "input_word_count": 3400
  },
  "seo": {
    "title_tag": "SEO title tag",
    "meta_description": "SEO meta description",
    "url_slug": "article-url-slug",
    "primary_keyword": "target keyword",
    "secondary_keywords": ["keyword 1", "keyword 2", "keyword 3"],
    "keyword_density": 0.8,
    "internal_link_suggestions": [
      {"anchor_text": "...", "suggested_url": "...", "context": "..."}
    ]
  },
  "article": {
    "headline": "The article headline",
    "subtitle": "Optional subtitle or deck",
    "body": "Full article text with markdown formatting...",
    "sections": [
      {"heading": "Section title", "word_count": 280, "key_point": "The main takeaway from this section"}
    ]
  },
  "voice_analysis": {
    "voice_markers_preserved": ["list of founder phrases used"],
    "personal_anecdotes_included": 3,
    "ai_marker_check": "clean",
    "tone_match": "matches config outreach.tone"
  },
  "data_points_used": [
    {"claim": "73% of stores have this issue", "source": "internal audit data", "location": "section 2"}
  ],
  "editorial_notes": {
    "words_cut_in_editing": 340,
    "strongest_section": "Section 3 -- the framework explanation",
    "weakest_section": "Section 5 -- could use a stronger example",
    "suggested_images": ["hero image concept", "framework diagram", "before/after screenshot"]
  },
  "repurpose_potential": {
    "linkedin_post_angles": ["angle 1", "angle 2"],
    "carousel_topics": ["topic 1"],
    "email_newsletter_hook": "hook text",
    "twitter_thread_points": ["point 1", "point 2", "point 3"]
  }
}
```

## Phase 9: Review

Present the article to the user:

1. Show the headline and subtitle
2. Show the full article with formatting
3. Highlight voice markers preserved from the original input
4. Show data points used and their sources
5. Show SEO metadata
6. Note repurpose potential (hand off to `content-repurposer`)
7. Ask for approval or revision requests

After approval, optionally:
- Publish to the target platform (if CMS access available)
- Feed into `content-repurposer` for multi-channel distribution
- Feed into `content-seo-optimizer` for keyword and readability tuning
- Create a `carousel-creator` carousel from the article's key points

## Example Usage

Trigger phrases:
- "Turn this transcript into a blog post"
- "Write a thought leadership article about [topic]"
- "Turn my notes into an article"
- "Write a LinkedIn article from this voice memo transcript"
- "Create a long-form piece about [topic] in my voice"
- "Polish these bullet points into a full article"

```
User: Turn this transcript from my podcast into a blog post [pastes 4000 word transcript]
Assistant: [analyzes transcript, extracts thesis and voice markers, fills evidence gaps with research, structures as opinion article, writes 2000-word draft in founder's voice, runs editorial passes, generates SEO metadata, returns structured JSON]
```

```
User: Write a thought leadership article about why D2C brands in India need dedicated CRO, not just a redesign
Assistant: [reads config, treats topic as hot take, builds argument with case study data, structures as opinion article, writes in founder voice, returns polished article with repurpose suggestions]
```
