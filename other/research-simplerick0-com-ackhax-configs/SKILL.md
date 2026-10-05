---
name: research
description: Deep research on a codebase topic using isolated context. Use when asked to investigate, explore, or understand how something works in the codebase without cluttering the main conversation.
---

# Research

Research "$ARGUMENTS" in isolated context.

## Process

1. Use Glob to find relevant files by name patterns
2. Use Grep to search for keywords, function names, references
3. Read key files to understand implementation
4. Trace connections across the codebase

## Output

Provide:
- Key findings with file:line references
- How components connect
- Recommendations or next steps if applicable
