---
name: deep-code-enrichment
description: Guide for running deep code scanning with LLM-generated symbol descriptions.
compatibility: opencode
metadata:
  audience: agents
  purpose: code-enrichment
---
## Workflow

1. Run `hero scan --code` first to ensure the code index is current.
2. Call `hero_code` with `action: unenriched` to get a batch of symbols needing descriptions.
3. For each symbol, read the source context and write a concise one-line description of what it does.
4. Call `hero_enrich` with the descriptions as a JSON array.
5. Repeat steps 2-4 until no more unenriched symbols are returned.

## Description Guidelines

- One sentence, starts with a verb (e.g. "Handles incoming MCP tool calls and dispatches to handlers")
- Focus on what the symbol DOES, not its signature
- Be specific to the codebase, not generic
- For types/structs: describe what they represent and their role
- For functions: describe the primary behavior and key side effects
- Skip trivial getters/setters — describe the business purpose instead
