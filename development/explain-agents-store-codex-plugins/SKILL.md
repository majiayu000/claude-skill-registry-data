---
name: explain
description: 'Step-by-step explanation of a file, function, or module with mini-diagram if appropriate Arguments: <file-path|module-path|symbol-name>.'
---

# Explain Code for Beginners

Provide a structured, beginner-friendly explanation. Target: $ARGUMENTS

## Instructions

1. Read the primary skill:
   - `${CLAUDE_PLUGIN_ROOT}/skills/codemap-explain/SKILL.md` — 4-layer explanation model

2. Parse `$ARGUMENTS` to determine scope:
   - If it's a file path → pass the file path to the agent
   - If it's a directory → pass the directory path to the agent
   - If it's a symbol (function/class name) → pass the symbol name to the agent
   - If no argument → ask user what to explain

3. Launch the **architect-explainer** agent with a prompt describing the target and any additional context from the user's message.

The agent applies the 4-layer model (Context → Data Flow → Details → Pitfalls), adjusts depth by scope, and generates mini-diagrams when 3+ components interact.