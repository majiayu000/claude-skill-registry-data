---
name: humanize
description: >
  Score and rewrite social captions and marketing copy so they don't read as
  AI-generated. A pre-review quality pass: run it on every caption batch before
  showing drafts to the user. Use when the user says "this sounds like AI",
  "make it sound human", "de-slop this", "humanize", "rewrite this caption",
  or asks why their posts feel generic. Every creation skill
  (plan-social-content, create-post-*) runs this pass automatically before its
  approval gate. The user's own brand rules (caption_writing_rules) always
  outrank this skill.
---

# Humanize

Score a draft against the AI-writing patterns below, fix what it flags, and
only surface drafts that score 90+. The user should never see a caption that
reads like ChatGPT wrote it.

Adapted from Wikipedia's "Signs of AI writing" patterns (via
ericosiu/ai-marketing-skills, MIT), tuned for short social copy.

## When to run

- Automatically: as the LAST step before any creation skill presents drafts
  for approval (plan-social-content batches, create-post-* captions,
  countdown series). Don't show the user the scoring math unless they ask —
  just fix and present clean drafts.
- On demand: when the user pastes copy and asks to make it sound human.

Order of authority: platform hard limits (marky-api platform rules) >
the user's caption_writing_rules and feedback log > this skill.
If a brand rule says "always use emojis", emojis stay.

## Scoring

Start at 100, deduct per hit (same pattern stacks up to 2x its penalty).
Ship at **90+**. Below 90: fix the top deductions and rescore, max 3 rounds.

### The #1 tell (fix on sight)

Negation definitions: "This is not X. This is Y." / "It's not just X, it's Y."
Say what something IS. Never define by negation.

### Banned vocabulary (−5 each)

delve, tapestry, landscape (abstract), leverage, multifaceted, nuanced,
pivotal, realm, robust, seamless, testament, transformative, underscore,
utilize, whilst, embark, comprehensive, intricate, commendable, meticulous,
paramount, groundbreaking, innovative, cutting-edge, synergy, holistic,
paradigm, ecosystem, crucial, enhance, fostering, garner, showcase, vibrant,
profound, renowned, breathtaking, nestled, stunning, elevate, game-changer,
unlock, supercharge, effortless

### Content patterns

| # | Pattern | Penalty | Fix |
|---|---------|---------|-----|
| 1 | Significance inflation — "a testament to", "pivotal moment", "reflects broader" | −10 | State the plain fact with a number or date |
| 2 | Vague attributions — "experts say", "studies show", no source | −8 | Name the source or cut the claim |
| 3 | Superficial "-ing" tails — "...showcasing our commitment, highlighting the importance of" | −8 | End the sentence at the fact |
| 4 | Promotional puffery — "boasts", "vibrant team", "profound commitment" | −8 | Concrete detail: headcount, result, date |
| 5 | Generic positive endings — "the future looks bright", "exciting times ahead" | −10 | End on a specific next step or a question |
| 6 | Formulaic challenge framing — "despite these challenges, X continues to thrive" | −10 | Name the actual problem and what changed |

### Language patterns

| # | Pattern | Penalty | Fix |
|---|---------|---------|-----|
| 7 | Banned-vocab clustering — 2+ banned words in one paragraph | −10 | Rewrite the paragraph in plain words |
| 8 | Copula avoidance — "serves as", "stands as", "represents" for "is" | −5 | Use is/are/has |
| 9 | Negative parallelisms — "not only X but Y", "it's not about X, it's about Y" | −5 | Make the positive claim directly |
| 10 | Rule-of-three overuse — forced triple adjectives/nouns/clauses | −8 | Keep the strongest one or two |
| 11 | Synonym cycling — "the CEO... the business leader... the company head" | −5 | Repeat the plain word |
| 12 | False ranges — "from X to Y" where X and Y aren't a scale | −5 | List the items plainly |

### Style patterns

| # | Pattern | Penalty | Fix |
|---|---------|---------|-----|
| 13 | Em-dash overuse — more than 1 per 200 words (Marky house rule: zero in external copy) | −5 | Periods and commas |
| 14 | Mechanical boldface on every key term | −3 | Bold nothing or one thing |
| 15 | Bolded-header-colon bullet lists everywhere | −5 | Prose or plain bullets |
| 16 | Title Case In Every Heading | −3 | Sentence case |
| 17 | Emoji as decoration on headings/bullets (🚀💡✅) | −5 | Emojis only where the brand voice uses them |
| 18 | Hashtag walls — a block of 10+ generic hashtags | −5 | Few, specific tags per platform rules |

### Communication + filler patterns

| # | Pattern | Penalty | Fix |
|---|---------|---------|-----|
| 19 | Collaborative artifacts — "hope this helps", "here is a caption", "let me know" | −10 | Delete; captions are the artifact |
| 20 | Knowledge-cutoff hedges — "as of 2025", "based on available information" | −10 | Verify and state, or cut |
| 21 | Sycophancy — "Great question!", "You're absolutely right!" | −8 | Delete |
| 22 | Filler phrases — "in order to", "it's important to note that", "at this point in time" | −5 each | "To", state it, "now" |
| 23 | Stacked hedging — "could potentially possibly" | −8 | One hedge max, or commit |
| 24 | Throat-clearing openers — first line restates the topic instead of hooking | −8 | Cut the first sentence; start at the hook |

## What good looks like

- An opinion or a specific claim, not reporting
- Short punches mixed with longer sentences
- Names, numbers, dates instead of adjectives
- is/has/does instead of elaborate verbs
- Reads at a 5th-grade level (Marky house rule)
- Sounds like the brand's samples in the brand profile, not like "content"

## Feedback

Friction or ideas while using this skill? Send it via the `submit_feedback`
MCP tool (see marky-api "Marky wants your feedback").
