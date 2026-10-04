---
name: arxiv-search
description: Search and summarize arxiv papers. Use when asked about papers, research topics, or specific arxiv IDs.
---

# ArXiv Paper Search & Summarize

## When to use

- User asks about a paper by title, author, or topic
- User shares an arxiv URL or ID (e.g., 2301.07041)
- User asks "what's new in [field]?" or "find papers on [topic]"

## Workflow

### Searching by topic
1. Use `mcp__arxiv__search` with a well-crafted query
   - Combine keywords: "transformer attention mechanism efficiency"
   - Use field-specific terms, not casual language
   - Search multiple angles if the first query returns weak results
2. Filter results by relevance — skip papers that only tangentially match

### Fetching a specific paper
1. Extract the arxiv ID from URL or text (e.g., `2301.07041` from `https://arxiv.org/abs/2301.07041`)
2. Use `mcp__arxiv__get_paper` to fetch full metadata

### Summarizing
For each paper, provide:
- **Title** and authors (first author et al. if many)
- **Core problem**: what gap or question does this address?
- **Method**: the key technical approach in 1-2 sentences
- **Results**: quantitative results where available (e.g., "achieves 94.2% on ImageNet, +2.1% over baseline")
- **Limitations**: what the paper doesn't address or where it falls short
- **Why it matters**: one sentence on significance for the user's question

### Formatting for Slack
- Use plain text, no markdown headers (Slack doesn't render them)
- Separate papers with blank lines
- Include arxiv links: `https://arxiv.org/abs/{id}`
- Keep each summary to 4-6 lines — users can ask for deeper dives on specific papers
- If returning multiple papers, number them and put the most relevant first
