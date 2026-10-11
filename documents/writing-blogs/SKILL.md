---
name: writing-blogs
description: Use when writing or editing a blog post, a documentation page or the README in envd-rs (website/content/**, README.md, docs/*.md). Plain, short, simple English, no AI-sounding words, charts for comparisons, English first with a Czech translation.
---

# Writing blog posts and docs

Readers are engineers, and many of them do not have English as their first language. Write so they understand every sentence the first time they read it.

## Sentences

- Put one idea in each sentence.
- Aim for 15 to 20 words. Split any sentence over 25 words.
- Put the subject and the verb near the start: subject, verb, object.
- Use active voice and present tense: "envd starts the process", not "the process is started by envd".
- Write "we" for the project and "you" for the reader.
- Mix short and medium sentences. Do not give every sentence the same length and rhythm.

## Words

- Pick the common word: use, start, help, show, about, so. Not `utilize`, `commence`, `assist`, `demonstrate`, `approximately`, `consequently`.
- Replace a phrase with one word when you can: "many", not "a number of".
- Use each technical term in one meaning, and keep the same term for the same thing everywhere.
- Explain an abbreviation the first time you use it.
- Drop words that judge instead of inform: simply, easily, just, obviously, clearly.
- No idioms, no jokes, no cultural references. They do not translate.
- Say the number: "2.0 times faster at p99", not "much faster".

## Words and patterns that sound machine-written

`scripts/check-prose.py` rejects them, and the git pre-push hook and the Claude Code hook run it. The full list lives in that script. The most common ones:

```
delve, tapestry, intricate, pivotal, landscape, foster, testament, multifaceted,
groundbreaking, transformative, paradigm, holistic, robust, leverage, synergy,
utilize, comprehensive, streamline, seamless, crucial, moreover, furthermore,
additionally, modern, cutting-edge, state-of-the-art, empower, unlock, elevate,
harness, effortless, blazing fast, powerful, journey, notably, enhance, navigate
"it's worth noting", "when it comes to", "in conclusion", "deep dive", "not just"
Czech: moderní, robustní, bezproblémový, revoluční, inovativní, klíčový, zásadní
```

Also avoid these patterns, even with plain words:

- `It is not X, it is Y` and `X is not just Y` framings.
- Lists that always have exactly three items.
- Announced insights such as "here is the real story".
- Invented crowds such as "most teams do X".
- Opening a sentence with a transition word (`Moreover`, `Additionally`).

## Characters

Use plain ASCII punctuation. The checker rejects:

```
arrows (U+2192 and friends): write "to" or rephrase
em dash and en dash: use a full stop, a comma or a colon; write "5 to 10" for ranges
ellipsis character, curly quotes, emoji
```

Czech files may use Czech quotes. Mermaid edges use ASCII (`-->`), and labels use a colon instead of an arrow.

## Structure of a post

1. **Title** that says the result, and a **description** of one or two sentences.
2. **Summary**: three to five bullets with the main numbers.
3. **Context**: what the thing is and why we measured or built it.
4. **Results at a glance**: charts first (`<CompareChart>` for Rust vs Go, `<Mermaid>` for flows), then a sentence on how to read them.
5. **Method**: versions, builds, hardware, tool, duration, what counts as noise. Another person must be able to repeat it.
6. **Details**: tables with the exact numbers.
7. **What made the difference**, **what did not work**, **known gaps**. Report the losses as clearly as the wins.
8. **Link to the source data** in the repository.

Keep paragraphs under 150 words, three to eight sentences. Give every section a heading that says what it contains. A one-sentence paragraph is fine.

## Numbers and claims

- Every number comes from a measurement in the repository or in CI. Name where it came from and when.
- Say what the setup was: CPUs, connections, duration, host.
- Call a difference under the run-to-run noise a tie.
- Do not round a loss away.

## Files and languages

- Posts live in `website/content/blog/<slug>.mdx`, docs in `website/content/docs/**`.
- English is the primary language. Each page has a Czech translation next to it as `<slug>.cs.mdx` (and `meta.cs.json` for docs folders), with the same structure, numbers and charts.
- Blog frontmatter: `title`, `description`, `author`, `date` (YYYY-MM-DD).
- Charts: `<CompareChart title unit note lowerIsBetter rows={[{ label, rust, go }]} />`. Diagrams: `<Mermaid chart={...} />`.

## Before you push

```bash
python3 scripts/check-prose.py
cd website && npm run build
```

Fix every finding by rewriting the sentence, not by swapping in a synonym from the same family.

## Sources

- Google developer documentation style guide, "Write for a global audience": https://developers.google.com/style/translation
- digital.gov plain language guide, "Write clearly and concisely": https://digital.gov/guides/plain-language/writing/clear-short
- Australian Government Style Manual, plain language quick guide: https://www.stylemanual.gov.au/style-manual-resources/quick-guides/quick-guide-plain-language
- Signs of AI writing: https://www.pounce.so/signs-of-ai-writing
