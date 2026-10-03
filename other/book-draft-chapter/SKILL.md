---
name: book-draft-chapter
description: Draft or revise a chapter of The AI Exoskeleton, grounded in canon files and source essays. Use when the user asks to draft, write, or revise a specific chapter by number or slug. Runs inline on main-context Opus (voice-sensitive work).
model: opus
---

# book-draft-chapter

Drafts or revises a chapter of *The AI Exoskeleton*. Always runs inline on the main Opus context. Never fork.

## Inputs

- **Chapter identifier**: a chapter number (1-10), `preface`, or `epilogue`. Slug forms like `start-with-claude-code` are also accepted.
- **Mode** (optional): `draft` (default, creates new) or `revise` (edits the existing file in place with a change log).

## Procedure

### 1. Load canon

Read every file in `canon/` before doing anything else. These are the `program.md` equivalent and define the book.

- `canon/thesis.md` — the argument the chapter must serve
- `canon/audience.md` — who's reading and what they walk away with
- `canon/book-voice.md` — book-specific voice rules
- `canon/outline.md` — locate the target chapter, read its synopsis and sourcing notes
- `canon/research-rules.md` — recency window (6mo default / 3mo preferred), citation tiers, anti-patterns
- `canon/book-craft-notes.md` — patterns for executive nonfiction the chapter should respect

Also read `~/.claude/rules/voice.md` (global voice authority). Book-voice extends it, does not replace it.

### 2. Identify the chapter

From `canon/outline.md`, extract for the target chapter:

