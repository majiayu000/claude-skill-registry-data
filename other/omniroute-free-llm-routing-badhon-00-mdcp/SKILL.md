---
name: omniroute-free-llm-routing
description: Route Claude Code and Codex CLI through OmniRoute to Ollama local models and eligible free hosted LLM providers with safe fallback and token-conscious context handling.
---

# OmniRoute Free LLM Routing

Read `MDCP_CONTEXT.md` and `integrations/omniroute/README.md` when available. Follow the complete workflow in `skills/omniroute-free-llm-routing/SKILL.md`.

- Use official OmniRoute CLI commands for Claude Code and Codex CLI.
- Preserve existing client configuration and credentials.
- Never claim hosted free tiers are unlimited or bypass quotas.
- Claude.ai and ChatGPT web are instruction consumers, not automatically local gateway clients.
- Prefer Ollama for local inference; check hardware and model license.
