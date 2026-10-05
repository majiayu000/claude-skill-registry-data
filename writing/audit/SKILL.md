---
name: audit
description: Review or draft prose so it reads like a person wrote it, not an AI. Catches AI-slop tells (cliché clusters, promotional register, "not just X but Y" parallelisms, copula avoidance, uniform sentence rhythm, and em-dash or emoji overuse) and suggests rewrites. Use when writing, editing, or reviewing docs, READMEs, blog posts, release notes, or marketing copy, or when the user asks to check content for AI slop, "sloppy AI", or to make writing sound human.
allowed-tools: Read
---

# slop-check

Make prose read like a person wrote it. This is a craft tool: the goal is a genuine voice that fits the piece, not a trick to fool an AI detector. Ignore detector scores entirely. They are noisy, and chasing them produces worse writing.

## The one rule that governs the rest

No single feature proves text is AI-written. Good human writers use em dashes, emoji, the word "delve," and the occasional cliché. The tell is a *cluster*: several markers stacked together, plus a flat, promotional register and a rigid shape. So weigh concentration and context, not isolated hits. One em dash in a strong paragraph is fine. Five em dashes, three "crucial"s, and a "in today's fast-paced world" in one section is slop.

Match the register, too. A playful blog post, a legal memo, and a terminal README have different rules. Fix what betrays a machine; keep what serves the reader.

## When reviewing a file or a passage

1. Read the target (a file the user names, a pasted passage, or the draft in progress).
2. Find the tells. Prioritize clusters and register over lone words.
3. For each finding, give four parts: its location, the pattern, why it reads as AI, and a concrete rewrite. Lay them out plainly (a short labeled line or a list). Do not string the parts together with em dashes, since this tool flags exactly that.
4. Offer a cleaned version of the worst paragraph so the fix is obvious.
5. Stay advisory. Do not rewrite the file unless the user asks. Preserve meaning, facts, and citations.

Order findings by severity. Lead with structure and register (the changes that matter), then phrasing, then punctuation and formatting.

## When drafting

Apply the same principles as you write, so the first draft is clean rather than something to scrub later. Vary sentence length. Prefer plain verbs. Cut a cliché before it reaches the page.

## High-signal tells to catch

The full, categorized catalog with examples and rewrites lives in [reference.md](reference.md). Load it when you need the exhaustive list or want to explain a call. The high-signal set:

- **Cliché clusters.** delve, leverage, tapestry, robust, seamless, pivotal, underscore, realm, vibrant, boasts, nestled, testament, foster, garner, intricate. Flag density, not a single use.
- **Stock phrases.** "it is important to note," "in today's fast-paced world," "plays a crucial role," "rich tapestry," "when it comes to."
- **Negative parallelisms.** "not just X, but Y," "it's not X, it's Y," "no X, no Y, just Z." LLMs reach for these to sound insightful; they usually correct a misconception the reader never held.
- **Copula avoidance.** "serves as," "stands as," "functions as," "acts as" replacing a plain "is" or "are." Restore the copula.
- **Rule-of-three padding.** Three adjectives or clauses where one would do, repeated across a piece.
- **Promotional register.** Travel-brochure adjectives and unearned significance: "vibrant," "nestled," "groundbreaking," "a testament to," "underscores its importance." Say what happened instead.
- **Hedging and vague authority.** "could potentially," "aims to," "experts argue," "studies show," "it is widely regarded" with nothing cited.
- **Uniform rhythm.** Sentences of the same length and shape, paragraph after paragraph. Break the pattern.
- **Formatting tells.** Em dashes standing in for commas, colons, or periods; decorative emoji; bold on every other phrase; Title Case On Ordinary Headings; horizontal-rule dividers between every section; smart quotes where plain ASCII is expected.
- **LLM leftovers.** "As an AI," "as of my knowledge cutoff," "I hope this helps," stray citation fragments like `oaicite` or `[cite: 1]`, and section-ending recaps that restate the section.

## House style (strictness)

Default to judgment: flag clusters and register, leave a well-placed em dash or emoji alone. For contexts that want zero tolerance, apply a strict house style: no spaced em dashes at all, no decorative emoji, ASCII quotes and apostrophes, sentence case in headings. If the user or the project states a house style, follow it over these defaults.

## What not to do

- Do not strip every em dash and emoji on sight. Used well, both are fine. Mechanical removal is its own kind of slop.
- Do not flatten a distinct voice into gray, hedged mush. Cutting slop should make writing sharper, not blander.
- Do not change meaning, drop citations, or invent facts while rewriting.
- Do not talk about detectors, detection scores, or "humanizing to pass a checker." That is not what this is.
