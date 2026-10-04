---
name: blog-research
description: Use when gathering sources for a blog post on this site — runs web research and produces a ready-to-paste APA reference list with DOIs pre-encoded so they survive MDX. Trigger on "research a post about X", "find sources for", "gather references", before drafting a long-form essay.
---

# Research sources for a post

Produces two things: working notes, and a reference list that can be pasted into a post
without breaking it.

## Prerequisite

The working doc must contain a `## Hypothesis` section. Check with:

```bash
yarn stage docs/research/<slug>.md --require research
```

If it is missing, run `blog-hypothesis` first. **Research without a falsifiable claim finds
only confirmation** — you gather what fits and never notice what does not. Do not back-fill
a hypothesis afterwards; one written after the evidence always matches it.

## Output location

```
docs/research/<slug>.md
```

Use the same snake_case slug the post will use. This directory is outside `data/`, so
Velite never ingests it. Append to the existing doc — the hypothesis is already there.

## Gathering

Use `WebSearch` / `WebFetch`, or the firecrawl skills for sites that need scraping.
Prefer primary sources: the paper over the summary, the filing over the press release,
the original post over the aggregator.

For each source record: author(s), year, exact title, publication, URL, DOI if one exists.
Capture these while reading — reconstructing a citation later is where errors enter.

## Citation format

APA 7, alphabetical by author surname, one blank line between entries. Match the existing
posts exactly: a bare `References` line after a `---` rule, **not** a `## References` heading.

```
---

References

Schluntz, E., & Zhang, B. (2024, December 19). Building effective agents. Anthropic. https://www.anthropic.com/engineering/building-effective-agents

Zadeh, L. A. (1965). Fuzzy sets. Information and Control, 8(3), 338–353. https://doi.org/10.1016/S0019-9958(65)90241-X
```

Disambiguate same-author-same-year with letter suffixes (`2025a`, `2025b`), ordered by date.

### Encode DOIs — this is the one that has actually broken the site

A raw `<` anywhere in the post makes MDX parse it as a JSX tag and the entire post
disappears with **no build error**. Legacy SICI DOIs contain angle brackets routinely:

```
BAD   https://doi.org/10.1002/(SICI)1097-0266(199708)18:7<509::AID-SMJ882>3.0.CO;2-Z
GOOD  https://doi.org/10.1002/(SICI)1097-0266(199708)18:7%3C509::AID-SMJ882%3E3.0.CO;2-Z
```

`<` → `%3C`, `>` → `%3E`. The encoded URL resolves identically. This shipped broken once
already (commit `974922b`) — encode every DOI as you write it, not as a cleanup pass.

### Mark what you could not verify

When a source is shaky, say so inline with `⚠` rather than dropping it or presenting it
as solid. This is an established convention in these posts:

```
Trivedy, V. (2025, October 24). The modern planning agent is really a dynamic, adaptive workflow generator. ⚠ earliest documented use of "harness engineering"; exact URL not re-confirmed

White paper. (n.d.). In Wikipedia. Retrieved 2026. ⚠ tertiary source, used only for the document-type history; Churchill White Paper (1922) as an early named instance is not confirmed against a government primary
```

**Never invent a citation, a DOI, a page range, or a publication date.** If a detail could
not be confirmed, write what is known and flag the gap with `⚠`. A missing page number is
a small problem; a fabricated one is a serious one.

## Notes file structure

```markdown
# Research: <post title>

## Question

What the post is trying to establish.

## Findings

Claim → source → strength of evidence. Note where sources disagree.

## Gaps

What could not be confirmed, and what would confirm it.

## References

<the APA list, DOIs already encoded>
```

## Verify before handing off

Paste the reference block into a scratch file and check it:

```bash
yarn validate <that file>
```

Any `doi-encoding` or `raw-angle-bracket` error means a citation would have broken the post.

## Next step

→ `blog-write` to draft the post around these sources.
