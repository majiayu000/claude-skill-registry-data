---
name: brand-voice
description: Extract and codify brand voice from existing content for consistent messaging
tags: [brand, voice, tone, content]
---

# Brand Voice

Extracts the agency's brand voice from existing content samples, codifies it into a reusable voice guide, and generates config updates for `agency.config.json`. The output ensures consistent tone across all outreach channels: cold emails, LinkedIn messages, Instagram DMs, proposals, and website copy.

## Prerequisites

- `agency.config.json` in the project root
- 3-5 samples of existing content from the user (emails, posts, proposals, website copy)
- Optional: examples of competitor messaging to differentiate against

## Phase 0: Read Current Config

1. Read `agency.config.json` from the project root.
2. Extract `outreach.tone` -- the current tone setting (e.g., "professional-friendly").
3. Extract `outreach.banned_phrases` -- phrases already flagged as off-limits.
4. Extract `agency_name` and `services[].name` for context.
5. Present current settings:
   ```
   CURRENT VOICE CONFIG:
   Tone: [tone value]
   Banned phrases: [list]

   Ready to analyze your content samples to build a complete voice guide.
   ```

## Phase 1: Gather Samples

Ask the user for 3-5 pieces of existing content. Prioritize content that performed well:

```
I need 3-5 samples of your best content. Prioritize:

1. A cold email that got a reply (paste the full email)
2. A LinkedIn post that got good engagement (paste the text)
3. A proposal intro or cover letter (paste the opening section)
4. Website copy (paste homepage or about page text)
5. An Instagram caption or DM that worked (paste the text)

The more variety, the better. Paste them in any order.
```

For each sample, tag:
- Channel (email, LinkedIn, Instagram, proposal, website)
- Performance (got reply, got engagement, closed deal, unknown)
- Audience (cold prospect, warm lead, existing client)

## Phase 2: Analyze Patterns

Across all samples, analyze:

**Sentence structure:**
- Average sentence length (count words per sentence)
- Short (< 10 words), medium (10-20), long (> 20) ratio
- Use of fragments vs complete sentences
- Paragraph length (sentences per paragraph)

**Vocabulary level:**
- Casual markers: contractions, slang, first names, exclamation marks
- Professional markers: industry jargon, formal transitions, title usage
- Technical markers: specific tool/platform names, metrics, technical terms
- Grade level estimate (Flesch-Kincaid approximation)

**Humor and personality:**
- None: strictly business, no personality markers
- Subtle: occasional wit, light observations
- Frequent: jokes, self-deprecation, playful language
- Note specific examples found

**Pronoun analysis:**
- I/me count (personal, founder-led voice)
- We/us count (team/agency voice)
- You/your count (prospect-focused)
- Calculate ratio: "you" should ideally be > 50% of pronoun usage in outreach

**Power words inventory:**
- List every strong/emotional word used across samples
- Categorize: urgency, exclusivity, trust, results, growth, pain

**Emotional register:**
- Empathetic (acknowledging pain) vs authoritative (stating expertise)
- Optimistic vs realistic
- Urgent vs patient

**Opening patterns:**
- How does each sample start? (question, statement, compliment, data point, story)
- Which openings correlate with performance?

**CTA patterns:**
- How does each sample end? (direct ask, soft suggestion, open question)
- Which CTAs correlate with performance?

## Phase 3: Generate Voice Guide