- Chapter number
- Title
- Synopsis paragraph
- Sourcing row (which Run Data Run essays to lift, mixed, or net-new)
- Position in the three-act arc (Diagnosis / Exoskeleton / Operator's Manual)

Determine the filename: `chapters/NN-<slug>.md` where `NN` is zero-padded chapter number (`00-preface.md`, `01-two-groups.md`, ..., `10-what-changes.md`, `11-epilogue.md`).

### 2b. Check research file

Look for `research/<chapter-slug>.md`. If it exists, the chapter's grounding research has already been done — read it before drafting and treat it as the source of truth for any external claims.

If it does not exist and the chapter has any net-new external claims (anything not lifted from a Run Data Run essay), pause drafting and surface this to the user. Per `canon/research-rules.md`, research drives drafting, not the other way around. Do not draft new factual claims without sources.

The exception: heavy-reuse chapters whose external claims all live in the source essays already. For those, the source essays' citations carry forward and the research file can be lighter (or skipped if every external claim has an essay-level citation).

### 3. Pull source material (if reuse-heavy)

If the chapter's sourcing row indicates heavy reuse or mixed, locate the named essays. Run Data Run essays live at:

```
<your-blog-archive>/<period>/<slug>/
```

Each essay is its own folder. Read the published draft (look for the most-developed `.md` file in the folder, often named after the slug or `draft.md` or similar).

Known essay locations relevant to this book:
- *Start With Claude Code* → `<your-blog-archive>/claude-code-magnum-opus/` (verify the filename inside)
- *The AI Translation Problem* → `<your-blog-archive>/ai-translation/`
- *Art of the Impossible* → `<your-blog-archive>/art-of-the-impossible/`
- *Context Graphs* → `<your-blog-archive>/context-graphs-trillion-dollar-opportunity/`
- *The Convergence* → `<your-blog-archive>/the-convergence/`
- *Exoskeleton* (precursor) → `<your-blog-archive>/exoskeleton/`

If a source essay isn't where expected, search via `ls <your-blog-archive>/*/` before giving up.

For *DS Team Stuck at Level 2* and *1000 Small Bets*, search the blog directory by keyword if not obvious.

### 4. Plan the chapter

Before writing prose, sketch the chapter's spine in plain language inside your reasoning. Three to five beats max:

- Opening hook (a scene, a specific moment, a sharp claim — never a summary of what's coming)
- Two to three argument moves
- A turn at the end (question, instruction, or one-line takeaway — never a recap)

Make sure each beat advances the chapter's role in the overall thesis arc.

### 5. Draft

Length target: 2,800 to 3,200 words.

Voice rules (non-negotiable, all from `voice.md` and `book-voice.md`):

- No em-dashes anywhere
- No banned words/phrases (delve, leverage, crucial, vital, "is real", "the whole game", "stopped me cold", "here's what/why", etc. — see `voice.md` for the full list)
- Vary sentence length aggressively. Within each paragraph, at least one sentence under 8 words and one over 20. Never three consecutive sentences in the 12-18 word range.
- Vary paragraph length. Range from 1 to 7 sentences. No uniform 3-4 sentence blocks.
- Every page needs at least one concrete anchor: a named person, a specific failure mode, a dated event, a metric, a system that exists.
- Tier 4 baseline with controlled drops to tier 2.5 (at least one passage per chapter where the voice drops to colleague-at-a-whiteboard register).
- The word "exoskeleton" appears no more than three times per chapter. Rotate: "harness," "operator's setup," "the system you wear."
- No bullet lists where prose works. No tables unless the data needs one. No callout boxes. No code blocks longer than three lines. No screenshots. No epigraphs.

If the chapter is a heavy-reuse chapter, the source essay is structural input, not text to copy. Lift the argument and the named anchors. Rewrite all prose for book pacing, register, and continuity with adjacent chapters. The reader should not be able to tell which sentences came from which essay.

### 6. Post-draft scan

Before showing the draft, scan it against this checklist:

1. Banned words/phrases — grep mentally for each category in `voice.md`
2. Em-dashes — zero tolerance
3. Three or more consecutive sentences in the 12-18 word range
4. Three or more consecutive paragraphs of the same length
5. Any sentence that opens with "Here's...", "The short version:", "What actually matters:" or similar algorithmic scaffolding
6. Any paragraph that ends on dramatic upswing ("it's what we lose", "that's the real risk")
7. "Exoskeleton" used more than three times
8. Any abstract assertion without a concrete anchor within two sentences
9. Any sentence that sounds like a LinkedIn post
10. Any unverified factual claim (named person, dated event, metric, system) — flag with `[VERIFY]` inline; do not invent

Fix everything in this list before presenting. Do not present a draft with `[VERIFY]` markers as finished — flag them to the user explicitly.

### 7. Write to disk

Write the draft to `chapters/NN-<slug>.md` with this frontmatter:

```markdown
---
chapter: NN
title: <Title>
slug: <slug>
status: draft-1
word_count: <approximate>
sources: <comma-separated list of source essays used, or "original">
last_drafted: <YYYY-MM-DD>
---

# Chapter NN — <Title>

<prose>
```

If revising, increment `status` (`draft-2`, `draft-3`, ...) and append a one-line change note to a `change_log` array in the frontmatter.

### 8. Surface for approval

Report to the user:

- Filename written
- Word count
- One-sentence summary of the chapter's argument (not a recap of what's "in" the chapter — a statement of what it argues)
- Any `[VERIFY]` markers that need fact-checking
- Any deliberate voice or structure choices the user should know about
- Any source material that was missing or had to be substituted

Do not repeat the chapter prose in chat. The user reads it from the file.

## What this skill does not do

- Does not fact-check claims (that's `book-fact-check`)
- Does not run adversarial critique (that's `book-adversarial-reader` and `book-red-team`)
- Does not export to PDF/ePub (that's `book-export`)
- Does not commit the draft to git (the user does that explicitly)

## Failure modes to avoid

- **Drafting before reading canon.** Every session is fresh. Always read `canon/` first.
- **Lifting essay prose verbatim.** Heavy-reuse chapters need rewriting, not copying.
- **Inventing facts to fill gaps.** Use `[VERIFY]` and surface to user. Never fabricate a name, date, study, or metric.
- **Forking to a sub-agent.** This skill is voice-sensitive and runs inline on main Opus only.
- **Skipping the post-draft scan.** The scan is what separates this from generic LLM prose.
