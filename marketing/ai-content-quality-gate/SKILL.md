---
name: ai-content-quality-gate
description: "Reviews Artificial Intelligence (AI)-assisted marketing content before publication and returns a publish / revise / kill verdict with an AI-tell detection checklist, a brand-voice score, a factual-claim verification log, an originality and added-value test, and line-level fixes. Use when reviewing a blog post, landing page, email, or social post drafted with an AI writing tool; setting up an editorial review step for AI-generated content at scale; content sounds generic or machine-written; or claims and statistics in a draft need verification before publishing."
---

# AI Content Quality Gate

> AI makes drafting free - this skill makes sure what ships is still worth a reader's time and safe to put your name on.

## What this skill is

A pre-publication review workflow for marketing content produced with help from Large Language Model (LLM) writing tools. It checks five things in order: whether the piece is factually safe, whether it adds something a reader could not get from asking an assistant directly, whether it sounds like the brand rather than a model, whether it is structurally sound, and whether it meets channel requirements. It ends in a clear verdict with specific fixes, so editorial review becomes a consistent gate instead of a matter of taste.

## What it solves

- Published statistics, quotes, or case details that were invented by a model
- Content that is fluent but says nothing a reader could not get from a general-purpose assistant
- Recognizable AI tells that erode reader trust and brand distinctiveness
- Inconsistent editorial standards across writers, agencies, and AI tools
- Search and social content penalized or ignored for low added value
- Review feedback like "make it pop" instead of actionable line edits

## When to invoke

- Before publishing any AI-assisted blog post, landing page, email, or social post
- Setting a standard review step for a team producing AI-drafted content at volume
- Auditing a backlog of existing content for quality and accuracy
- A draft feels generic, padded, or obviously machine-written
- Content includes statistics, customer claims, or competitor comparisons

## Phase 1: Intake

Record: content type, channel, target reader, single goal (inform, convert, retain), primary claim, brand voice guide (or 3 approved reference pieces), and which parts were AI-drafted. Without a voice reference, Phase 4 scoring is not reliable - ask for one.

## Phase 2: Factual-claim verification log

Extract every checkable claim and verify before anything else. A single fabricated fact is an automatic block.

| Claim | Type | Source cited | Verified? | Source quality | Action |
|-------|------|--------------|-----------|----------------|--------|
| | Statistic / quote / customer result / product capability / competitor statement / date | | Yes / No / Partial | Primary / secondary / none | Keep / correct / cite / cut |

Rules: statistics need a named primary source and year; quotes need a confirmed speaker; product capabilities must match the current release; competitor statements must be verifiable public facts; customer results need approval.

## Phase 3: Originality and added-value test

Ask: could a reader get this answer by asking a general-purpose assistant the headline as a question? Score each 0-2:

| Added-value signal | 0 | 1 | 2 |
|--------------------|---|---|---|
| First-party data or results | None | Referenced | Central to the piece |
| Expert experience | Generic | Some specific examples | Named practitioner insight, lessons learned |
| Point of view | Balanced summary | Mild stance | Clear, argued position |
| Specificity | Abstract advice | Some examples | Concrete steps, numbers, templates |
| Unique asset | None | Minor (quote, chart) | Framework, tool, dataset, or case study |

```
Added-value score = sum of the five signals (0-10)
```

Under 4 is a commodity piece; it is a kill or a full rewrite regardless of polish.

## Phase 4: AI-tell detection and brand-voice score

AI-tell checklist (count occurrences, flag lines):

| Tell | Example pattern |
|------|-----------------|
| Inflated openers | "In today's fast-paced world", "In the ever-evolving landscape" |
| Stock vocabulary | delve, tapestry, unlock, elevate, seamless, robust, game-changer, navigate the complexities |
| Rule-of-three padding | Lists of three adjectives or clauses in most paragraphs |
| Contrast formula | "It's not just X, it's Y" repeated |
| Hedged non-claims | "can potentially help", "may play a role" |
| Uniform rhythm | Every paragraph the same length; every section ends with a summary line |
| Generic conclusions | "In conclusion", restating the introduction |
| Unsourced authority | "Studies show", "experts agree" |
| Emoji or heading overuse | Decorative structure with thin content |

Brand-voice score, 1-5 per dimension against the voice guide:

| Dimension | 1 | 5 |
|-----------|---|---|
| Vocabulary | Generic, model-default words | Brand's own terms and phrasing |
| Tone | Mismatched (too formal or too casual) | Matches reference pieces |
| Sentence rhythm | Uniform | Varied, natural |
| Perspective | Faceless | Recognizable point of view |
| Reader fit | Written for everyone | Written for the stated reader |

## Phase 5: Structure and channel checks

- Headline promise is delivered in the body
- The first 2 sentences state the point; no throat-clearing
- One idea per section; every section earns its place
- Call to action matches the stated goal
- Channel requirements: length, links, accessibility (alt text, descriptive links), legal disclaimers, required AI-use disclosure where policy or regulation calls for it

## Phase 6: Verdict

| Verdict | Criteria |
|---------|----------|
| Publish | All claims verified, added-value 7+, voice average 4+, 3 or fewer AI tells, structure and channel checks pass |
| Revise | All claims verified or fixable, added-value 4-6 or voice average 3-3.9 or 4+ AI tells; return with line edits |
| Kill | Any unverifiable material claim that the piece depends on, added-value under 4, or the piece duplicates existing content |

Every Revise verdict includes: the top 3 changes that most improve the piece, line-level rewrites for flagged tells, and the claims to fix or remove.

## Output

- Verdict (Publish / Revise / Kill) with the criteria that drove it
- Factual-claim verification log
- Added-value score with the weakest signals named
- AI-tell list with line references and suggested rewrites
- Brand-voice scorecard
- Prioritized revision list (top 3 changes first)

## Operating rules

**Always**
- Verify facts before judging style
- Ask for a brand-voice reference before scoring voice
- Give line-level fixes, not general impressions
- Judge whether the piece adds value beyond what an assistant would answer directly
- Apply the same thresholds to human-written and AI-assisted drafts

**Never**
- Pass content containing an unverified statistic, quote, or customer result
- Treat removal of AI tells as sufficient when the piece has no added value
- Fabricate replacement sources or data when a claim fails verification
- Rely on AI-detection tools as proof of authorship
- Publish competitor comparisons that cannot be backed by public, dated evidence
