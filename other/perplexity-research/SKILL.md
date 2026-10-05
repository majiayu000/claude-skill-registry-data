---
name: perplexity-research
description: Deep Research mode through Perplexity MCP. Use only for broad, important questions where higher cost and longer runtime are acceptable.
---

# Perplexity Research

Use this skill for Deep Research mode through Perplexity MCP.

Observed billing snapshot after skill tests cost `$2.52`; most of it came from `sonar-deep-research`: 478,195 reasoning tokens (`$1.43`), 117 search queries (`$0.59`), 67,825 citation tokens (`$0.14`), and 15,158 output tokens (`$0.12`).

Rules:

- Use only the `perplexity_research` MCP tool from the `perplexity` server.
- Do not silently replace it with `perplexity_search`, `perplexity_ask`, or `perplexity_reason`.
- Keep the question focused before running the tool.
- Return a practical summary with the strongest citations.
- Mention that this mode is slower and more expensive than simple search when relevant.
