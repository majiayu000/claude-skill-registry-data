---
name: web-search
description: Search the web for recent information. Use when asked about recent events, docs, or blog posts.
---

# Web Search

## When to use

- User asks about recent events, releases, or news
- User asks "what's the latest on [topic]?"
- User needs documentation, blog posts, or tutorials
- User asks about something that may have changed after your training cutoff

## Tools

### WebSearch — broad discovery
Use for open-ended queries where you don't know the exact source:
- "latest PyTorch release features"
- "state of the art object detection 2026"
- "CUDA 13 breaking changes"

### WebFetch — read a specific page
Use when you have a URL (from search results or from the user):
- Reading a specific blog post or documentation page
- Following up on a search result for more detail

## Workflow

1. **Search first** with WebSearch using specific, targeted queries
   - Bad: "AI stuff" → Good: "diffusion model architecture improvements 2026"
   - If the first query is too broad, refine with more specific terms
2. **Read the most relevant results** with WebFetch to get details
3. **Synthesize** — don't just dump search results, answer the question
4. **Cite sources** — always include URLs so users can read the originals

## Formatting for Slack

- Answer the question first, then provide supporting details
- Include source URLs inline: "According to [source](url), ..."
- If multiple sources disagree, note the discrepancy
- Keep it concise — summarize rather than quoting paragraphs
- Distinguish between confirmed facts and preliminary/unverified information
