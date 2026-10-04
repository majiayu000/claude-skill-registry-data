---
name: docs-writing
description: "Writing rules for the regelrecht docs site (docs/). Use when writing or editing prose under docs/ — RFCs, guides, component docs, concept pages, and the NL/EN landing copy. Keeps docs prose free of AI-generated tells and consistent with the site's government-technical register. Not for code, commit messages, or PR descriptions."
---

# docs-writing

Prose in `docs/` is read by lawmakers, civil servants, and developers outside the team. It must read as written by a person, and it must sit in one consistent register: precise, government-technical, unhurried. The failure mode is not "wrong" but prose that is technically fine yet pattern-matches to LLM output — a reader notices within a paragraph, and for a government transparency project that costs credibility.

This skill covers everything under `docs/`:

- **English technical docs** — `docs/src/content/docs/**` (guide, operations, components, concepts, reference) and `docs/src/content/rfcs/**`. These are English, in a government-technical register.
- **Bilingual landing copy** — `docs/src/lib/landing-content.ts`. NL is the original; EN is a translation kept in the *same* register. Edit both datasets together; never let them drift.

There is precedent for this problem in the repo: PR #888 stripped LLM stylistic tells from draft RFCs by hand. This skill is that cleanup made repeatable.

## The tool detects; you decide

`check-prose-style.mjs` (next to this file) is a linter, not an arbiter. It catches mechanical signatures — em-dashes, banned phrases, "not X, but Y" contrasts — so your attention is free for the things a regex cannot see: rhythm, rule-of-three, register, whether a flagged contrast is actually a tell.

**You are the arbiter.** Run the script, read each finding, and judge it. An `error` from the script is almost always right (em-dashes and banned phrases have near-zero false positives), so clear them all. A `warn` is a *candidate* — a regex flagged a "not ... but" that may be a dramatic contrast or may be incidental. Read the sentence and decide. Do not blindly rewrite every warning, and do not blindly trust a green run either: the script is silent on cadence and rule-of-three, which are the tells it cannot mechanize. A clean script plus a careful human read is the bar, not the script alone.

```bash
# From the repo root. No args => the default docs prose set.
node .claude/skills/docs-writing/check-prose-style.mjs

# One file (e.g. the RFC you just touched):
node .claude/skills/docs-writing/check-prose-style.mjs docs/src/content/rfcs/rfc-025.md

# Make warnings fail too, for a final gate:
node .claude/skills/docs-writing/check-prose-style.mjs --strict
```

`error` findings exit 1; `warn` findings are reported but exit 0 unless `--strict`. Code is stripped before matching (fenced blocks, inline `code`, and everything outside string literals in `.ts`), so `--no-verify`, `a - b`, and dashes inside code never trip it.

## What the script cannot see — check these by hand

The regex catches surface tells. These are the ones you read for:

- **Rhythm.** Vary sentence and paragraph length. Every sentence at 15–20 words and every paragraph at three sentences reads as machine-generated even when every word is right. This is the single biggest tell and the script is blind to it.
- **Rule-of-three.** "X, Y, and Z" noun lists in titles and opening sentences are the structural signature LLMs overuse most. Two or four items is fine; three is suspicious unless the three things genuinely exist. Read every heading and lede aloud.
- **Rhetorical-question-then-answer.** "The result? Faster builds." Cut the question, lead with the answer. (Not linted — too many real FAQ questions on this site to distinguish mechanically.)
- **Closing that restates the opening.** Trust the reader; end on the last real point.
- **Manufactured balance.** Perfectly symmetric bullet lists, every bullet ending in a neat summary clause, adjacent bullets starting with the same verb. Humans trail off and vary.
- **Hedge-stacking.** "I think", "perhaps", "it seems" on every sentence. One or two load-bearing hedges are fine; the pattern-frequency is the tell.

## Register for these docs

- **English docs are government-technical, not marketing.** State what a thing does and how. No "powerful", "seamless", "elegant", "robust" unless substantiated on the same line. The landing page sells; the docs explain.
- **Be specific and name things.** "The harvester converts BWB XML to YAML" beats "the tool processes the data". "RFC-007" beats "an earlier design". Link RFCs and concept pages by their real identifiers — the site auto-links `RFC-NNN`.
- **Criticism and limitations stated plainly.** "This does not handle cross-law cycles yet" beats "there may be some edge cases to consider". Docs that hedge every limitation read as generated.
- **Domain terms keep their form.** Dutch domain vocabulary (`bewindspersoon`, `toetsingsinkomen`, `machine_readable`, `open_terms`) stays as-is in English prose. Keycloak "realm", "IT-landschap", "klantreis" are real terms here, not banned words — that is why the linter leaves them alone.
- **Landing NL is the source of truth.** When you edit `landing-content.ts`, write or revise the NL string first, then bring the EN translation into the same register. A change to one dataset that skips the other is a bug.

## Docs-specific mechanics

- **Frontmatter is reader-facing.** `title` and `description` render on the page and in search results — they get the same anti-tell treatment as the body. RFC frontmatter has required fields (`title`, `status`, `implementation`, `topic`, `date`, `authors`; `topic` takes a value from `docs/src/lib/rfc-topics.ts`); see `rfc-000.md` and `template.md`. Ground `status` and `implementation` in the codebase, not the RFC's aspirations.
- **Mermaid diagrams need an accessible name** (enforced separately by the a11y gate). When you add a diagram, its meaning must also be legible from the prose around it — do not make the diagram load-bearing for a reader who cannot see it.
- **Do not hand-edit generated files.** If a page is code-generated, change the source. (The BDD grammar and RFC link-rewriting are generated; markdown content pages are not.)

## Hard rules (unconditional)

These hold even without opening the checklist:

- **No em-dashes (—), ever.** Comma, period, parentheses, colon, or rewrite. An en-dash (–) as prose punctuation is out too, but an en-dash inside a range is correct typography and stays: `art. 257a–257h`, `11.3–12.4:1`, `€5.212 – €7.747`, `32 – 36 uur`, `September–December`. The linter knows the difference.
- **American English** for English text (organize, analyze, behavior) unless told otherwise.
- **No emoji in running prose**, no random mid-sentence bolding for emphasis.

## Before you ship a docs change

1. Run `check-prose-style.mjs` on the files you touched. Clear every `error`.
2. Read each `warn` and decide: real contrast → rewrite; incidental → leave it.
3. Read your headings and ledes aloud. Rule-of-three? Rewrite.
4. Scan for uniform rhythm — vary it.
5. If you edited `landing-content.ts`, confirm NL and EN both changed and match register.
6. Build still passes: `just docs-build` (or `npm run build` in `docs/`).

Then, if the prose is going to Anne to paste somewhere, pipe it through `pbcopy`.
