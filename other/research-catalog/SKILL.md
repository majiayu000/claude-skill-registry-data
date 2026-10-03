---
name: research-catalog
description: Whenever you do real external research (WebFetch, WebSearch, or Explore-agent fetches of URLs outside the repo), catalog it in docs/research/ before sending the synthesis back to the user. Credits the sources, captures the findings, and creates a traceable link from the decision back to the evidence.
---

# Research catalog and credit

> **No em-dashes.** Nothing this skill writes may contain an em-dash; use a comma, colon, or parentheses instead. Enforced by a repo hook that flags em-dashes in generated `.md`. See `/flagrare:write-docs`.

External research is someone else's work. The papers, blog posts, vendor docs, and open-source projects we lean on were written by named humans (or named orgs), and the project owes them three things: visible credit, a usable citation back, and a record of which decision their work informed. This skill is the way the project pays that debt.

It also pays a second debt, to the project's own future. ADRs say *what* was decided. Without a catalog of the research behind those decisions, the *why* drifts out of reach within months. This skill captures the evidence base alongside the decision, in a stable in-repo location, so a contributor six months from now can trace any non-obvious choice back to the work that justified it.

## When to invoke

Run this skill **immediately after** a research session that pulled in external sources, and **before** the synthesis is sent back to the user. Sources count as "external" when they came from:

- a WebFetch or WebSearch tool call
- an Explore-agent prompt that asked the agent to fetch URLs
- a referenced paper, blog post, vendor doc, or open-source repository you actually read

It does **not** apply to:

- Lookups inside the repo (`git log`, `grep`, file reads).
- Re-stating prior research without re-fetching anything.
- Trivial single-query lookups like "what's the latest version of X" or "is package Y on npm".
- Internal reasoning that doesn't lean on a citable external source.
- **Research that informed the project's dev tooling or workflow rather than the project's subject matter.** A catalog entry in `docs/research/` documents *why the product is built the way it is*, not *how the team chose to build it*. If you researched a commit-message convention, a testing framework's idioms, a changelog-formatting style, a build tool's options, or an agent-skill's calibration, that research belongs with the tooling it informed (a doc in the tool's own repo, a comment in the relevant config, a memory entry in the agent's working files). It does not belong in the project's research log alongside research about the project's actual domain.

The trigger is the conjunction of two things:

1. *Did external work inform the answer the user is about to read?* If no, don't catalog.
2. *Is the work the user is about to read part of the project's premise, its subject matter, the problem domain it tackles, the design decisions about what it does for its users?* If no, don't catalog *here*, catalog with the tooling instead, or skip cataloging entirely if the tooling lives elsewhere with its own provenance.

The rule of thumb: if a stranger reading `docs/research/` learns something about *what the product is and why it's designed this way*, the entry belongs. If they only learn *how the team built it*, it doesn't.

## Procedure

### 1. Pick a slug

Format: `YYYY-MM-DD-topic` in kebab-case. Examples:

- `2026-05-18-llm-persona-best-practices`
- `2026-03-14-vercel-ai-sdk-providers`

If you've already done research on a related topic *today*, append to that file rather than creating a new one. New sources get appended to its `## Sources` section; the synthesis section grows.

### 2. Create or open `docs/research/<slug>.md`

If `docs/research/` does not exist, create it now. Use the file template below.

### 3. Fill in one source entry per source

Only catalog sources that actually informed the synthesis. Don't pad the list with sources you skimmed and abandoned. Don't pad with sources you "could have used." The catalog reflects what the answer was *built from*, not what was *available*.

### 4. Update `docs/research/README.md`

If this file does not exist, create it using the index template below. Add a row linking the new catalog file. Keep the index in reverse chronological order (newest at the top).

### 5. Cross-link in the consuming artifact

Wherever the findings actually land, an ADR, a memory file, a code comment, a TSDoc block, reference the catalog file. The cross-link is what closes the loop. If a decision can't point at the research that justified it, the catalog isn't doing its job.

A typical cross-link looks like:

> *Based on research in [`docs/research/2026-05-18-llm-persona-best-practices.md`](../research/2026-05-18-llm-persona-best-practices.md).*

## File template

