---
name: research
description: Source-grounded web research for multi-source comparisons, landscape surveys, academic, company, or market research, and decisions that depend on current external evidence. Simple lookups and known-URL reading use ordinary web tools.
compatibility: Requires pi-web-access tools and the lazy Exa server behind the mcp gateway.
---

# Research

Own the evidence, not the deliverable. The user's request or another active workflow owns the output format.

Before substantive research, state the question and evidence approach in one or two lines, then proceed without waiting. Scale the work to uncertainty, consequence, and what the answer will decide.

## Route

Choose the narrowest path that can answer the question.

- Use `fetch_content` for known URLs, whole-page reading, and pasted-link batches.
- For a current third-party contract, load `read-the-damn-docs` and follow its evidence order.
- Use `web_search` for broad current coverage, ordinary external research, and search-grounded synthesis.
- Use Exa MCP basic search for semantic discovery, unfamiliar landscapes, niche sources, similar systems, papers, company or market discovery, implementation examples, and finding the right vocabulary.
- Use Exa MCP advanced search when the task benefits from publication, company, people, news, personal-site, or financial-report categories; precise domain or date filters; freshness controls; focused highlights; or subpage discovery.
- Use Exa MCP Agent when the work is genuinely multi-hop, needs deep research, requires structured output, enrichment, or list building, or would otherwise need several dependent searches and synthesis passes.
- Use `source_check` and direct source passages for mutable, disputed, surprising, or consequential claims.

Use both broad `web_search` and Exa when source diversity could change the conclusion. Use Exa Agent only when its delegated research loop earns the added latency.

## Exa through MCP

Exa tools stay behind the lazy `mcp` gateway. Connect or search the `exa` server when needed. Use only:

- `exa_web_search_exa`
- `exa_web_search_advanced_exa`
- `exa_web_fetch_exa`
- `exa_agent_run`

Use `mcp` tool discovery or description before the first call when the current schema is not visible. Exa owns those schemas, so this skill does not restate their parameters.

For advanced search, bound the result count and extracted content. When the described schema exposes `textMaxCharacters` and `highlightsMaxCharacters`, set both; start with 1,000 to 3,000 characters per result. Prefer focused highlights over full text and increase the bounds only when the first result is insufficient. In live testing, three unbounded results produced more than 140,000 characters.

For Exa Agent, choose effort adaptively. Use low effort for bounded tasks, medium for normal substantive research, and higher effort only when completeness is worth the additional time. Treat Agent output and field-level grounding as evidence to inspect, not a final verification result.

## Discover

Split a broad question into distinct search angles only when one query cannot cover it. Vary the question, source type, or opposing hypothesis instead of paraphrasing one query. Prefer primary-source domains when the source class is known.

Treat search summaries and generated structured output as leads. Evidence comes from the underlying sources.

## Read

Read the strongest sources bearing on each material part of the question. Prefer primary documentation, source code, changelogs, papers, standards, filings, and first-party statements for factual claims. Use independent analysis for comparisons, adoption, criticism, and real-world outcomes.

Use `get_search_content` with `findText` for relevant passages in stored results. Use `fetch_content` or Exa fetch when a selected source needs direct inspection. Trace consequential secondary claims back to their original source.

Keep different publishers, organizations, studies, actors, and repeated reports of one event separate. Same-publisher repetition is one source, not corroboration.

## Verify

For every decision-driving claim, identify the supporting or contradicting passage and its publication date when freshness matters. Search for evidence that would falsify the emerging conclusion. Separate observed facts from inference and unresolved uncertainty.

Use `source_check` with fetched content when exact passage-level support matters. Verify stale or time-sensitive details outside Exa deep or Agent output before relying on them.

## Stop

Stop when every material part of the answer has direct support, meaningful disagreement has been addressed, and another search is unlikely to change the conclusion. Source counts are evidence diagnostics, not quotas.

## Hand off evidence

Supply the gathered evidence, citations, disagreements, and limits in the shape required by the active deliverable. Research can feed a normal answer, report, HTML explainer, implementation, or other artifact without imposing research-specific presentation.
