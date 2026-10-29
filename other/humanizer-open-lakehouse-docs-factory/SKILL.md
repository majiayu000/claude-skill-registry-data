---
name: humanizer
description: |
  Remove AI writing patterns from a docs page (content/) or a blog draft
  (blogs/) without changing facts or flattening the author's stance. Two modes:
  `docs` keeps prose plain and uniform, `blog` preserves voice. Use when asked
  to humanize text, when prose "sounds like AI" or "too robotic", or as the
  last pass of drafting and revising.
argument-hint: 'Path to a content page or blogs/<slug>/index.md, optional mode:docs|blog'
---

# humanizer: remove AI writing patterns

Scan a file for the patterns in [`references/patterns.md`](references/patterns.md)
and rewrite the flagged passages. The catalog has 33 patterns, adapted from
[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
and [blader/humanizer](https://github.com/blader/humanizer). Read its
[Detection guidance](references/patterns.md#detection-guidance) before
rewriting anything: look for **clusters** of tells, not one em dash or one
formal word.

## Mode

The mode follows the path unless the caller sets it.

- **`docs`** (`content/**`). Plain, uniform, present tense. Remove the
  patterns. Don't "add soul", inject opinion, or vary rhythm for its own sake.
  Neutral writing is the right human voice for a how-to or reference page.
  Em dashes go (pattern 14).
- **`blog`** (`blogs/**`). The author's stance, first person, and rhythm are
  features (`blogs/QUALITY.md` facet (b), `blogs/CONVENTIONS.md` §8). Remove
  the patterns, not the point of view. Sterile, voiceless prose is a defect
  here too. Vary rhythm, keep specifics, and allow some edge. Flag em-dash
  overuse only.

## What a rewrite must not change

- Code, inline code, commands, paths, URLs, `file=` fences, directive lines
  (`:::tab[…]`, `::::journey`), `model:` link targets, and frontmatter.
- Numbers, versions, identifiers, error strings, and anything inside a table
  or a `<!-- compat: -->` block.
- Load-bearing hedges and conditions ("may", "if", "not supported", security
  and cost caveats). "May incur charges" becoming "incurs charges" is a
  factual regression.
- Quotations, and any list item that is really there (don't drop the third of
  three real things to avoid rule-of-three).

**Never add information.** A rewrite may cut, reorder, or rephrase. It must not
add a name, number, date, source, or claim the original didn't carry. A vague
sentence gets cut or flagged for the author, not given an invented specific.

## Steps

1. Read the file and `references/patterns.md`. Analyze prose only.
2. For each finding, record the line, the pattern, the current text, the
   suggested rewrite, and why. Self-check each suggestion: plain constructions
   (is/are/has) over ornate ones, the page's register, and in `docs` mode no
   `—` or `–` left.
3. When run interactively, ask whether to apply all, review each, or cancel.
   When a sub-agent runs it as a drafting pass, apply the rewrites and return
   the list.
4. After editing, run `uv run docsnip prose` on the result. A rewrite that
   introduces a hedge, a wrong product name, or an undefined acronym isn't
   done.

If nothing is found, say so: "No AI writing patterns detected in <path>."
