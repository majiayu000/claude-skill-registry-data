---
name: vault-synthesize
description: Synthesize or append structured wiki notes from dashboard signals into brain/ or global/ per capture-llm-wiki schema with citations. Use when user wants LLM to compound vault knowledge from USASpending context — human review recommended.
metadata:
  title: Vault Synthesize
  category: vault-admin
  status: active
  origin: karpathy-llm-wiki
  invoke: agent
  runtime: tools
  supports_llm: true
  max_turns: 6
  schema: data/knowledge/schema/capture-llm-wiki.md
---

# Vault Synthesize

Karpathy pattern — LLM is programmer, wiki is codebase. Never invent award_keys; cite app data or MCP results.

## Capture-insights adapter (no KG)

- **Run** from Agent Skills or chat ("synthesize vault from pursuit").
- Reads pursuit Studio markdown + DuckDB signals for the active Pipeline row.
- Writes `global/global_wiki/capture/synthesis_<slug>.md` — human review before promoting to brain/.
- Enable smart model in chat/UI for optional LLM synthesis section.