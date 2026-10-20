---
name: deep-research
description: "MUST read before the first search/fetch. Research a question across multiple sources and synthesize the findings into a clear, readable answer or report. Use whenever answering requires looking up information, not only when the user explicitly asks for in-depth research. Skip it only when no searching is needed."
compatibility: opencode
---

# Deep Research

## When to Use

- When the user requests in-depth or comprehensive research
- When the task requires gathering information, checking facts, and synthesizing findings across multiple sources
- When the deliverable is an in-depth research report grounded in credible sources

## Deep Research Best Practices

- Research the material dimensions needed to answer the user's question, respecting any scope or budget they specify
- When the user requests in-depth or comprehensive research, escalate the intensity of search and analysis
- Assume no prior knowledge and start by searching for definitions and basic background information
- Start with queries that can retrieve broader results, rather than using more precise queries
- MUST open and read multiple relevant URLs from search results using browser tools to gather diverse perspectives
- DO NOT rely solely on search result snippets as they are often incomplete; MUST follow up by navigating to the source URLs using browser tools
- Use follow-up searches to resolve specific gaps or contradictions that could materially change the answer. Stop when these are resolved or the necessary evidence is clearly unavailable; do not keep searching merely for reassurance
- Check source meaning, numerical units, and comparison baselines when first gathering evidence. Record support alongside the source URL and attach citations as you write, so correctness is built into the work
- MUST proactively save findings and URLs from search and browsing into files as they emerge, to prevent information loss
- Write a finished, readable report from the gathered evidence on the first writing pass; never deliver raw research notes as the final result

## Parallel Processing Best Practices

- When a step or subtask involves performing similar operations on 5 or more independent items, consider parallel processing
- Use the `agent` tool for parallel processing of subtasks
- Research agents own verification of their assigned facts. Synthesis should reuse their cited evidence; do not automatically add review agents or repeat their research

## Writing the Final Report

### Content and Style

- MUST start directly with useful, concrete content that answers the user's question. Do not add a separate opening summary, preamble, or introductory heading unless explicitly requested.
- Make every paragraph serve the user's actual purpose. Do not invent their role or intended use, or turn an informational request into implementation plans or action advice.
- Use a natural, approachable voice and plain, direct words. Keep the reasoning clear and coherent. Avoid academic or bureaucratic phrasing unless requested. Do not invent jargon or use language merely to sound professional.
- Use short, connected paragraphs that are comfortable to read on a phone. Each paragraph should develop one main point. Split long passages at natural shifts in thought; avoid both dense text blocks and choppy strings of one-sentence paragraphs.
- MUST keep syntax and reasoning unnested. Avoid clauses embedded inside other clauses and stacked conditions within a sentence. Keep each sentence focused on one main point, present one reasoning step at a time, and make causal and conditional relationships explicit.
- MUST minimize parallel enumeration, noun stacking, and rhetorical parallelism. Use Chinese "、" and enumeration commas sparingly. Unpack distinct ideas and explain their relationships; replacing punctuation with conjunctions is not enough.
- MUST avoid unnecessary metaphors and analogies. Explain literally by default. Use an analogy only when requested or clearly helpful; retain the actual explanation and state the analogy's limits. Never substitute it for evidence or reasoning.
- Keep the structure simple. Use headings only when they help navigation and identify a concrete topic, question, or finding. MUST NOT add executive summaries, conceptual primers, research-method or research-boundary sections unless explicitly requested, including renamed equivalents. Avoid generic section labels, repeated summaries, and unnecessary closing sections. Keep References.
- Explain through relevant details and concrete examples. Include technical terminology and mechanisms only when needed for the user's request. Explain necessary terms and unfamiliar abbreviations where they first matter.
- Omit unhelpful evidence-boundary discussions, conceptual distinctions, and process narration unless requested. Put material uncertainty and limitations beside the affected claim.
- Provide enough information and explanation to fully serve the request, without imposing a word-count target unless the user specifies one. Remove repetition and irrelevant expansion while giving useful content the space it needs.

### Format and References

- Default to GitHub-flavored Markdown. Use bold sparingly and avoid unnecessary emoji.
- MUST avoid excessive bullet points; write explanations in full sentences and paragraphs. Reserve brief lists for genuine sets or steps; avoid unnecessary nesting. MUST NOT use tables unless explicitly requested; then use concise Markdown pipe tables, never HTML tables.
- Cite sourced factual claims and data near the relevant text as `[1]`. End with a **References** section, using exactly `[1]: https://example.com "Descriptive source title"`. Every definition requires a double-quoted title; reuse the same numeric ID for the same source.
- Separate multiple citations with spaces: `[1] [2]`, never `[1][2]`. Do not use bare-URL reference entries, alias IDs such as `r1`, forms such as `[1][r1]`, nested links, or HTML anchors. Every citation must match a definition and support its associated claim.
- Attribute direct quotations and use blockquotes for quoted passages or cited definitions. Do not present paraphrases as quotations. Use inline hyperlinks for direct access to websites and resources.
- Include charts or images only when useful. Save visualizations as image files before embedding them with Markdown image syntax.
- Default author: **Manus AI**, unless specified otherwise. Do not convert to PDF unless explicitly requested.

### Delivery

Write in final form with citations from the start and deliver once the question is answered without known material errors. Default to no post-draft review or cross-review. Only revisit a concrete issue that could materially change the answer; normally resolve it in one targeted pass, with two passes total as the hard maximum across the lead and all agents. Reuse existing evidence and correct only affected passages, then deliver without another check or full rewrite. If support remains insufficient, qualify or omit the claim. Do not create standalone verification logs or validation scripts for ordinary reports. Keep accompanying messages brief and link files directly.
