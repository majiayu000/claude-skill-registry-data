---
name: review-research
description: "Verify research findings against the sources they cite, in fresh sub-agents that read each claim in context and quote each source verbatim. Takes a /research Markdown file, a writing Research issue or /research-piece's draft comment. Reports only; never edits the findings."
disable-model-invocation: true
---

Checks every claim in a set of research findings against the source it cites. Each source is read by a **fresh-context sub-agent** on the session's model that never wrote the findings, so a misread, invented or out-of-context claim gets caught rather than trusted.

A checked fact list is what `/review-piece`'s Spec axis treats as closed: a verified source list, or a Research comment's facts outside its `## Unverified` section. That axis checks a Piece against the list; this skill checks the list against its sources.

## 1. Pin the input

The input is one of:

- **A research file**: a Markdown path from `/research`. Read it.
- **A Research issue**, as `<repo> <n>`. Fetch it with `npm run issue:read -- <repo> <n> --body --comments`, state its title, and take the comment that holds the findings. If more than one comment could be the findings, ask which.
- **A draft Research comment**: the `comment.md` and texts folder `/research-piece` hands over before posting. Each source is the saved text its locators name, in that folder.

If the reference is ambiguous, or the issue is a Piece rather than Research, stop and say so.

Done when the findings text is pinned and its source is stated.

## 2. Extract claims and sources

Write a numbered list of **claims** to the scratchpad. A claim is one factual statement in the findings, quoted verbatim, with the source or sources it cites. Then group the claims by source: each source gets its URL or locator and the claims that cite it. A claim citing several sources goes under each.

A claim that cites nothing is not sent to a sub-agent; list it as **uncited** for the report. A Research comment's `## Unverified` section is outside its fact list: extract no claims from it.

Done when every factual statement in the findings is either under a source or uncited.

## 3. Spawn the sub-agents in parallel

One sub-agent per group, on the session's model (no `model` override), all Agent calls issued together in the foreground. Use one group for a short source list; split by source once it runs past about five sources, keeping each source's claims together.

Each prompt gives only that group's sources and claims, never the rest of the findings, and the brief: "Open each source yourself: a saved text by its path, paged per `docs/pdf-pages.md`; a long PDF by downloading it and printing the cited pages per `docs/pdf-pages.md`, deleting the download when the stage ends. For each claim, read the cited range plus one page either side; for a source with no pages, the cited paragraph plus the paragraph before and after it within the same heading. Read further only when the passage depends on text outside that window: a back-reference such as *as noted above*, a term defined elsewhere, a table, or a hedge or condition set up earlier. Then follow the pointer to the text it names, and say what you read. For each claim, return: the claim number; a verdict of **supported**, **partly supported** (only when the claim's meaning differs from the source: a number, a hedge, a scope, an attribution, a location, or **taken out of context**; say exactly what) or **unsupported** (**taken out of context** among its reasons); for taken out of context, what the surrounding text changes; the passage the verdict rests on, quoted verbatim from the source; and its location (section, page or heading). An ellipsis, dropped punctuation or a footnote marker is still supported; note it beside the verdict. Never paraphrase the source in place of a quote. A source you can't open or can't find the passage in, say so and mark its claims **unverified**, never supported. Under 400 words per five claims."

Done when every claim sent out has a verdict or an unverified mark.

## 4. Report

Present one table per source: claim number, claim, verdict, quote, location. A claim under several sources takes its best verdict, and the report says which source carried it. Put unverified and uncited claims in their own list after the tables.

A source is **verified** when every claim it carries is supported. For a `/research` file, only verified sources join the list `/review-piece`'s Spec axis treats as closed. For a Research comment, that list is every fact outside its `## Unverified` section once `/research-piece` has acted on the verdicts, partly supported facts included once rewritten from the reviewer's quote.

End with the counts for each verdict, unverified and uncited included, and the worst claim: unsupported before partly supported before unverified. Do not edit the findings; the developer or the researching agent fixes them, and for a draft comment that is `/research-piece`, which acts on the verdicts by its own steps.
