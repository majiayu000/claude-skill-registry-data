---
name: seo-ai-content-check
description: >
  Detect AI-generated content using pure text analysis (no external API calls).
  Analyzes sentence uniformity, vocabulary diversity, repetition patterns, hedging
  language, paragraph uniformity, and personal experience signals. Returns a 0-100
  confidence score plus flagged passages. Use when user says "AI content check",
  "AI detection", "AI written", "content authenticity", "AI content", "detect AI".
allowed-tools:
  - Read
  - Bash
  - Glob
  - WebFetch
---

# AI Content Check

Analyzes text for AI-generated content indicators using writing pattern analysis.
No external API calls — pure local text analysis.

## Inputs

- `target`: URL or file path.
  - If URL: fetch content with WebFetch, extract plain text from HTML body.
  - If file path: read directly with Read tool. Accepts .md, .txt, .html.
  - Strip HTML tags, navigation, headers/footers before analysis. Analyze body copy only.

## Execution

Perform all 6 analysis checks, then compute the confidence score.

**Check 1: Sentence Structure Uniformity (weight: 20%)**

Split text into sentences on `.`, `!`, `?` (ignore abbreviations like "e.g.", "vs.", "etc.").
Calculate word count per sentence. Compute standard deviation of sentence lengths.
- SD < 3 words: FLAGGED (very uniform — AI pattern)
- SD 3-6 words: WARNING
- SD > 6 words: PASS (natural variance)

Score: 0 if SD > 6, 50 if SD 3-6, 100 if SD < 3 (higher = more AI-like)

**Check 2: Vocabulary Diversity — Type-Token Ratio (weight: 20%)**

Tokenize text into lowercase words (strip punctuation). For each 500-word sliding window:
Calculate TTR = unique words / total words.
- TTR < 0.4: FLAGGED (low diversity — AI pattern)
- TTR 0.4-0.55: WARNING
- TTR > 0.55: PASS

If fewer than 500 words, analyze full text. Report worst window TTR.
Score: 0 if TTR > 0.55, 50 if 0.4-0.55, 100 if < 0.4

**Check 3: Repetition Patterns (weight: 20%)**

Detect over-used AI phrases — flag any of these appearing in the text:
"In conclusion", "It's worth noting", "It's important to note", "At the end of the day",
"In today's digital landscape", "In today's fast-paced", "In today's modern",
"Delve into", "Navigating the", "Leverage", "Cutting-edge", "Revolutionize",
"Seamlessly", "Robust solution", "Comprehensive guide", "Game-changer",
"Deep dive", "Unlock the potential", "Dive into"

Also detect 3+ word repeated phrases appearing 3+ times in text (using Bash grep -o).
Score: 0 if 0 phrases flagged, 25 per flagged phrase (max 100)

**Check 4: Hedging Language Rate (weight: 15%)**

Count hedging words/phrases per 1000 words:
"may", "might", "could", "perhaps", "arguably", "generally speaking",
"it could be argued", "one might say", "in some cases", "typically"
- Rate > 8 per 1000 words: FLAGGED
- Rate 4-8: WARNING
- Rate < 4: PASS

Score: 0 if < 4, 50 if 4-8, 100 if > 8

**Check 5: Paragraph Uniformity (weight: 10%)**

Split text into paragraphs (on double newlines or `<p>` tags).
Calculate word count per paragraph. Compute standard deviation of paragraph lengths.
Exclude paragraphs < 5 words (bullets, headers).
- SD < 15 words: FLAGGED (very uniform)
- SD 15-30: WARNING
- SD > 30: PASS

Score: 0 if SD > 30, 50 if 15-30, 100 if < 15

**Check 6: Personal Experience Signals (weight: 15%)**

Detect first-person experience markers:
"I tested", "I tried", "I found", "I noticed", "we found", "we tested",
"in my experience", "our team", "I've been", "we've been", "personally",
"my [N] years", "I recommend", "I use"

For opinion/review/guide content:
- 0 markers found: FLAGGED (AI typically avoids personal voice)
- 1-2 markers: NEUTRAL
- 3+ markers: PASS (authentic human voice)

Detect content type from headings — skip this check for factual/reference content.
Score: 100 if 0 markers (opinion content), 50 if 1-2, 0 if 3+

**Confidence Score Calculation**

Weighted average: (Check1×20 + Check2×20 + Check3×20 + Check4×15 + Check5×10 + Check6×15) / 100
- 0-30: Likely human-written
- 30-60: Mixed or AI-edited
- 60-100: Likely AI-generated

## Output Format

```
## AI Content Analysis: [filename/URL]

### Confidence Score: [N]/100 — [Likely Human / Mixed / Likely AI-Generated]

**Interpretation:** [0-30: Likely human | 30-60: Mixed/edited | 60-100: Likely AI]

### Detailed Findings

| Check | Score | Status | Detail |
|-------|-------|--------|--------|
| Sentence Uniformity | N/100 | PASS/WARN/FLAGGED | SD: N words |
| Vocabulary Diversity | N/100 | PASS/WARN/FLAGGED | TTR: N.NN |
| Repetition Patterns | N/100 | PASS/WARN/FLAGGED | N phrases detected |
| Hedging Language | N/100 | PASS/WARN/FLAGGED | N per 1000 words |
| Paragraph Uniformity | N/100 | PASS/WARN/FLAGGED | SD: N words |
| Experience Signals | N/100 | PASS/WARN/FLAGGED | N markers found |

### Flagged Passages

[Quote specific text passages that triggered flags, with explanation]

### Recommendations for Improving Authenticity

[If score > 30, specific suggestions to make content more human-like]

## Data Sources

- Source: [URL fetched via WebFetch / Local file] (no external AI detection API)
```
