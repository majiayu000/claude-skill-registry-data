---
name: vault-index-rebuild
description: Rebuild Knowledge Vault index.md from disk truth per capture-llm-wiki schema. Use when vault structure drifted or after bulk ingest of pursuit folders. Karpathy LLM wiki maintenance skill.
metadata:
  title: Vault Index Rebuild
  category: vault-admin
  status: active
  origin: karpathy-llm-wiki
  invoke: agent
  runtime: legacy
  supports_llm: true
  max_turns: 2
  schema: data/knowledge/schema/capture-llm-wiki.md
---

# Vault Index Rebuild

Updates `data/knowledge/index.md` only. Atomic — do not merge with vault-synthesize in one run.