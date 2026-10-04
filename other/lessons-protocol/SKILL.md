---
name: lessons-protocol
description: Self-Improvement Protocol for reading and writing lessons. Use when starting analysis, after finding bugs, or completing reviews.
user-invocable: false
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


# Self-Improvement Protocol

## Перед началом работы — проверь lessons

1. `serena: list_memories` → прочитай `lessons_*` релевантные текущей задаче
2. Если задача связана с bash/git/mcp/devops/typescript — прочитай `~/.claude/doc/lessons/{stack}.md`
3. Также проверь `known_issues`, `decisions`, `architecture` из Serena если релевантны

**В pipeline:** PipelineMemory автоматически вспоминает релевантные lessons при планировании и дебаге (pgvector + Voyage AI). Ручной recall не нужен — orchestrator делает это за тебя.

## После завершения — запиши lesson (если нашёл повторяющуюся проблему)

- **Project-specific** → `serena: write_memory` с именем `lessons_{область}`
- **Universal** → `~/.claude/doc/lessons/{stack}.md`
- **В pipeline:** orchestrator автоматически сохраняет lessons от debugger и reviewer в PipelineMemory
- **Формат:**
  ```
  ## Название проблемы
  - **Mistake:** Что пошло не так
  - **Root Cause:** Почему
  - **Rule:** Что делать чтобы избежать
  - **Date:** YYYY-MM-DD
  ```
