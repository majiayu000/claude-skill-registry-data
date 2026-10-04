---
name: booster-project-memory
description: |
  Использование долгосрочной памяти проекта (project_memory) 
  для сохранения контекста, архитектурных решений и инсайтов между сессиями.
---

# Booster Project Memory

## Цель

`project_memory` позволяет сохранять важную информацию (контекст, архитектурные решения, TO-DO) в `.agents/booster/memory.json`. Это нужно, чтобы агент не "забывал" важные детали при перезапусках и смене сессий.

В Cognitive Runtime добавлены структурированные факты:

- `remember_project_fact(category, fact, confidence, source, repo)`
- `project_memory_recall(query, categories, repo, limit)`

Они живут в том же `memory.json`, но имеют категории, confidence и источник.

## Как использовать

1. **Сохранение (set)**:
   При нахождении важного архитектурного инсайта или зависимости:
   `project_memory(action="set", key="architecture:auth", value="Авторизация использует JWT через кастомный middleware в src/auth.py")`

2. **Чтение (get)**:
   При старте работы (особенно в новом чате):
   `project_memory(action="get", key="architecture:auth")`

3. **Список ключей (list)**:
   Чтобы узнать, какие знания уже сохранены по проекту:
   `project_memory(action="list", key="")`

4. **Структурированный recall перед задачей**:
   Перед изменением кода:
   `project_memory_recall(query="добавить OAuth в auth flow")`

5. **Сохранение проверенного факта**:
   После анализа архитектуры:
   `remember_project_fact(category="architecture", fact="Frontend ходит в backend только через BFF", confidence=0.95, source="repo_map+impact_analysis")`

6. **Удаление (delete) и очистка (clear)**:
   Если информация устарела:
   `project_memory(action="delete", key="architecture:auth")`
   `project_memory(action="clear", key="")` # Очистить всю память

## Антипаттерны

- Не сохраняй огромные куски кода в память (сохраняй выводы и ссылки на файлы).
- Если проект переписывается, обновляй старые записи в памяти.
