---
name: multi-model-review
description: Multi-model ensemble review convergence loop and test gates across Gemini, Claude, and Copilot.
---

# Multi-Model Review Skill

## Operating Modes
1. **Quick Mode:** Fast staged diff review using clean-context subagents.
2. **Full Mode:** Multi-model review running across available providers (Gemini 3 Flash/Pro, Claude Sonnet, Copilot Auto) with independent review lenses.
3. **Convergence Loop:** Iteratively applies fixes via a merge agent until only suggestions remain or blocking findings are resolved.
