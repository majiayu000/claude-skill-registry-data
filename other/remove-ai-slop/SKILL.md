---
name: remove-ai-slop
description: Use when the user pastes text and asks to make it "less AI", "less ChatGPT", "less slop", "more human", "humanize", "de-slop", "de-AI", "edit out the AI tells", "remove AI giveaways", "clean up this generated copy", or says "this sounds AI-generated". Also use when the user asks to check writing before publishing, or when pasted draft copy shows multiple co-occurring AI tells (em-dash overuse, hedging filler, promotional padding, recap intros, copula avoidance, bullet-and-bold soup, assistant scaffolding) even if the user hasn't named the problem.
---

# Remove AI Slop

Rewrite text so it no longer reads as machine-generated, while preserving the author's meaning, register, and voice.

## Three principles

1. **Preserve meaning.** No new claims, no dropped facts, no editorialising.
2. **Preserve register.** Formal stays formal (just less floridly so). Casual stays casual.
3. **Cut, don't rewrite, when you can.** A lot of slop is *padding*. Deleting "It is important to note that" beats rephrasing it.

## When to act, when to leave alone

Act when, in the same paragraph, **two or more tells of any category co-occur OR three or more vocabulary-table words appear** — that's the threshold for forced rewrite even if individually each one looks defensible. Single isolated tells are usually fine. (This is the unified rule in [`../../shared/spec.md`](../../shared/spec.md).)

Don't act on:
- A single em-dash in a paragraph
- One use of `robust` or `leverage` when it's the right word
- Lists when the content is genuinely list-shaped
- Formal register when context demands it (legal, academic, regulatory)
- Long sentences — long sentences are fine; slop is *empty* sentences

If the input is already clean, return it unchanged and add a single line: `*No changes — text reads as written by a human.*`

## Categories of tells

Each category has a dedicated reference file. **Read the reference only when you need it** — when you've spotted that category of tell in the input and need the full table or fix recipe.

- **Overused vocabulary** — `references/overused-vocabulary.md` — the big word→alternative table
- **Formulaic constructions** — `references/formulaic-constructions.md` — "X, not Y", "not only X but also Y", copula avoidance, rule-of-three filler
- **Padding and filler** — `references/padding-and-filler.md` — promotional padding, hedging filler, superficial-analysis `-ing` tails, vague attribution
- **Formatting tells** — `references/formatting-tells.md` — em-dash overuse, bullet-and-bold soup, title-cased headings, excessive bolding, redundant summary sections
- **Scaffolding and recap** — `references/scaffolding-and-recap.md` — "Certainly!", "I hope this helps!", recap intros, "In conclusion" outros, "Despite challenges..." closers
- **Elegant variation** — `references/elegant-variation.md` — synonym-swapping that humans don't do

## Apply user and project overrides

Before flagging vocabulary, read whichever of these exist (skip silently if absent):

1. `~/.claude/config/remove-ai-slop/user-vocabulary.md` — the user's personal additions
2. `~/.claude/config/remove-ai-slop/user-allow-list.md` — words the user never wants flagged
3. `.claude/skills/remove-ai-slop/overrides/user-vocabulary.md` — project additions
4. `.claude/skills/remove-ai-slop/overrides/user-allow-list.md` — project allow-list

**Merge order:** defaults → personal → project. **Allow-list wins everything:** if a word appears on any allow-list, never flag it, even if it's in the defaults or in another addition.

See `overrides/README.md` for the file format.

## Output rules

Return **the rewritten text only**, in the same format as the input (plain text, markdown, etc.). No preamble. No "Here is the rewritten version:". No bullet list of changes.

**Explanation is opt-in.** Only explain what changed if asked ("what did you change", "show me the diff", "annotate"). If asked, follow with a short bulleted list under a `## Changes` heading — one bullet per *category* of change, not one per edit.

**Heavy-rewrite warning.** If the input was so saturated with slop that the rewrite is materially different, end with: `*Heavy rewrite — original meaning preserved but most sentences restructured.*`

## When given a file

Preserve all non-prose elements unchanged: code blocks, frontmatter, tables, image references, links. Only touch the prose. If prose is intertwined with structural markdown, edit in place and keep the structure.

## Edge cases

- **User wrote it themselves and is asking for a check.** Same workflow — return the rewrite. Don't apologise or hedge ("This may have been written by a human, but…"). They asked.
- **User wants only specific fixes** ("just remove the em-dashes"). Do only that. Don't expand scope.
- **Very short input** (a single sentence). Apply the principles. If there's nothing to fix, say so in one line — don't invent problems.
- **Translation or transcription.** Some tells (formal register, slight stiffness) are translation artefacts, not AI tells. Be conservative.
- **Text is intentionally in an AI voice** (parody, satire, a quote of AI output). Ask before editing.

## Examples

See `examples/before-after.md` for worked rewrites covering each category.
