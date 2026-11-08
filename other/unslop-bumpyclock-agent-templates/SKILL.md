---
name: unslop
description: Edit substantial prose to remove AI-style filler and repetition. Use for explicit style review or prose revision.
---

# Unslop

Apply the shared prose rules from `AGENTS.md`.
This skill owns the additional AI-tell catalog and editorial pass below.

Facts, exact quotations, identifiers, commands, code, notation, and necessary uncertainty take precedence over every style preference below. Preserve the requested genre, template, and intended meaning. The catalog identifies possible editing problems, not proof of who wrote a passage.

## Editorial pass

Apply the patterns that improve the requested prose. Check the revision for unsupported claims, lost qualifications, factual changes, and altered literals. Finish when the requested text is clearer and its meaning is intact, rather than continuing to rewrite merely to hide apparent AI authorship.

## Voice and genre

- **Opinions when appropriate.** Preserve or sharpen the author's supported position in criticism or advocacy. Keep impartial reports and factual notices impartial; do not invent a position to make them sound personal.
- **Vary rhythm.** Use sentence lengths that support clarity and the intended tone.
- **Acknowledge complexity.** Preserve material tradeoffs and uncertainty rather than adding a stock emotional reaction.
- **First person when appropriate.** Use "I" when it fits the genre and speaker. Do not manufacture personal experience, feelings, or credentials.
- **Avoid mechanical symmetry.** Use a natural structure unless a template, parallel comparison, or technical format benefits from consistency.

## Patterns to detect and fix

Rule numbers are stable local IDs.
Leave a gap after a rule removal.

### Content

1. **Puffery.** "pivotal moment", "testament to", "evolving landscape", "setting the stage for", "indelible mark", "deeply rooted". Cut puffery, state what happened.
2. **Name-dropping.** Remove decorative lists of media outlets. Keep attribution that lets the reader verify a material claim, and say what the source established.
3. **Promotional language.** "nestled", "vibrant", "breathtaking", "groundbreaking", "renowned", "stunning", "must-visit". Use neutral descriptions.
4. **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source when available. Remove empty attribution, not a material qualification, and do not present an unverified claim as established fact.
5. **Cutoff disclaimers.** "While specific details are limited..." Remove boilerplate only when it adds no useful limit. Preserve necessary uncertainty; verify consequential unknowns when sourcing is in scope rather than inventing facts or deleting caveats.
6. **Formulaic challenges.** "Despite challenges... continues to thrive." Replace with specific facts.

### Language

7. **"Not just X, but Y."** State the point directly instead.
8. **Rule of three.** Forcing ideas into groups of three. Use the natural number.
9. **False ranges.** "from X to Y" where X and Y aren't on a meaningful scale. List topics directly.

### Style

10. **Em dash overuse.** In ordinary editable prose, prefer periods or commas over em dashes, and a separate sentence over ornamental parentheses or substitute dashes. This is a style default, not a ban on punctuation needed for precision, exact quotations, technical syntax, or the requested format. Do not replace punctuation mechanically.
11. **Colon overuse.** Colons are useful before a list or example. Prefer a full sentence when a colon merely connects stock framing to a point. "If you're coming from traditional automation: instead of registering event handlers, you describe conditions" adds nothing with the colon. "Describing when the scheduler should fire works best as plain English" states the point directly. Preserve colons required by a format or technical syntax.
12. **Boldface overuse.** Don't bold every proper noun or acronym.
13. **Inline-header lists.** The tell is a bold label and colon that restates the line: "**Performance:** Performance improved...". Convert those to prose. A bold lead-in that ends in a period, names the item, and is followed by genuinely new detail ("**Schema in TypeScript.** Tables live in one file.") is fine, not a tell.
14. **Title case headings.** Prefer sentence case unless the requested style, source, or template requires otherwise.
15. **Decorative emojis.** Remove from headings and bullets.
16. **Curly quotes.** Prefer straight quotes in editable prose. Preserve exact source quotations, literals, and typography required by the requested format.

### Plain speech

17. **Mannered prose.** Prefer literal phrases over rhetorical fragments, personified code, figurative verbs, and stock framing phrases. Replace "A dial worth turning" with "a parameter worth varying". Replace an aphorism such as "wire it or delete it" with the concrete requirement.
18. **Over-compression.** Restore articles and verbs when terse fragments force the reader to decode prose. "Parser rejects bad date → exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing." Preserve literal code, CLI syntax, diagrams, and status labels.
