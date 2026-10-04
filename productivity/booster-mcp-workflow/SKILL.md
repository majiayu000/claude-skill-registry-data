---
name: booster-mcp-workflow
description: |
  Управление репозиториями, контекстом и артефактами через Booster MCP.
  Используй при начале работы с MCP-сервером Booster или если RepoMap/Code City недоступны.
---

# Booster MCP Workflow

## Цель

Безопасно подключить репозиторий к Booster MCP, получить актуальный контекст и убедиться, что артефакты анализа доступны агенту.

## Базовый Цикл

1. Проверь встроенные навыки через `list_agent_skills()`.
2. Для нового или большого локального репозитория сначала запусти из его корня `booster expand --profile balanced`. Это создаёт ограниченный scope и не загружает embedding-модель.
3. Прочитай `.agents/booster/scan_report.json`. Если достигнуты limits, реши осознанно: сохранить быстрый scope или повторить `booster expand --profile deep` перед индексацией.
4. Добавь проект: `add_repo("<absolute_repo_path>")`. MCP использует сохранённый `scan_config.json` и возвращает `job_id`.
5. Проверь job через `index_status(job_id="...")`; для bounded ожидания используй `wait_until_ready()`, а не долгий MCP request.
6. Проверь результаты индексации и пути к артефактам: `repo_stats()` и `get_repo_artifacts()`.
7. Получи сжатую структуру проекта: `inject_context()` или `get_repo_map()`.
8. Для известных символов, API и mixed-запросов используй `hybrid_search()`; для чисто смыслового поиска используй `semantic_search()`.
9. При необходимости получи рекомендации по актуальной документации: `fetch_stack_docs()`.
10. Выбери специализированный skill для дальнейшей работы.
11. Перед финальным ответом вызови `booster.task_complete(task_id="<task-id>")`: Booster поставит финальный reindex и сохранит commit-bound snapshot.

```text
booster expand --profile balanced
add_repo("D:\\workSpace\\project")
index_status(repo_path="D:\\workSpace\\project")
get_repo_artifacts()
inject_context(include_map=True, include_stack=True, include_conventions=True)
repo_stats()
hybrid_search("authenticate_user JWT")
fetch_stack_docs()
booster.task_complete(task_id="task-123")
```

## Проверка Артефактов

`get_repo_artifacts()` возвращает состояние канонических файлов:

- `.agents/booster/repo_map.md`
- `.agents/booster/repo_map_architecture.md`
- `.agents/booster/repo_map_symbols.md`
- `.agents/booster/index_health.json`
- `.agents/booster/code_city.html`
- `.agents/booster/scan_config.json`
- `.agents/booster/scan_report.json`
- `.agents/booster/latest.json`
- `.agents/booster/snapshots/<commit>-<state>-<digest>/`

`scan_report.json` является gate для дальнейшего алгоритма. Если он сообщает о `max_files`, `max_depth`, `max_total_bytes` или `max_directories`, не запускай `reindex_repo()` вслепую: сначала выбери подходящий профиль или явные лимиты через `booster expand`.

Если architecture map отсутствует:

1. Вызови `get_repo_map()` - инструмент сформирует bounded architecture map и сохранит её в артефактах.
2. Повтори `get_repo_artifacts()`.
3. Если карта всё ещё пуста, вызови `reindex_repo("<absolute_repo_path>")` и повтори проверку.

```text
get_repo_artifacts()
get_repo_map()
get_repo_artifacts()
```

## Маршрутизация Работы

- Новый или незнакомый проект: `booster-onboard`.
- Инъекция карты, стека и конвенций в контекст: `booster-context-inject`.
- Архитектурный обзор: `booster-architecture-map` и `booster-deep-dive`.
- Ошибка, stack trace или нестабильное поведение: `booster-bug-hunt`.
- Новая возможность: `booster-feature-add`.
- Рефакторинг без изменения поведения: `booster-refactor`.
- Code review: `booster-review`.
- Сложный граф вызовов: `booster-flipchart`.
- Долгосрочные выводы: `booster-project-memory`.

## Ограничения

- Передавай абсолютный путь в `add_repo()` и `reindex_repo()`.
- Не читай большой репозиторий подряд, пока не получены RepoMap и статистика.
- Не меняй `scan_config.json` вручную: обновляй scope через `booster expand`, чтобы report и конфигурация оставались согласованными.
- Не редактируй файлы в `.agents/booster` вручную: они являются автоматически генерируемыми артефактами.
- Для обновления уже добавленного проекта используй `reindex_repo()`, а не повторный `add_repo()`.
- `add_repo()` idempotent и сохраняет binding между MCP-процессами; не вызывай его повторно только для обновления индекса.
- Для изменения состава большого репозитория учитывай `stale=true` и дождись новой generation через `index_status`.
- После завершения задачи обязательно вызывай `booster.task_complete()`. Предыдущие commit-bound snapshots не удаляй.
