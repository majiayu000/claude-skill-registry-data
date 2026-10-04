---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Автоматизированный пайплайн разработки программного обеспечения. Сканирует проекты, расставляет приоритеты задач, анализирует код и оркеструет циклы разработки. Ноль зависимостей (только стандартная библиотека Python).

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="dev-soft-agent banner">

> **Русский** — Официальная русская версия `dev-soft-agent`.


# Dev Soft Agent (Русский)

Автоматизированный пайплайн разработки программного обеспечения. Извлечен из агента ATI компании BACH,
работает полностью автономно с использованием только стандартной библиотеки Python.

## Компоненты

```
scripts/
  config.py              Configuration (scan folders, naming prefixes, weights)
  project_manager.py     Project scan + classification by naming convention
  task_engine.py          TASKS.txt parser + code scanner (TODO/FIXME)
  code_analyzer.py       Static analysis (LOC, imports, classes, functions)
  dev_loop.py            Orchestrator (DevLoop)
  policies/
    naming.py            snake_case / PascalCase / SCREAMING_SNAKE validation
    encoding.py          UTF-8 enforcement + BOM detection
    paths.py             Hardcoded path detection
  prompt_templates/
    task_prompt.txt      LLM prompt for task processing
    review_prompt.txt    LLM prompt for code review
    analysis_prompt.txt  LLM prompt for project analysis
```

## Использование в качестве библиотеки Python

```python
from scripts.dev_loop import DevLoop
from scripts.config import Config

config = Config()
loop = DevLoop(config)

# Scan projects (Deutsch)
projects = loop.scan_projects()

# Select project (weighted random selection by naming convention) (Deutsch)
project = loop.select_project()

# Analyze code (Deutsch)
analysis = loop.analyze_project()
print(f"{analysis.total_loc} LOC, {analysis.todo_count} TODOs")

# Load and prioritize tasks (Deutsch)
tasks = loop.get_tasks()
for task in tasks:
    print(f"[{task.task_type.name}] {task.description} (Prio: {task.priority})")

# Complete dev session (Deutsch)
result = loop.run_session()
loop.save_session()
```

## Использование в качестве CLI

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /path/to/project
python -m devSoftAgent tasks /path/to/project
python -m devSoftAgent session --project my-project
python -m devSoftAgent status
```

## Соглашение об именовании (классификация проектов)

Проекты классифицируются на основе имени их папки:

| Префикс | Метка | Вес | Значение |
|--------|-------|--------|---------|
| `RDY` | Ready | 1.0 | Наивысший приоритет |
| `RDY_FAST` | Fast Ready | 0.5 | Быстрое выполнение |
| `FAST` | Fast | 0.33 | Небольшая задача |
| `DEV` | Development | 0.17 | В разработке |
| `REL` | Released | 0.0 | Готово, работа не требуется |
| `ARC` | Archived | 0.0 | В архиве |

Вес определяет вероятность при случайном выборе.

## Формат TASKS.txt

```markdown
# TASKS - ProjectName (Deutsch)
# As of: 2026-03-12 (Deutsch)

## OPEN
- [ ] [BUG] Description of the bug
- [ ] [FEATURE] New feature

## IN PROGRESS
- [-] [REFACTOR] Code restructuring

## DONE
- [x] [BUG] Fixed bug -- DONE 2026-03-01
```

## Политики

Политики качества, которые могут автоматически проверяться в коде:

- **NamingPolicy:** snake_case для модулей/функций, PascalCase для классов
- **EncodingPolicy:** Принудительное использование UTF-8, обнаружение BOM, флагирование CRLF
- **PathPolicy:** Обнаружение и отчётность по захардкоженным абсолютным путям

## Журнал изменений

### 0.1.0 (2026-03-12)
- Миграция из MODULAR_AGENTS/devSoftAgent в библиотеку навыков (skill library)
- Сканер проектов, движок задач, анализатор кода, DevLoop
- 3 политики (именование, кодировка, пути)
- 3 шаблона промптов (задача, ревью, анализ)