```
BRAND VOICE GUIDE: [Agency Name]
===

VOICE IN 3 WORDS: [word], [word], [word]
Example: "Direct, Helpful, Expert" or "Warm, Data-Driven, Bold"

---

WE ARE:
1. [attribute] -- [one-sentence example of how this shows up in writing]
2. [attribute] -- [example]
3. [attribute] -- [example]
4. [attribute] -- [example]
5. [attribute] -- [example]

WE ARE NOT:
1. [anti-attribute] -- [what to avoid]
2. [anti-attribute] -- [what to avoid]
3. [anti-attribute] -- [what to avoid]
4. [anti-attribute] -- [what to avoid]
5. [anti-attribute] -- [what to avoid]

---

TONE SPECTRUM:

Formal ---|---[X]------- Casual
Serious --|------[X]---- Playful
Technical -|--[X]-------- Simple
Reserved --|-------[X]--- Bold
Corporate -|--------[X]-- Personal

(X marks where the agency falls on each spectrum)

---

VOCABULARY:

ALWAYS USE:
- [word/phrase] -- [why it fits the voice]
- [word/phrase] -- [why]
- [word/phrase] -- [why]
- [word/phrase] -- [why]
- [word/phrase] -- [why]

NEVER USE:
- [word/phrase] -- [why it clashes]
- [word/phrase] -- [why]
- [word/phrase] -- [why]
- [word/phrase] -- [why]
- [word/phrase] -- [why]
(Include existing banned_phrases + newly identified ones)

---

SENTENCE PATTERNS:

Structure rules:
- [rule derived from analysis, e.g., "Lead with value, not credentials"]
- [rule, e.g., "Max 2 sentences before a line break in emails"]
- [rule, e.g., "Use questions to open, not statements"]
- [rule, e.g., "One idea per paragraph"]

Opening formulas (by performance):
1. [pattern] -- used in [sample], got [result]
2. [pattern] -- used in [sample], got [result]

CTA formulas (by performance):
1. [pattern] -- used in [sample], got [result]
2. [pattern] -- used in [sample], got [result]

---

BY CHANNEL:

Email:
- Tone adjustment: [how voice shifts for cold email]
- Max length: [words]
- Structure: [e.g., "hook -> pain -> proof -> CTA"]
- Signature style: [formal/casual]

LinkedIn:
- Tone adjustment: [how voice shifts for LinkedIn]
- Post format: [short-form, carousel narration, long-form]
- Connection note style: [approach]
- Comment style: [approach]

Instagram:
- Tone adjustment: [how voice shifts for IG]
- Caption style: [length, emoji usage, hashtag approach]
- DM style: [casual vs professional]

Proposals:
- Tone adjustment: [how voice shifts for proposals]
- Formality level: [higher/same/lower than email]
- Structure markers: [headers, bullets, data presentation]
```

## Phase 4: Generate Config Updates

Produce updated config values for `agency.config.json`:

```json
{
  "outreach": {
    "tone": "[2-3 word tone description derived from analysis]",
    "banned_phrases": [
      "existing_banned_1",
      "existing_banned_2",
      "newly_identified_1",
      "newly_identified_2",
      "newly_identified_3"
    ],
    "voice_attributes": [
      "attribute_1",
      "attribute_2",
      "attribute_3"
    ],
    "preferred_words": [
      "word_1",
      "word_2",
      "word_3"
    ],
    "sentence_max_length": 20,
    "paragraph_max_sentences": 2,
    "pronoun_target": {
      "you_ratio": 0.5,
      "we_ratio": 0.3,
      "i_ratio": 0.2
    }
  }
}
```

Present the diff between current and proposed config.

## Phase 5: Output

Return the complete brand voice package:

1. **Voice Guide** -- the full guide from Phase 3, formatted as a standalone document
2. **Config updates** -- JSON block ready to merge into `agency.config.json`
3. **Quick reference card** -- a 5-line cheat sheet for daily use:
   ```
   VOICE CHEAT SHEET: [Agency Name]
   Voice: [3 words]
   Open with: [formula]
   Close with: [formula]
   Always: [top rule]
   Never: [top anti-rule]
   ```
4. **Channel-specific templates** -- one sentence starter per channel showing the voice in action
5. **Recommended next steps**:
   - Update `message-generator` templates to reflect voice guide
   - Review existing email sequences for voice consistency
   - Re-run `brand-voice` quarterly or after significant pivot

If the user confirms, write the config updates directly into `agency.config.json`.

## Example Usage

Trigger phrases:
- "Define our brand voice"
- "Analyze our messaging tone"
- "Build a voice guide"
- "Make our outreach sound consistent"
- "What does our brand sound like?"

```
User: Define our brand voice
Assistant: [asks for content samples, analyzes patterns, builds voice guide, generates config updates]
```

```
User: Our cold emails sound too formal compared to our LinkedIn posts. Fix the voice.
Assistant: [analyzes both channels, identifies inconsistencies, updates voice guide with channel-specific adjustments]
```
