---
name: codex-chat
description: Use when user wants to ask Codex a question, get a second opinion, or consult with gpt-5.2. Triggers on phrases like "ask codex", "codex opinion", "what does codex think".
---

# Codex Chat Skill

General consultation with Codex (gpt-5.2) for questions, opinions, and analysis.

## When to Use

- User asks for Codex's opinion
- User wants a second AI perspective
- User explicitly mentions "codex" or "gpt-5.2"
- User asks for consultation on a technical question

## Reasoning Level

Default: **high**

If user mentions "quick" or "brief", use medium.
If user mentions "deep" or "thorough", use xhigh.

## Execution

1. Identify the question or topic
2. Gather relevant context (read files if needed)
3. Run: `codex exec -c model_reasoning_effort="high" "<question with context>"`
4. Return Codex's response with the session ID

## Response Format

```
**Codex Response:**
[Codex's analysis]

**Session ID:** [id] (use `/codex-resume` to continue)
```