```markdown
# Research: <human-readable topic>

- **Slug:** `<YYYY-MM-DD-topic>`
- **Date:** YYYY-MM-DD
- **Status:** complete | in-progress
- **Triggered by:** <what prompted this, a task #, an ADR draft, a question raised in chat>
- **Informed:** <where the findings landed, link to ADRs, src files, memory entries, etc. Fill in as cross-links are made.>

## Question

<One paragraph stating the actual question being researched. Be specific. "Best practices for LLM persona instructions" is OK; "LLM stuff" is not.>

## Sources

### [<Title>](<URL>)
- **Authors / Org:** <names if known, or "Anthropic", "OpenAI", etc. If anonymous or uncredited, say so.>
- **Type:** vendor doc | academic paper | engineering blog | open-source project | spec | news article | other
- **Published:** <YYYY-MM-DD if known, else "unknown" or "ongoing">
- **Accessed:** YYYY-MM-DD
- **Relevance:** high | medium | low
- **What this contributed:** <2-4 sentences. What did this source give us that the synthesis depends on? Not a summary of the source, a description of its contribution to OUR answer.>
- **Quoted:** (optional, when a finding hinges on specific phrasing)
  > "<verbatim quote>"

### [<Next source title>](<URL>)
…

## Synthesis

<The distilled answer to the question. This is the work product. It should be readable on its own, someone landing here cold should learn what was concluded and why. Cite source entries by linking back to them inline where they support a specific claim.>

## Downstream uses

- <ADR / file / memory entry / chat answer this informed, with a link>
- <…>
```

## Index template (for `docs/research/README.md`)

```markdown
# Research log

External research conducted for this project. Each entry credits the sources it leaned on and links forward to where the findings landed (ADRs, code, docs). See the `/flagrare:research-catalog` skill for the workflow, or just read an entry to see the shape.

## Sessions

| Date | Topic | Triggered by | Informed |
|------|-------|--------------|----------|
| YYYY-MM-DD | [Topic title](./YYYY-MM-DD-slug.md) | <task # or context> | <ADR / file / etc.> |

## Adding a session

When you research something external (vendor docs, papers, blog posts, open-source repos), the `/flagrare:research-catalog` skill produces a file in this directory and a row in this table. Run it before the synthesis goes back to the requester.
```

## Style rules for entries

The point of the catalog is utility for a human reader who didn't do the research. Optimise for that.

- **Credit named humans where the source names them.** Author lists matter; first-author + et al. is fine when the list is long. If the source is anonymous or uncredited (a random blog post with no byline), say "uncredited author", don't fudge.
- **Be honest about source quality.** Tag every source with `Type`. Don't quietly smooth over the difference between "Anthropic's official prompt-engineering guide" and "a Medium post by someone with three followers". Reader needs to know.
- **Quote where the finding hinges on phrasing.** If the source says something with specific weight ("Anthropic recommends X"), put the verbatim quote in the entry. Paraphrasing a quote and then claiming the source supports your paraphrase is how citations rot.
- **Distinguish primary from secondary.** If you read a blog post that cites a paper, the primary is the paper and the secondary is the blog. Cite both; mark which is which. Go to primary whenever possible.
- **Date everything.** Web pages move. The `Accessed:` field is what someone re-checking your work needs.
- **Write findings, not summaries.** Each source's `What this contributed` field should answer: *what would the synthesis be missing if this source weren't here?* If the honest answer is "nothing", don't catalog it.

## Anti-patterns

- **Catalog as a receipt.** A wall of links with no per-source contribution sentence is just a fetch log. The whole point is to make the bibliography useful, not present.
- **Padding for credibility.** Citing ten sources to make the answer look researched when only three actually drove the conclusions. Cite the three.
- **Citing only the convenient sources.** If the research surfaced a contradicting view (e.g., persona prompting *hurts* factual accuracy on knowledge tasks), include it. Honest research has dissent.
- **Bare-URL citations.** `[Anthropic prompt engineering](https://platform.claude.com/…)`, not just the URL. Without a title the link is invisible to anyone scanning.
- **Forgetting the index.** A new file with no row in `docs/research/README.md` is unfindable.
- **Forgetting the cross-link.** The research catalog without a back-link from the consuming artifact (ADR, code, memory) is one half of a bridge.

## Cross-references

- `/flagrare:staleness-audit`, pre-commit check that includes a "if research was conducted, was it cataloged?" step.
- `/flagrare:release-check`, post-commit, separate concern.
