---
name: ai-writing-detector
description: Score any piece of writing for AI-generation tells and produce a weighted 0-100 scorecard with flagged evidence and ranked fixes. Use this skill whenever the user asks "does this sound AI-written", "run this through the AI detector", "score this writing", "check this for AI tells", "would this pass as human", "humanize check", or wants any article, blog post, email, or copy audited for AI patterns before publishing. Also use it when the user pastes or points to text and asks how it reads, whether it's too "ChatGPT-ish", or wants a QA pass on generated content. Works on pasted text, files, and URLs.
---

# AI Writing Detector

Score writing for the density of AI-generation tells. This skill does **not** claim to detect authorship — detectors are unreliable in both directions, plenty of humans write in these patterns, and well-edited AI output avoids them. What it measures is real and actionable: how strongly the text exhibits the pattern cluster readers recognize as generated. Every report carries that framing.

The scoring model inverts the usual detector logic: the strongest tells are **absences** (no stance, no texture, no evidence trail), not word choices. A text can contain zero banned words and still score badly because it commits to nothing and could be published by anyone.

## Workflow

**1. Ingest.** Accept pasted text, a file path, or a URL (fetch it). Strip navigation/boilerplate if fetched. If the text is under ~150 words, warn that scores on short texts are noisy and skip the rhythm category (weights renormalize).

**2. Mechanical pass.** Run `scripts/tells_metrics.py <file>` (write pasted text to a temp file first). It returns JSON: lexicon hits, signpost phrases, hedge density, em-dash/triad/bold/colon densities, "not just X but Y" frames, paragraph and sentence rhythm uniformity (as coefficients of variation), and bullet share — with reference thresholds. If code execution is unavailable, estimate these by reading; say so in the report.

**3. Judgment pass.** Read the full text and score what no script can:

- **Stance**: Does the writer make at least one judgment that could be disagreed with? Are weak options given false equal weight? Are hedges doing the work of actual conditions?
- **Texture**: Specifics (numbers, dates, prices, named tools, edge cases, failure modes) vs. adjectives. Placeholder-people anecdotes ("imagine Sarah, a small business owner"). "Studies show" with no citation. Does anything here suggest someone actually did the work?
- **Audience awareness**: Are basics the intended reader obviously knows being explained? Are the reader's real objections addressed or dodged?
- **The 500-companies test**: Could this be published by 500 different companies/authors after swapping names and places? This is the single heaviest question in the model.
- **Structural intent**: Are sections evenly sized regardless of value? Does the conclusion restate the intro? Does anything digress, or does it march through an outline?

**4. Score.** Weighted categories, each scored 0–100 where **higher = more tell-like**:

| Category | Weight | Primary evidence |
|---|---:|---|
| Substance & stance | 35% | Judgment pass: 500-companies test, stance, false balance, hedging |
| Texture & specificity | 25% | Judgment pass: specifics, anecdote authenticity, evidence trail |
| Rhythm & structure | 20% | Script CVs + judgment: uniformity, symmetric sections, signposts, restating conclusion |
| Constructions & tics | 12% | Script: triads, em dashes, "not just X but Y", bold/colon density, bullet share |
| Lexicon | 8% | Script: banned-phrase hits per 1000 words |

Overall = weighted sum. Bands: **0–20 clean** (reads like a person who knows the subject), **21–40 light tells** (publishable; minor cleanup), **41–60 noticeable** (an attentive reader will clock it), **61–80 strong** (reads generated), **81–100 template-grade** (the 500-companies article).

Calibration guardrails: a text with genuine stance and texture should never score above 40 on lexicon hits alone — cap the influence of low-weight categories at their weight, no halo effects. Conversely, spotless mechanics cannot rescue a text that fails the 500-companies test; Substance & stance below is scored on content, not polish.

**5. Report.** Deliver in chat (create a file only if asked):

```
## AI Tells Score: NN/100 — [band]

| Category | Score | Weight | Key evidence |
|---|---:|---:|---|
| ... one row per category ...

### Flagged evidence
- [category] "short quoted excerpt" — why it reads generated
  (5–10 items max, worst first; quote at most a sentence each)

### Top fixes, ranked by score impact
1. ... (tie each fix to the category and points it would recover)

*This measures tell density, not authorship. Human writing can score high;
edited AI output can score low. Use it as an editorial QA signal.*
```

Number the fixes by expected impact — a stance fix is worth more than deleting every "delve". If the user then asks to fix the text, apply the fixes yourself; the rewrite must not introduce new tells (no fake anecdotes, no deliberate errors, no forced sass).

## Comparison mode

If given two versions ("did my edits help?"), score both, show the deltas per category, and name which edits moved which categories.

## Hard rules

- Never render an authorship verdict ("this was written by AI") — report tell density and evidence only.
- Never recommend fake typos, invented anecdotes, fabricated experience, or detector-evasion tricks as fixes. Fixes add stance, specificity, and asymmetry — they never manufacture fake humanity.
- Quote flagged excerpts at one sentence maximum; the report analyzes the text, it doesn't reproduce it.
- Score the text as its intended reader would experience it: a technical audience tolerates more structure; a narrative audience tolerates less.
