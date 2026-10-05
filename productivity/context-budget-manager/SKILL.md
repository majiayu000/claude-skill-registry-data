---
name: context-budget-manager
description: Use this skill to keep value-investing research runs token-efficient through routing, progressive disclosure, and context packet selection. Trigger when reports become long, many files are loaded, token usage is high, or a new sub-skill/reference is added.
---

# Context Budget Manager Skill

## Purpose

Keep the value investing research system from becoming a token-heavy monolith.

## When to Activate

Activate when:

- A skill or prompt becomes too long
- A research run loads many documents
- The user asks to reduce token usage
- A full research report is requested
- A new sub-skill or reference file is added

## Workflow

1. Identify task depth: L0, L1, L2, L3, or L4.
2. Route to the minimal context packet.
3. Estimate context size.
4. Remove examples and long references unless explicitly needed.
5. Prefer scripts for calculation.
6. Prefer data packets over full documents.
7. Log token usage and cache-hit rate when available.
8. If over budget, summarize or split before continuing.

## Output

Return:

- Selected files
- Estimated token count
- Removed or deferred files
- Risk of under-context
- Recommended next context packet
