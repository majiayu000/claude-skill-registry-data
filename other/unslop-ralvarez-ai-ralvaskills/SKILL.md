---
name: unslop
version: 1.0.0
description: Cut AI tells from any writing with numbered, citable rules (filler, vague attributions, AI vocabulary, forced threes, dash and bold habits, chatbot phrases). Use when editing or reviewing prose, docs, commit messages or reports, or when another skill says to write "through unslop".
---

# Unslop

Edit text to remove AI patterns. Scan for the patterns below, then rewrite. Preserve meaning and match the intended tone.

Rule numbers are stable ids that other skills cite. A removed rule leaves a gap, so the numbering follows upstream and a later upstream diff stays readable.

3. No trailing "-ing" phrases that add no fact ("highlighting...", "ensuring...").
5. No vague attributions ("experts believe"). Name the source or delete.
7. No AI vocabulary: additionally, crucial, delve, enhance, foster, landscape, pivotal, showcase, testament, underscore, vibrant.
8. Say "is" or "has", not "serves as", "stands as", "boasts", "features".
9. No "not just X, but Y". State the point.
10. Don't force ideas into threes.
11. One name per thing. Repeat it.
12. No "from X to Y" unless X and Y sit on a real scale.
13. No em dashes or en dashes. Prefer a period or a comma; where a dash reads better, use a spaced hyphen (` - `). Ranges use an unspaced hyphen (`2-4`).
14. A colon goes before a list or an example, never mid-sentence as a connector.
15. Don't bold every proper noun or acronym.
16. No bold label and colon that restates its line ("**Performance:** Performance improved..."). A bold lead-in that ends in a period and adds new detail is fine.
17. Sentence case headings.
18. No decorative emojis.
19. Straight quotes.
20. No chatbot phrases ("I hope this helps!", "Let me know if...").
22. No praise or agreement openers. Respond directly.
23. Cut filler. "In order to" becomes "to". Delete "it is important to note that".
24. One hedge at most: "may".
25. No generic conclusions. State specific plans or facts.
26. No abstract metaphor nouns: substrate, wedge, vector, nexus, primitive, harness, surface, scaffolding, paradigm, ratchet, north star, flywheel. Use the concrete word.
27. Say what it does, not how it feels. Name the mechanism or the number. Cut a sentence that could appear unchanged in another project's docs.
28. One idea per sentence. Split a sentence the reader has to reread.
29. Active voice. Name the actor unless it is unknown or doesn't matter.
30. Cut adverbs or use a stronger verb. Give the number.
31. Use the plain word: "use", not "utilize" or "leverage".
32. No metaphor, aphorism, personified code, or figurative verb where a literal phrase exists.
33. Write whole sentences with their articles and verbs. Spell out arrows and abbreviations.

## Divergence from upstream

Rule 13 differs on purpose. Upstream also bans hyphens used as dashes and parentheses in their place; this catalogue allows the spaced hyphen.

## Related skills

- [`commit-author`](../../workflows/commit-author/SKILL.md) and [`docs-architect`](../../workflows/docs-architect/SKILL.md) produce prose; run it through these rules before it ships.
- [`caveman`](../caveman/SKILL.md) is the opposite register, for output only a model reads; commits, docs and user replies are not caveman.

---

_Adapted from [cursor/plugins pstack `unslop`](https://github.com/cursor/plugins/tree/0b46ec399d55f2829e88822998f53b84944837d3/pstack/skills/unslop) by Lauren Tan (MIT). Changed for this workspace._
