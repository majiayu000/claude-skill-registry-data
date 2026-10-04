---
name: web-research
description: "Multi-step web research on a topic: search, filter sources, fetch content, produce a structured report with citations. Trigger on: research, recherchiere, find information about, was weiß man über, look up, investigate, give me an overview of."
user-invocable: true
---

# Web Research

## When to use
- User asks to research a topic, person, technology, or event
- User says "recherchiere", "was weiß man über", "find information about", "give me an overview"
- A single `web_search` would not be enough depth

## Steps

1. **Search** — call `web_search` with the user's topic (5–8 results).
   If the first query yields thin results, try one alternative query.

2. **Filter** — from the results, select the 3–5 most relevant and credible URLs.
   Prefer primary sources, official docs, and established publications.
   Skip social media, paywalled, or clearly low-quality pages.

3. **Fetch** — call `web_fetch` on each selected URL.
   If `web_fetch` fails for a URL, skip it and continue with the others.

4. **Synthesize** — combine the retrieved content into a structured report.
   Do not copy text verbatim; summarize and paraphrase.

5. **Reply** in the same language the user used.

## Output format

**Topic**: <research topic>

**Summary**
3–5 sentences capturing the most important findings.

**Key findings**
- Finding 1 — [Source title](url)
- Finding 2 — [Source title](url)
- Finding 3 — [Source title](url)

**Sources**
1. [Title](url) — one-line description
2. [Title](url) — one-line description
3. [Title](url) — one-line description

## Notes
- Always include source URLs so the user can verify the information.
- If fewer than 2 sources could be fetched, say so and offer to retry with different search terms.
- Do not invent or hallucinate facts; only report what the fetched content contains.
