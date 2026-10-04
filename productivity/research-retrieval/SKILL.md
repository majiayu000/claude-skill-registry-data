---
name: research-retrieval
description: Run evidence-first research, web/source search, Exa search, iterative retrieval, and research-before-coding workflows. Use when prompts ask for current facts, source-backed recommendations, market or company research, code/library discovery, query refinement, cited synthesis, deep research, or the old deep-research/research-ops/exa-search/iterative-retrieval/search-first skills.
---

# Research Retrieval

Use this skill when the answer depends on finding, evaluating, and synthesizing source material.

## Routing

- Read `references/search-first.md` before coding tasks where existing libraries, APIs, or patterns might already solve the problem.
- Read `references/exa-search.md` when Exa MCP is available or the user specifically wants Exa-style neural search.
- Read `references/iterative-retrieval.md` for broad or ambiguous tasks that require progressive query refinement.
- Read `references/deep-research.md` for multi-source research reports.
- Read `references/research-ops.md` for current-state research with explicit evidence handling.

## Workflow

1. Clarify the claim or decision the research must support.
2. Search broadly, then narrow by evidence quality, recency, and source authority.
3. Keep track of source URLs, dates, and uncertainty.
4. Synthesize rather than paste long excerpts.
5. Label inference, speculation, and reported claims distinctly.
6. For coding tasks, prefer primary documentation and actively check whether the proposed tool or API is current.

## Output

Return concise conclusions with citations or source notes, open questions, and the recommended next action.

