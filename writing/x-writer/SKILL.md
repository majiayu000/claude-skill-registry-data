---
name: x-writer
description: |
  Writing format, image generation, and pipeline for X (Twitter) content.
  Paragraph-based medium form, Fischerian Hooks, anti-performance writing.
  Progressive disclosure: article format scoring, thread/article images,
  comic strip generation, full brainstorm→polish→schedule pipeline.
  Built for use with OpenWriter.

  Use when: "/x-writer", "write for x", "x post format", "write this tweet",
  "format this post", "how should I write this", "format article",
  "evaluate article", "optimize article", "article image", "article cover",
  "thread images", "comic strip", "x comics", "comic panels", "generate panels",
  "polish tweet", "draft tweets", "write tweets", "write in my voice",
  "schedule tweet"
metadata:
  author: travsteward
  version: "0.2.1"
license: MIT
---

# X Writer

The writing format for X content. This skill defines HOW to write — not WHAT to write about. Apply these patterns to all tweets, threads, quote tweets, and replies.

## Core Philosophy

**The line-by-line style is dead.** Broken up, one-sentence-per-line writing signals EFFORT. It says "I am trying to get your attention." People see through it. They turn off. The pithy fragment style is the format of engagement farmers, not thinkers.

**We write in paragraphs.** Clean, flowing, natural paragraphs. Like a smart person talking to you, not a copywriter performing for you. The authority comes from the IDEAS, not the formatting tricks.

## The Fischerian Hook

Named after Fischer King (@FischerKing64), who demonstrates the pattern naturally.

**The first sentence of every paragraph is the hook.** It's a strong, declarative statement that pulls the reader in. Not a question. Not a teaser. A position.

Examples from Fischer King:

> "The worst part about people in white collar professions claiming they work '80-100 hours a week' is that they are all liars."

> "Every living President is watching Trump and realizing he lost the opportunity to shape the future of the country."

> "The most disturbing aspect of Gordon Ramsay's 'Kitchen Nightmares' is the revelation that so many restaurants are just microwaving your meal."

The hook is a complete thought that makes you want the next sentence. The paragraph then builds, explains, or lands the point. The hook isn't bait — it's the thesis.

**What a Fischerian Hook is NOT:**

- "Here's what nobody tells you about X..." (teaser bait)
- "I need to talk about something." (vague attention grab)
- "This." followed by a screenshot (lazy engagement)
- One-word sentences for "impact" (performance writing)

## Format: Medium Form

**Optimal length: 4-5 paragraphs.** Range: 3-6. This is the sweet spot for extended thought without losing attention.

- **3 paragraphs** — minimum for a real argument. Setup, development, landing.
- **4-5 paragraphs** — optimal. Enough room to build a framework, give evidence, and close with impact.
- **6 paragraphs** — maximum before you're writing an article. If you need more, make it a thread or an X Article.

**Each paragraph is 2-4 sentences.** Not one-liners. Not walls of text. Natural paragraph length that breathes.

**For threads:** each tweet is its own medium-form post (3-5 paragraphs). The thread isn't one long essay chopped up — it's a sequence of self-contained posts that build on each other.

## Anti-Performance Rules

1. **No single-sentence paragraphs for emphasis.** If a sentence is important, it lives inside a paragraph where the surrounding context makes it hit harder.

2. **No line breaks within paragraphs for dramatic effect.** A paragraph flows. If you need a new thought, start a new paragraph.

3. **No "Let me explain" or "Here's the thing" throat-clearing.** Start with the point. The Fischerian Hook eliminates all preamble.

4. **No emoji anchors.** No starting lines with emoji to create visual structure. The writing IS the structure.

5. **No rhetorical question chains.** "What if I told you...? What if everything you knew was wrong?" — this is performance, not writing.

6. **No trailing ellipsis for mystery.** "And the answer might surprise you..." — say the answer.

## Voice Characteristics

- **Declarative, not questioning.** State positions confidently. "This is how it works" not "Have you ever wondered how it works?"
- **Specific, not vague.** Names, numbers, studies, references. "Researchers butchered 30 deer with 60 handaxes" not "Studies show that..."
- **Conversational but not casual.** Like talking to a smart friend at dinner, not like texting. No slang, no "lol", no "ngl."
- **Variable sentence length.** Mix short declarative sentences with longer explanatory ones. The rhythm is natural speech, not metronome.
- **Authority through knowledge, not tone.** Don't TELL them you're an authority. Demonstrate it by knowing things they don't.

