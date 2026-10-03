---
name: vault-lint
description: Lint native Knowledge Vault markdown against capture-llm-wiki schema — frontmatter, wikilinks, citation hygiene. Use when user asks to health-check the vault or before bulk LLM synthesis. Karpathy LLM wiki maintenance skill.
metadata:
  title: Vault Lint
  category: vault-admin
  status: active
  origin: karpathy-llm-wiki
  invoke: agent
  runtime: legacy
  supports_llm: false
  schema: data/knowledge/schema/capture-llm-wiki.md
---

# Vault Lint

Agent admin task. **Run** from Agent Skills or chat ("lint vault"). Scans native `data/knowledge/` markdown against capture-llm-wiki schema — report only, no KG. Writes `global/global_wiki/capture/vault_lint_report.md`.