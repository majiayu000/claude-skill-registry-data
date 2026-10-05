---
name: memory-management
description: Persist and retrieve architectural context, user preferences, and project
  milestones across sessions. Use for crash-safe checkpointing, updating persistent
  memories, and managing context window retention.
argument-hint: <memory action or context to save>
---

<!-- Generated from skills/memory-management.md by tools/generate_integrations.py. Edit the source file, not this one. -->

# Skill: Memory & Context Management

## Purpose
Persist and retrieve important context across sessions, manage conversation state, and leverage memory systems efficiently. _Source: Anthropic (Category H)_

## Tools Required
- Memory CRUD tools (create/update/delete memory) _Source: Cursor (Category H)_
- Todo list tools (todo_write) _Source: Perplexity (Category N)_
- Persistent storage APIs (where available) _Source: Cursor (Category H)_
- Steering/configuration file tools _Source: Kiro (Category H)_

## General Principles
- Save context proactively — context windows are limited _Source: Amp (Category H)_
- Save early, save often — don't wait until end of task _Source: Kiro (Category N)_
- Prefer updating existing memories over creating duplicates _Source: Cursor (Category H)_
- Tag memories for efficient retrieval _Source: Cursor (Category H)_
- Prioritize: user preferences > project decisions > technical context > conversation state _Source: Notion (Category H)_

## Memory Creation (Windsurf pattern)

### What to Save
- User preferences (tone, formatting, tool usage preferences) _Source: OpenAI (Category H)_
- Explicit user requests to remember something _Source: Anthropic (Category H)_
- Important code snippets and project structure _Source: Amp (Category H)_
- Technical stack decisions _Source: Cursor (Category H)_
- Major milestones and feature decisions _Source: Cursor (Category H)_
- Design patterns and architectural choices _Source: Cursor (Category H)_
- Current task state for multi-session work _Source: Kiro (Category N)_

### How to Save
```python
# Create new memory
create_memory(
    Action="create",
    Content="User prefers verbose explanations with code examples",
    Title="User communication preference",
    Tags=["user_preference", "communication"],
    UserTriggered=False  # set True only if user explicitly asked
)

# Update existing memory (find semantically similar first)
create_memory(
    Action="update",
    Id="existing_memory_id",
    Content="Updated preference content",
    Title="Updated title"
)

# Delete incorrect memory
create_memory(
    Action="delete",
    Id="incorrect_memory_id"
)
```
_Source: Windsurf (Category H)_

### When to NOT Save
- Trivial temporary state _Source: Cursor (Category H)_
- Information that will be irrelevant after current task _Source: Cursor (Category H)_
- Content the user explicitly doesn't want saved _Source: Anthropic (Category H)_
- Sensitive/PII data _Source: Kiro (Category G)_

## Task Management (todo_write pattern)
- Use for multi-step tasks to track progress _Source: Perplexity (Category N)_
- Create at start of complex task _Source: Perplexity (Category N)_
- Mark items complete as soon as done (don't batch) _Source: Perplexity (Category N)_
- Keep exactly ONE item `in_progress` at a time _Source: Trae (Category N)_
- Update status in real-time _Source: Trae (Category N)_

```python
todo_write(
    todos=[
        {"content": "Implement user authentication", "status": "completed", "priority": "high"},
        {"content": "Add password validation", "status": "in_progress", "priority": "high"},
        {"content": "Write tests for auth flow", "status": "pending", "priority": "medium"}
    ]
)
```
_Source: Perplexity (Category N)_

## Session Continuation
- When ending a session, produce a structured summary _Source: Kiro (Category N)_
- Include: what was discussed, decisions made, current state, next steps _Source: Kiro (Category N)_
- The summary should be self-contained for next session to pick up _Source: Kiro (Category N)_

## Steering Files (Kiro pattern)
- For persistent behavioral instructions, use steering files _Source: Kiro (Category H)_
- Steering files can be:
  - **Always included** (default) — for universal instructions _Source: Kiro (Category O)_
  - **Conditional** (fileMatch) — triggered when specific files are read _Source: Kiro (Category O)_
  - **Manual** — only when explicitly referenced _Source: Kiro (Category O)_
- Use file references `#[[file:path]]` to include specs into context _Source: Kiro (Category H)_

## Conversation History Awareness
- Be aware of context window limits _Source: OpenAI (Category I)_
- If conversation is long, memory systems help preserve key facts _Source: Anthropic (Category H)_
- Don't repeat information that was already established _Source: Phind (Category B)_
- Refer back to earlier parts of conversation when relevant _Source: Poke (Category H)_
- If context is lost (new session), ask for summary if one wasn't provided _Source: Kiro (Category N)_