## Thread Format

When writing threads, each tweet follows the same medium-form paragraph rules:

1. **Tweet 1 (Hook tweet):** 3-5 paragraphs. First paragraph's first sentence is the thread hook — the reason someone stops scrolling. Include the primary image if there is one.

2. **Body tweets (2-N):** Each is a self-contained medium-form post. Each has its own Fischerian Hook. Each could stand alone as a tweet, but builds on the thread's argument.

3. **Close tweet:** Lands the framework. Not a call to action ("Follow for more!"). Not a summary. The final insight that makes the whole thread click.

**Thread images:** Each body tweet can have a progression image or supporting visual. Images support the argument — they don't replace it.

## Voice: Always Apply

Every piece of X content MUST be run through `/authors-voice` (or `/voice-apply`) before it's considered done. The x-writer skill handles format and structure. The voice skill handles tone, word choice, and eliminating AI tells.

> **Preferred path: OpenWriter's built-in Author's Voice "Enhance" plugin** (API-backed, full corpus RAG) — beats local Apply-minion briefs for X rewrites every time.

**AI tells to eliminate:**
- "Furthermore", "moreover", "additionally" — conjunction stacking that no human uses in casual prose
- "It's worth noting that" — throat-clearing
- "This is particularly important because" — explaining why something matters instead of just stating it
- "In essence", "fundamentally", "at its core" — filler abstractions
- "Arguably", "undeniably", "unquestionably" — hedging or over-asserting
- "Landscape", "paradigm", "ecosystem", "leveraging" — corporate AI vocabulary
- "Delve", "tapestry", "nuanced" — the most flagged AI words on the internet
- Balanced "on one hand / on the other hand" structures — real people take positions
- Ending with an inspirational reframe or call to reflection — just end

**The workflow (single pipeline — `/x-writer` does all three):**
1. **Format:** Draft content applying x-writer format rules (Fischerian hooks, paragraph structure, medium form)
2. **Polish:** Pull from the top 10 advertising practitioners in history. Score each rewrite 0-100. Don't stop until you hit 90%.
3. **Voice:** Run `/authors-voice` (or `/voice-apply`) to rewrite in your authenticated voice + anti-AI detection
4. **Final check:** If any sentence sounds like it came from ChatGPT, rewrite it

## Progressive Disclosure — Sub-Docs

Load on demand based on the task:

- **OpenWriter mechanics** — `tweetContext` / `articleContext` metadata, `content_type` (`tweet` / `reply` / `quote` / `article`), thread HRs, image handling, paragraph spacing, parent-tweet workflow → [`docs/openwriter-mechanics.md`](docs/openwriter-mechanics.md)
- **Article format** — evaluate (7-dimension score) or optimize X Articles. 10 rules for scroll-stop engagement → [`docs/article-format.md`](docs/article-format.md)
- **Images** — generate covers + thread images. 5 styles (Dark Editorial, Cinematic Realism, Abstract/Conceptual, Raw/Documentary, Dark Infographic), decision tree, character references → [`docs/images.md`](docs/images.md) + [`docs/images/`](docs/images/) (styles, characters, workflow)
- **Comics** — character-consistent comic strip panels for threads. 4 comic-specific styles, full pipeline → [`docs/comics.md`](docs/comics.md) + [`docs/comics/`](docs/comics/) (styles, characters, workflow)
- **Pipeline** — full brainstorm → polish (Author's Voice) workflow; scheduling/posting hands off to OpenWriter native (`mcp__openwriter__schedule_post`, `post_to_x`) → [`docs/pipeline.md`](docs/pipeline.md)

## Scripts

- `scripts/polish.js` — call Author's Voice `apply_voice` for tweet polishing
- `scripts/generate-image.js` — Gemini image generation with reference image support
- `scripts/characters/` — character reference PNGs for consistent multi-panel/thread image sets (user-supplied)

## What This Skill Does NOT Cover

- **What to write about** — topic strategy is outside this skill's scope
- **Posting/scheduling** — OpenWriter native: `mcp__openwriter__schedule_post`, `post_to_x`, `manage_schedule`
- **Scoring/prediction** — see grok-score skill
- **Reading tweets** — see x-reader skill ($0 fxtwitter reads)
- **Direct X API access** — see x-api skill (post-only per cost rule, when not going through OpenWriter)
