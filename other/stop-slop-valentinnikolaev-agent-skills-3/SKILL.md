---
name: stop-slop
description: Review or edit primarily English prose to remove formulaic AI-sounding phrases and structures while preserving meaning, evidence, qualifications, voice, formatting, and protected text. Use when the user explicitly asks to humanize, de-slop, remove AI tells, apply Stop Slop, or evade an AI-text detector; redirect detector-evasion requests toward ordinary quality editing without authorship or score promises. Do not invoke for routine drafting, standalone voice matching, code, creative voice, house-style work, or legal, academic, and technical precision edits unless the user explicitly requests Stop Slop treatment.
---

# Stop Slop

Remove formulaic writing without replacing the author's meaning or voice with another formula.

## Keep editing separate from detection

Treat `AI-sounding` as shorthand for formulaic prose, not an authorship verdict.

- Do not infer who wrote a passage, assign an AI probability, or promise that a rewrite will pass a detector.
- Do not optimize against detector scores or manufacture statistical irregularity.
- Do not inject typos, random synonyms, forced fragments, slang, anecdotes, dialogue, opinions, or personal experience to make text appear human-authored.
- If the user asks to beat a detector, explain this boundary briefly and offer an ordinary edit for clarity, specificity, rhythm, and voice.

## Preserve meaning before style

Treat semantic integrity as the highest-priority rule.

- Keep claims, numbers, names, dates, causal relationships, uncertainty, modality, and scope unchanged.
- Never add achievements, examples, evidence, metrics, credentials, or experience that the source does not contain.
- Preserve citations and source attribution.
- Preserve source-supported unusual details, mixed feelings, and unresolved tension when they carry the author's voice.
- Do not strengthen `may`, `some`, or `most` into universal claims.
- Do not remove legally, technically, or academically necessary qualifications.
- When a stronger rewrite needs missing facts, use an explicit placeholder or ask for them.

If a style heuristic conflicts with accuracy, genre, author intent, or readability, ignore the heuristic.

Separate formulaic delivery from weak substance. A rewrite cannot create originality, evidence, or earned authority that the source lacks; flag that gap instead of disguising it with style.

## Protect immutable spans

Do not alter these unless the user specifically includes them in scope:

- direct quotations and interview excerpts;
- code, commands, formulas, data, and configuration;
- citations, footnotes, URLs, and reference labels;
- product names, legal terms, defined terms, and proper nouns;
- placeholders, template variables, and required application fields.

Preserve Markdown, document structure, links, and other formatting outside the requested edit.

## Choose the operation

- **Review**: Identify formulaic patterns and explain targeted improvements. Do not rewrite or edit files.
- **Rewrite**: Return revised pasted prose while preserving its facts and structure unless the user requests broader restructuring.
- **File edit**: Edit only explicitly named files after the user asks for file changes. Inspect the diff and avoid unrelated formatting churn.

When the operation is unclear, prefer review for named files and rewrite for pasted text. Do not infer permission to edit a file from a request to review it.

## Choose the strength

- **Light**: Remove obvious filler and repetition while preserving nearly all phrasing.
- **Standard**: Remove recurring AI tells and improve rhythm without flattening genre or voice. Use by default after explicit invocation.
- **Strict**: Apply stronger compression for marketing, opinion, or outreach prose. Use only when the user asks for a strict or punchy rewrite.

For legal, academic, technical, policy, accessibility, or compliance prose, remain conservative even in strict mode.

## Match voice from evidence

Within an explicitly requested Stop Slop edit, read [references/voice.md](references/voice.md) when the user asks for their voice or supplies representative writing samples.

Let explicit voice instructions and repeated sample evidence override generic style heuristics when they remain appropriate for the target genre. Without a sample, preserve the target's existing register, strongest specific language, and deliberate quirks instead of choosing a preset persona. Never transfer facts, biography, opinions, anecdotes, quotations, or experiences from a voice sample into the target.

## Apply genre-aware heuristics

Read [references/phrases.md](references/phrases.md) when phrase-level patterns are relevant. Read [references/structures.md](references/structures.md) when rhythm or organization is the problem. Read [references/examples.md](references/examples.md) only when an example helps resolve ambiguity.

Treat every listed pattern as a diagnostic signal, not an automatic ban. Look for clusters, repetition, and mismatch with the genre or supplied voice; one word or punctuation mark is weak evidence.

1. Cut throat-clearing that delays the point.
2. Replace vague importance claims with the specific consequence already supported by the source.
3. Reduce repeated binary pivots, dramatic fragments, rhetorical setups, and meta-commentary when they feel mechanical.
4. Prefer active voice when the actor matters and is known; keep passive voice when the actor is unknown, irrelevant, deliberately withheld, or genre-appropriate.
5. Name human actors only when the source supports them. Do not invent an actor to avoid inanimate wording.
6. Vary rhythm according to the genre. Keep useful lists, questions, short sentences, and punctuation.
7. Preserve meaningful adverbs, transitions, emphasis, and em dashes when they carry precision or voice.
8. Avoid mirroring job titles, team names, document headings, or prompts as empty openers; retain them when the reader needs the context.
9. Replace generic claims of fit or impact with verified evidence already present, not fabricated specifics.
10. Remove revision residue such as redundant heading restatements, unraised objections, or fake alternatives when they add no information; preserve real objections, options, and change history where the genre needs them.
11. Keep one stable name for a referent instead of cycling through synonyms merely to avoid repetition.
12. Repair an awkward sentence or paragraph around its actual point instead of swapping each flagged word for a stock substitute.
13. After editing, scan for secondary convergence: a new opener, connector, sentence shape, or cadence that now repeats because it replaced the old formula.

## Respect language and voice

The bundled phrase and syntax references target English. For other languages, apply only the general goals of directness, specificity, semantic preservation, and natural rhythm unless the user supplies language-specific guidance.

Preserve deliberate dialect, humor, rhetorical style, brand voice, and memorable phrasing. Do not remove a construction merely because it could appear in AI writing.

## Validate the result

Before delivery:

1. Compare every factual claim, number, name, date, qualifier, and citation with the source.
2. Confirm protected spans and formatting remain intact.
3. Check that no placeholder became a fact and no example was invented.
4. If a voice sample was used, confirm that its habits transferred but its facts and persona did not.
5. Read the result aloud or simulate a careful read for genre fit, coherent rhythm, and preserved author voice.
6. Re-scan the finished passage for repeated replacement formulas and manufactured authenticity.
7. Remove only patterns that materially improved the text.

For review mode, return prioritized findings with exact excerpts and suggested revisions; add locations for long or file-based inputs, and distinguish style patterns from substance gaps. For rewrite mode, return the revised prose and briefly disclose any material structural change. For file-edit mode, summarize edited files and verification.

## License

See [LICENSE](LICENSE).
