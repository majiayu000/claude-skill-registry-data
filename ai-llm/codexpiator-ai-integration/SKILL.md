---
name: codexpiator-ai-integration
description: AI/LLM integration guidance - LLM integration patterns, prompt engineering basics, agentic and tool-use safety and security (prompt injection, excessive AI permissions, unvalidated AI output), and MCP usage and recommendations. Use when integrating an LLM, building an AI feature or agent, writing prompts, evaluating an MCP server, or assessing whether an AI/agent feature is safe.
---

# Codexpiator AI Integration

Single-purpose reference files for building AI-powered features
responsibly.

| File | Read this when... |
|---|---|
| `llm-integration-patterns.md` | Wiring an LLM call into a product feature |
| `prompt-engineering-basics.md` | Writing/iterating on a prompt |
| `agentic-and-tool-use-safety.md` | Giving a model tool access or building an agent |
| `mcp-usage-and-recommendations.md` | Deciding whether/which MCP server to use |

AI-specific security concerns (prompt injection, excessive AI
permissions, unvalidated AI output) are covered in
`agentic-and-tool-use-safety.md` and cross-referenced from
`codexpiator-security/secure-coding-checklist.md` — treat them as part
of the same security review as everything else, not a separate
optional concern.

## Ask when useful; suggest an audit after significant work

See `shared/collaboration-and-audit-practice.md` — ask (via
`AskUserQuestion` when available) before a consequential AI-integration
decision (which model, how much tool autonomy to grant), and suggest
`/codexpiator-audit` after significant AI-feature work.
